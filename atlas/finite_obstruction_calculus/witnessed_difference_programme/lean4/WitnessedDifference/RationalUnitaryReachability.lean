import WitnessedDifference.CertifiedPreservers

/-!
# Root-free unitary reachability on the supplied rational Hermitian carrier

This constructs the rank-one isometry and its inverse. The arithmetic
two-squares criterion is a separate, explicit premise only in the final
corollary; it is not an axiom or a hypothesis of the geometric construction.
-/

namespace WitnessedDifference.RationalUnitaryReachability

open WitnessedDifference.FiniteHermitianization
open WitnessedDifference.CertifiedPreservers

set_option maxHeartbeats 1200000
set_option linter.checkUnivs false
set_option linter.unusedSimpArgs false

universe u

def ginverse (z : GaussianRat) : GaussianRat := ⟨z.re / gnorm z, -z.im / gnorm z⟩
def gdivide (z w : GaussianRat) : GaussianRat := gmul z (ginverse w)

theorem gdivide_self (z : GaussianRat) (hz : z ≠ gzero) : gdivide z z = gone := by
  have hn : gnorm z ≠ 0 := fun h => hz ((gnorm_eq_zero_iff z).mp h)
  have hc := Rat.mul_inv_cancel (gnorm z) hn
  apply gaussian_ext <;>
    simp only [gdivide, ginverse, gmul, gone, Rat.div_def, gnorm] at * <;> grind

