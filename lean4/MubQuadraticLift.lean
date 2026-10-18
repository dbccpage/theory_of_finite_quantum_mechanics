import MubBoundedCoordinates

/-!
# Explicit block and transition coordinates for a quadratic quartet lift

AuthorityEffect: None.
The full matrix is checked directly; no determinant denominator is used.
-/

noncomputable section
namespace MUB.QuadraticLift
open BoundedBlockChart BoundedQuartetEquations MonomialTransport

abbrev LiftSlot := BoundedCoordinates.Slot ⊕ (I3 × I3) ⊕ (Fin 3 × I6 × I6)
abbrev Coord := LiftSlot × Bool

theorem coordinate_count : Fintype.card Coord = 386 := by
  norm_num [Coord, LiftSlot, BoundedCoordinates.Slot, I3, I6, Fintype.card_sum, Fintype.card_prod]

def base (r : Coord → ℝ) : BoundedCoordinates.Coord → ℝ := fun c => r (.inl c.1, c.2)
def complexAt (r : Coord → ℝ) (s : LiftSlot) : ℂ := ⟨r (s, false), r (s, true)⟩
def E (r : Coord → ℝ) : Mat3 := BoundedCoordinates.decodeE (base r)
def B (r : Coord → ℝ) : Mat3 := BoundedCoordinates.decodeB (base r)
def C (r : Coord → ℝ) : Mat3 := BoundedCoordinates.decodeC (base r)
def D (r : Coord → ℝ) : Mat3 := fun i j => complexAt r (.inr (.inl (i,j)))
def U (r : Coord → ℝ) : Mat6 := BoundedCoordinates.decodeU (base r)
def V (r : Coord → ℝ) : Mat6 := BoundedCoordinates.decodeV (base r)
def W (r : Coord → ℝ) : Fin 3 → Mat6 := fun a i j => complexAt r (.inr (.inr (a,i,j)))
def H (r : Coord → ℝ) : Mat6 := Matrix.fromBlocks (E r) (B r) (C r) (D r)

def transitions (H U V : Mat6) : Fin 3 → Mat6 :=
  ![H.conjTranspose * U, H.conjTranspose * V, U.conjTranspose * V]

def lift (r : BoundedCoordinates.Coord → ℝ) (d : Mat3) (w : Fin 3 → Mat6) : Coord → ℝ
  | (.inl s, b) => r (s,b)
  | (.inr (.inl (i,j)), b) => if b then (d i j).im else (d i j).re
  | (.inr (.inr (a,i,j)), b) => if b then (w a i j).im else (w a i j).re

@[simp] theorem base_lift (r : BoundedCoordinates.Coord → ℝ) (d : Mat3) (w : Fin 3 → Mat6) :
    base (lift r d w) = r := rfl
@[simp] theorem D_lift (r : BoundedCoordinates.Coord → ℝ) (d : Mat3) (w : Fin 3 → Mat6) :
    D (lift r d w) = d := rfl
@[simp] theorem W_lift (r : BoundedCoordinates.Coord → ℝ) (d : Mat3) (w : Fin 3 → Mat6) :
    W (lift r d w) = w := rfl

theorem lift_decode (r : Coord → ℝ) : lift (base r) (D r) (W r) = r := by
  funext ⟨s,b⟩
  rcases s with s | ⟨i,j⟩ | ⟨a,i,j⟩ <;> cases b <;> rfl

structure System (r : Coord → ℝ) : Prop where
  rawH : RawHadamard (H r)
  rawU : RawHadamard (U r)
  rawV : RawHadamard (V r)
  graph : W r = transitions (H r) (U r) (V r)
  overlapNorm : ∀ a i j, Complex.normSq (W r a i j) = 6

theorem System.rawQuartet {r : Coord → ℝ} (h : System r) : HasRawQuartet (H r) := by
  have hn (a : Fin 3) (i j : I6) :
      Complex.normSq (transitions (H r) (U r) (V r) a i j) = 6 := by
    rw [← h.graph]
    exact h.overlapNorm a i j
  refine ⟨h.rawH, U r, V r, h.rawU, h.rawV, ?_, ?_, ?_⟩
  · simpa [RawMU, transitions, Fintype.card_sum] using hn 0
  · simpa [RawMU, transitions, Fintype.card_sum] using hn 1
  · simpa [RawMU, transitions, Fintype.card_sum] using hn 2

theorem System.exists_quartet {r : Coord → ℝ} (h : System r) :
    ∃ Q, SzollosiQuartetSystem.Quartet Q := by
  apply exists_quartet_iff_exists_rawQuartet.mpr
  exact ⟨pullMatrix blockIndex.symm (H r),
    (hasRawQuartet_pull_iff blockIndex.symm (H r)).mpr h.rawQuartet⟩

