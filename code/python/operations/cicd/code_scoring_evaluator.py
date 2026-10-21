"""Code Scoring Evaluator & Gate (Version 2.0.0).

AuthorityEffect: None.
Origin: SCORING.md (Version 2.0.0)
Claim: urn:omega:scoring:code_scoring_evaluator:v2
Compatibility claim: urn:omega:scoring:grade-minimum-witness:v1
Scope Fence: grade_minimum_witness checks grade ordering only; the scanner does not certify source.
Profile: Non-Numeric
Mutation-Kills: 8 non-equivalent local witness mutants, executed by code/python/operations/cicd/test_scoring_control.py.
This count covers the legacy integer/order witness only, not the full static evaluator.

This evaluator records static observations and leaves unsupported gates null.
It does not execute source, tests or proofs. Complete externally reviewed
records can be validated against the CodeScoringRecordV2 Draft 2020-12 schema.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
import datetime
import hashlib
import json
from pathlib import Path
import re
import sys
import time
from typing import Any, Dict, List, Mapping, Optional, Tuple

try:
    import lizard  # type: ignore
    _HAS_LIZARD = True
except ImportError:
    _HAS_LIZARD = False

try:
    import jsonschema  # type: ignore
    _HAS_JSONSCHEMA = True
except ImportError:
    _HAS_JSONSCHEMA = False


def _find_repo_root(start: Path) -> Path:
    """Find repository root dynamically."""
    for parent in [start, *start.parents]:
        if (parent / ".git").exists() or (parent / "SCORING.md").exists():
            return parent
    return start.parents[3] if len(start.parents) > 3 else start


if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REPO_ROOT = _find_repo_root(Path(__file__).resolve())
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Scoring Constants (SCORING.md Version 2.0.0)
SCHEMA_VERSION = "2.0.0"
GRADE_ORDER: tuple[str, ...] = ("E", "D", "C", "B", "A", "A+")
GRADE_RANKS = {g: i for i, g in enumerate(GRADE_ORDER)}

PROFILES = ["Exact", "Quantized", "Numerical", "Symbolic/Formal", "Non-Numeric"]
LANGUAGES = [
    "SQL", "Lean 4", "C#", "C++", "Python", "Rust",
    "Coq/Rocq", "WolframAlpha", "WolframLanguage", "Other"
]
LEVELS = ["L1", "L2", "L3", "L4", "L5"]

class ScoringError(ValueError):
    """One violated scoring invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> ScoringError:
    return ScoringError(invariant, parameters)


