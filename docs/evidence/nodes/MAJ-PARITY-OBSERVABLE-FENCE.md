# MAJ-PARITY-OBSERVABLE-FENCE

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> That a Z2 parity operator squares to I and commutes with an effective Hamiltonian is checked as an algebraic property of declared finite matrices; capacitance shifts C_Q and reflectometry signals stay external models and do not establish protection or coherence.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

No experimental readout model is derived.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-C8 claims DEFINITION; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/majorana/lean4/MajoranaCore.lean`

- file: [papers/core/majorana/lean4/MajoranaCore.lean](../../../papers/core/majorana/lean4/MajoranaCore.lean)
- sha256 (`bytes`): `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071`
- cited in: node.lean, record TFQ-1173
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_majorana.json](../../../dag/research/lean_replay_campaign_majorana.json) (module `papers.core.majorana.lean4.MajoranaCore`): recorded sha256 `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ParityObservable` | yes | yes | yes | none | `#print axioms ParityObservable` |
| `parity_eigenvalues` | yes | yes | yes | none | `#print axioms parity_eigenvalues` |

- counts toward the grade: yes

### Python: `code/python/src/majorana/majorana_mzm_ising.py`

- file: [code/python/src/majorana/majorana_mzm_ising.py](../../../code/python/src/majorana/majorana_mzm_ising.py)
- sha256 (`bytes`): `a4ac5734a5ab1a872aeaafd3835ed71261f069dfb29c17c9b5572a03e63b1310`
- cited in: record TFQ-1173

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ParityAlgebraModel` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1173_maj_parity_observable_fence.md`

- file: [dag/derivations/28_majorana/tfq_1173_maj_parity_observable_fence.md](../../../dag/derivations/28_majorana/tfq_1173_maj_parity_observable_fence.md)
- sha256 (`lf-normalised`): `9adf8c1eafc83b860dc4c83fc0ebb3e5825ddfacef90c2b12cbbb07680975071`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1173
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `2f55c0f24f87388cfa9d7a4a7d832f34c0fa30b857d344811f4336f634c1684b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/majorana/the_majorana_problem_claim_ledger.md`

- file: [papers/core/majorana/the_majorana_problem_claim_ledger.md](../../../papers/core/majorana/the_majorana_problem_claim_ledger.md)
- sha256 (`lf-normalised`): `37cc191a881cbb0f8fb52e30c2b865f9e9e70e235b4530df7bdd7d1b5728cb86`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-PARITY-OBSERVABLE-FENCE` `DERIVED_PROSE`: [MAJ-HARDWARE-NARRATIVE-QUARANTINE](MAJ-HARDWARE-NARRATIVE-QUARANTINE.md) (DEFINITION)

Outgoing (1):

- `APP-R-MAJ-PARITY-SECTOR-SPLIT-EXACT` `COMPUTED`: [MAJ-PARITY-SECTOR-SPLIT-EXACT](MAJ-PARITY-SECTOR-SPLIT-EXACT.md) (COMPUTATIONALLY_CHECKED)
