---
name: ai-lead-n8n-bestanden
description: >-
  Hulpskill bij ai-lead-workflow-n8n; voor een eerste flow uit een blueprint begin je daar.
  Handle files and binary data in an n8n workflow that is built as an import file (works without
  MCP). Use when a flow reads or writes files — uploading a csv, xlsx or pdf through a form
  (Form Trigger file field), Extract From File, Convert To File, $binary vs $json,
  binaryPropertyName, binary that disappears after a node, or Merge to keep the binary. Also
  triggers on "csv uploaden in n8n", "bestand inlezen in n8n", "formulier met bijlage", "excel
  inlezen in n8n", "bestand maken in n8n".
---

Gebaseerd op czlonkowski/n8n-skills (MIT), commit e037563, aangepast door SPAIK: zonder MCP, voor flows als importbestand.

# n8n Binary and Data

Every n8n item carries two independent slots: `$json` for structured data and `$binary` for file bytes. They travel side by side through the workflow. File contents — the actual PDF, image, or zip — live in `$binary`, never in `$json`. Get that split wrong and you read an empty field, lose a file mid-flow, or hand an AI agent a tool input it can't use.

This skill covers where binary lives, how to read and write it, how to keep it from being silently stripped, the hard wall between binary and the AI-agent tool boundary, and why chat surfaces need a URL instead of raw bytes.

---

## The three rules that prevent 90% of binary bugs

1. **File contents are in `$binary`, not `$json`.** After an HTTP download, a "Read Files", or an email-attachment trigger, the bytes sit in `$binary.<key>`. `$json` holds metadata at most. Reading `$json.data` for file contents gives you nothing.

2. **Only with an AI connection: binary cannot cross the AI-agent tool boundary — in either direction.** Tool arguments and tool return values are JSON only. An uploaded image can't be passed into a tool as a file, and a tool can't return raw bytes. Pre-stage to storage and pass a key or URL through JSON instead. See `AGENT_TOOL_BINARY.md`.

3. **Only with a chat app connected: chat surfaces render images by URL, not by `$binary`.** Slack, Discord, Teams, Telegram, embedded webhook chat — none of them read the binary slot. The image has to live somewhere a URL can fetch it. See `CDN_REQUIREMENT.md`.

---

## Proven in the trial environment (n8n Cloud 2.47): form upload + csv

Tested on the instance (n8n Enterprise Cloud 2.47, 14 Nov):

- A **Form Trigger** (typeVersion 2.2) with a field `fieldType: "file"` puts the uploaded file in `$binary` under a property named **after the field label**. Field label `Bestand` → `$binary.Bestand` (not `$binary.data`).
- **Extract From File** (typeVersion 1.1) with `binaryPropertyName` set to that same label (`Bestand`) turns every csv row into one item, with the header row as field names.
- Clicking **Execute workflow** opens the form; the workflow does not need to be published for that.

Minimal parameters of both nodes:

```json
{"parameters":{"formTitle":"Upload je testbestand","formDescription":"Alleen verzonnen gegevens. Een csv-bestand met een kopregel.","formFields":{"values":[{"fieldLabel":"Bestand","fieldType":"file","multipleFiles":false,"acceptFileTypes":".csv","requiredField":true}]},"options":{}},"type":"n8n-nodes-base.formTrigger","typeVersion":2.2,"name":"Formulier"}
{"parameters":{"binaryPropertyName":"Bestand","options":{}},"type":"n8n-nodes-base.extractFromFile","typeVersion":1.1,"name":"Lees csv"}
```

These are fragments, not complete nodes: each node in the import file also needs an `id` (UUID), `position`, `notes` and `notesInFlow`, and the Form Trigger needs a `webhookId` (UUID). See `ai-lead-workflow-n8n` for the full file layout. Rename the field label and the `binaryPropertyName` together, or Extract From File finds nothing.

To check it: import the file in n8n and run it (Execute workflow, or Execute step); open the node and check the INPUT and OUTPUT panels — the Binary tab shows the file and the property name.

---

## The two slots

Each item is shaped like this:

```json
{
  "json": { "customerId": 42, "status": "sent" },
  "binary": {
    "invoice": {
      "data": "<base64-encoded bytes>",
      "mimeType": "application/pdf",
      "fileName": "invoice-42.pdf",
      "fileExtension": "pdf"
    }
  }
}
```

