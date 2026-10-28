---
name: ai-lead-workflow-power-automate
description: >-
  Maakt van een blueprint (of procesmap) en één gekozen stap een eerste flow in Microsoft
  Power Automate. Eerst een plannetje in gewone taal dat je samen scherp maakt, dan een
  bouwkaart die je stap voor stap in de designer klikt (welke actie, welke instelling, welke
  expressie), met een checklist van wat je zelf moet koppelen. Triggert op "workflow maken in
  Power Automate", "bouw dit in Power Automate", "cloud flow maken", "van blueprint naar Power
  Automate", "eerste prototype Power Automate", en op vragen over een Power Automate-flow die
  faalt of een expressie die niet werkt. Gebruik je n8n of Lleverage, neem dan
  ai-lead-workflow-n8n of ai-lead-workflow-lleverage.
metadata:
  version: "0.1"
  last_updated: "2026-10-28"
---

# Van blueprint naar Power Automate-flow

Je hebt een blueprint en je hebt één klein stuk gekozen dat je als eerste wilt bouwen. Deze
skill maakt daar een eerste prototype van in Power Automate. Niet het eindproduct, wel iets
waar je een echt gesprek over kunt voeren met de mensen die het straks gebruiken.

Anders dan bij n8n kan Claude niet zelf in Power Automate bouwen. Je krijgt daarom een
**bouwkaart**: per stap welke actie je toevoegt, hoe je hem noemt, wat je invult en welke
expressie je plakt. Jij klikt hem in de designer. De vakkennis daarachter staat in
`references/`.

---

## Vraag eerst dit

| Wat | Waarom |
|---|---|
| **De blueprint** of de uitwerking van je interviews | Zonder blueprint bouw je uit je hoofd, en dat is precies wat we niet willen |
| **Welke stap** je als eerste wilt automatiseren, en waarom die | Eén stap. Twee stappen is twee flows |
| **Wat komt er binnen** (mail, formulier, vast tijdstip, een systeem dat aanklopt) | Bepaalt de trigger |
| **Wat moet eruit** (mail terug, bericht in Teams, rij in een SharePoint-lijst of Excel-tabel) | Bepaalt het eind |
| **Waar wil je dat een mens kijkt** | Bij een eerste versie bijna altijd ergens. Liever te vroeg dan te laat |
| **Welke omgeving** en of je daar flows mag maken | Liefst een testomgeving. Is er alleen de standaardomgeving, dan mag die voor een prototype, met een eigen map en verzonnen data |
| **Welke licentie** je hebt: alleen Microsoft 365, of ook Power Automate Premium | Zonder Premium vallen de AI-stap (AI Builder), HTTP, Dataverse en eigen connectors af |
| **Welke systemen al gekoppeld zijn** (Outlook, Teams, SharePoint, Excel) | Een nieuwe koppeling vraag je aan, je bouwt er niet omheen |

Heb je geen blueprint, stuur dan terug naar `ai-lead-blueprint`.

---

## Stap 1: het plannetje

Schrijf de flow eerst uit als een lijstje van stappen in gewone taal, en leg dat voor. Vijf
tot tien stappen. Per stap: een korte naam, wat er gebeurt, en waar het antwoord vandaan
komt. Gebruik deze soorten, in de woorden van de AI lead. De rechterkolom is voor Claude
bij het bouwen, niet voor in het plannetje.

| Soort | Wat het doet | Wordt in Power Automate meestal |
|---|---|---|
| **binnenkomst** | mail, formulier, vast tijdstip, of een ander systeem dat aanklopt | *When a new email arrives (V3)*, *When a new response is submitted* (Forms), *Recurrence*, *When an HTTP request is received* (Premium) |
| **lezen** | AI haalt velden uit tekst of een document | *Run a prompt* (AI Builder). Premium, plus credits en Dataverse in de omgeving: eerst checken met IT |
| **rekenen of checken** | een regel toepassen, iets vergelijken, samenvoegen | *Compose*, *Condition*, *Filter array*, *Select* |
| **splitsen** | op een voorwaarde twee of meer kanten op | *Condition* of *Switch* |
| **mens vraagt of keurt** | de flow wacht tot iemand iets invult of goedkeurt | *Start and wait for an approval*, of *Post adaptive card and wait for a response* (Teams) |
| **ophalen of wegschrijven** | een lijst, een tabel, een API | *Get items* / *Create item* (SharePoint), *List rows present in a table* (Excel), *HTTP* (Premium) |
| **bericht** | mail of Teams | *Send an email (V2)*, *Post message in a chat or channel* |
| **einde** | wat je aan het eind wilt zien | het laatste bericht of de laatste rij; de run zelf zie je in de run history |

Regels voor het plannetje:

- **Na een splitsing** moet elke kant ergens eindigen, al is het maar in een bericht.
- **Wat de mens moet zien, staat in de tekst van de stap.** Een goedkeuring met alleen
  "Goedkeuren?" is nutteloos; zet erin wat er goedgekeurd wordt.
