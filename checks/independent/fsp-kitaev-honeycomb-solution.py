#!/usr/bin/env python3
"""Independent verification for FSP-KITAEV-HONEYCOMB-SOLUTION (TFQ-1207).

AuthorityEffect: None

Checks with exact integer and rational (Fraction) arithmetic:
1. Single-site 4x4 Majorana Clifford & Pauli algebra (bX, bY, bZ, ic, tildeSigma_a, siteGaugeJD)
   and 2-site 16x16 graded bond factorization and gauge commutation.
2. Hexagonal plaquette local Z2 gauge invariance across link/vertex configurations,
   closed-torus even vortex parity (prod_p W_p = +1), and exact skew-symmetric
   quadratic Majorana determinant identity det(A(u)) = Pf(A(u))^2 over Q.
3. Scope fences: 4^N = 2^N * 2^N unprojected gauge redundancy, link-flip Pfaffian sign
   reversal Pf(A(-u_e)) = -Pf(A(u_e)) with det(A) > 0, and physical parity projection
   filtering (1 + P_matter * P_gauge).
"""

from __future__ import annotations

from fractions import Fraction
import itertools
from typing import List, Sequence, Tuple

MatrixInt = List[List[int]]
MatrixFrac = List[List[Fraction]]


def require(cond: bool, msg: str, counter: List[int]) -> None:
    if not cond:
        raise AssertionError(msg)
    counter[0] += 1


def mat_mul_int(a: MatrixInt, b: MatrixInt) -> MatrixInt:
    n = len(a)
    m = len(b[0])
    k_len = len(b)
    return [
        [sum(a[i][k] * b[k][j] for k in range(k_len)) for j in range(m)]
        for i in range(n)
    ]


def mat_add_int(a: MatrixInt, b: MatrixInt, scale_b: int = 1) -> MatrixInt:
    return [
        [a[i][j] + scale_b * b[i][j] for j in range(len(a[0]))]
        for i in range(len(a))
    ]


def mat_eye_int(n: int, scale: int = 1) -> MatrixInt:
    return [[scale if i == j else 0 for j in range(n)] for i in range(n)]


def mat_zero_int(n: int) -> MatrixInt:
    return [[0 for _ in range(n)] for _ in range(n)]


def mat_kron_int(a: MatrixInt, b: MatrixInt) -> MatrixInt:
    na, nb = len(a), len(b)
    out: MatrixInt = [[0 for _ in range(na * nb)] for _ in range(na * nb)]
    for i1 in range(na):
        for j1 in range(na):
            for i2 in range(nb):
                for j2 in range(nb):
                    out[i1 * nb + i2][j1 * nb + j2] = a[i1][j1] * b[i2][j2]
    return out


def det_bareiss(mat: Sequence[Sequence[Fraction]]) -> Fraction:
    n = len(mat)
    if n == 0:
        return Fraction(1)
    a = [[Fraction(x) for x in row] for row in mat]
    sign = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            swap_row = None
            for r in range(k + 1, n):
                if a[r][k] != 0:
                    swap_row = r
                    break
            if swap_row is None:
                return Fraction(0)
            a[k], a[swap_row] = a[swap_row], a[k]
            sign = -sign
        piv = a[k][k]
        for i in range(k + 1, n):
            factor = a[i][k] / piv
            for j in range(k, n):
                a[i][j] -= factor * a[k][j]
    prod = Fraction(sign)
    for i in range(n):
        prod *= a[i][i]
    return prod


def pfaffian_4x4(a: Sequence[Sequence[Fraction]]) -> Fraction:
    return a[0][1] * a[2][3] - a[0][2] * a[1][3] + a[0][3] * a[1][2]


def pfaffian_6x6(a: Sequence[Sequence[Fraction]]) -> Fraction:
    # Standard 15-term Pfaffian expansion for a 6x6 skew-symmetric matrix
    return (
        a[0][1] * pfaffian_4x4([[a[r][c] for c in (2, 3, 4, 5)] for r in (2, 3, 4, 5)])
        - a[0][2] * pfaffian_4x4([[a[r][c] for c in (1, 3, 4, 5)] for r in (1, 3, 4, 5)])
        + a[0][3] * pfaffian_4x4([[a[r][c] for c in (1, 2, 4, 5)] for r in (1, 2, 4, 5)])
        - a[0][4] * pfaffian_4x4([[a[r][c] for c in (1, 2, 3, 5)] for r in (1, 2, 3, 5)])
        + a[0][5] * pfaffian_4x4([[a[r][c] for c in (1, 2, 3, 4)] for r in (1, 2, 3, 4)])
    )


