"""Build the evidence map of the derivation DAG from the DAG and the files on disk.

AuthorityEffect: None. This script reads dag/derivation_dag.json, the Lean replay
receipts in dag/research/ and the files the DAG cites. It writes a machine-readable
map (dag/evidence/evidence_map.json) and human-facing pages (docs/evidence/). It
changes no node status, runs no Lean, Rust or Python test, and calls no provider.

    python -I -X utf8 dag/evidence/build_evidence.py --write   # regenerate
    python -I -X utf8 dag/evidence/build_evidence.py --check   # exit 1 if stale

Every statement in the output is computed from a named file. Existence, symbol
presence and sha256 values are checks of this checkout only. A reference that
points outside this repository (the sibling atlas trees) is recorded as
external_unresolved: it is neither confirmed nor refuted here.

Evidence grades (computed; they rate the evidence, they do not restate a status):

  E0  no counted in-repo evidence file
  E1  at least one counted in-repo evidence file exists
  E2  E1, and at least one cited Lean, Rust or Python symbol is found in its
      in-repo file (the leaf rule of dag/validate_derivation_dag.py)
  E3  E2, and at least one cited Lean declaration lies in a file whose current
      sha256 equals the sha256 in a replay receipt with exit code 0, an
      axiom audit that passed and only propext, Classical.choice, Quot.sound
  E4  E3, plus an in-repo Rust or Python runnable test among the counted
      evidence, plus a recorded statement-match review of the node

"Counted" evidence is evidence that the node cites itself, or that a TFQ record
cites when that record names this node and no other. Evidence that a record
shares with other nodes is listed but not counted. Generated views (derivation
papers written by the syncs, the JSONL and Markdown views) are listed and never
counted.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "dag"
DAG_REL = "dag/derivation_dag.json"
MAP_REL = "dag/evidence/evidence_map.json"
DOCS_REL = "docs/evidence"
RESEARCH_REL = "dag/research"
FRONTIER_REVIEW_REL = "dag/research/frontier_targets_lean_review.md"
SCHEMA = "evidence_map.v1"

ALLOWED_AXIOMS = ("propext", "Classical.choice", "Quot.sound")
GRADES = ("E0", "E1", "E2", "E3", "E4")
EXTERNAL_PREFIXES = ("pr:", "external:")
PINNED_EOL_SUFFIXES = (".lean", ".rs", ".py", ".toml")
GENERATED_PATHS = (
    "dag/derivation_dag.json",
    "dag/theory_of_finite_qm.jsonl",
    "dag/theory_of_finite_qm.md",
)
CODE_KINDS = ("lean_decl", "rust_symbol", "rust_test", "python_symbol", "python_test")
KIND_GROUP = {"lean_decl": 0, "rust_symbol": 1, "rust_test": 1, "python_symbol": 2, "python_test": 2,
              "paper": 3, "external": 4}
GROUP_TITLE = {0: "Lean", 1: "Rust", 2: "Python", 3: "Documents and data", 4: "External sources"}
MISMATCH_ORDER = (
    "proved_lean_below_e3",
    "proved_lean_external_only",
    "receipt_not_current",
    "computational_no_runnable_test",
    "proved_prose_no_in_repo_document",
    "broken_reference",
    "receipt_names_uncited_module",
)
MISMATCH_TEXT = {
    "receipt_names_uncited_module": "A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence)",
    "proved_lean_below_e3": "PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt",
    "proved_lean_external_only": "PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout",
    "receipt_not_current": "A replay receipt exists for a cited Lean file, but its sha256 no longer matches the file or it records a failure",
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


# ---------------------------------------------------------------- file access

class Files:
    """Reads each repository file once; reports sha256 and text."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self._info: dict[str, dict | None] = {}
        self._text: dict[str, str] = {}

    def info(self, rel: str) -> dict | None:
        if rel not in self._info:
            path = self.root / rel
            if not path.is_file():
                self._info[rel] = None
            else:
                data = path.read_bytes()
                raw = hashlib.sha256(data).hexdigest()
                lf = hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()
                pinned = rel.endswith(PINNED_EOL_SUFFIXES)
                self._info[rel] = {
                    "sha256": raw if pinned else lf,
                    "sha256_basis": "bytes" if pinned else "lf-normalised",
                    "sha256_raw": raw,
                    "sha256_lf": lf,
                    "size": len(data),
                }
                self._text[rel] = data.decode("utf-8", errors="replace").replace("\r\n", "\n")
        return self._info[rel]

    def text(self, rel: str) -> str:
        self.info(rel)
        return self._text.get(rel, "")

    def is_dir(self, rel: str) -> bool:
        return (self.root / rel).is_dir()


