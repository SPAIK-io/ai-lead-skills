---
name: ai-lead-workflow-n8n
description: >-
  Use when the lead builds in n8n: the lead names n8n, or the CLAUDE.md or AGENTS.md of the
  working folder says so (e.g. "Wij bouwen in n8n."). Maakt van een blueprint (of procesmap) en
  één gekozen stap een eerste n8n-flow als importbestand (JSON), zonder MCP en zonder
  API-sleutels. Eerst een plannetje in gewone taal, dan een bestand dat je in n8n importeert
  (Import from File) en zelf draait, met per blok een Nederlandse naam en een notitie. Data komt
  uit een n8n Data Table of uit een csv via een formulier. Triggert op "workflow maken in n8n",
  "bouw dit in n8n", "n8n-flow als bestand", "importbestand voor n8n", "van blueprint naar
  n8n", "eerste prototype n8n". Is het platform niet genoemd en ligt het niet vast, dan maakt
  ai-lead-workflow eerst de keuze.
metadata:
  version: "0.4"
  last_updated: "2026-11-14"
---

# Van blueprint naar n8n-flow (als importbestand)

Je hebt een blueprint en je hebt één klein stuk gekozen dat je als eerste wilt bouwen. Deze
skill maakt daar een eerste prototype van in n8n. Niet het eindproduct, wel iets waar je een
echt gesprek over kunt voeren met de mensen die het straks gebruiken.

Claude bouwt niet in jouw n8n. Er is geen MCP-koppeling en je hebt geen API-sleutel nodig.
Claude schrijft een **bestand** (JSON) op je laptop. Jij importeert het in n8n, draait het en
kijkt in elk blok wat er binnenkomt en wat eruit gaat. Een beheerder zet de flow aan, niet jij.

De vakkennis over n8n zelf staat in vijf hulpskills: `ai-lead-n8n-patronen` (opbouw),
`ai-lead-n8n-blokken` (welk blok, welke instellingen), `ai-lead-n8n-expressies` (`{{ }}`),
`ai-lead-n8n-bestanden` (csv en andere bestanden) en `ai-lead-n8n-javascript` (alleen als er
echt een codeblok nodig is). De vormen die bewezen werken staan onderaan deze skill, onder Bouwstenen.

---

## Vraag eerst dit

| Wat | Waarom |
|---|---|
| **De blueprint** of de uitwerking van je interviews | Zonder blueprint bouw je uit je hoofd, en dat is precies wat we niet willen |
| **Welke stap** je als eerste wilt automatiseren, en waarom die | Eén stap. Twee stappen is twee flows |
| **Waar de data vandaan komt**: een Data Table in je n8n-project (welke, met welke kolommen) of een csv die je uploadt | Bepaalt het begin. Andere bronnen zijn er nog niet |
| **Wat eruit moet**: een overzicht dat je in n8n bekijkt, of regels in een Data Table die al bestaat | Bepaalt het eind |
| **Waar een mens kijkt** | Bij een eerste versie bijna altijd ergens. Liever te vroeg dan te laat |
| **Of er een AI-koppeling in je n8n is** | Zonder koppeling geen AI-stap (zie onder) |

Heb je geen blueprint, stuur dan terug naar `ai-lead-blueprint`. Weet je de kolomnamen niet
precies, vraag ze dan: open de tabel in n8n en kopieer de kopregel. Niet raden.

---

## Stap 1: het plannetje

Werk je in Claude Code, zet dan plan mode aan (Shift+Tab). Schrijf de flow eerst uit als een
lijstje van stappen in gewone taal en leg dat voor. Vijf tot tien stappen. Per stap: een korte
Nederlandse naam, wat er gebeurt, en welk blok het wordt. Gebruik deze soorten, in de woorden
van de AI lead. De rechterkolom is voor Claude bij het bouwen.

