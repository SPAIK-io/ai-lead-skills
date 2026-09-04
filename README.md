# AI lead skills

Skills voor AI leads bij klanten van [SPAIK](https://spaik.io), of ze nu in Lleverage of in n8n bouwen. Claude kiest zelf de passende bouw-skill; de interview- en procesmap-skills zijn voor iedereen gelijk. Ze volgen de opdracht uit
sessie 1: interviews met de mensen die het werk doen, één procesmap van vier kolommen,
en één klein stuk dat je als eerste bouwt.

| Skill | Wat hij doet | Roep je aan met |
|---|---|---|
| `ai-lead-interview` | Vooraf: doelzin, themaguide, vragen op maat, kaartje voor tijdens. Achteraf: transcript naar stappen, getallen, omwegen en gaten, plus terugkoppelbericht. | "interview voorbereiden", "transcript verwerken" |
| `ai-lead-procesmap` | Interviewmateriaal naar de vier kolommen (stap, wie, hoe lang, wat gaat mis), gaten apart, waar zit de tijd en waar de frustratie. Met een invulbare HTML. | "procesmap maken" |
| `ai-lead-workflow-n8n` | Zelfde plannetje-stap, maar dan gebouwd in n8n met de n8n-skills en de n8n-MCP (aparte plugin `czlonkowski/n8n-skills`). | "workflow maken in n8n", "bouw dit in n8n" |
| `ai-lead-workflow-lleverage` | Van procesmap en één gekozen stap naar een plannetje, en daaruit een importeerbare Lleverage-workflow (gebouwd door een script, dus altijd geldig), met een importchecklist. Bèta. | "workflow maken", "bouw dit in Lleverage" |

## Installeren

Stap-voor-stap met screenshots: [docs/ai-lead-skills-installeren.pdf](docs/ai-lead-skills-installeren.pdf).

**Eén keer, in claude.ai** (werkt op Mac en Windows): klik in het chatvenster op `+` > Add plugins
> Add > Add from a repository, plak `SPAIK-io/ai-lead-skills` en zet de plugin aan. De plugin
staat daarna op je account: in claude.ai én in Claude Code, als je die op hetzelfde account
gebruikt (Claude Code één keer herstarten).

Daarna typ je gewoon "interview voorbereiden", "procesmap maken" of "workflow maken" en pakt
Claude de skill op.

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
