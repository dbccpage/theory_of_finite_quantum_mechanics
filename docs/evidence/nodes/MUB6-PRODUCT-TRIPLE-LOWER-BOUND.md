# MUB6-PRODUCT-TRIPLE-LOWER-BOUND

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The bases U_r = A_r tensor C_r (r = 0, 1, 2) of C^6, with A_r = I, F_2, \[\[1,1\],\[i,-i\]\]/sqrt 2 and C_r = I, F_3, diag(1,w,w) F_3, are unitary and pairwise unbiased with squared overlaps 1/6, so C^6 has at least three MUBs.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `computational_no_runnable_test`: 2 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

None recorded.

## Bottleneck

This fixed triple is not the source triad {I_6, F_6, B_3} with a dephased circulant B_3, which is not checked; a fourth basis for any triple remains open (MUB6-GLOBAL-OBLIGATIONS).

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-063 claims PROVED_LEAN; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `papers/core/mub6/research/five_derivations_20261015/verify_symbolic.py`

- file: [papers/core/mub6/research/five_derivations_20261015/verify_symbolic.py](../../../papers/core/mub6/research/five_derivations_20261015/verify_symbolic.py)
- sha256 (`bytes`): `99fbbe53afb24df19d0d4db5993e7e7a21c2531b0027f7d0383eff2da5e016c3`
- cited in: record TFQ-1232

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `three_bases` (python_symbol) | yes | yes | yes | - | - |
| `verify_three_bases` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1232_mub6_product_triple_lower_bound.md`

- file: [dag/derivations/25_mub/tfq_1232_mub6_product_triple_lower_bound.md](../../../dag/derivations/25_mub/tfq_1232_mub6_product_triple_lower_bound.md)
- sha256 (`lf-normalised`): `00a26667a91ac862fca43189de6beec89301212ab1cbd2e4a3763fd82836c0c1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1232
- counts toward the grade: no

### Documents and data: `papers/core/mub6/documentation/theorem_mub6_lower_bound_kronecker_construction.md`

- file: [papers/core/mub6/documentation/theorem_mub6_lower_bound_kronecker_construction.md](../../../papers/core/mub6/documentation/theorem_mub6_lower_bound_kronecker_construction.md)
- sha256 (`lf-normalised`): `5a2a33acb6179ab69d7fb75477c83b1092758c24ace7b24b7d26f96f66d46f27`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/theory_of_finite_mub6.jsonl`

- file: [papers/core/mub6/theory_of_finite_mub6.jsonl](../../../papers/core/mub6/theory_of_finite_mub6.jsonl)
- sha256 (`lf-normalised`): `815b535641140895e823e99e201cf3314a9054db022f5a0c35be601a18663839`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/theory_of_finite_mub6.md`

- file: [papers/core/mub6/theory_of_finite_mub6.md](../../../papers/core/mub6/theory_of_finite_mub6.md)
- sha256 (`lf-normalised`): `b515bf981d6c3a339c2b0a7937d54d9deb05f3b53186c584b83f5fa3419dc902`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-PRODUCT-TRIPLE-LOWER-BOUND` `COMPUTED`: [MUB6-QUHEX-TENSOR-CARRIER](MUB6-QUHEX-TENSOR-CARRIER.md) (DEFINITION), [MUB-EXACT-PROJECTORS](MUB-EXACT-PROJECTORS.md) (DEFINITION)

Outgoing (1):

- `APP-R-MUB6-MAX-MUB-SIX-EQUALS-THREE` `GAP_NO_DERIVATION`: [MUB6-MAX-MUB-SIX-EQUALS-THREE](MUB6-MAX-MUB-SIX-EQUALS-THREE.md) (OPEN)