def load_json(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


# ---------------------------------------------------------------- references

LINE_SUFFIX = re.compile(r"^(.*?):(\d+(?:[-,]\d+)*)$")


def parse_ref(ref: str) -> tuple[str, str | None, str | None]:
    """Split path::symbol, drop a #anchor or :line suffix (kept as `where`)."""
    path, _, symbol = ref.partition("::")
    where = None
    if "#" in path:
        path, where = path.split("#", 1)
    match = LINE_SUFFIX.match(path)
    if match:
        path, where = match.group(1), match.group(2)
    return path, (symbol or None), where


def is_outside(path: str) -> bool:
    top = path.split("/")[0]
    return top.startswith("omega_engine") or top == ".claude"


def leaf_of(symbol: str) -> str:
    return symbol.split("::")[-1].split(".")[-1]


def declared_pattern(kind: str, leaf: str) -> re.Pattern:
    name = re.escape(leaf)
    if kind == "lean_decl":
        keywords = r"(?:theorem|lemma|def|abbrev|structure|inductive|class|instance|axiom|opaque|example)"
        return re.compile(
            rf"(?<![\w.']){keywords}\s+(?:[\w.'«»]*\.)?{name}(?![\w'])"
            rf"|^\s*\|\s*{name}(?![\w'])|^\s+{name}\s*:", re.M)
    if kind.startswith("rust"):
        return re.compile(rf"\b(?:fn|struct|enum|trait|const|static|type|mod|union)\s+{name}\b")
    return re.compile(rf"^\s*(?:async\s+)?(?:def|class)\s+{name}\b|^{name}\s*[:=]", re.M)


def rust_test_pattern(leaf: str) -> re.Pattern:
    return re.compile(
        r"#\[(?:test|tokio::test)\][^\n]*\n(?:\s*#\[[^\n]*\n)*\s*(?:pub\s+)?(?:async\s+)?fn\s+"
        + re.escape(leaf) + r"\b")


def is_test_file(path: str) -> bool:
    name = path.rsplit("/", 1)[-1]
    return "/tests/" in path or name.startswith("test_") or name.endswith("_test.py")


class Crates:
    """Maps a Rust path under code/rust to the cargo package that owns it."""

    def __init__(self, files: Files) -> None:
        self.files = files
        self.root_package = self._name("code/rust/Cargo.toml") or "theory_of_finite_qm"
        self._cache: dict[str, str] = {}

    def _name(self, rel: str) -> str | None:
        match = re.search(r'^\s*name\s*=\s*"([^"]+)"', self.files.text(rel), re.M)
        return match.group(1) if match else None

    def package(self, path: str) -> str:
        parts = path.split("/")
        if len(parts) > 4 and parts[:3] == ["code", "rust", "src"]:
            key = parts[3]
            if key not in self._cache:
                self._cache[key] = self._name(f"code/rust/src/{key}/Cargo.toml") or self.root_package
            return self._cache[key]
        return self.root_package


def lean_module(path: str) -> str | None:
    if path.startswith("lean4/") and path.count("/") == 1 and path.endswith(".lean"):
        return path[len("lean4/"):-len(".lean")]
    return None


def lake_roots(files: Files) -> set[str]:
    code = "\n".join(line.split("--")[0] for line in files.text("lean4/lakefile.lean").splitlines())
    roots: set[str] = set()
    for block in re.findall(r"roots\s*:=\s*#\[(.*?)\]", code, flags=re.S):
        roots.update(re.findall(r"`([\w.«»]+)", block))
    return roots


# ---------------------------------------------------------------- receipts

AXIOM_PRINT = re.compile(r"'([^']+)'\s+depends on axioms:\s*\[([^\]]*)\]", re.S)
NO_AXIOM_PRINT = re.compile(r"'([^']+)'\s+does not depend on any axioms")


def parse_axiom_output(text: str) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for name, axioms in AXIOM_PRINT.findall(text):
        found[name] = sorted(a.strip() for a in axioms.replace("\n", " ").split(",") if a.strip())
    for name in NO_AXIOM_PRINT.findall(text):
        found.setdefault(name, [])
    return found


def toolchain_of(lean_version: str | None) -> str | None:
    if not lean_version:
        return None
    match = re.search(r"version\s+([\w.\-]+)", lean_version)
    return match.group(1) if match else lean_version


def load_receipts(files: Files) -> tuple[list[dict], list[dict]]:
    """Index every dag/research/*.json that records Lean module results with a sha256."""
    receipts: list[dict] = []
    skipped: list[dict] = []
    for path in sorted((ROOT / RESEARCH_REL).glob("*.json")):
        rel = path.relative_to(ROOT).as_posix()
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if not isinstance(data, dict):
            continue
        meta = data.get("lean_replay") if isinstance(data.get("lean_replay"), dict) else None
        results = meta.get("results") if meta else None
        if not isinstance(results, list):
            attempt = data.get("results")
            if isinstance(attempt, list) and data.get("lean_version"):
                bad = any(isinstance(r, dict) and r.get("exit_code") not in (0, None) for r in attempt)
                skipped.append({"file": rel, "reason": "an attempt record, not a lean_replay receipt"
                                + ("; at least one module exited with a nonzero code" if bad else "")})
            elif "Lean" in json.dumps(data.get("checks", "")):
                skipped.append({"file": rel, "reason": "records Lean checks without per-module sha256"})
            continue
        file_info = files.info(rel) or {}
        for number, entry in enumerate(results):
            if not isinstance(entry, dict) or "module" not in entry or "sha256" not in entry:
                continue
            decl_axioms: dict[str, list[str]] = {}
            if isinstance(entry.get("axioms"), dict):
                decl_axioms = {k: sorted(v) for k, v in entry["axioms"].items() if isinstance(v, list)}
            elif isinstance(entry.get("output"), str):
                decl_axioms = parse_axiom_output(entry["output"])
            union = sorted({a for v in decl_axioms.values() for a in v})
            module = entry["module"]
            receipts.append({
                "id": f"{rel}#{number}:{module}",
                "dag_node": entry.get("dag_node"),
                "receipt_file": rel,
                "receipt_file_sha256": file_info.get("sha256_lf"),
                "checked_at": data.get("checked_at"),
                "module": module,
                "path": entry.get("source") or f"lean4/{module}.lean",
                "recorded_sha256": entry["sha256"],
                "exit_code": entry.get("exit_code"),
                "lean_version": meta.get("lean_version"),
                "toolchain": toolchain_of(meta.get("lean_version")),
                "mathlib_source_sha": meta.get("mathlib_source_sha"),
                "axiom_audit_passed": entry.get("axiom_audit_passed"),
                "admission_scan_passed": entry.get("admission_scan_passed"),
                "source_unchanged_during_build": entry.get("source_unchanged_during_build"),
                "built_successfully": entry.get("built_successfully"),
                "axioms_itemised": bool(decl_axioms),
                "axioms_union": union,
                "axioms_standard": all(a in ALLOWED_AXIOMS for a in union),
                "decl_count": len(decl_axioms),
                "_decl_axioms": decl_axioms,
                "_anchors": list(entry.get("anchors") or []),
            })
    return receipts, skipped


def receipt_ok(receipt: dict, sha_match: bool) -> bool:
    return bool(
        sha_match
        and receipt["exit_code"] == 0
        and receipt["axiom_audit_passed"] is not False
        and receipt["admission_scan_passed"] is not False
        and receipt["source_unchanged_during_build"] is not False
        and receipt["built_successfully"] is not False
        and receipt["axioms_standard"])


def decl_matches(symbol: str, name: str) -> bool:
    return name == symbol or name.endswith("." + symbol) or symbol.endswith("." + name)


# ---------------------------------------------------------------- reviews

FRONTIER_ROW = re.compile(r"^\|\s*([A-Z][A-Z0-9-]+)\s*\|(.*)\|\s*(FULL|NARROWED|REVERTED)\s*\|(.*)\|\s*$")


def frontier_reviews(files: Files) -> dict[str, dict]:
    info = files.info(FRONTIER_REVIEW_REL)
    if info is None:
        return {}
    out: dict[str, dict] = {}
    for line in files.text(FRONTIER_REVIEW_REL).splitlines():
        match = FRONTIER_ROW.match(line)
        if match:
            out[match.group(1)] = {
                "source": "frontier_targets_lean_review",
                "review": FRONTIER_REVIEW_REL,
                "review_sha256": info["sha256_lf"],
                "review_file_ok": True,
                "verdict": match.group(3),
                "theorems": match.group(2).strip(),
                "scope_effect": None,
                "narrowest_claim": None,
                "qualifies": match.group(3) in ("FULL", "NARROWED"),
            }
    return out


def pfp_review_of(node: dict, files: Files) -> dict | None:
    review = node.get("pfp_review")
    if not isinstance(review, dict):
        return None
    path = review.get("review")
    info = files.info(path) if isinstance(path, str) else None
    ok = bool(info and info["sha256_lf"] == review.get("review_sha256"))
    claim = review.get("narrowest_claim") or ""
    return {
        "source": "pfp_review",
        "review": path,
        "review_sha256": review.get("review_sha256"),
        "review_file_ok": ok,
        "verdict": review.get("verdict"),
        "scope_effect": review.get("scope_effect"),
        "narrowest_claim": claim,
        "does_not_support": review.get("does_not_support"),
        "next_test": review.get("next_test"),
        "prior_status": review.get("prior_status"),
        "qualifies": bool(ok and review.get("verdict") and claim and review.get("scope_effect") != "status_lowered"),
    }


# ---------------------------------------------------------------- items

class Builder:
    def __init__(self) -> None:
        self.files = Files(ROOT)
        self.dag = load_json(DAG_REL)
        self.nodes = {n["id"]: n for n in self.dag["nodes"]}
        self.crates = Crates(self.files)
        self.roots = lake_roots(self.files)
        self.receipts, self.skipped_receipts = load_receipts(self.files)
        self.receipts_by_path: dict[str, list[dict]] = collections.defaultdict(list)
        for receipt in self.receipts:
            self.receipts_by_path[receipt["path"]].append(receipt)
        self.frontier = frontier_reviews(self.files)
        self.papers = self._derivation_papers()
        self.records_by_node: dict[str, list[dict]] = collections.defaultdict(list)
        for record in self.dag["records"]:
            for node_id in record["existing_derivation_dag_ids"]:
                if node_id in self.nodes:
                    self.records_by_node[node_id].append(record)
        self.cited_files: set[str] = set()

    def _derivation_papers(self) -> dict[str, str]:
        papers: dict[str, str] = {}
        for path in sorted((ROOT / "dag/derivations").rglob("tfq_*.md")):
            match = re.match(r"tfq_(\d{4})_", path.name)
            if match:
                papers["TFQ-" + match.group(1)] = path.relative_to(ROOT).as_posix()
        return papers

    # -- one reference -> one item
    def make_item(self, ref: str, cited_in: str, counted: bool) -> dict | None:
        if ref.startswith("absent:"):
            return None
        external = ref.startswith(EXTERNAL_PREFIXES)
        path, symbol, where = parse_ref(ref)
        item: dict = {
            "path": path, "symbol": symbol, "where": where,
            "cited_in": [cited_in], "counted": counted,
            "file_exists": False, "symbol_exists": None, "symbol_declared": None,
            "generated": False, "replay": "n/a", "receipts": [], "decl_listed": False,
            "decl_axioms": None, "command": None, "command_note": None,
        }
        if external:
            item.update(kind="external", resolution="external")
            return item
        ext = Path(path).suffix.lower() if "." in path.rsplit("/", 1)[-1] else ""
        kind = {".lean": "lean_decl", ".rs": "rust_symbol", ".py": "python_symbol"}.get(ext, "paper")
        item["generated"] = path in GENERATED_PATHS or bool(re.match(r"dag/derivations/.+/tfq_\d{4}_.+\.md$", path))
        info = self.files.info(path)
        if info is None and not self.files.is_dir(path):
            item.update(kind=kind, resolution="external_unresolved" if is_outside(path) else "missing")
            return item
        item.update(kind=kind, resolution="present", file_exists=True)
        self.cited_files.add(path)
        if info is None:  # a directory
            item["is_dir"] = True
            return item
        if symbol and kind != "paper":
            leaf = leaf_of(symbol)
            text = self.files.text(path)
            item["symbol_exists"] = leaf in text
            item["symbol_declared"] = bool(declared_pattern(kind, leaf).search(text))
        self._classify_test(item)
        if item["kind"] == "lean_decl":
            self._attach_receipts(item, info)
        item["command"], item["command_note"] = self._command(item)
        return item

    def _classify_test(self, item: dict) -> None:
        path, symbol, kind = item["path"], item["symbol"], item["kind"]
        if kind == "rust_symbol":
            if symbol and rust_test_pattern(leaf_of(symbol)).search(self.files.text(path)):
                item["kind"] = "rust_test"
            elif not symbol and path.startswith("code/rust/tests/"):
                item["kind"] = "rust_test"
        elif kind == "python_symbol":
            if symbol:
                leaf = leaf_of(symbol)
                if is_test_file(path) and (leaf.startswith("test") or leaf.startswith("Test")
                                           or any(p.startswith("Test") for p in symbol.split("."))):
                    item["kind"] = "python_test"
            elif is_test_file(path):
                item["kind"] = "python_test"

    def _attach_receipts(self, item: dict, info: dict) -> None:
        rows = []
        symbol = item["symbol"]
        listed_axioms: set[str] = set()
        for receipt in self.receipts_by_path.get(item["path"], []):
            sha_match = receipt["recorded_sha256"] in (info["sha256_raw"], info["sha256_lf"])
            listed = False
            if symbol:
                for name, axioms in receipt["_decl_axioms"].items():
                    if decl_matches(symbol, name):
                        listed = True
                        listed_axioms.update(axioms)
                if any(decl_matches(symbol, name) for name in receipt["_anchors"]):
                    listed = True
            rows.append({"id": receipt["id"], "sha_match": sha_match,
                         "ok": receipt_ok(receipt, sha_match), "decl_listed": listed})
        item["receipts"] = sorted(rows, key=lambda r: r["id"])
        if not rows:
            item["replay"] = "none"
        elif any(r["ok"] for r in rows):
            item["replay"] = "verified"
        elif any(r["sha_match"] for r in rows):
            item["replay"] = "failed"
        else:
            item["replay"] = "stale"
        verified = [r for r in rows if r["ok"]]
        item["decl_listed"] = any(r["decl_listed"] for r in verified)
        if item["decl_listed"]:
            item["decl_axioms"] = sorted(listed_axioms)

    def _command(self, item: dict) -> tuple[str | None, str | None]:
        path, symbol, kind = item["path"], item["symbol"], item["kind"]
        if kind == "lean_decl":
            module = lean_module(path)
            if module and module in self.roots:
                build = f"cd lean4 && lake build {module}"
            else:
                build = f"cd lean4 && lake build   # the library that contains {path}"
            if symbol and module:
                return build, f"then, in a scratch file that imports {module}: #print axioms {symbol}"
            return build, None
        if kind == "python_test":
            target = path
            if item["symbol"]:
                target += "::" + item["symbol"].replace(".", "::")
            return f"python -m pytest {target}", None
        if kind == "rust_test" or kind == "rust_symbol":
            if not path.startswith("code/rust/"):
                return None, None
            package = self.crates.package(path)
            if kind == "rust_test":
                filt = f" {leaf_of(item['symbol'])}" if item["symbol"] else ""
                stem = ""
                if path.startswith("code/rust/tests/") and path.count("/") == 3:
                    stem = f" --test {path.rsplit('/', 1)[-1][:-3]}"
                return f"cd code/rust && cargo test -p {package}{stem}{filt}", None
            return None, f"no test is cited for this symbol; its crate is {package}"
        return None, None

    # -- all items of a node
    def node_items(self, node: dict) -> tuple[list[dict], list[str], list[str]]:
        node_id = node["id"]
        merged: dict[tuple, dict] = {}
        order: list[tuple] = []

        def add(item: dict | None) -> None:
            if item is None:
                return
            key = (item["path"], item["symbol"])
            if key in merged:
                held = merged[key]
                held["cited_in"] = sorted(set(held["cited_in"]) | set(item["cited_in"]))
                held["counted"] = held["counted"] or item["counted"]
            else:
                merged[key] = item
                order.append(key)

        for field in ("lean", "rust", "source"):
            for ref in node.get(field, []):
                add(self.make_item(ref, f"node.{field}", True))
        absent: list[str] = []
        record_ids: list[str] = []
        for receipt in self.receipts:
            if receipt.get("dag_node") != node_id or receipt["exit_code"] != 0:
                continue
            tag = f"receipt {receipt['receipt_file']} ({receipt['module']})"
            add(self.make_item(receipt["path"], tag, True))
            for anchor in receipt["_anchors"]:
                add(self.make_item(f"{receipt['path']}::{anchor}", tag, True))
        for record in self.records_by_node.get(node_id, []):
            rid = record["id"]
            record_ids.append(rid)
            exclusive = sum(1 for n in record["existing_derivation_dag_ids"] if n in self.nodes) == 1
            tag = f"record {rid}" if exclusive else f"record {rid} (shared)"
            for field in ("lean4", "rust", "python"):
                for ref in record.get(field, []):
                    if ref.startswith("absent:"):
                        absent.append(f"{rid} {field}: {ref[len('absent:'):].strip()}")
                    else:
                        add(self.make_item(ref, tag, exclusive))
            paper = self.papers.get(rid)
            if paper:
                add(self.make_item(paper, tag, False))
        items = [merged[k] for k in order]
        for item in items:
            item["counts"] = bool(item["counted"] and item["resolution"] == "present" and not item["generated"])
        items.sort(key=lambda i: (KIND_GROUP[i["kind"]], i["path"], i["symbol"] or ""))
        return items, sorted(set(record_ids)), sorted(set(absent))


# ---------------------------------------------------------------- grading

def counted_present(items: list[dict]) -> list[dict]:
    return [i for i in items if i["counts"]]


def grade_node(items: list[dict], reviews: list[dict]) -> tuple[str, dict]:
    present = counted_present(items)
    code = [i for i in present if i["kind"] in CODE_KINDS and i["symbol"] and i["symbol_exists"]]
    lean = [i for i in code if i["kind"] == "lean_decl" and i["replay"] == "verified"
            and (i["symbol_declared"] or i["decl_listed"])]
    tests = [i for i in present if i["kind"] in ("rust_test", "python_test")]
    reviewed = [r for r in reviews if r["qualifies"]]
    code_files = {i["path"] for i in present if i["kind"] in ("rust_symbol", "python_symbol")}
    facts = {
        "cited_code_files_not_tests": len(code_files),
        "counted_files": len({i["path"] for i in present}),
        "symbols_found": len(code),
        "lean_receipt_backed": len(lean),
        "runnable_tests": len(tests),
        "qualifying_reviews": len(reviewed),
    }
    if not present:
        grade = "E0"
    elif not code:
        grade = "E1"
    elif not lean:
        grade = "E2"
    elif tests and reviewed:
        grade = "E4"
    else:
        grade = "E3"
    return grade, facts


def next_step(grade: str, facts: dict) -> str:
    if grade == "E0":
        return "cite at least one in-repo file that bears on the statement"
    if grade == "E1":
        return "cite a Lean, Rust or Python symbol that exists in an in-repo file"
    if grade == "E2":
        return ("replay a cited Lean declaration and record a receipt whose sha256 matches the current file "
                "(see docs/evidence/README.md, Verify it yourself)")
    if grade == "E3":
        missing = []
        if not facts["runnable_tests"]:
            missing.append("an in-repo Rust or Python runnable test "
                           f"({facts['cited_code_files_not_tests']} in-repo Rust or Python file(s) cited, none a test)")
        if not facts["qualifying_reviews"]:
            missing.append("a recorded statement-match review")
        return "add " + " and ".join(missing)
    return "none: all E4 conditions hold"


def descendants(nodes: dict[str, dict], routes: list[dict]) -> dict[str, int]:
    succ: dict[str, set[str]] = collections.defaultdict(set)
    indeg = {n: 0 for n in nodes}
    for route in routes:
        out = route["output"]
        for src in route["inputs"]:
            if src in nodes and out in nodes and out not in succ[src]:
                succ[src].add(out)
                indeg[out] += 1
    order, queue = [], [n for n, d in indeg.items() if d == 0]
    while queue:
        cur = queue.pop()
        order.append(cur)
        for nxt in succ[cur]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                queue.append(nxt)
    ids = sorted(nodes)
    index = {n: i for i, n in enumerate(ids)}
    mask: dict[str, int] = {}
    for node in reversed(order):
        bits = 0
        for nxt in succ[node]:
            bits |= mask[nxt] | (1 << index[nxt])
        mask[node] = bits
    return {n: bin(mask.get(n, 0)).count("1") for n in nodes}


def node_flags(node: dict, items: list[dict], grade: str, facts: dict) -> list[dict]:
    flags: list[dict] = []
    status = node["status"]
    present = counted_present(items)

    def flag(kind: str, detail: str) -> None:
        flags.append({"kind": kind, "detail": detail})

    own_lean = [i for i in items if i["kind"] == "lean_decl" and "node.lean" in i["cited_in"]]
    if status == "PROVED_LEAN":
        if GRADES.index(grade) < GRADES.index("E3"):
            in_repo = [i for i in own_lean if i["resolution"] == "present"]
            replays = collections.Counter(i["replay"] for i in in_repo)
            detail = (f"grade {grade}; {len(own_lean)} Lean reference(s) cited, {len(in_repo)} in this checkout"
                      + (f" (replay: {', '.join(f'{k} {v}' for k, v in sorted(replays.items()))})" if in_repo else ""))
            flag("proved_lean_below_e3", detail)
        if own_lean and not any(i["resolution"] == "present" for i in own_lean):
            flag("proved_lean_external_only",
                 f"all {len(own_lean)} cited Lean reference(s) lie outside this checkout")
    if status == "COMPUTATIONALLY_CHECKED" and not facts["runnable_tests"]:
        flag("computational_no_runnable_test",
             f"{len([i for i in present if i['kind'] in ('rust_symbol', 'python_symbol')])} in-repo Rust or Python "
             "symbol(s) cited, none a test")
    if status == "PROVED_PROSE" and not [i for i in present if i["kind"] == "paper"]:
        flag("proved_prose_no_in_repo_document", "no in-repo non-generated document among the counted sources")
    for item in items:
        if item["kind"] == "lean_decl" and item["replay"] in ("stale", "failed") and item["counted"]:
            flag("receipt_not_current",
                 f"{item['path']}: replay {item['replay']} against {len(item['receipts'])} receipt(s)")
    uncited = sorted({i["path"] for i in items
                      if any(c.startswith("receipt ") for c in i["cited_in"])
                      and not any(c.startswith("node.") for c in i["cited_in"])})
    for path in uncited:
        flag("receipt_names_uncited_module",
             f"a replay receipt names this node for {path}, but the node's lean, rust and source fields do not cite it")
    for item in items:
        if not item["counted"] or item["resolution"] == "external":
            continue
        if item["resolution"] == "missing":
            flag("broken_reference", f"path not found: {item['path']}")
        elif item["symbol"] and item["symbol_exists"] is False:
            flag("broken_reference", f"symbol {item['symbol']} not found in {item['path']}")
    return flags


# ---------------------------------------------------------------- the map

def build_map() -> tuple[dict, Builder]:
    b = Builder()
    dag = b.dag
    desc = descendants(b.nodes, dag["routes"])
    node_rows: list[dict] = []
    mismatches: list[dict] = []
    for node in dag["nodes"]:
        items, record_ids, absent = b.node_items(node)
        reviews = []
        pfp = pfp_review_of(node, b.files)
        if pfp:
            reviews.append(pfp)
        if node["id"] in b.frontier:
            reviews.append(b.frontier[node["id"]])
        grade, facts = grade_node(items, reviews)
        flags = node_flags(node, items, grade, facts)
        node_rows.append({
            "id": node["id"], "stage": node["stage"], "status": node["status"],
            "grade": grade, "facts": facts, "next_step": next_step(grade, facts),
            "dependents": desc[node["id"]],
            "flags": flags, "records": record_ids, "absent_notes": absent,
            "reviews": reviews, "items": items,
        })
        for f in flags:
            mismatches.append({"node": node["id"], "stage": node["stage"], "status": node["status"],
                               "grade": grade, "kind": f["kind"], "detail": f["detail"],
                               "dependents": desc[node["id"]]})
    rank = {k: i for i, k in enumerate(MISMATCH_ORDER)}
    mismatches.sort(key=lambda m: (rank[m["kind"]], -m["dependents"], m["node"], m["detail"]))
    files_table = {}
    for path in sorted(b.cited_files):
        info = b.files.info(path)
        if info:
            files_table[path] = {"sha256": info["sha256"], "sha256_basis": info["sha256_basis"], "size": info["size"]}
    receipts_public = [{k: v for k, v in r.items() if not k.startswith("_")} for r in b.receipts]
    summary = summarize(node_rows, mismatches, b)
    dag_info = b.files.info(DAG_REL)
    document = {
        "schema_version": SCHEMA,
        "authority_effect": "None",
        "generator": "dag/evidence/build_evidence.py",
        "dag": {"path": DAG_REL, "sha256_lf": dag_info["sha256_lf"],
                "nodes": len(dag["nodes"]), "routes": len(dag["routes"])},
        "allowed_axioms": list(ALLOWED_AXIOMS),
        "grade_rules": {
            "E0": "no counted in-repo evidence file",
            "E1": "at least one counted in-repo evidence file exists",
            "E2": "E1, and a cited Lean, Rust or Python symbol is found in its in-repo file (leaf rule)",
            "E3": "E2, and a cited Lean declaration lies in a file whose current sha256 equals a replay receipt "
                  "sha256 with exit code 0, a passed axiom audit and only standard axioms",
            "E4": "E3, plus an in-repo runnable Rust or Python test, plus a recorded statement-match review",
        },
        "receipts": receipts_public,
        "receipts_not_indexed": b.skipped_receipts,
        "files": files_table,
        "summary": summary,
        "mismatches": mismatches,
        "nodes": node_rows,
    }
    return document, b


def summarize(node_rows: list[dict], mismatches: list[dict], b: Builder) -> dict:
    grid = collections.Counter((r["status"], r["grade"]) for r in node_rows)
    by_status = collections.Counter(r["status"] for r in node_rows)
    by_grade = collections.Counter(r["grade"] for r in node_rows)
    by_stage_grade = collections.Counter((r["stage"], r["grade"]) for r in node_rows)
    decls: dict[tuple, dict] = {}
    pl_lean = collections.Counter()
    pl_nodes = collections.Counter()
    for row in node_rows:
        own = [i for i in row["items"] if i["kind"] == "lean_decl" and "node.lean" in i["cited_in"]]
        for item in own:
            if item["resolution"] == "present" and item["symbol"]:
                decls[(item["path"], item["symbol"])] = item
        if row["status"] == "PROVED_LEAN":
            pl_nodes["total"] += 1
            res = collections.Counter(i["resolution"] for i in own)
            for k, v in res.items():
                pl_lean[k] += v
            if res.get("present"):
                pl_nodes["with_in_repo_lean"] += 1
            if res.get("external_unresolved") or res.get("external") or res.get("missing"):
                pl_nodes["with_some_outside_lean"] += 1
            if own and not res.get("present"):
                pl_nodes["outside_lean_only"] += 1
    replay = collections.Counter(i["replay"] for i in decls.values())
    listed = sum(1 for i in decls.values() if i["replay"] == "verified" and i["decl_listed"])
    all_lean = collections.Counter()
    for row in node_rows:
        for item in row["items"]:
            if item["kind"] == "lean_decl" and "node.lean" in item["cited_in"] and item["symbol"]:
                all_lean[item["resolution"]] += 1
    declared_gap = sum(1 for row in node_rows for i in row["items"]
                       if i["counted"] and i["symbol"] and i["symbol_exists"] and not i["symbol_declared"]
                       and i["kind"] in CODE_KINDS)
    mismatch_kinds = collections.Counter(m["kind"] for m in mismatches)
    e3 = [r for r in node_rows if r["grade"] == "E3"]
    return {
        "e3_nodes_with_review": sum(1 for r in e3 if r["facts"]["qualifying_reviews"]),
        "e3_nodes_with_review_and_cited_code_but_no_test": sum(
            1 for r in e3 if r["facts"]["qualifying_reviews"] and r["facts"]["cited_code_files_not_tests"]),
        "e3_nodes_with_test_but_no_review": sum(
            1 for r in e3 if r["facts"]["runnable_tests"] and not r["facts"]["qualifying_reviews"]),
        "nodes": len(node_rows),
        "by_status": dict(sorted(by_status.items())),
        "by_grade": {g: by_grade.get(g, 0) for g in GRADES},
        "status_by_grade": {s: {g: grid.get((s, g), 0) for g in GRADES} for s in STATUS_ORDER},
        "stage_by_grade": {s: {g: by_stage_grade.get((s, g), 0) for g in GRADES}
                           for s in sorted({r["stage"] for r in node_rows})},
        "lean_declarations_in_repo": {
            "distinct": len(decls),
            "replay_verified": replay.get("verified", 0),
            "replay_verified_and_declaration_itemised": listed,
            "replay_stale": replay.get("stale", 0),
            "replay_failed": replay.get("failed", 0),
            "no_receipt": replay.get("none", 0),
        },
        "lean_references_cited_in_node_lean_fields": dict(sorted(all_lean.items())),
        "proved_lean_lean_references": dict(sorted(pl_lean.items())),
        "proved_lean_nodes": dict(sorted(pl_nodes.items())),
        "cited_symbols_found_but_no_declaration_form": declared_gap,
        "receipts_indexed": len(b.receipts),
        "mismatches_by_kind": {k: mismatch_kinds.get(k, 0) for k in MISMATCH_ORDER},
        "mismatches_total": len(mismatches),
        "mismatch_nodes": len({m["node"] for m in mismatches}),
    }


# ---------------------------------------------------------------- pages

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


def node_page(row: dict, node: dict, document: dict, rows_by_id: dict, routes_in: list, routes_out: list) -> str:
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
            f"- cited Lean declarations covered by a current replay receipt: {row['facts']['lean_receipt_backed']}",
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
                check = m["command"] if group != 0 else f"#print axioms {m['symbol']}"
                kind = "" if group == 0 else f" ({m['kind']})"
                out.append(f"| `{cell(m['symbol'])}`{kind} | {yes_no(m['counts'])} | {yes_no(m['symbol_exists'])} | "
                           f"{yes_no(m['symbol_declared'])} | {cell(audited)} | {('`' + cell(check) + '`') if check not in ('-', None) else '-'} |")
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
    out += route_lines(routes_in, "inputs", rows_by_id)[:cap]
    if len(routes_in) > cap:
        out.append(f"- ... and {len(routes_in) - cap} more in `dag/derivation_dag.json`")
    out += ["", f"Outgoing ({len(routes_out)}):", ""]
    out += route_lines(routes_out, "output", rows_by_id)[:cap]
    if len(routes_out) > cap:
        out.append(f"- ... and {len(routes_out) - cap} more in `dag/derivation_dag.json`")
    if not routes_in:
        out += ["", "No incoming route."]
    out.append("")
    return "\n".join(out)


def route_lines(routes: list[dict], end: str, rows_by_id: dict) -> list[str]:
    lines = []
    for route in sorted(routes, key=lambda r: r["id"]):
        ends = route[end] if isinstance(route[end], list) else [route[end]]
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
        shown = [leaf_of(s) for s in symbols[:3]]
        more = f" +{len(symbols) - 3}" if len(symbols) > 3 else ""
        parts.append(f"[{cell(path.rsplit('/', 1)[-1])}]({'../' * depth}{path})"
                     + (f": {', '.join('`' + s + '`' for s in shown)}{more}" if shown else ""))
    rest = len(by_file) - 4
    if rest > 0:
        parts.append(f"+{rest} more file(s)")
    return "<br>".join(parts) if parts else "none in this checkout"


def stage_page(stage: str, rows: list[dict], nodes: dict) -> str:
    grades = collections.Counter(r["grade"] for r in rows)
    statuses = collections.Counter(r["status"] for r in rows)
    out = [f"# Stage {stage}", "",
           "Part of the [evidence map](../README.md). AuthorityEffect: None.", "",
           f"Nodes: {len(rows)}. Grades: {counts_line(grades, GRADES)}. Statuses: {counts_line(statuses, STATUS_ORDER)}.", "",
           "| Node | Status | Grade | Statement | Counted in-repo evidence | Flags |",
           "|---|---|---|---|---|---|"]
    for row in rows:
        flags = ", ".join(sorted({f["kind"] for f in row["flags"]})) or "-"
        out.append(f"| [{row['id']}](../nodes/{row['id']}.md) | `{row['status']}` | {row['grade']} | "
                   f"{cell(nodes[row['id']]['statement'], 140)} | {evidence_cell(row['items'], 3)} | {cell(flags)} |")
    out.append("")
    return "\n".join(out)


def readme_page(document: dict, rows: list[dict], stage_order: list[str], toolchain: str, mathlib: str) -> str:
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
            f"{lean_decl['replay_stale']} are in files whose receipt no longer matches. "
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
            "declarations are itemised; the others rest on the module-level audit.",
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


def render_all() -> dict[str, str]:
    document, b = build_map()
    dag = b.dag
    rows = document["nodes"]
    rows_by_id = {r["id"]: r for r in rows}
    routes_in: dict[str, list] = collections.defaultdict(list)
    routes_out: dict[str, list] = collections.defaultdict(list)
    for route in dag["routes"]:
        routes_in[route["output"]].append(route)
        for src in route["inputs"]:
            routes_out[src].append(route)
    toolchain = b.files.text("lean4/lean-toolchain").strip()
    manifest = json.loads(b.files.text("lean4/lake-manifest.json"))
    mathlib = next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib")
    outputs: dict[str, str] = {}
    outputs[MAP_REL] = json.dumps(document, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
    outputs[f"{DOCS_REL}/README.md"] = readme_page(document, rows, list(dag["stages"]), toolchain, mathlib) + "\n"
    outputs[f"{DOCS_REL}/mismatches.md"] = mismatch_page(document) + "\n"
    by_stage = collections.defaultdict(list)
    for row in rows:
        by_stage[row["stage"]].append(row)
    for stage, stage_rows in by_stage.items():
        outputs[f"{DOCS_REL}/stages/{stage}.md"] = stage_page(stage, stage_rows, b.nodes) + "\n"
    for row in rows:
        outputs[f"{DOCS_REL}/nodes/{row['id']}.md"] = node_page(
            row, b.nodes[row["id"]], document, rows_by_id, routes_in[row["id"]], routes_out[row["id"]])
    return outputs


def existing_generated() -> set[str]:
    found = {p.relative_to(ROOT).as_posix() for p in (ROOT / DOCS_REL).rglob("*.md")}
    if (ROOT / MAP_REL).is_file():
        found.add(MAP_REL)
    return found


def read_text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def stale(outputs: dict[str, str]) -> list[str]:
    problems = []
    for rel, text in sorted(outputs.items()):
        path = ROOT / rel
        if not path.is_file():
            problems.append(f"missing: {rel}")
        elif read_text(rel) != text:
            problems.append(f"differs: {rel}")
    for rel in sorted(existing_generated() - set(outputs)):
        problems.append(f"unexpected: {rel}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    outputs = render_all()
    if args.write:
        for rel in sorted(existing_generated() - set(outputs)):
            (ROOT / rel).unlink()
        for rel, text in outputs.items():
            path = ROOT / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.is_file() or read_text(rel) != text:
                path.write_text(text, encoding="utf-8", newline="\n")
        summary = json.loads(outputs[MAP_REL])["summary"]
        print(f"evidence map written: {summary['nodes']} nodes, grades {summary['by_grade']}, "
              f"{summary['mismatches_total']} flags")
        return 0
    problems = stale(outputs)
    if problems:
        for line in problems[:20]:
            print(line)
        if len(problems) > 20:
            print(f"... and {len(problems) - 20} more")
        print("evidence map is stale: run python -I -X utf8 dag/evidence/build_evidence.py --write")
        return 1
    print("evidence map current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
