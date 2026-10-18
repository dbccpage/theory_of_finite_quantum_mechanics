from __future__ import annotations
# SPDX-License-Identifier: Apache-2.0

"""Homology-correct tetron array benchmark.

Three sections:

1. **Structure** -- V/E/F and Euler characteristic from the carrier;
   ranks, ``dim H^1``, and the code distance from native
   ``majorana_gf2_diagnostic`` (``tetron`` / ``classify``).
2. **Terminal census** -- how residuals distribute across the five terminals,
   under two declared families. Uniform-random residuals are *not* used for the
   closed families: on a torus they are ~100% `OpenObstruction`, because
   closedness is ``rank d1`` independent conditions.
3. **Timing** -- the polynomial three-way split and the exponential l1
   certification are timed **separately**, against a dense Hilbert eigensolve
   on the same instance. Conflating them would misreport the speedup.

Run::

    python -m omega_engine.crates.majorana.demos.tetron_homology_benchmark
    python -m omega_engine.crates.majorana.demos.tetron_homology_benchmark \\
        --json artifacts/tetron_homology_report.json \\
        --ledger artifacts/tetron_certificate_ledger.jsonl

AuthorityEffect: None on every emitted certificate.
"""


import argparse
import json
import random
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

_PACKAGE_PARENT = Path(__file__).resolve().parents[2]
if str(_PACKAGE_PARENT) not in sys.path:
    sys.path.insert(0, str(_PACKAGE_PARENT))

from omega_engine.crates.majorana.carriers.surface_carrier import (  
    CarrierReport,
    build_tetron_array,
    logical_class_representative,
)
from omega_engine.crates.majorana.core.gf2_matrix import GF2Matrix  
from omega_engine.crates.majorana.engines.classifier import classify  
from omega_engine.crates.majorana.engines.harmonic import (  
    DEFAULT_BUDGET,
    class_representative,
    code_distance,
    h1_basis,
)
from omega_engine.crates.majorana.engines.terminalizer import terminalize  

INSTANCES: tuple[tuple[str, int, int], ...] = (
    ("disk", 3, 3),
    ("cylinder", 3, 3),
    ("torus", 2, 2),
    ("torus", 3, 3),
    ("torus", 3, 4),
    ("torus", 4, 4),
    ("torus", 4, 5),
    ("torus", 5, 5),
    ("torus", 6, 6),
)

DEFAULT_MAX_DENSE_DIM = 2048




