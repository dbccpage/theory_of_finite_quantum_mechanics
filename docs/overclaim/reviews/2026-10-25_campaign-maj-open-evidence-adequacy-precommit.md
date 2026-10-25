# Overclaim review: MAJ-OPEN-EVIDENCE-ADEQUACY

AuthorityEffect: None.

## Scope

The narrowed statement of MAJ-OPEN-EVIDENCE-ADEQUACY (record TFQ-1182). Status stays OPEN. No other node is in this review.

## Method

The module `lean4/CampaignMajOpenEvidenceAdequacy.lean` was read in full. The campaign build `lake build CampaignMajOpenEvidenceAdequacy` under Lean 4.35.0 exited 0 before this review; this review did not rebuild it and uses that receipt. The module has no import. Mathlib v4.35.0 commit 56a005855ea17e0b0958f73ec801ae140b0a1679 was present through a junction and unused by this module. Each `#print axioms` line in the receipt names no axioms. The independent check `checks/independent/maj-open-evidence-adequacy.py` recomputed the same integers and printed `checked 10 conditions, 0 failures`. Every numeral in the narrowed statement was recomputed that way.

## Result

0 FULL, 1 NARROWED, 0 OVERCLAIM.

## Corrections to the PR's own text

None. The statement is two integer readings and two coordinate maps. A laboratory protocol, a device model, a density operator, and a physical measurement map stay in the bottleneck. Status stays OPEN.

## Per-node table

| Node | Theorems that discharge it | Verdict | Reason |
|---|---|---|---|
| MAJ-OPEN-EVIDENCE-ADEQUACY | `diff_is_zero_neg_one`, `first_coord_kernel`, `second_coord_separates` | NARROWED | The theorems are three `decide` facts on the pairs (1, 0) and (1, 1). They do not supply a laboratory measurement map. Status stays OPEN. |

### Statement versus theorem

| Claim | Declaration | Verdict |
|---|---|---|
| the difference of (1, 0) and (1, 1) is (0, -1) | `diff_is_zero_neg_one` | NARROWED |
| the first coordinate of the difference is 0 and both readings have first coordinate 1 | `first_coord_kernel` | NARROWED |
| the second coordinate of the difference is -1, and the second coordinates are 0 and 1 | `second_coord_separates` | NARROWED |
| those second coordinates differ | `second_coord_separates` | NARROWED |
| a laboratory protocol separates topological zero modes from Andreev bound states | not proved | NOT PROVED |
| a density operator or a physical measurement map | not proved | NOT PROVED |

## Numbers recomputed

| Number | Recomputation | Match |
|---|---|---|
| 1 | first coordinate of both readings, and `1 - 1 = 0` | match |
| 0 | second coordinate of topo, first coordinate of the difference, and `1 - 1` | match |
| -1 | `0 - 1`, the second coordinate of the difference, and the second coordinate of (0, -1) | match |
| 10 | conditions counted by the independent check | match |
| 0 | failures counted by that check | match |

## Axioms

`diff_is_zero_neg_one`, `first_coord_kernel`, and `second_coord_separates` depend on no axioms. The module contains no `sorry`, no `axiom` declaration, no `native_decide`, and no `unsafe`.

## What the scanner could not decide

`scripts/overclaim_scan.py --changed-since origin/main --strict` reported HIGH 0, MEDIUM 0, LOW 3. Those LOW findings are R10 on TENSOR-ASSUMPTION-COUNTERMODELS and R5 on the refreshed notes for FQ-GAP-TENSOR-UNIQUENESS (`20261019`) and TENSOR-ASSUMPTION-COUNTERMODELS (`1/2`, `1/4`). They were left unchanged.

These three `decide` facts do not answer the laboratory question. The scanner cannot tell the two coordinate maps from a physical measurement protocol; the table above is the decision.
