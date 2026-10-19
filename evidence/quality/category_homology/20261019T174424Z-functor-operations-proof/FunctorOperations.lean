import Mathlib.CategoryTheory.Functor.Basic

/-! AuthorityEffect: None. Actual Mathlib identity/composition, pure partial-map
composition, and exact endpoint-data equality guard. Raw opposite/inclusion
declarations still require separate admission; no Rust/MIR extraction. -/
namespace TFQM.FunctorOperations
open CategoryTheory
variable {C D E H : Type} [Category C] [Category D] [Category E] [Category H]

theorem identity_object (X : C) : (𝟭 C).obj X = X := rfl
theorem identity_arrow {X Y : C} (f : X ⟶ Y) : (𝟭 C).map f = f := rfl
theorem composite_object (F : C ⥤ D) (G : D ⥤ E) (X : C) :
    (F ⋙ G).obj X = G.obj (F.obj X) := rfl
theorem composite_arrow (F : C ⥤ D) (G : D ⥤ E) {X Y : C} (f : X ⟶ Y) :
    (F ⋙ G).map f = G.map (F.map f) := rfl
theorem identity_then (F : C ⥤ D) : 𝟭 C ⋙ F = F := rfl
theorem then_identity (F : C ⥤ D) : F ⋙ 𝟭 D = F := rfl
theorem compose_associative (F : C ⥤ D) (G : D ⥤ E) (K : E ⥤ H) :
    (F ⋙ G) ⋙ K = F ⋙ (G ⋙ K) := rfl

def composePartial {α β γ : Type} (f : α → Option β) (g : β → Option γ) : α → Option γ :=
  fun x => (f x).bind g
theorem first_missing {α β γ : Type} (f : α → Option β) (g : β → Option γ) (x : α)
    (h : f x = none) : composePartial f g x = none := by simp [composePartial,h]
theorem second_missing {α β γ : Type} (f : α → Option β) (g : β → Option γ) (x : α) (y : β)
    (hf : f x = some y) (hg : g y = none) : composePartial f g x = none := by
  simp [composePartial,hf,hg]
theorem partial_success {α β γ : Type} (f : α → Option β) (g : β → Option γ)
    (x : α) (y : β) (z : γ) (hf : f x = some y) (hg : g y = some z) :
    composePartial f g x = some z := by simp [composePartial,hf,hg]
theorem partial_associative {α β γ δ : Type} (f : α → Option β) (g : β → Option γ)
    (k : γ → Option δ) : composePartial (composePartial f g) k = composePartial f (composePartial g k) := by
  funext x
  cases h : f x with
  | none => simp [composePartial,h]
  | some y => simp [composePartial,h]

structure Endpoint where
  name : String
  data : List String
  deriving DecidableEq

def exactMiddle {α : Type} (left right : Endpoint) (candidate : α) : Except Unit α :=
  if left = right then .ok candidate else .error ()
theorem equal_middle {α : Type} (endpoint : Endpoint) (candidate : α) :
    exactMiddle endpoint endpoint candidate = .ok candidate := by simp [exactMiddle]
theorem unequal_middle {α : Type} (left right : Endpoint) (candidate : α) (h : left ≠ right) :
    exactMiddle left right candidate = .error () := by simp [exactMiddle,h]
theorem names_insufficient {α : Type} (name : String) (first last : List String) (candidate : α)
    (h : first ≠ last) : exactMiddle ⟨name,first⟩ ⟨name,last⟩ candidate = .error () := by
  apply unequal_middle
  intro same
  exact h (congrArg Endpoint.data same)

def reverseTable {α β : Type} (table : α → α → β) : α → α → β := fun f g => table g f
theorem reverse_entry {α β : Type} (table : α → α → β) (f g : α) :
    reverseTable table f g = table g f := rfl
theorem reverse_twice {α β : Type} (table : α → α → β) : reverseTable (reverseTable table) = table := rfl

end TFQM.FunctorOperations

#print axioms TFQM.FunctorOperations.identity_object
#print axioms TFQM.FunctorOperations.identity_arrow
#print axioms TFQM.FunctorOperations.composite_object
#print axioms TFQM.FunctorOperations.composite_arrow
#print axioms TFQM.FunctorOperations.identity_then
#print axioms TFQM.FunctorOperations.then_identity
#print axioms TFQM.FunctorOperations.compose_associative
#print axioms TFQM.FunctorOperations.first_missing
#print axioms TFQM.FunctorOperations.second_missing
#print axioms TFQM.FunctorOperations.partial_success
#print axioms TFQM.FunctorOperations.partial_associative
#print axioms TFQM.FunctorOperations.equal_middle
#print axioms TFQM.FunctorOperations.unequal_middle
#print axioms TFQM.FunctorOperations.names_insufficient
#print axioms TFQM.FunctorOperations.reverse_entry
#print axioms TFQM.FunctorOperations.reverse_twice
