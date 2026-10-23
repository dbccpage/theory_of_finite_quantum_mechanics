# Review of the Genesis-Ongoing source refinement

AuthorityEffect: None. AI self-review, awaiting human review.

Scope: PG-GEN-ONGOING-FEWEST-CHANGES and the related obstruction/rewriting
interfaces, against main d5c544cc94ad7a85f8853df7aa65107e2801796c. Method: inspect every represented field,
constructor guard and both directions of the replay relation, the cost-bound
quantifiers, compatibility port and independent census. Not rebuilt by this
review; the campaign replay supplies compilation evidence.

Result: FULL for the stated finite-game mathematics, provisional. Existing
node statuses are unchanged. The original source Rename failure is retained.

| Atomic claim | Declaration and exact line | Verdict |
|---|---|---|
| Every source set state, merged names and arbitrary labels | `decode_encode` (`lean4/CampaignGenesisOngoingRefinement.lean:22`), `legal_iff_source` (`lean4/CampaignGenesisOngoingRefinement.lean:30`), `wf_iff_source` (`lean4/CampaignGenesisOngoingRefinement.lean:33`) | FULL within the stated source game |
| All source and wire guarded transitions, both directions and exact history lengths | `step_sound` (`lean4/CampaignGenesisOngoingRefinement.lean:88`), `step_complete` (`lean4/CampaignGenesisOngoingRefinement.lean:101`), `reach_sound` (`lean4/CampaignGenesisOngoingRefinement.lean:120`), `reach_complete` (`lean4/CampaignGenesisOngoingRefinement.lean:126`), `exact_transition_representation` (`lean4/CampaignGenesisOngoingRefinement.lean:136`) | FULL within the stated source game |
| Exact raw-array costs and all-writing lower/upper bounds | `costA_exact` (`lean4/CampaignGenesisOngoingRefinement.lean:46`), `costB_exact` (`lean4/CampaignGenesisOngoingRefinement.lean:49`), `full_fewest_A` (`lean4/CampaignGenesisOngoingRefinement.lean:230`), `full_fewest_B` (`lean4/CampaignGenesisOngoingRefinement.lean:242`) | FULL within the stated source game |
| Injective term rewriting, source histories, costs and wire histories | `source_step_rename` (`lean4/CampaignGenesisOngoingRefinement.lean:154`), `source_reach_rename` (`lean4/CampaignGenesisOngoingRefinement.lean:158`), `renaming_costs` (`lean4/CampaignGenesisOngoingRefinement.lean:162`), `wire_reach_rename` (`lean4/CampaignGenesisOngoingRefinement.lean:167`) | FULL within the stated source game |
| Tracked assertion persists through every no-remove history | `tracked_obstruction_persists` (`lean4/CampaignGenesisOngoingRefinement.lean:172`) | FULL within the stated source game |
| Exact assertion and identification obstructions | `identify_obstruction_iff` (`lean4/CampaignGenesisOngoingRefinement.lean:177`), `assertion_obstruction_iff` (`lean4/CampaignGenesisOngoingRefinement.lean:182`) | FULL within the stated source game |
| Legal build in two changes and general minimum of two | `build_two_steps` (`lean4/CampaignGenesisOngoingRefinement.lean:215`), `build_lower_bound` (`lean4/CampaignGenesisOngoingRefinement.lean:201`), `wire_build_lower_bound` (`lean4/CampaignGenesisOngoingRefinement.lean:223`) | FULL within the stated source game |

Corrections and boundaries: the upper bound chooses some initial writing; the
lower bound quantifies over all writings. Raw array order and duplicates are
quotiented to the source sets; encode uses classical finite-set enumeration.
An obstructed image is not an admitted performed change. No per-stage or
finite-game result is advertised as whole-engine minimality or runtime refinement.

Compatibility audit: the archive's Second/Rename.lean fails unchanged in Lean
4.35.0. The separate CampaignGenesisOngoingRename port retains its definitions
and propositions and repairs proof terms. The changed declarations are the two
all-writing bound proofs, ReachNoRemove.toReach, its obstruction proof (now via
pair_mem), and the final Reach decomposition's indexed cases. These are proofs
about the actual imported source St/Step/Reach, not a new surrogate game.

Numbers recomputed: the checker enumerates 627 states; 18,810 attempts = 4,494
performed + 14,316 refused; 627 duplicate-wire controls; both 627-target shortest
path tables (maxima 10/11, sums 3,006/3,225); 18,810 nonconsecutive rewriting
squares and 1,827 build controls. Four exact mutant controls are checked.
The source offsets three and four and the build minimum two are general Lean
bounds, also confirmed independently. General proofs have no state/label bound.

What the scanner cannot decide: whether an external runtime implements this
wire model faithfully or a human accepts the compatibility port and scope.
The failed original source is not claimed to have passed a replay.
