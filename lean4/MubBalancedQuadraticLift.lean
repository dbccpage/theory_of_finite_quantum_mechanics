import MubBalancedCompletion
import MubQuadraticLiftNarrowBox

/-!
# A 320-coordinate quartet model using balanced transition completions

AuthorityEffect: None. The 66 removed real coordinates are recovered by
affine formulas. All original full-matrix equations are retained after expansion.
-/

noncomputable section
namespace MUB.BalancedQuadraticLift
open BoundedBlockChart QuadraticLiftCompatibility QuadraticLiftNarrowBox

abbrev Slot := BoundedCoordinates.Slot ⊕ (I3 × I3) ⊕ (Fin 3 × Fin 5 × Fin 5)
abbrev Coord := Slot × Bool

theorem coordinate_count : Fintype.card Coord = 320 := by
  norm_num [Coord, Slot, BoundedCoordinates.Slot, I3, I6, Fintype.card_sum, Fintype.card_prod]

def core (r : Coord → ℝ) (a : Fin 3) : Matrix (Fin 5) (Fin 5) ℂ :=
  fun i j => ⟨r (.inr (.inr (a,i,j)),false), r (.inr (.inr (a,i,j)),true)⟩

def expand (r : Coord → ℝ) : QuadraticLift.Coord → ℝ
  | (.inl s,b) => r (.inl s,b)
  | (.inr (.inl (i,j)),b) => r (.inr (.inl (i,j)),b)
  | (.inr (.inr (a,i,j)),b) =>
      let z := BalancedCompletion.complete (core r a) (blockIndex i) (blockIndex j)
      if b then z.im else z.re

def compress (r : QuadraticLift.Coord → ℝ) : Coord → ℝ
  | (.inl s,b) => r (.inl s,b)
  | (.inr (.inl (i,j)),b) => r (.inr (.inl (i,j)),b)
  | (.inr (.inr (a,i,j)),b) =>
      r (.inr (.inr (a,blockIndex.symm i.castSucc,blockIndex.symm j.castSucc)),b)

def indexedW (r : QuadraticLift.Coord → ℝ) (a : Fin 3) : Matrix (Fin 6) (Fin 6) ℂ :=
  fun i j => QuadraticLift.W r a (blockIndex.symm i) (blockIndex.symm j)

theorem core_compress (r : QuadraticLift.Coord → ℝ) (a : Fin 3) :
    core (compress r) a = BalancedCompletion.restrict (indexedW r a) := rfl

theorem W_expand (r : Coord → ℝ) (a : Fin 3) (i j : I6) :
    QuadraticLift.W (expand r) a i j =
      BalancedCompletion.complete (core r a) (blockIndex i) (blockIndex j) := rfl

theorem compress_expand (r : Coord → ℝ) : compress (expand r) = r := by
  funext ⟨s,b⟩
  rcases s with s | ⟨i,j⟩ | ⟨a,i,j⟩
  · rfl
  · rfl
  · cases b <;> simp only [compress, expand, Equiv.apply_symm_apply, BalancedCompletion.complete_core]
    <;> rfl

theorem complete_compress_W {r : QuadraticLift.Coord → ℝ} (h : QuadraticLift.System r) (a : Fin 3) :
    BalancedCompletion.complete (core (compress r) a) = indexedW r a := by
  rw [core_compress]
  apply BalancedCompletion.complete_restrict
  · intro i
    exact (Equiv.sum_comp blockIndex.symm (fun j => QuadraticLift.W r a (blockIndex.symm i) j)).trans
      (transition_row_sum h a (blockIndex.symm i))
  · intro j
    exact (Equiv.sum_comp blockIndex.symm (fun i => QuadraticLift.W r a i (blockIndex.symm j))).trans
      (transition_column_sum h a (blockIndex.symm j))

theorem expand_compress {r : QuadraticLift.Coord → ℝ} (h : QuadraticLift.System r) :
    expand (compress r) = r := by
  funext ⟨s,b⟩
  rcases s with s | ⟨i,j⟩ | ⟨a,i,j⟩
  · rfl
  · rfl
  · cases b <;> simp only [expand, complete_compress_W h, indexedW, Equiv.symm_apply_apply]
    <;> rfl

