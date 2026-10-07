---
name: ai-lead-blueprint
description: >-
  Maakt van interviewmateriaal een blueprint van het werk: de stappen van links naar rechts,
  met zes banen eronder (wie het merkt, stap en wie, waarmee, hoe lang, wat gaat er mis,
  hoe voelt het). Zet de gaten erbij als vragen voor het volgende gesprek en beantwoordt
  de drie keuzevragen: waar zit de tijd, de fout en de frustratie. Levert een invulbare HTML
  die je aan de mensen kunt laten zien. Triggert op "blueprint maken", "procesmap maken",
  "proces in kaart", "interviews uitwerken naar een plaat".
metadata:
  version: "2.1"
  last_updated: "2026-10-07"
---

# Blueprint-skill voor AI leads

Een procesplaat laat het werk zien, maar niet de mensen. Wie alleen stappen tekent,
vergeet de klant of huurder die wacht, de collega die het overneemt als jij er niet bent, en waar
het pijn doet. Daarom maak je een blueprint: het werk zoals het loopt, mét de mensen
aan beide kanten.

Het blijft een werkblad, geen plaat voor aan de muur. Als hij mooi wordt, ben je te lang
bezig geweest. Het doel is dat je hem kunt laten zien aan de mensen die je sprak, zodat
zij kunnen zeggen wat er niet klopt.

---

## Vraag eerst dit

| Wat | Waarom |
|---|---|
| **Het materiaal** (transcripts, notities, samenvattingen) | Hier komt alles uit |
| **Welk werk** en waar het begint en eindigt | Zonder grenzen loopt de blueprint door tot het einde der tijden |
| **Wie het merkt** als dit werk goed of slecht gaat | De klant of huurder, een collega, een andere afdeling. Dit is de voorkant |
| **Hoeveel mensen** heb je gesproken | Onder de drie is de blueprint een hypothese, zeg dat er dan bij |

Is er geen materiaal, stuur dan terug naar `ai-lead-interview`. Een blueprint uit je hoofd
is precies wat we niet willen.

---

## De opbouw: stappen naar rechts, zes banen naar beneden

De stappen staan als kolommen van links naar rechts, vijf tot tien stuks. Onder elke stap
vul je zes banen in.

| Baan | Wat erin staat | Waar je op let |
|---|---|---|
| **Wie het merkt** | Wie op het resultaat wacht, en wat die ziet of ervaart | De voorkant. Vaak een klant of huurder, soms een collega of afdeling. Staat hier niemand, vraag dan waarom deze stap bestaat |
| **Stap, en wie** | Wat er gebeurt, in de taal van de mensen zelf, en welke rol het doet | Rol, niet naam, tenzij het echt één persoon is. "Iedereen" is geen stap maar een fase |
| **Waarmee** | Systeem, Excel, mail, papier, of het hoofd van één persoon | De achterkant. Het eigen Excel-lijstje en "dat weet alleen Marco" horen hier |
| **Hoe lang** | Actieve minuten én wachttijd apart | Zet erbij of het gemeten of geschat is. Altijd |
| **Wat gaat er mis** | Alleen wat je iemand hebt horen zeggen | Geen "kan efficiënter". Wel "moet drie keer terugbellen" |
| **Hoe voelt het** | Eén lijn van goed naar slecht, voor wie het doet en voor wie het merkt | Bij de diepste dip een letterlijke zin uit het gesprek. Twee lijnen mag, als ze uit elkaar lopen |

### Drie regels die de blueprint bruikbaar houden

**Lege vakjes zijn goed nieuws.** Elk vakje dat je niet kunt invullen is een vraag voor
je volgende gesprek. Vul ze niet in met een aanname, zet ze in de kantlijn. De baan "hoe
voelt het" blijft na het eerste gesprek vaak leeg; dat is de vraag voor het tweede.

**Wachttijd is een eigen getal of hij verdwijnt.** "Duurt twee minuten" is bijna nooit
waar: het is twee minuten typen en dan anderhalve dag wachten op antwoord. Die anderhalve
dag merkt de klant, en is meestal het echte probleem.

**De voorkant is geen aanname.** Wat de klant of collega merkt, heb je van hem gehoord
of in het werk gezien. Weet je het niet, dan is het een gat.

---

## Wat je oplevert

### 1. De blueprint zelf

De stappen met de zes banen, ingevuld met wat er in het materiaal staat. Per cel waar je
iets afleidt in plaats van citeert: markeer dat zichtbaar als afleiding.

### 2. De gaten

Een lijst met wat je nog niet weet, geordend op hoe belangrijk het is. Elk gat is
letterlijk een vraag die je de volgende keer stelt.

### 3. De drie keuzevragen

Beantwoord ze expliciet, met de onderbouwing uit het materiaal:

- **Waar zit de meeste tijd?**
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

- **Eén scrollbare pagina.** Stappen als kolommen, de zes banen als rijen; bij veel stappen
  scrolt de tabel horizontaal, niet de pagina
- **De gevoelslijn als lijn**, niet als tabelcel: een eenvoudige SVG met een punt per stap,
  sleepbaar of met een keuze van 1 tot 5
- **De tabel is bewerkbaar** (`contenteditable`), want tijdens het terugleggen zegt iemand
  "nee, dat gaat anders" en dan wil je het ter plekke aanpassen
- **Autosave naar `localStorage`**, met een zichtbare "opgeslagen om hh:mm"
- **Een knop die de blueprint als markdown downloadt**, zodat er een bestand overblijft
- **Print-CSS** zodat hij op A3 liggend te printen is
- Gaten in de kantlijn, visueel anders dan de ingevulde cellen

Bouw je dit binnen SPAIK, gebruik dan de tokens uit de `spaik-design`-skill. Bouw je het
bij een klant zonder die skill, hou het dan neutraal: één accentkleur, verder zwart op wit.

---

## Wat je hierna doet

1. **Laat de blueprint terugzien** aan de mensen die je sprak, en aan iemand van de
   voorkant als dat kan. Eén vraag: klopt dit? Dat is het goedkoopste moment om erachter te
   komen dat je iets verkeerd begrepen hebt.
2. **Kies één stap** om aan te pakken. Toets hem eerst: kun je de persoon noemen
   die dit mist, en heb je dat zelf gehoord? Nee is nee, en dan gaat hij van de lijst af
   tot je het wél gehoord hebt.
3. **Kies één getal** dat je vandaag al kunt tellen, en meet het nu. Zonder nulmeting kun
   je later niet laten zien dat er iets veranderd is.

---

## Regels

- **Alleen wat gezegd of gezien is.** Elke stap, elk getal, elk knelpunt en elk gevoel is
  terug te voeren op het materiaal. Kun je dat niet, dan is het een gat.
- **Gemeten of geschat, altijd erbij.** Een eerlijk geschat getal is bruikbaar. Een
  geschat getal dat als gemeten wordt gepresenteerd is een probleem.
- **De taal van de mensen zelf**, niet de systeemtaal. Zij zeggen "de brief doorzetten",
  niet "routering naar de oplosgroep".
- **Geen namen bij gevoel of fouten** in een blueprint die je deelt. Een rol volstaat.
- **Geen oplossingen in de blueprint.** Hij beschrijft wat er is. Wat je eraan gaat doen,
  komt daarna.
- Nederlands, je-vorm, geen em-dashes.
