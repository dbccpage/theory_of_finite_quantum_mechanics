# Review of the complete Genesis engine-mode source refinement

AuthorityEffect: None. AI self-review, awaiting human review.

Scope: PG-GEN-NO-RETURN against main 4a1e551210459ca8b410fada1e8eddb75e7b052c.
Method: inspect every represented field, guard, failure case and declaration
signature, then the independent census and its exact counts. Not rebuilt by
this review; compilation evidence is the campaign receipt. This is not an
independent human review.

Result: FULL for the stated all-history mathematical no-return claim,
provisional. Existing PROVED_LEAN status remains unchanged.

| Atomic claim | Declaration and exact line | Verdict |
|---|---|---|
| Every full source/array engine state and event has inverse representations | `source_array` (`lean4/CampaignGenesisNoReturn.lean:187`), `array_source` (`lean4/CampaignGenesisNoReturn.lean:191`), `sourceEvent_arrayEvent` (`lean4/CampaignGenesisNoReturn.lean:174`), `arrayEvent_sourceEvent` (`lean4/CampaignGenesisNoReturn.lean:179`) | FULL |
| Every guarded step and every finite optional replay commute | `engine_step_commutes` (`lean4/CampaignGenesisNoReturn.lean:202`), `engine_replay_commutes` (`lean4/CampaignGenesisNoReturn.lean:215`) | FULL |
| Success and failure are both reflected | `engine_replay_exact` (`lean4/CampaignGenesisNoReturn.lean:231`), `engine_replay_failure_exact` (`lean4/CampaignGenesisNoReturn.lean:245`) | FULL |
| Count is cumulative and actual regime change strictly increases it | `cumulative_potential` (`lean4/CampaignGenesisNoReturn.lean:266`), `strict_potential` (`lean4/CampaignGenesisNoReturn.lean:271`) | FULL |
| No return and cycle regimes constant | `no_return` (`lean4/CampaignGenesisNoReturn.lean:254`), `cycle_regime_const` (`lean4/CampaignGenesisNoReturn.lean:261`) | FULL |
| Full state can return after two switches | `two_switches_return` (`lean4/CampaignGenesisNoReturn.lean:277`) | FULL |

External runtime, responder and license refinement are not proved or claimed.
All regime fields and the Boolean mode are represented; two-switch recurrence
is retained. Invalid admission is not converted into a no-op. The count theorem
is transported through the complete interpreter proof rather than assumed as
a proxy for it.

Numbers recomputed: 6 * sum(9**k for k in range(5)) = 44,286 histories, checked
independently in SymPy; 38,638 failures, 204 successful states, 24,914 regime
change occurrences and 9,674 mode-only occurrences are enumerated. Five explicit
counterexample controls are checked. The final successful receipt matches all
twenty-one terminal audits. No history or arity cutoff occurs in the Lean result.

What the scanner cannot decide: whether an external engine runtime or responder
faithfully realizes these source semantics. That claim remains outside this
review and the preserved historical PFP review.
