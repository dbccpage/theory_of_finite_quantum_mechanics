# ADS-HAPPY-ENTROPY-MINCUT-TARGET

Stage: [ADS_CFT](../stages/ADS_CFT.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Finite statement, checked in Lean 4 for a hand-encoded model. Contract six copies of the six-leg perfect tensor on the {5,4} pentagon tiling: one central tensor and its five edge-neighbours, which are not adjacent to each other, so the patch has 20 dangling boundary legs (4 per outer tensor) and 6 bulk legs, every bulk leg fixed in the logical zero state. In Lean the 20-qubit boundary stabilizer is given by 20 explicit generators (15 local to the five outer blocks and 5 pushed through the internal bonds from the central tensor): they pairwise commute and have full GF(2) rank 20. For all 380 proper contiguous boundary intervals A (20 starting positions, lengths 1 to 19), with S(A) = rank(G restricted to A) - |A| in bits and mincut(A) the minimal number of bonds cut separating A from its complement in the six-tensor star graph: S(A) \<= mincut(A) on all 380 intervals, S(A) = mincut(A) on exactly 340 intervals, and S(A) = mincut(A) - 1 on exactly 40. The Ryu-Takayanagi equality therefore fails on this patch for 40 intervals; it is not a statement that holds for every region.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declaration references covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Not proved in Lean: that the 20 explicit generators are the boundary stabilizer of the contracted six-tensor network with bulk legs fixed at logical zero (they are entered by hand from the pushing rules of the code generators); that mincut as computed (a minimum over side assignments of the six tensors) is the minimal curve cut in the planar dual; the list of the 40 intervals where equality fails (only the counts are stated). The correspondence to a continuum minimal-surface area is the imported formula and is not part of the target.

## Source status

Recomputed in Python on 2026-10-22 across all 380 contiguous intervals of the 20 boundary legs (340 equalities S(A) = mincut(A) and 40 intervals with S(A) = 4 \< 5 = mincut(A)). Lean: checked in Lean 4.35.0 via lake build FrontierHappyMincut (library FrontierTargets in lean4/lakefile.lean) in the form recorded in the statement; replay receipt in dag/research/frontier_targets_lean_replay.json; per-node review in dag/research/frontier_targets_lean_review.md.

## Review

- Frontier Lean review: [dag/research/frontier_targets_lean_review.md](../../../dag/research/frontier_targets_lean_review.md); verdict `NARROWED`; qualifies for E4: yes.
  - theorems that discharge the node, as listed by the review: `boundary_stabilizer_commutes_and_full_rank_20`, `happy_patch_380_intervals_entropy_vs_mincut`
  - the review's reason for its verdict is in the row of this node in the review file

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/FrontierHappyMincut.lean`

- file: [lean4/FrontierHappyMincut.lean](../../../lean4/FrontierHappyMincut.lean)
- sha256 (`bytes`): `6f58261a079f7be32a18dcc1e0b2a7bceb0c823270e474b89ebbdc33d292a5be`
- cited in: node.lean, node.source, receipt dag/research/frontier_targets_lean_replay.json (FrontierHappyMincut)
- replay: `verified`
  - receipt [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json) (module `FrontierHappyMincut`): recorded sha256 `6f58261a079f7be32a18dcc1e0b2a7bceb0c823270e474b89ebbdc33d292a5be` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build FrontierHappyMincut`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FrontierHappyMincut.boundary_stabilizer_commutes_and_full_rank_20` | yes | yes | yes | propext | `#print axioms FrontierHappyMincut.boundary_stabilizer_commutes_and_full_rank_20` |
| `FrontierHappyMincut.happy_patch_380_intervals_entropy_vs_mincut` | yes | yes | yes | propext | `#print axioms FrontierHappyMincut.happy_patch_380_intervals_entropy_vs_mincut` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/32_ads_cft/tfq_2209_ads_happy_entropy_mincut_target.md`

- file: [dag/derivations/32_ads_cft/tfq_2209_ads_happy_entropy_mincut_target.md](../../../dag/derivations/32_ads_cft/tfq_2209_ads_happy_entropy_mincut_target.md)
- sha256 (`lf-normalised`): `dbba6930bf5794144d7e3021228db7df63b19b073c22b37f1e97c8b86e7e8207`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2209
- counts toward the grade: no

### Documents and data: `dag/research/frontier_targets_lean_replay.json`

- file: [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json)
- sha256 (`lf-normalised`): `1c66aabd3bb726fafcd0238c259644d6f79dd304178d171a75ea36d6522bd2cc`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:1503.06237`

## Routes

Incoming (1):

- `FRO-R-ADS-HAPPY-ENTROPY-MINCUT-TARGET` `DERIVED_LEAN`: [ADS-FIVE-QUBIT-PERFECT-TENSOR-TARGET](ADS-FIVE-QUBIT-PERFECT-TENSOR-TARGET.md) (PROVED_LEAN), [ADS-RT-FORMULA-IMPORT](ADS-RT-FORMULA-IMPORT.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

