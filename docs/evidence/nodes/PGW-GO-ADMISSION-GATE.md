# PGW-GO-ADMISSION-GATE

Stage: [GENESIS](../stages/GENESIS.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The fifteenth derivation keeps the ninth's states and changes and adds one given sentence: a result is reached, whether it is admitted is not given by the reaching, and the admission of every result is recorded. Under the chosen reading C-A1 admission is a two-valued record kept with the result: reaching leaves not-admitted, and every reached result can be admitted by a record that is not one of the four kinds of change. The Lean statements reaching_does_not_admit and reaching_ne_admitted hold by definition (reaching = .notAdmitted, and the two records differ), and admission is neither an assertion of r or s nor a third multiplicity.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Chosen reading C-A1: admission is a two-valued record kept with the result (assumption)

## Bottleneck

A declared record, not a theorem about Step9: a Lean function from Step9 to Admission is ledger row O2 and was not built, and the ledger marks D4 to D8 as chosen or by construction; admission_of_reaching is a Python function named in the vacuous self-comparison gate, not a Lean declaration.

## Source status

genesis_ongoing paper/fifteenth/claim_ledger.md G15, C-A1 and D4; chosen reading, definitional Lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisOngoing/Fifteenth/Step.lean`

- file: [lean4/Imported/GenesisOngoing/Fifteenth/Step.lean](../../../lean4/Imported/GenesisOngoing/Fifteenth/Step.lean)
- sha256 (`bytes`): `e7f115a5104f2bc5d54bc1b9b7227d4cfe3807f05f98f9382644b7b2db9e5bf1`
- cited in: node.lean, record TFQ-0481
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoing.Fifteenth.Step`): recorded sha256 `e7f115a5104f2bc5d54bc1b9b7227d4cfe3807f05f98f9382644b7b2db9e5bf1` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoing/Fifteenth/Step.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `reaching_does_not_admit` | yes | yes | yes | none | `#print axioms reaching_does_not_admit` |
| `reaching_ne_admitted` | yes | yes | yes | none | `#print axioms reaching_ne_admitted` |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/fifteenth/admission.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/fifteenth/admission.py](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/fifteenth/admission.py)
- sha256 (`bytes`): `6afbef24a0fb9cc81c4e39b2114fd1f92b836209a5033acc8f2301d4b49b9b3b`
- cited in: record TFQ-0481

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `admission_of_reaching` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/fifteenth/claim_ledger.md`

- file: [atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/fifteenth/claim_ledger.md](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/fifteenth/claim_ledger.md)
- sha256 (`lf-normalised`): `8b6201de03fb52ac14ba7cf9225edda0d0025ce9c98755064866864a20ae0d4d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0481_go_admission_gate.md`

- file: [dag/derivations/02_genesis/tfq_0481_go_admission_gate.md](../../../dag/derivations/02_genesis/tfq_0481_go_admission_gate.md)
- sha256 (`lf-normalised`): `190b587ec9e79cc970e73f7b1f1c743a7eead451b87dd4a37398125571d402cb`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0481
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:0e64131ef8fa37dfd5979d1cd82872324bbe93c10dc82fbdd78643e39acb8684:38`

## Absences recorded by the TFQ records

- TFQ-0481 rust: the H3V7N5QF package holds no Rust

## Routes

Incoming (1):

- `PGW-R-GO-ADMISSION-GATE` `DERIVED_PROSE`: [PGW-GO-TWO-RELATIONS-SWAP](PGW-GO-TWO-RELATIONS-SWAP.md) (PROVED_LEAN)

Outgoing (4):

- `GTH-R-GTH-LANG-CORE` `GAP_NO_DERIVATION`: [GTH-LANG-CORE](GTH-LANG-CORE.md) (OPEN)
- `GTH-R-GTH-SHADOW` `GAP_NO_DERIVATION`: [GTH-SHADOW](GTH-SHADOW.md) (OPEN)
- `OPS-R-AXIS1-WELLFOUNDED-ADMISSION` `GAP_NO_DERIVATION`: [OPS-AXIS1-WELLFOUNDED-ADMISSION](OPS-AXIS1-WELLFOUNDED-ADMISSION.md) (IMPORTED_ASSUMPTION)
- `PGW-R-GO-LEFTOVER-UNBOUNDEDNESS` `DERIVED_LEAN`: [PGW-GO-LEFTOVER-UNBOUNDEDNESS](PGW-GO-LEFTOVER-UNBOUNDEDNESS.md) (PROVED_LEAN)
