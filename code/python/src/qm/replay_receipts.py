"""Replay only the two finite computation receipts repaired in PR #205.

AuthorityEffect: None. No mathematical promotion follows from byte identity.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .gleason_cyclotomic import GleasonCyclotomic
from .higher_entangle import HigherDimEntanglementWitness

APP_ROOT = next(
    (parent for parent in Path(__file__).resolve().parents
     if (parent / "finite_quantum_mechanics.md").is_file()),
    Path(__file__).resolve().parents[3],
)
METHODS = (
    "verify_cabello_hypergraph_structure", "non_psd_cabello_witness",
    "pseudo_state_diagonal_witness", "bounded_triad_algebraic_search_d3",
    "topological_disconnectedness_analysis",
    "bounded_triad_algebraic_search_higher_conductors",
    "topological_disconnectedness_higher_conductors",
    "evaluate_meyer_rational_vs_cyclotomic_colorability",
    "evaluate_clifton_kent_incompleteness_polytope",
    "evaluate_padic_and_nonstandard_obstructions",
)

def method_census() -> int:
    """Count Gleason methods the two receipts call, after checking each attribute exists."""
    missing = [name for name in METHODS if not hasattr(GleasonCyclotomic, name)]
    if missing:
        raise AttributeError("gleason receipt methods missing: " + ", ".join(missing))
    if not hasattr(HigherDimEntanglementWitness, "full_escalation_hierarchy_summary"):
        raise AttributeError("higher-dimensional receipt is missing full_escalation_hierarchy_summary")
    return len(METHODS)


def render_receipts() -> dict[str, bytes]:
    reports = {
        "gleason_cyclotomic_obstruction.json": {
            "authority_effect": "None",
            "schema": "fqm-finite-review-v2",
            "scope": "FINITE_CONFIGURATIONS_ONLY; DENSE_SPHERE_GLEASON_OPEN",
            "reports": {name: getattr(GleasonCyclotomic, name)() for name in METHODS},
        },
        "higher_dim_conductor_bounds.json": {
            "authority_effect": "None",
            "schema": "fqm-finite-review-v2",
            **HigherDimEntanglementWitness.full_escalation_hierarchy_summary(),
        },
    }
    return {name: (json.dumps(value, sort_keys=True, indent=2, default=str) + "\n").encode("utf-8")
            for name, value in reports.items()}

def check_receipts(directory: Path, rendered: dict[str, bytes]) -> list[str]:
    return [name for name, data in rendered.items()
            if not (directory / name).is_file() or (directory / name).read_bytes() != data]

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=APP_ROOT / "evidence")
    args = parser.parse_args()
    rendered = render_receipts()
    if args.check:
        mismatches = check_receipts(args.output, rendered)
        for name in mismatches:
            print("FAIL: receipt differs or is missing: " + name)
        if not mismatches:
            print("PASS: two finite computation receipts are byte-identical")
        return bool(mismatches)
    args.output.mkdir(parents=True, exist_ok=True)
    for name, data in rendered.items():
        (args.output / name).write_bytes(data)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

__all__ = ['APP_ROOT', 'METHODS', 'check_receipts', 'main', 'render_receipts']
