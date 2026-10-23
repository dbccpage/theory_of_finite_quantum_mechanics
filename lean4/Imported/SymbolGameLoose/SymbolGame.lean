/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/SymbolGame.lean
   Original sha256: c484feee2b2fbb697cf4d0bf5175d7bf63e93c7de23abf95d433f93b3f330f3d (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.SymbolGameLoose.SymbolGame
   Reason         : S(n)
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.SymbolGameLoose.Expressivity
import Imported.SymbolGameLoose.GrammarCeiling

/-!
# Symbol Game (Inc 4 theory half)

Glue module: pulls in the `expressivityNorm` definition (Q1-A) and the
`expressivity_norm_le_grammar_ceiling` bound theorem (Q1-B).
-/
