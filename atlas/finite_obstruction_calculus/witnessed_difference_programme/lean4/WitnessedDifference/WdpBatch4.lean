import Init.Data.Rat
import Init.Grind.Ordered.Rat
import WitnessedDifference.Core

/-!
# WDP Batch 4 Mechanization (`TFQ-0580`, `TFQ-1026`, `TFQ-0391`, `TFQ-0544`, `TFQ-0556`)

This self-contained Lean 4 module mechanizes the five finite and tractable
derivations of Batch 4 in the Witnessed Difference Programme (WDP) DAG:

1. **`TFQ-0580` (`PGW-WDP-EXACT-SCALAR-HADAMARD-OBSTRUCTION` / `GEN-WDP-68`)**:
   2-adic parity descent showing $2 a^2 \ne b^2$ for all nonzero integers $b \ne 0$,
   so no rational fraction $(a/b)$ squares to $1/2$ and neither the real symmetric
   Hadamard matrix nor the $T$-gate candidate is unitary over exact rational/Gaussian-rational
   scalars without quadratic extension or scaled-unitary tracking.
2. **`TFQ-1026` (`FQ-IMPL-WDP-AMPLITUDE-BRIDGE` / `WDP-CH19-P11..P12`)**:
   Exact Gaussian-rational amplitude bridge: unit norm of the Pythagorean phase
   $u = (3 + 4i)/5$, coboundary invariance of triangle cycle holonomy exponents,
   common-phase invariance of both quadratic $N(z_1 + z_2)$ and quartic $N(z_1 + z_2)^2$
   readouts together with their non-coincidence on interference inputs, and the
   modulo-5 induction $(3 + 4i)^n \equiv 3 + 4i \pmod{5}$ showing $u^n \ne 1$ for all $n \ge 1$.
3. **`TFQ-0391` (`PG-GEN-SAMENESS-REFINEMENTS`)**:
   Four-stage sameness refinement hierarchy (`Same22`, `Same23`, `Same24`, `Same25`)
   from Genesis derivations 22–25 and its exact cohomological invariants:
   loop excess $e(x,x)$, symmetric two-way sum $e(x,y)+e(y,x)$, triangle circulation
   $e(x,y)+e(y,z)+e(z,x)$, filled-term loop balance, and filled-triple circulation balance.
4. **`TFQ-0544` (`PGW-WDP-PHI-WELL-DEFINED-L1-DUALITY` / `WDP-CH04-P01`, `P02`, `C01`, `P07`)**:
   Representative independence of residual repair costs under vertex coboundary shifts,
   weighted $\ell^1$ weak duality over $\mathbb{Q}$ on the triangle complex, and
   global primal optimality certified by a matching dual circulation.
5. **`TFQ-0556` (`PGW-WDP-BRIDGE-REPORT-FIBER-OBSERVER` / `GEN-WDP-03`, `GEN-WDP-06`)**:
   Necessary and sufficient fiber-constancy condition for decision decoders on
   occupied reports, post-processing obstruction, and concrete witness separations
   showing that event multisets lose final state and final states lose occurrence counts.
-/

namespace WitnessedDifference.WdpBatch4

set_option linter.unusedVariables false

/-! ## 1. `TFQ-0580`: Exact Scalar Hadamard Obstruction (`GEN-WDP-68`) -/

theorem two_mul_sq (k : Nat) : (2 * k) * (2 * k) = 4 * (k * k) := by
  calc (2 * k) * (2 * k)
    _ = 2 * (k * (2 * k)) := Nat.mul_assoc 2 k (2 * k)
    _ = 2 * (2 * k * k) := by rw [Nat.mul_comm k (2 * k)]
    _ = 2 * (2 * (k * k)) := by rw [Nat.mul_assoc 2 k k]
    _ = (2 * 2) * (k * k) := (Nat.mul_assoc 2 2 (k * k)).symm
    _ = 4 * (k * k) := rfl

theorem two_mul_add_one_sq (k : Nat) :
    (2 * k + 1) * (2 * k + 1) = 4 * (k * k) + 4 * k + 1 := by
  rw [Nat.add_mul, Nat.mul_add, Nat.mul_add, two_mul_sq]
  omega

