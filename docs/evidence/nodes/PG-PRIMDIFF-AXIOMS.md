# PG-PRIMDIFF-AXIOMS

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Rust-side axiom list for primitive difference (A1-A10) and a GenesisAdmissionKernel whose admit_difference admits an ordered pair under a token; also the Phi1/Gamma2/R_cl triad signature type. This is an implementation of the admitted floor, not a derivation of it.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 22
- cited Lean declarations covered by a current replay receipt: 22
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

- `receipt_names_uncited_module`: a replay receipt names this node for lean4/PrimdiffAxioms.lean, but the node's lean, rust and source fields do not cite it. A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence).
- `broken_reference`: path not found: code/python/src/majorana/tests/unit/test_primitive_difference.py. A cited in-repo path or symbol cannot be found in this checkout.

## Imported structure

- Finite carrier items (assumption)

## Bottleneck

Bridge obligation GEN-WDP-O01 (justify or explicitly admit the primitive-to-witness carrier, signature, law and challenge-generation floor) is open; the explicit admission is done, the stronger derivation is not; definitions of A2, A4 and A6-A9 are not in the pinned source.

## Source status

PrimitiveDifferenceAxiom A1-A10 (Rust enum); Genesis admission kernel

## Review

- PFP review: [dag/results/PG-PRIMDIFF-AXIOMS/reviews/20261021_batch01b_audit/delivery_review_result.json](../../../dag/results/PG-PRIMDIFF-AXIOMS/reviews/20261021_batch01b_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `caveat_added`; prior status `DEFINITION`; qualifies for E4: yes.
  - narrowest claim: In a small product model (carriers of at most three points, at most one triangular face, A10 a free flag), the transcribed axioms A1, A4, A5 and A10 are jointly satisfiable and A1, A4, A10 are each violable alone from one point and A5 (together with A7) from three points; A3 holds because a reflexive-transitive closure is a preorder; A7 is A5 under the reading of A7 as d1 vanishing on im d0; the kernel enforces only A1 and carrier membership (the token is stored, never checked); and the transcribed R_cl rule refuses exactly on the exact-but-not-closed cell that d1 o d0 = 0 empties, a branch the source cannot reach because it rejects d1 o d0 != 0 at construction. This is evidence about a transcription of the list, not a derivation of it.
  - does not support: A derivation of the axiom list (obligation GEN-WDP-O01 and paper pin tfq_0394 stay open: this is a transcription and a small-model study, not a justification); that the predicates for A2, A4 and A6-A9 are the intended ones (the pinned file has names only; the one-line glosses come from an external copy of the file whose bytes differ from the pin); independence of A1 and A10 as a finding about the axioms (it holds by construction of the product model); A9: the relabelling check is an isomorphism (permuting vertex labels while keeping the cochain index-wise) and cannot fail, so it says nothing about observer-selected metrics; carriers of more than 3 points; real-valued Phi1, Gamma2 and R_cl values (here Phi1 is the unit-weight L1 distance to im d0 in integers and Gamma the L1 norm of d1 h); that the exact/closed classification equals classify_exact; any reachability of the source r_cl None branch; the Born, Hilbert or physical reading of any axiom.
  - next test: Obtain the definitions of A2, A4 and A6-A9 from the FOC-006 / FOC-000 sources (not bound here), replace the gloss-based predicates by them, and decide whether A9 is independent at all: test it with a weighted L1 norm whose weights are not permuted with the vertices (an observer-selected metric), since the present relabelling check is an isomorphism and cannot fail.

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
| `QuantumMechanics.DerivationDagQMClosure.pg_root_coproduct_inert_diamond_and_six_operation_separation` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.pg_root_coproduct_inert_diamond_and_six_operation_separation` |
| `QuantumMechanics.DerivationDagQMClosure.pg_six_operations_and_primdiff_admission_gate` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.pg_six_operations_and_primdiff_admission_gate` |
- counts toward the grade: yes

### Lean: `lean4/PrimdiffAxioms.lean`

- file: [lean4/PrimdiffAxioms.lean](../../../lean4/PrimdiffAxioms.lean)
- sha256 (`bytes`): `f41974512bd2143da41aa286cf55a45b2169c2e6690996bc01945cbea4ad8e16`
- cited in: receipt dag/research/pfp_batch01_lean_replay.json (PrimdiffAxioms)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `PrimdiffAxioms`): recorded sha256 `f41974512bd2143da41aa286cf55a45b2169c2e6690996bc01945cbea4ad8e16` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build PrimdiffAxioms`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `PrimdiffAxioms.a1_a4_a5_independent_on_three_vertices` | yes | yes | yes | propext | `#print axioms PrimdiffAxioms.a1_a4_a5_independent_on_three_vertices` |
| `PrimdiffAxioms.admit_error_a1` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PrimdiffAxioms.admit_error_a1` |
| `PrimdiffAxioms.admit_ok_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PrimdiffAxioms.admit_ok_iff` |
| `PrimdiffAxioms.admit_preserves_inv` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PrimdiffAxioms.admit_preserves_inv` |
| `PrimdiffAxioms.admit_token_irrelevant` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PrimdiffAxioms.admit_token_irrelevant` |
| `PrimdiffAxioms.d1_d0` | yes | yes | yes | propext | `#print axioms PrimdiffAxioms.d1_d0` |
| `PrimdiffAxioms.defect_gauge_invariant` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PrimdiffAxioms.defect_gauge_invariant` |
| `PrimdiffAxioms.descends_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PrimdiffAxioms.descends_iff` |
| `PrimdiffAxioms.duplicates_stored` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PrimdiffAxioms.duplicates_stored` |
| `PrimdiffAxioms.empty_structure_is_a_model` | yes | yes | yes | propext | `#print axioms PrimdiffAxioms.empty_structure_is_a_model` |
| `PrimdiffAxioms.exact_closed` | yes | yes | yes | Quot.sound, propext | `#print axioms PrimdiffAxioms.exact_closed` |
| `PrimdiffAxioms.exact_not_closed` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PrimdiffAxioms.exact_not_closed` |
| `PrimdiffAxioms.face_nilpotent_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PrimdiffAxioms.face_nilpotent_iff` |
| `PrimdiffAxioms.rcl_defined_of_nilpotent` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PrimdiffAxioms.rcl_defined_of_nilpotent` |
| `PrimdiffAxioms.rcl_eq_none_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PrimdiffAxioms.rcl_eq_none_iff` |
| `PrimdiffAxioms.rcl_refuses_zero_one` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PrimdiffAxioms.rcl_refuses_zero_one` |
| `PrimdiffAxioms.reverse_orientation_accepted` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PrimdiffAxioms.reverse_orientation_accepted` |
| `PrimdiffAxioms.rtc_least` | yes | yes | yes | none | `#print axioms PrimdiffAxioms.rtc_least` |
| `PrimdiffAxioms.rtc_preorder` | yes | yes | yes | none | `#print axioms PrimdiffAxioms.rtc_preorder` |
| `PrimdiffAxioms.trichotomy` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PrimdiffAxioms.trichotomy` |
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/obstruction.rs`

