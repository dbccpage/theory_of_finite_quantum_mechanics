# PGW-IDENTITY-CONVENTION-UNDECIDABLE

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Whether \<a\> supplied after \<\> is a new state depends on an identity convention that no prompt had declared. Under the opaque convention a state is what the regime can tell apart, and with O empty \<\> and \<a\> are not told apart; under the exact-inscription convention a state is the inscription itself, the strings differ, and the regime has one more syntactic state. Trials 1 and 2 answered under the first convention and the full replay under the second, calling \<a\> a new state. The analysis keeps both branches and records the effect as undecidable until one convention is declared.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 14
- distinct cited Lean declarations covered by a current replay receipt: 14
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- A declared identity convention, opaque or exact-inscription, chosen by the host (assumption)

## Bottleneck

The observer family and interpretation of identity are declared. This is logical dependence on a convention, not a computability undecidability theorem, a preferred identity convention, or a replay of the historical model responses. It grants no operational or physical authority. Original target retained as an obligation: Whether \<a\> supplied after \<\> is a new state depends on an identity convention that no prompt had declared. Under the opaque convention a state is what the regime can tell apart, and with O empty \<\> and \<a\> are not told apart; under the exact-inscription convention a state is the inscription itself, the strings differ, and the regime has one more syntactic state. Trials 1 and 2 answered under the first convention and the full replay under the second, calling \<a\> a new state. The analysis keeps both branches and records the effect as undecidable until one convention is declared. Prior boundary: Records that the answer is relative to the convention; it does not choose one, and the three replies are behaviour of one unrecorded model, not evidence for either convention.

## Source status

v1 Red round item 1 (conditional verdict); 000_oepregen 03_results_and_arguments.md section 2 and 02_trial_record.md Prompt 12; current Lean observer-family theorem and exact/empty-family inscription comparison, with original CONDITIONAL status retained

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignIdentityConvention.lean`

- file: [lean4/CampaignIdentityConvention.lean](../../../lean4/CampaignIdentityConvention.lean)
- sha256 (`bytes`): `fa42557ad55d2b9150bea0a4c9d38a205d41e2d688115bb71091d0b96c6f8ff6`
- cited in: node.lean, receipt dag/research/campaign_pgw-identity-convention-undecidable_lean_replay.json (CampaignIdentityConvention), record TFQ-0423
- replay: `verified`
  - receipt [dag/research/campaign_pgw-identity-convention-undecidable_lean_replay.json](../../../dag/research/campaign_pgw-identity-convention-undecidable_lean_replay.json) (module `CampaignIdentityConvention`): recorded sha256 `fa42557ad55d2b9150bea0a4c9d38a205d41e2d688115bb71091d0b96c6f8ff6` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignIdentityConvention`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignIdentityConvention.Indistinguishable` | yes | yes | yes | none | `#print axioms CampaignIdentityConvention.Indistinguishable` |
| `CampaignIdentityConvention.IsNew` | yes | yes | yes | none | `#print axioms CampaignIdentityConvention.IsNew` |
| `CampaignIdentityConvention.adding_identity_separates` | yes | yes | yes | none | `#print axioms CampaignIdentityConvention.adding_identity_separates` |
| `CampaignIdentityConvention.empty_family_identifies_all` | yes | yes | yes | none | `#print axioms CampaignIdentityConvention.empty_family_identifies_all` |
| `CampaignIdentityConvention.exactObserver` | yes | yes | yes | none | `#print axioms CampaignIdentityConvention.exactObserver` |
| `CampaignIdentityConvention.exact_inscription_is_new` | yes | yes | yes | none | `#print axioms CampaignIdentityConvention.exact_inscription_is_new` |
| `CampaignIdentityConvention.exact_observer_sees_new` | yes | yes | yes | none | `#print axioms CampaignIdentityConvention.exact_observer_sees_new` |
| `CampaignIdentityConvention.forgetting_preserves_indistinguishability` | yes | yes | yes | none | `#print axioms CampaignIdentityConvention.forgetting_preserves_indistinguishability` |
| `CampaignIdentityConvention.no_convention_independent_answer` | yes | yes | yes | none | `#print axioms CampaignIdentityConvention.no_convention_independent_answer` |
| `CampaignIdentityConvention.observational_equivalence` | yes | yes | yes | none | `#print axioms CampaignIdentityConvention.observational_equivalence` |
| `CampaignIdentityConvention.opaqueObserver` | yes | yes | yes | none | `#print axioms CampaignIdentityConvention.opaqueObserver` |
| `CampaignIdentityConvention.opaque_inscription_is_not_new` | yes | yes | yes | none | `#print axioms CampaignIdentityConvention.opaque_inscription_is_not_new` |
| `CampaignIdentityConvention.opaque_observer_sees_no_new` | yes | yes | yes | none | `#print axioms CampaignIdentityConvention.opaque_observer_sees_no_new` |
| `CampaignIdentityConvention.withIdentity` | yes | yes | yes | none | `#print axioms CampaignIdentityConvention.withIdentity` |

