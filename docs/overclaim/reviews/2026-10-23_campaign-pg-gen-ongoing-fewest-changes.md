# Review of the Genesis-Ongoing source refinement

AuthorityEffect: None. AI self-review, awaiting human review.

Scope: PG-GEN-ONGOING-FEWEST-CHANGES and the related obstruction/rewriting
interfaces, against main d5c544cc94ad7a85f8853df7aa65107e2801796c. Method: inspect every represented field,
constructor guard and both directions of the replay relation, the cost-bound
quantifiers, compatibility port and independent census. Not rebuilt by this
review; the campaign replay supplies compilation evidence.

Result: 3 FULL, 0 NARROWED, 0 OVERCLAIM for the stated finite-game mathematics, provisional. Existing
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

Numeric LOW triage (exact SymPy, all historical blocks):

- `dag/derivations/02_genesis/tfq_0388_ongoing_obstruction_answers.md:69`: [570, -1140, 855] plus 855 = 1140; 4*57 + 3*2 + 3 = 237; 124 - 61 - 2 = 61.
- `dag/derivations/02_genesis/tfq_0389_fewest_changes_formula.md:68`: [590, -1180, 885] plus 885 = 1180; 4*59 + 3*2 + 2 = 244; 128 - 63 - 2 = 63.
- `dag/derivations/02_genesis/tfq_0389_fewest_changes_formula.md:81`: [580, -1160, 870] plus 870 = 1160; 4*58 + 3*2 + 4 = 242; 126 - 62 - 2 = 62.
- `dag/derivations/02_genesis/tfq_0390_rewriting_and_persistence_reconcile.md:71`: [590, -1180, 885] plus 885 = 1180; 4*59 + 3*2 + 2 = 244; 128 - 63 - 2 = 63.

These descriptor identities are not premises of the source game proof. The new note's census is independently recomputed; 4.35.0 is a toolchain identifier. Three further LOW findings are inherited tensor receipt/numeric metadata. Receipt attribution was corrected so port symbols are assigned to the port file, with explicit port citations; no new broken reference is accepted.

The port also explicitly audits `Seed.Second.Step3.rename`, `Reach3.rename`,
`fewest_changes3_every_writing_A` and `_B` in `lean4/CampaignGenesisOngoingRename.lean`, retaining their second-seed scopes. These are additional direct witnesses for the original rewriting node, separate from the four-move first-seed wrappers.

Second-seed exact anchors: `Seed.Second.Step3.rename`
(`lean4/CampaignGenesisOngoingRename.lean:81`), `Reach3.rename` (:97),
`fewest_changes3_every_writing_A` (:218) and `_B` (:243). Their apart-name and
asserted-given premises are retained; they are not the unrestricted first-seed
four-move formula. Final successful replay reports 49 distinct audit anchors:
29 refinement declarations, 16 compatibility declarations, and four source
build declarations. Every axiom is permitted. All 24 prescribed campaign tests
and static campaign gates pass. Scanner HIGH=0, MEDIUM=0, LOW=7; all numeric
findings are triaged above. The two additional repository diagnostic failures
remain the unchanged HilbertLiftOperators JSON error and TFQ-0084 prompt delta.
The regenerated evidence map introduces no broken reference or uncited module.
