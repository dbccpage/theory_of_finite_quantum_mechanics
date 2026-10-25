# MUB6-WEYL-HEISENBERG-D6

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On C^6 with shift X|j\> = |j+1 mod 6\> and clock Z|j\> = w^j |j\>, w = exp(2 pi i/6), one has Z X = w X Z, and the 36 operators X^p Z^q are pairwise orthogonal for the trace pairing tr(A* B).

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Weyl-Heisenberg commutation and Hilbert-Schmidt orthogonality of displacement operators (standard)

## Bottleneck

These standard identities are not checked in this checkout for d = 6; the source writes X Z = w Z X, which holds only under the opposite clock convention; no MUB count follows from them.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-053 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/25_mub/tfq_1223_mub6_weyl_heisenberg_d6.md`

- file: [dag/derivations/25_mub/tfq_1223_mub6_weyl_heisenberg_d6.md](../../../dag/derivations/25_mub/tfq_1223_mub6_weyl_heisenberg_d6.md)
- sha256 (`lf-normalised`): `42914161de12fcd9ff1b4206dbfbcb02950bcbd5394b458c717ef80b69eb4619`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1223
- counts toward the grade: no

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

- `APP-R-MUB6-WEYL-HEISENBERG-D6` `CONDITIONAL_ON_IMPORT`: [MUB6-QUHEX-TENSOR-CARRIER](MUB6-QUHEX-TENSOR-CARRIER.md) (DEFINITION)

Outgoing (1):

- `APP-R-MUB6-WEYL-STABILIZER-BOUND` `GAP_NO_DERIVATION`: [MUB6-WEYL-STABILIZER-BOUND](MUB6-WEYL-STABILIZER-BOUND.md) (OPEN)
