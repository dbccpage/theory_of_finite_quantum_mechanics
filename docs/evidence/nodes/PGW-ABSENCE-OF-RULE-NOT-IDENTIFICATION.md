# PGW-ABSENCE-OF-RULE-NOT-IDENTIFICATION

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `DEFINITION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Asked whether the regime distinguishes \<a\> and \<ab\>, identifies them or cannot decide, Trial 1 answered that the current regime identifies them; the analysis corrects this, since the absence of a distinguishing rule does not imply identification. Formalization A: with no equality, equivalence or observation relation declared, neither \<a\> = \<ab\> nor \<a\> ≠ \<ab\> is internally derivable, and status(\<a\>, \<ab\>) = UNDECIDABLE. Formalization B is the separate definition ≈ₙ, under which an empty O_n gives \<a\> ≈ₙ \<ab\> vacuously. The reply 'identifies them' imported an identification relation unless B had been declared first, and the failure-mode chapter names it premature relation.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

A and B are two declared readings and no theorem chooses between them; vacuous ≈ₙ under B does not install an object-language equality rule.

## Source status

v1 section 3 Formalization A (declared UNDECIDABLE status) beside Formalization B; 04_named_failure_modes.md premature relation

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/paper.md`

- file: [atlas/papers/finite_obstruction_calculus/genesis/paper.md](../../../atlas/papers/finite_obstruction_calculus/genesis/paper.md)
- sha256 (`lf-normalised`): `0dde974e14ff1b54ff6e65705a1194aea38fad7e65bf77b159a07ea1b96bb9a5`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/01_pregenesis/tfq_0424_absence_of_rule_not_identification.md`

- file: [dag/derivations/01_pregenesis/tfq_0424_absence_of_rule_not_identification.md](../../../dag/derivations/01_pregenesis/tfq_0424_absence_of_rule_not_identification.md)
- sha256 (`lf-normalised`): `82c0a3a6029e7f28a6567fa3ea0c105ff03750969e3d62694cc583a2ff51fecb`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0424
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:0a9068781f8c282418f8ae2933ae6502b1bef56df91c16758cf730de1e359149:147-175`
- `external:sha256:2e49c338376d7a78a6a89cdd340c9b3c351c485c20d4127e3c455b3fb1570428:55-60`

## Absences recorded by the TFQ records

- TFQ-0424 lean4: no Lean three-valued status for an undeclared relation; the vacuous case of formalization B is empty_profiles_equal in pregenesis_to_minimal_symbol_systems/lean4/Observation.lean
- TFQ-0424 python: no Python UNDECIDABLE status for a pair with no declared relation
- TFQ-0424 rust: no Rust UNDECIDABLE status for a pair with no declared relation

## Routes

Incoming (1):

- `PGW-R-ABSENCE-OF-RULE-NOT-IDENTIFICATION` `DERIVED_PROSE`: [PGW-IDENTITY-CONVENTION-UNDECIDABLE](PGW-IDENTITY-CONVENTION-UNDECIDABLE.md) (CONDITIONAL)

Outgoing (1):

- `PGW-R-FORCED-SEPARATION-LIFT-NOT-UNIQUE` `DERIVED_LEAN`: [PGW-FORCED-SEPARATION-LIFT-NOT-UNIQUE](PGW-FORCED-SEPARATION-LIFT-NOT-UNIQUE.md) (PROVED_LEAN)
