/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/research_programs/wdp_reasoning/RefinementAxioms.lean
   Original sha256: 09ac0b21525cbf7cd67af904346d7a44060296734cb7a55a68ccf82a30805df1 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.WdpReasoning.RefinementAxioms
   Reason         : WDP
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.WdpReasoning.ExecutableReasoning

#print axioms WitnessedReasoning.Executable.references_sound
#print axioms WitnessedReasoning.Executable.checkStep_sound
#print axioms WitnessedReasoning.Executable.replay_sound
#print axioms WitnessedReasoning.Executable.checkStep_justified
#print axioms WitnessedReasoning.Executable.replay_refines_trace
#print axioms WitnessedReasoning.Executable.checkProof_binding
#print axioms WitnessedReasoning.Executable.checkProof_sound
#print axioms WitnessedReasoning.Executable.checkCountermodel_binding
#print axioms WitnessedReasoning.Executable.checkCountermodel_models
#print axioms WitnessedReasoning.Executable.checkCountermodel_sound
#print axioms WitnessedReasoning.Executable.checked_verdicts_exclusive
#print axioms WitnessedReasoning.Executable.checked_interpretation
#print axioms WitnessedReasoning.Executable.graph_derivable_reachable
#print axioms WitnessedReasoning.Executable.graph_reachable_derivable
#print axioms WitnessedReasoning.Executable.graph_derivable_iff_reachable
#print axioms WitnessedReasoning.Executable.checked_graph_proof
#print axioms WitnessedReasoning.Executable.checked_graph_countermodel
