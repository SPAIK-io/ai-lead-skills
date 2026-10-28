# Triggers

## Contents
- Choosing a trigger
- Trigger conditions
- Preventing loop-back (flow re-triggers itself)
- Dataverse trigger filters
- HTTP request trigger
- Recurrence and time zones
- Trigger concurrency and Split on
- Agent triggers

## Choosing a trigger

| Need | Trigger | Note |
|---|---|---|
| React to SharePoint changes | *When an item is created or modified* | Polling - expect minutes of delay depending on licence; not real-time |
| React to Dataverse changes | *When a row is added, modified or deleted* | Event-based; has column and row filters (below) |
| External system pushes events | *When an HTTP request is received* | Premium; see HTTP section |
| External system without webhooks | Recurrence + query "changed since last run" | Store the watermark (last run time) in a list/table or env-independent store, not a variable |
| Mailbox | *When a new email arrives (V3)* / *in a shared mailbox (V2)* | Polling |
| User clicks a button on an item | *For a selected item* (SharePoint) / *When a row is selected* (Dataverse) | Instant |
| Called from Power Apps | *Power Apps (V2)* | Typed inputs |
| Called from another flow | *Manually trigger a flow* (child flow) | See performance.md → child flows |
| Called from an agent | *When an agent calls the flow* | See agent-flow-integration.md |

## Trigger conditions

Set in trigger → Settings → Trigger conditions. When the condition is false, no run is created.

Rules:
- Each condition is a WDL expression that **starts with `@`**.
- Multiple rows are combined with **AND**. OR logic goes inside one expression with `or()`.
- Reference fields via `triggerOutputs()?['body/<InternalName>']` (SharePoint) or `triggerBody()?['field']`.
- A broken condition silently blocks every run - test it as a Compose in a copy of the flow first.

Examples:

```
@equals(triggerOutputs()?['body/Status/Value'], 'Submitted')
```
SharePoint choice column equals "Submitted".

```
@and(equals(triggerOutputs()?['body/Priority/Value'], 'High'), greater(int(coalesce(triggerOutputs()?['body/Amount'], 0)), 1000))
```

```
@not(equals(toLower(triggerOutputs()?['body/Editor/Email']), 'svc-flow@client.nl'))
```
Skip changes made by the flow's own service account (loop prevention).

## Preventing loop-back

A flow that updates the item that triggered it fires again - every time. Pick one defence, in this order:

Trigger concurrency set to 1 does **not** prevent loop-back; it only queues the extra runs.

1. **Trigger condition excluding the flow's service account** (above). Only works if the flow's connection uses a dedicated account - with the builder's own account it would also block their manual edits.
2. **Only fire on relevant column changes.** SharePoint: add *Get changes for an item or a file (properties only)* with *Since* = `triggerOutputs()?['body/{TriggerWindowStartToken}']` (needs versioning on the list) and check `body('Get_changes...')?['ColumnHasChanged']?['Status']`. Dataverse: use *Select columns* on the trigger.
3. **Processed flag column**, set by the flow, checked in the trigger condition.

## Dataverse trigger filters

- **Change type**: added / modified / deleted / combinations.
- **Scope**: Organization for system-wide automation (User/Business unit only see their own rows).
- **Select columns**: comma-separated logical names; the flow fires only when one of these changes. Leave out the columns the flow itself writes.
- **Filter rows**: OData on the row, e.g. `statuscode eq 1 and prefix_category eq 100000001`.
- **Run as**: flow owner, modifying user, or row owner - decides whose permissions downstream Dataverse actions use.

## HTTP request trigger

Setup: add the trigger → define the JSON schema with *Use sample payload to generate schema* → save to get the URL.

Who can trigger the flow:
- **Any user in my tenant** (default for new flows) - caller sends an Entra ID bearer token with audience `https://service.flow.microsoft.com/`.
- **Specific users in my tenant** - same, plus allowed users or service principal object IDs.
- **Anyone** - no authentication; the URL (with its `sig` parameter) is the secret. Use only when the caller cannot obtain an Entra token (common for SaaS webhooks); then also require a shared-secret header: first action compares `triggerOutputs()?['headers']?['x-api-key']` with a secret environment variable and, on mismatch, returns a 401 Response and Terminates.

Behaviour:
- Without a *Response* action the caller gets `202 Accepted` immediately.
- With a *Response* action the caller waits; it must respond within **120 seconds**. Long work goes after the Response action.
- Request body limit 100 MB.
- Treat the URL as a credential: never commit it to source control or paste it in tickets.

## Recurrence and time zones

- Set *Time zone* on the trigger and use *At these hours* / *At these minutes* for "every weekday at 08:00". Then DST is handled; a UTC-only schedule shifts by an hour twice a year.
- "Every 24 hours" drifts from the save time; prefer fixed hours.
- For catch-up logic, compute the window from the trigger's scheduled time (`trigger()?['scheduledTime']`) rather than `utcNow()`, so a delayed run doesn't skip data.

## Trigger concurrency and Split on

- **Concurrency control** (trigger settings): off by default. When on, default 25, range 1–100. Set to 1 to serialise runs (shared counters, APIs that can't handle parallel writes).
- **Enabling it cannot be undone** without deleting and re-adding the trigger (error `CannotDisableTriggerConcurrency`). Warn before recommending.
- **Split on** (array-body triggers): each element becomes its own run. Expensive in runs; leave off unless every element truly needs an independent run.

## Agent triggers

- Agent-called flows use *When an agent calls the flow* with typed input parameters; design those inputs per agent-flow-integration.md.
- Agent flows can also run on a schedule or on events for autonomous agents; they then consume Copilot Credits at the standard rate.
