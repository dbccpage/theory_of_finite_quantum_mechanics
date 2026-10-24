/-
Exact algebraic model; AuthorityEffect: None.
Five-integer face-vector translations preserve the displayed linear functionals; solving two rational linear equations characterizes invariant count weights. In Lean no simplicial complex, move admissibility, topology, or flat-connection extension count is constructed. The independent checker performs additional finite simplex-set examples, not a general refinement proof. normalizedFlatGaugeSum declares inverse-G cancellation for delta 0 and 1 and returns zero otherwise; it proves no gauge-bundle counting theorem. The Regge shift and WDW mass are supplied scalar formulas, not geometric action differences or constraint solutions. The stated face-count trajectories and arithmetic remain exact.
Historical names are labels; their physical or operational interpretations require separate evidence.
-/

import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Rat.Defs
import Mathlib.Tactic



open scoped BigOperators Matrix

namespace CampaignFspPachnerInvarianceClaim


structure FaceVector4D where
  n0 : ℤ
  n1 : ℤ
  n2 : ℤ
  n3 : ℤ
  n4 : ℤ
  deriving DecidableEq, Repr


def eulerChar4D (f : FaceVector4D) : ℤ :=
  f.n0 - f.n1 + f.n2 - f.n3 + f.n4


def pachner1to5 (f : FaceVector4D) : FaceVector4D :=
  ⟨f.n0 + 1, f.n1 + 5, f.n2 + 10, f.n3 + 10, f.n4 + 4⟩


def pachner5to1 (f : FaceVector4D) : FaceVector4D :=
  ⟨f.n0 - 1, f.n1 - 5, f.n2 - 10, f.n3 - 10, f.n4 - 4⟩


def pachner2to4 (f : FaceVector4D) : FaceVector4D :=
  ⟨f.n0, f.n1 + 1, f.n2 + 4, f.n3 + 5, f.n4 + 2⟩


def pachner4to2 (f : FaceVector4D) : FaceVector4D :=
  ⟨f.n0, f.n1 - 1, f.n2 - 4, f.n3 - 5, f.n4 - 2⟩


def pachner3to3 (f : FaceVector4D) : FaceVector4D :=
  f


theorem pachner_moves_preserve_euler_characteristic (f : FaceVector4D) :
    eulerChar4D (pachner1to5 f) = eulerChar4D f ∧
    eulerChar4D (pachner5to1 f) = eulerChar4D f ∧
    eulerChar4D (pachner2to4 f) = eulerChar4D f ∧
    eulerChar4D (pachner4to2 f) = eulerChar4D f ∧
    eulerChar4D (pachner3to3 f) = eulerChar4D f ∧
    pachner5to1 (pachner1to5 f) = f ∧
    pachner4to2 (pachner2to4 f) = f := by
  rcases f with ⟨n0, n1, n2, n3, n4⟩
  refine ⟨?_, ?_, ?_, ?_, rfl, ?_, ?_⟩
  · unfold eulerChar4D pachner1to5; ring
  · unfold eulerChar4D pachner5to1; ring
  · unfold eulerChar4D pachner2to4; ring
  · unfold eulerChar4D pachner4to2; ring
  · unfold pachner5to1 pachner1to5; congr 1 <;> ring
  · unfold pachner4to2 pachner2to4; congr 1 <;> ring


def s4SeedFaceVector : FaceVector4D :=
  ⟨6, 15, 20, 15, 6⟩


theorem s4_seed_surgical_sequence_face_vectors_and_chi :
    let f1 := pachner1to5 s4SeedFaceVector
    let f2 := pachner2to4 f1
    let f3 := pachner3to3 f2
    eulerChar4D s4SeedFaceVector = 2 ∧
    f1 = ⟨7, 20, 30, 25, 10⟩ ∧
    eulerChar4D f1 = 2 ∧
    f2 = ⟨7, 21, 34, 30, 12⟩ ∧
    eulerChar4D f2 = 2 ∧
    f3 = ⟨7, 21, 34, 30, 12⟩ ∧
    eulerChar4D f3 = 2 := by
  decide


def dehnSommervilleDefect (f : FaceVector4D) : ℤ :=
  2 * f.n3 - 5 * f.n4


