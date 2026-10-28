#!/usr/bin/env python3
"""Lint Power Automate flow definitions against the hard rules of the ai-lead-workflow-power-automate skill.

Usage:
    python scripts/lint_flow.py <path> [--json]

<path> may be: an exported solution .zip, an unzipped solution folder,
a Workflows/<Name>-<GUID>.json file, or a bare definition .json
(an object with "triggers"/"actions").

Exit code: 0 = no errors, 1 = errors found, 2 = nothing could be read.
Only the Python 3 standard library is used.
"""
import json
import os
import re
import sys
import zipfile

LOOP_TYPES = {"Foreach", "Until"}
VARIABLE_WRITE_TYPES = {
    "SetVariable", "IncrementVariable", "DecrementVariable",
    "AppendToArrayVariable", "AppendToStringVariable",
}
CALL_TYPES = {"OpenApiConnection", "ApiConnection", "Http", "HttpWebhook", "Workflow"}
AGENT_TRIGGER_KINDS = {"skills", "virtualagent", "copilot"}

# Designer default names (spaces already replaced by underscores in JSON keys).
DEFAULT_NAMES = {
    "Compose", "Condition", "Apply_to_each", "Scope", "HTTP", "Get_items", "Get_item",
    "Create_item", "Update_item", "Delete_item", "Send_an_email_(V2)", "Initialize_variable",
    "Set_variable", "Increment_variable", "Append_to_array_variable", "Append_to_string_variable",
    "Parse_JSON", "Filter_array", "Select", "Do_until", "Switch", "Terminate", "List_rows",
    "Get_a_row_by_ID", "Add_a_new_row", "Update_a_row", "Delay", "Response",
    "Post_message_in_a_chat_or_channel", "Get_file_content", "Create_file", "Run_a_Child_Flow",
    "Respond_to_a_PowerApp_or_flow", "Respond_to_the_agent", "Create_HTML_table",
    "Create_CSV_table", "Join", "Send_an_HTTP_request_to_SharePoint",
    "Start_and_wait_for_an_approval",
}
DEFAULT_NAME_RE = re.compile(r"^(?P<base>.+?)(_\d+)?$")

URL_RE = re.compile(r"https?://[^\s\"'}]+", re.I)
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
GUID_RE = re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b")
# Input keys that legitimately hold connection plumbing, not business values.
PLUMBING_KEYS = {"host", "connectionName", "apiId", "operationId", "connection", "authentication",
                 "schema", "$schema"}


