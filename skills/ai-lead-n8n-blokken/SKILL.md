---
name: ai-lead-n8n-blokken
description: >-
  Hulpskill bij ai-lead-workflow-n8n; voor een eerste flow uit een blueprint begin je daar.
  Configure n8n nodes (blocks) when building a flow as an import file, without MCP or API keys.
  Use when setting node parameters - which fields each resource/operation needs, how
  displayOptions show or hide fields, node JSON shape and typeVersion - and when picking the
  native nodes that replace Code (Filter, If, Switch, Summarize, Aggregate, Split Out, Merge,
  Sort, Limit, Remove Duplicates, Date & Time, Data Table, Extract From File, HTTP Request
  pagination). Triggers - "blok instellen in n8n", "welke node gebruik ik", "parameters van een
  n8n-blok", "welk veld is verplicht".
---

Gebaseerd op czlonkowski/n8n-skills (MIT), commit e037563, aangepast door SPAIK: zonder MCP, voor flows als importbestand.

# n8n Node Configuration

Expert guidance for operation-aware node configuration with property dependencies, for flows that Claude writes as a workflow JSON file and the lead imports in n8n (Workflows → Create workflow → ⋯ → Import from File).

For node types and typeVersions proven on n8n Cloud 2.47 (see ai-lead-workflow-n8n), follow `ai-lead-workflow-n8n`; examples here may show other versions.

---

## Configuration Philosophy

**Progressive disclosure**: Start minimal, add complexity as needed.

Configuration best practices:
- Know the operation's required fields (the tables in [OPERATION_PATTERNS.md](OPERATION_PATTERNS.md) and [NATIVE_NODES.md](NATIVE_NODES.md)) and write only those.
- Import the file and run it: what n8n shows on the node and in its INPUT and OUTPUT panels is the test.
- When unsure of an exact parameter name, nesting or typeVersion, say so honestly instead of guessing.

**Key insight**: Most configurations need only a handful of fields, not the full schema!

---

## Core Concepts

### 1. Operation-Aware Configuration

**Not all fields are always required** - it depends on operation!

**Example**: Slack node
```javascript
// For operation='post'
{
  "resource": "message",
  "operation": "post",
  "channel": "#general",  // Required for post
  "text": "Hello!"        // Required for post
}

// For operation='update'
{
  "resource": "message",
  "operation": "update",
  "messageId": "123",     // Required for update (different!)
  "text": "Updated!"      // Required for update
  // channel NOT required for update
}
```

**Key**: Resource + operation determine which fields are required!

### 2. Property Dependencies

**Fields appear/disappear based on other field values**

**Example**: HTTP Request node
```javascript
// When method='GET'
{
  "method": "GET",
  "url": "https://api.example.com"
  // sendBody not shown (GET doesn't have body)
}

// When method='POST'
{
  "method": "POST",
  "url": "https://api.example.com",
  "sendBody": true,       // Now visible!
  "body": {               // Required when sendBody=true
    "contentType": "json",
    "content": {...}
  }
}
```

**Mechanism**: displayOptions control field visibility

### 3. Finding the Right Fields Without Tools

Work in this order:

1. **Know the operation's required fields** - the tables in this skill and its reference files cover the common nodes.
   Write those, nothing more.
2. **Import the file and look** - a node that shows red or a warning after import misses a required field. Open it:
   n8n points at the field.
3. **Run it** - Execute workflow, or Execute step on one node. Open the node and check its INPUT and OUTPUT panels to
   see what actually arrives and leaves.
4. **When unsure, copy from the editor** - let the lead build the node once in the n8n editor with the right
   resource and operation, select it and copy it (Ctrl/Cmd+C). The pasted JSON gives the exact parameter names,
   nesting and `typeVersion`; base the import file on that.

---

## Configuration Workflow

### Standard Process

1. Identify node type and operation.
2. Look up the operation's required fields (tables below and in the reference files).
3. Write the required fields in the import file.
4. Import in n8n; open any node that shows red or a warning and see which field n8n points at.
5. If a field is unclear → copy the node from the editor (Ctrl/Cmd+C) and compare.
6. Add optional fields as needed.
7. Run it (Execute workflow / Execute step) and check INPUT and OUTPUT of each node.
8. Hand over: the lead runs and shows the flow; a beheerder turns flows on, not the lead.

