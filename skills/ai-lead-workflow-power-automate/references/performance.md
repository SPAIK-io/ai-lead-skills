# Performance

## Contents
- Loops with API calls
- Concurrency in Apply to each
- Pagination
- Batching
- Connector throttling
- Child flows
- Trigger-side savings
- Profiling a slow run
- High-volume webhook intake

## Loops with API calls

The usual cause of a slow flow: one connector call per item, sequentially. Fix in this order:

1. **Filter at the source** - Filter Query on *Get items*, Filter rows on *List rows*, a `query=` parameter on REST APIs. Never fetch everything to discard 90% in the flow.
2. **Replace loops with Filter array / Select** for anything that only transforms data (see expressions.md → Arrays without loops).
3. **Batch the writes** (below).
4. **Turn on concurrency** for independent iterations.
5. **Child flows** only when per-item work is heavy and independent.

## Concurrency in Apply to each

- Default: **sequential** (degree 1). Settings → Concurrency control → on → degree 1–50.
- Parallel iterations have no guaranteed order and share variables: Set/Increment/Append variable inside a parallel loop is a race condition. Collect results with a Compose inside the loop instead - referenced **outside** the loop, `outputs('Compose_-_item_result')` returns an array with one entry per iteration. Counters become `length()` on that array or on a Filter array over it; an item index comes from `range()` (expressions.md).
- A failed iteration doesn't stop the other iterations; the Apply to each ends as Failed. For per-item error handling:

```
Apply to each - item                 concurrency 10
   Scope - Try item
      HTTP - update incident
   Compose - item result             run after Try item: is successful, has failed, has timed out
      { "id": @{items('Apply_to_each_-_item')?['ID']}, "status": "@{actions('Scope_-_Try_item')?['status']}" }
Filter array - failed items          From: outputs('Compose_-_item_result')   item()?['status'] is not equal to Succeeded
Condition - any failed?              length(body('Filter_array_-_failed_items')) greater than 0 → log + Terminate Failed (outside the loop)
```

- Starting degree against an external API: 5–10, raise while no 429s appear.
- Lower the degree when the target API throttles (429).
- Apply to each handles up to 5,000 items on the Low performance profile (owner with only Microsoft 365/seeded or free licensing) or 100,000 on premium licensing; chunk larger sets with `chunk()` or child flows.
- Action nesting is limited to 8 levels; deeper logic goes into a child flow.

## Pagination

- *Get items* / *List rows* / many list actions: Settings → Pagination → on, threshold up to 5,000 (Low performance profile) or 100,000.
- Pagination follows `@odata.nextLink` only. For REST APIs with their own paging (offset/limit, page numbers, cursors) build a Do until loop - see http-and-rest-apis.md.
- Use *Select columns* (Dataverse) / *Limit columns by view* (SharePoint) to cut payload size.

## Batching

| Target | How |
|---|---|
| SharePoint | *Send an HTTP request to SharePoint* → `_api/$batch` with many operations in one call; keep batches around 100 operations and check the response per operation |
| Microsoft Graph | `POST https://graph.microsoft.com/v1.0/$batch`, max 20 requests per batch |
| Dataverse | *Perform a changeset request* (atomic group of actions) or the Web API `$batch` via HTTP with Entra auth |
| Email to many | One message to a distribution list or BCC instead of one email per item |
| Reports | Build one HTML/CSV table with *Create HTML table* / *Create CSV table* and send once |

## Connector throttling

Limits are per connection per 60 seconds; examples: SharePoint 600 calls, Office 365 Outlook 300 calls. Check the connector's reference page for others before relying on a number.

Symptoms: 429 errors, long waits in run history, "throttled" notes on actions.
Mitigation: fewer calls (filter, batch), lower loop concurrency, Delay between batches, spread work over scheduled runs. A second connection (another service account) doubles capacity but needs the client's approval.

## Child flows

Use for reuse (error logger), modularity (break a 50-action flow) and parallel heavy work.

Requirements:
- Parent and child are in the **same solution**.
- Child trigger: *Manually trigger a flow* (or Power Apps / Power Apps V2).
- Child ends with *Respond to a PowerApp or flow*; the parent waits for that response.
- Child connections: in the child's run-only users settings, set each connection to the embedded connection ("Use this connection") instead of "Provided by run-only user", or the parent call fails.

Fire-and-forget: put *Respond to a PowerApp or flow* at the start of the child, so the parent continues while the child keeps working. Each child run counts as a separate run against limits.

## Trigger-side savings

- Trigger conditions / Dataverse Select columns prevent runs instead of exiting early (triggers.md).
- For polling triggers, avoid a large items-per-poll setting when only a few changes are expected.

## Profiling a slow run

Run history shows duration per action. Typical findings:
- Apply to each slow → it runs sequentially (default) or makes calls per item.
- *Get items* slow → no Filter Query, unindexed column on a large list, or pagination over everything.
- Many Compose actions → not the problem; look at connector actions.
- One slow HTTP call per item → cache the response (variable/Compose for the run, or a list/table refreshed on a schedule).

## High-volume webhook intake

```
HTTP request trigger → validate → push to a queue (Azure Service Bus / Storage queue / Dataverse table) → Response 202
Separate flow: queue trigger → process with controlled concurrency
```
Accepting and processing are decoupled, so spikes don't time out callers.
