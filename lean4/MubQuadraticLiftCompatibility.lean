import MubQuadraticLift

/-!
# Compatibility identities among all three transition matrices

AuthorityEffect: None. These are consequences of the full quartet equations,
not sufficient conditions for a quartet or a nonexistence result.
-/

noncomputable section
namespace MUB.QuadraticLiftCompatibility
open QuadraticLift BoundedBlockChart BoundedQuartetEquations MonomialTransport
open scoped BigOperators

theorem raw_column_gram (A : Mat6) (h : RawHadamard A) :
    A.conjTranspose * A = (6 : ℂ) • (1 : Mat6) := by
  simpa [I6, Fintype.card_sum] using h.2

theorem raw_row_gram (A : Mat6) (h : RawHadamard A) :
    A * A.conjTranspose = (6 : ℂ) • (1 : Mat6) :=
  six_mul_comm _ _ (raw_column_gram A h)

theorem overlap_compose (A B C : Mat6) (hB : RawHadamard B) :
    (A.conjTranspose * B) * (B.conjTranspose * C) =
      (6 : ℂ) • (A.conjTranspose * C) := by
  rw [Matrix.mul_assoc, ← Matrix.mul_assoc B B.conjTranspose C,
    raw_row_gram B hB, Matrix.smul_mul, Matrix.one_mul, Matrix.mul_smul]

theorem overlap_column_gram (A B : Mat6) (hA : RawHadamard A) (hB : RawHadamard B) :
    (A.conjTranspose * B).conjTranspose * (A.conjTranspose * B) =
      (36 : ℂ) • (1 : Mat6) := by
  rw [Matrix.conjTranspose_mul, Matrix.conjTranspose_conjTranspose,
    overlap_compose B A B hA, raw_column_gram B hB, smul_smul]
  norm_num

theorem overlap_row_gram (A B : Mat6) (hA : RawHadamard A) (hB : RawHadamard B) :
    (A.conjTranspose * B) * (A.conjTranspose * B).conjTranspose =
      (36 : ℂ) • (1 : Mat6) := by
  have h := overlap_column_gram B A hB hA
  simpa only [Matrix.conjTranspose_mul, Matrix.conjTranspose_conjTranspose] using h

theorem firstRow_row_sum (A : Mat6) (hA : RawHadamard A) (hf : FirstRow A) (i : I6) :
    ∑ j, A i j = if i = Sum.inl 0 then 6 else 0 := by
  change ∀ j, A (Sum.inl 0) j = 1 at hf
  have h := congrFun (congrFun (raw_row_gram A hA) i) (Sum.inl 0)
  simpa [Matrix.mul_apply, Matrix.conjTranspose_apply, hf, Matrix.one_apply] using h

theorem overlap_row_sum (A B : Mat6) (hB : RawHadamard B)
    (hAfirst : FirstRow A) (hBfirst : FirstRow B) (i : I6) :
    ∑ j, (A.conjTranspose * B) i j = 6 := by
  change ∀ j, A (Sum.inl 0) j = 1 at hAfirst
  simp only [Matrix.mul_apply, Matrix.conjTranspose_apply]
  rw [Finset.sum_comm]
  simp_rw [← Finset.mul_sum, firstRow_row_sum B hB hBfirst]
  simp [hAfirst]

theorem overlap_column_sum (A B : Mat6) (hA : RawHadamard A)
    (hAfirst : FirstRow A) (hBfirst : FirstRow B) (j : I6) :
    ∑ i, (A.conjTranspose * B) i j = 6 := by
  have h := overlap_row_sum B A hA hBfirst hAfirst j
  have heq : A.conjTranspose * B = (B.conjTranspose * A).conjTranspose := by
    simp only [Matrix.conjTranspose_mul, Matrix.conjTranspose_conjTranspose]
  rw [heq]
  simp only [Matrix.conjTranspose_apply, ← star_sum, h]
  norm_num

theorem H_firstRow (r : Coord → ℝ) : FirstRow (H r) := by
  intro j
  cases j <;> rfl

