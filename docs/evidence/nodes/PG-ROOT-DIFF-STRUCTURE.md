# PG-ROOT-DIFF-STRUCTURE

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `ADMITTED_PRIMITIVE`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Admitted root of the programme: Real_0 = PrimitiveDifference ⊔ Structure, a typed coproduct of two independently posited channels. As a type construction (arbitrary payload types, same two-constructor shape as OntologyBasic.Real0) the coproduct is a categorical coproduct that singles out no map between the channels and supplies no element of either; the existence of a map out of it that is the identity on one channel holds exactly when that channel is nonempty or the other is empty, so for inhabited channels (as the real record types are) bare function-existence is not a no-reduction theorem. \[The clauses 'carrier-Structure precedes a primitive difference', 'residual-Structure (Q^1 = C^1/im d0) is what the difference produces' and 'the ladder is a definability order and mints no authority' are not addressed.\]

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 21
- cited Lean declarations covered by a current replay receipt: 20
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `receipt_names_uncited_module`: a replay receipt names this node for lean4/RootDiffStructure.lean, but the node's lean, rust and source fields do not cite it. A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence).

## Imported structure

- Structure carrier (assumption: declared, not derived)
- Primitive difference delta_0 (assumption: admitted primitive)

## Bottleneck

Admitted, not derived. Only coproduct neutrality for abstract payload types is kernel-checked; 'no reduction of either channel to the other' has no non-trivial formalisation here and the precedence/definability clauses are untouched. Two sources mark the lineage withdrawn (ENC-1138); no derivation from the literal inscription (PG-INERT-DIAMOND).

## Source status

DEFINITION (anomalon ledger C1); DEFINED (ENC-1138); GTLA rule 2 'admitted root'

## Review

- PFP review: [dag/results/PG-ROOT-DIFF-STRUCTURE/reviews/20261021_batch01b_audit/delivery_review_result.json](../../../dag/results/PG-ROOT-DIFF-STRUCTURE/reviews/20261021_batch01b_audit/delivery_review_result.json); file present and sha256 matches the node's record: no; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `ADMITTED_PRIMITIVE`; qualifies for E4: no.
  - narrowest claim: The typed coproduct of two payload types (same two-constructor shape as OntologyBasic.Real0) is a categorical coproduct that supplies no map between the channels and no element of either channel: a map out of it that is the identity on one channel exists exactly when that channel is nonempty or the other is empty (so bare existence of such a map is not a reduction theorem for inhabited channels), and the two nonemptiness conditions are independent of the construction and of each other.
  - does not support: Anything about the actual OntologyBasic.Real0 beyond its constructor shape (the file is not imported; its payloads are universe-polymorphic record types). The real Real0 has the record TYPES PrimitiveDifference and Structure as channels; both are inhabited, so by retracts_to_pd_iff and retracts_to_s_iff retractions in both directions exist for it: the emptiness cases of this file are not instances of the real node, and nothing here says either channel is irreducible to the other. That either channel exists, is real or has an origin (admitted posits, ENC-1138 lineage withdrawn); the passage from the literal inscription (PG-INERT-DIAMOND, route marked GAP_NO_DERIVATION); the clauses "carrier-Structure precedes a primitive difference", "residual-Structure Q^1 = C^1/im d0 is what the difference produces" and "the ladder is a definability order"; any physical or interpretive reading.
  - next test: Formalise the clause "carrier-Structure precedes a primitive difference": define precedence as the statement that a PrimitiveDifference record can be built with no Structure value in scope (Source := PUnit) and a Structure record with no PrimitiveDifference, then decide whether Source must equal Structure.Carrier for the node text to be meant, by a finite model or a counterexample.

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
| `QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation` |
| `QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure` |
| `QuantumMechanics.DerivationDagQMClosure.pg_root_coproduct_inert_diamond_and_six_operation_separation` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.pg_root_coproduct_inert_diamond_and_six_operation_separation` |
- counts toward the grade: yes

### Lean: `lean4/FiniteDensity.lean`

- file: [lean4/FiniteDensity.lean](../../../lean4/FiniteDensity.lean)
- sha256 (`bytes`): `e62172019a4407f5101e62681d2139ff9fa2a7201e4424ad8b0a6143f5eae763`
- cited in: record TFQ-0086 (shared)
- replay: `none`
- check: `cd lean4 && lake build FiniteDensity`
- counts toward the grade: no

### Lean: `lean4/Imported/AnomalonBoundary/OntologyBasic.lean`

- file: [lean4/Imported/AnomalonBoundary/OntologyBasic.lean](../../../lean4/Imported/AnomalonBoundary/OntologyBasic.lean)
- sha256 (`bytes`): `122848b820ebf20aa3cad5e8e198524bb1aa269498a2895c6e6ac786cb2e6b8a`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/AnomalonBoundary/OntologyBasic.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Real0` | yes | yes | yes | - | `#print axioms Real0` |
- counts toward the grade: yes

