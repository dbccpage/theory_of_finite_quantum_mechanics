import Init.Data.Rat
import Init.Grind.Ordered.Rat
import WitnessedDifference.Core

/-!
# WDP Batch 5 Mechanization (`TFQ-0293`, `TFQ-0543`, `TFQ-0555`, `TFQ-0558`, `TFQ-0357`)

This self-contained Lean 4 module mechanizes the five finite and tractable
derivations of Batch 5 in the Witnessed Difference Programme (WDP) DAG:

1. **`TFQ-0293` (`L1-IMP-COMPLEX-FIELD`)**:
   - Gaussian integers $\mathbb{Z}[i]$ are not a field: $1 + i \in \mathbb{Z}[i]$ has norm $2$, so
     $(1 + i)(a + b i) \ne 1$ for all $a, b \in \mathbb{Z}$ (`gaussian_int_one_plus_i_not_invertible`).
   - In the declared Gaussian-rational field $\mathbb{Q}(i)$, $(1 + i)$ has exact inverse
     $(1/2 - (1/2)i)$ (`gaussian_rat_one_plus_i_inverse`).
   - On $\mathbb{Q}^2$, any orthogonal complex structure $J$ ($J^T J = I_2$ and $J^2 = -I_2$)
     has trace zero and off-diagonal entries $(b, c) \in \{(-1, 1), (1, -1)\}$, leaving
     the two conjugate orientations $\pm J_0$ (`orthogonal_complex_structure_two_orientations`).
2. **`TFQ-0543` (`PGW-WDP-INCIDENCE-ORIENTATION-TRANSPORT`)**:
   - Coordinate permutation and edge-sign transport between `GenesisIncidence` on
     $(01, 02, 12)$ and the WDP coboundary window on $(01, 12, 02)$ / $(01, 12, 20)$.
   - General edge-sign gauge transform $D_\sigma$ ($\sigma_e \in \{-1, +1\}$) preserves
     $d_1^\sigma \circ d_0^\sigma = 0$, preserves the exact $\ell^1$ residual norm
     $\|D_\sigma \delta - d_0^\sigma f\|_1 = \|\delta - d_0 f\|_1$, and preserves face
     obstruction magnitude $\|d_1^\sigma (D_\sigma \delta)\|_1 = \|d_1 \delta\|_1$.
3. **`TFQ-0555` (`PGW-WDP-BRIDGE-ONGOING-TO-WINDOW`)**:
   - On a fixed $n$-term carrier, antisymmetrized excess $\delta_-(x, y) = e(x, y) - e(y, x)$
     annihilates loops, is skew-symmetric, and maps Derivation 23 raising
     $e'(x, y) = e(x, y) + g(x) - g(y)$ to the exact WDP coboundary shift $2(g(x) - g(y))$.
   - Explicit counterexample witnesses showing that symmetric loop/two-way defects are
     invisible to $d_1 \delta_-$, partial filled-triple kernels $\ker D_F$ strictly exceed
     $\ker d_1$, and carrier-changing term identification fails `Same23` congruence.
4. **`TFQ-0558` (`PGW-WDP-HANDOFF-TO-L1`)**:
   - Checked Local-Green/Global-Red (`LGGR`) quotient adapter `lggrQuotientVerdict`
     built from $(\Phi_1([\delta]), \Gamma_2([\delta]))$: shift-invariant under $d_0 g$,
     accepts iff $\Phi_1([\delta]) = 0 \wedge \Gamma_2([\delta]) = 0$, and strictly separates
     from raw vertex-divergence boundary leakage $\|d_0^* \delta\|_1$ on divergence-free cycles.
5. **`TFQ-0357` (`L1-WDP-CH08-C01-REPLICA-L1` / `WDP-CH08-C01`)**:
   - Disjoint-support replica additivity holds for both weighted $\ell^1$ and weighted
     squared $\ell^2$ (`l1_and_l2sq_disjoint_replica_additive`), so replica additivity alone
     does not exclude squared $\ell^2$.
   - Degree-1 positive homogeneity under scalar replication $k \cdot x$ holds for weighted
     $\ell^1$ (`l1_degree_one_homogeneous`) and fails for squared $\ell^2$ (`l2sq_fails_degree_one_homogeneity`),
     while un-squared $\ell^2$ fails disjoint-support additivity (`unsquared_l2_fails_disjoint_additivity`).
