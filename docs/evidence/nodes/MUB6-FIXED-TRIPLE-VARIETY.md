# MUB6-FIXED-TRIPLE-VARIETY

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a fixed triple T of complex 6x6 matrices and a candidate U in 72 real coordinates, each MU residual equals tr(P_{T_a,i} P_{U,j}) - 1/6, and the real zero set of the 108 MU and 72 orthonormality residuals is empty iff no U has U* U = I and |\<T_a,i, U_j\>|^2 = 1/6 for all a, i, j.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Emptiness is not established for any MU triple or uniformly over a family; a complete seven-basis family would make the variety of its first three bases nonempty (family_triple_variety_nonempty).

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-064 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/ConcreteMubPolynomials.lean`

- file: [lean4/ConcreteMubPolynomials.lean](../../../lean4/ConcreteMubPolynomials.lean)
- sha256 (`bytes`): `bbb3720eb5391c9fdd3ac7f2781cff250dde03931f564befc2472e7c92080955`
- cited in: node.lean, record TFQ-1233
- replay: `none`
- check: `cd lean4 && lake build ConcreteMubPolynomials`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `family_triple_variety_nonempty` | yes | yes | yes | - | `#print axioms family_triple_variety_nonempty` |
| `muPolynomial_eval_projector_trace` | yes | yes | yes | - | `#print axioms muPolynomial_eval_projector_trace` |
| `polynomialIdeal_le_eval_kernel_iff` | yes | yes | yes | - | `#print axioms polynomialIdeal_le_eval_kernel_iff` |
| `polynomialVariety_eq_empty_iff` | yes | yes | yes | - | `#print axioms polynomialVariety_eq_empty_iff` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1233_mub6_fixed_triple_variety.md`

- file: [dag/derivations/25_mub/tfq_1233_mub6_fixed_triple_variety.md](../../../dag/derivations/25_mub/tfq_1233_mub6_fixed_triple_variety.md)
- sha256 (`lf-normalised`): `bd05b7e6477d568c8c7e3909e287f3612f7dd061f48078ce8277e96b048831c3`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1233
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `edeb29b681854d6ff67bdf072e4d3163995e068973662ebb77220ba009345238`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/mub6_claim_ledger.md`

- file: [papers/core/mub6/mub6_claim_ledger.md](../../../papers/core/mub6/mub6_claim_ledger.md)
- sha256 (`lf-normalised`): `e21c9d2f20bd0e87979c8b003ab6e2c60422c19cfdd0117308db09ec10c47f7a`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/theory_of_finite_mub6.jsonl`

- file: [papers/core/mub6/theory_of_finite_mub6.jsonl](../../../papers/core/mub6/theory_of_finite_mub6.jsonl)
- sha256 (`lf-normalised`): `79a8e74d457a2c236999a6a1dcd1ff010f0f878b245c205f5f049add18ae2234`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/theory_of_finite_mub6.md`

- file: [papers/core/mub6/theory_of_finite_mub6.md](../../../papers/core/mub6/theory_of_finite_mub6.md)
- sha256 (`lf-normalised`): `4df95e7f697d7ab11bfa44f282353267197198f74bcfb535e5f10c18ffbeabf5`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-FIXED-TRIPLE-VARIETY` `DERIVED_LEAN`: [MUB6-QUARTET-RAW-HADAMARD-TRANSPORT](MUB6-QUARTET-RAW-HADAMARD-TRANSPORT.md) (PROVED_LEAN), [MUB-EXACT-PROJECTORS](MUB-EXACT-PROJECTORS.md) (DEFINITION)

Outgoing (4):

- `APP-R-MUB6-180-RESIDUAL-COUNT` `DERIVED_LEAN`: [MUB6-180-RESIDUAL-COUNT](MUB6-180-RESIDUAL-COUNT.md) (PROVED_LEAN)
- `APP-R-MUB6-FOURTH-BASIS-FLAT-MOMENTS` `DERIVED_LEAN`: [MUB6-FOURTH-BASIS-FLAT-MOMENTS](MUB6-FOURTH-BASIS-FLAT-MOMENTS.md) (PROVED_LEAN)
- `APP-R-MUB6-MOMENT-EVALUATION-FLAT` `DERIVED_LEAN`: [MUB6-MOMENT-EVALUATION-FLAT](MUB6-MOMENT-EVALUATION-FLAT.md) (PROVED_LEAN)
- `APP-R-MUB6-POSITIVSTELLENSATZ-CLAIM` `GAP_NO_DERIVATION`: [MUB6-POSITIVSTELLENSATZ-CLAIM](MUB6-POSITIVSTELLENSATZ-CLAIM.md) (OPEN)
