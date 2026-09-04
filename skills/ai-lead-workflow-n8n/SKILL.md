---
name: ai-lead-workflow-n8n
description: >-
  Maakt van een procesmap en één gekozen stap een eerste workflow in n8n. Eerst een plannetje
  in gewone taal dat je samen scherp maakt, dan bouwt Claude hem met de n8n-skills en de
  n8n-MCP rechtstreeks in je n8n-omgeving, met een checklist van wat je zelf moet koppelen.
  Triggert op "workflow maken in n8n", "bouw dit in n8n", "van procesmap naar n8n", "eerste
  prototype n8n". Gebruik je Lleverage, neem dan ai-lead-workflow-lleverage.
metadata:
  version: "0.1"
  last_updated: "2026-09-04"
---

# Van procesmap naar n8n-workflow

Je hebt een procesmap en je hebt één klein stuk gekozen dat je als eerste wilt bouwen. Deze
skill maakt daar een werkend eerste prototype van in n8n. Niet het eindproduct, wel iets
waar je een echt gesprek over kunt voeren met de mensen die het straks gebruiken.

Het bouwen zelf doet Claude met twee dingen die je apart installeert (zie onderaan): de
**n8n-skills** (hoe je nodes goed configureert) en de **n8n-MCP** (Claude kan nodes opzoeken,
valideren en de workflow direct in jouw n8n zetten). Deze skill gaat over het stuk ervóór:
welke stap, welke stappen, waar een mens kijkt, en wat je bewust weglaat.

---

## Vraag eerst dit

| Wat | Waarom |
|---|---|
| **De procesmap** of de uitwerking van je interviews | Zonder map bouw je uit je hoofd, en dat is precies wat we niet willen |
| **Welke stap** je als eerste wilt automatiseren, en waarom die | Eén stap. Twee stappen is twee workflows |
| **Wat komt er binnen** (mail, formulier, vast tijdstip, een systeem dat aanklopt) | Bepaalt de trigger |
| **Wat moet eruit** (mail terug, bericht in Teams of Slack, rij in een sheet, alleen een scherm) | Bepaalt het eind |
| **Waar wil je dat een mens kijkt** | Bij een eerste versie bijna altijd ergens. Liever te vroeg dan te laat |
| **Welke n8n-omgeving** en of de MCP gekoppeld is | Zonder koppeling kan Claude wel praten maar niet bouwen |

Heb je geen procesmap, stuur dan terug naar `ai-lead-procesmap`.

---

## Stap 1: het plannetje

Schrijf de workflow eerst uit als een lijstje van stappen in gewone taal, en leg dat voor.
Vijf tot tien stappen. Per stap: een korte naam, wat er gebeurt, en waar het antwoord vandaan
komt. Gebruik deze soorten, in de woorden van de AI lead, niet in n8n-nodenamen:

| Soort | Wat het doet |
|---|---|
| **binnenkomst** | mail, formulier, vast tijdstip, of een ander systeem dat aanklopt |
| **lezen** | AI haalt velden uit tekst of een document |
| **rekenen of checken** | een regel toepassen, iets vergelijken, samenvoegen |
| **splitsen** | op een voorwaarde twee of meer kanten op |
| **mens vraagt of keurt** | de flow wacht tot iemand iets invult of goedkeurt |
| **ophalen of wegschrijven** | een API, een sheet, een database, een tabel |
| **bericht** | mail, Teams, Slack |
| **einde** | wat je aan het eind wilt zien |

Regels voor het plannetje:

- **Na een splitsing** moet elke kant ergens eindigen, al is het maar in een einde.
- **Wat de mens moet zien, staat in de tekst van de stap.** "Goedkeuren?" zonder context is
  nutteloos; zet erin wat er goedgekeurd wordt.
- **Geheimen nooit in het plan.** Wachtwoorden en API-sleutels gaan in n8n als credential.
- **Wat er bewust niet in zit**, schrijf je eronder. Dat is de agenda voor versie twee.

Leg het plannetje voor als tabel, en pas aan tot de AI lead zegt: ja, zo werkt het bij ons.
Dit is het moment waarop de meeste fouten eruit gaan. Niet doorbouwen voordat dit klopt.

---

## Stap 2: bouwen

Nu pas de n8n-kant. Werk het plannetje stap voor stap af met de n8n-skills en de MCP:

1. **Start met `n8n-workflow-patterns`** om het plannetje op een bewezen patroon te leggen
   (webhook, mail, gepland, AI met mens-in-de-lus).
2. **Per stap de juiste node** opzoeken en configureren met `n8n-node-configuration`; voor
   AI-stappen `n8n-agents`, voor code `n8n-code-javascript`, voor verwijzingen tussen nodes
   `n8n-expression-syntax`.
3. **Valideer** via de MCP vóór je de workflow wegzet. Fouten los je op met
   `n8n-validation-expert`; foutafhandeling zet je vanaf het begin goed met `n8n-error-handling`.
4. **Zet de workflow in n8n** via de MCP, uit, niet actief. De AI lead zet hem zelf aan na
   de test.

Bouw alleen wat in het plannetje staat. Vraagt een stap om een koppeling die er nog niet is
(een credential, een systeem waar de lead geen toegang toe heeft), zet daar dan een
placeholder-node neer met een duidelijke notitie, zodat de flow wel importeert en de rest
getest kan worden.

Werk je zonder MCP, lever dan de workflow als JSON-bestand dat de AI lead in n8n importeert,
en zeg er eerlijk bij dat hij niet gevalideerd is.

---

## Stap 3: wat je oplevert

1. **De workflow in n8n**, met een naam die zegt wat hij doet, en uitgeschakeld.
2. **De koppelchecklist**, in gewone taal: welke credentials de AI lead zelf moet invullen,
   welke mailbox of kanaal, welke sheet of tabel eerst moet bestaan.
3. **Hoe je hem test:** welke mail je stuurt of wat je in het formulier zet, en wat je dan
   moet zien. Eén concreet geval uit de interviews, niet een verzonnen voorbeeld.
4. **Wat er bewust niet in zit** en waarom.

---

## Regels

- **Eén stap uit de procesmap per workflow.** Wordt het plan langer dan tien stappen, dan
  bouw je te veel tegelijk.
- **Altijd een mens erin bij versie één**, tenzij de AI lead uitlegt waarom het veilig is.
- **Niets verzinnen.** Adressen, kanalen, sheet-namen komen van de AI lead.
- **Geen geheimen in het plan of de workflow.**
- Nederlands, je-vorm, korte zinnen, geen em-dashes.

---

## Wat je vooraf nodig hebt

- Toegang tot een n8n-omgeving, liefst een eigen testproject, met een API-sleutel.
- De n8n-skills plus MCP als plugin: `czlonkowski/n8n-skills` (MIT). Installeren zoals deze
  plugin, en de MCP koppelen met de URL en API-sleutel van je n8n-omgeving; de README van
  die plugin legt uit hoe.
- Deze plugin (`ai-lead-skills`) voor het interview, de procesmap en dit plannetje.
