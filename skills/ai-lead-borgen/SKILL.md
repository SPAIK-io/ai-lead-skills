---
name: ai-lead-borgen
description: >-
  Helpt een AI lead zijn gebouwde flow te borgen, zodat een ander hem kan uitleggen en
  stilzetten. Maakt drie stukken die bij het certificaat horen: de uitlegkaart (de vijf vragen,
  beantwoord zonder de flow open), de governance-check (zeven punten plus de drempel, met
  tekenregels voor AI-manager, IT-buddy en leidinggevende) en de beheerdocumentatie (negen
  onderdelen) voor de vervanger. Toetst of elke stap uit te leggen is, of per stap duidelijk is
  of het AI is of een gewone stap, en of er een menscontrole en twee namen zijn. Levert één
  invulbare HTML, printbaar op A4, plus een lijst van wat nog open staat en bij wie. Triggert op
  "flow borgen", "uitlegkaart maken", "governance-check invullen", "beheerdocumentatie schrijven",
  "overdracht aan mijn vervanger", "klaar voor livegang", "bewijsstukken voor het certificaat".
metadata:
  version: "1.0"
  last_updated: "2026-11-02"
---

# Borgen: van werkende flow naar een flow die een ander kan beheren

Je flow werkt. Maar als jij op vakantie bent, wat gebeurt er dan? Bij veel flows is het
eerlijke antwoord: niks. Er is één naam, en alles wat je moet weten zit in het hoofd van
die ene persoon.

Deze skill maakt drie stukken die dat oplossen, en die je nodig hebt voor je certificaat:

1. **De uitlegkaart.** Vijf vragen over je flow, beantwoord zonder dat je hem openhebt. Lukt
   dat niet, dan is hij niet af. Uitlegbaar is de norm.
2. **De governance-check.** Zeven punten plus de drempel. Punt 1 tot en met 3 vul je zelf in
   en tekent de AI-manager. Punt 4 tot en met 7 tekent de IT-buddy. De drempel tekent je
   leidinggevende.
3. **De beheerdocumentatie.** Negen onderdelen. Je vervanger moet er de flow mee kunnen
   uitleggen en stilzetten. Hij hoeft hem niet te kunnen bouwen.

De skill vult niets in op gok. Wat jij niet weet, wordt een vraag aan de IT-buddy, de
AI-manager of je leidinggevende. Een lege regel met een eerlijke vraag erbij is beter dan
een mooi antwoord dat niet klopt, want een ander gaat erop vertrouwen.

---

## Vraag eerst dit

Vraag het één voor één, niet als lijst. Ontbreekt iets, dan vraag je het. Je gaat niet
door met een aanname.

| Wat | Waarom |
|---|---|
| **De flow**: een export, het plannetje uit de bouw-skill, of een beschrijving per stap (wat erin gaat, wat eruit komt) | Hier komen de stappen en de uitlegkaart uit. Zonder flow is er niets te borgen |
| **Het platform** (n8n, Lleverage, Power Automate of iets anders) | Bepaalt waar de log, de versies en de uitknop zitten |
| **De flowzin** | "Als er ___ binnenkomt, zet de flow ___ klaar, en ___ beslist." Komt bovenaan de beheerdocumentatie |
| **Wie eigenaar is en wie vervanger**, met hoe je ze bereikt | Twee namen. Is er nog geen vervanger, dan is dat het eerste open punt |
| **De kaders en risiconiveaus van de klant**, als die er zijn | Voor punt 3. Zonder kaders vul je het risiconiveau niet in, dan is het een vraag aan de AI-manager |
| **Wat er na de flow gebeurt**: kijkt een mens naar elke uitkomst, of gaat die zonder mens door naar een klant of systeem? | Bepaalt de drempel: 90% of 95% |
| **De score op de eval-set** van twintig gevallen, als je al gemeten hebt | Voor de drempelregel. Nog niet gemeten? Dan blijft die regel open |
| **Hoe de menscontrole eruitziet**: waar zit de mens, wat ziet hij, wat keurt hij goed | Voor onderdeel 5 van de beheerdocumentatie |

Heb je een export, lees die dan zelf. Maar de lead beantwoordt de vijf vragen eerst in zijn
eigen woorden. Pas daarna leg je zijn antwoord naast de export.

