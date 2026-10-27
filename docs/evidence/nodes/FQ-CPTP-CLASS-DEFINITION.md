# FQ-CPTP-CLASS-DEFINITION

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The channel class is defined: CPTP via Choi PSD with Kraus rank bound (d=2: Choi dimension 4, Kraus rank at most 4), and Stinespring realizations with a declared weighted environment metric. A definition, not a derivation of the class.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- positivity (Choi PSD) (assumption)

## Bottleneck

Class is declared; channel availability is an operational premise.

## Source status

GAP-F001-S000-007 status DEFINED

## Review

- PFP review: [dag/results/FQ-CPTP-CLASS-DEFINITION/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/FQ-CPTP-CLASS-DEFINITION/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `DEFINITION`; qualifies for E4: yes.
  - narrowest claim: Full depolarizing Choi arrays, eigenvector actions, rank controls and TP partial trace are exact; eigenvalue nonnegativity iff -1/3\<=p\<=1 and trace2 are kernel checked.
  - does not support: Prove the full Choi-PSD/Kraus/Stinespring bridge, environment metric and any actual field/conductor necessity. A class definition and data flags do not derive the channel class.
  - next test: Prove the full Choi-PSD/Kraus/Stinespring bridge, environment metric and any actual field/conductor necessity. A class definition and data flags do not derive the channel class.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CptpChannelsStinespring.lean`

- file: [lean4/CptpChannelsStinespring.lean](../../../lean4/CptpChannelsStinespring.lean)
- sha256 (`bytes`): `a2cc913c5c8c2bcdf1fc029625b52cebeb2ee1c19913e1f886f287bbcddde62a`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `CptpChannelsStinespring`): recorded sha256 `a2cc913c5c8c2bcdf1fc029625b52cebeb2ee1c19913e1f886f287bbcddde62a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CptpChannelsStinespring`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `choi_dimension_is_four` | yes | yes | yes | none | `#print axioms choi_dimension_is_four` |
| `depol_choi_1_3_psd` | yes | yes | yes | none | `#print axioms depol_choi_1_3_psd` |

- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: record TFQ-0262
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`
- counts toward the grade: yes

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0262_cptp_class_recorded_as_a_definition.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0262_cptp_class_recorded_as_a_definition.md](../../../dag/derivations/12_finite_qm_structure/tfq_0262_cptp_class_recorded_as_a_definition.md)
- sha256 (`lf-normalised`): `327c476359539bbdd3578d8ea2e58b097be196dbe7d83e987f5b44738a66f8f0`
- generated view: listed, not counted
- cited in: record TFQ-0262
- counts toward the grade: no

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml`

- file: [sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml](../../../sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `722a38e963f9ae31ac005968a71e39dff5964e452f5aca1e5cb4506dc0ece190`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:19f735a77b55e8182884060c73a1c66ccc64e14b24e1c3d5a173d64f8fe5b024::ExactChoiMatrix`
- `external:sha256:7ecaf8b5a2fd5a4428b83ca6f579e8bda5323dd5ca0b2d87b0138227eb0e5cf3::WeightedStinespring`

## Absences recorded by the TFQ records

- TFQ-0262 python: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm
- TFQ-0262 rust: no local rust twin located for external:sha256:19f735a77b55e8182884060c73a1c66ccc64e14b24e1c3d5a173d64f8fe5b024
- TFQ-0262 rust: no local rust twin located for external:sha256:7ecaf8b5a2fd5a4428b83ca6f579e8bda5323dd5ca0b2d87b0138227eb0e5cf3
- TFQ-0262 rust: no local rust twin located for external:sha256:e17359f64c885efb596f3390cf43cc40c25011d24ded59d783982b1eb15318df

## Routes

Incoming (1):

- `FQ-R-CPTP` `CONDITIONAL_ON_IMPORT`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `FQ-R-TRACE-NORM` `GAP_NO_DERIVATION`: [FQ-TRACE-NORM-FROM-CPTP-MONOTONICITY](FQ-TRACE-NORM-FROM-CPTP-MONOTONICITY.md) (OPEN)
