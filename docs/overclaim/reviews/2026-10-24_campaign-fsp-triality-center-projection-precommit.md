# Pre-Commit Review: `FSP-TRIALITY-CENTER-PROJECTION` (`TFQ-1202`)

AuthorityEffect: None.

- **Node**: `FSP-TRIALITY-CENTER-PROJECTION` (`TFQ-1202` / `FSP-DERIV-038`)
- **Stage**: `FERMION_SIGN`
- **Status**: `OPEN` (preserved)
- **Evidence Grade**: `E1 -> E3` (`L4D`, 0 flags)
- **Lean 4 Module**: `lean4/CampaignFspTrialityCenterProjection.lean` (10 theorems, 0 `sorry`, 0 custom axioms, 6/6 mutants killed)
- **Independent Check**: `checks/independent/fsp-triality-center-projection.py` (`PASS: checks=3949 zomega=2404 projection=871 y_junction=639 scope_fences=35 failures=0`)
- **Statement-Match Review**:
  1. **What it supports**: Canonical-ensemble $\mathbb{Z}_3$ center projector $\Pi_{\mathbb{Z}_3}(q) = \sum_{k=0}^2 \omega^{q k}$ in $\mathbb{Z}[\omega]$ ($\omega^2 + \omega + 1 = 0$), Fourier isolation $\sum_{k=0}^2 (Z_0 + \omega^k Z_1 + \omega^{2k} Z_2) = 3 Z_0$ removing fractional-triality amplitudes $Z_1, Z_2$, persistence of intra-sector baryon sign differences $3(w_{B,+} - w_{B,-}) < 0$, 4-vertex simplicial Y-junction nilpotence $d_1 \circ d_0 = 0$ and 2-cochain curvature, and Polyakov-loop sector action sum/gap identities.
  2. **What it does not support**: Does not claim that $\mathbb{Z}_3$ center averaging solves the dense lattice QCD sign problem (`OPEN` status preserved) and explicitly fences the historical `GIN-C10` and `GIN-C11` fixtures.
  3. **Scope fences included**: `zero_triality_baryon_sector_sign_persistence`, `gin_c11_confined_sector_multiplicity_imbalance`, and `gin_c10_c11_historical_fixture_scope_fence`.