def _require_int(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the scoring boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where an integer was required", role=role)
    if isinstance(value, int):
        return value
    raise _fail("value is not an integer", role=role, received=type(value).__name__)


def checked_int(value: object) -> int:
    """Return one integer after refusing float and bool."""
    return _require_int(value, "checked")


def _rank(grade: object) -> int:
    if not isinstance(grade, str) or grade not in GRADE_RANKS:
        raise _fail("grade is not on the scale", grade=str(grade))
    return GRADE_RANKS[grade]


def _minimum(grades: tuple[str, ...]) -> str:
    chosen = grades[0]
    for grade in grades[1:]:
        if _rank(grade) < _rank(chosen):
            chosen = grade
    return chosen


def grade_minimum_witness() -> int:
    """Return 0 when min(A+, A, B) is B and min(E, A+) is E."""
    high = min_grade(("A+", "A", "B"))
    low = min_grade(("E", "A+"))
    if high != "B":
        raise _fail("minimum of A+, A, B is not B", grade=high)
    if low != "E":
        raise _fail("minimum of E and A+ is not E", grade=low)
    if _rank("A") - _rank("E") != 4:
        raise _fail("rank gap from E to A is not 4", gap=_rank("A") - _rank("E"))
    if _rank("A+") - _rank("B") != 2:
        raise _fail("rank gap from B to A+ is not 2", gap=_rank("A+") - _rank("B"))
    return checked_int(0)


# Draft 2020-12 JSON Schema (from SCORING.md Section 6)
SCHEMA_V2: Dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://omega-engine.org/schemas/code-scoring-record.v2.json",
    "title": "CodeScoringRecordV2",
    "type": "object",
    "required": [
        "schema_version",
        "artifact",
        "profile",
        "level",
        "gates",
        "composite_grade",
        "score_token",
        "evaluation_timestamp"
    ],
    "properties": {
        "schema_version": {"type": "string", "const": "2.0.0"},
        "artifact": {
            "type": "object",
            "required": ["path", "language", "sha256"],
            "properties": {
                "path": {"type": "string"},
                "language": {
                    "type": "string",
                    "enum": LANGUAGES
                },
                "sha256": {"type": "string", "pattern": "^[a-f0-9]{64}$"}
            }
        },
        "profile": {
            "type": "string",
            "enum": PROFILES
        },
        "level": {
            "type": "string",
            "enum": LEVELS
        },
        "gates": {
            "type": "object",
            "required": ["G1", "G2", "G3", "G4", "G5"],
            "properties": {
                "G1": {"type": ["string", "null"], "enum": [*GRADE_ORDER, None]},
                "G2": {"type": ["string", "null"], "enum": [*GRADE_ORDER, None]},
                "G3": {"type": ["string", "null"], "enum": [*GRADE_ORDER, None]},
                "G4": {"type": ["string", "null"], "enum": [*GRADE_ORDER, None]},
                "G5": {"type": ["string", "null"], "enum": [*GRADE_ORDER, None]}
            }
        },
        "composite_grade": {
            "type": ["string", "null"],
            "enum": [*GRADE_ORDER, None]
        },
        "score_token": {
            "type": ["string", "null"],
            "pattern": r"^L[1-5](E|D|C|B|A\+?)$"
        },
        "is_complete": {"type": "boolean"},
        "grade_ceiling": {
            "type": "string",
            "enum": GRADE_ORDER
        },
        "evaluation_timestamp": {"type": "string", "format": "date-time"},
        "mutation_accounting": {
            "type": "object",
            "properties": {
                "killed": {"type": "integer", "minimum": 0},
                "survived": {"type": "integer", "minimum": 0},
                "demonstrably_equivalent": {"type": "integer", "minimum": 0},
                "invalid": {"type": "integer", "minimum": 0},
                "inconclusive": {"type": "integer", "minimum": 0},
                "unrun": {"type": "integer", "minimum": 0},
                "conservative_ratio": {"type": ["number", "null"], "minimum": 0.0, "maximum": 1.0}
            }
        }
    }
}


def min_grade(grades: List[Optional[str]]) -> Optional[str]:
    """Return the weakest known grade; an empty or incomplete assessment is null."""
    if isinstance(grades, (str, bytes)) or not isinstance(grades, (list, tuple)):
        raise _fail("grades are not a sequence", received=type(grades).__name__)
    for grade in grades:
        if grade is not None:
            _rank(grade)
    if not grades or any(g is None for g in grades):
        return None
    return _minimum(tuple(grades))


def grade_ceiling(grades: List[Optional[str]]) -> str:
    """Compute known grade ceiling from all evaluated non-null gates."""
    valid_grades = [g for g in grades if g is not None]
    if not valid_grades:
        return "A+"
    return min(valid_grades, key=lambda g: GRADE_RANKS.get(g, -1))


@dataclass(frozen=True)
class GateScore:
    """Evaluation result for an individual quality gate."""
    gate_name: str
    grade: Optional[str]
    rationale: str


