# LQG-PR-ALLOWED-REGION-TARGET

Stage: [LOOP_QUANTUM_GRAVITY](../stages/LOOP_QUANTUM_GRAVITY.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Finite statement, checked in Lean 4 in the following narrowed form. For each admissible 6-tuple (a,b,c,d,e,f) of twice-spins at most 8 (all four triads (a,b,c), (a,e,f), (d,b,f), (d,e,c) admissible), take lengths l = j + 1/2 = (twice-spin + 1)/2. Lean computes 288 V^2 (scaled by 64, as the integer cayleyMengerScaled64) as the 3x3 Gram determinant of the squared edge lengths at the vertex where a, b, f meet, which equals the Cayley-Menger determinant. Across all 13,691 admissible 6-tuples: 10,884 have 288 V^2 \> 0 (classically allowed region, a Euclidean tetrahedron exists), 2,807 have 288 V^2 \< 0 (forbidden region), and none has 288 V^2 = 0. Exact values of 288 V^2 and of the squared 6j symbol are checked on three witnesses only: (2,2,2,2,2,2) with 729/16 and 1/36; (1,1,2,1,1,2) with -81/16 and 1/36; (2,2,4,2,2,4) with -4375/16 and 1/900. The comparison of magnitudes with the asymptotic formula is numerical and imported, and is not part of the target.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Not proved in Lean: the exact squared 6j value for every tuple (three witnesses only, so the node does not give "the exact value in each case"); the identity between the 3x3 Gram form used by Lean and the bordered 5x5 Cayley-Menger determinant (an independent exact Python recomputation with the bordered 5x5 determinant reproduces the counts 13,691 / 10,884 / 2,807 and the three witness values); that 288 V^2 = 0 never occurs for any shifted-spin tuple (the module header claims it through a congruence mod 8; only the count 0 for twice-spins \<= 8 is a Lean theorem). The Cayley-Menger sign convention follows the P0 mining run of TFQ-0084; the asymptotic comparison is not exact.

## Source status

Cayley-Menger determinant 288 V^2 regimes (4 \> 0 for regular j=1/2, 0 for flat, -6075/16 \< 0 for admissible a=(4,4,4,4,4,8)) recomputed with Python fractions.Fraction on 2026-10-22. Lean: checked in Lean 4.35.0 via lake build FrontierPrAllowedRegion (library FrontierTargets in lean4/lakefile.lean) in the form recorded in the statement; replay receipt in dag/research/frontier_targets_lean_replay.json; per-node review in dag/research/frontier_targets_lean_review.md.

## Review

- Frontier Lean review: [dag/research/frontier_targets_lean_review.md](../../../dag/research/frontier_targets_lean_review.md); verdict `NARROWED`; qualifies for E4: yes.
  - theorems that discharge the node, as listed by the review: `ponzano_regge_allowed_forbidden_classification_le8`, `allowed_and_forbidden_witnesses_with_6j_squares`
  - the review's reason for its verdict is in the row of this node in the review file

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/FrontierPrAllowedRegion.lean`

- file: [lean4/FrontierPrAllowedRegion.lean](../../../lean4/FrontierPrAllowedRegion.lean)
- sha256 (`bytes`): `9005ac46571d0b3b728b37a7edc5ff2e45b201979e92861021251da371910446`
- cited in: node.lean, node.source, receipt dag/research/frontier_targets_lean_replay.json (FrontierPrAllowedRegion)
- replay: `verified`
  - receipt [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json) (module `FrontierPrAllowedRegion`): recorded sha256 `9005ac46571d0b3b728b37a7edc5ff2e45b201979e92861021251da371910446` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FrontierPrAllowedRegion`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FrontierPrAllowedRegion.allowed_and_forbidden_witnesses_with_6j_squares` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierPrAllowedRegion.allowed_and_forbidden_witnesses_with_6j_squares` |
| `FrontierPrAllowedRegion.ponzano_regge_allowed_forbidden_classification_le8` | yes | yes | yes | none | `#print axioms FrontierPrAllowedRegion.ponzano_regge_allowed_forbidden_classification_le8` |

- counts toward the grade: yes

### Lean: `lean4/ReggePachnerWdw.lean`

- file: [lean4/ReggePachnerWdw.lean](../../../lean4/ReggePachnerWdw.lean)
- sha256 (`bytes`): `b641629a6da8c48d0a0f0018b087cd5fef52f9f8e5ad8f7a24e734134a5fb798`
- cited in: node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_loop_quantum_gravity.json](../../../dag/research/lean_replay_campaign_loop_quantum_gravity.json) (module `ReggePachnerWdw`): recorded sha256 `b641629a6da8c48d0a0f0018b087cd5fef52f9f8e5ad8f7a24e734134a5fb798` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build ReggePachnerWdw`
- counts toward the grade: yes

### Documents and data: `dag/derivations/33_loop_quantum_gravity/tfq_2309_lqg_pr_allowed_region_target.md`

- file: [dag/derivations/33_loop_quantum_gravity/tfq_2309_lqg_pr_allowed_region_target.md](../../../dag/derivations/33_loop_quantum_gravity/tfq_2309_lqg_pr_allowed_region_target.md)
- sha256 (`lf-normalised`): `f2602c81af7a79f744f9fd78eee7e85771ea68bdeed0458b792790b5a3558b3b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2309
- counts toward the grade: no

### Documents and data: `dag/research/frontier_targets_lean_replay.json`

- file: [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json)
- sha256 (`lf-normalised`): `1c66aabd3bb726fafcd0238c259644d6f79dd304178d171a75ea36d6522bd2cc`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:math-ph/9812013`

## Routes

Incoming (1):

- `FRO-R-LQG-PR-ALLOWED-REGION-TARGET` `DERIVED_LEAN`: [LQG-6J-EXACT-AND-PENTAGON-TARGET](LQG-6J-EXACT-AND-PENTAGON-TARGET.md) (PROVED_LEAN), [LQG-PR-ASYMPTOTICS-IMPORT](LQG-PR-ASYMPTOTICS-IMPORT.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

