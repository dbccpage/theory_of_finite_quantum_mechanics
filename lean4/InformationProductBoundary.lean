import Std
namespace InformationProductBoundary
universe u v
/-- Cloning is specified only on the admitted blank-input slice. -/
def Clones {A : Type u} (blank : A) (f : A × A → A × A) : Prop := ∀ x, f (x,blank) = (x,x)
def productCloner {A : Type u} {B : Type v} (f : A × A → A × A) (g : B × B → B × B)
    (p : (A × B) × (A × B)) : (A × B) × (A × B) :=
  let a := f (p.1.1,p.2.1)
  let b := g (p.1.2,p.2.2)
  ((a.1,b.1),(a.2,b.2))

theorem clones_product {A : Type u} {B : Type v} (a : A) (b : B)
    (f : A × A → A × A) (g : B × B → B × B) (hf : Clones a f) (hg : Clones b g) :
    Clones (a,b) (productCloner f g) := by
  intro x; simp [productCloner, hf x.1, hg x.2]

def controlledFlip (p : Bool × Bool) : Bool × Bool := (xor p.1 p.2,p.2)

theorem controlledFlip_involution (p : Bool × Bool) : controlledFlip (controlledFlip p) = p := by
  rcases p with ⟨a,b⟩; cases a <;> cases b <;> rfl

/-- Local reversible operations alone omit a permutation of the composite. -/
theorem controlledFlip_not_product :
    ¬ ∃ f g : Bool → Bool, ∀ p, controlledFlip p = (f p.1,g p.2) := by
  rintro ⟨f,g,h⟩
  have a := congrArg Prod.fst (h (false,false))
  have b := congrArg Prod.fst (h (false,true))
  simp [controlledFlip] at a b
  simp_all
end InformationProductBoundary
#print axioms InformationProductBoundary.clones_product
#print axioms InformationProductBoundary.controlledFlip_involution
#print axioms InformationProductBoundary.controlledFlip_not_product
