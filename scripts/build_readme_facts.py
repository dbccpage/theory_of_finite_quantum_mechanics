"""Regenerate the facts block of README.md from repository files.

AuthorityEffect: None. Every number in the block is computed here from a named
file or from the output of a named repository command; nothing is typed by hand.
The block sits between the markers ``<!-- facts:begin -->`` and
``<!-- facts:end -->``.

    python -I -X utf8 scripts/build_readme_facts.py --write    # rewrite the block
    python -I -X utf8 scripts/build_readme_facts.py --check    # exit 1 if stale

``--skip-contracts`` reuses the contract/score row already in README.md instead
of running ``scripts/contract_scores.py check`` (about a minute); the fast test
in ``dag/test_readme_facts.py`` uses it. Counts are inventory counts: a test
function count is not a pass result, and a Lean file count is not a build.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
BEGIN = "<!-- facts:begin -->"
END = "<!-- facts:end -->"
CONTRACT_ROW = "| Contract/score companions |"
ATLAS_PREFIX = "atlas/"
ALLOWED_AXIOMS = ("propext", "Classical.choice", "Quot.sound")
SCOPE_EFFECTS = ("consistent", "caveat_added", "statement_narrowed", "status_lowered")
# Nodes named in the README text; their stage and status are read from the DAG.
NAMED_NODES = (
    "FQ-GAP-BORN-UNIQUENESS-GLEASON",
    "FQ-CONTINUUM-HILBERT-LIFT-CONSTRUCTION",
    "FQ-GAP-CONTINUUM-HILBERT-LIFT",
    "L1-IMP-HILBERT-INNER-PRODUCT",
    "L1-IMP-COMPLEX-FIELD",
    "FQ-GAP-STONE-CONTINUOUS-TIME",
    "FQ-GAP-U1-CIRCLE",
    "L1-IMP-LINEAR-ISOMETRIC-DYNAMICS",
    "PGW-ENDOGENOUS-DEMAND-OB1",
    "COMP-C4-UNBOUNDED-SUPPLY-IMPORT",
    "COMP-C7-NF-REACH-UNDECIDABLE",
    "QCV-VIABILITY-NEEDS-ALL-REQUIREMENTS",
    "QCV-PHYSICAL-SATISFIABILITY-OPEN",
    "MUB6-MAX-MUB-SIX-EQUALS-THREE",
    "FSP-MASTER-DICHOTOMY-REFUTED",
    "TFQ-0084",
)


def load_json(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def link(rel: str) -> str:
    return f"[`{rel}`]({rel})"


def tracked_files() -> list[str]:
    out = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT)
    names = [n for n in out.decode("utf-8").split("\0") if n]
    # atlas/ is a byte-identical source archive of paper folders, not part of this repository's inventory.
    return sorted(n for n in names if not n.startswith(ATLAS_PREFIX) and (ROOT / n).is_file())


# ---------------------------------------------------------------- DAG facts

def dag_facts() -> dict:
    dag = load_json("dag/derivation_dag.json")
    nodes = dag["nodes"]
    review_key = [n for n in nodes if "pfp_review" in n]
    effects = collections.Counter(
        (n["pfp_review"] or {}).get("scope_effect") for n in review_key)
    return {
        "nodes": len(nodes),
        "routes": len(dag["routes"]),
        "stages_declared": len(dag["stages"]),
        "stages_used": len({n["stage"] for n in nodes}),
        "by_status": collections.Counter(n["status"] for n in nodes),
        "by_stage": collections.Counter(n["stage"] for n in nodes),
        "stage_order": list(dag["stages"]),
        "by_id": {n["id"]: n for n in nodes},
        "pfp_review_nodes": len(review_key),
        "pfp_effects": effects,
        "refs": reference_resolution(nodes),
    }


def reference_resolution(nodes) -> dict:
    counts = collections.Counter()
    for node in nodes:
        for field in ("lean", "rust"):
            for ref in node[field]:
                path = ref.split("::")[0]
                if re.match(r"^[a-z]+:", path):
                    counts[(field, "external")] += 1
                elif (ROOT / path).exists():
                    counts[(field, "present")] += 1
                else:
                    counts[(field, "absent")] += 1
    return counts


def validator_line() -> str:
    proc = subprocess.run(
        [sys.executable, "-I", "-X", "utf8", "dag/validate_derivation_dag.py", "--no-files"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    lines = [ln for ln in proc.stdout.splitlines() if ln.strip()]
    return (lines[-1] if lines else "no output") + f" (exit {proc.returncode})"


def jsonl_records() -> int:
    text = (ROOT / "dag/theory_of_finite_qm.jsonl").read_text(encoding="utf-8")
    return sum(1 for ln in text.splitlines() if ln.strip())


def derivation_papers() -> tuple[int, int]:
    base = ROOT / "dag/derivations"
    folders = [p for p in base.iterdir() if p.is_dir()]
    papers = sum(1 for f in folders for p in f.rglob("*.md"))
    return papers, len(folders)


# ---------------------------------------------------------------- PFP facts

def pfp_facts() -> dict:
    prompts = sorted((ROOT / "dag/prompts").glob("*.yaml"))
    index = load_json("dag/operads/index.json")["nodes"]
    stages = collections.Counter(n["current_stage"] for n in index)
    review_dirs = sorted(p for p in (ROOT / "dag/results").glob("*/reviews/*") if p.is_dir())
    nodes_with_reviews = {p.parent.parent.name for p in review_dirs}
    boundaries = sum(1 for d in review_dirs if has_boundary(d))
    p4 = 0
    for d in review_dirs:
        # review_result.json and delivery_review_result.json may repeat one count.
        values = [v.get("rejected_P4_mutations") for v in map(_read_json, d.glob("*.json"))
                  if isinstance(v, dict)]
        p4 += max([v for v in values if isinstance(v, int)], default=0)
    return {
        "prompts": len(prompts),
        "index_nodes": len(index),
        "stages": stages,
        "review_dirs": len(review_dirs),
        "nodes_with_reviews": len(nodes_with_reviews),
        "boundaries": boundaries,
        "p4_rejected": p4,
    }


def _read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeDecodeError):
        return None


def has_boundary(directory: Path) -> bool:
    keys = ("supports", "does_not_support", "narrowest_claim")
    for f in directory.glob("*.json"):
        value = _read_json(f)
        if not isinstance(value, dict):
            continue
        for candidate in (value.get("claim_boundary"), value):
            if isinstance(candidate, dict) and all(k in candidate for k in keys):
                return True
    return False


def corpus_audit() -> dict:
    records = load_json("dag/fragments/unified_dag.json")["domain_records"]
    claimed = [r for r in records if r["source_claimed_status"] == "PROVED_LEAN"]
    return {
        "records": len(records),
        "corpora": len({r["corpus"] for r in records}),
        "claimed_lean": len(claimed),
        "kept_lean": sum(1 for r in claimed if r["status"] == "PROVED_LEAN"),
        "refuted": sum(1 for r in claimed if r["status"] == "REFUTED"),
        "lowered": collections.Counter(
            r["status"] for r in claimed if r["status"] not in ("PROVED_LEAN", "REFUTED")),
    }


# ---------------------------------------------------------------- Lean facts

def lean_facts(files: list[str]) -> dict:
    lean = [f for f in files if f.endswith(".lean")]
    trees = collections.Counter()
    for f in lean:
        top = f.split("/")[0]
        trees[top if top in ("lean4", "papers", "code", "dag") else "other"] += 1
    lakefile = (ROOT / "lean4/lakefile.lean").read_text(encoding="utf-8")
    code_only = "\n".join(ln.split("--")[0] for ln in lakefile.splitlines())
    roots = []
    for block in re.findall(r"roots\s*:=\s*#\[(.*?)\]", code_only, flags=re.S):
        roots += re.findall(r"`([\w.«»]+)", block)
    mathlib = re.search(r'require\s+mathlib\s+from\s+git\s+"[^"]+"\s*@\s*"([^"]+)"', lakefile)
    manifest = load_json("lean4/lake-manifest.json")
    rev = next((p["rev"] for p in manifest["packages"] if p["name"] == "mathlib"), None)
    return {
        "trees": trees,
        "libs": len(re.findall(r"^\s*lean_lib\b", code_only, flags=re.M)),
        "roots": len(roots),
        "toolchain": (ROOT / "lean4/lean-toolchain").read_text(encoding="utf-8").strip(),
        "mathlib": mathlib.group(1) if mathlib else None,
        "mathlib_rev": rev,
        "placeholders": placeholder_counts(lean),
    }


def strip_lean(text: str) -> str:
    """Remove comments (nested block and line) and string literals."""
    out, i, depth, n = [], 0, 0, len(text)
    while i < n:
        if text.startswith("/-", i):
            depth += 1; i += 2; continue
        if depth and text.startswith("-/", i):
            depth -= 1; i += 2; continue
        if depth:
            if text[i] == "\n":
                out.append("\n")
            i += 1; continue
        if text.startswith("--", i):
            j = text.find("\n", i)
            i = n if j < 0 else j; continue
        if text[i] == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == chr(92) else 1
            i = j + 1; continue
        out.append(text[i]); i += 1
    return "".join(out)


ADMIT_TACTIC = re.compile(r"(?:^\s*(?:·\s*)?|\bby\s+|;\s*|<;>\s*)admit\s*$", re.M)


def placeholder_counts(lean: list[str]) -> dict:
    counts = collections.Counter()
    for rel in lean:
        top = rel.split("/")[0]
        if top not in ("lean4", "papers", "code"):
            continue
        text = strip_lean((ROOT / rel).read_text(encoding="utf-8", errors="replace"))
        counts[(top, "sorry")] += len(re.findall(r"(?<![\w.'])sorry(?![\w'])", text))
        tactic = len(ADMIT_TACTIC.findall(text))
        counts[(top, "admit")] += tactic
        counts[(top, "admit_ident")] += len(re.findall(r"(?<![\w'])admit(?![\w'])", text)) - tactic
    return counts


AXIOM_LINE = (
    re.compile(r"depends on axioms:\s*\[([^\]]*)\]"),
    re.compile(r"^\S+\.lean:\d+\s+\S+\s+\[([^\]]*)\]\s*$"),
    re.compile(r"^\s*Axioms:\s*\[([^\]]*)\]"),
)
NO_AXIOM_LINE = re.compile(r"does not depend on any axioms")


def axiom_receipts(files: list[str]) -> dict:
    receipts = [f for f in files if (
        re.fullmatch(r"dag/research/[^/]*axioms[^/]*\.txt", f)
        or re.fullmatch(r"papers/.*/axiom_report[^/]*\.txt", f)
        or re.fullmatch(r"(?:.*/)?evidence/axiom_reports/[^/]*\.txt", f))]
    per_file, seen, print_lines = {}, collections.Counter(), 0
    for rel in receipts:
        lines = 0
        for ln in (ROOT / rel).read_text(encoding="utf-8", errors="replace").splitlines():
            print_lines += "#print axioms" in ln
            if NO_AXIOM_LINE.search(ln):
                lines += 1; continue
            for pattern in AXIOM_LINE:
                m = pattern.search(ln)
                if m:
                    lines += 1
                    for ax in (a.strip() for a in m.group(1).split(",")):
                        if ax and ax != "none":
                            seen[ax] += 1
                    break
        per_file[rel] = lines
    return {"files": per_file, "seen": seen, "print_lines": print_lines,
            "outside": sorted(a for a in seen if a not in ALLOWED_AXIOMS)}


# ---------------------------------------------------------------- tests, contracts

def test_functions(files: list[str]) -> dict:
    counts = collections.Counter()
    for rel in files:
        scope = "results" if rel.startswith("dag/results/") else "main"
        if rel.endswith(".py"):
            text = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
            counts[("py", scope)] += len(re.findall(r"^\s*(?:async\s+)?def test_\w*", text, re.M))
        elif rel.endswith(".rs"):
            text = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
            counts[("rs", scope)] += len(re.findall(r"#\[test\]", text))
    return counts


def contract_row(skip: bool) -> str:
    if skip:
        current = README.read_text(encoding="utf-8")
        start, end = current.find(BEGIN), current.find(END)
        for ln in current[max(start, 0):max(end, 0)].splitlines():
            if ln.startswith(CONTRACT_ROW):
                return ln
    proc = subprocess.run(
        [sys.executable, "-I", "-X", "utf8", "scripts/contract_scores.py", "check"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    try:
        result = json.loads(proc.stdout)
        value = (f"combined_files = {result['combined_files']}, "
                 f"all_passed = {str(result['all_passed']).lower()}")
    except (ValueError, KeyError):
        value = f"could not parse output (exit {proc.returncode})"
    return f"{CONTRACT_ROW} {value} | `python -I -X utf8 scripts/contract_scores.py check` |"


# ---------------------------------------------------------------- render

def fmt_counter(counter, order=None) -> str:
    keys = order or sorted(counter, key=lambda k: (-counter[k], k))
    return ", ".join(f"{k} {counter[k]}" for k in keys if counter.get(k))


def render(skip_contracts: bool = False) -> str:
    files = tracked_files()
    dag = dag_facts()
    pfp = pfp_facts()
    audit = corpus_audit()
    lean = lean_facts(files)
    axioms = axiom_receipts(files)
    tests = test_functions(files)
    papers, folders = derivation_papers()
    refs = dag["refs"]
    ph = lean["placeholders"]

    if dag["pfp_review_nodes"]:
        review = (f"{dag['pfp_review_nodes']} nodes carry `pfp_review`; scope_effect: "
                  + fmt_counter(dag["pfp_effects"], SCOPE_EFFECTS))
    else:
        review = "pending merge of #133 (no node on this branch carries a `pfp_review` key)"

    rows = [
        ("Derivation DAG nodes / routes", f"{dag['nodes']} / {dag['routes']}", link("dag/derivation_dag.json")),
        ("DAG stages (declared / with nodes)", f"{dag['stages_declared']} / {dag['stages_used']}", link("dag/derivation_dag.json")),
        ("DAG validator", f"`{validator_line()}`", "`python -I -X utf8 dag/validate_derivation_dag.py --no-files`"),
        ("TFQ records", str(jsonl_records()), link("dag/theory_of_finite_qm.jsonl")),
        ("Derivation papers", f"{papers} in {folders} stage folders", link("dag/derivations")),
        ("Lean references in DAG nodes",
         f"{refs[('lean', 'present')]} resolve to a file in this checkout, {refs[('lean', 'absent')]} do not "
         f"(sibling or historical paths), {refs[('lean', 'external')]} marked `external:`", link("dag/derivation_dag.json")),
        ("Rust references in DAG nodes",
         f"{refs[('rust', 'present')]} resolve to a file in this checkout, {refs[('rust', 'absent')]} do not, "
         f"{refs[('rust', 'external')]} marked `external:`", link("dag/derivation_dag.json")),
        ("PFP prompts / indexed operad collections", f"{pfp['prompts']} / {pfp['index_nodes']}",
         f"{link('dag/prompts')}, {link('dag/operads/index.json')}"),
        ("PFP stage per prompt", fmt_counter(pfp["stages"]), link("dag/operads/index.json")),
        ("Nodes with executed review results", f"{pfp['nodes_with_reviews']} nodes, {pfp['review_dirs']} review directories",
         "`dag/results/*/reviews/`"),
        ("Review directories with a supports / does_not_support / narrowest_claim boundary",
         str(pfp["boundaries"]), "`dag/results/*/reviews/*/*.json`"),
        ("P4 mutations rejected, as recorded in review records (`rejected_P4_mutations`, one value per directory)", str(pfp["p4_rejected"]),
         "`dag/results/*/reviews/*/*.json`"),
        ("PFP review outcomes on DAG nodes", review, link("dag/derivation_dag.json")),
        ("Outside-corpus records audited", f"{audit['records']} records from {audit['corpora']} corpora",
         link("dag/fragments/unified_dag.json")),
        ("Of those, claimed `PROVED_LEAN` by their source",
         f"{audit['claimed_lean']}: kept {audit['kept_lean']}, refuted {audit['refuted']}, recorded lower "
         f"{sum(audit['lowered'].values())} ({fmt_counter(audit['lowered'])})", link("dag/fragments/unified_dag.json")),
        ("Tracked `.lean` files", fmt_counter(lean["trees"], ["lean4", "papers", "code", "dag", "other"])
         + " (the `dag` files are run snapshots)", "`git ls-files`"),
        ("Lake libraries / module roots in `lean4/lakefile.lean`", f"{lean['libs']} / {lean['roots']}", link("lean4/lakefile.lean")),
        ("Lean toolchain", f"`{lean['toolchain']}`", link("lean4/lean-toolchain")),
        ("Mathlib", f"`{lean['mathlib']}` (manifest rev `{(lean['mathlib_rev'] or '')[:12]}`)",
         f"{link('lean4/lakefile.lean')}, {link('lean4/lake-manifest.json')}"),
        ("Axiom receipts / declaration lines audited",
         f"{len(axioms['files'])} files / {sum(axioms['files'].values())} lines "
         f"(literal `#print axioms` lines: {axioms['print_lines']})",
         "`dag/research/*axioms*.txt`, `papers/**/axiom_report*.txt`, `**/evidence/axiom_reports/*.txt`"),
        ("Axioms named in those receipts", fmt_counter(axioms["seen"]) + "; outside {propext, Classical.choice, Quot.sound}: "
         + (", ".join(axioms["outside"]) or "none"), "same receipts"),
        ("`sorry` tokens outside comments and strings",
         f"lean4 {ph[('lean4', 'sorry')]}, papers {ph[('papers', 'sorry')]}, code {ph[('code', 'sorry')]}", "`git ls-files '*.lean'`"),
        ("`admit` used as a tactic",
         f"lean4 {ph[('lean4', 'admit')]}, papers {ph[('papers', 'admit')]}, code {ph[('code', 'admit')]} "
         f"(identifiers named `admit`: {ph[('lean4', 'admit_ident')] + ph[('papers', 'admit_ident')] + ph[('code', 'admit_ident')]})",
         "`git ls-files '*.lean'`"),
        ("Python test functions (`def test_`)", f"{tests[('py', 'main')]} (plus {tests[('py', 'results')]} in `dag/results` snapshots)",
         "`git ls-files '*.py'`"),
        ("Rust test functions (`#[test]`)", f"{tests[('rs', 'main')]} (plus {tests[('rs', 'results')]} in `dag/results` snapshots)",
         "`git ls-files '*.rs'`"),
    ]
    out = [BEGIN,
           "<!-- Generated by scripts/build_readme_facts.py --write. Do not edit by hand. -->",
           "",
           "| Fact | Value | Source |",
           "|---|---|---|"]
    out += [f"| {a} | {b} | {c} |" for a, b, c in rows]
    out.append(contract_row(skip_contracts))
    out += ["",
            "Counts of test functions and files are inventory counts, not pass results. "
            "Status labels are the DAG's own; the legend is in `dag/derivation_dag.json` (`status_legend`).",
            "",
            "Nodes by status: " + fmt_counter(dag["by_status"]) + ".",
            "",
            "Nodes by stage: " + fmt_counter(dag["by_stage"], [s for s in dag["stage_order"]]) + ".",
            "",
            "Nodes named in this README:",
            "",
            "| Node | Stage | Status |",
            "|---|---|---|"]
    for node_id in NAMED_NODES:
        node = dag["by_id"].get(node_id)
        out.append(f"| `{node_id}` | {node['stage']} | `{node['status']}` |" if node
                   else f"| `{node_id}` | absent on this branch | |")
    out.append(END)
    return "\n".join(out)


def splice(text: str, block: str) -> str:
    start, end = text.find(BEGIN), text.find(END)
    if start < 0 or end < start:
        raise SystemExit("README.md has no facts markers")
    return text[:start] + block + text[end + len(END):]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--skip-contracts", action="store_true")
    args = parser.parse_args(argv)
    current = README.read_text(encoding="utf-8")
    updated = splice(current, render(args.skip_contracts))
    if args.write:
        if updated != current:
            README.write_text(updated, encoding="utf-8", newline="\n")
        print("README facts written")
        return 0
    if updated != current:
        print("README facts are stale: run scripts/build_readme_facts.py --write")
        return 1
    print("README facts current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
