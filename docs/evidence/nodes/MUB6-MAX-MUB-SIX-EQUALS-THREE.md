# MUB6-MAX-MUB-SIX-EQUALS-THREE

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Open problem: the maximum number of pairwise mutually unbiased bases in C^6 is three.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The lower bound three is checked (MUB6-DERIV-063); the upper bound is equivalent to MUB6-DERIV-085 and is open; the cited Lean name MUB.TerminalTheorem.max_mub_six_equals_three does not exist in this checkout. N(6) \<= 5 is recorded separately as MUB6-OPENAI-FAMILY-LE-FIVE (external theorem of OpenAI, not built here); it does not decide whether a quartet exists. OpenAI N(6)=3 is recorded as external context only: a binary64 seed-cover, Stage A/B/C and clique-search pipeline whose code and run archive are unreleased (verification/ returns 404) and whose Lean tree does not formalize it; it is not imported.

## Source status

dag/derivations/25_mub/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-086 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/25_mub/mub6/README.md`

- file: [dag/derivations/25_mub/mub6/README.md](../../../dag/derivations/25_mub/mub6/README.md)
- sha256 (`lf-normalised`): `fcf24743ee6d9dab9c377dc5158e9cac9769f062d7defbfb006e053c55255bf9`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/mub6/mub6_change_log.md`

- file: [dag/derivations/25_mub/mub6/mub6_change_log.md](../../../dag/derivations/25_mub/mub6/mub6_change_log.md)
- sha256 (`lf-normalised`): `22c69b95eea012b3e0be02f10274bb53152f14cf487e289edcad3a02b45c7871`
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

### Documents and data: `dag/derivations/25_mub/tfq_1255_mub6_max_mub_six_equals_three.md`

- file: [dag/derivations/25_mub/tfq_1255_mub6_max_mub_six_equals_three.md](../../../dag/derivations/25_mub/tfq_1255_mub6_max_mub_six_equals_three.md)
- sha256 (`lf-normalised`): `0712afc90a04b256308bf63fde1172a68da0eb6b21dbb59b68822c44a8d66035`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1255
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-MUB6-MAX-MUB-SIX-EQUALS-THREE` `GAP_NO_DERIVATION`: [MUB6-GLOBAL-OBLIGATIONS](MUB6-GLOBAL-OBLIGATIONS.md) (OPEN), [MUB6-NO-QUARTET-D6](MUB6-NO-QUARTET-D6.md) (OPEN), [MUB6-PRODUCT-TRIPLE-LOWER-BOUND](MUB6-PRODUCT-TRIPLE-LOWER-BOUND.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

