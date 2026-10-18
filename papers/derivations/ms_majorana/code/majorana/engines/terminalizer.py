from __future__ import annotations


import argparse
import json
from pathlib import Path
from typing import Any

from omega_engine.crates.majorana.core.gf2_schema import mod2
from omega_engine.crates.majorana.carriers.parity_carrier import MajoranaParityCarrier
from omega_engine.crates.majorana.core.gf2_diagnostic import classify_native, schedule_terminal
from omega_engine.crates.majorana.core.gf2_matrix import GF2Matrix


D0_DEMO = [[1], [1], [0]]
D1_DEMO = [[1, 1, 0]]
RESIDUALS_DEMO = {
    "exact": [1, 1, 0],
    "closed": [0, 0, 1],
    "open": [1, 0, 0],
}


def xor_vec(left: list[int], right: list[int]) -> list[int]:
    return [mod2(a + b) for a, b in zip(left, right)]


def hamming_weight(vector: list[int]) -> int:
    return sum(mod2(x) for x in vector)


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    if not matrix:
        return []
    return [[row[j] for row in matrix] for j in range(len(matrix[0]))]


def mat_vec_mul(matrix: list[list[int]], vector: list[int]) -> list[int]:
    return [
        mod2(sum(mod2(a) * mod2(b) for a, b in zip(row, vector)))
        for row in matrix
    ]


def validate_complex(d0: list[list[int]] | GF2Matrix, d1: list[list[int]] | GF2Matrix) -> bool:
    if not isinstance(d0, GF2Matrix):
        d0_mat = GF2Matrix(d0)
    else:
        d0_mat = d0
    if not isinstance(d1, GF2Matrix):
        d1_mat = GF2Matrix(d1, cols=d0_mat.rows)
    else:
        d1_mat = d1

    try:
        carrier = MajoranaParityCarrier(
            carrier_kind="majorana_parity_gf2",
            coefficient_field="GF2",
            D0=d0_mat.data,
            D1=d1_mat.data,
            residual=[0] * d0_mat.rows,
        ).normalized()
        carrier.validate_shape()
    except ValueError:
        return False

    for column in transpose(carrier.D0):
        if any(d1_mat.mat_vec_mul(column)):
            return False
    return True


def solve_exact(d0: list[list[int]] | GF2Matrix, residual: list[int]) -> list[int] | None:
    if not isinstance(d0, GF2Matrix):
        d0_mat = GF2Matrix(d0)
    else:
        d0_mat = d0
    return d0_mat.solve(residual)


def compute_coherence(d1: list[list[int]] | GF2Matrix, residual: list[int]) -> list[int]:
    if not isinstance(d1, GF2Matrix):
        d1_mat = GF2Matrix(d1, cols=len(residual))
    else:
        d1_mat = d1
    return d1_mat.mat_vec_mul(residual)


def normal_form_mod_image(
    d0: list[list[int]] | GF2Matrix,
    d1: list[list[int]] | GF2Matrix | None,
    residual: list[int]
) -> list[int]:
    if not isinstance(d0, GF2Matrix):
        d0_mat = GF2Matrix(d0)
    else:
        d0_mat = d0

    normal = [mod2(x) for x in residual]
    d0_t = d0_mat.transpose()
    rref_d0_t, _ = d0_t.rref()

    basis: list[list[int]] = []
    for r in range(rref_d0_t.rows):
        row = rref_d0_t[r]
        if any(row):
            basis.append(row)

    basis_pivots = []
    for vec in basis:
        pivot = next((i for i, x in enumerate(vec) if x), None)
        if pivot is not None:
            basis_pivots.append((pivot, vec))
    basis_pivots.sort(key=lambda x: x[0])

    for pivot, vec in basis_pivots:
        if normal[pivot]:
            normal = xor_vec(normal, vec)

    return normal


