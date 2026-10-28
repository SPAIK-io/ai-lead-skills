# Debugging

## Contents
- Triage checklist
- Reading run history
- Compose as breakpoint
- Error messages and what they mean
- "Works for me, not for others"
- Trigger doesn't fire
- Agent-called flows
- Resubmit vs test
- When stuck

## Triage checklist

```
Debug:
- [ ] 1. Is there a run at all? No run → "Trigger doesn't fire"
- [ ] 2. Open the failed run; find the FIRST failed action inside the deepest Scope/loop
- [ ] 3. Read its INPUTS (what it received), then its outputs/error
- [ ] 4. Trace the bad input back to the action/expression that produced it
- [ ] 5. Fix once, then Resubmit the failed run to confirm
```

Ask the user for: the error text from run history, the inputs of the failing action, and the action's Peek code - before guessing.

## Reading run history

- Run history keeps 30 days.
- A failed Scope or loop only says `ActionFailed`; expand it to the inner action that failed. In loops, page through iterations ("Show only failed iterations" where available).
- Skipped actions (grey) are consequences, not causes.
- Duration per action pinpoints slow steps (performance.md).
- *Peek code* (… menu on an action) shows the stored JSON: exact expression text and real property paths.

## Compose as breakpoint

Add `Compose - debug <what>` with the suspect sub-expression, run, read the output. For chained expressions, one Compose per step. Remove before production, or keep behind a `vDebug` environment variable check.

## Error messages and what they mean

| Message (abridged) | Meaning → fix |
|---|---|
| `InvalidTemplate … cannot be evaluated because property 'X' doesn't exist, available properties are …` | Path wrong or field missing → use `?['X']`, check the listed properties for the real name |
| `… property 'X' cannot be selected. Property selection is not supported on values of type 'String'` | The value is JSON text → `json(...)` first; or it's an array → index `[0]` / Filter array |
| `… property 'X' cannot be selected … type 'Array'` | You indexed an array like an object → `first(...)?['X']` or loop |
| `The template language function 'int' was invoked with a parameter that is not valid` | Empty or decimal/Dutch-formatted text → guard and normalise (expressions.md) |
| `The template language function 'json' expects … ` / `'length' expects …` | Null or wrong type passed → `coalesce()` / `empty()` first |
| `ActionFailed. An action failed. No dependent actions succeeded.` | Container status → expand Scope/loop for the real error |
| `… is skipped: the 'runAfter' condition for action 'Y' is not satisfied. Expected status values 'Succeeded' and actual value 'Failed'` | Upstream failure; set run-after on purpose or fix Y |
| `ConnectionAuthorizationFailed` / `Unauthorized` on a connector | Connection expired, owner left, password changed, or connection reference points to the wrong connection → re-authenticate / remap |
| `403 Forbidden` (SharePoint `UnauthorizedAccessException`) | The connection's account lacks rights on that site/item → open it in a browser as that account |
| `429 Too Many Requests` | Throttling → fewer calls, lower concurrency, batching (performance.md) |
| `BadGateway` / `GatewayTimeout` after ~120 s | Synchronous call too slow → async pattern, smaller requests |
| `CannotDisableTriggerConcurrency` | Trigger concurrency can't be switched off → delete and re-add the trigger |
| Initialize variable can't be added/saved inside a Scope, Condition or loop | It's only allowed at the top level → move it before `Try` |
| Flow save error on an expression | Unbalanced parentheses/quotes, a function typo, or a reference to a renamed/removed action |

## "Works for me, not for others"

Test runs and normal runs use the same connections. Differences come from:
- **Instant flows shared with run-only users**: each connection is either *Provided by run-only user* (runs as them; they need access and, for premium connectors, a licence) or *Use this connection* (runs as the embedded connection).
- **Agent-called flows**: always run with the flow's connections; the user's own rights aren't applied (agent-flow-integration.md).
- **Different environment / connection reference mapping** after import (alm-and-governance.md).
- **Data-level permissions**: the item exists but the connection's account can't see it.

## Trigger doesn't fire

1. Flow turned on? (Imported flows can be off when connection references weren't mapped.)
2. Trigger condition false? Copy it into a Compose in a test flow and evaluate against a real item.
3. Pointing at the right site/list/table/environment?
4. SharePoint polling delay - wait a few minutes before concluding.
5. Dataverse: Select columns / Filter rows / Scope too narrow?
6. HTTP trigger: caller uses the current URL and passes authentication per the trigger's *Who can trigger* setting? Callers get 401/403 when the auth setting doesn't match.
7. Was the flow suspended? Repeated trigger failures, licence or DLP changes suspend flows - check the owner's mailbox and the flow details page.

## Agent-called flows

1. **Flow run history first**: no run → the agent didn't call it (tool selection/description). Run with wrong inputs → the agent filled them wrongly (descriptions/examples). Run with right inputs but wrong outputs → flow bug.
2. **Copilot Studio test pane activity map**: which tool was selected, with which inputs, what came back.
3. Error code 3000 / timeout → see agent-flow-integration.md → Common failures.

## Resubmit vs test

- **Resubmit** (run history): replays the original trigger data with the **current** flow definition - ideal after fixing a bug.
- **Test → Manually / with recently used trigger data**: quick iteration while building.
- A Resubmit re-executes all actions, including emails and creates. Check side effects before bulk resubmits.

## When stuck

1. Minimal repro: new flow, only the failing action with hardcoded inputs. Works → the bug is in the upstream data.
2. Disable half of the flow (copy, delete actions) and bisect.
3. Check the connector's "Known issues and limitations" on its Learn reference page.
4. Search the exact error text in the Power Platform community forum.
