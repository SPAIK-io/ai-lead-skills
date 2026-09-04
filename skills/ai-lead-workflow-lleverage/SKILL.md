---
name: ai-lead-workflow-lleverage
description: >-
  Maakt van een procesmap en één gekozen stap een eerste workflow die je in Lleverage kunt
  importeren. Eerst een plannetje in gewone taal dat je samen scherp maakt, dan bouwt een
  script de JSON uit bouwstenen die bewezen werken, met een checklist van wat je na import
  zelf moet kiezen. Triggert op "workflow maken", "bouw dit in Lleverage", "van procesmap
  naar flow", "eerste prototype", "lleverage json".
metadata:
  version: "0.1"
  last_updated: "2026-09-04"
---

# Van procesmap naar Lleverage-workflow

Je hebt een procesmap en je hebt één klein stuk gekozen dat je als eerste wilt bouwen. Deze
skill maakt daar een werkend eerste prototype van: een bestand dat je in Lleverage importeert
en meteen kunt draaien. Niet het eindproduct, wel iets waar je een echt gesprek over kunt
voeren met de mensen die het straks gebruiken.

De skill doet het denken samen met jou en laat het typen aan een script over. Daardoor is
de JSON altijd geldig, of hij komt helemaal niet.

---

## Vraag eerst dit

| Wat | Waarom |
|---|---|
| **De procesmap** of de uitwerking van je interviews | Zonder map bouw je uit je hoofd, en dat is precies wat we niet willen |
| **Welke stap** je als eerste wilt automatiseren, en waarom die | Eén stap. Twee stappen is twee workflows |
| **Wat komt er binnen** (mail, formulier, vast tijdstip, een systeem dat aanklopt) | Bepaalt de trigger |
| **Wat moet eruit** (mail terug, bericht in Slack, rij in een tabel, alleen een scherm) | Bepaalt het eind |
| **Waar wil je dat een mens kijkt** | Bij een eerste versie bijna altijd ergens. Liever te vroeg dan te laat |

Heb je geen procesmap, stuur dan terug naar `ai-lead-procesmap`.

---

## Stap 1: het plannetje

Schrijf de workflow eerst uit als een lijstje van stappen in gewone taal, en leg dat voor.
Vijf tot tien stappen. Elke stap krijgt een korte naam (letters en underscores, bijvoorbeeld
`Lees_Mail`) en een soort uit de tabel hieronder.

| Soort | Wat het doet | Waar het antwoord staat |
|---|---|---|
| `llm` | Leest tekst en haalt er velden uit, of schrijft tekst | `{{Naam.output.veld}}` |
| `extract` | Haalt velden uit tekst met een vast schema (strakker dan llm) | `{{Naam.output.veld}}` |
| `js` | Een stukje code: rekenen, checken, samenvoegen | `{{Naam.result.veld}}` |
| `branch` | Splitst op een voorwaarde in twee of meer takken | takken heten zoals jij ze noemt |
| `mens_vraag` | Een mens vult iets aan of corrigeert; de flow wacht | `{{Naam.data.veld}}` |
| `mens_keur` | Een mens keurt goed of af; de flow wacht en splitst in `goed` en `fout` | takken `goed` / `fout` |
| `mail_sturen` | Stuurt een nieuwe mail via Outlook | |
| `mail_beantwoorden` | Antwoordt op de mail die de flow startte (alleen bij mail-trigger) | |
| `slack` | Bericht in een Slack-kanaal | |
| `http` | Haalt iets op uit een API of stuurt iets weg | `{{Naam.data}}` |
| `tabel_schrijven` / `tabel_lezen` | Rij in een Lleverage-tabel schrijven of lezen | `{{Naam.record}}` |
| `output` | Eindpunt: wat je in de run ziet | |

Triggers: `mail` (nieuwe mail in een map), `app` (formulier met velden), `schedule` (vaste
tijden) of `api` (een ander systeem klopt aan).

Regels voor het plannetje:

- **Na een `branch` of `mens_keur`** zeg je bij de volgende stap welke tak: `"na": "Splits.order"`
  of `"na": "Keur.goed"`. Elke tak moet ergens eindigen, al is het maar in een `output`.
