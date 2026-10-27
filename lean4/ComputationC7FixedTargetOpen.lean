-- Narrowed slice of COMP-C7-FIXED-TARGET-OPEN.
-- Two erasures reach one fixed word.
-- Reach for the extended rule set R0 prime stays open.

structure HoleRule where
  lhs : List Nat
  rhs : List Nat

def applies (rule : HoleRule) (left right word result : List Nat) : Prop :=
  word = left ++ rule.lhs ++ right ∧ result = left ++ rule.rhs ++ right

theorem eraseOneToFixed :
    applies (HoleRule.mk [1] []) [] [0] [1, 0] [0] := by
  constructor <;> rfl

theorem eraseTwoToFixed :
    applies (HoleRule.mk [2] []) [] [0] [2, 0] [0] := by
  constructor <;> rfl

#print axioms eraseOneToFixed
#print axioms eraseTwoToFixed
