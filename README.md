# AI lead skills

Skills voor AI leads bij klanten van [SPAIK](https://spaik.io), of ze nu in Lleverage, n8n of Power Automate bouwen. Begin met "maak een workflow": de startskill vraagt één keer waarin je bouwt en kiest dan de passende bouw-skill; de interview- en blueprint-skills zijn voor iedereen gelijk. Ze volgen de opdracht uit
sessie 1: interviews met de mensen die het werk doen, één blueprint van het werk met de mensen erin,
en één klein stuk dat je als eerste bouwt.

| Skill | Wat hij doet | Roep je aan met |
|---|---|---|
| `ai-lead-interview` | Vooraf: doelzin, themaguide, vragen op maat, kaartje voor tijdens. Achteraf: transcript naar stappen, getallen, omwegen en gaten, plus terugkoppelbericht. | "interview voorbereiden", "transcript verwerken" |
| `ai-lead-blueprint` | Interviewmateriaal naar een service blueprint: de stappen van links naar rechts met de banen eronder (de klant, de lijn van zicht, collega's, waarmee, hoe vaak, hoe lang, wat gaat mis, hoe voelt het en voor wie), hoe vaak keer hoe lang uitgerekend, gaten apart, en waar de tijd, de fout en de dip zitten. Met een invulbare HTML. | "blueprint maken", "procesmap maken" |
| `ai-lead-workflow` | Startskill voor "maak een workflow". Kijkt of vastligt waarin je bouwt (in wat je zegt, of een regel `Wij bouwen in n8n.` in de CLAUDE.md van je map), vraagt het anders één keer, biedt aan het vast te leggen, en gaat door met de bouw-skill van dat platform. | "maak een workflow", "flow bouwen", "eerste prototype" |
| `ai-lead-workflow-n8n` | Zelfde plannetje-stap, maar dan voor n8n: Claude schrijft de flow als bestand dat je importeert (Import from File) en zelf draait. Geen MCP en geen API-sleutel nodig. Data uit een Data Table of een csv via een formulier; elk blok een Nederlandse naam en een notitie in gewone taal. Met de bewezen bouwstenen en een check. | "workflow maken in n8n", "bouw dit in n8n" |
| `ai-lead-n8n-patronen`, `-blokken`, `-expressies`, `-bestanden`, `-javascript` | Hulpskills met n8n-vakkennis voor het bouwen als bestand: opbouw van een flow, welk blok met welke instellingen, `{{ }}`-expressies, bestanden en csv, en codeblokken (alleen als niets anders past). | pakt Claude zelf bij het bouwen |
| `ai-lead-workflow-lleverage` | Van blueprint en één gekozen stap naar een plannetje, en daaruit een importeerbare Lleverage-workflow (gebouwd door een script, dus altijd geldig), met een importchecklist. Kan sinds 0.6.0 ook een databasevraag (alleen lezen, speeltuin). Bèta. | "workflow maken in Lleverage", "bouw dit in Lleverage" |
| `ai-lead-workflow-power-automate` | Zelfde plannetje-stap, maar dan voor Power Automate: een bouwkaart die je zelf in de designer klikt (welke actie, welke instelling, welke expressie), met een koppelchecklist. | "workflow maken in Power Automate", "bouw dit in Power Automate" |

## Installeren

Stap-voor-stap met screenshots: de pdf `docs/ai-lead-skills-installeren.pdf` in de GitHub-repo https://github.com/SPAIK-io/ai-lead-skills (die zit niet in de zip).

**Eén keer, in claude.ai** (werkt op Mac en Windows, geen GitHub-account nodig): klik in het
chatvenster op `+` > Add plugins > Add > Add from a repository, plak `SPAIK-io/ai-lead-skills` en
zet de plugin aan. De plugin
staat daarna op je account: in claude.ai én in Claude Code, als je die op hetzelfde account
gebruikt (Claude Code één keer herstarten).

Daarna typ je gewoon "interview voorbereiden", "blueprint maken" of "maak een workflow" en pakt
Claude de skill op. Bij "maak een workflow" vraagt Claude de eerste keer waarin je bouwt (n8n,
Lleverage of Power Automate) en biedt aan dat in de CLAUDE.md van je map te zetten, zodat het
niet opnieuw gevraagd wordt.

**Bijwerken:** updates komen vanzelf binnen, meestal binnen een uur. Wil je het nu: open de
plugin (Customize > Plugins > Yours > Ai lead skills), drie puntjes > Check for updates.
"No changes since the last release" betekent dat je al de nieuwste hebt.

**Zie je "This marketplace is already added"?** Dan staat de bron er al. Niet opnieuw
toevoegen; ga naar Discover, zoek "Ai lead skills" en zet hem aan.

**Alleen Claude Code in de terminal, zonder claude.ai:**

```
/plugin marketplace add SPAIK-io/ai-lead-skills
/plugin install ai-lead-skills@ai-lead
```

## Eigenaarschap en verbeteringen

SPAIK beheert deze repo. Iedereen mag lezen en gebruiken; wijzigen gaat via ons, zodat
iedereen dezelfde versie heeft. Heb je een verbetering: zeg het in de groep of bij de
maandelijkse sessie, open een issue, of stuur een pull request. Pas de skill niet lokaal
aan in je eigen `.claude/skills`, want dan mis je elke update.

## Bronvermelding

De vijf skills `ai-lead-n8n-*` zijn gebaseerd op [czlonkowski/n8n-skills](https://github.com/czlonkowski/n8n-skills)
van Romuald Członkowski (MIT, commit e037563), aangepast door SPAIK: zonder MCP, voor flows als
importbestand. Licentie, notices en wat we veranderden staan in [`third_party/n8n-skills/`](third_party/n8n-skills/).
