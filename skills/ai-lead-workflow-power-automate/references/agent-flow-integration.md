# Flows called by Copilot Studio agents

The flow is the deterministic action layer under a non-deterministic orchestrator. The orchestrator picks the flow from its name and description, fills inputs from the conversation (or asks the user), calls it, and phrases an answer from the outputs. The agent side (topics, instructions, knowledge) is built in Copilot Studio and is outside this skill.

## Contents
- Requirements checklist
- Name and description
- Inputs
- Outputs
- Validation and type coercion
- Error responses
- Long-running work
- Confirmation before destructive actions
- Credentials and permissions
- Testing
- Common failures

## Requirements checklist

```
Agent-called flow:
- [ ] Trigger: When an agent calls the flow
- [ ] Response: Respond to the agent - reached on EVERY path (success, validation failure, Catch)
- [ ] Every Respond action returns the same set of outputs
- [ ] Response within 100 seconds; longer work after the Respond action
- [ ] Respond to the agent → Settings → Networking → Asynchronous response: Off
- [ ] Flow stored in a solution in the same environment as the agent
- [ ] Inputs and outputs have descriptive names and descriptions with examples
- [ ] Inputs validated and coerced at the top
```

## Name and description

- Name: plain verb-noun the orchestrator can match: `Create service request`, `Get order status`.
- Description (two sentences): what it does + when to use it. "Creates a facilities service request for the signed-in user. Use when the user reports a building or workplace problem."
- Two flows with overlapping descriptions → the orchestrator picks inconsistently. Make the *when* part mutually exclusive.

## Inputs

- Name in natural language ("caller email"), never `param1`; use the agent's conversation language for names and descriptions.
- Description with an example: "Email address of the person reporting the issue, e.g. jan.jansen@gemeente.nl". The orchestrator uses name + description to ask the user for missing values - a sloppy description produces a sloppy question.
- Keep to the simple types the trigger offers (text, number, yes/no). Pass lists or structures as text containing JSON and `json()` it in the flow.
- Make inputs optional only when the flow has a real default; optional inputs often arrive as `''`.

## Outputs

- Flat, named outputs, not one prose message: `success`, `incidentNumber`, `incidentUrl`, `status`, `assignedTo`, `errorMessage`.
- The orchestrator writes the sentence; outputs carry facts. A prose output tends to be quoted verbatim or paraphrased oddly.
- Human-readable status (`"Open"`), not only codes.
- Include URLs to records - the agent shows them as links.
- Lists: return the top 5–10 as a JSON text output plus `totalCount`; hundreds of rows degrade answers and slow the response.
- No secrets, internal IDs from other systems, or debug data.

## Validation and type coercion

Coerce in the Initialize variable actions (top level), validate as the first step inside `Try` (same layout as error-handling.md):

```
Initialize variable - vAmount (Integer): if(empty(triggerBody()?['number']), 0, int(triggerBody()?['number']))
Initialize variable - vEmail (String):   toLower(trim(coalesce(triggerBody()?['text'], '')))
Scope - Try
   Condition - input valid?   e.g. and(contains(variables('vEmail'), '@'), greater(variables('vAmount'), 0))
     no → Respond to the agent (success false, errorType INVALID_INPUT, …) → Terminate Failed
   … main work at the top level of Try (not inside the Condition's yes-branch)
```

Check the real input keys in the trigger's Peek code: designer inputs are stored as `text`, `text_1`, `number` etc. - reference them by those keys, not by display name.

## Error responses

Because every Respond action must have the same outputs, define one output contract and fill it on every path:

| Output | Success | Failure |
|---|---|---|
| `success` | true | false |
| `errorType` | empty | `INVALID_INPUT` / `NOT_FOUND` / `SYSTEM_ERROR` |
| `errorMessage` | empty | Human-readable reason |
| `suggestedAction` | empty | "Check the incident number or search by caller." |
| data fields | filled | empty |

In Catch: set `vErrorMessage`, log, *Respond to the agent* with `success` false. The Terminate Failed comes from the Condition after `Finally` (error-handling.md layout) - the agent already has its answer; the run still shows as failed for monitoring. On failure paths fill data outputs with literal `''`, never with outputs of actions that may not have run.

## Long-running work

The Respond action must run within 100 seconds, while a synchronous HTTP action may legitimately take up to 120 seconds (its Timeout setting only bounds the asynchronous pattern). If the API can be slow, don't wait for it before responding. For longer work:
- Respond early with `trackingId` and `status: "Started"`, continue after the Respond action (up to the 30-day run limit), write the result to a table.
- A second flow `Get request status` takes the tracking ID and returns the current status.

## Confirmation before destructive actions

- Simple: the agent/topic asks the user to confirm before calling the flow; the flow assumes confirmation happened.
- With preview: a `Prepare …` flow returns what will change ("47 records") and a token; an `Execute …` flow takes the token. Use when the impact must be computed server-side.

## Credentials and permissions

The flow's actions run with the connections configured in the flow (maker or service account), not with the chatting user's permissions. If the action must respect the user's rights, pass the user's identity as an input (from the agent's system variables) and enforce access in the flow, or design the agent tool to use end-user authentication. Scope the service account to exactly what the flow needs.

## Testing

1. Test the flow alone with *Test → Manually*: realistic values, empty values, wrong types, unknown IDs.
2. Check every path returns all outputs.
3. Then test through the agent: the activity map shows which tool was chosen, what inputs were filled and what came back.

## Common failures

| Symptom | Cause |
|---|---|
| Agent says "Something unexpected happened… Error code: 3000" | Asynchronous response is on, or the flow runs in the background |
| Agent times out / no answer | Respond to the agent not reached within 100 s, or not reached on a failure path |
| Flow not listed as a tool | Not in a solution, or in another environment than the agent |
| Inputs arrive empty | Orchestrator couldn't fill them (vague description), or the flow reads the wrong key (`text` vs display name) |
| Agent misreports the result | Prose output or missing `success` flag - return structured outputs |
| Works in test, fails for users | Connection in the flow lacks access to the user's data, or the flow should enforce user-level access itself |
