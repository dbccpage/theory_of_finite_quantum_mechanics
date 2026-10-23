# LQG-6J-EXACT-AND-PENTAGON-TARGET

Stage: [LOOP_QUANTUM_GRAVITY](../stages/LOOP_QUANTUM_GRAVITY.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Finite statement, checked in Lean 4 in the following narrowed form. The Wigner 6j symbol with twice-spins at most 6 is S sqrt(P), where S is Racah's single-sum factor, computed with exact integer factorials, and P is the product of four rational triangle factors; Lean defines the rational square W^2 = S^2 P (sixJSquaredRat) in this way. Checks: (i) the signed Racah factor S is invariant under the four generators of the 24 tetrahedral symmetries (the column swaps 12 and 23 and the double row flips on columns 12 and 23) for all 3,418 admissible 6-tuples with twice-spins at most 6 (the invariance of P under the symmetries is evident, since they permute its four triangle factors, but is not part of the Lean check); (ii) the orthogonality relation sum over x of (x+1)(y+1) {a b x; c d y}{a b x; c d y'} = delta(y,y') in twice-spin labels, for the 1,928 admissible tuples (a,b,c,d,y,y') whose labels and whose intermediate twice-spin x all lie at or below 6; (iii) the Biedenharn-Elliott (pentagon) identity for all 814 admissible 9-tuples with twice-spins at most 3, and for four explicit instances with twice-spins up to 6 (all labels 2; labels 3 with p=q=r=2; (a,b,c,d,e,f,p,q,r) = (4,2,3,3,2,4,3,3,2); and (6,0,6,0,6,0,6,6,6)). Exact arithmetic in the rationals with one square root per symbol.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Not proved in Lean: the Biedenharn-Elliott identity exhaustively for twice-spins 4 to 6 (four instances only); orthogonality for tuples whose intermediate range exceeds twice-spin 6; invariance of P, W^2 and the signed symbol under the symmetry generators, and invariance under the whole group (the closure of the tuple set under the generators is not stated). Exact enumeration with big integers. The classical 6j is not the q-deformed 6j at level 2 recorded in TFQ-0105; the q to 1 limit is not part of the target.

## Source status

Racah single-sum rational squares and values for 2j \<= 2 recomputed with Python fractions.Fraction on 2026-10-22. Lean: checked in Lean 4.35.0 via lake build FrontierClassical6j (library FrontierTargets in lean4/lakefile.lean) in the form recorded in the statement; replay receipt in dag/research/frontier_targets_lean_replay.json; per-node review in dag/research/frontier_targets_lean_review.md.

## Review

- Frontier Lean review: [dag/research/frontier_targets_lean_review.md](../../../dag/research/frontier_targets_lean_review.md); verdict `NARROWED`; qualifies for E4: yes.
  - theorems that discharge the node, as listed by the review: `tetrahedral_symmetry_all_3418_admissible_le6`, `classical_6j_orthogonality_all_1928_le6`, `classical_6j_biedenharn_elliott_pentagon`
  - the review's reason for its verdict is in the row of this node in the review file

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/FrontierClassical6j.lean`

- file: [lean4/FrontierClassical6j.lean](../../../lean4/FrontierClassical6j.lean)
- sha256 (`bytes`): `46a223afed518f0b5fb71747b23efaf0984a8bc1daa9e2f94862756baa46284a`
- cited in: node.lean, node.source, receipt dag/research/frontier_targets_lean_replay.json (FrontierClassical6j)
- replay: `verified`
  - receipt [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json) (module `FrontierClassical6j`): recorded sha256 `46a223afed518f0b5fb71747b23efaf0984a8bc1daa9e2f94862756baa46284a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FrontierClassical6j`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FrontierClassical6j.classical_6j_biedenharn_elliott_pentagon` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierClassical6j.classical_6j_biedenharn_elliott_pentagon` |
| `FrontierClassical6j.classical_6j_orthogonality_all_1928_le6` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierClassical6j.classical_6j_orthogonality_all_1928_le6` |
| `FrontierClassical6j.tetrahedral_symmetry_all_3418_admissible_le6` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierClassical6j.tetrahedral_symmetry_all_3418_admissible_le6` |
- counts toward the grade: yes

### Lean: `lean4/H023DiscreteSpinfoamAmplitudes.lean`

- file: [lean4/H023DiscreteSpinfoamAmplitudes.lean](../../../lean4/H023DiscreteSpinfoamAmplitudes.lean)
- sha256 (`bytes`): `926c526a9087b9648e1fc3107ae89d4d16f0525234d8901e916a29a516d70457`
- cited in: node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_loop_quantum_gravity.json](../../../dag/research/lean_replay_campaign_loop_quantum_gravity.json) (module `H023DiscreteSpinfoamAmplitudes`): recorded sha256 `926c526a9087b9648e1fc3107ae89d4d16f0525234d8901e916a29a516d70457` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build H023DiscreteSpinfoamAmplitudes`
- counts toward the grade: yes

### Rust: `code/rust/src/general_relativity/spin_foam.rs`

- file: [code/rust/src/general_relativity/spin_foam.rs](../../../code/rust/src/general_relativity/spin_foam.rs)
- sha256 (`bytes`): `8ab22473e5ebc36ab2cb23247e2d6835664bab9ac0e9f0f26b6ab9b4fd63892e`
- cited in: node.source
- note: no test is cited for this symbol; its crate is tfqm_general_relativity
- counts toward the grade: yes

### Documents and data: `dag/derivations/33_loop_quantum_gravity/tfq_2308_lqg_6j_exact_and_pentagon_target.md`

- file: [dag/derivations/33_loop_quantum_gravity/tfq_2308_lqg_6j_exact_and_pentagon_target.md](../../../dag/derivations/33_loop_quantum_gravity/tfq_2308_lqg_6j_exact_and_pentagon_target.md)
- sha256 (`lf-normalised`): `78840b6c1ca1892f3022f3721f07b93590c456759f2114d072e772bed6e854b5`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2308
- counts toward the grade: no

### Documents and data: `dag/research/frontier_targets_lean_replay.json`

- file: [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json)
- sha256 (`lf-normalised`): `1c66aabd3bb726fafcd0238c259644d6f79dd304178d171a75ea36d6522bd2cc`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FRO-R-LQG-6J-EXACT-AND-PENTAGON-TARGET` `DERIVED_LEAN`: [LQG-PONZANO-REGGE-1968-SOURCE](LQG-PONZANO-REGGE-1968-SOURCE.md) (SOURCE_RECORD), [TFQ-0198](TFQ-0198.md) (COMPUTATIONALLY_CHECKED)

Outgoing (1):

- `FRO-R-LQG-PR-ALLOWED-REGION-TARGET` `DERIVED_LEAN`: [LQG-PR-ALLOWED-REGION-TARGET](LQG-PR-ALLOWED-REGION-TARGET.md) (PROVED_LEAN)
