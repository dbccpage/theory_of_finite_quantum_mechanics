# CQFT-FINITE-STRICT-POSET-SPACELIKE

Stage: [CAUSAL_QFT](../stages/CAUSAL_QFT.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> lean4/CausalOrder.lean defines FiniteStrictPoset n (an irreflexive transitive relation on Fin n) and spacelike separation (x differs from y and neither precedes the other). It establishes spacelike_symm and spacelike_irrefl; on the named examples C1 (0\<1, 0\<2), C2 (the four-element diamond) and N4 (the four-element N poset with 0\<2, 1\<2, 1\<3) it establishes c1_spacelike_1_2, c1_spacelike_symm_irrefl (with a deprecated alias incomparability_not_transitive_c1), c2_causal_0_3, n4_spacelike_not_transitive, spacelike_not_transitive (three distinct elements d0, d3, d2 on N4 with d0 spacelike to d3 and d3 spacelike to d2 while d0\<d2), order_independence_witness (C1 and its dual differ) and the table entries c1_mu_spacelike_vanishes and c2_mu_top_bottom (value 1). Scope: four decided examples, no general causal-set theory. The table c2_mu is checked entry by entry; the Lean file does not state the Mobius recursion for it.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 11
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 10 Lean reference(s) cited, 10 in this checkout (replay: none 10). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

The table c2_mu is checked entry by entry on C2; a general Mobius recursion over FiniteStrictPoset n is not formalized in CausalOrder.lean.

## Source status

Declarations read in this change from the cited Lean file, which is a root in lean4/lakefile.lean; the file was not rebuilt here.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CausalOrder.lean`

- file: [lean4/CausalOrder.lean](../../../lean4/CausalOrder.lean)
- sha256 (`bytes`): `f8f04b749262b26eeae39f3fc0d96b55e3fd02283f7df29a1c2042faf017edf0`
- cited in: node.lean, record TFQ-2100
- replay: `none`
- check: `cd lean4 && lake build CausalOrder`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `c1_mu_spacelike_vanishes` | yes | yes | yes | - | `#print axioms c1_mu_spacelike_vanishes` |
| `c1_spacelike_1_2` | yes | yes | yes | - | `#print axioms c1_spacelike_1_2` |
| `c1_spacelike_symm_irrefl` | yes | yes | yes | - | `#print axioms c1_spacelike_symm_irrefl` |
| `c2_causal_0_3` | yes | yes | yes | - | `#print axioms c2_causal_0_3` |
| `c2_mu_top_bottom` | yes | yes | yes | - | `#print axioms c2_mu_top_bottom` |
| `incomparability_not_transitive_c1` | yes | yes | yes | - | `#print axioms incomparability_not_transitive_c1` |
| `n4_spacelike_not_transitive` | yes | yes | yes | - | `#print axioms n4_spacelike_not_transitive` |
| `order_independence_witness` | yes | yes | yes | - | `#print axioms order_independence_witness` |
| `spacelike_irrefl` | yes | yes | yes | - | `#print axioms spacelike_irrefl` |
| `spacelike_not_transitive` | yes | yes | yes | - | `#print axioms spacelike_not_transitive` |
| `spacelike_symm` | yes | yes | yes | - | `#print axioms spacelike_symm` |
- counts toward the grade: yes

### Python: `code/python/src/general_relativity/causal_set.py`

- file: [code/python/src/general_relativity/causal_set.py](../../../code/python/src/general_relativity/causal_set.py)
- sha256 (`bytes`): `fe0391e534586e7ef4b5856b1c9f9fa190a19f55fdd368e36d85950ef1af92fb`
- cited in: node.source
- counts toward the grade: yes

### Python: `code/python/src/qm/causal_order.py`

- file: [code/python/src/qm/causal_order.py](../../../code/python/src/qm/causal_order.py)
- sha256 (`bytes`): `a1ca43c436feb220b99eb2274b2019e9ad5cd4d61781db5e3d695895863a44d9`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/31_causal_qft/tfq_2100_cqft_finite_strict_poset_spacelike.md`

- file: [dag/derivations/31_causal_qft/tfq_2100_cqft_finite_strict_poset_spacelike.md](../../../dag/derivations/31_causal_qft/tfq_2100_cqft_finite_strict_poset_spacelike.md)
- sha256 (`lf-normalised`): `18dceff1280637c1bf88af34fa3998b4e1e8b01ccc635e30b5d40c7319f2e507`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2100
- counts toward the grade: no

## Routes

Incoming (1):

- `FRO-R-CQFT-FINITE-STRICT-POSET-SPACELIKE` `RECORD_PARENT`: [DS-QM074-NO-SIGNALING-MARGINAL](DS-QM074-NO-SIGNALING-MARGINAL.md) (PROVED_LEAN)

Outgoing (5):

- `FRO-R-CQFT-BLMS-1987-SOURCE` `RECORD_PARENT`: [CQFT-BLMS-1987-SOURCE](CQFT-BLMS-1987-SOURCE.md) (SOURCE_RECORD)
- `FRO-R-CQFT-FINITE-CAUSET-IDENTIFICATION` `DERIVED_PROSE`: [CQFT-FINITE-CAUSET-IDENTIFICATION](CQFT-FINITE-CAUSET-IDENTIFICATION.md) (DEFINITION)
- `FRO-R-CQFT-FINITE-POSET-NET-TARGET` `DERIVED_LEAN`: [CQFT-FINITE-POSET-NET-TARGET](CQFT-FINITE-POSET-NET-TARGET.md) (PROVED_LEAN)
- `FRO-R-CQFT-HAAG-KASTLER-1964-SOURCE` `RECORD_PARENT`: [CQFT-HAAG-KASTLER-1964-SOURCE](CQFT-HAAG-KASTLER-1964-SOURCE.md) (SOURCE_RECORD)
- `FRO-R-CQFT-ORDERED-PRODUCT-LINEAR-EXTENSION-TARGET` `DERIVED_LEAN`: [CQFT-ORDERED-PRODUCT-LINEAR-EXTENSION-TARGET](CQFT-ORDERED-PRODUCT-LINEAR-EXTENSION-TARGET.md) (PROVED_LEAN)
