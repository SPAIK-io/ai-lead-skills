# ALM and governance

## Contents
- Solutions
- Environment variables
- Connection references and service accounts
- DLP
- Promotion: manual and pipelines
- Ownership and access
- Setup for client work
- Typical incidents

## Solutions

Everything going to test/production lives in a solution with a client-specific publisher prefix (never `cr`). Build inside the solution from the first action: adding later means converting connections to connection references by hand.

- Dev: unmanaged. Test/production: **managed** (no direct edits; the dev solution is the source of truth).
- Bump the solution version on every export.
- Export the unmanaged solution to source control as well when the client has a repo (pac CLI `pac solution unpack` gives diffable files).

## Environment variables

For every value that differs per environment: site URLs, list names/IDs, API base URLs, mailboxes, feature flags, `is_production`.

- Types: text, number, yes/no, JSON, data source, **secret** (backed by Azure Key Vault - needs the client's Azure admin).
- Before exporting, **remove the current value** from the solution so dev values don't travel to production; set values during import or in the target environment.
- Not for per-user data or frequently changing values (use a table).
- Reference in flows via the Environment variables section of dynamic content; in code view they appear as `@parameters('<display name> (<schema name>)')`.

## Connection references and service accounts

- Flows point to connection references; each environment maps them to its own connection.
- Test and production connections belong to **service accounts** (`svc-<purpose>-<env>@client.nl`) with least privilege, not to the builder's personal account.
- Each connection reference needs a working connection in the target environment before the flow can be turned on.

## DLP

Data policies (Power Platform admin center) group connectors into Business, Non-business and Blocked per environment. A flow can't combine Business and Non-business connectors; violating flows are suspended - including existing flows when a policy changes.

Recommendations to give the client's admin:
- Business: SharePoint, Outlook, Teams, Dataverse, Approvals, and the custom connectors the solution needs.
- **HTTP connector: use endpoint filtering** (allow only the API hosts the solution calls, e.g. `https://api.example.com/*`) instead of blocking it outright - blocking breaks every API integration.
- Environments hosting Copilot Studio agents: block unauthenticated chat and limit knowledge/actions connectors per the client's policy.
- New connectors default to the policy's default group - review custom connectors after every DLP change.

The builder (AI lead or consultant) usually has no admin rights in the tenant: list required DLP and environment changes as explicit actions for the client's admin.

## Promotion: manual and pipelines

- Start with manual export (managed) → import, mapping connection references and environment variable values in the import wizard.
- Move to **Power Platform pipelines** (dev → test → prod, optional approval gates) when the solution enters long-term operation; setup requires the client's admin and a pipelines host environment.
- After import: check flows are turned on, connection references mapped, environment variable values set.

## Ownership and access

- Cloud flows: owner + co-owners + run-only users. Add a team/security group or the service account as co-owner so the flow survives people leaving.
- Solution-aware flows can have their owner changed to a service account (flow details → Edit owner, or via admin).
- Run-only connection choice: *Provided by run-only user* vs *Use this connection* (debugging.md).

## Setup for client work

```
Client setup:
- [ ] Environments: Dev (sandbox), Test, Production
- [ ] One solution per project, client-specific publisher prefix
- [ ] Connection references for every connector; service accounts in Test/Prod
- [ ] Environment variables for everything environment-specific; current values removed before export
- [ ] DLP checked with the client's admin (HTTP endpoint filtering!)
- [ ] Central error log + Teams channel (error-handling.md)
- [ ] Handover: import steps, env var list, connection owners, monitoring, who to call
```

## Typical incidents

| Symptom | Usual cause |
|---|---|
| Worked yesterday, fails today | Connection expired/revoked, service account password or MFA change, permission removed at the source, DLP change, connector schema change |
| Flow suspended | DLP violation, licence change, repeated trigger failures |
| Flow off after import | Connection references not mapped |
| Dev values in production | Current values exported with the solution |
| Flow runs in the wrong environment | No `is_production` check - add an environment variable and Terminate early when it doesn't match |
