# AUTHF-RICE-GODEL-OPEN

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> No recovered declaration states Rice's theorem, a halting-problem reduction, Goedel's second incompleteness theorem or the LLM corollary; the only link toward them is the class-relative transport with a supplied no-decider premise, which the recovery-time MathlibBridge file instantiates for halting only.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
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

Instantiate the transport for a nontrivial extensional property of encoded programs with Mathlib's ComputablePred.rice and a computable reduction from the DTM0 carrier before any such claim.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record AUTHF-25 claims OPEN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/29_computation/tfq_1363_authf_rice_godel_open.md`

- file: [dag/derivations/29_computation/tfq_1363_authf_rice_godel_open.md](../../../dag/derivations/29_computation/tfq_1363_authf_rice_godel_open.md)
- sha256 (`lf-normalised`): `ead5173465a916243e4c7cd542892045da220da6e070701a2f3ee7ab86f02c86`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1363
- counts toward the grade: no

### Documents and data: `papers/foundations/authorization_incompleteness/evidence/original/formal/README.md`

- file: [papers/foundations/authorization_incompleteness/evidence/original/formal/README.md](../../../papers/foundations/authorization_incompleteness/evidence/original/formal/README.md)
- sha256 (`lf-normalised`): `bee9b788be86ffc01647ed94d7259d5e7d8767fd9633064488101a952ecf6793`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md`

- file: [papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md](../../../papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md)
- sha256 (`lf-normalised`): `50b2673ad6e6ce3e8f3cba55fbcc848fac64db21600db6e8d1a9e63e96b7f915`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-AUTHF-RICE-GODEL-OPEN` `GAP_NO_DERIVATION`: [PGW-CONTEXT-DECISION-PROCEDURE](PGW-CONTEXT-DECISION-PROCEDURE.md) (OPEN), [AUTHF-CLASS-RELATIVE-TRANSPORT](AUTHF-CLASS-RELATIVE-TRANSPORT.md) (PROVED_LEAN)

Outgoing (0):