theorem dehn_sommerville_codim1_invariant_under_pachner_moves (f : FaceVector4D) :
    dehnSommervilleDefect (pachner1to5 f) = dehnSommervilleDefect f ∧
    dehnSommervilleDefect (pachner2to4 f) = dehnSommervilleDefect f ∧
    dehnSommervilleDefect (pachner3to3 f) = dehnSommervilleDefect f ∧
    dehnSommervilleDefect s4SeedFaceVector = 0 := by
  refine ⟨?_, ?_, rfl, by decide⟩
  · unfold dehnSommervilleDefect pachner1to5; ring
  · unfold dehnSommervilleDefect pachner2to4; ring


def linearStateSumExponent (w : Fin 5 → ℚ) (f : FaceVector4D) : ℚ :=
  w 0 * (f.n0 : ℚ) + w 1 * (f.n1 : ℚ) + w 2 * (f.n2 : ℚ) +
    w 3 * (f.n3 : ℚ) + w 4 * (f.n4 : ℚ)


theorem linear_topological_state_sum_pachner_invariance_iff
    (w : Fin 5 → ℚ) (f : FaceVector4D) :
    ((linearStateSumExponent w (pachner1to5 f) = linearStateSumExponent w f ∧
      linearStateSumExponent w (pachner2to4 f) = linearStateSumExponent w f) ↔
      (w 0 = 10 * w 2 + 15 * w 3 + 6 * w 4 ∧
       w 1 = -4 * w 2 - 5 * w 3 - 2 * w 4)) ∧
    linearStateSumExponent ![1, -1, 1, -1, 1] (pachner1to5 f) =
      linearStateSumExponent ![1, -1, 1, -1, 1] f ∧
    linearStateSumExponent ![0, 0, 0, 2, -5] (pachner2to4 f) =
      linearStateSumExponent ![0, 0, 0, 2, -5] f := by
  refine ⟨?_, ?_, ?_⟩
  · unfold linearStateSumExponent pachner1to5 pachner2to4
    push_cast
    constructor
    · rintro ⟨h15, h24⟩
      constructor <;> linarith
    · rintro ⟨hw0, hw1⟩
      constructor <;> linarith
  · unfold linearStateSumExponent pachner1to5
    simp [Matrix.cons_val_zero, Matrix.cons_val_one]
    ring
  · unfold linearStateSumExponent pachner2to4
    simp [Matrix.cons_val_zero, Matrix.cons_val_one]
    ring


def normalizedFlatGaugeSum (groupOrder invNorm0 flatCount : ℚ) (deltaN0 : ℕ) : ℚ :=
  match deltaN0 with
  | 0 => invNorm0 * flatCount
  | 1 => (groupOrder⁻¹ * invNorm0) * (groupOrder * flatCount)
  | _ => 0


theorem z2_gauge_state_sum_vertex_normalization_invariance
    (G invNorm0 flatCount : ℚ) (hG : G ≠ 0) :
    normalizedFlatGaugeSum G invNorm0 flatCount 1 =
      normalizedFlatGaugeSum G invNorm0 flatCount 0 ∧
    normalizedFlatGaugeSum 2 (1 / 64) 32 1 = 1 / 2 ∧
    normalizedFlatGaugeSum 2 (1 / 64) 32 0 = 1 / 2 := by
  refine ⟨?_, ?_, ?_⟩
  · unfold normalizedFlatGaugeSum
    calc
      G⁻¹ * invNorm0 * (G * flatCount) = (G⁻¹ * G) * (invNorm0 * flatCount) := by ring
      _ = 1 * (invNorm0 * flatCount) := by rw [inv_mul_cancel₀ hG]
      _ = invNorm0 * flatCount := by ring
  · unfold normalizedFlatGaugeSum
    norm_num
  · unfold normalizedFlatGaugeSum
    norm_num


def pachnerReggeActionShift (m : ℕ) (areaInt epsInt : ℚ) : ℚ :=
  (m : ℚ) * areaInt * epsInt


