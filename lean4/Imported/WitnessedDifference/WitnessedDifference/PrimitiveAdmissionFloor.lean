/- Imported from the sibling atlas so that this repository carries its own Lean evidence.
   Original path : omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/PrimitiveAdmissionFloor.lean
   Original sha256: df9d149bbd06124fd7b6226656f0588be037bbbf121f12c99ec35ea4b123ae15 (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.WitnessedDifference.WitnessedDifference.PrimitiveAdmissionFloor
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
/- Explicit admission floor. The inscription supplies none of these inputs.
   Core Lean; AuthorityEffect: None. -/
import Init

namespace WitnessedDifference.PrimitiveAdmissionFloor

structure ExhibitedCut (V : Type) where
  relation : V → V → Prop
  first : V
  second : V
  exhibited : relation first second
  protectedLaw : ∀ x, ¬ relation x x

theorem endpoints_apart {V : Type} (cut : ExhibitedCut V) : cut.first ≠ cut.second := by
  intro same
  have diagonal := cut.exhibited
  rw [same] at diagonal
  exact cut.protectedLaw cut.second diagonal

theorem no_cut_on_subsingleton {V : Type} [Subsingleton V] (cut : ExhibitedCut V) : False :=
  endpoints_apart cut (Subsingleton.elim _ _)

theorem identification_breaks_law {V W : Type} (cut : ExhibitedCut V)
    (q : V → W) (target : W → W → Prop)
    (preserves : ∀ x y, cut.relation x y → target (q x) (q y))
    (law : ∀ w, ¬ target w w) : q cut.first ≠ q cut.second := by
  intro same
  have transported := preserves cut.first cut.second cut.exhibited
  rw [same] at transported
  exact law (q cut.second) transported

/- Minimality of the witness hypotheses, independently of any glyph reading. -/
theorem instance_without_law_allows_singleton :
    ∃ (r : Unit → Unit → Prop), r () () :=
  ⟨fun _ _ => True, True.intro⟩

theorem law_without_instance_allows_singleton :
    ∃ (r : Unit → Unit → Prop), ∀ x, ¬ r x x :=
  ⟨fun _ _ => False, fun _ impossible => impossible⟩

def forwardCut : ExhibitedCut Bool where
  relation x y := x = false ∧ y = true
  first := false
  second := true
  exhibited := ⟨rfl, rfl⟩
  protectedLaw := by
    intro x diagonal
    cases x <;> simp at diagonal

def reverseCut : ExhibitedCut Bool where
  relation x y := x = true ∧ y = false
  first := true
  second := false
  exhibited := ⟨rfl, rfl⟩
  protectedLaw := by
    intro x diagonal
    cases x <;> simp at diagonal

theorem minimum_has_two_orientations : forwardCut.first ≠ reverseCut.first := by
  decide

/- Under a declared unary/binary separation language, either choice has two
   admitted items (one form, one instance). Only a priced arity tie-breaker
   distinguishes them. This is not a cost theorem for an undeclared language. -/
inductive SeparationResponse where
  | unaryMark
  | binaryLink
deriving DecidableEq

def itemCost (_ : SeparationResponse) : Nat := 2
def arityCost : SeparationResponse → Nat
  | .unaryMark => 1
  | .binaryLink => 2

theorem raw_item_cost_ties : itemCost .unaryMark = itemCost .binaryLink := rfl
theorem declared_arity_cost_selects : arityCost .unaryMark < arityCost .binaryLink := by decide

#print axioms endpoints_apart
#print axioms no_cut_on_subsingleton
#print axioms identification_breaks_law
#print axioms instance_without_law_allows_singleton
#print axioms law_without_instance_allows_singleton
#print axioms minimum_has_two_orientations
#print axioms raw_item_cost_ties
#print axioms declared_arity_cost_selects
end WitnessedDifference.PrimitiveAdmissionFloor
