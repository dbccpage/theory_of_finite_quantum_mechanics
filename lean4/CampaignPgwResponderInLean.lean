/-
Narrowed boundary for PGW-RESPONDER-IN-LEAN.
The mark and the link copy the item shapes of deltaU0 and deltaBL in
lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean.
This module does not apply them to a regime and does not state the sealed responder.
-/

inductive PgwDemand where
  | collapsed
  | separable
  deriving DecidableEq

inductive PgwItem where
  | form (arity : Nat)
  | inst (args : List Nat)
  | rule (index : Nat)
  deriving DecidableEq

def pgwRead (demand : PgwDemand) (holdsUniform : Bool) : Bool :=
  decide (demand = .collapsed) && !holdsUniform

def pgwAritySum : List PgwItem → Nat
  | [] => 0
  | .form a :: rest => a + pgwAritySum rest
  | _ :: rest => pgwAritySum rest

def pgwHasRule : List PgwItem → Bool
  | [] => false
  | .rule _ :: _ => true
  | _ :: rest => pgwHasRule rest

def pgwWithin (items : List PgwItem) : Bool :=
  decide (items.length <= 2) && decide (pgwAritySum items <= 2) && !pgwHasRule items

def pgwMark : List PgwItem := [.form 1, .inst [0]]

def pgwLink : List PgwItem := [.form 2, .inst [0, 1]]

def pgwRuled : List PgwItem := [.form 1, .rule 0]

def pgwThree : List PgwItem := [.form 1, .inst [0], .inst [1]]

def pgwMu1 (items : List PgwItem) : Nat := items.length

def pgwMu2 (items : List PgwItem) : Nat × Nat := (items.length, pgwAritySum items)

def pgwLexLt (p q : Nat × Nat) : Bool :=
  decide (p.1 < q.1) || (decide (p.1 = q.1) && decide (p.2 < q.2))

def pgwReadCount : Nat :=
  (if pgwRead .collapsed false then 1 else 0) +
    (if pgwRead .collapsed true then 1 else 0) +
    (if pgwRead .separable false then 1 else 0) +
    (if pgwRead .separable true then 1 else 0)

theorem pgwRead_table :
    pgwRead .collapsed false = true ∧ pgwRead .collapsed true = false ∧
      pgwRead .separable false = false ∧ pgwRead .separable true = false := by
  decide

theorem pgwRead_count : pgwReadCount = 1 := by
  decide

theorem pgwMark_link_shape :
    pgwMark.length = 2 ∧ pgwLink.length = 2 ∧
      pgwAritySum pgwMark = 1 ∧ pgwAritySum pgwLink = 2 ∧
      pgwMark ≠ pgwLink := by
  decide

theorem pgwMu1_tie : pgwMu1 pgwMark = 2 ∧ pgwMu1 pgwLink = 2 := by
  decide

theorem pgwMu2_pairs :
    pgwMu2 pgwMark = (2, 1) ∧ pgwMu2 pgwLink = (2, 2) := by
  decide

theorem pgwMu2_mark_before_link :
    pgwLexLt (pgwMu2 pgwMark) (pgwMu2 pgwLink) = true := by
  decide

theorem pgwBound_inside :
    pgwWithin pgwMark = true ∧ pgwWithin pgwLink = true := by
  decide

theorem pgwRuled_outside :
    pgwRuled.length = 2 ∧ pgwWithin pgwRuled = false := by
  decide

theorem pgwThree_outside :
    pgwThree.length = 3 ∧ pgwWithin pgwThree = false := by
  decide

#print axioms pgwRead_table
#print axioms pgwRead_count
#print axioms pgwMark_link_shape
#print axioms pgwMu1_tie
#print axioms pgwMu2_pairs
#print axioms pgwMu2_mark_before_link
#print axioms pgwBound_inside
#print axioms pgwRuled_outside
#print axioms pgwThree_outside