def terminalize(
    d0: list[list[int]] | GF2Matrix,
    d1: list[list[int]] | GF2Matrix,
    residual: list[int]
) -> dict[str, Any]:
    if not isinstance(d0, GF2Matrix):
        d0_mat = GF2Matrix(d0)
    else:
        d0_mat = d0
    if not isinstance(d1, GF2Matrix):
        d1_mat = GF2Matrix(d1, cols=d0_mat.rows)
    else:
        d1_mat = d1

    try:
        carrier = MajoranaParityCarrier(
            carrier_kind="majorana_parity_gf2",
            coefficient_field="GF2",
            D0=d0_mat.data,
            D1=d1_mat.data,
            residual=residual,
        ).normalized()
        carrier.validate_shape()
    except ValueError as exc:
        reason_slug = str(exc).lower().replace(" ", "_")
        return {
            "terminal_status": "RepresentationInvalid",
            "reason": str(exc),
            "certificate_alpha": None,
            "normal_form": None,
            "coherence_witness": None,
            "q1_norm": None,
            "algebraic_class_id": f"representation-invalid:{reason_slug}",
        }

    native = classify_native(d0_mat.data, d1_mat.data, carrier.residual)
    status = schedule_terminal(native["terminal"])
    if status == "RepresentationInvalid":
        return {
            "terminal_status": "RepresentationInvalid",
            "reason": "D1*D0 != 0",
            "certificate_alpha": None,
            "normal_form": None,
            "coherence_witness": None,
            "q1_norm": None,
            "algebraic_class_id": "representation-invalid:complex_relation_violation",
        }

    if status == "Exact":
        return {
            "terminal_status": "Exact",
            "reason": "residual lies in im(D0)",
            "certificate_alpha": native["certificate_alpha"],
            "normal_form": None,
            "coherence_witness": None,
            "q1_norm": 0,
            "algebraic_class_id": "exact",
        }

    if status == "OpenObstruction":
        witness = [mod2(bit) for bit in native["coherence_witness"]]
        normal_form = normal_form_mod_image(d0_mat, d1_mat, carrier.residual)
        witness_str = "".join(str(bit) for bit in witness)
        return {
            "terminal_status": "OpenObstruction",
            "reason": "D1*r != 0",
            "certificate_alpha": None,
            "normal_form": None,
            "coherence_witness": witness,
            "q1_norm": hamming_weight(normal_form),
            "algebraic_class_id": f"open-obstruction:{witness_str}",
        }

    normal_form = normal_form_mod_image(d0_mat, d1_mat, carrier.residual)
    nf_str = "".join(str(bit) for bit in normal_form)
    return {
        "terminal_status": "ClosedResidual",
        "reason": "r not in im(D0) and D1*r = 0",
        "certificate_alpha": None,
        "normal_form": normal_form,
        "coherence_witness": None,
        "q1_norm": hamming_weight(normal_form),
        "algebraic_class_id": f"closed-residual:{nf_str}",
    }

def demo_payload() -> dict[str, Any]:
    from omega_engine.crates.majorana.certificates.ledger import INTERPRETATIONS
    rows = {
        name: terminalize(D0_DEMO, D1_DEMO, residual)
        for name, residual in RESIDUALS_DEMO.items()
    }
    return {
        name: {
            "terminal_status": row["terminal_status"],
            "interpretation": INTERPRETATIONS.get(row["terminal_status"], ""),
            "certificate_alpha": row["certificate_alpha"],
            "normal_form": row["normal_form"],
            "coherence_witness": row["coherence_witness"],
            "q1_norm": str(row["q1_norm"]) if row["q1_norm"] is not None else "null",
        }
        for name, row in rows.items()
    }


def write_ledger(path: Path) -> None:
    from omega_engine.crates.majorana.certificates.ledger import ledger_row
    rows = [
        ledger_row(D0_DEMO, D1_DEMO, residual)
        for residual in RESIDUALS_DEMO.values()
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as output:
        for row in rows:
            output.write(json.dumps(row, allow_nan=False, sort_keys=True) + "\n")





def main() -> int:
    from omega_engine.crates.majorana.certificates.ledger import verify_ledger
    parser = argparse.ArgumentParser(
        description="GF(2) Majorana parity obstruction terminalizer"
    )
    parser.add_argument("--demo", action="store_true", help="print the three-case demo JSON")
    parser.add_argument("--write-ledger", type=Path, help="write replayable certificate ledger JSONL")
    parser.add_argument("--write-demo-json", type=Path, help="write demo output JSON")
    parser.add_argument("--verify-ledger", type=Path, help="verify a replayable certificate ledger JSONL")
    args = parser.parse_args()

    payload = demo_payload()

    if args.write_ledger is not None:
        write_ledger(args.write_ledger)

    if args.write_demo_json is not None:
        args.write_demo_json.parent.mkdir(parents=True, exist_ok=True)
        args.write_demo_json.write_text(
            json.dumps(payload, allow_nan=False, indent=2, sort_keys=False) + "\n",
            encoding="utf-8",
        )

    if args.demo:
        print(json.dumps(payload, allow_nan=False, indent=2, sort_keys=False))

    if args.verify_ledger is not None:
        result = verify_ledger(args.verify_ledger)
        print(json.dumps(result, allow_nan=False, indent=2, sort_keys=True))
        return 0 if result["verified"] else 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())




