# ADS-FIVE-QUBIT-PERFECT-TENSOR-TARGET

Stage: [ADS_CFT](../stages/ADS_CFT.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Formalized finite statement. The \[\[5,1,3\]\] code of Laflamme, Miquel, Paz and Zurek has stabilizer generators XZZXI, IXZZX, XIXZZ, ZXIXZ and logical operators XXXXX and ZZZZZ. Its Choi state is the six-qubit stabilizer state with generators g tensor I (four of them), XXXXX tensor X and ZZZZZ tensor Z. Checked in Lean 4 on Pauli operators modulo phase (GF(2) symplectic vectors): the six generators pairwise commute and generate a group of 64 distinct elements, with weight distribution 1 element of weight 0, 45 of weight 4 and 18 of weight 6 (the hexacode six-qubit state), so every non-identity element has weight at least 4, which is the perfect-tensor condition (every bipartition with at most three legs on one side has a maximally mixed marginal); for all twenty 3|3 bipartitions the stabilizer subgroup supported on one side is trivial, so the entropy is 3 bits by the stabilizer formula S(A) = |A| - log2 |G_A|; and in the five-qubit code the normalizer of the 16-element stabilizer has order 64 and its 48 elements outside the stabilizer (the nontrivial logical operators, modulo phase) have minimum weight 3. The reading of weights and local stabilizer subgroups as marginals and entropies is the standard stabilizer-formalism dictionary and is not formalised on density matrices.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Checked in Lean 4 by exhaustive GF(2) symplectic enumeration over the 64-element stabilizer group, the 20 bipartitions and the 1024-element five-qubit Pauli group. A finite stabilizer enumeration is not a statement about AdS/CFT.

## Source status

Source generators audited against arXiv:1503.06237 Appendix A.1 eqs. (A1)-(A7) pp. 24-25, and weight enumerator 1 + 45 z^4 + 18 z^6, all twenty 3|3 bipartition entropies (3 bits) and minimum logical weight 3 recomputed in Python on 2026-10-22. Lean: checked in Lean 4.35.0 via lake build FrontierFiveQubitPerfectTensor (library FrontierTargets in lean4/lakefile.lean) in the form recorded in the statement; replay receipt in dag/research/frontier_targets_lean_replay.json; per-node review in dag/research/frontier_targets_lean_review.md.

## Review

- Frontier Lean review: [dag/research/frontier_targets_lean_review.md](../../../dag/research/frontier_targets_lean_review.md); verdict `FULL`; qualifies for E4: yes.
  - theorems that discharge the node, as listed by the review: `choi_generators_commute_and_group_order_64`, `choi_perfect_tensor_weight_distribution`, `all_twenty_3_3_bipartitions_maximal_entropy`, `five_qubit_logical_minimum_weight_3`
  - the review's reason for its verdict is in the row of this node in the review file

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/FrontierFiveQubitPerfectTensor.lean`

- file: [lean4/FrontierFiveQubitPerfectTensor.lean](../../../lean4/FrontierFiveQubitPerfectTensor.lean)
- sha256 (`bytes`): `129bfdeb6503169d4a5cfc277cf71628909dd4abef168722b2f79f60567b152a`
- cited in: node.lean, node.source, receipt dag/research/frontier_targets_lean_replay.json (FrontierFiveQubitPerfectTensor)
- replay: `verified`
  - receipt [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json) (module `FrontierFiveQubitPerfectTensor`): recorded sha256 `129bfdeb6503169d4a5cfc277cf71628909dd4abef168722b2f79f60567b152a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build FrontierFiveQubitPerfectTensor`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FrontierFiveQubitPerfectTensor.all_twenty_3_3_bipartitions_maximal_entropy` | yes | yes | yes | propext | `#print axioms FrontierFiveQubitPerfectTensor.all_twenty_3_3_bipartitions_maximal_entropy` |
| `FrontierFiveQubitPerfectTensor.choi_generators_commute_and_group_order_64` | yes | yes | yes | propext | `#print axioms FrontierFiveQubitPerfectTensor.choi_generators_commute_and_group_order_64` |
| `FrontierFiveQubitPerfectTensor.choi_perfect_tensor_weight_distribution` | yes | yes | yes | propext | `#print axioms FrontierFiveQubitPerfectTensor.choi_perfect_tensor_weight_distribution` |
| `FrontierFiveQubitPerfectTensor.five_qubit_logical_minimum_weight_3` | yes | yes | yes | propext | `#print axioms FrontierFiveQubitPerfectTensor.five_qubit_logical_minimum_weight_3` |
- counts toward the grade: yes

### Lean: `lean4/H036ThreeQubitCodeSyndromeRecovery.lean`

- file: [lean4/H036ThreeQubitCodeSyndromeRecovery.lean](../../../lean4/H036ThreeQubitCodeSyndromeRecovery.lean)
- sha256 (`bytes`): `b15c930d114e54c9c99010142e46019afa0af0d2cfa4507c9634cc5d00a81ca7`
- cited in: node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_ads_cft.json](../../../dag/research/lean_replay_campaign_ads_cft.json) (module `H036ThreeQubitCodeSyndromeRecovery`): recorded sha256 `b15c930d114e54c9c99010142e46019afa0af0d2cfa4507c9634cc5d00a81ca7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build H036ThreeQubitCodeSyndromeRecovery`
- counts toward the grade: yes

