# Review of the Genesis replay representation campaign

AuthorityEffect: None. AI self-review, awaiting human review.

Scope: PG-GEN-SUPPLY-ERASURE and its PG-GEN-SUPPLY-NO-OP dependency,
against main `611b954f66d5a3464512dd2a5e5ef6f88013ea84`. The compiled LF
source commit is `2b0da98eb`; the replay receipt supplies its full SHA.

Method: read every exported declaration, its source types and the independent
checker, and compare the atomic claims below. Lean and Lake were not run as
part of this review: the campaign's completed build receipt supplies that
evidence, including its warnings. This is not an independent human review.

Result: 2 FULL, 0 NARROWED, 0 OVERCLAIM for the stated mathematical claims.
No status is raised. The runtime/compiler and Alpha responder boundaries
remain explicit. The one-step potential result is supplementary evidence;
this review does not close the separate engine-mode no-return refinement.

## Per-node statement versus theorem

All new declarations below are in `lean4/CampaignGenesisReplayRefinement.lean`.
The final replay receipt binds each printed declaration to the compiled file.

| Atomic claim | Declaration | Verdict |
|---|---|---|
| Every five-field list-copy regime and event has an inverse source representation | `source_copy` (`lean4/CampaignGenesisReplayRefinement.lean:40`), `copy_source` (`lean4/CampaignGenesisReplayRefinement.lean:43`), `source_copy_event` (`lean4/CampaignGenesisReplayRefinement.lean:46`), `copy_source_event` (`lean4/CampaignGenesisReplayRefinement.lean:49`) | FULL |
| Copy and source steps and every finite partial replay commute | `copy_step_commutes` (`lean4/CampaignGenesisReplayRefinement.lean:56`), `copy_replay_commutes` (`lean4/CampaignGenesisReplayRefinement.lean:74`) | FULL |
| Array coordinates represent the source exactly | `decode_encode` (`lean4/CampaignGenesisReplayRefinement.lean:104`), `encode_decode` (`lean4/CampaignGenesisReplayRefinement.lean:107`), `array_step_commutes` (`lean4/CampaignGenesisReplayRefinement.lean:137`) | FULL |
| Success, every output coordinate and failure are reflected over all finite histories | `array_replay_commutes` (`lean4/CampaignGenesisReplayRefinement.lean:159`), `array_replay_exact` (`lean4/CampaignGenesisReplayRefinement.lean:171`), `array_failure_exact` (`lean4/CampaignGenesisReplayRefinement.lean:184`) | FULL |
| Removing supply preserves the whole partial result | `source_supply_erasure` (`lean4/CampaignGenesisReplayRefinement.lean:201`), `array_supply_erasure` (`lean4/CampaignGenesisReplayRefinement.lean:215`) | FULL |
| Supply does not admit a datum or alter any store, in either declared reading | `source_supply_no_op` (`lean4/CampaignGenesisReplayRefinement.lean:194`), `array_supply_no_op` (`lean4/CampaignGenesisReplayRefinement.lean:197`), `reading_arrays` (`lean4/CampaignGenesisReplayRefinement.lean:278`) | FULL under the declared reading definitions |
| Token-aware duplicate admission erases state-dependently | `token_array_replay` (`lean4/CampaignGenesisReplayRefinement.lean:221`), using compiled source `Derivation.erase_replay` | FULL |
| A successful real source change strictly increases the actual potential | `second_step_commutes` (`lean4/CampaignGenesisReplayRefinement.lean:244`), `source_change_strict` (`lean4/CampaignGenesisReplayRefinement.lean:271`) | FULL for a source step |
| The CPython/Rust runtimes or Alpha responder refine this model | not proved | NOT CLAIMED |

## Numbers recomputed

| Quantity | Exact recomputation | Result |
|---|---|---|
| 92,823 histories from three bases, alphabet size 13, lengths through four | `3 * sum(13**k for k in range(5))`, independently in SymPy | match |
| 88,808 failing histories, 429 successful states, 2,289 strict changes | exhaustive independent interpreters | match |
| 4,681 token histories | `sum(8**k for k in range(5))`, independently in SymPy | match |
| Six killed semantic mutations, three malformed-input refusals | explicit counterexample records and refusal calls | match |
| 26 new declaration audits and two source-erasure audits | terminal print commands matched to parsed successful build output | match |
| Both reading-array coordinates and failure after supply | Lean `reading_arrays` (`lean4/CampaignGenesisReplayRefinement.lean:278`), `invalid_after_supply` (`lean4/CampaignGenesisReplayRefinement.lean:282`); independent replay | match |

No fixed history or argument-length bound occurs in the Lean representation
theorems. The census is regression evidence, not their quantifier scope.

## Corrections and scope fences

The source Basic blob was compared to the exact GitHub blob at the historical
sealed commit, not inferred from a filename or tag label. The companion
erasure and SecondRun modules are separately bound local atlas sources.
No archived source was edited. Compatibility and unused-tactic warnings
are retained, bounding the author assessment to L4D. Lake registration is
L1C under the explicit configuration exception; its capability is not inferred
from the theorem's subject.

Finite execution agreement does not establish runtime or compiler refinement.
The array interpreter is separately defined by array operations, and its
general correspondence is proved against the actual imported source function.
The code does not define its array step by decoding, calling source step and
encoding the answer. Partial failure is not converted into a no-op.

## Scanner and validation

The final scanner and full campaign outputs are recorded in
`dag/research/campaign_pg-gen-supply-erasure_checks.json`. The scan reports HIGH=0, MEDIUM=0, LOW=5. Three LOW findings concern
existing tensor receipt/numeric metadata. Two concern the historical PFP
boilerplate in `dag/derivations/02_genesis/tfq_0379_supply_does_not_admit.md:82`
and `dag/derivations/02_genesis/tfq_0386_supply_erasure_on_replay.md:80`. Exact
SymPy arithmetic gives 520 - 1040 + 780 + 780 = 1040,
4*52 + 3*2 + 4 = 218, and 114 - 56 - 2 = 56; for the other row it gives
530 - 1060 + 795 + 795 = 1060, 4*53 + 3*2 + 2 = 220, and
116 - 57 - 2 = 57. These are descriptor arithmetic, not a derivation of
Genesis or its cochains, and are not used as mathematical premises.
No scanner baseline exception is introduced by this unit. Any pre-existing failing
whole-repository diagnostic is retained in that receipt and the PR body.

## What the scanner cannot decide

Whether an external runtime faithfully implements these mathematical operations,
the Alpha responder/license obligations, and the final human assessment of the
historical and implementation correspondence remain outside this review.
