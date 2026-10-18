"""Exact minimum-grade certificate for the five-gate rubric.

Origin: SCORING.md section 1.2, The Fail-Closed Weakest Link Rule.
Claim: urn:omega:scoring:grade-minimum-witness:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/operations/cicd/test_scoring_control.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 8; AST Sonar cognitive complexity max 9; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 8.
Scope Fence: grade_minimum_witness checks the ordered minimum on the six
named grades. The file scanner reports text patterns and lizard cyclomatic
complexity. It does not prove that a scanned file meets L5A.
"""

from __future__ import annotations

import ast
import importlib
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence


GRADE_ORDER: tuple[str, ...] = ("E", "D", "C", "B", "A", "A+")
GRADE_RANKS: dict[str, int] = {grade: index for index, grade in enumerate(GRADE_ORDER)}


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


def min_grade(grades: Sequence[str]) -> str:
    """Return the weakest grade under the SCORING.md order."""
    if isinstance(grades, (str, bytes)) or not isinstance(grades, (list, tuple)):
        raise _fail("grades are not a sequence", received=type(grades).__name__)
    if len(grades) == 0:
        return "E"
    return _minimum(tuple(grades))


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


@dataclass(frozen=True)
class GateScore:
    """One gate grade and its rationale."""

    gate_name: str
    grade: str
    rationale: str


@dataclass(frozen=True)
class FileScoreRecord:
    """Typed evaluation record for a single source file."""

    path: str
    language: str
    level: str
    provenance: GateScore
    arithmetic: GateScore
    panics: GateScore
    tests: GateScore
    complexity: GateScore
    composite_grade: str
    score_token: str
    limiting_reason: str

    def to_markdown_table(self) -> str:
        """Render the record as a markdown table."""
        return "\n".join(_markdown_lines(self))


def _markdown_lines(record: FileScoreRecord) -> tuple[str, ...]:
    return (
        "| Field | Value |",
        "|---|---|",
        f"| **Path** | `{record.path}` |",
        f"| **Language** | `{record.language}` |",
        f"| **Level** | `{record.level}` |",
        f"| **Gate 1 (Provenance)** | `{record.provenance.grade}` ({record.provenance.rationale}) |",
        f"| **Gate 2 (Arithmetic)** | `{record.arithmetic.grade}` ({record.arithmetic.rationale}) |",
        f"| **Gate 3 (Panics)** | `{record.panics.grade}` ({record.panics.rationale}) |",
        f"| **Gate 4 (Tests)** | `{record.tests.grade}` ({record.tests.rationale}) |",
        f"| **Gate 5 (Complexity)** | `{record.complexity.grade}` ({record.complexity.rationale}) |",
        f"| **Grade** | `{record.composite_grade}` |",
        f"| **Composite Score** | `{record.score_token}` |",
        f"| **Reason** | {record.limiting_reason} |",
    )


@dataclass(frozen=True)
class CodeScoringReceipt:
    """Machine receipt for one scoring run."""

    gate_name: str = "code_scoring_evaluator_v1"
    operational_status: str = "STANDBY_OFF"
    enforced: bool = False
    status: str = "PASS"
    authority_effect: str = "None"
    files_evaluated: int = 0
    records: tuple[dict[str, object], ...] = ()
    execution_time_ns: int = 0
    nonclaims: tuple[str, ...] = (
        "AuthorityEffect: None",
        "Evaluates text against the five-gate rubric in SCORING.md",
        "Standby mode does not alter or block commit pipelines unless --enforce is set",
    )

    def to_dict(self) -> dict[str, object]:
        return {
            "gate_name": self.gate_name,
            "operational_status": self.operational_status,
            "enforced": self.enforced,
            "status": self.status,
            "authority_effect": self.authority_effect,
            "files_evaluated": self.files_evaluated,
            "records": self.records,
            "execution_time_ns": self.execution_time_ns,
            "nonclaims": self.nonclaims,
        }


def detect_language(path: Path) -> str:
    """Detect a rubric language from the file suffix."""
    suffix = path.suffix.lower()
    if suffix == ".py":
        return "Python"
    if suffix == ".rs":
        return "Rust"
    if suffix == ".lean":
        return "Lean 4"
    if suffix == ".sql":
        return "SQL"
    return "Unknown"


