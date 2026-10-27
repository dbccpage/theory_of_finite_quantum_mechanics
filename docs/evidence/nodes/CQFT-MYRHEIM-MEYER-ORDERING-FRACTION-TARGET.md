# CQFT-MYRHEIM-MEYER-ORDERING-FRACTION-TARGET

Stage: [CAUSAL_QFT](../stages/CAUSAL_QFT.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Finite statement, checked in Lean 4 in the following narrowed form. The ordering fraction of a finite causal set is the exact rational r = 2R/(n(n-1)), with R the number of strictly related pairs (CausalSet.ordering_fraction); Lean computes r(C1)=2/3 and r(C2)=5/6 from the relation tables of CausalOrder.lean. In Sorkin (2003, arXiv:gr-qc/0309009 Section 7 p. 16), the expected ordering fraction of a Poisson sprinkling into a d-dimensional Minkowski causal interval normalized by binom(N,2) is f(d) = (3/2) Gamma(d+1) Gamma(d/2 + 1) / Gamma(3d/2 + 1) = Gamma(d+1) Gamma(d/2) / (2 Gamma(3d/2)) (in Reid 2003, arXiv:gr-qc/0207103 Section III eq. (5) p. 5, normalizing by \<N\>^2 instead of binom(N,2) gives f(d)/2 = Gamma(d+1) Gamma(d/2) / (4 Gamma(3d/2))), with exact rational values f(1)=1, f(2)=1/2, f(3)=8/35 and f(4)=1/10; in Lean these four values are entered as a table (70 f(d) = 70, 35, 16, 7) and not derived from the Gamma formula. (i) If the n x n grid with the componentwise product order has R(n) = (n(n+1)/2)^2 - n^2 strictly related pairs (a count entered as a definition in Lean, not derived from a poset), then 4 R(n) = n^2 (n-1)(n+3), the ordering fraction is r = (n+3)/(2(n+1)) for all n \>= 2 with r(n) - 1/2 = 1/(n+1), the values for n=2..6 are 5/6, 3/4, 7/10, 2/3, 9/14, and r(2) = 5/6 equals the exactly computed r(C2) of the diamond. This is an observation about a lattice, not an instance of the sprinkling theorem. (ii) An exact nearest-dimension selector over d in {1,2,3,4} with tie reporting is defined and checked on the six inputs 5/6, 3/4, 7/10, 1/2, 8/35, 1/10, giving \[1\], \[1,2\] (an exact tie), \[2\], \[2\], \[3\], \[4\]. (iii) The Hasse covering relation of any FiniteStrictPoset is contained in every subrelation E of the order such that every related pair is in E or has an intermediate element (one half of "unique transitive reduction"); C1 has 2 links and C2 has 4; the Mobius tables c1_mu and c2_mu of CausalOrder.lean satisfy the Mobius recursion and c2_mu(d0,d3)=1.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- distinct cited Lean declarations covered by a current replay receipt: 7
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Not proved in Lean: that the n x n grid poset (a FiniteStrictPoset on n^2 points) has R(n) strictly related pairs, so (i) is arithmetic on a posited count cross-checked against the diamond only at n=2; the derivation of f(d) from the Gamma-function formula; correctness of the nearest-dimension selector beyond the six listed inputs; that the Hasse relation itself generates the order and is the minimal such relation. Everything is rational arithmetic on named finite posets. The dimension estimator is a heuristic for sprinklings; the finite estimate on a small poset carries no manifold statement.

## Source status

Source formulas audited against arXiv:gr-qc/0309009 Section 7 p. 16 and arXiv:gr-qc/0207103 Section III eqs. (4)-(5) pp. 4-5, and exact rational values f(1)=1, f(2)=1/2, f(3)=8/35, f(4)=1/10 and r(grid_n)=(n+3)/(2(n+1)) recomputed with Python fractions.Fraction on 2026-10-22. Lean: checked in Lean 4.35.0 via lake build FrontierMyrheimMeyer (library FrontierTargets in lean4/lakefile.lean) in the form recorded in the statement; replay receipt in dag/research/frontier_targets_lean_replay.json; per-node review in dag/research/frontier_targets_lean_review.md.

## Review

- Frontier Lean review: [dag/research/frontier_targets_lean_review.md](../../../dag/research/frontier_targets_lean_review.md); verdict `NARROWED`; qualifies for E4: yes.
  - theorems that discharge the node, as listed by the review: `gridStrictPairs_factorization`, `grid_ordering_fraction_closed_form`, `grid_ordering_fraction_minus_half`, `grid_values_2_to_6_and_c2_agreement`, `myrheim_meyer_nearest_dimension_checks`, `covers_subset_of_generating_subrelation`, `hasse_links_and_mobius_recursions_C1_C2`
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

### Lean: `lean4/FrontierMyrheimMeyer.lean`

- file: [lean4/FrontierMyrheimMeyer.lean](../../../lean4/FrontierMyrheimMeyer.lean)
- sha256 (`bytes`): `85bc63a2e22cd344072233eb921722db8eb1b10167f23daa55f1cae15f6fece7`
- cited in: node.lean, node.source, receipt dag/research/frontier_targets_lean_replay.json (FrontierMyrheimMeyer)
- replay: `verified`
  - receipt [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json) (module `FrontierMyrheimMeyer`): recorded sha256 `85bc63a2e22cd344072233eb921722db8eb1b10167f23daa55f1cae15f6fece7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FrontierMyrheimMeyer`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FrontierMyrheimMeyer.covers_subset_of_generating_subrelation` | yes | yes | yes | Quot.sound, propext | `#print axioms FrontierMyrheimMeyer.covers_subset_of_generating_subrelation` |
| `FrontierMyrheimMeyer.gridStrictPairs_factorization` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierMyrheimMeyer.gridStrictPairs_factorization` |
| `FrontierMyrheimMeyer.grid_ordering_fraction_closed_form` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierMyrheimMeyer.grid_ordering_fraction_closed_form` |
| `FrontierMyrheimMeyer.grid_ordering_fraction_minus_half` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierMyrheimMeyer.grid_ordering_fraction_minus_half` |
| `FrontierMyrheimMeyer.grid_values_2_to_6_and_c2_agreement` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierMyrheimMeyer.grid_values_2_to_6_and_c2_agreement` |
| `FrontierMyrheimMeyer.hasse_links_and_mobius_recursions_C1_C2` | yes | yes | yes | propext | `#print axioms FrontierMyrheimMeyer.hasse_links_and_mobius_recursions_C1_C2` |
| `FrontierMyrheimMeyer.myrheim_meyer_nearest_dimension_checks` | yes | yes | yes | none | `#print axioms FrontierMyrheimMeyer.myrheim_meyer_nearest_dimension_checks` |

- counts toward the grade: yes

### Python: `code/python/src/general_relativity/causal_set.py`

- file: [code/python/src/general_relativity/causal_set.py](../../../code/python/src/general_relativity/causal_set.py)
- sha256 (`bytes`): `fe0391e534586e7ef4b5856b1c9f9fa190a19f55fdd368e36d85950ef1af92fb`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/31_causal_qft/tfq_2113_cqft_myrheim_meyer_ordering_fraction_target.md`

- file: [dag/derivations/31_causal_qft/tfq_2113_cqft_myrheim_meyer_ordering_fraction_target.md](../../../dag/derivations/31_causal_qft/tfq_2113_cqft_myrheim_meyer_ordering_fraction_target.md)
- sha256 (`lf-normalised`): `e6e460c1befb7a6cf5e3211883c1a3648363ea24faeac87f059c8b8f2bed802e`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2113
- counts toward the grade: no

### Documents and data: `dag/research/frontier_targets_lean_replay.json`

- file: [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json)
- sha256 (`lf-normalised`): `f34cd1ed156fa81d00adb9c939a21d262964134472af8231083525a54cc7abce`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:gr-qc/0207103`
- `external:arXiv:gr-qc/0309009`

## Routes

Incoming (1):

- `FRO-R-CQFT-MYRHEIM-MEYER-ORDERING-FRACTION-TARGET` `DERIVED_LEAN`: [CQFT-FINITE-CAUSET-IDENTIFICATION](CQFT-FINITE-CAUSET-IDENTIFICATION.md) (DEFINITION)

Outgoing (0):

