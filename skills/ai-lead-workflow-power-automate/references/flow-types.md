# Flow types: cloud flow vs agent flow vs desktop flow

## Comparison

| | Cloud flow | Agent flow | Desktop flow (RPA) |
|---|---|---|---|
| Built in | make.powerautomate.com | Copilot Studio | Power Automate Desktop (Windows) |
| Interface to systems | Connectors / APIs | Same connectors and WDL as cloud flows | UI automation (clicks, keys, screen scraping) |
| Typical triggers | Automated, instant, scheduled, HTTP, Power Apps | *When an agent calls the flow*, schedule, events | Started by a cloud flow, or manually from the console |
| Billing | Power Automate licensing | Copilot Credits (per 100 actions) | Attended / unattended bot licences |
| Pick when | Reuse, multiple callers, integrations, schedules | Logic used by agents in Copilot Studio, simple licensing for end users | No API exists |

## Decision tree

```
Is a UI the only interface (no API)?
├── yes → desktop flow, orchestrated by a cloud flow
└── no  → Is it only ever called from Copilot Studio agents?
          ├── yes → agent flow
          └── no  → cloud flow in a solution
                    (callable from agents, apps, schedules and other flows)
```

## Licensing model

Structure only - check current prices and rates on learn.microsoft.com before quoting them to a client.

- Standard connectors (SharePoint, Outlook, Teams…) run under Microsoft 365 licences.
- Premium connectors (HTTP, custom connectors, Dataverse, AI Builder, many third-party) need Power Automate Premium (per user) or Process (per flow).
- Agent flows consume Copilot Credits per 100 actions. Runs triggered by *When an agent calls the flow* for a user with a Microsoft 365 Copilot licence are not charged; agent flows with other triggers consume credits at the standard rate. When prepaid credits run out, new agent flow runs are blocked.
- Agent flows can use premium connectors (HTTP, Dataverse…) without Power Automate Premium for end users; the usage is covered by Copilot Credits. Verify before quoting to a client.
- Cloud flows called from an agent use Power Automate licensing, not Copilot Credits.
- Consequence for client work: if only agents call the logic and end users lack premium licences, an agent flow avoids per-user premium licensing; if the same logic also runs from apps or schedules, use a cloud flow and license it accordingly.

## Boundary cases

- **Used by an agent and elsewhere** → cloud flow in a solution with the agent trigger/response pair (see agent-flow-integration.md) plus a separate parent flow for the other entry points, or one cloud flow per entry point calling a shared child flow.
- **Desktop flow from an agent** → agent flow or cloud flow calls the desktop flow. Unattended RPA adds latency; it rarely fits within the 100-second agent response window, so respond first with a tracking ID.
- **Logic Apps** → same engine and WDL. Choose it only when an Azure-oriented team wants infrastructure-as-code deployment (Bicep/ARM/Terraform); for business-owned automation stay in Power Automate.

## Migrating

| From → to | How |
|---|---|
| Non-solution flow → solution-aware | Add to a solution, replace direct connections with connection references. Do it early. |
| Cloud flow → agent flow | Rebuild or convert in Copilot Studio; keep a copy if broader reuse is possible. |
| Cloud flow ↔ desktop flow | No conversion; different tools. |
