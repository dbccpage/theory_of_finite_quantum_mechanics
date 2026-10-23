# L1-IMP-TRANSITION-PROBABILITY-LAW

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Imported dynamical law: the evolution of rays preserves the Born probability of every transported rank-one effect in every state; conditional on this law the dynamics is a linear or conjugate-linear similarity. Campaign hypothesis map on Q(i)^n: a supplied linear lift with finite orthogonality calibration and a nonzero anchor preserves transition probabilities; fixed-frame statistics for all basis, real pair and imaginary pair probes in every nonzero state, together with nonvanishing, also suffice and fix every ray. On Q(i)^2, reversible ray dynamics can preserve norms, basis and real pair statistics, report-swap covariance and orthogonality while changing a transition probability from 9/10 to 1/10. A reversible linear subspace-lattice automorphism changes another probability from 1/2 to 1/5. The dynamical law remains supplied, not derived from primitive difference.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 10
- cited Lean, Rust or Python symbols found in their in-repo files: 88
- cited Lean declarations covered by a current replay receipt: 85
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- transition-probability (Born rank-one readout) preservation by the ray dynamics: assumption
- For the conditional linear route: LinearLift, OrthogonalCalibration and NonzeroAnchor.
- For the fixed-frame route: Nonvanishing and TomographicStatistics; these force each ray to be fixed.

## Bottleneck

The sufficient packages add explicit structure: a Gaussian-rational linear lift plus finite zero-probability calibration, or nonvanishing plus all-state fixed-frame tomographic statistics. Neither package is a derivation from primitive difference or a strictly weaker replacement for the full law. Static Born readout, reversibility, report-swap covariance, norms, basis and real pair statistics and orthogonality are jointly insufficient in dimension two. Subspace order preservation without orthocomplement preservation is also insufficient. Arbitrary ray bijections in higher dimensions under orthogonality alone, affine positive-effect automorphisms and evolving measurement-frame covariance are not classified here.

## Source status

Supplied law of the ray dynamics in dag/results/L1-IMP-LINEAR-ISOMETRIC-DYNAMICS/runs/20261021T190000Z_finite_wigner: the dynamics sends nonzero vectors of the exact carrier Q(i)^n to nonzero vectors and preserves the transition probability tp x y = |\<x,y\>|^2/(|x|^2|y|^2) between nonzero vectors (Theorem.TpPreserving), equivalently the normalised Born readout hf (P x) y / vnorm y of rank-one effects (Similarity.tpPreserving_iff_born, Kernel.tp_eq_born). Nothing in the finite theory forces a dynamics to preserve this readout; it is the operational hypothesis of the Wigner theorem. Campaign outcome Narrowed: conditional sufficient packages and exact global two-sector ray countermodels, with no status promotion; see the campaign derivation note and Lean replay receipt.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignTransitionProbability.lean`

- file: [lean4/CampaignTransitionProbability.lean](../../../lean4/CampaignTransitionProbability.lean)
- sha256 (`bytes`): `c1049f591250df2dfcb3f87f2f7a8c4e2b3ba51949d08f86a3d53d23fcf82b42`
- cited in: node.lean, receipt dag/research/campaign_l1-imp-transition-probability-law_lean_replay.json (CampaignTransitionProbability), record TFQ-1047
- replay: `verified`
  - receipt [dag/research/campaign_l1-imp-transition-probability-law_lean_replay.json](../../../dag/research/campaign_l1-imp-transition-probability-law_lean_replay.json) (module `CampaignTransitionProbability`): recorded sha256 `c1049f591250df2dfcb3f87f2f7a8c4e2b3ba51949d08f86a3d53d23fcf82b42` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignTransitionProbability`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignTransitionProbability.Balanced` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.Balanced` |
