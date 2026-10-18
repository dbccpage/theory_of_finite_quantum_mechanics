"""CLI for DDA demos and Prime 000 admission (OE-000 7-step)."""

from __future__ import annotations
import argparse
import json

from omega_engine.crates.prime.prime_000 import (
    DeclarationPacket,
    admit_declaration,
)
from omega_engine.crates.discrete_deformation_algebra.dda_demos import ALL_DDA_DEMOS


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="omega_engine.dda")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="List DDA and Prime demos")
    sub.add_parser("dda-demos", help="Run DDA fused-spec demos 1–9")
    sub.add_parser("prime000", help="Run a complete Prime 000 declaration (OE-000)")
    sub.add_parser(
        "rabbit-intake", help="Run Rabbit prompt intake stack and DDA trace lowering"
    )

    args = p.parse_args(argv)

    if args.cmd == "list":
        print("dda demos: 1..9")
        print("prime000, rabbit-intake")
        return 0

    if args.cmd == "dda-demos":
        out = [fn() for fn in ALL_DDA_DEMOS]
        print(json.dumps(out, indent=2))
        return 0

    if args.cmd == "rabbit-intake":
        from omega_engine.crates.discrete_deformation_algebra.rabbit_intake import RabbitIntakePipeline

        pipeline = RabbitIntakePipeline()
        packets = pipeline.build_diagnostic_packet_bundle()
        engine, tape = pipeline.execute_admitted_dda_trace()
        print(
            json.dumps(
                {
                    "prompt": pipeline.prompt,
                    "diagnostic_packet_count": len(packets),
                    "emitted_families": [p.family_id for p in packets],
                    "dda_tape": tape,
                    "terminalized": engine.is_terminalized,
                    "authority_effect": "None",
                },
                indent=2,
            )
        )
        return 0

    if args.cmd == "prime000":
        pkt = DeclarationPacket(
            domain="demo",
            locus_hash="sha256:demo_locus",
            carrier="C_fin",
            observer="obs_declared",
            primitive_difference="delta_0",
            zero_rel="exact_eq",
            witness="w1",
        )
        decision = admit_declaration(pkt)
        print(
            json.dumps(
                {
                    "kind": decision.kind.value,
                    "reason": decision.reason,
                    "filled_steps": list(decision.filled_steps),
                    "steps": list(decision.steps),
                    "authority_effect": decision.authority_effect,
                },
                indent=2,
                default=str,
            )
        )
        return 0

    return 0


