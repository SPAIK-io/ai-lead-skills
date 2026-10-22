# Samen een skill maken

Een skill is een vaste instructie die Claude zelf pakt als een vraag erbij past. Hij is de
moeite waard voor werk dat terugkomt en waar je steeds dezelfde correcties maakt. Voor iets
dat je één keer doet is een gewone vraag genoeg.

## Stappen

0. **Bestaat het al?** Doet een skill die de gebruiker al heeft dit (bijvoorbeeld `tegenspraak`
   voor kritisch lezen)? Gebruik die dan. Bouw geen tweede skill die op dezelfde woorden afgaat.
1. **Eerst met de hand.** De gebruiker doet de taak in een gewoon gesprek, met de correcties
   die nodig zijn. Die correcties zijn de grondstof.
2. **Kijk wat Claude zonder skill al kan.** Doe dezelfde taak in een nieuw gesprek buiten het
   Project en zonder uitleg, zodat Project-instructies en andere skills niet meetellen. Wat
   dan al goed gaat, hoort niet in de skill. In de skill komt alleen wat Claude zonder hulp
   fout doet of niet kan weten: eigen regels, voorkeuren, kaders, de toon.
3. **Schrijf het verschil op.** Kort, in gewone taal. Liever tien regels die kloppen dan een
   pagina die Claude ook zonder skill wel weet.
4. **De beschrijving.** Bovenaan staat een beschrijving met de woorden die de gebruiker echt
   typt als de skill moet afgaan ("maak mijn weekverslag", "zet dit in ons format"). Claude kiest
   een skill op die beschrijving, dus vage woorden betekenen dat hij niet afgaat.
5. **Testen.** Twee echte taken waarbij hij moet afgaan, en één waarbij hij juist niet moet
   afgaan. Kijk of Claude in het gesprek laat zien dat de skill gebruikt wordt.
6. **Aanzetten.** Vraag Claude "maak hier een skill van". Lukt dat niet: een map met de naam
   van de skill (kleine letters, streepjes, bijvoorbeeld `weekverslag`), daarin een bestand
   `SKILL.md`, de map zippen en uploaden onder Customize > Skills.
7. **Een plek voor correcties.** Onderaan een eigen skill een kopje "Mijn correcties", waar de
   gebruiker na gebruik zelf een regel bijzet en de skill opnieuw uploadt. Een skill past
   zichzelf niet aan, en een skill uit een plugin kan de gebruiker niet wijzigen.

## Opbouw van een SKILL.md

```text
---
name: weekverslag
description: Maakt mijn weekverslag voor het team in ons vaste format. Gebruik dit als ik
  zeg "maak mijn weekverslag" of mijn aantekeningen van de week deel.
---

# Weekverslag

[Wat de skill doet, in twee zinnen.]

## Zo werk je
1. ...

## Regels
- ...

## Mijn correcties
- ...
```

## Onderhoud

Kijk na een paar weken samen naar het leerlog: welke correcties komen steeds terug? Zet ze in
de skill. Gaat een skill nooit af, dan zit het probleem bijna altijd in de beschrijving.
