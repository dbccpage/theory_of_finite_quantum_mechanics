"""Render the evidence map as Markdown.

AuthorityEffect: None. Every function here is a pure function of the evidence-map
document (dag/evidence/build_evidence.py, build_map) and the DAG node statements.
Nothing here opens a file, hashes a file or reads a receipt: if a page needs a fact,
the document must carry it.
"""
from __future__ import annotations

import collections
import re
import sys
from pathlib import Path

_DAG_DIR = str(Path(__file__).resolve().parents[1])
if _DAG_DIR not in sys.path:  # python -I does not put the script directory on sys.path
    sys.path.insert(0, _DAG_DIR)
from validate_derivation_dag import symbol_leaf  # noqa: E402

DOCS_REL = "docs/evidence"
KIND_GROUP = {"lean_decl": 0, "rust_symbol": 1, "rust_test": 1, "python_symbol": 2, "python_test": 2,
              "paper": 3, "external": 4}
GROUP_TITLE = {0: "Lean", 1: "Rust", 2: "Python", 3: "Documents and data", 4: "External sources"}
MISMATCH_TEXT = {
    "receipt_names_uncited_module": "A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence)",
    "proved_lean_below_e3": "PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt",
    "proved_lean_external_only": "PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout",
    "receipt_not_current": "A replay receipt exists for a cited Lean file, but its sha256 no longer matches the file, it records a failure, or it records no passed axiom audit",
    "computational_no_runnable_test": "COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited",
    "proved_prose_no_in_repo_document": "PROVED_PROSE with no in-repo source document cited",
    "broken_reference": "A cited in-repo path or symbol cannot be found in this checkout",
}
STATUS_ORDER = (
    "PROVED_LEAN",
    "PROVED_PROSE",
    "COMPUTATIONALLY_CHECKED",
    "CONDITIONAL",
    "DEFINITION",
    "IMPORTED_ASSUMPTION",
    "ADMITTED_PRIMITIVE",
    "SOURCE_RECORD",
    "OPEN",
    "REFUTED",
)
STATUS_GROUPS = (
    ("Proved in this repository, kernel-checked Lean", ("PROVED_LEAN",)),
    ("Proved in prose", ("PROVED_PROSE",)),
    ("Checked by computation", ("COMPUTATIONALLY_CHECKED",)),
    ("Conditional on named hypotheses", ("CONDITIONAL",)),
    ("Definitions", ("DEFINITION",)),
    ("Imported or admitted, not derived here", ("IMPORTED_ASSUMPTION", "ADMITTED_PRIMITIVE")),
    ("External results recorded, not audited here", ("SOURCE_RECORD",)),
    ("Open", ("OPEN",)),
    ("Refuted", ("REFUTED",)),
)


def md_escape(text: str) -> str:
    """Stop statement text from being read as links, HTML or code."""
    for char in ("\\", "[", "]", "<", ">", "`"):
        text = text.replace(char, "\\" + char)
    return text


def cell(text: object, limit: int | None = None) -> str:
    out = " ".join(str(text).split())
    if limit and len(out) > limit:
        out = out[: limit - 3].rstrip() + "..."
    return md_escape(out).replace("|", "\\|")


def link(depth: int, path: str, text: str | None = None) -> str:
    return f"[{text or path}]({'../' * depth}{path})"


def file_ref(depth: int, item: dict) -> str:
    label = item["path"] + (f"::{item['symbol']}" if item["symbol"] else "")
    if item["resolution"] == "present":
        return f"[`{label}`]({'../' * depth}{item['path']})"
    return f"`{label}`"


def short_sha(sha: str | None) -> str:
    return sha[:12] if sha else "-"


def yes_no(value: object) -> str:
    return "-" if value is None else ("yes" if value else "no")


def replay_of(members: list[dict]) -> str:
    return members[0]["replay"]


