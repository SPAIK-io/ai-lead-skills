"""Controleert een n8n-importbestand tegen de bouwstenen die bewezen werken (zie Bouwstenen in SKILL.md).

Gebruik: python3 check_flow.py <bestand>.json   (of: python / py)
Alleen de standaardbibliotheek. Fouten (FOUT) eerst oplossen; waarschuwingen (LET OP) bespreken.
Exit 0 = geen fouten, 1 = fouten, 2 = verkeerd aangeroepen.
"""
import json
import re
import sys

BEWEZEN = {
    "n8n-nodes-base.manualTrigger": {1},
    "n8n-nodes-base.formTrigger": {2.2},
    "n8n-nodes-base.extractFromFile": {1.1},
    "n8n-nodes-base.dataTable": {1.1},
    "n8n-nodes-base.filter": {2.2},
    "n8n-nodes-base.if": {2.2},
    "n8n-nodes-base.set": {3.4},
    "n8n-nodes-base.summarize": {1.1},
    "n8n-nodes-base.sort": {1},
    "n8n-nodes-base.merge": {3.2},
    "n8n-nodes-base.noOp": {1},
}
CODE = "n8n-nodes-base.code"
STICKY = "n8n-nodes-base.stickyNote"
BEGIN = {
    "n8n-nodes-base.manualTrigger",
    "n8n-nodes-base.formTrigger",
    "n8n-nodes-base.webhook",
    "n8n-nodes-base.scheduleTrigger",
}
MEER_INGANGEN = {"n8n-nodes-base.merge", "n8n-nodes-base.compareDatasets"}
# Interne n8n-blokken die niet met een ander systeem praten, maar ook niet bewezen zijn.
KERN = {"n8n-nodes-base." + k for k in (
    "noOp", "stickyNote", "wait", "splitOut", "aggregate", "limit", "removeDuplicates",
    "dateTime", "splitInBatches", "extractFromFile", "convertToFile", "html", "xml", "markdown",
    "compareDatasets", "renameKeys", "switch", "crypto", "respondToWebhook", "form", "stopAndError",
)} | BEGIN
CODE_SLEUTELS = {"jsCode", "pythonCode"}
CODE_NAAR_BUITEN = re.compile(r"httpRequest|\bfetch\s*\(")
DATATABLE_OK = {"get", "insert"}
# Blokken die met een ander systeem praten. Ook hun Trigger- en Tool-variant telt mee.
KOPPELINGEN = {
    "httpRequest", "emailSend", "emailReadImap", "microsoftOutlook", "microsoftTeams",
    "microsoftExcel", "microsoftOneDrive", "microsoftSharePoint", "microsoftToDo", "gmail",
    "googleSheets", "googleDrive", "googleCalendar", "slack", "telegram", "discord",
    "postgres", "mySql", "microsoftSql", "mongoDb", "redis", "oracleDatabase", "snowflake",
    "ftp", "ssh", "executeCommand", "readWriteFile", "awsS3", "sendGrid", "twilio", "openAi",
    "jira", "salesforce", "hubspot", "notion", "airtable", "supabase", "graphql", "rssFeedRead",
    "aiTransform", "n8n",
}
KOPPEL_TEKST = "koppeling of AI-blok: niet toegestaan zonder akkoord"
UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
GEHEIME_SLEUTEL = re.compile(
    r"^(api[_-]?key|apikey|x[_-]api[_-]key|password|passwd|wachtwoord|secret|client[_-]?secret|"
    r"token|access[_-]?token|auth[_-]?token|refresh[_-]?token|bearer|authorization|private[_-]?key)$",
    re.I,
)
GEHEIME_WAARDE = re.compile(
    r"(^(bearer|basic)\s+[A-Za-z0-9._~+/=-]{12,}$)|(\b(sk|pk|rk)-[A-Za-z0-9_-]{16,})|"
    r"(\bgh[pousr]_[A-Za-z0-9]{20,})|(\bxox[abpr]-[A-Za-z0-9-]{10,})|"
    r"(\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.)|(-----BEGIN [A-Z ]*PRIVATE KEY-----)",
    re.I,
)
VERWIJZING = re.compile(r"""\$\(\s*(['"])(.+?)\1\s*\)|\$node\[\s*(['"])(.+?)\3\s*\]""")


def versie(v):
    """Maakt van 1, 1.0, "1" en "1.1" een vergelijkbaar getal; None als het niet kan."""
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        try:
            return float(v.strip())
        except ValueError:
            return None
    return None


def teksten(waarde, sleutel=""):
    """Alle (sleutel, tekst)-paren in een geneste structuur."""
    if isinstance(waarde, dict):
        for k, v in waarde.items():
            yield from teksten(v, str(k))
    elif isinstance(waarde, list):
        for v in waarde:
            yield from teksten(v, sleutel)
    elif isinstance(waarde, str):
        yield sleutel, waarde


