# Naming conventions

Apply from the first action; renaming later breaks hand-written expression references.

## Flows

Pattern: `[Group] - Verb Noun (trigger context)`

- `Facilities - Create Request from Form (when item created)`
- `HR - Sync Candidates to Dataverse (daily 06:00)`
- `Log Error (child flow)`

Agent-called flows: the agent reads the flow name as the tool name, so use a plain verb-noun without trigger context: `Create service request`, `Get order status`.

Avoid: `Flow 1`, names without a verb, mixed languages within one project.

## Triggers

| Trigger | Pattern | Example |
|---|---|---|
| SharePoint | `When item is <event> - <list>` | `When item is created - Vacation Requests` |
| Dataverse | `When row is <event> - <table>` | `When row is added - Contacts` |
| Recurrence | `Recurrence - <schedule>` | `Recurrence - weekdays 08:00` |
| HTTP | `When HTTP request received - <purpose>` | `When HTTP request received - order webhook` |
| Manual / child | `Manually triggered - <purpose>` | `Manually triggered - log error` |
| Agent | `When an agent calls the flow - <action>` | `When an agent calls the flow - create incident` |

## Actions

Pattern: `<default action name> - <purpose>`. The default name keeps the action type visible; ` - ` is the separator (the new designer rejects `:`).

- `Send an email (V2) - notify requester`
- `Get items - open tickets for current user`
- `HTTP - get order details`
- `Apply to each - candidate`

Keep the purpose part short (whole name under ~60 characters): every expression reference repeats it, e.g. `body('HTTP_-_get_order_details')`. Never leave defaults like `Compose 3`.

## Scopes

`Try`, `Catch`, `Finally`; for multi-stage flows `Try - fetch data`, `Try - write results`.

## Variables

`v` + camelCase: `vErrorMessage`, `vRetryCount`, `vIncidentId`. No type in the name.

## Connection references

`<Connector> - <Solution> - <Purpose>`: `SharePoint - HR Portal - Vacation Requests`. Rename the auto-generated ones before the first export.

## Environment variables

Display name in plain words; schema name = publisher prefix + lowercase with underscores: `abc_api_base_url`, `abc_sharepoint_site_url`, `abc_admin_mailbox` (prefix `abc`). The name describes the value, never contains it.

## Publisher prefix

Applies to schema names of solution components (Dataverse tables/columns, environment variables, connection references). Flows don't get it in their display name. Use one prefix per client, never the default `cr`.

## Notes on actions

Use the action's note (… menu → Add a note) for the *why*: workarounds, ticket numbers, known API quirks.

## Pre-production check

- [ ] Flow name has group, verb and trigger context (or plain verb-noun for agent flows)
- [ ] No default action names left
- [ ] Variables `v` + camelCase, all initialised at top level
- [ ] Scopes named Try / Catch / Finally
- [ ] Connection references renamed
- [ ] No hardcoded URLs, emails or GUIDs - environment variables instead