### Example: Configuring HTTP Request

Start minimal (`method`, `url`, `authentication`), import, and let each node warning surface the next required field (`sendBody` for POST → `body` when `sendBody=true`) until the node is clean and a run returns the expected OUTPUT. Full step-by-step walkthrough in **[OPERATION_PATTERNS.md](OPERATION_PATTERNS.md#worked-example-configuring-http-request-step-by-step)**.

### Options Collections

Many settings live inside a node's `options` collection, not at the top of `parameters`: HTTP Request pagination and
batching, Webhook raw body, Merge combine settings, Date & Time `includeInputFields`, … Check the node's options
(in [NATIVE_NODES.md](NATIVE_NODES.md), or in the editor under "Add option") before deciding a job needs a Code node.

### Fields Filled From a Live Service

Some fields get their values from the connected service (a spreadsheet, a channel, a table): the dropdown is loaded
live. Don't guess an ID for them. These are resource-locator fields, written as `{"__rl": true, "mode": "name" | "id" |
"list" | "url", "value": "…"}` - keep that shape. When the value is unknown, leave it for the lead to pick in the
editor after import and say so in the node's note. Data Table nodes: the lead picks the table after import.

---

## Which node for which job

Before reaching for a Code node, check this table; a Code node is the exception and gets an extra IT check.

| Job | Use |
|---|---|
| Flag that only picks a route; dropping items | conditions in IF / Switch / Filter |
| Constant, error or return item | Edit Fields (Set) |
| Restore earlier context | `$('Node').item` |
| Pick rows after a Data Table get | the get's order by + limit |
| Group and sum | Summarize |
| Items to one array / array to items | Aggregate / Split Out |
| Join two lists | Merge (combine by fields) |
| Diff or sync two lists | Compare Datasets |
| Dedupe, also across runs | Remove Duplicates |
| Top-N | Sort + Limit |
| Dates | Date & Time, or a Luxon one-liner |
| XML / HTML / Markdown / CSV / XLSX | XML, HTML, Markdown, Extract From File / Convert To File |
| Paging an API (no service node) | HTTP Request's pagination option ¹ |
| Throttle calls | HTTP Request's batching option ¹, or Loop + Wait |
| Hash, HMAC, UUID | Crypto (+ Webhook raw body) ¹ |

¹ Only with approval for a connection.

Configs and traps per node: **[NATIVE_NODES.md](NATIVE_NODES.md)**.

---

## Property Dependencies Deep Dive

Fields have `displayOptions` visibility rules: `show`/`hide` blocks where multiple conditions are AND'd and multiple values are OR'd (e.g. `body` shows when `sendBody=true` AND `method IN (POST, PUT, PATCH)`). The three recurring patterns are the boolean toggle (sendBody → body), the operation switch (post vs update show different fields), and type selection (string vs boolean conditions). To find what controls a field, look up its parent field in the dependency patterns, or copy the node from the editor with the field visible — especially when n8n flags a field you don't see.

Mechanism details, all four dependency patterns, complex flows, nested dependencies, and troubleshooting are in **[DEPENDENCIES.md](DEPENDENCIES.md)** (quick-reference recap under [Quick Reference: displayOptions and Common Dependency Patterns](DEPENDENCIES.md#quick-reference-displayoptions-and-common-dependency-patterns)).

---

## Common Node Patterns

### Pattern 1: Resource/Operation Nodes

**Examples**: Slack, Google Sheets, Airtable

**Structure**:
```javascript
{
  "resource": "<entity>",      // What type of thing
  "operation": "<action>",     // What to do with it
  // ... operation-specific fields
}
```

**How to configure**:
1. Choose resource
2. Choose operation
3. Look up the operation-specific requirements ([OPERATION_PATTERNS.md](OPERATION_PATTERNS.md)), or copy the node from the editor with that operation selected
4. Configure required fields

### Pattern 2: HTTP-Based Nodes

**Examples**: HTTP Request, Webhook

**Structure**:
```javascript
{
  "method": "<HTTP_METHOD>",
  "url": "<endpoint>",
  "authentication": "<type>",
  // ... method-specific fields
}
```

**Dependencies**:
- POST/PUT/PATCH → sendBody available
- sendBody=true → body required
- authentication != "none" → credentials required

**Critical: credentials block, node id, typeVersion**
- **No `credentials` block in the import file.** If your role can only view credentials, or there are no connections to
  systems yet, Claude never creates a credential. Never set a placeholder credential ID (e.g. `"id": "REPLACE_ME"`) — n8n's
  UI renders a permanently disabled credential selector for unknown IDs. Without the block, the node shows the
  credential as missing and gets a normal clickable dropdown.
- **Node `id` must be a UUID v4**, not a readable slug — the frontend binds forms and the credential component to it.
- **Don't hardcode old `typeVersion` values** — use the versions in `ai-lead-workflow-n8n`, or copy the node from the
  editor to see the current one (httpRequest is 4.4+).

### Pattern 3: Database Nodes

**Examples**: Postgres, MySQL, MongoDB

**Structure**:
```javascript
{
  "operation": "<query|insert|update|delete>",
  // ... operation-specific fields
}
```

**Dependencies**:
- operation="executeQuery" → query required
- operation="insert" → table + values required
- operation="update" → table + values + where required

**Critical: Write operations may return 0 items**
- INSERT, UPDATE, DELETE can produce 0 n8n output items, depending on the node and operation (raw query execution reliably returns 0 result rows; some database nodes return the affected rows)
- Set `alwaysOutputData: true` on write-operation nodes to keep downstream chains alive
- Downstream nodes should use `$('UpstreamNode').all()` instead of `$input` if they need data

### Pattern 4: Conditional Logic Nodes

**Examples**: IF, Switch, Merge

**Structure**:
```javascript
{
  "conditions": {
    "<type>": [
      {
        "operation": "<operator>",
        "value1": "...",
        "value2": "..."  // Only for binary operators
      }
    ]
  }
}
```

**Dependencies**:
- Binary operators (equals, contains, etc.) → value1 + value2
- Unary operators (isEmpty, isNotEmpty) → value1 only + singleValue: true

The current IF/Filter/Switch conditions shape (v2+, `leftValue` / `rightValue` / `operator`) is in
[NATIVE_NODES.md](NATIVE_NODES.md).

---

## Operation-Specific Configuration

Required fields shift with resource + operation: Slack `post` needs `channel`+`text`, but `update` needs `messageId`+`text` (channel optional) and `channel/create` needs `name`. HTTP `GET` uses `sendQuery`+`queryParameters`; `POST` needs `sendBody`+`body`. IF binary operators (`equals`) need `value1`+`value2`; unary (`isEmpty`) need only `value1` plus `singleValue: true`. Concrete minimal configs for each in **[OPERATION_PATTERNS.md](OPERATION_PATTERNS.md#operation-specific-configuration-examples)**.

---

## Handling Conditional Requirements

Some fields are required only under certain conditions: HTTP `body` is required when `sendBody=true` AND `method IN (POST, PUT, PATCH, DELETE)`; IF `singleValue` should be `true` when the operator is unary (`isEmpty`, `isNotEmpty`, `true`, `false`) — write it yourself in the import file, nothing adds it for you. Discover conditional requirements by reading the warning n8n shows on the node after import, copying the node from the editor with the condition switched on, or iterating from a minimal config. Worked discovery examples in **[DEPENDENCIES.md](DEPENDENCIES.md#handling-conditional-requirements)**.

---

## Node-Specific Configuration Notes

### SplitInBatches v3

```javascript
{
  "batchSize": 100,  // Number of items per batch
  "options": {}
}
```

**Output wiring**:
- `main[0]` (done) → Connect to downstream processing (add Limit 1 first)
- `main[1]` (each batch) → Connect to loop body, then loop back to SplitInBatches input

See `ai-lead-n8n-patronen` for detailed loop and nested loop patterns.

### Google Sheets Node

**Per-item execution**: Each input item triggers a separate API call. If you have 100 items and use a Google Sheets "Append Row" node, it makes 100 API calls. To write in bulk, collect the rows into one item with an Aggregate node first, then use a single HTTP Request with the Sheets API.

**Formula columns**: Never use `append` on sheets with formula columns — it overwrites formulas. Instead, use HTTP Request with Google Sheets API `values.update` (PUT) method and a `googleApi` credential.

---

## Configuration Anti-Patterns

### ❌ Don't: Over-configure Upfront

**Bad**:
```javascript
// Adding every possible field
{
  "method": "GET",
  "url": "...",
  "sendQuery": false,
  "sendHeaders": false,
  "sendBody": false,
  "timeout": 10000,
  "ignoreResponseCode": false,
  // ... 20 more optional fields
}
```

**Good**:
```javascript
// Start minimal
{
  "method": "GET",
  "url": "...",
  "authentication": "none"
}
// Add fields only when needed
```

### ❌ Don't: Skip the Test Run

**Bad**:
```javascript
// Write the file and hand it over unseen
const workflow = {...};
// "Import it, it should work"
```

**Good**:
```javascript
// Hand over with the test steps
// 1. Import from File
// 2. Open each node: no red marks or warnings
// 3. Execute workflow (or Execute step on one node)
// 4. Check each node's INPUT and OUTPUT panels against what you expect
```

### ❌ Don't: Ignore Operation Context

**Bad**:
```javascript
// Same config for all Slack operations
{
  "resource": "message",
  "operation": "post",
  "channel": "#general",
  "text": "..."
}

