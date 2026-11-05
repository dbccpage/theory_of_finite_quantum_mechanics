"""Conditional CH20 finite-table evaluator; AuthorityEffect: None.

Declared Boolean tables are the finite semantic model, not assertions about
physical truth. Evidence is replayed against that model before status routing.
Outside-profile takes precedence over refusal; refusal precedes evidence.
Ill-typed queries raise errors before the five-status algebra.
"""

from dataclasses import dataclass
from enum import Enum


class Status(str, Enum):
    PROVED = "Proved"
    REFUTED = "Refuted"
    UNDETERMINED = "Undetermined"
    OUTSIDE_PROFILE = "OutsideProfile"
    REFUSED = "Refused"


@dataclass(frozen=True)
class Evidence:
    query: str
    value: bool

    def __post_init__(self):
        if not isinstance(self.query, str) or type(self.value) is not bool:
            raise TypeError("evidence requires a string query and Boolean value")


@dataclass(frozen=True)
class Profile:
    table: tuple[tuple[str, bool], ...]
    admitted: frozenset[str]
    refused: frozenset[str] = frozenset()
    budget: int = 1

    def __post_init__(self):
        object.__setattr__(self, "table", tuple(tuple(row) for row in self.table))
        object.__setattr__(self, "admitted", frozenset(self.admitted))
        object.__setattr__(self, "refused", frozenset(self.refused))
        keys = []
        for row in self.table:
            if len(row) != 2 or not isinstance(row[0], str) or type(row[1]) is not bool:
                raise TypeError("table rows require string queries and Boolean values")
            keys.append(row[0])
        if len(keys) != len(set(keys)):
            raise ValueError("duplicate query in semantic table")
        if not self.admitted <= set(keys) or not self.refused <= self.admitted:
            raise ValueError("admission and policy must reference declared queries")
        if type(self.budget) is not int or self.budget < 0:
            raise ValueError("budget must be a nonnegative integer")


def verify_evidence(profile: Profile, evidence: Evidence) -> bool:
    """Recheck a candidate independently of claimed status or admission policy."""
    return evidence.query in dict(profile.table) and dict(profile.table)[evidence.query] is evidence.value


def status_guards(profile: Profile, query: str, candidates=()) -> tuple[bool, ...]:
    """Return disjoint guards in Status iteration order, after bounded replay."""
    if not isinstance(query, str) or query not in dict(profile.table):
        raise ValueError("query is not in the declared ambient grammar")
    if not isinstance(candidates, tuple) or any(not isinstance(e, Evidence) for e in candidates):
        raise TypeError("candidates must be a finite tuple of Evidence")
    admitted = query in profile.admitted
    allowed = admitted and query not in profile.refused
    checked = candidates[:profile.budget] if allowed else ()
    proved = allowed and any(e.query == query and e.value and verify_evidence(profile, e) for e in checked)
    refuted = allowed and any(e.query == query and not e.value and verify_evidence(profile, e) for e in checked)
    return (proved, refuted, allowed and not proved and not refuted,
            not admitted, admitted and not allowed)


def evaluate(profile: Profile, query: str, candidates=()) -> Status:
    guards = status_guards(profile, query, candidates)
    selected = [status for status, holds in zip(Status, guards) if holds]
    if len(selected) != 1:
        raise ValueError("status predicates are not exclusive and exhaustive")
    return selected[0]


@dataclass(frozen=True)
class ProfileTransport:
    """Injective finite query encoding preserving the declared Boolean model.

    Grammar/model fidelity does not preserve budget, admission or policy. Only
    independently replayed evidence is transported, never a terminal status.
    """
    source: Profile
    target: Profile
    mapping: tuple[tuple[str, str], ...]

    def __post_init__(self):
        object.__setattr__(self, "mapping", tuple(tuple(row) for row in self.mapping))
        source_table, target_table = dict(self.source.table), dict(self.target.table)
        if any(len(row) != 2 for row in self.mapping):
            raise ValueError("transport requires pairs")
        encoding = dict(self.mapping)
        if len(encoding) != len(self.mapping) or set(encoding) != set(source_table):
            raise ValueError("transport must encode every source query exactly once")
        if len(set(encoding.values())) != len(encoding):
            raise ValueError("transport must be injective")
        for query, encoded in encoding.items():
            if encoded not in target_table or source_table[query] is not target_table[encoded]:
                raise ValueError("transport does not preserve the declared model")

    def transport_evidence(self, evidence: Evidence) -> Evidence:
        if not verify_evidence(self.source, evidence):
            raise ValueError("source evidence failed replay")
        transported = Evidence(dict(self.mapping)[evidence.query], evidence.value)
        if not verify_evidence(self.target, transported):
            raise ValueError("target evidence failed replay")
        return transported