| Soort | Wat het doet | Wordt in n8n |
|---|---|---|
| **begin** | jij klikt op start, of je uploadt een csv in een formulier | *Manual Trigger*, of *Form Trigger* met een bestandsveld |
| **ophalen** | rijen uit een tabel halen | *Data Table* (get) |
| **inlezen** | een csv omzetten naar rijen | *Extract from File* |
| **filteren** | alleen de rijen doorlaten die aan een regel voldoen | *Filter* |
| **rekenen of velden maken** | een veld uitrekenen, een datum leesbaar maken, velden kiezen | *Edit Fields (Set)* |
| **splitsen** | op een voorwaarde twee kanten op | *If* |
| **tellen** | per groep tellen of optellen | *Summarize* |
| **sorteren** | op volgorde zetten | *Sort* |
| **koppelen** | twee lijsten naast elkaar zetten op een gedeeld veld | *Merge* (combine by fields) |
| **wegschrijven** | regels toevoegen aan een tabel die al bestaat | *Data Table* (insert) |
| **einde** | waar je de uitkomst ziet | het laatste blok, of een *No Operation*-blok met een duidelijke naam |

Regels voor het plannetje:

- **Na een splitsing** eindigt elke kant ergens, al is het maar in een einde met een naam.
- **Wat de mens moet zien, staat in de naam en de notitie van het blok.** "Controleren" met
  in de notitie wat er gecontroleerd moet worden en door wie.
- **Wat er bewust niet in zit**, schrijf je eronder. Dat is de agenda voor versie twee.

Leg het plannetje voor als tabel en pas aan tot de AI lead zegt: ja, zo werkt het bij ons. Pas
dan bouwen. Zegt de lead zelf dat hij het plan overslaat en akkoord gaat, zet het plannetje dan
kort bovenaan je antwoord en bouw door.

---

## Stap 2: het bestand bouwen

Bouw alleen wat in het plannetje staat. Neem de vormen uit **Bouwstenen** (onderaan) letterlijk over: dat
zijn de blokken en versies die op n8n Cloud 2.47 zijn geïmporteerd en gedraaid. Neem ook de
`typeVersion` en de vaste instellingen over (Data Table 1.1 met `limit`, Filter en If met
`typeValidation: "loose"`), ook als je uit je hoofd een andere vorm kent. Wil je een blok dat
daar niet in staat, zeg dan dat het niet getest is (zie `ai-lead-n8n-blokken`).

Vaste regels voor het bestand:

- **Elk blok een Nederlandse naam** die zegt wat het doet ("Alleen betaalde facturen", niet
  "Filter1"), en een **notitie in gewone taal** (`notes` met `notesInFlow: true`). De notitie
  staat in n8n onder het blok. Eén of twee zinnen: wat doet dit blok, en wat zie je erna.
- **Ids als UUID**, namen uniek (de verbindingen gaan op naam).
- **`settings.timezone: "Europe/Amsterdam"`.** Datums uit een Data Table komen terug als
  middernacht UTC; zonder deze instelling laat een datumexpressie de dag ervoor zien.
- **`active: false`.** Geen credentials in het bestand, geen wachtwoorden, geen sleutels.
- **Een Data Table kiest de lead zelf.** Claude kent het id van de tabel niet. Laat `value` leeg
  en zet in de notitie welke tabel de lead na het importeren moet kiezen.
- **Een Data Table get draait per binnenkomende regel.** Komen er tien regels binnen, dan haalt
  hij de tabel tien keer op. Zet hem daarom direct na het beginblok, of zet `"executeOnce": true`
  op het blok (naast `parameters`) als hij later in de flow staat.
- **Een codeblok alleen als geen gewoon blok past** (zie de tabel in `ai-lead-n8n-blokken`). Een
  codeblok krijgt een notitie die begint met `Waarom code:` en in gewone taal uitlegt wat het doet,
  en het krijgt een extra check van IT voordat de flow aangaat. Zeg dat erbij.
- **Geen AI-stap, tenzij de lead zegt dat er een AI-koppeling in zijn n8n is.** Is die er, zet
  dan een lege plek neer: een *No Operation*-blok "Hier komt de AI-stap" met in de notitie wat de
  AI moet doen, wat erin gaat en wat eruit moet komen. Welk model en welke koppeling mogen, ligt
  bij je organisatie; vul dat niet in. Zonder koppeling doet een mens die stap, of zet je hem
  onder "bewust niet".
- **Geen koppelingen met andere systemen** (mail, Teams, SharePoint, een API). Vraagt het plan
  erom, zet dan een *No Operation*-blok "Hier komt: …" met een notitie, zodat de rest wel draait.

Sla het bestand op in de map waar de lead werkt, met een naam die zegt wat de flow doet
(bijvoorbeeld `facturen-per-leverancier.json`). Is Python beschikbaar, draai dan de check. Het
commando heet `python3`, `python` of (op Windows) `py`; probeer ze in die volgorde:

