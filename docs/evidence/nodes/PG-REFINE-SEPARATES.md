# PG-REFINE-SEPARATES

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A supplied tag t separates a collapsed pair exactly when it differs there, and the refined report (q, t) keeps q as its first projection and never merges what q separated. For a conflict relation inside the collapse of q, some b-bit tag resolves every conflict iff the relation has a proper 2^b-colouring (an odd closed walk forbids one bit; a finite type with all pairs in conflict needs ceil(log2 m) bits). Finding such a tag, its cost, and the one-bit converse (Konig) in the kernel are not addressed.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 16
- distinct cited Lean declarations covered by a current replay receipt: 16
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

- `receipt_names_uncited_module`: a replay receipt names this node for lean4/RefineSeparates.lean, but the node's lean, rust and source fields do not cite it. A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence).

## Imported structure

- Supplied tag (assumption)

## Bottleneck

Tag supply is an input; the node establishes existence criteria only, with no algorithm or complexity statement for finding a tag.

## Source status

Section 9 - binary support and observation refinement; WDP-P001-004 proved

## Review

- PFP review: [dag/results/PG-REFINE-SEPARATES/reviews/20261021_batch01b_audit/delivery_review_result.json](../../../dag/results/PG-REFINE-SEPARATES/reviews/20261021_batch01b_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: For a report q and a conflict relation C inside its collapse, SOME b-bit tag resolves all conflicts iff C has a proper 2^b-colouring (refine_separates_many); a GIVEN tag resolves C iff it is proper (resolves_iff_proper). The source refine_separates is the forward direction for one pair; refine_separates_iff is the one-pair equivalence on collapsed pairs.
  - does not support: Any algorithm, complexity or guarantee for FINDING a tag (the tables and the iff are existence statements, not search procedures); which tag a host should supply; the converse of the odd-closed-walk theorem in the kernel (Konig; native only); conflict graphs on more than 5 vertices beyond the 14 named ones; infinite carriers; any measurement, physical or interpretive reading of tags.
  - next test: First prove in Lean the converse of no_one_bit_of_odd_cycle (a finite symmetric conflict relation with no odd closed walk has a proper Bool tag), then that breadth-first 2-colouring is sound and complete for deciding it, as the first algorithmic statement about finding a tag; the present node establishes existence criteria only.

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

### Lean: `lean4/Imported/PreGenesisToMssn/Paper.lean`

- file: [lean4/Imported/PreGenesisToMssn/Paper.lean](../../../lean4/Imported/PreGenesisToMssn/Paper.lean)
- sha256 (`bytes`): `5f0ebfc1710b91ce84d4570d7653a3cb8396824adecfaba16fa59a96354b9e12`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.PreGenesisToMssn.Paper`): recorded sha256 `5f0ebfc1710b91ce84d4570d7653a3cb8396824adecfaba16fa59a96354b9e12` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/PreGenesisToMssn/Paper.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `refine_separates` | yes | yes | yes | none | `#print axioms refine_separates` |

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
| `supplied_tag_separates` | yes | yes | yes | none | `#print axioms supplied_tag_separates` |

- counts toward the grade: yes

### Lean: `lean4/RefineSeparates.lean`

- file: [lean4/RefineSeparates.lean](../../../lean4/RefineSeparates.lean)
- sha256 (`bytes`): `27eb996394f29091540847f284ccfb33e220f0e6d25974810e9888ff4223a5ea`
- cited in: receipt dag/research/pfp_batch01_lean_replay.json (RefineSeparates)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `RefineSeparates`): recorded sha256 `27eb996394f29091540847f284ccfb33e220f0e6d25974810e9888ff4223a5ea` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build RefineSeparates`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `RefineSeparates.bits_iff_colours` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RefineSeparates.bits_iff_colours` |
| `RefineSeparates.fibre_bits_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RefineSeparates.fibre_bits_iff` |
| `RefineSeparates.fibre_one_bit_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RefineSeparates.fibre_one_bit_iff` |
| `RefineSeparates.fibre_report_bits_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RefineSeparates.fibre_report_bits_iff` |
| `RefineSeparates.no_one_bit_of_odd_cycle` | yes | yes | yes | Quot.sound, propext | `#print axioms RefineSeparates.no_one_bit_of_odd_cycle` |
| `RefineSeparates.proper_union` | yes | yes | yes | none | `#print axioms RefineSeparates.proper_union` |
| `RefineSeparates.refine_keeps_old_separation` | yes | yes | yes | none | `#print axioms RefineSeparates.refine_keeps_old_separation` |
| `RefineSeparates.refine_retains` | yes | yes | yes | none | `#print axioms RefineSeparates.refine_retains` |
| `RefineSeparates.refine_separates` | yes | yes | yes | none | `#print axioms RefineSeparates.refine_separates` |
| `RefineSeparates.refine_separates_iff` | yes | yes | yes | propext | `#print axioms RefineSeparates.refine_separates_iff` |
| `RefineSeparates.refine_separates_many` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RefineSeparates.refine_separates_many` |
| `RefineSeparates.resolves_iff_proper` | yes | yes | yes | propext | `#print axioms RefineSeparates.resolves_iff_proper` |
| `RefineSeparates.triangle_no_one_bit` | yes | yes | yes | Quot.sound, propext | `#print axioms RefineSeparates.triangle_no_one_bit` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/01_pregenesis/tfq_0370_supplied_binary_refinement.md`

- file: [dag/derivations/01_pregenesis/tfq_0370_supplied_binary_refinement.md](../../../dag/derivations/01_pregenesis/tfq_0370_supplied_binary_refinement.md)
- sha256 (`lf-normalised`): `6231decd1f0d8bbd2343b5bc2c4302aef0b8b5ef431b29b2ba9e7a947c835a56`
- generated view: listed, not counted
- cited in: record TFQ-0370
- counts toward the grade: no

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0334_let_one_supplied_binary_tag_separate_one_collapsed_pair_and_keep_the.md`

- file: [dag/derivations/05_mssn_sn/tfq_0334_let_one_supplied_binary_tag_separate_one_collapsed_pair_and_keep_the.md](../../../dag/derivations/05_mssn_sn/tfq_0334_let_one_supplied_binary_tag_separate_one_collapsed_pair_and_keep_the.md)
- sha256 (`lf-normalised`): `736fd2f68c58d965418ee2bba17e283a397b821777bac6e9b65021a3f5d88def`
- generated view: listed, not counted
- cited in: record TFQ-0334
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

- TFQ-0334 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean
- TFQ-0334 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/code/sn_mssn_checks.py
- TFQ-0334 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/code/tests/test_sn_mssn_checks.py
- TFQ-0370 lean4: declaration obligation: refine_separates, one supplied tag, one collapsed pair
- TFQ-0370 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean
- TFQ-0370 python: missing obligation: preservation.refine must take the tag as an argument and must not search for a tag
- TFQ-0370 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/preservation.py
- TFQ-0370 rust: missing obligation: a supplied-tag splitter in crate pre_mssn_preservation with the tag passed in, not chosen inside the function

## Routes

Incoming (1):

- `PG-R-REFINE` `DERIVED_LEAN`: [PG-COLLAPSE-BARRIER](PG-COLLAPSE-BARRIER.md) (PROVED_LEAN), [PG-DEMAND-ACCOUNTING](PG-DEMAND-ACCOUNTING.md) (PROVED_LEAN)

Outgoing (1):

- `PG-R-OLD-IMAGE` `DERIVED_LEAN`: [PG-OLD-IMAGE-INJECTIVE](PG-OLD-IMAGE-INJECTIVE.md) (PROVED_LEAN)
