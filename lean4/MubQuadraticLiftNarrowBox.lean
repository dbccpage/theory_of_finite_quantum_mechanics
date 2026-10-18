import MubQuadraticLiftTable

/-!
# A smaller rational box for the quadratic quartet table

AuthorityEffect: None. The bound agrees with the first native square-isolation
sweep. This theorem checks the bound directly from the matrix equations; it
does not verify the native parser or its general contractor implementation.
-/

noncomputable section
namespace MUB.QuadraticLiftNarrowBox
open QuadraticLift QuadraticLiftIndices QuadraticLiftCodedSystem QuadraticLiftPolynomials
open BoundedBlockChart
open BoundedExportIndices (bit index6)

def transitionRadius : ℚ := 10035 / 4096

theorem transitionRadius_bounds :
    0 ≤ (transitionRadius : ℝ) ∧ (transitionRadius : ℝ) < 3 ∧
      6 ≤ (transitionRadius : ℝ) ^ 2 := by
  norm_num [transitionRadius]

theorem components_of_norm_six (z : ℂ) (hz : Complex.normSq z = 6) :
    -(transitionRadius : ℝ) ≤ z.re ∧ z.re ≤ transitionRadius ∧
      -(transitionRadius : ℝ) ≤ z.im ∧ z.im ≤ transitionRadius := by
  have hs : z.re ^ 2 + z.im ^ 2 = 6 := by
    simpa [Complex.normSq_apply, pow_two] using hz
  have hr : z.re ^ 2 ≤ (transitionRadius : ℝ) ^ 2 := by
    nlinarith [sq_nonneg z.im, transitionRadius_bounds.2.2]
  have hi : z.im ^ 2 ≤ (transitionRadius : ℝ) ^ 2 := by
    nlinarith [sq_nonneg z.re, transitionRadius_bounds.2.2]
  have hbr := (sq_le_sq.mp hr)
  have hbi := (sq_le_sq.mp hi)
  rw [abs_of_nonneg transitionRadius_bounds.1] at hbr hbi
  exact ⟨(abs_le.mp hbr).1, (abs_le.mp hbr).2, abs_le.mp hbi⟩

def narrowRadius : LiftSlot → ℝ
  | .inl _ => 1
  | .inr (.inl _) => 1
  | .inr (.inr _) => transitionRadius

def NarrowBox (r : Coord → ℝ) : Prop :=
  ∀ c, -narrowRadius c.1 ≤ r c ∧ r c ≤ narrowRadius c.1

theorem system_narrowBox {r : Coord → ℝ} (h : System r) (hb : InBox r) : NarrowBox r := by
  rintro ⟨s,b⟩
  rcases s with s | ⟨i,j⟩ | ⟨a,i,j⟩
  · exact hb (.inl s,b)
  · exact hb (.inr (.inl (i,j)),b)
  · have hn := components_of_norm_six (W r a i j) (h.overlapNorm a i j)
    cases b
    · exact ⟨hn.1, hn.2.1⟩
    · exact hn.2.2

def narrowCodeRadius (i : Nat) : ℚ := if i < 170 then 1 else transitionRadius

theorem narrow_radius_code (c : Coord) :
    (narrowCodeRadius (variableCode c) : ℝ) = narrowRadius c.1 := by
  rcases c with ⟨s,b⟩
  rcases s with s | ⟨i,j⟩ | ⟨a,i,j⟩
  · have h := BoundedExportIndices.variableCode_lt (s,b)
    have h' : variableCode (.inl s,b) < 170 := by
      change BoundedExportIndices.variableCode (s,b) < 170
      omega
    rw [narrowCodeRadius, if_pos h']
    norm_num [narrowRadius]
  · have hi := i.isLt
    have hj := j.isLt
    cases b <;> simp [variableCode, narrowCodeRadius, narrowRadius, bit,
      show 152 + 2 * (3 * i.val + j.val) < 170 by omega,
      show 152 + 2 * (3 * i.val + j.val) + 1 < 170 by omega]
  · have hn : ¬ 170 + 2 * (36 * a.val + 6 * index6 i + index6 j) + bit b < 170 := by omega
    simp [variableCode, narrowCodeRadius, narrowRadius, hn]

def NarrowCodedBox (x : Fin 386 → ℝ) : Prop :=
  ∀ i, -(narrowCodeRadius i.val : ℝ) ≤ x i ∧ x i ≤ (narrowCodeRadius i.val : ℝ)

theorem narrowCodedBox_iff (x : Fin 386 → ℝ) : NarrowCodedBox x ↔ NarrowBox (pull x) := by
  constructor
  · intro h c
    simpa only [pull, variableFin, narrow_radius_code] using h (variableFin c)
  · intro h i
    obtain ⟨c,hc⟩ := variableFin_bijective.2 i
    rw [← hc]
    simpa only [pull, variableFin, narrow_radius_code] using h c

theorem narrowCodedBox_subset {x : Fin 386 → ℝ} (h : NarrowCodedBox x) : CodedBox x := by
  intro i
  have hr : (narrowCodeRadius i.val : ℝ) ≤ (codeRadius i.val : ℝ) := by
    by_cases hi : i.val < 170
    · simp [narrowCodeRadius, codeRadius, hi]
    · simpa [narrowCodeRadius, codeRadius, hi] using le_of_lt transitionRadius_bounds.2.1
  exact ⟨le_trans (neg_le_neg hr) (h i).1, le_trans (h i).2 hr⟩

theorem exists_quartet_iff_narrow_table :
    (∃ Q, SzollosiQuartetSystem.Quartet Q) ↔
      ∃ x, QuadraticLiftTable.TableSolution x ∧ NarrowCodedBox x := by
  rw [QuadraticLiftTable.exists_quartet_iff_table]
  constructor
  · rintro ⟨x,hx,hb⟩
    have hs := (solution_iff_system (pull x)).mp
      ((codedSolution_iff x).mp ((QuadraticLiftTable.tableSolution_iff x).mp hx))
    exact ⟨x, hx, (narrowCodedBox_iff x).mpr (system_narrowBox hs ((codedBox_iff x).mp hb))⟩
  · rintro ⟨x,hx,hb⟩
    exact ⟨x,hx,narrowCodedBox_subset hb⟩

#print axioms transitionRadius_bounds
#print axioms components_of_norm_six
#print axioms system_narrowBox
#print axioms narrow_radius_code
#print axioms narrowCodedBox_iff
#print axioms narrowCodedBox_subset
#print axioms exists_quartet_iff_narrow_table
end MUB.QuadraticLiftNarrowBox
