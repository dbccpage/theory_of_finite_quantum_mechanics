# CQFT-CAUSAL-FACTORIZATION-IMPORT

Stage: [CAUSAL_QFT](../stages/CAUSAL_QFT.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Imported property, audited and corrected against Epstein and Glaser (1973, Section 1.1 condition (C.A.) pp. 214-215, Section 2.1 condition (Caus. 1) eq. (9) p. 218, Section 2.2 eq. (30) p. 223) and Brunetti and Fredenhagen (2000, arXiv:math-ph/9903028, Section 1 eq. (2) p. 4 and Section 3 Condition P3 p. 15): the scattering operator satisfies V(g, h1+h2) = S(g)^{-1} S(g+h1+h2) = V(g, h1) V(g, h2) (and at g=0, S(g1+g2) = S(g1) S(g2)) whenever supp h1 does not intersect the causal past of supp h2, written supp h1 cap (supp h2 + V^-) = empty (which includes spacelike separation as well as causal future separation, not only supp h1 inside the causal future of supp h2). Equivalently at each order n, the time-ordered operator-valued distributions factorize as T(P union Q) = T(P) T(Q) whenever {x_i : i in P} cap ({x_j : j in Q} + V^-) = empty (eq. (30) p. 223; Condition P3 p. 15), and renormalization reduces to extending time-ordered products across the total diagonal. The repository has neither operator-valued distributions nor a continuum Minkowski causal cone.

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

- operator-valued distributions (assumption)
- time ordering on spacetime (assumption)

## Bottleneck

Audited against Epstein-Glaser (1973) eqs. (9), (30) and Brunetti-Fredenhagen (2000) eq. (2) and Condition P3. The continuum distribution extension has no counterpart in the repository's finite posets.

## Source status

Audited and corrected against the full texts of Epstein and Glaser (1973, Section 1.1 pp. 214-215, Section 2.1 eq. (9) p. 218, Section 2.2 eq. (30) p. 223) and Brunetti and Fredenhagen (2000, arXiv:math-ph/9903028, Section 1 eq. (2) p. 4, Section 3 Condition P3 p. 15) on 2026-10-22; taken as an imported assumption of this branch.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/31_causal_qft/tfq_2109_cqft_causal_factorization_import.md`

- file: [dag/derivations/31_causal_qft/tfq_2109_cqft_causal_factorization_import.md](../../../dag/derivations/31_causal_qft/tfq_2109_cqft_causal_factorization_import.md)
- sha256 (`lf-normalised`): `0570d4c3d7868b0b56a25702a8fa11febcca555a0e21f1dfe2bcf5029cfa1e8b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2109
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:math-ph/9903028`
- `external:numdam:AIHPA_1973__19_3_211_0`

## Routes

Incoming (1):

- `FRO-R-CQFT-CAUSAL-FACTORIZATION-IMPORT` `CONDITIONAL_ON_IMPORT`: [CQFT-EPSTEIN-GLASER-1973-SOURCE](CQFT-EPSTEIN-GLASER-1973-SOURCE.md) (SOURCE_RECORD)

Outgoing (1):

- `FRO-R-CQFT-ORDERED-PRODUCT-LINEAR-EXTENSION-TARGET` `DERIVED_LEAN`: [CQFT-ORDERED-PRODUCT-LINEAR-EXTENSION-TARGET](CQFT-ORDERED-PRODUCT-LINEAR-EXTENSION-TARGET.md) (PROVED_LEAN)