```
python3 scripts/check_flow.py <bestand>.json
```

Die controleert of het geldige JSON is, alleen bewezen blokken en versies bevat, de tijdzone
goed staat, elk blok een naam en notitie heeft, de verbindingen en verwijzingen kloppen, en er
geen credentials, koppelingen, AI-blokken of vastgezette gegevens (pinData) in zitten. Fouten eerst oplossen. Een waarschuwing bespreek je met de lead. Is er geen Python, loop
die punten dan zelf na en zeg dat erbij.

---

## Stap 3: wat je oplevert

1. **Het bestand**, met een flownaam die zegt wat hij doet.
2. **Zo importeer je hem**: in je project in n8n een nieuwe workflow maken (Create workflow),
   dan het menu met de drie puntjes → Import from File, en het bestand kiezen.
3. **Wat je na het importeren zelf kiest**: per Data Table-blok de tabel. Een blok met een rode
   rand mist nog iets; open het en kijk welk veld n8n aanwijst.
4. **Hoe je hem test**: klik op Execute workflow. Bij een formulier opent n8n het formulier; je
   hoeft niets te publiceren. Zeg per blok wat je moet zien (hoeveel regels, welke velden) en
   laat de lead in elk blok kijken wat er binnenkomt en uitgaat. Test met verzonnen gegevens:
   echte gegevens van huurders, klanten of collega's horen niet in een test.
5. **Wat er bewust niet in zit** en waarom.
6. **Wie hem aanzet**: niemand nog. Moet de flow vanzelf gaan draaien, dan vraag je dat aan de
   beheerder. Jij draait hem met de hand.

---

## Regels

- **Eén stap uit de blueprint per flow.** Wordt het plan langer dan tien stappen, dan bouw je te
  veel tegelijk.
- **Altijd een mens erin bij versie één**, tenzij de AI lead uitlegt waarom het veilig is.
- **Elke stap kun je uitleggen.** Kan de AI lead een blok niet in gewone taal uitleggen, dan gaat
  het er niet in. Een codeblok krijgt een extra check van IT.
- **De beheerder zet de flow aan.** Jij importeert, draait met de hand en laat zien.
- **Alleen verzonnen data**, uit een Data Table in je project of uit een csv die je uploadt.
- **Een nieuwe koppeling vraag je aan.** Je bouwt er niet omheen. Welke systemen, modellen en
  koppelingen mogen, bepaalt je organisatie; schrijf niets op als afgesproken wat dat nog niet is.
- **Niets verzinnen.** Tabel- en kolomnamen komen van de AI lead. Weet je niet zeker of een blok
  of instelling zo bestaat, zeg dat dan in plaats van te gokken.
- Nederlands, je-vorm, korte zinnen, geen em-dashes. Namen van knoppen en blokken in n8n in het
  Engels, zoals ze in het scherm staan.

---

## Wat je vooraf nodig hebt

- Een inlog op n8n en een project waarin je workflows mag maken en importeren.
- De Data Tables met verzonnen data in dat project, of een csv met verzonnen data.
- Claude Code op je laptop met deze plugin (`ai-lead-skills`). Een MCP-koppeling of API-sleutel
  is niet nodig.

---

## Bouwstenen die bewezen werken

Deze vormen zijn op 14 november 2026 geïmporteerd en gedraaid op n8n Enterprise Cloud 2.47
(bewezen oefenflows). Neem ze letterlijk over en verander alleen namen,
velden, waarden en notities. Een blok of versie die hier niet staat, is niet getest: zeg dat.

| Blok | `type` | `typeVersion` |
|---|---|---|
| Manual Trigger | `n8n-nodes-base.manualTrigger` | 1 |
| Form Trigger | `n8n-nodes-base.formTrigger` | 2.2 |
| Extract from File | `n8n-nodes-base.extractFromFile` | 1.1 |
| Data Table (get, insert) | `n8n-nodes-base.dataTable` | 1.1 |
| Filter | `n8n-nodes-base.filter` | 2.2 |
| If | `n8n-nodes-base.if` | 2.2 |
| Edit Fields (Set) | `n8n-nodes-base.set` | 3.4 |
| Summarize | `n8n-nodes-base.summarize` | 1.1 |
| Sort | `n8n-nodes-base.sort` | 1 |
| Merge | `n8n-nodes-base.merge` | 3.2 |
| No Operation | `n8n-nodes-base.noOp` | 1 |