theorem nat_sq_parity_decomp (n : Nat) :
    (n = 2 * (n / 2) ∧ n * n = 4 * ((n / 2) * (n / 2))) ∨
    (n = 2 * (n / 2) + 1 ∧ n * n = 4 * ((n / 2) * (n / 2)) + 4 * (n / 2) + 1) := by
  have hdiv : n = 2 * (n / 2) + (n % 2) := by omega
  have hmod : n % 2 = 0 ∨ n % 2 = 1 := by omega
  rcases hmod with h0 | h1
  · left
    have hn : n = 2 * (n / 2) := by omega
    refine ⟨hn, ?_⟩
    conv => lhs; rw [hn]
    exact two_mul_sq (n / 2)
  · right
    have hn : n = 2 * (n / 2) + 1 := by omega
    refine ⟨hn, ?_⟩
    conv => lhs; rw [hn]
    exact two_mul_add_one_sq (n / 2)

/-- 2-adic parity descent (`GEN-WDP-68`): for all `a b : Nat` with `b > 0`, `2 * a^2 ≠ b^2`. -/
theorem nat_two_mul_sq_ne_sq : ∀ (b a : Nat), b > 0 → 2 * (a * a) ≠ b * b
  | b, a, hb, heq => by
    rcases nat_sq_parity_decomp b with ⟨hb_even, hbsq⟩ | ⟨hb_odd, hbsq⟩
    · rcases nat_sq_parity_decomp a with ⟨ha_even, hasq⟩ | ⟨ha_odd, hasq⟩
      · have hdesc : 2 * ((a / 2) * (a / 2)) = (b / 2) * (b / 2) := by omega
        have hb2_pos : b / 2 > 0 := by omega
        have hb2_lt : b / 2 < b := by omega
        exact nat_two_mul_sq_ne_sq (b / 2) (a / 2) hb2_pos hdesc
      · omega
    · omega
termination_by b => b

theorem int_natAbs_mul_self (x : Int) :
    (x.natAbs * x.natAbs : Nat) = (x * x).natAbs := by
  exact (Int.natAbs_mul x x).symm

/-- Integer form of `GEN-WDP-68`: no rational fraction `a / b` (`b ≠ 0`) satisfies `2 * a^2 = b^2`. -/
theorem int_two_mul_sq_ne_sq (a b : Int) (hb : b ≠ 0) : 2 * (a * a) ≠ b * b := by
  intro heq
  have hnat : 2 * (a.natAbs * a.natAbs) = b.natAbs * b.natAbs := by
    have h1 : (2 * (a * a)).natAbs = (b * b).natAbs := congrArg Int.natAbs heq
    rw [Int.natAbs_mul 2 (a * a), Int.natAbs_mul a a, Int.natAbs_mul b b] at h1
    exact h1
  have hb_pos : b.natAbs > 0 := Int.natAbs_pos.mpr hb
  exact nat_two_mul_sq_ne_sq b.natAbs a.natAbs hb_pos hnat

/-- Exact Gaussian-rational scalar pair. -/
structure GaussianRat where
  re : Rat
  im : Rat
  deriving DecidableEq, Repr

def gzero : GaussianRat := ⟨0, 0⟩
def gone : GaussianRat := ⟨1, 0⟩
def gi : GaussianRat := ⟨0, 1⟩
def gadd (z w : GaussianRat) : GaussianRat := ⟨z.re + w.re, z.im + w.im⟩
def gmul (z w : GaussianRat) : GaussianRat :=
  ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩
def gconj (z : GaussianRat) : GaussianRat := ⟨z.re, -z.im⟩
def gnorm (z : GaussianRat) : Rat := z.re * z.re + z.im * z.im

/-- Unscaled integer-fraction presentation `(a / b)` of a candidate rational Hadamard entry. -/
def hadamardDiagNormNum (a b : Int) : Int := 2 * (a * a)
def hadamardDiagNormDen (b : Int) : Int := b * b

/-- Neither the symmetric real Hadamard matrix `(a/b) [[1,1],[1,-1]]` nor the `T`-gate diagonal
`[[1,0],[0,(a/b)(1+i)]]` can achieve unit column norm `2 a^2 = b^2` for any `a, b ∈ ℤ` with `b ≠ 0`. -/
theorem exact_scalar_hadamard_and_t_obstruction (a b : Int) (hb : b ≠ 0) :
    hadamardDiagNormNum a b ≠ hadamardDiagNormDen b :=
  int_two_mul_sq_ne_sq a b hb