@dataclass(frozen=True)
class FileScoreRecord:
    """Typed evaluation record for a single source or formal artifact."""
    path: str
    language: str
    profile: str
    level: str
    provenance: GateScore
    semantic_numeric: GateScore
    failure_safety: GateScore
    tests: GateScore
    complexity: GateScore
    composite_grade: Optional[str]
    score_token: Optional[str]
    grade_ceiling: str
    is_complete: bool
    limiting_reason: str
    sha256: str
    mutation_accounting: Optional[Dict[str, Any]] = None

    # Backwards-compatible aliases for v1 consumers
    @property
    def arithmetic(self) -> GateScore:
        return self.semantic_numeric

    @property
    def panics(self) -> GateScore:
        return self.failure_safety

    def to_schema_dict(self) -> Dict[str, Any]:
        """Convert to dictionary matching CodeScoringRecordV2 JSON Schema with backwards-compatible aliases."""
        d: Dict[str, Any] = {
            "schema_version": SCHEMA_VERSION,
            "artifact": {
                "path": self.path,
                "language": self.language,
                "sha256": self.sha256,
            },
            # Backwards-compatible top-level fields
            "path": self.path,
            "language": self.language,
            "profile": self.profile,
            "level": self.level,
            "level_assessment": "provisional static lower bound; manual capability review required",
            "gates": {
                "G1": self.provenance.grade,
                "G2": self.semantic_numeric.grade,
                "G3": self.failure_safety.grade,
                "G4": self.tests.grade,
                "G5": self.complexity.grade,
            },
            # Gate details with rationales for display/logging
            "provenance": asdict(self.provenance),
            "semantic_numeric": asdict(self.semantic_numeric),
            "arithmetic": asdict(self.semantic_numeric),  # v1 alias
            "failure_safety": asdict(self.failure_safety),
            "panics": asdict(self.failure_safety),  # v1 alias
            "tests": asdict(self.tests),
            "complexity": asdict(self.complexity),
            "composite_grade": self.composite_grade,
            "score_token": self.score_token,
            "is_complete": self.is_complete,
            "grade_ceiling": self.grade_ceiling,
            "limiting_reason": self.limiting_reason,
            "evaluation_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
        if self.mutation_accounting:
            d["mutation_accounting"] = self.mutation_accounting
        return d

    def to_markdown_table(self) -> str:
        """Render evaluation as a markdown table conforming to SCORING.md."""
        token_display = f"`{self.score_token}`" if self.score_token else "`null` (Incomplete)"
        grade_display = f"`{self.composite_grade}`" if self.composite_grade else f"`null` (Ceiling: `{self.grade_ceiling}`)"
        return (
            f"| Field | Value |\n"
            f"|---|---|\n"
            f"| **Path** | `{self.path}` |\n"
            f"| **Language** | `{self.language}` |\n"
            f"| **Profile** | `{self.profile}` |\n"
            f"| **Level** | `{self.level}` |\n"
            f"| **Gate 1 (Provenance)** | `{self.provenance.grade}` ({self.provenance.rationale}) |\n"
            f"| **Gate 2 (Semantic & Numeric)** | `{self.semantic_numeric.grade}` ({self.semantic_numeric.rationale}) |\n"
            f"| **Gate 3 (Failure & Safety)** | `{self.failure_safety.grade}` ({self.failure_safety.rationale}) |\n"
            f"| **Gate 4 (Verification & Tests)** | `{self.tests.grade}` ({self.tests.rationale}) |\n"
            f"| **Gate 5 (Structure & Complexity)** | `{self.complexity.grade}` ({self.complexity.rationale}) |\n"
            f"| **Grade** | {grade_display} |\n"
            f"| **Composite Score** | {token_display} |\n"
            f"| **Reason** | {self.limiting_reason} |"
        )


@dataclass(frozen=True)
class CodeScoringReceipt:
    """Typed machine receipt for CI/CD code scoring evaluation."""
    gate_name: str = "code_scoring_evaluator_v2"
    schema_version: str = SCHEMA_VERSION
    operational_status: str = "STANDBY_OFF"  # "STANDBY_OFF" (advisory) or "ENFORCED"
    enforced: bool = False
    status: str = "PASS"
    authority_effect: str = "None"
    files_evaluated: int = 0
    records: Tuple[Dict[str, Any], ...] = ()
    schema_validation_passed: bool = True
    validation_errors: Tuple[str, ...] = ()
    execution_time_sec: float = 0.0
    nonclaims: Tuple[str, ...] = field(
        default_factory=lambda: (
            "AuthorityEffect: None",
            "Static triage only: no tests, proofs, safety or provenance checks are executed",
            "Capability is a provisional L1 lower bound pending source review",
            "Standby mode does not alter or block commit pipelines unless --enforce is set",
        )
    )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def validate_record_against_schema(record_dict: Dict[str, Any]) -> List[str]:
    """Validate schema and grade consistency; unavailable validators fail closed."""
    if not isinstance(record_dict, dict):
        return ["A scoring record must be an object"]
    errors: List[str] = []
    if _HAS_JSONSCHEMA:
        validator = jsonschema.Draft202012Validator(SCHEMA_V2, format_checker=jsonschema.FormatChecker())
        errors.extend(f"JSONSchema violation at {err.json_path}: {err.message}"
                      for err in validator.iter_errors(record_dict))
    else:
        errors.append("Draft 2020-12 validation unavailable: install the jsonschema scoring dependency")
    timestamp = record_dict.get("evaluation_timestamp")
    try:
        if not isinstance(timestamp, str) or re.fullmatch(
                r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})", timestamp, re.IGNORECASE) is None:
            raise ValueError("timestamp is not an RFC3339 date-time")
        datetime.datetime.fromisoformat(timestamp.upper().replace("Z", "+00:00"))
    except ValueError:
        errors.append("Invalid evaluation_timestamp date-time")
    artifact = record_dict.get("artifact")
    gates = record_dict.get("gates")
    if not isinstance(artifact, dict) or not isinstance(gates, dict):
        return errors + ["artifact and gates must be objects"]
    sha = artifact.get("sha256")
    if not isinstance(sha, str) or re.fullmatch(r"[a-f0-9]{64}", sha) is None:
        errors.append("Invalid SHA-256 digest")
    values = [gates.get(key) for key in ("G1", "G2", "G3", "G4", "G5")]
    if any(key not in gates for key in ("G1", "G2", "G3", "G4", "G5")):
        errors.append("All five gates must be present")
    if any(value is not None and (not isinstance(value, str) or value not in GRADE_ORDER) for value in values):
        return errors + ["Gate values must be known grades or null"]
    complete = all(value is not None for value in values)
    expected = min_grade(values)
    if record_dict.get("composite_grade") != expected:
        errors.append("composite_grade must equal the five-gate minimum, or null when incomplete")
    token = f"{record_dict.get('level')}{expected}" if complete else None
    if record_dict.get("score_token") != token:
        errors.append("score_token must match the level and completed minimum, or be JSON null")
    if "is_complete" in record_dict and record_dict["is_complete"] is not complete:
        errors.append("is_complete disagrees with gate completeness")
    if "grade_ceiling" in record_dict and record_dict["grade_ceiling"] != grade_ceiling(values):
        errors.append("grade_ceiling disagrees with assessed gates")
    mutation = record_dict.get("mutation_accounting")
    if mutation is not None:
        outcomes = ("killed", "survived", "demonstrably_equivalent", "invalid", "inconclusive", "unrun")
        if not isinstance(mutation, dict) or any(type(mutation.get(key)) is not int or mutation[key] < 0 for key in outcomes):
            errors.append("Mutation accounting requires all six nonnegative integer outcome counts")
        else:
            total = sum(mutation[key] for key in outcomes)
            if "generated" in mutation and (type(mutation["generated"]) is not int or mutation["generated"] != total):
                errors.append("Mutation outcome counts do not conserve generated candidates")
            denominator = sum(mutation[key] for key in ("killed", "survived", "inconclusive", "unrun"))
            ratio = mutation["killed"] / denominator if denominator else None
            reported = mutation.get("conservative_ratio")
            if isinstance(reported, bool) or reported != ratio:
                errors.append("Conservative mutation ratio does not match eligible outcomes")
    return errors