- file: [code/rust/src/wdp/obstruction.rs](../../../code/rust/src/wdp/obstruction.rs)
- sha256 (`bytes`): `d4a9514b3ee22c73ac47193206838c49cd5d908485d2c38dd026cd3bd9416cf8`
- cited in: record TFQ-0344 (shared)
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: no

### Rust: `code/rust/src/wdp/primitive_axiomatics.rs`

- file: [code/rust/src/wdp/primitive_axiomatics.rs](../../../code/rust/src/wdp/primitive_axiomatics.rs)
- sha256 (`bytes`): `c1ae6edba4d807a8247b3a2726dd7d07f30d83dbb27611e036c09e5e6ef26efc`
- cited in: record TFQ-0344 (shared)
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_wdp/src/primitive_axiomatics.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/primitive_axiomatics.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Python: `code/python/src/majorana/tests/unit/test_primitive_difference.py`

- file: `code/python/src/majorana/tests/unit/test_primitive_difference.py`
- resolution: `missing` (not found in this checkout)
- cited in: record TFQ-0394
- counts toward the grade: no

### Documents and data: `dag/derivations/01_pregenesis/tfq_0394_primitive_axiom_list_underived.md`

- file: [dag/derivations/01_pregenesis/tfq_0394_primitive_axiom_list_underived.md](../../../dag/derivations/01_pregenesis/tfq_0394_primitive_axiom_list_underived.md)
- sha256 (`lf-normalised`): `12a0fd9c3cad9b27b0ffd39cc38863219f0667b6fe8b361aa2f1f28e4526db2d`
- generated view: listed, not counted
- cited in: record TFQ-0394
- counts toward the grade: no

### Documents and data: `dag/derivations/06_wdp/tfq_0344_do_not_derive_the_degree_1_window_c0_c1_c2_d0_d1_from.md`

- file: [dag/derivations/06_wdp/tfq_0344_do_not_derive_the_degree_1_window_c0_c1_c2_d0_d1_from.md](../../../dag/derivations/06_wdp/tfq_0344_do_not_derive_the_degree_1_window_c0_c1_c2_d0_d1_from.md)
- sha256 (`lf-normalised`): `c16aa4ea4b517bdc1a92a8369e95aeb46571eb4ab99577a59f4423c1aecdfdd9`
- generated view: listed, not counted
- cited in: record TFQ-0344 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_bridge_register.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_bridge_register.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0394 lean4: declaration obligation: HasRawDistinction is not a stand-in for an unread A1-A10 enum
- TFQ-0394 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/lean4/FromPrimitiveDifferenceToFiniteObstructionCalculus/B001_raw_distinction.lean
- TFQ-0394 python: missing obligation: test_primitive_difference.py was listed and not opened; it must not be read as the A1-A10 list
- TFQ-0394 rust: missing obligation: the axiom enum cited by the DAG was not opened; do not equate it with omega_ooutwire_primitives until a path is checked

## Routes

Incoming (0):


Outgoing (1):

- `PG-R-GAP-GENESIS-TO-WINDOW` `DERIVED_LEAN`: [PG-WDP-DEGREE1-WINDOW](PG-WDP-DEGREE1-WINDOW.md) (DEFINITION)

No incoming route.
