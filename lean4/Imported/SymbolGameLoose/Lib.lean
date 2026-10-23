/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/Lib.lean
   Original sha256: 255425e183973deb7597bca9dc734800b1df7ede284a549a91e1b9a66a045eb8 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.SymbolGameLoose.Lib
   Reason         : S(n)
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.SymbolGameLoose.Expressivity
import Imported.SymbolGameLoose.Family
/-!
# Symbol Game (Inc 4 theory half)

Glue module: pulls in the `expressivityNorm` definition (Q1-A) and the
`expressivity_norm_le_grammar_ceiling` bound theorem (Q1-B).
-/
