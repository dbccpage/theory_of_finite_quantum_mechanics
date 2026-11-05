"""Per-run case aggregate with unique identifiers. AuthorityEffect: None."""
from .boundary import Violation
from collections.abc import Iterator
from .boundary import evaluate, require
from .outcome import Outcome

MAX_CASES = 100_000
MAX_ID_LENGTH = 1024


class Cases:
    """Owns result identities and counts; no state survives a checker invocation."""

    def __init__(self) -> None:
        self._checks = 0
        self._rows: list[tuple[str, bool]] = []
        self._names: set[str] = set()

    def append(self, row: tuple[str, bool]) -> None:
        if type(row) is not tuple or len(row) != 2:
            raise Violation("input", "case row must be an (identity, bool) pair")
        name, passed = row
        if type(name) is not str or not name.strip():
            raise Violation("input", "case identity must be a nonempty string")
        if type(passed) is not bool:
            raise Violation("input", "case status must be a bool")
        if len(name) > MAX_ID_LENGTH:
            raise Violation("resource", "case identity exceeds 1024 characters")
        if name in self._names:
            raise Violation("duplicate", f"duplicate case identity: {name}")
        if len(self._rows) >= MAX_CASES:
            raise Violation("resource", "case aggregate exceeds 100000 entries")
        self._names.add(name)
        self._rows.append((name, passed))
        self._checks += 1

    def record(self, name: str, passed: bool) -> Outcome[None]:
        """Transactional admission: failed rows leave both indexes unchanged."""
        return evaluate(self.append, (name, passed))

    @property
    def checks(self) -> int:
        return self._checks

    def require(self, condition: bool, message: str) -> None:
        self._checks += 1
        require(condition, message)

    def __len__(self) -> int:
        return len(self._rows)

    def __iter__(self) -> Iterator[tuple[str, bool]]:
        return iter(tuple(self._rows))
