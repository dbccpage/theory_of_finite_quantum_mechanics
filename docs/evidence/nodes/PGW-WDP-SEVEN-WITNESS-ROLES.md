# PGW-WDP-SEVEN-WITNESS-ROLES

Stage: [WDP](../stages/WDP.md). Status: `DEFINITION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> WDP-CH02-D01 defines a residual-locus witness as a typed locus L with evidence that the residual's component at L is nonzero under the declared test; the locus is a witness to a proposition, not a memory, observer, agent or apparatus. Section 2.2 replaces the one word witness by seven typed roles, ResidualLocusWitness, RetentionWitness, RepairWitness, ContextWitness, DualCertificateWitness, DescentReceipt and CounterexampleWitness, written Witness_k\[P\](x, e) with the proposition P and kind k in the type. WDP-CH02-P01 states that in the nominal typed interface no role tag coerces to another unless an explicit adapter and its hypotheses are declared. On the oriented triangle the circulation functional ℓ vanishes on im d₀ and gives ℓ(1,1,1) = 3, a dual certificate that observes, retains and decides nothing.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

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

### Rust: `omega_engine/crates_rs/omega_wdp/src/observer.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/observer.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/06_wdp/tfq_0539_wdp_seven_witness_roles.md`

- file: [dag/derivations/06_wdp/tfq_0539_wdp_seven_witness_roles.md](../../../dag/derivations/06_wdp/tfq_0539_wdp_seven_witness_roles.md)
- sha256 (`lf-normalised`): `b21ba644ca850c1ad2e4ae3f44ffbff3d3f43c6d0da9e1d3faf9f2f8b5faae90`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0539
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/006_oewdp/levels/level_01_witness_function.md`

- file: `omega_engine_education/documentation/006_oewdp/levels/level_01_witness_function.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine/crates_rs/omega_wdp/src/observer.rs::adapt_quotient`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/observer.py::adapt_quotient`

## Absences recorded by the TFQ records

- TFQ-0539 lean4: the claim map lists WDP-CH02-D01 and WDP-CH02-P01 without an exact Lean declaration

## Routes

Incoming (1):

- `PGW-R-WDP-SEVEN-WITNESS-ROLES` `DERIVED_PROSE`: [PGW-WDP-QUOTIENT-DEFECT-ROOT-P](PGW-WDP-QUOTIENT-DEFECT-ROOT-P.md) (DEFINITION)

Outgoing (1):

- `PGW-R-WDP-RETENTION-PACKET` `DERIVED_PROSE`: [PGW-WDP-RETENTION-PACKET](PGW-WDP-RETENTION-PACKET.md) (DEFINITION)