def counts_line(counter: dict, order: tuple) -> str:
    return ", ".join(f"{k} {counter[k]}" for k in order if counter.get(k))


def node_page(row: dict, node: dict, document: dict, rows_by_id: dict) -> str:
    routes_in, routes_out = row["routes"]["in"], row["routes"]["out"]
    receipts = {r["id"]: r for r in document["receipts"]}
    files = document["files"]
    out = [f"# {row['id']}", "",
           f"Stage: {link(1, 'stages/' + row['stage'] + '.md', row['stage'])}. "
           f"Status: `{row['status']}`. Evidence grade: **{row['grade']}**. "
           f"[Evidence map overview](../README.md). AuthorityEffect: None.", "",
           "## Statement", ""]
    out += [f"> {md_escape(line)}" if line.strip() else ">" for line in node["statement"].splitlines()] or [">"]
    out += ["", "## Grade", "",
            f"Evidence grade **{row['grade']}** (rules in the [overview](../README.md#evidence-grades)). "
            "The grade rates the evidence this checkout holds; it is separate from the status.", "",
            f"- counted in-repo evidence files: {row['facts']['counted_files']}",
            f"- cited Lean, Rust or Python symbols found in their in-repo files: {row['facts']['symbols_found']}",
            f"- distinct cited Lean declarations covered by a current replay receipt: {row['facts']['lean_receipt_backed']}",
            f"- counted in-repo runnable tests: {row['facts']['runnable_tests']}",
            f"- counted in-repo Rust or Python files that are not tests: {row['facts']['cited_code_files_not_tests']}",
            f"- recorded statement-match reviews that qualify: {row['facts']['qualifying_reviews']}",
            f"- next step to raise the grade: {row['next_step']}", ""]
    out += ["## Flags", ""]
    if row["flags"]:
        out += [f"- `{f['kind']}`: {f['detail']}. {MISMATCH_TEXT[f['kind']]}." for f in row["flags"]]
    else:
        out.append("None. Status and evidence are consistent under the rules in the overview.")
    out += ["", "## Imported structure", ""]
    out += [f"- {md_escape(x)}" for x in node["imported_structure"]] or ["None recorded."]
    out += ["", "## Bottleneck", "", md_escape(node["bottleneck"]), ""]
    if node.get("source_status"):
        out += ["## Source status", "", md_escape(node["source_status"]), ""]
    out += ["## Review", ""]
    if row["reviews"]:
        for review in row["reviews"]:
            if review["source"] == "pfp_review":
                out += [f"- PFP review: {link(3, review['review'], review['review'])}; file present and sha256 matches the node's "
                        f"record: {'yes' if review['review_file_ok'] else 'no'}; verdict `{review['verdict']}`; "
                        f"scope effect `{review['scope_effect']}`; prior status `{review['prior_status']}`; "
                        f"qualifies for E4: {'yes' if review['qualifies'] else 'no'}.",
                        f"  - narrowest claim: {cell(review['narrowest_claim'])}",
                        f"  - does not support: {cell(review['does_not_support'])}",
                        f"  - next test: {cell(review['next_test'])}"]
            else:
                out += [f"- Frontier Lean review: {link(3, review['review'], review['review'])}; verdict `{review['verdict']}`; "
                        f"qualifies for E4: {'yes' if review['qualifies'] else 'no'}.",
                        f"  - theorems that discharge the node, as listed by the review: {review['theorems']}",
                        "  - the review's reason for its verdict is in the row of this node in the review file"]
    else:
        out.append("No recorded statement-match review.")
    out += ["", "## Evidence items", ""]
    if not row["items"]:
        out.append("None cited.")
    else:
        out += ["Items are grouped by file. \"Counts\" means the item counts toward the grade: the file is in this "
                "checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. "
                "To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a "
                "scratch file that imports it.", ""]
    groups: dict[tuple, list[dict]] = collections.OrderedDict()
    for item in row["items"]:
        groups.setdefault((KIND_GROUP[item["kind"]], item["path"]), []).append(item)
    for (group, path), members in groups.items():
        first = members[0]
        if group == 4:
            continue
        out += [f"### {GROUP_TITLE[group]}: `{path}`", ""]
        if first["resolution"] == "present":
            out.append(f"- file: {link(3, path, path)}")
            if path in files:
                f = files[path]
                out.append(f"- sha256 (`{f['sha256_basis']}`): `{f['sha256']}`")
        else:
            out.append(f"- file: `{path}`")
            out.append(f"- resolution: `{first['resolution']}`"
                       + (" (a path outside this repository; neither confirmed nor refuted here)"
                          if first["resolution"] == "external_unresolved" else " (not found in this checkout)"))
        if first["generated"]:
            out.append("- generated view: listed, not counted")
        cited = sorted({c for m in members for c in m["cited_in"]})
        out.append(f"- cited in: {', '.join(cited)}")
        if group == 0 and first["resolution"] == "present":
            out.append(f"- replay: `{replay_of(members)}`")
            rids = sorted({rr["id"] for m in members for rr in m["receipts"]})
            for rid in rids:
                rec = receipts[rid]
                rr = next(r for m in members for r in m["receipts"] if r["id"] == rid)
                state = "matches the current file" if rr["sha_match"] else "differs from the current file"
                out.append(f"  - receipt {link(3, rec['receipt_file'], rec['receipt_file'])} (module `{rec['module']}`): "
                           f"recorded sha256 `{rec['recorded_sha256']}` {state}; exit code {rec['exit_code']}; "
                           f"Lean {rec['toolchain']}; Mathlib `{short_sha(rec['mathlib_source_sha'])}`; "
                           f"axiom audit passed: {yes_no(rec['axiom_audit_passed'])}; "
                           f"axioms recorded: {', '.join(rec['axioms_union']) or 'none'}"
                           + ("" if rec["axioms_itemised"] else " (not itemised)")
                           + f"; only standard axioms: {yes_no(rec['axioms_standard'])}")
        commands = []
        for m in members:
            if m["command"] and m["command"] not in commands:
                commands.append(m["command"])
        if len(commands) == 1 or (group == 0 and commands):
            out.append(f"- check: `{commands[0]}`")
        symbols = [m for m in members if m["symbol"]]
        if first["resolution"] == "present" and symbols:
            out += ["", "| Symbol | Counts | Found | Declaration form | Audited axioms | Check |",
                    "|---|---|---|---|---|---|"]
            for m in symbols:
                audited = ("none" if m["decl_axioms"] == [] else ", ".join(m["decl_axioms"])) \
                    if m["decl_axioms"] is not None else ("module-level" if m["replay"] == "verified" else "-")
                if m["decl_ambiguous"]:
                    audited = "ambiguous: several receipt names end in this symbol; module-level only"
                check = m["command"] if group != 0 else f"#print axioms {m['symbol']}"
                kind = "" if group == 0 else f" ({m['kind']})"
                out.append(f"| `{cell(m['symbol'])}`{kind} | {yes_no(m['counts'])} | {yes_no(m['symbol_exists'])} | "
                           f"{yes_no(m['symbol_declared'])} | {cell(audited)} | {('`' + cell(check) + '`') if check not in ('-', None) else '-'} |")
            out.append("")
        elif first["resolution"] == "present" and group in (1, 2) and first["command_note"]:
            out.append(f"- note: {first['command_note']}")
        out.append(f"- counts toward the grade: {yes_no(any(m['counts'] for m in members))}")
        out.append("")
    external = [m for (g, _), ms in groups.items() if g == 4 for m in ms]
    if external:
        out += [f"### {GROUP_TITLE[4]}", "",
                "Named by the node; not in this repository and not checked here.", ""]
        out += [f"- `{m['path']}" + (f"::{m['symbol']}" if m["symbol"] else "") + "`" for m in external]
        out.append("")
    if row["absent_notes"]:
        out += ["## Absences recorded by the TFQ records", ""] + [f"- {n}" for n in row["absent_notes"]] + [""]
    out += ["## Routes", ""]
    cap = 60
    out += [f"Incoming ({len(routes_in)}):", ""]
    out += route_lines(routes_in, rows_by_id)[:cap]
    if len(routes_in) > cap:
        out.append(f"- ... and {len(routes_in) - cap} more in `dag/derivation_dag.json`")
    out += ["", f"Outgoing ({len(routes_out)}):", ""]
    out += route_lines(routes_out, rows_by_id)[:cap]
    if len(routes_out) > cap:
        out.append(f"- ... and {len(routes_out) - cap} more in `dag/derivation_dag.json`")
    if not routes_in:
        out += ["", "No incoming route."]
    out.append("")
    return "\n".join(out)


