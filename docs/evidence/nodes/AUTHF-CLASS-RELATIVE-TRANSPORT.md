# AUTHF-CLASS-RELATIVE-TRANSPORT

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Given a map from source instances to proposals that preserves the source predicate as proposal validity, and closure of the allowed proposal deciders under precomposition with that map, a source predicate with no allowed total decider yields a proposal validity predicate with no allowed total decider.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 6 Lean reference(s) cited, 6 in this checkout (replay: none 6). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

The allowed classes and the source no-decider premise are supplied; no computability class, halting-style source theorem or Rice reduction is instantiated.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record no_source_decider_blocks_total_authorizer claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AuthIncompleteness/GlobalLift.lean`

- file: [lean4/AuthIncompleteness/GlobalLift.lean](../../../lean4/AuthIncompleteness/GlobalLift.lean)
- sha256 (`bytes`): `9b488fac5fdf6cdf084af17a0dfe773bdd18f1e95803a27bfaf118da82d1a49b`
- cited in: node.lean, node.source, record TFQ-1347
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/GlobalLift.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.GlobalComputabilityLift.ClosedUnderReduction` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.GlobalComputabilityLift.ClosedUnderReduction` |
| `AuthorizationIncompleteness.GlobalComputabilityLift.Decides` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.GlobalComputabilityLift.Decides` |
| `AuthorizationIncompleteness.GlobalComputabilityLift.NoTotalDecider` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.GlobalComputabilityLift.NoTotalDecider` |
| `AuthorizationIncompleteness.GlobalComputabilityLift.ValidityReduction` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.GlobalComputabilityLift.ValidityReduction` |
| `AuthorizationIncompleteness.GlobalComputabilityLift.no_source_decider_blocks_total_authorizer` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.GlobalComputabilityLift.no_source_decider_blocks_total_authorizer` |
| `AuthorizationIncompleteness.GlobalComputabilityLift.total_authorizer_yields_source_decider` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.GlobalComputabilityLift.total_authorizer_yields_source_decider` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1347_authf_class_relative_transport.md`

- file: [dag/derivations/29_computation/tfq_1347_authf_class_relative_transport.md](../../../dag/derivations/29_computation/tfq_1347_authf_class_relative_transport.md)
- sha256 (`lf-normalised`): `5be59ac840aa87a6ad771cf976e8779e42c0d19be995fb9ed220f1de82b4fb8f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1347
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-AUTHF-CLASS-RELATIVE-TRANSPORT` `DERIVED_LEAN`: [PGW-CONTEXT-DECISION-PROCEDURE](PGW-CONTEXT-DECISION-PROCEDURE.md) (OPEN)

Outgoing (3):

- `APP-R-AUTHF-MATHLIB-HALTING-BRIDGE` `DERIVED_LEAN`: [AUTHF-MATHLIB-HALTING-BRIDGE](AUTHF-MATHLIB-HALTING-BRIDGE.md) (PROVED_LEAN)
- `APP-R-AUTHF-RICE-GODEL-OPEN` `GAP_NO_DERIVATION`: [AUTHF-RICE-GODEL-OPEN](AUTHF-RICE-GODEL-OPEN.md) (OPEN)
- `APP-R-AUTHF-TERMINAL-ACCEPT-BIT` `DERIVED_LEAN`: [AUTHF-TERMINAL-ACCEPT-BIT](AUTHF-TERMINAL-ACCEPT-BIT.md) (PROVED_LEAN)