| `CampaignTransitionProbability.BasisStatistics` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.BasisStatistics` |
| `CampaignTransitionProbability.BornRule` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.BornRule` |
| `CampaignTransitionProbability.LinearLift` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.LinearLift` |
| `CampaignTransitionProbability.Nonvanishing` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignTransitionProbability.Nonvanishing` |
| `CampaignTransitionProbability.NonzeroAnchor` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignTransitionProbability.NonzeroAnchor` |
| `CampaignTransitionProbability.NonzeroVec` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignTransitionProbability.NonzeroVec` |
| `CampaignTransitionProbability.NormPreserving` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.NormPreserving` |
| `CampaignTransitionProbability.OrthogonalCalibration` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.OrthogonalCalibration` |
| `CampaignTransitionProbability.Orthogonality` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.Orthogonality` |
| `CampaignTransitionProbability.ProbeStatistics` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.ProbeStatistics` |
| `CampaignTransitionProbability.Ray` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.Ray` |
| `CampaignTransitionProbability.RayCompatible` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.RayCompatible` |
| `CampaignTransitionProbability.RealProbeStatistics` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.RealProbeStatistics` |
| `CampaignTransitionProbability.ReportSwapCovariant` | yes | yes | yes | propext | `#print axioms CampaignTransitionProbability.ReportSwapCovariant` |
| `CampaignTransitionProbability.Reversible` | yes | yes | yes | none | `#print axioms CampaignTransitionProbability.Reversible` |
| `CampaignTransitionProbability.SameRay` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.SameRay` |
| `CampaignTransitionProbability.SubspaceLatticeLift` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.SubspaceLatticeLift` |
| `CampaignTransitionProbability.TomographicStatistics` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.TomographicStatistics` |
| `CampaignTransitionProbability.Vec` | yes | yes | yes | none | `#print axioms CampaignTransitionProbability.Vec` |
| `CampaignTransitionProbability.balanced_of_orthogonal` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.balanced_of_orthogonal` |
| `CampaignTransitionProbability.balanced_reportSwap` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.balanced_reportSwap` |
| `CampaignTransitionProbability.balanced_smul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.balanced_smul` |
| `CampaignTransitionProbability.balanced_star` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.balanced_star` |
| `CampaignTransitionProbability.born_rule` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.born_rule` |
| `CampaignTransitionProbability.calibration_norms` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.calibration_norms` |
| `CampaignTransitionProbability.calibration_similarity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.calibration_similarity` |
| `CampaignTransitionProbability.conditionalConjugation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.conditionalConjugation` |
| `CampaignTransitionProbability.conditionalConjugation_basis` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.conditionalConjugation_basis` |
| `CampaignTransitionProbability.conditionalConjugation_coordinate_norm` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.conditionalConjugation_coordinate_norm` |
| `CampaignTransitionProbability.conditionalConjugation_involutive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.conditionalConjugation_involutive` |
| `CampaignTransitionProbability.conditionalConjugation_nonvanishing` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.conditionalConjugation_nonvanishing` |
| `CampaignTransitionProbability.conditionalConjugation_norm` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.conditionalConjugation_norm` |
| `CampaignTransitionProbability.conditionalConjugation_not_linearLift` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.conditionalConjugation_not_linearLift` |
| `CampaignTransitionProbability.conditionalConjugation_not_tomographic` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.conditionalConjugation_not_tomographic` |
| `CampaignTransitionProbability.conditionalConjugation_not_tpPreserving` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.conditionalConjugation_not_tpPreserving` |
| `CampaignTransitionProbability.conditionalConjugation_orth_forward` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.conditionalConjugation_orth_forward` |
| `CampaignTransitionProbability.conditionalConjugation_orthogonality` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.conditionalConjugation_orthogonality` |
| `CampaignTransitionProbability.conditionalConjugation_rayCompatible` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.conditionalConjugation_rayCompatible` |
| `CampaignTransitionProbability.conditionalConjugation_realProbes` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.conditionalConjugation_realProbes` |
| `CampaignTransitionProbability.conditionalConjugation_reportSwap` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.conditionalConjugation_reportSwap` |
| `CampaignTransitionProbability.conditionalConjugation_reversible` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.conditionalConjugation_reversible` |
| `CampaignTransitionProbability.countermodelRayEquiv` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.countermodelRayEquiv` |
| `CampaignTransitionProbability.countermodel_probabilities` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.countermodel_probabilities` |
| `CampaignTransitionProbability.identity_calibration` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.identity_calibration` |
| `CampaignTransitionProbability.identity_linearLift` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.identity_linearLift` |
| `CampaignTransitionProbability.identity_nonvanishing` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignTransitionProbability.identity_nonvanishing` |
| `CampaignTransitionProbability.imaginary_probe_probabilities` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.imaginary_probe_probabilities` |
| `CampaignTransitionProbability.insufficient_lattice_package` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.insufficient_lattice_package` |
| `CampaignTransitionProbability.insufficient_operational_package` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.insufficient_operational_package` |
| `CampaignTransitionProbability.involutiveRayEquiv` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.involutiveRayEquiv` |
| `CampaignTransitionProbability.ip_sub_left` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.ip_sub_left` |
| `CampaignTransitionProbability.ip_sub_right` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.ip_sub_right` |
| `CampaignTransitionProbability.linearRayEquiv` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.linearRayEquiv` |
| `CampaignTransitionProbability.linear_calibration_tpPreserving` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.linear_calibration_tpPreserving` |
| `CampaignTransitionProbability.linear_calibration_wigner` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.linear_calibration_wigner` |
| `CampaignTransitionProbability.normSq_neg_local` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.normSq_neg_local` |
| `CampaignTransitionProbability.oneSector_sameRay` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.oneSector_sameRay` |
| `CampaignTransitionProbability.oneSector_tpPreserving` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.oneSector_tpPreserving` |
| `CampaignTransitionProbability.orthogonality_calibration` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.orthogonality_calibration` |
| `CampaignTransitionProbability.rayMap` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.rayMap` |
| `CampaignTransitionProbability.raySetoid` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.raySetoid` |
| `CampaignTransitionProbability.reportSwap` | yes | yes | yes | propext | `#print axioms CampaignTransitionProbability.reportSwap` |
| `CampaignTransitionProbability.sameRay_refl` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.sameRay_refl` |
| `CampaignTransitionProbability.sameRay_symm` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.sameRay_symm` |
| `CampaignTransitionProbability.sameRay_trans` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.sameRay_trans` |
| `CampaignTransitionProbability.stretch` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.stretch` |
| `CampaignTransitionProbability.stretchLattice` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.stretchLattice` |
| `CampaignTransitionProbability.stretchRayEquiv` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.stretchRayEquiv` |
| `CampaignTransitionProbability.stretch_lattice` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.stretch_lattice` |
| `CampaignTransitionProbability.stretch_linearLift` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.stretch_linearLift` |
| `CampaignTransitionProbability.stretch_not_tpPreserving` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.stretch_not_tpPreserving` |
| `CampaignTransitionProbability.stretch_probabilities` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.stretch_probabilities` |
| `CampaignTransitionProbability.tomography_identity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.tomography_identity` |
| `CampaignTransitionProbability.tomography_sameRay` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.tomography_sameRay` |
| `CampaignTransitionProbability.tomography_tpPreserving` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.tomography_tpPreserving` |
| `CampaignTransitionProbability.witnessA` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignTransitionProbability.witnessA` |
| `CampaignTransitionProbability.witnessA_ne` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.witnessA_ne` |
| `CampaignTransitionProbability.witnessB` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.witnessB` |
| `CampaignTransitionProbability.witnessB_ne` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignTransitionProbability.witnessB_ne` |
- counts toward the grade: yes

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