theorem regge_action_non_invariant_under_curved_pachner_subdivision
    (areaInt epsInt : ℚ) (hA : 0 < areaInt) (hE : epsInt ≠ 0) :
    pachnerReggeActionShift 10 areaInt 0 = 0 ∧
    pachnerReggeActionShift 4 areaInt 0 = 0 ∧
    pachnerReggeActionShift 10 areaInt epsInt ≠ 0 ∧
    pachnerReggeActionShift 4 areaInt epsInt ≠ 0 := by
  have hA_ne : areaInt ≠ 0 := ne_of_gt hA
  refine ⟨by unfold pachnerReggeActionShift; ring,
          by unfold pachnerReggeActionShift; ring, ?_, ?_⟩
  · unfold pachnerReggeActionShift
    exact mul_ne_zero (mul_ne_zero (by norm_num) hA_ne) hE
  · unfold pachnerReggeActionShift
    exact mul_ne_zero (mul_ne_zero (by norm_num) hA_ne) hE


def curvedWdwDefectMass (f : FaceVector4D) : ℚ :=
  3 * (f.n1 : ℚ)


theorem curved_wdw_defect_mass_shifts_under_pachner_moves :
    let f0 := s4SeedFaceVector
    let f1 := pachner1to5 f0
    let f2 := pachner2to4 f1
    let f3 := pachner3to3 f2
    curvedWdwDefectMass f0 = 45 ∧
    curvedWdwDefectMass f1 = 60 ∧
    curvedWdwDefectMass f2 = 63 ∧
    curvedWdwDefectMass f3 = 63 ∧
    curvedWdwDefectMass f0 < curvedWdwDefectMass f1 ∧
    curvedWdwDefectMass f1 < curvedWdwDefectMass f2 := by
  dsimp only
  unfold curvedWdwDefectMass s4SeedFaceVector pachner1to5 pachner2to4 pachner3to3
  norm_num


theorem signed_hinge_deficits_can_cancel_under_pachner_move_fence :
    let deficits : Fin 4 → ℚ := ![1, -1, 1, -1]
    0 < deficits 0 ∧
    (∑ i : Fin 4, deficits i) = 0 := by
  dsimp only
  refine ⟨by norm_num, ?_⟩
  simp [Fin.sum_univ_four]


theorem unnormalized_simplex_weight_fails_pachner_invariance_fence
    (w4 : ℚ) (hw4 : w4 ≠ 0) (f : FaceVector4D) :
    linearStateSumExponent ![0, 0, 0, 0, w4] (pachner1to5 f) -
      linearStateSumExponent ![0, 0, 0, 0, w4] f = 4 * w4 ∧
    linearStateSumExponent ![0, 0, 0, 0, w4] (pachner2to4 f) -
      linearStateSumExponent ![0, 0, 0, 0, w4] f = 2 * w4 ∧
    4 * w4 ≠ 0 ∧
    2 * w4 ≠ 0 := by
  refine ⟨?_, ?_, mul_ne_zero (by norm_num) hw4, mul_ne_zero (by norm_num) hw4⟩
  · unfold linearStateSumExponent pachner1to5
    simp [Matrix.cons_val_zero, Matrix.cons_val_one]
    ring
  · unfold linearStateSumExponent pachner2to4
    simp [Matrix.cons_val_zero, Matrix.cons_val_one]
    ring


theorem pachner_moves_independent_of_fermion_sign_fence (f : FaceVector4D) :
    (1 : ℤ) * eulerChar4D (pachner1to5 f) + (-1 : ℤ) * eulerChar4D (pachner1to5 f) = 0 ∧
    (1 : ℤ) * eulerChar4D (pachner2to4 f) + (-1 : ℤ) * eulerChar4D (pachner2to4 f) = 0 := by
  refine ⟨by ring, by ring⟩

#print axioms pachner_moves_preserve_euler_characteristic
#print axioms s4_seed_surgical_sequence_face_vectors_and_chi
#print axioms dehn_sommerville_codim1_invariant_under_pachner_moves
#print axioms linear_topological_state_sum_pachner_invariance_iff
#print axioms z2_gauge_state_sum_vertex_normalization_invariance
#print axioms regge_action_non_invariant_under_curved_pachner_subdivision
#print axioms curved_wdw_defect_mass_shifts_under_pachner_moves
#print axioms signed_hinge_deficits_can_cancel_under_pachner_move_fence
#print axioms unnormalized_simplex_weight_fails_pachner_invariance_fence
#print axioms pachner_moves_independent_of_fermion_sign_fence

end CampaignFspPachnerInvarianceClaim
