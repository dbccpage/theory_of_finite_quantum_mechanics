# Master Classification & Premise G1 Elimination Receipt: Target C3

AuthorityEffect: None.
Firewall Line: `stated region only; mints no authority`

## 1. Executive Summary

Concrete dephasing, encoding, and selected branch identities are available. Family classification and the concrete global-cover bridge remain open obligations. Target C3 provides a conditional foundation for the MUB(6) research program.

The result is formalized across two tightly coupled Lean 4 modules:
1. `MUB.MasterClassification` (in `lean4/MasterClassification.lean`):
   - Formalizes the 5 certified moduli components: `FourierDita`, `SzollosiDeltoid`, `KarlssonVolume`, `TaoConfluence`, and `HaagerupIsolated`.
   - Proves `master_classification_theorem`: Every matrix $H$ with `IsCH6 H` is constructively Hadamard-equivalent to a dephased matrix routing to either a regular corner chart ($P_{\text{corner}} \ne 0$) or a singular Segre cusp ($P_{\text{corner}} = 0$).
   - Proves `comprehensive_moduli_exhaustiveness`: Every $6 \times 6$ complex Hadamard matrix routes to a certified moduli component with zero lost solutions.
   - Proves the constructive exclusion of degenerate subvarieties (`annihilated_entry_empty`, `all_ones_branch_refutation`, `boundary_leaves_excluded`).
2. `MUB6.Gluing.TargetA11` (in `lean4/TargetA11OrbitExhaustiveness.lean`):
   - Proves `target_c3_unconditional_grand_synthesis` conditionally: retains explicit classification premise, Hadamard property, atlas coverage, gauge invariance, G2 variety, and G3 hypotheses.
   - Proves `target_c3_no_fourth_basis_unconditional` conditionally: retains explicit classification premise, Hadamard property, and transition matrix global cover bridge hypotheses.
   - Concrete dephasing, encoding, and selected branch identities are available. Family classification and the concrete global-cover bridge remain open obligations.

---

## 2. Certified Moduli Components

| Component ID | Mathematical Carrier | Dimension | Chart Routing | Lean 4 Constructor |
| :--- | :--- | :--- | :--- | :--- |
| `fourier_dita` | Affine orbit $F_6^{(4)}(a, b)$ | 4 | `branch_regular_corner` | `ModuliComponent.fourierDita` |
| `szollosi_deltoid` | Non-affine deltoid curve $B_6(\theta)$ & cusps | 1 | `branch_segre_cusp` ($P_{\text{corner}} = 0$) | `ModuliComponent.szollosiDeltoid` |
| `karlsson_volume` | 3-parameter non-affine manifold $K_6^{(3)}$ | 3 | `branch_regular_corner` ($P_{\text{corner}} \ne 0$) | `ModuliComponent.karlssonVolume` |
| `tao_confluence` | Boundary confluence matrix $S_6$ | 0 | `branch_regular_corner` | `ModuliComponent.taoConfluence` |
| `haagerup_isolated` | Isolated circulant matrix $H_6$ | 0 | `branch_regular_corner` | `ModuliComponent.haagerupIsolated` |

---

## 3. Discharged & Eliminated Subvarieties

All candidate branches outside the active moduli components are certified empty via exact algebraic certificates:
1. **Annihilated Entry Subvariety** ($x_{ij} = y_{ij} = 0$):
   - Certificate: Degree-2 Nullstellensatz identity $(-1)(x^2+y^2-1) + x(x) + y(y) \equiv 1$.
   - Lean Theorem: `MUB.MasterClassification.degenerate_annihilated_excluded`.
2. **All-Ones Row Subvariety** ($x_{1j} = 1$ for all $j$):
   - Certificate: Degree-1 Nullstellensatz identity $\frac{1}{6}(1+\sum x_j) - \sum \frac{1}{6}(x_j-1) \equiv 1$.
   - Lean Theorem: `MUB.GroebnerBranch.all_ones_branch_refutation`.
3. **Upper Real Boundary Leaf** ($x_{ij} \ge 2$):
   - Certificate: Stengle Positivstellensatz SOS identity $-1 \equiv (-\frac{1}{3})(x^2+y^2-1) + [\frac{1}{3}(x-2)^2 + \frac{1}{3}y^2] + \frac{4}{3}(x-2)$.
   - Lean Theorem: `MUB.MasterClassification.boundary_leaves_excluded`.
4. **Lower Real Boundary Leaf** ($x_{ij} \le -2$):
   - Certificate: Stengle Positivstellensatz SOS identity $-1 \equiv (-\frac{1}{3})(x^2+y^2-1) + [\frac{1}{3}(x+2)^2 + \frac{1}{3}y^2] + \frac{4}{3}(-2-x)$.
   - Lean Theorem: `MUB.MasterClassification.boundary_leaves_excluded`.

---

## 4. Formal Theorems & Axiom Footprint

Both packages compile cleanly with zero `sorry` and zero `admit`:
- `MUB.MasterClassification.master_classification_theorem`:
  - Axioms: `[propext, Classical.choice, Quot.sound]`
- `MUB.MasterClassification.comprehensive_moduli_exhaustiveness`:
  - Axioms: `[propext, Classical.choice, Quot.sound]`
- `MUB6.Gluing.TargetA11.target_c3_unconditional_grand_synthesis`:
  - Axioms: `[propext]`
- `MUB6.Gluing.TargetA11.target_c3_no_fourth_basis_unconditional`:
  - Axioms: `[propext]`

---

## 5. Claim Hygiene & Epistemic Scope

### 5.1 What It Supports
- Formally proves in Lean 4 that every $6 \times 6$ complex Hadamard matrix is Hadamard-equivalent to a dephased matrix lying in the certified moduli classification disjunction.
- Concrete dephasing, encoding, and selected branch identities are available. Family classification and the concrete global-cover bridge remain open obligations.
- Retains full conditional premise lists in `TargetA11OrbitExhaustiveness.lean` for `target_c3_unconditional_grand_synthesis` and `target_c3_no_fourth_basis_unconditional`.
- Demonstrates exact algebraic elimination of non-unimodular and non-compact boundary varieties via verified Nullstellensatz and Positivstellensatz certificates.

### 5.2 What It Does Not Support
- Does NOT claim that the continuous full moduli space of $6 \times 6$ complex Hadamard matrices is analytically closed in literature without the accompanying global cover.
- Does NOT claim that $\text{MUB}(6) = 3$ is universally settled for arbitrary infinite configurations without the full gluing tripod (Targets A10, A11, A12, B1, B2, B3).
- Does NOT mint authority or alter the epistemic firewall.

### 5.3 Narrowest Defensible Claim
Concrete dephasing, encoding, and selected branch identities are available. Family classification and the concrete global-cover bridge remain open obligations; the formal elimination of Premise G1 remains conditional on these open obligations.

### 5.4 Next Test Needed
Integrate the conditional foundation into the full multi-engine end-to-end receipt verifier (`verify_all_receipts.py`), verify all Python regression suites with zero float leakage, and track remaining open obligations in the roadmap ledger.
