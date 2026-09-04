# Bouwstenen die het script kent

Elke bouwsteen is geoogst uit een export die in Lleverage heeft gedraaid. Status:
**bewezen** = in productie of live-getest, **gezien** = uit een geïmporteerde export, nog
niet door ons in een echte run bewezen.

| plan-soort | Lleverage-node | status |
|---|---|---|
| trigger `mail` | `integrationV2Trigger` (Outlook, nieuwe mail) | bewezen |
| trigger `schedule` | `scheduleTrigger` | bewezen |
| trigger `app` | `appTrigger` + `form` | gezien |
| trigger `api` | `apiCallTrigger` | gezien |
| `llm` | `llm` met `_jsonOutput` | bewezen |
| `extract` | `extract` | gezien |
| `js` | `javascript` | bewezen |
| `branch` | `branch` | bewezen |
| `mens_vraag` | `requestInput` | gezien |
| `mens_keur` | `requestApproval` | gezien |
| `mail_sturen` | `external` microsoft-outlook_send-email | bewezen |
| `mail_beantwoorden` | `external` microsoft-outlook_reply-to-email | bewezen |
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
