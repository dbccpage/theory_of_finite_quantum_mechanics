# LQG-TV-LEVEL2-PENTAGON-TARGET

Stage: [LOOP_QUANTUM_GRAVITY](../stages/LOOP_QUANTUM_GRAVITY.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Finite statement, checked in Lean 4 for a transcribed table. At q = exp(i pi/4) with spin labels 0, 1/2, 1 (twice-spin 0, 1, 2), the normalized recoupling symbol isingF(a,b,c,d,e,f) is entered in Lean as an explicit case table over Q(sqrt 2) (values 0, +-1, +-sqrt(2)/2, transcribed from ising_f in code/rust/src/general_relativity/spin_foam.rs). On that table Lean checks in exact arithmetic over Q(sqrt 2): the quantum dimensions (1, sqrt 2, 1) with d_1^2 - d_0 = d_2 and d_1 d_2 - d_1 = 0 (truncation); exactly 36 nonzero entries among the 729 label 6-tuples; the orthogonality relation sum over f of isingF(a,b,c,d,e,f) isingF(a,b,c,d,e',f) = delta(e,e') for all admissible labels; and the pentagon identity sum over r of isingF(a,b,c,q,p,r) isingF(a,r,d,e,q,s) isingF(b,c,d,s,r,t) = isingF(p,c,d,e,q,t) isingF(a,b,t,e,p,s) across all 3^9 = 19,683 label assignments in {0,1,2}^9 (both sides zero unless the six boundary triads are admissible). The repository's fence (TFQ-0105) refuses an admission of triangulation invariance; this target discharges only the identity on those labels, not invariance of a state sum on a triangulated manifold.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Not proved in Lean: that the transcribed table equals the quantum 6j symbol at q = exp(i pi/4), neither derived from the q-Racah sum nor linked to the Rust function (the module imports H023 and H024 but uses nothing from them); the Z\[zeta_12\] data of H023 and H024; the dimension-weighted Turaev-Viro form of the identity (the checks are on the unitary-normalized F-symbols). The step from the local identity to invariance on a triangulation is not part of the target.

## Source status

Quantum Biedenharn-Elliott pentagon identity at level 2 (q = exp(i pi/4), twice-spins {0,1,2}) verified across all 3^9 = 19,683 label 9-tuples over Q(sqrt 2) using Python fractions.Fraction on 2026-10-22. Lean: checked in Lean 4.35.0 via lake build FrontierTvLevel2Pentagon (library FrontierTargets in lean4/lakefile.lean) in the form recorded in the statement; replay receipt in dag/research/frontier_targets_lean_replay.json; per-node review in dag/research/frontier_targets_lean_review.md.

## Review

- Frontier Lean review: [dag/research/frontier_targets_lean_review.md](../../../dag/research/frontier_targets_lean_review.md); verdict `NARROWED`; qualifies for E4: yes.
  - theorems that discharge the node, as listed by the review: `level2_quantum_dimensions_and_truncation`, `isingF_nonzero_count_36`, `level2_orthogonality_all_admissible`, `level2_quantum_pentagon_identity_all_19683`
  - the review's reason for its verdict is in the row of this node in the review file

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DiscreteSpinfoamAmplitudes.lean`

- file: [lean4/DiscreteSpinfoamAmplitudes.lean](../../../lean4/DiscreteSpinfoamAmplitudes.lean)
- sha256 (`bytes`): `b91f33b05cf90bd65fc8e51d6929ad5e1a5da57a6a6c908ad83bdf81e45db866`
- cited in: node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_loop_quantum_gravity.json](../../../dag/research/lean_replay_campaign_loop_quantum_gravity.json) (module `DiscreteSpinfoamAmplitudes`): recorded sha256 `b91f33b05cf90bd65fc8e51d6929ad5e1a5da57a6a6c908ad83bdf81e45db866` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build DiscreteSpinfoamAmplitudes`
- counts toward the grade: yes

### Lean: `lean4/FourSimplexSpinfoamS4.lean`

- file: [lean4/FourSimplexSpinfoamS4.lean](../../../lean4/FourSimplexSpinfoamS4.lean)
- sha256 (`bytes`): `e06939b3eb2914c80c0d62ccd771b0121231d65a3323481cc9edc59554722695`
- cited in: node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_implementation_sibling.json](../../../dag/research/lean_replay_campaign_implementation_sibling.json) (module `FourSimplexSpinfoamS4`): recorded sha256 `e06939b3eb2914c80c0d62ccd771b0121231d65a3323481cc9edc59554722695` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build FourSimplexSpinfoamS4`
- counts toward the grade: yes

### Lean: `lean4/FrontierTvLevel2Pentagon.lean`

- file: [lean4/FrontierTvLevel2Pentagon.lean](../../../lean4/FrontierTvLevel2Pentagon.lean)
- sha256 (`bytes`): `b1295e80e928d638db8fa5ddb3fedf981381983866c7addd76a96e20e9ebd841`
- cited in: node.lean, node.source, receipt dag/research/frontier_targets_lean_replay.json (FrontierTvLevel2Pentagon)
- replay: `verified`
  - receipt [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json) (module `FrontierTvLevel2Pentagon`): recorded sha256 `b1295e80e928d638db8fa5ddb3fedf981381983866c7addd76a96e20e9ebd841` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FrontierTvLevel2Pentagon`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FrontierTvLevel2Pentagon.isingF_nonzero_count_36` | yes | yes | yes | none | `#print axioms FrontierTvLevel2Pentagon.isingF_nonzero_count_36` |
