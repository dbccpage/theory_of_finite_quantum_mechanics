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

### Lean: `lean4/IdentityConvention.lean`

- file: [lean4/IdentityConvention.lean](../../../lean4/IdentityConvention.lean)
- sha256 (`bytes`): `3a3d58657a3f1ce6a385da5e3afe1e74bbce3eb37257582f8359e197e9388fda`
- cited in: node.lean, receipt dag/research/campaign_pgw-identity-convention-undecidable_lean_replay.json (IdentityConvention), record TFQ-0423
- replay: `verified`
  - receipt [dag/research/campaign_pgw-identity-convention-undecidable_lean_replay.json](../../../dag/research/campaign_pgw-identity-convention-undecidable_lean_replay.json) (module `IdentityConvention`): recorded sha256 `3a3d58657a3f1ce6a385da5e3afe1e74bbce3eb37257582f8359e197e9388fda` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build IdentityConvention`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `IdentityConvention.Indistinguishable` | yes | yes | yes | none | `#print axioms IdentityConvention.Indistinguishable` |
| `IdentityConvention.IsNew` | yes | yes | yes | none | `#print axioms IdentityConvention.IsNew` |
| `IdentityConvention.adding_identity_separates` | yes | yes | yes | none | `#print axioms IdentityConvention.adding_identity_separates` |
| `IdentityConvention.empty_family_identifies_all` | yes | yes | yes | none | `#print axioms IdentityConvention.empty_family_identifies_all` |
| `IdentityConvention.exactObserver` | yes | yes | yes | none | `#print axioms IdentityConvention.exactObserver` |
| `IdentityConvention.exact_inscription_is_new` | yes | yes | yes | none | `#print axioms IdentityConvention.exact_inscription_is_new` |
| `IdentityConvention.exact_observer_sees_new` | yes | yes | yes | none | `#print axioms IdentityConvention.exact_observer_sees_new` |
| `IdentityConvention.forgetting_preserves_indistinguishability` | yes | yes | yes | none | `#print axioms IdentityConvention.forgetting_preserves_indistinguishability` |
| `IdentityConvention.no_convention_independent_answer` | yes | yes | yes | none | `#print axioms IdentityConvention.no_convention_independent_answer` |
| `IdentityConvention.observational_equivalence` | yes | yes | yes | none | `#print axioms IdentityConvention.observational_equivalence` |
| `IdentityConvention.opaqueObserver` | yes | yes | yes | none | `#print axioms IdentityConvention.opaqueObserver` |
| `IdentityConvention.opaque_inscription_is_not_new` | yes | yes | yes | none | `#print axioms IdentityConvention.opaque_inscription_is_not_new` |
| `IdentityConvention.opaque_observer_sees_no_new` | yes | yes | yes | none | `#print axioms IdentityConvention.opaque_observer_sees_no_new` |
| `IdentityConvention.withIdentity` | yes | yes | yes | none | `#print axioms IdentityConvention.withIdentity` |

- counts toward the grade: yes

### Python: `checks/independent/pgw-identity-convention-undecidable.py`

- file: [checks/independent/pgw-identity-convention-undecidable.py](../../../checks/independent/pgw-identity-convention-undecidable.py)
- sha256 (`bytes`): `cdb0ef8292785b35a0ec2f28c112fab192b39f91be0d3da290b4ca5774a34b98`
- cited in: record TFQ-0423
- counts toward the grade: yes

### Documents and data: `dag/derivations/01_pregenesis/tfq_0423_identity_convention_undecidable.md`

- file: [dag/derivations/01_pregenesis/tfq_0423_identity_convention_undecidable.md](../../../dag/derivations/01_pregenesis/tfq_0423_identity_convention_undecidable.md)
- sha256 (`lf-normalised`): `ada6fd565fa15e07f7098a1290da5f420d0895f900ff9ba6100cdc6e09df2202`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0423
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-identity-convention-undecidable.md`

- file: [dag/derivations/independent/pgw-identity-convention-undecidable.md](../../../dag/derivations/independent/pgw-identity-convention-undecidable.md)
- sha256 (`lf-normalised`): `14a06da7dc857a3d8ae74f3096c4dd3773285bcefcfb31dcf01b69f065a2c88a`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_pgw-identity-convention-undecidable_lean_replay.json`

- file: [dag/research/campaign_pgw-identity-convention-undecidable_lean_replay.json](../../../dag/research/campaign_pgw-identity-convention-undecidable_lean_replay.json)
- sha256 (`lf-normalised`): `37e83844e20d3c63f8b4613e0c2b5c86437d46829d65190f001798adf17089d3`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:0a9068781f8c282418f8ae2933ae6502b1bef56df91c16758cf730de1e359149:731-737`
- `external:sha256:1713d12cc07cce5f295bb69922c49e278be2277c31d4fecee6b41ecb87d639bb:36-43`
- `external:sha256:2e49c338376d7a78a6a89cdd340c9b3c351c485c20d4127e3c455b3fb1570428:43-53`

## Absences recorded by the TFQ records

- TFQ-0423 rust: no Rust switch between identity conventions

## Routes

Incoming (1):

- `PGW-R-IDENTITY-CONVENTION-UNDECIDABLE` `CONDITIONAL_ON_IMPORT`: [PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT](PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT.md) (CONDITIONAL)

Outgoing (2):

- `APP-R-COMP-C1-IDENTITY-CONVENTION-INPUT` `CONDITIONAL_ON_IMPORT`: [COMP-C1-IDENTITY-CONVENTION-INPUT](COMP-C1-IDENTITY-CONVENTION-INPUT.md) (IMPORTED_ASSUMPTION)
- `PGW-R-ABSENCE-OF-RULE-NOT-IDENTIFICATION` `DERIVED_PROSE`: [PGW-ABSENCE-OF-RULE-NOT-IDENTIFICATION](PGW-ABSENCE-OF-RULE-NOT-IDENTIFICATION.md) (DEFINITION)