def detect_language(path: Path) -> str:
    """Detect language from file suffix."""
    suffix = path.suffix.lower()
    if suffix == ".py":
        return "Python"
    if suffix == ".rs":
        return "Rust"
    if suffix == ".lean":
        return "Lean 4"
    if suffix == ".sql":
        return "SQL"
    if suffix == ".cs":
        return "C#"
    if suffix in (".cpp", ".hpp", ".cc", ".cxx", ".h"):
        return "C++"
    if suffix == ".v":
        return "Coq/Rocq"
    if suffix in (".wl", ".m", ".nb"):
        return "WolframLanguage"
    return "Other"


def detect_profile(path: Path, text: str, language: str) -> str:
    """Detect computational profile from explicit annotations or domain heuristics."""
    # Check explicit annotation in comments or metadata
    match = re.search(r"(?:profile|computational[-_]profile)\s*[:=]\s*([A-Za-z0-9_/ -]+)", text, re.IGNORECASE)
    if match:
        raw = match.group(1).strip()
        lower = raw.lower()
        if "exact" in lower:
            return "Exact"
        if "quantized" in lower:
            return "Quantized"
        if "numerical" in lower:
            return "Numerical"
        if "symbolic" in lower or "formal" in lower:
            return "Symbolic/Formal"
        if "non-numeric" in lower or "nonnumeric" in lower or "non_numeric" in lower:
            return "Non-Numeric"

    # Domain & Language Heuristics
    if language in ("Lean 4", "Coq/Rocq"):
        return "Symbolic/Formal"

    if language == "SQL":
        return "Quantized"

    path_str = str(path).lower().replace("\\", "/")

    # Non-Numeric documentation, tooling, or CI/CD
    if path.suffix.lower() in (".md", ".txt", ".json", ".yaml", ".yml", ".toml"):
        return "Non-Numeric"
    if any(k in path_str for k in ("operations/", "cicd/", "scripts/", "tools/", "governance/contracts/")):
        # If explicitly using BigRational or exact math in operations, make it Exact
        if "bigrational" in text.lower() or "exact_" in text.lower():
            return "Exact"
        return "Non-Numeric"

    # Numerical sweeps, simulations, Monte Carlo, or floating-point benchmarks
    if any(k in path_str for k in ("sweep", "simulation", "monte_carlo", "noise_mc", "benchmark")):
        return "Numerical"

    # Exact foundational core (crates, number theory, MUB, Majorana, rational arithmetic)
    return "Exact"


