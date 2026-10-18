/-!
# Inc 4 Q1-A: `expressivityNorm` on `Q¹_n`

The Lean side of the Symbol Game expressivity norm, lined up with the Rust
`omega_symbol_game::expressivity::norm`.

## Carrier

We model a Symbol-Game expressivity problem at level `n` as a finite list of
overlap discrepancies `h : List Int`. Each entry is the integer discrepancy
on one overlap of the declared nerve. The Rust crate keeps the rational
representative; here we work over `Int` because the verdict trichotomy and
the grammar ceiling are integer-valued.

## Norm

`expressivityNorm h := Σ_e |h e|`.

This is the rational `ℓ¹` mass `‖h_n‖_1` of the C¹ defect cochain, computed on
a *chosen canonical representative*. It does NOT descend to the quotient `Q¹_n`:
it is invariant only under the kernel of `d⁰` (a constant potential, where
`d⁰ c = (c.tgt - c.src) = 0` leaves every entry fixed), NOT under a general
`δ ∈ im d⁰`, since a non-constant potential changes the per-entry `natAbs` and
hence the sum. The Rust S2 AT witnesses the constant-gauge invariance and
exhibits a non-constant potential that shifts the value.

## Firewall

This file is the *definition*. Authority is not minted here. The
companion file `GrammarCeiling.lean` proves the bound; the sealed
terminalizer in `omega_sweep_kernel` is the only authority surface.
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

namespace OmegaCosmology.SymbolGame

/-- `expressivityNorm h := Σ |h e|` — the rational ℓ¹ mass of the C¹
    defect cochain `h_n`. -/
def expressivityNorm (h : List Int) : Nat :=
  h.foldr (fun x acc => x.natAbs + acc) 0

/-- The empty problem has zero norm. -/
theorem expressivityNorm_nil : expressivityNorm [] = 0 := rfl

/-- The norm of a cons is the head plus the tail. -/
theorem expressivityNorm_cons (x : Int) (xs : List Int) :
    expressivityNorm (x :: xs) = x.natAbs + expressivityNorm xs := rfl

/-- The norm is non-negative (it lives in `Nat`). -/
theorem expressivityNorm_nonneg (h : List Int) : 0 ≤ expressivityNorm h := by
  exact Nat.zero_le _

/-- The defect mass adds across a disjoint union of overlaps. -/
theorem expressivityNorm_append (h1 h2 : List Int) :
    expressivityNorm (h1 ++ h2) = expressivityNorm h1 + expressivityNorm h2 := by
  induction h1 with
  | nil =>
    rw [List.nil_append, expressivityNorm_nil, Nat.zero_add]
  | cons x xs ih =>
    rw [List.cons_append, expressivityNorm_cons, ih, expressivityNorm_cons, Nat.add_assoc]

/-- Global sign flip of the cochain does not change the ℓ¹ mass. -/
theorem expressivityNorm_neg (h : List Int) :
    expressivityNorm (h.map Neg.neg) = expressivityNorm h := by
  induction h with
  | nil => rfl
  | cons x xs ih =>
    rw [List.map_cons, expressivityNorm_cons, expressivityNorm_cons, Int.natAbs_neg, ih]

/-- A non-constant shift of `[1, -1]` changes the norm, so the mass does not
    descend along a general coboundary. -/
theorem nonconstant_shift_changes_norm :
    expressivityNorm [1, -1] = 2 ∧
      expressivityNorm [2, -1] = 3 ∧
      expressivityNorm [1, -1] ≠ expressivityNorm [2, -1] := by
  decide

end OmegaCosmology.SymbolGame
