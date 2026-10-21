"""One contract/scoring-history document per artifact, with exact legacy custody.

Old names are logical receipt addresses, never newly created files. RecordPath is
an opt-in adapter for existing quality tools; it does not patch pathlib globally.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
INDEX = "evidence/contract_score_migration/index.json"
SCHEMA = "tfqm.contract-score.v1"
LEGACY = re.compile(r"(?<!\.contract)\.(contract|scoring|score)\.(?:yaml|yml|yam)$")
SUFFIX = ".contract.score.yaml"
_cached_index = None


def sha(data):
    return hashlib.sha256(data).hexdigest()


def parse(text):
    value = yaml.load(text, Loader=yaml.CSafeLoader)
    if not isinstance(value, dict):
        raise ValueError("Contract/score must be a mapping")
    # Preserve YAML dates in the readable projection; exact types/bytes remain
    # available from raw_utf8 rather than being reconstructed from this view.
    return json.loads(json.dumps(value, default=str, allow_nan=False))


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def index():
    global _cached_index
    if _cached_index is None:
        p = ROOT / INDEX
        _cached_index = json.loads(p.read_text(encoding="utf-8"))["files"] if p.is_file() else {}
    return _cached_index


def source_for(path):
    path = Path(path)
    match = LEGACY.search(path.name)
    if not match:
        raise ValueError("Not a legacy contract/score name: " + str(path))
    base = path.with_name(path.name[:match.start()])
    candidates = [base, *[Path(str(base) + ext) for ext in (".rs", ".py", ".toml", ".lean")],
                  Path(str(base) + "_contract.py")]
    found = [p for p in candidates if p.is_file()]
    if len(found) > 1:
        raise ValueError("Ambiguous source: " + str(path))
    return found[0] if found else None


def canonical_path(path):
    path = Path(path)
    if path.name.endswith(SUFFIX):
        return path
    key = relative(path)
    if key in index():
        destination = (ROOT / index()[key]["combined_path"]).resolve()
        destination.relative_to(ROOT)  # reject an escaping index entry
        return destination
    source = source_for(path)
    if source:
        return source.with_name(source.stem + SUFFIX)
    base = LEGACY.sub("", path.name)
    base = re.sub(r"\.(rs|py|toml|lean)$", "", base)
    return path.with_name(base + SUFFIX)


def load(path):
    document = json.loads(Path(path).read_text(encoding="utf-8"))
    if document.get("schema_version") != SCHEMA:
        raise ValueError("Unknown combined document schema")
    return document


def empty(source):
    return {"schema_version": SCHEMA, "AuthorityEffect": "None", "artifact": relative(source) if source else None,
            "contract": None, "current_contract": None, "current_scoring": None,
            "contract_history": [], "scoring_history": [], "legacy_paths": {},
            "history_order": "Import/append order; no missing assessment dates are invented.",
            "assurance": "Storage migration only; imported grades and claims are not independently verified or promoted."}


def add(document, alias, data, kind):
    text = data.decode("utf-8")
    record = parse(text)
    digest = sha(data)
    history = document["contract_history" if kind == "contract" else "scoring_history"]
    entry = next((e for e in history if e["sha256"] == digest), None)
    if entry is None:
        entry = {"sha256": digest, "bytes": len(data), "record": record,
                 "raw_utf8": text, "original_paths": []}
        history.append(entry)
    if alias not in entry["original_paths"]:
        entry["original_paths"].append(alias)
    document["legacy_paths"][alias] = digest
    document["current_contract" if kind == "contract" else "current_scoring"] = digest
    if kind == "contract":
        document["contract"] = record


def save(path, document):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(document, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(text, encoding="utf-8", newline="\n")
    os.replace(temporary, path)


def archived_bytes(path, expected_sha256=None):
    key = relative(path)
    document = load(canonical_path(path))
    digest = expected_sha256 or document["legacy_paths"].get(key)
    for entry in document["contract_history"] + document["scoring_history"]:
        if entry["sha256"] == digest and key in entry["original_paths"]:
            data = entry["raw_utf8"].encode("utf-8")
            if sha(data) != digest or len(data) != entry["bytes"]:
                raise ValueError("Corrupt archived record: " + key)
            return data
    raise FileNotFoundError("No matching archived path/hash: " + key)


def read_bytes(path, expected_sha256=None):
    path = Path(path)
    if path.is_file():
        data = path.read_bytes()
        if expected_sha256 is None or sha(data) == expected_sha256:
            return data
    if LEGACY.search(path.name):
        return archived_bytes(path, expected_sha256)
    raise FileNotFoundError(str(path))


def write_legacy(path, data):
    """Append a writer's assessment/contract without recreating an old sidecar."""
    path = Path(path)
    destination = canonical_path(path)
    source = source_for(path)
    document = load(destination) if destination.is_file() else empty(source)
    add(document, relative(path), data, LEGACY.search(path.name)[1])
    save(destination, document)


