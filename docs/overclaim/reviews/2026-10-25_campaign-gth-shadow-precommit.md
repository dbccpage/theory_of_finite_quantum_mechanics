# Overclaim review: GTH-SHADOW

AuthorityEffect: None.

## Scope

The narrowed statement of GTH-SHADOW (record TFQ-2400). Status stays OPEN. No other node is in this review.

## Method

The module `lean4/CampaignGthShadow.lean` was read in full. The campaign build `lake build CampaignGthShadow` under Lean 4.35.0 exited 0 before this review; this review did not rebuild it and uses that receipt. The module has no import. Mathlib v4.35.0 commit 56a005855ea17e0b0958f73ec801ae140b0a1679 was present through a junction and unused by this module. Each `#print axioms` line in the receipt names no axioms. The independent check `checks/independent/gth-shadow.py` recomputed the same integers and printed `checked 19 conditions, 0 failures`. Every numeral in the narrowed statement was recomputed that way.

The genesis-to-higher fragment rejects a non-empty `lean` list on this node. The node `lean` list stays empty. The module is cited from the node source and from the replay receipt, and it is not a status witness.

## Result

0 FULL, 1 NARROWED, 0 OVERCLAIM.

## Corrections to the PR's own text

None. The statement is one triangle, one reach map, and one pair of parallel edges. A construction from the admission gate stays in the bottleneck. Status stays OPEN.

## Per-node table

| Node | Theorems that discharge it | Verdict | Reason |
|---|---|---|---|
| GTH-SHADOW | `face_id_01`, `face_id_02`, `face_id_12`, `reach_collapses`, `reach_pair_differs`, `parallel_edges` | NARROWED | The theorems are six `decide` facts on one triangle and two constant maps. They do not build a semi-simplicial set from the admission gate. The node `lean` list stays empty. Status stays OPEN. |

### Statement versus theorem

| Claim | Declaration | Verdict |
|---|---|---|
| the target of (0, 2) equals the target of (1, 2), and both are 2 | `face_id_01` | NARROWED |
| the target of (0, 1) equals the source of (1, 2), and both are 1 | `face_id_02` | NARROWED |
| the source of (0, 1) equals the source of (0, 2), and both are 0 | `face_id_12` | NARROWED |
| the reach map sends 0 and 1 to 0 | `reach_collapses` | NARROWED |
| the pair (0, 0) differs from the edge (0, 1) | `reach_pair_differs` | NARROWED |
| the two source values agree at 0 and the two target values agree at 1 | `parallel_edges` | NARROWED |
| a construction from the admission gate | not proved | NOT PROVED |
| a general finite semi-simplicial set or globular set | not proved | NOT PROVED |

## Numbers recomputed

| Number | Recomputation | Match |
|---|---|---|
| 0 | sources of (0, 1) and (0, 2), both reach values, and both edge sources | match |
| 1 | target of (0, 1), source of (1, 2), and both edge targets | match |
| 2 | targets of (0, 2) and (1, 2) | match |
| 19 | conditions counted by the independent check | match |
| 0 | failures counted by that check | match |

## Axioms

`face_id_01`, `face_id_02`, `face_id_12`, `reach_collapses`, `reach_pair_differs`, and `parallel_edges` depend on no axioms. The module contains no `sorry`, no `axiom` declaration, no `native_decide`, and no `unsafe`.

## What the scanner could not decide

`scripts/overclaim_scan.py --changed-since origin/main --strict` reported HIGH 0, MEDIUM 0, LOW 3. Those LOW findings are R10 on TENSOR-ASSUMPTION-COUNTERMODELS and R5 on the refreshed notes for FQ-GAP-TENSOR-UNIQUENESS (`20261019`) and TENSOR-ASSUMPTION-COUNTERMODELS (`1/2`, `1/4`). They were left unchanged.

The executed prompt `dag/prompts/genesis_to_higher_gth_shadow_open.yaml` still carries the earlier research target. `generate_prompts.py` refused to rewrite that executed prompt. The node statement is the narrowed triangle.

These six `decide` facts do not build a shadow from the admission gate. The scanner cannot tell this triangle from that missing construction; the table above is the decision.
