#!/usr/bin/env python3
"""Bouwt een importeerbare Lleverage-workflow uit een plannetje.

Gebruik:  python3 build_flow.py plan.json > workflow.json
          python3 build_flow.py plan.json --check      (alleen valideren)

Het plannetje is klein en leesbaar; dit script doet het typen. Het bouwt ALLEEN met
bouwstenen die we kennen (zie bouwstenen.md). Vraag je iets anders, dan weigert het
met een duidelijke melding in plaats van een JSON die niet importeert.

Plan-formaat (JSON):
{
  "naam": "Korte naam",
  "trigger": {"soort": "mail" | "app" | "schedule" | "api",
              "velden": {"Tekst": "uitleg"}          (alleen app / api)
              "cron": "0 7 * * 1-5"}                  (alleen schedule)
  "stappen": [
    {"naam": "Lees_Mail", "soort": "llm", "prompt": "...{{Mailbox.data.body}}...",
     "uitvoer": {"klant": "string", "regels": "array"}},
    {"naam": "Check", "soort": "js", "script": "return {ok: Lees_Mail.output.klant !== ''};"},
    {"naam": "Splits", "soort": "branch", "condities": {"ok": "Check.result.ok === true", "niet_ok": "Check.result.ok === false"}},
    {"naam": "Vraag_Mens", "soort": "mens_vraag", "titel": "...", "velden": {"Antwoord": "string"}, "na": "Splits.niet_ok"},
    {"naam": "Keur", "soort": "mens_keur", "titel": "...", "na": "Vraag_Mens"},
    {"naam": "Mail_Terug", "soort": "mail_sturen", "aan": "...", "onderwerp": "...", "tekst": "...", "na": "Keur.goed"},
    {"naam": "Antwoord", "soort": "mail_beantwoorden", "tekst": "..."},
    {"naam": "Slack", "soort": "slack", "tekst": "..."},
    {"naam": "Haal_Op", "soort": "http", "url": "...", "methode": "GET"},
    {"naam": "Lees_Tekst", "soort": "extract", "bron": "Form.data.Tekst", "uitvoer": {"naam": "string"}},
    {"naam": "Bewaar", "soort": "tabel_schrijven", "tabel": "leads", "data": {"naam": "{{Lees_Tekst.output.naam}}"}},
    {"naam": "Klaar", "soort": "output", "tekst": "..."}
  ]
}
Volgorde = lijstvolgorde, tenzij "na" iets anders zegt ("Stap" of "Branch.tak" of "Keur.goed"/"Keur.fout").
Soorten uitvoer: "string", "number", "boolean", "array" (van objecten met vrije velden), "string?" (mag null).
"""
import json, re, sys, uuid

X0, XSTEP, Y, YSTEP = 45, 440, 45, 300
KIES = "<KIES NA IMPORT>"
MODEL = {"languageModelId": 46, "modelName": "anthropic/claude-sonnet-4.6", "providerName": "Anthropic"}
EXTRACT_MODEL = {"languageModelId": 48, "modelName": "openai/gpt-5.4-mini", "providerName": "OpenAI"}
RETRY = {"intervalMs": 1000, "maxRetries": 2, "onFailStrategy": "fail"}
OUTLOOK_BASE = "https://actions.lleverage.ai/nodes"


def lit(v): return {"type": "literal", "value": v}
def auto(v): return {"type": "auto", "value": v}


class PlanFout(Exception): pass


def schema_van(velden):
    """{"klant": "string", "regels": "array", "datum": "string?"} -> JSON-schema."""
    props, req = {}, []
    for k, t in (velden or {}).items():
        if isinstance(t, dict):
            props[k] = t; req.append(k); continue
        optional = t.endswith("?"); t = t.rstrip("?")
        if t == "array":
            props[k] = {"type": "array", "items": {"type": "object", "additionalProperties": True}}
        elif t in ("string", "number", "boolean"):
            props[k] = {"type": [t, "null"] if optional else t}
        else:
            raise PlanFout(f"onbekend veldtype '{t}' bij '{k}' (string, number, boolean, array, of met ? erachter)")
        if not optional: req.append(k)
    return {"type": "object", "required": req, "additionalProperties": False, "properties": props}


