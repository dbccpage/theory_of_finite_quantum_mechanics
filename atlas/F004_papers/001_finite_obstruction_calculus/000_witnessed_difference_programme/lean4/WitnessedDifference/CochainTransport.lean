/- Structural transport laws with their exact hypotheses. Core Lean.
   No norm preservation or unrestricted horn filling is inferred. -/
import Init

namespace WitnessedDifference.CochainTransport

def Repairs {R C : Type} (add : C → C → C) (d : R → C) (x y : C) : Prop :=
  ∃ r, y = add x (d r)

theorem repair_transport {R C R' C' : Type}
    (add : C → C → C) (add' : C' → C' → C')
    (d : R → C) (d' : R' → C') (f0 : R → R') (f1 : C → C')
    (additive : ∀ x y, f1 (add x y) = add' (f1 x) (f1 y))
    (square : ∀ r, f1 (d r) = d' (f0 r))
    {x y : C} (repair : Repairs add d x y) : Repairs add' d' (f1 x) (f1 y) := by
  obtain ⟨r, equation⟩ := repair
  refine ⟨f0 r, ?_⟩
  rw [equation, additive, square]

theorem composed_square {A B C A' B' C' : Type}
    (d : A → A') (e : B → B') (k : C → C')
    (f0 : A → B) (f1 : A' → B') (g0 : B → C) (g1 : B' → C')
    (first : ∀ a, f1 (d a) = e (f0 a))
    (second : ∀ b, g1 (e b) = k (g0 b)) :
    ∀ a, g1 (f1 (d a)) = k (g0 (f0 a)) := by
  intro a
  rw [first, second]

theorem retraction_reflects_repair {R C R' C' : Type}
    (add : C → C → C) (add' : C' → C' → C')
    (d : R → C) (d' : R' → C')
    (up : C → C') (down0 : R' → R) (down1 : C' → C)
    (additive : ∀ x y, down1 (add' x y) = add (down1 x) (down1 y))
    (square : ∀ r, down1 (d' r) = d (down0 r))
    (retract : ∀ x, down1 (up x) = x)
    {x y : C} (repair : Repairs add' d' (up x) (up y)) : Repairs add d x y := by
  have descended := repair_transport add' add d' d down0 down1 additive square repair
  simpa only [retract] using descended

theorem homotopy_agrees_on_closed_classes {C0 C1 C2 D1 : Type}
    (add : D1 → D1 → D1) (zeroC : C2) (zeroD : D1)
    (right_unit : ∀ x, add x zeroD = x)
    (d0 : C0 → D1) (d1 : C1 → C2) (h1 : C1 → C0) (h2 : C2 → D1)
    (left right : C1 → D1)
    (zero : h2 zeroC = zeroD)
    (filler : ∀ x, left x = add (right x) (add (d0 (h1 x)) (h2 (d1 x))))
    (x : C1) (closed : d1 x = zeroC) : Repairs add d0 (right x) (left x) := by
  refine ⟨h1 x, ?_⟩
  rw [filler, closed, zero, right_unit]

#print axioms repair_transport
#print axioms composed_square
#print axioms retraction_reflects_repair
#print axioms homotopy_agrees_on_closed_classes
end WitnessedDifference.CochainTransport
