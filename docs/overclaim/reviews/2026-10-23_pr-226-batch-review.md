# Independent review of PR #226

AuthorityEffect: None. AI-assisted review; no human approval is claimed.

Scope: 261d75576f2644b184b3bf79be5ef738531daa6e, checker refactoring and evidence corrections. Result: 3 FULL for the finite-game statements of PG-GEN-ONGOING-FEWEST-CHANGES, PG-GEN-ONGOING-OBSTRUCTION and PG-GEN-REWRITING-COMMUTATION. Existing statuses remain unchanged. This is a mathematical representation theorem about the supplied finite game, not runtime/compiler or global engine certification.

| Atomic claim | Declaration location | Boundary |
| --- | --- | --- |
| Complete source-state representation and raw-array legality/WF | CampaignGenesisOngoingRefinement.lean:10-33, decode_encode, legal_iff_source, wf_iff_source | Arrays may duplicate entries; decode takes sets. Classical encode is not deterministic serialization. |
| All guarded operations and exact-length histories in both directions | Same file:52-145, decode operation laws, step_sound/complete, reach_sound/complete, exact_transition_representation | Every source guard retained; a refused image is not a performed change. |
| Costs and matching lower/upper bounds | Same file:36-49 and 230-253, costA_exact, costB_exact, full_fewest_A/B | Upper bound from some initial permutation; lower bound from every permutation. Includes merged names and arbitrary natural labels. |
| Injective rewriting and tracked obstruction | Same file:147-185, source_step_rename, source_reach_rename, renaming_costs, wire_reach_rename, tracked_obstruction_persists, obstruction iff lemmas | Injectivity and no-removal-of-tracked-pair hypotheses remain explicit. |
| Minimum two-step build | Same file:187-228, build_lower_bound, build_two_steps, wire_build_lower_bound | The diagnostic quotient fixes all old terms and produces a loop; it is not itself an allowed identification. |
| Compatibility port and second-seed scope | CampaignGenesisOngoingRename.lean:81,97,218,243 and 281-496 | Original propositions retained; second-seed apart-name/asserted-given premises are not dropped. |

The full port was compared with archived Second/Rename.lean: only inverse rewriting and indexed proof scripts, a new pair_mem helper, and audit prints differ beyond its header. The archive is unchanged. Independent direct replay of the original archive fails at the old rewrite/induction scripts, while a fresh 3,147-job focused build and direct replay of both delivered modules succeed. All 49 unique audited declarations use only propext, Classical.choice and Quot.sound. Nine dependency content hashes match, including the failed original Rename source; no new external provenance attestation is claimed.

The original checker has maximum CCN 50 and cognitive complexity 52. Cognitive complexity above 40 is G5=E under SCORING.md, so its historical D assessment is explicitly corrected without rewriting historical record bytes. Separating enumeration, transition comparison, shortest paths, rewriting, build checks and controls yields maxima 25/22. Unknown operation names now fail explicitly in both implementations.

Four fixed regression fixtures were mislabeled as four executed source mutants. The checker and current note now call them negative controls. A separately executed stale-name source mutation fails the independent source/array equality in both normal and optimized Python. Normal/optimized repaired outputs agree; all original census values remain identical: 627 states, 18,810 attempts, 4,494 performed, 14,316 refused, 627 duplicate controls, two 627-target distance tables with maxima 10/11 and sums 3,006/3,225, 18,810 rewriting squares and 1,827 two-step build controls. Strict mypy passes.

Historical descriptor arithmetic in the author's LOW triage is arithmetically consistent but does not validate the provenance or mathematical relevance of those synthetic PFP blocks. This review does not promote that metadata into source-game evidence. The old independent receipt's mutation-accounting field is a historical output superseded by this review, not a current coverage claim.

Scores: both substantive proof APIs L4D; bounded regression checker L3D and declarative Lake configuration L1D under approved support exceptions. Source-bound evidence includes the original failed replay and the successful delivered replay separately. No full default Lean library build or whole-repository scoring success is asserted. Final integrated campaign checks are recorded separately.
