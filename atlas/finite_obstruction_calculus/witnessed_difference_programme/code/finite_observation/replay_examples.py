"""Construct or independently replay the finite observation demonstration bundle."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path

from .solver import Instance, Instrument, instance_data, solve, verify, verify_lp_pair


def adaptive_instance(*, submitted: bool = False) -> Instance:
    first = (0, 1, 0, 1, 0, 0, 1, 1) if submitted else (0, 0, 0, 0, 1, 1, 1, 1)
    return Instance(
        tuple(str(i) for i in range(1, 9)), ("*",) * 8,
        ("1", "1", "2", "2", "3", "3", "4", "4"),
        tuple(Instrument(name, tuple(map(str, values)), F(price)) for name, values, price in (
            ("A", first, 1), ("B", (0, 0, 1, 1, 0, 0, 0, 0), 3),
            ("C", (0, 0, 0, 0, 0, 0, 1, 1), 3))),
    )


def fano_instance() -> Instance:
    lines = ((0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5))
    return Instance(
        ("*",) + tuple(str(i) for i in range(7)), ("*",) * 8, ("0",) + ("1",) * 7,
        tuple(Instrument(str(i), ("0",) + tuple(str(int(point in line)) for point in range(7)), F(1))
              for i, line in enumerate(lines)),
    )


def fixtures() -> dict[str, Instance]:
    return {
        "adaptive_corrected": adaptive_instance(),
        "adaptive_submitted_infeasible": adaptive_instance(submitted=True),
        "fano_integrality_gap": fano_instance(),
        "infeasible_miniature": Instance(("1", "2", "3"), ("*",) * 3, ("0", "1", "0"),
                                        (Instrument("m1", ("0", "0", "1"), F(1)), Instrument("m2", ("0", "0", "1"), F(1)))),
        "visible_report_resolves": Instance(("0", "1"), ("0", "1"), ("0", "1"), ()),
    }


def build_bundle() -> dict:
    return {name: {"input": instance_data(instance), "certificate": solve(instance)} for name, instance in fixtures().items()}


def replay_bundle(bundle: object) -> dict:
    expected = fixtures()
    if type(bundle) is not dict or set(bundle) != set(expected):
        raise ValueError("bundle must contain each named fixture exactly once")
    summary = {}
    for name, instance in expected.items():
        row = bundle[name]
        if type(row) is not dict or set(row) != {"input", "certificate"} or row["input"] != instance_data(instance):
            raise ValueError(f"{name}: substituted input or malformed bundle row")
        checked = verify(instance, row["certificate"])
        if not checked.accepted:
            raise ValueError(f"{name}: {checked.code}: {checked.detail}")
        summary[name] = {"fixed": row["certificate"]["fixed"]["value"], "adaptive": row["certificate"]["adaptive"]["value"],
                         "infeasible_pair": row["certificate"]["infeasible_pair"]}
    summary["fano_integrality_gap"]["lp_optimum"] = str(verify_lp_pair(fano_instance(), (F(1, 3),) * 7, (F(1, 3),) * 7))
    return summary


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _reject_number(value: str) -> None:
    raise ValueError(f"nonexact JSON number {value}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", type=Path, help="write the complete proposed certificate bundle")
    group.add_argument("--check", type=Path, help="replay submitted bundle without generating replacement certificates")
    args = parser.parse_args()
    if args.check:
        bundle = json.loads(args.check.read_text(encoding="utf-8"), object_pairs_hook=_unique_object,
                            parse_float=_reject_number, parse_constant=_reject_number)
    else:
        bundle = build_bundle()
    summary = replay_bundle(bundle)
    if args.write:
        args.write.write_text(json.dumps(bundle, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": "VERIFIED", "authority_effect": "None", "examples": summary}, indent=2))


if __name__ == "__main__":
    main()
