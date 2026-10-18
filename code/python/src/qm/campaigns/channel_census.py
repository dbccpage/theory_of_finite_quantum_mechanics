"""Census of classical channels by exact column sums.

Origin: code/python/src/qm/campaigns/channel_census.py
Claim: urn:omega:fqm:qm:classical-channel-census:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 5; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: A channel is counted when every column sums to 1 over Q.
This census is classical, not a CPTP classification. The locked count is 2.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_COUNT = 2


class ChannelCensusError(Exception):
    """One violated channel invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> ChannelCensusError:
    return ChannelCensusError(invariant, parameters)


def _require_fraction(value: object, role: str) -> Fraction:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


def _require_rows(matrix: object) -> tuple[object, ...]:
    if isinstance(matrix, (str, bytes)):
        raise _fail("a classical channel must be a nonempty tuple", received=type(matrix).__name__)
    if not isinstance(matrix, tuple):
        raise _fail("a classical channel must be a nonempty tuple", received=type(matrix).__name__)
    if len(matrix) == 0:
        raise _fail("a classical channel must be a nonempty tuple", received=type(matrix).__name__)
    return matrix


def _parse_row(row: object) -> tuple[Fraction, ...]:
    if isinstance(row, (str, bytes)):
        raise _fail("channel row is not a tuple", received=type(row).__name__)
    if not isinstance(row, tuple):
        raise _fail("channel row is not a tuple", received=type(row).__name__)
    parsed: list[Fraction] = []
    for entry in row:
        parsed.append(_require_fraction(entry, "entry"))
    return tuple(parsed)


def _require_square(rows: tuple[tuple[Fraction, ...], ...]) -> tuple[tuple[Fraction, ...], ...]:
    width = len(rows[0])
    if width != len(rows):
        raise _fail("a classical channel must be square", rows=len(rows), columns=width)
    return rows


def _require_width(rows: tuple[tuple[Fraction, ...], ...], width: int) -> tuple[tuple[Fraction, ...], ...]:
    index = 0
    while index < len(rows):
        if len(rows[index]) != width:
            raise _fail("channel rows differ in width", width=width, actual=len(rows[index]))
        index += 1
    return rows


def _parse_matrix(matrix: object) -> tuple[tuple[Fraction, ...], ...]:
    raw = _require_rows(matrix)
    parsed: list[tuple[Fraction, ...]] = []
    for row in raw:
        parsed.append(_parse_row(row))
    square = _require_square(tuple(parsed))
    return _require_width(square, len(square[0]))


def column_sum(matrix: object, column: object) -> Fraction:
    """Sum one column of a square rational channel."""
    rows = _parse_matrix(matrix)
    index = _require_fraction(column, "column")
    if index.denominator != 1 or index < 0 or index >= len(rows):
        raise _fail("column is outside the channel", column=str(index))
    total = Fraction(0)
    slot = int(index)
    row_index = 0
    while row_index < len(rows):
        total += rows[row_index][slot]
        row_index += 1
    return total


def _trace_preserving(matrix: object) -> bool:
    rows = _parse_matrix(matrix)
    column = 0
    while column < len(rows):
        if column_sum(rows, column) != 1:
            return False
        column += 1
    return True


def trace_preserving_count(channels: object) -> int:
    """How many channels have every column sum equal to 1."""
    if isinstance(channels, (str, bytes)) or not isinstance(channels, tuple):
        raise _fail("channel list is not a tuple", received=type(channels).__name__)
    count = 0
    for channel in channels:
        if _trace_preserving(channel):
            count += 1
    return count


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


def qubit_channel_census() -> int:
    """Identity and the fair depolarizing channel are counted. The leak is not."""
    identity = ((1, 0), (0, 1))
    depolarizing = ((Fraction(1, 2), Fraction(1, 2)), (Fraction(1, 2), Fraction(1, 2)))
    leaking = ((Fraction(1, 2), 0), (0, Fraction(1, 2)))
    count = trace_preserving_count((identity, depolarizing, leaking))
    if count != _COUNT:
        raise _fail("qubit channel census drifted", count=count)
    return count


_MARK = 7


def _mark() -> int:
    return _MARK


def certify(probe: object | None = None) -> Fraction:
    """Refuse a non-rational probe, then return the census 2."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    return _locked(Fraction(qubit_channel_census()), Fraction(_COUNT), "channel census drifted")


def main() -> int:
    value = qubit_channel_census()
    print(value)
    if value == _COUNT:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
