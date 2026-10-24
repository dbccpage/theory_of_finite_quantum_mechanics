# Pre-Commit Review: `FSP-TROYER-WIESE-REDUCTION` (`TFQ-1192`)

AuthorityEffect: None.

- **Node**: `FSP-TROYER-WIESE-REDUCTION` (`TFQ-1192` / `FSP-DERIV-026`)
- **Stage**: `FERMION_SIGN`
- **Status**: `IMPORTED_ASSUMPTION` (preserved)
- **Evidence Grade**: `E1 -> E3` (`L4D`, 0 flags)
- **Lean 4 Module**: `lean4/CampaignFspTroyerWieseReduction.lean` (10 theorems, 0 `sorry`, 0 custom axioms, 6/6 mutants killed)
- **Independent Check**: `checks/independent/fsp-troyer-wiese-reduction.py` (`checks=608 ising_gaps=232 thermal_tail=352 basis_walks=4 scope_fences=20 failures=0`)
- **Statement-Match Review**:
  1. **What it supports**: Integer $\pm J$ Ising bond-flip parity and frustrated triangle spectrum ($E_0 = -J$, $E_1 = 3 J$, gap $4 J > 0$), the Troyer-Wiese (2005) Eqs. (10)-(11) Boltzmann excited-state tail bound $(3 N J \cdot 2^N)/(1 + W) < J / 4$ for $W \ge 12 N \cdot 2^N$ ($\beta J \ge N \ln 2 + \ln(12 N)$), YES/NO decision window separation at $E_{\text{th}} + J / 2$, Hadamard conjugation $U_H \sigma_z U_H = 2 \sigma_x$, negative length-3 closed-walk weight $(-J)^3 = -J^3 < 0$, and relative sign variance $1/s^2 - 1$ monotonicity.
  2. **What it does not support**: Does not formalize Barahona's 3D Ising spin-glass NP-completeness proof in Lean (`IMPORTED_ASSUMPTION` preserved) and does not reduce to the Hubbard model or make fixed finite system sizes $N$ intractable.
  3. **Scope fences included**: Basis dependence ($U_H \sigma_x U_H = 2 \sigma_z$ is diagonal), fixed-$N$ / bipartite Hubbard determinant positivity $(\det A)^2 \ge 0$, and withdrawn `HaltingQuotient` / `GenesisFspBridge` fixture boundaries.
