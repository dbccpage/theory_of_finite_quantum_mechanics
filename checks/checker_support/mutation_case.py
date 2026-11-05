"""Immutable fault-injection request in the independent-checker verification context."""
from dataclasses import dataclass
import re
from .boundary import Violation


@dataclass(frozen=True, slots=True)
class MutationCase:
    identity: str
    source: str
    before: str
    after: str
    tests: tuple[str, ...]

    def __post_init__(self) -> None:
        patterns = ((self.identity, r"[a-z][a-z0-9-]{0,79}"),
                    (self.source, r"[a-z][a-z0-9_]*\.py"))
        for value, pattern in patterns:
            if type(value) is not str or re.fullmatch(pattern, value) is None:
                raise Violation("input", "mutation identity or source basename is invalid")
        for text in (self.before, self.after):
            if type(text) is not str or not text or len(text) > 8192:
                raise Violation("input", "mutation replacement must have 1..8192 characters")
        if self.before == self.after:
            raise Violation("input", "mutation must change the source")
        if type(self.tests) is not tuple or not 1 <= len(self.tests) <= 32:
            raise Violation("input", "mutation requires 1..32 test names")
        if any(type(name) is not str or re.fullmatch(r"test_[a-z0-9_]+", name) is None
               for name in self.tests):
            raise Violation("input", "mutation test names must identify test methods")
        if len(set(self.tests)) != len(self.tests):
            raise Violation("duplicate", "mutation test names must be unique")

    def apply(self, source: str) -> str:
        """Require exactly one matching occurrence, refusing stale or ambiguous recipes."""
        if type(source) is not str or source.count(self.before) != 1:
            raise Violation("input", "mutation target must occur exactly once")
        return source.replace(self.before, self.after, 1)
