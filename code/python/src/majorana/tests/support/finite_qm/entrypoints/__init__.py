"""Finite-QM entrypoints.

AuthorityEffect: None.
"""

from importlib import import_module as _import_module

__all__ = ['c250_b03_embeddings', 'c250_replay_review', 'c250_score_block', 'c500_verify_execution', 'consolidate_sources', 'replay_review_receipts']

def __getattr__(name):
    if name not in __all__:
        raise AttributeError(name)
    value = _import_module(f"{__name__}.{name}")
    globals()[name] = value
    return value

def __dir__():
    return sorted(set(globals()) | set(__all__))
