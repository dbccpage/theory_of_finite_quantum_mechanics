# PGW-SN-POSTNIKOV-REFUSAL

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_PROSE`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The construction index n of S(n) is distinct from Postnikov depth j. For j ≥ 0 the Postnikov truncations of a fixed space preserve π₀, so an empty space followed by a point cannot be two truncations of one space. If a topological realization ρ is supplied, its tower at fixed n is written P_j(ρ(S(n))) with its own hypotheses, and growth across n stays a separate construction that needs its own maps and preservation proofs. The combined paper lists S(n) is automatically a Postnikov tower among withdrawn inferences, and ledger row WDP-P001-017 withdraws automatic Postnikov structure.

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

- `proved_prose_no_in_repo_document`: no in-repo non-generated document among the counted sources. PROVED_PROSE with no in-repo source document cited.

## Imported structure

- A topological realization ρ of S(n) with preservation maps, which the source does not supply (assumption)

## Bottleneck

This refuses the identification of S(n) with a Postnikov tower; it constructs no realization ρ and no Postnikov tower of one, and the withdrawn WDP-P001-017 row is not reactivated.

## Source status

002_oesn sn.md section 4 (written pi0 argument); 000_pre_genesis_to_mssn paper.md section 16; ledger WDP-P001-017 withdrawn

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0520_sn_postnikov_refusal.md`

- file: [dag/derivations/05_mssn_sn/tfq_0520_sn_postnikov_refusal.md](../../../dag/derivations/05_mssn_sn/tfq_0520_sn_postnikov_refusal.md)
- sha256 (`lf-normalised`): `fa938310a6c4653f7e163861b23b22a76044d47af29061aa4560fc23f38331f1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0520
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/paper_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/paper_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/002_oesn/sn.md`

- file: `omega_engine_education/documentation/002_oesn/sn.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0520 lean4: no Lean statement about Postnikov truncations in the S(n) or MSS-N packages
- TFQ-0520 python: no Python check of Postnikov truncations
- TFQ-0520 rust: no Rust check of Postnikov truncations

## Routes

Incoming (1):

- `PGW-R-SN-POSTNIKOV-REFUSAL` `DERIVED_PROSE`: [PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL](PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-GENESIS-BRIDGES-LEDGER` `DERIVED_PROSE`: [PGW-WDP-GENESIS-BRIDGES-LEDGER](PGW-WDP-GENESIS-BRIDGES-LEDGER.md) (DEFINITION)
