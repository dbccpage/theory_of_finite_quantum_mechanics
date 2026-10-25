# PG-FREE-MONOID-NONISO

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Free monoids on alphabets of different finite sizes are not isomorphic (a monoid isomorphism induces a bijection of alphabets via atoms; in general FreeMonoid a is isomorphic to FreeMonoid b iff a and b are in bijection), and discrete categories with different finite object counts are not equivalent. The underlying sets of nonempty free monoids are in bijection, so a numeral/alphabet re-presentation can be a set bijection but cannot be an isomorphism of the free-monoid multiplication or an equivalence of discrete categories; other structures are not addressed.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 18
- cited Lean declaration references covered by a current replay receipt: 18
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

- `receipt_names_uncited_module`: a replay receipt names this node for lean4/FreeMonoidNoniso.lean, but the node's lean, rust and source fields do not cite it. A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence).

## Imported structure

None recorded.

## Bottleneck

The obstruction is multiplicativity via atoms, not cardinality; Classical.choice is used for the isomorphism-to-alphabet-bijection direction; structures other than free-monoid multiplication and discrete categories are unaddressed.

## Source status

Theorem 5 / WDP-P001-007, -008 proved

## Review

- PFP review: [dag/results/PG-FREE-MONOID-NONISO/reviews/20261021_batch01a_audit/delivery_review_result.json](../../../dag/results/PG-FREE-MONOID-NONISO/reviews/20261021_batch01a_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: A monoid isomorphism between free monoids on any two alphabets induces a bijection of the alphabets, so free monoids on finite alphabets of different sizes are not isomorphic and discrete categories with different finite object counts are not equivalent; a bare bijection of the underlying sets does exist for sizes at least one, so a numeral or alphabet re-presentation cannot be an isomorphism of the free-monoid (word concatenation) structure or of the discrete-category structure; other structures are not addressed.
  - does not support: Any structure on numerals or alphabets other than the free-monoid multiplication or the discrete category (a numeral or alphabet re-presentation may still be a non-isomorphic map, a set bijection, or an isomorphism of some other structure; no other structure, such as free commutative monoids, is examined); language restriction, partial recovery and total erasure (separate ledger row WDP-P001-009); infinite alphabets beyond the general Lean statement; the native homomorphism search covers short generator images only and is an instance, not the general theorem.
  - next test: Decide which numeral or alphabet re-presentations ARE structure-preserving: classify the monoid homomorphisms between free monoids on different alphabet sizes that are injective (codes) or onto (decoders), and prove which of them preserve atoms, as the next step beyond the isomorphism obstruction proved here.

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
| `QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition` |

- counts toward the grade: yes

### Lean: `lean4/FreeMonoidNoniso.lean`

- file: [lean4/FreeMonoidNoniso.lean](../../../lean4/FreeMonoidNoniso.lean)
- sha256 (`bytes`): `97453073da4c402585e900368fd9f71837da6621bc43bd43d9cd409b67027990`
- cited in: receipt dag/research/pfp_batch01_lean_replay.json (FreeMonoidNoniso)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `FreeMonoidNoniso`): recorded sha256 `97453073da4c402585e900368fd9f71837da6621bc43bd43d9cd409b67027990` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FreeMonoidNoniso`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FreeMonoidNoniso.alphabetEquiv` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FreeMonoidNoniso.alphabetEquiv` |
| `FreeMonoidNoniso.bijection_but_not_isomorphic` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FreeMonoidNoniso.bijection_but_not_isomorphic` |
| `FreeMonoidNoniso.card_atoms` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FreeMonoidNoniso.card_atoms` |
| `FreeMonoidNoniso.card_words_of_length` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FreeMonoidNoniso.card_words_of_length` |
| `FreeMonoidNoniso.discrete_equivalence_card` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FreeMonoidNoniso.discrete_equivalence_card` |
| `FreeMonoidNoniso.discrete_equivalence_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FreeMonoidNoniso.discrete_equivalence_iff` |
| `FreeMonoidNoniso.freeMonoid_iso_iff_equiv` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FreeMonoidNoniso.freeMonoid_iso_iff_equiv` |
| `FreeMonoidNoniso.free_monoid_zero_subsingleton` | yes | yes | yes | Quot.sound | `#print axioms FreeMonoidNoniso.free_monoid_zero_subsingleton` |
| `FreeMonoidNoniso.isAtom_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms FreeMonoidNoniso.isAtom_iff` |
| `FreeMonoidNoniso.isAtom_map_iff` | yes | yes | yes | Quot.sound | `#print axioms FreeMonoidNoniso.isAtom_map_iff` |
| `FreeMonoidNoniso.no_discrete_equivalence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FreeMonoidNoniso.no_discrete_equivalence` |
| `FreeMonoidNoniso.no_free_monoid_iso` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FreeMonoidNoniso.no_free_monoid_iso` |
| `FreeMonoidNoniso.set_bijection_exists` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FreeMonoidNoniso.set_bijection_exists` |
| `FreeMonoidNoniso.unequal_finite_alphabets_not_wordiso` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FreeMonoidNoniso.unequal_finite_alphabets_not_wordiso` |

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
| `unequal_finite_alphabets_not_iso` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms unequal_finite_alphabets_not_iso` |

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
| `no_discrete_equivalence` | yes | yes | yes | Quot.sound, propext | `#print axioms no_discrete_equivalence` |
| `no_free_monoid_iso` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms no_free_monoid_iso` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/01_pregenesis/tfq_0373_free_monoid_size_noniso.md`

