---
name: ai-lead-workflow-lleverage
description: >-
  Maakt van een blueprint (of procesmap) en één gekozen stap een eerste workflow die je in Lleverage kunt
  importeren. Eerst een plannetje in gewone taal dat je samen scherp maakt, dan bouwt een
  script de JSON uit bouwstenen die bewezen werken, met een checklist van wat je na import
  zelf moet kiezen. Triggert op "workflow maken", "bouw dit in Lleverage", "van blueprint naar flow", "van procesmap
  naar flow", "eerste prototype", "lleverage json", "flow met database", "databasevraag in
  Lleverage".
metadata:
  version: "0.4"
  last_updated: "2026-10-05"
---

# Van blueprint naar Lleverage-workflow

Je hebt een blueprint en je hebt één klein stuk gekozen dat je als eerste wilt bouwen. Deze
skill maakt daar een werkend eerste prototype van: een bestand dat je in Lleverage importeert
en meteen kunt draaien. Niet het eindproduct, wel iets waar je een echt gesprek over kunt
voeren met de mensen die het straks gebruiken.

De skill doet het denken samen met jou en laat het typen aan een script over. Het script
controleert de structuur (verwijzingen, takken, eindpunten) en weigert een plan dat niet klopt.
Of Lleverage elke bouwsteen precies zo accepteert, staat per bouwsteen in `bouwstenen.md`.

---

## Vraag eerst dit

| Wat | Waarom |
|---|---|
| **De blueprint** of de uitwerking van je interviews | Zonder blueprint bouw je uit je hoofd, en dat is precies wat we niet willen |
| **Welke stap** je als eerste wilt automatiseren, en waarom die | Eén stap. Twee stappen is twee workflows |
| **Wat komt er binnen** (mail, formulier, vast tijdstip, een systeem dat aanklopt) | Bepaalt de trigger |
| **Wat moet eruit** (mail terug, bericht in Slack, rij in een tabel, alleen een scherm) | Bepaalt het eind |
| **Waar wil je dat een mens kijkt** | Bij een eerste versie bijna altijd ergens. Liever te vroeg dan te laat |

Heb je geen blueprint, stuur dan terug naar `ai-lead-blueprint`.

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
| `mens_keur` | Een mens keurt goed of af; de flow wacht en splitst in `goed` en `fout` | takken `goed` / `fout`; wie klikte: `{{Naam.resolvedBy}}` |
| `mail_sturen` | Stuurt een nieuwe mail via Outlook | |
| `mail_beantwoorden` | Antwoordt op de mail die de flow startte (alleen bij mail-trigger) | |
| `slack` | Bericht in een Slack-kanaal | |
| `http` | Haalt iets op uit een API of stuurt iets weg | `{{Naam.data}}` |
| `tabel_schrijven` / `tabel_lezen` | Rij in een Lleverage-tabel schrijven of lezen | `{{Naam.record}}` |
| `database` | Leest rijen uit de database met één SELECT (alleen lezen, speeltuin) | alleen in een `js`-stap: `Naam.result` (de rijen) |
| `output` | Eindpunt: wat je in de run ziet | |

Triggers: `mail` (nieuwe mail in een map; velden `mailbox`, `map`), `app` (formulier; `velden`),
`schedule` (vaste tijden; `cron`) of `api` (een ander systeem klopt aan; `velden`).

Wat elke soort nodig heeft:

| Soort | Verplicht | Optioneel |
|---|---|---|
| `llm` | `prompt` | `uitvoer` (velden met type) |
| `extract` | `bron` (zonder accolades, bv. `Form.data.Tekst`), `uitvoer` | |
| `js` | `script` | |
| `branch` | `condities` (tak: expressie, zonder accolades) | |
| `mens_vraag` | `velden` | `titel`, `onderwerp`, `uitleg`, `defaults` |
| `mens_keur` | | `titel`, `uitleg`, `goed`, `fout` (knopteksten) |
| `mail_sturen` | `aan`, `onderwerp`, `tekst` | `van` |
| `mail_beantwoorden` | `tekst` | `aan` |
| `slack` | `tekst` | `kanaal` |
| `http` | `url` | `methode`, `body`, `auth` |
| `tabel_schrijven` | `tabel`, `data` (kolom: waarde) | |
| `tabel_lezen` | `tabel` | `filter` (kolom: waarde), `modus` (`first` of `all`) |
| `database` | `sql`, plus bovenin het plan `lead` (je achtervoegsel) | `lead` per stap, `verbinding` (andere naam connection-secret) |
| `output` | `tekst` | |