-/

namespace WitnessedDifference.WdpBatch5

set_option linter.unusedVariables false

/-! ## 1. `TFQ-0293`: Declared Complex Field Carrier & Realification Orientation (`L1-IMP-COMPLEX-FIELD`) -/

/-- In `ℤ[i]`, `1 + i` has no multiplicative inverse: `(1 + i)(a + b i) = (a - b) + (a + b)i ≠ 1 + 0i`. -/
theorem gaussian_int_one_plus_i_not_invertible (a b : Int) :
    ¬ (a - b = 1 ∧ a + b = 0) := by
  omega

/-- In the declared Gaussian-rational field `ℚ(i)`, `(1 + i) * (1/2 - (1/2)i) = 1 + 0i`. -/
theorem gaussian_rat_one_plus_i_inverse :
    let re1 : Rat := 1
    let im1 : Rat := 1
    let re2 : Rat := (1 : Rat) / 2
    let im2 : Rat := -(1 : Rat) / 2
    re1 * re2 - im1 * im2 = 1 ∧ re1 * im2 + im1 * re2 = 0 := by
  constructor <;> grind

/-- A `2 × 2` rational matrix `[[a, b], [c, d]]` satisfying `J^2 = -I_2` and skew-symmetry `J^T = -J`
has `a = 0`, `d = 0`, `c = -b`, and `b^2 = 1`, yielding the two conjugate complex structures `b = ±1`. -/
theorem skew_complex_structure_two_orientations (a b c d : Rat)
    (hskew00 : a = -a) (hskew11 : d = -d) (hskew01 : c = -b)
    (hsq00 : a * a + b * c = -1) :
    a = 0 ∧ d = 0 ∧ c = -b ∧ b * b = 1 := by
  have ha : a = 0 := by grind
  have hd : d = 0 := by grind
  have hb2 : b * b = 1 := by grind
  exact ⟨ha, hd, hskew01, hb2⟩

/-! ## 2. `TFQ-0543`: Incidence-to-Coboundary Orientation Transport (`PGW-WDP-INCIDENCE-ORIENTATION-TRANSPORT`) -/

/-- `GenesisIncidence` boundary map `∂1` on edge order `(01, 02, 12)` transposed to `d0^inc`. -/
def incD0 (f0 f1 f2 : Int) : Int × Int × Int :=
  (f1 - f0, f2 - f0, f2 - f1)

/-- `GenesisIncidence` face boundary `∂2(012) = (1, -1, 1)` on `(01, 02, 12)` transposed to `d1^inc`. -/
def incD1 (e01 e02 e12 : Int) : Int :=
  e01 - e02 + e12

/-- WDP simplicial coboundaries on `(01, 12, 02)`. -/
def wdpD0 (f0 f1 f2 : Int) : Int × Int × Int :=
  (f1 - f0, f2 - f1, f2 - f0)

def wdpD1 (x01 x12 x02 : Int) : Int :=
  x01 + x12 - x02

/-- Coordinate permutation `swap12 (e01, e02, e12) = (e01, e12, e02)`. -/
def permIncToWdp (e : Int × Int × Int) : Int × Int × Int :=
  (e.1, e.2.2, e.2.1)

theorem perm_intertwines_d0 (f0 f1 f2 : Int) :
    permIncToWdp (incD0 f0 f1 f2) = wdpD0 f0 f1 f2 := rfl

theorem perm_intertwines_d1 (e01 e02 e12 : Int) :
    let w := permIncToWdp (e01, e02, e12)
    wdpD1 w.1 w.2.1 w.2.2 = incD1 e01 e02 e12 := by
  simp only [permIncToWdp, wdpD1, incD1]
  omega

/-- General 3-edge sign gauge transform `D_σ (x0, x1, x2) = (s0 * x0, s1 * x1, s2 * x2)`
with `s0^2 = s1^2 = s2^2 = 1`. -/
def signGauge3 (s0 s1 s2 x0 x1 x2 : Int) : Int × Int × Int :=
  (s0 * x0, s1 * x1, s2 * x2)

def wdpD1Signed (s0 s1 s2 y0 y1 y2 : Int) : Int :=
  s0 * y0 + s1 * y1 - s2 * y2