### Python: `checks/independent/l1-imp-transition-probability-law.py`

- file: [checks/independent/l1-imp-transition-probability-law.py](../../../checks/independent/l1-imp-transition-probability-law.py)
- sha256 (`bytes`): `9641eb17d294a9160f69dc02f2102c18780b6ade7867246aa98da1072f4029d2`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1047_l1_imp_transition_probability_law.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1047_l1_imp_transition_probability_law.md](../../../dag/derivations/08_l1_to_l2/tfq_1047_l1_imp_transition_probability_law.md)
- sha256 (`lf-normalised`): `eb6121daf844f6943e16f480096ea1e11aacf6ab71b54d86bc1c9411b51dd9ff`
- generated view: listed, not counted
- cited in: record TFQ-1047
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/l1-imp-transition-probability-law.md`

- file: [dag/derivations/independent/l1-imp-transition-probability-law.md](../../../dag/derivations/independent/l1-imp-transition-probability-law.md)
- sha256 (`lf-normalised`): `cde71b3f1b42b7ab2c91468e3b56061323de1616c1378823bf08f53e76bb8f33`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_l1-imp-transition-probability-law_lean_replay.json`

- file: [dag/research/campaign_l1-imp-transition-probability-law_lean_replay.json](../../../dag/research/campaign_l1-imp-transition-probability-law_lean_replay.json)
- sha256 (`lf-normalised`): `973cb66334355e84819efd6735cec8b7d1ff36fa5c1466b4e319be76cae1a179`
- cited in: node.source
- counts toward the grade: yes

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