def _has_origin(text: str) -> bool:
    return "Origin:" in text


def _has_claim(text: str) -> bool:
    return "Claim:" in text


def _has_authority(text: str) -> bool:
    return "AuthorityEffect:" in text


def _has_fence(text: str) -> bool:
    return "Scope Fence:" in text


def evaluate_gate1_provenance(text: str) -> GateScore:
    """Score origin, claim, authority, and scope fence text."""
    if not _has_origin(text):
        return GateScore("Provenance", "E", "No origin declared")
    if not _has_claim(text) or not _has_authority(text):
        return GateScore("Provenance", "C", "Origin present, but claim ID or authority effect missing")
    if _has_fence(text):
        return GateScore("Provenance", "A+", "Origin, claim, authority effect, and scope fence present")
    return GateScore("Provenance", "A", "Origin, claim, and authority effect present")


def _parsed_python(text: str) -> ast.AST | None:
    try:
        return ast.parse(text)
    except SyntaxError:
        return None


def _tree_has_float(tree: ast.AST) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, float):
            return True
    return False


def _python_has_float(text: str) -> bool:
    tree = _parsed_python(text)
    if tree is None:
        return False
    return _tree_has_float(tree)


def _text_has_float(text: str, language: str) -> bool:
    if language == "Python":
        return _python_has_float(text)
    if language == "Rust":
        return "f32" in text or "f64" in text
    if language == "Lean 4":
        return "Float" in text
    if language == "SQL":
        return "FLOAT" in text or "DOUBLE PRECISION" in text or " REAL " in text
    return False


def evaluate_gate2_arithmetic(text: str, language: str) -> GateScore:
    """Score exact numeric text, with Python float constants refused."""
    if _text_has_float(text, language):
        return GateScore("Arithmetic", "E", f"Binary float text detected in {language}")
    if "isinstance" in text and "bool" in text:
        return GateScore("Arithmetic", "A", "Exact numeric text with a boolean-subclass guard")
    return GateScore("Arithmetic", "B", f"No binary float constant detected in {language}")


def _python_has_assert(text: str) -> bool:
    tree = _parsed_python(text)
    if tree is None:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            return True
    return False


def _rust_abort(text: str) -> str | None:
    if "panic!" in text or ".unwrap()" in text:
        return "panic or unwrap"
    if ".expect(" in text or "todo!" in text:
        return "expect or todo"
    return None


def _lean_abort(text: str) -> str | None:
    if "sorry" in text or "panic!" in text:
        return "sorry or panic"
    return None


def evaluate_gate3_panics(text: str, language: str, is_test_file: bool) -> GateScore:
    """Score reachable abort forms."""
    if is_test_file:
        return GateScore("Panics", "A", "Test harness")
    return _panic_grade(text, language)


def _panic_grade(text: str, language: str) -> GateScore:
    if language == "Python" and _python_has_assert(text):
        return GateScore("Panics", "E", "assert statement found in library code")
    if language == "Rust":
        return _named_abort(_rust_abort(text))
    if language == "Lean 4":
        return _named_abort(_lean_abort(text))
    return GateScore("Panics", "A", "No scanned abort form")


def _named_abort(name: str | None) -> GateScore:
    if name is None:
        return GateScore("Panics", "A", "No scanned abort form")
    return GateScore("Panics", "E", f"{name} found in library text")


def evaluate_gate4_tests(path: Path, text: str) -> GateScore:
    """Score the presence of a sibling mutation harness."""
    if "test_" in path.name:
        return GateScore("Tests", "A", "Test harness file")
    sibling = path.parent / f"test_{path.stem}.py"
    if sibling.is_file() and "Mutation-Kills:" in text:
        return GateScore("Tests", "A", "Sibling mutation harness recorded")
    if sibling.is_file():
        return GateScore("Tests", "B", "Sibling tests without a recorded kill count")
    return GateScore("Tests", "E", "No sibling test file")


def _lizard_module() -> object | None:
    try:
        return importlib.import_module("lizard")
    except ImportError:
        return None


