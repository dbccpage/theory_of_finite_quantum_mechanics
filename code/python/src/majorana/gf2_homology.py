"""Exact GF(2) homology group and quotient basis computation.

Computes H1 = ker(D1) / im(D0) over GF(2) from boundary matrices.

contract_id: urn:omega:math:chain_complex:v1.0.0
contract_id: urn:omega:math:cohomology:v1.0.0
"""
from __future__ import annotations


import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .gf2_matrix import GF2Matrix


@dataclass(frozen=True, slots=True)
class HomologyResult:
    """Result of GF(2) homology computation for H1.

    contract_id: urn:omega:math:cohomology:v1.0.0
    """
    rank_D0: int
    rank_D1: int
    dim_C1: int
    dim_H1: int
    basis_H1: tuple[tuple[int, ...], ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "rank_D0": self.rank_D0,
            "rank_D1": self.rank_D1,
            "dim_C1": self.dim_C1,
            "dim_H1": self.dim_H1,
            "basis_H1": [list(v) for v in self.basis_H1],
        }


def compute_homology(d0_data: list[list[int]], d1_data: list[list[int]]) -> HomologyResult:
    """Compute the homology group and a minimal homology basis for H1 over GF(2).

    contract_id: urn:omega:math:chain_complex:v1.0.0
    """
    d0_mat = GF2Matrix(d0_data)
    d1_mat = GF2Matrix(d1_data)

    dim_C1 = d0_mat.rows

    d0_t = d0_mat.transpose()
    rref_d0_t, _ = d0_t.rref()
    im_d0_basis = [row for row in rref_d0_t.to_list() if any(row)]
    rank_D0 = len(im_d0_basis)

    _, pivots_d1 = d1_mat.rref()
    rank_D1 = len(pivots_d1)

    ker_d1_basis = d1_mat.kernel_basis()
    dim_ker_D1 = len(ker_d1_basis)

    dim_H1 = dim_ker_D1 - rank_D0

    B = [list(v) for v in im_d0_basis]
    basis_H1: list[list[int]] = []

    for v in ker_d1_basis:
        if not B:
            B.append(v)
            basis_H1.append(v)
        else:
            A = GF2Matrix(B)
            A_T = A.transpose()
            if A_T.solve(v) is None:
                B.append(v)
                basis_H1.append(v)

    return HomologyResult(
        rank_D0=rank_D0,
        rank_D1=rank_D1,
        dim_C1=dim_C1,
        dim_H1=dim_H1,
        basis_H1=tuple(tuple(v) for v in basis_H1),
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Exact GF(2) homology group and quotient basis reporter"
    )
    parser.add_argument(
        "--carrier",
        type=Path,
        required=True,
        help="Path to JSON file containing the MajoranaParityCarrier",
    )
    args = parser.parse_args()

    try:
        with args.carrier.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if "D0" not in data and isinstance(data, list) and len(data) > 0:
            data = data[0]

        if "D0" not in data or "D1" not in data:
            print(json.dumps({"error": "Invalid carrier format. Missing D0 or D1."}, indent=2))
            return 1

        result = compute_homology(data["D0"], data["D1"])
        print(json.dumps(result.to_dict(), indent=2))
        return 0
    except Exception as e:
        print(json.dumps({"error": f"Homology calculation failed: {str(e)}"}, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