// Then switching operation without updating config
{
  "resource": "message",
  "operation": "update",  // Changed
  "channel": "#general",  // Wrong field for update!
  "text": "..."
}
```

**Good**:
```javascript
// Check requirements when changing operation
// (OPERATION_PATTERNS.md, or copy the node from the editor with "update" selected)
// See what update operation needs (messageId, not channel)
```

---

## Changing One Field in an Existing Flow

There is no live connection to n8n, so a change goes through the file or the editor:

- **In the import file**: change only that node's field (e.g. `parameters.jsCode` in a Code node, a URL in a long
  HTML email body, a typo in a JSON body) and import again into a fresh workflow.
- **Or paste the block**: give the lead the changed node's JSON; they delete the old node in the editor, paste the
  new one (Ctrl/Cmd+V) and reconnect it.
- **Keep the node `name` the same.** `connections` refer to nodes by name, and expressions like `$('Node')` too; a
  renamed node loses its wires and breaks those expressions.
- Change exactly the spot you mean. In JSON, a Code node's code is one escaped string (`\n`, `\"`); edit it carefully
  so the file stays valid JSON, or n8n refuses the import.

---

## Best Practices

### Do

1. **Start from the required fields**
   - Use the tables in this skill and its reference files
   - Write only what the operation needs
   - Add optional fields later

