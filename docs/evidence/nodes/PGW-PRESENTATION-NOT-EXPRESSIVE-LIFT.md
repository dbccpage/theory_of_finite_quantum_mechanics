# PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Write P for the presented inscriptions and O for the internal observations. Supplying \<a\> after \<\> changes P from {\<\>} to {\<a\>} and leaves O_1 = O_0 = ∅, so no new internal distinction is available. With q : P → N sending an inscription to the distinctions the regime has, x ≠ y in P can hold while q(x) = q(y) in N, so a new presentation does not imply a new internal class, and in the other direction q(x) = q(y) does not imply x = y. Under the opaque convention \<a\> is a new presentation state in the same internal class as \<\>; the statement holds under that convention only.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 19
- distinct cited Lean declarations covered by a current replay receipt: 18
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Opaque identity convention: a state is what the regime can tell apart, so internal identity is the quotient by ≈ₙ (assumption)

## Bottleneck

Under the exact-inscription convention \<a\> is a new state; the statement concerns discriminating power, not meaning, since a regime can gain a syntactic distinction such as empty versus nonempty payload without assigning a a referent. Reviewed in PR 185: lean4/PregenesisPresentationLift.lean checks a two-inscription model (Inscription = {nil, markA}, convention comparison, P0 = {nil} against P1 = {nil, markA}) in which the distinction map q is the constant empty map by definition and the exact-inscription convention is defined as equality, so O_0 = O_1 = empty, the non-injectivity of q and the statement that the collapse holds under the opaque convention only are properties of those definitions. Not proved: an observation family O_n and q derived from it, supplying \<a\> as an operation that leaves O unchanged, P changing to {\<a\>} as the statement words it (the model has P1 = {\<\>, \<a\>}), the link between q and the Genesis regime model of the module, and the opaque identity convention itself, which stays an import.

## Source status

000_oepregen 03_results_and_arguments.md section 2 (statement 2, holds under one convention); v1 Derivation 3

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/PreGenesisToMssn/Observation.lean`

- file: [lean4/Imported/PreGenesisToMssn/Observation.lean](../../../lean4/Imported/PreGenesisToMssn/Observation.lean)
- sha256 (`bytes`): `ccbdc2919571c7267a4dc3697bf9b59bbbaa4e37481a731dd6649ebdefce12e1`
- cited in: node.lean, record TFQ-0422
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.PreGenesisToMssn.Observation`): recorded sha256 `ccbdc2919571c7267a4dc3697bf9b59bbbaa4e37481a731dd6649ebdefce12e1` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/PreGenesisToMssn/Observation.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `empty_profiles_equal` | yes | yes | yes | Quot.sound, propext | `#print axioms empty_profiles_equal` |

- counts toward the grade: yes

### Lean: `lean4/PregenesisPresentationLift.lean`

- file: [lean4/PregenesisPresentationLift.lean](../../../lean4/PregenesisPresentationLift.lean)
- sha256 (`bytes`): `fd65daacff92b9e244716272be323ce9e5364e7cbfe6c8f4e69ca8bf2e4d13cc`
- cited in: node.lean, receipt dag/research/campaign_pgw-presentation-not-expressive-lift_lean_replay.json (PregenesisPresentationLift), record TFQ-0422
- replay: `verified`
  - receipt [dag/research/campaign_pgw-presentation-not-expressive-lift_lean_replay.json](../../../dag/research/campaign_pgw-presentation-not-expressive-lift_lean_replay.json) (module `PregenesisPresentationLift`): recorded sha256 `fd65daacff92b9e244716272be323ce9e5364e7cbfe6c8f4e69ca8bf2e4d13cc` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build PregenesisPresentationLift`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `PregenesisPresentationLift.P0_ssubset_P1` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PregenesisPresentationLift.P0_ssubset_P1` |