def evaluate_gate1_provenance(text: str, language: str) -> GateScore:
    """Source annotations alone do not establish provenance or claim mapping."""
    return GateScore("Provenance", None,
                     "Unassessed: source labels require source-pinned provenance and claim review.")


def evaluate_gate2_semantic_and_numeric(text: str, language: str, profile: str, is_test_file: bool) -> GateScore:
    """Record the selected profile without treating syntax as mathematical evidence."""
    return GateScore("Semantic/Numeric", None,
                     f"Unassessed: {profile} is a profile selection; semantics and domains require review.")


def evaluate_gate3_failure_safety(text: str, language: str, is_test_file: bool) -> GateScore:
    """Absence of abort keywords cannot establish complete failure behavior."""
    return GateScore("Failure/Safety", None,
                     "Unassessed: no checked failure-path, reachability or trusted-computation evidence supplied.")


def evaluate_gate4_tests(path: Path, language: str) -> Tuple[GateScore, Optional[Dict[str, Any]]]:
    """No test, compiler, proof checker or mutation campaign is executed here."""
    return GateScore("Verification", None,
                     "Unassessed: test names and mutation comments are not execution receipts."), None


def evaluate_gate5_structure_and_complexity(path: Path, text: str, language: str) -> GateScore:
    """A partial source metric is an observation, not a complete G5 assessment."""
    detail = "No supported complexity tool measurement available."
    if _HAS_LIZARD and language in ("Python", "Rust", "C++", "C#"):
        try:
            analysis = lizard.analyze_file(str(path))
            maximum = max((f.cyclomatic_complexity for f in analysis.function_list), default=0)
            detail = f"Lizard source CCN maximum = {maximum}."
        except Exception as error:
            detail = f"Complexity measurement failed: {type(error).__name__}."
    return GateScore("Structure/Complexity", None,
                     detail + " Unassessed: cognitive complexity, nesting, expanded code and operational costs need review.")


def assign_level(text: str, language: str, path: Path) -> str:
    """Return a provisional lower bound; keyword presence cannot certify capability."""
    return "L1"