def copy_file(source, destination):
    """Preserve old receipt-addressed bytes while creating only combined YAML."""
    if LEGACY.search(Path(source).name) or LEGACY.search(Path(destination).name):
        data = read_bytes(source)
        if LEGACY.search(Path(destination).name):
            write_legacy(destination, data)
        else:
            Path(destination).write_bytes(data)
        return destination
    return shutil.copyfile(source, destination)


class RecordPath(type(Path())):
    """Scoped logical view for old receipt names used by existing audit tools."""
    def read_bytes(self):
        return read_bytes(Path(self)) if LEGACY.search(self.name) else super().read_bytes()

    def read_text(self, encoding=None, errors=None, newline=None):
        if LEGACY.search(self.name):
            text = self.read_bytes().decode(encoding or "utf-8", errors or "strict")
            return text.replace("\r\n", "\n").replace("\r", "\n") if newline is None else text
        if newline is None:
            return super().read_text(encoding=encoding, errors=errors)
        return super().read_text(encoding=encoding, errors=errors, newline=newline)

    def is_file(self, **kwargs):
        if super().is_file(**kwargs):
            return True
        if LEGACY.search(self.name):
            try:
                archived_bytes(Path(self))
                return True
            except (FileNotFoundError, ValueError):
                return False
        return False

    def exists(self, **kwargs):
        return self.is_file(**kwargs) if LEGACY.search(self.name) else super().exists(**kwargs)

    def write_text(self, data, encoding=None, errors=None, newline=None):
        if LEGACY.search(self.name):
            if newline is not None:
                data = data.replace("\n", newline)
            write_legacy(Path(self), data.encode(encoding or "utf-8", errors or "strict"))
            return len(data)
        return super().write_text(data, encoding=encoding, errors=errors, newline=newline)

    def write_bytes(self, data):
        if LEGACY.search(self.name):
            write_legacy(Path(self), data)
            return len(data)
        return super().write_bytes(data)


def migrate(apply=False):
    files = [p for p in subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
             if p and LEGACY.search(p) and (ROOT / p).is_file()]
    if not files:
        if (ROOT / INDEX).is_file():
            check()
        return
    groups = defaultdict(list)
    plans = dict(index())
    inputs = {}
    for name in files:
        path = ROOT / name
        data = path.read_bytes()
        parse(data.decode("utf-8"))  # complete preflight before writing/deleting
        target = canonical_path(path)
        plans[name] = {"combined_path": relative(target), "sha256": sha(data), "bytes": len(data)}
        inputs[name] = plans[name]
        groups[target].append((name, data, LEGACY.search(name)[1], source_for(path)))
    print(json.dumps({"legacy_files": len(files), "combined_files": len(groups), "apply": apply}), flush=True)
    if not apply:
        return
    for target, entries in groups.items():
        sources = {source for _, _, _, source in entries if source is not None}
        if len(sources) > 1:
            raise ValueError("Multiple source artifacts would share " + str(target))
        document = load(target) if target.is_file() else empty(next(iter(sources), None))
        # Plain legacy .score is older fallback; explicit source .scoring is the
        # preferred current view, not an assertion of assessment chronology.
        entries.sort(key=lambda e: (e[2] == "scoring", ".rs.scoring." in e[0] or ".py.scoring." in e[0], e[0]))
        for alias, data, kind, _ in entries:
            add(document, alias, data, kind)
        save(target, document)
    # Bring known archived versions into the live artifact's history too. An
    # archive's claimed artifact path is used only if that source exists here;
    # no source or score is invented for standalone registry objects.
    live_histories = {}
    for entries in groups.values():
        for alias, data, kind, _ in entries:
            record = parse(data.decode("utf-8"))
            artifact = record.get("artifact", {})
            name = artifact.get("path") if isinstance(artifact, dict) else None
            if not isinstance(name, str) or not name.startswith("code/"):
                continue
            source = ROOT / name
            if not source.is_file():
                continue
            target = source.with_name(source.stem + SUFFIX)
            if target not in groups:
                continue
            document = live_histories.setdefault(target, load(target))
            old_contract, old_score, old_view = document["current_contract"], document["current_scoring"], document["contract"]
            add(document, alias, data, kind)
            document["current_contract"], document["current_scoring"], document["contract"] = old_contract, old_score, old_view
    for target, document in live_histories.items():
        save(target, document)
    global _cached_index
    index_path = ROOT / INDEX
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps({"schema_version": SCHEMA, "files": plans}, indent=2) + "\n", encoding="utf-8")
    _cached_index = plans
    # Verify exact reconstruction for EVERY input before deleting ANY input.
    for alias, reference in inputs.items():
        data = archived_bytes(ROOT / alias, reference["sha256"])
        if data != (ROOT / alias).read_bytes():
            raise ValueError("Migration byte mismatch: " + alias)
    for alias, reference in inputs.items():
        path = (ROOT / alias).resolve()
        path.relative_to(ROOT)
        if sha(path.read_bytes()) != reference["sha256"]:
            raise ValueError("Input changed during migration: " + alias)
        path.unlink()
    print("All original bytes verified; legacy files removed.", flush=True)


