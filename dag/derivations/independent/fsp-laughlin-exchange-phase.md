# Independent Derivation Note: `FSP-LAUGHLIN-EXCHANGE-PHASE` (`TFQ-1208`)

> **AuthorityEffect**: `None`  
> **Node**: `FSP-LAUGHLIN-EXCHANGE-PHASE` (`TFQ-1208`, Rank 27, Stage `FERMION_SIGN`)  
> **Status**: `IMPORTED_ASSUMPTION` (`E1 -> E3`, `Narrowed`)

---

## 1. Scope and Hypothesis Explicitness

`FSP-LAUGHLIN-EXCHANGE-PHASE` records the Arovas–Schrieffer–Wilczek result that adiabatic exchange of two quasiholes in the $\nu = 1/m$ Laughlin fractional quantum Hall state yields statistical phase $\theta = \pi / m$ and braiding monodromy $2\theta = 2\pi / m$.

This campaign narrowing replaces the missing `FqhLaughlinBraiding.lean::laughlin_fractional_exchange_phase` reference and the numeric-constant `2 % 3 != 0` / `gcd 2 3 = 1` checks in `FqhLaughlinBraiding.lean` with:
- [`lean4/CampaignFspLaughlinExchangePhase.lean`](../../../lean4/CampaignFspLaughlinExchangePhase.lean) (`L4D`, 10 theorems, 0 `sorry`, standard axioms only, 6/6 semantic mutations killed by `lake build`).
- [`checks/independent/fsp-laughlin-exchange-phase.py`](../../../checks/independent/fsp-laughlin-exchange-phase.py) (exact integer and `Fraction` arithmetic, normal and `-O` mode).

---

## 2. Formalized Identities (`lean4/CampaignFspLaughlinExchangePhase.lean`)

1. **General-$m$ Laughlin Jastrow polynomial exchange parity** (`laughlin_two_body_jastrow_exchange_parity`, `laughlin_odd_m_fermionic_and_even_m_bosonic`, `laughlin_three_body_vandermonde_transposition_flips_sign_for_odd_m`):
   - Over any commutative ring $R$, $(z_2 - z_1)^m = (-1)^m (z_1 - z_2)^m$ for all $m : \mathbb{N}$: odd $m = 2k + 1$ produces fermionic antisymmetry and even $m = 2k$ produces bosonic symmetry, including under pairwise transpositions in the three-body Vandermonde Jastrow product $(z_1 - z_2)^m (z_1 - z_3)^m (z_2 - z_3)^m$.
2. **Holomorphic quasihole polynomial symmetry fence** (`laughlin_quasihole_holomorphic_polynomial_symmetric_fence`):
   - The bare holomorphic two-quasihole prefactor $\prod_{j} (z_j - \eta_1)(z_j - \eta_2)$ is strictly symmetric under $\eta_1 \leftrightarrow \eta_2$. This proves that the fractional statistical phase $\theta = \pi / m$ is not obtained from bare algebraic substitution $\eta_1 \leftrightarrow \eta_2$, but requires the Arovas–Schrieffer–Wilczek adiabatic Berry connection and plasma normalization integral (which remain imported literature results).
3. **Exact $\mathrm{SL}_2(\mathbb{Z})$ cyclotomic companion matrices for $\nu = 1/3$ exchange and monodromy** (`laughlin_m3_exchange_companion_cyclotomic_relations`, `laughlin_m3_monodromy_cyclotomic_and_non_involution`):
   - The companion matrix $R_6 = \begin{pmatrix} 0 & -1 \\ 1 & 1 \end{pmatrix}$ of $\exp(i\pi/3)$ satisfies $\det(R_6) = 1$, $\mathrm{Tr}(R_6) = 1$, $\Phi_6(R_6) = R_6^2 - R_6 + I_2 = 0$, $R_6^3 = -I_2$ ($m = 3$ quasihole exchanges recover the electron fermionic sign $-1$), $R_6^6 = I_2$, and $R_6 \notin \{I_2, -I_2\}$.
   - The monodromy matrix $M_3 = R_6^2 = \begin{pmatrix} -1 & -1 \\ 1 & 0 \end{pmatrix}$ of $\exp(i 2\pi/3)$ satisfies $\det(M_3) = 1$, $\mathrm{Tr}(M_3) = -1$, $\Phi_3(M_3) = I_2 + M_3 + M_3^2 = 0$, $M_3^3 = I_2$, and $M_3^2 \neq I_2$.