def route_lines(routes: list[dict], rows_by_id: dict) -> list[str]:
    lines = []
    for route in routes:
        ends = route["nodes"]
        shown = ", ".join(f"[{e}]({e}.md) ({rows_by_id[e]['status'] if e in rows_by_id else '?'})" for e in ends)
        lines.append(f"- `{route['id']}` `{route['status']}`: {shown}")
    return lines


def evidence_cell(items: list[dict], depth: int) -> str:
    by_file: dict[str, list[str]] = collections.OrderedDict()
    for item in items:
        if not item["counts"]:
            continue
        by_file.setdefault(item["path"], [])
        if item["symbol"]:
            by_file[item["path"]].append(item["symbol"])
    parts = []
    for path, symbols in list(by_file.items())[:4]:
        shown = [symbol_leaf(s) for s in symbols[:3]]
        more = f" +{len(symbols) - 3}" if len(symbols) > 3 else ""
        parts.append(f"[{cell(path.rsplit('/', 1)[-1])}]({'../' * depth}{path})"
                     + (f": {', '.join('`' + s + '`' for s in shown)}{more}" if shown else ""))
    rest = len(by_file) - 4
    if rest > 0:
        parts.append(f"+{rest} more file(s)")
    return "<br>".join(parts) if parts else "none in this checkout"