def structure_row(topology: str, rows: int, cols: int, budget: int) -> dict[str, Any]:
    carrier, report = build_tetron_array(rows, cols, topology)
    distance, distance_exact = code_distance(carrier.D0, carrier.D1, budget=budget)
    row = report.summary()
    row.update(
        {
            "instance": f"{topology} {rows}x{cols}",
            "code_distance": distance if distance_exact else None,
            "code_distance_upper_bound": distance,
            "code_distance_exact": distance_exact,
            "hilbert_dim": 2 ** (report.num_mzm // 2),
            "coset_size": 2 ** report.rank_d0,
        }
    )
    return row




def _closed_basis(carrier: Any, report: CarrierReport) -> list[list[int]]:
    d1 = GF2Matrix(carrier.D1, cols=report.num_channels)
    return d1.kernel_basis() if d1.rows else []


def census_iid_noise(
    topology: str, rows: int, cols: int, rate: float, trials: int, seed: int, budget: int
) -> dict[str, Any]:
    """Family A: each parity channel is independently wrong with probability ``rate``.

    This is the realistic detection regime, and it is dominated by
    `OpenObstruction` -- which is the point: local island checks *do* fire.
    """
    carrier, report = build_tetron_array(rows, cols, topology)
    rng = random.Random(seed)
    counts: Counter[str] = Counter()
    for _ in range(trials):
        residual = [1 if rng.random() < rate else 0 for _ in range(report.num_channels)]
        counts[classify(carrier.D0, carrier.D1, residual, budget=budget)[
            "terminal_status"
        ]] += 1
    return {
        "family": "iid_channel_noise",
        "instance": f"{topology} {rows}x{cols}",
        "rate": rate,
        "trials": trials,
        "terminals": dict(counts),
    }


def census_closed_exhaustive(
    topology: str, rows: int, cols: int, budget: int
) -> dict[str, Any]:
    """Family B: every residual that passes **all** island parity checks.

    ``ker d1`` has ``2 ** dim ker d1`` elements. Each cohomology class is a
    coset of ``im d0``, so every class holds exactly ``2 ** rank d0`` of them
    and there are ``2 ** dim H^1`` classes. The terminal depends only on the
    class, so the census is *analytic* -- no sampling and no enumeration of the
    whole kernel. Only the ``2 ** dim H^1`` class representatives are
    classified. ``test_benchmark.py`` checks the formula against brute force.
    """
    carrier, report = build_tetron_array(rows, cols, topology)
    basis = h1_basis(carrier.D0, carrier.D1)
    per_class = 1 << report.rank_d0

    counts: Counter[str] = Counter()
    classes: list[dict[str, Any]] = []
    for code in range(1 << basis.dim):
        coordinates = [(code >> index) & 1 for index in range(basis.dim)]
        residual = class_representative(basis, coordinates)
        cert = classify(carrier.D0, carrier.D1, residual, budget=budget)
        counts[cert["terminal_status"]] += per_class
        classes.append(
            {
                "class_id": cert["class_id"],
                "phi1_weight": cert["phi1_weight"],
                "phi1_exact": cert["phi1_exact"],
                "terminal_status": cert["terminal_status"],
            }
        )

    return {
        "family": "closed_exhaustive",
        "instance": f"{topology} {rows}x{cols}",
        "num_closed_residuals": 1 << (report.num_channels - report.rank_d1),
        "dim_ker_d1": report.num_channels - report.rank_d1,
        "rank_d0": report.rank_d0,
        "dim_h1": report.dim_h1,
        "residuals_per_class": per_class,
        "terminals": dict(counts),
        "classes": sorted(classes, key=lambda item: item["class_id"] or ""),
    }




def _dense_hilbert_baseline(dimension: int, max_dim: int) -> dict[str, Any]:
    """Dense Hermitian eigensolve on the Fock space of the same MZM count."""
    bytes_needed = dimension * dimension * 16
    if dimension > max_dim:
        return {
            "ran": False,
            "reason": (
                f"dense dimension {dimension:,} exceeds --max-dense-dim "
                f"{max_dim:,}; a dense {dimension:,} x {dimension:,} complex "
                f"matrix needs {bytes_needed / 2**30:.1f} GiB"
            ),
            "ms": None,
            "bytes": bytes_needed,
        }
    import numpy as np

    start = time.perf_counter()
    matrix = np.random.randn(dimension, dimension) + 1j * np.random.randn(
        dimension, dimension
    )
    matrix = 0.5 * (matrix + matrix.conj().T)
    np.linalg.eigvalsh(matrix)
    return {
        "ran": True,
        "reason": None,
        "ms": (time.perf_counter() - start) * 1000.0,
        "bytes": bytes_needed,
    }


def timing_row(
    topology: str,
    rows: int,
    cols: int,
    trials: int,
    seed: int,
    budget: int,
    max_dense_dim: int,
) -> dict[str, Any]:
    carrier, report = build_tetron_array(rows, cols, topology)
    rng = random.Random(seed)
    residuals = [
        [1 if rng.random() < 0.08 else 0 for _ in range(report.num_channels)]
        for _ in range(trials)
    ]

    start = time.perf_counter()
    for residual in residuals:
        terminalize(carrier.D0, carrier.D1, residual)
    split_ms = (time.perf_counter() - start) * 1000.0 / trials

    if report.dim_h1 > 0:
        logical = logical_class_representative(report, axis="column", index=0)
    else:
        logical = [0] * report.num_channels
    start = time.perf_counter()
    cert = classify(carrier.D0, carrier.D1, logical, budget=budget)
    phi1_ms = (time.perf_counter() - start) * 1000.0

    hilbert_dim = 2 ** (report.num_mzm // 2)
    dense = _dense_hilbert_baseline(hilbert_dim, max_dense_dim)

    return {
        "instance": f"{topology} {rows}x{cols}",
        "num_mzm": report.num_mzm,
        "num_channels": report.num_channels,
        "dim_h1": report.dim_h1,
        "hilbert_dim": hilbert_dim,
        "split_ms_per_residual": split_ms,
        "phi1_ms_per_residual": phi1_ms,
        "phi1_exact": cert["phi1_exact"],
        "phi1_coset_size": cert["phi1_coset_size"],
        "dense_hilbert": dense,
        "split_speedup_vs_dense": (
            dense["ms"] / split_ms if dense["ran"] and split_ms > 0 else None
        ),
        "authority_effect": "None",
    }




def build_report(
    trials: int = 200,
    seed: int = 20260805,
    budget: int = DEFAULT_BUDGET,
    max_dense_dim: int = DEFAULT_MAX_DENSE_DIM,
) -> dict[str, Any]:
    structure = [
        structure_row(topology, rows, cols, budget) for topology, rows, cols in INSTANCES
    ]
    census = [
        census_iid_noise("torus", 3, 3, rate, trials, seed, budget)
        for rate in (0.02, 0.05, 0.10)
    ] + [
        census_closed_exhaustive("disk", 3, 3, budget),
        census_closed_exhaustive("cylinder", 3, 3, budget),
        census_closed_exhaustive("torus", 3, 3, budget),
        census_closed_exhaustive("torus", 3, 4, budget),
    ]
    timing = [
        timing_row(topology, rows, cols, 50, seed, budget, max_dense_dim)
        for topology, rows, cols in INSTANCES
    ]
    return {
        "generated_for": "2026-08-05",
        "structure": structure,
        "census": census,
        "timing": timing,
        "certificates": ledger_rows(budget=budget),
        "budget": budget,
        "authority_effect": "None",
        "non_claims": [
            "no physical Majorana modes, hardware, or quantum speedup is claimed",
            "over GF(2) all l^p norms coincide on 0/1 vectors; no l1-vs-l2 "
            "separation is claimed",
            "the dense Hilbert baseline answers a different question (a "
            "spectrum, not a parity class); the comparison bounds cost, not "
            "capability",
        ],
    }


def ledger_rows(budget: int = DEFAULT_BUDGET) -> list[dict[str, Any]]:
    """One certificate per terminal per topology, replay-verifiable."""
    from omega_engine.crates.majorana.certificates.ledger import classified_ledger_row

    rows: list[dict[str, Any]] = []
    for topology in ("disk", "cylinder", "torus"):
        carrier, report = build_tetron_array(3, 3, topology)
        d0 = GF2Matrix(carrier.D0)

        gauge_alpha = [0] * report.num_mzm
        gauge_alpha[0] = 1
        single = [0] * report.num_channels
        single[0] = 1

        cases: list[tuple[str, list[int], int]] = [
            ("gauge", d0.mat_vec_mul(gauge_alpha), budget),
            ("single_channel", single, budget),
        ]
        if report.dim_h1 > 0:
            logical = logical_class_representative(report, axis="column", index=0)
            cases.append(("logical_string", logical, budget))
            cases.append(("logical_string_capped", logical, 4))

        for label, residual, case_budget in cases:
            rows.append(
                classified_ledger_row(
                    carrier.D0,
                    carrier.D1,
                    residual,
                    budget=case_budget,
                    instance=f"{topology} 3x3 / {label}",
                )
            )
    return rows




def _print_report(report: dict[str, Any]) -> None:
    print("=" * 92)
    print(" HOMOLOGY-CORRECT MAJORANA / TETRON RESIDUAL CLASSIFIER")
    print(" AuthorityEffect = None on every certificate")
    print("=" * 92)

    print("\n[1] CARRIER STRUCTURE  (dim H^1 from native majorana_gf2_diagnostic tetron)\n")
    print("    dist:  n = certified minimum;  <=n? = UNCERTIFIED upper bound "
          "(a coset search was capped);  - = not computed")
    header = (
        f"{'instance':16} {'V':>4} {'E':>4} {'F':>4} {'chi':>4} {'rk d0':>6} "
        f"{'rk d1':>6} {'graph b1':>9} {'dim H1':>7} {'dist':>7} {'2^floor(V/2)':>13}"
    )
    print(header)
    print("-" * len(header))
    for row in report["structure"]:
        bound = row.get("code_distance_upper_bound")
        if row["code_distance"] is not None:
            distance = str(row["code_distance"])
        elif bound is not None:
            distance = f"<={bound}?"
        else:
            distance = "-"
        print(
            f"{row['instance']:16} {row['num_mzm']:4} {row['num_channels']:4} "
            f"{row['num_islands']:4} {row['euler_characteristic']:4} "
            f"{row['rank_d0']:6} {row['rank_d1']:6} {row['graph_b1']:9} "
            f"{row['dim_h1']:7} {distance:>7} {row['hilbert_dim']:13,}"
        )

    print("\n[2a] TERMINAL CENSUS -- iid channel noise on torus 3x3\n")
    print(f"{'rate':>6} {'trials':>7}  terminals")
    for row in report["census"]:
        if row["family"] != "iid_channel_noise":
            continue
        print(f"{row['rate']:6.2f} {row['trials']:7}  {row['terminals']}")

    print(
        "\n[2b] TERMINAL CENSUS -- exhaustive over residuals passing EVERY island check\n"
    )
    for row in report["census"]:
        if row["family"] != "closed_exhaustive":
            continue
        print(
            f"  {row['instance']:14} closed residuals = 2^{row['dim_ker_d1']} = "
            f"{row['num_closed_residuals']:,}   dim H^1 = {row['dim_h1']}   "
            f"per class = 2^{row['rank_d0']}"
        )
        print(f"    terminals: {row['terminals']}")
        for entry in row["classes"]:
            print(
                f"      {entry['class_id']:8} phi1 = {entry['phi1_weight']:3} "
                f"(exact={entry['phi1_exact']})  -> {entry['terminal_status']}"
            )

    print("\n[3] TIMING -- polynomial split vs exponential l1 vs dense Hilbert\n")
    header = (
        f"{'instance':16} {'V':>4} {'dim H1':>7} {'split ms':>10} "
        f"{'phi1 ms':>10} {'exact':>6} {'coset':>16} {'dense dim':>11} "
        f"{'dense ms':>11} {'split x':>9}"
    )
    print(header)
    print("-" * len(header))
    for row in report["timing"]:
        dense = row["dense_hilbert"]
        dense_ms = f"{dense['ms']:11.1f}" if dense["ran"] else f"{'INFEASIBLE':>11}"
        speedup = (
            f"{row['split_speedup_vs_dense']:9,.1f}"
            if row["split_speedup_vs_dense"] is not None
            else f"{'-':>9}"
        )
        print(
            f"{row['instance']:16} {row['num_mzm']:4} {row['dim_h1']:7} "
            f"{row['split_ms_per_residual']:10.4f} {row['phi1_ms_per_residual']:10.2f} "
            f"{str(row['phi1_exact']):>6} "
            f"{row['phi1_coset_size']:16,} {row['hilbert_dim']:11,} {dense_ms} "
            f"{speedup}"
        )
    for row in report["timing"]:
        dense = row["dense_hilbert"]
        if not dense["ran"]:
            print(f"  {row['instance']:16} dense baseline not run: {dense['reason']}")

    print("\n[4] NON-CLAIMS\n")
    for item in report["non_claims"]:
        print(f"  - {item}")
    print()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Homology-correct Majorana / tetron residual classifier benchmark"
    )
    parser.add_argument("--json", type=Path, help="write the full report as JSON")
    parser.add_argument(
        "--ledger", type=Path, help="write a replayable classified certificate ledger"
    )
    parser.add_argument("--trials", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260805)
    parser.add_argument("--phi1-budget", type=int, default=DEFAULT_BUDGET)
    parser.add_argument("--max-dense-dim", type=int, default=DEFAULT_MAX_DENSE_DIM)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    report = build_report(
        trials=args.trials,
        seed=args.seed,
        budget=args.phi1_budget,
        max_dense_dim=args.max_dense_dim,
    )
    if not args.quiet:
        _print_report(report)

    if args.json is not None:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(f"wrote report -> {args.json}")

    if args.ledger is not None:
        from omega_engine.crates.majorana.certificates.ledger import (
            verify_classified_ledger,
            write_classified_ledger,
        )

        rows = ledger_rows(budget=args.phi1_budget)
        write_classified_ledger(args.ledger, rows)
        verification = verify_classified_ledger(args.ledger)
        print(
            f"wrote ledger -> {args.ledger} "
            f"({verification['checked']} rows, verified={verification['verified']})"
        )
        if not verification["verified"]:
            print(json.dumps(verification["failures"][:5], indent=2))
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())