/-! ## 2. `TFQ-1026`: WDP Amplitude Bridge (`WDP-CH19-P11..P12`) -/

theorem gnorm_mul (w z : GaussianRat) :
    gnorm (gmul w z) = gnorm w * gnorm z := by
  cases w
  cases z
  simp only [gnorm, gmul]
  grind

theorem gmul_add (w z1 z2 : GaussianRat) :
    gmul w (gadd z1 z2) = gadd (gmul w z1) (gmul w z2) := by
  cases w
  cases z1
  cases z2
  simp only [gmul, gadd, GaussianRat.mk.injEq]
  constructor <;> grind

/-- Quadratic interference readout `N(z1 + z2)`. -/
def readoutQuadratic (z1 z2 : GaussianRat) : Rat :=
  gnorm (gadd z1 z2)

/-- Quartic interference readout `N(z1 + z2)^2`. -/
def readoutQuartic (z1 z2 : GaussianRat) : Rat :=
  let r := gnorm (gadd z1 z2)
  r * r

/-- Both `readoutQuadratic` and `readoutQuartic` are strictly invariant under a common unit-norm phase `w`. -/
theorem readout_quadratic_phase_invariant (w z1 z2 : GaussianRat) (hw : gnorm w = 1) :
    readoutQuadratic (gmul w z1) (gmul w z2) = readoutQuadratic z1 z2 := by
  unfold readoutQuadratic
  rw [← gmul_add, gnorm_mul, hw]
  grind

theorem readout_quartic_phase_invariant (w z1 z2 : GaussianRat) (hw : gnorm w = 1) :
    readoutQuartic (gmul w z1) (gmul w z2) = readoutQuartic z1 z2 := by
  unfold readoutQuartic
  rw [← gmul_add, gnorm_mul, hw]
  grind

/-- Common-phase invariance does not select `readoutQuadratic` over `readoutQuartic`:
they disagree on constructive interference `z1 = z2 = 1`. -/
theorem readout_quadratic_ne_quartic :
    readoutQuadratic gone gone = 4 ∧
    readoutQuartic gone gone = 16 ∧
    readoutQuadratic gone gone ≠ readoutQuartic gone gone := by
  simp only [readoutQuadratic, readoutQuartic, gone, gadd, gnorm]
  refine ⟨by grind, by grind, by grind⟩

/-- The canonical Pythagorean unit phase `u = (3 + 4i) / 5 ∈ U(1)(ℚ(i))`. -/
def pythagoreanPhase : GaussianRat := ⟨(3 : Rat) / 5, (4 : Rat) / 5⟩

theorem pythagorean_phase_unit_norm : gnorm pythagoreanPhase = 1 := by
  simp only [gnorm, pythagoreanPhase]
  grind

/-- Triangle holonomy exponent `a01 + a12 + a20` for integer edge cochains is strictly invariant
under any vertex coboundary shift `d0 f = (f1 - f0, f2 - f1, f0 - f2)`. -/
def triangleHolonomyExp (a01 a12 a20 : Int) : Int :=
  a01 + a12 + a20

theorem triangle_holonomy_coboundary_invariant (a01 a12 a20 f0 f1 f2 : Int) :
    triangleHolonomyExp (a01 + (f1 - f0)) (a12 + (f2 - f1)) (a20 + (f0 - f2)) =
      triangleHolonomyExp a01 a12 a20 := by
  unfold triangleHolonomyExp
  omega

/-- Gaussian integer powers `(3 + 4i)^n = (re_n, im_n)` certifying that `u^n ≠ 1` for all `n ≥ 1`. -/
def gintPow34 : Nat → Int × Int
  | 0 => (1, 0)
  | n + 1 =>
    let p := gintPow34 n
    (3 * p.1 - 4 * p.2, 3 * p.2 + 4 * p.1)

/-- For every `n : Nat`, `(3 + 4i)^(n + 1) ≡ (3, 4) (mod 5)`. -/
theorem gintPow34_mod5 (n : Nat) :
    (gintPow34 (n + 1)).1 % 5 = 3 ∧ (gintPow34 (n + 1)).2 % 5 = 4 := by
  induction n with
  | zero =>
    simp [gintPow34]
  | succ k ih =>
    simp only [gintPow34] at ih ⊢
    omega

