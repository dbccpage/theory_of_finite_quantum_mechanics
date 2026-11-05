"""Propose or replay exact finite certificates for the joint-support examples."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from calibrated_recovery.replay import _no_float, _unique

from .examples import isolated_collision, isolated_cost_peak, parity_points, shared_error
from .reference import propose_cost, verify_cost


def fixtures():
    return {
        "shared_error": shared_error(),
        "isolated_collision": isolated_collision(),
        "parity_points": parity_points(),
        "isolated_cost_peak": isolated_cost_peak(),
    }


def propose_bundle() -> dict:
    return {name: propose_cost(model) for name, model in fixtures().items()}


def verify_bundle(bundle: object) -> dict:
    models = fixtures()
    if type(bundle) is not dict or set(bundle) != set(models):
        raise ValueError("exact named joint-support inventory required")
    result = {}
    for name, model in models.items():
        checked = verify_cost(model, bundle[name])
        if not checked.accepted:
            raise ValueError(f"{name}: {checked.code}: {checked.detail}")
        certificate = bundle[name]["finite_certificate"]
        result[name] = {
            "fixed": certificate["fixed"]["value"],
            "adaptive": certificate["adaptive"]["value"],
        }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--propose", type=Path)
    group.add_argument("--verify", type=Path)
    args = parser.parse_args()
    if args.propose:
        args.propose.write_text(json.dumps(propose_bundle(), indent=2) + "\n", encoding="utf-8")
        print("Joint-support cost certificates proposed; replay with --verify.")
    else:
        bundle = json.loads(
            args.verify.read_text(encoding="utf-8"),
            object_pairs_hook=_unique,
            parse_float=_no_float,
            parse_constant=_no_float,
        )
        print(
            json.dumps(
                {"authority_effect": "None", "checked_costs": verify_bundle(bundle)}, indent=2
            )
        )


if __name__ == "__main__":
    main()