- **Verwijzen doe je op naam:** `{{Lees_Mail.output.klant}}`. In een `js`-script zonder
  accolades: `Lees_Mail.output.klant`.
- **Wat de mens moet zien, staat in de tekst van de stap.** Een `mens_keur` met alleen
  "Goedkeuren?" is nutteloos; zet erin wat er goedgekeurd wordt.
- **Geheimen nooit in het plan.** Een API-sleutel gaat als `{{_env.NAAM}}` en wordt in
  Lleverage als secret gezet.

Leg het plannetje voor als tabel, en pas aan tot de AI lead zegt: ja, zo werkt het bij ons.
Dit is het moment waarop de meeste fouten eruit gaan. Niet doorbouwen voordat dit klopt.

Voorbeelden van complete plannen staan in `voorbeelden/`.

---

## Stap 2: bouwen

Zet het plannetje om naar het JSON-formaat uit `scripts/build_flow.py` (de docstring
bovenin beschrijft elk veld) en draai:

```
python3 scripts/build_flow.py plan.json > <naam>.workflow.json
```

Het script zegt één van drie dingen:

- **`OK: n nodes`** plus regels die beginnen met `NA IMPORT:`. Die regels zijn de checklist
  voor de AI lead, zie stap 3.
- **`PLAN-FOUT: ...`** Het plan vraagt iets wat het script niet kent, of mist iets. Los het
  op in het plan, niet in de JSON.
- **`FOUT: ...`** Structuurfout: een verwijzing naar een stap die niet bestaat, een tak die
  nergens heen gaat. Ook oplossen in het plan.

Schrijf nooit zelf JSON en pas nooit de uitvoer van het script met de hand aan. Klopt er
iets niet, dan klopt het plan niet, of het script mist een bouwsteen. In dat laatste geval
zeg je dat eerlijk en lever je dat deel als beschrijving in plaats van als JSON.

Kan Claude hier geen Python draaien, geef dan het plan-JSON en de opdracht om het script te
draaien mee aan de AI lead; het script staat in de plugin.

---

## Stap 3: wat je oplevert

1. **Het workflow-bestand**, met een naam die zegt wat hij doet.
2. **De importchecklist**, uit de `NA IMPORT`-regels van het script, in gewone taal:
   welke connection, welke mailbox of map, welke tabel eerst aanmaken. In Lleverage staan
   dezelfde punten in de beschrijving van de betreffende node, te herkennen aan
   `KIES NA IMPORT`.
3. **Hoe je hem test:** welke mail je stuurt of wat je in het formulier plakt, en wat je dan
   moet zien in de run. Eén concreet geval uit de interviews, niet een verzonnen voorbeeld.
4. **Wat er bewust niet in zit** en waarom: de uitzonderingen uit de procesmap die je in
   deze eerste versie overslaat. Dat is de agenda voor versie twee.

Importeren: in Lleverage een nieuwe workflow aanmaken, importeren, de checklist afwerken,
dan Run. Loopt hij vast, dan staat de echte fout meestal in het onderste foutblok van het
paneel, niet in het bovenste.

---

## Wat niet kan, en wat je dan doet

De bouwstenen in de tabel zijn de bouwstenen die bewezen werken. Andere koppelingen (Teams,
SharePoint, Excel, een ERP) zitten er niet in. Vraagt het plan daar toch om, dan:

- zeg je dat die stap niet als JSON meekomt,
- lever je hem als `output` of als `js`-stap met een duidelijke placeholder-tekst, zodat de
  flow wel importeert en draait,
- en beschrijf je in gewone taal wat daar later moet komen.

Een flow die draait met een gat erin is beter dan een flow die niet importeert.

---

## Regels

- **Eén stap uit de procesmap per workflow.** Wordt het plan langer dan tien stappen, dan
  bouw je te veel tegelijk.
- **Altijd een mens erin bij versie één**, tenzij de AI lead expliciet zegt van niet en
  kan uitleggen waarom het veilig is.
- **Niets verzinnen.** Mailadressen, kanalen, tabelnamen komen van de AI lead. Weet die het
  niet, dan blijft de placeholder staan.
- **Geen geheimen in het plan of de JSON.**
- Nederlands, je-vorm, korte zinnen, geen em-dashes.
