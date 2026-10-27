# CQFT-RS-FINITE-CYCLICITY-TARGET

Stage: [CAUSAL_QFT](../stages/CAUSAL_QFT.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Finite statement, checked in Lean 4 in the following narrowed form. Let Omega be a dA x dB matrix over a semiring R (the amplitude matrix of a vector in H_A tensor H_{A^c}; for qubits dA = 2^|A| and dB = 2^|A^c|, but the qubit tensor-factor bookkeeping is not formalised). Omega is cyclic for End(H_A) when every dA x dB matrix is X Omega for some X. (a) If Omega has a left inverse L with L Omega = I_dB (full column rank dB, which over a field is full rank of the reduced state on A^c) then Omega is cyclic and Omega is separating for End(H_{A^c}) (Omega Y = 0 implies Y = 0). (b) Conversely, cyclic implies a left inverse whenever dB \<= dA (an injection Fin dB -\> Fin dA is supplied). (c) A nonzero vector in the right kernel of Omega makes Omega not separating. (d) Exact 3-qubit instances over Z for the product vector |000\>, GHZ = |000\>+|111\> and W = |100\>+|010\>+|001\>: explicit nonzero right-kernel vectors for every single-site unfolding (2 x 4), explicit integer left inverses of every pair-of-sites unfolding (4 x 2) for GHZ and W, and a zero column in every pair-of-sites unfolding of |000\>.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
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

Not proved in Lean: separating implies full column rank (so the three-way equivalence is not complete); the identification of full column rank with full rank of the reduced state; the qubit subset bookkeeping; the conclusion "not cyclic" for the single-site cases (cyclic implies left inverse is proved only for dB \<= dA, and a single site has dA=2 \< dB=4; the kernel vectors give non-separating only) and for |000\> on pairs (a zero column is exhibited but "zero column implies no left inverse implies not cyclic" is not stated as a theorem); that |000\> is cyclic for the full algebra. A Lean proof of the equivalence for general n is open. The relation to the continuum theorem is an analogy: finite dimension has no translation group or spectrum condition.

## Source status

Algebraic instances verified with exact Python arithmetic on 2026-10-22. Lean: checked in Lean 4.35.0 via lake build FrontierRsCyclicity (library FrontierTargets in lean4/lakefile.lean) in the form recorded in the statement; replay receipt in dag/research/frontier_targets_lean_replay.json; per-node review in dag/research/frontier_targets_lean_review.md.

## Review

- Frontier Lean review: [dag/research/frontier_targets_lean_review.md](../../../dag/research/frontier_targets_lean_review.md); verdict `NARROWED`; qualifies for E4: yes.
  - theorems that discharge the node, as listed by the review: `cyclic_of_fullComplementaryRank`, `fullComplementaryRank_of_cyclic`, `separating_of_fullComplementaryRank`, `not_separating_of_right_kernel`, `single_site_not_cyclic_prod_ghz_w`, `pair_of_sites_cyclic_for_GHZ3_and_W3_not_prod3`
  - the review's reason for its verdict is in the row of this node in the review file

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/FrontierRsCyclicity.lean`

- file: [lean4/FrontierRsCyclicity.lean](../../../lean4/FrontierRsCyclicity.lean)
- sha256 (`bytes`): `b30a13817f44362f693009c1502a8654a1c090f66fbc5e7cd08df2f8d4be493e`
- cited in: node.lean, node.source, receipt dag/research/frontier_targets_lean_replay.json (FrontierRsCyclicity)
- replay: `verified`
  - receipt [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json) (module `FrontierRsCyclicity`): recorded sha256 `b30a13817f44362f693009c1502a8654a1c090f66fbc5e7cd08df2f8d4be493e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FrontierRsCyclicity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FrontierRsCyclicity.cyclic_of_fullComplementaryRank` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierRsCyclicity.cyclic_of_fullComplementaryRank` |
| `FrontierRsCyclicity.fullComplementaryRank_of_cyclic` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierRsCyclicity.fullComplementaryRank_of_cyclic` |
| `FrontierRsCyclicity.not_separating_of_right_kernel` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierRsCyclicity.not_separating_of_right_kernel` |
| `FrontierRsCyclicity.pair_of_sites_cyclic_for_GHZ3_and_W3_not_prod3` | yes | yes | yes | Quot.sound, propext | `#print axioms FrontierRsCyclicity.pair_of_sites_cyclic_for_GHZ3_and_W3_not_prod3` |
| `FrontierRsCyclicity.separating_of_fullComplementaryRank` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierRsCyclicity.separating_of_fullComplementaryRank` |
| `FrontierRsCyclicity.single_site_not_cyclic_prod_ghz_w` | yes | yes | yes | none | `#print axioms FrontierRsCyclicity.single_site_not_cyclic_prod_ghz_w` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/31_causal_qft/tfq_2107_cqft_rs_finite_cyclicity_target.md`

- file: [dag/derivations/31_causal_qft/tfq_2107_cqft_rs_finite_cyclicity_target.md](../../../dag/derivations/31_causal_qft/tfq_2107_cqft_rs_finite_cyclicity_target.md)
- sha256 (`lf-normalised`): `808575bad0f15e050c33fe4683ec851b7ef4da887a7275521d26756b69507848`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2107
- counts toward the grade: no

### Documents and data: `dag/research/frontier_targets_lean_replay.json`

- file: [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json)
- sha256 (`lf-normalised`): `f34cd1ed156fa81d00adb9c939a21d262964134472af8231083525a54cc7abce`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FRO-R-CQFT-RS-FINITE-CYCLICITY-TARGET` `DERIVED_LEAN`: [CQFT-REEH-SCHLIEDER-THEOREM-IMPORT](CQFT-REEH-SCHLIEDER-THEOREM-IMPORT.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

