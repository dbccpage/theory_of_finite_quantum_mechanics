# L1-IMP-TRANSITION-PROBABILITY-LAW

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Transition-probability preservation of the ray dynamics: the evolution of rays of the lift preserves the Born probability of every rank-one effect in every state. Under this law the dynamics is a linear or conjugate-linear similarity (L1-IMP-LINEAR-ISOMETRIC-DYNAMICS); without it, any bijection of rays is admissible. Supplied, not derived from primitive difference.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 8
- cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- transition-probability (Born rank-one readout) preservation by the ray dynamics: assumption

## Bottleneck

No finite-theory primitive forces the ray dynamics to preserve the Born readout of rank-one effects; deriving it (for instance from report relabelling invariance and the Born rule on the lift) is item 1 of the run next steps.

## Source status

Supplied law of the ray dynamics in dag/results/L1-IMP-LINEAR-ISOMETRIC-DYNAMICS/runs/20261021T190000Z_finite_wigner: the dynamics sends nonzero vectors of the exact carrier Q(i)^n to nonzero vectors and preserves the transition probability tp x y = |\<x,y\>|^2/(|x|^2|y|^2) between nonzero vectors (Theorem.TpPreserving), equivalently the normalised Born readout hf (P x) y / vnorm y of rank-one effects (Similarity.tpPreserving_iff_born, Kernel.tp_eq_born). Nothing in the finite theory forces a dynamics to preserve this readout; it is the operational hypothesis of the Wigner theorem.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/FiniteWignerKernel.lean`

- file: [lean4/FiniteWignerKernel.lean](../../../lean4/FiniteWignerKernel.lean)
- sha256 (`bytes`): `29346e2ba6220f3d2587a609c93d77d6d06a87a48d8297cb3a80c1f3231660ab`
- cited in: node.lean, record TFQ-1047
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `FiniteWignerKernel`): recorded sha256 `29346e2ba6220f3d2587a609c93d77d6d06a87a48d8297cb3a80c1f3231660ab` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteWignerKernel`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WignerFable.Kernel.tp` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFable.Kernel.tp` |
| `WignerFable.Kernel.tp_eq_born` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFable.Kernel.tp_eq_born` |
- counts toward the grade: yes

### Lean: `lean4/FiniteWignerSimilarity.lean`

- file: [lean4/FiniteWignerSimilarity.lean](../../../lean4/FiniteWignerSimilarity.lean)
- sha256 (`bytes`): `d4244d574e5710133144d985426b646c1f7ed4d18ffc489d6f1605be5483cb37`
- cited in: node.lean, record TFQ-1047
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `FiniteWignerSimilarity`): recorded sha256 `d4244d574e5710133144d985426b646c1f7ed4d18ffc489d6f1605be5483cb37` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteWignerSimilarity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WignerFable.Similarity.tpPreserving_iff_born` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFable.Similarity.tpPreserving_iff_born` |
- counts toward the grade: yes

### Lean: `lean4/FiniteWignerTheorem.lean`

- file: [lean4/FiniteWignerTheorem.lean](../../../lean4/FiniteWignerTheorem.lean)
- sha256 (`bytes`): `b2474d25f679caeb99da3348c7bed0b5f0fe408d9b93667016fc8da9ebeb8292`
- cited in: node.lean, node.source, record TFQ-1047
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `FiniteWignerTheorem`): recorded sha256 `b2474d25f679caeb99da3348c7bed0b5f0fe408d9b93667016fc8da9ebeb8292` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteWignerTheorem`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WignerFable.Theorem.TpPreserving` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFable.Theorem.TpPreserving` |
| `WignerFable.Theorem.tpPreserving_of_similarity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFable.Theorem.tpPreserving_of_similarity` |
- counts toward the grade: yes

### Rust: `code/rust/src/qm/finite_wigner.rs`

- file: [code/rust/src/qm/finite_wigner.rs](../../../code/rust/src/qm/finite_wigner.rs)
- sha256 (`bytes`): `4bb3ada0b37f7eb54f994c358eb477c1fd32b5cc57ce801de2f926bc4c33995f`
- cited in: node.rust, record TFQ-1047

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `born_transition` (rust_symbol) | yes | yes | yes | - | - |
| `transition_probability` (rust_symbol) | yes | yes | yes | - | - |
| `verify_induced` (rust_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1047_l1_imp_transition_probability_law.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1047_l1_imp_transition_probability_law.md](../../../dag/derivations/08_l1_to_l2/tfq_1047_l1_imp_transition_probability_law.md)
- sha256 (`lf-normalised`): `9d8bf5432cf3807345efd0f3f8cf827cf8ecd08c9bf94e9d83432870fe14851b`
- generated view: listed, not counted
- cited in: record TFQ-1047
- counts toward the grade: no

### Documents and data: `dag/results/L1-IMP-LINEAR-ISOMETRIC-DYNAMICS/runs/20261021T190000Z_finite_wigner/README.md`

- file: [dag/results/L1-IMP-LINEAR-ISOMETRIC-DYNAMICS/runs/20261021T190000Z_finite_wigner/README.md](../../../dag/results/L1-IMP-LINEAR-ISOMETRIC-DYNAMICS/runs/20261021T190000Z_finite_wigner/README.md)
- sha256 (`lf-normalised`): `8b5050fbb9f1e046b3f6fbde489956734d5e6d4b5f1ef936ad56cdd6abf82a49`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/results/L1-IMP-LINEAR-ISOMETRIC-DYNAMICS/runs/20261021T190000Z_finite_wigner/review.md`

- file: [dag/results/L1-IMP-LINEAR-ISOMETRIC-DYNAMICS/runs/20261021T190000Z_finite_wigner/review.md](../../../dag/results/L1-IMP-LINEAR-ISOMETRIC-DYNAMICS/runs/20261021T190000Z_finite_wigner/review.md)
- sha256 (`lf-normalised`): `c47b6d96998dcd53375828e9925862b63fcd37b84f6f12f13ac5960bf4a47629`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (0):


Outgoing (2):

- `L1-R-DYNAMICS-FINITE-WIGNER` `CONDITIONAL_ON_IMPORT`: [L1-IMP-LINEAR-ISOMETRIC-DYNAMICS](L1-IMP-LINEAR-ISOMETRIC-DYNAMICS.md) (CONDITIONAL)
- `L1-R-DYNAMICS-GAP` `CONDITIONAL_ON_IMPORT`: [L1-IMP-LINEAR-ISOMETRIC-DYNAMICS](L1-IMP-LINEAR-ISOMETRIC-DYNAMICS.md) (CONDITIONAL)

No incoming route.
