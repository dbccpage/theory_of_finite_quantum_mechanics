/- Imported so that this repository carries its own Lean evidence.
   Original sha256: 9151218761964ffc6424be4d796d4addb62beb2698a64196bc3b6b99a6af3653 (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.PreGenesisToMssn.TriangleHomology
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.PreGenesisToMssn.GraphHomology

/-! Integral homology of the oriented triangle, before and after attaching its
face. The cycles and boundaries belong to actual chain complexes and the H1
objects are the kernel/image quotient groups constructed in Homology.lean. -/
namespace PreMssn.TriangleHomology
open Lean.Grind
open AddCommMonoid AddCommGroup
open Homology

structure Chain where
  x : Int
  y : Int
  z : Int
  deriving DecidableEq, Repr

theorem Chain.ext {a b : Chain} (hx : a.x = b.x) (hy : a.y = b.y)
    (hz : a.z = b.z) : a = b := by
  cases a; cases b; simp_all

instance chainGroup : AddCommGroup Chain where
  zero := ⟨0, 0, 0⟩
  add a b := ⟨a.x + b.x, a.y + b.y, a.z + b.z⟩
  neg a := ⟨-a.x, -a.y, -a.z⟩
  sub a b := ⟨a.x - b.x, a.y - b.y, a.z - b.z⟩
  add_zero _ := Chain.ext (Int.add_zero _) (Int.add_zero _) (Int.add_zero _)
  add_comm _ _ := Chain.ext (Int.add_comm _ _) (Int.add_comm _ _) (Int.add_comm _ _)
  add_assoc _ _ _ := Chain.ext (Int.add_assoc _ _ _) (Int.add_assoc _ _ _) (Int.add_assoc _ _ _)
  neg_add_cancel a := Chain.ext (neg_add_cancel a.x) (neg_add_cancel a.y) (neg_add_cancel a.z)
  sub_eq_add_neg _ _ := Chain.ext Int.sub_eq_add_neg Int.sub_eq_add_neg Int.sub_eq_add_neg

def diagonal (k : Int) : Chain := ⟨k, k, k⟩

def differential : AddHom Chain Chain where
  toFun a := ⟨a.z - a.x, a.x - a.y, a.y - a.z⟩
  map_zero := rfl
  map_add a b := by
    apply Chain.ext
    · change (a.z + b.z) - (a.x + b.x) = (a.z - a.x) + (b.z - b.x)
      omega
    · change (a.x + b.x) - (a.y + b.y) = (a.x - a.y) + (b.x - b.y)
      omega
    · change (a.y + b.y) - (a.z + b.z) = (a.y - a.z) + (b.y - b.z)
      omega

def faceBoundary : AddHom Int Chain where
  toFun := diagonal
  map_zero := rfl
  map_add _ _ := rfl

theorem paper_boundary_matches (a : Chain) :
    (differential a).x = (triangleBoundary a.x a.y a.z).1 ∧
    (differential a).y = (triangleBoundary a.x a.y a.z).2.1 ∧
    (differential a).z = (triangleBoundary a.x a.y a.z).2.2 := ⟨rfl, rfl, rfl⟩

theorem kernel_iff (a : Chain) : differential a = 0 ↔ a = diagonal a.x := by
  constructor
  · intro h
    have hy := congrArg Chain.y h
    have hz := congrArg Chain.z h
    change a.x - a.y = 0 at hy
    change a.y - a.z = 0 at hz
    exact Chain.ext rfl (by change a.y = a.x; omega) (by change a.z = a.x; omega)
  · intro h
    rw [h]
    apply Chain.ext <;> exact Int.sub_self _

theorem kernel_coordinates_iff (a : Chain) :
    differential a = 0 ↔ a.x = a.y ∧ a.y = a.z := by
  rw [kernel_iff]
  constructor
  · intro h
    have hx := congrArg Chain.y h
    have hz := congrArg Chain.z h
    change a.y = a.x at hx
    change a.z = a.x at hz
    exact ⟨hx.symm, hx.trans hz.symm⟩
  · rintro ⟨hxy, hyz⟩
    exact Chain.ext rfl hxy.symm (hxy.trans hyz).symm

/-- Every integral cycle is a unique integer multiple of the oriented cycle. -/
theorem kernel_unique_coordinate (a : Chain) :
    differential a = 0 ↔ ∃ k, a = diagonal k ∧ ∀ j, a = diagonal j → j = k := by
  constructor
  · intro h
    refine ⟨a.x, (kernel_iff a).mp h, ?_⟩
    intro j hj
    exact (congrArg Chain.x hj).symm
  · rintro ⟨k, hk, _⟩
    rw [hk]
    apply Chain.ext <;> exact Int.sub_self _

/-- There are no two-cells: the upper chain group is the zero group PUnit. -/
def unfilledComplex : Complex where
  upper := PUnit
  middle := Chain
  lower := Chain
  boundary := AddHom.zero _ _
  differential := differential
  square_zero _ := rfl

/-- One freely generated two-cell has boundary (1,1,1). -/
def filledComplex : Complex where
  upper := Int
  middle := Chain
  lower := Chain
  boundary := faceBoundary
  differential := differential
  square_zero k := by apply Chain.ext <;> exact Int.sub_self k

def unfilledCycle : AddHom Int (Cycle unfilledComplex) where
  toFun k := ⟨diagonal k, by apply Chain.ext <;> exact Int.sub_self k⟩
  map_zero := rfl
  map_add _ _ := rfl

def cycleCoordinate : AddHom (Cycle unfilledComplex) Int where
  toFun a := a.val.x
  map_zero := rfl
  map_add _ _ := rfl

def toInteger : AddHom (Homology unfilledComplex) Int :=
  quotientDescend (boundaryCycle unfilledComplex) cycleCoordinate (fun _ => rfl)

def fromInteger : AddHom Int (Homology unfilledComplex) :=
  (quotientProjection (boundaryCycle unfilledComplex)).comp unfilledCycle

/-- Actual unfilled triangle H1 is the infinite cyclic additive group. -/
def unfilledH1Iso : AddIso (Homology unfilledComplex) Int where
  forward := toInteger
  backward := fromInteger
  left_inverse q := by
    induction q using Quotient.inductionOn with
    | _ a =>
      apply congrArg (quotientProjection (boundaryCycle unfilledComplex))
      exact Subtype.ext ((kernel_iff a.val).mp a.property).symm
  right_inverse _ := rfl

def unfilledClass (k : Int) := fromInteger k

theorem unfilled_class_eq_iff (k j : Int) :
    unfilledClass k = unfilledClass j ↔ k = j := by
  constructor
  · exact fun h => congrArg toInteger h
  · exact congrArg unfilledClass

theorem unfilled_generator_nonzero : unfilledClass 1 ≠ 0 := by
  intro h
  have bad := congrArg toInteger h
  change (1 : Int) = 0 at bad
  exact (by decide : (1 : Int) ≠ 0) bad

/-- Every filled cycle is the boundary of its unique coordinate times the face. -/
theorem filled_cycle_is_boundary (a : Cycle filledComplex) :
    boundaryCycle filledComplex a.val.x = a :=
  Subtype.ext ((kernel_iff a.val).mp a.property).symm

theorem filled_h1_zero (q : Homology filledComplex) : q = 0 := by
  induction q using Quotient.inductionOn with
  | _ a =>
    exact (quotient_class_zero_iff (boundaryCycle filledComplex) a).mpr
      ⟨a.val.x, filled_cycle_is_boundary a⟩

def filledH1Iso : AddIso (Homology filledComplex) PUnit where
  forward := AddHom.zero _ _
  backward := AddHom.zero _ _
  left_inverse q := (filled_h1_zero q).symm
  right_inverse _ := rfl

def attachment : Morphism unfilledComplex filledComplex where
  upper := AddHom.zero _ _
  middle := AddHom.identity _
  lower := AddHom.identity _
  boundary_commutes _ := rfl
  differential_commutes _ := rfl

theorem attachment_kills_h1 (q : Homology unfilledComplex) :
    homologyMap attachment q = 0 := filled_h1_zero _

theorem attachment_has_no_chain_retraction :
    ¬∃ r : Morphism filledComplex unfilledComplex,
      ∀ a, r.middle (attachment.middle a) = a := by
  rintro ⟨r, fixes⟩
  apply unfilled_generator_nonzero
  apply induced_homology_injective attachment r fixes
  rw [attachment_kills_h1, (homologyMap attachment).map_zero]

/-- Exact cycle coordinate for the bounded replay; noncycles are refused. -/
def classify (filled : Bool) (a : Chain) : Option Int :=
  if a.x == a.y && a.y == a.z then some (if filled then 0 else a.x) else none

theorem classify_unfilled (a : Chain) (h : differential a = 0) :
    classify false a = some (toInteger (quotientProjection (boundaryCycle unfilledComplex)
      ⟨a, h⟩)) := by
  change classify false a = some a.x
  have ha := (kernel_iff a).mp h
  rw [ha]
  simp [classify, diagonal]

theorem classify_filled (a : Chain) (h : differential a = 0) :
    classify true a = some 0 := by
  rw [(kernel_iff a).mp h]
  simp [classify, diagonal]

theorem classify_refuses_iff (filled : Bool) (a : Chain) :
    classify filled a = none ↔ differential a ≠ 0 := by
  simp [classify, kernel_coordinates_iff]

end PreMssn.TriangleHomology
