"""Independent finite behavior quotient checker for AUTH-RICE-THEOREM-IMPORT.

AuthorityEffect: None. A bounded table has decidable finite equivalence classes.
The recorded three-code table is checked without importing production code.
No infinite program semantics, universal machine or Rice theorem is derived.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checker_support.boundary import cli, evaluate, Violation
from checker_support.cases import Cases
from checker_support.domains import integer, sequence
from checker_support.outcome import Outcome

MAX_CODES = 64
MAX_CARRIER = 32


@dataclass(frozen=True, slots=True)
class FiniteBehaviorCarrier:
    """Immutable finite semantics aggregate, with one total row per code.

    Invariants: 1..64 codes, common carrier of 1..32 points, outputs in that
    carrier, exact integer tokens excluding bool. Rows are detached snapshots.
    """

    rows: tuple[tuple[int, ...], ...]

    def __post_init__(self) -> None:
        rows = sequence(self.rows, "behavior table", maximum=MAX_CODES)
        if not rows:
            raise Violation("input", "behavior table requires at least one code")
        first = sequence(rows[0], "behavior row", maximum=MAX_CARRIER)
        if not first:
            raise Violation("input", "behavior carrier must be nonempty")
        width = len(first)
        normalized = tuple(tuple(integer(value, "behavior output", 0, width-1)
                           for value in sequence(row, "behavior row", size=width, maximum=MAX_CARRIER))
                           for row in rows)
        object.__setattr__(self, "rows", normalized)

    def behavior(self, code: int, point: int) -> int:
        integer(code, "code", 0, len(self.rows)-1)
        integer(point, "carrier point", 0, len(self.rows[0])-1)
        return self.rows[code][point]

    def identity_bits(self) -> tuple[bool, ...]:
        identity = tuple(range(len(self.rows[0])))
        return tuple(row == identity for row in self.rows)

    def equivalence_classes(self) -> tuple[tuple[int, ...], ...]:
        """Stable first-code ordering; O(codes * carrier) expected hash work."""
        groups: dict[tuple[int, ...], list[int]] = {}
        for code, behavior in enumerate(self.rows):
            groups.setdefault(behavior, []).append(code)
        return tuple(tuple(codes) for codes in groups.values())

    def factor_property(self, bits: object) -> Outcome[tuple[bool, ...]]:
        """Descend a code predicate to behavior classes, or refuse a split class."""
        return evaluate(self._factor_property, bits)

    def _factor_property(self, bits: object) -> tuple[bool, ...]:
        values = sequence(bits, "property bits", size=len(self.rows), maximum=MAX_CODES)
        if any(type(value) is not bool for value in values):
            raise Violation("input", "property values must be bool, not integer flags")
        predicate = tuple(value is True for value in values)
        factored: list[bool] = []
        for codes in self.equivalence_classes():
            value = predicate[codes[0]]
            if any(predicate[code] != value for code in codes):
                raise Violation("check", "predicate is not constant on behavior equivalence classes")
            factored.append(value)
        return tuple(factored)


BEHAVIOR_TABLE = ((0, 1), (0, 1), (0, 0))
RECORDED_CARRIER = FiniteBehaviorCarrier(BEHAVIOR_TABLE)


def beh(code: int, index: int) -> int:
    return RECORDED_CARRIER.behavior(code, index)


def id_bit(code: int) -> bool:
    integer(code, "code", 0, len(BEHAVIOR_TABLE)-1)
    return RECORDED_CARRIER.identity_bits()[code]


def code_zero(code: int) -> bool:
    integer(code, "code", 0, len(BEHAVIOR_TABLE)-1)
    return code == 0


def check() -> int:
    run = Cases()
    for code, expected_row in enumerate(((0, 1), (0, 1), (0, 0))):
        for point, expected in enumerate(expected_row):
            run.require(beh(code, point) == expected, "recorded behavior entry")
        run.require(id_bit(code) == (code in (0, 1)), "recorded identity-table bit")
        run.require(code_zero(code) == (code == 0), "recorded code-zero bit")
    run.require(RECORDED_CARRIER.equivalence_classes() == ((0, 1), (2,)), "behavior quotient")
    factored = RECORDED_CARRIER.factor_property(tuple(id_bit(code) for code in range(3)))
    run.require(factored.ok and factored.value == (True, False), "identity property descends")
    refused = RECORDED_CARRIER.factor_property(tuple(code_zero(code) for code in range(3)))
    run.require(not refused.ok and refused.error is not None and refused.error.kind == "check",
                "code-zero property does not descend")
    print(f"auth-rice-theorem-import checks={run.checks} failures=0 codes=3 "
          "classes=2 id_true=2 code_zero_true=1 scope=finite_table authority=None")
    return 0


if __name__ == "__main__":
    raise SystemExit(cli(check))
