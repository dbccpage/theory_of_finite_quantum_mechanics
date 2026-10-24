# Pre-Commit Review: `FSP-FRACTON-MOBILITY` (`TFQ-1218`)

AuthorityEffect: None.

- **Node**: `FSP-FRACTON-MOBILITY` (`TFQ-1218` / `FSP-DERIV-054`)
- **Stage**: `FERMION_SIGN`
- **Status**: `IMPORTED_ASSUMPTION` (preserved)
- **Evidence Grade**: `E1 -> E3` (`L4D`, 0 flags)
- **Lean 4 Module**: `lean4/CampaignFspFractonMobility.lean` (10 theorems, 0 `sorry`, 0 custom axioms, 6/6 mutants killed)
- **Independent Check**: `checks/independent/fsp-fracton-mobility.py` (`checks=6133 fracton_mobility=5326 lineon_mobility=787 scope_fences=20 failures=0`)
- **Statement-Match Review**:
  1. **What it supports**: Single-edge Pauli-$Z$ cube syndrome weight $4$, isolated 0D fracton single-edge hop barrier $\Delta E = 4 J > 0$ (weight $1 \to 3$), rectangular membrane 4-corner quadrupole conservation and foliated separation penalty $\Delta S = \kappa R$, 2D planon dipole mobility ($\Delta E = 0$), 1D collinear lineon string mobility ($\Delta E = 0$), and $90^\circ$ corner-turn orthogonal lineon defect creation (weight $4 \to 6$, $\Delta E = 2 J_A > 0$).
  2. **What it does not support**: Does not claim that subdimensional mobility constraints in a bosonic stabilizer code eliminate the fermion sign problem for physical lattice fermions.
  3. **Scope fences included**: 2D planon dipole braiding ($\operatorname{sgn}(\tau) = -1$), 1D T-junction 3-step exchange ($\operatorname{sgn}(\tau) = -1$), and non-abelian $SU(2)_2$ hinge holonomy negative trace $\operatorname{Tr}(-I_2) = -2 < 0$.
