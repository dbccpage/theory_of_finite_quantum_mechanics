# FSP-QCD-CHEMICAL-POTENTIAL-DET

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For lattice Dirac operators with chemical potential, gamma5 D(mu) gamma5 = D(-mu*)^dagger, hence det D(mu)^* = det D(-mu*); for real mu != 0 this relates D(mu) to D(-mu) only and det D(mu) is in general complex.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 21
- distinct cited Lean declarations covered by a current replay receipt: 20
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- lattice QCD with staggered quarks at chemical potential (standard)

## Bottleneck

Standard continuum/thermodynamic QCD chemical-potential sign-problem framework imported; lean4/FermionSignQcdChemicalPotentialDet.lean establishes the exact gamma_5-chemical-potential determinant conjugation identity (det D(mu))* = det D(-mu*), reality at mu = 0 and purely imaginary mu = i mu_I, the Hasenfratz-Karsch and Kogut-Susskind staggered operator identities, the explicit SU(3) clock link U = diag(i,i,-1) with Im Tr(U) = 2 != 0, the 6x6 chiral SU(3) determinant witness det D_SU3(2) = 63/8 - 27i and det D_SU3(1/2) = 63/8 + 27i, and the diagonal SU(2) reality contrast; lean4/FQCD/StrongCouplingAreaLaw.lean establishes the finite-lattice Matrix (Site x Color x WeylSpinIdx) chemical-potential wrapper D_W(z), the matrix intertwining identity Gamma_5 D_W(z) Gamma_5 = D_W(z^-1)^H, determinant conjugation det D_W(z^-1) = star (det D_W(z)), and phase-quenched determinant positivity det(D_W(z) D_W(z^-1)) = |det D_W(z)|^2 \>= 0 (assembledWilsonDiracChemPotMatrix_intertwining_and_phase_quenched_positivity); while checks/independent/fsp-qcd-chemical-potential-det.py checks 1D and 2D staggered SU(3) vs SU(2) lattices.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-037 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/FQCD/StrongCouplingAreaLaw.lean`

- file: [lean4/FQCD/StrongCouplingAreaLaw.lean](../../../lean4/FQCD/StrongCouplingAreaLaw.lean)
- sha256 (`bytes`): `9f32c0851eac5b2326999627e68f6d35da1f73bb1f05cd001a998cc971d8108b`
- cited in: node.lean, record TFQ-1201
- replay: `verified`
  - receipt [dag/research/campaign_tfq-1050_lean_replay.json](../../../dag/research/campaign_tfq-1050_lean_replay.json) (module `FQCD.StrongCouplingAreaLaw`): recorded sha256 `9f32c0851eac5b2326999627e68f6d35da1f73bb1f05cd001a998cc971d8108b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/campaign_tfq-1052_lean_replay.json](../../../dag/research/campaign_tfq-1052_lean_replay.json) (module `FQCD.StrongCouplingAreaLaw`): recorded sha256 `9f32c0851eac5b2326999627e68f6d35da1f73bb1f05cd001a998cc971d8108b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/FQCD/StrongCouplingAreaLaw.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FQCD.assembledWilsonDiracChemPotMatrix_det_inv_eq_star` | yes | yes | yes | module-level | `#print axioms FQCD.assembledWilsonDiracChemPotMatrix_det_inv_eq_star` |
| `FQCD.assembledWilsonDiracChemPotMatrix_gamma5_intertwine` | yes | yes | yes | module-level | `#print axioms FQCD.assembledWilsonDiracChemPotMatrix_gamma5_intertwine` |
| `FQCD.assembledWilsonDiracChemPotMatrix_intertwining_and_phase_quenched_positivity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.assembledWilsonDiracChemPotMatrix_intertwining_and_phase_quenched_positivity` |

- counts toward the grade: yes

### Lean: `lean4/FermionSignQcdChemicalPotentialDet.lean`

