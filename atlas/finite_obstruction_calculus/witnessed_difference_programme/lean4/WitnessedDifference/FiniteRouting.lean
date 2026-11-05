/- Finite mathematical routing evidence; no infinite convergence premise. -/
namespace WitnessedDifference.FiniteRouting
variable {A B C D E F : Type}
theorem transports_closed (d1 : B → C) (e1 : E → F) (f1 : B → E) (f2 : C → F)
    (zeroC : C) (zeroF : F)
    (commute : ∀ x, e1 (f1 x) = f2 (d1 x))
    (preserveZero : f2 zeroC = zeroF) (x : B) (closed : d1 x = zeroC) :
    e1 (f1 x) = zeroF := by rw [commute, closed, preserveZero]
theorem transports_repairs (d0 : A → B) (e0 : D → E) (f0 : A → D) (f1 : B → E)
    (commute : ∀ x, e0 (f0 x) = f1 (d0 x)) (x : A) :
    f1 (d0 x) = e0 (f0 x) := (commute x).symm

def iterate {X : Type} (next : X → X) : Nat → X → X
  | 0, x => x
  | n+1, x => next (iterate next n x)
theorem fixed_point_stationary {X : Type} (next : X → X) (x : X)
    (fixed : next x = x) : ∀ n, iterate next n x = x := by
  intro n
  induction n with
  | zero => rfl
  | succ n ih => exact (congrArg next ih).trans fixed
#print axioms transports_closed
#print axioms transports_repairs
#print axioms fixed_point_stationary
end WitnessedDifference.FiniteRouting
