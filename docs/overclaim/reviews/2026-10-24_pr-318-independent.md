# Independent review of PR #318

Scope: original head 3f3fdc5f5c5f238a7fac4ef10f6172a8db5dabcf. Exact source lean4/CampaignPgwDeclaredInputFloor.lean, SHA-256 4d60da82673bbba0522a875cbfa3b99c7ba076845b877b5a97438110da6e5beb.

AuthorityEffect: None. Result: BLOCKED. No status was raised.

## Statement versus theorem

Seven declared constants and a filtered candidate list. The values do not prove a necessary input floor or execute any engine.

| Declaration | Checked statement boundary |
|---|---|
| `lean4/CampaignPgwDeclaredInputFloor.lean:28 pgwBounds_values` | `: pgwRounds = 15 ∧ pgwGuard = 250 ∧ pgwDataCeiling = 4 ∧ pgwItemBound = 2 ∧ pgwInputCount = 2 ∧ pgwEngines = 4 ∧ pgwReadings = 2` |
| `lean4/CampaignPgwDeclaredInputFloor.lean:34 pgwInput_eq_items` | `: pgwInputCount = pgwItemBound` |
| `lean4/CampaignPgwDeclaredInputFloor.lean:37 pgwOne_below_input` | `: 1 < pgwInputCount` |
| `lean4/CampaignPgwDeclaredInputFloor.lean:40 pgwGuard_above_rounds` | `: pgwRounds < pgwGuard` |
| `lean4/CampaignPgwDeclaredInputFloor.lean:43 pgwEngines_ne_readings` | `: pgwEngines ≠ pgwReadings` |
| `lean4/CampaignPgwDeclaredInputFloor.lean:46 pgwStrictlyBelow_list` | `: pgwStrictlyBelow = [0, 1, 2, 3]` |
| `lean4/CampaignPgwDeclaredInputFloor.lean:49 pgwStrictlyBelow_length` | `: pgwStrictlyBelow.length = 4` |
| `lean4/CampaignPgwDeclaredInputFloor.lean:52 pgwCeiling_not_below` | `: decide (pgwDataCeiling < pgwDataCeiling) = false` |

## Corrections and acceptance

Current capability: **L1**. The substantive L4 floor is not met. SCORING.md section 2 distinguishes elementary tables and bounded-domain developments from production architecture. A topic, proof count or passing compiler is not a level basis.

Missing companions and stale source bindings are repaired. Existing assessment history is retained; former L4 claims and unrelated supergravity gate text are superseded where present. No policy, baseline, support-exception, floor or scanner allowlist is changed.

Existing six-mutant summaries are historical reports. Their logs and complete candidate bytes were not supplied for independent fault attribution. They do not establish a new mutation score; current generated/killed counts are zero and the ratio is null.

## Verification and numbers

Fresh original-head checks and the repaired-source reruns are in `dag/research/pr_318_independent_review_validation.json`. Independent normal and optimized execution recompute the finite numbers; a passing enumeration does not prove an unbounded or physical interpretation. Compiler module-system warnings are retained. No A/B engineering score is claimed.

## Remaining work

A substantive, actually needed L4 mathematical/API development is required before acceptance. Artificial wrappers and a relabelled score would not resolve this. The current L1D build registration also needs a reviewed current-byte binding under its already-authorized support rule; no new exception is introduced here.

The required DAG/pipeline errors are reported as failures, including errors inherited from the base. This PR must remain a draft until all acceptance requirements pass.
