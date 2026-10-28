# Error handling

## Contents
- Try / Catch / Finally layout
- Getting the error out of `Try`
- Run URL for notifications
- Run-after for a single action
- Retry policies
- Custom retry loop
- Validate before acting
- Central error logging
- Desktop flows

## Try / Catch / Finally layout

```
Initialize variable - vErrorMessage (String, empty)        ← top level, before Try
Scope - Try
   └─ the actual work
Scope - Catch          run after Try: has failed, has timed out
   ├─ Filter array - failed actions in Try                 (see next section)
   ├─ Set variable - vErrorMessage                          ← first, so it's set even if logging fails
   ├─ Run a Child Flow - Log Error  /  Post message - Teams
   └─ (agent flow) Respond to the agent - success false    ← see agent-flow-integration.md
Scope - Finally        run after Catch: is successful, has failed, is skipped, has timed out
   └─ cleanup
Condition - failed?    expression: not(empty(variables('vErrorMessage')))
   └─ yes: Terminate - Failed, message: variables('vErrorMessage')
```

Why the final Condition: once Catch handles the error the run reports **Succeeded**, which hides failures from run history filters and monitoring. Terminate (Failed) restores the correct status. Terminate can't be placed inside Apply to each or Do until, and nothing after it runs - so not inside Catch when Finally must still run.

## Getting the error out of `Try`

`result('Try')` returns an array with one object per **top-level** action in the Scope (`name`, `status`, `code`, `error`, `outputs`, …). Actions nested in a Condition or loop inside Try show up only as their container. Keep risky actions at the top level of Try, or wrap them in their own Scope.

There is no inline filter in WDL, so use the action:

```
Filter array - failed actions in Try
  From: result('Try')
  Condition (advanced): @or(equals(item()?['status'], 'Failed'), equals(item()?['status'], 'TimedOut'))
```

Message - connectors put it in different places, so coalesce:

```
coalesce(
  first(body('Filter_array_-_failed_actions_in_Try'))?['outputs']?['body']?['error']?['message'],
  first(body('Filter_array_-_failed_actions_in_Try'))?['outputs']?['body']?['message'],
  first(body('Filter_array_-_failed_actions_in_Try'))?['error']?['message'],
  'Unknown error')
```

Failed action name: `first(body('Filter_array_-_failed_actions_in_Try'))?['name']`.
For one specific action: `actions('HTTP_-_get_order_details')?['outputs']?['body']`.

## Run URL for notifications

Include it in every error notification:

```
concat('https://make.powerautomate.com/environments/', workflow()?['tags']?['environmentName'], '/flows/', workflow()?['name'], '/runs/', workflow()?['run']?['name'])
```

## Run-after for a single action

For an action allowed to fail (e.g. delete a file that may be gone): set the next action's run-after to *is successful, has failed*. Only do this for expected failures; blanket run-after hides real problems.

For a specific fallback: add a parallel branch after the risky action with run-after *has failed* only.

## Retry policies

Action → Settings → Retry policy. Retries only on 408, 429, 5xx and connection errors - never on other 4xx.

| Policy | Use for |
|---|---|
| Default (exponential, 4 retries) | Most actions |
| None | Non-idempotent POSTs (creating records) where a retry after a timeout may create duplicates; also when a custom retry loop handles it |
| Exponential, custom | Known-flaky API needing more attempts |
| Fixed interval | APIs with a known rate window |

## Custom retry loop

Only for non-transient "not ready yet" cases (404 until a record exists, 409 lock). Transient errors are the retry policy's job.

```
Initialize variable - vAttempt (Integer, 0)       ← top level
Initialize variable - vDone (Boolean, false)       ← top level
Do until - retry API call                          Count 10, Timeout PT15M
   condition (advanced): @or(variables('vDone'), greaterOrEquals(variables('vAttempt'), 5))
   ├─ HTTP - get order details                     retry policy: None
   └─ Condition - call succeeded?                  run after HTTP: is successful, has failed, has timed out
        expression: equals(actions('HTTP_-_get_order_details')?['status'], 'Succeeded')
        yes: Set variable - vDone = true
        no:  Increment variable - vAttempt
             Delay - count: mul(variables('vAttempt'), 10), unit: Second
After the loop: Condition on vDone → no: set vErrorMessage, fail explicitly
```

Checking `actions(...)?['status']` instead of `statusCode` also handles timeouts, where there is no status code.

## Validate before acting

At the top of Try, for inputs from forms, HTTP callers or agents:

```
Compose - validation errors
  (build a string listing problems, or use a Condition per required field)
Condition - input valid?
  no: set vErrorMessage (→ Catch-like path), respond with a clear message, Terminate Failed
```

Bad input then never reaches downstream systems, and the caller (or agent) gets a message it can relay.

## Central error logging

Build once per environment as a child flow `Log Error (child flow)` with inputs: flow name, run URL, action name, error message, severity, context JSON. It writes a row to a SharePoint list or Dataverse table and posts high severity to a Teams channel. Every Catch calls it. Baseline for client work: this log + Teams channel + a monthly review of the log.

## Desktop flows

Desktop flows have per-action *On error* settings (continue, retry, run subflow, throw). Throw to the orchestrating cloud flow so its Catch reports it.
