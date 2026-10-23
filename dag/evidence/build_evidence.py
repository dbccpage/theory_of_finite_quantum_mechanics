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

This module is the model: it loads, resolves and grades, and returns one document
(build_map) that carries everything a page needs. dag/evidence/render_evidence.py
turns that document and the DAG statements into Markdown without reading any file.
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
for _dir in (HERE, Path(__file__).resolve().parent):  # python -I does not put the script directory on sys.path
    if str(_dir) not in sys.path:
        sys.path.insert(0, str(_dir))
from render_evidence import DOCS_REL, KIND_GROUP, STATUS_ORDER, render_pages  # noqa: E402
from validate_derivation_dag import line_ref_path, split_ref, symbol_leaf  # noqa: E402

DAG_REL = "dag/derivation_dag.json"
MAP_REL = "dag/evidence/evidence_map.json"
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
MISMATCH_ORDER = (
    "proved_lean_below_e3",
    "proved_lean_external_only",
    "receipt_not_current",
    "computational_no_runnable_test",
    "proved_prose_no_in_repo_document",
    "broken_reference",
    "receipt_names_uncited_module",
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

def split_citation(ref: str) -> tuple[str, str | None, str | None]:
    """path, symbol and the :line or #anchor tail of a citation, by the validator's own helpers."""
    raw, symbol = split_ref(ref)
    if ref.startswith(EXTERNAL_PREFIXES):
        return raw, symbol, None
    path = line_ref_path(raw)
    return path, symbol, raw[len(path):].lstrip(":#") or None


def is_outside(path: str) -> bool:
    top = path.split("/")[0]
    return top.startswith("omega_engine") or top == ".claude"


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
            top = data.get("results")
            # A campaign receipt can store the same module results at the top
            # level. An attempt record has no per-declaration axioms object.
            campaign = (
                isinstance(top, list) and bool(top)
                and all(isinstance(r, dict) and isinstance(r.get("axioms"), dict)
                        and "module" in r and "sha256" in r and r.get("exit_code") == 0
                        for r in top)
            )
            if campaign:
                meta = data
                results = top
            else:
                if isinstance(top, list) and data.get("lean_version"):
                    bad = any(isinstance(r, dict) and r.get("exit_code") not in (0, None) for r in top)
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
                "lean_version": meta.get("lean_version") or data.get("toolchain"),
                "toolchain": toolchain_of(meta.get("lean_version") or data.get("toolchain")),
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
    """The E3 rule as published: matching sha256, exit code 0, a passed axiom audit, standard axioms only.

    An absent audit flag is not a pass: the flag must be True.
    """
    return bool(
        sha_match
        and receipt.get("exit_code") == 0
        and receipt.get("axiom_audit_passed") is True
        and receipt.get("axioms_standard") is True)


def matching_names(symbol: str, names) -> list[str]:
    """Receipt names that denote the cited symbol: equal to it, or ending in '.' + symbol.

    One direction only. More than one match means the cited symbol is a bare leaf
    shared by several declarations; the caller must treat that as ambiguous.
    """
    return sorted(n for n in set(names) if n == symbol or n.endswith("." + symbol))


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
        path, symbol, where = split_citation(ref)
        item: dict = {
            "path": path, "symbol": symbol, "where": where,
            "cited_in": [cited_in], "counted": counted,
            "file_exists": False, "symbol_exists": None, "symbol_declared": None,
            "generated": False, "replay": "n/a", "receipts": [], "decl_listed": False, "decl_ambiguous": False,
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
            leaf = symbol_leaf(symbol)
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
            if symbol and rust_test_pattern(symbol_leaf(symbol)).search(self.files.text(path)):
                item["kind"] = "rust_test"
            elif not symbol and path.startswith("code/rust/tests/"):
                item["kind"] = "rust_test"
        elif kind == "python_symbol":
            if symbol:
                leaf = symbol_leaf(symbol)
                if is_test_file(path) and (leaf.startswith("test") or leaf.startswith("Test")
                                           or any(p.startswith("Test") for p in symbol.split("."))):
                    item["kind"] = "python_test"
            elif is_test_file(path):
                item["kind"] = "python_test"

    def _attach_receipts(self, item: dict, info: dict) -> None:
        rows = []
        symbol = item["symbol"]
        listed_axioms: set[str] = set()
        itemised = False
        for receipt in self.receipts_by_path.get(item["path"], []):
            sha_match = receipt["recorded_sha256"] in (info["sha256_raw"], info["sha256_lf"])
            hits = matching_names(symbol, [*receipt["_decl_axioms"], *receipt["_anchors"]]) if symbol else []
            ok = receipt_ok(receipt, sha_match)
            if ok and len(hits) == 1 and hits[0] in receipt["_decl_axioms"]:
                listed_axioms.update(receipt["_decl_axioms"][hits[0]])
                itemised = True
            rows.append({"id": receipt["id"], "sha_match": sha_match, "ok": ok,
                         "decl_listed": len(hits) == 1, "decl_ambiguous": len(hits) > 1})
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
        item["decl_ambiguous"] = not item["decl_listed"] and any(r["decl_ambiguous"] for r in verified)
        if itemised:
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
                filt = f" {symbol_leaf(item['symbol'])}" if item["symbol"] else ""
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


def descendant_counts(nodes: dict[str, dict], routes: list[dict]) -> dict[str, int]:
    """Unique descendants of each node. Acyclicity is checked by validate_derivation_dag.py, not here."""
    succ: dict[str, set[str]] = collections.defaultdict(set)
    for route in routes:
        for src in route["inputs"]:
            succ[src].add(route["output"])
    below: dict[str, set[str]] = {}

    def reach(node: str) -> set[str]:
        if node not in below:
            below[node] = set()  # a cycle adds nothing instead of recursing forever
            found: set[str] = set()
            for nxt in succ[node]:
                found |= {nxt} | reach(nxt)
            below[node] = found
        return below[node]

    return {n: len(reach(n)) for n in nodes}


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
    # A module is uncited when the receipt names it for this node but no node field cites ANY declaration in that file;
    # receipt anchors the node does not name individually are not a citation gap.
    node_paths = {i["path"] for i in items if any(c.startswith("node.") for c in i["cited_in"])}
    uncited = sorted({i["path"] for i in items if any(c.startswith("receipt ") for c in i["cited_in"])} - node_paths)
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

def build_map() -> dict:
    b = Builder()
    dag = b.dag
    desc = descendant_counts(b.nodes, dag["routes"])
    routes_in: dict[str, list] = collections.defaultdict(list)
    routes_out: dict[str, list] = collections.defaultdict(list)
    for route in dag["routes"]:
        routes_in[route["output"]].append({"id": route["id"], "status": route["status"], "nodes": route["inputs"]})
        for src in route["inputs"]:
            routes_out[src].append({"id": route["id"], "status": route["status"], "nodes": [route["output"]]})
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
            "routes": {"in": sorted(routes_in[node["id"]], key=lambda r: r["id"]),
                       "out": sorted(routes_out[node["id"]], key=lambda r: r["id"])},
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
    summary = summarize(node_rows, mismatches, len(b.receipts))
    dag_info = b.files.info(DAG_REL)
    manifest = json.loads(b.files.text("lean4/lake-manifest.json"))
    document = {
        "schema_version": SCHEMA,
        "authority_effect": "None",
        "generator": "dag/evidence/build_evidence.py",
        "dag": {"path": DAG_REL, "sha256_lf": dag_info["sha256_lf"],
                "nodes": len(dag["nodes"]), "routes": len(dag["routes"])},
        "allowed_axioms": list(ALLOWED_AXIOMS),
        "grades": list(GRADES),
        "mismatch_kinds": list(MISMATCH_ORDER),
        "stages": list(dag["stages"]),
        "lean": {"toolchain": b.files.text("lean4/lean-toolchain").strip(),
                 "mathlib_rev": next(x["rev"] for x in manifest["packages"] if x["name"] == "mathlib")},
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
    return document


def summarize(node_rows: list[dict], mismatches: list[dict], receipts_indexed: int) -> dict:
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
    listed = sum(1 for i in decls.values() if i["replay"] == "verified" and i["decl_axioms"] is not None)
    ambiguous = sum(1 for i in decls.values() if i["replay"] == "verified" and i["decl_ambiguous"])
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
            "replay_verified_with_ambiguous_receipt_name": ambiguous,
            "replay_stale": replay.get("stale", 0),
            "replay_failed": replay.get("failed", 0),
            "no_receipt": replay.get("none", 0),
        },
        "lean_references_cited_in_node_lean_fields": dict(sorted(all_lean.items())),
        "proved_lean_lean_references": dict(sorted(pl_lean.items())),
        "proved_lean_nodes": dict(sorted(pl_nodes.items())),
        "cited_symbols_found_but_no_declaration_form": declared_gap,
        "receipts_indexed": receipts_indexed,
        "mismatches_by_kind": {k: mismatch_kinds.get(k, 0) for k in MISMATCH_ORDER},
        "mismatches_total": len(mismatches),
        "mismatch_nodes": len({m["node"] for m in mismatches}),
    }


def render_all() -> dict[str, str]:
    document = build_map()
    statements = {n["id"]: n for n in load_json(DAG_REL)["nodes"]}
    outputs = render_pages(document, statements)
    outputs[MAP_REL] = json.dumps(document, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
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