- file: [lean4/FermionSignQcdChemicalPotentialDet.lean](../../../lean4/FermionSignQcdChemicalPotentialDet.lean)
- sha256 (`bytes`): `019d4ab1b47d30170969daf29ec72bba44cdf575c30b2ffe1e8c83d6776a5255`
- cited in: node.lean, receipt dag/research/campaign_fsp-qcd-chemical-potential-det_lean_replay.json (FermionSignQcdChemicalPotentialDet), record TFQ-1201
- replay: `verified`
  - receipt [dag/research/campaign_fsp-qcd-chemical-potential-det_lean_replay.json](../../../dag/research/campaign_fsp-qcd-chemical-potential-det_lean_replay.json) (module `FermionSignQcdChemicalPotentialDet`): recorded sha256 `019d4ab1b47d30170969daf29ec72bba44cdf575c30b2ffe1e8c83d6776a5255` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FermionSignQcdChemicalPotentialDet`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FermionSignQcdChemicalPotentialDet.det_conj_by_involution` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignQcdChemicalPotentialDet.det_conj_by_involution` |
| `FermionSignQcdChemicalPotentialDet.diracMu_det_conj` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignQcdChemicalPotentialDet.diracMu_det_conj` |
| `FermionSignQcdChemicalPotentialDet.diracMu_gamma5_adjoint` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignQcdChemicalPotentialDet.diracMu_gamma5_adjoint` |
| `FermionSignQcdChemicalPotentialDet.gamma5_imag_mu_det_im_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignQcdChemicalPotentialDet.gamma5_imag_mu_det_im_zero` |
| `FermionSignQcdChemicalPotentialDet.gamma5_mu_intertwine_det_conj` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignQcdChemicalPotentialDet.gamma5_mu_intertwine_det_conj` |
| `FermionSignQcdChemicalPotentialDet.gamma5_real_mu_det_conj` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignQcdChemicalPotentialDet.gamma5_real_mu_det_conj` |
| `FermionSignQcdChemicalPotentialDet.gamma5_zero_mu_det_im_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignQcdChemicalPotentialDet.gamma5_zero_mu_det_im_zero` |
| `FermionSignQcdChemicalPotentialDet.staggeredDiracMu_det_conj` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignQcdChemicalPotentialDet.staggeredDiracMu_det_conj` |
| `FermionSignQcdChemicalPotentialDet.staggeredDiracMu_gamma5_adjoint` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignQcdChemicalPotentialDet.staggeredDiracMu_gamma5_adjoint` |
| `FermionSignQcdChemicalPotentialDet.su2DiagLink_block_det_im_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignQcdChemicalPotentialDet.su2DiagLink_block_det_im_zero` |
| `FermionSignQcdChemicalPotentialDet.su3ClockLink_det` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignQcdChemicalPotentialDet.su3ClockLink_det` |
| `FermionSignQcdChemicalPotentialDet.su3ClockLink_trace_im_ne_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignQcdChemicalPotentialDet.su3ClockLink_trace_im_ne_zero` |
| `FermionSignQcdChemicalPotentialDet.su3ClockLink_unitary` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignQcdChemicalPotentialDet.su3ClockLink_unitary` |
| `FermionSignQcdChemicalPotentialDet.su3FugacityDirac_complex_det_witness` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignQcdChemicalPotentialDet.su3FugacityDirac_complex_det_witness` |
| `FermionSignQcdChemicalPotentialDet.su3FugacityDirac_det_at_half` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignQcdChemicalPotentialDet.su3FugacityDirac_det_at_half` |
| `FermionSignQcdChemicalPotentialDet.su3FugacityDirac_det_at_two` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignQcdChemicalPotentialDet.su3FugacityDirac_det_at_two` |
| `FermionSignQcdChemicalPotentialDet.su3FugacityDirac_gamma5_intertwine` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignQcdChemicalPotentialDet.su3FugacityDirac_gamma5_intertwine` |

- counts toward the grade: yes

### Python: `checks/independent/fsp-qcd-chemical-potential-det.py`

- file: [checks/independent/fsp-qcd-chemical-potential-det.py](../../../checks/independent/fsp-qcd-chemical-potential-det.py)
- sha256 (`bytes`): `b3b85e4eb8d26d593e359942890fb7d9332b7e5d2c50a5d57ef04215b1bf9a16`
- cited in: record TFQ-1201

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1201_fsp_qcd_chemical_potential_det.md`

- file: [dag/derivations/26_fsp/tfq_1201_fsp_qcd_chemical_potential_det.md](../../../dag/derivations/26_fsp/tfq_1201_fsp_qcd_chemical_potential_det.md)
- sha256 (`lf-normalised`): `928c602c8d18a41d705ac16e9d268e414c16c004263dfe966a6342a44e51b715`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1201
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-qcd-chemical-potential-det.md`

- file: [dag/derivations/independent/fsp-qcd-chemical-potential-det.md](../../../dag/derivations/independent/fsp-qcd-chemical-potential-det.md)
- sha256 (`lf-normalised`): `e21a0969eb966833dda9dfa2778c00b70db7ed7e06d7788183fe61395cc09527`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `3e88f1a70b66b0b90cc915acb5c802c118775e65cc8970af6c5a423f27ddd755`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-QCD-CHEMICAL-POTENTIAL-DET` `CONDITIONAL_ON_IMPORT`: [FSP-SU2-ADJOINT-REAL-DET](FSP-SU2-ADJOINT-REAL-DET.md) (IMPORTED_ASSUMPTION)

Outgoing (2):

- `APP-R-FSP-IMAGINARY-MU-REAL-DET` `CONDITIONAL_ON_IMPORT`: [FSP-IMAGINARY-MU-REAL-DET](FSP-IMAGINARY-MU-REAL-DET.md) (IMPORTED_ASSUMPTION)
- `APP-R-FSP-TRIALITY-CENTER-PROJECTION` `GAP_NO_DERIVATION`: [FSP-TRIALITY-CENTER-PROJECTION](FSP-TRIALITY-CENTER-PROJECTION.md) (OPEN)