---

## Werkwijze

### 1. De uitlegkaart: eerst zonder de flow

Stel de lead de vijf vragen, één per keer, en laat hem antwoorden zonder te kijken:

| # | Vraag | Waar je op let |
|---|---|---|
| 1 | **Welke data, uit welke bron?** | Elk systeem, elke mailbox, elk bestand bij naam. "Uit het systeem" is te vaag |
| 2 | **Per batch of in één keer?** | Draait hij per geval, of pakt hij een stapel tegelijk, en wanneer? |
| 3 | **Waar valt het besluit?** | Wie beslist, en bij welke stap. Beslist de flow zelf, dan moet dat er staan |
| 4 | **Waarvoor een taalmodel?** | Alleen de stappen waar interpretatie nodig is. Rekenen, filteren en omzetten horen gewone stappen te zijn |
| 5 | **Wat schrijf je terug, en wat log je?** | Waar komt de uitkomst terecht, en wat wordt per stap vastgelegd: wat erin ging en wat eruit kwam |

Leg dan zijn antwoorden naast de flow. Zeg het eerlijk als ze verschillen. Een stap die hij
vergat, een bron die hij niet noemde, een AI-stap die hij een gewone stap noemde: dat zijn
precies de dingen die een vervanger straks ook niet weet. Laat hem het antwoord verbeteren
in zijn eigen woorden, niet in de woorden van de export.

### 2. De stappen langs

Maak per stap één regel: wat erin gaat, wat eruit komt, en of het **AI** of een **gewone
stap** is. Toets elke regel:

- **Kan de lead deze stap uitleggen** aan iemand die er niet bij was? Zo niet, markeer hem.
- **Is duidelijk of het AI is of niet?** Twijfel is een open punt, geen keuze die jij maakt.
- **Doet een AI-stap iets wat een gewone stap ook kan** (rekenen, filteren, omzetten)? Zeg
  het. Een AI-stap kan van dag tot dag iets anders geven.
- **Wat gebeurt er als de flow het niet zeker weet?** Er moet een menscontrole zitten op wat
  de flow niet zeker weet. Begin in adviesstand: de flow doet het werk, een mens beslist.
- **Wordt per stap gelogd** wat erin gaat en wat eruit komt? Alleen de uitkomst checken is
  niet genoeg.

### 3. De governance-check

Vul de zeven punten en de drempel in. Gebruik de tabel in
[`borgen-template.html`](borgen-template.html), die volgt bijlage C van het handboek.

- **Punt 1 tot en met 3** vult de lead in. Jij helpt formuleren, uit wat hij zelf vertelde.
  Bij punt 3: middelhoog risico gaat langs de eigen poort van de klant. Kent de lead de
  kaders niet, dan blijft het antwoord leeg en gaat de vraag naar de AI-manager.
- **Punt 4 tot en met 7** zijn van de IT-buddy. Vul in wat de lead weet en zet erbij dat de
  IT-buddy het moet bevestigen. Wat de lead niet weet, wordt een vraag aan de IT-buddy.
- **De drempel**: 90% als een mens elke uitkomst controleert voordat die verder gaat (18 van
  20 goed op de eval-set). 95% als de uitkomst zonder mens doorgaat naar een klant of een
  systeem (19 van 20 goed, en de vijf lastige gevallen gaan allemaal goed of netjes naar een
  mens). Twintig gevallen is een rookproef, geen meting.
- **Tekenregels blijven leeg.** De skill tekent nooit en zet nooit een vinkje voor iemand.
  Een handtekening is van de AI-manager, de IT-buddy of de leidinggevende.

### 4. De beheerdocumentatie

Schrijf de negen onderdelen voor de vervanger, niet voor de lead. Hij leest het twee
werkdagen voor de overdracht en moet de flow daarna zonder hulp kunnen uitleggen.

1. **Wat de flow doet**, in de flowzin en in vijf regels.
2. **De uitlegkaart**: de vijf vragen.
3. **Eigenaar en vervanger**, met hoe je ze bereikt.
4. **Stappen**: per stap wat erin gaat, wat eruit komt, en of het AI of een gewone stap is.
5. **Menscontrole**: waar zit de mens, wat keurt hij goed, en hoe staat het
   goedkeuringspercentage (het deel dat ongewijzigd wordt goedgekeurd).