### Lean: `lean4/H042ShorNineQubitCode.lean`

- file: [lean4/H042ShorNineQubitCode.lean](../../../lean4/H042ShorNineQubitCode.lean)
- sha256 (`bytes`): `6bb233631905c18bbef63f8fa4a9b3b012a65d33d14c187e3e7f8b9fe2df82c9`
- cited in: node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_ads_cft.json](../../../dag/research/lean_replay_campaign_ads_cft.json) (module `H042ShorNineQubitCode`): recorded sha256 `6bb233631905c18bbef63f8fa4a9b3b012a65d33d14c187e3e7f8b9fe2df82c9` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build H042ShorNineQubitCode`
- counts toward the grade: yes

### Lean: `lean4/H044SurfaceCodeToricTopology.lean`

- file: [lean4/H044SurfaceCodeToricTopology.lean](../../../lean4/H044SurfaceCodeToricTopology.lean)
- sha256 (`bytes`): `fb7dabdab6050799ef04a17f7ca0892c4cab39b4781db08d9445a9496915e15b`
- cited in: node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_ads_cft.json](../../../dag/research/lean_replay_campaign_ads_cft.json) (module `H044SurfaceCodeToricTopology`): recorded sha256 `fb7dabdab6050799ef04a17f7ca0892c4cab39b4781db08d9445a9496915e15b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build H044SurfaceCodeToricTopology`
- counts toward the grade: yes

### Documents and data: `dag/derivations/32_ads_cft/tfq_2208_ads_five_qubit_perfect_tensor_target.md`

- file: [dag/derivations/32_ads_cft/tfq_2208_ads_five_qubit_perfect_tensor_target.md](../../../dag/derivations/32_ads_cft/tfq_2208_ads_five_qubit_perfect_tensor_target.md)
- sha256 (`lf-normalised`): `7dd65d1a5167fbb095d20a0828ad13641431a3fc6c88ff9cc8b3cf58343c3b0d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2208
- counts toward the grade: no

### Documents and data: `dag/research/frontier_targets_lean_replay.json`

- file: [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json)
- sha256 (`lf-normalised`): `1c66aabd3bb726fafcd0238c259644d6f79dd304178d171a75ea36d6522bd2cc`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:1503.06237`
- `external:arXiv:quant-ph/9602019`

## Routes

Incoming (1):

- `FRO-R-ADS-FIVE-QUBIT-PERFECT-TENSOR-TARGET` `DERIVED_LEAN`: [ADS-HAPPY-2015-SOURCE](ADS-HAPPY-2015-SOURCE.md) (SOURCE_RECORD)

Outgoing (2):

- `FRO-R-ADS-HAPPY-ENTROPY-MINCUT-TARGET` `DERIVED_LEAN`: [ADS-HAPPY-ENTROPY-MINCUT-TARGET](ADS-HAPPY-ENTROPY-MINCUT-TARGET.md) (PROVED_LEAN)
- `FRO-R-ADS-LOGICAL-RECONSTRUCTION-TARGET` `DERIVED_LEAN`: [ADS-LOGICAL-RECONSTRUCTION-TARGET](ADS-LOGICAL-RECONSTRUCTION-TARGET.md) (PROVED_LEAN)
