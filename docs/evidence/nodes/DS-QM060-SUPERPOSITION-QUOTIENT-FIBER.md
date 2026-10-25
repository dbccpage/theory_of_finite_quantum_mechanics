# DS-QM060-SUPERPOSITION-QUOTIENT-FIBER

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Under the supplied lift c = sqrt(w) e^{i theta}, |c|^2 = w is redundant, phase lies in the kernel of the phase-blind map delta, and phase reappears as a mixing cross term: (1,1) and (1,-1) share a quotient point and differ in the fiber. Superposition is observer-relative; no probability mass in the fiber.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declaration references covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- complex amplitude lift c_gamma with unit phases (lift)
- U(1) phase carrier (assumption)

## Bottleneck

Reuse of upstream theorem; no new derivation of the lift.

## Source status

\[DEFINITION\]/\[reuse\] (QM-060-C1..C4); theorem is a reuse of pub-010 T3/T4

## Review

- PFP review: [dag/results/DS-QM060-SUPERPOSITION-QUOTIENT-FIBER/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM060-SUPERPOSITION-QUOTIENT-FIBER/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Gaussian population invariance and the two-path cross-term identity are checked on exact records and literal rational Lean identities.
  - does not support: Construct and justify any full U(1) lift, quotient and physical readout; finite Gaussian controls alone do not select that carrier.
  - next test: Construct and justify any full U(1) lift, quotient and physical readout; finite Gaussian controls alone do not select that carrier.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0251 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm060_061_phase_fiber_and_interference_non_descent` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm060_061_phase_fiber_and_interference_non_descent` |

- counts toward the grade: yes

### Lean: `lean4/H009PhaseFiber.lean`

- file: [lean4/H009PhaseFiber.lean](../../../lean4/H009PhaseFiber.lean)
- sha256 (`bytes`): `0a41e5169888c39cab352ab7b0889bb01fdf0e1ab7410d7386d999c0958fa4b3`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `H009PhaseFiber`): recorded sha256 `0a41e5169888c39cab352ab7b0889bb01fdf0e1ab7410d7386d999c0958fa4b3` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build H009PhaseFiber`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `global_phase_in_fiber` | yes | yes | yes | Quot.sound, propext | `#print axioms global_phase_in_fiber` |
| `phase_fiber` | yes | yes | yes | Quot.sound, propext | `#print axioms phase_fiber` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/phase_blind_quotient.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/phase_blind_quotient.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0251_superposition_as_a_quotient_fiber.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0251_superposition_as_a_quotient_fiber.md](../../../dag/derivations/12_finite_qm_structure/tfq_0251_superposition_as_a_quotient_fiber.md)
- sha256 (`lf-normalised`): `fd30063978c3acac62e4d0a4944f225af21e50c7b2a9c17085ee5449739aea8e`
- generated view: listed, not counted
- cited in: record TFQ-0251 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/060_superposition_as_the_quotient_fiber/qm_060_superposition_as_the_quotient_fiber_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/060_superposition_as_the_quotient_fiber/qm_060_superposition_as_the_quotient_fiber_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0251 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm

## Routes

Incoming (2):

- `DS-R-SUPERPOSITION-FIBER` `DERIVED_LEAN`: [DS-QM062-U1-RESIDUES-IMPORT](DS-QM062-U1-RESIDUES-IMPORT.md) (IMPORTED_ASSUMPTION)
- `DS-R-U1-SELECTOR` `DERIVED_LEAN`: [DS-QM062-U1-SELECTOR-LAYERS](DS-QM062-U1-SELECTOR-LAYERS.md) (COMPUTATIONALLY_CHECKED), [DS-QM062-U1-RESIDUES-IMPORT](DS-QM062-U1-RESIDUES-IMPORT.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `DS-R-INTERFERENCE` `DERIVED_LEAN`: [DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE](DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE.md) (PROVED_LEAN)
