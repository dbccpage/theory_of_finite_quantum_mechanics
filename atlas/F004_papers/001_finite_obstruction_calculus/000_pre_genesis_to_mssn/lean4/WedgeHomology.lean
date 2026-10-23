import FreeGroup

/-! The cellular graph with one vertex and two loop edges. Its actual integral
H1 is the free abelian group on the edges and has two integer coordinates.
The free-group commutator has zero image in this homology quotient. Continuous
loop/homotopy comparison is not a premise hidden in these definitions. -/
namespace PreMssn.WedgeHomology
open Lean.Grind
open Homology FreeAbelian GraphHomology GraphExtensions FiniteCoordinates

def wedge : Graph where
  Vertex := PUnit
  Edge := Bool
  source _ := PUnit.unit
  target _ := PUnit.unit

theorem boundary_zero (q : Free Bool) : boundary wedge q = 0 := by
  apply hom_ext (boundary wedge) (AddHom.zero _ _) _ q
  intro e
  exact loop_boundary_zero wedge e rfl

def asCycle : AddHom (Free Bool) (Cycle (graphH1Complex wedge)) where
  toFun q := ⟨q, boundary_zero q⟩
  map_zero := rfl
  map_add _ _ := rfl

def cycleValue : AddHom (Cycle (graphH1Complex wedge)) (Free Bool) where
  toFun q := q.val
  map_zero := rfl
  map_add _ _ := rfl

def toFree : AddHom (Homology (graphH1Complex wedge)) (Free Bool) :=
  quotientDescend (boundaryCycle (graphH1Complex wedge)) cycleValue (fun _ => rfl)

def fromFree : AddHom (Free Bool) (Homology (graphH1Complex wedge)) :=
  (quotientProjection (boundaryCycle (graphH1Complex wedge))).comp asCycle

def wedgeH1Iso : AddIso (Homology (graphH1Complex wedge)) (Free Bool) where
  forward := toFree
  backward := fromFree
  left_inverse q := by
    induction q using Quotient.inductionOn with
    | _ a =>
      apply congrArg (quotientProjection (boundaryCycle (graphH1Complex wedge)))
      exact Subtype.ext rfl
  right_inverse _ := rfl

def edgeNumber (b : Bool) : Fin 2 := if b then 1 else 0
def numberedEdge (i : Fin 2) : Bool := i.val != 0

theorem edge_number_left : ∀ b, numberedEdge (edgeNumber b) = b := by decide +kernel
theorem edge_number_right : ∀ i, edgeNumber (numberedEdge i) = i := by decide +kernel

def wedgeH1Coordinates : AddIso (Homology (graphH1Complex wedge)) (Vector 2) :=
  (wedgeH1Iso.comp (carrierIso edgeNumber numberedEdge edge_number_left edge_number_right)).comp
    (freeFiniteIso 2)

def commutatorClass : Homology (graphH1Complex wedge) :=
  fromFree (FreeGroup.abelianization (FreeGroup.commutator (FreeGroup.gen false) (FreeGroup.gen true)))

theorem commutator_class_zero : commutatorClass = 0 := by
  unfold commutatorClass
  rw [FreeGroup.abelianized_commutator, fromFree.map_zero]

theorem commutator_distinction :
    FreeGroup.commutator (FreeGroup.gen false) (FreeGroup.gen true) ≠ (1 : FreeGroup.Free Bool) ∧
      commutatorClass = 0 :=
  ⟨FreeGroup.two_generator_commutator_nontrivial, commutator_class_zero⟩

end PreMssn.WedgeHomology
