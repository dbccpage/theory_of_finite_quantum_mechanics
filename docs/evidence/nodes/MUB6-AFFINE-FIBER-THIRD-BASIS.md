# MUB6-AFFINE-FIBER-THIRD-BASIS

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `REFUTED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Refuted claim: no affine family through F_2 tensor F_3 contains a third basis unbiased to both the identity and the base matrix; the product triple I_6, F_2 tensor F_3 / sqrt 6, and A_2 tensor C_2 (itself row-phase equivalent to F_2 tensor F_3) is pairwise unbiased.

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

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Affine-fiber stratification of CHM(6) is not formalized; the counterexample is the exact SymPy check of the product triple recorded at MUB6-DERIV-063.

## Source status

dag/derivations/25_mub/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-062 claims PROVED_LEAN; audited status REFUTED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `dag/derivations/25_mub/mub6/research/five_derivations_20261015/verify_symbolic.py`

- file: [dag/derivations/25_mub/mub6/research/five_derivations_20261015/verify_symbolic.py](../../../dag/derivations/25_mub/mub6/research/five_derivations_20261015/verify_symbolic.py)
- sha256 (`bytes`): `99fbbe53afb24df19d0d4db5993e7e7a21c2531b0027f7d0383eff2da5e016c3`
- cited in: record TFQ-1231

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `three_bases` (python_symbol) | yes | yes | yes | - | - |
| `verify_three_bases` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/mub6/documentation/theorem_mub6_lower_bound_kronecker_construction.md`

- file: [dag/derivations/25_mub/mub6/documentation/theorem_mub6_lower_bound_kronecker_construction.md](../../../dag/derivations/25_mub/mub6/documentation/theorem_mub6_lower_bound_kronecker_construction.md)
- sha256 (`lf-normalised`): `5a2a33acb6179ab69d7fb75477c83b1092758c24ace7b24b7d26f96f66d46f27`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/mub6/theory_of_finite_mub6.jsonl`

- file: [dag/derivations/25_mub/mub6/theory_of_finite_mub6.jsonl](../../../dag/derivations/25_mub/mub6/theory_of_finite_mub6.jsonl)
- sha256 (`lf-normalised`): `815b535641140895e823e99e201cf3314a9054db022f5a0c35be601a18663839`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/mub6/theory_of_finite_mub6.md`

- file: [dag/derivations/25_mub/mub6/theory_of_finite_mub6.md](../../../dag/derivations/25_mub/mub6/theory_of_finite_mub6.md)
- sha256 (`lf-normalised`): `0e5866c8c56eb624576b512e2f51f0378271797285bb11c764a9708a234085e1`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1231_mub6_affine_fiber_third_basis.md`

- file: [dag/derivations/25_mub/tfq_1231_mub6_affine_fiber_third_basis.md](../../../dag/derivations/25_mub/tfq_1231_mub6_affine_fiber_third_basis.md)
- sha256 (`lf-normalised`): `5f31755a4fe921827f0177534d9cb07d1e7e89f0ccc8b7404908b5f8f78e3939`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1231
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-MUB6-AFFINE-FIBER-THIRD-BASIS` `DERIVED_PROSE`: [MUB6-FOURIER-DITA-FAMILY-CHM](MUB6-FOURIER-DITA-FAMILY-CHM.md) (PROVED_LEAN)

Outgoing (0):

