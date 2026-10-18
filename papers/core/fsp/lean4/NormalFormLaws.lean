import Std

/-!
AuthorityEffect: None.
Concrete normalizers, not route predicates: an integral quotient section and
the binary triangle switching section. These prove the stated finite families;
they do not mechanically verify Python RREF or its general graph traversal.
-/

namespace NormalFormLaws

structure IntegralCochain where
  x : Int
  y : Int
deriving DecidableEq, Repr

def integralGauge (a : Int) (c : IntegralCochain) : IntegralCochain :=
  ⟨c.x + a, c.y + 2 * a⟩

def integralNormal (c : IntegralCochain) : IntegralCochain :=
  ⟨0, c.y - 2 * c.x⟩

def integralEquivalent (c d : IntegralCochain) : Prop :=
  ∃ a : Int, integralGauge a c = d

theorem integral_sound (c : IntegralCochain) :
    integralEquivalent c (integralNormal c) := by
  refine ⟨-c.x, ?_⟩
  cases c with
  | mk x y =>
    simp only [integralGauge, integralNormal]
    congr 1 <;> omega

theorem integral_idempotent (c : IntegralCochain) :
    integralNormal (integralNormal c) = integralNormal c := by
  simp [integralNormal]

theorem integral_complete (c d : IntegralCochain) :
    integralNormal c = integralNormal d ↔ integralEquivalent c d := by
  constructor
  · intro h
    have hy := congrArg IntegralCochain.y h
    refine ⟨d.x - c.x, ?_⟩
    cases c with
    | mk x y =>
      cases d with
      | mk z w =>
        simp only [integralNormal] at hy
        simp only [integralGauge]
        congr 1 <;> omega
  · rintro ⟨a, h⟩
    rw [← h]
    simp only [integralNormal, integralGauge]
    congr 1 <;> omega

structure TriangleSigns where
  s01 : Bool
  s12 : Bool
  s20 : Bool
deriving DecidableEq, Repr

def triangleCycle (s : TriangleSigns) : Bool :=
  (s.s01.xor s.s12).xor s.s20

def triangleNormal (s : TriangleSigns) : TriangleSigns :=
  ⟨false, false, triangleCycle s⟩

def triangleGauge (a0 a1 a2 : Bool) (s : TriangleSigns) : TriangleSigns :=
  ⟨(s.s01.xor a0).xor a1, (s.s12.xor a1).xor a2, (s.s20.xor a2).xor a0⟩

def triangleEquivalent (s t : TriangleSigns) : Prop :=
  ∃ a0 a1 a2 : Bool, triangleGauge a0 a1 a2 s = t

theorem triangle_sound (s : TriangleSigns) :
    triangleEquivalent s (triangleNormal s) := by
  refine ⟨false, s.s01, s.s01.xor s.s12, ?_⟩
  rcases s with ⟨a, b, c⟩
  cases a <;> cases b <;> cases c <;> rfl

theorem triangle_idempotent (s : TriangleSigns) :
    triangleNormal (triangleNormal s) = triangleNormal s := by
  rcases s with ⟨a, b, c⟩
  cases a <;> cases b <;> cases c <;> rfl

theorem triangle_cycle_invariant (s : TriangleSigns) (a0 a1 a2 : Bool) :
    triangleCycle (triangleGauge a0 a1 a2 s) = triangleCycle s := by
  rcases s with ⟨a, b, c⟩
  cases a <;> cases b <;> cases c <;>
    cases a0 <;> cases a1 <;> cases a2 <;> rfl

theorem triangle_complete (s t : TriangleSigns) :
    triangleNormal s = triangleNormal t ↔ triangleEquivalent s t := by
  constructor
  · intro h
    refine ⟨false, s.s01.xor t.s01, (s.s01.xor t.s01).xor (s.s12.xor t.s12), ?_⟩
    rcases s with ⟨a, b, c⟩
    rcases t with ⟨d, e, f⟩
    cases a <;> cases b <;> cases c <;>
      cases d <;> cases e <;> cases f <;> first | rfl | cases h
  · rintro ⟨a0, a1, a2, h⟩
    rw [← h]
    unfold triangleNormal
    rw [triangle_cycle_invariant]

theorem odd_triangle_cannot_be_switched_positive (s : TriangleSigns)
    (h : triangleCycle s = true) (a0 a1 a2 : Bool) :
    triangleGauge a0 a1 a2 s ≠ ⟨false, false, false⟩ := by
  intro hz
  have hi := triangle_cycle_invariant s a0 a1 a2
  rw [hz, h] at hi
  cases hi

#print axioms integral_sound
#print axioms integral_idempotent
#print axioms integral_complete
#print axioms triangle_sound
#print axioms triangle_idempotent
#print axioms triangle_cycle_invariant
#print axioms triangle_complete
#print axioms odd_triangle_cannot_be_switched_positive

end NormalFormLaws