### Het geraamte

```json
{
  "name": "Facturen per leverancier",
  "nodes": [],
  "pinData": {},
  "connections": {},
  "active": false,
  "settings": { "executionOrder": "v1", "timezone": "Europe/Amsterdam" },
  "tags": []
}
```

Elk blok heeft deze velden naast `parameters`, `type` en `typeVersion`:

```json
{
  "position": [224, 0],
  "id": "<uuid>",
  "name": "Alleen betaalde facturen",
  "notes": "Laat alleen de facturen door met status Betaald.",
  "notesInFlow": true
}
```

Zet de blokken 224 punten uit elkaar op de x-as (0, 224, 448, …). Bij een splitsing de twee
kanten op y = -96 en y = 96.

### Verbindingen

Op naam van het blok. `index` is de ingang van het volgende blok.

```json
"connections": {
  "Start": { "main": [[{ "node": "Haal facturen op", "type": "main", "index": 0 }]] },
  "Haal facturen op": { "main": [[{ "node": "Alleen betaalde facturen", "type": "main", "index": 0 }]] }
}
```

- **If** heeft twee uitgangen: de eerste lijst is `true`, de tweede `false`:
  `"Meer dan 10%?": { "main": [[{ "node": "Controleren", "type": "main", "index": 0 }], [{ "node": "Binnen marge", "type": "main", "index": 0 }]] }`
- **Merge** heeft twee ingangen: de ene lijst komt op `"index": 0`, de andere op `"index": 1`.
  Eén startblok mag naar twee blokken tegelijk wijzen (twee items in dezelfde lijst).

### Begin

**Manual Trigger**: de flow start als je op Execute workflow klikt.

```json
{ "parameters": {}, "type": "n8n-nodes-base.manualTrigger", "typeVersion": 1, "name": "Start",
  "notes": "Start de flow als je op Execute workflow klikt.", "notesInFlow": true }
```

**Form Trigger met csv-upload**: Execute workflow opent het formulier; publiceren is niet nodig.
De binary-eigenschap heet zoals het veldlabel (hier `Bestand`). Een Form Trigger heeft ook een
`webhookId` (UUID) nodig.

```json
{ "parameters": {
    "formTitle": "Upload je testbestand",
    "formDescription": "Alleen verzonnen gegevens. Een csv-bestand met een kopregel.",
    "formFields": { "values": [ { "fieldLabel": "Bestand", "fieldType": "file", "multipleFiles": false,
                                  "acceptFileTypes": ".csv", "requiredField": true } ] },
    "options": {} },
  "type": "n8n-nodes-base.formTrigger", "typeVersion": 2.2, "name": "Formulier",
  "webhookId": "<uuid>" }
```

**Extract from File**: van elke regel in de csv één rij.

```json
{ "parameters": { "binaryPropertyName": "Bestand", "options": {} },
  "type": "n8n-nodes-base.extractFromFile", "typeVersion": 1.1, "name": "Lees csv" }
```

### Data Table

**Ophalen** (get). Claude kent het id van de tabel niet: laat `value` leeg. De lead kiest de tabel
na het importeren; zet in de notitie welke.

```json
{ "parameters": {
    "operation": "get",
    "dataTableId": { "__rl": true, "value": "", "mode": "list" },
    "limit": 500 },
  "type": "n8n-nodes-base.dataTable", "typeVersion": 1.1, "name": "Haal facturen op",
  "notes": "Leest de rijen uit de tabel facturen. Schrijft niets. Kies na het importeren de tabel facturen.",
  "notesInFlow": true }
```

In de bewezen flows stond hier een ingevuld id met `"cachedResultName": "<tabelnaam>"`. Dat id
geeft de lead, als hij het wil: het staat in de adresbalk als hij de tabel opent
(`…/datatables/<id>`). `limit` 500 haalt maximaal 500 rijen; zet het hoger als de tabel groter is.

**Wegschrijven** (insert, de standaard: geen `operation`). Maak eerst met Edit Fields precies de
kolommen van de doeltabel; `autoMapInputData` zet elk veld in de kolom met dezelfde naam.

```json
{ "parameters": {
    "dataTableId": { "__rl": true, "value": "", "mode": "list" },
    "columns": { "mappingMode": "autoMapInputData", "value": {}, "matchingColumns": [], "schema": [],
                 "attemptToConvertTypes": false, "convertFieldsToString": false },
    "options": {} },
  "type": "n8n-nodes-base.dataTable", "typeVersion": 1.1, "name": "Schrijf in oefenresultaten" }
```