/-- Consequently, the imaginary part of `(3 + 4i)^(n + 1)` is never zero (`im % 5 = 4`),
so `u^(n + 1) = ((3 + 4i) / 5)^(n + 1) ≠ 1` for all `n ≥ 0` (`WDP-CH19-P12`). -/
theorem gintPow34_im_ne_zero (n : Nat) :
    (gintPow34 (n + 1)).2 ≠ 0 := by
  have hmod := (gintPow34_mod5 n).2
  omega

/-! ## 3. `TFQ-0391`: Genesis Sameness Refinements (`PG-GEN-SAMENESS-REFINEMENTS`) -/

/-- Excess function `e(x, y) = M_r(x, y) - M_s(x, y)` on `n` terms. -/
abbrev ExcessFn := Nat → Nat → Int

/-- Derivation 22 sameness at fixed writing: equal pairwise excess. -/
def Same22 (e1 e2 : ExcessFn) : Prop :=
  ∀ x y, e1 x y = e2 x y

/-- Derivation 23 sameness at fixed writing: excess differs by a vertex potential `g(x) - g(y)` from raising terms. -/
def Same23 (e1 e2 : ExcessFn) : Prop :=
  ∃ g : Nat → Int, ∀ x y, e1 x y = e2 x y + (g x - g y)

/-- Derivation 24 sameness at fixed writing: `Same23` on assertions plus identical filled-term predicate `F`. -/
def Same24 (e1 e2 : ExcessFn) (F1 F2 : Nat → Bool) : Prop :=
  Same23 e1 e2 ∧ ∀ x, F1 x = F2 x

/-- Derivation 25 sameness at fixed writing: `Same23` on assertions plus identical filled-triple predicate `T`. -/
def Same25 (e1 e2 : ExcessFn) (T1 T2 : Nat → Nat → Nat → Bool) : Prop :=
  Same23 e1 e2 ∧ ∀ x y z, T1 x y z = T2 x y z

theorem same22_implies_same23 {e1 e2 : ExcessFn} (h : Same22 e1 e2) : Same23 e1 e2 := by
  refine ⟨fun _ => 0, fun x y => ?_⟩
  dsimp
  have hxy := h x y
  omega

/-- Loop excess `e(x, x)` is strictly invariant under Derivation 23 raising (`Same23`). -/
theorem same23_preserves_loops {e1 e2 : ExcessFn} (h : Same23 e1 e2) (x : Nat) :
    e1 x x = e2 x x := by
  rcases h with ⟨g, hg⟩
  have hxx := hg x x
  omega

/-- Two-way sum `e(x, y) + e(y, x)` is strictly invariant under Derivation 23 raising (`Same23`). -/
theorem same23_preserves_two_way {e1 e2 : ExcessFn} (h : Same23 e1 e2) (x y : Nat) :
    e1 x y + e1 y x = e2 x y + e2 y x := by
  rcases h with ⟨g, hg⟩
  have hxy := hg x y
  have hyx := hg y x
  omega

/-- Triangle circulation `e(x, y) + e(y, z) + e(z, x)` is strictly invariant under Derivation 23 raising (`Same23`). -/
def aroundTriple (e : ExcessFn) (x y z : Nat) : Int :=
  e x y + e y z + e z x

theorem same23_preserves_around {e1 e2 : ExcessFn} (h : Same23 e1 e2) (x y z : Nat) :
    aroundTriple e1 x y z = aroundTriple e2 x y z := by
  unfold aroundTriple
  rcases h with ⟨g, hg⟩
  have hxy := hg x y
  have hyz := hg y z
  have hzx := hg z x
  omega

/-- Derivation 24 filled-term balance (`F x = true ∧ e x x = 0`) is an invariant of `Same24`. -/
def TermBalances24 (e : ExcessFn) (F : Nat → Bool) (x : Nat) : Prop :=
  F x = true ∧ e x x = 0

theorem same24_balances_iff {e1 e2 : ExcessFn} {F1 F2 : Nat → Bool}
    (h : Same24 e1 e2 F1 F2) (x : Nat) :
    TermBalances24 e1 F1 x ↔ TermBalances24 e2 F2 x := by
  unfold TermBalances24
  rw [h.2 x, same23_preserves_loops h.1 x]

