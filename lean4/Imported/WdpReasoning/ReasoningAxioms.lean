/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/research_programs/wdp_reasoning/ReasoningAxioms.lean
   Original sha256: 3478e5702a14e75a0824563206dc52fd6a095556c99d192f887dc5880f0cda4f (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.WdpReasoning.ReasoningAxioms
   Reason         : WDP
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.WdpReasoning.WitnessedReasoning

#print axioms WitnessedReasoning.derivation_sound
#print axioms WitnessedReasoning.derivable_is_model
#print axioms WitnessedReasoning.derivable_iff_entailed
#print axioms WitnessedReasoning.countermodel_excludes_derivation
#print axioms WitnessedReasoning.inert_seed_derives_nothing
#print axioms WitnessedReasoning.checked_trace_derivable
#print axioms WitnessedReasoning.checked_trace_sound
#print axioms WitnessedReasoning.learned_rule_conservative
#print axioms WitnessedReasoning.interpreted_claim_sound
#print axioms WitnessedReasoning.derivation_substitution
#print axioms WitnessedReasoning.theory_weakening
#print axioms WitnessedReasoning.report_collision
#print axioms WitnessedReasoning.processing_preserves_collision
#print axioms WitnessedReasoning.history_collision
#print axioms WitnessedReasoning.constant_question_needs_no_injective_report