- **Een mail-trigger staat op een eigen map**, met een Outlook-regel die alleen jouw
  testafzenders daarin zet. Nooit op de Inbox of op een map waar al een flow op draait.
  Stuur testmails vanaf een tweede adres, niet vanaf de mailbox van de flow zelf. Anders
  belandt de mail die de flow terugstuurt weer in die map, en start de flow opnieuw.
- **Een AI-stap zonder Premium** kan niet. Laat dan de mens de velden invullen
  (*Post adaptive card and wait for a response* met invoervelden), of zet er een
  `Compose - TODO AI-stap` neer en zet de AI-stap bij versie twee.
- **Geheimen nooit in het plan.** Wachtwoorden en API-sleutels gaan in een connection of
  een environment variable, nooit in een actie.
- **Wat er bewust niet in zit**, schrijf je eronder. Dat is de agenda voor versie twee.

Leg het plannetje voor als tabel, en pas aan tot de AI lead zegt: ja, zo werkt het bij ons.
Dit is het moment waarop de meeste fouten eruit gaan. Niet doorbouwen voordat dit klopt.

---

## Stap 2: de bouwkaart

Nu pas de Power Automate-kant. Werk het plannetje stap voor stap uit. Lees per onderwerp het
bestand in `references/` helemaal; ze zijn kort. Neem deze checklist op in je werkaantekeningen
en vink af:

```
Bouwkaart:
- [ ] 1. Soort flow gekozen (bijna altijd cloud flow)       → references/flow-types.md
- [ ] 2. Trigger, en zo nodig trigger conditions            → references/triggers.md
- [ ] 3. Solution, connections, environment variables       → references/alm-and-governance.md
- [ ] 4. Namen volgens de afspraak                          → references/naming-conventions.md
- [ ] 5. Try/Catch met melding en Terminate bij een fout    → references/error-handling.md
- [ ] 6. Lussen en lijsten (pagination, concurrency)        → references/performance.md
- [ ] 7. Elke expressie gecheckt tegen de harde regels       → references/hard-rules.md
- [ ] 8. Opgeleverd in het formaat hieronder, met testplan
```

Waar je verder kijkt:

- **Expressies** schrijven of repareren: `references/expressions.md`.
- **Veelgebruikte connectors** (SharePoint, Outlook, Teams, Excel, Approvals, bestanden, CSV):
  `references/common-patterns.md`.
- **Een API aanroepen**, of de flow wordt zelf aangeroepen: `references/http-and-rest-apis.md`.
- **De flow wordt aangeroepen door een Copilot Studio-agent**: `references/agent-flow-integration.md`.
- **De flow faalt of start niet**: `references/debugging.md`.

**Solution of niet.** Mag de AI lead in de omgeving een solution maken, bouw dan vanaf de
eerste actie in een solution. Mag dat niet, bouw dan gewoon onder My flows en zet bij de open
punten dat de flow voor productie in een solution moet, samen met IT. Environment variables
bestaan alleen in een solution: onder My flows vul je de waarde (site, lijst, mailbox) direct
in en zet je hem bij de open punten.

**Houd versie één klein.** De references zijn geschreven voor consultants. Neem eruit over
wat de flow nu nodig heeft; service accounts, Key Vault, pipelines, DLP en een centrale
foutlog worden open punten voor IT, geen acties op de bouwkaart. Foutafhandeling in versie
één: een Scope `Try` met het werk, en een Scope `Catch` (run after `Try`: has failed, has
timed out) met één melding in Teams of mail met de link naar de run, daarna Terminate
(Failed). Finally en het uitlezen van de foutmelding komen in versie twee. Actienamen: de
Engelse standaardnaam plus een doel in de taal van de klant, bijvoorbeeld
`Get items - open aanvragen`.

**De AI-stap (*Run a prompt*).** Zet bij een mail eerst *Html to text* voor de mailtekst.
Vraag in de prompt om JSON-uitvoer met vaste veldnamen. Verzin het pad naar die velden niet:
laat de AI lead na de eerste testrun in de outputs van de actie aflezen waar ze staan, en
vul de verwijzingen dan pas in.

**Zo ziet de bouwkaart eruit.** Namen van acties en instellingen in het Engels, precies zoals
ze in de designer staan. Elke stap krijgt één zin in gewone taal, zodat de AI lead hem kan
uitleggen.

````markdown
**Flow:** <naam volgens naming-conventions> · **Soort:** cloud flow (in solution `<naam>` / onder My flows) · **Trigger:** <trigger>
**Nodig:** connections: … · environment variables: … · licentie: standaard | Premium (waarom)

**Variabelen** (alleen als de flow iets moet bijhouden; altijd bovenaan, buiten elke Scope)
1. Initialize variable - `vAantal` (Integer, 0)

**Stappen**
2. Scope - `Try`
   2.1 Get items - `Get items - open aanvragen`
       - Wat dit doet: haalt alle aanvragen op die nog open staan.
       - Site Address: env var `<prefix>_sharepoint_site_url`
       - Filter Query: `Status eq 'Open'`
       - Settings: Pagination aan, threshold 5000
   2.2 …
3. Scope - `Catch` · run after `Try`: has failed, has timed out
   …

