# L1-QM003-C17-COMPOSABLE-FACTORIZATION

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Diagonal Markov-composable channels factor through the residual density carrier (qm003_c17_diagonal_composable_factorization), while Hadamard off-diagonal coherence separates matrix composition from diagonal multiplication.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

None recorded.

## Bottleneck

Lean states the 2x2 case: products of diagonal 2x2 integer matrices are diagonal with entrywise products, and the Hadamard matrix gives an explicit off-diagonal counterexample. General dimension and general Markov kernels are not in Lean.

## Source status

QM_003 C17 diagonal composable factorization and off-diagonal coherence boundary mechanized in DerivationDagQMClosure.lean

## Review

- PFP review: [dag/results/L1-QM003-C17-COMPOSABLE-FACTORIZATION/reviews/20261020_born_boundary_audit/delivery_review_result.json](../../../dag/results/L1-QM003-C17-COMPOSABLE-FACTORIZATION/reviews/20261020_born_boundary_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Exact stochastic composition/action equality and diagonal density presentation, plus scalar matrix multiplication identities and the Hadamard defect in Lean.
  - does not support: Prove source residual-density factorization on its full carrier and channel class. The source diagonal multiplication anchor alone does not prove it.
  - next test: Prove source residual-density factorization on its full carrier and channel class. The source diagonal multiplication anchor alone does not prove it.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1005
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.qm003_c17_diagonal_composable_factorization` | yes | yes | yes | propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm003_c17_diagonal_composable_factorization` |
| `QuantumMechanics.DerivationDagQMClosure.qm003_c17_off_diagonal_obstruction_to_diagonal_factorization` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm003_c17_off_diagonal_obstruction_to_diagonal_factorization` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1005_l1_qm003_c17_composable_factorization.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1005_l1_qm003_c17_composable_factorization.md](../../../dag/derivations/08_l1_to_l2/tfq_1005_l1_qm003_c17_composable_factorization.md)
- sha256 (`lf-normalised`): `b1690f1a31fedcbe26aeaafd4aae8e802ad7b2ba7ae930cad7f27ff414593192`
- generated view: listed, not counted
- cited in: record TFQ-1005
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_l1_to_l2_bridges_and_ladder_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- `external:sha256:e3c1fb4d47cc71d77c93d54d3e25ddefd4cfd203d33b327084ad5d0426656e6e`

## Routes

Incoming (1):

- `L1-R-QM003-C17-FACTORIZATION` `COMPUTED`: [L1-DENSITY-LIFT-SIGNED-SQRT-PUB009](L1-DENSITY-LIFT-SIGNED-SQRT-PUB009.md) (OPEN)

Outgoing (0):