def score_source_file(file_path: Path, profile_override: Optional[str] = None) -> FileScoreRecord:
    """Score a single source file across all five gates and return a typed record."""
    raw_bytes = file_path.read_bytes()
    sha256_hash = hashlib.sha256(raw_bytes).hexdigest()
    text = raw_bytes.decode(encoding="utf-8", errors="ignore")

    language = detect_language(file_path)
    profile = profile_override if profile_override in PROFILES else detect_profile(file_path, text, language)
    is_test = "test" in file_path.name.lower() or "tests" in file_path.parts

    provenance = evaluate_gate1_provenance(text, language)
    semantic_numeric = evaluate_gate2_semantic_and_numeric(text, language, profile, is_test)
    failure_safety = evaluate_gate3_failure_safety(text, language, is_test)
    tests, mutation = evaluate_gate4_tests(file_path, language)
    complexity = evaluate_gate5_structure_and_complexity(file_path, text, language)

    gate_grades = [
        provenance.grade,
        semantic_numeric.grade,
        failure_safety.grade,
        tests.grade,
        complexity.grade,
    ]
    composite_grade = min_grade(gate_grades)
    grade_ceil = grade_ceiling(gate_grades)
    is_complete = all(g is not None for g in gate_grades)
    level = assign_level(text, language, file_path)

    score_token = f"{level}{composite_grade}" if composite_grade is not None else None

    # Determine limiting gate reason
    all_gates = [provenance, semantic_numeric, failure_safety, tests, complexity]
    if composite_grade is not None:
        limiting_gates = [g for g in all_gates if g.grade == composite_grade]
        gate_name = limiting_gates[0].gate_name
        rationale = limiting_gates[0].rationale
        limiting_reason = f"Grade bounded by Gate ({gate_name}): {rationale}"
    else:
        unassessed = [g.gate_name for g in all_gates if g.grade is None]
        limiting_reason = f"Assessment incomplete; unassessed gates: {', '.join(unassessed)} (Ceiling: {grade_ceil})"

    try:
        repo_rel_path = file_path.resolve().relative_to(REPO_ROOT.resolve())
    except ValueError:
        repo_rel_path = file_path

    return FileScoreRecord(
        path=str(repo_rel_path).replace("\\", "/"),
        language=language,
        profile=profile,
        level=level,
        provenance=provenance,
        semantic_numeric=semantic_numeric,
        failure_safety=failure_safety,
        tests=tests,
        complexity=complexity,
        composite_grade=composite_grade,
        score_token=score_token,
        grade_ceiling=grade_ceil,
        is_complete=is_complete,
        limiting_reason=limiting_reason,
        sha256=sha256_hash,
        mutation_accounting=mutation,
    )


def evaluate_scoring_rubric(
    target_paths: List[Path],
    enforced: bool = False,
    min_required_grade: Optional[str] = None,
    profile_override: Optional[str] = None,
    validate_schema: bool = True,
) -> CodeScoringReceipt:
    """Run code scoring evaluator over the specified paths."""
    t0 = time.perf_counter()
    records: List[FileScoreRecord] = []
    validation_errors: List[str] = []

    for path in target_paths:
        if path.is_file():
            records.append(score_source_file(path, profile_override=profile_override))
        elif path.is_dir():
            for child in path.rglob("*"):
                if child.is_file() and child.suffix in (
                    ".py", ".rs", ".lean", ".sql", ".cs", ".cpp", ".hpp", ".v", ".md"
                ):
                    records.append(score_source_file(child, profile_override=profile_override))

    t1 = time.perf_counter()

    # Validate each record against Draft 2020-12 JSON Schema
    record_dicts = [r.to_schema_dict() for r in records]
    if validate_schema:
        for r_dict in record_dicts:
            errs = validate_record_against_schema(r_dict)
            if errs:
                validation_errors.extend([f"{r_dict['artifact']['path']}: {e}" for e in errs])

    if not records:
        validation_errors.append("No source artifacts were evaluated")
    for path in target_paths:
        if not path.exists():
            validation_errors.append(f"Missing target path: {path}")
    status = "PASS"
    if validation_errors and enforced:
        status = "FAIL"

    if min_required_grade is not None and min_required_grade not in GRADE_ORDER:
        raise ValueError("Unknown minimum grade")
    if enforced:
        min_rank = GRADE_RANKS[min_required_grade or "E"]
        for r in records:
            if r.composite_grade is None or GRADE_RANKS.get(r.composite_grade, 0) < min_rank:
                status = "FAIL"
                break

    op_status = "ENFORCED" if enforced else "STANDBY_OFF"

    return CodeScoringReceipt(
        gate_name="code_scoring_evaluator_v2",
        schema_version=SCHEMA_VERSION,
        operational_status=op_status,
        enforced=enforced,
        status=status,
        authority_effect="None",
        files_evaluated=len(records),
        records=tuple(record_dicts),
        schema_validation_passed=len(validation_errors) == 0,
        validation_errors=tuple(validation_errors),
        execution_time_sec=round(t1 - t0, 4),
    )


