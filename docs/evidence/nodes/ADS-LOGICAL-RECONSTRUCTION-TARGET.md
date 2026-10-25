# ADS-LOGICAL-RECONSTRUCTION-TARGET

Stage: [ADS_CFT](../stages/ADS_CFT.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Formalized finite statement. For the \[\[5,1,3\]\] code, each of the ten 3-qubit subsets T of physical qubits supports a representative of each of the three nontrivial logical classes (the cosets of the stabilizer by XXXXX, ZZZZZ and YYYYY, the product class), and no 2-qubit subset supports a representative of any of them. Equivalent statement also checked in Lean 4: all 105 non-identity Pauli errors of weight 1 or 2 anticommute with a stabilizer generator, so none lies in the normalizer and erasure of any two qubits is correctable (the Knill-Laflamme condition). All operators are Pauli operators modulo phase. This is the smallest exact instance of the subregion-reconstruction picture of bulk operators.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Checked in Lean 4 over the 16-element stabilizer, its three logical cosets, all 10 triples, all 10 pairs and all 105 low-weight Pauli errors. The identification with bulk operator reconstruction in AdS/CFT is the imported picture of the source.

## Source status

Recomputed in Python over the 64-element normalizer on 2026-10-22 (unique representative per logical class on each of the 10 triples, zero on each of the 10 pairs). Lean: checked in Lean 4.35.0 via lake build FrontierLogicalReconstruction (library FrontierTargets in lean4/lakefile.lean) in the form recorded in the statement; replay receipt in dag/research/frontier_targets_lean_replay.json; per-node review in dag/research/frontier_targets_lean_review.md.

## Review

- Frontier Lean review: [dag/research/frontier_targets_lean_review.md](../../../dag/research/frontier_targets_lean_review.md); verdict `FULL`; qualifies for E4: yes.
  - theorems that discharge the node, as listed by the review: `every_triple_reconstructs_all_three_logical_classes`, `no_pair_supports_any_nontrivial_logical_class`, `two_qubit_erasure_detectable_all_105`
  - the review's reason for its verdict is in the row of this node in the review file

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/FrontierLogicalReconstruction.lean`

- file: [lean4/FrontierLogicalReconstruction.lean](../../../lean4/FrontierLogicalReconstruction.lean)
- sha256 (`bytes`): `d6f5ed40800a8c76ebdd20cd96d7bafedcbd379de3b7abdd9a8821b744e9f76c`
- cited in: node.lean, node.source, receipt dag/research/frontier_targets_lean_replay.json (FrontierLogicalReconstruction)
- replay: `verified`
  - receipt [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json) (module `FrontierLogicalReconstruction`): recorded sha256 `d6f5ed40800a8c76ebdd20cd96d7bafedcbd379de3b7abdd9a8821b744e9f76c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build FrontierLogicalReconstruction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FrontierLogicalReconstruction.every_triple_reconstructs_all_three_logical_classes` | yes | yes | yes | propext | `#print axioms FrontierLogicalReconstruction.every_triple_reconstructs_all_three_logical_classes` |
| `FrontierLogicalReconstruction.no_pair_supports_any_nontrivial_logical_class` | yes | yes | yes | propext | `#print axioms FrontierLogicalReconstruction.no_pair_supports_any_nontrivial_logical_class` |
| `FrontierLogicalReconstruction.two_qubit_erasure_detectable_all_105` | yes | yes | yes | propext | `#print axioms FrontierLogicalReconstruction.two_qubit_erasure_detectable_all_105` |

- counts toward the grade: yes

### Lean: `lean4/H036ThreeQubitCodeSyndromeRecovery.lean`

- file: [lean4/H036ThreeQubitCodeSyndromeRecovery.lean](../../../lean4/H036ThreeQubitCodeSyndromeRecovery.lean)
- sha256 (`bytes`): `b15c930d114e54c9c99010142e46019afa0af0d2cfa4507c9634cc5d00a81ca7`
- cited in: node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_ads_cft.json](../../../dag/research/lean_replay_campaign_ads_cft.json) (module `H036ThreeQubitCodeSyndromeRecovery`): recorded sha256 `b15c930d114e54c9c99010142e46019afa0af0d2cfa4507c9634cc5d00a81ca7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build H036ThreeQubitCodeSyndromeRecovery`
- counts toward the grade: yes

### Documents and data: `dag/derivations/32_ads_cft/tfq_2210_ads_logical_reconstruction_target.md`

- file: [dag/derivations/32_ads_cft/tfq_2210_ads_logical_reconstruction_target.md](../../../dag/derivations/32_ads_cft/tfq_2210_ads_logical_reconstruction_target.md)
- sha256 (`lf-normalised`): `e9c33cc4815e3b03edd53b36665b9df35041c470bd468d51d7513bfb683cfa5f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2210
- counts toward the grade: no

### Documents and data: `dag/research/frontier_targets_lean_replay.json`

- file: [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json)
- sha256 (`lf-normalised`): `1c66aabd3bb726fafcd0238c259644d6f79dd304178d171a75ea36d6522bd2cc`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:1411.7041`
- `external:arXiv:quant-ph/9602019`

## Routes

Incoming (1):

- `FRO-R-ADS-LOGICAL-RECONSTRUCTION-TARGET` `DERIVED_LEAN`: [ADS-FIVE-QUBIT-PERFECT-TENSOR-TARGET](ADS-FIVE-QUBIT-PERFECT-TENSOR-TARGET.md) (PROVED_LEAN), [ADS-ADH-2015-SOURCE](ADS-ADH-2015-SOURCE.md) (SOURCE_RECORD)

Outgoing (0):