/-- Derivation 25 filled-triple balance (`T x y z = true ∧ aroundTriple e x y z = 0`) is an invariant of `Same25`. -/
def TripleBalances25 (e : ExcessFn) (T : Nat → Nat → Nat → Bool) (x y z : Nat) : Prop :=
  T x y z = true ∧ aroundTriple e x y z = 0

theorem same25_balances_iff {e1 e2 : ExcessFn} {T1 T2 : Nat → Nat → Nat → Bool}
    (h : Same25 e1 e2 T1 T2) (x y z : Nat) :
    TripleBalances25 e1 T1 x y z ↔ TripleBalances25 e2 T2 x y z := by
  unfold TripleBalances25
  rw [h.2 x y z, same23_preserves_around h.1 x y z]

/-! ## 4. `TFQ-0544`: Quotient Norm Well-Definedness & Weighted $\ell^1$ Duality (`WDP-CH04-P01`, `C01`, `P07`) -/

def ratAbs (q : Rat) : Rat :=
  if 0 ≤ q then q else -q

theorem rat_le_ratAbs (q : Rat) : q ≤ ratAbs q := by
  unfold ratAbs
  split <;> grind

theorem rat_neg_le_ratAbs (q : Rat) : -q ≤ ratAbs q := by
  unfold ratAbs
  split <;> grind

theorem rat_mul_le_mul_ratAbs (y r w : Rat) (hy : ratAbs y ≤ w) :
    y * r ≤ w * ratAbs r := by
  have hy_pos : y ≤ ratAbs y := rat_le_ratAbs y
  have hy_neg : -y ≤ ratAbs y := rat_neg_le_ratAbs y
  unfold ratAbs
  split
  · next hr =>
    have hwy : 0 ≤ w - y := by grind
    have hprod : 0 ≤ (w - y) * r := Rat.mul_nonneg hwy hr
    grind
  · next hr =>
    have hwy : 0 ≤ w + y := by grind
    have hnr : 0 ≤ -r := by grind
    have hprod : 0 ≤ (w + y) * (-r) := Rat.mul_nonneg hwy hnr
    grind

/-- Triangle coboundary `d0 f = (f1 - f0, f2 - f1, f2 - f0)` over `Rat`. -/
def ratD0 (f0 f1 f2 : Rat) : Rat × Rat × Rat :=
  (f1 - f0, f2 - f1, f2 - f0)

/-- Weighted `ℓ¹` residual norm `w01 |r01| + w12 |r12| + w20 |r20|` on the triangle complex. -/
def weightedResidualL1 (w01 w12 w20 d01 d12 d20 f0 f1 f2 : Rat) : Rat :=
  w01 * ratAbs (d01 - (f1 - f0)) +
  w12 * ratAbs (d12 - (f2 - f1)) +
  w20 * ratAbs (d20 - (f2 - f0))

/-- `WDP-CH04-P01`: Representative independence of the weighted `ℓ¹` residual cost under any
coboundary shift `δ' = δ + d0 g` and translated repair `f' = f + g`. -/
theorem weighted_residual_shift_invariant
    (w01 w12 w20 d01 d12 d20 f0 f1 f2 g0 g1 g2 : Rat) :
    weightedResidualL1 w01 w12 w20
      (d01 + (g1 - g0)) (d12 + (g2 - g1)) (d20 + (g2 - g0))
      (f0 + g0) (f1 + g1) (f2 + g2) =
    weightedResidualL1 w01 w12 w20 d01 d12 d20 f0 f1 f2 := by
  unfold weightedResidualL1
  have h1 : d01 + (g1 - g0) - (f1 + g1 - (f0 + g0)) = d01 - (f1 - f0) := by grind
  have h2 : d12 + (g2 - g1) - (f2 + g2 - (f1 + g1)) = d12 - (f2 - f1) := by grind
  have h3 : d20 + (g2 - g0) - (f2 + g2 - (f0 + g0)) = d20 - (f2 - f0) := by grind
  rw [h1, h2, h3]

/-- Dual circulation condition `d0* y = 0` on the triangle complex:
`y01 = y12 = -y20 = c` for a cycle circulation scalar `c`. -/
def dualPairingTriangle (c d01 d12 d20 : Rat) : Rat :=
  c * d01 + c * d12 - c * d20