def rankOne {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (w : QVec ι) (β : GaussianRat) (x : QVec ι) : QVec ι :=
  vadd x (complexSmul C (gneg (gdivide (hermitian F w x) β)) w)

theorem rankOne_add {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (w : QVec ι) (β : GaussianRat) (x y : QVec ι) :
    rankOne F w β (vadd x y) = vadd (rankOne F w β x) (rankOne F w β y) := by
  unfold rankOne
  rw [hermitian_add_right]
  funext j
  simp only [complexSmul, gneg, gdivide, gmul, gadd, vadd, vsmul]
  grind

theorem rankOne_smul {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (w : QVec ι) (β z : GaussianRat) (x : QVec ι) :
    rankOne F w β (complexSmul C z x) = complexSmul C z (rankOne F w β x) := by
  unfold rankOne
  rw [hermitian_smul_right, complexSmul_add_vector, ← complexSmul_mul]
  have hc : gneg (gdivide (gmul z (hermitian F w x)) β) =
      gmul z (gneg (gdivide (hermitian F w x) β)) := by
    apply gaussian_ext <;> simp only [gneg, gdivide, gmul] <;> grind
  rw [hc]

theorem rankOne_preserves {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (w : QVec ι) (β : GaussianRat)
    (hβ : β ≠ gzero) (hw : hermitian F w w = gadd β (gconj β)) (x y : QVec ι) :
    hermitian F (rankOne F w β x) (rankOne F w β y) = hermitian F x y := by
  have hn : gnorm β ≠ 0 := fun h => hβ ((gnorm_eq_zero_iff β).mp h)
  have hc := Rat.mul_inv_cancel (gnorm β) hn
  simp only [rankOne, hermitian_add_left, hermitian_add_right,
    hermitian_smul_left, hermitian_smul_right]
  rw [hermitian_conjugate_symmetry F w x, hw]
  apply gaussian_ext <;>
    simp only [gadd, gneg, gdivide, ginverse, gconj, gmul, gnorm, Rat.div_def] at * <;> grind

theorem rankOne_inverse {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (w : QVec ι) (β : GaussianRat)
    (hβ : β ≠ gzero) (hw : hermitian F w w = gadd β (gconj β)) (x : QVec ι) :
    rankOne F w (gconj β) (rankOne F w β x) = x := by
  have hn : gnorm β ≠ 0 := fun h => hβ ((gnorm_eq_zero_iff β).mp h)
  have hc := Rat.mul_inv_cancel (gnorm β) hn
  simp only [rankOne, hermitian_add_right, hermitian_smul_right, hw]
  funext j
  simp only [complexSmul, vadd, vsmul, gadd, gneg, gdivide, ginverse, gconj,
    gmul, gnorm, Rat.div_def] at *
  grind

structure Unitary {ι : Type u} (C : ComplexStructure ι) (F : CompatibleForm C) where
  toFun : QVec ι → QVec ι
  inverse : QVec ι → QVec ι
  additive : ∀ x y, toFun (vadd x y) = vadd (toFun x) (toFun y)
  homogeneous : ∀ z x, toFun (complexSmul C z x) = complexSmul C z (toFun x)
  preserves : ∀ x y, hermitian F (toFun x) (toFun y) = hermitian F x y
  left_inverse : ∀ x, inverse (toFun x) = x
  right_inverse : ∀ x, toFun (inverse x) = x

def rankOneUnitary {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (w : QVec ι) (β : GaussianRat)
    (hβ : β ≠ gzero) (hw : hermitian F w w = gadd β (gconj β)) : Unitary C F where
  toFun := rankOne F w β
  inverse := rankOne F w (gconj β)
  additive := rankOne_add F w β
  homogeneous := rankOne_smul F w β
  preserves := rankOne_preserves F w β hβ hw
  left_inverse := rankOne_inverse F w β hβ hw
  right_inverse := by
    have hbc : gconj β ≠ gzero := by
      intro hz
      have hre := congrArg GaussianRat.re hz
      have him := congrArg GaussianRat.im hz
      apply hβ
      apply gaussian_ext <;> simp only [gzero, gconj] at * <;> grind
    have hwc : hermitian F w w = gadd (gconj β) (gconj (gconj β)) := by
      rw [hw, gconj_involutive]
      apply gaussian_ext <;> simp only [gadd, gconj] <;> grind
    intro x
    have hi := rankOne_inverse F w (gconj β) hbc hwc x
    simpa only [gconj_involutive] using hi

theorem equal_norm_unitary {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (hpos : PositiveDefinite F)
    (f v : QVec ι) (heq : F.form f f = F.form v v) :
    ∃ U : Unitary C F, U.toFun f = v := by
  by_cases hfv : f = v
  · exact ⟨⟨id, id, fun _ _ => rfl, fun _ _ => rfl, fun _ _ => rfl,
             fun _ => rfl, fun _ => rfl⟩, hfv⟩
  · let w := vadd f (vneg v)
    let β := hermitian F w f
    have hwn : w ≠ vzero := by
      intro hz
      apply hfv
      funext j
      have hj := congrFun hz j
      simp only [w, vadd, vneg, vzero] at hj
      grind
    have hww : F.form w w = 2*β.re := by
      have hsym := F.symmetric f v
      simp only [w, β, hermitian, F.add_left, form_add_right, form_neg_left, form_neg_right]
      grind
    have hβ : β ≠ gzero := by
      have hp := form_positive F hpos w hwn
      intro hz
      have hre := congrArg GaussianRat.re hz
      simp only [gzero] at hre
      rw [hre] at hww
      grind
    have hw : hermitian F w w = gadd β (gconj β) := by
      rw [hermitian_self]
      apply gaussian_ext <;> simp only [gadd, gconj] <;> grind
    refine ⟨rankOneUnitary F w β hβ hw, ?_⟩
    change rankOne F w β f = v
    unfold rankOne
    change vadd f (complexSmul C (gneg (gdivide β β)) w) = v
    rw [gdivide_self β hβ]
    funext j
    simp only [complexSmul, gone, gneg, vadd, vsmul, w, vneg]
    grind

def RayReachable {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (f g : QVec ι) : Prop :=
  ∃ U : Unitary C F, ∃ a : GaussianRat, a ≠ gzero ∧ U.toFun f = complexSmul C a g

theorem ray_reachable_iff_gaussian_norm {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (hpos : PositiveDefinite F)
    (f g : QVec ι) (hf : f ≠ vzero) (hg : g ≠ vzero) :
    RayReachable F f g ↔ ∃ a : GaussianRat, gnorm a = F.form f f / F.form g g := by
  have hfp := form_positive F hpos f hf
  have hgp := form_positive F hpos g hg
  have hgn : F.form g g ≠ 0 := by grind
  constructor
  · rintro ⟨U, a, _, ha⟩
    have hu := congrArg GaussianRat.re (U.preserves f f)
    simp only [hermitian] at hu
    rw [ha, form_smul_self] at hu
    refine ⟨a, ?_⟩
    have hc := Rat.div_mul_cancel (a := F.form f f) hgn
    grind
  · rintro ⟨a, ha⟩
    have hc := Rat.div_mul_cancel (a := F.form f f) hgn
    have hn : a ≠ gzero := by
      intro hz
      rw [hz] at ha
      simp only [gnorm, gzero] at ha
      grind
    have heq : F.form f f = F.form (complexSmul C a g) (complexSmul C a g) := by
      rw [form_smul_self, ha]
      exact hc.symm
    rcases equal_norm_unitary F hpos f (complexSmul C a g) heq with ⟨U, hU⟩
    exact ⟨U, a, hn, hU⟩

/-- Elementary primality, stated here without a Mathlib dependency. -/
def IsPrime (p : Nat) : Prop :=
  2 ≤ p ∧ ∀ d : Nat, d ∣ p → d = 1 ∨ d = p

/-- The displayed exponent is the exact, even multiplicity of `p` in `n`. -/
def EvenPrimeValuation (p n : Nat) : Prop :=
  ∃ k : Nat, p ^ (2*k) ∣ n ∧ ¬ p ^ (2*k+1) ∣ n

/-- Reduced positive rationals have even numerator and denominator valuations
at every prime congruent to three modulo four. Negative valuations are retained
through the denominator, rather than silently discarded. -/
def RationalNormParity (r : Rat) : Prop :=
  ∀ p : Nat, IsPrime p → p % 4 = 3 →
    EvenPrimeValuation p r.num.natAbs ∧ EvenPrimeValuation p r.den

theorem gaussian_norm_iff_two_rational_squares (r : Rat) :
    (∃ a : GaussianRat, gnorm a = r) ↔
      ∃ x y : Rat, x*x + y*y = r := by
  constructor
  · rintro ⟨a, ha⟩
    exact ⟨a.re, a.im, ha⟩
  · rintro ⟨x, y, h⟩
    exact ⟨⟨x, y⟩, h⟩

/-- P03 with the imported arithmetic theorem stated at its actual prime scope. -/
theorem gaussian_norm_iff_prime_parity
    (twoSquares : ∀ r : Rat, 0 < r →
      ((∃ x y : Rat, x*x + y*y = r) ↔ RationalNormParity r))
    (r : Rat) (hr : 0 < r) :
    (∃ a : GaussianRat, gnorm a = r) ↔ RationalNormParity r := by
  rw [gaussian_norm_iff_two_rational_squares, twoSquares r hr]

/-- Only the explicitly stated number-theoretic theorem is imported as a premise. -/
theorem reachability_from_two_squares {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (hpos : PositiveDefinite F)
    (twoSquares : ∀ r : Rat, 0 < r →
      ((∃ x y : Rat, x*x + y*y = r) ↔ RationalNormParity r))
    (f g : QVec ι) (hf : f ≠ vzero) (hg : g ≠ vzero) :
    RayReachable F f g ↔ RationalNormParity (F.form f f / F.form g g) := by
  rw [ray_reachable_iff_gaussian_norm F hpos f g hf hg]
  apply gaussian_norm_iff_prime_parity twoSquares
  have hfp := form_positive F hpos f hf
  have hgp := form_positive F hpos g hg
  have hp := Rat.inv_pos.mpr hgp
  exact Rat.mul_pos hfp hp

end WitnessedDifference.RationalUnitaryReachability

#print axioms WitnessedDifference.RationalUnitaryReachability.rankOne_preserves
#print axioms WitnessedDifference.RationalUnitaryReachability.rankOne_inverse
#print axioms WitnessedDifference.RationalUnitaryReachability.equal_norm_unitary
#print axioms WitnessedDifference.RationalUnitaryReachability.ray_reachable_iff_gaussian_norm
#print axioms WitnessedDifference.RationalUnitaryReachability.gaussian_norm_iff_prime_parity
#print axioms WitnessedDifference.RationalUnitaryReachability.reachability_from_two_squares