def stage_page(stage: str, rows: list[dict], nodes: dict, grades: list[str]) -> str:
    statuses = collections.Counter(r["status"] for r in rows)
    out = [f"# Stage {stage}", "",
           "Part of the [evidence map](../README.md). AuthorityEffect: None.", "",
           f"Nodes: {len(rows)}. Grades: {counts_line(collections.Counter(r["grade"] for r in rows), tuple(grades))}. Statuses: {counts_line(statuses, STATUS_ORDER)}.", "",
           "| Node | Status | Grade | Statement | Counted in-repo evidence | Flags |",
           "|---|---|---|---|---|---|"]
    for row in rows:
        flags = ", ".join(sorted({f["kind"] for f in row["flags"]})) or "-"
        out.append(f"| [{row['id']}](../nodes/{row['id']}.md) | `{row['status']}` | {row['grade']} | "
                   f"{cell(nodes[row['id']]['statement'], 140)} | {evidence_cell(row['items'], 3)} | {cell(flags)} |")
    out.append("")
    return "\n".join(out)


def readme_page(document: dict, rows: list[dict]) -> str:
    GRADES = tuple(document["grades"])
    MISMATCH_ORDER = tuple(document["mismatch_kinds"])
    stage_order = document["stages"]
    toolchain, mathlib = document["lean"]["toolchain"], document["lean"]["mathlib_rev"]
    s = document["summary"]
    n = s["nodes"]
    g = s["by_grade"]
    lean_decl = s["lean_declarations_in_repo"]
    pl = s["status_by_grade"]["PROVED_LEAN"]
    pl_total = sum(pl.values())
    pl_e3 = pl["E3"] + pl["E4"]
    pl_refs = s["proved_lean_lean_references"]
    platforms = ", ".join(sorted({m.group(1) for r in document["receipts"]
                                  for m in [re.search(r",\s*([\w.]+-[\w.-]+),", r["lean_version"] or "")] if m})) or "an unrecorded platform"
    out = ["# Evidence map of the derivation DAG", "",
           "AuthorityEffect: None. This directory is generated by "
           "[`dag/evidence/build_evidence.py`](../../dag/evidence/build_evidence.py) from "
           "[`dag/derivation_dag.json`](../../dag/derivation_dag.json) and the files in this checkout. "
           "It changes no status and adds no result. Its job is to show, node by node, which files back each "
           "claim, how strong that backing is, and where a status says more than the backing supports.", "",
           "The machine-readable form is [`dag/evidence/evidence_map.json`](../../dag/evidence/evidence_map.json). "
           "Each node has a page under [`nodes/`](nodes) and each stage a table under [`stages/`](stages). "
           f"Everything below is recomputed by `python -I -X utf8 dag/evidence/build_evidence.py --check`.", "",
           "## Progress at a glance", "",
           f"The DAG has {n} nodes in {len(stage_order)} stages. Evidence grades: {counts_line(g, GRADES)}.", "",
           "### What is proved here, what is imported, what is open", "",
           "| Group | Statuses | Nodes | Meaning |", "|---|---|---|---|"]
    meaning = {
        "PROVED_LEAN": "Lean declarations are cited as stating the node. Whether they lie in this repository and have a current replay receipt is in the grade table.",
        "PROVED_PROSE": "A written proof exists; no machine check is claimed.",
        "COMPUTATIONALLY_CHECKED": "An exact finite computation is recorded.",
        "CONDITIONAL": "Holds given hypotheses that the node names; the hypotheses are not derived.",
        "DEFINITION": "A definition or construction, not a claim of truth.",
        "IMPORTED_ASSUMPTION": "Taken in from outside the finite construction.",
        "ADMITTED_PRIMITIVE": "Admitted as a starting object.",
        "SOURCE_RECORD": "An external result is recorded; nothing here audits it.",
        "OPEN": "No derivation is recorded.",
        "REFUTED": "A counterexample is recorded.",
    }
    for title, statuses in STATUS_GROUPS:
        total = sum(s["by_status"].get(x, 0) for x in statuses)
        out.append(f"| {title} | {', '.join('`' + x + '`' for x in statuses)} | {total} | "
                   f"{' '.join(meaning[x] for x in statuses)} |")
    out += ["", f"Of the {pl_total} `PROVED_LEAN` nodes, {pl_e3} reach grade E3 or E4 "
            f"({pl_e3 * 100 // max(pl_total, 1)} percent); {pl_total - pl_e3} do not. The second group is listed in "
            "[mismatches](mismatches.md).", "",
            f"Grade E4 needs an in-repo runnable test and a recorded review as well as a replayed Lean declaration. "
            f"{g['E4']} nodes meet all three. Among the {g['E3']} nodes at E3, {s['e3_nodes_with_review']} have a qualifying "
            f"review, {s['e3_nodes_with_review_and_cited_code_but_no_test']} of those cite in-repo Rust or Python code that is "
            f"not a test, and {s['e3_nodes_with_test_but_no_review']} have a runnable test but no review.", "",
            "### Where the Lean evidence stands", "",
            f"The `lean` fields of nodes cite {lean_decl['distinct']} distinct Lean declarations that lie in files of this checkout. "
            f"{lean_decl['replay_verified']} of them are in a file whose current sha256 matches a passing replay receipt; "
            f"{lean_decl['no_receipt']} are in files with no receipt in `dag/research/`; "
            f"{lean_decl['replay_stale']} are in files whose receipt no longer matches; "
            f"{lean_decl['replay_failed']} are in files whose current-hash receipt failed the build or axiom audit. "
            f"The `PROVED_LEAN` nodes cite {sum(pl_refs.values())} Lean references; "
            f"{pl_refs.get('external_unresolved', 0) + pl_refs.get('missing', 0)} "
            f"({(pl_refs.get('external_unresolved', 0) + pl_refs.get('missing', 0)) * 100 // max(sum(pl_refs.values()), 1)} percent) "
            "lie in sibling-atlas paths or do not exist in this checkout. "
            f"{s['proved_lean_nodes'].get('outside_lean_only', 0)} `PROVED_LEAN` nodes cite no Lean "
            "file that this checkout holds.", "",
            "### Status by evidence grade", "",
            "| Status | " + " | ".join(GRADES) + " | Total |", "|---|" + "---|" * (len(GRADES) + 1)]
    for status in STATUS_ORDER:
        row = s["status_by_grade"][status]
        out.append(f"| `{status}` | " + " | ".join(str(row[x]) for x in GRADES) + f" | {sum(row.values())} |")
    out.append("| Total | " + " | ".join(str(g[x]) for x in GRADES) + f" | {n} |")
    out += ["", "### Stage by evidence grade", "",
            "| Stage | " + " | ".join(GRADES) + " | Total | `PROVED_LEAN` | Flags |",
            "|---|" + "---|" * (len(GRADES) + 3)]
    stage_rows = collections.defaultdict(list)
    for row in rows:
        stage_rows[row["stage"]].append(row)
    for stage in stage_order:
        if stage not in stage_rows:
            continue
        sg = s["stage_by_grade"][stage]
        sr = stage_rows[stage]
        out.append(f"| [{stage}](stages/{stage}.md) | " + " | ".join(str(sg[x]) for x in GRADES)
                   + f" | {len(sr)} | {sum(1 for r in sr if r['status'] == 'PROVED_LEAN')} | "
                   f"{sum(len(r['flags']) for r in sr)} |")
    out += ["", "## Evidence grades", "",
            "The grade is computed from the files in this checkout. It rates the evidence, not the truth of the claim. "
            "A node reaches a grade only if it meets every lower condition.", ""]
    out += [f"- **{k}**: {v}." for k, v in document["grade_rules"].items()]
    out += ["", "Counting rules:", "",
            "- Evidence is counted when the node cites it, or when a TFQ record cites it and names only this node. "
            "Evidence a record shares with other nodes is listed on the node page and not counted.",
            "- A replay receipt that names a node (`dag_node`) contributes its Lean module and its anchor declarations as evidence "
            "for that node. When the node's own fields do not cite that module, the node is flagged `receipt_names_uncited_module`.",
            "- Grades are independent of status. A node whose status is `OPEN`, `CONDITIONAL` or `DEFINITION` can reach E3 because "
            "a Lean module attached to it compiles; the grade then says only that the attached module was replayed, not that it "
            "establishes the statement. The node page and the review record say what the module supports.",
            "- Derivation papers written by the syncs, and the generated JSONL and Markdown views, are listed and not counted: "
            "they restate the DAG and do not bear on a claim.",
            "- A symbol \"exists\" under the validator's leaf rule: the last name component occurs in the cited file. "
            "Counted symbols whose leaf occurs but for which no declaration form (`theorem`, `def`, `fn`, `struct`, ...) matched: "
            f"{s['cited_symbols_found_but_no_declaration_form']}. E3 additionally requires a declaration form or a listing in the receipt.",
            "- Paths that begin with `omega_engine` or `.claude` name sibling trees that are not in this repository. "
            "They are recorded as `external_unresolved`: neither confirmed nor refuted here.",
            "- Lean receipts are the files in `dag/research/` whose Lean results carry a module name and a sha256. "
            "A receipt covers a Lean file, not a single declaration, unless the receipt itemises the declaration's axioms. "
            f"{lean_decl['replay_verified_and_declaration_itemised']} of the {lean_decl['replay_verified']} receipt-backed "
            "declarations are itemised; the others rest on the module-level audit. A cited symbol is matched to a receipt name "
            "only if the receipt name equals it or ends in a dot followed by it; when more than one receipt name matches, "
            "the match is recorded as ambiguous and no axiom list is copied "
            f"({lean_decl['replay_verified_with_ambiguous_receipt_name']} declarations).",
            "- File sha256 values are over the file bytes for `.lean`, `.rs`, `.py` and `.toml` files (their line endings are "
            "pinned in `.gitattributes`) and over the LF-normalised text for other files.",
            "", "## Verify it yourself", "",
            "### (a) Static check, a few seconds, no Lean or Rust needed", "",
            "From the repository root, with Python 3.11 or later:", "",
            "```", "python -I -X utf8 dag/evidence/build_evidence.py --check",
            "python -I -X utf8 dag/validate_derivation_dag.py --no-files", "```", "",
            "The first command regenerates the map in memory and fails if any file under `docs/evidence/` or "
            "`dag/evidence/evidence_map.json` differs. The second checks the DAG schema, vocabulary, acyclicity and "
            "forbidden words and ends with `failures=0`. Neither runs Lean, Rust or any test. "
            "`python -m pytest dag/evidence/test_evidence.py` checks the grading rules on chosen nodes.", "",
            "### (b) Check one node", "",
            "Open a node page, for example [ADS-FIVE-QUBIT-PERFECT-TENSOR-TARGET](nodes/ADS-FIVE-QUBIT-PERFECT-TENSOR-TARGET.md). "
            "Each evidence item gives the file, its sha256 and the command to check it. To compare a hash:", "",
            "```", "python -c \"import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())\" "
            "lean4/FrontierFiveQubitPerfectTensor.lean", "```", "",
            "The result should equal the recorded sha256 in "
            "[`dag/research/frontier_targets_lean_replay.json`](../../dag/research/frontier_targets_lean_replay.json).", "",
            "### (c) Replay the Lean receipts", "",
            f"The receipts record builds with Lean {toolchain.split(':v')[-1]} and Mathlib at `{mathlib}`, "
            f"on {platforms}. Another platform with the same toolchain should reproduce the exit codes and the axiom lines; "
            "the receipts do not claim that it was tried.", "",
            "```",
            "git clone https://github.com/dbccpage/theory_of_finite_quantum_mechanics.git",
            "cd theory_of_finite_quantum_mechanics/lean4",
            "cat lean-toolchain            # " + toolchain,
            "lake exe cache get            # fetch the Mathlib cache for the pinned revision",
            "lake build FrontierFiveQubitPerfectTensor",
            "```", "",
            "Then list the axioms of a cited declaration. Save as `Check.lean` inside `lean4/`:", "",
            "```", "import FrontierFiveQubitPerfectTensor",
            "#print axioms FrontierFiveQubitPerfectTensor.choi_generators_commute_and_group_order_64", "```", "",
            "and run `lake env lean Check.lean`. The expected output lists only `propext`, `Classical.choice` and `Quot.sound`, or no axioms. "
            "Anything else, or a build error, contradicts the receipt. Receipts for the other modules are in "
            "[`pfp_batch01_lean_replay.json`](../../dag/research/pfp_batch01_lean_replay.json) and the `tensor_*_validation.json` files "
            "in [`dag/research/`](../../dag/research). The receipts record 25 to 225 seconds per module on one machine; "
            "replaying all of them takes hours.", "",
            "## Where status and evidence disagree", "",
            f"{s['mismatches_total']} flags on {s['mismatch_nodes']} nodes. They are reported here and the DAG statuses are not changed. "
            "The full list, with one line per flag, is in [mismatches](mismatches.md).", "",
            "| Flag | Count | Meaning |", "|---|---|---|"]
    for kind in MISMATCH_ORDER:
        out.append(f"| `{kind}` | {s['mismatches_by_kind'][kind]} | {MISMATCH_TEXT[kind]} |")
    out += ["", "The ten flags on `PROVED_LEAN` nodes with the most downstream nodes:", "",
            "| Node | Stage | Grade | Downstream nodes | Flag |", "|---|---|---|---|---|"]
    top = [m for m in document["mismatches"] if m["kind"] == "proved_lean_below_e3"][:10]
    for m in top:
        out.append(f"| [{m['node']}](nodes/{m['node']}.md) | {m['stage']} | {m['grade']} | {m['dependents']} | {cell(m['detail'], 160)} |")
    out += ["", "## What this map does not do", "",
            "- It does not check that a Lean statement says what the node says. Only a recorded review does that, and the grade E4 asks for one.",
            "- It does not rebuild Lean, run Rust or Python tests, or fetch anything. A receipt is a recorded result, checked here only "
            "for a matching file hash.",
            "- It does not resolve the sibling atlas trees. Their references stay `external_unresolved`.",
            "- It indexes the receipts in `dag/research/*.json` that carry per-module sha256 values. "
            "Other receipts are not indexed: " + "; ".join(
                f"`{x['file']}` ({x['reason']})" for x in document["receipts_not_indexed"]) +
            (". " if document["receipts_not_indexed"] else "") +
            "The `*.axioms.txt` files, the per-run Lean receipts under `dag/results/`, and the Rust and Python test outcomes "
            "are not used for grading in this version.",
            "- A grade is a floor for the evidence found by following the node's own citations. A node with a low grade may "
            "have better evidence that it does not cite.", ""]
    return "\n".join(out)