**Expressies** (zo typ je ze in de fx-editor, zonder `@` ervoor; trigger conditions en Filter array in advanced mode beginnen juist wel met `@`)
- 2.3 `Compose - vervaldatum`: `addDays(utcNow(), 7, 'yyyy-MM-dd')`

**Testplan**
- Normaal geval · lege of foute invoer · iets downstream faalt (verwacht: Terminate Failed en een melding)

**Aannames en open punten**
````

Bouw alleen wat in het plannetje staat. Vraagt een stap om een koppeling die er nog niet is
(geen Premium, geen toegang tot dat systeem), zet daar dan een `Compose - TODO <wat hier
moet komen>` neer met een notitie. Zo kun je de flow opslaan en de rest testen. Een flow die
draait met een gat erin is beter dan een flow die niet opslaat.

**Nakijken na het bouwen (optioneel).** Staat de flow in een solution, exporteer die dan
(Solutions > Export > unmanaged) en geef de zip aan Claude. Claude draait
`python3 scripts/lint_flow.py <zip>` en bespreekt de fouten en waarschuwingen. Zie
`references/flow-json-and-solutions.md`.

---

## Stap 3: wat je oplevert

1. **De bouwkaart**, met een flownaam die zegt wat hij doet.
2. **De koppelchecklist**, in gewone taal: welke connections de AI lead zelf aanmaakt of
   kiest, welke mailbox of map, welk Teams-kanaal, welke SharePoint-lijst of Excel-tabel
   eerst moet bestaan (met welke kolommen), en of er iets Premium in zit.
3. **Hoe je hem test:** welke mail je stuurt of wat je in het formulier zet, en wat je dan
   moet zien. Eén geval zoals je het in de interviews hoorde, nagebouwd met verzonnen
   gegevens. Echte gegevens van klanten, huurders of collega's horen niet in een test.
   Een flow staat na opslaan meteen aan: zet hem uit (Turn off) tot je gaat testen, of test
   via Test > Manually.
4. **Wat er bewust niet in zit** en waarom.

---

## Standaarden

- Tijdzone `W. Europe Standard Time`. Zet bij een *Recurrence*-trigger de Time zone op
  Amsterdam, dan blijft 08:00 ook na de zomertijd 08:00.
- Nederlandse weergave: `formatDateTime(x, 'dd-MM-yyyy', 'nl-NL')`,
  `formatNumber(x, 'N2', 'nl-NL')`.
- Namen van flows en acties in één taal per project; volg de klant.
- De AI lead is meestal maker, geen beheerder. DLP-regels, service accounts, pipelines en
  Key Vault lopen via IT: zet ze als actiepunt voor IT in de open punten.
- Licenties, prijzen en limieten veranderen vaak. Check ze op learn.microsoft.com voordat de
  AI lead ze aan IT of de klant doorgeeft, en noem de datum.

---

## Later: importeren in plaats van klikken

Power Automate kan een flow importeren als zip (Import package of een solution). Daarmee zou
Claude de flow kunnen invullen in plaats van een bouwkaart te geven: de AI lead exporteert
een flow met alleen de trigger, Claude vult de stappen in, de AI lead importeert hem weer en
kiest de connections. Dat is nog niet getest. Tot dat gebeurd is, lever je een bouwkaart en
geen zelfgemaakt importbestand.

---

## Regels

- **Eén stap uit de blueprint per flow.** Wordt het plan langer dan tien stappen, dan bouw je
  te veel tegelijk.
- **Altijd een mens erin bij versie één**, tenzij de AI lead uitlegt waarom het veilig is.
- **Test en productie blijven gescheiden.** Je bouwt en test in de testomgeving (of bij een prototype de standaardomgeving met een eigen map), met verzonnen
  data. Naar productie gaat een flow pas na een check met IT.
- **Elke stap kun je uitleggen.** Kan de AI lead een actie niet in gewone taal uitleggen, dan
  gaat hij er niet in. Een lange expressie of een HTTP-actie krijgt een extra check van IT
  voordat hij live gaat.
- **Een nieuwe koppeling vraag je aan.** Is een systeem nog niet gekoppeld, of is er Premium
  nodig, dan bouw je er niet omheen, maar vraag je het aan volgens de afspraken van je
  organisatie.
- **Niets verzinnen.** Adressen, kanalen, lijst- en tabelnamen komen van de AI lead. Bestaat
  een functie of actie misschien niet, zeg dat dan in plaats van te gokken.
- **Geen geheimen in het plan of de bouwkaart.**
- Nederlands, je-vorm, korte zinnen, geen em-dashes. Namen van acties en knoppen in het
  Engels, zoals ze in de designer staan.

---

## Wat je vooraf nodig hebt

- Toegang tot Power Automate (make.powerautomate.com), liefst in een testomgeving.
- Een Microsoft 365-licentie voor de standaardconnectors; Power Automate Premium als het plan
  een AI-stap, HTTP, Dataverse of een eigen connector nodig heeft.
- Een goedkeuring (Approvals) werkt in de standaardomgeving meteen. In een andere omgeving
  moet IT het eerst klaarzetten.
- Deze plugin (`ai-lead-skills`) voor het interview, de blueprint en dit plannetje.