4. **Abelian involution obstruction, general-$m$ monodromy residue, modular $S$-matrix exponent, and weight asymmetry fences** (`no_z2_involution_matches_m3_monodromy_fence`, `general_m_monodromy_residue_and_odd_coprime`, `abelian_anyon_modular_s_exponent_and_z3_character_sum`, `unequal_quasihole_quasielectron_weights_prevent_z3_cancellation_fence`):
   - No $2 \times 2$ integer involution matrix $J$ ($J^2 = I_2$) equals $M_3$ or $R_6$.
   - For all $m \ge 3$, $2 \bmod m = 2 \neq 0$, and for all $k : \mathbb{N}$, $\gcd(2, 2k + 1) = 1$.
   - The abelian modular $S$-matrix exponent combination $e(a, b) + e(0, 0) - e(a, 0) - e(0, b) = a b$, and while equal weights across $(I_2, M_3, M_3^2)$ sum to $0$, unequal quasihole/quasielectron weights $w_{\mathrm{qh}} \neq w_{\mathrm{qe}}$ leave $(w_{\mathrm{qh}} - w_{\mathrm{qe}}) I_2 \neq 0$.

---

## 3. Claim Hygiene Summary

1. **What it supports**: Formalizes in Lean 4 and checks in Python the general-$m$ Laughlin Jastrow electron exchange parity $(-1)^m$, the symmetry of the bare holomorphic quasihole polynomial $\prod_j (z_j - \eta_1)(z_j - \eta_2)$ under $\eta_1 \leftrightarrow \eta_2$, the exact $\mathrm{SL}_2(\mathbb{Z})$ cyclotomic algebra of the $\pi/3$ exchange and $2\pi/3$ monodromy operators, the non-involution obstruction ($J^2 = I_2 \implies J \neq M_3, R_6$), general-$m$ residue/coprimality ($2 \bmod m = 2$ for $m \ge 3$ and $\gcd(2, 2k+1) = 1$), and the non-cancellation of $\mathbb{Z}_3$ sectors under unequal quasihole/quasielectron weights.
2. **What it does not support**: It does not compute the continuum 2D plasma screening integral, adiabatic Berry-connection line integral $\oint \mathcal{A}_{\mathrm{Berry}} \cdot d\mathbf{x}$, or magnetic-translation torus ground-state multiplet in Lean 4 or Python; the physical Arovas–Schrieffer–Wilczek Berry phase calculation remains an imported assumption.
3. **Narrowest defensible claim**: In the finite polynomial and cyclotomic matrix model for Laughlin $\nu = 1/m$, electron Jastrow factors transform by $(-1)^m$ while bare holomorphic quasihole prefactors are symmetric under $\eta_1 \leftrightarrow \eta_2$ (isolating the Berry connection as the source of $\theta = \pi/m$), and the resulting $\mathbb{Z}_6 / \mathbb{Z}_3$ exchange and monodromy operators at $m = 3$ cannot be matched by any $\mathbb{Z}_2$ involution or cancelled when $w_{\mathrm{qh}} \neq w_{\mathrm{qe}}$.
4. **Next test needed**: Audit and narrow `PGW-WDP-BRIDGE-REPORT-FIBER-OBSERVER` (Rank 28, `CONDITIONAL`) by verifying the exact report-fibre constancy equivalence and negative counterexamples in Lean 4 and Python.
