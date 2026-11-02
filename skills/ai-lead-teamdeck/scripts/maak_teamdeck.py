#!/usr/bin/env python3
"""Bouwt het teamdeck van een AI lead uit het sjabloon.

Gebruik:
  python3 maak_teamdeck.py inhoud.json --klant havensteder --uit teamdeck-<team>.html

inhoud.json bevat wat de lead in het interview vertelde (zie SKILL.md, "Wat er in inhoud.json staat").
De klant-voorinstelling (klanten/<naam>.json) levert huisstijl en programmadata. Wat in inhoud.json
staat, gaat voor. Het script controleert de tekst en stopt met een lijst fouten als iets niet klopt.
"""
import argparse, base64, html, json, re, sys, time
from pathlib import Path

HIER = Path(__file__).resolve().parent.parent
SJABLOON = HIER / "sjabloon" / "teamdeck.html"

# Maximale lengtes, zodat alles op de slide past (gemeten op de render van 1280 x 720)
MAX = {"naam": 40, "team": 40, "proces": 80, "meldplek": 70, "testmoment": 90, "taken": 120,
       "tip1.kort": 110, "tip1.kort_uitkomst": 120, "tip1.beter": 300, "tip1.beter_uitkomst": 90,
       "zorg": 140, "cohort_zin": 150, "band": 90, "uren_kop": 30, "planning_tot": 30,
       "matrix.soort": 20, "matrix.ai": 75, "matrix.jij": 75, "signaal": 60,
       "mijlpaal.datum": 16, "mijlpaal.titel": 20, "mijlpaal.tekst": 70}

VERPLICHT = ["organisatie", "cohort_zin", "uren_kop", "planning_tot", "mijlpalen", "testmoment",
             "taken", "tip1", "matrix", "signalen"]


def lees(pad):
    try:
        return json.loads(Path(pad).read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(f"Bestand niet gevonden: {pad}")
    except json.JSONDecodeError as e:
        sys.exit(f"{pad} is geen geldige JSON: {e}")


def data_uri(pad):
    p = Path(pad)
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".svg": "image/svg+xml"}[p.suffix.lower()]
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def tekstlogo(naam, kleur):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="420" height="80"><text x="0" y="56" '
           f'font-family="Helvetica Neue,Arial,sans-serif" font-size="48" font-weight="700" '
           f'fill="{kleur}">{html.escape(naam)}</text></svg>')
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def e(t):
    return html.escape(str(t), quote=True)


def beter_html(t):
    # [[ ... ]] wordt een markering: het stuk dat de prompt beter maakt
    delen = re.split(r"\[\[(.*?)\]\]", t)
    return "".join(f"<mark>{e(d)}</mark>" if i % 2 else e(d) for i, d in enumerate(delen))


def controleer(d):
    fout = []
    for k in VERPLICHT:
        if not d.get(k):
            fout.append(f"'{k}' ontbreekt of is leeg")

    def lengte(sleutel, waarde):
        kaal = re.sub(r"\[\[|\]\]", "", str(waarde))
        if len(kaal) > MAX[sleutel]:
            fout.append(f"'{sleutel}' is {len(kaal)} tekens, maximaal {MAX[sleutel]}: {kaal[:60]}...")

    for k in ["naam", "team", "proces", "meldplek", "testmoment", "taken", "zorg", "cohort_zin",
              "band", "uren_kop", "planning_tot"]:
        if d.get(k):
            lengte(k, d[k])
    tip = d.get("tip1") or {}
    for k in ["kort", "kort_uitkomst", "beter", "beter_uitkomst"]:
        if not tip.get(k):
            fout.append(f"'tip1.{k}' ontbreekt")
        else:
            lengte(f"tip1.{k}", tip[k])
    if tip.get("beter") and "[[" not in tip["beter"]:
        fout.append("'tip1.beter' heeft geen [[markering]] op wat de prompt beter maakt")
    m = d.get("matrix") or []
    if len(m) != 3:
        fout.append(f"'matrix' heeft {len(m)} rijen, het moeten er 3 zijn")
    for r in m:
        for k in ["soort", "ai", "jij"]:
            if not r.get(k):
                fout.append(f"matrixrij mist '{k}'")
            else:
                lengte(f"matrix.{k}", r[k])
    sg = d.get("signalen") or []
    if len(sg) != 4:
        fout.append(f"'signalen' heeft {len(sg)} regels, het moeten er 4 zijn")
    for t in sg:
        lengte("signaal", t)
    mp = d.get("mijlpalen") or []
    if mp and len(mp) != 4:
        fout.append(f"'mijlpalen' heeft {len(mp)} momenten, het moeten er 4 zijn")
    for p in mp:
        for k in ["datum", "titel", "tekst"]:
            if not p.get(k):
                fout.append(f"mijlpaal mist '{k}'")
            else:
                lengte(f"mijlpaal.{k}", p[k])

    alle_tekst = json.dumps(d, ensure_ascii=False)
    if "—" in alle_tekst:
        fout.append("er staat een gedachtestreep (—) in de tekst; gebruik een punt, komma of dubbele punt")
    if re.search(r"\[(?!\[)[A-Za-zÀ-ÿ ]{2,}\](?!\])|\bTODO\b|\bINVULLEN\b|XXX", alle_tekst):
        fout.append("er staat nog een placeholder in de tekst ([...], TODO of INVULLEN)")
    if re.search(r"\bu\b|\buw\b", alle_tekst, re.I):
        fout.append("er staat 'u' of 'uw' in de tekst; het deck spreekt collega's aan met 'je'")
    return fout


