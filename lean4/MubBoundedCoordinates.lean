import MubBoundedQuartetEquations

/-!
# Real coordinates for the bounded quartet equations

AuthorityEffect: None.

The 152 coordinates are an ambient parameter count, not a dimension claim.
The codec retains all five matrices and all the quartet equations.
-/

noncomputable section
namespace MUB.BoundedCoordinates
open BoundedBlockChart BoundedQuartetEquations MonomialTransport

abbrev Slot := (Fin 2 × Fin 2) ⊕ (Fin 2 × Fin 3) ⊕
  (Fin 3 × Fin 2) ⊕ (Fin 5 × I6) ⊕ (Fin 5 × I6)
abbrev Coord := Slot × Bool

theorem coordinate_count : Fintype.card Coord = 152 := by
  norm_num [Coord, Slot, I6, Fintype.card_sum, Fintype.card_prod]

def fillE {R : Type*} [One R] (f : Fin 2 × Fin 2 → R) : Matrix I3 I3 R :=
  Fin.cases (fun _ => 1) (fun i => Fin.cases 1 (fun j => f (i, j)))

def fillB {R : Type*} [One R] (f : Fin 2 × Fin 3 → R) : Matrix I3 I3 R :=
  Fin.cases (fun _ => 1) (fun i j => f (i, j))

def fillC {R : Type*} [One R] (f : Fin 3 × Fin 2 → R) : Matrix I3 I3 R :=
  fun i => Fin.cases 1 (fun j => f (i, j))

def fillBasis {R : Type*} [One R] (f : Fin 5 × I6 → R) : Matrix I6 I6 R :=
  fun i => Fin.cases (fun _ => 1) (fun k j => f (k, j)) (blockIndex i)

def complexAt (r : Coord → ℝ) (s : Slot) : ℂ := ⟨r (s, false), r (s, true)⟩
def decodeE (r : Coord → ℝ) : Mat3 := fillE (fun s => complexAt r (.inl s))
def decodeB (r : Coord → ℝ) : Mat3 := fillB (fun s => complexAt r (.inr (.inl s)))
def decodeC (r : Coord → ℝ) : Mat3 := fillC (fun s => complexAt r (.inr (.inr (.inl s))))
def decodeU (r : Coord → ℝ) : Mat6 :=
  fillBasis (fun s => complexAt r (.inr (.inr (.inr (.inl s)))))
def decodeV (r : Coord → ℝ) : Mat6 :=
  fillBasis (fun s => complexAt r (.inr (.inr (.inr (.inr s)))))

def entry (E B C : Mat3) (U V : Mat6) : Slot → ℂ
  | .inl (i, j) => E i.succ j.succ
  | .inr (.inl (i, j)) => B i.succ j
  | .inr (.inr (.inl (i, j))) => C i j.succ
  | .inr (.inr (.inr (.inl (i, j)))) => U (blockIndex.symm i.succ) j
  | .inr (.inr (.inr (.inr (i, j)))) => V (blockIndex.symm i.succ) j

def encode (E B C : Mat3) (U V : Mat6) (c : Coord) : ℝ :=
  if c.2 then (entry E B C U V c.1).im else (entry E B C U V c.1).re

theorem complexAt_encode (E B C : Mat3) (U V : Mat6) (s : Slot) :
    complexAt (encode E B C U V) s = entry E B C U V s := by
  rfl

theorem decodeE_encode (E B C : Mat3) (U V : Mat6)
    (hr : ∀ j, E 0 j = 1) (hc : ∀ i, E i 0 = 1) :
    decodeE (encode E B C U V) = E := by
  ext i j
  refine Fin.cases ?_ (fun k => ?_) i
  · simp [decodeE, fillE, hr]
  · refine Fin.cases ?_ (fun l => ?_) j
    · simp [decodeE, fillE, hc]
    · simp [decodeE, fillE, complexAt_encode, entry]

theorem decodeB_encode (E B C : Mat3) (U V : Mat6) (hr : ∀ j, B 0 j = 1) :
    decodeB (encode E B C U V) = B := by
  ext i j
  refine Fin.cases ?_ (fun k => ?_) i <;>
    simp [decodeB, fillB, complexAt_encode, entry, hr]

theorem decodeC_encode (E B C : Mat3) (U V : Mat6) (hc : ∀ i, C i 0 = 1) :
    decodeC (encode E B C U V) = C := by
  ext i j
  refine Fin.cases ?_ (fun k => ?_) j <;>
    simp [decodeC, fillC, complexAt_encode, entry, hc]

theorem decodeU_encode (E B C : Mat3) (U V : Mat6) (hr : FirstRow U) :
    decodeU (encode E B C U V) = U := by
  ext i j
  obtain ⟨k, rfl⟩ := blockIndex.symm.surjective i
  refine Fin.cases ?_ (fun l => ?_) k
  · exact (hr j).symm
  · simp [decodeU, fillBasis, complexAt_encode, entry]

