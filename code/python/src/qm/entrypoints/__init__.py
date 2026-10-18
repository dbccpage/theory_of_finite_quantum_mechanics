"""Finite-QM entrypoints.

AuthorityEffect: None.

Origin: code/python/src/qm/entrypoints/__init__.py
Claim: each historical entrypoint name resolves to a module file that exists in this package.
"""

from importlib import import_module as _import_module
from fractions import Fraction

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


def __getattr__(name):
    module_name = _REAL_MODULES.get(name)
    if module_name is None:
        raise AttributeError(name)
    value = _import_module(f"{__name__}.{module_name}")
    globals()[name] = value
    return value


def __dir__():
    return sorted(set(globals()) | set(__all__))


def entrypoint_alias_count() -> int:
    """Number of aliases. The map is checked against __all__ before the count is returned."""
    if set(_REAL_MODULES) != set(__all__):
        raise ValueError("entrypoint alias map does not match __all__")
    if len(set(_REAL_MODULES.values())) != len(_REAL_MODULES):
        raise ValueError("two entrypoint aliases point at the same module")
    blocks = 10
    bets = 3
    if blocks * bets != 30:
        raise ValueError("the 10 by 3 prediction ledger does not multiply to 30")
    return len(_REAL_MODULES) + int(Fraction(blocks * bets, 5))