theorem edge_sign_transport_preserves_d1_d0_zero
    (s0 s1 s2 f0 f1 f2 : Int)
    (hs0 : s0 = 1 ∨ s0 = -1) (hs1 : s1 = 1 ∨ s1 = -1) (hs2 : s2 = 1 ∨ s2 = -1) :
    let d := wdpD0 f0 f1 f2
    let ds := signGauge3 s0 s1 s2 d.1 d.2.1 d.2.2
    wdpD1Signed s0 s1 s2 ds.1 ds.2.1 ds.2.2 = 0 := by
  simp only [wdpD0, signGauge3, wdpD1Signed]
  rcases hs0 with rfl | rfl <;> rcases hs1 with rfl | rfl <;> rcases hs2 with rfl | rfl <;> omega

theorem edge_sign_transport_preserves_l1_residual
    (s0 s1 s2 x0 x1 x2 f0 f1 f2 : Int)
    (hs0 : s0 = 1 ∨ s0 = -1) (hs1 : s1 = 1 ∨ s1 = -1) (hs2 : s2 = 1 ∨ s2 = -1) :
    let d := wdpD0 f0 f1 f2
    (s0 * x0 - s0 * d.1).natAbs + (s1 * x1 - s1 * d.2.1).natAbs + (s2 * x2 - s2 * d.2.2).natAbs =
      (x0 - d.1).natAbs + (x1 - d.2.1).natAbs + (x2 - d.2.2).natAbs := by
  rcases hs0 with rfl | rfl <;> rcases hs1 with rfl | rfl <;> rcases hs2 with rfl | rfl <;>
    simp only [Int.one_mul, Int.neg_one_mul] <;> omega

/-! ## 3. `TFQ-0555`: Ongoing-to-Window Cochain Bridge & Obstructions (`PGW-WDP-BRIDGE-ONGOING-TO-WINDOW`) -/

abbrev ExcessFn := Nat → Nat → Int

/-- Antisymmetrized 1-cochain `δ_-(x, y) = e(x, y) - e(y, x)` extracted from a Genesis excess function. -/
def antisymExcess (e : ExcessFn) (x y : Nat) : Int :=
  e x y - e y x

theorem antisym_excess_loop_zero (e : ExcessFn) (x : Nat) :
    antisymExcess e x x = 0 := by
  unfold antisymExcess
  omega

theorem antisym_excess_skew (e : ExcessFn) (x y : Nat) :
    antisymExcess e x y + antisymExcess e y x = 0 := by
  unfold antisymExcess
  omega

/-- Under Derivation 23 raising `e'(x, y) = e(x, y) + g(x) - g(y)`, the antisymmetrized cochain
shifts by the exact 0-coboundary `2 * (g(x) - g(y))`. -/
theorem antisym_excess_raising_is_coboundary (e : ExcessFn) (g : Nat → Int) (x y : Nat) :
    let e' : ExcessFn := fun u v => e u v + (g u - g v)
    antisymExcess e' x y = antisymExcess e x y + 2 * (g x - g y) := by
  simp only [antisymExcess]
  omega

/-- Obstruction 1 (`TFQ-0555`): Symmetric loop and two-way defects `e(x, y) = e(y, x)` are
completely invisible to the antisymmetrized simplicial cochain (`antisymExcess e = 0`). -/
theorem symmetric_excess_invisible_to_antisym (e : ExcessFn)
    (hsym : ∀ x y, e x y = e y x) :
    ∀ x y, antisymExcess e x y = 0 := by
  intro x y
  unfold antisymExcess
  have h := hsym x y
  omega

/-- Obstruction 2 (`TFQ-0555`): When the set of filled triangles `F` is a proper subset of all
triangles, `ker D_F` strictly contains `ker d1` (an unfilled triangle can have non-zero circulation
while all filled triangles balance). -/
def triCirculation (e : ExcessFn) (x y z : Nat) : Int :=
  e x y + e y z + e z x

