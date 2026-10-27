-- COMP-C3-NO-FIXED-BOUND. Not a default target.
-- One letter, no rewrite step, length bound 1.
-- A computable start-word map and normal-form reachability stay outside this module.


namespace ComputationC3NoFixedBound
abbrev Word := List (Fin 1)

def bound : Nat := 1

def start : Word := [0]

def long : Word := [0, 0]

def emptyW : Word := []

def inBound (w : Word) : Prop := w.length ≤ bound

inductive ReachB : Word → Word → Prop where
  | refl (a : Word) : ReachB a a

theorem reach_eq {a b : Word} (h : ReachB a b) : a = b := by
  cases h
  rfl

theorem reaches_self : ReachB start start :=
  ReachB.refl start

theorem start_in : inBound start := by
  simp [inBound, start, bound]

theorem empty_in : inBound emptyW := by
  simp [inBound, emptyW, bound]

theorem long_len : long.length = 2 := by
  simp [long]

theorem long_out : ¬ inBound long := by
  simp [inBound, long, bound]

theorem not_long : ¬ ReachB start long := by
  intro h
  have hlen : start.length = long.length := by
    rw [reach_eq h]
  simp [start, long] at hlen

theorem not_empty : ¬ ReachB start emptyW := by
  intro h
  have hlen : start.length = emptyW.length := by
    rw [reach_eq h]
  simp [start, emptyW] at hlen

#print axioms reach_eq
#print axioms reaches_self
#print axioms start_in
#print axioms empty_in
#print axioms long_len
#print axioms long_out
#print axioms not_long
#print axioms not_empty

end ComputationC3NoFixedBound
