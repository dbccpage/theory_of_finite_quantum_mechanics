# QCV-REPAIR-NEEDED-BUT-COSTLY

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The union-bound recurrence p(k+1) = a*p(k) with a \>= 1 and p(0) \> 0 does not tend to zero; for 2 \<= a \<= b fault locations the certified threshold 1/pairCount(b) is at most 1/pairCount(a).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 8
- cited Lean declaration references covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The location counts are declared; nothing here says how many repair locations a physical code needs.

## Source status

dag/research/quantum_computation_self_obstruction.md record QCV-Q1C claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/QcConcatenation.lean`

- file: [lean4/QcConcatenation.lean](../../../lean4/QcConcatenation.lean)
- sha256 (`bytes`): `5fea043a891ddf38414c7d169710a95f54e3f28b7b94fc11bd96ecef69541c63`
- cited in: node.lean, record TFQ-1317
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `QcConcatenation`): recorded sha256 `5fea043a891ddf38414c7d169710a95f54e3f28b7b94fc11bd96ecef69541c63` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build QcConcatenation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `lin_closed` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms lin_closed` |
| `lin_not_goesToZero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms lin_not_goesToZero` |
| `pairCount_mono` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms pairCount_mono` |
| `threshold_decreases_with_repair` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms threshold_decreases_with_repair` |

- counts toward the grade: yes

### Rust: `code/rust/src/qm/campaigns/qc_self_obstruction.rs`

- file: [code/rust/src/qm/campaigns/qc_self_obstruction.rs](../../../code/rust/src/qm/campaigns/qc_self_obstruction.rs)
- sha256 (`bytes`): `7ec8808a14754317eca2df6528a90985a6cbbaaddbf17c611cd236cd45eef4e3`
- cited in: node.rust, record TFQ-1317

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `linear_level` (rust_symbol) | yes | yes | yes | - | - |
| `pair_count` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/src/qm/qc_self_obstruction.py`

- file: [code/python/src/qm/qc_self_obstruction.py](../../../code/python/src/qm/qc_self_obstruction.py)
- sha256 (`bytes`): `bfc41c6def8f655c61bde3475189a299d276bae04e1f8c75f09f1d35a6d89d66`
- cited in: record TFQ-1317

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `linear_level` (python_symbol) | yes | yes | yes | - | - |
| `pair_count` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1317_qcv_repair_needed_but_costly.md`

- file: [dag/derivations/29_computation/tfq_1317_qcv_repair_needed_but_costly.md](../../../dag/derivations/29_computation/tfq_1317_qcv_repair_needed_but_costly.md)
- sha256 (`lf-normalised`): `85ca6f259f21f925c0efd38ea3702027b3c5cd08ab24173784e32bdd918d9d82`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1317
- counts toward the grade: no

### Documents and data: `dag/research/quantum_computation_self_obstruction.md`

- file: [dag/research/quantum_computation_self_obstruction.md](../../../dag/research/quantum_computation_self_obstruction.md)
- sha256 (`lf-normalised`): `8ae1b2ae291ee74f773da07740ebd0c1f98842bc01d7ec6a4d3c267e0077d178`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/quantum_computation_self_obstruction_axioms.txt`

- file: [dag/research/quantum_computation_self_obstruction_axioms.txt](../../../dag/research/quantum_computation_self_obstruction_axioms.txt)
- sha256 (`lf-normalised`): `b4c803ee2b1a4fe8af1d9d92a351fb11c61d2791bea01a5b7cd3dd7c1623af81`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-QCV-REPAIR-NEEDED-BUT-COSTLY` `DERIVED_LEAN`: [QCV-SELF-OBSTRUCTION-MODEL](QCV-SELF-OBSTRUCTION-MODEL.md) (DEFINITION)

Outgoing (0):

