import time
import numpy as np
from omega_engine.crates.majorana.core.gf2_matrix import GF2Matrix


def benchmark_kitaev_majorana_wire(num_sites: int = 10):
    num_majoranas = 2 * num_sites
    num_bonds = num_majoranas - 1

    d0_data = []
    for i in range(num_bonds):
        row = [0] * num_majoranas
        row[i] = 1
        row[i + 1] = 1
        d0_data.append(row)

    gf2_d0 = GF2Matrix(d0_data)

    b_defect = [0] * num_bonds
    b_defect[0] = 1

    t0 = time.perf_counter()
    sol_gf2 = gf2_d0.solve(b_defect)
    rref_matrix, pivots = gf2_d0.rref()
    rank_f2 = len(pivots)
    t1 = time.perf_counter()
    time_f2 = t1 - t0

    hilbert_dim = 2 ** num_sites
    t2 = time.perf_counter()
    H = np.random.randn(hilbert_dim, hilbert_dim) + 1j * np.random.randn(hilbert_dim, hilbert_dim)
    H = 0.5 * (H + H.conj().T)
    rho = np.eye(hilbert_dim, dtype=complex) / hilbert_dim
    dt = 0.01
    w_eig, v_eig = np.linalg.eigh(H)
    U = v_eig @ np.diag(np.exp(-1j * w_eig * dt)) @ v_eig.conj().T
    rho_next = U @ rho @ U.conj().T
    t3 = time.perf_counter()
    time_hilbert = t3 - t2

    speedup = time_hilbert / time_f2 if time_f2 > 0 else float('inf')

    print("==========================================================")
    print(f" KITAEV MAJORANA WIRE BENCHMARK ({num_sites} Sites / {num_majoranas} Majorana Modes)")
    print("==========================================================")
    print(f" Hilbert Space Dimension: {hilbert_dim} x {hilbert_dim} ({hilbert_dim**2:,} matrix entries)")
    print(f" F2 Cohomology Matrix:    {num_bonds} x {num_majoranas} (rank = {rank_f2})")
    print(f" F2 Cohomology Time:      {time_f2 * 1000:.4f} ms")
    print(f" Full Hilbert State Time: {time_hilbert * 1000:.4f} ms (2^{num_sites} dense state matrix evolution)")
    print(" Note: GF(2) cochain solver tracks 1D parity boundary obstructions.")
    print(" Non-interacting free-fermion baselines scale as O(N^3) via 2N x 2N single-particle matrices.")
    print("==========================================================")

    return time_f2, time_hilbert, speedup


if __name__ == "__main__":
    benchmark_kitaev_majorana_wire(num_sites=10)




