# PGW-MSSN-ASCENT-TRIAD

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `DEFINITION`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> MSS-N separates three evidence states: declared successor ≠ candidate lift ≠ licensed lift. A declared successor is a research obligation stated by an atlas row; a candidate lift is submitted data, a proposed pair of maps with repair witnesses; a licensed lift has exhausted repairs, a minimized extension, a verified retraction and a passing host replay. Every atlas row is a declared successor specification, and its successor rationale stays unproved until an accepted lift record is attested.

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

The levels catalogue sets lift_status unlicensed; a PASS LiftReceipt from evaluate_two_boxed_laws_gate consumes supplied flags and is a candidate check, not a licensed lift, and the CandidateLift record shape is metadata only.

## Source status

pregenesis_to_minimal_symbol_systems paper.md section 15; 003_oemssn levels/README.md invariant 3 and curriculum.md Lesson 1

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `education/minimal_symbol_systems/code/rust/src/obstruction_detector.rs`

- file: [education/minimal_symbol_systems/code/rust/src/obstruction_detector.rs](../../../education/minimal_symbol_systems/code/rust/src/obstruction_detector.rs)
- sha256 (`bytes`): `439bafc4a90225a06b9e80fb2d9458ecd3718cd1908db47b734056ef8b6c3de2`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CandidateLift` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md`

- file: [atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md](../../../atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md)
- sha256 (`lf-normalised`): `a4a7d840b11e912896032aebc9ead95f7978c0e6f60656f44645c6d8fadf593b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0529_mssn_ascent_triad.md`

- file: [dag/derivations/05_mssn_sn/tfq_0529_mssn_ascent_triad.md](../../../dag/derivations/05_mssn_sn/tfq_0529_mssn_ascent_triad.md)
- sha256 (`lf-normalised`): `c076e364e5af4093e5a7808189456a4913b9f2eed4d19b03e691d9caf88c6a1f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0529
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:6313c51659873eb093e3ef4171a13eac33217dd96e168a97416623d6248005b9:51-53`
- `external:sha256:ea610e33827464418f0f2786ff65c9af072659bf2884a9411900e07d482e9740:29-31`
- `external:upstream/education/minimal_symbol_systems/code/rust/src/obstruction_detector.rs::CandidateLift`

## Absences recorded by the TFQ records

- TFQ-0529 lean4: no Lean statement of the ascent triad; candidateLiftCondition is recorded under TFQ-0534
- TFQ-0529 python: no Python check of lift evidence states

## Routes

Incoming (1):

- `PGW-R-MSSN-ASCENT-TRIAD` `DERIVED_PROSE`: [PGW-MSSN-ATLAS-NOT-DERIVATION](PGW-MSSN-ATLAS-NOT-DERIVATION.md) (DEFINITION)

Outgoing (1):

- `PGW-R-MSSN-ALPHABET-DECLARATIONS` `DERIVED_PROSE`: [PGW-MSSN-ALPHABET-DECLARATIONS](PGW-MSSN-ALPHABET-DECLARATIONS.md) (DEFINITION)
