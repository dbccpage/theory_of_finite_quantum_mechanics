# -*- coding: utf-8 -*-
"""
Command-line interface for the CODA application.
Provides subcommands: status, layers, evaluate, stress-test.

AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import sys
from sympy import Matrix, Rational

from coda_application.domain.entities import ProblemInstance
from coda_application.domain.value_objects import LayerId
from coda_application.infrastructure.rust_bridge import RustCrateBridge
from coda_application.application import _certificate_checks
from coda_application.application import evaluate_coda_pipeline


def cmd_status() -> int:
    """Displays CODA framework status and Rust crate workspace integration."""
    print("=" * 60)
    print("CODA Application: 9-Layer Architecture Status")
    print("AuthorityEffect: None")
    print("=" * 60)

    bridge = RustCrateBridge()
    available = bridge.is_workspace_available()
    crates = bridge.get_available_crates() if available else []

    print(f"Rust Crate Workspace (omega_engine/crates_rs): {'FOUND' if available else 'NOT FOUND'}")
    print(f"Total Member Crates Registered: {len(crates)}")
    if crates:
        print("Key Math/Pipeline Crates:")
        for c in ["omega_solvers", "omega_pipelines", "omega_homology", "omega_terminalizers", "omega_types"]:
            status = "PRESENT" if c in crates else "MISSING"
            print(f"  - {c:<25} : {status}")

    print("\nCODA Nine Layers Active: YES (domain imports no use-case, infrastructure or presentation module)")
    return 0


def cmd_layers() -> int:
    """Lists the 9 layers of CODA."""
    layers = [
        (LayerId.FOC, "Finite Obstruction Calculus", "Quotients Phi_1, cocycles Gamma_2, LP dual witnesses"),
        (LayerId.MUR, "Meta & Universal Re-Presentation", "Declared overlap agreement and coordinate loss"),
        (LayerId.CS, "Continuum Shadow", "Total map between supplied fine and coarse labels"),
        (LayerId.CS_Q, "Continuum Shadow to Continuum Bridge", "Equality and distances of supplied finite section vectors"),
        (LayerId.Q, "The Continuum", "Rational interval order and diameter"),
        (LayerId.A, "Anomalon", "The Anomalon as a typed leftover; residual classes registered"),
        (LayerId.OR, "Omniversal Re-Presentation", "Declared incompatible overlaps and empty-sieve refusal"),
        (LayerId.FDA, "Finite Descent Authority", "Seven halt guards, role split, authority conservation"),
        (LayerId.GTLA, "General Theory of Layered Authority", "Local authorized, residual, or refusal record"),
    ]
    print("=" * 80)
    print("THE NINE LAYERS OF CODA (GTLA Stack)")
    print("=" * 80)
    for idx, (lid, name, desc) in enumerate(layers, 1):
        print(f"Layer {idx:02d} [{lid.value:<5}] : {name:<36} | {desc}")
    return 0


def cmd_evaluate(licensed: bool = False, obstructed: bool = False) -> int:
    """Evaluates a canonical problem instance through the 9 CODA layers.

    ``licensed`` attaches a bare license claim, to show that a flag is refused: no token
    is ever minted from the command line. Authorization needs an AuthorityGrant.
    """
    print("=" * 60)
    print(f"Executing CODA 9-Layer Pipeline (licensed={licensed}, obstructed={obstructed})")
    print("=" * 60)

    # Construct canonical problem instance
    if obstructed:
        defect = Matrix([Rational(1), Rational(0)])
    else:
        defect = Matrix([Rational(0), Rational(0)])

    d0 = Matrix([[-1, 1], [1, -1]])
    d1 = Matrix.zeros(1, 2)

    prob = ProblemInstance(
        problem_id="cli_eval_instance",
        raw_data="cli_payload",
        candidate_sieve=("cand1", "cand2"),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U0": (Rational(1, 2),)},
        overlaps={("U0", "U0"): True},
        d0=d0,
        d1=d1,
        defect_cochain=defect,
        fda_license_granted=licensed,
    )

    outcome = evaluate_coda_pipeline(prob)

    print(f"Problem ID      : {outcome.problem_id}")
    print(f"Terminal Kind   : {outcome.terminal_kind.value}")
    print(f"Firewall Route  : {outcome.firewall_decision.value}")
    pair = outcome.residual_pair
    print(f"Phi_1 Defect    : {pair.phi1.sympy_rational if pair else 'unknown'}")
    print(f"Gamma_2 Defect  : {pair.gamma2.sympy_rational if pair else 'unknown'}")
    print(f"Authority Token : {'PRESENT' if outcome.is_authorized else 'NONE'}")
    print(f"Terminal Reason : {outcome.reason}")
    print("\nLayer Execution Audit Trail:")
    for rec in outcome.layer_records:
        status = "OK" if rec.succeeded else "FAIL"
        print(f"  - [{rec.layer_id.value:<5}] {status:<4} : {rec.diagnostic_message}")

    return 0


def cmd_stress_test(num_vertices: int = 20, chord_interval: int = 10, licensed: bool = False) -> int:
    """Executes an end-to-end stress test piping high-dimensional graph instances through CODA."""
    import time

    print("=" * 80)
    print(f"CODA HIGH-DIMENSIONAL GRAPH STRESS TEST (V={num_vertices}, Chord={chord_interval})")
    print("AuthorityEffect: None")
    print("=" * 80)

    t0 = time.perf_counter()
    prob = RustCrateBridge.generate_high_dim_graph_instance(
        num_vertices=num_vertices,
        chord_interval=chord_interval,
        licensed=licensed,
    )
    t_gen = time.perf_counter() - t0
    print(f"Graph Construction Completed in {t_gen:.4f}s | Vertices: {num_vertices}, Edges: {prob.d0.rows}")

    t1 = time.perf_counter()
    outcome = evaluate_coda_pipeline(prob)
    t_eval = time.perf_counter() - t1
    total_time = time.perf_counter() - t0

    print(f"9-Layer Pipeline Completed in    {t_eval:.4f}s | Total Runtime: {total_time:.4f}s")
    verdicts = []
    print("Runtime is a measurement of this run; no universal runtime bound is claimed.")
    print(f"Terminal Outcome                : {outcome.terminal_kind.value}")
    pair = outcome.residual_pair
    verdicts.append(pair is not None)
    print(f"Phi_1 Quotient Distance         : {pair.phi1.sympy_rational if pair else 'unknown (FAIL)'}")

    for name, valid, detail in _certificate_checks(prob, outcome):
        verdicts.append(valid)
        print(f"{name}: {'PASS' if valid else 'FAIL'} — {detail}")

    # Any FAIL verdict above is a failed run.
    return 0 if all(verdicts) else 1


def _vertex_count(text: str) -> int:
    try:
        value = int(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid vertex count {text!r}") from exc
    if value < 10:
        raise argparse.ArgumentTypeError("the stress test needs at least 10 vertices")
    return value


def _chord(text: str) -> int:
    try:
        value = int(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid chord interval {text!r}") from exc
    if value < 0:
        raise argparse.ArgumentTypeError("the chord interval must be non-negative")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="coda",
        description="CODA Application: Nine-Layer Obstruction & Authority Firewall Framework",
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("status", help="Display framework and Rust crate integration status")
    subparsers.add_parser("layers", help="List the 9 layers of CODA")

    eval_parser = subparsers.add_parser("evaluate", help="Evaluate a problem instance through the 9 layers")
    eval_parser.add_argument(
        "--licensed", action="store_true", help="Attach a bare license claim (refused: a flag never mints authority)"
    )
    eval_parser.add_argument("--obstructed", action="store_true", help="Inject non-zero quotient defect Phi_1 > 0")

    stress_parser = subparsers.add_parser("stress-test", help="Run a finite graph certificate check and record elapsed time")
    stress_parser.add_argument("--vertices", type=_vertex_count, default=20, help="Number of vertices, >= 10 (default: 20)")
    stress_parser.add_argument("--chord", type=_chord, default=10, help="Chordal bypass interval (default: 10)")
    stress_parser.add_argument("--licensed", action="store_true", help="Attach a bare license claim (never authorizes)")

    args = parser.parse_args(argv)

    if args.command == "status":
        return cmd_status()
    elif args.command == "layers":
        return cmd_layers()
    elif args.command == "evaluate":
        return cmd_evaluate(licensed=args.licensed, obstructed=args.obstructed)
    elif args.command == "stress-test":
        return cmd_stress_test(num_vertices=args.vertices, chord_interval=args.chord, licensed=args.licensed)
    else:
        parser.print_help(sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
