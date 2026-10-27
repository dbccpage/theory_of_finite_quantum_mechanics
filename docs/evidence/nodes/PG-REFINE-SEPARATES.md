# PG-REFINE-SEPARATES

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A supplied tag t separates a collapsed pair exactly when it differs there, and the refined report (q, t) keeps q as its first projection and never merges what q separated. For a conflict relation inside the collapse of q, some b-bit tag resolves every conflict iff the relation has a proper 2^b-colouring (an odd closed walk forbids one bit; a finite type with all pairs in conflict needs ceil(log2 m) bits). Finding such a tag, its cost, and the one-bit converse (Konig) in the kernel are not addressed.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 15
- distinct cited Lean declarations covered by a current replay receipt: 15
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

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

### Lean: `lean4/Imported/PreGenesisToMssn/Paper.lean`

- file: [lean4/Imported/PreGenesisToMssn/Paper.lean](../../../lean4/Imported/PreGenesisToMssn/Paper.lean)
- sha256 (`bytes`): `95b210aaa49b592cff7b6c3c53ec558b3e50cebaae659c3df48b25f5ef48c687`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.PreGenesisToMssn.Paper`): recorded sha256 `95b210aaa49b592cff7b6c3c53ec558b3e50cebaae659c3df48b25f5ef48c687` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/PreGenesisToMssn/Paper.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `refine_separates` | yes | yes | yes | none | `#print axioms refine_separates` |

- counts toward the grade: yes

### Lean: `lean4/Imported/SnMssn/Paper001.lean`

- file: [lean4/Imported/SnMssn/Paper001.lean](../../../lean4/Imported/SnMssn/Paper001.lean)
- sha256 (`bytes`): `fdb943d23939f39abef9dab6b2dd9f3936cd23c0df02f4453ecf369e3b1a3e51`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.SnMssn.Paper001`): recorded sha256 `fdb943d23939f39abef9dab6b2dd9f3936cd23c0df02f4453ecf369e3b1a3e51` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/SnMssn/Paper001.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `supplied_tag_separates` | yes | yes | yes | none | `#print axioms supplied_tag_separates` |

- counts toward the grade: yes

### Lean: `lean4/RefineSeparates.lean`

- file: [lean4/RefineSeparates.lean](../../../lean4/RefineSeparates.lean)
- sha256 (`bytes`): `27eb996394f29091540847f284ccfb33e220f0e6d25974810e9888ff4223a5ea`
- cited in: node.lean, receipt dag/research/pfp_batch01_lean_replay.json (RefineSeparates)
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

### Documents and data: `atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md`

- file: [atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md](../../../atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md)
- sha256 (`lf-normalised`): `a4a7d840b11e912896032aebc9ead95f7978c0e6f60656f44645c6d8fadf593b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/paper_claim_ledger.md`

- file: [atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/paper_claim_ledger.md](../../../atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/paper_claim_ledger.md)
- sha256 (`lf-normalised`): `ca7ad135453d393688ceadf73eb214ccc6976589928f1dc43597e287bbfc6209`
- cited in: node.source
- counts toward the grade: yes

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

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`

## Absences recorded by the TFQ records

- TFQ-0334 lean4: no local lean twin located for atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/lean4/Paper001.lean
- TFQ-0334 python: no local python twin located for atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/code/sn_mssn_checks.py
- TFQ-0334 python: no local python twin located for atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/code/tests/test_sn_mssn_checks.py
- TFQ-0370 lean4: declaration obligation: refine_separates, one supplied tag, one collapsed pair
- TFQ-0370 lean4: no local lean twin located for atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/lean4/Paper.lean
- TFQ-0370 python: missing obligation: preservation.refine must take the tag as an argument and must not search for a tag
- TFQ-0370 python: no local python twin located for atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/code/preservation.py
- TFQ-0370 rust: missing obligation: a supplied-tag splitter in crate pre_mssn_preservation with the tag passed in, not chosen inside the function

## Routes

Incoming (1):

- `PG-R-REFINE` `DERIVED_LEAN`: [PG-COLLAPSE-BARRIER](PG-COLLAPSE-BARRIER.md) (PROVED_LEAN), [PG-DEMAND-ACCOUNTING](PG-DEMAND-ACCOUNTING.md) (PROVED_LEAN)

Outgoing (1):

- `PG-R-OLD-IMAGE` `DERIVED_LEAN`: [PG-OLD-IMAGE-INJECTIVE](PG-OLD-IMAGE-INJECTIVE.md) (PROVED_LEAN)
