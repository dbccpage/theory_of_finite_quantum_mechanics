import HilbertMubStructure
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.LinearAlgebra.Matrix.Trace

/-!
# Concrete projectors of a finite complex MUB family

AuthorityEffect: None.

This forward construction uses the existing coordinate-vector family, with
basis labels equal to coordinate labels. It derives self-adjointness,
same-basis multiplication, completeness, trace one, rank one, and the MU
cross-trace equation for actual complex matrices. It does not construct a
family in dimension six, a moment functional, or a flat GNS extraction.
-/

namespace MUB.FiniteComplexMubFamily
open scoped BigOperators Matrix

variable {ι B : Type*} [Fintype ι] [DecidableEq ι] [Fintype B] [DecidableEq B]

noncomputable def concreteProjector (family : FiniteComplexMubFamily ι B ι)
    (b : B) (l : ι) : Matrix ι ι ℂ :=
  Matrix.vecMulVec (family.vector b l) (star (family.vector b l))

theorem concreteProjector_self_adjoint (family : FiniteComplexMubFamily ι B ι)
    (b : B) (l : ι) : (family.concreteProjector b l).conjTranspose = family.concreteProjector b l := by
  simp [concreteProjector]

theorem concreteProjector_same_basis_mul (family : FiniteComplexMubFamily ι B ι)
    (b : B) (l k : ι) :
    family.concreteProjector b l * family.concreteProjector b k =
      if l = k then family.concreteProjector b l else 0 := by
  unfold concreteProjector
  rw [Matrix.vecMulVec_mul_vecMulVec]
  have h := family.same_basis_inner b l k
  change (star (family.vector b l)) ⬝ᵥ family.vector b k = _ at h
  rw [h]
  split_ifs with hlk
  · subst k
    simp
  · simp

theorem concreteProjector_complete (family : FiniteComplexMubFamily ι B ι)
    (b : B) : ∑ l, family.concreteProjector b l = 1 := by
  let U : Matrix ι ι ℂ := fun i l => family.vector b l i
  have hU : U.conjTranspose * U = 1 := by
    ext i j
    change finiteHilbertInner (family.vector b i) (family.vector b j) = _
    simpa only [Matrix.one_apply] using family.same_basis_inner b i j
  have hUU : U * U.conjTranspose = 1 := mul_eq_one_comm.mp hU
  rw [← hUU]
  ext i j
  simp only [Matrix.sum_apply, concreteProjector, Matrix.vecMulVec_apply,
    Matrix.mul_apply, Matrix.conjTranspose_apply]
  rfl

theorem concreteProjector_trace_one (family : FiniteComplexMubFamily ι B ι)
    (b : B) (l : ι) : Matrix.trace (family.concreteProjector b l) = 1 := by
  have h := family.same_basis_inner b l l
  simp only [ite_true] at h
  rw [concreteProjector, Matrix.trace_vecMulVec]
  simpa [finiteHilbertInner, dotProduct, mul_comm] using h

theorem concreteProjector_rank_le_one (family : FiniteComplexMubFamily ι B ι)
    (b : B) (l : ι) : (family.concreteProjector b l).rank ≤ 1 := by
  exact Matrix.rank_vecMulVec_le _ _

theorem concreteProjector_rank_one (family : FiniteComplexMubFamily ι B ι)
    (b : B) (l : ι) : (family.concreteProjector b l).rank = 1 := by
  have hn : (star (family.vector b l)) ⬝ᵥ family.vector b l = 1 := by
    simpa [finiteHilbertInner, dotProduct] using family.same_basis_inner b l l
  have hfix : (family.concreteProjector b l) *ᵥ family.vector b l = family.vector b l := by
    rw [concreteProjector, Matrix.vecMulVec_mulVec, hn]
    simp
  have hne : family.vector b l ≠ 0 := by
    intro h
    simp [h] at hn
  have hp : 0 < (family.concreteProjector b l).rank := by
    change 0 < Module.finrank ℂ (LinearMap.range (family.concreteProjector b l).mulVecLin)
    apply Module.finrank_pos_iff_exists_ne_zero.mpr
    refine ⟨⟨family.vector b l, ⟨family.vector b l, hfix⟩⟩, ?_⟩
    intro h
    exact hne (congrArg Subtype.val h)
  exact le_antisymm (family.concreteProjector_rank_le_one b l) (Nat.succ_le_of_lt hp)

theorem concreteProjector_cross_basis_trace (family : FiniteComplexMubFamily ι B ι)
    {b c : B} (hbc : b ≠ c) (l k : ι) :
    Matrix.trace (family.concreteProjector b l * family.concreteProjector c k) =
      (Fintype.card ι : ℂ)⁻¹ := by
  have ht : Matrix.trace (family.concreteProjector b l * family.concreteProjector c k) =
      finiteHilbertInner (family.vector b l) (family.vector c k) *
        star (finiteHilbertInner (family.vector b l) (family.vector c k)) := by
    rw [concreteProjector, concreteProjector, Matrix.vecMulVec_mul_vecMulVec,
      Matrix.trace_vecMulVec]
    simp only [dotProduct, Pi.smul_apply, smul_eq_mul, finiteHilbertInner,
      star_sum, Pi.star_apply, star_mul, star_star]
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i hi
    ring
  rw [ht]
  exact family.cross_basis_unbiased hbc l k

end MUB.FiniteComplexMubFamily

#print axioms MUB.FiniteComplexMubFamily.concreteProjector_self_adjoint
#print axioms MUB.FiniteComplexMubFamily.concreteProjector_same_basis_mul
#print axioms MUB.FiniteComplexMubFamily.concreteProjector_complete
#print axioms MUB.FiniteComplexMubFamily.concreteProjector_trace_one
#print axioms MUB.FiniteComplexMubFamily.concreteProjector_rank_le_one

#print axioms MUB.FiniteComplexMubFamily.concreteProjector_rank_one

#print axioms MUB.FiniteComplexMubFamily.concreteProjector_cross_basis_trace
