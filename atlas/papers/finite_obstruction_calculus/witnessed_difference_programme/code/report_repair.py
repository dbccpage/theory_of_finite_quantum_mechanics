"""Independent integer-table reference for least report repair.

The native owner is omega_category_theory::finite_report_repair. This paper
reference does not acquire missing measurements, license edits or run an app.
"""

from collections.abc import Sequence


def _integer(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _tables(report: Sequence[int], answers: Sequence[Sequence[int]]) -> None:
    if not isinstance(report, (list, tuple)) or not isinstance(answers, (list, tuple)):
        raise ValueError("explicit finite tables required")
    if len(report) != len(answers) or any(not _integer(x) for x in report):
        raise ValueError("invalid report table")
    width = len(answers[0]) if answers and isinstance(answers[0], (list, tuple)) else 0
    for row in answers:
        if not isinstance(row, (list, tuple)) or len(row) != width:
            raise ValueError("ragged answer table")
        if any(not _integer(value) for value in row):
            raise ValueError("exact integer answers required")


def _classes(keys: Sequence[object]) -> tuple[int, ...]:
    ids: dict[object, int] = {}
    return tuple(ids.setdefault(key, len(ids)) for key in keys)


def least_repair(report: Sequence[int], answers: Sequence[Sequence[int]]) -> tuple[int, ...]:
    """Direct joint-profile oracle, independent of a witness-selection algorithm."""
    _tables(report, answers)
    return _classes([(r, tuple(row)) for r, row in zip(report, answers, strict=True)])


def split_class(
    report: Sequence[int], answers: Sequence[Sequence[int]],
    first: int, second: int, question: int,
) -> tuple[int, ...]:
    """Split the entire witnessed class; keep all other classes intact."""
    _tables(report, answers)
    if any(not _integer(i) or i < 0 for i in (first, second, question)):
        raise ValueError("invalid witness index")
    if first >= len(report) or second >= len(report) or question >= len(answers[first]):
        raise ValueError("witness outside table")
    if report[first] != report[second] or answers[first][question] == answers[second][question]:
        raise ValueError("not a lost-answer witness")
    return _classes([
        (r, row[question] if r == report[first] else None)
        for r, row in zip(report, answers, strict=True)
    ])


def replay_repair(
    report: Sequence[int], answers: Sequence[Sequence[int]],
    steps: Sequence[tuple[int, int, int]], candidate: Sequence[int],
) -> bool:
    """Replay without searching; compare the final pair relation to the oracle."""
    _tables(report, answers)
    if not isinstance(steps, (list, tuple)) or len(steps) > len(report):
        raise ValueError("invalid or excessive step sequence")
    if not isinstance(candidate, (list, tuple)) or any(not _integer(x) for x in candidate):
        raise ValueError("invalid partition")
    current = _classes(list(report))
    for step in steps:
        if not isinstance(step, (list, tuple)) or len(step) != 3:
            raise ValueError("invalid step")
        current = split_class(current, answers, *step)
    if tuple(candidate) != current:
        return False
    target = least_repair(report, answers)
    return all((current[i] == current[j]) == (target[i] == target[j])
               for i in range(len(report)) for j in range(i))
