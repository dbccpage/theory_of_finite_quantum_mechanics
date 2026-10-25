-- Campaign narrowing of COMP-C2-STEP3-NOT-WORD-STEP.
-- Three concrete list moves are one-hole word steps.
-- The general Genesis Step3 encoding stays open.

structure HoleRule where
  lhs : List Nat
  rhs : List Nat

def applies (rule : HoleRule) (left right word result : List Nat) : Prop :=
  word = left ++ rule.lhs ++ right ∧ result = left ++ rule.rhs ++ right

theorem addTermWordStep :
    applies (HoleRule.mk [] [1]) [0] [] [0] [0, 1] := by
  constructor <;> rfl

theorem addAssertionWordStep :
    applies (HoleRule.mk [] [0, 1]) [0, 1] [] [0, 1] [0, 1, 0, 1] := by
  constructor <;> rfl

theorem identifyWordStep :
    applies (HoleRule.mk [1] []) [0] [] [0, 1] [0] := by
  constructor <;> rfl

def merge01 (t : Nat) : Nat :=
  if t = 1 then 0 else t

theorem merge01SendsBothToZero : merge01 0 = 0 ∧ merge01 1 = 0 ∧ 0 ≠ 1 := by
  decide

theorem merge01FixesOther (t : Nat) (h : t ≠ 1) : merge01 t = t := by
  unfold merge01
  simp [h]

#print axioms addTermWordStep
#print axioms addAssertionWordStep
#print axioms identifyWordStep
#print axioms merge01SendsBothToZero
#print axioms merge01FixesOther
