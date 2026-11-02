---
name: ai-lead-teamdeck
description: >-
  Maakt het teamdeck waarmee een AI lead zijn eigen afdeling meeneemt: wat zijn rol is, vijf
  tips die collega's morgen al gebruiken, en twee dingen die hij van ze nodig heeft (ergernissen
  melden en meetesten). Eerst een kort interview over het team, dan vult een script een vast
  sjabloon in de huisstijl van de organisatie. Levert één HTML die de lead zelf presenteert,
  20 tot 30 minuten in het teamoverleg. Triggert op "teamdeck", "deck voor mijn team",
  "mijn team meenemen", "presentatie voor mijn afdeling", "collega's meekrijgen", "teamoverleg
  over AI".
metadata:
  version: "1.0"
  last_updated: "2026-11-02"
---

# Teamdeck voor AI leads

Een flow die niemand gebruikt, is weggegooid werk. Je collega's moeten weten wat je doet,
er iets aan hebben, en je vertellen waar het werk knelt. Een algemeen AI-praatje doet dat niet.
Voorbeelden uit hun eigen week wel.

Daarom stel je eerst vragen over het team, en vult een script daarna een vast deck: vijftien
slides, de opbouw en vormgeving liggen vast. Jij schrijft alleen de tekst die bij deze afdeling
hoort. Zo ziet elk deck er goed uit, en kan er geen datum of huisstijl mis gaan.

---

## Vraag eerst dit

Stel de vragen één voor één, in spreektaal. Wacht op het antwoord voor je de volgende stelt.
Weet de lead iets niet, laat het dan leeg: hij vult het later in het deck zelf in.

| # | Vraag | Waar het in het deck komt |
|---|---|---|
| 1 | **Voor welke organisatie?** Staat die in `klanten/`, dan komen huisstijl en programmadata daaruit. Anders: zie "Nieuwe organisatie" | Huisstijl, planning, slide 2 |
| 2 | **Je naam en je team.** Wat doet het team, in één zin, en met hoeveel mensen? | Omslag, coachprompt |
| 3 | **Welk werk komt elke week terug?** Vraag door tot je drie of vier concrete taken hebt, met wie ze doet en voor wie | Voorbeeldprompt, het overzicht AI of jij, coachprompt |
| 4 | **Welk proces heb je gekozen?** In één zin, in de woorden van het team | Slide 4 |
| 5 | **Hoe kijkt je team naar AI?** Wie is enthousiast, wie sceptisch of bang, en waarvoor? Wat zei iemand letterlijk? Heb je een vier-krachtenkaart of borgingskaart, gebruik die | De zin over de zorg op slide 5 |
| 6 | **Waar loopt je team tegenaan?** Overtypen, zoeken, steeds dezelfde vraag, dubbel werk | De vier ergernissen op slide 13 |
| 7 | **Waar kunnen collega's ideeën kwijt, en wanneer kunnen ze meetesten?** | Slide 13 en 14 |

Vraag niet naar namen van collega's of huurders en klanten. Die horen niet in het deck.

---

## Wat je schrijft

Je schrijft `inhoud.json`. Het voorbeeld staat in `voorbeeld/inhoud-voorbeeld.json`: kopieer de
vorm, niet de tekst.