2. **Import and run iteratively**
   - Write → Import → Check warnings → Run → Check INPUT/OUTPUT → Fix → Repeat
   - Two or three rounds is normal
   - Read n8n's node warnings carefully

3. **Copy from the editor when stuck**
   - If a field seems missing, build the node in the editor and copy it (Ctrl/Cmd+C)
   - Understand what controls field visibility
   - Say honestly when you don't know a parameter name

4. **Respect operation context**
   - Different operations = different requirements
   - Always re-check the required fields when changing operation
   - Don't assume configs are transferable

5. **Write operator structure complete**
   - Unary operators carry `singleValue: true`
   - Nothing fixes the import file for you
   - Copy a condition from the editor when unsure of the shape

### ❌ Don't

1. **Guess field names or versions**
   - Not sure? Say so and copy the node from the editor
   - Follow the typeVersions in `ai-lead-workflow-n8n`

2. **Configure blindly**
   - Always run the flow before handing it over
   - Understand why fields are required
   - Check the parent field for conditional fields

3. **Copy configs without understanding**
   - Different operations need different fields
   - Import and run after copying
   - Adjust for new context
   - The lead must be able to explain every step of the flow

4. **Add a `credentials` block or create credentials**
   - Leave it out; the node shows the credential as missing after import
   - If your role can only view credentials, you cannot create one either

---

## Native Nodes for Data Jobs

