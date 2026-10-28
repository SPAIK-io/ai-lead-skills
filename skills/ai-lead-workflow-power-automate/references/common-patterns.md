# Common connector patterns

## Contents
- SharePoint
- Outlook
- Teams
- Dataverse
- Excel Online
- Approvals
- Files and PDF
- CSV

HTTP/REST calls are in http-and-rest-apis.md; retry loops in error-handling.md.

## SharePoint

**Get items**
- Site Address / List Name from environment variables.
- Filter Query uses **internal** column names (column settings URL → `Field=`). Spaces appear as `_x0020_`.
- Operators: `eq`, `ne`, `gt`, `ge`, `lt`, `le`, `and`, `or`, `startswith(Title,'abc')`, `substringof('abc',Title)`. Choice: `Status eq 'Open'`. Person: `Author/EMail eq 'x@y.nl'`. Lookup: `Department/Id eq 5`.
- Lists over 5,000 items: filter on **indexed** columns, or the query fails on the list view threshold.
- Top Count + Pagination when more than one page is expected (performance.md).

**Create / update item**
- Person fields: `<Field> Claims` = the user's email (or `i:0#.f|membership|user@domain`).
- *Update item*: empty fields stay unchanged; required columns (Title) must still be filled. To clear a field send `null` via an expression.
- Partial update without required fields, or without creating a new version / changing Modified By: *Send an HTTP request to SharePoint* → `POST _api/web/lists/getbytitle('List')/items(<id>)/validateUpdateListItem` with
  ```json
  { "formValues": [ { "FieldName": "Status", "FieldValue": "Closed" } ], "bNewDocumentUpdate": true }
  ```
  (`bNewDocumentUpdate: true` skips the new version.)

**Which columns changed** → *Get changes for an item or a file (properties only)*, see triggers.md → loop-back.

**Attachments / files** - list attachments: *Get attachments* + *Get attachment content*. Document libraries: *Get file content* / *Get file content using path*.

## Outlook

- HTML email: *Send an email (V2)*, body is HTML in the new designer's code view; put tables built with *Create HTML table* in it.
- From a shared mailbox: *Send an email from a shared mailbox (V2)* (connection user needs Send As).
- Attachments array: `[{"Name": "report.pdf", "ContentBytes": @{body('Get_file_content')?['$content']}}]` - the connector file object is `{"$content-type": …, "$content": "<base64>"}`; pass `$content`, or the whole file body in the designer's attachment field.
- Incoming shared mailbox: *When a new email arrives in a shared mailbox (V2)*.

## Teams

- *Post message in a chat or channel*, Post as *Flow bot* for system messages, *User* when it should come from a person.
- Adaptive cards: *Post adaptive card in a chat or channel*; *Post adaptive card and wait for a response* for simple in-chat approvals. Design at adaptivecards.io/designer.
- @mention: *Get an @mention token for a user* → insert `outputs('Get_an_@mention_token_for_a_user')?['body/atMention']` in the message.

## Dataverse

- *List rows*: Select columns (logical names, comma separated), Filter rows (OData), Expand Query for related tables, or FetchXML for complex joins/aggregates.
- Lookup on create/update: value `/accounts(<guid>)` - entity set name (plural) + GUID.
- Choice columns return the integer value; the label is in `…@OData.Community.Display.V1.FormattedValue`.
- Atomic multi-row writes: *Perform a changeset request*.
- *Search rows* (Dataverse search must be enabled) for fuzzy text search across tables.

## Excel Online (Business)

- Data must be in a **table**; reference the table by name, not ID, when files are replaced.
- *List rows present in a table* returns 256 rows by default - enable Pagination. Set DateTime Format = ISO 8601, otherwise dates come as serial numbers.
- Slow and lock-prone with concurrent writes; for anything multi-user prefer SharePoint or Dataverse.

## Approvals

- *Start and wait for an approval*: types *Approve/Reject - First to respond*, *Approve/Reject - Everyone must approve*, *Custom responses - Wait for one / for all*.
- Outcome: `body('Start_and_wait_for_an_approval')?['outcome']`; comments in `?['responses']`.
- Approvers need no Power Automate licence. Pending approvals time out after 30 days with the run; for escalations set Settings → Timeout on the approval action (e.g. `P3D`) and add an escalation branch with run-after *has timed out*.

## Files and PDF

- HTML → PDF: *Create file* (`.html`) in OneDrive → *Convert file* (OneDrive, target PDF) → delete the temp file.
- Word template: *Populate a Microsoft Word template* (premium) → *Convert Word Document to PDF*.
- File names: `concat('report-', formatDateTime(utcNow(), 'yyyyMMdd-HHmm'), '.pdf')`; strip `\ / : * ? " < > |` from user input.

## CSV

- Generate: *Create CSV table* (Custom columns to control headers). Excel opens UTF-8 CSV with a `;` separator best in Dutch locale - replace commas or build lines with `join()`.
- Parse: split on `decodeUriComponent('%0D%0A')` (Windows files) or `%0A`, `skip(…, 1)` for the header, then Select with `split(item(), ';')[0]`, `split(item(), ';')[1]`… - no per-row loop needed. Quoted fields containing separators need a proper parser (Office Script or a small function), not split.
