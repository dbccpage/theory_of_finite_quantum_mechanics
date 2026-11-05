"""Propose or replay the three named Appendix X finite cost certificates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .bridge import COST_DOMAIN, propose_cost, verify_cost
from .examples import correlated_enclosure, separated, touching


def fixtures():
    return {
        "separated": separated(),
        "touching": touching(),
        "correlated_enclosure": correlated_enclosure(),
    }


def propose_bundle() -> dict:
    return {name: propose_cost(model) for name, model in fixtures().items()}


def verify_bundle(bundle: object) -> dict:
    models = fixtures()
    if type(bundle) is not dict or set(bundle) != set(models):
        raise ValueError("exact named fixture inventory required")
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


def _unique(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate JSON key")
        value[key] = item
    return value


def _no_float(value):
    raise ValueError(f"nonexact JSON number: {value}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--propose", type=Path)
    group.add_argument("--verify", type=Path)
    args = parser.parse_args()
    if args.propose:
        bundle = propose_bundle()
        args.propose.write_text(json.dumps(bundle, indent=2) + "\n", encoding="utf-8")
        print("Cost certificates proposed; replay them with --verify.")
    else:
        bundle = json.loads(
            args.verify.read_text(encoding="utf-8"),
            object_pairs_hook=_unique,
            parse_float=_no_float,
            parse_constant=_no_float,
        )
        print(
            json.dumps(
                {
                    "scope": COST_DOMAIN,
                    "bounded_raw_api_feasibility": "NOT_CERTIFIED",
                    "authority_effect": "None",
                    "checked_costs": verify_bundle(bundle),
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