| `PregenesisPresentationLift.exact_nil_markA_not_equiv` | yes | yes | yes | Quot.sound, propext | `#print axioms PregenesisPresentationLift.exact_nil_markA_not_equiv` |
| `PregenesisPresentationLift.exact_presentation_card` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PregenesisPresentationLift.exact_presentation_card` |
| `PregenesisPresentationLift.exists_distinct_presentations_same_class` | yes | yes | yes | Quot.sound, propext | `#print axioms PregenesisPresentationLift.exists_distinct_presentations_same_class` |
| `PregenesisPresentationLift.fails_under_exact` | yes | yes | yes | Quot.sound, propext | `#print axioms PregenesisPresentationLift.fails_under_exact` |
| `PregenesisPresentationLift.general_non_injectivity_consequences` | yes | yes | yes | none | `#print axioms PregenesisPresentationLift.general_non_injectivity_consequences` |
| `PregenesisPresentationLift.holds_under_opaque` | yes | yes | yes | Quot.sound, propext | `#print axioms PregenesisPresentationLift.holds_under_opaque` |
| `PregenesisPresentationLift.inscription_card` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PregenesisPresentationLift.inscription_card` |
| `PregenesisPresentationLift.new_presentation_not_implies_new_internal_class` | yes | yes | yes | Quot.sound, propext | `#print axioms PregenesisPresentationLift.new_presentation_not_implies_new_internal_class` |
| `PregenesisPresentationLift.nil_ne_markA` | yes | yes | yes | none | `#print axioms PregenesisPresentationLift.nil_ne_markA` |
| `PregenesisPresentationLift.no_new_internal_distinction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PregenesisPresentationLift.no_new_internal_distinction` |
| `PregenesisPresentationLift.opaque_nil_markA_equiv` | yes | yes | yes | Quot.sound, propext | `#print axioms PregenesisPresentationLift.opaque_nil_markA_equiv` |
| `PregenesisPresentationLift.opaque_quotient_card` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PregenesisPresentationLift.opaque_quotient_card` |
| `PregenesisPresentationLift.q_non_injective_witness` | yes | yes | yes | Quot.sound, propext | `#print axioms PregenesisPresentationLift.q_non_injective_witness` |
| `PregenesisPresentationLift.same_internal_class_not_implies_same_presentation` | yes | yes | yes | Quot.sound, propext | `#print axioms PregenesisPresentationLift.same_internal_class_not_implies_same_presentation` |
| `PregenesisPresentationLift.statement_holds_under_opaque_only` | yes | yes | yes | Quot.sound, propext | `#print axioms PregenesisPresentationLift.statement_holds_under_opaque_only` |
| `PregenesisPresentationLift.two_marks_in_unformed_regime_collapsed` | yes | yes | yes | propext | `#print axioms PregenesisPresentationLift.two_marks_in_unformed_regime_collapsed` |

- counts toward the grade: yes

### Python: `checks/independent/pgw-presentation-not-expressive-lift.py`

- file: [checks/independent/pgw-presentation-not-expressive-lift.py](../../../checks/independent/pgw-presentation-not-expressive-lift.py)
- sha256 (`bytes`): `11490a7350cd3707be4844f886a505a9d2f3577aa26d1821e761cb1d849d9ee8`
- cited in: record TFQ-0422

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/01_pregenesis/tfq_0422_presentation_not_expressive_lift.md`

- file: [dag/derivations/01_pregenesis/tfq_0422_presentation_not_expressive_lift.md](../../../dag/derivations/01_pregenesis/tfq_0422_presentation_not_expressive_lift.md)
- sha256 (`lf-normalised`): `d010f49283283d97594404541d9e6bf325245daf13e8ce692e527e3be825d550`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0422
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

- TFQ-0422 rust: no Rust record separating presentation state from internal class

## Routes

Incoming (1):

- `PGW-R-PRESENTATION-NOT-EXPRESSIVE-LIFT` `CONDITIONAL_ON_IMPORT`: [PGW-OBSERVATIONAL-EQUIVALENCE](PGW-OBSERVATIONAL-EQUIVALENCE.md) (DEFINITION)

Outgoing (2):

- `APP-R-AUTH-TC0-TAPE-CONTROL-TYPING` `COMPUTED`: [AUTH-TC0-TAPE-CONTROL-TYPING](AUTH-TC0-TAPE-CONTROL-TYPING.md) (COMPUTATIONALLY_CHECKED)
- `PGW-R-IDENTITY-CONVENTION-UNDECIDABLE` `CONDITIONAL_ON_IMPORT`: [PGW-IDENTITY-CONVENTION-UNDECIDABLE](PGW-IDENTITY-CONVENTION-UNDECIDABLE.md) (CONDITIONAL)
