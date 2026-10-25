# Pre-Commit Review: `FSP-NICOLAI-MAP-CLAIM` (`TFQ-1205`)

AuthorityEffect: None.

- **Node**: `FSP-NICOLAI-MAP-CLAIM` (`TFQ-1205` / `FSP-DERIV-041`)
- **Stage**: `FERMION_SIGN`
- **Status**: `OPEN` (preserved)
- **Evidence Grade**: `E1 -> E3` (`L4D`, 0 flags)
- **Lean 4 Module**: `lean4/CampaignFspNicolaiMapClaim.lean` (10 theorems, 0 `sorry`, 0 custom axioms, 6/6 mutants killed)
- **Independent Check**: `checks/independent/fsp-nicolai-map-claim.py` (`PASS: checks=4083 jacobian=896 positivity=2980 branch=196 scope_fences=11 failures=0`)
- **Statement-Match Review**:
  1. **What it supports**: Explicit 2-site and 3-site periodic skew-plus-diagonal lattice Nicolai map Jacobian identities ($J = D_{\mathrm{kin}}(\kappa) + \mathrm{diag}(w_i) = D_F$), strict determinant positivity under convex quartic superpotentials ($W''(\phi_i) = m + c\phi_i^2 \ge m > 0$), branch sign decomposition $J = \mathrm{sgn}(J)\cdot |J|$, non-convex fold branch cancellation, cubic 3-branch sign defect, and SUSY-breaking negative determinant flips.
  2. **What it does not support**: Does not claim that Nicolai maps eliminate the fermion sign problem in general lattice fermion Hamiltonians (`OPEN` status preserved) and explicitly fences the historical `regge_wdw_core.lean` `t = t` tautology.
  3. **Scope fences included**: Historical `NicolaiMapSignSuppressionPredicate t t` tautology fence and model-specificity non-injectivity fence.
