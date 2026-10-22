# COMP-C7-NF-REACH-UNDECIDABLE

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For the fixed rewriting regime Rules M0 and its explicit family of start words, the predicate that the start word of the input reaches an irreducible word is not computable, as a predicate of the code or of the natural number input.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 5 Lean reference(s) cited, 5 in this checkout (replay: none 5). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- Mathlib ComputablePred.halting_problem

## Bottleneck

The statement is about the family startWord; that the input-to-start-word map is computable is not proved (COMP-C7c).

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C7b claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisCompUniv.lean`

- file: [lean4/GenesisCompUniv.lean](../../../lean4/GenesisCompUniv.lean)
- sha256 (`bytes`): `966d60cf259d7c22f275e13ab58dd6d027330f6ae146536eb68a97ddb97620f3`
- cited in: node.lean, node.source, record TFQ-1309
- replay: `none`
- check: `cd lean4 && lake build GenesisCompUniv`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `nfReach_iff` | yes | yes | yes | - | `#print axioms nfReach_iff` |
| `nfReach_not_computable` | yes | yes | yes | - | `#print axioms nfReach_not_computable` |
| `reach_irreducible_iff` | yes | yes | yes | - | `#print axioms reach_irreducible_iff` |
| `reach_irreducible_not_computable` | yes | yes | yes | - | `#print axioms reach_irreducible_not_computable` |
| `startWord_rep` | yes | yes | yes | - | `#print axioms startWord_rep` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1309_comp_c7_nf_reach_undecidable.md`

- file: [dag/derivations/29_computation/tfq_1309_comp_c7_nf_reach_undecidable.md](../../../dag/derivations/29_computation/tfq_1309_comp_c7_nf_reach_undecidable.md)
- sha256 (`lf-normalised`): `23d47205164dea84203754bfa3013b7d27ed65624881541d98bedb7c8dcb340f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1309
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C7-NF-REACH-UNDECIDABLE` `DERIVED_LEAN`: [COMP-C7-MACHINE-HALTING-UNDECIDABLE](COMP-C7-MACHINE-HALTING-UNDECIDABLE.md) (PROVED_LEAN), [COMP-C5-CLOSURES-HALTING](COMP-C5-CLOSURES-HALTING.md) (PROVED_LEAN)

Outgoing (3):

- `APP-R-COMP-C3-NO-FIXED-BOUND` `CONDITIONAL_ON_IMPORT`: [COMP-C3-NO-FIXED-BOUND](COMP-C3-NO-FIXED-BOUND.md) (CONDITIONAL)
- `APP-R-COMP-C7-ENCODED-INSTANCE-REDUCTION` `CONDITIONAL_ON_IMPORT`: [COMP-C7-ENCODED-INSTANCE-REDUCTION](COMP-C7-ENCODED-INSTANCE-REDUCTION.md) (CONDITIONAL)
- `APP-R-COMP-C7-FIXED-TARGET-OPEN` `GAP_NO_DERIVATION`: [COMP-C7-FIXED-TARGET-OPEN](COMP-C7-FIXED-TARGET-OPEN.md) (OPEN)
