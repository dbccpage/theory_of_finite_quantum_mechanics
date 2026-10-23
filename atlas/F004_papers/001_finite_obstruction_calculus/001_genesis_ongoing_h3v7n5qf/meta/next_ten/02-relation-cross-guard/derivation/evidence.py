"""Deterministic evidence generator for Problem 02 (relation-cross-guard).

Generates evidence files and verifies byte-identical reproduction under --check.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Sequence
from itertools import combinations_with_replacement
from pathlib import Path
from typing import Any

# Ensure derivation package and repo code are importable
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from cost import (  # noqa: E402 - standalone path bootstrap above
    minimum_changes,
    minimum_peak_terms,
    shortest_construction,
)
from model import (  # noqa: E402 - standalone path bootstrap above
    DState,
    GuardedExploration,
    canonical,
    compare_with_ninth,
    count_disjoint_results,
    empty,
    explore,
    witness_blocked_pair,
    witness_identification_bypass,
    witness_two_term_bypass,
)

EVIDENCE_DIR = _HERE / "evidence"


def sha256_text(text: str) -> str:
    """Compute hex SHA-256 digest of utf-8 text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def generate_run_evidence(exp: GuardedExploration) -> dict[str, Any]:
    """Generate summary data for guarded exploration."""
    return {
        "bound_terms": exp.bound_terms,
        "bound_assertions": exp.bound_assertions,
        "rounds": exp.rounds,
        "total_results": exp.total_results,
        "last_new_round": exp.last_new_round,
        "new_per_round": exp.new_per_round,
        "attempts_per_round": exp.attempts_per_round,
        "blocked_attempts_per_round": exp.blocked_attempts_per_round,
        "frontier_count": len(exp.frontier),
    }


def generate_frontier_evidence(exp: GuardedExploration) -> list[dict[str, str]]:
    """Generate exact frontier record of exits beyond declared bounds."""
    out: list[dict[str, str]] = []
    for exit_item in exp.frontier:
        out.append(
            {
                "source_state": exit_item.state.key(),
                "change": exit_item.change.written(exit_item.state),
                "reason": exit_item.reason,
            }
        )
    return out


def generate_witnesses_evidence() -> dict[str, Any]:
    """Generate concrete witness data for blocked addition and identification bypasses."""
    s_blocked, c_blocked = witness_blocked_pair()
    p1 = witness_identification_bypass()
    p2 = witness_two_term_bypass()

    return {
        "blocked_pair": {
            "state": s_blocked.key(),
            "change": c_blocked.written(s_blocked),
            "rel": c_blocked.rel,
            "x": c_blocked.x,
            "y": c_blocked.y,
        },
        "one_term_bypass": {
            "target": p1[-1][1].key(),
            "steps": len(p1),
            "sequence": [
                {"step": i + 1, "change": c.written(s), "result": next_s.key()}
                for i, ((c, next_s), s) in enumerate(
                    zip(p1, [canonical(empty())] + [x[1] for x in p1[:-1]])
                )
            ],
        },
        "two_term_bypass": {
            "target": p2[-1][1].key(),
            "steps": len(p2),
            "sequence": [
                {"step": i + 1, "change": c.written(s), "result": next_s.key()}
                for i, ((c, next_s), s) in enumerate(
                    zip(p2, [canonical(empty())] + [x[1] for x in p2[:-1]])
                )
            ],
        },
    }


def generate_differential_checks() -> dict[str, Any]:
    """Run differential comparisons between independent models."""
    cmp_ninth = compare_with_ninth(bound_terms=3, bound_assertions=3, rounds=6)

    # Differential check 1: Round 3 divergence
    r3_ninth_diff = cmp_ninth["diff_per_round"][3]  # type: ignore[index]
    r3_check_pass = r3_ninth_diff == ["1::0-0*1|0-0*1"]

    # Differential check 2: Pure additions vs full changes at round 5
    exp_all = explore(bound_terms=3, bound_assertions=3, rounds=5, additions_only=False)
    exp_add = explore(bound_terms=3, bound_assertions=3, rounds=5, additions_only=True)
    round5_divergence = sorted(
        s.key() for s in (set(exp_all.results_at_round(5)) - set(exp_add.results_at_round(5)))
    )
    r5_check_pass = round5_divergence == ["1::0-0*1|0-0*1"]

    # Differential check 3: 2-term target reachability with n<=2 vs n<=3
    target_2term = canonical(DState.of(2, ((0, 1),), ((0, 1),)))
    exp_n2 = explore(bound_terms=2, bound_assertions=4, rounds=8)
    exp_n3 = explore(bound_terms=3, bound_assertions=4, rounds=8)
    n2_reachable = target_2term in exp_n2.depth
    n3_reachable = target_2term in exp_n3.depth
    term_inflation_pass = (not n2_reachable) and n3_reachable

    return {
        "cmp_ninth": cmp_ninth,
        "round3_divergence": r3_ninth_diff,
        "round3_check_pass": r3_check_pass,
        "round5_additions_vs_all_divergence": round5_divergence,
        "round5_check_pass": r5_check_pass,
        "two_term_target_reachable_n2": n2_reachable,
        "two_term_target_reachable_n3": n3_reachable,
        "term_inflation_check_pass": term_inflation_pass,
    }