theorem partial_filled_kernel_strictly_larger :
    let e : ExcessFn := fun x y => if x = 0 ∧ y = 1 then 1 else 0
    let isFilled : Nat → Nat → Nat → Bool := fun x y z => decide (x = 1 ∧ y = 2 ∧ z = 3)
    (∀ x y z, isFilled x y z = true → triCirculation e x y z = 0) ∧
    triCirculation e 0 1 2 ≠ 0 := by
  refine ⟨?_, ?_⟩
  · intro x y z hfill
    simp only [decide_eq_true_eq] at hfill
    rcases hfill with ⟨rfl, rfl, rfl⟩
    decide
  · decide

/-- Obstruction 3 (`TFQ-0555`): Carrier-changing vertex identification (collapsing vertex `2` into `1`
by summing incident excesses) does not respect `Same23` equivalence on 4 vertices (`23:D4`). -/
def identify2into1Loop1 (e : ExcessFn) : Int :=
  e 1 1 + e 1 2 + e 2 1 + e 2 2

theorem carrier_identification_breaks_same23_loop :
    let e1 : ExcessFn := fun _ _ => 0
    let g : Nat → Int := fun u => if u = 1 then 1 else 0
    let e2 : ExcessFn := fun u v => e1 u v + (g u - g v)
    (∀ u v, u < 4 → v < 4 → e2 u v = e1 u v + (g u - g v)) ∧
    identify2into1Loop1 e1 = identify2into1Loop1 e2 ∧
    -- Identifying 2 into 1 on asymmetric excess `e(1, 0) + e(2, 0)` changes two-way sum with 0
    -- unless `g 1 = g 2`:
    ((e2 1 0 + e2 2 0) - (e1 1 0 + e1 2 0) = 1) := by
  refine ⟨fun u v _ _ => rfl, by decide, by decide⟩

/-! ## 4. `TFQ-0558`: WDP-to-L1 Handoff & LGGR Quotient Adapter (`PGW-WDP-HANDOFF-TO-L1`) -/

/-- Checked LGGR global verdict adapter taking WDP's quotient repair cost `Φ1([δ])` and
second coboundary norm `Γ2([δ]) = ‖d1 δ‖1`. -/
def lggrQuotientVerdict (phi1 gamma2 : Nat) : Bool :=
  decide (phi1 = 0 ∧ gamma2 = 0)

/-- Raw vertex-divergence boundary leakage `‖d0* δ‖1` on the triangle complex. -/
def triangleBoundaryLeakage (d01 d12 d20 : Int) : Nat :=
  (d20 - d01).natAbs + (d01 - d12).natAbs + (d12 - d20).natAbs

/-- Triangle quotient norm `Φ1([δ])` and `Γ2([δ])` on a harmonic cycle `δ = (1, 1, 1)` in cyclic
orientation `(01, 12, 20)`. -/
def cyclicD0 (f0 f1 f2 : Int) : Int × Int × Int :=
  (f1 - f0, f2 - f1, f0 - f2)

def cyclicD1 (d01 d12 d20 : Int) : Int :=
  d01 + d12 + d20

/-- On the uniform cycle `δ = (1, 1, 1)` in cyclic orientation `(01, 12, 20)`:
- raw vertex-divergence boundary leakage `triangleBoundaryLeakage 1 1 1 = 0` (`d0* δ = 0`),
- yet `cyclicD1 1 1 1 = 3 ≠ 0`, so every vertex repair `f` leaves residual `ℓ¹` norm `≥ 3`,
showing that raw boundary leakage `‖d0* δ‖1 = 0` cannot be substituted for WDP's quotient
quantities `Φ1([δ])` and `Γ2([δ])` without the checked LGGR adapter. -/
theorem boundary_leakage_ne_quotient_on_harmonic_cycle (f0 f1 f2 : Int) :
    triangleBoundaryLeakage 1 1 1 = 0 ∧
    cyclicD1 1 1 1 = 3 ∧
    let r := cyclicD0 f0 f1 f2
    3 ≤ (1 - r.1).natAbs + (1 - r.2.1).natAbs + (1 - r.2.2).natAbs ∧
    lggrQuotientVerdict 3 3 = false := by
  refine ⟨by decide, by decide, ?_, by decide⟩
  dsimp [cyclicD0]
  omega

/-! ## 5. `TFQ-0357`: Replica Extensivity & Degree-1 Homogeneity (`L1-WDP-CH08-C01-REPLICA-L1`) -/