| Veld | Wat | Let op |
|---|---|---|
| `naam`, `team`, `proces`, `meldplek` | Uit vraag 2, 4 en 7 | Mag leeg, dan vult de lead het in het deck in |
| `taken` | Drie terugkerende taken in één zin, zonder punt | Komt in de coachprompt na "Mijn terugkerende taken zijn:" |
| `tip1.kort` | Een korte, vage opdracht voor een taak uit vraag 3 | Zo vraagt iemand het die AI nog niet kent |
| `tip1.kort_uitkomst` | Wat er dan uitkomt, in één zin | Eerlijk: netjes maar leeg |
| `tip1.beter` | Dezelfde opdracht met het waarom erbij, en aan het eind "Vraag me eerst wat je nog moet weten." | Zet wat de prompt beter maakt tussen `[[` en `]]`. Geen persoonsgegevens: geen naam, geen gezinssituatie, geen adres |
| `tip1.beter_uitkomst` | Wat er dan gebeurt, in één zin | |
| `matrix` | Drie rijen: `soort` (een mail, een verslag, uitzoeken), `ai` (AI maakt de eerste versie) en `jij` (jij doet het zelf) | Links routine. Rechts werk met een oordeel, een emotie, of gevolgen voor één persoon |
| `signalen` | Vier ergernissen uit vraag 6, als "Je ..."-zin | De laatste mag "Je denkt: dit moet toch slimmer kunnen" zijn |
| `zorg` | Optioneel. De zorg uit vraag 5 eerlijk benoemd, en wat er echt gebeurt | Beloof niets wat de lead niet kan waarmaken, zoals "niemand verliest zijn baan". Wel: wat de flow klaarzet, ziet eerst een mens |

Voor een organisatie zonder voorinstelling komen er vijf velden bij: `organisatie`, `cohort_zin`
(wat er gebeurt: hoeveel leads, wie het overzicht houdt), `uren_kop` (bijvoorbeeld "Een dag per
week."), `planning_tot`, `mijlpalen` (vier: `datum`, `titel`, `tekst`, en `nu: true` bij de
eerstvolgende) en `testmoment`. Vraag die aan de lead, of laat de AI-manager ze aanleveren.
Verzin geen data.

**Schrijfregels.** Je-vorm, nooit "u". Korte zinnen die je hardop zou zeggen. Geen gedachtestreep.
"Digitale collega" in een hele zin, niet "agent". Woorden uit het team zelf, geen AI-jargon.

---

## Bouwen

1. **Laat de lead de inhoud eerst zien**, als een kort overzicht in de chat: de voorbeeldprompt,
   de drie rijen, de vier ergernissen en de zin over de zorg. Vraag: klopt dit voor je team?
   Pas aan tot hij ja zegt.
2. **Draai het script:**
   ```
   python3 scripts/maak_teamdeck.py inhoud.json --klant <naam> --uit teamdeck-<team>.html
   ```
   `--klant` is een bestand in `klanten/` zonder `.json`, of `neutraal`. Het script controleert
   lengtes, het aantal rijen, gedachtestreepjes, placeholders en "u". Stopt het met een lijst,
   los die op in `inhoud.json` en draai opnieuw. Maak een te lange zin korter, niet de letter kleiner.
3. **Lever het HTML-bestand op.** Kun je het openen, bekijk dan slide 7, 9 en 13: die hebben de
   meeste tekst.

---

## Nieuwe organisatie

Heeft de organisatie nog geen bestand in `klanten/`, gebruik dan `neutraal` en vraag de lead om
de kleur van de organisatie als hexcode (`"kleur": {"accent": "#..."}` in `inhoud.json`) en het
logo als PNG of SVG (`"logo": "/pad/naar/logo.png"`). Zonder logo zet het script de naam van de
organisatie neer. Wordt het deck vaker gebruikt bij dezelfde organisatie, maak dan een eigen
bestand in `klanten/` naar het voorbeeld van `havensteder.json`, met in `bron` waar de kleuren
en de data vandaan komen.

---

## Wat je oplevert

- `teamdeck-<team>.html`: één bestand, werkt offline, opent in elke browser.
- Drie regels uitleg voor de lead:
  - Openen, dan **Invullen** voor wat nog leeg is, dan **Klaar**.
  - Presenteren met de pijltjes, **F** voor volledig scherm. Eindig met de vraag op de laatste
    slide en schrijf mee wat je hoort: dat zijn je volgende gesprekken.
  - **PDF** om het daarna met je team te delen.

## Wat je niet doet

- Geen slides toevoegen, weghalen of anders vormgeven. Mist er iets, meld het aan SPAIK.
- Geen beloftes over banen, besparingen of livedatums die de lead niet zelf kan waarmaken.
- Geen cijfers verzinnen. Het deck heeft er geen nodig.