def radius : Slot → ℝ
  | .inl _ => 1
  | .inr (.inl _) => 1
  | .inr (.inr _) => transitionRadius

def InBox (r : Coord → ℝ) : Prop := ∀ c, -radius c.1 ≤ r c ∧ r c ≤ radius c.1
def System (r : Coord → ℝ) : Prop := QuadraticLift.System (expand r)

theorem compress_inBox {r : QuadraticLift.Coord → ℝ} (hb : NarrowBox r) : InBox (compress r) := by
  rintro ⟨s,b⟩
  rcases s with s | ⟨i,j⟩ | ⟨a,i,j⟩
  · exact hb (.inl s,b)
  · exact hb (.inr (.inl (i,j)),b)
  · exact hb (.inr (.inr (a,blockIndex.symm i.castSucc,blockIndex.symm j.castSucc)),b)

theorem expand_inBox {r : Coord → ℝ} (h : System r) (hb : InBox r) : NarrowBox (expand r) := by
  rintro ⟨s,b⟩
  rcases s with s | ⟨i,j⟩ | ⟨a,i,j⟩
  · exact hb (.inl s,b)
  · exact hb (.inr (.inl (i,j)),b)
  · have hn := components_of_norm_six _ (h.overlapNorm a i j)
    cases b
    · exact ⟨hn.1,hn.2.1⟩
    · exact hn.2.2

theorem exists_quartet_iff_balanced_lift :
    (∃ Q, SzollosiQuartetSystem.Quartet Q) ↔ ∃ r, System r ∧ InBox r := by
  constructor
  · intro hQ
    obtain ⟨r,hr,hb⟩ := QuadraticLift.exists_quartet_iff_lift.mp hQ
    refine ⟨compress r, ?_, compress_inBox (system_narrowBox hr hb)⟩
    unfold System
    rw [expand_compress hr]
    exact hr
  · rintro ⟨r,hr,_⟩
    exact hr.exists_quartet

theorem zero_inBox : InBox (fun _ => 0) := by
  rintro ⟨s,b⟩
  rcases s with s | ⟨i,j⟩ | ⟨a,i,j⟩
  · norm_num [radius]
  · norm_num [radius]
  · exact ⟨neg_nonpos.mpr transitionRadius_bounds.1,transitionRadius_bounds.1⟩

theorem expand_zero_corner (a : Fin 3) :
    QuadraticLift.W (expand (fun _ => 0)) a
      (blockIndex.symm (Fin.last 5)) (blockIndex.symm (Fin.last 5)) = -24 := by
  simp only [W_expand, Equiv.apply_symm_apply, BalancedCompletion.complete_corner]
  norm_num [core]
  rfl

theorem zero_expansion_not_narrowBox : ¬ NarrowBox (expand (fun _ => 0)) := by
  intro h
  have hb := h (.inr (.inr (0,blockIndex.symm (Fin.last 5),blockIndex.symm (Fin.last 5))),false)
  have he := congrArg Complex.re (expand_zero_corner 0)
  change expand (fun _ => 0)
    (.inr (.inr (0,blockIndex.symm (Fin.last 5),blockIndex.symm (Fin.last 5))),false) = -24 at he
  rw [he] at hb
  norm_num [narrowRadius,transitionRadius] at hb

theorem zero_not_system : ¬ System (fun _ => 0) :=
  fun h => zero_expansion_not_narrowBox (expand_inBox h zero_inBox)

#print axioms coordinate_count
#print axioms core_compress
#print axioms W_expand
#print axioms compress_expand
#print axioms complete_compress_W
#print axioms expand_compress
#print axioms compress_inBox
#print axioms expand_inBox
#print axioms exists_quartet_iff_balanced_lift
#print axioms zero_inBox
#print axioms expand_zero_corner
#print axioms zero_expansion_not_narrowBox
#print axioms zero_not_system
end MUB.BalancedQuadraticLift
