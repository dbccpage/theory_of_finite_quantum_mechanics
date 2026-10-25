# Pre-Commit Review: `FSP-THETA-TERM-COMPLEX-WEIGHT` (`TFQ-1198`)

AuthorityEffect: None.

- **Node**: `FSP-THETA-TERM-COMPLEX-WEIGHT` (`TFQ-1198` / `FSP-DERIV-034`)
- **Stage**: `FERMION_SIGN`
- **Status**: `IMPORTED_ASSUMPTION` (preserved)
- **Evidence Grade**: `E1 -> E3` (`L4D`, 0 flags)
- **Lean 4 Module**: `lean4/CampaignFspThetaTermComplexWeight.lean` (10 theorems, 0 `sorry`, 0 custom axioms, 6/6 mutants killed)
- **Independent Check**: `checks/independent/fsp-theta-term-complex-weight.py` (`PASS: checks=2058 index=179 phase=1426 sector=371 scope_fences=82 failures=0`)
- **Statement-Match Review**:
  1. **What it supports**: Lattice chiral index $Q_{\mathrm{top}} = n_+ - n_-$ CP antisymmetry, rational vacuum angle $\theta = (p/q)\pi$ integrality condition $q \mid p Q_{\mathrm{top}}$, CP-conjugate pair sine cancellation leaving $2 w \cos(\theta Q_{\mathrm{top}})$ (negative for obtuse phases $c < 0$), $\theta = \pi$ parity homomorphism $\sigma_\pi(Q_1 + Q_2) = \sigma_\pi(Q_1)\sigma_\pi(Q_2)$, two-sector partition sum cancellation $Z(\pi) = w_0 - w_1 < Z_{\mathrm{pq}} = w_0 + w_1$, and CP-symmetric 3-sector second moment $2 w_1 > 0$.
  2. **What it does not support**: Does not establish continuum $\theta$-vacuum sign-problem phenomenology (`IMPORTED_ASSUMPTION` preserved) and explicitly fences the historical `GIN-C9` Nat arithmetic inequality `w0 != w0 + deltaS`.
  3. **Scope fences included**: `gin_c9_su2_action_gap_fixture_scope_fence` and `theta_term_phenomenology_scope_fence`.