- counts toward the grade: yes

### Python: `checks/independent/pgw-identity-convention-undecidable.py`

- file: [checks/independent/pgw-identity-convention-undecidable.py](../../../checks/independent/pgw-identity-convention-undecidable.py)
- sha256 (`bytes`): `cdb0ef8292785b35a0ec2f28c112fab192b39f91be0d3da290b4ca5774a34b98`
- cited in: record TFQ-0423
- counts toward the grade: yes

### Documents and data: `dag/derivations/01_pregenesis/tfq_0423_identity_convention_undecidable.md`

- file: [dag/derivations/01_pregenesis/tfq_0423_identity_convention_undecidable.md](../../../dag/derivations/01_pregenesis/tfq_0423_identity_convention_undecidable.md)
- sha256 (`lf-normalised`): `8f4757a6b4462dd8ffc9648aaa0141d7303a8801ac9697b9a9694f32afee2e0b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0423
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-identity-convention-undecidable.md`

- file: [dag/derivations/independent/pgw-identity-convention-undecidable.md](../../../dag/derivations/independent/pgw-identity-convention-undecidable.md)
- sha256 (`lf-normalised`): `f87209a164e7f316d94f594c94d2bc044d6db08e596368db6475bb9cf5514b27`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_pgw-identity-convention-undecidable_lean_replay.json`

- file: [dag/research/campaign_pgw-identity-convention-undecidable_lean_replay.json](../../../dag/research/campaign_pgw-identity-convention-undecidable_lean_replay.json)
- sha256 (`lf-normalised`): `efda3ed2fccff1da587fae1da7078f45fa5afe4ec13f9ee9403bb5d5c70e433f`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `omega_engine_education/documentation/000_oepregen/02_trial_record.md`

- file: `omega_engine_education/documentation/000_oepregen/02_trial_record.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/000_oepregen/03_results_and_arguments.md`

- file: `omega_engine_education/documentation/000_oepregen/03_results_and_arguments.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/000_oepregen/sources/analysis_derivation_v1.md`

- file: `omega_engine_education/documentation/000_oepregen/sources/analysis_derivation_v1.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0423 rust: no Rust switch between identity conventions

## Routes

Incoming (1):

- `PGW-R-IDENTITY-CONVENTION-UNDECIDABLE` `CONDITIONAL_ON_IMPORT`: [PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT](PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT.md) (CONDITIONAL)

Outgoing (2):

- `APP-R-COMP-C1-IDENTITY-CONVENTION-INPUT` `CONDITIONAL_ON_IMPORT`: [COMP-C1-IDENTITY-CONVENTION-INPUT](COMP-C1-IDENTITY-CONVENTION-INPUT.md) (IMPORTED_ASSUMPTION)
- `PGW-R-ABSENCE-OF-RULE-NOT-IDENTIFICATION` `DERIVED_PROSE`: [PGW-ABSENCE-OF-RULE-NOT-IDENTIFICATION](PGW-ABSENCE-OF-RULE-NOT-IDENTIFICATION.md) (DEFINITION)
