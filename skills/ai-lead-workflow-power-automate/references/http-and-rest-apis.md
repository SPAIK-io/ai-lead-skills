# HTTP calls and REST APIs

## Contents
- HTTP action essentials
- Parsing responses
- Paging through a REST API
- External systems calling a flow

## HTTP action essentials

- Premium connector. In client tenants check DLP: the HTTP connector may be blocked or limited to allowed endpoints (alm-and-governance.md).
- Base URLs and credentials come from environment variables (secrets as Key Vault-backed secret environment variables), never hardcoded.
- Authentication options on the action: Basic, Client certificate, Active Directory OAuth (client credentials against Entra ID), Raw (custom `Authorization` header). Use a dedicated API account with least privilege.
- Set `Accept: application/json`; for bodies `Content-Type: application/json`.
- Timeout: a synchronous call must complete within 120 seconds. For APIs returning `202` + `Location`, keep *Asynchronous pattern* on (Settings) so the action polls; turn it off when the API's 202 means "accepted, done".
- Retry policy: default retries 408/429/5xx. Set **None** on POSTs that create records when a timeout-then-retry could create duplicates.
- A 4xx/5xx fails the action - downstream checks need run-after *has failed* (error-handling.md).
- Typical status meaning: `400` bad field/query or missing mandatory field, `401` wrong credentials, `403` missing permission, `404` unknown ID, `409` conflict/lock, `429` throttled.
- Prefer a custom connector when the same API is used across many flows (shared auth, typed actions, cleaner DLP classification).
- Request only the fields the flow needs when the API supports it (`$select`, `fields=`), and fetch reference/lookup lists once per run instead of per item.

## Parsing responses

- *Parse JSON* with Content `body('HTTP_-_…')`; generate the schema from a real response.
- Then edit the schema: remove optional fields from `required`, allow nulls with `"type": ["string", "null"]`. Otherwise the first missing or null field fails the run.
- For one or two fields skip Parse JSON: `body('HTTP_-_…')?['id']`.
- An empty body (204) breaks Parse JSON - branch on the status code first.

## Paging through a REST API

The built-in Pagination setting only follows `@odata.nextLink`. Other paging schemes need a loop:

```
Initialize variable - vOffset (Integer, 0)              ← top level
Initialize variable - vResults (Array, [])              ← top level
Initialize variable - vMorePages (Boolean, true)        ← top level
Do until - pages     condition: @not(variables('vMorePages'))   Count 200, Timeout PT30M
   HTTP - get page        uri: …?offset=@{variables('vOffset')}&limit=<page size>
   Compose - page items   if(equals(outputs('HTTP_-_get_page')?['statusCode'], 204), createArray(), body('HTTP_-_get_page'))
   Apply to each - page item   (sequential)   over outputs('Compose_-_page_items')
      Append to array variable - vResults: items('Apply_to_each_-_page_item')
   Set variable - vMorePages: equals(length(outputs('Compose_-_page_items')), <page size>)
   Increment variable - vOffset by <page size>
```

*Set variable* can't reference its own variable, hence *Append to array variable*. Adapt the "more pages" test to the API: a next-link or cursor present, returned count equals page size, or a status/header the API documents for partial results.

## External systems calling a flow

- If the caller can send an Entra ID bearer token, use *Who can trigger the flow: Any user in my tenant / Specific users* (triggers.md).
- If it can't (many SaaS webhooks), the trigger needs *Anyone*: protect it with a shared-secret header checked as the first step and keep the URL out of exports and tickets.
- Respond quickly (Response action early, or no Response → 202) so the caller doesn't wait on slow work.
- Let the caller send IDs and fetch details via the API in the flow, rather than pushing large payloads.
