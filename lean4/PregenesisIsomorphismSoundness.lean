/-
Narrowed boundary for PGW-ISOMORPHISM-SOUNDNESS-IN-LEAN.
A coloring is a pair of bits. The key is the lexicographic minimum of
that pair, read as numbers, and the pair with the two bits exchanged.
This module does not check an implemented regime key or an exported orbit.
-/

abbrev PgwIsoColor := Bool × Bool

def pgwIsoSwap (c : PgwIsoColor) : PgwIsoColor := (c.2, c.1)

def pgwIsoBit (b : Bool) : Nat := if b then 1 else 0

def pgwIsoSer (c : PgwIsoColor) : Nat × Nat := (pgwIsoBit c.1, pgwIsoBit c.2)

def pgwIsoKey (c : PgwIsoColor) : Nat × Nat :=
  let s := pgwIsoSer c
  let t := pgwIsoSer (pgwIsoSwap c)
  if s.1 < t.1 then s
  else if t.1 < s.1 then t
  else if s.2 ≤ t.2 then s
  else t

def pgwIsoUniverse : List PgwIsoColor :=
  [(false, false), (false, true), (true, false), (true, true)]

theorem pgwIsoSwapInvolutive (c : PgwIsoColor) : pgwIsoSwap (pgwIsoSwap c) = c := by
  rcases c with ⟨a, b⟩
  rfl

theorem pgwIsoKeysOfFour :
    pgwIsoKey (false, false) = (0, 0) ∧
    pgwIsoKey (false, true) = (0, 1) ∧
    pgwIsoKey (true, false) = (0, 1) ∧
    pgwIsoKey (true, true) = (1, 1) := by
  decide

theorem pgwIsoKeySwap (c : PgwIsoColor) : pgwIsoKey (pgwIsoSwap c) = pgwIsoKey c := by
  rcases c with ⟨a, b⟩
  cases a <;> cases b <;> decide

theorem pgwIsoKeyIff (c d : PgwIsoColor) :
    pgwIsoKey c = pgwIsoKey d ↔ (c = d ∨ pgwIsoSwap c = d) := by
  rcases c with ⟨a, b⟩
  rcases d with ⟨x, y⟩
  cases a <;> cases b <;> cases x <;> cases y <;> decide

theorem pgwIsoConstants :
    pgwIsoSwap (false, false) = (false, false) ∧
    pgwIsoSwap (true, true) = (true, true) ∧
    pgwIsoKey (false, false) ≠ pgwIsoKey (true, true) := by
  decide

theorem pgwIsoFour : pgwIsoUniverse.length = 4 := by
  decide

theorem pgwIsoMixed :
    (pgwIsoUniverse.filter fun c => decide (pgwIsoKey c = (0, 1))).length = 2 := by
  decide

#print axioms pgwIsoSwapInvolutive
#print axioms pgwIsoKeysOfFour
#print axioms pgwIsoKeySwap
#print axioms pgwIsoKeyIff
#print axioms pgwIsoConstants
#print axioms pgwIsoFour
#print axioms pgwIsoMixed
