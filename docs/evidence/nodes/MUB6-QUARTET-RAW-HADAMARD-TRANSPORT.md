# MUB6-QUARTET-RAW-HADAMARD-TRANSPORT

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A quartet of pairwise unbiased orthonormal bases of C^6 exists iff some 6x6 matrix H has a raw quartet: H, U, V with unit-modulus entries, M* M = 6I, and |(A* B)_ij|^2 = 6 for each pair; raw-quartet existence is invariant under row and column permutation-phase equivalence.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Global exclusion still needs complete representative coverage and nonextension for every representative, which no_quartet_of_concrete_representatives takes as hypotheses.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-056 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/MubMonomialTransport.lean`

- file: [lean4/MubMonomialTransport.lean](../../../lean4/MubMonomialTransport.lean)
- sha256 (`bytes`): `1e0f4d069de79c8c48da3425acc14a335bc13ee6d0ebeee4af1f234323e4aa63`
- cited in: node.lean, record TFQ-1225
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `MubMonomialTransport`): recorded sha256 `1e0f4d069de79c8c48da3425acc14a335bc13ee6d0ebeee4af1f234323e4aa63` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build MubMonomialTransport`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `hasRawQuartet_iff_of_monomialEquivalent` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms hasRawQuartet_iff_of_monomialEquivalent` |

- counts toward the grade: yes

### Lean: `lean4/MubQuartetTransportBridge.lean`

- file: [lean4/MubQuartetTransportBridge.lean](../../../lean4/MubQuartetTransportBridge.lean)
- sha256 (`bytes`): `9a8fe3fc0f59e06b2c1e5b53bdfd5f63b4ae197f0adfee76008a034acd36afb5`
- cited in: node.lean, record TFQ-1225
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `MubQuartetTransportBridge`): recorded sha256 `9a8fe3fc0f59e06b2c1e5b53bdfd5f63b4ae197f0adfee76008a034acd36afb5` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build MubQuartetTransportBridge`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `exists_quartet_iff_exists_rawQuartet` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms exists_quartet_iff_exists_rawQuartet` |
| `no_quartet_of_concrete_representatives` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms no_quartet_of_concrete_representatives` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1225_mub6_quartet_raw_hadamard_transport.md`

- file: [dag/derivations/25_mub/tfq_1225_mub6_quartet_raw_hadamard_transport.md](../../../dag/derivations/25_mub/tfq_1225_mub6_quartet_raw_hadamard_transport.md)
- sha256 (`lf-normalised`): `8ea4466aeaef7ba6a33f51565491e8bb63d89f2715cd8b2e37dacdb030fb974c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1225
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `31ddd89d2594bb5ad401aadb99a3a91edb6ea8e33158386031a40b1dc36f7223`
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

- `APP-R-MUB6-QUARTET-RAW-HADAMARD-TRANSPORT` `DERIVED_LEAN`: [MUB-EXACT-PROJECTORS](MUB-EXACT-PROJECTORS.md) (DEFINITION)

Outgoing (11):

- `APP-R-MUB6-CAUCHY-BINET-MINOR-BOUND` `DERIVED_LEAN`: [MUB6-CAUCHY-BINET-MINOR-BOUND](MUB6-CAUCHY-BINET-MINOR-BOUND.md) (PROVED_LEAN)
- `APP-R-MUB6-CORNER-ROUTING-DEPHASING` `DERIVED_LEAN`: [MUB6-CORNER-ROUTING-DEPHASING](MUB6-CORNER-ROUTING-DEPHASING.md) (PROVED_LEAN)
- `APP-R-MUB6-FIXED-TRIPLE-VARIETY` `DERIVED_LEAN`: [MUB6-FIXED-TRIPLE-VARIETY](MUB6-FIXED-TRIPLE-VARIETY.md) (PROVED_LEAN)
- `APP-R-MUB6-FOURIER-DITA-FAMILY-CHM` `DERIVED_LEAN`: [MUB6-FOURIER-DITA-FAMILY-CHM](MUB6-FOURIER-DITA-FAMILY-CHM.md) (PROVED_LEAN)
- `APP-R-MUB6-HAAGERUP-MATRIX-CHM` `DERIVED_LEAN`: [MUB6-HAAGERUP-MATRIX-CHM](MUB6-HAAGERUP-MATRIX-CHM.md) (PROVED_LEAN)
- `APP-R-MUB6-KARLSSON-AFFINE-ANSATZ` `DERIVED_LEAN`: [MUB6-KARLSSON-AFFINE-ANSATZ](MUB6-KARLSSON-AFFINE-ANSATZ.md) (PROVED_LEAN)
- `APP-R-MUB6-QUADRATIC-LIFT-386` `DERIVED_LEAN`: [MUB6-QUADRATIC-LIFT-386](MUB6-QUADRATIC-LIFT-386.md) (PROVED_LEAN)
- `APP-R-MUB6-SZOLLOSI-COMMON-RAYS` `DERIVED_LEAN`: [MUB6-SZOLLOSI-COMMON-RAYS](MUB6-SZOLLOSI-COMMON-RAYS.md) (PROVED_LEAN)
- `APP-R-MUB6-SZOLLOSI-TWO-CIRCULANT` `DERIVED_LEAN`: [MUB6-SZOLLOSI-TWO-CIRCULANT](MUB6-SZOLLOSI-TWO-CIRCULANT.md) (PROVED_LEAN)
- `APP-R-MUB6-TAO-MATRIX-CHM` `DERIVED_LEAN`: [MUB6-TAO-MATRIX-CHM](MUB6-TAO-MATRIX-CHM.md) (PROVED_LEAN)
- `APP-R-MUB6-TRANSITION-BALANCE-SYZYGY` `DERIVED_LEAN`: [MUB6-TRANSITION-BALANCE-SYZYGY](MUB6-TRANSITION-BALANCE-SYZYGY.md) (PROVED_LEAN)