def _analysis_functions(path: Path, module: object) -> tuple[object, ...] | None:
    analyze = getattr(module, "analyze_file", None)
    if not callable(analyze):
        return None
    try:
        analysis = analyze(str(path))
    except OSError:
        return None
    functions = getattr(analysis, "function_list", None)
    if not isinstance(functions, list):
        return None
    return tuple(functions)


def _worst_ccn(functions: tuple[object, ...]) -> int:
    worst = 0
    for function in functions:
        value = _require_int(getattr(function, "cyclomatic_complexity", None), "cyclomatic_complexity")
        if value > worst:
            worst = value
    return worst


def _measured_ccn(path: Path) -> int | None:
    module = _lizard_module()
    if module is None:
        return None
    functions = _analysis_functions(path, module)
    if functions is None:
        return None
    return _worst_ccn(functions)


def _ccn_grade(worst: int) -> str:
    if worst <= 10:
        return "A"
    if worst <= 15:
        return "B"
    if worst <= 20:
        return "C"
    if worst <= 50:
        return "D"
    return "E"


def evaluate_gate5_complexity(path: Path) -> GateScore:
    """Score lizard cyclomatic complexity."""
    worst = _measured_ccn(path)
    if worst is None:
        return GateScore("Complexity", "E", "Cyclomatic complexity was not measured")
    grade = _ccn_grade(worst)
    return GateScore("Complexity", grade, f"Max cyclomatic complexity = {worst}")


def assign_level(text: str) -> str:
    """Heuristic level tag. This is not a proof of L5."""
    if "urn:omega:" in text and "Scope Fence:" in text:
        return "L4"
    if "def " in text or "theorem " in text:
        return "L3"
    return "L2"


def _repo_root(start: Path) -> Path:
    for parent in (start, *start.parents):
        if (parent / "SCORING.md").is_file():
            return parent
    raise _fail("SCORING.md was not found", start=str(start))


def _relative_path(file_path: Path) -> str:
    root = _repo_root(file_path)
    if file_path.is_relative_to(root):
        return file_path.relative_to(root).as_posix()
    return file_path.as_posix()


def _gate_dict(gate: GateScore) -> dict[str, object]:
    return {"gate_name": gate.gate_name, "grade": gate.grade, "rationale": gate.rationale}


def _record_dict(record: FileScoreRecord) -> dict[str, object]:
    return {
        "path": record.path,
        "language": record.language,
        "level": record.level,
        "provenance": _gate_dict(record.provenance),
        "arithmetic": _gate_dict(record.arithmetic),
        "panics": _gate_dict(record.panics),
        "tests": _gate_dict(record.tests),
        "complexity": _gate_dict(record.complexity),
        "composite_grade": record.composite_grade,
        "score_token": record.score_token,
        "limiting_reason": record.limiting_reason,
    }


def _limiting_reason(record_gates: tuple[GateScore, ...], composite: str) -> str:
    for gate in record_gates:
        if gate.grade == composite:
            return f"Grade bounded by Gate ({gate.gate_name}): {gate.rationale}"
    return "Grade bounded by an unrecorded gate"


def score_source_file(file_path: Path) -> FileScoreRecord:
    """Score one source file across the five gates."""
    text = file_path.read_text(encoding="utf-8")
    language = detect_language(file_path)
    is_test = "test_" in file_path.name
    provenance = evaluate_gate1_provenance(text)
    arithmetic = evaluate_gate2_arithmetic(text, language)
    panics = evaluate_gate3_panics(text, language, is_test)
    tests = evaluate_gate4_tests(file_path, text)
    complexity = evaluate_gate5_complexity(file_path)
    gates = (provenance, arithmetic, panics, tests, complexity)
    composite = min_grade(tuple(gate.grade for gate in gates))
    level = assign_level(text)
    return FileScoreRecord(
        path=_relative_path(file_path),
        language=language,
        level=level,
        provenance=provenance,
        arithmetic=arithmetic,
        panics=panics,
        tests=tests,
        complexity=complexity,
        composite_grade=composite,
        score_token=f"{level}{composite}",
        limiting_reason=_limiting_reason(gates, composite),
    )


def _append_source(records: list[FileScoreRecord], child: Path) -> None:
    if child.is_file() and child.suffix in {".py", ".rs", ".lean", ".sql"}:
        records.append(score_source_file(child))


