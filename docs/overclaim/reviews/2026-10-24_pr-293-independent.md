# Independent review of PR #293

Scope: original head 792fdf2d66015416c3b3b7e5e0282bf3c044b526. Exact source lean4/CampaignL1U1SelectorFiniteField.lean, SHA-256 c6923e5a0caf8b78f30dd401f71c13cdb1c9001a75c7a7d30096e3b3965ecbf3.

AuthorityEffect: None. Result: BLOCKED. No status was raised.

## Statement versus theorem

The Fin 5 norm table and product examples are exhaustive for that carrier. They do not select a coefficient field or derive a general finite-field circle formula.

| Declaration | Checked statement boundary |
|---|---|
| `lean4/CampaignL1U1SelectorFiniteField.lean:15 circle_iff` | `(x y : Fin 5) : x * x + y * y = 1 ↔ (x = 0 ∧ y = 1) ∨ (x = 0 ∧ y = 4) ∨ (x = 1 ∧ y = 0) ∨ (x = 4 ∧ y = 0)` |
| `lean4/CampaignL1U1SelectorFiniteField.lean:21 circle_count` | `: circleCount = 4 := rfl theorem four_eq_pred_five : 4 = 5 - 1 := rfl theorem six_eq_succ_five : 5 + 1 = 6 := rfl theorem four_ne_six : 4 ≠ 6` |
| `lean4/CampaignL1U1SelectorFiniteField.lean:30 four_plus_one_eq_zero` | `: (4 : Fin 5) + 1 = 0` |
| `lean4/CampaignL1U1SelectorFiniteField.lean:33 gen_square` | `: mul5 0 1 0 1 = (4, 0)` |
| `lean4/CampaignL1U1SelectorFiniteField.lean:36 gen_square_ne_one` | `: ((4 : Fin 5), 0) ≠ (1, 0)` |
| `lean4/CampaignL1U1SelectorFiniteField.lean:39 gen_cube` | `: mul5 4 0 0 1 = (0, 4)` |
| `lean4/CampaignL1U1SelectorFiniteField.lean:42 gen_fourth` | `: mul5 0 4 0 1 = (1, 0)` |
| `lean4/CampaignL1U1SelectorFiniteField.lean:45 off_circle_one_one` | `: (1 : Fin 5) * 1 + 1 * 1 ≠ 1` |
| `lean4/CampaignL1U1SelectorFiniteField.lean:48 one_one_norm` | `: (1 : Fin 5) * 1 + 1 * 1 = 2` |
| `lean4/CampaignL1U1SelectorFiniteField.lean:51 two_ne_one` | `: 2 ≠ 1` |
| `lean4/CampaignL1U1SelectorFiniteField.lean:54 isotropic_nonzero` | `: ((2 : Fin 5), 1) ≠ (0, 0)` |
| `lean4/CampaignL1U1SelectorFiniteField.lean:57 isotropic_norm_zero` | `: (2 : Fin 5) * 2 + 1 * 1 = 0` |

## Corrections and acceptance

Current capability: **L2**. The substantive L4 floor is not met. SCORING.md section 2 distinguishes elementary tables and bounded-domain developments from production architecture. A topic, proof count or passing compiler is not a level basis.

Missing companions and stale source bindings are repaired. Existing assessment history is retained; former L4 claims and unrelated supergravity gate text are superseded where present. No policy, baseline, support-exception, floor or scanner allowlist is changed.

Existing six-mutant summaries are historical reports. Their logs and complete candidate bytes were not supplied for independent fault attribution. They do not establish a new mutation score; current generated/killed counts are zero and the ratio is null.

## Verification and numbers

Fresh original-head checks and the repaired-source reruns are in `dag/research/pr_293_independent_review_validation.json`. Independent normal and optimized execution recompute the finite numbers; a passing enumeration does not prove an unbounded or physical interpretation. Compiler module-system warnings are retained. No A/B engineering score is claimed.

## Remaining work

A substantive, actually needed L4 mathematical/API development is required before acceptance. Artificial wrappers and a relabelled score would not resolve this. The current L1D build registration also needs a reviewed current-byte binding under its already-authorized support rule; no new exception is introduced here.

The required DAG/pipeline errors are reported as failures, including errors inherited from the base. This PR must remain a draft until all acceptance requirements pass.
