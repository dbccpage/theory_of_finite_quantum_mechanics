# Independent review of PR #313

Scope: original head 39685dd7815d7d23f6234cd37e0e20d0fe01502a. Exact source lean4/CampaignPgwKItemDeltaGrammar.lean, SHA-256 ec5e9fc278a581722704503dcc453a9421c86e63da5a3fdb90f04de94ccf3e9b.

AuthorityEffect: None. Result: BLOCKED. No status was raised.

## Statement versus theorem

Four copied two-item lists have the stated lengths/arities and are distinct. They are not a complete candidate grammar or a responder-size theorem.

| Declaration | Checked statement boundary |
|---|---|
| `lean4/CampaignPgwKItemDeltaGrammar.lean:30 pgwKItem_lengths` | `: pgwDeltaU0.length = 2 ∧ pgwDeltaU1.length = 2 ∧ pgwDeltaBL.length = 2 ∧ pgwDeltaBD.length = 2` |
| `lean4/CampaignPgwKItemDeltaGrammar.lean:35 pgwKItem_arities` | `: pgwFormArity pgwDeltaU0 = 1 ∧ pgwFormArity pgwDeltaU1 = 1 ∧ pgwFormArity pgwDeltaBL = 2 ∧ pgwFormArity pgwDeltaBD = 2` |
| `lean4/CampaignPgwKItemDeltaGrammar.lean:40 pgwKItem_arity_sum` | `: pgwAritySum4 = 6` |
| `lean4/CampaignPgwKItemDeltaGrammar.lean:43 pgwKItem_pairwise` | `: pgwDeltaU0 ≠ pgwDeltaU1 ∧ pgwDeltaU0 ≠ pgwDeltaBL ∧ pgwDeltaU0 ≠ pgwDeltaBD ∧ pgwDeltaU1 ≠ pgwDeltaBL ∧ pgwDeltaU1 ≠ pgwDeltaBD ∧ pgwDeltaBL ≠ pgwDeltaBD` |
| `lean4/CampaignPgwKItemDeltaGrammar.lean:49 pgwKItem_three_length` | `: ([PgwStep.form 1, .inst [0], .inst [1]] : List PgwStep).length = 3` |
| `lean4/CampaignPgwKItemDeltaGrammar.lean:53 pgwKItem_three_above_two` | `: ([PgwStep.form 1, .inst [0], .inst [1]] : List PgwStep).length > 2` |

## Corrections and acceptance

Current capability: **L2**. The substantive L4 floor is not met. SCORING.md section 2 distinguishes elementary tables and bounded-domain developments from production architecture. A topic, proof count or passing compiler is not a level basis.

Missing companions and stale source bindings are repaired. Existing assessment history is retained; former L4 claims and unrelated supergravity gate text are superseded where present. No policy, baseline, support-exception, floor or scanner allowlist is changed.

Existing six-mutant summaries are historical reports. Their logs and complete candidate bytes were not supplied for independent fault attribution. They do not establish a new mutation score; current generated/killed counts are zero and the ratio is null.

## Verification and numbers

Fresh original-head checks and the repaired-source reruns are in `dag/research/pr_313_independent_review_validation.json`. Independent normal and optimized execution recompute the finite numbers; a passing enumeration does not prove an unbounded or physical interpretation. Compiler module-system warnings are retained. No A/B engineering score is claimed.

## Remaining work

A substantive, actually needed L4 mathematical/API development is required before acceptance. Artificial wrappers and a relabelled score would not resolve this. The current L1D build registration also needs a reviewed current-byte binding under its already-authorized support rule; no new exception is introduced here.

The required DAG/pipeline errors are reported as failures, including errors inherited from the base. This PR must remain a draft until all acceptance requirements pass.
