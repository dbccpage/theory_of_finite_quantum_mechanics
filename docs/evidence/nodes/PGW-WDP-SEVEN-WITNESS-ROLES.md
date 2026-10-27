# PGW-WDP-SEVEN-WITNESS-ROLES

Stage: [WDP](../stages/WDP.md). Status: `DEFINITION`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> WDP-CH02-D01 defines a residual-locus witness as a typed locus L with evidence that the residual's component at L is nonzero under the declared test; the locus is a witness to a proposition, not a memory, observer, agent or apparatus. Section 2.2 replaces the one word witness by seven typed roles, ResidualLocusWitness, RetentionWitness, RepairWitness, ContextWitness, DualCertificateWitness, DescentReceipt and CounterexampleWitness, written Witness_k\[P\](x, e) with the proposition P and kind k in the type. WDP-CH02-P01 states that in the nominal typed interface no role tag coerces to another unless an explicit adapter and its hypotheses are declared. On the oriented triangle the circulation functional ℓ vanishes on im d₀ and gives ℓ(1,1,1) = 3, a dual certificate that observes, retains and decides nothing.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

A syntactic fence, not the 42 directed semantic non-implications between roles; the executable check (adapt_quotient and adapt_operational refusing MISSING_ADAPTER or ADAPTER_MISMATCH) covers observer representations and does not enumerate the seven tags.

## Source status

WDP monograph §2.1-§2.2 WDP-CH02-D01 definition and WDP-CH02-P01 typing proposition

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/observer.py`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/observer.py](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/observer.py)
- sha256 (`bytes`): `8ca3528b4e8b891abc63a178d4a773b8b8b06da7665f418a7298f24baa261271`
- cited in: record TFQ-0539

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `adapt_quotient` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md)
- sha256 (`lf-normalised`): `753d1c99c799f84f9a71912b98082d590c89c531f980c112b62ee2a86ab2726b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0539_wdp_seven_witness_roles.md`

- file: [dag/derivations/06_wdp/tfq_0539_wdp_seven_witness_roles.md](../../../dag/derivations/06_wdp/tfq_0539_wdp_seven_witness_roles.md)
- sha256 (`lf-normalised`): `a7b27af35a701a17d60457fd6b8ffcd3dfeef2ca8120502b85b39e2f365df429`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0539
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:7dade8e5406842b3be776bcb1b6a4747fbaa697b0bdae9f1112e7fae6d9d22dc::adapt_quotient`
- `external:sha256:a3928cbb59159e343cc8ec518c3015f08d59955caa77d0e07f6e4428202a863f:123-159`
- `external:upstream/external:sha256:7dade8e5406842b3be776bcb1b6a4747fbaa697b0bdae9f1112e7fae6d9d22dc::adapt_quotient`

## Absences recorded by the TFQ records

- TFQ-0539 lean4: the claim map lists WDP-CH02-D01 and WDP-CH02-P01 without an exact Lean declaration

## Routes

Incoming (1):

- `PGW-R-WDP-SEVEN-WITNESS-ROLES` `DERIVED_PROSE`: [PGW-WDP-QUOTIENT-DEFECT-ROOT-P](PGW-WDP-QUOTIENT-DEFECT-ROOT-P.md) (DEFINITION)

Outgoing (1):

- `PGW-R-WDP-RETENTION-PACKET` `DERIVED_PROSE`: [PGW-WDP-RETENTION-PACKET](PGW-WDP-RETENTION-PACKET.md) (DEFINITION)