def check():
    errors = []
    versions = {}
    targets = {reference["combined_path"] for reference in index().values()}
    for name in subprocess.check_output(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT).decode().split("\0"):
        if name.endswith(SUFFIX):
            targets.add(name)
    for name in sorted(targets):
        try:
            target = (ROOT / name).resolve()
            target.relative_to(ROOT)
            document = load(target)
            for history in ("contract_history", "scoring_history"):
                seen = set()
                for entry in document[history]:
                    raw = entry["raw_utf8"].encode("utf-8")
                    if entry["sha256"] in seen:
                        raise ValueError("Duplicate history version")
                    seen.add(entry["sha256"])
                    if sha(raw) != entry["sha256"] or len(raw) != entry["bytes"]:
                        raise ValueError("Corrupt history bytes")
                    if json.dumps(parse(raw.decode("utf-8")), sort_keys=True) != json.dumps(entry["record"], sort_keys=True):
                        raise ValueError("Readable record differs from original bytes")
                    for alias in entry["original_paths"]:
                        versions[(name, alias, entry["sha256"])] = len(raw)
            contracts = {e["sha256"]: e["record"] for e in document["contract_history"]}
            if document["contract"] != contracts.get(document["current_contract"]):
                raise ValueError("Current contract view differs from history")
            if document["current_scoring"] is not None and not any(e["sha256"] == document["current_scoring"] for e in document["scoring_history"]):
                raise ValueError("Current score is absent from history")
        except (OSError, ValueError, KeyError) as exc:
            errors.append({"path": name, "error": str(exc)})
    for alias, reference in index().items():
        try:
            size = versions[(reference["combined_path"], alias, reference["sha256"])]
            if size != reference["bytes"]:
                raise ValueError("Length mismatch")
            if (ROOT / alias).is_file():
                raise ValueError("Legacy file still present")
        except (OSError, ValueError, KeyError) as exc:
            errors.append({"path": alias, "error": str(exc)})
    print(json.dumps({"originals": len(index()), "combined_files": len(targets), "all_passed": not errors, "errors": errors}, indent=2))
    if errors:
        raise SystemExit(1)


