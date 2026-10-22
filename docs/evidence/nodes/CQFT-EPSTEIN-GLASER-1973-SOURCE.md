# CQFT-EPSTEIN-GLASER-1973-SOURCE

Stage: [CAUSAL_QFT](../stages/CAUSAL_QFT.md). Status: `SOURCE_RECORD`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Epstein and Glaser (1973, Ann. Inst. H. Poincare A 19, 211-295, Abstract p. 211, Section 1.1 pp. 214-215, Section 2.1 eq. (9) p. 218, Section 2.2 eq. (30) p. 223, and Section 5 pp. 231-237) give an inductive construction of the perturbation series S(g) = 1 + sum_{n\>=1} (i^n / n!) int T_n(x_1,...,x_n) g(x_1)...g(x_n) dx in which each order T_n is constructed from lower orders by causal factorization outside the total diagonal and by splitting causal distributions with scaling degree bounds on the diagonal. This node records the paper as published.

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

None recorded.

## Bottleneck

Record only. Audited against the Numdam full text (AIHPA_1973__19_3_211_0); nothing in the paper is used as a premise of a repository theorem.

## Source status

Audited against the full Numdam PDF of Epstein and Glaser (1973, Ann. Inst. H. Poincare A 19, 211-295, Sections 1-5 pp. 211-237) on 2026-10-22; recorded as an external source record.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/31_causal_qft/tfq_2108_cqft_epstein_glaser_1973_source.md`

- file: [dag/derivations/31_causal_qft/tfq_2108_cqft_epstein_glaser_1973_source.md](../../../dag/derivations/31_causal_qft/tfq_2108_cqft_epstein_glaser_1973_source.md)
- sha256 (`lf-normalised`): `605bbe07aa6d2d068fdd033f95c097fa72c26ab46b5d5bcea8a09d12ee0650f4`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2108
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:numdam:AIHPA_1973__19_3_211_0`

## Routes

Incoming (1):

- `FRO-R-CQFT-EPSTEIN-GLASER-1973-SOURCE` `RECORD_PARENT`: [CQFT-LOCAL-NET-AXIOMS-IMPORT](CQFT-LOCAL-NET-AXIOMS-IMPORT.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `FRO-R-CQFT-CAUSAL-FACTORIZATION-IMPORT` `CONDITIONAL_ON_IMPORT`: [CQFT-CAUSAL-FACTORIZATION-IMPORT](CQFT-CAUSAL-FACTORIZATION-IMPORT.md) (IMPORTED_ASSUMPTION)