def canonicalLift (r : BoundedCoordinates.Coord → ℝ) : Coord → ℝ :=
  let e := BoundedCoordinates.decodeE r
  let b := BoundedCoordinates.decodeB r
  let c := BoundedCoordinates.decodeC r
  lift r (forcedD e b c)
    (transitions (completion e b c) (BoundedCoordinates.decodeU r) (BoundedCoordinates.decodeV r))

theorem canonicalLift_system (r : BoundedCoordinates.Coord → ℝ) (h : BoundedCoordinates.System r) :
    System (canonicalLift r) := by
  have ha := (blockEquations_iff_admissible _ _ _).mp h.toBlockEquations
  refine ⟨ha.hadamard, h.rawU, h.rawV, rfl, ?_⟩
  intro a i j
  change Complex.normSq (transitions _ _ _ a i j) = 6
  fin_cases a
  · have hm := (scaled_mu_iff _ _ _ _ h.determinant_bound).mp h.scaledMU_U
    simpa [RawMU, transitions, Fintype.card_sum] using hm i j
  · have hm := (scaled_mu_iff _ _ _ _ h.determinant_bound).mp h.scaledMU_V
    simpa [RawMU, transitions, Fintype.card_sum] using hm i j
  · simpa [RawMU, transitions, Fintype.card_sum] using h.muUV i j

def radius : LiftSlot → ℝ
  | .inl _ => 1
  | .inr (.inl _) => 1
  | .inr (.inr _) => 3

def InBox (r : Coord → ℝ) : Prop := ∀ c, -radius c.1 ≤ r c ∧ r c ≤ radius c.1

theorem real_bounds_of_six (z : ℂ) (hz : Complex.normSq z = 6) :
    -3 ≤ z.re ∧ z.re ≤ 3 ∧ -3 ≤ z.im ∧ z.im ≤ 3 := by
  have hs : z.re ^ 2 + z.im ^ 2 = 6 := by simpa [Complex.normSq_apply, pow_two] using hz
  refine ⟨?_, ?_, ?_, ?_⟩ <;>
    nlinarith [sq_nonneg z.re, sq_nonneg z.im, sq_nonneg (z.re + 3),
      sq_nonneg (z.re - 3), sq_nonneg (z.im + 3), sq_nonneg (z.im - 3)]

theorem lift_inBox (r : BoundedCoordinates.Coord → ℝ) (d : Mat3) (w : Fin 3 → Mat6)
    (hr : BoundedCoordinates.InBox r) (hd : UnitEntries d)
    (hw : ∀ a i j, Complex.normSq (w a i j) = 6) : InBox (lift r d w) := by
  rintro ⟨s,b⟩
  rcases s with s | ⟨i,j⟩ | ⟨a,i,j⟩
  · exact hr (s,b)
  · have h := real_bounds_of_unit (d i j) (hd i j)
    cases b
    · exact ⟨h.1,h.2.1⟩
    · exact h.2.2
  · have h := real_bounds_of_six (w a i j) (hw a i j)
    cases b
    · exact ⟨h.1,h.2.1⟩
    · exact h.2.2

theorem canonicalLift_inBox (r : BoundedCoordinates.Coord → ℝ)
    (h : BoundedCoordinates.System r) (hb : BoundedCoordinates.InBox r) :
    InBox (canonicalLift r) := by
  have ha := (blockEquations_iff_admissible _ _ _).mp h.toBlockEquations
  exact lift_inBox r _ _ hb ha.unitD (canonicalLift_system r h).overlapNorm

theorem exists_quartet_iff_lift :
    (∃ Q, SzollosiQuartetSystem.Quartet Q) ↔ ∃ r, System r ∧ InBox r := by
  constructor
  · intro hQ
    obtain ⟨r,hr,hb⟩ := BoundedCoordinates.exists_quartet_iff_coordinates.mp hQ
    exact ⟨canonicalLift r, canonicalLift_system r hr, canonicalLift_inBox r hr hb⟩
  · rintro ⟨r,hr,_⟩
    exact hr.exists_quartet

#print axioms coordinate_count
#print axioms base_lift
#print axioms D_lift
#print axioms W_lift
#print axioms lift_decode
#print axioms System.rawQuartet
#print axioms System.exists_quartet
#print axioms canonicalLift_system
#print axioms real_bounds_of_six
#print axioms lift_inBox
#print axioms canonicalLift_inBox
#print axioms exists_quartet_iff_lift
end MUB.QuadraticLift
