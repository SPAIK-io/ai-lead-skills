# Working with flow JSON and solution files

## Contents
- Where flow JSON comes from
- Solution zip layout
- Reviewing a flow
- Editing a flow in a solution zip (validation loop)
- Lint script reference

## Where flow JSON comes from

| Source | Contains | Use for |
|---|---|---|
| *Peek code* on an action | That action's inputs/settings | Exact expression text and paths |
| Copied action (designer copy/paste) | One action or Scope with children | Moving logic between flows in the designer |
| Exported solution .zip → `Workflows/<Name>-<GUID>.json` | Full definition + connection references | Full review, bulk edits, linting |

When the user shares JSON, treat it as the source of truth: read all of it, refer to actions by their JSON keys (`Get_items_-_open_requests`), and don't assume settings that aren't in it (absent `runtimeConfiguration.concurrency` = defaults).

## Solution zip layout

```
solution.zip
├── [Content_Types].xml
├── customizations.xml
├── solution.xml                 ← <Version>1.0.0.3</Version>
└── Workflows/
    └── <FlowName>-<GUID>.json   ← properties.definition (triggers, actions)
                                    properties.connectionReferences
```

Inside a definition: `triggers` and `actions` are objects keyed by name; each action has `type` (`OpenApiConnection`, `Http`, `Scope`, `Foreach`, `Until`, `If`, `Switch`, `InitializeVariable`, `Terminate`, `Response`, …), `inputs`, `runAfter` (`{"Try": ["Failed", "TimedOut"]}`), and children under `actions` / `else.actions` / `cases.<case>.actions` / `default.actions`. Settings sit in `runtimeConfiguration` (concurrency, pagination) and `inputs.retryPolicy`.

## Reviewing a flow

1. Run the linter (below) and read its findings.
2. Walk the definition top-down against references/hard-rules.md and the naming convention.
3. Report findings grouped as **Errors** (will fail or misbehave), **Risks** (performance, silent failures, security), **Hygiene** (naming, hardcoded values). For each: action key, problem, concrete fix.

## Editing a flow in a solution zip (validation loop)

Use when the user attaches an exported **unmanaged** solution and wants changes applied.

```
Solution edit:
- [ ] 1. Unzip to a working folder; never edit the original upload
- [ ] 2. Locate the flow in Workflows/; edit only properties.definition (and connectionReferences only when adding a connector)
- [ ] 3. Run: python scripts/lint_flow.py <unzipped folder>
- [ ] 4. Errors? Fix, rerun step 3. Continue only when there are no errors
- [ ] 5. Bump <Version> in solution.xml
- [ ] 6. Zip the folder CONTENTS (not the folder): cd <folder> && zip -r -X ../<Solution>_<version>.zip .
- [ ] 7. Deliver with import instructions: import into DEV as unmanaged, check connection references, turn the flow on, test
```

Never change: GUIDs, file names in `Workflows/`, `connectionReferenceLogicalName` values, or the publisher. A new connector needs a matching connection reference in `customizations.xml` - prefer letting the user add that action in the designer, then edit the exported result.

## Lint script reference

`scripts/lint_flow.py` checks a flow definition for the rules in references/hard-rules.md. Run it - don't read it - unless it breaks.

```
python scripts/lint_flow.py <path>          # .zip, unzipped solution folder, Workflows/*.json, or a bare definition .json
python scripts/lint_flow.py <path> --json   # machine-readable output
```

No dependencies beyond the Python 3 standard library. Exit code 1 when errors are found.

Checks:
- **Errors**: Initialize variable outside the top level; Terminate inside a loop; trigger condition without leading `@`; variable written inside a parallel Apply to each; agent flow Respond actions with different outputs; asynchronous Response in an agent flow; Catch-style Scope whose run-after lacks Failed.
- **Warnings**: no failure handling at all; failure handling but no Terminate Failed; Apply to each with connector/HTTP calls; Do until without explicit limits; HTTP POST with default retry; default (unrenamed) action names; `:` in action names; hardcoded URLs, email addresses or GUIDs; trigger concurrency enabled (irreversible).
