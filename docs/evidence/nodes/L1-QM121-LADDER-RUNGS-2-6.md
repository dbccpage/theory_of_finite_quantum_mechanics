# L1-QM121-LADDER-RUNGS-2-6

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Ladder over QM_020 rung 1: diagonal density (2), channels as stochastic kernels (3), path-sum as matrix power (4), superposition phase content as quotient fiber U(1)^(|E_w|-1) (5), interference as non-l1 cross term (6). The ceiling of the ladder is the C/U(1) carrier, Born-quadratic uniqueness (Gleason) and the continuum / unitarity limit, all imported.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 1 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.
- `broken_reference`: path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py. A cited in-repo path or symbol cannot be found in this checkout.

## Imported structure

- C / U(1) carrier: assumption
- Gleason: assumption
- continuum / unitarity: assumption

## Bottleneck

Lean checks fixed numerical instances of rungs 2 to 6 (one diagonal expectation, one diagonal matrix product, the Hadamard square, one cross-term inequality). The rungs as general statements are not in Lean; the ceiling imports stay imported.

## Source status

QM_121 rungs 2-6: rung 2 PROVED prose (ENC-1126); rungs 1 and 6 'MECHANIZED reuse'; C10 C/U(1) carrier IMPORTED / OPEN (OB-U1); C9 Born-quadratic IMPORTED (OB-BORN)

## Review

- PFP review: [dag/results/L1-QM121-LADDER-RUNGS-2-6/reviews/20261020_born_boundary_audit/delivery_review_result.json](../../../dag/results/L1-QM121-LADDER-RUNGS-2-6/reviews/20261020_born_boundary_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Complete retained stochastic path tables and matrix-power equality, diagonal action and exact two-phase readout, with finite composition algebra in Lean.
  - does not support: Prove arbitrary-rung/source representation refinements and discharge the admitted carrier, Born uniqueness and continuous/unitary limits.
  - next test: Prove arbitrary-rung/source representation refinements and discharge the admitted carrier, Born uniqueness and continuous/unitary limits.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_thm7_and_qm121_ladder_rungs_2_to_6_separation` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_thm7_and_qm121_ladder_rungs_2_to_6_separation` |
| `QuantumMechanics.DerivationDagQMClosure.qm121_ladder_rungs_2_to_6_certificate` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm121_ladder_rungs_2_to_6_certificate` |

- counts toward the grade: yes

### Rust: `code/rust/src/qm/campaigns/density_matrix.rs`

- file: [code/rust/src/qm/campaigns/density_matrix.rs](../../../code/rust/src/qm/campaigns/density_matrix.rs)
- sha256 (`bytes`): `847f1fc1386da04441491f4862781239c7b07e7886d169a2a9fac8b7eb2cff8e`
- cited in: record TFQ-0309
- note: no test is cited for this symbol; its crate is theory_of_finite_qm
- counts toward the grade: yes

### Python: `code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py`

- file: `code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py`
- resolution: `missing` (not found in this checkout)
- cited in: record TFQ-0309
- counts toward the grade: no

### Documents and data: `dag/derivations/09_finite_hilbert/tfq_0309_ingredient_ladder_stops_before_the_imported_ceiling.md`

- file: [dag/derivations/09_finite_hilbert/tfq_0309_ingredient_ladder_stops_before_the_imported_ceiling.md](../../../dag/derivations/09_finite_hilbert/tfq_0309_ingredient_ladder_stops_before_the_imported_ceiling.md)
- sha256 (`lf-normalised`): `f08c3c792bf8ed2c68ba7fba3caba50b94b7aa31a11d0b61aed5bcd0363ddc38`
- generated view: listed, not counted
- cited in: record TFQ-0309
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_l1_to_l2_bridges_and_ladder_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche16_master_177_node_172_route_dag_completeness_and_operad_audit_witness`
- `external:sha256:91902ad0b3daed220b6cb851493f83faf8fe90131ef5b3e5e3260cc721968c14`
- `external:sha256:98fc999af806971f93da6244c85ae5f6a48fd4de46a9f54fa9754dedc5f12918:168`
- `external:sha256:be048d5e98615cff70b3cdc1ebaa78a56395d67d55ca655cbb41494e307cde65`
- `external:sha256:ee8e39c10a0f428eec9ee784dadd1e19d791ccd38d73ad173f62abcdd1bdb3b6`

## Absences recorded by the TFQ records

- TFQ-0309 rust: no local rust twin located for external:sha256:a2c0d7450948662c89ffb80f0ebcfa02f1f013179a207d3d24db3421e81e84c6

## Routes

Incoming (1):

- `L1-R-LADDER` `COMPUTED`: [L1-QM020-THM1-DIRECT-NORMALIZATION](L1-QM020-THM1-DIRECT-NORMALIZATION.md) (PROVED_LEAN), [L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY](L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY.md) (PROVED_PROSE), [L1-QM020-THM7-REPRESENTATION-CAPACITY](L1-QM020-THM7-REPRESENTATION-CAPACITY.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