The table under [Which node for which job](#which-node-for-which-job) picks the node; **[NATIVE_NODES.md](NATIVE_NODES.md)** has each one's
`parameters` JSON and traps. The traps that bite most:

- **Summarize** — `fieldsToSplitBy` is one comma-separated string; outputs are named `sum_amount`, `count_id`, …
- **Split Out** — `include` defaults to `noOtherFields`: the parent's fields are dropped unless you keep them.
- **Merge** — `combineByFields` + `joinMode` (`keepMatches`, `keepNonMatches`, `enrichInput1`, …); `numberInputs` only on
  append / SQL / position / choose-branch modes.
- **Compare Datasets** — four outputs in fixed order: in A only, same, different, in B only.
- **Remove Duplicates** — `removeItemsSeenInPreviousExecutions` dedupes across runs (v2), replacing static-data Code.
- **Date & Time** — set `options.includeInputFields: true`, or only the new date field survives.
- **HTTP Request pagination** — always `limitPagesFetched: true` + `maxRequests`; an object body arrives as one item per page.
- **Crypto** — use typeVersion 2: HMAC and signing secrets come from a `crypto` credential (v1 kept them in the JSON).
- **Node settings** — `executeOnce`, `alwaysOutputData`, `notes` / `notesInFlow` sit next to `parameters`, not inside it.

---

## Silent-Failure Gotchas by Node Family

Some misconfigurations import without any warning, run without error, and quietly do the wrong thing — the node shows the fields exist but not what happens when you omit them. You catch them only by running the flow and checking the INPUT and OUTPUT panels. The high-frequency ones:

- **Switch** — no `options.fallbackOutput` ⇒ unmatched items silently dropped.
- **Merge** — `numberInputs` defaults to 2 (extra sources drop; `numberOfInputs` is not a field and is ignored); `useDataOfInput` is 1-indexed vs the 0-indexed `connections.<src>.main[idx]` slot (`useDataOfInput: "N"` → `main[N-1]`).
- **Database** — `{{ }}` interpolation into `parameters.query` is SQL injection; use `$1/$2` placeholders + `options.queryReplacement`.
- **Slack** — Block Kit must be wrapped `={{ { "blocks": ... } }}` or it posts as plain text.
- **Webhook / Respond** — `options.responseCode` defaults to 200 even on error branches; a top-level `responseCode` is ignored.
- **Schedule Trigger** — timezone is workflow-level (Workflow Settings), not per-rule.

Full symptom/cause/fix detail (in workflow-JSON terms) in **[NODE_FAMILY_GOTCHAS.md](NODE_FAMILY_GOTCHAS.md)**.

---

## Detailed References

For comprehensive guides on specific topics:

- **[DEPENDENCIES.md](DEPENDENCIES.md)** - Deep dive into property dependencies and displayOptions
- **[OPERATION_PATTERNS.md](OPERATION_PATTERNS.md)** - Common configuration patterns by node type
- **[NATIVE_NODES.md](NATIVE_NODES.md)** - Configs for the native nodes that replace Code (transform, dedupe, diff, dates, pagination, HMAC, files) and node settings
- **[NODE_FAMILY_GOTCHAS.md](NODE_FAMILY_GOTCHAS.md)** - Silent runtime traps by family (Switch, Merge, Database, Slack, Webhook, Schedule)

---

## Summary

**Configuration Strategy**:
1. Look up the operation's required fields
2. Write them in the import file, nothing more
3. Import; open any node with a warning and add the field n8n points at
4. Unsure of a name or version? Copy the node from the editor
5. Run it and check INPUT and OUTPUT per node (avg 2-3 rounds)
6. Hand over with the test steps; a beheerder turns the flow on

**Key Principles**:
- **Operation-aware**: Different operations = different requirements
- **Progressive disclosure**: Start minimal, add as needed
- **Dependency-aware**: Understand field visibility rules
- **Run-driven**: Let the import warnings and the test run guide configuration

**AI agent / LLM nodes**: only when the lead says an AI connection is available; see `ai-lead-workflow-n8n`.

**Related Skills**:
- **ai-lead-workflow-n8n** - Build the flow as an import file; proven node types and typeVersions
- **ai-lead-n8n-expressies** - Configure expression fields
- **ai-lead-n8n-patronen** - Apply workflow patterns with proper configuration
- **ai-lead-n8n-javascript** - When a Code node is the justified exception
- **ai-lead-n8n-bestanden** - Files and binary data
