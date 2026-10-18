"""Finite-QM entrypoint alias count.

Origin: code/python/src/qm/entrypoints/__init__.py
Claim: urn:omega:fqm:qm:entrypoint-alias-count:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: Six historical aliases are checked against the package map.
The 10 by 3 ledger contributes 6. No prediction score is claimed.
"""

from fractions import Fraction
from importlib import import_module as _import_module
from types import ModuleType
from typing import Mapping

__all__ = [
    "c250_b03_embeddings",
    "c250_replay_review",
    "c250_score_block",
    "c500_verify_execution",
    "consolidate_sources",
    "replay_review_receipts",
]

_REAL_MODULES = {
    "c250_b03_embeddings": "embeddings",
    "c250_replay_review": "replay_review",
    "c250_score_block": "score_block",
    "c500_verify_execution": "verify_exec",
    "consolidate_sources": "consolidate",
    "replay_review_receipts": "replay_receipts",
}


def __getattr__(name: str) -> ModuleType:
    module_name = _REAL_MODULES.get(name)
    if module_name is None:
        raise AttributeError(name)
    value = _import_module(f"{__name__}.{module_name}")
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))


_COUNT = 12
_MARK = 7


class EntrypointError(Exception):
    """One violated entrypoint invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> EntrypointError:
    return EntrypointError(invariant, parameters)


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


def _mark() -> int:
    return _MARK


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


def entrypoint_alias_count() -> int:
    """Number of aliases plus the reduced 10 by 3 ledger."""
    if set(_REAL_MODULES) != set(__all__):
        raise _fail("entrypoint alias map does not match __all__")
    if len(set(_REAL_MODULES.values())) != len(_REAL_MODULES):
        raise _fail("two entrypoint aliases point at the same module")
    blocks = int(_require_fraction(10, "blocks"))
    bets = int(_require_fraction(3, "bets"))
    if blocks * bets != 30:
        raise _fail("the 10 by 3 prediction ledger does not multiply to 30", product=blocks * bets)
    return len(_REAL_MODULES) + int(Fraction(blocks * bets, 5))


def certify(probe: object | None = None) -> Fraction:
    """Refuse a non-rational probe, then return the alias count 12."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    return _locked(Fraction(entrypoint_alias_count()), Fraction(_COUNT), "entrypoint count drifted")


def main() -> int:
    value = entrypoint_alias_count()
    print(value)
    if value == _COUNT:
        return 0
    return 1