/-- Dual pairing annihilates every coboundary shift: `⟨y, δ - d0 f⟩ = ⟨y, δ⟩`. -/
theorem dual_pairing_coboundary_invariant (c d01 d12 d20 f0 f1 f2 : Rat) :
    dualPairingTriangle c (d01 - (f1 - f0)) (d12 - (f2 - f1)) (d20 - (f2 - f0)) =
      dualPairingTriangle c d01 d12 d20 := by
  unfold dualPairingTriangle
  grind

/-- `WDP-CH04-P07` / `C01` (Weak Duality over `ℚ`): For any dual circulation `c` bounded by
`|c| ≤ w01`, `|c| ≤ w12`, `|c| ≤ w20` and any vertex repair `(f0, f1, f2)`,
`dualPairingTriangle c d01 d12 d20 ≤ weightedResidualL1 w01 w12 w20 d01 d12 d20 f0 f1 f2`. -/
theorem weighted_l1_weak_duality_triangle
    (c w01 w12 w20 d01 d12 d20 f0 f1 f2 : Rat)
    (hw01 : ratAbs c ≤ w01) (hw12 : ratAbs c ≤ w12) (hw20 : ratAbs (-c) ≤ w20) :
    dualPairingTriangle c d01 d12 d20 ≤
      weightedResidualL1 w01 w12 w20 d01 d12 d20 f0 f1 f2 := by
  rw [← dual_pairing_coboundary_invariant c d01 d12 d20 f0 f1 f2]
  unfold dualPairingTriangle weightedResidualL1
  have b1 := rat_mul_le_mul_ratAbs c (d01 - (f1 - f0)) w01 hw01
  have b2 := rat_mul_le_mul_ratAbs c (d12 - (f2 - f1)) w12 hw12
  have b3 := rat_mul_le_mul_ratAbs (-c) (d20 - (f2 - f0)) w20 hw20
  grind

/-- Certified primal-dual optimality (`WDP-CH04-C01`): whenever a feasible dual circulation `c`
matches the weighted `ℓ¹` residual cost of a candidate repair `(f0*, f1*, f2*)`, that repair
achieves the global minimum across all rational repairs `(f0, f1, f2)`. -/
theorem certified_primal_dual_optimality
    (c w01 w12 w20 d01 d12 d20 f0s f1s f2s f0 f1 f2 : Rat)
    (hw01 : ratAbs c ≤ w01) (hw12 : ratAbs c ≤ w12) (hw20 : ratAbs (-c) ≤ w20)
    (hcert : weightedResidualL1 w01 w12 w20 d01 d12 d20 f0s f1s f2s =
      dualPairingTriangle c d01 d12 d20) :
    weightedResidualL1 w01 w12 w20 d01 d12 d20 f0s f1s f2s ≤
      weightedResidualL1 w01 w12 w20 d01 d12 d20 f0 f1 f2 := by
  rw [hcert]
  exact weighted_l1_weak_duality_triangle c w01 w12 w20 d01 d12 d20 f0 f1 f2 hw01 hw12 hw20

/-! ## 5. `TFQ-0556`: Report-Fiber Observer Bridge (`GEN-WDP-03` & `GEN-WDP-06`) -/

