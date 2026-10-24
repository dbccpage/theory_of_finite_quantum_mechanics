# Independent Derivation & Scope Narrowing: `FSP-COBORDISM-INTRINSIC-SIGN` (`TFQ-1211` / `FSP-DERIV-047`)

## 1. Node Identity and Epistemic Contract

- **Node ID**: `FSP-COBORDISM-INTRINSIC-SIGN` (`TFQ-1211` / `FSP-DERIV-047`)
- **Stage**: `FERMION_SIGN`
- **Status**: `OPEN` (narrowed to exact finite spectral-asymmetry, mapping-torus determinant, Arf Gaussian sign-sum, mod-2 cobordism pairing, and class-specific representation no-go/scope-fence theorems in Lean 4 and an independent exact-arithmetic Python verifier)
- **Lean 4 Module**: [`lean4/CampaignFspCobordismIntrinsicSign.lean`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspCobordismIntrinsicSign.lean) (`L4D`, 10 theorems, 0 `sorry`, standard Lean 4 axioms only, 6/6 semantic mutations killed)
- **Independent Python Verifier**: [`checks/independent/fsp-cobordism-intrinsic-sign.py`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/checks/independent/fsp-cobordism-intrinsic-sign.py)

---

## 2. Exact Finite Algebraic Prototypes & Class-Specific Representation No-Go

