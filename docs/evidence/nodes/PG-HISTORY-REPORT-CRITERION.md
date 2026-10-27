# PG-HISTORY-REPORT-CRITERION

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A question over histories factors through the report image iff it is constant on report fibers, and the factorization is unique on the image (the extension to all reports is unique iff the report is surjective or the answer set is trivial). The direction constancy =\> factoring is proved from a selector of fiber representatives without any axiom, and with Classical.choice for an arbitrary report; a choice-free version for explicitly listed histories is PG-PREGEN-CONSTRUCTIVE-SUMMARY; necessity of choice for arbitrary history types is not decided.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 15
- distinct cited Lean declarations covered by a current replay receipt: 15
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Classical.choice (assumption: in Paper.lean, per its header comment)

## Bottleneck

Whether Classical.choice is necessary for constancy =\> factoring on arbitrary history types is undecided.

## Source status

Theorem 2 - history report criterion (Lean: history_report_criterion, history_factor_unique)

## Review

- PFP review: [dag/results/PG-HISTORY-REPORT-CRITERION/reviews/20261021_batch01a_audit/delivery_review_result.json](../../../dag/results/PG-HISTORY-REPORT-CRITERION/reviews/20261021_batch01a_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: For arbitrary types, an answer factors through the report image iff it is constant on report fibers, uniquely on the image; the direction constancy =\> factoring is proved from a selector of fiber representatives (a hypothesis, axiom-free) and, for an arbitrary report, with Classical.choice; necessity of a selector or of choice is not shown; verified exhaustively on 16 small function-space triples.
  - does not support: Necessity of a selector or of Classical.choice for the direction constancy =\> factoring (this node establishes no independence or unprovability result; the selector is a hypothesis, not a construction); the constructive listed-history reconstruction (node PG-PREGEN-CONSTRUCTIVE-SUMMARY); any structure on H, V or S, probability, measurement or physical interpretation of reports.
  - next test: Decide whether constancy on fibers =\> factoring through the image is provable without Classical.choice for an arbitrary history type (prove it, or give a choice-free model in which a fiber-constant question fails to factor), beyond the selector hypothesis proved here and the listed-history version of node 166.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/HistoryReport.lean`

- file: [lean4/HistoryReport.lean](../../../lean4/HistoryReport.lean)
- sha256 (`bytes`): `420e89ea7590479d90d1a16e9cea9b70f634e5dfc18d283397143f8c06773c0f`
- cited in: node.lean, receipt dag/research/pfp_batch01_lean_replay.json (HistoryReport)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `HistoryReport`): recorded sha256 `420e89ea7590479d90d1a16e9cea9b70f634e5dfc18d283397143f8c06773c0f` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build HistoryReport`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `HistoryReport.extension_unique_of_surjective` | yes | yes | yes | Quot.sound | `#print axioms HistoryReport.extension_unique_of_surjective` |
| `HistoryReport.factor_unique_on_image` | yes | yes | yes | Quot.sound | `#print axioms HistoryReport.factor_unique_on_image` |
| `HistoryReport.factors_of_fiberConstant_of_selector` | yes | yes | yes | none | `#print axioms HistoryReport.factors_of_fiberConstant_of_selector` |
| `HistoryReport.fiberConstant_of_factors` | yes | yes | yes | none | `#print axioms HistoryReport.fiberConstant_of_factors` |
| `HistoryReport.history_report_criterion` | yes | yes | yes | Classical.choice | `#print axioms HistoryReport.history_report_criterion` |
| `HistoryReport.instance_split` | yes | yes | yes | propext | `#print axioms HistoryReport.instance_split` |
| `HistoryReport.not_factors_of_split` | yes | yes | yes | none | `#print axioms HistoryReport.not_factors_of_split` |
| `HistoryReport.off_image_not_unique` | yes | yes | yes | none | `#print axioms HistoryReport.off_image_not_unique` |
| `HistoryReport.selector_exists` | yes | yes | yes | Classical.choice | `#print axioms HistoryReport.selector_exists` |

- counts toward the grade: yes

### Lean: `lean4/Imported/PreGenesisToMssn/Paper.lean`

- file: [lean4/Imported/PreGenesisToMssn/Paper.lean](../../../lean4/Imported/PreGenesisToMssn/Paper.lean)
- sha256 (`bytes`): `95b210aaa49b592cff7b6c3c53ec558b3e50cebaae659c3df48b25f5ef48c687`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.PreGenesisToMssn.Paper`): recorded sha256 `95b210aaa49b592cff7b6c3c53ec558b3e50cebaae659c3df48b25f5ef48c687` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/PreGenesisToMssn/Paper.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `history_factor_unique` | yes | yes | yes | Quot.sound | `#print axioms history_factor_unique` |
| `history_report_criterion` | yes | yes | yes | Classical.choice | `#print axioms history_report_criterion` |

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
| `descent_unique` | yes | yes | yes | none | `#print axioms descent_unique` |
| `exists_descent_of_constant` | yes | yes | yes | Classical.choice | `#print axioms exists_descent_of_constant` |

- counts toward the grade: yes

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/Descent.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/Descent.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Descent.lean)
- sha256 (`bytes`): `2e0971ee2a47dac5047bfc00ae2ee90f3241ad6142a7ea1b8b90cb03b4c3b5e1`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.WitnessedDifference.WitnessedDifference.Descent`): recorded sha256 `2e0971ee2a47dac5047bfc00ae2ee90f3241ad6142a7ea1b8b90cb03b4c3b5e1` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/Descent.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `function_descends_iff_fiber_constant` | yes | yes | yes | Classical.choice | `#print axioms function_descends_iff_fiber_constant` |

