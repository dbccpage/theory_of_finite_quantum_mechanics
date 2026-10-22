# QM-221: Finite $\mathfrak{su}(3)_c$ QCD Gross–Wilczek–Politzer Asymptotic Freedom and Wilson-Loop Confinement Witness over $\mathbb{Q}$

**AuthorityEffect:** None.

## 1. Executive Summary

This research note documents **QM-221** (`qcd_beta0_wilson_confinement_control`), extending the finite Standard Model gauge-sector bridge (`QM-220`) to the non-Abelian strong interaction $\mathfrak{su}(3)_c$. Using the two-layer finite-to-continuum architecture over $\mathbb{Q}$ and Gaussian rationals $\mathbb{Q}(i)$, the control establishes:

1. **Part A — Rational-Weighted $\mathfrak{su}(3)_c$ Gell-Mann Basis and $9 \times 9$ Fierz Completeness over $\mathbb{Q}(i)$:**
   By replacing $T_8 = \frac{1}{2\sqrt{3}}\operatorname{diag}(1, 1, -2)$ with the unscaled rational diagonal generator $\tilde{T}_8 = \sqrt{3} T_8 = \frac{1}{2}\operatorname{diag}(1, 1, -2)$ paired with rational Killing weight $w_8 = 1/3$ (and $w_{1..7} = 1$ on $\tilde{T}_{1..7} = \frac{1}{2}\lambda_{1..7}$), the entire 8-generator $\mathfrak{su}(3)_c$ algebra lives inside $M_3(\mathbb{Q}(i))$ without irrational $\sqrt{3}$ extensions. Exhaustive matrix arithmetic checks Hermiticity, tracelessness, weighted Killing orthogonality
   $$w_a \operatorname{tr}(\tilde{T}_a \tilde{T}_b) = T_F \delta_{ab}, \qquad T_F = \frac{1}{2},$$
   the Jacobi identity across all $\binom{8}{3} = 56$ triples, the fundamental Casimir operator
   $$\sum_{a=1}^{8} w_a \tilde{T}_a^2 = C_F I_3, \qquad C_F = \frac{N_c^2 - 1}{2 N_c} = \frac{4}{3},$$
   the adjoint Casimir operator
   $$\sum_{a=1}^{8} w_a [\tilde{T}_a, [\tilde{T}_a, X]] = C_A X, \qquad C_A = N_c = 3,$$
   and the $9 \times 9$ Fierz completeness identity across all $3^4 = 81$ index quadruples $(i, j, k, l) \in \{0, 1, 2\}^4$:
   $$\sum_{a=1}^{8} w_a (\tilde{T}_a)_{ij} (\tilde{T}_a)_{kl} = \frac{1}{2}\delta_{il}\delta_{kj} - \frac{1}{6}\delta_{ij}\delta_{kl}.$$
   Projecting one-gluon exchange onto color irreducible channels yields attraction in the color-singlet $q\bar{q}$ channel ($-C_F = -4/3 < 0$), repulsion in the color-octet $q\bar{q}$ channel ($\frac{1}{2}C_A - C_F = +1/6 > 0$), repulsion in the symmetric sextet $qq$ channel ($+1/3 > 0$), and attraction in the antisymmetric antitriplet diquark $qq$ channel ($-2/3 < 0$).