def is_koppeling(soort):
    if soort.startswith("@n8n/n8n-nodes-langchain."):
        return True
    if soort.startswith("n8n-nodes-base."):
        kort = soort.split(".", 1)[1]
        for staart in ("Trigger", "Tool"):
            if kort.endswith(staart):
                kort = kort[: -len(staart)]
        return kort in KOPPELINGEN
    return False


def check(pad):
    fouten, letop = [], []
    try:
        with open(pad, encoding="utf-8-sig") as f:
            wf = json.load(f)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
        return [f"geen geldige JSON: {e}"], []

    if not isinstance(wf, dict):
        return ["bovenste niveau is geen object ({...}); dit is geen n8n-workflow"], []
    for sleutel in ("name", "nodes", "connections", "settings"):
        if sleutel not in wf:
            fouten.append(f"veld '{sleutel}' ontbreekt bovenin")
    nodes = wf.get("nodes", [])
    if not isinstance(nodes, list):
        fouten.append("'nodes' is geen lijst")
        nodes = []
    elif not nodes:
        fouten.append("'nodes' is leeg: er staat geen enkel blok in de flow")
    connections = wf.get("connections", {})
    if not isinstance(connections, dict):
        fouten.append("'connections' is geen object")
        connections = {}
    if wf.get("active") is not False:
        fouten.append("'active' moet false zijn: de beheerder zet de flow aan")
    settings = wf.get("settings") if isinstance(wf.get("settings"), dict) else {}
    if settings.get("timezone") != "Europe/Amsterdam":
        fouten.append("settings.timezone moet 'Europe/Amsterdam' zijn (anders datums een dag te vroeg)")
    if wf.get("pinData"):
        fouten.append("pinData is niet leeg: vastgezette gegevens, mogelijk echte gegevens. Haal ze weg")

    soorten, namen, ids = {}, set(), set()
    geldige_nodes = []
    for i, n in enumerate(nodes):
        if not isinstance(n, dict):
            fouten.append(f"blok {i + 1} is geen object")
            continue
        naam = n.get("name")
        if not isinstance(naam, str) or not naam.strip():
            fouten.append(f"blok {i + 1} heeft geen naam")
            continue
        if naam in namen:
            fouten.append(f"naam dubbel: '{naam}' (verbindingen gaan op naam)")
        namen.add(naam)
        nid = str(n.get("id", "")).lower()
        if nid and nid in ids:
            fouten.append(f"'{naam}': id dubbel ({n.get('id')}); elk blok heeft een eigen id nodig")
        ids.add(nid)
        soorten[naam] = n.get("type")
        geldige_nodes.append(n)

    for n in geldige_nodes:
        naam, soort = n["name"], n.get("type")
        params = n.get("parameters") if isinstance(n.get("parameters"), dict) else {}
        if not isinstance(soort, str) or not soort:
            fouten.append(f"'{naam}': type ontbreekt")
            continue
        if "typeVersion" not in n:
            fouten.append(f"'{naam}': typeVersion ontbreekt")
        elif versie(n.get("typeVersion")) is None:
            fouten.append(f"'{naam}': typeVersion '{n.get('typeVersion')}' is geen getal")
        pos = n.get("position")
        if not (isinstance(pos, list) and len(pos) == 2
                and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in pos)):
            fouten.append(f"'{naam}': position ontbreekt of is geen [x, y]")
        if not UUID.match(str(n.get("id", ""))):
            fouten.append(f"'{naam}': id is geen UUID")
        if soort == STICKY:
            continue

        v = versie(n.get("typeVersion"))
        notitie_gemeld = False
        if is_koppeling(soort):
            fouten.append(f"'{naam}': {soort}: {KOPPEL_TEKST}")
        elif soort == CODE:
            notitie = str(n.get("notes", "")).lstrip().lower()
            if not notitie.startswith(("waarom code:", "why code:")):
                fouten.append(f"'{naam}': codeblok zonder notitie die begint met 'Waarom code:'")
                notitie_gemeld = True
            letop.append(f"'{naam}': codeblok; de lead moet het kunnen uitleggen en IT kijkt extra mee")
            code = " ".join(str(params.get(k, "")) for k in CODE_SLEUTELS)
            if CODE_NAAR_BUITEN.search(code):
                letop.append(f"'{naam}': code roept iets buiten n8n aan (httpRequest of fetch); dat is een koppeling")
        elif soort in BEWEZEN:
            if v is not None and v not in {float(x) for x in BEWEZEN[soort]}:
                letop.append(f"'{naam}': {soort} versie {n.get('typeVersion')}, bewezen is {sorted(BEWEZEN[soort])}")
        elif soort in KERN:
            letop.append(f"'{naam}': blok {soort} staat niet in de bouwstenen (niet getest)")
        else:
            fouten.append(f"'{naam}': {soort}: onbekend blok, mogelijk koppeling: eerst akkoord")

        if not notitie_gemeld and (not str(n.get("notes", "")).strip() or n.get("notesInFlow") is not True):
            fouten.append(f"'{naam}': notitie ontbreekt (notes + notesInFlow: true)")
        if "credentials" in n:
            fouten.append(f"'{naam}': bevat credentials; die horen niet in het bestand")
        if soort == "n8n-nodes-base.formTrigger" and not UUID.match(str(n.get("webhookId", ""))):
            fouten.append(f"'{naam}': Form Trigger heeft een webhookId (UUID) nodig")
        if soort == "n8n-nodes-base.webhook":
            letop.append(f"'{naam}': webhook als begin; een beheerder moet de flow aanzetten voordat hij werkt")
        if soort == "n8n-nodes-base.dataTable":
            rl = params.get("dataTableId") if isinstance(params.get("dataTableId"), dict) else {}
            if not rl.get("value"):
                letop.append(f"'{naam}': geen tabel gekozen; de lead kiest hem na het importeren")
            operatie = params.get("operation", "insert")
            if operatie == "get" and "limit" not in params and not params.get("returnAll"):
                letop.append(f"'{naam}': Data Table get zonder limit (standaard maar 50 rijen); zet limit, bv. 500")
            if operatie not in DATATABLE_OK:
                letop.append(f"'{naam}': Data Table '{operatie}' verandert of verwijdert rijen; bewezen zijn alleen get en insert")
        voorwaarden = params.get("conditions")
        opties = voorwaarden.get("options") if isinstance(voorwaarden, dict) else None
        if isinstance(opties, dict) and opties.get("typeValidation") == "strict":
            letop.append(f"'{naam}': typeValidation 'strict'; bewezen is 'loose' (strict faalt op een getal als tekst)")

        gemeld_geheim = False
        for sleutel, tekst in teksten(params):
            if sleutel not in CODE_SLEUTELS and "{{" in tekst and "}}" in tekst and not tekst.startswith("="):
                letop.append(f"'{naam}': veld '{sleutel}' bevat {{{{ }}}} maar begint niet met '='; n8n leest het als gewone tekst")
            for m in VERWIJZING.finditer(tekst):
                doel = m.group(2) or m.group(4)
                if doel not in namen:
                    fouten.append(f"'{naam}': verwijst naar blok '{doel}', dat niet bestaat")
            if not gemeld_geheim and tekst.strip() and (
                (GEHEIME_SLEUTEL.match(sleutel) and not tekst.startswith("=")) or GEHEIME_WAARDE.search(tekst)
            ):
                letop.append(f"'{naam}': veld '{sleutel}' lijkt een wachtwoord of sleutel; controleer en haal weg")
                gemeld_geheim = True

    if geldige_nodes and not any(n.get("type") in BEGIN for n in geldige_nodes):
        fouten.append("geen beginblok (Manual Trigger, Form Trigger, Webhook of Schedule Trigger)")

    verbonden = set()
    for van, uit in connections.items():
        if van not in namen:
            fouten.append(f"verbinding vanaf onbekend blok '{van}'")
        verbonden.add(van)
        if not isinstance(uit, dict):
            fouten.append(f"verbindingen van '{van}' hebben niet de vorm {{\"main\": [[...]]}}")
            continue
        for soort_verb, takken in uit.items():
            if not isinstance(takken, list):
                fouten.append(f"verbindingen van '{van}' ({soort_verb}) zijn geen lijst")
                continue
            for tak in takken:
                if tak is None:
                    continue
                if not isinstance(tak, list):
                    fouten.append(f"een uitgang van '{van}' is geen lijst")
                    continue
                for doel in tak:
                    if not isinstance(doel, dict) or not isinstance(doel.get("node"), str):
                        fouten.append(f"een verbinding van '{van}' mist 'node'")
                        continue
                    naar = doel["node"]
                    verbonden.add(naar)
                    if naar not in namen:
                        fouten.append(f"verbinding van '{van}' naar onbekend blok '{naar}'")
                        continue
                    index = doel.get("index", 0)
                    if not isinstance(index, int) or isinstance(index, bool):
                        fouten.append(f"verbinding van '{van}' naar '{naar}': index is geen getal")
                    elif index >= 1 and soorten.get(naar) not in MEER_INGANGEN:
                        fouten.append(f"verbinding van '{van}' naar ingang {index} van '{naar}', maar dat blok heeft één ingang")
    echte = {n["name"] for n in geldige_nodes if n.get("type") != STICKY}
    if len(echte) > 1:
        for naam in sorted(echte - verbonden):
            letop.append(f"'{naam}' hangt los (geen verbinding)")
    return fouten, letop


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    fouten, letop = check(sys.argv[1])
    for f in fouten:
        print("FOUT  ", f)
    for w in letop:
        print("LET OP", w)
    print(f"{len(fouten)} fout(en), {len(letop)} waarschuwing(en)")
    sys.exit(1 if fouten else 0)