- counts toward the grade: yes

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/ProposalAdmissionBridge.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/ProposalAdmissionBridge.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/ProposalAdmissionBridge.lean)
- sha256 (`bytes`): `96cc6757237ae9cfcc72783b985ad3f8b77e0452928dc43cf0a2f653475248a2`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.WitnessedDifference.WitnessedDifference.ProposalAdmissionBridge`): recorded sha256 `96cc6757237ae9cfcc72783b985ad3f8b77e0452928dc43cf0a2f653475248a2` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/ProposalAdmissionBridge.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `factorization_iff_fiber_constancy` | yes | yes | yes | Classical.choice | `#print axioms factorization_iff_fiber_constancy` |

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

### Documents and data: `dag/derivations/01_pregenesis/tfq_0366_history_report_fiber_criterion.md`

- file: [dag/derivations/01_pregenesis/tfq_0366_history_report_fiber_criterion.md](../../../dag/derivations/01_pregenesis/tfq_0366_history_report_fiber_criterion.md)
- sha256 (`lf-normalised`): `9c4e2c7072b28d74e69d34e85592d8759f1f95b2456517a9d497e59d4a279086`
- generated view: listed, not counted
- cited in: record TFQ-0366
- counts toward the grade: no

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0338_descend_a_question_to_the_realized_report_image_exactly_when_it_is.md`

- file: [dag/derivations/05_mssn_sn/tfq_0338_descend_a_question_to_the_realized_report_image_exactly_when_it_is.md](../../../dag/derivations/05_mssn_sn/tfq_0338_descend_a_question_to_the_realized_report_image_exactly_when_it_is.md)
- sha256 (`lf-normalised`): `7a0ac07464e815ab7eb78ca28b9b4b90feb864cceb6e5308be9d0151826054cc`
- generated view: listed, not counted
- cited in: record TFQ-0338
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- `external:sha256:c9695009f0223f680802cec81590d681e386060da9a98d7715878b885bda6700::FactorizationCertificate`

## Absences recorded by the TFQ records

- TFQ-0338 lean4: no local lean twin located for atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/lean4/Paper001.lean
- TFQ-0338 python: no local python twin located for atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/code/sn_mssn_checks.py
- TFQ-0366 lean4: declaration obligation: history_report_criterion and history_factor_unique, with Classical.choice left visible on the unlisted direction
- TFQ-0366 lean4: no local lean twin located for atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/lean4/Paper.lean
- TFQ-0366 python: missing obligation: preservation.report_factor must be checked against fiber constancy and must return no factor off the image
- TFQ-0366 python: no local python twin located for atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/code/preservation.py
- TFQ-0366 rust: missing obligation: a report-factor checker in crate pre_mssn_preservation that refuses answers outside the realized image

## Routes

Incoming (1):

- `PG-R-HISTORY-CRITERION` `DERIVED_LEAN`: [PG-COLLAPSE-BARRIER](PG-COLLAPSE-BARRIER.md) (PROVED_LEAN), [PG-GEN-NO-RETURN](PG-GEN-NO-RETURN.md) (PROVED_LEAN)

Outgoing (6):

- `APP-R-AUTH-TC0-TAPE-CONTROL-TYPING` `COMPUTED`: [AUTH-TC0-TAPE-CONTROL-TYPING](AUTH-TC0-TAPE-CONTROL-TYPING.md) (COMPUTATIONALLY_CHECKED)
- `FRO-R-CT-FINITE-DISTINGUISHABILITY-REPORT-FIBERS` `DERIVED_LEAN`: [CT-FINITE-DISTINGUISHABILITY-REPORT-FIBERS](CT-FINITE-DISTINGUISHABILITY-REPORT-FIBERS.md) (PROVED_LEAN)
- `PG-R-CONSTRUCTIVE-SUMMARY` `DERIVED_LEAN`: [PG-PREGEN-CONSTRUCTIVE-SUMMARY](PG-PREGEN-CONSTRUCTIVE-SUMMARY.md) (PROVED_LEAN)
- `PG-R-PROTECTED` `DERIVED_LEAN`: [PG-WDP-PROTECTED-QUESTIONS](PG-WDP-PROTECTED-QUESTIONS.md) (PROVED_LEAN)
- `PGW-R-REPLAY-NECESSITY` `DERIVED_LEAN`: [PGW-REPLAY-NECESSITY](PGW-REPLAY-NECESSITY.md) (PROVED_LEAN)
- `PGW-R-WDP-OBSERVER-QUOTIENT-PASSIVITY` `DERIVED_PROSE`: [PGW-WDP-OBSERVER-QUOTIENT-PASSIVITY](PGW-WDP-OBSERVER-QUOTIENT-PASSIVITY.md) (DEFINITION)
