# AUTH-G5A-CLASS-RELATIVE-TRANSPORT

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> If a map from a source predicate into proposal validity preserves the predicate exactly, and the allowed proposal deciders are closed under precomposition with that map, then a source predicate with no allowed total decider gives a proposal predicate with no allowed total decider.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- decision classes allowedHard and allowedProposal as arbitrary predicates on Bool-valued functions

## Bottleneck

Instantiate the allowed classes with ComputablePred on a code type, take the halting problem as the source predicate and prove closure under the reduction; the declaration supplies none of the three.

## Source status

papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md record AIT-G5a claims proved, rooted target (axiom-free); audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/foundations/authorization_incompleteness/evidence/original/formal/global_computability_lift_models.lean`

- file: [papers/foundations/authorization_incompleteness/evidence/original/formal/global_computability_lift_models.lean](../../../papers/foundations/authorization_incompleteness/evidence/original/formal/global_computability_lift_models.lean)
- sha256 (`bytes`): `c3a3d2a9ba5fb5a78f1a36ebdb3e3e754510956143097a8af4831df74fddb18d`
- cited in: node.lean, record TFQ-1334
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains papers/foundations/authorization_incompleteness/evidence/original/formal/global_computability_lift_models.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.GlobalComputabilityLift.no_source_decider_blocks_total_authorizer` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.GlobalComputabilityLift.no_source_decider_blocks_total_authorizer` |
| `AuthorizationIncompleteness.GlobalComputabilityLift.total_authorizer_yields_source_decider` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.GlobalComputabilityLift.total_authorizer_yields_source_decider` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1334_auth_g5a_class_relative_transport.md`

- file: [dag/derivations/29_computation/tfq_1334_auth_g5a_class_relative_transport.md](../../../dag/derivations/29_computation/tfq_1334_auth_g5a_class_relative_transport.md)
- sha256 (`lf-normalised`): `a18d753563e9a069689eb8991818203deb0eb5e8224897268b251b8601671043`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1334
- counts toward the grade: no

### Documents and data: `papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md`

- file: [papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md](../../../papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md)
- sha256 (`lf-normalised`): `4ca81b6ae8e724b54c7abf43ea951c119c2cff31a375e45cd7d79299adc7f70c`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/foundations/authorization_incompleteness/authorization_incompleteness_theory_claim_ledger.md`

- file: [papers/foundations/authorization_incompleteness/authorization_incompleteness_theory_claim_ledger.md](../../../papers/foundations/authorization_incompleteness/authorization_incompleteness_theory_claim_ledger.md)
- sha256 (`lf-normalised`): `28aa3a825d1b0296270b62f9a33a4a67b6c2a2d708028444a7f725ad46697feb`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/foundations/authorization_incompleteness/proof_program.md`

- file: [papers/foundations/authorization_incompleteness/proof_program.md](../../../papers/foundations/authorization_incompleteness/proof_program.md)
- sha256 (`lf-normalised`): `e624d01a2371d6d8856a17c535ad1916abd8b1353450755c7281fe22e87b720f`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-AUTH-G5A-CLASS-RELATIVE-TRANSPORT` `DERIVED_LEAN`: [TFQ-0330](TFQ-0330.md) (OPEN)

Outgoing (3):

- `APP-R-AUTH-G5-GLOBAL-COMPUTABILITY-LIFT` `GAP_NO_DERIVATION`: [AUTH-G5-GLOBAL-COMPUTABILITY-LIFT](AUTH-G5-GLOBAL-COMPUTABILITY-LIFT.md) (OPEN)
- `APP-R-AUTH-G5B-CARRIER-ADMISSION-GATE` `DERIVED_PROSE`: [AUTH-G5B-CARRIER-ADMISSION-GATE](AUTH-G5B-CARRIER-ADMISSION-GATE.md) (DEFINITION)
- `APP-R-AUTH-G5C-TERMINALIZATION-CONSEQUENCE` `DERIVED_LEAN`: [AUTH-G5C-TERMINALIZATION-CONSEQUENCE](AUTH-G5C-TERMINALIZATION-CONSEQUENCE.md) (PROVED_LEAN)
