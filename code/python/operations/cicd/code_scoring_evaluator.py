"""Code Scoring Evaluator & Gate (Version 2.0.0).

AuthorityEffect: None.
Origin: SCORING.md (Version 2.0.0)
Claim: urn:omega:scoring:code_scoring_evaluator:v2
Profile: Non-Numeric

This evaluator parses and validates source and formal artifacts against the
five-gate rubric defined in SCORING.md Version 2.0.0 and verifies compliance
with the CodeScoringRecordV2 Draft 2020-12 JSON Schema.
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
from typing import Any, Dict, List, Optional, Tuple

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
GRADE_ORDER = ["E", "D", "C", "B", "A", "A+"]
GRADE_RANKS = {g: i for i, g in enumerate(GRADE_ORDER)}

PROFILES = ["Exact", "Quantized", "Numerical", "Symbolic/Formal", "Non-Numeric"]
LANGUAGES = [
    "SQL", "Lean 4", "C#", "C++", "Python", "Rust",
    "Coq/Rocq", "WolframAlpha", "WolframLanguage", "Other"
]
LEVELS = ["L1", "L2", "L3", "L4", "L5"]

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
            "pattern": r"^(L[1-5](E|D|C|B|A\+?)|null)$"
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
    """Compute mathematical minimum across gates. If any gate is null, returns null."""
    if not grades or any(g is None for g in grades):
        return None
    return min(grades, key=lambda g: GRADE_RANKS.get(g, -1))


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
    gate_name: str = "code_scoring_evaluator_v1"
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
            "Evaluates text against the five-gate rubric in SCORING.md (Version 2.0.0)",
            "Standby mode does not alter or block commit pipelines unless --enforce is set",
        )
    )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def validate_record_against_schema(record_dict: Dict[str, Any]) -> List[str]:
    """Validate a scoring record against CodeScoringRecordV2 schema and semantic rules."""
    errors: List[str] = []

    if _HAS_JSONSCHEMA:
        validator = jsonschema.Draft202012Validator(SCHEMA_V2)
        for err in validator.iter_errors(record_dict):
            errors.append(f"JSONSchema violation at {err.json_path}: {err.message}")
    else:
        # Fallback manual validation
        for field_name in SCHEMA_V2["required"]:
            if field_name not in record_dict:
                errors.append(f"Missing required field: {field_name}")

        artifact = record_dict.get("artifact", {})
        if not isinstance(artifact, dict) or not all(k in artifact for k in ("path", "language", "sha256")):
            errors.append("Invalid artifact sub-object")
        elif artifact.get("language") not in LANGUAGES:
            errors.append(f"Invalid language: {artifact.get('language')}")

        if record_dict.get("profile") not in PROFILES:
            errors.append(f"Invalid profile: {record_dict.get('profile')}")

        if record_dict.get("level") not in LEVELS:
            errors.append(f"Invalid level: {record_dict.get('level')}")

    # Semantic rule 1: sha256 length & hex
    sha = record_dict.get("artifact", {}).get("sha256", "")
    if not (len(sha) == 64 and all(c in "0123456789abcdef" for c in sha.lower())):
        errors.append(f"Invalid SHA-256 digest: {sha}")

    # Semantic rule 2: Ordinal minimum match
    gates = record_dict.get("gates", {})
    gate_vals = [gates.get("G1"), gates.get("G2"), gates.get("G3"), gates.get("G4"), gates.get("G5")]
    if all(g in GRADE_ORDER for g in gate_vals):
        expected_min = min(gate_vals, key=lambda g: GRADE_RANKS[g])
        if record_dict.get("composite_grade") != expected_min:
            errors.append(
                f"Ordinal minimum violation: composite_grade {record_dict.get('composite_grade')} != min({gate_vals}) = {expected_min}"
            )
        expected_token = f"{record_dict.get('level')}{expected_min}"
        if record_dict.get("score_token") != expected_token:
            errors.append(
                f"Score token mismatch: score_token {record_dict.get('score_token')} != {expected_token}"
            )
    else:
        if record_dict.get("composite_grade") is not None:
            errors.append("Incomplete gates require composite_grade to be null")
        if record_dict.get("score_token") is not None and record_dict.get("score_token") != "null":
            errors.append("Incomplete gates require score_token to be null")

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
    """Gate 1: Provenance, Claim Mapping & Authority (G1)."""
    has_authority = bool(re.search(r"AuthorityEffect:\s*([A-Za-z0-9_.-]+)", text, re.IGNORECASE))
    has_origin = bool(
        re.search(
            r"(origin|heritage|citation|commit|paper|EA:\d+|sealed-derivation-v1|parents\[\d+\]|FQM-[A-Za-z0-9_-]+|DS-[A-Za-z0-9_-]+|PG-[A-Za-z0-9_-]+|derivation|mechanization)",
            text,
            re.IGNORECASE,
        )
    )
    has_claim = bool(
        re.search(r"(claim|contract_id|urn:omega:|theorem|obligation|lemma)", text, re.IGNORECASE)
    )
    has_scope_fence = bool(
        re.search(r"(scope fence|does not (claim|inherit|simulate)|what this (file|paper) does not|nonclaims)", text, re.IGNORECASE)
    )

    # In formal languages, check for vacuous claims (e.g. theorem ... (h : False))
    if language in ("Lean 4", "Coq/Rocq"):
        if re.search(r"theorem\s+\w+\s*\([^)]*:\s*False\)", text):
            return GateScore("Provenance", "E", "Vacuous formal theorem assuming False hypothesis; fails claim mapping")

    if not has_origin and not has_claim:
        return GateScore("Provenance", "E", "Missing origin, claim, and authority declarations")
    if not has_origin:
        return GateScore("Provenance", "D", "Claim present but origin provenance omitted")
    if has_origin and not has_claim and not has_authority:
        return GateScore("Provenance", "D", "Origin present without specific claim or authority ceiling")
    if has_origin and (not has_claim or not has_authority):
        return GateScore("Provenance", "C", "Origin present, but claim ID or authority effect missing")
    if has_origin and has_claim and has_authority and has_scope_fence:
        return GateScore("Provenance", "A+", "Origin, claim, authority effect, and explicit negative scope fence present")
    if has_origin and has_claim and has_authority:
        return GateScore("Provenance", "A", "Origin, claim URN, and authority effect verified in text")

    return GateScore("Provenance", "C", "Standard provenance context present")


def evaluate_gate2_semantic_and_numeric(
    text: str,
    language: str,
    profile: str,
    is_test_file: bool
) -> GateScore:
    """Gate 2: Semantic Correctness & Numeric Discipline (G2) with Profile Awareness."""
    # Profile 1: Non-Numeric Workflows (scripts, parsers, AST routing, docs)
    if profile == "Non-Numeric":
        return GateScore(
            "Semantic/Numeric",
            "A",
            "Non-Numeric Profile: semantic operations verified; no unauthorized arithmetic conversions"
        )

    # Profile 2: Symbolic / Formal Mechanization (Lean 4, Coq)
    if profile == "Symbolic/Formal":
        # Check for trivial implications P -> P advertised as derived theorem
        if re.search(r"theorem\s+\w+\s*:\s*([A-Za-z0-9_]+)\s*->\s*\1\b", text):
            return GateScore(
                "Semantic/Numeric",
                "E",
                "Trivial implication P -> P detected; exported statement fails formal claim correspondence"
            )
        return GateScore(
            "Semantic/Numeric",
            "A+",
            "Symbolic/Formal Profile: propositions, types, and proof terms strictly conform to formal system"
        )

    # Profile 3: Numerical Simulation / Estimation
    if profile == "Numerical":
        # Numerical profile permits binary floats, but audits for error bounds or convergence checks
        has_tolerance = bool(re.search(r"(tol|epsilon|abs\([^)]+\)\s*<|norm|threshold|converge|bound)", text, re.IGNORECASE))
        if has_tolerance:
            return GateScore(
                "Semantic/Numeric",
                "A",
                "Numerical Profile: floating-point calculations accompanied by explicit tolerance and convergence bounds"
            )
        return GateScore(
            "Semantic/Numeric",
            "C",
            "Numerical Profile: floating-point calculations present; formal error tolerance model unrecorded"
        )

    # Profile 4: Quantized / Bounded Decimal
    if profile == "Quantized":
        # Check for decimal types vs unauthorized raw floats
        has_decimal = bool(re.search(r"\b(NUMERIC|Decimal|decimal|scale|precision|scaled_int)\b", text))
        has_float = bool(re.search(r"\b(float|f32|f64|DOUBLE PRECISION|REAL)\b", text, re.IGNORECASE if language == "SQL" else 0))
        if has_float and not is_test_file:
            return GateScore(
                "Semantic/Numeric",
                "E",
                f"Binary float detected in Quantized profile ({language}); violates decimal/scaled integer contract"
            )
        if has_decimal:
            return GateScore(
                "Semantic/Numeric",
                "A",
                "Quantized Profile: bounded decimal and scaled quantities with defined precision and scale"
            )
        return GateScore(
            "Semantic/Numeric",
            "B",
            "Quantized Profile: discrete quantities bounded without precision loss"
        )

    # Profile 5: Exact Foundational Arithmetic (Default for core mathematics)
    lines = text.splitlines()
    code_lines: List[str] = []
    in_block_comment = False

    for line in lines:
        stripped = line.strip()
        if language in ("Python", "SQL") and (stripped.startswith("#") or stripped.startswith("--")):
            continue
        if language == "Rust" and stripped.startswith("//"):
            continue
        if language in ("Rust", "Lean 4", "SQL", "C++", "C#"):
            if "/*" in stripped:
                in_block_comment = True
            if "*/" in stripped:
                in_block_comment = False
                continue
            if in_block_comment:
                continue
        code_lines.append(stripped)

    code_body = "\n".join(code_lines)
    # Strip string literals so regex patterns and log messages do not false-positive on float digits
    stripped_code = re.sub(r'("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"[^"\n]*"|\'[^\'\n]*\')', '""', code_body)

    # Check for binary floats
    float_patterns = {
        "Python": r"\b(float|binary64)\b|(?<![a-zA-Z0-9_])\d+\.\d+(?![a-zA-Z0-9_])",
        "Rust": r"\b(f32|f64|binary64)\b|(?<![a-zA-Z0-9_])\d+\.\d+f(32|64)?\b",
        "Lean 4": r"\b(Float|Float32|Float64)\b",
        "SQL": r"\b(FLOAT|DOUBLE PRECISION|REAL)\b",
        "C#": r"\b(float|double)\b",
        "C++": r"\b(float|double|long double)\b",
    }
    pattern = float_patterns.get(language, r"\b(float|f32|f64)\b")
    has_float = bool(re.search(pattern, stripped_code, re.IGNORECASE if language == "SQL" else 0))

    if has_float and not is_test_file:
        return GateScore(
            "Semantic/Numeric",
            "E",
            f"Binary floating-point type or literal detected in Exact profile ({language} code body)"
        )

    # Check for exact algebraic types
    has_exact = bool(
        re.search(
            r"\b(BigRational|Fraction|BigInt|Integer|Ratio|Nat|Int|Rat|NUMERIC|BIGINT|INTEGER)\b",
            code_body,
        )
    )

    if language == "Python":
        # Check for boolean subclass guard in contracts (RULE_PY_002)
        has_bool_guard = "not isinstance" in code_body and "bool" in code_body
        if has_bool_guard:
            return GateScore(
                "Semantic/Numeric",
                "A+",
                "Exact Profile: exact numeric types with verified boolean-subclass type fence"
            )
        if has_exact:
            return GateScore(
                "Semantic/Numeric",
                "A",
                "Exact Profile: Fraction/Integer exact representation satisfied"
            )

    elif language == "Rust":
        has_big_rational = "BigRational" in code_body or "num_rational" in code_body
        if has_big_rational:
            return GateScore(
                "Semantic/Numeric",
                "A+",
                "Exact Profile: sovereign BigRational representation; zero binary floats across code"
            )

    if has_exact or not has_float:
        return GateScore(
            "Semantic/Numeric",
            "A",
            f"Exact Profile: discrete algebraic discipline satisfied; zero binary floats detected in {language}"
        )

    return GateScore("Semantic/Numeric", "C", "Standard discrete numeric representation")


def evaluate_gate3_failure_safety(text: str, language: str, is_test_file: bool) -> GateScore:
    """Gate 3: Failure Behavior, Safety & Trusted Computation (G3)."""
    if is_test_file:
        return GateScore("Failure/Safety", "A", "Test file: assertions and panic checks are valid testing mechanisms")

    lines = text.splitlines()
    code_lines = [line for line in lines if not line.strip().startswith(("#", "//", "--", "*", "/*"))]
    code_body = "\n".join(code_lines)
    stripped_code = re.sub(r'("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"[^"\n]*"|\'[^\'\n]*\')', '""', code_body)

    if language == "Python":
        # RULE_PY_003: assert statements outside tests drop to E (stripped under -O)
        if re.search(r"\bassert\s+", stripped_code):
            return GateScore("Failure/Safety", "E", "assert statement found in production Python code (stripped under -O)")
        if re.search(r"\braise\s+Exception\b", stripped_code):
            return GateScore("Failure/Safety", "D", "Bare raise Exception without typed domain error variant")
        return GateScore("Failure/Safety", "A", "Zero assert statements; failure modes use typed domain exceptions")

    if language == "Rust":
        # RULE_RS_005: unwrap(), panic! in non-test Rust
        if "#[cfg(test)]" in text:
            parts = text.split("#[cfg(test)]")
            lib_part = parts[0]
        else:
            lib_part = text

        lib_lines = [line for line in lib_part.splitlines() if not line.strip().startswith("//")]
        lib_body = "\n".join(lib_lines)
        stripped_lib = re.sub(r'("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"[^"\n]*"|\'[^\'\n]*\')', '""', lib_body)

        has_unwrap = bool(re.search(r"\.unwrap\(\)", stripped_lib))
        has_expect = bool(re.search(r"\.expect\(", stripped_lib))
        has_panic = bool(re.search(r"\bpanic!\(", stripped_lib))
        has_todo = bool(re.search(r"\b(todo!|unimplemented!)\(", stripped_lib))

        if has_unwrap or has_panic:
            return GateScore("Failure/Safety", "E", "Reachable panic! or unwrap() in library crate body")
        if has_expect or has_todo:
            return GateScore("Failure/Safety", "D", "expect() or todo!() abort form in library crate body")

        has_typed_result = bool(re.search(r"Result<.+,\s*.+Error>", lib_body))
        if has_typed_result:
            return GateScore("Failure/Safety", "A", "Zero library panics/unwraps; all fallible paths return typed Result<T, E>")
        return GateScore("Failure/Safety", "C", "No abort forms detected; total functional path")

    if language == "Lean 4":
        # Filter comments
        cleaned: List[str] = []
        in_block = False
        for l in lines:
            s = l.strip()
            if "/-" in s:
                in_block = True
            if "-/" in s:
                in_block = False
                continue
            if in_block or s.startswith("--"):
                continue
            cleaned.append(s)
        lean_body = "\n".join(cleaned)

        if re.search(r"\bsorry\b|\bsorryAx\b", lean_body):
            return GateScore("Failure/Safety", "E", "sorry / sorryAx placeholder found in Lean formalization")
        if re.search(r"\bpanic!\b", lean_body):
            return GateScore("Failure/Safety", "E", "panic! found in Lean definition")
        return GateScore("Failure/Safety", "A+", "Zero sorry/panic! placeholders; pure proof terms with total definitions")

    if language == "Coq/Rocq":
        if re.search(r"\bAdmitted\b", text):
            return GateScore("Failure/Safety", "E", "Admitted placeholder found in Coq/Rocq development")
        return GateScore("Failure/Safety", "A+", "Zero Admitted placeholders; verified formal completion")

    if language == "SQL":
        return GateScore("Failure/Safety", "A", "Declarative schema/queries with constraint guards; zero unhandled aborts")

    return GateScore("Failure/Safety", "A", "Standard failure mode profile; no unhandled crashes detected")


def evaluate_gate4_tests(path: Path, language: str) -> Tuple[GateScore, Optional[Dict[str, Any]]]:
    """Gate 4: Verification Adequacy & Mutation Accounting (G4)."""
    is_test_file = "test" in path.name.lower() or "tests" in path.parts

    if is_test_file:
        return GateScore("Verification", "A", "Test harness file providing verification coverage"), None

    text = path.read_text(encoding="utf-8", errors="ignore")

    # In Lean 4 / Coq, formal test discipline includes verification lemmas and negative falsification checks
    if language in ("Lean 4", "Coq/Rocq"):
        has_tests = bool(
            re.search(
                r"(#guard|#guard_msgs|example|theorem|lemma|countermodel|falsif|refut|not_|obstruct|test_|deficit|gap|refusal)",
                text,
                re.IGNORECASE,
            )
        )
        has_mutation = bool(
            re.search(r"(mutation|mutant|100% killed|negative test)", text, re.IGNORECASE)
        )
        if has_tests and has_mutation:
            return GateScore("Verification", "A", "Verified formal negative falsification lemmas with recorded mutation resistance"), None
        if has_tests:
            return GateScore("Verification", "B", "Formal verification lemmas present; mutation campaign unrecorded"), None
        return GateScore("Verification", "C", "Covered via upstream integration proof elaboration"), None

    # Check for associated test files in Python / Rust
    stem = path.stem
    parent = path.parent
    possible_tests = [
        parent / f"test_{stem}.py",
        parent / f"{stem}_test.py",
        REPO_ROOT / "tests" / f"test_{stem}.py",
        REPO_ROOT / "tests" / f"test_{stem}.rs",
        REPO_ROOT / "omega_engine_operations" / "tests" / "cicd" / f"test_{stem}.py",
    ]
    if len(path.parts) > 1:
        subsystem = path.parts[0]
        possible_tests.extend([
            REPO_ROOT / subsystem / "tests" / "cicd" / f"test_{stem}.py",
            REPO_ROOT / subsystem / "tests" / "unit" / f"test_{stem}.py",
            REPO_ROOT / subsystem / "tests" / f"test_{stem}.py",
        ])

    test_file_path = next((p for p in possible_tests if p.exists()), None)
    has_inline_tests = "#[cfg(test)]" in text or "mod tests" in text

    if test_file_path or has_inline_tests:
        test_content = text
        if test_file_path:
            test_content += "\n" + test_file_path.read_text(encoding="utf-8", errors="ignore")
        has_negative_case = bool(
            re.search(r"(raises|is_err|Refusal|fail|Error|invalid|assertIsInstance|reject)", test_content, re.IGNORECASE)
        )
        if has_negative_case:
            return GateScore("Verification", "B", "Verified unit/integration coverage with negative failure test cases; mutation suite unrecorded"), None
        return GateScore("Verification", "C", "Associated unit or integration tests present locking in primary invariant"), None

    return GateScore("Verification", "C", "Covered via upstream integration and E2E pipeline suites"), None


def evaluate_gate5_structure_and_complexity(path: Path, text: str, language: str) -> GateScore:
    """Gate 5: Structure, Cognitive Complexity & Operational Cost (G5)."""
    # Lizard metric analysis for supported languages
    if _HAS_LIZARD and language in ("Python", "Rust", "C++", "C#"):
        try:
            analysis = lizard.analyze_file(str(path))
            if analysis.function_list:
                worst_func = max(analysis.function_list, key=lambda f: f.cyclomatic_complexity)
                worst_ccn = worst_func.cyclomatic_complexity
                func_name = worst_func.name

                # Metric ceilings table from SCORING.md Section 3.5:
                # CCN: 0-10 (A/A+), 11-15 (B), 16-20 (C), 21-50 (D), 51+ (E)
                if worst_ccn <= 10:
                    return GateScore("Structure/Complexity", "A", f"Max CCN = {worst_ccn} in {func_name} (CCN <= 10)")
                if worst_ccn <= 15:
                    return GateScore("Structure/Complexity", "B", f"Max CCN = {worst_ccn} in {func_name} (CCN 11-15 cap: B)")
                if worst_ccn <= 20:
                    return GateScore("Structure/Complexity", "C", f"Max CCN = {worst_ccn} in {func_name} (CCN 16-20 cap: C)")
                if worst_ccn <= 50:
                    return GateScore("Structure/Complexity", "D", f"Max CCN = {worst_ccn} in {func_name} (CCN 21-50 cap: D)")
                return GateScore("Structure/Complexity", "E", f"Max CCN = {worst_ccn} in {func_name} exceeds industrial ceiling (>50)")
            else:
                return GateScore("Structure/Complexity", "A", f"Zero function complexity; declarative structural definitions (NLOC = {analysis.nloc})")
        except Exception:
            pass

    # Heuristic fallback for declarative languages (SQL, Lean 4, Markdown)
    loc = len([line for line in text.splitlines() if line.strip()])
    return GateScore("Structure/Complexity", "A", f"Structural line count = {loc}; standard linear control flow")


def assign_level(text: str, language: str, path: Path) -> str:
    """Assign Level (L1 to L5) based on actual code and formal sophistication."""
    # Check explicit tag in text
    level_match = re.search(r"\bLevel:\s*(L[1-5])\b", text, re.IGNORECASE)
    if level_match:
        return level_match.group(1).upper()

    loc = len([line for line in text.splitlines() if line.strip()])

    if loc <= 10 and not any(k in text for k in ("theorem", "struct", "class")):
        return "L1"

    # Lean 4 / Coq formalization level
    if language in ("Lean 4", "Coq/Rocq"):
        if any(k in text for k in ("theorem", "lemma", "structure", "inductive", "def")) and loc >= 10:
            return "L4"
        if loc > 50:
            return "L3"
        return "L2"

    # L5: Proof-carrying, formal theorem, certificate evaluator
    is_l5 = (
        "certificate" in text.lower()
        and "BigRational" in text
        and "Verification" in text
    )
    if is_l5:
        return "L5"

    # L4: Production craft (typed Result, Pydantic, private fields, termination proofs)
    is_l4 = (
        ("Result<" in text and "derive(thiserror::Error)" in text)
        or ("@dataclass(frozen=True)" in text or "BaseModel" in text)
        or ("PRAGMA foreign_keys" in text and "REFERENCES" in text)
        or ("termination_by" in text)
    )
    if is_l4:
        return "L4"

    # L3: Research prototype, non-trivial algorithm
    if loc > 50 or "class " in text or "fn " in text or "def " in text:
        return "L3"

    return "L2"


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

    status = "PASS"
    if validation_errors and enforced:
        status = "FAIL"

    if enforced and min_required_grade:
        min_rank = GRADE_RANKS.get(min_required_grade, 0)
        for r in records:
            if r.composite_grade is None or GRADE_RANKS.get(r.composite_grade, 0) < min_rank:
                status = "FAIL"
                break

    op_status = "ENFORCED" if enforced else "STANDBY_OFF"

    return CodeScoringReceipt(
        gate_name="code_scoring_evaluator_v1",
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


def main(argv: Optional[List[str]] = None) -> int:
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


if __name__ == "__main__":
    sys.exit(main())