def mismatch_page(document: dict) -> str:
    MISMATCH_ORDER = tuple(document["mismatch_kinds"])
    out = ["# Status and evidence mismatches", "",
           "Part of the [evidence map](README.md). AuthorityEffect: None. Generated; every flag the grading rules raise is listed. "
           "A flag is a report, not a change: no node status was altered.", "",
           "| Flag | Count |", "|---|---|"]
    for kind in MISMATCH_ORDER:
        out.append(f"| `{kind}`: {MISMATCH_TEXT[kind]} | {document['summary']['mismatches_by_kind'][kind]} |")
    out.append("")
    for kind in MISMATCH_ORDER:
        rows = [m for m in document["mismatches"] if m["kind"] == kind]
        out += [f"## `{kind}` ({len(rows)})", "", MISMATCH_TEXT[kind] + ". Ordered by downstream nodes, most first.", ""]
        if not rows:
            out += ["None.", ""]
            continue
        out += ["| Node | Stage | Status | Grade | Downstream | Detail |", "|---|---|---|---|---|---|"]
        for m in rows:
            out.append(f"| [{m['node']}](nodes/{m['node']}.md) | {m['stage']} | `{m['status']}` | {m['grade']} | "
                       f"{m['dependents']} | {cell(m['detail'], 200)} |")
        out.append("")
    return "\n".join(out)




def render_pages(document: dict, nodes: dict[str, dict]) -> dict[str, str]:
    """Every generated Markdown page, keyed by repository-relative path."""
    rows = document["nodes"]
    rows_by_id = {r["id"]: r for r in rows}
    outputs = {
        f"{DOCS_REL}/README.md": readme_page(document, rows) + "\n",
        f"{DOCS_REL}/mismatches.md": mismatch_page(document) + "\n",
    }
    by_stage: dict[str, list[dict]] = collections.defaultdict(list)
    for row in rows:
        by_stage[row["stage"]].append(row)
    for stage, stage_rows in by_stage.items():
        outputs[f"{DOCS_REL}/stages/{stage}.md"] = stage_page(stage, stage_rows, nodes, document["grades"]) + "\n"
    for row in rows:
        outputs[f"{DOCS_REL}/nodes/{row['id']}.md"] = node_page(row, nodes[row["id"]], document, rows_by_id)
    return outputs
