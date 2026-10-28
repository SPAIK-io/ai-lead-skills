# Expressions (WDL)

Same language and functions as Azure Logic Apps: learn.microsoft.com/azure/logic-apps/workflow-definition-language-functions-reference. Only non-obvious material is listed here.

## Contents
- Where `@` goes
- Referencing actions, loops and the trigger
- Null, empty and type traps
- Strings and case
- Numbers and Dutch formatting
- Dates and time zones
- Arrays without loops
- Objects
- Workflow metadata
- Compose vs variable
- Debugging an expression

## Where `@` goes

| Context | Write |
|---|---|
| fx editor in the designer | `addDays(utcNow(), 7)` - no `@` |
| Inside a text field / JSON string | `"Ticket @{variables('vId')} created"` |
| Code view, whole value | `"@variables('vArray')"` - keeps array/object/number type |
| Code view, interpolated | `"@{variables('vArray')}"` - always a **string**; an array becomes `"[...]"` text |
| Trigger condition / Filter array advanced mode | starts with `@` |

Common bug: an HTTP body field `"items": "@{body('Select')}"` sends a string, not an array. Use `"items": @{body('Select')}` without quotes in the JSON body field, or build the whole body in a Compose.

## Referencing actions, loops and the trigger

- `body('Get_items_-_open_requests')`, `outputs('HTTP_-_call_API')?['statusCode']`, `outputs('HTTP_-_call_API')?['headers']?['Location']`
- Name mapping: spaces → `_`, other characters unchanged; a `'` in a name is doubled.
- Current loop item: `items('Apply_to_each_-_candidate')?['Email']`; in Filter array/Select: `item()?['Email']`.
- Loop index: none built in. Use `range(0, length(body('Get_items')?['value']))` as the loop input; then the index is `items('Apply_to_each')` and the element `body('Get_items')?['value'][items('Apply_to_each')]`. Safe with parallel concurrency, unlike a counter variable.
- SharePoint trigger fields: `triggerOutputs()?['body/Title']`, choice: `triggerOutputs()?['body/Status/Value']`, person: `triggerOutputs()?['body/Author/Email']`.
- Any action's status/error: `actions('Name')?['status']`, `actions('Name')?['error']`.

## Null, empty and type traps

| Trap | Fix |
|---|---|
| `coalesce('', 'x')` returns `''` | `if(empty(triggerBody()?['text']), 'x', triggerBody()?['text'])` |
| `length(null)` throws | `length(coalesce(body('X'), createArray()))` or test with `empty()` first |
| `int('')`, `int('3.5')` throw | `if(empty(x), 0, int(x))`; decimal text: keep it as `float(x)`, or truncate with `int(first(split(x, '.')))` |
| `'1000'` vs `1000` | `equals('1000', 1000)` is false - convert at the boundary with `int()` / `float()` |
| `body('Get_item')?['Field']` on a missing property | `?['...']` returns null instead of throwing - use `?` on every hop |
| Property selection on a string | The value is a JSON string: wrap it with `json()` first |
| `bool('yes')` throws | `bool()` accepts true/false/1/0; map other text with `equals(toLower(x), 'ja')` |

## Strings and case

- `contains()`, `startsWith()`, `indexOf()` and `replace()` are case-sensitive. Normalise both sides with `toLower()` when comparing user, agent or form text - also for `equals()` to be safe.
- Newline: `decodeUriComponent('%0A')`; CRLF: `decodeUriComponent('%0D%0A')`.
- `nthIndexOf(text, ';', 2)`, `slice(text, start, end)`, `lastIndexOf()` beat chains of `substring()`.
- `trim()` doesn't remove non-breaking spaces from HTML/Outlook (`decodeUriComponent('%C2%A0')`) - `replace()` them first.
- Strip HTML from an email body: use the *Html to text* action (Content Conversion connector) instead of regex attempts.

## Numbers and Dutch formatting

- Display: `formatNumber(1234.5, 'N2', 'nl-NL')` → `1.234,50`; currency `formatNumber(x, 'C2', 'nl-NL')`.
- Parse Dutch input `1.234,56`: `float(replace(replace(x, '.', ''), ',', '.'))`.
- Check before converting: `isInt(x)`, `isFloat(x)` (isFloat accepts a locale: `isFloat(x, 'nl-NL')`).
- `rand(min, max)` - max is exclusive. `div(7, 2)` on integers returns `3`; use `div(float(7), 2)` for `3.5`.