In [`papers/core/fsp/the_problem_of_the_fermion_sign.md`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/papers/core/fsp/the_problem_of_the_fermion_sign.md#L829-L853) (Section 9.17) and [`papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md#L32-L32) (`GIN-C22`), the finite algebraic prototypes and their representation-class scope boundaries decompose into five exact components:

1. **Discrete Spectral Asymmetry $\eta$-Jump and Fermion Parity Reversal**:
   - For integer eigenvalues $\lambda \in \mathbb{Z}$, the discrete spectral sign $\mathrm{spectralSign}(\lambda) \in \{-1, 0, +1\}$ is odd ($\mathrm{spectralSign}(-\lambda) = -\mathrm{spectralSign}(\lambda)$) and vanishes on every particle-hole symmetric pair $(\lambda, -\lambda)$ ([`spectralSign_odd_and_symmetric_pair_zero`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspCobordismIntrinsicSign.lean#L54-L58)).
   - When a single mode crosses zero from $-\lambda < 0$ to $+\lambda > 0$ ($\lambda > 0$), $\mathrm{spectralSign}$ jumps by $+2$ ($\Delta(\eta/2) = 1$) and reverses the fermion parity sign $(-1)^{k+1} = -(-1)^k$ ([`single_eigenvalue_crossing_eta_jump_by_two`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspCobordismIntrinsicSign.lean#L63-L74)).

2. **Finite Mapping-Torus Fermion Determinant Sign Reversal**:
   - The $2 \times 2$ mapping-torus Dirac block $\mathrm{diracMappingBlock}(m, s) = \begin{pmatrix} m & s \\ 1 & m \end{pmatrix}$ with mass $m \in \mathbb{Z}$ and $S^1$ holonomy twist $s \in \mathbb{Z}$ has determinant $m^2 - s$; at the massless point $m = 0$, the untwisted antiperiodic sector ($s = -1$) has $\det = +1 > 0$ whereas the $\mathbb{Z}_2$-twisted periodic sector ($s = +1$) has $\det = -1 < 0$, so their equal-weight sum vanishes ([`mapping_torus_fermion_det_sign_reversal`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspCobordismIntrinsicSign.lean#L84-L91)).

3. **Arf Quadratic Refinement Gaussian Sign Sums and Mod-2 AHSS Cobordism Pairing**:
   - On $(\mathrm{Fin}\ 2)^2$, the even Arf-0 quadratic form $q_0(x, y) = x y$ has Gaussian sign sum $\sum_{x,y \in \mathbb{F}_2} (-1)^{q_0(x,y)} = +2$ ($\frac{1}{2} \sum = +1 = (-1)^0$), whereas the odd Arf-1 quadratic form $q_1(x, y) = x y + x + y$ has Gaussian sign sum $-2$ ($\frac{1}{2} \sum = -1 = (-1)^1$) ([`arf_gaussian_sign_sum_dichotomy`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspCobordismIntrinsicSign.lean#L106-L110)).
   - The mod-2 5D Spin cobordism pairing $\nu_5(a_3, \mathrm{Arf}, w_1, \sigma/16) = a_3 \cdot \mathrm{Arf} + w_1 \cdot (\sigma/16) \in \mathbb{Z}_2$ vanishes on the anomaly-free $T^4$ sector ($\mathrm{Arf} = 0, \sigma/16 = 0$) and evaluates to $1 \neq 0$ on both the $K3$ gauge-gravitational sector ($a_3 = 0, w_1 = 1, \sigma/16 = 1$) and the Postnikov-Arf sector ($a_3 = 1, \mathrm{Arf} = 1, w_1 = 0$) ([`ahss_5d_spin_cobordism_pairing_sectors`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspCobordismIntrinsicSign.lean#L120-L128)).

4. **Class-Specific Representation No-Go and 5D Bulk Inflow Cancellation**:
   - In any symmetry-preserving representation class whose configuration weights $w_0, w_1 \ge 0$ are nonnegative and whose partition sum $Z = w_0 + w_1$ obeys the odd anomalous Ward identity $Z = -Z$ ($U(f) Z = -Z$), every representation satisfies $w_0 = 0 \wedge w_1 = 0$, ruling out any positive partition sum $Z > 0$ within that declared symmetry-preserving class ([`anomaly_odd_ward_identity_rules_out_positive_weights_in_class`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspCobordismIntrinsicSign.lean#L134-L142)).
   - Coupling a 4D boundary class $\nu_5 \in \mathbb{Z}_2$ to its 5D bulk topological inflow partner $-\nu_5 \in \mathbb{Z}_2$ cancels the total class ($\nu_5 + (-\nu_5) = 0$) and yields positive product sign $(-1)^{\nu_5} (-1)^{\nu_5} = +1$ ([`five_d_bulk_inflow_cancels_boundary_anomaly_sign`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspCobordismIntrinsicSign.lean#L147-L152)).

5. **Class-Specificity, $\mathrm{Pin}^-$ $\mathbb{Z}_{16}$, and Thermal Asymmetry Scope Fences (`GIN-C22`)**:
   - Outside the symmetry-constrained representation class, a basis change can eliminate off-diagonal negative signs: conjugating $\mathrm{offDiagSignedMat} = \begin{pmatrix} 1 & -1 \\ -1 & 1 \end{pmatrix}$ by the unnormalized Hadamard matrix $P = \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$ diagonalizes it to $2 \cdot \begin{pmatrix} 0 & 0 \\ 0 & 2 \end{pmatrix}$ with nonnegative entries while preserving $\mathrm{Tr} = 2$ and $\det = 0$ ([`basis_change_removes_sign_outside_constrained_class_fence`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspCobordismIntrinsicSign.lean#L181-L188)).
   - In $\mathbb{Z}_{16}$ ($\Omega_5^{\mathrm{Pin}^-}$), the generator $1$ is not annihilated by 2-fold or 8-fold pairing ($2 \cdot 1 \neq 0, 8 \cdot 1 \neq 0$), and thermal orientation weight asymmetry $w_+ \neq w_-$ leaves a nonzero residual $w_+ - w_- \neq 0$ even when $\nu_5 = 0$ ([`pin_minus_z16_order_sixteen_fence`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspCobordismIntrinsicSign.lean#L156-L161), [`thermal_orientation_weight_asymmetry_fence`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspCobordismIntrinsicSign.lean#L193-L196)).

---

## 3. Summary of Claims (Claim Hygiene Compliance)

1. **What it supports**:
   - Formalizes in Lean 4 ([`lean4/CampaignFspCobordismIntrinsicSign.lean`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspCobordismIntrinsicSign.lean)) and an independent exact-arithmetic Python verifier ([`checks/independent/fsp-cobordism-intrinsic-sign.py`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/checks/independent/fsp-cobordism-intrinsic-sign.py)) the discrete spectral asymmetry $\Delta\eta = +2$ zero-crossing jump, the $2 \times 2$ mapping-torus determinant sign reversal at $m = 0$, the Arf-0 ($+2$) vs Arf-1 ($-2$) Gaussian sign sum dichotomy, the mod-2 AHSS cobordism pairing $\nu_5 = a_3 \cdot \mathrm{Arf} + w_1 \cdot (\sigma/16)$, the class-specific no-go for nonnegative representations obeying an odd anomaly Ward identity $Z = -Z$, 5D bulk inflow cancellation $\nu_5 + (-\nu_5) = 0$, and the Hadamard basis-change and $\mathbb{Z}_{16}$ scope fences.
2. **What it does not support**:
   - Does not compute smooth continuum Atiyah-Patodi-Singer $\eta$-invariants on 5-manifolds or claim a representation-independent sign no-go outside the declared symmetry-preserving representation class (`GIN-C22`).
3. **Narrowest defensible claim**:
   - Within any representation class whose nonnegative weights $w_i \ge 0$ preserve an odd anomaly Ward identity $Z = -Z$ (induced in the finite prototype by an odd zero-mode crossing, Arf-1 quadratic refinement, or $\nu_5 = 1$ mod-2 cobordism pairing), no positive partition sum $Z > 0$ exists without either coupling to a compensating 5D bulk counterterm $-\nu_5$ or leaving the symmetry-constrained representation class.
4. **Next test needed**:
   - Narrow `PGW-IDENTITY-CONVENTION-UNDECIDABLE` in the frontier derivation queue.