def bouw(d, uit):
    s = SJABLOON.read_text(encoding="utf-8")
    k = d["kleur"]
    org = d["organisatie"]
    logo = d.get("_logo_uri") or tekstlogo(org, k["inkt"])
    mijlpalen = "\n".join(
        f'    <div class="mijlpaal{" nu" if p.get("nu") else ""}"><div class="datum">{e(p["datum"])}</div>'
        f'<h3>{e(p["titel"])}</h3><p>{e(p["tekst"])}</p></div>' for p in d["mijlpalen"])
    matrix = "\n".join(
        f'    <div class="taak">{e(r["soort"])}</div><div class="ai">{e(r["ai"])}</div><div>{e(r["jij"])}</div>'
        for r in d["matrix"])
    signalen = "\n".join(
        f'    <div class="signaal"><span class="q">?</span>{e(t)}</div>' for t in d["signalen"])
    zorg = f'<p class="onder" style="margin-top:26px">{e(d["zorg"])}</p>\n  ' if d.get("zorg") else ""
    band = d.get("band") or "Ik doe dit naast mijn gewone werk, en ik blijf gewoon jullie collega."
    slug = re.sub(r"[^a-z0-9]+", "-", f'{org}-{d.get("team", "")}'.lower()).strip("-")
    vervang = {
        "kleur.accent": k["accent"], "kleur.accent_licht": k["accent_licht"], "kleur.steun": k["steun"],
        "kleur.steun_donker": k["steun_donker"], "kleur.vlak": k["vlak"], "kleur.inkt": k["inkt"],
        "font": d["font"], "logo": logo, "organisatie": e(org),
        "spaik_mark": data_uri(HIER / "sjabloon" / "spaik-logomark.svg"),
        "ink": data_uri(HIER / "sjabloon" / "ink-ai-lead-tussen.jpg"),
        "sleutel": f"teamdeck-{slug}-{int(time.time())}",
        "naam": e(d.get("naam", "")), "team": e(d.get("team", "")), "proces": e(d.get("proces", "")),
        "meldplek": e(d.get("meldplek", "")), "testmoment": e(d["testmoment"]),
        "planning_tot": e(d["planning_tot"]), "cohort_zin": e(d["cohort_zin"]), "band": e(band),
        "uren_kop": e(d["uren_kop"]), "mijlpalen": mijlpalen, "zorg": zorg,
        "tip1.kort": e(d["tip1"]["kort"]), "tip1.kort_uitkomst": e(d["tip1"]["kort_uitkomst"]),
        "tip1.beter": beter_html(d["tip1"]["beter"]), "tip1.beter_uitkomst": e(d["tip1"]["beter_uitkomst"]),
        "matrix": matrix, "taken": e(d["taken"].rstrip(". ")), "signalen": signalen,
    }
    for sleutel, waarde in vervang.items():
        s = s.replace(f"⟦{sleutel}⟧", waarde)
    over = re.findall(r"⟦[^⟧]+⟧", s)
    if over:
        sys.exit(f"Sjabloonfout, niet ingevuld: {sorted(set(over))}")
    Path(uit).write_text(s, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inhoud")
    ap.add_argument("--klant", default="neutraal", help="naam van een bestand in klanten/, zonder .json")
    ap.add_argument("--uit", required=True)
    a = ap.parse_args()

    klantpad = HIER / "klanten" / f"{a.klant}.json"
    if not klantpad.exists():
        bekend = ", ".join(p.stem for p in (HIER / "klanten").glob("*.json"))
        sys.exit(f"Geen voorinstelling '{a.klant}'. Bekend: {bekend}")
    d = lees(klantpad)
    inhoud = lees(a.inhoud)
    for sleutel, waarde in inhoud.items():
        if sleutel == "kleur":
            d["kleur"].update(waarde)
        elif waarde not in (None, "", []):
            d[sleutel] = waarde
    if d.get("logo"):
        logo = Path(d["logo"])
        if not logo.is_absolute():
            logo = HIER / "klanten" / logo
        if not logo.exists():
            sys.exit(f"Logo niet gevonden: {logo}")
        d["_logo_uri"] = data_uri(logo)

    fouten = controleer(d)
    if fouten:
        print("Het deck is niet gemaakt. Los dit eerst op:")
        for f in fouten:
            print(f"  - {f}")
        sys.exit(1)
    bouw(d, a.uit)
    leeg = [k for k in ["naam", "team", "proces", "meldplek"] if not d.get(k)]
    print(f"Klaar: {a.uit}")
    if leeg:
        print("Nog leeg (de lead vult het in het deck in, met de knop Invullen): " + ", ".join(leeg))


if __name__ == "__main__":
    main()