6. **Bij een storing**: hoe merk je het, hoe zet je de flow stil, wat doet de afdeling dan,
   wie bel je. De keten is: gebruiker, dan AI lead, dan IT-buddy, dan pas SPAIK en alleen
   voor wat nieuw of ingewikkeld is.
7. **Bij een update van model of platform**: draai de eval-set opnieuw voordat je live gaat.
8. **Als het proces verandert**: wie vertelt het de eigenaar, en welke stappen raakt het.
9. **Waar alles staat**: flow, export, eval-set, log.

Test elk onderdeel met één vraag: kan de vervanger dit doen met alleen deze tekst? "Zet de
flow uit" is geen instructie. "Open de flow in het platform, klik op actief, zet hem op uit"
wel. Weet de lead de knoppen niet, dan is het een vraag aan de IT-buddy.

---

## Wat je oplevert

### In de HTML

Kopieer [`borgen-template.html`](borgen-template.html), noem hem naar de flow (bijvoorbeeld
`borgen-<flow>.html`) en vul hem in. Hij heeft drie tabs: uitlegkaart, governance-check en
beheerdocumentatie. Alle velden zijn bewerkbaar, hij slaat zichzelf op in de browser, en
bij afdrukken komt elke tab op een eigen A4. Een knop zet alles om naar markdown.

- Wat de lead zelf zei, zet je er gewoon in.
- Wat je uit de export haalde en de lead nog niet bevestigde, zet je in een
  `<span class="afgeleid">`. Dat is zichtbaar anders.
- Wat niemand weet, laat je leeg en zet je in het blok **Nog open, en bij wie**.
- De stappentabel heeft vijf regels, want de flowzin gaat uit van drie tot vijf stappen.
  Heeft de flow er meer, voeg dan regels toe en zeg in de chat dat de flow groter is dan
  de flowzin.

### In de chat

Een korte stand, in deze vorm:

```
Wat af is: <welke onderdelen helemaal ingevuld zijn>
Nog niet af: <wat ontbreekt, eerlijk, ook als het veel is>

Vragen voor de IT-buddy:
- <vraag>
Vragen voor de AI-manager:
- <vraag>
Vragen voor de leidinggevende:
- <vraag>
Te tekenen: <wie, welk punt>
```

Zeg het als de flow nog niet af is. Bijvoorbeeld: geen vervanger, geen menscontrole op wat
de flow niet zeker weet, een stap die de lead niet kan uitleggen, of nog geen score op de
eval-set. Dat is geen falen, het is wat er deze week nog moet gebeuren.

---

## Wat hij niet doet

- **Geen antwoorden verzinnen.** Niet voor persoonsgegevens, niet voor de log, niet voor de
  uitknop, niet voor het risiconiveau. Wat de lead niet weet, is een vraag.
- **Niet tekenen.** De tekenregels zijn voor de AI-manager, de IT-buddy en de leidinggevende.
- **Niet meten.** De score op de eval-set komt van de lead. De skill rekent niets na en
  verzint geen percentage.
- **Niet besluiten over de livegang.** Dat doen IT en de AI lead samen, als de drempel
  gehaald is en de governance-check getekend. De datum bepaalt IT.
- **Niet de flow verbeteren.** Valt er iets op (een AI-stap die een gewone stap kan zijn,
  geen log), dan zeg je het. Repareren doe je in de bouw-skill van je platform.
- **Geen adoptieplan of business case.** Dat zijn andere bewijsstukken.

---

## Regels

- **De lead blijft eigenaar.** De beheerdocumentatie is geen overdracht van de flow, maar
  zorgt dat een tweede persoon hem kan uitleggen en stilzetten.
- **Gemeten of geschat, altijd erbij.** Ook bij het goedkeuringspercentage en de score.
- **De woorden van de lead**, niet de namen van nodes of acties uit de export.
- **"Digitale collega met review"**, niet "automatisering", zolang er een mens kijkt naar wat
  de flow niet zeker weet.
- Nederlands, je-vorm, korte zinnen, geen em-dashes.
