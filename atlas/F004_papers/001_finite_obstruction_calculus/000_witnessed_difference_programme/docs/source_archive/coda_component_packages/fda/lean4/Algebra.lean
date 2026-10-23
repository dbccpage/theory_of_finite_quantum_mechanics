import FDA

/-!
# Reconstruction FDA algebra

Publication wrapper for `CodaReconstruction.FDA`.

Claim map: FDA-01 `terminal_has_history`, `routing_refusal_persists`;
FDA-02 `standing_sound`; FDA-03 `replay_standing`; FDA-04
`untrusted_verifier_countermodel`, `authority_not_observation`.

Standing is a recorded grant plus a verifying witness. Observation is not
authorization. A pipeline that refuses at routing cannot later mint a terminal.
-/

#check Coda.FDA.standing_sound
#print axioms Coda.FDA.standing_sound
#check Coda.FDA.authority_not_observation
#print axioms Coda.FDA.authority_not_observation
#check Coda.FDA.untrusted_verifier_countermodel
#print axioms Coda.FDA.untrusted_verifier_countermodel
#check Coda.FDA.replay_standing
#print axioms Coda.FDA.replay_standing
#check Coda.FDA.terminal_has_history
#print axioms Coda.FDA.terminal_has_history
#check Coda.FDA.routing_refusal_persists
#print axioms Coda.FDA.routing_refusal_persists
