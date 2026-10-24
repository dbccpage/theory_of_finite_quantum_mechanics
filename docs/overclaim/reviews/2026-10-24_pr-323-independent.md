# Independent review of PR #323

Scope: original head f225bc5cf4fd568d9fa84bf8b63c720f84a9438f. Exact source lean4/CampaignPgwIsomorphismSoundnessInLean.lean, SHA-256 c2602a24aae6b99d24608c00c76234467829da96088ed24cdc129f3193370d2b.

AuthorityEffect: None. Result: BLOCKED. No status was raised.

## Statement versus theorem

The two-datum imported U0 and U1 regimes have an explicit swap isomorphism and equal exhaustive keys; the supplied binary BL regime is not isomorphic and its key differs. This uses an imported general classification theorem for three closed fixtures. No Python implementation refinement, budget-truncated search soundness, or exported-run orbit comparison is proved.

| Declaration | Checked statement boundary |
|---|---|
| `lean4/CampaignPgwIsomorphismSoundnessInLean.lean:34 pgwIso_U0_wf` | `: U0.wf` |
| `lean4/CampaignPgwIsomorphismSoundnessInLean.lean:51 pgwIso_U1_wf` | `: U1.wf` |
| `lean4/CampaignPgwIsomorphismSoundnessInLean.lean:68 pgwIso_BL_wf` | `: BL.wf` |
| `lean4/CampaignPgwIsomorphismSoundnessInLean.lean:85 pgwIso_set_collections` | `: SetCollections U0 ∧ SetCollections U1 ∧ SetCollections BL` |
| `lean4/CampaignPgwIsomorphismSoundnessInLean.lean:93 pgwIso_candidate_counts` | `: (candidateKeys U0).length = 2 ∧ (candidateKeys U1).length = 2 ∧ (candidateKeys BL).length = 2` |
| `lean4/CampaignPgwIsomorphismSoundnessInLean.lean:99 pgwIso_keys_eq` | `: canonicalKey U0 = canonicalKey U1` |
| `lean4/CampaignPgwIsomorphismSoundnessInLean.lean:104 pgwIso_U0_not_BL` | `(h : Iso U0 BL) : False` |
| `lean4/CampaignPgwIsomorphismSoundnessInLean.lean:107 pgwIso_keys_ne` | `: canonicalKey U0 ≠ canonicalKey BL` |

## Corrections and acceptance

Current capability: **L2**. The substantive L4 floor is not met. SCORING.md section 2 distinguishes elementary tables and bounded-domain developments from production architecture. A topic, proof count or passing compiler is not a level basis.

Missing companions and stale source bindings are repaired. Existing assessment history is retained; former L4 claims and unrelated supergravity gate text are superseded where present. No policy, baseline, support-exception, floor or scanner allowlist is changed.

Existing six-mutant summaries are historical reports. Their logs and complete candidate bytes were not supplied for independent fault attribution. They do not establish a new mutation score; current generated/killed counts are zero and the ratio is null.

## Verification and numbers

Fresh original-head checks and the repaired-source reruns are in `dag/research/pr_323_independent_review_validation.json`. Independent normal and optimized execution recompute the finite numbers; a passing enumeration does not prove an unbounded or physical interpretation. Compiler module-system warnings are retained. No A/B engineering score is claimed.

## Remaining work

A substantive, actually needed L4 mathematical/API development is required before acceptance. Artificial wrappers and a relabelled score would not resolve this. The current L1D build registration also needs a reviewed current-byte binding under its already-authorized support rule; no new exception is introduced here.

The required DAG/pipeline errors are reported as failures, including errors inherited from the base. This PR must remain a draft until all acceptance requirements pass.
