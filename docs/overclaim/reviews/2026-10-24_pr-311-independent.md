# Independent review of PR #311

Scope: original head 15ed49e105af679648d5bcf3272b2dc6cc491604. Exact source lean4/CampaignPgwContextFidelity.lean, SHA-256 b2e809eb8eb262db8101602ebeb242043e07260005f91b7cc848ac061656ac81.

AuthorityEffect: None. Result: BLOCKED. No status was raised.

## Statement versus theorem

A two-code equality table rejects (0,1) and accepts (1,1). It neither defines general ValidTrace nor validates real replay histories.

| Declaration | Checked statement boundary |
|---|---|
| `lean4/CampaignPgwContextFidelity.lean:24 pgwContext_codes_differ` | `: pgwContextStale ≠ pgwContextReplay` |
| `lean4/CampaignPgwContextFidelity.lean:27 pgwContext_empty_claim_on_stale` | `: pgwContextEmptyClaim pgwContextStale = true` |
| `lean4/CampaignPgwContextFidelity.lean:30 pgwContext_empty_claim_on_replay` | `: pgwContextEmptyClaim pgwContextReplay = false` |
| `lean4/CampaignPgwContextFidelity.lean:33 pgwContext_binding_refuses_stale` | `: pgwContextAcceptBinding pgwContextStale pgwContextReplay = false` |
| `lean4/CampaignPgwContextFidelity.lean:37 pgwContext_binding_accepts_match` | `: pgwContextAcceptBinding pgwContextReplay pgwContextReplay = true` |
| `lean4/CampaignPgwContextFidelity.lean:41 pgwContext_accept_count` | `: pgwContextAcceptCount = 2` |

## Corrections and acceptance

Current capability: **L1**. The substantive L4 floor is not met. SCORING.md section 2 distinguishes elementary tables and bounded-domain developments from production architecture. A topic, proof count or passing compiler is not a level basis.

Missing companions and stale source bindings are repaired. Existing assessment history is retained; former L4 claims and unrelated supergravity gate text are superseded where present. No policy, baseline, support-exception, floor or scanner allowlist is changed.

Existing six-mutant summaries are historical reports. Their logs and complete candidate bytes were not supplied for independent fault attribution. They do not establish a new mutation score; current generated/killed counts are zero and the ratio is null.

## Verification and numbers

Fresh original-head checks and the repaired-source reruns are in `dag/research/pr_311_independent_review_validation.json`. Independent normal and optimized execution recompute the finite numbers; a passing enumeration does not prove an unbounded or physical interpretation. Compiler module-system warnings are retained. No A/B engineering score is claimed.

## Remaining work

A substantive, actually needed L4 mathematical/API development is required before acceptance. Artificial wrappers and a relabelled score would not resolve this. The current L1D build registration also needs a reviewed current-byte binding under its already-authorized support rule; no new exception is introduced here.

The required DAG/pipeline errors are reported as failures, including errors inherited from the base. This PR must remain a draft until all acceptance requirements pass.