Typen voor `uitvoer` en `velden`: `string`, `number`, `boolean`, `array`, en `string?` als het
leeg mag zijn. Namen van stappen en velden: letters, cijfers, underscore, beginnend met een letter.

Wat de mail-trigger geeft: `{{Mailbox.subject}}`, `{{Mailbox.body}}`, `{{Mailbox.from}}`,
`{{Mailbox.files}}`. Het formulier: `{{Form.data.<veld>}}`.

Regels voor het plannetje:

- **Na een `branch` of `mens_keur`** zeg je bij de volgende stap welke tak: `"na": "Splits.order"`
  of `"na": "Keur.goed"`. Elke tak moet ergens eindigen, al is het maar in een `output`.
- **Verwijzen doe je op naam:** `{{Lees_Mail.output.klant}}`. In een `js`-script zonder
  accolades: `Lees_Mail.output.klant`.
- **Wat de mens moet zien, staat in de tekst van de stap.** Een `mens_keur` met alleen
  "Goedkeuren?" is nutteloos; zet erin wat er goedgekeurd wordt.
- **Een mail-trigger staat op een eigen map**, met een Outlook-regel die alleen jouw
  testafzenders daarin zet. Nooit op de Inbox of op een map waar al een flow op draait. Geef
  in het plan de mapnaam op (`"map": "AI LEAD <NAAM>"`).
- **Geheimen nooit in het plan.** Een API-sleutel gaat als `{{_env.NAAM}}` en wordt in
  Lleverage als secret gezet.

### Een databasevraag (`database`)

Gebruik een databaseblok als de flow gegevens nodig heeft die al in de database staan:
orders, klanten, artikelen. Het blok stelt één vraag (een SELECT) en geeft de rijen terug.
Wil je iets opzoeken bij één mail of formulier, dan bouwt een `js`-stap eerst de vraag.

```json
{"naam": "Nieuwste orders mailen", "lead": "PIET",
 "trigger": {"soort": "schedule", "cron": "0 8 1 1 *"},
 "stappen": [
  {"naam": "Haal_Orders", "soort": "database",
   "sql": "SELECT salesordernumber, salesordername FROM playground.sales_order_header ORDER BY ordercreationdatetime DESC LIMIT 20"},
  {"naam": "Maak_Lijst", "soort": "js",
   "script": "var rijen = Haal_Orders.result || []; return {aantal: rijen.length, tekst: rijen.map(function (r) { return r.salesordernumber + ' ' + r.salesordername; }).join('<br>')};"},
  ...
```

Het hele voorbeeld (plan en workflow) staat in `voorbeelden/plan_database_orders.json`.

- **`lead` bovenin het plan is je achtervoegsel**, zoals je secrets in Lleverage heten:
  `POSTGRES_CONNECTION_STRING_DEV_<ACHTERVOEGSEL>`, `POSTGRES_SSH_KEY_<..>` en de variables
  `POSTGRES_SSH_HOST_<..>`, `_PORT_<..>`, `_USER_<..>`. Hoofdletters, geen accenten
  (`JOSE`, niet `José`). Zonder achtervoegsel weigert het script. Er komt nooit een
  wachtwoord of sleutel in het plan of de JSON.
- **Alleen lezen, alleen de speeltuin.** De SQL begint met `SELECT`, bevat geen
  schrijfopdracht (insert, update, delete, drop, alter, create, truncate, grant, revoke, copy),
  geen `;` in het midden, en leest uit schema `playground` (`FROM playground.<tabel>`).
- **Geen `--` commentaar** in de SQL: valt een regeleinde weg, dan is de rest van de vraag
  commentaar. `/* ... */` mag wel.
- **Geen `{{..}}` midden in de SQL.** Moet er een waarde uit de flow in, laat dan een `js`-stap
  de hele SELECT bouwen (`return {sql: "SELECT ... FROM playground..."}`, laat alleen letters,
  cijfers en streepjes door) en zet in het databaseblok precies `"sql": "{{Bouw_SQL.result.sql}}"`.