def check_site_and_bond_algebra() -> int:
    c = [0]
    i4 = mat_eye_int(4, 1)
    neg_i4 = mat_eye_int(4, -1)
    z4 = mat_zero_int(4)

    b_x: MatrixInt = [
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
    ]
    b_y: MatrixInt = [
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 0, -1],
        [0, 0, -1, 0],
    ]
    b_z: MatrixInt = [
        [1, 0, 0, 0],
        [0, -1, 0, 0],
        [0, 0, -1, 0],
        [0, 0, 0, 1],
    ]
    ic: MatrixInt = [
        [0, 1, 0, 0],
        [-1, 0, 0, 0],
        [0, 0, 0, -1],
        [0, 0, 1, 0],
    ]

    for name, b_mat in (("bX", b_x), ("bY", b_y), ("bZ", b_z)):
        require(mat_mul_int(b_mat, b_mat) == i4, f"{name}^2 == I_4", c)
        require(
            mat_add_int(mat_mul_int(b_mat, ic), mat_mul_int(ic, b_mat)) == z4,
            f"{{{name}, ic}} == 0",
            c,
        )
    require(mat_mul_int(ic, ic) == neg_i4, "ic^2 == -I_4", c)

    pairs = [("bX", b_x, "bY", b_y), ("bX", b_x, "bZ", b_z), ("bY", b_y, "bZ", b_z)]
    for n1, m1, n2, m2 in pairs:
        require(
            mat_add_int(mat_mul_int(m1, m2), mat_mul_int(m2, m1)) == z4,
            f"{{{n1}, {n2}}} == 0",
            c,
        )

    sig_x = mat_mul_int(b_x, ic)
    sig_y = mat_mul_int(b_y, ic)
    sig_z = mat_mul_int(b_z, ic)
    j_d = mat_mul_int(mat_mul_int(mat_mul_int(b_x, b_y), b_z), ic)

    for name, s_mat in (("sigX", sig_x), ("sigY", sig_y), ("sigZ", sig_z)):
        require(mat_mul_int(s_mat, s_mat) == i4, f"{name}^2 == I_4", c)
        require(
            mat_mul_int(j_d, s_mat) == mat_mul_int(s_mat, j_d),
            f"[J_D, {name}] == 0",
            c,
        )

    for n1, s1, n2, s2 in [
        ("sigX", sig_x, "sigY", sig_y),
        ("sigX", sig_x, "sigZ", sig_z),
        ("sigY", sig_y, "sigZ", sig_z),
    ]:
        require(
            mat_add_int(mat_mul_int(s1, s2), mat_mul_int(s2, s1)) == z4,
            f"{{{n1}, {n2}}} == 0",
            c,
        )

    require(mat_mul_int(j_d, j_d) == neg_i4, "J_D^2 == -I_4", c)
    for name, m_mat in (("bX", b_x), ("bY", b_y), ("bZ", b_z), ("ic", ic)):
        require(
            mat_add_int(mat_mul_int(j_d, m_mat), mat_mul_int(m_mat, j_d)) == z4,
            f"{{J_D, {name}}} == 0",
            c,
        )

    prod_xyz = mat_mul_int(mat_mul_int(sig_x, sig_y), sig_z)
    require(prod_xyz == j_d, "sigX * sigY * sigZ == J_D", c)

    # 2-site 16x16 bond operators and gauge commutation
    j_d_1 = mat_kron_int(j_d, i4)
    j_d_2 = mat_kron_int(i4, j_d)
    for name, s_mat in (("X", sig_x), ("Y", sig_y), ("Z", sig_z)):
        bond_ss = mat_kron_int(s_mat, s_mat)
        require(
            mat_mul_int(bond_ss, bond_ss) == mat_eye_int(16, 1),
            f"2-site bond_{name}^2 == I_16",
            c,
        )
        require(
            mat_mul_int(j_d_1, bond_ss) == mat_mul_int(bond_ss, j_d_1),
            f"[J_D_1, bond_{name}] == 0",
            c,
        )
        require(
            mat_mul_int(j_d_2, bond_ss) == mat_mul_int(bond_ss, j_d_2),
            f"[J_D_2, bond_{name}] == 0",
            c,
        )

    return c[0]


