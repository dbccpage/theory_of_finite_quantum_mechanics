# PGW-IDENTITY-CONVENTION-UNDECIDABLE

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Whether \<a\> supplied after \<\> is a new state depends on an identity convention that no prompt had declared. Under the opaque convention a state is what the regime can tell apart, and with O empty \<\> and \<a\> are not told apart; under the exact-inscription convention a state is the inscription itself, the strings differ, and the regime has one more syntactic state. Trials 1 and 2 answered under the first convention and the full replay under the second, calling \<a\> a new state. The analysis keeps both branches and records the effect as undecidable until one convention is declared.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 12
- cited Lean declarations covered by a current replay receipt: 11
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- A declared identity convention, opaque or exact-inscription, chosen by the host (assumption)

## Bottleneck

Records that the answer is relative to the convention; it does not choose one, and the three replies are behaviour of one unrecorded model, not evidence for either convention. Narrowed in lean4/CampaignPgwIdentityConventionUndecidable.lean and checks/independent/pgw-identity-convention-undecidable.py: models observation-family regimes PreGenesisRegime alpha beta with supplyInscription preserving obs (O_1 = O_0) and enlarging presented.card by +1, links obsProfile equality to PreMssn.Observation.SameProfile and genesisUnaryProfile equality to GenesisComputation.Collapsed, checks the Prompt 12 branch split (false with delta = 0 under opaqueConv vs true with delta = +1 under exactInscription, and undecidableWithoutConvention false true when no convention is declared), establishes agreement on profile-injective regimes, and keeps the host-declared identity convention as an explicit import (status remains CONDITIONAL).

## Source status

v1 Red round item 1 (conditional verdict); 000_oepregen 03_results_and_arguments.md section 2 and 02_trial_record.md Prompt 12

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignPgwIdentityConventionUndecidable.lean`

- file: [lean4/CampaignPgwIdentityConventionUndecidable.lean](../../../lean4/CampaignPgwIdentityConventionUndecidable.lean)
- sha256 (`bytes`): `a3bb1c027c2e3421e71fa2dbb67bca6a1d60e9c33dfdcb181d07bfd157b4bc09`
- cited in: node.lean, record TFQ-0423
- replay: `verified`
  - receipt [dag/research/campaign_pgw-identity-convention-undecidable_lean_replay.json](../../../dag/research/campaign_pgw-identity-convention-undecidable_lean_replay.json) (module `CampaignPgwIdentityConventionUndecidable`): recorded sha256 `a3bb1c027c2e3421e71fa2dbb67bca6a1d60e9c33dfdcb181d07bfd157b4bc09` matches the current file; exit code 0; Lean None; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignPgwIdentityConventionUndecidable`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.conventions_agree_iff_fresh_profile` | yes | yes | yes | module-level | `#print axioms CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.conventions_agree_iff_fresh_profile` |
| `CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.genesisUnaryProfile_eq_iff_collapsed` | yes | yes | yes | module-level | `#print axioms CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.genesisUnaryProfile_eq_iff_collapsed` |
| `CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.injective_obsProfile_implies_conventions_coincide` | yes | yes | yes | module-level | `#print axioms CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.injective_obsProfile_implies_conventions_coincide` |
| `CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.no_convention_free_evaluator_fence` | yes | yes | yes | module-level | `#print axioms CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.no_convention_free_evaluator_fence` |
| `CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.obsProfile_eq_iff_sameProfile_and_empty_obs_collapse` | yes | yes | yes | module-level | `#print axioms CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.obsProfile_eq_iff_sameProfile_and_empty_obs_collapse` |
| `CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.opaque_stateCount_le_exact_stateCount` | yes | yes | yes | module-level | `#print axioms CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.opaque_stateCount_le_exact_stateCount` |
| `CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.stateCount_supply_markA_delta_zero_vs_one` | yes | yes | yes | module-level | `#print axioms CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.stateCount_supply_markA_delta_zero_vs_one` |
| `CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.supplyInscription_preserves_obs_and_enlarges_presentation` | yes | yes | yes | module-level | `#print axioms CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.supplyInscription_preserves_obs_and_enlarges_presentation` |
| `CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.supply_markA_after_ground_branch_divergence` | yes | yes | yes | module-level | `#print axioms CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.supply_markA_after_ground_branch_divergence` |
| `CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.trial_votes_do_not_determine_convention_fence` | yes | yes | yes | module-level | `#print axioms CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.trial_votes_do_not_determine_convention_fence` |
| `CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.unformed_vs_firstSeparation_regime_convention_bridge` | yes | yes | yes | module-level | `#print axioms CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.unformed_vs_firstSeparation_regime_convention_bridge` |
- counts toward the grade: yes

### Python: `checks/independent/pgw-identity-convention-undecidable.py`

- file: [checks/independent/pgw-identity-convention-undecidable.py](../../../checks/independent/pgw-identity-convention-undecidable.py)
- sha256 (`bytes`): `b66edcfb325bbf2dbe067be1a5b94ab367810e3788f9d8c7244841ed4a347428`
- cited in: record TFQ-0423

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/01_pregenesis/tfq_0423_identity_convention_undecidable.md`

- file: [dag/derivations/01_pregenesis/tfq_0423_identity_convention_undecidable.md](../../../dag/derivations/01_pregenesis/tfq_0423_identity_convention_undecidable.md)
- sha256 (`lf-normalised`): `9c27c623d546afa80883805d8fc99a5516cad6648914599002bcf28283fed0b4`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0423
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-identity-convention-undecidable.md`

- file: [dag/derivations/independent/pgw-identity-convention-undecidable.md](../../../dag/derivations/independent/pgw-identity-convention-undecidable.md)
- sha256 (`lf-normalised`): `d383e2dfad51c369ebd66efb12828bbe65b647c39b5323665cba307b1e14ae24`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_pgw-identity-convention-undecidable_independent.json`

- file: [dag/research/campaign_pgw-identity-convention-undecidable_independent.json](../../../dag/research/campaign_pgw-identity-convention-undecidable_independent.json)
- sha256 (`lf-normalised`): `ac89924d9263e3000e29e9c18a122eddc388d944a1a21e19b3559a48154fc365`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_pgw-identity-convention-undecidable_lean_mutation.json`

- file: [dag/research/campaign_pgw-identity-convention-undecidable_lean_mutation.json](../../../dag/research/campaign_pgw-identity-convention-undecidable_lean_mutation.json)
- sha256 (`lf-normalised`): `f864dad6da3e8714cff0753b0f477067dbc6a81565d54ec4ff89e34dcc1ce13c`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_pgw-identity-convention-undecidable_lean_replay.json`

- file: [dag/research/campaign_pgw-identity-convention-undecidable_lean_replay.json](../../../dag/research/campaign_pgw-identity-convention-undecidable_lean_replay.json)
- sha256 (`lf-normalised`): `6dbb8b763bd60e7ae8e46aadde6671641f24700402f39ab2f961b20853d1fa9b`
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