def form_ui(velden):
    ui = {"ui:order": list(velden), "ui:groups": [{"key": "invoer", "label": "Invoer"}]}
    for k in velden: ui[k] = {"ui:group": "invoer", "ui:widget": "textarea", "ui:label": k}
    return ui


class Bouwer:
    def __init__(self, plan):
        self.plan = plan
        self.nodes, self.edges, self.namen, self.meldingen = [], [], {}, []
        self.col = 0

    def node(self, naam, type_, inputs, desc, rij=0, width=320):
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", naam):
            raise PlanFout(f"stapnaam '{naam}' mag alleen letters, cijfers en _ bevatten (refs werken op de naam)")
        if naam in self.namen: raise PlanFout(f"stapnaam '{naam}' komt twee keer voor")
        n = {"id": "n-" + re.sub(r"[^a-z0-9]+", "-", naam.lower()), "nodeId": naam, "type": type_,
             "inputs": inputs, "position": {"x": X0 + XSTEP * self.col, "y": Y + YSTEP * rij},
             "width": width, "description": desc, "descriptionManual": True}
        self.col += 1
        self.nodes.append(n); self.namen[naam] = n
        return n

    def edge(self, a, b, cond=None):
        e = {"source": a["id"], "target": b["id"]}
        if cond: e["condition"] = cond
        self.edges.append(e)

    # ---- trigger ----
    def trigger(self):
        t = self.plan.get("trigger") or {}
        soort = t.get("soort")
        if soort == "mail":
            self.meldingen.append("Mailbox: kies na import de mailbox, de map en de Outlook-connection.")
            return self.node("Mailbox", "integrationV2Trigger", {
                "folder": auto(t.get("map", "Inbox")), "appName": auto("microsoft-outlook"),
                "accountId": lit(KIES), "targetUser": auto(t.get("mailbox", KIES)),
                "componentKey": auto("new-email-received"), "includeAttachmentsEnabled": auto("true"),
                "senderFilterMode": auto("BLACKLIST"), "senderFilterAddresses": auto(t.get("mailbox", KIES)),
                "configuredProps": lit({"selectedApp": {"name": "Microsoft Outlook", "img_src": "/images/integrations/microsoft-outlook.png"}})},
                "KIES NA IMPORT: mailbox, map, connection. Vuurt bij elke nieuwe mail in die map. Gebruik {{Mailbox.data.subject}}, {{Mailbox.data.body}}, {{Mailbox.files}}.")
        if soort == "app":
            velden = t.get("velden") or {"Tekst": "Plak hier je tekst"}
            a = self.node("App", "appTrigger", {"visibility": auto("Private"),
                          "appConfig": lit({"heading": self.plan.get("naam", "Workflow"), "intro": t.get("intro", ""), "showTraces": True})},
                          "Start via de app-knop in Lleverage.")
            f = self.node("Form", "form", {"schema": lit(schema_van({k: "string" for k in velden})), "uiSchema": lit(form_ui(velden))},
                          "Invoerformulier. Velden: " + ", ".join(f"{{{{Form.data.{k}}}}}" for k in velden))
            self.edge(a, f); return f
        if soort == "schedule":
            return self.node("Schedule", "scheduleTrigger", {"cronExpression": lit(t.get("cron", "0 7 * * 1-5")), "timeZone": lit("Europe/Amsterdam")},
                             "Draait op vaste tijden (cron, Europe/Amsterdam).")
        if soort == "api":
            velden = t.get("velden") or {"tekst": "string"}
            return self.node("API_Call", "apiCallTrigger", {"auth": auto("None"), "schema": lit(schema_van({k: "string" for k in velden})),
                             "uiSchema": lit({"ui:order": list(velden)})}, "Start via een HTTP-call. Velden onder {{API_Call.body.<veld>}}.")
        raise PlanFout("trigger.soort moet mail, app, schedule of api zijn")

    # ---- stappen ----
    def stap(self, s, rij):
        naam, soort = s.get("naam"), s.get("soort")
        if not naam: raise PlanFout(f"stap zonder naam: {s}")
        if soort == "llm":
            vid = str(uuid.uuid4())
            inputs = {"_activeVariantId": lit(vid), "_variants": lit({vid: {"id": vid, "title": "Variant 1", "maxSteps": 1, "temperature": 0,
                      "systemMessage": "", **MODEL, "messages": [{"role": "user", "content": [{"type": "text", "text": s["prompt"]}]}]}})}
            if s.get("uitvoer"):
                inputs["_jsonFormat"] = lit(True); inputs["_jsonOutput"] = lit(schema_van(s["uitvoer"]))
                desc = f"LLM. Uitvoer onder {{{{{naam}.output.<veld>}}}}: " + ", ".join(s["uitvoer"])
            else:
                desc = f"LLM. Tekst onder {{{{{naam}.output}}}}"
            return self.node(naam, "llm", inputs, desc, rij)
        if soort == "extract":
            return self.node(naam, "extract", {"variables": lit([s["bron"]]), "schema": lit(schema_van(s["uitvoer"])), **{k: lit(v) for k, v in EXTRACT_MODEL.items()}},
                             f"Extractie uit {s['bron']}. Uitvoer onder {{{{{naam}.output.<veld>}}}}. CONTROLEER NA IMPORT: model.", rij)
        if soort == "js":
            if "{{" in s["script"]: raise PlanFout(f"{naam}: geen {{{{ }}}} in een script; gebruik de node-naam direct, bv. Lees_Mail.output.klant")
            if "\x00" in s["script"]: raise PlanFout(f"{naam}: null-byte in script")
            return self.node(naam, "javascript", {"script": lit(s["script"])}, f"Code. Uitvoer onder {{{{{naam}.result.<veld>}}}}", rij)
        if soort == "branch":
            conds = s["condities"]
            if not isinstance(conds, dict) or not conds: raise PlanFout(f"{naam}: condities moet een dict zijn {{tak: expressie}}")
            n = self.node(naam, "branch", {"conditions": lit(list(conds.values())), "useLanguageMode": lit(False), "languageConditions": lit([""] * len(conds))},
                          "Vertakking. Takken: " + ", ".join(f"{k} (index {i})" for i, k in enumerate(conds)), rij)
            n["_takken"] = {k: i for i, k in enumerate(conds)}
            return n
        if soort == "mens_vraag":
            velden = s.get("velden") or {"Antwoord": "string"}
            sch = schema_van(velden)
            for k, d in (s.get("defaults") or {}).items(): sch["properties"][k]["default"] = d
            return self.node(naam, "requestInput", {"type": lit("INPUT"), "title": lit(s.get("titel", "Even checken")),
                             "subject": auto(s.get("onderwerp", s.get("titel", "Even checken"))), "description": auto(s.get("uitleg", "")),
                             "schema": lit(sch), "uiSchema": lit({"ui:order": list(velden), "ui:groups": [{"key": "keuze", "label": "Jouw antwoord"}],
                                                                  **{k: {"ui:group": "keuze", "ui:label": k} for k in velden}})},
                             f"Mens vult aan; flow wacht. Antwoord onder {{{{{naam}.data.<veld>}}}}", rij)
        if soort == "mens_keur":
            n = self.node(naam, "requestApproval", {"type": lit("APPROVAL"), "title": auto(s.get("titel", "Goedkeuren?")),
                          "description": auto(s.get("uitleg", "")), "priority": lit("MEDIUM"),
                          "buttons": lit([{"label": s.get("goed", "Goedkeuren"), "value": "approve", "variant": "success"},
                                          {"label": s.get("fout", "Afkeuren"), "value": "reject", "variant": "destructive"}])},
                          "Mens keurt goed (index 0) of af (index 1); flow wacht.", rij)
            n["_takken"] = {"goed": 0, "fout": 1}
            return n
        if soort == "mail_sturen":
            self.meldingen.append(f"{naam}: kies na import de Outlook-connection en controleer het afzenderadres.")
            return self.node(naam, "external", {"_baseUrl": lit(OUTLOOK_BASE), "_nodeKey": lit("microsoft-outlook_send-email"), "credentialId": lit(KIES),
                             "targetUser": auto(s.get("van", KIES)), "to": auto(s["aan"]), "subject": auto(s["onderwerp"]), "body": auto(s["tekst"]),
                             "bodyType": lit("HTML" if "<" in s["tekst"] else "Text"), "importance": lit("Normal"), "saveToSentItems": lit(False),
                             "__retryOptions": lit(RETRY)}, "Mail versturen via Outlook. KIES NA IMPORT: connection + afzender.", rij)
        if soort == "mail_beantwoorden":
            if "Mailbox" not in self.namen: raise PlanFout(f"{naam}: mail_beantwoorden kan alleen met trigger.soort = mail")
            self.meldingen.append(f"{naam}: kies na import de Outlook-connection.")
            return self.node(naam, "external", {"_baseUrl": lit(OUTLOOK_BASE), "_nodeKey": lit("microsoft-outlook_reply-to-email"), "credentialId": lit(KIES),
                             "targetUser": auto(self.plan["trigger"].get("mailbox", KIES)), "messageId": auto("{{Mailbox.data.id}}"),
                             "recipients": auto(s.get("aan", "{{Mailbox.data.from}}")), "comment": auto(s["tekst"]),
                             "commentType": lit("HTML" if "<" in s["tekst"] else "Text"), "replyAll": lit(False), "timezone": auto("Europe/Amsterdam"),
                             "__retryOptions": lit(RETRY)}, "Antwoord op de binnengekomen mail. KIES NA IMPORT: connection.", rij)
        if soort == "slack":
            self.meldingen.append(f"{naam}: kies na import de Slack-connection en het kanaal.")
            return self.node(naam, "external", {"_baseUrl": lit(OUTLOOK_BASE), "_nodeKey": lit("slack_send-channel-message"), "credentialId": lit(KIES),
                             "channel": auto(s.get("kanaal", KIES)), "text": auto(s["tekst"])}, "Slack-bericht. KIES NA IMPORT: connection + kanaal.", rij)
        if soort == "http":
            inputs = {"url": auto(s["url"]), "method": lit(s.get("methode", "GET").upper()), "__retryOptions": lit(RETRY)}
            if s.get("body") is not None: inputs["body"] = lit(s["body"]); inputs["contentType"] = lit("application/json")
            if s.get("auth"): inputs["authorization"] = auto(s["auth"])
            return self.node(naam, "httpRequest", inputs, f"HTTP-call. Antwoord onder {{{{{naam}.data}}}}. Secrets via {{{{_env.NAAM}}}}.", rij)
        if soort == "tabel_schrijven":
            self.meldingen.append(f"{naam}: maak na import de tabel '{s['tabel']}' aan en kies hem in de node.")
            return self.node(naam, "dataTablesCreate", {"projectId": lit(KIES), "tableId": lit(KIES), "tableName": lit(s["tabel"]), "data": lit(s["data"])},
                             f"Rij schrijven in Lleverage-tabel '{s['tabel']}'. KIES NA IMPORT: project + tabel.", rij)
        if soort == "tabel_lezen":
            self.meldingen.append(f"{naam}: kies na import de tabel '{s['tabel']}'.")
            return self.node(naam, "dataTablesFind", {"projectId": lit(KIES), "tableId": lit(KIES), "tableName": lit(s["tabel"]), "returnMode": lit(s.get("modus", "all"))},
                             f"Rijen lezen uit '{s['tabel']}'. Uitvoer onder {{{{{naam}.record}}}}. KIES NA IMPORT: tabel + filters.", rij)
        if soort == "output":
            return self.node(naam, "output", {"body": auto(s["tekst"]), "statusCode": lit(200)}, "Eindpunt: dit zie je in de run.", rij)
        raise PlanFout(f"{naam}: onbekende soort '{soort}'. Kies uit llm, extract, js, branch, mens_vraag, mens_keur, mail_sturen, mail_beantwoorden, slack, http, tabel_schrijven, tabel_lezen, output")

    def bouw(self):
        vorige = self.trigger()
        rij = 0
        for s in self.plan.get("stappen") or []:
            n = self.stap(s, rij)
            bron, cond = vorige, None
            if s.get("na"):
                ref = s["na"]
                if "." in ref:
                    bnaam, tak = ref.split(".", 1)
                    b = self.namen.get(bnaam)
                    if not b or "_takken" not in b: raise PlanFout(f"{s['naam']}: 'na' verwijst naar '{bnaam}' maar dat is geen branch of mens_keur")
                    if tak not in b["_takken"]: raise PlanFout(f"{s['naam']}: tak '{tak}' bestaat niet op {bnaam}; takken: {list(b['_takken'])}")
                    bron, cond = b, f"{bnaam}.index === {b['_takken'][tak]}"
                else:
                    bron = self.namen.get(ref)
                    if not bron: raise PlanFout(f"{s['naam']}: 'na' verwijst naar onbekende stap '{ref}'")
                    if "_takken" in bron: raise PlanFout(f"{s['naam']}: '{ref}' is een vertakking, kies een tak: {ref}.<tak>")
            elif "_takken" in vorige:
                raise PlanFout(f"{s['naam']}: komt na vertakking '{vorige['nodeId']}', geef 'na': '{vorige['nodeId']}.<tak>' op")
            self.edge(bron, n, cond); vorige = n
        for n in self.nodes: n.pop("_takken", None)
        return {"version": 15, "layoutMode": "free", "nodes": self.nodes, "edges": self.edges, "subworkflows": {}}


