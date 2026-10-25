# PR #318: sequential repair and merge decision

AuthorityEffect: None. Outcome: NARROWED; acceptance remains BLOCKED.

This PR is the first item in the requested sequential queue. No later PR is advanced by this decision.

## Concrete repair

In `checks/independent/pgw-declared-input-floor.py`, the former `prints_axioms` guard counted report lines. Replacing `pgwInput_eq_items` by a second `pgwBounds_values` report kept that count unchanged and passed the guard. The repaired guard compares the complete multiset of report names with `THEOREM_NAMES`, so a duplicate cannot replace a required name.

The source-bound regression is [the guard receipt](2026-10-24_pr-318-axiom-report-regression.json). It records these actual exits:

| Checker | Unchanged source | Duplicate replacing a required report | Missing report |
|---|---|---|---|
| Historical | 0 | 0 (defect reproduced) | 1 |
| Repaired | 0 | 1 | 1 |

Normal and optimized CLI execution retain `checked 39 claims, failures 0`. Import remains quiet and does not mutate `sys.path`; strict mypy passes. The one new checker-guard mutation is counted as one generated and one killed. This is a narrowly scoped regression, not a general mutation-coverage certificate. Earlier zero-count checker bookkeeping is retained as superseded history. The formal proof assessment still claims no new proof mutation campaign.

## Statement versus theorem

`lean4/CampaignPgwDeclaredInputFloor.lean:10-26` declares seven numerals and a candidate list. Its eight theorems at lines 28-53 evaluate those supplied constants and list comparisons. It does not quantify over engines, responder minima, admissible candidate deltas, runs, or extensions of a run beyond the experiment's bounds. Its current capability remains L1D. The independent checker remains L2D. Neither meets the substantive L4D floor.

| Required claim | Delivered evidence | Decision |
|---|---|---|
| The displayed bound numerals and elementary comparisons | The eight Lean declarations and the independent arithmetic/source check | NARROWED |
| A necessary declared-input floor | No such Lean declaration | NOT PROVED |
| A one-input reduction that continues past the historical bounds | No responder or unbounded continuation theorem in this PR | NOT PROVED |
| The alternate completion-gate reading | No new author ruling or formal discharge | NOT ESTABLISHED |

## The missing bridge is identified by the sources

The local imported development says explicitly that the candidate space, responder and generators were not reconstructed: `lean4/Imported/Genesis19l57g1/SecondRun/Run.lean:18-25`. Its event-history monotonicity theorem therefore cannot certify a particular responder's minimum or continued availability of responses.

The pinned original [PROMPT.md:298-302](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_run/PROMPT.md#L298-L302) states the same boundary. [STATUS.md:309-313](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_run/STATUS.md#L309-L313) names extending the carriers past the bounds as open and says that a Lean statement of the chain needs the responder in Lean. [CLAIM_LEDGER.md:119](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_run/CLAIM_LEDGER.md#L119) labels the streamless-carrier observation a finite computation and excludes a floor proof or unbounded reduction.

The actual [carries_forward definition](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_run/fwd_runs.py#L465-L472) tests the nonempty bounded frontier and absence of a switch marker in those representative histories. It is not an unbounded liveness decision. These are source inspections; the historical engine enumeration was not replayed here. Returned UTF-8 source hashes and precise citations are in [the source audit](2026-10-24_pr-318-pinned-source-audit.json). The imported Lean header preserves the original F004 paper-tree path and its custody hash.

The substantive repair still needed is an actual formalization of the admitted candidate grammar, demand generator, both responder validity/cost rules with every tied minimum, and the relation of those responses to admitted events. A floor theorem or a continuation proof must then concern those definitions, including every retained bound. A new wrapper around the seven numerals would not supply that bridge.

## Checks and refusal

Fresh Lean 4.35.0 elaboration passed at the unchanged proof-source hash, with the pinned Mathlib source. The current campaign pipeline and binding/history results are in [the final report](2026-10-24_pr-318-campaign-checks.md) and `dag/research/pr_318_campaign_pipeline.json`; these are regenerated after the checker repair. The earlier fresh sequential attempt and the missing-sparse-input attempt remain in the local evidence records. Only the named sealed inputs were restored from exact Git blobs; no shared cache target was copied or changed.

Governance retains the focal L1D floor rejection and the unrelated base companion binding failure for `CampaignSnE08WeightedL1Duality.lean`. The latter is not an excuse to accept the former. No new exception, baseline change, population reduction, node promotion or inflated capability score is introduced. The PR remains draft and is not merged. The sequential queue stops here until #318 actually satisfies the retained acceptance rules.

Direct fresh elaboration and all axiom outputs are in [the fresh Lean receipt](2026-10-24_pr-318-fresh-elaboration.json). Lake module replay is recorded separately; the direct invocation does not rely on that replay.
