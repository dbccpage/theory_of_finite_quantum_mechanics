import WitnessedDifference.Core

/-!
# Primitive difference and a typed finite coboundary identity
-/

namespace WitnessedDifference

structure PrimitiveDifference (α : Type _) where
  left : α
  right : α
  apart : left ≠ right

namespace PrimitiveDifference

def parity {α : Type _} [DecidableEq α]
    (d : PrimitiveDifference α) (x : α) : Option Bool :=
  if x = d.left then some false
  else if x = d.right then some true
  else none

@[simp] theorem parity_left {α : Type _} [DecidableEq α]
    (d : PrimitiveDifference α) : d.parity d.left = some false := by
  simp [parity]

@[simp] theorem parity_right {α : Type _} [DecidableEq α]
    (d : PrimitiveDifference α) : d.parity d.right = some true := by
  simp [parity, d.apart.symm]

theorem parity_separates_marks {α : Type _} [DecidableEq α]
    (d : PrimitiveDifference α) :
    d.parity d.left ≠ d.parity d.right := by
  simp

end PrimitiveDifference

namespace Cochain

def d0 {Vertex A : Type _} [Sub A]
    (f : Vertex → A) (a b : Vertex) : A :=
  f b - f a

def d1 {Vertex A : Type _} [Add A] [Sub A]
    (edge : Vertex → Vertex → A) (a b c : Vertex) : A :=
  edge b c - edge a c + edge a b

theorem triangle_d1_d0
    {Vertex A : Type _} [AddCommGroup A]
    (f : Vertex → A) (a b c : Vertex) :
    d1 (d0 f) a b c = 0 := by
  simp only [d1, d0]
  exact AddCommGroup.triangle_zero (f a) (f b) (f c)

end Cochain
end WitnessedDifference