class Linter:
    def __init__(self, flow_name, definition):
        self.flow = flow_name
        self.d = definition
        self.findings = []
        self.responses = []          # (path, output_keys, action)
        self.has_failure_handling = False
        self.has_terminate_failed = False
        self.action_count = 0
        self.default_names = []
        self.hardcoded = {"URL": set(), "email": set(), "GUID": set()}
        self.agent_flow = False

    def add(self, severity, path, message):
        self.findings.append({"flow": self.flow, "severity": severity, "path": path, "message": message})

    # ---------- triggers ----------
    def check_triggers(self):
        for name, trig in (self.d.get("triggers") or {}).items():
            kind = str(trig.get("kind", "")).lower()
            if kind in AGENT_TRIGGER_KINDS:
                self.agent_flow = True
            for cond in trig.get("conditions") or []:
                expr = str(cond.get("expression", "")).strip()
                if expr and not expr.startswith("@"):
                    self.add("error", f"trigger:{name}",
                             f"Trigger condition must start with '@': {expr[:80]}")
            conc = (trig.get("runtimeConfiguration") or {}).get("concurrency")
            if conc:
                self.add("warning", f"trigger:{name}",
                         f"Trigger concurrency is enabled ({conc.get('runs', '?')} runs). "
                         "It cannot be switched off without deleting and re-adding the trigger.")

    # ---------- actions ----------
    @staticmethod
    def children(action):
        """Yield (label, child_actions_dict) for every nested branch."""
        if isinstance(action.get("actions"), dict):
            yield "", action["actions"]
        else_branch = action.get("else") or {}
        if isinstance(else_branch.get("actions"), dict):
            yield "else", else_branch["actions"]
        for case_name, case in (action.get("cases") or {}).items():
            if isinstance(case.get("actions"), dict):
                yield f"case:{case_name}", case["actions"]
        default = action.get("default") or {}
        if isinstance(default.get("actions"), dict):
            yield "default", default["actions"]

    def walk(self, actions, path, depth, loop_stack):
        for name, action in (actions or {}).items():
            self.action_count += 1
            here = f"{path}/{name}" if path else name
            atype = action.get("type", "")
            self.check_action(name, here, action, atype, depth, loop_stack)
            new_stack = loop_stack
            if atype in LOOP_TYPES:
                new_stack = loop_stack + [(name, atype, self.loop_parallelism(action))]
            for label, child in self.children(action):
                child_path = f"{here}[{label}]" if label else here
                self.walk(child, child_path, depth + 1, new_stack)

    @staticmethod
    def loop_parallelism(action):
        conc = (action.get("runtimeConfiguration") or {}).get("concurrency") or {}
        try:
            return int(conc.get("repetitions", 1))
        except (TypeError, ValueError):
            return 1

    def check_action(self, name, here, action, atype, depth, loop_stack):
        inputs = action.get("inputs") or {}

        if atype == "InitializeVariable" and depth > 0:
            self.add("error", here, "Initialize variable is only allowed at the top level of the flow.")

        if atype == "Terminate":
            if any(t in LOOP_TYPES for _, t, _ in loop_stack):
                self.add("error", here, "Terminate cannot be placed inside Apply to each or Do until.")
            if str(inputs.get("runStatus", "")).lower() == "failed":
                self.has_terminate_failed = True

        if atype in VARIABLE_WRITE_TYPES:
            parallel = [n for n, t, p in loop_stack if t == "Foreach" and p > 1]
            if parallel:
                self.add("error", here,
                         f"Variable write inside parallel Apply to each '{parallel[-1]}' is a race condition. "
                         "Use Compose + Select after the loop, or set concurrency to 1.")

        if atype in CALL_TYPES:
            foreach = [(n, p) for n, t, p in loop_stack if t == "Foreach"]
            if foreach:
                loop_name, par = foreach[-1]
                mode = "sequential (default)" if par <= 1 else f"parallel ({par})"
                self.add("warning", here,
                         f"API call per item inside Apply to each '{loop_name}', {mode}. "
                         "Filter at source, batch, or use Select/Filter array where possible.")

        if atype == "Until":
            limit = action.get("limit") or inputs.get("limit")
            if not limit:
                self.add("warning", here, "Do until has no explicit limit (defaults: 60 iterations, PT1H).")

        if atype == "Http":
            method = str(inputs.get("method", "")).upper()
            if method == "POST" and "retryPolicy" not in inputs:
                self.add("warning", here,
                         "HTTP POST uses the default retry policy; a retry after a timeout can create duplicates. "
                         "Consider retryPolicy None for non-idempotent calls.")

        # failure handling
        for prev, statuses in (action.get("runAfter") or {}).items():
            statuses_l = [str(s).lower() for s in statuses]
            if "failed" in statuses_l or "timedout" in statuses_l:
                self.has_failure_handling = True
            if "catch" in name.lower() and atype == "Scope" and "failed" not in statuses_l:
                self.add("error", here,
                         f"Scope '{name}' looks like a Catch but its run-after on '{prev}' lacks 'Failed'.")

        if atype == "Response":
            schema = (inputs.get("schema") or {}).get("properties")
            body = inputs.get("body")
            keys = set(schema.keys()) if isinstance(schema, dict) else (
                set(body.keys()) if isinstance(body, dict) else set())
            self.responses.append((here, keys, action))

        # naming hygiene
        m = DEFAULT_NAME_RE.match(name)
        if m and (name in DEFAULT_NAMES or m.group("base") in DEFAULT_NAMES):
            self.default_names.append(name)
        if ":" in name:
            self.add("warning", here, "Action name contains ':' - the new designer rejects it; use ' - '.")

        self.scan_hardcoded(inputs)

    def scan_hardcoded(self, value, key=None):
        if key in PLUMBING_KEYS:
            return
        if isinstance(value, dict):
            for k, v in value.items():
                self.scan_hardcoded(v, k)
        elif isinstance(value, list):
            for v in value:
                self.scan_hardcoded(v, key)
        elif isinstance(value, str):
            if "parameters(" in value:      # environment variable reference
                return
            for u in URL_RE.findall(value):
                if "schema.management.azure.com" not in u and "json-schema.org" not in u:
                    self.hardcoded["URL"].add(u)
            for e in EMAIL_RE.findall(value):
                self.hardcoded["email"].add(e)
            for g in GUID_RE.findall(value):
                self.hardcoded["GUID"].add(g)

    # ---------- flow-level ----------
    def finish(self):
        if self.default_names:
            names = ", ".join(sorted(self.default_names)[:15])
            more = "" if len(self.default_names) <= 15 else f" (+{len(self.default_names) - 15} more)"
            self.add("warning", "(flow)", f"Actions still have default names: {names}{more}")

        if not self.has_failure_handling and self.action_count > 5:
            self.add("warning", "(flow)",
                     "No run-after on Failed/TimedOut anywhere - add Try/Catch/Finally Scopes.")
        if self.has_failure_handling and not self.has_terminate_failed:
            self.add("warning", "(flow)",
                     "Failures are caught but no Terminate with status Failed exists - "
                     "the run will report Succeeded after an error.")

        for kind, values in self.hardcoded.items():
            if values:
                sample = ", ".join(sorted(values)[:5])
                more = "" if len(values) <= 5 else f" (+{len(values) - 5} more)"
                self.add("warning", "(flow)",
                         f"Hardcoded {kind}(s): {sample}{more} - use environment variables if they differ per environment.")

        if self.responses:
            key_sets = {frozenset(k) for _, k, _ in self.responses if k}
            if len(key_sets) > 1:
                sev = "error" if self.agent_flow else "warning"
                detail = "; ".join(f"{p}: {sorted(k)}" for p, k, _ in self.responses)
                self.add(sev, "(flow)", f"Response actions return different outputs: {detail}")
            if self.agent_flow:
                for p, _, act in self.responses:
                    if "asynchronous" in str(act.get("operationOptions", "")).lower():
                        self.add("error", p, "Agent flow response is asynchronous - set Asynchronous response Off.")
        elif self.agent_flow:
            self.add("error", "(flow)", "Agent-triggered flow has no Respond to the agent action.")

    def run(self):
        self.check_triggers()
        self.walk(self.d.get("actions"), "", 0, [])
        self.finish()
        return self.findings


