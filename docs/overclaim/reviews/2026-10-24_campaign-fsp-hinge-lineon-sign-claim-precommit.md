# Pre-Commit Review: `FSP-HINGE-LINEON-SIGN-CLAIM` (`TFQ-1219`)

AuthorityEffect: None.

- **Node**: `FSP-HINGE-LINEON-SIGN-CLAIM` (`TFQ-1219` / `FSP-DERIV-055`)
- **Stage**: `FERMION_SIGN`
- **Status**: `OPEN` (preserved)
- **Evidence Grade**: `E1 -> E3` (`L4D`, 0 flags)
- **Lean 4 Module**: `lean4/CampaignFspHingeLineonSignClaim.lean` (10 theorems, 0 `sorry`, 0 custom axioms, 6/6 mutants killed)
- **Independent Check**: `checks/independent/fsp-hinge-lineon-sign-claim.py` (`checks=872 open_chain=807 periodic_ring=18 intersecting_junctions=42 holonomy_fences=5 failures=0`)
- **Statement-Match Review**:
  1. **What it supports**: On an isolated 1D open chain, nearest-neighbor hardcore fermion steps preserve site order $x_1 < x_2$, pass over $0$ intermediate Jordan-Wigner sites (hop sign $+1$), and induce the identity permutation on closed loops ($\operatorname{sgn}(1) = +1$).
  2. **What it does not support**: Does not support the unrestricted claim that 3D foliated fracton models with 1D hinge lineons are automatically sign-free (`GIN-C24`).
  3. **Scope fences included**: Periodic 1D ring cyclic winding ($N=2$, sign $-1$), intersecting hinge T-junction 6-step exchange (sign $-1$), $90^\circ$ corner-turn foliated projection obstruction ($\operatorname{Tr} = -2 < 0$), and non-abelian 2-gauge hinge commutator holonomy $J D (-J) D = -I_2$ ($\operatorname{Tr}(-I_2) = -2 < 0$, $\Phi_1 = 2 > 0$).
