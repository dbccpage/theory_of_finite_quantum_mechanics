# CQFT-ORDERED-PRODUCT-LINEAR-EXTENSION-TARGET

Stage: [CAUSAL_QFT](../stages/CAUSAL_QFT.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Finite statement, checked in Lean 4 in the following narrowed form. For a FiniteStrictPoset P and elements A_x (x in P) of a monoid with A_x A_y = A_y A_x for all spacelike pairs x,y: the ordered product along a listing of P is unchanged by one adjacent swap of spacelike elements, hence by any chain of adjacent spacelike swaps. Exact checks: the diamond C2 has exactly 2 linear extensions among the 24 permutations of its four points, \[0,1,2,3\] and \[0,2,1,3\], connected by one adjacent spacelike swap of 1 and 2; the N poset has exactly 5 linear extensions; with integer 2x2 Pauli matrices on C2 the two ordered products agree when the spacelike points 1 and 2 carry the commuting matrices Z and Z, and differ by the sign -1 (and are unequal) when they carry the anticommuting matrices X and Z. The distribution extension and the ultraviolet content of the Epstein-Glaser construction have no finite counterpart.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 6
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Not proved in Lean: that any two linear extensions of an arbitrary finite strict poset are connected by a chain of adjacent spacelike swaps, which is the step that turns swap invariance into independence from the choice of linear extension. Connectivity is exhibited for the two extensions of C2 only; for the N poset the five extensions are counted but their connectivity, and hence the equality of their ordered products, is not stated. The relation to Epstein-Glaser is an analogy.

## Source status

Verified against lean4/CausalOrder.lean on 2026-10-22. Lean: checked in Lean 4.35.0 via lake build FrontierLinearExtension (library FrontierTargets in lean4/lakefile.lean) in the form recorded in the statement; replay receipt in dag/research/frontier_targets_lean_replay.json; per-node review in dag/research/frontier_targets_lean_review.md.

## Review

- Frontier Lean review: [dag/research/frontier_targets_lean_review.md](../../../dag/research/frontier_targets_lean_review.md); verdict `NARROWED`; qualifies for E4: yes.
  - theorems that discharge the node, as listed by the review: `orderedProd_eq_of_adjSpacelikeSwap`, `orderedProd_eq_of_spacelikeSwapChain`, `linear_extensions_of_C2_and_N`, `c2_extensions_connected_by_swap`, `c2_pauli_commuting_and_anticommuting_products`
  - the review's reason for its verdict is in the row of this node in the review file

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CausalOrder.lean`

- file: [lean4/CausalOrder.lean](../../../lean4/CausalOrder.lean)
- sha256 (`bytes`): `f8f04b749262b26eeae39f3fc0d96b55e3fd02283f7df29a1c2042faf017edf0`
- cited in: node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_causal_qft.json](../../../dag/research/lean_replay_campaign_causal_qft.json) (module `CausalOrder`): recorded sha256 `f8f04b749262b26eeae39f3fc0d96b55e3fd02283f7df29a1c2042faf017edf0` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CausalOrder`
- counts toward the grade: yes

### Lean: `lean4/FrontierLinearExtension.lean`

- file: [lean4/FrontierLinearExtension.lean](../../../lean4/FrontierLinearExtension.lean)
- sha256 (`bytes`): `31d4eb6ee8e25cb2decc6c89f478accd26dbe97b8e7fbba357cdcbd4eb37c2bc`
- cited in: node.lean, node.source, receipt dag/research/frontier_targets_lean_replay.json (FrontierLinearExtension)
- replay: `verified`
  - receipt [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json) (module `FrontierLinearExtension`): recorded sha256 `31d4eb6ee8e25cb2decc6c89f478accd26dbe97b8e7fbba357cdcbd4eb37c2bc` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FrontierLinearExtension`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FrontierLinearExtension.c2_extensions_connected_by_swap` | yes | yes | yes | none | `#print axioms FrontierLinearExtension.c2_extensions_connected_by_swap` |
| `FrontierLinearExtension.c2_pauli_commuting_and_anticommuting_products` | yes | yes | yes | propext | `#print axioms FrontierLinearExtension.c2_pauli_commuting_and_anticommuting_products` |
| `FrontierLinearExtension.linear_extensions_of_C2_and_N` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierLinearExtension.linear_extensions_of_C2_and_N` |
| `FrontierLinearExtension.orderedProd_append` | yes | yes | yes | propext | `#print axioms FrontierLinearExtension.orderedProd_append` |
| `FrontierLinearExtension.orderedProd_eq_of_adjSpacelikeSwap` | yes | yes | yes | propext | `#print axioms FrontierLinearExtension.orderedProd_eq_of_adjSpacelikeSwap` |
| `FrontierLinearExtension.orderedProd_eq_of_spacelikeSwapChain` | yes | yes | yes | propext | `#print axioms FrontierLinearExtension.orderedProd_eq_of_spacelikeSwapChain` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/31_causal_qft/tfq_2110_cqft_ordered_product_linear_extension_target.md`

- file: [dag/derivations/31_causal_qft/tfq_2110_cqft_ordered_product_linear_extension_target.md](../../../dag/derivations/31_causal_qft/tfq_2110_cqft_ordered_product_linear_extension_target.md)
- sha256 (`lf-normalised`): `fa744417f2049199a2a92a5950cbe60df2410ef87bdff23552f54b16165c4c89`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2110
- counts toward the grade: no

### Documents and data: `dag/research/frontier_targets_lean_replay.json`

- file: [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json)
- sha256 (`lf-normalised`): `1c66aabd3bb726fafcd0238c259644d6f79dd304178d171a75ea36d6522bd2cc`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FRO-R-CQFT-ORDERED-PRODUCT-LINEAR-EXTENSION-TARGET` `DERIVED_LEAN`: [CQFT-CAUSAL-FACTORIZATION-IMPORT](CQFT-CAUSAL-FACTORIZATION-IMPORT.md) (IMPORTED_ASSUMPTION), [CQFT-FINITE-STRICT-POSET-SPACELIKE](CQFT-FINITE-STRICT-POSET-SPACELIKE.md) (PROVED_LEAN)

Outgoing (0):

