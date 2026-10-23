# PG-CHAIN-RETRACTION

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> If chain maps i: C -\> D and r: D -\> C satisfy r∘i = id, then induced homology map is injective, so extending a complex cannot kill an old class. Instances: two isolated points and a triangle with attached face have no such retraction onto the smaller complex where the class would be killed.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 8
- cited Lean, Rust or Python symbols found in their in-repo files: 18
- cited Lean declarations covered by a current replay receipt: 18
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test)

## Flags

- `receipt_names_uncited_module`: a replay receipt names this node for lean4/ChainRetraction.lean, but the node's lean, rust and source fields do not cite it. A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence).

## Imported structure

- Chain complex over a declared coefficient ring (assumption)

## Bottleneck

The bridge from declared inclusions to the Genesis/WDP growth statement (WDP-CH04-N02) on an actual Genesis/WDP complex pair; full-complex formalisation of the two named cases; non-linear retractions.

## Source status

Theorem 6 / chain-retraction obstruction (homology injective)

## Review

- PFP review: [dag/results/PG-CHAIN-RETRACTION/reviews/20261021_batch01a_audit/delivery_review_result.json](../../../dag/results/PG-CHAIN-RETRACTION/reviews/20261021_batch01a_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `caveat_added`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: For chain maps i: C -\> D and r: D -\> C over a ring with r . i = id on the middle module and r commuting with the boundary, the induced map on homology is injective, so an extension admitting such an r cannot kill an old class; the two-points and triangle-with-face extensions kill a class (kernel, in the modelled degree fragment, and native) and admit no linear chain retraction (kernel, same fragment).
  - does not support: The bridge from declared inclusions to WDP-CH04-N02 (growth of the Genesis/WDP complexes does not repair an obstruction) for any actual Genesis/WDP complex pair; coefficient rings other than the declared one in the native tables; infinite or non-free complexes in the native tables; non-linear retractions and the full-complex (all degrees at once) formalisation of the two named cases; an integral failure of the converse for a genuine subcomplex inclusion (the Z instance is a one-term map, not a subcomplex); the converse over Q as a Lean theorem (it is a standard fact over a field, only observed here on the listed complexes); any physical reading.
  - next test: Take one actual Genesis/WDP growth inclusion named by WDP-CH04-N02, write it in the native complex encoding with its basis subset, and decide by the retraction system and the rank of H(i) whether the old obstruction class is killed or a chain retraction exists, so that the bridge from the general theorem to the WDP growth statement is tested on a real complex.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/ChainRetraction.lean`

- file: [lean4/ChainRetraction.lean](../../../lean4/ChainRetraction.lean)
- sha256 (`bytes`): `94f50b9df3ae5fa4f31c1461289535ce947ac7d769e9aece38acd2556451ed26`
- cited in: receipt dag/research/pfp_batch01_lean_replay.json (ChainRetraction)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `ChainRetraction`): recorded sha256 `94f50b9df3ae5fa4f31c1461289535ce947ac7d769e9aece38acd2556451ed26` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build ChainRetraction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ChainRetraction.Hmap_injective` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ChainRetraction.Hmap_injective` |
| `ChainRetraction.TimesTwo.converse_fails_over_int` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ChainRetraction.TimesTwo.converse_fails_over_int` |
| `ChainRetraction.Triangle.cls_killed` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ChainRetraction.Triangle.cls_killed` |
| `ChainRetraction.Triangle.cls_ne_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ChainRetraction.Triangle.cls_ne_zero` |
| `ChainRetraction.Triangle.no_chain_retraction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ChainRetraction.Triangle.no_chain_retraction` |
| `ChainRetraction.Triangle.square_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ChainRetraction.Triangle.square_zero` |
| `ChainRetraction.TwoPoints.cls_killed` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ChainRetraction.TwoPoints.cls_killed` |
| `ChainRetraction.TwoPoints.cls_ne_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ChainRetraction.TwoPoints.cls_ne_zero` |
| `ChainRetraction.TwoPoints.no_chain_retraction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ChainRetraction.TwoPoints.no_chain_retraction` |
| `ChainRetraction.cannot_kill` | yes | yes | yes | none | `#print axioms ChainRetraction.cannot_kill` |
| `ChainRetraction.kernel_trivial` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ChainRetraction.kernel_trivial` |
| `ChainRetraction.no_retraction_of_killed` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ChainRetraction.no_retraction_of_killed` |
- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition` |
- counts toward the grade: yes

### Lean: `lean4/FiniteCochain.lean`

- file: [lean4/FiniteCochain.lean](../../../lean4/FiniteCochain.lean)
- sha256 (`bytes`): `344749ef8c272d08ff04702031ce24e3cc5b41709f6c47d5f95afb2c3bf6d9f8`
- cited in: record TFQ-0195
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_implementation_sibling.json](../../../dag/research/lean_replay_campaign_implementation_sibling.json) (module `FiniteCochain`): recorded sha256 `344749ef8c272d08ff04702031ce24e3cc5b41709f6c47d5f95afb2c3bf6d9f8` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteCochain`
- counts toward the grade: yes

### Lean: `lean4/Imported/PreGenesisToMssn/Homology.lean`

- file: [lean4/Imported/PreGenesisToMssn/Homology.lean](../../../lean4/Imported/PreGenesisToMssn/Homology.lean)
- sha256 (`bytes`): `c2d4c354ae83deec3317716ed1324cc2560e190f9c9c39f8b1000c97e01b315c`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.PreGenesisToMssn.Homology`): recorded sha256 `c2d4c354ae83deec3317716ed1324cc2560e190f9c9c39f8b1000c97e01b315c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/PreGenesisToMssn/Homology.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `induced_homology_injective` | yes | yes | yes | Quot.sound, propext | `#print axioms induced_homology_injective` |
- counts toward the grade: yes

### Lean: `lean4/Imported/PreGenesisToMssn/Paper.lean`

- file: [lean4/Imported/PreGenesisToMssn/Paper.lean](../../../lean4/Imported/PreGenesisToMssn/Paper.lean)
- sha256 (`bytes`): `5f0ebfc1710b91ce84d4570d7653a3cb8396824adecfaba16fa59a96354b9e12`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.PreGenesisToMssn.Paper`): recorded sha256 `5f0ebfc1710b91ce84d4570d7653a3cb8396824adecfaba16fa59a96354b9e12` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/PreGenesisToMssn/Paper.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `chain_retraction_cannot_kill` | yes | yes | yes | none | `#print axioms chain_retraction_cannot_kill` |
- counts toward the grade: yes

### Lean: `lean4/Imported/SnMssn/Paper001.lean`

- file: [lean4/Imported/SnMssn/Paper001.lean](../../../lean4/Imported/SnMssn/Paper001.lean)
- sha256 (`bytes`): `1a79ddc7a70157834ee80ed3890124aadd149093336ac49776eab3c167b4fb07`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.SnMssn.Paper001`): recorded sha256 `1a79ddc7a70157834ee80ed3890124aadd149093336ac49776eab3c167b4fb07` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/SnMssn/Paper001.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `homology_injective_of_chain_retraction` | yes | yes | yes | none | `#print axioms homology_injective_of_chain_retraction` |
| `triangle_retraction_impossible` | yes | yes | yes | none | `#print axioms triangle_retraction_impossible` |
| `two_point_retraction_impossible` | yes | yes | yes | Quot.sound, propext | `#print axioms two_point_retraction_impossible` |
- counts toward the grade: yes

### Rust: `code/rust/src/homology/simplicial.rs`

- file: [code/rust/src/homology/simplicial.rs](../../../code/rust/src/homology/simplicial.rs)
- sha256 (`bytes`): `1468fc9164c77765488691bf65f3cae138962b25de51858c1269d8a9ab19cb91`
- cited in: record TFQ-0195
- note: no test is cited for this symbol; its crate is theory_of_finite_qm
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/lib.rs`

- file: [code/rust/src/wdp/lib.rs](../../../code/rust/src/wdp/lib.rs)
- sha256 (`bytes`): `aa868cc58a3c6fdf1eabfcdd46798329bf560389e83367c574259837d2d3ed4c`
- cited in: record TFQ-0195
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/obstruction.rs`

- file: [code/rust/src/wdp/obstruction.rs](../../../code/rust/src/wdp/obstruction.rs)
- sha256 (`bytes`): `d4a9514b3ee22c73ac47193206838c49cd5d908485d2c38dd026cd3bd9416cf8`
- cited in: record TFQ-0346 (shared)
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_homology/src/chain_map.rs`

- file: `omega_engine/crates_rs/omega_homology/src/chain_map.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_homology/src/integral_chain_equivalence.rs`

- file: `omega_engine/crates_rs/omega_homology/src/integral_chain_equivalence.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/01_pregenesis/tfq_0375_chain_retraction_old_class.md`

- file: [dag/derivations/01_pregenesis/tfq_0375_chain_retraction_old_class.md](../../../dag/derivations/01_pregenesis/tfq_0375_chain_retraction_old_class.md)
- sha256 (`lf-normalised`): `6c66f7f52cd55a5c81e088f88245875f698adbf9b4fc78c2c35d1d4e6e366f41`
- generated view: listed, not counted
- cited in: record TFQ-0375
- counts toward the grade: no

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0337_record_homology_injectivity_under_a_chain_map_retraction_and_record_that_the_two_point.md`

- file: [dag/derivations/05_mssn_sn/tfq_0337_record_homology_injectivity_under_a_chain_map_retraction_and_record_that_the_two_point.md](../../../dag/derivations/05_mssn_sn/tfq_0337_record_homology_injectivity_under_a_chain_map_retraction_and_record_that_the_two_point.md)
- sha256 (`lf-normalised`): `0c09bf4ad8e9d5d94de08a6902582cbe615fcb572c696c53d1f7ffc2540a4946`
- generated view: listed, not counted
- cited in: record TFQ-0337
- counts toward the grade: no

### Documents and data: `dag/derivations/06_wdp/tfq_0346_do_not_lower_phi1_by_passing_to_a_larger_complex_attaching_faces.md`

- file: [dag/derivations/06_wdp/tfq_0346_do_not_lower_phi1_by_passing_to_a_larger_complex_attaching_faces.md](../../../dag/derivations/06_wdp/tfq_0346_do_not_lower_phi1_by_passing_to_a_larger_complex_attaching_faces.md)
- sha256 (`lf-normalised`): `6b435bb1723d6faae4828b1c28409220469504c82b119f60d2b15a2e2d5fdab4`
- generated view: listed, not counted
- cited in: record TFQ-0346 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/22_implementation_sibling/tfq_0195_use_finite_rational_homology_and_simplicial_complexes_as_carriers_not_as_a.md`

- file: [dag/derivations/22_implementation_sibling/tfq_0195_use_finite_rational_homology_and_simplicial_complexes_as_carriers_not_as_a.md](../../../dag/derivations/22_implementation_sibling/tfq_0195_use_finite_rational_homology_and_simplicial_complexes_as_carriers_not_as_a.md)
- sha256 (`lf-normalised`): `cf8f2843c9f722335b7bf30c649ba760c2e0921ed9f900664b560e81e7744840`
- generated view: listed, not counted
- cited in: record TFQ-0195
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/paper_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/paper_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0195 python: not located
- TFQ-0195 rust: no local rust twin located for omega_engine/crates_rs/omega_homology/src/chain_map.rs
- TFQ-0195 rust: no local rust twin located for omega_engine/crates_rs/omega_homology/src/cochain_primitive_difference.rs
- TFQ-0195 rust: no local rust twin located for omega_engine/crates_rs/omega_homology/src/finite_rational_homology.rs
- TFQ-0337 lean4: no local lean twin located for lean4/Imported/SnMssn/Paper001.lean
- TFQ-0337 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/code/sn_mssn_checks.py
- TFQ-0375 lean4: declaration obligation: chain_retraction_cannot_kill on a declared ChainFragment
- TFQ-0375 lean4: no local lean twin located for lean4/Imported/PreGenesisToMssn/Paper.lean
- TFQ-0375 python: missing obligation: graph_homology_ranks on the two named complexes, without a retraction that kills the old class
- TFQ-0375 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/preservation.py
- TFQ-0375 rust: missing obligation: chain-retraction check for the two-point graph and the attached triangle in crate pre_mssn_preservation

## Routes

Incoming (1):

- `PG-R-CHAIN-RETRACTION` `DERIVED_LEAN`: [PG-FREE-MONOID-NONISO](PG-FREE-MONOID-NONISO.md) (PROVED_LEAN)

Outgoing (3):

- `PG-R-GROWTH` `DERIVED_LEAN`: [PG-WDP-GROWTH-NO-REPAIR](PG-WDP-GROWTH-NO-REPAIR.md) (PROVED_LEAN)
- `PGW-R-MSSN-ROWS-1-TO-6-SPECIFIED` `DERIVED_PROSE`: [PGW-MSSN-ROWS-1-TO-6-SPECIFIED](PGW-MSSN-ROWS-1-TO-6-SPECIFIED.md) (DEFINITION)
- `UDG-R-TFQ-0376` `GAP_NO_DERIVATION`: [TFQ-0376](TFQ-0376.md) (OPEN)