def _collect_dir(path: Path) -> tuple[FileScoreRecord, ...]:
    records: list[FileScoreRecord] = []
    for child in sorted(path.rglob("*")):
        _append_source(records, child)
    return tuple(records)


def _collect(path: Path) -> tuple[FileScoreRecord, ...]:
    if path.is_file():
        return (score_source_file(path),)
    if path.is_dir():
        return _collect_dir(path)
    raise _fail("path is not a file or directory", path=str(path))


def _collect_paths(paths: Sequence[Path]) -> tuple[FileScoreRecord, ...]:
    records: list[FileScoreRecord] = []
    for path in paths:
        records.extend(_collect(path))
    return tuple(records)


def _status(records: Sequence[FileScoreRecord], enforced: bool, minimum: str | None) -> str:
    if not enforced or minimum is None:
        return "PASS"
    floor = _rank(minimum)
    for record in records:
        if _rank(record.composite_grade) < floor:
            return "FAIL"
    return "PASS"


def evaluate_scoring_rubric(
    target_paths: Sequence[Path],
    enforced: bool = False,
    min_required_grade: str | None = None,
) -> CodeScoringReceipt:
    """Score the given files and return an integer-timed receipt."""
    if isinstance(target_paths, (str, bytes)) or not isinstance(target_paths, (list, tuple)):
        raise _fail("targets are not a sequence", received=type(target_paths).__name__)
    started = time.perf_counter_ns()
    records = _collect_paths(tuple(target_paths))
    elapsed = checked_int(time.perf_counter_ns() - started)
    status = _status(records, enforced, min_required_grade)
    mode = "ENFORCED" if enforced else "STANDBY_OFF"
    return CodeScoringReceipt(
        gate_name="code_scoring_evaluator_v1",
        operational_status=mode,
        enforced=enforced,
        status=status,
        authority_effect="None",
        files_evaluated=len(records),
        records=tuple(_record_dict(record) for record in records),
        execution_time_ns=elapsed,
    )


def _flag_value(argv: Sequence[str], flag: str) -> str | None:
    for index, item in enumerate(argv):
        if item == flag:
            return _value_after(argv, index, flag)
    return None


def _value_after(argv: Sequence[str], index: int, flag: str) -> str:
    if index + 1 >= len(argv):
        raise _fail("flag is missing a value", flag=flag)
    return argv[index + 1]


def _paths_from(argv: Sequence[str]) -> tuple[Path, ...]:
    skipped = False
    paths: list[Path] = []
    for item in argv:
        if item in {"--enforce", "--json"}:
            continue
        if item == "--min-grade":
            skipped = True
            continue
        if skipped:
            skipped = False
            continue
        if item.startswith("--"):
            raise _fail("flag is unknown", flag=item)
        paths.append(Path(item))
    return tuple(paths)


def _default_paths(paths: Sequence[Path]) -> tuple[Path, ...]:
    if len(paths) == 0:
        return (_repo_root(Path(__file__).resolve()) / "SCORING.md",)
    return tuple(paths)


def _print_receipt(receipt: CodeScoringReceipt, as_json: bool) -> None:
    if as_json:
        print(json.dumps(receipt.to_dict(), indent=2))
        return
    print(f"Gate Status        : {receipt.status}")
    print(f"Operational Mode   : {receipt.operational_status} (enforced={receipt.enforced})")
    print(f"Files Evaluated    : {receipt.files_evaluated}")
    print(f"Execution Time ns  : {receipt.execution_time_ns}")
    print(f"AuthorityEffect    : {receipt.authority_effect}")


def main(argv: Sequence[str] | None = None) -> int:
    """Print the grade-minimum certificate, then an optional file receipt."""
    sealed = grade_minimum_witness()
    if sealed != 0:
        print(sealed)
        return 1
    args = tuple(() if argv is None else argv)
    if len(args) == 0:
        print(sealed)
        return 0
    minimum = _flag_value(args, "--min-grade")
    receipt = evaluate_scoring_rubric(
        _default_paths(_paths_from(args)),
        enforced="--enforce" in args,
        min_required_grade=minimum,
    )
    _print_receipt(receipt, "--json" in args)
    if receipt.status == "PASS":
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main(tuple(sys.argv[1:])))
