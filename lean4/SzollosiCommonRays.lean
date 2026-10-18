import MubMonomialTransport
import Mathlib.Tactic.NormNum

/-!
# Common rays and concrete quartet completion

AuthorityEffect: None.

Raw vectors have unit-modulus entries and first coordinate one. Their
normalization is by sqrt(6). The predicates use the existing concrete
RawHadamard, RawMU and HasRawQuartet definitions. No finiteness assumption
on the common-ray set is needed for the equivalence or pair obstruction.
-/

noncomputable section
namespace MUB.SzollosiCommonRays
open MonomialTransport
open scoped BigOperators

abbrev Vec := Fin 6 → ℂ
abbrev SixMatrix := Mat (Fin 6)

def overlap (z w : Vec) : ℂ := ∑ i, star (z i) * w i
def column (U : SixMatrix) (j : Fin 6) : Vec := fun i => U i j

def CommonRay (H : SixMatrix) (z : Vec) : Prop :=
  z 0 = 1 ∧ (∀ i, Complex.normSq (z i) = 1) ∧
    ∀ k, Complex.normSq (overlap (column H k) z) = 6

def RayBasis (H U : SixMatrix) : Prop :=
  RawHadamard U ∧ ∀ j, CommonRay H (column U j)

def rephase (U : SixMatrix) : SixMatrix :=
  action U (Equiv.refl _) (Equiv.refl _) (fun _ => 1) (fun j => star (U 0 j))

theorem overlap_columns (U V : SixMatrix) (i j : Fin 6) :
    overlap (column U i) (column V j) = (U.conjTranspose * V) i j := by
  rfl

theorem rephase_phase_unit (U : SixMatrix) (hU : RawHadamard U) :
    ∀ j, Complex.normSq (star (U 0 j)) = 1 := by
  intro j
  simpa [Complex.star_def, Complex.normSq_conj] using hU.1 0 j

theorem rephase_first_row (U : SixMatrix) (hU : RawHadamard U) (j : Fin 6) :
    rephase U 0 j = 1 := by
  have h := congrArg (fun t : ℝ => (t : ℂ)) (hU.1 0 j)
  simpa [rephase, action, Complex.star_def, Complex.normSq_eq_conj_mul_self,
    mul_comm] using h

theorem rephase_hadamard (U : SixMatrix) (hU : RawHadamard U) :
    RawHadamard (rephase U) := by
  exact action_hadamard U _ _ _ _ (by intro i; simp)
    (rephase_phase_unit U hU) hU

theorem rephase_mu_right (H U : SixMatrix) (hU : RawHadamard U)
    (hHU : RawMU H U) : RawMU H (rephase U) := by
  have h := action_mu H U (Equiv.refl _) (Equiv.refl _) (Equiv.refl _)
    (fun _ => 1) (fun _ => 1) (fun j => star (U 0 j))
    (by intro i; simp) (by intro i; simp) (rephase_phase_unit U hU) hHU
  have hid : action H (Equiv.refl _) (Equiv.refl _)
      (fun _ => 1) (fun _ => 1) = H := by
    ext i j
    simp [action]
  rw [hid] at h
  exact h

theorem rephase_mu_both (U V : SixMatrix) (hU : RawHadamard U)
    (hV : RawHadamard V) (hUV : RawMU U V) :
    RawMU (rephase U) (rephase V) := by
  exact action_mu U V (Equiv.refl _) (Equiv.refl _) (Equiv.refl _)
    (fun _ => 1) (fun j => star (U 0 j)) (fun j => star (V 0 j))
    (by intro i; simp) (rephase_phase_unit U hU) (rephase_phase_unit V hV) hUV

theorem rephase_rayBasis (H U : SixMatrix) (hU : RawHadamard U)
    (hHU : RawMU H U) : RayBasis H (rephase U) := by
  refine ⟨rephase_hadamard U hU, ?_⟩
  intro j
  refine ⟨rephase_first_row U hU j, ?_, ?_⟩
  · intro i
    exact (rephase_hadamard U hU).1 i j
  · intro k
    rw [overlap_columns]
    simpa using rephase_mu_right H U hU hHU k j

theorem rayBasis_mu (H U : SixMatrix) (h : RayBasis H U) : RawMU H U := by
  intro i j
  simpa [overlap_columns] using (h.2 j).2.2 i

/-- Two common-ray bases with all cross overlaps unbiased are exactly a completion. -/
theorem quartet_iff_ray_bases (H : SixMatrix) (hH : RawHadamard H) :
    HasRawQuartet H ↔
      ∃ U V, RayBasis H U ∧ RayBasis H V ∧ RawMU U V := by
  constructor
  · rintro ⟨_, U, V, hU, hV, hHU, hHV, hUV⟩
    exact ⟨rephase U, rephase V, rephase_rayBasis H U hU hHU,
      rephase_rayBasis H V hV hHV, rephase_mu_both U V hU hV hUV⟩
  · rintro ⟨U, V, hU, hV, hUV⟩
    exact ⟨hH, U, V, hU.1, hV.1, rayBasis_mu H U hU,
      rayBasis_mu H V hV, hUV⟩

/-- The stronger pair obstruction works even for an infinite common-ray set. -/
theorem no_quartet_of_no_unbiased_ray_pair (H : SixMatrix)
    (hpair : ∀ z w, CommonRay H z → CommonRay H w →
      Complex.normSq (overlap z w) ≠ 6) : ¬ HasRawQuartet H := by
  intro hq
  obtain ⟨U, V, hU, hV, hUV⟩ := (quartet_iff_ray_bases H hq.1).mp hq
  apply hpair (column U 0) (column V 0) (hU.2 0) (hV.2 0)
  rw [overlap_columns]
  simpa using hUV 0 0

#print axioms quartet_iff_ray_bases
#print axioms no_quartet_of_no_unbiased_ray_pair

end MUB.SzollosiCommonRays