theorem U_firstRow (r : Coord → ℝ) : FirstRow (U r) := by
  exact (BoundedCoordinates.decode_gauges (base r)).2.2.2.2.1

theorem V_firstRow (r : Coord → ℝ) : FirstRow (V r) := by
  exact (BoundedCoordinates.decode_gauges (base r)).2.2.2.2.2

theorem transition_column_gram {r : Coord → ℝ} (h : System r) (a : Fin 3) :
    (W r a).conjTranspose * W r a = (36 : ℂ) • (1 : Mat6) := by
  rw [h.graph]
  fin_cases a
  · exact overlap_column_gram _ _ h.rawH h.rawU
  · exact overlap_column_gram _ _ h.rawH h.rawV
  · exact overlap_column_gram _ _ h.rawU h.rawV

theorem transition_row_gram {r : Coord → ℝ} (h : System r) (a : Fin 3) :
    W r a * (W r a).conjTranspose = (36 : ℂ) • (1 : Mat6) := by
  rw [h.graph]
  fin_cases a
  · exact overlap_row_gram _ _ h.rawH h.rawU
  · exact overlap_row_gram _ _ h.rawH h.rawV
  · exact overlap_row_gram _ _ h.rawU h.rawV

theorem cycle_02 {r : Coord → ℝ} (h : System r) :
    W r 0 * W r 2 = (6 : ℂ) • W r 1 := by
  rw [h.graph]
  exact overlap_compose _ _ _ h.rawU

theorem cycle_01 {r : Coord → ℝ} (h : System r) :
    (W r 0).conjTranspose * W r 1 = (6 : ℂ) • W r 2 := by
  rw [h.graph]
  change ((H r).conjTranspose * U r).conjTranspose * ((H r).conjTranspose * V r) = _
  rw [Matrix.conjTranspose_mul, Matrix.conjTranspose_conjTranspose]
  exact overlap_compose _ _ _ h.rawH

theorem cycle_12 {r : Coord → ℝ} (h : System r) :
    W r 1 * (W r 2).conjTranspose = (6 : ℂ) • W r 0 := by
  rw [h.graph]
  change ((H r).conjTranspose * V r) * ((U r).conjTranspose * V r).conjTranspose = _
  rw [Matrix.conjTranspose_mul, Matrix.conjTranspose_conjTranspose]
  exact overlap_compose _ _ _ h.rawV

theorem transition_row_sum {r : Coord → ℝ} (h : System r) (a : Fin 3) (i : I6) :
    ∑ j, W r a i j = 6 := by
  rw [h.graph]
  fin_cases a
  · exact overlap_row_sum _ _ h.rawU (H_firstRow r) (U_firstRow r) i
  · exact overlap_row_sum _ _ h.rawV (H_firstRow r) (V_firstRow r) i
  · exact overlap_row_sum _ _ h.rawV (U_firstRow r) (V_firstRow r) i

theorem transition_column_sum {r : Coord → ℝ} (h : System r) (a : Fin 3) (j : I6) :
    ∑ i, W r a i j = 6 := by
  rw [h.graph]
  fin_cases a
  · exact overlap_column_sum _ _ h.rawH (H_firstRow r) (U_firstRow r) j
  · exact overlap_column_sum _ _ h.rawH (H_firstRow r) (V_firstRow r) j
  · exact overlap_column_sum _ _ h.rawU (U_firstRow r) (V_firstRow r) j

#print axioms raw_column_gram
#print axioms raw_row_gram
#print axioms overlap_compose
#print axioms overlap_column_gram
#print axioms overlap_row_gram
#print axioms firstRow_row_sum
#print axioms overlap_row_sum
#print axioms overlap_column_sum
#print axioms H_firstRow
#print axioms U_firstRow
#print axioms V_firstRow
#print axioms transition_column_gram
#print axioms transition_row_gram
#print axioms cycle_02
#print axioms cycle_01
#print axioms cycle_12
#print axioms transition_row_sum
#print axioms transition_column_sum
end MUB.QuadraticLiftCompatibility
