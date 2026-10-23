# CQFT-REEH-SCHLIEDER-THEOREM-IMPORT

Stage: [CAUSAL_QFT](../stages/CAUSAL_QFT.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Imported property: in a net of local algebras on Minkowski space with a translation action whose generators have positive spectrum (spectrum condition) and a vacuum vector, the vacuum is cyclic for every local algebra, and under further hypotheses separating for the algebra of a region with spacelike complement. The proof uses analytic continuation of translations, hence a continuous translation group and its generator (Stone's theorem) on an infinite-dimensional Hilbert space. Both are open nodes of the repository.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- spectrum condition and continuous translation group (assumption)
- vacuum vector (assumption)

## Bottleneck

The inputs of the property are the continuum Hilbert lift and the Stone theorem, which the repository records as open. The gap route below lists them.

## Source status

Taken from the cited source as an assumption of this branch; the source's own hypotheses and exact wording are not audited here.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/31_causal_qft/tfq_2106_cqft_reeh_schlieder_theorem_import.md`

- file: [dag/derivations/31_causal_qft/tfq_2106_cqft_reeh_schlieder_theorem_import.md](../../../dag/derivations/31_causal_qft/tfq_2106_cqft_reeh_schlieder_theorem_import.md)
- sha256 (`lf-normalised`): `02c7acd87ac5490bb7230c41036bd3f46f2c56e966ca16edb9dd1050c9c186a6`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2106
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:Nuovo-Cimento-22-1051-1961`
- `external:doi:10.1063/1.1704187`

## Routes

Incoming (2):

- `FRO-R-CQFT-REEH-SCHLIEDER-THEOREM-IMPORT` `CONDITIONAL_ON_IMPORT`: [CQFT-REEH-SCHLIEDER-1961-SOURCE](CQFT-REEH-SCHLIEDER-1961-SOURCE.md) (SOURCE_RECORD)
- `FRO-R-CQFT-REEH-SCHLIEDER-THEOREM-IMPORT-X1` `GAP_NO_DERIVATION`: [FQ-GAP-STONE-CONTINUOUS-TIME](FQ-GAP-STONE-CONTINUOUS-TIME.md) (CONDITIONAL), [FQ-GAP-CONTINUUM-HILBERT-LIFT](FQ-GAP-CONTINUUM-HILBERT-LIFT.md) (CONDITIONAL)

Outgoing (1):

- `FRO-R-CQFT-RS-FINITE-CYCLICITY-TARGET` `DERIVED_LEAN`: [CQFT-RS-FINITE-CYCLICITY-TARGET](CQFT-RS-FINITE-CYCLICITY-TARGET.md) (PROVED_LEAN)