### Lean: `lean4/RootDiffStructure.lean`

- file: [lean4/RootDiffStructure.lean](../../../lean4/RootDiffStructure.lean)
- sha256 (`bytes`): `63a62b1dcd98373ab6a5019b54e567ad7d55894f6eca73a95a19e6f5af305084`
- cited in: receipt dag/research/pfp_batch01_lean_replay.json (RootDiffStructure)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `RootDiffStructure`): recorded sha256 `63a62b1dcd98373ab6a5019b54e567ad7d55894f6eca73a95a19e6f5af305084` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build RootDiffStructure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `RootDiffStructure.card_maps_out` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RootDiffStructure.card_maps_out` |
| `RootDiffStructure.card_maps_out_pow` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RootDiffStructure.card_maps_out_pow` |
| `RootDiffStructure.card_real0` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RootDiffStructure.card_real0` |
| `RootDiffStructure.exhaustive` | yes | yes | yes | none | `#print axioms RootDiffStructure.exhaustive` |
| `RootDiffStructure.no_identification` | yes | yes | yes | none | `#print axioms RootDiffStructure.no_identification` |
| `RootDiffStructure.no_reduction_to_pd` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RootDiffStructure.no_reduction_to_pd` |
| `RootDiffStructure.no_reduction_to_s` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RootDiffStructure.no_reduction_to_s` |
| `RootDiffStructure.nonempty_real0_iff` | yes | yes | yes | Classical.choice | `#print axioms RootDiffStructure.nonempty_real0_iff` |
| `RootDiffStructure.pd_injective` | yes | yes | yes | none | `#print axioms RootDiffStructure.pd_injective` |
| `RootDiffStructure.pd_ne_st` | yes | yes | yes | none | `#print axioms RootDiffStructure.pd_ne_st` |
| `RootDiffStructure.posits_independent` | yes | yes | yes | none | `#print axioms RootDiffStructure.posits_independent` |
| `RootDiffStructure.real0_empty_of_both_empty` | yes | yes | yes | none | `#print axioms RootDiffStructure.real0_empty_of_both_empty` |
| `RootDiffStructure.retractions_both_ways_of_nonempty` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RootDiffStructure.retractions_both_ways_of_nonempty` |
| `RootDiffStructure.retracts_to_pd_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RootDiffStructure.retracts_to_pd_iff` |
| `RootDiffStructure.retracts_to_s_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RootDiffStructure.retracts_to_s_iff` |
| `RootDiffStructure.st_injective` | yes | yes | yes | none | `#print axioms RootDiffStructure.st_injective` |
| `RootDiffStructure.universal` | yes | yes | yes | Quot.sound | `#print axioms RootDiffStructure.universal` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_types/src/primitive_difference.rs`

- file: `omega_engine/crates_rs/omega_types/src/primitive_difference.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Python: `code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py`

- file: `code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py`
- resolution: `missing` (not found in this checkout)
- cited in: record TFQ-0086 (shared)
- counts toward the grade: no

### Documents and data: `.claude/rules/authority/rl_gtla_rules_rubric.md`

- file: `.claude/rules/authority/rl_gtla_rules_rubric.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/01_pregenesis/tfq_0001_gap_between_and_difference_joined_with_structure.md`

- file: [dag/derivations/01_pregenesis/tfq_0001_gap_between_and_difference_joined_with_structure.md](../../../dag/derivations/01_pregenesis/tfq_0001_gap_between_and_difference_joined_with_structure.md)
- sha256 (`lf-normalised`): `e5299832395b3f700f68e619fb30d3a1fab83d0c2a0e3a6be8c963dc1fee8daa`
- generated view: listed, not counted
- cited in: record TFQ-0001
- counts toward the grade: no

### Documents and data: `dag/derivations/01_pregenesis/tfq_0392_inscription_to_coproduct_gap.md`