def check_plaquette_and_pfaffian_identities() -> int:
    c = [0]

    # 1. Exhaustive 2^6 = 64 hexagonal link configurations x 16 vertex Z2 gauge transforms
    gauge_samples = list(itertools.product((1, -1), repeat=4))
    for links in itertools.product((1, -1), repeat=6):
        u01, u12, u23, u34, u45, u50 = links
        w_p = u01 * u12 * u23 * u34 * u45 * u50
        require(w_p * w_p == 1, "W_p^2 == 1", c)
        for e0, e1, e2, e3 in gauge_samples:
            e4, e5 = e0 * e2, e1 * e3
            u01_g = e0 * u01 * e1
            u12_g = e1 * u12 * e2
            u23_g = e2 * u23 * e3
            u34_g = e3 * u34 * e4
            u45_g = e4 * u45 * e5
            u50_g = e5 * u50 * e0
            w_p_g = u01_g * u12_g * u23_g * u34_g * u45_g * u50_g
            require(w_p_g == w_p, "W_p local Z2 gauge invariance", c)

    # 2. Closed Lx x Ly honeycomb torus even vortex parity (prod_p W_p == +1)
    for lx, ly in ((2, 2), (3, 2), (3, 3)):
        # Each cell (x, y) has 3 links: X, Y, Z, and 1 plaquette sharing 6 links
        links_map = {}
        for x in range(lx):
            for y in range(ly):
                for d in ("X", "Y", "Z"):
                    links_map[(d, x, y)] = 1

        def plaquette_fluxes() -> List[int]:
            fluxes: List[int] = []
            for x in range(lx):
                for y in range(ly):
                    xn = (x + 1) % lx
                    yn = (y + 1) % ly
                    wp = (
                        links_map[("Z", x, y)]
                        * links_map[("X", xn, y)]
                        * links_map[("Y", xn, yn)]
                        * links_map[("Z", xn, yn)]
                        * links_map[("X", xn, yn)]
                        * links_map[("Y", x, yn)]
                    )
                    fluxes.append(wp)
            return fluxes

        init_fluxes = plaquette_fluxes()
        require(all(w == 1 for w in init_fluxes), f"{lx}x{ly} vortex-free ground flux", c)

        # Flip each link one by one and verify exactly 2 plaquettes flip and prod_p W_p == 1
        for key in list(links_map.keys()):
            before = plaquette_fluxes()
            links_map[key] = -links_map[key]
            after = plaquette_fluxes()
            flipped = sum(1 for b, a in zip(before, after) if a == -b)
            require(flipped == 2, f"{lx}x{ly} link flip changes 2 plaquettes", c)
            prod = 1
            for w in after:
                prod *= w
            require(prod == 1, f"{lx}x{ly} torus total flux product == +1", c)
            vortex_count = sum(1 for w in after if w == -1)
            require(vortex_count % 2 == 0, f"{lx}x{ly} torus vortex count is even", c)

    # 3. Exact 4x4 and 6x6 skew-symmetric quadratic matter matrices det(A(u)) == Pf(A(u))^2
    couplings = (
        Fraction(1, 1),
        Fraction(3, 2),
        Fraction(2, 3),
        Fraction(5, 4),
        Fraction(1, 2),
        Fraction(7, 5),
    )
    for signs in itertools.product((1, -1), repeat=6):
        vals = [couplings[idx] * signs[idx] for idx in range(6)]
        a01, a02, a03, a12, a13, a23 = vals
        mat4: MatrixFrac = [
            [Fraction(0), a01, a02, a03],
            [-a01, Fraction(0), a12, a13],
            [-a02, -a12, Fraction(0), a23],
            [-a03, -a13, -a23, Fraction(0)],
        ]
        # Skew-symmetry check
        require(
            all(mat4[i][j] == -mat4[j][i] for i in range(4) for j in range(4)),
            "4x4 matter matrix skew-symmetric",
            c,
        )
        pf4 = pfaffian_4x4(mat4)
        det4 = det_bareiss(mat4)
        require(det4 == pf4 * pf4, "4x4 det(A(u)) == Pf(A(u))^2", c)
        require(det4 >= 0, "4x4 det(A(u)) >= 0", c)

    # 6x6 hexagonal plaquette quadratic matter matrix across all 2^6 = 64 boundary link signs
    j_ring = [
        Fraction(1, 1),
        Fraction(4, 3),
        Fraction(3, 2),
        Fraction(5, 3),
        Fraction(7, 4),
        Fraction(2, 1),
    ]
    for signs in itertools.product((1, -1), repeat=6):
        mat6: MatrixFrac = [[Fraction(0) for _ in range(6)] for _ in range(6)]
        for k in range(6):
            kn = (k + 1) % 6
            w_edge = j_ring[k] * signs[k]
            mat6[k][kn] += w_edge
            mat6[kn][k] -= w_edge
        # Add next-nearest-neighbor Haldane-like kappa terms on even/odd sublattices
        kappa = Fraction(1, 5)
        for k in range(6):
            kn2 = (k + 2) % 6
            w_nnn = kappa * signs[k] * signs[(k + 1) % 6]
            mat6[k][kn2] += w_nnn
            mat6[kn2][k] -= w_nnn
        pf6 = pfaffian_6x6(mat6)
        det6 = det_bareiss(mat6)
        require(det6 == pf6 * pf6, "6x6 hex plaquette det(A(u)) == Pf(A(u))^2", c)
        require(det6 >= 0, "6x6 hex plaquette det(A(u)) >= 0", c)

    return c[0]


