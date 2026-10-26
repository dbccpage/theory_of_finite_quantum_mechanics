import WitnessedDifference.RationalUnitaryReachability

/-!
# The coordinate-frame part of projective uniqueness

The global classification first reduces two representatives to a semilinear
map fixing every ray. These lemmas check the concrete frame steps of that
reduction: basis and sum rays force one common scalar; mixed rays force the
field branch to be identity. They do not postulate the existence of a
semilinear representative for an arbitrary orthogonality-preserving bijection.
-/

namespace WitnessedDifference.ProjectiveFrameRigidity

open WitnessedDifference.FiniteHermitianization
open WitnessedDifference.CertifiedPreservers
open WitnessedDifference.RationalUnitaryReachability

set_option linter.unusedSimpArgs false
set_option maxHeartbeats 800000

universe u

abbrev KVec (ι : Type u) := ι → GaussianRat
def kadd {ι : Type u} (x y : KVec ι) : KVec ι := fun j => gadd (x j) (y j)
def ksmul {ι : Type u} (a : GaussianRat) (x : KVec ι) : KVec ι := fun j => gmul a (x j)
def basis {ι : Type u} [DecidableEq ι] (j : ι) : KVec ι :=
  fun k => if k = j then gone else gzero

theorem add_zero (a : GaussianRat) : gadd a gzero = a := by
  apply gaussian_ext <;> simp only [gadd, gzero] <;> grind

theorem zero_add (a : GaussianRat) : gadd gzero a = a := by
  apply gaussian_ext <;> simp only [gadd, gzero] <;> grind

theorem mul_zero (a : GaussianRat) : gmul a gzero = gzero := by
  apply gaussian_ext <;> simp only [gmul, gzero] <;> grind

theorem inverse_mul (a : GaussianRat) (ha : a ≠ gzero) :
    gmul (ginverse a) a = gone := by
  have hn : gnorm a ≠ 0 := fun h => ha ((gnorm_eq_zero_iff a).mp h)
  have hc := Rat.div_mul_cancel (a := a.re) hn
  have hd := Rat.div_mul_cancel (a := -a.im) hn
  apply gaussian_ext <;> simp only [ginverse, gmul, gone]
  all_goals simp only [gnorm] at *; grind

theorem mul_left_cancel (a x y : GaussianRat) (ha : a ≠ gzero)
    (h : gmul a x = gmul a y) : x = y := by
  have he := congrArg (gmul (ginverse a)) h
  rw [← gmul_assoc, ← gmul_assoc, inverse_mul a ha, gone_mul, gone_mul] at he
  exact he

theorem two_basis_coefficients {ι : Type u} [DecidableEq ι]
    (b j : ι) (h : b ≠ j) (a c t : GaussianRat)
    (he : kadd (ksmul a (basis b)) (ksmul c (basis j)) =
      ksmul t (kadd (basis b) (basis j))) : a = t ∧ c = t := by
  have hb := congrFun he b
  have hj := congrFun he j
  simp [kadd, ksmul, basis, h, Ne.symm h,
    gmul_one, mul_zero, add_zero, zero_add] at hb hj
  exact ⟨hb, hj⟩

theorem frame_scalars_equal {ι : Type u} [DecidableEq ι]
    (b : ι) (columns : ι → KVec ι) (a : ι → GaussianRat)
    (hbasis : ∀ j, columns j = ksmul (a j) (basis j))
    (hsums : ∀ j, j ≠ b → ∃ t,
      kadd (columns b) (columns j) = ksmul t (kadd (basis b) (basis j))) :
    ∀ j, a j = a b := by
  intro j
  by_cases h : j = b
  · rw [h]
  · obtain ⟨t, ht⟩ := hsums j h
    rw [hbasis b, hbasis j] at ht
    obtain ⟨hb, hj⟩ := two_basis_coefficients b j (Ne.symm h) (a b) (a j) t ht
    exact hj.trans hb.symm

theorem mixed_ray_branch_rigidity {ι : Type u} [DecidableEq ι]
    (b j : ι) (h : b ≠ j) (a : GaussianRat) (ha : a ≠ gzero)
    (φ : RationalScalarHom)
    (hmixed : ∀ t : GaussianRat, ∃ c : GaussianRat,
      kadd (ksmul a (basis b)) (ksmul (gmul a (φ.toFun t)) (basis j)) =
        ksmul c (kadd (basis b) (ksmul t (basis j)))) :
    ∀ t, φ.toFun t = t := by
  intro t
  obtain ⟨c, hc⟩ := hmixed t
  have hb := congrFun hc b
  have hj := congrFun hc j
  simp [kadd, ksmul, basis, h, Ne.symm h,
    gmul_one, mul_zero, add_zero, zero_add] at hb hj
  rw [← hb] at hj
  exact mul_left_cancel a (φ.toFun t) t ha hj

end WitnessedDifference.ProjectiveFrameRigidity

#print axioms WitnessedDifference.ProjectiveFrameRigidity.two_basis_coefficients
#print axioms WitnessedDifference.ProjectiveFrameRigidity.frame_scalars_equal
#print axioms WitnessedDifference.ProjectiveFrameRigidity.mixed_ray_branch_rigidity
