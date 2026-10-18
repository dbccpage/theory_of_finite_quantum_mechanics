"""Canonical three-point RPCNF fixture for the relational coincidence harness.

Origin: papers/derivations/relational_point_coincidence/relational_point_coincidence_and_witnessed_difference_claim_ledger.md
Claim: urn:omega:fqm:gr003:canonical-three-point-rpcnf:v1
AuthorityEffect: None
Mutation-Kills: 3 non-equivalent source mutants, executed by papers/derivations/relational_point_coincidence/code/tests/test_relational_spacetime.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 3; AST Sonar cognitive complexity max 2; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 3.
Scope Fence: The fixture is one finite relation. It does not derive a continuum spacetime or authorize the scalar fields it names.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

_CODE_DIR = str(Path(__file__).resolve().parents[1])
if _CODE_DIR not in sys.path:
    sys.path.insert(0, _CODE_DIR)

from relational_spacetime import EventTuple, RelationalCertificateError, SpacetimeRelation


def harness_key_width() -> int:
    """RPCNF candidate keys in this harness have width 4."""
    return 4


def _row(
    phi0: int,
    phi1: int,
    phi2: int,
    phi3: int,
    density: int,
    kretschmann: int,
) -> EventTuple:
    return EventTuple(
        {
            "phi0": Fraction(phi0),
            "phi1": Fraction(phi1),
            "phi2": Fraction(phi2),
            "phi3": Fraction(phi3),
            "matter_density": Fraction(density),
            "kretschmann": Fraction(kretschmann),
        }
    )


def canonical_three_point() -> SpacetimeRelation:
    """The three witnessed rows used to lock CLM-GR003-005."""
    attributes = {"phi0", "phi1", "phi2", "phi3", "matter_density", "kretschmann"}
    relation = SpacetimeRelation(
        attributes,
        [
            _row(1, 0, 0, 0, 10, 48),
            _row(2, 1, 0, 0, 5, 12),
            _row(3, 1, 1, 1, 1, 3),
        ],
    )
    key = {"phi0", "phi1", "phi2", "phi3"}
    certificate = relation.check_rpcnf(key, {"t", "x", "y", "z"})
    if certificate.is_rpcnf is not True:
        raise RelationalCertificateError(
            "canonical three-point relation left RPCNF",
            {"violations": certificate.violations},
        )
    if len(key) != harness_key_width():
        raise RelationalCertificateError("harness key width drifted", {"width": len(key)})
    return relation


def refuse_float_probe(value: object) -> str:
    """Name the boundary refusal for a float probe without computing with it."""
    if isinstance(value, float):
        raise RelationalCertificateError(
            "float refused at the public boundary",
            {"role": "harness probe", "received": "float"},
        )
    return type(value).__name__
