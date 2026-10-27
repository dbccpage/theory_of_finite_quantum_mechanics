# L1-QM020-THM2B-MINKOWSKI

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Strict l^p (p\>1) subadditivity for two nonzero vectors with disjoint supports follows from standard Minkowski / strict convexity. The paper cites it as standard analysis.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 9
- distinct cited Lean declarations covered by a current replay receipt: 9
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- real analysis (Minkowski, strict convexity): assumption

## Bottleneck

Real exponent p\>1, a Minkowski comparison on real vectors, strict convexity, roots, and transport past this Nat square, cubic, and one disjoint pair stay outside the checked slice. A zero input is an equality case of the square expansion.

## Source status

Thm 2b STANDARD / imported real analysis; audit: imported

## Review

- PFP review: [dag/research/pr_388_current_scope_review.json](../../../dag/research/pr_388_current_scope_review.json); file present and sha256 matches the node's record: yes; verdict `scoped_natural_arithmetic_reviewed`; scope effect `caveat_added`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: Reviewed scope: Nat values a and b satisfy (a + b) * (a + b) = a * a + b * b + 2 * (a * b). When both are positive, 2 * (a * b) \> 0 and a * a + b * b \< (a + b) * (a + b). When the left input is 0, 2 * (0 * b) = 0 and (0 + b) * (0 + b) = b * b. When the right input is 0, 2 * (a * 0) = 0 and (a + 0) * (a + 0) = a * a. Nat values a and b satisfy (a + b) * (a + b) * (a + b) = a * a * a + b * b * b + 3 * a * b * (a + b). A disjoint Nat pair satisfies (x + 0) * (x + 0) + (0 + y) * (0 + y) = x * x + y * y.
  - does not support: Real exponent p\>1, a Minkowski comparison on real vectors, strict convexity, roots, and transport past this Nat square, cubic, and one disjoint pair stay outside the standing text. A zero input is an equality case of the square expansion.
  - next test: Retain the real-analysis import until the original real-p statement is mechanized.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BornRedundancy.lean`

- file: [lean4/BornRedundancy.lean](../../../lean4/BornRedundancy.lean)
- sha256 (`bytes`): `8868c1ceab52414128cac38a298bd28ca9cfc723613053c01ee90f23933b830b`
- cited in: record TFQ-0291 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `BornRedundancy`): recorded sha256 `8868c1ceab52414128cac38a298bd28ca9cfc723613053c01ee90f23933b830b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornRedundancy`
- counts toward the grade: no

### Lean: `lean4/L1MinkowskiSquareExpansion.lean`

- file: [lean4/L1MinkowskiSquareExpansion.lean](../../../lean4/L1MinkowskiSquareExpansion.lean)
- sha256 (`bytes`): `b273845ba9ac549d0874c53cf6cf526446cebbd24624f6bba6a37d98697e65ed`
- cited in: node.lean, receipt dag/research/campaign_l1-qm020-thm2b-minkowski_lean_replay.json (L1MinkowskiSquareExpansion), receipt dag/research/pr_388_round2_replay.json (L1MinkowskiSquareExpansion)
- replay: `verified`
  - receipt [dag/research/campaign_l1-qm020-thm2b-minkowski_lean_replay.json](../../../dag/research/campaign_l1-qm020-thm2b-minkowski_lean_replay.json) (module `L1MinkowskiSquareExpansion`): recorded sha256 `b273845ba9ac549d0874c53cf6cf526446cebbd24624f6bba6a37d98697e65ed` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/pr_388_round2_replay.json](../../../dag/research/pr_388_round2_replay.json) (module `L1MinkowskiSquareExpansion`): recorded sha256 `b273845ba9ac549d0874c53cf6cf526446cebbd24624f6bba6a37d98697e65ed` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build L1MinkowskiSquareExpansion`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `L1MinkowskiSquareExpansion.cross_positive` | yes | yes | yes | Quot.sound, propext | `#print axioms L1MinkowskiSquareExpansion.cross_positive` |
| `L1MinkowskiSquareExpansion.cross_zero_left` | yes | yes | yes | Quot.sound, propext | `#print axioms L1MinkowskiSquareExpansion.cross_zero_left` |
| `L1MinkowskiSquareExpansion.cross_zero_right` | yes | yes | yes | Quot.sound, propext | `#print axioms L1MinkowskiSquareExpansion.cross_zero_right` |
| `L1MinkowskiSquareExpansion.cubic_sum` | yes | yes | yes | Quot.sound, propext | `#print axioms L1MinkowskiSquareExpansion.cubic_sum` |
| `L1MinkowskiSquareExpansion.disjoint_pair_squares` | yes | yes | yes | none | `#print axioms L1MinkowskiSquareExpansion.disjoint_pair_squares` |
| `L1MinkowskiSquareExpansion.square_eq_left_zero` | yes | yes | yes | Quot.sound, propext | `#print axioms L1MinkowskiSquareExpansion.square_eq_left_zero` |
| `L1MinkowskiSquareExpansion.square_eq_right_zero` | yes | yes | yes | Quot.sound, propext | `#print axioms L1MinkowskiSquareExpansion.square_eq_right_zero` |
| `L1MinkowskiSquareExpansion.square_expansion` | yes | yes | yes | Quot.sound, propext | `#print axioms L1MinkowskiSquareExpansion.square_expansion` |
| `L1MinkowskiSquareExpansion.square_strict` | yes | yes | yes | Quot.sound, propext | `#print axioms L1MinkowskiSquareExpansion.square_strict` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_0291_disjoint_aggregation_and_the_real_p_1_import.md`

- file: [dag/derivations/08_l1_to_l2/tfq_0291_disjoint_aggregation_and_the_real_p_1_import.md](../../../dag/derivations/08_l1_to_l2/tfq_0291_disjoint_aggregation_and_the_real_p_1_import.md)
- sha256 (`lf-normalised`): `72aa61a0c03b52b231249dc1bd6f198ed2e0c9d3434a2e08a7840f2f2dcb30c9`
- generated view: listed, not counted
- cited in: record TFQ-0291 (shared)
- counts toward the grade: no

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/claims/claim_ledger.yaml`

- file: [sources/atlas/papers/finite_quantum_mechanics/claims/claim_ledger.yaml](../../../sources/atlas/papers/finite_quantum_mechanics/claims/claim_ledger.yaml)
- sha256 (`lf-normalised`): `0d891e04d6b8ff46e95360a919f7c2a64074a2d4f9732a2e481f868e41c385a7`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche10_chsh_tsirelson_pr_box_tier3_uniqueness_edgewise_l1_and_import_boundaries_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`
- `external:sha256:8534bf2948b65ab72605a33c219105f09458247c00aa57acc8beb275df568d27:235`

## Routes

Incoming (1):

- `L1-R-THM2B` `CONDITIONAL_ON_IMPORT`: [L1-QM020-THM2A-L1-ADDITIVITY-DEFECT](L1-QM020-THM2A-L1-ADDITIVITY-DEFECT.md) (PROVED_LEAN)

Outgoing (0):

