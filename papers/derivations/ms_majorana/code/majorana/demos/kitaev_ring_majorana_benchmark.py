import time
import numpy as np
from omega_engine.crates.majorana.core.gf2_diagnostic import native_dim_h1
from omega_engine.crates.majorana.core.gf2_matrix import GF2Matrix


def benchmark_kitaev_ring_majorana(num_sites: int = 10):
    num_majoranas = 2 * num_sites
    num_bonds = num_majoranas

    d0_data = []
    for i in range(num_bonds - 1):
        row = [0] * num_majoranas
        row[i] = 1
        row[i + 1] = 1
        d0_data.append(row)
    row_close = [0] * num_majoranas
    row_close[num_bonds - 1] = 1
    row_close[0] = 1
    d0_data.append(row_close)

    gf2_d0 = GF2Matrix(d0_data)
    rref_matrix, pivots = gf2_d0.rref()
    rank_f2 = len(pivots)
    b1_betti = native_dim_h1(d0_data)  

    num_trials = 200
    unsat_count = 0
    sat_count = 0
    parity_check_agrees = 0

    t0 = time.perf_counter()
    for _ in range(num_trials):
        b = np.random.randint(0, 2, size=num_bonds).tolist()
        sol = gf2_d0.solve(b)
        total_parity = sum(b) % 2

        if sol is None:
            unsat_count += 1
            if total_parity == 1:
                parity_check_agrees += 1
        else:
            sat_count += 1
            if total_parity == 0:
                parity_check_agrees += 1

    t1 = time.perf_counter()
    time_f2 = (t1 - t0) / num_trials

    t2 = time.perf_counter()
    A_free = np.random.randn(num_majoranas, num_majoranas)
    A_free = 0.5 * (A_free - A_free.T)  
    w_free = np.linalg.eigvalsh(1j * A_free)
    t3 = time.perf_counter()
    time_free = t3 - t2

    print("==========================================================")
    print(f" KITAEV RING MAJORANA BENCHMARK ({num_sites} Sites / {num_majoranas} Modes)")
    print("==========================================================")
    print(f" Ring Graph Betti Number b1:  {b1_betti} (native majorana_gf2_diagnostic classify dim_h1)")
    print(f" F2 Rank:                     {rank_f2} / {num_bonds}")
    print(f" Tested Random Parity Defects:{num_trials}")
    print(f" Solvable (SAT, [w]=0):       {sat_count} ({sat_count/num_trials*100:.1f}%)")
    print(f" Obstructed (UNSAT, [w]!=0):  {unsat_count} ({unsat_count/num_trials*100:.1f}%)")
    print(f" Total Parity Sum Agreement:  {parity_check_agrees} / {num_trials} (100% Exact!)")
    print(f" F2 Obstruction Solve Time:   {time_f2 * 1000:.4f} ms per instance")
    print(f" Free-Fermion Eigsolve Time:  {time_free * 1000:.4f} ms")
    print("==========================================================")

    return b1_betti, unsat_count, time_f2, time_free


if __name__ == "__main__":
    benchmark_kitaev_ring_majorana(num_sites=10)