### Filter en If

Zelfde vorm voor beide. `operator.type` is `string`, `number`, `boolean` of `dateTime`.
Bijvoorbeeld `string` + `equals`, `number` + `gt` (groter dan), `lt`, `gte`, `lte`.

```json
{ "parameters": {
    "conditions": {
      "options": { "caseSensitive": true, "leftValue": "", "typeValidation": "loose", "version": 2 },
      "conditions": [ { "id": "<uuid>", "leftValue": "={{ $json.status }}", "rightValue": "Betaald",
                        "operator": { "type": "string", "operation": "equals" } } ],
      "combinator": "and" },
    "options": {} },
  "type": "n8n-nodes-base.filter", "typeVersion": 2.2, "name": "Alleen betaalde facturen" }
```

Voor een If: `"type": "n8n-nodes-base.if"`, ook versie 2.2, en twee uitgangen (zie Verbindingen).

### Edit Fields (Set)

Elk veld met naam, waarde en type (`string`, `number`, `boolean`). Een expressie begint met `=`.
Met `"includeOtherFields": true` blijven de andere velden van de rij staan; zonder blijven alleen
de velden die je hier noemt.

```json
{ "parameters": {
    "assignments": { "assignments": [
      { "id": "<uuid>", "name": "factuur", "value": "={{ $json.factuur_nr }}", "type": "string" },
      { "id": "<uuid>", "name": "datum", "value": "={{ $json.factuur_dt.toDateTime().toFormat('dd-MM-yyyy') }}", "type": "string" },
      { "id": "<uuid>", "name": "afwijking_pct", "value": "={{ Math.round(($json.meetstaat / $json.offerte - 1) * 1000) / 10 }}", "type": "number" }
    ] },
    "options": {} },
  "type": "n8n-nodes-base.set", "typeVersion": 3.4, "name": "Maak overzicht" }
```

Een datum uit een Data Table leesbaar maken: `{{ $json.<veld>.toDateTime().toFormat('dd-MM-yyyy') }}`.
Dat geeft alleen de goede dag met `settings.timezone: "Europe/Amsterdam"`.

### Summarize

Eén regel per groep. `aggregation` is bijvoorbeeld `count` of `sum`. De uitkomst heet
`<aggregation>_<veld>`: `sum_bedrag_incl`, `count_factuur_nr`. Rijen zonder waarde in het
groepsveld komen samen in één regel zonder naam: vaak een datafout, laat de lead ernaar kijken.

```json
{ "parameters": {
    "fieldsToSummarize": { "values": [
      { "aggregation": "count", "field": "factuur_nr" },
      { "aggregation": "sum", "field": "bedrag_incl" } ] },
    "fieldsToSplitBy": "leverancier",
    "options": {} },
  "type": "n8n-nodes-base.summarize", "typeVersion": 1.1, "name": "Tel per leverancier" }
```

### Sort

```json
{ "parameters": {
    "type": "simple",
    "sortFieldsUi": { "sortField": [ { "fieldName": "sum_bedrag_incl", "order": "descending" } ] },
    "options": {} },
  "type": "n8n-nodes-base.sort", "typeVersion": 1, "name": "Grootste eerst" }
```

### Merge (twee lijsten koppelen)

`enrichInput1`: alle regels van ingang 1 blijven, met de velden van ingang 2 erbij als het
gedeelde veld gelijk is. Regels zonder match houden een leeg veld; vang dat op met `|| 0`.

```json
{ "parameters": {
    "mode": "combine", "combineBy": "combineByFields",
    "fieldsToMatchString": "opdracht_nr", "joinMode": "enrichInput1", "options": {} },
  "type": "n8n-nodes-base.merge", "typeVersion": 3.2, "name": "Koppel op opdracht" }
```

### No Operation (einde of lege plek)

Doet niets. Gebruik het als einde van een tak met een duidelijke naam, of als lege plek voor iets
wat er nog niet is (een AI-stap, een koppeling). De uitleg staat in de notitie.

```json
{ "parameters": {}, "type": "n8n-nodes-base.noOp", "typeVersion": 1, "name": "Controleren",
  "notes": "Hier komen de facturen die de afdeling moet nakijken.", "notesInFlow": true }
```