def export_v2(path_or_document):
    """Deterministically export active assessment as a canonical SCORING.md v2.0.0 record."""
    if isinstance(path_or_document, (str, Path)):
        doc = load(canonical_path(path_or_document))
    else:
        doc = path_or_document
    
    scoring_id = doc.get("current_scoring")
    if not scoring_id:
        raise ValueError("Document has no current_scoring assessment")
    
    entry = next((e for e in doc.get("scoring_history", []) if e["sha256"] == scoring_id), None)
    if not entry:
        raise ValueError(f"Current scoring digest {scoring_id} not found in history")
    
    record = entry["record"]
    contract = doc.get("contract") or {}
    
    art_path = doc.get("artifact") or record.get("artifact", {}).get("path")
    if isinstance(art_path, dict):
        rel_path = art_path.get("path", "")
    else:
        rel_path = str(art_path) if art_path else ""
    
    ext = Path(rel_path).suffix.lower()
    lang_map = {
        ".py": "Python",
        ".rs": "Rust",
        ".lean": "Lean 4",
        ".sql": "SQL",
        ".cs": "C#",
        ".cpp": "C++",
        ".cc": "C++",
        ".cxx": "C++",
        ".v": "Coq/Rocq",
        ".wl": "WolframLanguage",
        ".m": "WolframLanguage",
    }
    language = record.get("artifact", {}).get("language") or lang_map.get(ext, "Other")
    
    source_sha = record.get("artifact", {}).get("sha256")
    if not source_sha and rel_path and (ROOT / rel_path).is_file():
        source_sha = sha((ROOT / rel_path).read_bytes())
    if not source_sha:
        source_sha = "0" * 64
    
    profile = record.get("profile") or contract.get("profile", "Exact")
    level = record.get("level", "L2")
    gates_in = record.get("gates", {})
    gates = {
        "G1": gates_in.get("G1"),
        "G2": gates_in.get("G2"),
        "G3": gates_in.get("G3"),
        "G4": gates_in.get("G4"),
        "G5": gates_in.get("G5"),
    }
    
    composite_grade = record.get("composite_grade")
    score_token = record.get("score_token")
    if score_token == "null":
        score_token = None
    is_complete = record.get("is_complete", False)
    
    grade_ceiling = record.get("grade_ceiling")
    if not grade_ceiling:
        assessed = [g for g in gates.values() if g is not None]
        if assessed:
            ranks = {"E": 0, "D": 1, "C": 2, "B": 3, "A": 4, "A+": 5}
            grade_ceiling = min(assessed, key=lambda g: ranks.get(g, -1))
        else:
            grade_ceiling = "E"
    
    timestamp = record.get("evaluation_timestamp")
    if not timestamp:
        receipt_paths = [ev.get("path", "") for ev in record.get("evidence", []) if isinstance(ev, dict)]
        for rp in receipt_paths:
            m = re.search(r"(\d{8})T(\d{6})Z", rp)
            if m:
                d_str, t_str = m.group(1), m.group(2)
                timestamp = f"{d_str[:4]}-{d_str[4:6]}-{d_str[6:8]}T{t_str[:2]}:{t_str[2:4]}:{t_str[4:6]}+00:00"
                break
        if not timestamp:
            timestamp = "2026-10-20T22:00:00+00:00"
    
    v2 = {
        "schema_version": "2.0.0",
        "artifact": {
            "path": rel_path,
            "language": language,
            "sha256": source_sha,
        },
        "profile": profile,
        "level": level,
        "gates": gates,
        "composite_grade": composite_grade,
        "score_token": score_token,
        "is_complete": is_complete,
        "grade_ceiling": grade_ceiling,
        "evaluation_timestamp": timestamp,
    }
    
    mutation = record.get("mutation_accounting")
    if mutation:
        v2["mutation_accounting"] = mutation
    elif "mutation_outcomes" in record:
        outcomes = record["mutation_outcomes"]
        killed = outcomes.get("KILLED", outcomes.get("killed", 0))
        survived = outcomes.get("SURVIVED", outcomes.get("survived", 0))
        equiv = outcomes.get("EQUIVALENT", outcomes.get("demonstrably_equivalent", 0))
        invalid = outcomes.get("INVALID", outcomes.get("invalid", 0))
        inconc = outcomes.get("INCONCLUSIVE", outcomes.get("inconclusive", 0))
        unrun = outcomes.get("UNRUN", outcomes.get("unrun", 0))
        denom = killed + survived + inconc + unrun
        ratio = (killed / denom) if denom > 0 else None
        v2["mutation_accounting"] = {
            "killed": killed,
            "survived": survived,
            "demonstrably_equivalent": equiv,
            "invalid": invalid,
            "inconclusive": inconc,
            "unrun": unrun,
            "conservative_ratio": ratio,
        }
    
    return v2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("migrate", "check", "read", "hash", "export-v2"))
    parser.add_argument("path", nargs="?")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--sha256")
    args = parser.parse_args()
    if args.command == "migrate":
        migrate(args.apply)
    elif args.command == "check":
        check()
    elif args.command == "export-v2":
        if args.path is None:
            parser.error("path is required")
        print(json.dumps(export_v2(ROOT / args.path), indent=2))
    else:
        if args.path is None:
            parser.error("path is required")
        data = read_bytes(ROOT / args.path, args.sha256)
        if args.command == "hash":
            print(sha(data))
        else:
            sys.stdout.buffer.write(data)


if __name__ == "__main__":
    main()