# ---------- loading ----------
def extract_definition(obj):
    if not isinstance(obj, dict):
        return None
    props = obj.get("properties")
    if isinstance(props, dict) and isinstance(props.get("definition"), dict):
        return props["definition"]
    if isinstance(obj.get("definition"), dict):
        return obj["definition"]
    if "actions" in obj or "triggers" in obj:
        return obj
    return None


def load_flows(path):
    """Return list of (name, definition)."""
    flows = []

    def add_json(name, text):
        try:
            obj = json.loads(text)
        except json.JSONDecodeError as exc:
            print(f"Skipping {name}: invalid JSON ({exc})", file=sys.stderr)
            return
        definition = extract_definition(obj)
        if definition is None:
            print(f"Skipping {name}: no flow definition found", file=sys.stderr)
            return
        flows.append((name, definition))

    if os.path.isfile(path) and path.lower().endswith(".zip"):
        with zipfile.ZipFile(path) as zf:
            for member in zf.namelist():
                if member.lower().startswith("workflows/") and member.lower().endswith(".json"):
                    add_json(os.path.basename(member), zf.read(member).decode("utf-8-sig"))
    elif os.path.isdir(path):
        wf = os.path.join(path, "Workflows")
        folder = wf if os.path.isdir(wf) else path
        for fname in sorted(os.listdir(folder)):
            if fname.lower().endswith(".json"):
                with open(os.path.join(folder, fname), encoding="utf-8-sig") as fh:
                    add_json(fname, fh.read())
    elif os.path.isfile(path):
        with open(path, encoding="utf-8-sig") as fh:
            add_json(os.path.basename(path), fh.read())
    else:
        print(f"Path not found: {path}", file=sys.stderr)
    return flows


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    as_json = "--json" in argv
    if len(args) != 1:
        print(__doc__)
        return 2
    flows = load_flows(args[0])
    if not flows:
        print("No flow definitions found.", file=sys.stderr)
        return 2

    findings = []
    for name, definition in flows:
        findings.extend(Linter(name, definition).run())

    errors = [f for f in findings if f["severity"] == "error"]
    if as_json:
        print(json.dumps({"flows": [n for n, _ in flows], "findings": findings}, indent=2))
    else:
        for name, _ in flows:
            own = [f for f in findings if f["flow"] == name]
            print(f"== {name}: {sum(f['severity'] == 'error' for f in own)} error(s), "
                  f"{sum(f['severity'] == 'warning' for f in own)} warning(s)")
            for f in sorted(own, key=lambda x: x["severity"]):
                print(f"  [{f['severity'].upper()}] {f['path']}: {f['message']}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
