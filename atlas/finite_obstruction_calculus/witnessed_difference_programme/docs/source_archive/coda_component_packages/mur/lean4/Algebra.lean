/-!
# Reconstruction MUR algebra

Self-contained formalization of reconstruction MUR algebra (MUR-D1, MUR-T1, MUR-T3, MUR-T4, MUR-T5).
AuthorityEffect: None.

A transport is a commuting square of states and observations. Composites
commute. A collision of observations is preserved. A collapsed fibre cannot
be recovered.
-/

namespace Coda.MUR

structure Transport (X : Type _) (A : Type _) (Y : Type _) (B : Type _) (p : X → A) (q : Y → B) where
  states : X → Y
  observations : A → B
  commutes : ∀ x, q (states x) = observations (p x)

def Transport.comp {X A Y B Z C : Type _} {p : X → A} {q : Y → B} {r : Z → C}
    (f : Transport X A Y B p q) (g : Transport Y B Z C q r) : Transport X A Z C p r where
  states := g.states ∘ f.states
  observations := g.observations ∘ f.observations
  commutes := by intro x; simp [g.commutes, f.commutes]

theorem composite_commutes {X A Y B Z C : Type _} {p : X → A} {q : Y → B} {r : Z → C}
    (f : Transport X A Y B p q) (g : Transport Y B Z C q r) (x : X) :
    r (g.states (f.states x)) = g.observations (f.observations (p x)) := by
  rw [g.commutes, f.commutes]

theorem collision_transports {X A Y B : Type _} {p : X → A} {q : Y → B}
    (f : Transport X A Y B p q) {x y : X} (same : p x = p y) :
    q (f.states x) = q (f.states y) := by rw [f.commutes, f.commutes, same]

theorem postprocess_preserves_collision {X A B : Type _} (p : X → A) (f : A → B)
    {x y : X} (h : p x = p y) : f (p x) = f (p y) := congrArg f h

theorem loss_is_not_recoverable :
    ¬ ∃ recover : Unit → Bool, ∀ b, recover () = b := by
  rintro ⟨recover, h⟩
  have impossible : false = true := (h false).symm.trans (h true)
  cases impossible

end Coda.MUR

#check Coda.MUR.composite_commutes
#print axioms Coda.MUR.composite_commutes
#check Coda.MUR.collision_transports
#print axioms Coda.MUR.collision_transports
#check Coda.MUR.postprocess_preserves_collision
#print axioms Coda.MUR.postprocess_preserves_collision
#check Coda.MUR.loss_is_not_recoverable
#print axioms Coda.MUR.loss_is_not_recoverable
