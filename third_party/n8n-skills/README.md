# Bron: czlonkowski/n8n-skills

Vijf skills in deze plugin zijn gebaseerd op de open-source skills van Romuald Członkowski.

- Bron: https://github.com/czlonkowski/n8n-skills
- Versie: plugin `n8n-mcp-skills` 1.37.1, commit `e037563` (main, 24 oktober 2026)
- Licentie: MIT, zie `LICENSE` in deze map. De bron bevat ook materiaal van n8n-io/skills onder
  Apache 2.0; zie `NOTICES` en `NOTICES-APACHE-2.0.txt`. Dat materiaal (de hooks) nemen wij niet over.

## Wat we overnamen

| Bron | In deze plugin |
|---|---|
| `skills/n8n-expression-syntax` | `skills/ai-lead-n8n-expressies` |
| `skills/n8n-node-configuration` | `skills/ai-lead-n8n-blokken` |
| `skills/n8n-workflow-patterns` | `skills/ai-lead-n8n-patronen` |
| `skills/n8n-code-javascript` | `skills/ai-lead-n8n-javascript` |
| `skills/n8n-binary-and-data` | `skills/ai-lead-n8n-bestanden` |

Niet overgenomen: de hooks, de router `using-n8n-mcp-skills`, de MCP-configuratie en de overige
skills (onder andere n8n-mcp-tools-expert, n8n-validation-expert, n8n-agents, n8n-error-handling).

## Wat SPAIK veranderde

- Nieuwe namen, ook in `name:` in de frontmatter, en een nieuwe `description:` die past bij een
  AI lead die een n8n-flow als importbestand bouwt.
- Alle instructies over MCP-tools eruit (zoals get_node, validate_node, validate_workflow,
  search_nodes, de n8n_*-tools, templates en hooks). In plaats daarvan: het bestand importeren in
  n8n, draaien, en in het blok kijken wat er binnenkomt en uitgaat.
- Verwijzingen naar skills die we niet meenemen eruit, of de kern in één zin; verwijzingen tussen
  de vijf skills naar de nieuwe namen. De README per skill is weggelaten.
- Toegevoegd: een verwijzing naar `ai-lead-workflow-n8n` voor de bouwstenen die op n8n Cloud 2.47
  bewezen werken, de tabel "Which node for which job" in `ai-lead-n8n-blokken` (uit de router), de
  regel dat een codeblok uitlegbaar is en een extra IT-check krijgt, en de bewezen vorm van een
  formulier met csv-upload in `ai-lead-n8n-bestanden`.
- Bovenaan elke SKILL.md staat: "Gebaseerd op czlonkowski/n8n-skills (MIT), commit e037563,
  aangepast door SPAIK: zonder MCP, voor flows als importbestand."

De n8n-kennis zelf is zoveel mogelijk ongewijzigd en in het Engels gebleven.
