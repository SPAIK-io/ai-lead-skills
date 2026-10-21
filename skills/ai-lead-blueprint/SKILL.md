---
name: ai-lead-blueprint
description: >-
  Maakt van interviewmateriaal een service blueprint van het werk: de stappen van links naar
  rechts, met de banen eronder (de klant, de lijn van zicht, collega's, waarmee, hoe vaak,
  hoe lang, wat gaat mis, hoe voelt het en voor wie). Rekent uit hoeveel tijd je terugwint
  (hoe vaak keer hoe lang), zet de gaten erbij als vragen voor het volgende gesprek en
  beantwoordt de drie keuzevragen: waar zit de tijd, de fout en de frustratie. Levert een
  invulbare HTML die je aan de mensen kunt laten zien. Triggert op "blueprint maken",
  "service blueprint", "procesmap maken", "proces in kaart", "interviews uitwerken naar een plaat".
metadata:
  version: "2.2"
  last_updated: "2026-10-07"
---

# Blueprint-skill voor AI leads

Een procesplaat laat het werk zien, maar niet de mensen. Wie alleen stappen tekent,
vergeet de klant of huurder die wacht, de collega die het overneemt als jij er niet bent, en waar
het pijn doet. Daarom maak je een service blueprint: het werk zoals het loopt, mét de mensen
aan beide kanten.

Bovenaan staat wat de klant doet en merkt. Daaronder, onder een stippellijn, wat collega's
doen en waarmee. Zo loopt het niet door elkaar: je ziet in één oogopslag welk intern werk
de klant laat wachten.

Het blijft een werkblad, geen plaat voor aan de muur. Als hij mooi wordt, ben je te lang
bezig geweest. Het doel is dat je hem kunt laten zien aan de mensen die je sprak, zodat
zij kunnen zeggen wat er niet klopt.

---

## Vraag eerst dit

| Wat | Waarom |
|---|---|
| **Het materiaal** (transcripts, notities, samenvattingen) | Hier komt alles uit |
| **Welk werk** en waar het begint en eindigt | Zonder grenzen loopt de blueprint door tot het einde der tijden |
| **Wie de klant is** van dit werk | De huurder, of de collega of afdeling die op het resultaat wacht. Die komt in de bovenste baan |
| **Hoeveel mensen** heb je gesproken | Onder de drie is de blueprint een hypothese, zeg dat er dan bij |

Is er geen materiaal, stuur dan terug naar `ai-lead-interview`. Een blueprint uit je hoofd
is precies wat we niet willen.

---

## De opbouw: stappen naar rechts, banen naar beneden

De stappen staan als kolommen van links naar rechts, vijf tot tien stuks. Geef elke stap
een korte naam in de taal van de mensen zelf. Onder elke stap vul je de banen in, in deze
volgorde:

| # | Baan | Wat erin staat | Waar je op let |
|---|---|---|---|
| 1 | **De klant** | Wie het merkt: de huurder, of de collega of afdeling die op het resultaat wacht. Wat die doet en wat die merkt | Dit is de klantlaag. Doet de klant bij een stap niets, schrijf dan wat hij merkt: wachten, niets horen, een brief krijgen. Merkt niemand iets van de stap, vraag dan waarom hij bestaat |
| 2 | **Lijn van zicht** | Een stippellijn, geen tekst | Alles eronder ziet de klant niet. Hij merkt het alleen als wachttijd of als fout |
| 3 | **Collega's** | Wat er intern gebeurt, en wie het doet | Rol, niet naam, tenzij het echt één persoon is. "Iedereen" is geen stap maar een fase |
| 4 | **Waarmee** | Systeem, Excel, mail, papier, of het hoofd van één persoon | Het eigen Excel-lijstje en "dat weet alleen Marco" horen hier |
| 5 | **Hoe vaak** | Per dag, week, maand of jaar | Zet erbij of het gemeten of geschat is. Altijd |
| 6 | **Hoe lang** | Per keer: actieve tijd én wachttijd apart | Gemeten of geschat, altijd erbij. Weet je alleen een totaal voor het hele werk, zet dat over de hele breedte en schrijf in de stappen "per stap niet gemeten" |
| 7 | **Wat gaat mis** | Alleen wat iemand gezegd heeft | Geen "kan efficiënter". Wel "moet drie keer terugbellen" |
| 8 | **Hoe voelt het, en voor wie** | Een lijn van goed naar slecht, met de naam of rol van wiens ervaring het is | Klant én collega is twee lijnen. Bij de diepste dip een letterlijke zin uit het gesprek |