theorem decodeV_encode (E B C : Mat3) (U V : Mat6) (hr : FirstRow V) :
    decodeV (encode E B C U V) = V := by
  ext i j
  obtain ⟨k, rfl⟩ := blockIndex.symm.surjective i
  refine Fin.cases ?_ (fun l => ?_) k
  · exact (hr j).symm
  · simp [decodeV, fillBasis, complexAt_encode, entry]

theorem encode_decode (r : Coord → ℝ) :
    encode (decodeE r) (decodeB r) (decodeC r) (decodeU r) (decodeV r) = r := by
  funext ⟨s, b⟩
  rcases s with s | s | s | s | s <;> cases b <;>
    simp [encode, entry, decodeE, decodeB, decodeC, decodeU, decodeV,
      fillE, fillB, fillC, fillBasis, complexAt]

theorem decode_gauges (r : Coord → ℝ) :
    (∀ j, decodeE r 0 j = 1) ∧ (∀ i, decodeE r i 0 = 1) ∧
    (∀ j, decodeB r 0 j = 1) ∧ (∀ i, decodeC r i 0 = 1) ∧
    FirstRow (decodeU r) ∧ FirstRow (decodeV r) := by
  refine ⟨fun _ => rfl, ?_, fun _ => rfl, fun _ => rfl, fun _ => rfl, fun _ => rfl⟩
  intro i
  refine Fin.cases ?_ (fun k => ?_) i <;> rfl

def System (r : Coord → ℝ) : Prop :=
  QuartetEquations (decodeE r) (decodeB r) (decodeC r) (decodeU r) (decodeV r)

def InBox (r : Coord → ℝ) : Prop := ∀ c, -1 ≤ r c ∧ r c ≤ 1

theorem encode_system (E B C : Mat3) (U V : Mat6) (h : QuartetEquations E B C U V) :
    System (encode E B C U V) := by
  unfold System
  rw [decodeE_encode E B C U V h.rowE h.columnE, decodeB_encode E B C U V h.rowB,
    decodeC_encode E B C U V h.columnC, decodeU_encode E B C U V h.rowU,
    decodeV_encode E B C U V h.rowV]
  exact h

theorem encode_inBox (E B C : Mat3) (U V : Mat6) (h : QuartetEquations E B C U V) :
    InBox (encode E B C U V) := by
  have he : ∀ s, Complex.normSq (entry E B C U V s) = 1 := by
    rintro (⟨i, j⟩ | ⟨i, j⟩ | ⟨i, j⟩ | ⟨i, j⟩ | ⟨i, j⟩)
    · exact h.unitE _ _
    · exact h.unitB _ _
    · exact h.unitC _ _
    · exact h.rawU.1 _ _
    · exact h.rawV.1 _ _
  rintro ⟨s, b⟩
  have hb := real_bounds_of_unit _ (he s)
  cases b
  · exact ⟨hb.1, hb.2.1⟩
  · exact ⟨hb.2.2.1, hb.2.2.2⟩

theorem system_inBox (r : Coord → ℝ) (h : System r) : InBox r := by
  simpa only [encode_decode] using encode_inBox _ _ _ _ _ h

theorem exists_quartet_iff_coordinates :
    (∃ Q : Fin 4 → Mat (Fin 6), SzollosiQuartetSystem.Quartet Q) ↔
      ∃ r : Coord → ℝ, System r ∧ InBox r := by
  rw [exists_quartet_iff_equations]
  constructor
  · rintro ⟨E, B, C, U, V, h⟩
    exact ⟨encode E B C U V, encode_system E B C U V h, encode_inBox E B C U V h⟩
  · rintro ⟨r, h, _⟩
    exact ⟨decodeE r, decodeB r, decodeC r, decodeU r, decodeV r, h⟩

theorem no_quartet_iff_no_coordinates :
    (∀ Q : Fin 4 → Mat (Fin 6), ¬ SzollosiQuartetSystem.Quartet Q) ↔
      ∀ r : Coord → ℝ, InBox r → ¬ System r := by
  constructor
  · intro hn r hb hs
    obtain ⟨Q, hQ⟩ := exists_quartet_iff_coordinates.mpr ⟨r, hs, hb⟩
    exact hn Q hQ
  · intro hn Q hQ
    obtain ⟨r, hs, hb⟩ := exists_quartet_iff_coordinates.mp ⟨Q, hQ⟩
    exact hn r hb hs

#print axioms coordinate_count
#print axioms decodeE_encode
#print axioms decodeB_encode
#print axioms decodeC_encode
#print axioms decodeU_encode
#print axioms decodeV_encode
#print axioms encode_decode
#print axioms decode_gauges
#print axioms encode_system
#print axioms encode_inBox
#print axioms system_inBox
#print axioms exists_quartet_iff_coordinates
#print axioms no_quartet_iff_no_coordinates
end MUB.BoundedCoordinates
