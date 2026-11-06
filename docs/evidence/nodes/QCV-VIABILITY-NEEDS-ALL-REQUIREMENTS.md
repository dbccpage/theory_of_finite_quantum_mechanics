# QCV-VIABILITY-NEEDS-ALL-REQUIREMENTS

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For g \< 1, kappa \> 0 and c(k) \>= 0, the backlog is bounded and some positive physical rate has p(k) tending to zero iff r \>= lam/((1-g)*kappa) and some M \> 0 has amp(k) \<= M^(2^k); with no supply the backlog is unbounded, with g \>= 1 it is unbounded for every supply, and a tight profile p(k+1) \>= c(k)*p(k)^2 with c(k) \>= a*b^(2^k), b \> 1, p(0) \> 0 does not tend to zero.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- distinct cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

A statement about the declared model: a failed requirement shows the certificate is empty, not that a physical machine fails.

## Source status

dag/derivations/29_computation/quantum_computation_self_obstruction.md record QCV-Q5B claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/QcSelfObstruction.lean`

- file: [lean4/QcSelfObstruction.lean](../../../lean4/QcSelfObstruction.lean)
- sha256 (`bytes`): `be7f59c979614e015b49da0d9b4e233e5166f39b91a0c6de61d3e51659209a83`
- cited in: node.lean, record TFQ-1325
- replay: `verified`
  - receipt [evidence/lean_receipts/lean_replay_campaign_computation.json](../../../evidence/lean_receipts/lean_replay_campaign_computation.json) (module `QcSelfObstruction`): recorded sha256 `be7f59c979614e015b49da0d9b4e233e5166f39b91a0c6de61d3e51659209a83` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build QcSelfObstruction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `level_error_ge` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms level_error_ge` |
| `model_viable_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms model_viable_iff` |
| `not_viable_dexp_profile` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms not_viable_dexp_profile` |
| `not_viable_unit_gain` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms not_viable_unit_gain` |
| `not_viable_without_supply` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms not_viable_without_supply` |

- counts toward the grade: yes

### Rust: `code/rust/src/qm/campaigns/qc_self_obstruction.rs`

- file: [code/rust/src/qm/campaigns/qc_self_obstruction.rs](../../../code/rust/src/qm/campaigns/qc_self_obstruction.rs)
- sha256 (`bytes`): `7ec8808a14754317eca2df6528a90985a6cbbaaddbf17c611cd236cd45eef4e3`
- cited in: node.rust, record TFQ-1325

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `viability_report` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/src/qm/qc_self_obstruction.py`

- file: [code/python/src/qm/qc_self_obstruction.py](../../../code/python/src/qm/qc_self_obstruction.py)
- sha256 (`bytes`): `bfc41c6def8f655c61bde3475189a299d276bae04e1f8c75f09f1d35a6d89d66`
- cited in: record TFQ-1325

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `viability_report` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/quantum_computation_self_obstruction.md`

- file: [dag/derivations/29_computation/quantum_computation_self_obstruction.md](../../../dag/derivations/29_computation/quantum_computation_self_obstruction.md)
- sha256 (`lf-normalised`): `303d0562ed0666748c50b6b844ae4c57a8e4bd4bef15f817d7f4622a68783ccd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1325_qcv_viability_needs_all_requirements.md`

- file: [dag/derivations/29_computation/tfq_1325_qcv_viability_needs_all_requirements.md](../../../dag/derivations/29_computation/tfq_1325_qcv_viability_needs_all_requirements.md)
- sha256 (`lf-normalised`): `6f38d3aa990e7be567b9ad798cbfdb2dca723c42a2bb00eba7186aff9b1e3c8d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1325
- counts toward the grade: no

### Documents and data: `evidence/axiom_reports/quantum_computation_self_obstruction_axioms.txt`

- file: [evidence/axiom_reports/quantum_computation_self_obstruction_axioms.txt](../../../evidence/axiom_reports/quantum_computation_self_obstruction_axioms.txt)
- sha256 (`lf-normalised`): `b4c803ee2b1a4fe8af1d9d92a351fb11c61d2791bea01a5b7cd3dd7c1623af81`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-QCV-VIABILITY-NEEDS-ALL-REQUIREMENTS` `DERIVED_LEAN`: [QCV-CONDITIONAL-VIABILITY-CERTIFICATE](QCV-CONDITIONAL-VIABILITY-CERTIFICATE.md) (CONDITIONAL)

Outgoing (0):