2. **Part B — 1-Loop Gross–Wilczek–Politzer $\beta_0$ and 2-Loop Caswell–Jones $\beta_1$ over $\mathbb{Q}$:**
   The 1-loop QCD beta-function coefficient separates into the paramagnetic gluon spin contribution $+4 C_A = 12$, the diamagnetic gluon orbital contribution $-\frac{1}{3}C_A = -1$ (summing to the non-Abelian antiscreening term $\frac{11}{3}C_A = 11$), and the Dirac quark loop screening contribution $-\frac{4}{3}T_F n_f = -\frac{2}{3}n_f$:
   $$\beta_0(3, n_f) = \frac{11}{3}C_A - \frac{4}{3}T_F n_f = 11 - \frac{2}{3}n_f.$$
   Over $\mathbb{Q}$, $\beta_0(3, n_f) > 0$ holds for $0 \le n_f \le 16$ (with $\beta_0(3, 0) = 11$, $\beta_0(3, 3) = 9$, $\beta_0(3, 5) = 23/3$, $\beta_0(3, 6) = 7$, and $\beta_0(3, 16) = 1/3$), and reverses sign at $n_f = 17$ ($\beta_0(3, 17) = -1/3 < 0$). Combining $\beta_0$ with the 2-loop Caswell–Jones coefficient
   $$\beta_1(3, n_f) = \frac{34}{3}C_A^2 - \left(\frac{20}{3}C_A + 4 C_F\right)T_F n_f = 102 - \frac{38}{3}n_f$$
   at $n_f = 16$ ($\beta_0 = 1/3 > 0$, $\beta_1 = -302/3 < 0$) yields the exact Banks–Zaks perturbative infrared fixed-point ratio $-\beta_0 / \beta_1 = 1/302$.

3. **Part C — Finite-Graph DFM Plaquette Reduction and Wilson-Loop Creutz Confinement Witness:**
   On the $3 \times 3$ planar square lattice ($|V| = 9$, $|E| = 12$), Dressing Field Method (DFM) spanning-tree gauge reduction neutralizes $|E_T| = |V| - 1 = 8$ link variables to the identity, projecting the lattice gauge configuration onto $b_1(G) = |E| - |V| + 1 = 4$ independent fundamental plaquette holonomies without Faddeev–Popov ghosts. At strong-coupling character expansion parameter $\tilde{\beta} = \beta / (2 N_c^2) = 1/9$ ($\beta = 2$), the multiplicative Creutz ratio
   $$\chi_{\mathrm{mult}}(R, T) = \frac{W(R, T)\,W(R - 1, T - 1)}{W(R, T - 1)\,W(R - 1, T)}$$
   cancels perimeter and corner factors identically, yielding $\chi_{\mathrm{mult}}^{\mathrm{area}}(R, T) = \tilde{\beta} = 1/9 < 1$ under the strong-coupling area law $W_{\mathrm{area}}(R, T) = \tilde{\beta}^{RT}$ versus $\chi_{\mathrm{mult}}^{\mathrm{perim}}(R, T) = 1$ under the perimeter law $W_{\mathrm{perim}}(R, T) = \tilde{\beta}^{2(R+T)}$ across all $(R, T) \in \{2, 3\}^2$.

4. **Part D — 12-Decimal Rational Interval Enclosures for Running $\alpha_s(Q^2)$ and String Tension $\sigma a^2$:**
   From $\alpha_s(M_Z^2) = 1179/10000$ at $n_f = 5$ ($\beta_0 = 23/3$), certified rational interval arithmetic encloses 1-loop ultraviolet running at $L = \ln(Q^2/M_Z^2) \in \{2, 4\}$ by the $\overline{\mathrm{MS}}$ formula $\alpha_s(Q^2) = \alpha_s(M_Z^2) / (1 + \beta_0 \alpha_s(M_Z^2) L / (4\pi))$:
   $$\alpha_s(L = 2) \approx 0.103072040480, \qquad \alpha_s(L = 4) \approx 0.091557149048,$$
   and encloses the strong-coupling dimensionless string tension $\sigma a^2 = -\ln \chi_{\mathrm{mult}}^{\mathrm{area}} = \ln 9 = 2\ln 3 \approx 2.197224577336$ to 12 decimal places.

---

## 2. Tri-Anchor Verification Summary

