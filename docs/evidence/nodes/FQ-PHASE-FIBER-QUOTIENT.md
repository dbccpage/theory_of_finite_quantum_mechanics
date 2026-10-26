# FQ-PHASE-FIBER-QUOTIENT

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On Z\[i\]-valued report vectors the phase-blind weight |c_q|^2 is nonnegative and real; a global phase and (in the Lean example) a relative phase lie inside one phase-blind fiber; two vectors are zero-related under the phase-blind difference iff phasePD_zeroRel_iff. Fiber enumeration uses a declared finite unit group.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Gaussian-integer/rational amplitude vectors (assumption)
- quadratic readout |.|^2 (assumption)
- finite phase group for fiber enumeration (assumption)

## Bottleneck

Not covered by the PFP review: Relate multi-report unit-group orbits to the intended quotient without identifying an orbit with the full norm fiber. A general finite-group action/quotient operad and coherence proof remain open.

## Source status

ledger: LEAN PROVED (RECEIPTED); H008/H009 headers: "Candidate only. Not PROVEN. Kind: LIFT RUNG"

## Review

- PFP review: [dag/results/FQ-PHASE-FIBER-QUOTIENT/reviews/20261019_scope_audit/review_result.json](../../../dag/results/FQ-PHASE-FIBER-QUOTIENT/reviews/20261019_scope_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `caveat_added`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Source phase-equivalence and relative/global-phase kernel statements are rechecked; the full single-coordinate norm25 integer fiber has twelve points while the declared unit orbit has four.
  - does not support: Relate multi-report unit-group orbits to the intended quotient without identifying an orbit with the full norm fiber. A general finite-group action/quotient operad and coherence proof remain open.
  - next test: Relate multi-report unit-group orbits to the intended quotient without identifying an orbit with the full norm fiber. A general finite-group action/quotient operad and coherence proof remain open.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: record TFQ-0251 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`
- counts toward the grade: no

### Lean: `lean4/H008PhaseBlindPresentation.lean`

- file: [lean4/H008PhaseBlindPresentation.lean](../../../lean4/H008PhaseBlindPresentation.lean)
- sha256 (`bytes`): `2ec11e9bfcd5470fd556ee7fe46ecb455c4ab6b5acde7b06213b624e65da439e`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `H008PhaseBlindPresentation`): recorded sha256 `2ec11e9bfcd5470fd556ee7fe46ecb455c4ab6b5acde7b06213b624e65da439e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build H008PhaseBlindPresentation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `weight_nonneg` | yes | yes | yes | Quot.sound, propext | `#print axioms weight_nonneg` |

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
| `phasePD_zeroRel_iff` | yes | yes | yes | none | `#print axioms phasePD_zeroRel_iff` |
| `relative_phase_in_fiber` | yes | yes | yes | Quot.sound | `#print axioms relative_phase_in_fiber` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/phase_averaged_shadow.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/phase_averaged_shadow.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

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

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`

- file: [sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md](../../../sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `5e43f206b08726fd4b27888d6fed3f211aac8398d5f8bf3dce712c415d7d81cc`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics_claim_ledger.md`

- file: [sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics_claim_ledger.md](../../../sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics_claim_ledger.md)
- sha256 (`lf-normalised`): `b9adbe593870ae277067c746b426f7b937a9cf98319cd4c8c0b712d9059dd5ac`
- cited in: node.source
- counts toward the grade: yes

## Absences recorded by the TFQ records

- TFQ-0251 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm

## Routes

Incoming (2):

- `FQ-R-PHASE-FIBER` `CONDITIONAL_ON_IMPORT`: [FQ-PRIMDIFF-QUOTIENT-KERNEL](FQ-PRIMDIFF-QUOTIENT-KERNEL.md) (PROVED_LEAN), [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)
- `X-R-PHASE-BLIND-TO-FQ-FIBER` `DERIVED_LEAN`: [L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE](L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE.md) (PROVED_LEAN)

Outgoing (5):

- `FQ-R-BORN-REDUNDANCY` `CONDITIONAL_ON_IMPORT`: [FQ-BORN-NORMALIZATION-REDUNDANCY](FQ-BORN-NORMALIZATION-REDUNDANCY.md) (PROVED_LEAN)
- `FQ-R-DESCENT` `COMPUTED`: [FQ-PHASE-BLIND-DESCENT-ZERO-RETAINED](FQ-PHASE-BLIND-DESCENT-ZERO-RETAINED.md) (COMPUTATIONALLY_CHECKED)
- `FQ-R-NONDESCENT` `DERIVED_LEAN`: [FQ-INTERFERENCE-NONDESCENT](FQ-INTERFERENCE-NONDESCENT.md) (PROVED_LEAN)
- `FQ-R-SORKIN-CLASS` `COMPUTED`: [FQ-SORKIN-READOUT-CLASS-QM208](FQ-SORKIN-READOUT-CLASS-QM208.md) (COMPUTATIONALLY_CHECKED)
- `FQ-R-U1` `COMPUTED`: [FQ-U1-TRANSPORT-N-TORSION](FQ-U1-TRANSPORT-N-TORSION.md) (COMPUTATIONALLY_CHECKED)