- file: [dag/derivations/01_pregenesis/tfq_0373_free_monoid_size_noniso.md](../../../dag/derivations/01_pregenesis/tfq_0373_free_monoid_size_noniso.md)
- sha256 (`lf-normalised`): `5c9113aaf9f6d099a9aa0cb79ff70df7d5bdd80c8fa4c6254ccbcbd8aa648c69`
- generated view: listed, not counted
- cited in: record TFQ-0373
- counts toward the grade: no

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0336_keep_unequal_finite_alphabets_from_a_free_monoid_isomorphism_and_keep_language_restriction.md`

- file: [dag/derivations/05_mssn_sn/tfq_0336_keep_unequal_finite_alphabets_from_a_free_monoid_isomorphism_and_keep_language_restriction.md](../../../dag/derivations/05_mssn_sn/tfq_0336_keep_unequal_finite_alphabets_from_a_free_monoid_isomorphism_and_keep_language_restriction.md)
- sha256 (`lf-normalised`): `8eae86d8a681cfe018680dead98addbe03bb1b79bfe4154e7a03ca9fbd3e76b0`
- generated view: listed, not counted
- cited in: record TFQ-0336
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

- TFQ-0336 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean
- TFQ-0336 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean
- TFQ-0336 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/code/sn_mssn_checks.py
- TFQ-0373 lean4: declaration obligation: unequal_finite_alphabets_not_iso for unequal finite alphabet sizes
- TFQ-0373 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean
- TFQ-0373 python: missing obligation: a size comparison beside free_reduce in preservation.py that refuses an isomorphism when alphabet sizes differ
- TFQ-0373 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/tests/test_free_words.py
- TFQ-0373 rust: missing obligation: finite-alphabet non-isomorphism in crate pre_mssn_preservation

## Routes

Incoming (1):

- `PG-R-MONOID-NONISO` `DERIVED_LEAN`: [PG-SN-CARRIER](PG-SN-CARRIER.md) (PROVED_LEAN)

Outgoing (5):

- `APP-R-AUTH-DTM1-TOKEN-CODE-ROUNDTRIP` `DERIVED_LEAN`: [AUTH-DTM1-TOKEN-CODE-ROUNDTRIP](AUTH-DTM1-TOKEN-CODE-ROUNDTRIP.md) (PROVED_LEAN)
- `APP-R-COMP-C2-WORD-REWRITING` `DERIVED_PROSE`: [COMP-C2-WORD-REWRITING](COMP-C2-WORD-REWRITING.md) (DEFINITION)
- `APP-R-COMP-C8-BINARY-CODING` `DERIVED_LEAN`: [COMP-C8-BINARY-CODING](COMP-C8-BINARY-CODING.md) (PROVED_LEAN)
- `PG-R-CHAIN-RETRACTION` `DERIVED_LEAN`: [PG-CHAIN-RETRACTION](PG-CHAIN-RETRACTION.md) (PROVED_LEAN)
- `UDG-R-TFQ-0374` `GAP_NO_DERIVATION`: [TFQ-0374](TFQ-0374.md) (OPEN)