The key inside `binary` (`invoice` here) is the **binary property name**. Most file-handling nodes have a `binaryPropertyName` parameter that points at it — the producer names the slot, the consumer references it by that name. The default key across most nodes is `data`, so when nothing tells you otherwise, assume `$binary.data`.

`$json` and `$binary` are separate namespaces. An expression like `{{ $binary.invoice.fileName }}` reads file metadata; `{{ $json.customerId }}` reads data. They never mix.

This split also explains a webhook gotcha: a Webhook trigger receiving `multipart/form-data` puts the uploaded file in `$binary` and the accompanying form fields in `$json.body` — so an uploaded file is not somewhere under `$json` at all. (The `$json.body` nesting for webhooks is **ai-lead-n8n-expressies** territory.)

See `BINARY_BASICS.md` for the full slot anatomy, mime types, and size limits.

---

## Producing binary

You rarely build a `$binary` slot by hand — nodes populate it for you:

| Source | How binary appears |
|---|---|
| Form Trigger with a `file` field | Uploaded file in `$binary.<field label>` (see the proven section above) |
| HTTP Request with `responseFormat: "file"` | Response body lands in `$binary.data` (or the name you set) |
| Read/Write Files from Disk | File contents read into `$binary` |
| Storage downloads (S3, Google Drive, Dropbox, etc.) | Downloaded file in `$binary.<key>` |
| Email triggers with attachments | Each attachment arrives in `$binary` |
| Provider AI media nodes (image/audio gen) | Set `options.binaryPropertyOutput` so the bytes land where the next node looks |

For an HTTP download, the one field that matters is `responseFormat`. Check it after import: run the node and open its OUTPUT panel — the Binary tab should show the file. Leaving it as the default JSON/string format is the classic reason a downloaded file ends up as garbled text in `$json` instead of clean bytes in `$binary`.

---

## Reading and writing binary in a Code node

Most workflows never need to crack open the bytes — they just pass binary through to a consumer (email attachment, file upload, Slack file). Most byte jobs have a native node: **Extract From File** (CSV, XLSX, PDF text, JSON, plain text → items or a field), **Convert To File** (items → CSV / XLSX / JSON / text file), **Crypto** (hash a file with `binaryData: true`), **Compression** (zip / gzip). Read or write raw bytes in a Code node only when no node handles the format, with a `Why Code:` note.

**Read** with `getBinaryDataBuffer` — do not try to base64-decode `$binary.<key>.data` by hand:

```javascript
// Code node, "Run Once for Each Item"
const buffer = await this.helpers.getBinaryDataBuffer(0, 'data'); // (itemIndex, propertyName)
const text = buffer.toString('utf-8');
const length = buffer.length;

return [{
  json: { ...$json, length },
  binary: $input.item.binary,   // pass the binary through, or it's gone
}];
```

**Write** by building the slot yourself — base64 the bytes plus a mime type and file name:

```javascript
const text = 'Hello, world!';
return [{
  json: { ok: true },
  binary: {
    report: {
      data: Buffer.from(text).toString('base64'),
      mimeType: 'text/plain',
      fileName: 'report.txt',
      fileExtension: 'txt',
    },
  },
}];
```

The Code-node sandbox, helpers, and execution modes are the domain of **ai-lead-n8n-javascript** — use that for the language-level detail. The one binary-specific thing to remember here: a Code node that returns `[{ json: {...} }]` without re-attaching `binary` **silently drops the file**. See `BINARY_BASICS.md`.

---

## Keeping binary alive across transforms

JSON-only nodes — Edit Fields (Set), Code, IF, and others — can drop the `$binary` slot from their output. The workflow validates clean and runs without error; the file just isn't there downstream when the email node goes to attach it.

Two ways to keep it:

- **Pass-through option on the transforming node.** Edit Fields has `includeOtherFields`; a Code node can return `binary: $input.item.binary` explicitly. Cheapest fix when it's available.
- **Fan out and Merge by position.** Route the source into both the transform and a bypass branch, then recombine with a Merge in `combineByPosition` mode. The JSON comes from the transform side, the binary survives on the bypass side.

