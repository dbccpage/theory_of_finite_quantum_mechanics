# L1-QM020-THM3-ROW-SPARSITY

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A linear map that is descent-compatible (respects the l1 weight descent on a chosen sector basis, with phase rotation freedom) is monomial, i.e. strictly row-sparse. Lean covers the 2x2 real case.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- linear representation of sectors: assumption
- unit phase rotations: assumption

## Bottleneck

Lean states the 2x2 integer case: a 2x2 matrix is descent-compatible iff each row has at most one nonzero entry (descent_compatible_iff_row_sparse). The n x n statement is not in Lean, and 'monomial' (invertible) needs an injectivity or column condition the statement omits.

## Source status

General-n row-sparsity characterization mechanized in DerivationDagQMClosure.lean

## Review

- PFP review: [dag/results/L1-QM020-THM3-ROW-SPARSITY/reviews/20261020_born_boundary_audit/delivery_review_result.json](../../../dag/results/L1-QM020-THM3-ROW-SPARSITY/reviews/20261020_born_boundary_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Exact phase-sign readouts, row sparsity, determinant, monomial and rank distinctions; general row interference and a singular sparse control in Lean.
  - does not support: Prove the full representation refinement and add injectivity/column conditions before claiming monomial invertibility. No scalar label licenses the stronger claim.
  - next test: Prove the full representation refinement and add injectivity/column conditions before claiming monomial invertibility. No scalar label licenses the stronger claim.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BornRedundancy.lean`

- file: [lean4/BornRedundancy.lean](../../../lean4/BornRedundancy.lean)
- sha256 (`bytes`): `8868c1ceab52414128cac38a298bd28ca9cfc723613053c01ee90f23933b830b`
- cited in: node.lean, record TFQ-0300 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `BornRedundancy`): recorded sha256 `8868c1ceab52414128cac38a298bd28ca9cfc723613053c01ee90f23933b830b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornRedundancy`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `descent_compatible_iff_row_sparse` | yes | yes | yes | Quot.sound, propext | `#print axioms descent_compatible_iff_row_sparse` |
| `row_sparse_implies_descent_compatible` | yes | yes | yes | propext | `#print axioms row_sparse_implies_descent_compatible` |

- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_phase_blind_descent_general_n_row_sparsity` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_phase_blind_descent_general_n_row_sparsity` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_0300_descent_compatible_maps_stay_row_sparse.md`

- file: [dag/derivations/08_l1_to_l2/tfq_0300_descent_compatible_maps_stay_row_sparse.md](../../../dag/derivations/08_l1_to_l2/tfq_0300_descent_compatible_maps_stay_row_sparse.md)
- sha256 (`lf-normalised`): `2cc468ab3c0ecf70660ddb84a55c40c691a49519ee14585e283fdbc50cde7e38`
- generated view: listed, not counted
- cited in: record TFQ-0300 (shared)
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`
- `external:sha256:8534bf2948b65ab72605a33c219105f09458247c00aa57acc8beb275df568d27:408`
- `external:sha256:a2c0d7450948662c89ffb80f0ebcfa02f1f013179a207d3d24db3421e81e84c6::classify_descent`

## Absences recorded by the TFQ records

- TFQ-0300 rust: no local rust twin located for external:sha256:a2c0d7450948662c89ffb80f0ebcfa02f1f013179a207d3d24db3421e81e84c6

## Routes

Incoming (1):

- `L1-R-THM3` `COMPUTED`: [L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED](L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED.md) (CONDITIONAL), [L1-IMP-COMPLEX-FIELD](L1-IMP-COMPLEX-FIELD.md) (CONDITIONAL), [L1-IMP-U1-PHASES](L1-IMP-U1-PHASES.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

