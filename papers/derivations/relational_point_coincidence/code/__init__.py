"""Package certificate that witnessed points coincide exactly on a four-name key.

Origin: papers/derivations/relational_point_coincidence/relational_point_coincidence_and_witnessed_difference_claim_ledger.md
Claim: urn:omega:fqm:gr003:point-coincidence-candidate-key:v1
AuthorityEffect: None
Mutation-Kills: 3 non-equivalent source mutants, executed by papers/derivations/relational_point_coincidence/code/tests/test_relational_spacetime.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 4; AST Sonar cognitive complexity max 3; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 4.
Scope Fence: Agreement on four declared names is not continuous general relativity, not quantum gravity, and not a proof that every scalar family separates points.
"""

from __future__ import annotations

from relational_spacetime import EventTuple, RelationalCertificateError, SpacetimeRelation

PUBLIC_TYPES = (EventTuple, RelationalCertificateError, SpacetimeRelation)

__all__ = [
    "PUBLIC_TYPES",
    "EventTuple",
    "RelationalCertificateError",
    "SpacetimeRelation",
    "points_coincide",
    "witnessed_key_width",
]


def _fail(invariant: str, **parameters: object) -> RelationalCertificateError:
    return RelationalCertificateError(invariant, parameters)


def _one_name(value: object) -> str:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role="key", received="float")
    if type(value) is not str:
        raise _fail("candidate key name is not a string", role="key", received=type(value).__name__)
    if value == "":
        raise _fail("candidate key name is empty", role="key")
    return value


def _name_set(key: object) -> frozenset[str]:
    if isinstance(key, (str, bytes)):
        raise _fail("candidate key is not a name collection", received=type(key).__name__)
    if not isinstance(key, (set, frozenset, tuple, list)):
        raise _fail("candidate key is not a name collection", received=type(key).__name__)
    names: list[str] = []
    for item in key:
        names.append(_one_name(item))
    return frozenset(names)


def witnessed_key_width(key: object) -> int:
    """Return 4 when the supplied candidate key has the RPCNF width."""
    names = _name_set(key)
    if len(names) != 4:
        raise _fail("candidate key width is not 4", width=len(names))
    return len(names)


def points_coincide(left: object, right: object, key: object) -> bool:
    """CLM-GR003-001: supplied points coincide when their four-name projections agree."""
    if not isinstance(left, EventTuple) or not isinstance(right, EventTuple):
        raise _fail("coincidence expects two event tuples", received="non-event")
    witnessed_key_width(key)
    names = _name_set(key)
    same = left.project(names) == right.project(names)
    if type(same) is not bool:
        raise _fail("coincidence comparison was not boolean")
    return same
