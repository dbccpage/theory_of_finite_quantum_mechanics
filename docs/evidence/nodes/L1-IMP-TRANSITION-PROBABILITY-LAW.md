# L1-IMP-TRANSITION-PROBABILITY-LAW

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Imported dynamical law: the evolution of rays preserves the Born probability of every transported rank-one effect in every state; conditional on this law the dynamics is a linear or conjugate-linear similarity. Campaign hypothesis map on Q(i)^n: a supplied linear lift with finite orthogonality calibration and a nonzero anchor preserves transition probabilities; fixed-frame statistics for all basis, real pair and imaginary pair probes in every nonzero state, together with nonvanishing, also suffice and fix every ray. On Q(i)^2, reversible ray dynamics can preserve norms, basis and real pair statistics, report-swap covariance and orthogonality while changing a transition probability from 9/10 to 1/10. A reversible linear subspace-lattice automorphism changes another probability from 1/2 to 1/5. The dynamical law remains supplied, not derived from primitive difference.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 10
- cited Lean, Rust or Python symbols found in their in-repo files: 88
- distinct cited Lean declarations covered by a current replay receipt: 85
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

### Lean: `lean4/FiniteWignerKernel.lean`

- file: [lean4/FiniteWignerKernel.lean](../../../lean4/FiniteWignerKernel.lean)
- sha256 (`bytes`): `4a8cb01b2b211c84c8f0630d0a7716e75740731887e2ca9f8c400f3deb361814`
- cited in: node.lean, record TFQ-1047
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `FiniteWignerKernel`): recorded sha256 `4a8cb01b2b211c84c8f0630d0a7716e75740731887e2ca9f8c400f3deb361814` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteWignerKernel`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WignerFinite.Kernel.tp` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.Kernel.tp` |
| `WignerFinite.Kernel.tp_eq_born` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.Kernel.tp_eq_born` |

- counts toward the grade: yes

### Lean: `lean4/FiniteWignerSimilarity.lean`

- file: [lean4/FiniteWignerSimilarity.lean](../../../lean4/FiniteWignerSimilarity.lean)
- sha256 (`bytes`): `1358d7bfd2451add737744d0fc685cd5454dbb78f821b2261d14e8161be65a1e`
- cited in: node.lean, record TFQ-1047
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `FiniteWignerSimilarity`): recorded sha256 `1358d7bfd2451add737744d0fc685cd5454dbb78f821b2261d14e8161be65a1e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteWignerSimilarity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WignerFinite.Similarity.tpPreserving_iff_born` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.Similarity.tpPreserving_iff_born` |

- counts toward the grade: yes

### Lean: `lean4/FiniteWignerTheorem.lean`

- file: [lean4/FiniteWignerTheorem.lean](../../../lean4/FiniteWignerTheorem.lean)
- sha256 (`bytes`): `77ae8e0eb904a0c1fa22dbbfdfd12e3504ab7424424c10beecd6a8173da63527`
- cited in: node.lean, node.source, record TFQ-1047
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `FiniteWignerTheorem`): recorded sha256 `77ae8e0eb904a0c1fa22dbbfdfd12e3504ab7424424c10beecd6a8173da63527` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteWignerTheorem`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WignerFinite.Theorem.TpPreserving` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.Theorem.TpPreserving` |
| `WignerFinite.Theorem.tpPreserving_of_similarity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.Theorem.tpPreserving_of_similarity` |

- counts toward the grade: yes

### Lean: `lean4/TransitionProbability.lean`

- file: [lean4/TransitionProbability.lean](../../../lean4/TransitionProbability.lean)
- sha256 (`bytes`): `b2bd31978802c1e023f0b58b87e3ef40955a535f6cc3785e2714896ec53fea36`
- cited in: node.lean, receipt dag/research/campaign_l1-imp-transition-probability-law_lean_replay.json (TransitionProbability), record TFQ-1047
- replay: `verified`
  - receipt [dag/research/campaign_l1-imp-transition-probability-law_lean_replay.json](../../../dag/research/campaign_l1-imp-transition-probability-law_lean_replay.json) (module `TransitionProbability`): recorded sha256 `b2bd31978802c1e023f0b58b87e3ef40955a535f6cc3785e2714896ec53fea36` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build TransitionProbability`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `TransitionProbability.Balanced` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.Balanced` |