### Hoe vaak keer hoe lang

Hoe vaak keer hoe lang is de tijd die je terugwint als een stap sneller of vanzelf gaat.
Weet je bij een stap allebei, reken het dan uit en zet het onder de stap.

- Reken met de **actieve tijd**: dat zijn de uren van collega's. Wachttijd tel je niet mee,
  die kost geen werkuren. Hij hoort wel bij wat de klant merkt, dus noem hem apart.
- Zet beide in dezelfde eenheid, bijvoorbeeld uren per maand.
- Is een van de twee geschat, dan is de uitkomst ook geschat. Schrijf dat erbij.
- Weet je er maar één, reken dan niets uit. Het ontbrekende getal is een gat.

Voorbeeld: 40 keer per week (geschat) keer 12 minuten actief (gemeten) is 8 uur per week,
ongeveer 35 uur per maand. Geschat, want hoe vaak is geschat.

### Drie regels die de blueprint bruikbaar houden

**Lege vakjes zijn goed nieuws.** Elk vakje dat je niet kunt invullen is een vraag voor
je volgende gesprek. Vul ze niet in met een aanname, zet ze in de kantlijn. De baan "hoe
voelt het" blijft na het eerste gesprek vaak leeg; dat is de vraag voor het tweede.

**Wachttijd is een eigen getal of hij verdwijnt.** "Duurt twee minuten" is bijna nooit
waar: het is twee minuten typen en dan anderhalve dag wachten op antwoord. Die anderhalve
dag merkt de klant, en is meestal het echte probleem.

**De klantlaag is geen aanname.** Wat de klant doet en merkt, heb je van hem gehoord of in
het werk gezien. Weet je het niet, dan is het een gat. Wat de klant doet en wat collega's
doen, zet je nooit in dezelfde baan.

---

## Wat je oplevert

### 1. De blueprint zelf

De stappen met alle banen, ingevuld met wat er in het materiaal staat, en per stap de
uitkomst van hoe vaak keer hoe lang als je die kunt uitrekenen. Per cel waar je iets
afleidt in plaats van citeert: markeer dat zichtbaar als afleiding.

In markdown ziet hij er zo uit (één kolom per stap):

```markdown
| | Melding binnen | Inplannen | ... |
|---|---|---|---|
| **De klant** | Huurder belt, krijgt een nummer | Hoort niets | |
| - - - lijn van zicht - - - | | | |
| **Collega's** | Klantcontact zet de melding in het systeem | Planner belt de aannemer | |
| **Waarmee** | Systeem | Excel van de planner, telefoon | |
| **Hoe vaak** | 40 per week (geschat) | 40 per week (geschat) | |
| **Hoe lang** | 6 min actief (gemeten), geen wachttijd | 12 min actief (gemeten), 2 dagen wachten (geschat) | |
| **Terugwinnen** | 4 uur per week (geschat) | 8 uur per week (geschat) | |
| **Wat gaat mis** | | "Moet drie keer terugbellen" (planner) | |
| **Hoe voelt het** | Huurder: 3, planner: 4 | Huurder: 1 "Ik hoor gewoon niks", planner: 2 | |
```

Gevoel schrijf je in markdown als cijfer van 1 (slecht) tot 5 (goed), met voor elke lijn
de rol erbij.

### 2. De gaten

Een lijst met wat je nog niet weet, geordend op hoe belangrijk het is. Elk gat is
letterlijk een vraag die je de volgende keer stelt.

### 3. De drie keuzevragen

Beantwoord ze expliciet, met de onderbouwing uit het materiaal:

- **Waar zit de meeste tijd?** Gebruik hoe vaak keer hoe lang, en zeg of het gemeten of
  geschat is. Zit de meeste tijd in wachten, zeg dat dan apart.