def evaluate_main(argv: Optional[List[str]] = None) -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="Code Scoring Evaluator & Gate (SCORING.md Version 2.0.0)"
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[REPO_ROOT / "SCORING.md"],
        help="Paths to files or directories to evaluate",
    )
    parser.add_argument(
        "--enforce",
        action="store_true",
        default=False,
        help="Enable strict gate enforcement mode (default is STANDBY_OFF)",
    )
    parser.add_argument(
        "--min-grade",
        type=str,
        default=None,
        choices=GRADE_ORDER,
        help="Minimum required grade under --enforce mode (e.g. B or A)",
    )
    parser.add_argument(
        "--profile",
        type=str,
        default=None,
        choices=PROFILES,
        help="Explicit computational profile override (Exact, Quantized, Numerical, Symbolic/Formal, Non-Numeric)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="Output raw JSON receipt conforming to CodeScoringRecordV2 Draft 2020-12 Schema",
    )
    args = parser.parse_args(argv)

    receipt = evaluate_scoring_rubric(
        target_paths=[p.resolve() for p in args.paths],
        enforced=args.enforce,
        min_required_grade=args.min_grade,
        profile_override=args.profile,
        validate_schema=True,
    )

    if args.json:
        print(json.dumps(receipt.to_dict(), indent=2))
        return 0 if receipt.status == "PASS" else 1

    print("\n" + "=" * 70)
    print("CODE SCORING EVALUATOR RECEIPT (Version 2.0.0)")
    print("=" * 70)
    print(f"Gate Status        : {receipt.status}")
    print(f"Operational Mode   : {receipt.operational_status} (enforced={receipt.enforced})")
    print(f"Files Evaluated    : {receipt.files_evaluated}")
    print(f"Schema Validation  : {'PASS' if receipt.schema_validation_passed else 'FAIL'}")
    print(f"Execution Time     : {receipt.execution_time_sec}s")
    print(f"AuthorityEffect    : {receipt.authority_effect}")
    print("=" * 70 + "\n")

    if receipt.validation_errors:
        print("Schema Validation Errors:")
        for err in receipt.validation_errors:
            print(f"  - {err}")
        print("\n" + "-" * 70 + "\n")

    for rec_dict in receipt.records:
        rec = FileScoreRecord(
            path=rec_dict["artifact"]["path"],
            language=rec_dict["artifact"]["language"],
            profile=rec_dict["profile"],
            level=rec_dict["level"],
            provenance=GateScore(**rec_dict["provenance"]),
            semantic_numeric=GateScore(**rec_dict["semantic_numeric"]),
            failure_safety=GateScore(**rec_dict["failure_safety"]),
            tests=GateScore(**rec_dict["tests"]),
            complexity=GateScore(**rec_dict["complexity"]),
            composite_grade=rec_dict["composite_grade"],
            score_token=rec_dict["score_token"],
            grade_ceiling=rec_dict["grade_ceiling"],
            is_complete=rec_dict["is_complete"],
            limiting_reason=rec_dict.get("limiting_reason", f"Composite: {rec_dict['score_token']}"),
            sha256=rec_dict["artifact"]["sha256"],
            mutation_accounting=rec_dict.get("mutation_accounting"),
        )
        print(rec.to_markdown_table())
        print("\n" + "-" * 70 + "\n")

    if not receipt.enforced:
        print("[NOTICE] Evaluator is in STANDBY_OFF mode. Results are advisory only.")

    return 0 if receipt.status == "PASS" else 1


def main(argv: Optional[List[str]] = None) -> int:
    """Keep the no-argument grade-minimum witness API; arguments run static triage."""
    if not argv:
        print(grade_minimum_witness())
        return 0
    return evaluate_main(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
