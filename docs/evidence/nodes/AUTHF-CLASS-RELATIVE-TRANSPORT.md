# AUTHF-CLASS-RELATIVE-TRANSPORT

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Given a map from source instances to proposals that preserves the source predicate as proposal validity, and closure of the allowed proposal deciders under precomposition with that map, a source predicate with no allowed total decider yields a proposal validity predicate with no allowed total decider.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 6
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

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
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `AuthIncompleteness.GlobalLift`): recorded sha256 `9b488fac5fdf6cdf084af17a0dfe773bdd18f1e95803a27bfaf118da82d1a49b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/GlobalLift.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.GlobalComputabilityLift.ClosedUnderReduction` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.GlobalComputabilityLift.ClosedUnderReduction` |
| `AuthorizationIncompleteness.GlobalComputabilityLift.Decides` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.GlobalComputabilityLift.Decides` |
| `AuthorizationIncompleteness.GlobalComputabilityLift.NoTotalDecider` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.GlobalComputabilityLift.NoTotalDecider` |
| `AuthorizationIncompleteness.GlobalComputabilityLift.ValidityReduction` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.GlobalComputabilityLift.ValidityReduction` |
| `AuthorizationIncompleteness.GlobalComputabilityLift.no_source_decider_blocks_total_authorizer` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.GlobalComputabilityLift.no_source_decider_blocks_total_authorizer` |
| `AuthorizationIncompleteness.GlobalComputabilityLift.total_authorizer_yields_source_decider` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.GlobalComputabilityLift.total_authorizer_yields_source_decider` |

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