| `TransitionProbability.BasisStatistics` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.BasisStatistics` |
| `TransitionProbability.BornRule` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.BornRule` |
| `TransitionProbability.LinearLift` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.LinearLift` |
| `TransitionProbability.Nonvanishing` | yes | yes | yes | Quot.sound, propext | `#print axioms TransitionProbability.Nonvanishing` |
| `TransitionProbability.NonzeroAnchor` | yes | yes | yes | Quot.sound, propext | `#print axioms TransitionProbability.NonzeroAnchor` |
| `TransitionProbability.NonzeroVec` | yes | yes | yes | Quot.sound, propext | `#print axioms TransitionProbability.NonzeroVec` |
| `TransitionProbability.NormPreserving` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.NormPreserving` |
| `TransitionProbability.OrthogonalCalibration` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.OrthogonalCalibration` |
| `TransitionProbability.Orthogonality` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.Orthogonality` |
| `TransitionProbability.ProbeStatistics` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.ProbeStatistics` |
| `TransitionProbability.Ray` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.Ray` |
| `TransitionProbability.RayCompatible` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.RayCompatible` |
| `TransitionProbability.RealProbeStatistics` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.RealProbeStatistics` |
| `TransitionProbability.ReportSwapCovariant` | yes | yes | yes | propext | `#print axioms TransitionProbability.ReportSwapCovariant` |
| `TransitionProbability.Reversible` | yes | yes | yes | none | `#print axioms TransitionProbability.Reversible` |
| `TransitionProbability.SameRay` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.SameRay` |
| `TransitionProbability.SubspaceLatticeLift` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.SubspaceLatticeLift` |
| `TransitionProbability.TomographicStatistics` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.TomographicStatistics` |
| `TransitionProbability.Vec` | yes | yes | yes | none | `#print axioms TransitionProbability.Vec` |
| `TransitionProbability.balanced_of_orthogonal` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.balanced_of_orthogonal` |
| `TransitionProbability.balanced_reportSwap` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.balanced_reportSwap` |
| `TransitionProbability.balanced_smul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.balanced_smul` |
| `TransitionProbability.balanced_star` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.balanced_star` |
| `TransitionProbability.born_rule` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.born_rule` |
| `TransitionProbability.calibration_norms` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.calibration_norms` |
| `TransitionProbability.calibration_similarity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.calibration_similarity` |
| `TransitionProbability.conditionalConjugation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.conditionalConjugation` |
| `TransitionProbability.conditionalConjugation_basis` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.conditionalConjugation_basis` |
| `TransitionProbability.conditionalConjugation_coordinate_norm` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.conditionalConjugation_coordinate_norm` |
| `TransitionProbability.conditionalConjugation_involutive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.conditionalConjugation_involutive` |
| `TransitionProbability.conditionalConjugation_nonvanishing` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.conditionalConjugation_nonvanishing` |
| `TransitionProbability.conditionalConjugation_norm` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.conditionalConjugation_norm` |
| `TransitionProbability.conditionalConjugation_not_linearLift` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.conditionalConjugation_not_linearLift` |
| `TransitionProbability.conditionalConjugation_not_tomographic` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.conditionalConjugation_not_tomographic` |
| `TransitionProbability.conditionalConjugation_not_tpPreserving` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.conditionalConjugation_not_tpPreserving` |
| `TransitionProbability.conditionalConjugation_orth_forward` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.conditionalConjugation_orth_forward` |
| `TransitionProbability.conditionalConjugation_orthogonality` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.conditionalConjugation_orthogonality` |
| `TransitionProbability.conditionalConjugation_rayCompatible` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.conditionalConjugation_rayCompatible` |
| `TransitionProbability.conditionalConjugation_realProbes` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.conditionalConjugation_realProbes` |
| `TransitionProbability.conditionalConjugation_reportSwap` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.conditionalConjugation_reportSwap` |
| `TransitionProbability.conditionalConjugation_reversible` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.conditionalConjugation_reversible` |
| `TransitionProbability.countermodelRayEquiv` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.countermodelRayEquiv` |
| `TransitionProbability.countermodel_probabilities` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.countermodel_probabilities` |
| `TransitionProbability.identity_calibration` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.identity_calibration` |
| `TransitionProbability.identity_linearLift` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.identity_linearLift` |
| `TransitionProbability.identity_nonvanishing` | yes | yes | yes | Quot.sound, propext | `#print axioms TransitionProbability.identity_nonvanishing` |
| `TransitionProbability.imaginary_probe_probabilities` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.imaginary_probe_probabilities` |
| `TransitionProbability.insufficient_lattice_package` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.insufficient_lattice_package` |
| `TransitionProbability.insufficient_operational_package` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.insufficient_operational_package` |
| `TransitionProbability.involutiveRayEquiv` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.involutiveRayEquiv` |
| `TransitionProbability.ip_sub_left` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.ip_sub_left` |
| `TransitionProbability.ip_sub_right` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.ip_sub_right` |
| `TransitionProbability.linearRayEquiv` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.linearRayEquiv` |
| `TransitionProbability.linear_calibration_tpPreserving` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.linear_calibration_tpPreserving` |
| `TransitionProbability.linear_calibration_wigner` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.linear_calibration_wigner` |
| `TransitionProbability.normSq_neg_local` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.normSq_neg_local` |
| `TransitionProbability.oneSector_sameRay` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.oneSector_sameRay` |
| `TransitionProbability.oneSector_tpPreserving` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.oneSector_tpPreserving` |
| `TransitionProbability.orthogonality_calibration` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.orthogonality_calibration` |
| `TransitionProbability.rayMap` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.rayMap` |
| `TransitionProbability.raySetoid` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.raySetoid` |
| `TransitionProbability.reportSwap` | yes | yes | yes | propext | `#print axioms TransitionProbability.reportSwap` |
| `TransitionProbability.sameRay_refl` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.sameRay_refl` |
| `TransitionProbability.sameRay_symm` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.sameRay_symm` |
| `TransitionProbability.sameRay_trans` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.sameRay_trans` |
| `TransitionProbability.stretch` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.stretch` |
| `TransitionProbability.stretchLattice` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.stretchLattice` |
| `TransitionProbability.stretchRayEquiv` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.stretchRayEquiv` |
| `TransitionProbability.stretch_lattice` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.stretch_lattice` |
| `TransitionProbability.stretch_linearLift` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.stretch_linearLift` |
| `TransitionProbability.stretch_not_tpPreserving` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.stretch_not_tpPreserving` |
| `TransitionProbability.stretch_probabilities` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.stretch_probabilities` |
| `TransitionProbability.tomography_identity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.tomography_identity` |
| `TransitionProbability.tomography_sameRay` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.tomography_sameRay` |
| `TransitionProbability.tomography_tpPreserving` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.tomography_tpPreserving` |
| `TransitionProbability.witnessA` | yes | yes | yes | Quot.sound, propext | `#print axioms TransitionProbability.witnessA` |
| `TransitionProbability.witnessA_ne` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.witnessA_ne` |
| `TransitionProbability.witnessB` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.witnessB` |
| `TransitionProbability.witnessB_ne` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms TransitionProbability.witnessB_ne` |

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
- sha256 (`lf-normalised`): `aa32c9d601678d6cba3a22fb3b44c058c92c0d72417b1f4a549391bb38fe0f7f`
- generated view: listed, not counted
- cited in: record TFQ-1047
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/l1-imp-transition-probability-law.md`

- file: [dag/derivations/independent/l1-imp-transition-probability-law.md](../../../dag/derivations/independent/l1-imp-transition-probability-law.md)
- sha256 (`lf-normalised`): `6c9010a68ea4b3c13f88f0467d5c98ec8dc4fd1afffedf7581dd48222a74601a`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_l1-imp-transition-probability-law_lean_replay.json`

- file: [dag/research/campaign_l1-imp-transition-probability-law_lean_replay.json](../../../dag/research/campaign_l1-imp-transition-probability-law_lean_replay.json)
- sha256 (`lf-normalised`): `0b7fff93e5596fb0885d32e91297b8ebefd9a3dd24fa3009a60e3aa2942e04b5`
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
