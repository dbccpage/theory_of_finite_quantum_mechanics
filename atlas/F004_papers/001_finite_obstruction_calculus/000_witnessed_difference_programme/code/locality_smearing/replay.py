"""Generate or independently replay finite exact witnesses, without model calls.

python -m locality_smearing.replay generate
python -m locality_smearing.replay check
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from fractions import Fraction as Q
from pathlib import Path

from certified_progress.replay import regular, strict_json
from witnessed_difference.exact_linear import ExactField, congruence_diagonalize
from witnessed_difference.outcomes import Accepted

from .car import exchange_cycle, response
from .checker import check_alternating, check_congruence, check_recovery, check_subdivision
from .finite import (
    alternating_average,
    differences,
    exponential_envelope,
    observation_completion,
    positive_threshold,
    primitive,
    subdivide,
    time_consistency_constant,
)
from .locality import check_locality, fixture

ROOT = Path(__file__).resolve().parents[2]
RECEIPT = ROOT / "code" / "locality_smearing" / "examples.json"


def rational_matrix(matrix):
    return [[str(x) for x in row] for row in matrix.tolist()]


def congruence(matrix):
    rows = tuple(tuple(Q(str(x)) for x in row) for row in matrix.tolist())
    result = congruence_diagonalize(rows, ExactField.RATIONAL)
    if not isinstance(result, Accepted):
        raise ValueError(result)
    c = result.value
    return {
        "basis": [[str(x) for x in row] for row in c.basis],
        "diagonal": [str(x) for x in c.diagonal],
    }, list(c.inertia)


def source_hashes():
    paths = sorted((ROOT / "code" / "locality_smearing").rglob("*.py"))
    paths += sorted((ROOT / "docs" / "source_archive" / "locality_and_smearing").glob("*"))
    paths += [ROOT / "docs" / "meron_field_limit_derivations" / "code" / "gate_e_exact_counterexample.py"]
    paths += [ROOT / "code/trotter_characteristic_polynomials.py"]
    paths += [ROOT / "lean4" / "WitnessedDifference" / "CARResponseWitness.lean"]
    return {p.relative_to(ROOT).as_posix(): hashlib.sha256(regular(p)).hexdigest() for p in paths}


def generate():
    import sympy as sp

    matrices = []
    for m in range(1, 5):
        data = response(m)
        cert, inertia = congruence(data["matrix"])
        matrices.append(
            {
                "M": m,
                "theta": str(data["theta"]),
                "step_r": str(data["step_r"]),
                "partition": str(data["partition"]),
                "staggered_eigenvalue": str(data["eigenvalue"]),
                "matrix": rational_matrix(data["matrix"]),
                "congruence": cert,
                "inertia": inertia,
            }
        )
    errors = tuple((i & 1, (i >> 1) & 1, (i >> 2) & 1) for i in range(8))
    repairs = ((0, 0, 0), (1, 1, 0))
    rows = ((1, 1, 0),)
    extra = observation_completion(rows, errors, repairs)
    samples = [[str(Q(j, 8))] * 4 for j in range(8)]
    local = fixture()
    rho, sigma, near, op = [
        sp.Matrix([[sp.Rational(x) for x in row] for row in local[k]])
        for k in ("rho", "sigma", "near", "operator")
    ]
    beta = sp.Rational(local["beta"])
    forms = {
        "rho": rho,
        "sigma": sigma,
        "upper": beta * sp.eye(4) + op - near,
        "lower": beta * sp.eye(4) - op + near,
    }
    local_certificate = {
        "forms": {name: congruence(a)[0] for name, a in forms.items()},
        "readout_difference": "1/4",
    }
    a_bound = time_consistency_constant(Q(1, 10), 4, 1, 0)
    margin = 1 / (4 * exponential_envelope(Q(1, 10), 4))
    return {
        "schema": "wdp-locality-smearing-examples-v1",
        "authority_effect": "None",
        "source_hashes": source_hashes(),
        "car": matrices,
        "exchange": exchange_cycle(),
        "locality": {"problem": local, "certificate": local_certificate},
        "time_limit": {
            "profile": "constant-one-on-each-site",
            "theta": "1/10",
            "L": 4,
            "amplitude_bound": "1",
            "derivative_bound": "0",
            "error_numerator": str(a_bound),
            "positive_margin": str(margin),
            "strict_M0": positive_threshold(a_bound, margin),
        },
        "completion": {
            "syndrome": rows,
            "errors": errors,
            "repairs": repairs,
            "certificate": extra,
        },
        "smearing": {
            "samples": samples,
            "derivative_bound": "1",
            "average": str(alternating_average(samples)),
        },
        "cochain": {
            "values": ["1", "-1", "-1", "1"],
            "primitive": list(map(str, primitive([1, -1, -1, 1]))),
            "subdivision": list(map(str, subdivide([1, -1, -1, 1], 3))),
            "factor": 3,
        },
    }


def check(data):
    if data.get("source_hashes") != source_hashes() or data.get("authority_effect") != "None":
        raise ValueError("source bytes or authority binding changed")
    if data.get("schema") != "wdp-locality-smearing-examples-v1":
        raise ValueError("unknown receipt schema")
    if [r["M"] for r in data["car"]] != [1, 2, 3, 4]:
        raise ValueError("missing retained CAR instance")
    for row in data["car"]:
        # Original declared parameters, never parameters extracted from the certificate.
        original = response(row["M"])
        if (
            row["theta"] != "1/10"
            or row["step_r"] != str(original["step_r"])
            or row["partition"] != str(original["partition"])
            or row["matrix"] != rational_matrix(original["matrix"])
            or row["staggered_eigenvalue"] != str(original["eigenvalue"])
            or not check_congruence(row["matrix"], row["congruence"])
        ):
            raise ValueError("CAR input, witness, or eigenvalue changed")
        diagonal = list(map(Q, row["congruence"]["diagonal"]))
        inertia = [
            sum(x > 0 for x in diagonal),
            sum(x < 0 for x in diagonal),
            sum(x == 0 for x in diagonal),
        ]
        if row["inertia"] != inertia or inertia != [4 * row["M"], 1, 4 * row["M"] - 1]:
            raise ValueError("incorrect finite inertia")
    lean = regular(ROOT / "lean4/WitnessedDifference/CARResponseWitness.lean").decode("utf-8")
    den = int(re.search(r"def denominator : Int := (\d+)", lean)[1])
    scaled = json.loads(
        re.search(r"def scaledMatrix : List \(List Int\) := (\[.*?\n\])", lean, re.S)[1]
    )
    if den != 2825760 or scaled != [[Q(x) * den for x in row] for row in data["car"][0]["matrix"]]:
        raise ValueError("formal integer matrix differs from actual CAR response")
    # JSON converts tuple moves to lists; compare canonicalized exact exchange data.
    ex = json.loads(json.dumps(exchange_cycle(), default=int))
    if data["exchange"] != ex or ex["product"] != -1:
        raise ValueError("changed CAR exchange")
    if data["locality"]["problem"] != fixture() or not check_locality(
        fixture(), data["locality"]["certificate"]
    ):
        raise ValueError("locality task or submitted norm witness changed")
    # Independent rational consequence checker for the written analytic envelope.
    # It checks arithmetic/premises, not the analytic proof by numerically sampling.
    t = data["time_limit"]
    theta = Q(1, 10)
    e4, e16 = (1 - theta / 8) ** (-32), (1 - theta / 2) ** (-32)
    a_bound = 4 * (30 * (theta + theta * theta) * e16 + 2 * theta * e4)
    margin = 1 / (4 * e4)
    expected = {
        "profile": "constant-one-on-each-site",
        "theta": "1/10",
        "L": 4,
        "amplitude_bound": "1",
        "derivative_bound": "0",
        "error_numerator": str(a_bound),
        "positive_margin": str(margin),
        "strict_M0": max(1, a_bound // margin + 1),
    }
    if t != expected or not t["strict_M0"] * margin > a_bound:
        raise ValueError("wrong profile, margin, normalization or strict time threshold")
    c = data["completion"]
    rows, errors, repairs = map(
        lambda x: tuple(map(tuple, x)), (c["syndrome"], c["errors"], c["repairs"])
    )
    cert = c["certificate"]
    if (
        rows != ((1, 1, 0),)
        or errors != tuple((i & 1, (i >> 1) & 1, (i >> 2) & 1) for i in range(8))
        or repairs != ((0, 0, 0), (1, 1, 0))
    ):
        raise ValueError("completion original input changed")
    if (
        cert["minimum"] != 1
        or len(cert["extra_rows"]) != 1
        or not check_recovery(
            (*rows, *map(tuple, cert["extra_rows"])), errors, repairs, cert["decoder"]
        )
    ):
        raise ValueError("invalid upper completion witness")
    # Independent lower certificate: the original observer collides on 000 and 001.
    if not check_recovery(
        rows, errors, repairs, {"kind": "collision", "left": [0, 0, 0], "right": [0, 0, 1]}
    ):
        raise ValueError("missing lower completion obstruction")
    s = data["smearing"]
    expected_samples = [[str(Q(j, 8))] * 4 for j in range(8)]
    if (
        s["samples"] != expected_samples
        or s["derivative_bound"] != "1"
        or not check_alternating(s["samples"], s["derivative_bound"], s["average"])
    ):
        raise ValueError("invalid smearing witness")
    c = data["cochain"]
    if (
        c["values"] != ["1", "-1", "-1", "1"]
        or c["factor"] != 3
        or not check_subdivision(c["values"], c["factor"], c["subdivision"])
        or differences(c["primitive"]) != tuple(map(Q, c["values"]))
    ):
        raise ValueError("invalid cochain witness")
    if data["source_hashes"] != source_hashes():
        raise ValueError("source changed during replay")
    return {
        "accepted": True,
        "car_instances": 4,
        "provider_calls": 0,
        "scope": "finite exact matrices, syndrome decoder, pairing and cochain witnesses",
        "authority_effect": "None",
    }


def main():
    if sys.argv[1:] == ["generate"]:
        data = generate()
        RECEIPT.write_text(
            json.dumps(data, indent=2, default=int) + "\n", encoding="utf-8", newline="\n"
        )
    elif sys.argv[1:] != ["check"]:
        raise SystemExit(__doc__)
    data = strict_json(regular(RECEIPT))
    print(json.dumps(check(data), indent=2))


if __name__ == "__main__":
    main()
