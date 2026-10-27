# PGW-MSSN-ATLAS-NOT-DERIVATION

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `DEFINITION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> MSS-N is an externally designed atlas of glyph grammars and declared verification targets, a side branch and not the next Genesis stage, so MSS-2 ≠ S(2). Its 101 rows MSS-0 to MSS-100 are proposed capability rows: each row is a specification target and a stated obligation, not evidence that the target was met. Coverage C(N) counts specified rows, and licensed depth D(k) is the length of an unbroken chain of machine-checked lift records. No licensed lift exists, so D = 0, and 100 rows give C(100) coverage without showing that row 0 generated row 100.

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

- MSS-N atlas of 101 rows, externally designed and not constrained to blind derivation (assumption)

## Bottleneck

Per-row evidence flags and evaluator names are catalogue metadata, not test or proof receipts; levels graded COMPUTED (0, 1, 23, 35, 36, 48) receive shape checks by level membership and do not give depth 6.

## Source status

pregenesis_to_minimal_symbol_systems paper.md section 6; 003_oemssn curriculum.md Lesson 1 and levels/README.md section 1

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md`

- file: [atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md](../../../atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md)
- sha256 (`lf-normalised`): `a4a7d840b11e912896032aebc9ead95f7978c0e6f60656f44645c6d8fadf593b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0528_mssn_atlas_not_derivation.md`

- file: [dag/derivations/05_mssn_sn/tfq_0528_mssn_atlas_not_derivation.md](../../../dag/derivations/05_mssn_sn/tfq_0528_mssn_atlas_not_derivation.md)
- sha256 (`lf-normalised`): `903d6bea6989d0cb5795c7fb05348b6d4c06a196fbde6fefc5d6d93a0d3a16dc`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0528
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:6313c51659873eb093e3ef4171a13eac33217dd96e168a97416623d6248005b9:27-35`
- `external:sha256:ea610e33827464418f0f2786ff65c9af072659bf2884a9411900e07d482e9740:22-28`

## Absences recorded by the TFQ records

- TFQ-0528 lean4: no Lean statement of atlas coverage or licensed depth
- TFQ-0528 python: no Python count of licensed depth
- TFQ-0528 rust: no Rust lift-record chain; no licensed lift exists

## Routes

Incoming (1):

- `PGW-R-MSSN-ATLAS-NOT-DERIVATION` `DERIVED_PROSE`: [PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL](PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL.md) (PROVED_LEAN), [TFQ-0368](TFQ-0368.md) (SOURCE_RECORD)

Outgoing (1):

- `PGW-R-MSSN-ASCENT-TRIAD` `DERIVED_PROSE`: [PGW-MSSN-ASCENT-TRIAD](PGW-MSSN-ASCENT-TRIAD.md) (DEFINITION)