/-- Occupied report image `{r : R // ∃ x, report x = r}`. -/
abbrev OccupiedReport {X : Type} {R : Type} (report : X → R) :=
  {r : R // ∃ x, report x = r}

def liftToOccupied {X : Type} {R : Type} (report : X → R) (x : X) : OccupiedReport report :=
  ⟨report x, ⟨x, rfl⟩⟩

def FiberConstant {X : Type} {R : Type} {D : Type} (report : X → R) (decision : X → D) : Prop :=
  ∀ x y : X, report x = report y → decision x = decision y

/-- Report-kernel setoid `x ≈ y ↔ report x = report y` for constructive `Quotient.lift` descent
(matching `omega_codex`'s `ZeroEquivalence` axiom profile: `[propext, Quot.sound]`, zero `Classical.choice`). -/
def reportKernelSetoid {X : Type} {R : Type} (report : X → R) : Setoid X where
  r x y := report x = report y
  iseqv := ⟨fun _ => rfl, fun h => h.symm, fun h1 h2 => h1.trans h2⟩

abbrev ReportQuotient {X : Type} {R : Type} (report : X → R) :=
  Quotient (reportKernelSetoid report)

/-- Constructive `GEN-WDP-03` (`Quotient.lift` formulation, zero `Classical.choice`):
A decision decoder on the report-kernel quotient `ReportQuotient report` exists and is unique
if and only if `decision` is constant on the fibers of `report`. -/
theorem report_quotient_decoder_iff {X : Type} {R : Type} {D : Type}
    (report : X → R) (decision : X → D) :
    (∃ dec : ReportQuotient report → D,
      (∀ x, dec (Quotient.mk (reportKernelSetoid report) x) = decision x) ∧
      (∀ dec' : ReportQuotient report → D,
        (∀ x, dec' (Quotient.mk (reportKernelSetoid report) x) = decision x) → dec' = dec)) ↔
    FiberConstant report decision := by
  constructor
  · rintro ⟨dec, hdec, _⟩ x y hrep
    have hq : Quotient.mk (reportKernelSetoid report) x =
        Quotient.mk (reportKernelSetoid report) y := Quotient.sound hrep
    exact (hdec x).symm.trans ((congrArg dec hq).trans (hdec y))
  · intro hfib
    let dec : ReportQuotient report → D :=
      Quotient.lift decision (fun x y hxy => hfib x y hxy)
    have hdec : ∀ x, dec (Quotient.mk (reportKernelSetoid report) x) = decision x :=
      fun _ => rfl
    refine ⟨dec, hdec, ?_⟩
    intro dec' hdec'
    funext q
    refine Quotient.inductionOn q (fun x => ?_)
    exact (hdec' x).trans (hdec x).symm

/-- `GEN-WDP-03`: A decision decoder on the occupied report image exists and is unique if and only if
the decision is constant on the fibers of the declared report. -/
theorem report_fiber_decoder_iff {X : Type} {R : Type} {D : Type}
    (report : X → R) (decision : X → D) :
    (∃ dec : OccupiedReport report → D,
      (∀ x, dec (liftToOccupied report x) = decision x) ∧
      (∀ dec' : OccupiedReport report → D,
        (∀ x, dec' (liftToOccupied report x) = decision x) → dec' = dec)) ↔
    FiberConstant report decision := by
  constructor
  · rintro ⟨dec, hdec, _⟩ x y hrep
    have hlift : liftToOccupied report x = liftToOccupied report y := Subtype.ext hrep
    exact (hdec x).symm.trans ((congrArg dec hlift).trans (hdec y))
  · intro hfib
    let dec : OccupiedReport report → D := fun r => decision (Classical.choose r.property)
    have hdec : ∀ x, dec (liftToOccupied report x) = decision x := by
      intro x
      exact hfib (Classical.choose (liftToOccupied report x).property) x
        (Classical.choose_spec (liftToOccupied report x).property)
    refine ⟨dec, hdec, ?_⟩
    intro dec' hdec'
    funext r
    rcases r.property with ⟨x, hx⟩
    have hr : liftToOccupied report x = r := Subtype.ext hx
    rw [← hr, hdec' x, hdec x]

/-- `GEN-WDP-06` (a): Event multiset (count of `+1` and `-1` steps) loses the final state when
step order determines clamping/saturation: `[+1, -1]` vs `[-1, +1]` under `max(0, s + step)`. -/
def clampedFold : List Int → Int → Int
  | [], s => s
  | delta :: rest, s =>
    let next := if s + delta < 0 then 0 else s + delta
    clampedFold rest next

theorem event_multiset_loses_final_state :
    let traceA : List Int := [1, -1]
    let traceB : List Int := [-1, 1]
    traceA.count 1 = traceB.count 1 ∧
    traceA.count (-1) = traceB.count (-1) ∧
    clampedFold traceA 0 ≠ clampedFold traceB 0 := by
  decide

/-- `GEN-WDP-06` (b): Final state loses occurrence counts: `[1, -1]` and `[]` both end at state `0`
from initial state `0`, but have different step occurrence counts (`2 ≠ 0`). -/
theorem final_state_loses_occurrence_count :
    let traceA : List Int := [1, -1]
    let traceB : List Int := []
    clampedFold traceA 0 = clampedFold traceB 0 ∧
    traceA.length ≠ traceB.length := by
  decide

end WitnessedDifference.WdpBatch4
