# FQ-PRIM-TO-QM-SELECTION-OPEN

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Primitive difference does not select the declared quantum model or readout. Direct packet-walk execution is an integration result: the complexes, Cayley parameter, cyclotomic weights, detector and squared-amplitude readout were supplied independently of the computed difference value.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- all of FQ-DECLARED-QUANTUM-INTERFACE (assumption)

## Bottleneck

Selection of a declared quantum model or readout from primitive difference stays open. Packet-walk execution, the complexes, the Cayley parameter, cyclotomic weights, the detector and a squared-amplitude readout are not this integer witness. Continuum M_n(C) and Gleason n\>=3 remain external imports. The D2, D3, D2xD3, D3^2 and D3^3 counts and the gap d-1 \< d^2-1 for d \>= 2 stay outside this witness.

## Source status

7-stage finite relational operad chain (D2, D3, D2xD3, D3^2, D3^3) and d-dimensional diagonal vs rebit vs qubit state-parameter gap (d-1 \< d^2-1) mechanized in CoupledRelationalProjectors.lean and DerivationDagQMClosure.lean; continuum Hilbert/Gleason imports remain external

## Review

- PFP review: [dag/results/FQ-PRIM-TO-QM-SELECTION-OPEN/reviews/20261019_structure_audit/review_result.json](../../../dag/results/FQ-PRIM-TO-QM-SELECTION-OPEN/reviews/20261019_structure_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `caveat_added`; prior status `CONDITIONAL`; qualifies for E4: yes.
  - narrowest claim: Identical two-label input carrier and amplitudes admit distinct positive normalized quadratic and quartic rules, with a symmetric agreement control; the 1:2 example is checked in Lean.
  - does not support: Derive a quantum carrier/readout selection principle and its hypotheses. Full continuum matrix/Hilbert/Gleason imports are not discharged by executing a declared packet walk.
  - next test: Derive a quantum carrier/readout selection principle and its hypotheses. Full continuum matrix/Hilbert/Gleason imports are not discharged by executing a declared packet walk.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFqPrimToQmSelection.lean`

- file: [lean4/CampaignFqPrimToQmSelection.lean](../../../lean4/CampaignFqPrimToQmSelection.lean)
- sha256 (`bytes`): `df3bc709da599a889424f62769a2524e54753a69bfa0e5214319542215dcb1a4`
- cited in: node.lean, receipt dag/research/campaign_fq-prim-to-qm-selection-open_lean_replay.json (CampaignFqPrimToQmSelection), receipt dag/research/pr_365_review_replay.json (CampaignFqPrimToQmSelection), record TFQ-1010
- replay: `verified`
  - receipt [dag/research/campaign_fq-prim-to-qm-selection-open_lean_replay.json](../../../dag/research/campaign_fq-prim-to-qm-selection-open_lean_replay.json) (module `CampaignFqPrimToQmSelection`): recorded sha256 `df3bc709da599a889424f62769a2524e54753a69bfa0e5214319542215dcb1a4` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/pr_365_review_replay.json](../../../dag/research/pr_365_review_replay.json) (module `CampaignFqPrimToQmSelection`): recorded sha256 `df3bc709da599a889424f62769a2524e54753a69bfa0e5214319542215dcb1a4` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFqPrimToQmSelection`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `normalized_first_weights_differ` | yes | yes | yes | none | `#print axioms normalized_first_weights_differ` |
| `quad_weights` | yes | yes | yes | none | `#print axioms quad_weights` |
| `quart_weights` | yes | yes | yes | none | `#print axioms quart_weights` |
| `symmetric_agreement` | yes | yes | yes | none | `#print axioms symmetric_agreement` |

- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1010
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_prim_to_qm_selection_finite_quotient_vs_continuum_gap` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_prim_to_qm_selection_finite_quotient_vs_continuum_gap` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/coupled_relational_operad.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/coupled_relational_operad.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1010
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1010
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_wdp/src/amplitude_bridge.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/amplitude_bridge.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1010
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_wdp/src/genesis_realification_adapter.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/genesis_realification_adapter.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1010
- counts toward the grade: no

### Python: `checks/independent/fq-prim-to-qm-selection-open.py`

- file: [checks/independent/fq-prim-to-qm-selection-open.py](../../../checks/independent/fq-prim-to-qm-selection-open.py)
- sha256 (`bytes`): `c34d80dd31d3b6b62f4773165707bfd5c67a3de6834a1941bfc5e7dadbf45760`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1010_fq_prim_to_qm_selection_open.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1010_fq_prim_to_qm_selection_open.md](../../../dag/derivations/10_finite_qm_core/tfq_1010_fq_prim_to_qm_selection_open.md)
- sha256 (`lf-normalised`): `3ad368064d38d9f624e7cd0f1e313f8e53c164e214d45cc56109de54205d5b2d`
- generated view: listed, not counted
- cited in: record TFQ-1010
- counts toward the grade: no

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml`

- file: [sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml](../../../sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `722a38e963f9ae31ac005968a71e39dff5964e452f5aca1e5cb4506dc0ece190`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md`

- file: [sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md](../../../sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `85ca7b22b1c1e360a4c17ad8a9e0bddae03433592585b01d23a74cd09c82929e`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FQ-R-GAP-PRIM-TO-SELECTION` `CONDITIONAL_ON_IMPORT`: [FQ-PRIMDIFF-QUOTIENT-KERNEL](FQ-PRIMDIFF-QUOTIENT-KERNEL.md) (PROVED_LEAN)

Outgoing (0):

