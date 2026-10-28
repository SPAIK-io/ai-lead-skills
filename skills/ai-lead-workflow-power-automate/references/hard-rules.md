# Hard rules

Verified Power Automate behaviours where generic answers usually go wrong. Apply them to every build card, expression and review.

## Contents
- Rules 1-15
- Verify before stating
- Expression formatting
- Example
- Old patterns

## Rules 1-15

1. **Apply to each runs sequentially by default** (concurrency 1). Parallel only with the loop's own Concurrency control on (max 50) - a different setting from trigger concurrency (rule 8). Never Set/Append/Increment a variable inside a parallel Apply to each - use Compose inside the loop and Select/Filter array afterwards, or keep it sequential.
2. **Initialize variable only at the top level** of the flow - never inside a Scope, Condition, Switch or loop. Declare every variable before the `Try` Scope.
3. **WDL has no inline `filter()` / lambda and no `createObject()`.** Filtering and mapping arrays is done with the **Filter array** and **Select** actions; objects are built as JSON in a Compose. Never invent a function - if unsure it exists, say so and use a Compose-based construction.
4. **A failed HTTP call (4xx/5xx) fails the action**; the next action is skipped unless its run-after includes *has failed*. Any status-code check after an HTTP action needs that run-after.
5. **`coalesce()` only skips `null`** - an empty string `''` passes through. Agent and form inputs often arrive as `''`. Use `if(empty(x), 'default', x)`.
6. **`int('')`, `int('3.5')` and `float('3,14')` throw.** Guard with `empty()` and normalise Dutch decimals before converting.
7. **Trigger conditions are WDL expressions starting with `@`.** Multiple condition rows are combined with AND; put OR logic in one expression.
8. **Trigger concurrency control cannot be switched off** once enabled (only by deleting and re-adding the trigger). Say so before recommending it. It serialises runs; it does not stop a flow from re-triggering itself.
9. **A flow that catches an error still ends as Succeeded.** End the failure path with **Terminate** (Failed). Terminate cannot sit inside Apply to each or Do until.
10. **Action names in expressions:** spaces become `_`, all other characters stay. `Send an email (V2) - notify requester` → `outputs('Send_an_email_(V2)_-_notify_requester')`. Rename actions *before* referencing them.
11. **Agent-called flows:** trigger *When an agent calls the flow*, reply with *Respond to the agent* within **100 seconds**, Asynchronous response **off**, flow stored in a solution in the agent's environment, and every Respond action returns the **same outputs**. Work that takes longer goes *after* the Respond action.
12. **Do until defaults to 60 iterations / 1 hour.** Always set Count and Timeout explicitly.
13. **List actions return one page** unless Pagination is on; the pagination threshold maxes out at 5,000 on the Low performance profile (flows whose owner has only Microsoft 365/seeded or free licensing) or 100,000 on premium-licensed flows.
14. **HTTP action, HTTP trigger, custom connectors, Dataverse and AI Builder actions (e.g. *Run a prompt*) are premium.** AI Builder also needs credits and a Dataverse-enabled environment. Flag licence impact when proposing them.
15. **Run history is kept 30 days.** Anything needed longer is logged by the flow itself.

## Verify before stating

Licensing, prices, Copilot Credit rates, connector throttling limits and preview features change often. Before giving anything the user will repeat to a client or IT on those topics, check learn.microsoft.com with a web search and mention the date checked. Everything else in this skill can be used directly.

## Expression formatting

In the fx editor no `@`; inside a text field use `@{...}`; in code view/JSON a whole-value expression is `"@expr"` (keeps its type) and `"@{expr}"` always produces a string.

## Example

Input: *"Expressie die de vervaldatum 5 werkdagen na vandaag geeft"*
Output: no loop-free WDL function counts working days. Give a Do until that adds one day at a time and skips `dayOfWeek()` 0 and 6 (Count 30, Timeout PT1M), with `vDueDate` initialised at top level - not an invented `addBusinessDays()`.

## Old patterns

Legacy items you may still meet in older flows:

- HTTP trigger URLs on `*.logic.azure.com` moved to new URLs after 2025-11-30; current URLs are on `*.environment.api.powerplatform.com`. Callers with an old URL must be updated with the URL shown in the trigger.
- Copilot flows built with *When Power Virtual Agents calls a flow* / *Return value(s) to Power Virtual Agents* or *Run a flow from Copilot* / *Respond to Copilot* - the current pair is *When an agent calls the flow* / *Respond to the agent*.
- Classic designer naming with colons (`Action: purpose`) - the new designer rejects `:` in action names; use ` - `.