- file: [dag/derivations/01_pregenesis/tfq_0392_inscription_to_coproduct_gap.md](../../../dag/derivations/01_pregenesis/tfq_0392_inscription_to_coproduct_gap.md)
- sha256 (`lf-normalised`): `12b8df2a8a5beebd90a38c0cd77b219190e4711fa38464adaf8425f12b18300d`
- generated view: listed, not counted
- cited in: record TFQ-0392 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/01_pregenesis/tfq_0393_admitted_root_coproduct.md`

- file: [dag/derivations/01_pregenesis/tfq_0393_admitted_root_coproduct.md](../../../dag/derivations/01_pregenesis/tfq_0393_admitted_root_coproduct.md)
- sha256 (`lf-normalised`): `dbd5898bb1c5040f0f8ee270c294f4dd8b429c61f7fe831c82bd111ef0f3fe1b`
- generated view: listed, not counted
- cited in: record TFQ-0393
- counts toward the grade: no

### Documents and data: `dag/derivations/19_finite_qg/tfq_0086_fq_gap_continuum_hilbert_lift_stays_unpaid_no_continuum_hilbert_space_is_admitted_at_the_root.md`

- file: [dag/derivations/19_finite_qg/tfq_0086_fq_gap_continuum_hilbert_lift_stays_unpaid_no_continuum_hilbert_space_is_admitted_at_the_root.md](../../../dag/derivations/19_finite_qg/tfq_0086_fq_gap_continuum_hilbert_lift_stays_unpaid_no_continuum_hilbert_space_is_admitted_at_the_root.md)
- sha256 (`lf-normalised`): `878199cafd2c1775202016787f8d29ad515ee87124dc446accd96e04f3a1741c`
- generated view: listed, not counted
- cited in: record TFQ-0086 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/19_finite_qg/tfq_0087_relational_difference_is_a_finite_carrier_smooth_spacetime_and_the_einstein_equation.md`

- file: [dag/derivations/19_finite_qg/tfq_0087_relational_difference_is_a_finite_carrier_smooth_spacetime_and_the_einstein_equation.md](../../../dag/derivations/19_finite_qg/tfq_0087_relational_difference_is_a_finite_carrier_smooth_spacetime_and_the_einstein_equation.md)
- sha256 (`lf-normalised`): `7c5e5fd4a9a2eaefb7ec0c0286f269c06a07f2513ae9d2abeb73d7a2f4497e00`
- generated view: listed, not counted
- cited in: record TFQ-0087
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/029_the_anomalon_boundary/the_anomalon_boundary_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/029_the_anomalon_boundary/the_anomalon_boundary_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_library/coda_library/encyclopedia/entries/foundations/enc-1138-stratified-root-boundary.md`

- file: `omega_engine_library/coda_library/encyclopedia/entries/foundations/enc-1138-stratified-root-boundary.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0392 lean4: missing declaration obligation: no arrow in 000_pre_genesis_to_mssn/lean4/Paper.lean from a literal inscription to a coproduct root
- TFQ-0392 python: missing obligation: a negative check that no function in 000_pre_genesis_to_mssn/code/preservation.py sends literal <> to a two-channel coproduct
- TFQ-0392 rust: missing obligation: a refused conversion in omega_ooutwire_primitives from the inscription token to a Difference-Structure value
- TFQ-0393 lean4: missing declaration obligation: a coproduct Real_0 distinct from HasRawDistinction in B001_raw_distinction.lean
- TFQ-0393 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/lean4/FromPrimitiveDifferenceToFiniteObstructionCalculus/B001_raw_distinction.lean
- TFQ-0393 python: missing obligation: a two-summand carrier in the S000 python package that is not constructed from preservation.py token data
- TFQ-0393 rust: missing obligation: a coproduct struct whose constructors are independent of the inscription token in omega_ooutwire_primitives

## Routes

Incoming (1):

- `PG-R-GAP-DIAMOND-TO-ROOT` `GAP_NO_DERIVATION`: [PG-INERT-DIAMOND](PG-INERT-DIAMOND.md) (DEFINITION)

Outgoing (3):

- `PG-R-ROOT-TO-ADMISSION-FLOOR` `CONDITIONAL_ON_IMPORT`: [PG-ADMISSION-FLOOR](PG-ADMISSION-FLOOR.md) (PROVED_LEAN)
- `UDG-R-TFQ-0088` `RECORD_PARENT`: [TFQ-0088](TFQ-0088.md) (SOURCE_RECORD)
- `X-R-ROOT-TO-PRIMDIFF-KERNEL` `CONDITIONAL_ON_IMPORT`: [FQ-PRIMDIFF-QUOTIENT-KERNEL](FQ-PRIMDIFF-QUOTIENT-KERNEL.md) (PROVED_LEAN)
