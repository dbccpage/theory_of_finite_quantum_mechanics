"""Create and audit conservative contracts for the code and Lean source scope.

This tool intentionally does *not* infer L4 certification from source shape,
file names, or the presence of a companion file.  Its baseline assessment is a
source-pinned coverage record: every in-scope artifact receives an identity and
scope contract plus an explicitly incomplete v2 score.  A later assessment can
append evidence-backed gate grades without losing this baseline or older
history.

The scope is the governed population declared in ``governance/policy.json``
(today: Python/Rust source below ``code/`` and Lean source below ``lean4/``,
tracked or ordinary-untracked).  Build/cache directories and sealed run
snapshots are excluded by the same policy; the rule is recorded in the audit
receipt.  Acceptance (completed score at L4 and grade D or better, with the
grandfather list ``governance/baseline.json``) is decided by ``governance-check``
in ``code/rust/src/governance``, not here.  A source listed in the baseline with unchanged bytes is still audited, but its defects are reported under ``grandfathered_errors`` and do not fail the check.

Commands: ``check`` (audit, read-only unless ``--write-audit``), ``prepare``
(write coverage baselines; never demotes a completed byte-bound score),
``population`` (print the governed paths) and ``record SOURCE --contract C
--score S`` (append an assessment to a companion and make it current).
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
# One source of truth: the population, exclusions, companion naming, schemas and
# grade vocabulary come from governance/policy.json, which the Rust governance
# crate (code/rust/src/governance) and every build.rs read too.
POLICY_PATH = ROOT / "governance" / "policy.json"
POLICY = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
SCHEMA = POLICY["companion"]["document_schema"]
COMPANION_SUFFIX = POLICY["companion"]["suffix"]
COLLISION_SUFFIXES = tuple(POLICY["companion"]["collision_suffixes"])
BASELINE_ID = "source-coverage-baseline-v1"
AUDIT_PATH = ROOT / "evidence" / "contract_score_coverage_scope_audit.json"
POPULATIONS = tuple((item["language"], tuple(item["globs"])) for item in POLICY["populations"])
SOURCE_SUFFIXES = {glob.rsplit("*", 1)[-1]: language for language, globs in POPULATIONS for glob in globs}
PROFILES = {"Exact", "Quantized", "Numerical", "Symbolic/Formal", "Non-Numeric"}
GRADES = set(POLICY["grade_order"])
LEVELS = set(POLICY["level_order"])
EXCLUDED_PARTS = set(POLICY["exclusions"]["path_parts"])
EXCLUDED_GLOBS = tuple(POLICY["exclusions"]["path_globs"])


def _wildcard(pattern, text, is_star, single) -> bool:
    """Same dynamic programme as governance::policy::wildcard: O(len(pattern) * len(text))."""
    row = [True] + [False] * len(text)
    for element in pattern:
        if is_star(element):
            seen, nxt = False, []
            for reached in row:
                seen = seen or reached
                nxt.append(seen)
            row = nxt
        else:
            row = [False] + [reached and single(element, item) for reached, item in zip(row, text)]
    return row[-1]


def glob_match(pattern: str, path: str) -> bool:
    """Same rule as governance::policy::glob_match: ``**`` spans whole components,
    ``*`` any run of characters within one component, ``?`` one character."""

    def component(pat: str, text: str) -> bool:
        return _wildcard(pat, text, lambda c: c == "*", lambda c, t: c == "?" or c == t)

    return _wildcard(pattern.split("/"), path.split("/"), lambda p: p == "**", component)


BASELINE_PATH = ROOT / "governance" / "baseline.json"
_BASELINE: Optional[Dict[str, Any]] = None


def baseline_entries() -> Dict[str, Any]:
    """The grandfather list governance/baseline.json, shared with governance-check."""
    global _BASELINE
    if _BASELINE is None:
        _BASELINE = json.loads(BASELINE_PATH.read_text(encoding="utf-8")).get("entries", {}) if BASELINE_PATH.is_file() else {}
    return _BASELINE


def grandfathered(normalized: str, digest: str) -> bool:
    """Listed in the baseline with exactly these bytes (the rule of governance-check)."""
    entry = baseline_entries().get(normalized)
    return isinstance(entry, dict) and entry.get("sha256") == digest


def exempt_without_companion(normalized: str, digest: str) -> bool:
    """Pinned boilerplate, or a grandfathered source, needs no companion of its own."""
    return pinned_boilerplate(normalized, digest) is not None or grandfathered(normalized, digest)


def pinned_boilerplate(normalized: str, digest: str) -> Optional[Dict[str, Any]]:
    """The policy pin admitting this exact file (for example the build.rs hook), if any."""
    for pin in POLICY["pinned_boilerplate"]:
        if glob_match(pin["glob"], normalized) and pin["sha256"] == digest:
            return pin
    return None


def population_language(normalized: str) -> Optional[str]:
    """The language of the policy population this repository-relative path is in, if any."""
    if any(part in EXCLUDED_PARTS for part in normalized.split("/")):
        return None
    if any(glob_match(glob, normalized) for glob in EXCLUDED_GLOBS):
        return None
    for language, globs in POPULATIONS:
        if any(glob_match(glob, normalized) for glob in globs):
            return language
    return None


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
        if population_language(normalized) is not None:
            result.append(normalized)
    return result


def source_paths() -> List[Path]:
    """Return the complete source population without depending on glob quirks."""
    result: List[Path] = []
    for name in listed_source_names():
        absolute = ROOT / name
        if absolute.is_file():
            result.append(absolute)
    return sorted(set(result), key=rel)


def sources_in_change(changed: set[str]) -> List[Path]:
    """Sources whose own path, or either companion spelling, is in ``changed``."""
    selected: List[Path] = []
    for name in listed_source_names():
        path = Path(name)
        companion_spellings = {
            path.with_name(path.stem + COMPANION_SUFFIX).as_posix(),
            name + COMPANION_SUFFIX,
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
    for suffix in COLLISION_SUFFIXES:
        sibling = source.with_suffix(suffix)
        if sibling != source and sibling.is_file():
            return source.with_name(source.name + COMPANION_SUFFIX)
    return source.with_name(source.stem + COMPANION_SUFFIX)


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
    language = population_language(rel(source))
    if language is None:
        raise ValueError("not in a governed population: " + rel(source))
    return language


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
    if pinned_boilerplate(rel(source), sha256(source.read_bytes())) is not None:
        return False  # admitted by exact bytes in governance/policy.json; no companion
    companion = companion_for(source)
    document = parse_document(companion) if companion.is_file() else new_document(source)
    if companion.is_file():
        try:
            current = validate_document(document, rel(source), sha256(source.read_bytes()), language_for(source))
        except (ValueError, TypeError, KeyError):
            current = None
        if current is not None and current.get("is_complete") is True:
            # Never demote a completed, byte-bound assessment to the coverage baseline.
            return False
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


def validate_document(document: Dict[str, Any], source_name: str, source_digest: str, language: str) -> Dict[str, Any]:
    """Return the current score record of a valid, byte-bound companion; raise ValueError otherwise."""
    if document.get("schema_version") != SCHEMA:
        raise ValueError("wrong combined-document schema")
    c_entry = history_entry(document, "contract_history", document.get("current_contract"))
    s_entry = history_entry(document, "scoring_history", document.get("current_scoring"))
    for entry, kind in ((c_entry, "contract"), (s_entry, "score")):
        current_error = valid_current_entry(entry)
        if current_error:
            raise ValueError(kind + " " + current_error)
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
    return score


def audit_population(sources: Optional[List[Path]] = None) -> Tuple[Dict[str, Any], bool]:
    if sources is None:
        sources = source_paths()
    records: List[Dict[str, Any]] = []
    errors: List[Dict[str, str]] = []
    grandfathered_errors: List[Dict[str, str]] = []
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
        pin = pinned_boilerplate(source_name, source_digest)
        if pin is not None:
            record.update({"valid": True, "assessment_status": "pinned_boilerplate", "template": pin["template"], "is_complete": None})
            records.append(record)
            continue
        try:
            if not companion.is_file():
                raise ValueError("missing companion")
            document = parse_document(companion)
            score = validate_document(document, source_name, source_digest, language)
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
            record.update({"valid": False, "error": detail})
            if grandfathered(source_name, source_digest):
                # Unchanged since governance/baseline.json: reported, not blocking.
                record["grandfathered"] = True
                grandfathered_errors.append({"path": source_name, "error": detail})
            else:
                errors.append({"path": source_name, "error": detail})
        records.append(record)
    completed = sum(1 for item in records if item.get("is_complete") is True)
    pinned = sum(1 for item in records if item.get("assessment_status") == "pinned_boilerplate")
    audit = {
        "schema_version": "tfqm.contract-score-coverage-audit.v1",
        "authority_effect": "None",
        "assessment_id": BASELINE_ID,
        "population_rule": {
            "policy": rel(POLICY_PATH),
            "included": {language: list(globs) for language, globs in POPULATIONS},
            "excluded_parts": sorted(EXCLUDED_PARTS),
            "excluded_globs": list(EXCLUDED_GLOBS),
            "source_discovery": "git ls-files --cached --others --exclude-standard -z followed by explicit path filtering",
        },
        "summary": {
            "sources": len(records),
            "valid_contracts_and_scores": len(records) - len(errors) - len(grandfathered_errors),
            "invalid_or_missing": len(errors) + len(grandfathered_errors),
            "invalid_but_grandfathered": len(grandfathered_errors),
            "blocking_errors": len(errors),
            "by_language": dict(sorted(language_counts.items())),
            "by_preliminary_profile": dict(sorted(profile_counts.items())),
            "completed_scores": completed,
            "pinned_boilerplate": pinned,
            "incomplete_scores": len(records) - completed - pinned,
            "generated_governance_twins": twin_count,
            "non_twin_sources": len(records) - twin_count,
        },
        "errors": errors,
        "grandfathered_errors": grandfathered_errors,
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


def command_check(audit_path: Path, write: bool, sources: Optional[List[Path]] = None, scope_note: Optional[str] = None) -> int:
    audit, passed = audit_population(sources)
    write = write and scope_note is None
    payload: Dict[str, Any] = {
        "audit": rel(audit_path) if write else None,
        "passed": passed,
        "summary": audit["summary"],
        "errors": audit["errors"],
    }
    if write:
        write_audit(audit, audit_path)
    if scope_note is not None:
        payload["scope"] = scope_note
    print(json.dumps(payload, indent=2))
    return 0 if passed else 1


def command_population() -> int:
    """Print the governed population, one path per line (CI compares it with governance-check list)."""
    for source in source_paths():
        print(rel(source))
    return 0


def load_record(path: Path) -> Dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(str(path) + " must hold a JSON object")
    return value


def command_record(source_arg: Path, contract_path: Path, score_path: Path) -> int:
    """Append a contract and a score record to a source's companion and make them current.

    Both records must bind the source's path and current SHA-256 (``artifact``).
    Earlier history is kept; nothing is graded here. ``governance-check explain``
    then reports whether the score meets the floor.
    """
    source = (source_arg if source_arg.is_absolute() else ROOT / source_arg).resolve()
    source_name, digest = rel(source), sha256(source.read_bytes())
    language = language_for(source)
    contract, score = load_record(contract_path), load_record(score_path)
    for kind, record in (("contract", contract), ("score", score)):
        path, bound = source_artifact(record)
        if path != source_name or bound != digest:
            raise SystemExit("{} record must bind {} at {} (found {} at {})".format(kind, source_name, digest, path, bound))
    problem = score_error(score, source_name, digest, language)
    if problem:
        raise SystemExit("score record rejected: " + problem)
    companion = companion_for(source)
    document = parse_document(companion) if companion.is_file() else new_document(source)
    label = rel(companion) + "#" + str(score.get("assessment_id", "assessment"))
    document["current_contract"] = append_history(document, "contract_history", contract, label)
    document["current_scoring"] = append_history(document, "scoring_history", score, label)
    document["contract"] = contract
    document["artifact"] = source_name
    document["assurance"] = "Current score recorded by score_scope_contracts.py record; grades are the assessor's, checked against SCORING.md by review."
    atomic_write(companion, canonical_json(document))
    print(json.dumps({"companion": rel(companion), "score_token": score.get("score_token"), "is_complete": score.get("is_complete")}))
    return 0


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "check", "population", "record"),
                        help="prepare companions, audit them, print the population, or record an assessment")
    parser.add_argument("source", nargs="?", type=Path, help="record: the source file")
    parser.add_argument("--audit", type=Path, default=AUDIT_PATH, help="repository-relative or absolute audit JSON destination")
    parser.add_argument("--write-audit", action="store_true", help="check: also rewrite the audit JSON (prepare always writes it)")
    parser.add_argument("--contract", type=Path, help="record: JSON contract record")
    parser.add_argument("--score", type=Path, help="record: JSON score record (SCORING.md v2.0.0)")
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
    if args.command == "population":
        return command_population()
    if args.command == "record":
        if args.source is None or args.contract is None or args.score is None:
            parser.error("record needs SOURCE --contract FILE --score FILE")
        return command_record(args.source, args.contract, args.score)
    if not args.changed_since:
        return command_check(audit_path, args.write_audit)
    base, changed = changed_paths(args.changed_since)
    selected = sources_in_change(changed)
    note = (
        "in-scope sources changed since {} (merge base {}), including ordinary untracked files. "
        "The tracked audit file is not written. Grades are not read."
    ).format(args.changed_since, base[:12])
    return command_check(audit_path, False, selected, note)


if __name__ == "__main__":
    sys.exit(main())
