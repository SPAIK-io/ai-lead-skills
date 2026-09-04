# Bouwstenen die het script kent

Elke bouwsteen is geoogst uit een export die uit Lleverage kwam. Status:
**bewezen** = in productie of live-getest, **gezien** = de vorm komt uit een export die ooit
in Lleverage stond, maar wij hebben hem nog niet zelf geïmporteerd en gedraaid. Voor "gezien"
loopt een importsessie (testflows T1 t/m T7); tot die klaar is, zijn `.data`, `.record` en
`.index` bij die bouwstenen aannames.

| plan-soort | Lleverage-node | status |
|---|---|---|
| trigger `mail` | `integrationV2Trigger` (Outlook, nieuwe mail); velden `.body` `.subject` `.from` `.files` | bewezen |
| trigger `schedule` | `scheduleTrigger` | bewezen |
| trigger `app` | `appTrigger` + `form` | bewezen (T1, 4 sep) |
| trigger `api` | `apiCallTrigger` | gezien |
| `llm` | `llm` met `_jsonOutput` | bewezen |
| `extract` | `extract`; geeft ook `.confidence` en `.missingFields` | bewezen (T1, 4 sep) |
| `js` | `javascript` | bewezen |
| `branch` | `branch` | bewezen |
| `mens_vraag` | `requestInput` | gezien |
| `mens_keur` | `requestApproval` | gezien |
| `mail_sturen` | `external` microsoft-outlook_send-email | bewezen |
| `mail_beantwoorden` | `external` microsoft-outlook_reply-to-email; `messageId` = `{{Mailbox.body.id}}` | bewezen (2.21 t/m 2.28), T7 test opnieuw |
| `slack` | `external` slack_send-channel-message | bewezen |
| `http` | `httpRequest` | bewezen |
| `tabel_schrijven` / `tabel_lezen` | `dataTablesCreate` / `dataTablesFind` | gezien |
| `output` | `output` | bewezen |

Niet in het script: forEach met subworkflow, databaseQuery (eigen database via tunnel),
PDF-naar-tekst, en alle andere integraties. Die komen erbij zodra ze bewezen zijn.

Omgevingswaarden die het script niet kan weten en als `<KIES NA IMPORT>` achterlaat:
connection-id's (Outlook, Slack), mailbox en map, tabel- en project-id's, Slack-kanaal.
Het model-id (46 = Claude Sonnet 4.6, 48 = GPT-5.4 mini) is per Lleverage-organisatie;
klopt hij niet, dan kies je het model in de node opnieuw.