- **Waar gaat het het vaakst mis?**
- **Waar is de dip in de gevoelslijn het diepst, en voor wie?**

Vallen ze op dezelfde stap, dan heb je een sterke kans. Vallen ze uit elkaar, benoem dat
als een keuze in plaats van hem stilletjes te maken. Tijd overtuigt het management. De
dip overtuigt de mensen die het straks moeten gebruiken, en dat zijn degenen die het
aanzetten.

### 4. Wat je vooraf dacht

Eén regel: wat was de aanname, en wat bleek het? Dit is het bewijs dat de gesprekken iets
hebben opgeleverd.

---

## De HTML

Lever de blueprint ook als één HTML-bestand dat de AI lead kan openen en laten zien:

- **Eén scrollbare pagina.** Stappen als kolommen, de banen als rijen in de volgorde
  hierboven; bij veel stappen scrolt de tabel horizontaal, niet de pagina
- **De lijn van zicht als stippellijn** tussen de klant en de collega's, over de hele
  breedte, met het label "lijn van zicht: hieronder ziet de klant niets"
- **Hoe vaak keer hoe lang wordt uitgerekend** zodra beide in een stap staan, met "geschat"
  erbij als een van de twee geschat is
- **De gevoelslijn als lijn**, niet als tabelcel: een eenvoudige SVG met een punt per stap,
  sleepbaar of met een keuze van 1 tot 5. Elke lijn heeft een label met de naam of rol, en
  je kunt een tweede lijn toevoegen. Bij de diepste dip staat de letterlijke zin
- **De tabel is bewerkbaar** (`contenteditable`), want tijdens het terugleggen zegt iemand
  "nee, dat gaat anders" en dan wil je het ter plekke aanpassen
- **Autosave naar `localStorage`**, met een zichtbare "opgeslagen om hh:mm"
- **Een knop die de blueprint als markdown downloadt**, in de vorm hierboven, zodat er een
  bestand overblijft
- **Print-CSS** zodat hij op A3 liggend te printen is
- Gaten in de kantlijn, visueel anders dan de ingevulde cellen

Bouw je dit binnen SPAIK, gebruik dan de tokens uit de `spaik-design`-skill. Bouw je het
bij een klant zonder die skill, hou het dan neutraal: één accentkleur, verder zwart op wit.

---

## Wat je hierna doet

1. **Laat de blueprint terugzien** aan de mensen die je sprak, en aan de klant of collega
   die het merkt als dat kan. Eén vraag: klopt dit? Dat is het goedkoopste moment om
   erachter te komen dat je iets verkeerd begrepen hebt.
2. **Kies één stap** om aan te pakken. Toets hem eerst: wanneer ging dit voor het laatst
   mis, en wie vertelde je dat? Kun je geen moment en geen persoon noemen, dan gaat hij van
   de lijst af tot je het wél gehoord hebt.
3. **Kies één getal** dat je vandaag al kunt tellen, en meet het nu. Zonder nulmeting kun
   je later niet laten zien dat er iets veranderd is. Is hoe vaak of hoe lang bij die stap
   nog geschat, dan is dat een goed eerste getal.

---

## Regels

- **Alleen wat gezegd of gezien is.** Elke stap, elk getal, elk knelpunt en elk gevoel is
  terug te voeren op het materiaal. Kun je dat niet, dan is het een gat.
- **Gemeten of geschat, altijd erbij.** Een eerlijk geschat getal is bruikbaar. Een
  geschat getal dat als gemeten wordt gepresenteerd is een probleem. Dat geldt ook voor de
  uitkomst van hoe vaak keer hoe lang.
- **De taal van de mensen zelf**, niet de systeemtaal. Zij zeggen "de brief doorzetten",
  niet "routering naar de oplosgroep".
- **Geen namen bij gevoel of fouten** in een blueprint die je deelt. Een rol volstaat. Een
  naam bij een gevoelslijn mag alleen in je eigen werkversie.
- **Geen oplossingen in de blueprint.** Hij beschrijft wat er is. Wat je eraan gaat doen,
  komt daarna.
- Nederlands, je-vorm, geen em-dashes.