| `FrontierTvLevel2Pentagon.level2_orthogonality_all_admissible` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierTvLevel2Pentagon.level2_orthogonality_all_admissible` |
| `FrontierTvLevel2Pentagon.level2_quantum_dimensions_and_truncation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierTvLevel2Pentagon.level2_quantum_dimensions_and_truncation` |
| `FrontierTvLevel2Pentagon.level2_quantum_pentagon_identity_all_19683` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierTvLevel2Pentagon.level2_quantum_pentagon_identity_all_19683` |

- counts toward the grade: yes

### Rust: `code/rust/src/general_relativity/spin_foam.rs`

- file: [code/rust/src/general_relativity/spin_foam.rs](../../../code/rust/src/general_relativity/spin_foam.rs)
- sha256 (`bytes`): `8ab22473e5ebc36ab2cb23247e2d6835664bab9ac0e9f0f26b6ab9b4fd63892e`
- cited in: node.source
- note: no test is cited for this symbol; its crate is tfqm_general_relativity
- counts toward the grade: yes

### Rust: `code/rust/src/qm/finite_spinfoam.rs`

- file: [code/rust/src/qm/finite_spinfoam.rs](../../../code/rust/src/qm/finite_spinfoam.rs)
- sha256 (`bytes`): `a541eaef1a2c1fcd54317f865a923f8f70a7202e151d6565c5d2f5b4c6e15d58`
- cited in: node.source
- note: no test is cited for this symbol; its crate is theory_of_finite_qm
- counts toward the grade: yes

### Documents and data: `dag/derivations/33_loop_quantum_gravity/tfq_2311_lqg_tv_level2_pentagon_target.md`

- file: [dag/derivations/33_loop_quantum_gravity/tfq_2311_lqg_tv_level2_pentagon_target.md](../../../dag/derivations/33_loop_quantum_gravity/tfq_2311_lqg_tv_level2_pentagon_target.md)
- sha256 (`lf-normalised`): `09ef75c49a88dcf563d8af53b6c672ad10e22d150d651ebcf2f66d8799f3395e`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2311
- counts toward the grade: no

### Documents and data: `dag/research/frontier_targets_lean_replay.json`

- file: [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json)
- sha256 (`lf-normalised`): `f34cd1ed156fa81d00adb9c939a21d262964134472af8231083525a54cc7abce`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:doi:10.1016/0040-9383(92)90015-A`

## Routes

Incoming (1):

- `FRO-R-LQG-TV-LEVEL2-PENTAGON-TARGET` `DERIVED_LEAN`: [LQG-TURAEV-VIRO-1992-SOURCE](LQG-TURAEV-VIRO-1992-SOURCE.md) (SOURCE_RECORD), [TFQ-0198](TFQ-0198.md) (COMPUTATIONALLY_CHECKED), [TFQ-0104](TFQ-0104.md) (SOURCE_RECORD)

Outgoing (1):

- `FRO-R-LQG-CONTINUUM-LIMIT-GAP` `GAP_NO_DERIVATION`: [LQG-CONTINUUM-LIMIT-GAP](LQG-CONTINUUM-LIMIT-GAP.md) (OPEN)