- **De rijen lees je alleen in een `js`-stap**, als `Haal_Orders.result` (een lijst met één
  object per rij, kolomnamen als velden). Niet `.rows` of `.data`, en nooit `{{Haal_Orders...}}`
  in een tekst: maak eerst in de `js`-stap een tekst of getal, en gebruik dat verderop.
- **Testen:** met een `schedule`-trigger klik je in Lleverage op Run; een `app`-trigger draait
  pas na Publish.

Na import: kies in het databaseblok de databaseverbinding "ODS dev", of controleer dat de
secrets en variables met jouw achtervoegsel in je Lleverage-project staan (Control > Secrets).
Het script zet dat in de `NA IMPORT`-regels.

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
  voor de AI lead, zie stap 3. Staat er `LET OP: geen mens in deze flow`, bespreek dat dan
  expliciet met de AI lead.
- **`PLAN-FOUT: ...`** Het plan vraagt iets wat het script niet kent, of mist iets. Los het
  op in het plan, niet in de JSON.
- **`FOUT: ...`** Structuurfout: een verwijzing naar een stap die niet bestaat, een tak die
  nergens heen gaat. Ook oplossen in het plan.

Schrijf nooit zelf JSON en pas nooit de uitvoer van het script met de hand aan. Klopt er
iets niet, dan klopt het plan niet, of het script mist een bouwsteen. In dat laatste geval
zeg je dat eerlijk en lever je dat deel als beschrijving in plaats van als JSON.

Gebruik je Claude in claude.ai zonder terminal, dan kan het script daar meestal gewoon draaien
(Claude voert Python uit). Lukt dat niet, bewaar dan het plan als `plan.json` en vraag je duo
of Brahma om het script te draaien; dat kost een minuut. Schrijf de JSON niet met de hand.

---

## Stap 3: wat je oplevert

1. **Het workflow-bestand**, met een naam die zegt wat hij doet.
2. **De importchecklist**, uit de `NA IMPORT`-regels van het script, in gewone taal:
   welke connection, welke mailbox of map, welke tabel eerst aanmaken, welke databaseverbinding. In Lleverage staan
   dezelfde punten in de beschrijving van de betreffende node, te herkennen aan
   `KIES NA IMPORT`.
3. **Hoe je hem test:** welke mail je stuurt of wat je in het formulier plakt, en wat je dan
   moet zien in de run. Eén concreet geval uit de interviews, niet een verzonnen voorbeeld.
4. **Wat er bewust niet in zit** en waarom: de uitzonderingen uit de blueprint die je in
   deze eerste versie overslaat. Dat is de agenda voor versie twee.

Importeren: in Lleverage een nieuwe workflow aanmaken, importeren, de checklist afwerken,
dan Run. Loopt hij vast, dan staat de echte fout meestal in het onderste foutblok van het
paneel, niet in het bovenste.

---

## Wat niet kan, en wat je dan doet

De bouwstenen in de tabel zijn de bouwstenen die we kennen. Een deel is in productie bewezen,
een deel alleen in een testflow gezien; welke wat is staat in `bouwstenen.md`. Andere koppelingen (Teams,
SharePoint, Excel, een ERP) zitten er niet in. Vraagt het plan daar toch om, dan:

- zeg je dat die stap niet als JSON meekomt,
- lever je hem als `output` of als `js`-stap met een duidelijke placeholder-tekst, zodat de
  flow wel importeert en draait,
- en beschrijf je in gewone taal wat daar later moet komen.

Een flow die draait met een gat erin is beter dan een flow die niet importeert.

---

## Regels

- **Eén stap uit de blueprint per workflow.** Wordt het plan langer dan tien stappen, dan
  bouw je te veel tegelijk.
- **Altijd een mens erin bij versie één**, tenzij de AI lead expliciet zegt van niet en
  kan uitleggen waarom het veilig is.
- **Niets verzinnen.** Mailadressen, kanalen, tabelnamen komen van de AI lead. Weet die het
  niet, dan blijft de placeholder staan.
- **Geen geheimen in het plan of de JSON.**
- Nederlands, je-vorm, korte zinnen, geen em-dashes.