## Dates and time zones

- Flows run in UTC. Amsterdam: `convertTimeZone(utcNow(), 'UTC', 'W. Europe Standard Time', 'yyyy-MM-dd HH:mm')` - handles DST.
- Dutch names: `formatDateTime(x, 'dddd d MMMM yyyy', 'nl-NL')` → `donderdag 22 oktober 2026`.
- Parse a Dutch date string: `parseDateTime('22-10-2026', 'nl-NL', 'dd-MM-yyyy')`.
- Difference in minutes: `div(sub(ticks(end), ticks(start)), 600000000)` (1 tick = 100 ns). `dateDifference(start, end)` returns a `d.hh:mm:ss` string.
- Day of week: `dayOfWeek(x)` → 0 = Sunday … 6 = Saturday.
- SharePoint and Dataverse return UTC ISO strings. A date-only SharePoint value can show as the previous day 22:00/23:00Z - convert to Amsterdam time before formatting.
- Excel returns serial numbers unless *List rows present in a table* → DateTime Format = ISO 8601. Convert a serial: `addDays('1899-12-30', int(x))`.
- OData date filters: SharePoint `Modified ge '@{addDays(utcNow(), -7, 'yyyy-MM-ddTHH:mm:ssZ')}'`; Dataverse `modifiedon ge @{addDays(utcNow(), -7)}`.

## Arrays without loops

| Goal | Do |
|---|---|
| Keep matching items | **Filter array** (`item()?['Status']` is equal to `Open`) |
| Reshape objects | **Select** with key/value map |
| Array of plain values | **Select** in text mode with `item()?['Email']` |
| Join to text | `join(body('Select_-_emails'), ';')` |
| Deduplicate | `union(body('Select'), body('Select'))` |
| First match | `first(body('Filter_array'))?['ID']` (null if none) |
| Count matches | `length(body('Filter_array'))` |
| Batches of N | `chunk(array, 100)` → Apply to each over the chunks |
| Sort / reverse | `sort(array, 'Title')`, `reverse(array)` |
| Skip / take | `skip(array, 10)`, `take(array, 5)` |
| Membership | `contains(array, 'value')` (exact, case-sensitive) |
| Match items across two lists | Apply to each over the smaller list, Filter array on the larger list inside it (no API call per item) |
| Sum without loop | `xpath(xml(json(concat('{"r":{"v":', string(body('Select_-_amounts')), '}}'))), 'sum(/r/v)')` |

## Objects

- There is no `createObject()` in WDL. Build an object by writing JSON in a Compose's inputs (with `@{...}` / `@...` inside), or with `json(concat(...))` / `addProperty()`.
- Parse JSON text: `json(text)`; serialise: `string(object)`.
- Modify without rebuilding: `addProperty(obj, 'key', value)`, `setProperty(obj, 'key', value)`, `removeProperty(obj, 'key')`. Nested: `setProperty(obj, 'a', setProperty(obj?['a'], 'b', value))`.
- Property names with spaces or special characters: `?['Display Name']`.
- Parse JSON action: generate the schema from a real sample, then remove fields that can be missing from `required` and allow nulls (`"type": ["string", "null"]`), otherwise runs fail on the first null.

## Workflow metadata

`workflow()?['name']` (flow ID), `workflow()?['run']?['name']` (run ID), `workflow()?['tags']?['environmentName']`, `workflow()?['tags']?['flowDisplayName']`, `trigger()?['scheduledTime']`, `guid()`. Run URL: see error-handling.md.

## Compose vs variable

- **Compose**: value computed once; immutable; reference with `outputs('Compose_-_x')`. Default choice.
- **Variable**: only for values that change (counters, accumulators, error message). Initialise at top level only.

## Debugging an expression

1. Put the sub-expression in its own Compose and read the output in run history.
2. Break long chains into several Composes.
3. Copy a real value from the previous action's outputs and build against that.
4. Check the exact path in *Peek code* when the UI label differs from the JSON property.
