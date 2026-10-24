/-
Narrowed boundary for PGW-K-ITEM-DELTA-GRAMMAR.
The four lists copy the item shapes of deltaU0, deltaU1, deltaBL, and deltaBD
in lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean.
This module does not apply them to a regime and does not enumerate a sealed space.
-/

inductive PgwStep where
  | form (arity : Nat)
  | inst (args : List Nat)
  deriving DecidableEq

def pgwDeltaU0 : List PgwStep := [.form 1, .inst [0]]

def pgwDeltaU1 : List PgwStep := [.form 1, .inst [1]]

def pgwDeltaBL : List PgwStep := [.form 2, .inst [0, 1]]

def pgwDeltaBD : List PgwStep := [.form 2, .inst [0, 0]]

def pgwFormArity : List PgwStep → Nat
  | [] => 0
  | .form a :: _ => a
  | _ :: rest => pgwFormArity rest

def pgwAritySum4 : Nat :=
  pgwFormArity pgwDeltaU0 + pgwFormArity pgwDeltaU1 +
    pgwFormArity pgwDeltaBL + pgwFormArity pgwDeltaBD

theorem pgwKItem_lengths :
    pgwDeltaU0.length = 2 ∧ pgwDeltaU1.length = 2 ∧
      pgwDeltaBL.length = 2 ∧ pgwDeltaBD.length = 2 := by
  decide

theorem pgwKItem_arities :
    pgwFormArity pgwDeltaU0 = 1 ∧ pgwFormArity pgwDeltaU1 = 1 ∧
      pgwFormArity pgwDeltaBL = 2 ∧ pgwFormArity pgwDeltaBD = 2 := by
  decide

theorem pgwKItem_arity_sum : pgwAritySum4 = 6 := by
  decide

theorem pgwKItem_pairwise :
    pgwDeltaU0 ≠ pgwDeltaU1 ∧ pgwDeltaU0 ≠ pgwDeltaBL ∧ pgwDeltaU0 ≠ pgwDeltaBD ∧
      pgwDeltaU1 ≠ pgwDeltaBL ∧ pgwDeltaU1 ≠ pgwDeltaBD ∧
      pgwDeltaBL ≠ pgwDeltaBD := by
  decide

theorem pgwKItem_three_length :
    ([PgwStep.form 1, .inst [0], .inst [1]] : List PgwStep).length = 3 := by
  decide

theorem pgwKItem_three_above_two :
    ([PgwStep.form 1, .inst [0], .inst [1]] : List PgwStep).length > 2 := by
  decide

#print axioms pgwKItem_lengths
#print axioms pgwKItem_arities
#print axioms pgwKItem_arity_sum
#print axioms pgwKItem_pairwise
#print axioms pgwKItem_three_length
#print axioms pgwKItem_three_above_two
