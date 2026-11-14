---
name: ai-lead-workflow
description: >-
  Startpunt voor elke vraag om een workflow te maken als het platform niet genoemd is. Kijkt of
  vastligt waarin de AI lead bouwt (n8n, Lleverage of Power Automate), vraagt het anders één keer,
  en gaat dan verder met de juiste bouw-skill. Triggert op "workflow maken", "maak een workflow",
  "flow bouwen", "eerste prototype", "van blueprint naar flow", "van procesmap naar flow", "dit
  automatiseren", "kun je dit automatiseren", zonder platformnaam. Noemt de lead het platform
  zelf, of ligt het vast, dan neemt de bouw-skill van dat platform het over.
metadata:
  version: "0.1"
  last_updated: "2026-11-14"
---

# Workflow maken: eerst het platform

Je wilt van je blueprint een eerste flow maken. Per platform is er een eigen bouw-skill, want
n8n, Lleverage en Power Automate werken anders. Deze skill zorgt dat je de goede krijgt, en dat
je de vraag maar één keer hoeft te beantwoorden.

---

## 1. Ligt het platform al vast?

Kijk eerst, in deze volgorde:

1. **Wat de lead net zei.** Noemt hij n8n, Lleverage of Power Automate, dan ligt het vast.
2. **De `CLAUDE.md` of `AGENTS.md` van de werkmap.** Een regel als `Wij bouwen in n8n.` legt het
   vast. Ook een andere duidelijke zin over het platform telt.

Wat de lead nu zegt, gaat voor. Noemt hij een ander platform dan in `CLAUDE.md` staat, zeg dan
het verschil ("In je CLAUDE.md staat n8n, jij noemt nu Power Automate") en vraag of je de regel in
`CLAUDE.md` moet aanpassen. Bouw intussen in het platform dat hij nu noemt.

Ligt het vast, ga dan meteen naar stap 4. Vraag het niet opnieuw.

## 2. Vraag het één keer

Ligt het niet vast, vraag dan precies één keer:

> Waar bouw je in: n8n, Lleverage of Power Automate?

Heb je de tool AskUserQuestion, gebruik die dan, met de drie platforms als keuzes. Anders stel je
de vraag als gewone vraag. Wacht op het antwoord. Begin niet aan een plan of een flow, en kies
niet zelf een platform.

## 3. Stel voor het vast te leggen

Dit kan alleen in Claude Code, waar je in een map werkt. In de Claude-app is er geen `CLAUDE.md`
die je kunt schrijven: sla deze stap daar over en ga door naar stap 4.

Weet je het platform, stel dan voor:

> Zal ik in de CLAUDE.md van deze map zetten: `Wij bouwen in <platform>.`? Dan vraag ik het
> volgende keer niet opnieuw.

Alleen na een ja schrijf je die regel. Bestaat `CLAUDE.md` al, voeg de regel dan onderaan toe en
laat de rest staan; staat er al een regel over het platform, vervang dan alleen die regel. Bestaat hij niet, maak hem dan aan met alleen die regel. Zegt de lead nee,
dan schrijf je niets en ga je gewoon door.

## 4. Ga door met de juiste skill

| Platform | Skill |
|---|---|
| n8n | `ai-lead-workflow-n8n` |
| Lleverage | `ai-lead-workflow-lleverage` |
| Power Automate | `ai-lead-workflow-power-automate` |

Laad die skill en volg hem vanaf het begin. Wat de lead al vertelde (de blueprint, de stap die
hij wil bouwen) neem je mee, zodat hij het niet twee keer hoeft te zeggen.

## 5. Een ander platform

Noemt de lead een ander platform (bijvoorbeeld Make, Zapier of UiPath), zeg dan eerlijk dat er
voor dat platform geen skill is. Verwijs hem naar zijn AI-manager om te bespreken waar hij gaat
bouwen. Bouw er niet zelf iets voor uit je hoofd.

---

## Regels

- Eén vraag, één keer. Niet opnieuw vragen als het platform al vastligt.
- Niets in `CLAUDE.md` schrijven zonder ja van de lead.
- Nederlands, je-vorm, korte zinnen, geen em-dashes.
