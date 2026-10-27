/- Imported so that this repository carries its own Lean evidence.
   Original sha256: cb6ea864c35aed2c0d74f99255b41d210761ed8618a0316e57d8589a873c6117 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.LegacyTopLevel.Expressivity
   Reason         : S(n)
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   Renamed        : 2026-10-27, directory and namespace names only (lean4/RENAMES.json).
   AuthorityEffect: None. -/
/-!
# Inc 4 Q1-A: `expressivityNorm` on `Q¹_n`

The expressivity norm on finite symbol strings.

## Carrier

We model an expressivity problem at level `n` as a finite list of
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
terminalizer of the sweep kernel is the only authority surface.
-/

namespace FiniteCosmology.SymbolCarrier

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

end FiniteCosmology.SymbolCarrier
