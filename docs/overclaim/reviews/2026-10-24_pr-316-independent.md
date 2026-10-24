# Independent review of PR #316

Scope: original head b0e963a35bbe065c9c628df73df758a330a4eac6. Exact source lean4/CampaignPgwResponderInLean.lean, SHA-256 a34f1b2c2c613cd3b2dd699af64e683c19d04bfa57b48d659bb8d4cd9bb313b9.

AuthorityEffect: None. Result: BLOCKED. No status was raised.

## Statement versus theorem

A declared Boolean read table, list cost functions, and copied mark/link examples. There is no execution of the sealed responder, no general minimum, and no regime-level refusal theorem.

| Declaration | Checked statement boundary |
|---|---|
| `lean4/CampaignPgwResponderInLean.lean:56 pgwRead_table` | `: pgwRead .collapsed false = true ∧ pgwRead .collapsed true = false ∧ pgwRead .separable false = false ∧ pgwRead .separable true = false` |
| `lean4/CampaignPgwResponderInLean.lean:61 pgwRead_count` | `: pgwReadCount = 1` |
| `lean4/CampaignPgwResponderInLean.lean:64 pgwMark_link_shape` | `: pgwMark.length = 2 ∧ pgwLink.length = 2 ∧ pgwAritySum pgwMark = 1 ∧ pgwAritySum pgwLink = 2 ∧ pgwMark ≠ pgwLink` |
| `lean4/CampaignPgwResponderInLean.lean:70 pgwMu1_tie` | `: pgwMu1 pgwMark = 2 ∧ pgwMu1 pgwLink = 2` |
| `lean4/CampaignPgwResponderInLean.lean:73 pgwMu2_pairs` | `: pgwMu2 pgwMark = (2, 1) ∧ pgwMu2 pgwLink = (2, 2)` |
| `lean4/CampaignPgwResponderInLean.lean:77 pgwMu2_mark_before_link` | `: pgwLexLt (pgwMu2 pgwMark) (pgwMu2 pgwLink) = true` |
| `lean4/CampaignPgwResponderInLean.lean:81 pgwBound_inside` | `: pgwWithin pgwMark = true ∧ pgwWithin pgwLink = true` |
| `lean4/CampaignPgwResponderInLean.lean:85 pgwRuled_outside` | `: pgwRuled.length = 2 ∧ pgwWithin pgwRuled = false` |
| `lean4/CampaignPgwResponderInLean.lean:89 pgwThree_outside` | `: pgwThree.length = 3 ∧ pgwWithin pgwThree = false` |

## Corrections and acceptance

Current capability: **L2**. The substantive L4 floor is not met. SCORING.md section 2 distinguishes elementary tables and bounded-domain developments from production architecture. A topic, proof count or passing compiler is not a level basis.

Missing companions and stale source bindings are repaired. Existing assessment history is retained; former L4 claims and unrelated supergravity gate text are superseded where present. No policy, baseline, support-exception, floor or scanner allowlist is changed.

Existing six-mutant summaries are historical reports. Their logs and complete candidate bytes were not supplied for independent fault attribution. They do not establish a new mutation score; current generated/killed counts are zero and the ratio is null.

## Verification and numbers

Fresh original-head checks and the repaired-source reruns are in `dag/research/pr_316_independent_review_validation.json`. Independent normal and optimized execution recompute the finite numbers; a passing enumeration does not prove an unbounded or physical interpretation. Compiler module-system warnings are retained. No A/B engineering score is claimed.

## Remaining work

A substantive, actually needed L4 mathematical/API development is required before acceptance. Artificial wrappers and a relabelled score would not resolve this. The current L1D build registration also needs a reviewed current-byte binding under its already-authorized support rule; no new exception is introduced here.

The required DAG/pipeline errors are reported as failures, including errors inherited from the base. This PR must remain a draft until all acceptance requirements pass.