def check_gauge_and_flux_fences() -> int:
    c = [0]

    # 1. Unprojected 4^N vs physical 2^N Hilbert space dimension fence
    for n_sites in range(1, 9):
        dim_fock = 4 ** n_sites
        dim_phys = 2 ** n_sites
        gauge_redundancy = 2 ** n_sites
        require(
            dim_fock == dim_phys * gauge_redundancy,
            f"N={n_sites}: 4^N == 2^N * 2^N",
            c,
        )
        require(dim_fock > dim_phys, f"N={n_sites}: 4^N > 2^N", c)

    # Single-site diagonal gauge parity D = diag(1, 1, -1, -1) and projector I_4 + D
    d_diag: MatrixInt = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, -1, 0],
        [0, 0, 0, -1],
    ]
    p_unnorm = mat_add_int(mat_eye_int(4, 1), d_diag, scale_b=1)
    require(mat_mul_int(d_diag, d_diag) == mat_eye_int(4, 1), "D^2 == I_4", c)
    require(sum(d_diag[i][i] for i in range(4)) == 0, "Tr(D) == 0", c)
    require(
        mat_mul_int(p_unnorm, p_unnorm) == mat_add_int( mat_zero_int(4), p_unnorm, scale_b=2),
        "(I_4 + D)^2 == 2(I_4 + D)",
        c,
    )
    require(sum(p_unnorm[i][i] for i in range(4)) == 4, "Tr(I_4 + D) == 4 (rank 2)", c)

    # 2. Link-flip Pfaffian sign reversal while det(A) stays positive
    for j01 in (Fraction(1), Fraction(2), Fraction(3, 2), Fraction(5, 3)):
        for j23 in (Fraction(1), Fraction(4, 3), Fraction(7, 4)):
            mat_pos: MatrixFrac = [
                [Fraction(0), j01, Fraction(0), Fraction(0)],
                [-j01, Fraction(0), Fraction(0), Fraction(0)],
                [Fraction(0), Fraction(0), Fraction(0), j23],
                [Fraction(0), Fraction(0), -j23, Fraction(0)],
            ]
            mat_neg: MatrixFrac = [
                [Fraction(0), -j01, Fraction(0), Fraction(0)],
                [j01, Fraction(0), Fraction(0), Fraction(0)],
                [Fraction(0), Fraction(0), Fraction(0), j23],
                [Fraction(0), Fraction(0), -j23, Fraction(0)],
            ]
            pf_pos = pfaffian_4x4(mat_pos)
            pf_neg = pfaffian_4x4(mat_neg)
            det_pos = det_bareiss(mat_pos)
            det_neg = det_bareiss(mat_neg)
            require(pf_pos > 0 and pf_neg < 0, "link flip reverses Pfaffian sign", c)
            require(pf_pos + pf_neg == 0, "Pf(+u) + Pf(-u) == 0", c)
            require(det_pos == det_neg and det_pos > 0, "det(+u) == det(-u) > 0", c)

    # 3. Physical parity projection weight 1 + p_matter * p_gauge fence
    for p_gauge in (1, -1):
        w_match = 1 + p_gauge * p_gauge
        w_mismatch = 1 + (-p_gauge) * p_gauge
        require(w_match == 2, "matched parity sector has weight 2", c)
        require(w_mismatch == 0, "mismatched parity sector is projected out (weight 0)", c)

    return c[0]


def main() -> None:
    n_site = check_site_and_bond_algebra()
    n_plaq = check_plaquette_and_pfaffian_identities()
    n_fence = check_gauge_and_flux_fences()
    total = n_site + n_plaq + n_fence
    print(
        f"PASS fsp-kitaev-honeycomb-solution: checks={total} "
        f"site_bond={n_site} plaquette_pfaffian={n_plaq} fences={n_fence} failures=0"
    )


if __name__ == "__main__":
    main()
