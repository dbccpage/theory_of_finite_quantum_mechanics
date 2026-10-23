"""Create and audit conservative contracts for the code and Lean source scope.

This tool intentionally does *not* infer L4 certification from source shape,
file names, or the presence of a companion file.  Its baseline assessment is a
source-pinned coverage record: every in-scope artifact receives an identity and
scope contract plus an explicitly incomplete v2 score.  A later assessment can
append evidence-backed gate grades without losing this baseline or older
history.

The scope is all tracked or ordinary-untracked Python/Rust source below
``code/`` and Lean source below ``lean4/``.  Build/cache directories and sealed
run snapshots are excluded by an explicit rule recorded in the audit receipt.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Dict, Iterable, List, Optional, Tuple

try:
    import yaml
except ImportError as error:  # pragma: no cover - the repository toolchain has PyYAML
    raise SystemExit("PyYAML is required to read existing contract history") from error


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "tfqm.contract-score.v1"
BASELINE_ID = "source-coverage-baseline-v1"
AUDIT_PATH = ROOT / "evidence" / "contract_score_coverage_scope_audit.json"
SOURCE_SUFFIXES = {".py": "Python", ".rs": "Rust", ".lean": "Lean 4"}
PROFILES = {"Exact", "Quantized", "Numerical", "Symbolic/Formal", "Non-Numeric"}
GRADES = {"E", "D", "C", "B", "A", "A+"}
LEVELS = {"L1", "L2", "L3", "L4", "L5"}
EXCLUDED_PARTS = {"__pycache__", ".lake", "target", "node_modules"}
SEALED_PREFIXES = ("dag/results/", "dag/sealed_runs/", "sealed_runs/")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    # pathlib.Path.write_text gained its newline parameter after the Python 3.9
    # interpreter pinned by this repository, so write through open explicitly.
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    os.replace(temporary, path)


def changed_paths(ref: str) -> Tuple[str, set[str]]:
    """Files changed since ``ref``, plus ordinary untracked files.

    The comparison base is the merge base of ``ref`` and ``HEAD``. A missing
    merge base falls through to ``ref`` itself; a ref git cannot resolve then
    fails the diff rather than reporting an empty change.
    """
    try:
        base = subprocess.check_output(
            ["git", "merge-base", ref, "HEAD"],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
        ).decode("utf-8").strip()
    except subprocess.CalledProcessError:
        base = ref.strip()
    if not base:
        base = ref.strip()
    diff = subprocess.check_output(
        ["git", "diff", "--name-only", "--no-renames", "-z", base],
        cwd=ROOT,
    ).decode("utf-8")
    others = subprocess.check_output(
        ["git", "ls-files", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
    ).decode("utf-8")
    names: set[str] = set()
    for blob in (diff, others):
        for name in blob.split("\0"):
            if name:
                names.add(name.replace("\\", "/"))
    return base, names


def listed_source_names() -> List[str]:
    """In-scope source names from git, without stating each path."""
    raw = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
    ).decode("utf-8")
    result: List[str] = []
    for name in raw.split("\0"):
        if not name:
            continue
        normalized = name.replace("\\", "/")
        path = Path(normalized)
        if any(part in EXCLUDED_PARTS for part in path.parts):
            continue
        if normalized.startswith(SEALED_PREFIXES):
            continue
        in_code = normalized.startswith("code/") and path.suffix in {".py", ".rs"}
        in_lean = normalized.startswith("lean4/") and path.suffix == ".lean"
        if in_code or in_lean:
            result.append(normalized)
    return result


def source_paths() -> List[Path]:
    """Return the complete source population without depending on glob quirks."""
    result: List[Path] = []
    for name in listed_source_names():
        absolute = ROOT / name
        if absolute.is_file():
            result.append(absolute)
    return sorted(result, key=rel)


def sources_in_change(changed: set[str]) -> List[Path]:
    """Sources whose own path, or either companion spelling, is in ``changed``."""
    selected: List[Path] = []
    for name in listed_source_names():
        path = Path(name)
        companion_spellings = {
            path.with_name(path.stem + ".contract.score.yaml").as_posix(),
            name + ".contract.score.yaml",
        }
        if name not in changed and changed.isdisjoint(companion_spellings):
            continue
        absolute = ROOT / name
        if not absolute.is_file():
            continue
        if name in changed or rel(companion_for(absolute)) in changed:
            selected.append(absolute)
    return sorted(selected, key=rel)


def companion_for(source: Path) -> Path:
    # Historical companions are normally named from the stem.  That spelling
    # collides when a directory contains (for example) both ``module.py`` and
    # ``module.rs``.  Keep the historical file intact, but give *both* live
    # sources an extension-qualified active companion in that case.
    for suffix in SOURCE_SUFFIXES:
        sibling = source.with_suffix(suffix)
        if sibling != source and sibling.is_file():
            return source.with_name(source.name + ".contract.score.yaml")
    return source.with_name(source.stem + ".contract.score.yaml")


def parse_document(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        value = yaml.safe_load(text)
    if not isinstance(value, dict):
        raise ValueError("contract-score companion must be a mapping")
    return value


def language_for(source: Path) -> str:
    return SOURCE_SUFFIXES[source.suffix]


def profile_for(source: Path, text: str) -> str:
    """Select a preliminary profile while leaving semantic verification null."""
    if source.suffix == ".lean":
        return "Symbolic/Formal"
    lowered = text.lower()
    if any(token in lowered for token in ("numpy", "np.", "float", "f64", "f32", "decimal")):
        return "Numerical"
    if any(token in lowered for token in ("fraction", "bigrational", "bigint", "rational", "finfield")):
        return "Exact"
    return "Non-Numeric"


def role_for(source: Path) -> str:
    name = source.name.lower()
    parts = {part.lower() for part in source.parts}
    if name.startswith("test_") or "tests" in parts or "test" in name:
        return "test or verification harness"
    if source.stem in {"__init__", "lib", "mod"}:
        return "package or module entrypoint"
    if source.suffix == ".lean":
        return "Lean 4 formal source module"
    return "source module"


def source_artifact(record: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    artifact = record.get("artifact")
    if isinstance(artifact, dict):
        path = artifact.get("path")
        digest = artifact.get("sha256")
        return (path if isinstance(path, str) else None, digest if isinstance(digest, str) else None)
    path = record.get("subject")
    digest = record.get("source_sha256")
    return (path if isinstance(path, str) else None, digest if isinstance(digest, str) else None)


def history_entry(document: Dict[str, Any], kind: str, digest: Any) -> Optional[Dict[str, Any]]:
    if not isinstance(digest, str):
        return None
    for entry in document.get(kind, []):
        if isinstance(entry, dict) and entry.get("sha256") == digest:
            return entry
    return None


def append_history(document: Dict[str, Any], key: str, record: Dict[str, Any], label: str) -> str:
    raw = canonical_json(record)
    digest = sha256(raw.encode("utf-8"))
    history = document.setdefault(key, [])
    if not any(isinstance(entry, dict) and entry.get("sha256") == digest for entry in history):
        history.append(
            {
                "sha256": digest,
                "bytes": len(raw.encode("utf-8")),
                "record": record,
                "raw_utf8": raw,
                "original_paths": [label],
            }
        )
    return digest


def baseline_contract(source: Path, source_digest: str, language: str) -> Dict[str, Any]:
    source_name = rel(source)
    return {
        "schema_id": "tfqm.source-contract.v1",
        "contract_id": BASELINE_ID,
        "subject": source_name,
        "source_sha256": source_digest,
        "artifact": {"path": source_name, "sha256": source_digest, "language": language},
        "authority_effect": "None",
        "role": role_for(source),
        "purpose": "Pin this source artifact to the repository-wide contract-scoring population.",
        "operations": {
            "source_identity": "The exact source bytes identified by subject and source_sha256.",
            "scope_boundary": "This baseline establishes coverage and custody only; it does not certify semantics, safety, proof validity, or tests.",
        },
        "owned_invariants": [
            "The companion identifies one source path and its exact current SHA-256 digest.",
            "AuthorityEffect is None; no scientific, mathematical, or release authority is promoted.",
        ],
        "boundaries": [
            "No exported claim mapping, dependency audit, semantic review, failure review, or verification result is inferred from source shape.",
            "A completed engineering score requires evidence at the applicable public boundary under SCORING.md.",
        ],
        "evidence": [
            {"path": source_name, "sha256": source_digest},
            {"path": "SCORING.md", "sha256": sha256((ROOT / "SCORING.md").read_bytes())},
        ],
    }


def baseline_score(source: Path, source_digest: str, language: str, profile: str) -> Dict[str, Any]:
    source_name = rel(source)
    assert profile in PROFILES
    return {
        "schema_version": "2.0.0",
        "assessment_id": BASELINE_ID,
        "assessment_status": "incomplete_static_coverage_only",
        "AuthorityEffect": "None",
        "artifact": {"path": source_name, "sha256": source_digest, "language": language},
        "profile": profile,
        "profile_status": "preliminary static classification; Gate G2 remains unassessed and this is not a semantic profile certification",
        "level": "L1",
        "level_assessment": "provisional static lower bound only; no capability certification is claimed",
        "gates": {"G1": None, "G2": None, "G3": None, "G4": None, "G5": None},
        "composite_grade": None,
        "score_token": None,
        "is_complete": False,
        "grade_ceiling": "A+",
        "limiting_reason": "Only source identity and scope coverage were audited. All five SCORING.md gates require independent evidence.",
        "required_for_completion": [
            "G1 claim and provenance mapping",
            "G2 semantic and numeric discipline review",
            "G3 failure/trust-boundary review",
            "G4 boundary-appropriate proof or test receipt",
            "G5 language-appropriate structural and resource review",
        ],
        "rubric": {"path": "SCORING.md", "sha256": sha256((ROOT / "SCORING.md").read_bytes())},
        "evaluation_timestamp": "2026-10-21T00:00:00+00:00",
        "evidence": [{"path": source_name, "sha256": source_digest}],
    }


def new_document(source: Path) -> Dict[str, Any]:
    return {
        "schema_version": SCHEMA,
        "AuthorityEffect": "None",
        "artifact": rel(source),
        "contract": None,
        "current_contract": None,
        "current_scoring": None,
        "contract_history": [],
        "scoring_history": [],
        "legacy_paths": {},
        "history_order": "Import/append order; no missing assessment dates are invented.",
        "assurance": "Coverage baseline only; prior records are retained but not independently promoted.",
    }


def prepare_source(source: Path) -> bool:
    companion = companion_for(source)
    document = parse_document(companion) if companion.is_file() else new_document(source)
    if document.get("schema_version") != SCHEMA:
        raise ValueError("unexpected combined-document schema")
    for key in ("contract_history", "scoring_history"):
        if not isinstance(document.get(key), list):
            raise ValueError("malformed history: " + key)
    document.setdefault("legacy_paths", {})
    document["artifact"] = rel(source)
    document["AuthorityEffect"] = "None"
    source_digest = sha256(source.read_bytes())
    language = language_for(source)
    text = source.read_text(encoding="utf-8", errors="replace")
    contract = baseline_contract(source, source_digest, language)
    score = baseline_score(source, source_digest, language, profile_for(source, text))
    c_digest = append_history(document, "contract_history", contract, rel(companion) + "#coverage-contract")
    s_digest = append_history(document, "scoring_history", score, rel(companion) + "#coverage-score")
    changed = document.get("current_contract") != c_digest or document.get("current_scoring") != s_digest or document.get("contract") != contract
    document["contract"] = contract
    document["current_contract"] = c_digest
    document["current_scoring"] = s_digest
    document["history_order"] = "Import/append order; no missing assessment dates are invented."
    document["assurance"] = "Coverage baseline only; prior records are retained but not independently promoted."
    encoded = canonical_json(document)
    if not companion.is_file() or companion.read_text(encoding="utf-8") != encoded:
        atomic_write(companion, encoded)
        changed = True
    return changed


def valid_current_entry(entry: Optional[Dict[str, Any]]) -> Optional[str]:
    if not isinstance(entry, dict):
        return "missing current history entry"
    raw = entry.get("raw_utf8")
    if not isinstance(raw, str):
        return "history entry has no raw_utf8"
    raw_bytes = raw.encode("utf-8")
    if sha256(raw_bytes) != entry.get("sha256") or len(raw_bytes) != entry.get("bytes"):
        return "history entry bytes do not match its digest"
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        try:
            parsed = yaml.safe_load(raw)
        except yaml.YAMLError:
            return "history raw_utf8 is not parseable YAML/JSON"
    if parsed != entry.get("record"):
        return "history readable record differs from raw_utf8"
    return None


def score_error(score: Dict[str, Any], source_name: str, source_digest: str, language: str) -> Optional[str]:
    if score.get("schema_version") != "2.0.0":
        return "current score is not a v2 record"
    path, digest = source_artifact(score)
    if path != source_name or digest != source_digest:
        return "current score does not bind the current source bytes"
    artifact = score.get("artifact")
    if not isinstance(artifact, dict) or artifact.get("language") != language:
        return "current score has the wrong language"
    if score.get("profile") not in PROFILES or score.get("level") not in LEVELS:
        return "current score has an invalid profile or level"
    gates = score.get("gates")
    if not isinstance(gates, dict) or set(gates) != {"G1", "G2", "G3", "G4", "G5"}:
        return "current score lacks the five named gates"
    if any(value is not None and value not in GRADES for value in gates.values()):
        return "current score has an invalid gate grade"
    grade = score.get("composite_grade")
    token = score.get("score_token")
    if grade is not None and grade not in GRADES:
        return "current score has an invalid composite grade"
    if token is not None and (not isinstance(token, str) or len(token) < 3 or token[:2] not in LEVELS or token[2:] not in GRADES):
        return "current score has an invalid score token"
    if not isinstance(score.get("is_complete"), bool):
        return "current score has no completion flag"
    if score.get("grade_ceiling") not in GRADES:
        return "current score has an invalid grade ceiling"
    if not isinstance(score.get("evaluation_timestamp"), str):
        return "current score has no evaluation timestamp"
    if grade is None and token is not None:
        return "current score has a token without a composite grade"
    if grade is not None and (token is None or token[2:] != grade):
        return "current score token does not agree with its composite grade"
    if score["is_complete"] and (grade is None or token is None or any(value is None for value in gates.values())):
        return "completed score has an unassessed gate or no composite"
    return None


def audit_population(sources: Optional[List[Path]] = None) -> Tuple[Dict[str, Any], bool]:
    if sources is None:
        sources = source_paths()
    records: List[Dict[str, Any]] = []
    errors: List[Dict[str, str]] = []
    language_counts: Counter[str] = Counter()
    profile_counts: Counter[str] = Counter()
    twin_count = 0
    for source in sources:
        source_name = rel(source)
        source_digest = sha256(source.read_bytes())
        language = language_for(source)
        language_counts[language] += 1
        companion = companion_for(source)
        record: Dict[str, Any] = {
            "path": source_name,
            "sha256": source_digest,
            "language": language,
            "companion": rel(companion),
            "generated_governance_twin": source_name.startswith("code/python/governance/") and source.name.endswith("_contract.py"),
        }
        if record["generated_governance_twin"]:
            twin_count += 1
        try:
            if not companion.is_file():
                raise ValueError("missing companion")
            document = parse_document(companion)
            if document.get("schema_version") != SCHEMA:
                raise ValueError("wrong combined-document schema")
            c_entry = history_entry(document, "contract_history", document.get("current_contract"))
            s_entry = history_entry(document, "scoring_history", document.get("current_scoring"))
            for entry, kind in ((c_entry, "contract"), (s_entry, "score")):
                current_error = valid_current_entry(entry)
                if current_error:
                    raise ValueError(kind + " " + current_error)
            if c_entry is None or s_entry is None:
                raise ValueError("missing current history entry")
            contract = document.get("contract")
            if contract != c_entry.get("record"):
                raise ValueError("current contract view differs from current history")
            if not isinstance(contract, dict):
                raise ValueError("current contract is not a mapping")
            c_path, c_digest = source_artifact(contract)
            if c_path != source_name or c_digest != source_digest:
                raise ValueError("current contract does not bind current source bytes")
            score = s_entry.get("record")
            if not isinstance(score, dict):
                raise ValueError("current score is not a mapping")
            current_error = score_error(score, source_name, source_digest, language)
            if current_error:
                raise ValueError(current_error)
            profile_counts[score["profile"]] += 1
            record.update(
                {
                    "contract_digest": document["current_contract"],
                    "score_digest": document["current_scoring"],
                    "assessment_status": score.get("assessment_status"),
                    "score_token": score.get("score_token"),
                    "is_complete": score.get("is_complete"),
                    "valid": True,
                }
            )
        except (OSError, ValueError, TypeError, yaml.YAMLError) as error:
            detail = str(error)
            errors.append({"path": source_name, "error": detail})
            record.update({"valid": False, "error": detail})
        records.append(record)
    completed = sum(1 for item in records if item.get("is_complete") is True)
    audit = {
        "schema_version": "tfqm.contract-score-coverage-audit.v1",
        "authority_effect": "None",
        "assessment_id": BASELINE_ID,
        "population_rule": {
            "included": "tracked and ordinary-untracked *.py and *.rs under code/, and *.lean under lean4/",
            "excluded_parts": sorted(EXCLUDED_PARTS),
            "sealed_snapshot_prefixes": list(SEALED_PREFIXES),
            "source_discovery": "git ls-files --cached --others --exclude-standard -z followed by explicit path filtering",
        },
        "summary": {
            "sources": len(records),
            "valid_contracts_and_scores": len(records) - len(errors),
            "invalid_or_missing": len(errors),
            "by_language": dict(sorted(language_counts.items())),
            "by_preliminary_profile": dict(sorted(profile_counts.items())),
            "completed_scores": completed,
            "incomplete_scores": len(records) - completed,
            "generated_governance_twins": twin_count,
            "non_twin_sources": len(records) - twin_count,
        },
        "errors": errors,
        "artifacts": records,
        "scope_boundary": "This audit proves source-to-companion coverage and current-byte custody. It does not promote incomplete static assessments to engineering-grade certification.",
    }
    return audit, not errors


def write_audit(audit: Dict[str, Any], path: Path) -> None:
    atomic_write(path, canonical_json(audit))


def command_prepare(audit_path: Path) -> int:
    sources = source_paths()
    changed = 0
    for index, source in enumerate(sources, start=1):
        if prepare_source(source):
            changed += 1
        if index % 500 == 0 or index == len(sources):
            print("prepared {}/{}".format(index, len(sources)), flush=True)
    audit, passed = audit_population()
    write_audit(audit, audit_path)
    print(json.dumps({"prepared": len(sources), "changed_companions": changed, "audit": rel(audit_path), "passed": passed, "summary": audit["summary"]}, indent=2))
    return 0 if passed else 1


def command_check(audit_path: Path, sources: Optional[List[Path]] = None, scope_note: Optional[str] = None) -> int:
    audit, passed = audit_population(sources)
    payload: Dict[str, Any] = {
        "audit": rel(audit_path),
        "passed": passed,
        "summary": audit["summary"],
        "errors": audit["errors"],
    }
    if scope_note is None:
        write_audit(audit, audit_path)
    else:
        payload["audit"] = None
        payload["scope"] = scope_note
    print(json.dumps(payload, indent=2))
    return 0 if passed else 1


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "check"), help="prepare companions or audit them without source changes")
    parser.add_argument("--audit", type=Path, default=AUDIT_PATH, help="repository-relative or absolute audit JSON destination")
    parser.add_argument(
        "--changed-since",
        metavar="REF",
        help="with check: only in-scope sources added or edited since REF (merge base), plus ordinary untracked files. Does not write the audit file.",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    if args.changed_since and args.command != "check":
        parser.error("--changed-since is only valid with check")
    audit_path = args.audit if args.audit.is_absolute() else ROOT / args.audit
    try:
        audit_path.resolve().relative_to(ROOT.resolve())
    except ValueError:
        parser.error("--audit must stay inside the repository")
    if args.command == "prepare":
        return command_prepare(audit_path)
    if not args.changed_since:
        return command_check(audit_path)
    base, changed = changed_paths(args.changed_since)
    selected = sources_in_change(changed)
    note = (
        "in-scope sources changed since {} (merge base {}), including ordinary untracked files. "
        "The tracked audit file is not written. Grades are not read."
    ).format(args.changed_since, base[:12])
    return command_check(audit_path, selected, note)


if __name__ == "__main__":
    sys.exit(main())
