# AI lead skills

Skills voor AI leads bij klanten van [SPAIK](https://spaik.io). Ze volgen de opdracht uit
sessie 1: interviews met de mensen die het werk doen, één procesmap van vier kolommen,
en één klein stuk dat je als eerste bouwt.

| Skill | Wat hij doet | Roep je aan met |
|---|---|---|
| `ai-lead-interview` | Vooraf: doelzin, themaguide, vragen op maat, kaartje voor tijdens. Achteraf: transcript naar stappen, getallen, omwegen en gaten, plus terugkoppelbericht. | "interview voorbereiden", "transcript verwerken" |
| `ai-lead-procesmap` | Interviewmateriaal naar de vier kolommen (stap, wie, hoe lang, wat gaat mis), gaten apart, waar zit de tijd en waar de frustratie. Met een invulbare HTML. | "procesmap maken" |
| `ai-lead-workflow-lleverage` | In aanbouw. Van procesmap naar een eerste workflow die je in Lleverage kunt importeren. | "workflow maken" |

## Installeren

**De makkelijkste route, werkt op Mac en Windows:** open claude.ai, klik in het chatvenster op
`+` > Add plugins > Add > Add from a repository, en plak
`https://github.com/SPAIK-io/ai-lead-skills`. Zet de plugin aan. Gebruik je ook Claude Code op
hetzelfde account, herstart die dan één keer: de skills staan er dan ook in.

**Alleen Claude Code, zonder claude.ai** (typ dit in Claude Code zelf, niet in je terminal):

```
/plugin marketplace add SPAIK-io/ai-lead-skills
/plugin install ai-lead-skills@ai-lead
```

Daarna typ je gewoon "interview voorbereiden" of "procesmap maken" en pakt Claude de skill op.
Updates komen vanzelf mee.

## Eigenaarschap en verbeteringen

SPAIK beheert deze repo. Iedereen mag lezen en gebruiken; wijzigen gaat via ons, zodat
iedereen dezelfde versie heeft. Heb je een verbetering: zeg het in de groep of bij de
maandelijkse sessie, open een issue, of stuur een pull request. Pas de skill niet lokaal
aan in je eigen `.claude/skills`, want dan mis je elke update.