def generate_cost_checks() -> dict[str, Any]:
    """Compare exact formulas and paths with a separately enumerated finite census."""
    targets: set[DState] = set()
    for n in range(3):
        for m in range(5):
            for slots in combinations_with_replacement(range(2 * n * n), m):
                values = [0] * (2 * n * n)
                for slot in slots:
                    values[slot] += 1
                targets.add(canonical(DState(n, tuple(values[: n * n]), tuple(values[n * n :]))))
    exp = explore(bound_terms=2, bound_assertions=4, rounds=10)
    predicted = {state for state in targets if minimum_peak_terms(state) <= 2}
    if set(exp.depth) != predicted or any(
        exp.depth[state] != minimum_changes(state) for state in predicted
    ):
        raise ValueError("cost or term-cap prediction disagrees with bounded exploration")
    for target in sorted(targets, key=lambda state: state.key()):
        trace = shortest_construction(target)
        final = trace[-1][1] if trace else empty()
        if (
            canonical(final) != target
            or len(trace) != minimum_changes(target)
            or max([0, *(state.n for _, state in trace)]) != minimum_peak_terms(target)
        ):
            raise ValueError("constructed path disagrees with target, cost or peak")
    return {
        "term_bound": 2,
        "assertion_bound": 4,
        "rounds": 10,
        "canonical_targets": len(targets),
        "reachable_within_term_bound": len(exp.depth),
        "all_depths_and_constructions_match": True,
        "scope": "Bounded computational checks only; the general statements have written proofs, not new Lean theorems.",
    }


def build_all_artifacts(target_dir: Path) -> dict[str, str]:
    """Compute and serialize all evidence artifacts to dict of filename -> json text."""
    exp = explore(bound_terms=3, bound_assertions=3, rounds=6)

    run_data = generate_run_evidence(exp)
    frontier_data = generate_frontier_evidence(exp)
    witness_data = generate_witnesses_evidence()
    diff_data = generate_differential_checks()
    disjoint_counts = count_disjoint_results(bound_terms=3, bound_assertions=3)
    formal_status = {
        "lean_source_sha256": hashlib.sha256((_HERE / "Derivation.lean").read_bytes()).hexdigest(),
        "compiler_executed_by_this_writer": False,
        "general_cost_and_peak_formalized": False,
        "python_lean_transport_proved": False,
        "retained_static_annotation": "lean_axioms.txt",
        "scope": "The retained annotation was hardcoded by the historical writer. It is excluded from the current computational manifest and is not a compiler attestation. Capture actual compiler output independently.",
    }

    artifacts: dict[str, str] = {
        "run.json": json.dumps(run_data, indent=2, sort_keys=True) + "\n",
        "frontier.json": json.dumps(frontier_data, indent=2, sort_keys=True) + "\n",
        "witnesses.json": json.dumps(witness_data, indent=2, sort_keys=True) + "\n",
        "differential.json": json.dumps(diff_data, indent=2, sort_keys=True) + "\n",
        "disjoint_counts.json": json.dumps(disjoint_counts, indent=2, sort_keys=True) + "\n",
        "formal_status.json": json.dumps(formal_status, indent=2, sort_keys=True) + "\n",
        "cost_checks.json": json.dumps(generate_cost_checks(), indent=2, sort_keys=True) + "\n",
    }

    # Manifest
    manifest_lines = []
    for name in sorted(artifacts.keys()):
        digest = sha256_text(artifacts[name])
        manifest_lines.append(f"{digest}  {name}\n")
    artifacts["MANIFEST.sha256"] = "".join(manifest_lines)

    return artifacts


def write_evidence(out_dir: Path) -> None:
    """Generate and write all evidence artifacts to out_dir."""
    out_dir.mkdir(parents=True, exist_ok=True)
    artifacts = build_all_artifacts(out_dir)
    for name, content in artifacts.items():
        (out_dir / name).write_bytes(content.encode("utf-8"))


def check_evidence(out_dir: Path) -> bool:
    """Verify that existing evidence directory matches regenerated artifacts byte-for-byte."""
    if not out_dir.exists():
        return False
    artifacts = build_all_artifacts(out_dir)
    for name, expected in artifacts.items():
        file_path = out_dir / name
        if not file_path.exists():
            return False
        if file_path.read_bytes() != expected.encode("utf-8"):
            return False
    return True


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point for evidence generation and checking."""
    parser = argparse.ArgumentParser(description="Evidence generator for Problem 02")
    parser.add_argument("--out", type=Path, default=EVIDENCE_DIR, help="Output evidence directory")
    parser.add_argument(
        "--check", action="store_true", help="Verify byte-identical match with existing evidence"
    )
    args = parser.parse_args(argv)

    if args.check:
        if not check_evidence(args.out):
            print(f"Evidence check FAILED: directory {args.out} differs or is missing.")
            return 1
        print(f"Evidence check PASSED: all artifacts in {args.out} match byte-for-byte.")
        return 0

    write_evidence(args.out)
    print(f"Evidence successfully written to {args.out}.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