```
[Source with binary] ─┬─→ [Edit Fields: change JSON] ─┐
                      │      (binary stripped here)     ├─→ [Merge: combineByPosition] ─→ [Email: attach]
                      └──────────────────────────────────┘
                          (bypass — binary passes through untouched)
```

`combineByPosition` pairs item N from each input, so the field counts must line up. The connection wiring and the alternatives for many-strip-point chains (upload-early, sub-workflow) are in `MERGE_FOR_CONTEXT.md`.

---

## The agent-tool binary boundary

Only relevant when the lead says an AI connection is available in their n8n; see `ai-lead-workflow-n8n`.

This is the sharpest edge. An AI Agent talks to its tools (Custom Code Tool, Call n8n Workflow Tool, HTTP Request Tool) over JSON. Binary does not fit through that pipe in either direction. The fix is the same shape both ways: **stage the bytes in storage, pass a key/URL through JSON, fetch on the other side.**

**Inbound — a user uploads a file the agent's tool must operate on:**

1. The chat trigger gives you a `files[]` array. Split it out and upload each file to private storage under a hashed key.
2. Re-merge that branch before the agent runs (it's a synchronization barrier, not decoration), and set `executeOnce: true` on the agent so N files don't trigger N agent runs.
3. Inject the keys into the agent's system prompt, listing both the original name (human context) and the storage key (what the tool needs), with an explicit "use EXACTLY this key".
4. The tool receives the key as a string argument and downloads the file from storage itself.

**Outbound — a tool generates a file the agent must return:**

1. The tool sub-workflow generates the binary, uploads it to storage, and returns JSON like `{ "ok": true, "key": "...", "url": "https://...", "mimeType": "image/png" }`.
2. The agent embeds the URL in its reply (or passes the key to another tool).

`passthroughBinaryImages: true` on the agent only changes what the **LLM sees** for vision — it does **not** let tools receive the file, and it's image-only (no PDFs, audio, or video). You still need the upload-and-pass-key pattern for any tool. Full patterns, hash strategy, storage choices, and the long-running-tool variant are in `AGENT_TOOL_BINARY.md`.

> The AI-Agent-with-tools shape is in **ai-lead-n8n-patronen**.

---

## The CDN requirement for chat surfaces

Only relevant when a chat app (Teams, Slack, …) is connected; the leads have no such connection yet.

When a workflow generates an image and the user wants it shown inside a chat message:

- **Binary on the item isn't enough.** The chat client renders messages that reference images by URL (or pushes bytes through the platform's own file-upload API). It never reads `$binary`.
- **The bytes have to live somewhere a URL can fetch over HTTPS.** Upload to an object store or drive first, then embed the returned URL.
- **n8n has no built-in CDN.** The user provides the storage.

Ask which storage they already use rather than defaulting to S3 — object storage (S3, R2, GCS, Azure Blob, Backblaze B2, Supabase Storage) and drive-style services (Dropbox, Google Drive, OneDrive, Box) all work and all change the URL shape. Cloudflare R2 is the lowest-friction starting point if they have nothing. For sensitive content, use a signed URL with an expiry rather than a permanently public one. See `CDN_REQUIREMENT.md`.

---

## What's NOT available

- **`$fromAI()` cannot carry binary.** It fills tool parameters with strings, numbers, booleans, and objects — never file bytes. Pass a storage key instead.
- **Tool arguments and returns are JSON only.** There is no "binary parameter" on an agent tool, in or out.
- **n8n ships no CDN or public file host.** Serving a file over a URL is always something the user's storage does, not n8n.
- **`getBinaryDataBuffer` is a Code-node helper.** It isn't available in the Custom Code Tool sandbox.

---

## Where Data Tables live

For persistent tabular storage — reference-counting staged files, tracking which keys are live, dedup — use an n8n Data Table (the Data Table node is in **ai-lead-n8n-blokken**). This skill does not cover Data Tables.

---

## Anti-patterns

