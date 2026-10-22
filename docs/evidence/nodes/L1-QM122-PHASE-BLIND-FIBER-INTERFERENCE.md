# L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Over Z\[i\] with the unnormalized two-sector Hadamard readout (|a+b|^2, |a-b|^2): for any nonzero Gaussian amplitudes a, b no function of the phase-blind weights (|a|^2, |b|^2) determines the readout on the product of the weight fibers (rotation by i or by -1 suffices); mixing doubles the total weight and the readout difference is 4 Re(a conj b); a zero first or zero second sector makes the readout descend. The source witnesses (1,1)/(1,-1) are instances. Complex Hilbert amplitudes, normalized or projective states, more than two sectors, other mixes and the link to the Vec GaussInt Bool declarations (H008/H010) are not covered.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 14
- cited Lean declarations covered by a current replay receipt: 10
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

- `receipt_names_uncited_module`: a replay receipt names this node for lean4/PhaseBlindFiber.lean, but the node's lean, rust and source fields do not cite it. A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence).

## Imported structure

- unit phases: assumption

## Bottleneck

Z\[i\] -\> C embedding and the identification with the source H008/H010 declarations are not formalised; normalized/projective readout with n\>=3 sectors and non-Hadamard unitary mixes are open.

## Source status

QM_122 ledger LEAN4_PROOF; file headers: 'Candidate only. Not PROVEN' (H013 headers); build not rerun by me

## Review

- PFP review: [dag/results/L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE/reviews/20261021_batch01a_audit/delivery_review_result.json](../../../dag/results/L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE/reviews/20261021_batch01a_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Over Z\[i\] with the unnormalized two-sector Hadamard readout: both sector amplitudes nonzero implies the weight pair does not determine the readout; a zero first or zero second sector implies it does.
  - does not support: Complex-Hilbert amplitudes beyond Z\[i\]; normalized or projective states; more than two sectors; mixes other than the unnormalized 2x2 Hadamard; the embedding of Z\[i\] into C (non-descent on the Gaussian-lattice fibers gives non-descent on the full complex phase fibers only after that embedding is formalised); the identification of the module readout with the source declarations phaseBlind/mix/readout over Vec GaussInt Bool (H008/H010), which is a modelling identification, not a checked one; any measurement, branch or physical interpretation of the phase fiber.
  - next test: Decide non-descent of the normalized projective readout w(a+b)/(2(w(a)+w(b))) for n\>=3 complex sectors under a unitary mix other than the 2x2 Hadamard, by exhibiting a fiber pair with different readouts or a descending fiber.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition` |
- counts toward the grade: yes

### Lean: `lean4/H008PhaseBlindPresentation.lean`

- file: [lean4/H008PhaseBlindPresentation.lean](../../../lean4/H008PhaseBlindPresentation.lean)
- sha256 (`bytes`): `2ec11e9bfcd5470fd556ee7fe46ecb455c4ab6b5acde7b06213b624e65da439e`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build H008PhaseBlindPresentation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `phase_blind_presentation` | yes | yes | yes | - | `#print axioms phase_blind_presentation` |
- counts toward the grade: yes

### Lean: `lean4/H010InterferenceNonDescent.lean`

- file: [lean4/H010InterferenceNonDescent.lean](../../../lean4/H010InterferenceNonDescent.lean)
- sha256 (`bytes`): `e46f995a5af051ddb72746a7dfb674cccc95a3eb3a499d52a0287e5700f06703`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build H010InterferenceNonDescent`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `mix_separates` | yes | yes | yes | - | `#print axioms mix_separates` |
| `no_descent_through_fiber` | yes | yes | yes | - | `#print axioms no_descent_through_fiber` |
- counts toward the grade: yes

### Lean: `lean4/PhaseBlindFiber.lean`

- file: [lean4/PhaseBlindFiber.lean](../../../lean4/PhaseBlindFiber.lean)
- sha256 (`bytes`): `302e3a2da088ad7de12570522d30a4bbd1f5c03099a22d4b7ff6be6baa75ad6d`
- cited in: receipt dag/research/pfp_batch01_lean_replay.json (PhaseBlindFiber)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `PhaseBlindFiber`): recorded sha256 `302e3a2da088ad7de12570522d30a4bbd1f5c03099a22d4b7ff6be6baa75ad6d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build PhaseBlindFiber`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `PhaseBlindFiber.descends_when_second_zero` | yes | yes | yes | propext | `#print axioms PhaseBlindFiber.descends_when_second_zero` |
| `PhaseBlindFiber.descends_when_zero_sector` | yes | yes | yes | propext | `#print axioms PhaseBlindFiber.descends_when_zero_sector` |
| `PhaseBlindFiber.fiber_changes_readout` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PhaseBlindFiber.fiber_changes_readout` |
| `PhaseBlindFiber.no_descent` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PhaseBlindFiber.no_descent` |
| `PhaseBlindFiber.phase_blind_fiber_interference` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PhaseBlindFiber.phase_blind_fiber_interference` |
| `PhaseBlindFiber.readout_interference` | yes | yes | yes | Quot.sound, propext | `#print axioms PhaseBlindFiber.readout_interference` |
| `PhaseBlindFiber.readout_total` | yes | yes | yes | Quot.sound, propext | `#print axioms PhaseBlindFiber.readout_total` |
| `PhaseBlindFiber.w_I_mul` | yes | yes | yes | Quot.sound, propext | `#print axioms PhaseBlindFiber.w_I_mul` |
| `PhaseBlindFiber.w_eq_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PhaseBlindFiber.w_eq_zero` |
| `PhaseBlindFiber.witness_readouts` | yes | yes | yes | none | `#print axioms PhaseBlindFiber.witness_readouts` |
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

### Documents and data: `dag/derivations/09_finite_hilbert/tfq_0310_finite_hilbert_boundary_from_a_presented_carrier.md`

- file: [dag/derivations/09_finite_hilbert/tfq_0310_finite_hilbert_boundary_from_a_presented_carrier.md](../../../dag/derivations/09_finite_hilbert/tfq_0310_finite_hilbert_boundary_from_a_presented_carrier.md)
- sha256 (`lf-normalised`): `67fd961bf04a6879f486db996d6a2e24b6db5a2ff2f2cd33a7669cc387dc22d7`
- generated view: listed, not counted
- cited in: record TFQ-0310
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/122_finite_hilbert_boundary_from_primitive_difference/qm_122_finite_hilbert_boundary_from_primitive_difference_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/122_finite_hilbert_boundary_from_primitive_difference/qm_122_finite_hilbert_boundary_from_primitive_difference_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0310 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/_code/qm_122/qm122_lib/qm122_dual.py
- TFQ-0310 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/hilbert_space.rs
- TFQ-0310 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/phase_blind_quotient.rs

## Routes

Incoming (1):

- `L1-R-PHASE-BLIND-INTERFERENCE` `DERIVED_LEAN`: [L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY](L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY.md) (PROVED_LEAN), [L1-IMP-U1-PHASES](L1-IMP-U1-PHASES.md) (IMPORTED_ASSUMPTION)

Outgoing (2):

- `L1-R-MNC-LEFTOVER` `DERIVED_LEAN`: [L1-QM122-LEFTOVER-MNC-NOT-RECOVERED](L1-QM122-LEFTOVER-MNC-NOT-RECOVERED.md) (PROVED_LEAN)
- `X-R-PHASE-BLIND-TO-FQ-FIBER` `DERIVED_LEAN`: [FQ-PHASE-FIBER-QUOTIENT](FQ-PHASE-FIBER-QUOTIENT.md) (PROVED_LEAN)
