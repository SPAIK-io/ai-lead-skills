---
name: ai-lead-procesmap
description: >-
  Maakt van interviewmateriaal een procesmap van vier kolommen: stap, wie doet het,
  hoe lang, wat gaat er mis. Zet de gaten erbij als vragen voor het volgende gesprek
  en beantwoordt de twee keuzevragen: waar zit de meeste tijd en waar zit de meeste
  frustratie. Levert een invulbare HTML die je aan de mensen kunt laten zien.
  Triggert op "procesmap maken", "proces in kaart", "interviews uitwerken naar een plaat".
metadata:
  version: "1.0"
  last_updated: "2026-08-12"
---

# Procesmap-skill voor AI leads

Een procesmap is een werkblad, geen plaat voor aan de muur. Als hij mooi wordt, ben je
te lang bezig geweest. Het doel is dat je hem kunt laten zien aan de mensen die je
sprak, zodat zij kunnen zeggen wat er niet klopt.

---

## Vraag eerst dit

| Wat | Waarom |
|---|---|
| **Het materiaal** (transcripts, notities, samenvattingen) | Hier komt alles uit |
| **Welk proces** en waar het begint en eindigt | Zonder grenzen loopt de map door tot het einde der tijden |
| **Hoeveel mensen** heb je gesproken | Onder de drie is de map een hypothese, zeg dat er dan bij |

Is er geen materiaal, stuur dan terug naar `ai-lead-interview`. Een procesmap uit je
hoofd is precies wat we niet willen.

---

## De vier kolommen, meer niet

| Kolom | Wat erin staat | Waar je op let |
|---|---|---|
| **Stap** | Wat er gebeurt, in de taal van de mensen zelf | Vijf tot tien stappen. Meer betekent dat je te fijn hebt gesneden |
| **Wie doet het** | Rol, niet naam, tenzij het echt één persoon is | Staat er "iedereen", dan is het geen stap maar een fase |
| **Hoe lang** | Actieve minuten én wachttijd apart | Zet erbij of het gemeten of geschat is. Altijd |
| **Wat gaat er mis** | Alleen wat je iemand hebt horen zeggen | Geen "kan efficiënter". Wel "moet drie keer terugbellen" |

### Twee regels die de map bruikbaar houden

**Lege vakjes zijn goed nieuws.** Elk vakje dat je niet kunt invullen is een vraag voor
je volgende gesprek. Vul ze niet in met een aanname, zet ze in de kantlijn.

**Wachttijd is een eigen kolom of hij verdwijnt.** "Duurt twee minuten" is bijna nooit
waar: het is twee minuten typen en dan anderhalve dag wachten op antwoord. Die
anderhalve dag is meestal het echte probleem.

---

## Wat je oplevert

### 1. De map zelf

Een tabel met de vier kolommen, ingevuld met wat er in het materiaal staat. Per cel
waar je iets afleidt in plaats van citeert: markeer dat zichtbaar als afleiding.

### 2. De gaten

Een lijst met wat je nog niet weet, geordend op hoe belangrijk het is. Elk gat is
letterlijk een vraag die je de volgende keer stelt.

### 3. De twee keuzevragen

Beantwoord deze twee expliciet, met de onderbouwing uit het materiaal:

- **Waar zit de meeste tijd?**
- **Waar zit de meeste frustratie?**

Is dat niet dezelfde stap, benoem dat als een keuze in plaats van hem stilletjes te
maken. Tijd overtuigt het management. Frustratie overtuigt de mensen die het straks
moeten gaan gebruiken, en dat zijn degenen die het aanzetten.

### 4. Wat je vooraf dacht

Eén regel: wat was de aanname, en wat bleek het? Dit is het bewijs dat de gesprekken
iets hebben opgeleverd.

---

## De HTML

Lever de map ook als één HTML-bestand dat de AI lead kan openen en laten zien:

- **Eén scrollbare pagina.** Geen tabbladen, geen meerdere schermen
- **De tabel is bewerkbaar** (`contenteditable`), want tijdens het terugleggen zegt
  iemand "nee, dat gaat anders" en dan wil je het ter plekke aanpassen
- **Autosave naar `localStorage`**, met een zichtbare "opgeslagen om hh:mm"
- **Een knop die de map als markdown downloadt**, zodat er een bestand overblijft
- **Print-CSS** zodat het op A4 liggend te printen is
- Gaten in de kantlijn, visueel anders dan de ingevulde cellen

Bouw je dit binnen SPAIK, gebruik dan de tokens uit de `spaik-design`-skill. Bouw je
het bij een klant zonder die skill, hou het dan neutraal: één accentkleur, verder
zwart op wit.

---

## Wat je hierna doet

1. **Laat de map terugzien** aan de mensen die je sprak. Eén vraag: klopt dit? Dat is
   het goedkoopste moment om erachter te komen dat je iets verkeerd begrepen hebt.
2. **Kies één stap** om aan te pakken. Loop hem langs de poort: kun je de persoon
   noemen die dit mist, en heb je dat zelf gehoord? Nee is nee, en dan gaat hij van de
   lijst af tot je het wél gehoord hebt.
3. **Kies één getal** dat je vandaag al kunt tellen, en meet het nu. Zonder nulmeting
   kun je later niet laten zien dat er iets veranderd is.

---

## Regels

- **Alleen wat gezegd is.** Elke stap, elk getal en elk knelpunt is terug te voeren op
  het materiaal. Kun je dat niet, dan is het een gat.
- **Gemeten of geschat, altijd erbij.** Een eerlijk geschat getal is bruikbaar. Een
  geschat getal dat als gemeten wordt gepresenteerd is een probleem.
- **De taal van de mensen zelf**, niet de systeemtaal. Zij zeggen "de order overtypen",
  niet "orderinvoer in het ERP".
- **Geen oplossingen in de map.** De map beschrijft wat er is. Wat je eraan gaat doen,
  komt daarna.
- Nederlands, je-vorm, geen em-dashes.