| Anti-pattern | What goes wrong | Fix |
|---|---|---|
| Reading file contents from `$json` | Bytes live in `$binary`; `$json` is empty or metadata only | Read `$binary.<key>`, or `getBinaryDataBuffer` in a Code node |
| HTTP download without `responseFormat: "file"` | Bytes arrive as mangled text in `$json`, not clean binary | Set `responseFormat: "file"` on the HTTP Request node |
| Code node returns `[{json:{...}}]`, no `binary` | The file is silently dropped downstream | Re-attach `binary: $input.item.binary` in the return |
| JSON transform (Edit Fields/IF) eats the binary | Email/upload node finds nothing to attach | Pass-through option, or fan out + Merge by position |
| Passing an uploaded file into a tool via `$fromAI` | `$fromAI` can't carry binary; the tool gets nothing | Pre-stage to storage, inject the key in the system prompt, tool fetches by key |
| Assuming `passthroughBinaryImages` lets tools see the file | It only affects what the LLM sees, and only for images | Still need the upload-and-pass-key pattern for tools |
| Tool returns raw binary to the agent | Tool output is JSON; bytes don't survive (and bloat context) | Upload, return `{ key, url }` in JSON |
| Posting `$binary` to a chat surface and expecting an image | Chat clients render by URL, not raw bytes | Upload to storage/CDN, embed the URL or use the platform file API |
| Hardcoding base64 in a Code node | Huge workflow JSON, slow, leaky | Reference via `$binary`, or upload and reference by URL |

---

## Reference files

| File | Read when |
|---|---|
| `BINARY_BASICS.md` | First time handling binary, or reading/writing the `$binary` slot, mime types, size limits |
| `AGENT_TOOL_BINARY.md` | Only with an AI connection: an agent tool needs an uploaded file, or produces one — the boundary in either direction |
| `MERGE_FOR_CONTEXT.md` | Binary disappears after a JSON transform and you need to re-attach it |
| `CDN_REQUIREMENT.md` | Only with a chat app connected: showing images in a chat surface or anywhere that needs URL-referenced images |

---

## Integration with Other Skills

**ai-lead-workflow-n8n**: the build skill — how the import file is laid out (ids, positions, notes, webhookId) and how the lead imports and runs it.

**ai-lead-n8n-javascript**: the Code node is where you read/write raw bytes (`getBinaryDataBuffer`, `Buffer.from(...).toString('base64')`). That skill owns the sandbox, helpers, and execution-mode detail — this skill owns the rule that binary must be re-attached on return.

**ai-lead-n8n-patronen**: the agent-tool binary boundary sits inside the AI-Agent-with-tools pattern; the CDN flow is a generate → upload → reply chain.

**ai-lead-n8n-blokken**: `responseFormat`, `binaryPropertyName`, `includeOtherFields`, `binaryPropertyOutput` are all conditional fields — check the exact names on the node in the user's n8n version (open the node after import).

**ai-lead-n8n-expressies**: addressing `$binary.<key>.fileName` vs `$json.body` (webhook uploads in particular) is expression territory.

The Custom Code Tool sandbox (AI agents only) is narrower than the Code node — no `$binary`, no `getBinaryDataBuffer`, no `$fromAI` — so a tool that needs a file gets it through this skill's storage-key pattern.

---

## Verifying binary survived

A stripped binary slot gives no error — it's a silent failure. Confirm it ran correctly:

1. Import the file in n8n and run it (Execute workflow, or Execute step).
2. Open each node and check the INPUT and OUTPUT panels — the Binary tab shows the file and the property name, with its metadata even if the file is too large to preview.
3. The node where `binary` last appears is the node before the strip. That's where the pass-through or Merge goes.

---

## Quick Reference Checklist

- [ ] File contents read from `$binary.<key>` — never `$json`
- [ ] HTTP downloads use `responseFormat: "file"`
- [ ] Code nodes re-attach `binary` on return when the file must continue
- [ ] JSON transforms either pass binary through or Merge it back (`combineByPosition`)
- [ ] No attempt to pass binary into/out of an agent tool — keys/URLs through JSON instead
- [ ] `passthroughBinaryImages` used only for LLM vision, not as a tool channel
- [ ] Chat-surface images uploaded to storage; the URL is embedded, not the bytes
- [ ] Storage backend chosen with the user (not defaulted to S3); signed URLs for sensitive content
- [ ] Binary presence confirmed by inspecting the execution, not by validation

---

**Remember**: two slots, side by side. Data rides in `$json`, files ride in `$binary` — and the moment a file has to cross an agent tool or reach a chat surface, it travels as a URL, not as bytes.