def valideer(wf):
    p = []
    ids = {n["id"] for n in wf["nodes"]}; namen = {n["nodeId"] for n in wf["nodes"]}
    raw = json.dumps(wf, ensure_ascii=False)
    if "\x00" in raw: p.append("null-byte in export")
    for e in wf["edges"]:
        if e["source"] not in ids or e["target"] not in ids: p.append(f"edge naar onbekende node: {e}")
    for ref in sorted(set(re.findall(r"\{\{([A-Za-z_][A-Za-z0-9_]*)\.", raw))):
        if ref not in namen and ref != "_env": p.append(f"{{{{{ref}.…}}}} verwijst naar een stap die niet bestaat")
    for n in wf["nodes"]:
        uit = [e for e in wf["edges"] if e["source"] == n["id"]]
        if n["type"] in ("branch", "requestApproval"):
            if not uit: p.append(f"{n['nodeId']}: vertakking zonder vervolg")
            if any("condition" not in e for e in uit): p.append(f"{n['nodeId']}: uitgang zonder condition")
        elif n["type"] not in ("output", "return") and not uit:
            p.append(f"{n['nodeId']}: doodlopende stap (geen vervolg en geen output)")
        if n["type"] == "javascript":
            for ref in set(re.findall(r"\b([A-Z][A-Za-z0-9_]*)\.(?:output|result|data|record|files)\b", n["inputs"]["script"]["value"])):
                if ref not in namen: p.append(f"{n['nodeId']}: script gebruikt '{ref}' maar die stap bestaat niet")
    if sum(n["type"].endswith("Trigger") for n in wf["nodes"]) != 1: p.append("precies één trigger vereist")
    return p


def main():
    if len(sys.argv) < 2: print(__doc__); sys.exit(2)
    plan = json.load(open(sys.argv[1]))
    try:
        b = Bouwer(plan); wf = b.bouw()
    except PlanFout as e:
        print(f"PLAN-FOUT: {e}", file=sys.stderr); sys.exit(1)
    except KeyError as e:
        print(f"PLAN-FOUT: verplicht veld ontbreekt: {e}", file=sys.stderr); sys.exit(1)
    problemen = valideer(wf)
    for m in b.meldingen: print("NA IMPORT: " + m, file=sys.stderr)
    if problemen:
        for x in problemen: print("FOUT: " + x, file=sys.stderr)
        sys.exit(1)
    print(f"OK: {len(wf['nodes'])} nodes, {len(wf['edges'])} edges", file=sys.stderr)
    if "--check" not in sys.argv: print(json.dumps(wf, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