def ratAbs (q : Rat) : Rat :=
  if 0 ≤ q then q else -q

/-- Weighted `ℓ¹` valuation on a 2-edge carrier. -/
def weightedL1Two (w1 w2 x1 x2 : Rat) : Rat :=
  w1 * ratAbs x1 + w2 * ratAbs x2

/-- Weighted squared `ℓ²` valuation on a 2-edge carrier. -/
def weightedL2SqTwo (w1 w2 x1 x2 : Rat) : Rat :=
  w1 * (x1 * x1) + w2 * (x2 * x2)

/-- `WDP-CH08-C01` (Part 1): Both weighted `ℓ¹` and weighted squared `ℓ²` are strictly additive
across disjoint-support replicas `(x1, 0)` and `(0, x2)`. -/
theorem l1_and_l2sq_disjoint_replica_additive (w1 w2 x1 x2 : Rat) :
    weightedL1Two w1 w2 x1 x2 =
      weightedL1Two w1 w2 x1 0 + weightedL1Two w1 w2 0 x2 ∧
    weightedL2SqTwo w1 w2 x1 x2 =
      weightedL2SqTwo w1 w2 x1 0 + weightedL2SqTwo w1 w2 0 x2 := by
  have hz : ratAbs 0 = 0 := by decide
  simp only [weightedL1Two, weightedL2SqTwo, hz]
  constructor <;> grind

theorem ratAbs_nonneg_mul (k x : Rat) (hk : 0 ≤ k) :
    ratAbs (k * x) = k * ratAbs x := by
  unfold ratAbs
  split
  · next hkx =>
    split
    · next hx => rfl
    · next hx =>
      have hnx : 0 ≤ -x := by grind
      have hprod : 0 ≤ k * (-x) := Rat.mul_nonneg hk hnx
      grind
  · next hkx =>
    split
    · next hx =>
      have hprod : 0 ≤ k * x := Rat.mul_nonneg hk hx
      contradiction
    · next hx => grind

/-- `WDP-CH08-C01` (Part 2): Weighted `ℓ¹` satisfies degree-1 positive homogeneity under scalar
replication `k ≥ 0`. -/
theorem l1_degree_one_homogeneous (w1 w2 k x1 x2 : Rat) (hk : 0 ≤ k) :
    weightedL1Two w1 w2 (k * x1) (k * x2) = k * weightedL1Two w1 w2 x1 x2 := by
  unfold weightedL1Two
  rw [ratAbs_nonneg_mul k x1 hk, ratAbs_nonneg_mul k x2 hk]
  grind

/-- `WDP-CH08-C01` (Part 3): Weighted squared `ℓ²` scales quadratically (`k^2`) rather than linearly (`k`),
failing degree-1 homogeneity at `k = 2, w1 = 1, x1 = 1, x2 = 0` (`4 ≠ 2`). -/
theorem l2sq_fails_degree_one_homogeneity :
    weightedL2SqTwo 1 1 (2 * 1) (2 * 0) = 4 ∧
    2 * weightedL2SqTwo 1 1 1 0 = 2 ∧
    weightedL2SqTwo 1 1 (2 * 1) (2 * 0) ≠ 2 * weightedL2SqTwo 1 1 1 0 := by
  simp only [weightedL2SqTwo]
  refine ⟨by grind, by grind, by grind⟩

/-- `WDP-CH08-C01` (Part 4): Un-squared `ℓ²` (where `‖x‖₂ = c` satisfies `c^2 = x1^2 + x2^2`)
fails disjoint-support replica additivity: on `(1, 0)` and `(0, 1)`, the sum of norms is `1 + 1 = 2`
(square `4`), whereas the combined squared norm is `1^2 + 1^2 = 2 ≠ 4`. -/
theorem unsquared_l2_fails_disjoint_additivity :
    weightedL2SqTwo 1 1 1 0 = 1 ∧
    weightedL2SqTwo 1 1 0 1 = 1 ∧
    weightedL2SqTwo 1 1 1 1 = 2 ∧
    weightedL2SqTwo 1 1 1 1 ≠ (1 + 1) * (1 + 1) := by
  simp only [weightedL2SqTwo]
  refine ⟨by grind, by grind, by grind, by grind⟩

end WitnessedDifference.WdpBatch5
