"""Exact rational Hubbard auxiliary-field determinants and finite lattice scaling benchmark.

Status: Discrete Mathematical & Computational Model
AuthorityEffect: None
Matches code/rust/src/fsp/hubbard.rs bit-for-bit.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import json
from typing import Any, Dict, List, Sequence, Tuple


def exact_determinant(mat: Sequence[Sequence[Fraction]]) -> Fraction:
    """Exact rational matrix determinant via Gaussian elimination over Q."""
    n = len(mat)
    if n == 0:
        return Fraction(1)
    for row in mat:
        if len(row) != n:
            raise ValueError("matrix must be square for determinant")

    a: List[List[Fraction]] = [[Fraction(x) for x in row] for row in mat]
    det = Fraction(1)
    sign_flips = 0

    for col in range(n):
        pivot_row = None
        for row in range(col, n):
            if a[row][col] != 0:
                pivot_row = row
                break
        if pivot_row is None:
            return Fraction(0)

        if pivot_row != col:
            a[col], a[pivot_row] = a[pivot_row], a[col]
            sign_flips ^= 1

        p_val = a[col][col]
        det *= p_val

        for r in range(col + 1, n):
            if a[r][col] != 0:
                factor = a[r][col] / p_val
                for c in range(col, n):
                    a[r][c] -= factor * a[col][c]

    if sign_flips == 1:
        det = -det
    return det


def exact_matrix_mul(
    a: Sequence[Sequence[Fraction]],
    b: Sequence[Sequence[Fraction]],
) -> List[List[Fraction]]:
    """Multiply two square matrices over Q."""
    n = len(a)
    if n == 0 or len(b) != n:
        raise ValueError("matrix dimension mismatch in multiplication")
    for row in a:
        if len(row) != n:
            raise ValueError("matrix A is not square")
    for row in b:
        if len(row) != n:
            raise ValueError("matrix B is not square")

    c = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        row_a = a[i]
        row_c = c[i]
        for k in range(n):
            aik = row_a[k]
            if aik == 0:
                continue
            row_b = b[k]
            for j in range(n):
                bkj = row_b[j]
                if bkj != 0:
                    row_c[j] += aik * bkj
    return c


def exact_kinetic_matrix(
    sites: int,
    bonds: Sequence[Tuple[int, int]],
    r: Fraction,
) -> List[List[Fraction]]:
    """Compute palindromic kinetic matrix over Q:
    Product of bond exponentials in forward then reverse order:
    K = prod_e B_e * prod_{e^rev} B_e
    where r = exp(dtau * t / 2) is an exact rational parameter.
    """
    if sites <= 0:
        raise ValueError("sites must be positive")
    r_frac = Fraction(r)
    if r_frac <= 0:
        raise ValueError("r parameter must be strictly positive")

    r_inv = Fraction(1) / r_frac
    cosh_val = (r_frac + r_inv) / Fraction(2)
    sinh_val = (r_frac - r_inv) / Fraction(2)

    k_mat = [[Fraction(int(i == j)) for j in range(sites)] for i in range(sites)]
    schedule = list(bonds) + list(reversed(bonds))

    for u, v in schedule:
        if u < 0 or v < 0 or u >= sites or v >= sites or u == v:
            raise ValueError("invalid bond endpoint")
        b = [[Fraction(int(i == j)) for j in range(sites)] for i in range(sites)]
        b[u][u] = cosh_val
        b[v][v] = cosh_val
        b[u][v] = sinh_val
        b[v][u] = sinh_val
        k_mat = exact_matrix_mul(b, k_mat)

    return k_mat


@dataclass(frozen=True)
class HubbardDeterminantReceipt:
    mask: int
    det_up: Fraction
    det_down: Fraction
    total_weight: Fraction
    is_strictly_positive: bool
    attractive_symmetry_holds: bool


@dataclass(frozen=True)
class HubbardEnsembleSummary:
    sites: int
    slices: int
    total_fields: int
    negative_fields_count: int
    zero_fields_count: int
    total_determinant_sum: Fraction
    absolute_determinant_sum: Fraction
    average_sign: Fraction
    attractive_square_root_protected: bool


def evaluate_hubbard_determinants(
    sites: int,
    bonds: Sequence[Tuple[int, int]],
    slices: int,
    r: Fraction,
    hs: Fraction,
    fugacity: Fraction,
    attractive: bool,
    field_masks: Sequence[int],
) -> HubbardEnsembleSummary:
    """Compute exact auxiliary-field Hubbard determinants for declared field masks."""
    if sites <= 0 or slices <= 0:
        raise ValueError("sites and slices must be positive")
    if not field_masks:
        raise ValueError("at least one field mask required")

    r_frac = Fraction(r)
    hs_frac = Fraction(hs)
    fug_frac = Fraction(fugacity)

    k_mat = exact_kinetic_matrix(sites, bonds, r_frac)
    total_sum = Fraction(0)
    abs_sum = Fraction(0)
    neg_count = 0
    zero_count = 0
    all_attractive_protected = True

    for mask in field_masks:
        b_up = [[Fraction(int(i == j)) for j in range(sites)] for i in range(sites)]
        b_down = [[Fraction(int(i == j)) for j in range(sites)] for i in range(sites)]

        for time in range(slices):
            v_up = [[Fraction(0) for _ in range(sites)] for _ in range(sites)]
            v_down = [[Fraction(0) for _ in range(sites)] for _ in range(sites)]

            for j in range(sites):
                bit = (mask >> (time * sites + j)) & 1
                s_val = 1 if bit == 1 else -1
                exp_up = s_val
                exp_down = s_val if attractive else -s_val

                hs_up = hs_frac if exp_up == 1 else (Fraction(1) / hs_frac)
                hs_down = hs_frac if exp_down == 1 else (Fraction(1) / hs_frac)

                v_up[j][j] = fug_frac * hs_up
                v_down[j][j] = fug_frac * hs_down

            slice_up = exact_matrix_mul(k_mat, v_up)
            slice_down = exact_matrix_mul(k_mat, v_down)

            b_up = exact_matrix_mul(slice_up, b_up)
            b_down = exact_matrix_mul(slice_down, b_down)

        for i in range(sites):
            b_up[i][i] += Fraction(1)
            b_down[i][i] += Fraction(1)

        det_up = exact_determinant(b_up)
        det_down = exact_determinant(b_down)

        symmetry_holds = (det_up == det_down) if attractive else True
        if attractive and not symmetry_holds:
            all_attractive_protected = False

        weight = det_up * det_down
        if weight == 0:
            zero_count += 1
        elif weight < 0:
            neg_count += 1

        total_sum += weight
        abs_sum += abs(weight)

    avg_sign = Fraction(0) if abs_sum == 0 else (total_sum / abs_sum)

    return HubbardEnsembleSummary(
        sites=sites,
        slices=slices,
        total_fields=len(field_masks),
        negative_fields_count=neg_count,
        zero_fields_count=zero_count,
        total_determinant_sum=total_sum,
        absolute_determinant_sum=abs_sum,
        average_sign=avg_sign,
        attractive_square_root_protected=(all_attractive_protected and attractive),
    )


@dataclass(frozen=True)
class HubbardLatticeScalingRow:
    """Exact rational Hubbard determinant scaling row matching Rust HubbardLatticeScalingRow."""
    label: str
    sites: int
    num_bonds: int
    slices: int
    attractive: bool
    evaluated_fields: int
    negative_fields_count: int
    zero_fields_count: int
    average_sign: Fraction
    attractive_square_root_protected: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "label": self.label,
            "sites": self.sites,
            "num_bonds": self.num_bonds,
            "slices": self.slices,
            "attractive": self.attractive,
            "evaluated_fields": self.evaluated_fields,
            "negative_fields_count": self.negative_fields_count,
            "zero_fields_count": self.zero_fields_count,
            "average_sign": str(self.average_sign),
            "attractive_square_root_protected": self.attractive_square_root_protected,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HubbardLatticeScalingRow":
        return cls(
            label=str(data["label"]),
            sites=int(data["sites"]),
            num_bonds=int(data["num_bonds"]),
            slices=int(data["slices"]),
            attractive=bool(data["attractive"]),
            evaluated_fields=int(data["evaluated_fields"]),
            negative_fields_count=int(data["negative_fields_count"]),
            zero_fields_count=int(data["zero_fields_count"]),
            average_sign=Fraction(str(data["average_sign"])),
            attractive_square_root_protected=bool(data["attractive_square_root_protected"]),
        )


def hubbard_rectangular_bonds(
    rows: int,
    cols: int,
    periodic: bool = False,
) -> Tuple[int, List[Tuple[int, int]]]:
    """Construct 2D rectangular grid bonds (rows x cols sites) with optional periodic wrapping."""
    if rows <= 0 or cols <= 0:
        raise ValueError("rows and cols must be positive")
    sites = rows * cols
    bonds: List[Tuple[int, int]] = []
    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c
            if c + 1 < cols:
                bonds.append((idx, r * cols + (c + 1)))
            elif periodic and cols > 2:
                bonds.append((idx, r * cols))
            if r + 1 < rows:
                bonds.append((idx, (r + 1) * cols + c))
            elif periodic and rows > 2:
                bonds.append((idx, c))
    return sites, bonds


def benchmark_hubbard_lattice_scaling() -> List[HubbardLatticeScalingRow]:
    """Finite lattice scaling benchmark for exact rational Hubbard auxiliary-field determinants
    across 1D rings and 2D grids up to 3x4 (12 sites) and multiple Trotter slices.
    Matches Rust tfqm_fsp::benchmark_hubbard_lattice_scaling bit-for-bit.
    """
    r = Fraction(3, 2)
    hs = Fraction(2)
    unit_fugacity = Fraction(1)
    doped_fugacity = Fraction(3, 5)

    _, bonds_2x2 = hubbard_rectangular_bonds(2, 2, False)
    _, bonds_2x3 = hubbard_rectangular_bonds(2, 3, False)
    _, bonds_2x4 = hubbard_rectangular_bonds(2, 4, False)
    _, bonds_3x3 = hubbard_rectangular_bonds(3, 3, False)
    _, bonds_3x4 = hubbard_rectangular_bonds(3, 4, False)
    _, bonds_1x10 = hubbard_rectangular_bonds(1, 10, True)

    frust_2x3 = list(bonds_2x3) + [(0, 4), (1, 5)]
    frust_3x3 = list(bonds_3x3) + [(0, 4), (4, 8)]

    def sample_masks(sites: int, slices: int) -> List[int]:
        total_bits = min(sites * slices, 62)
        all_ones = (1 << total_bits) - 1
        alt_a = 0x5555_5555 & all_ones
        alt_b = 0xAAAA_AAAA & all_ones
        return [
            0,
            1,
            (1 << min(sites, total_bits)) - 1,
            alt_a,
            alt_b,
            all_ones,
        ]

    configs: List[Tuple[str, int, List[Tuple[int, int]], int, Fraction, bool]] = [
        ("plaquette_2x2_attractive", 4, bonds_2x2, 2, unit_fugacity, True),
        ("grid_2x3_attractive", 6, bonds_2x3, 2, unit_fugacity, True),
        ("grid_2x4_attractive", 8, bonds_2x4, 2, unit_fugacity, True),
        ("grid_3x3_attractive", 9, bonds_3x3, 1, unit_fugacity, True),
        ("ring_10_attractive", 10, bonds_1x10, 1, unit_fugacity, True),
        ("grid_3x4_attractive", 12, bonds_3x4, 1, unit_fugacity, True),
        ("frustrated_2x3_repulsive_doped", 6, frust_2x3, 2, doped_fugacity, False),
        ("frustrated_3x3_repulsive_doped", 9, frust_3x3, 1, doped_fugacity, False),
    ]

    rows: List[HubbardLatticeScalingRow] = []
    for label, sites, bonds, slices, fugacity, attractive in configs:
        masks = sample_masks(sites, slices)
        summary = evaluate_hubbard_determinants(
            sites=sites,
            bonds=bonds,
            slices=slices,
            r=r,
            hs=hs,
            fugacity=fugacity,
            attractive=attractive,
            field_masks=masks,
        )
        rows.append(
            HubbardLatticeScalingRow(
                label=label,
                sites=sites,
                num_bonds=len(bonds),
                slices=slices,
                attractive=attractive,
                evaluated_fields=summary.total_fields,
                negative_fields_count=summary.negative_fields_count,
                zero_fields_count=summary.zero_fields_count,
                average_sign=summary.average_sign,
                attractive_square_root_protected=summary.attractive_square_root_protected,
            )
        )
    return rows


def hubbard_scaling_to_canonical_json(rows: Sequence[HubbardLatticeScalingRow]) -> str:
    """Serialize HubbardLatticeScalingRow list to canonical 2-space pretty JSON with LF line endings."""
    return json.dumps([row.to_dict() for row in rows], indent=2)


def hubbard_scaling_from_canonical_json(json_str: str) -> List[HubbardLatticeScalingRow]:
    """Deserialize HubbardLatticeScalingRow list from canonical JSON string."""
    raw = json.loads(json_str)
    return [HubbardLatticeScalingRow.from_dict(item) for item in raw]