| Verification Anchor | Artifact Path | Key Checked Invariants |
|---|---|---|
| **Rust Native Kernel** | `omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/qcd_beta0_wilson_confinement_control.rs` | `test_qm221_qcd_beta0_wilson_confinement_control` (81-entry Fierz identity, $\beta_0, \beta_1$, Creutz ratio, 12-decimal enclosures) |
| **Python Use Case & E2E** | `python/finite_qm/use_cases/qcd_beta0_wilson_confinement_control.py`, `tests/e2e/test_e2e_qcd_beta0_wilson_confinement_control.py` | 5 E2E tests checking Parts A–E and Fable MCTS receipt parity |
| **Lean 4 Kernel** | `lean4/FiniteQM.lean` (`lean4/FiniteQM.lean` Part IV) | 6 theorems (`su3_casimir_and_channel_identities`, `su3_fierz_diagonal_and_offdiagonal_identities`, `qcd_beta0_asymptotic_freedom_window`, `qcd_beta1_and_banks_zaks_fixed_point`, `wilson_creutz_ratio_area_vs_perimeter`, `wilson_lattice_3x3_dfm_betti_identity`), `0` `sorryAx` |

---

## 3. Claim Hygiene Summary

1. **What it supports:**
   - Supports that the 8-dimensional $\mathfrak{su}(3)_c$ Lie algebra, its Killing form, fundamental Casimir $C_F = 4/3$, adjoint Casimir $C_A = 3$, and $9 \times 9$ Fierz completeness identity admit an exact rational-weighted representation over $\mathbb{Q}(i)$ using $w = (1, 1, 1, 1, 1, 1, 1, 1/3)$.
   - Supports that the 1-loop Gross–Wilczek–Politzer coefficient $\beta_0(3, n_f) = 11 - \frac{2}{3}n_f$, the 2-loop Caswell–Jones coefficient $\beta_1(3, n_f) = 102 - \frac{38}{3}n_f$, the asymptotic freedom window $0 \le n_f \le 16$, the Banks–Zaks ratio $1/302$ at $n_f = 16$, and the strong-coupling Wilson-loop Creutz ratio $\chi_{\mathrm{mult}}^{\mathrm{area}} = \tilde{\beta} = 1/9 < 1 = \chi_{\mathrm{mult}}^{\mathrm{perim}}$ are exact rational identities over $\mathbb{Q}$, checked in Rust, Python, and Lean 4 (`0` `sorryAx`).
2. **What it does not support:**
   - Does not support a continuum $4\mathrm{D}$ Yang–Mills mass-gap existence proof in the sense of the Clay Millennium Problem or non-perturbative confinement in the continuum limit $a \to 0$ at weak coupling $\beta \to \infty$.
   - Does not replace Monte Carlo lattice QCD hadron spectroscopy or higher-loop $\overline{\mathrm{MS}}$ threshold matching.
3. **The narrowest defensible claim:**
   - Within the declared finite algebraic and strong-coupling lattice model over $\mathbb{Q}(i)$ and $\mathbb{Q}$, the rational-weighted $\mathfrak{su}(3)_c$ generators satisfy the 81-entry Fierz completeness identity with $C_F = 4/3$ and $C_A = 3$, the 1-loop and 2-loop beta coefficients satisfy $\beta_0(3, n_f) = 11 - \frac{2}{3}n_f$ and $\beta_1(3, n_f) = 102 - \frac{38}{3}n_f$, DFM spanning-tree reduction reduces the $3 \times 3$ lattice to $b_1 = 4$ plaquettes, and the strong-coupling Creutz ratio distinguishes area-law confinement ($\chi = 1/9$) from perimeter-law behavior ($\chi = 1$).
4. **The next test needed:**
   - Extend the finite non-Abelian gauge and chiral fermion controls to **QM-222**: finite axial-vector triangle anomaly and Chern–Weil topological index / Witten $\mathfrak{su}(2)$ global parity control, or finite 2-flavor chiral $\mathfrak{su}(2)_L \times \mathfrak{su}(2)_R \to \mathfrak{su}(2)_V$ Gell-Mann–Oakes–Renner (GMOR) pion-decay algebraic control over $\mathbb{Q}$.
