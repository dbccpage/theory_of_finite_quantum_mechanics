# FSP-QCD-CHEMICAL-POTENTIAL-DET

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For lattice Dirac operators with chemical potential, gamma5 D(mu) gamma5 = D(-mu*)^dagger, hence det D(mu)^* = det D(-mu*); for real mu != 0 this relates D(mu) to D(-mu) only and det D(mu) is in general complex.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 18
- distinct cited Lean declarations covered by a current replay receipt: 17
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- lattice QCD with staggered quarks at chemical potential (standard)

## Bottleneck

Standard continuum/thermodynamic QCD chemical-potential sign-problem framework imported; lean4/CampaignFspQcdChemicalPotentialDet.lean establishes the exact gamma_5-chemical-potential determinant conjugation identity (det D(mu))* = det D(-mu*), reality at mu = 0 and purely imaginary mu = i mu_I, the Hasenfratz-Karsch and Kogut-Susskind staggered operator identities, the explicit SU(3) clock link U = diag(i,i,-1) with Im Tr(U) = 2 != 0, the 6x6 chiral SU(3) determinant witness det D_SU3(2) = 63/8 - 27i and det D_SU3(1/2) = 63/8 + 27i, and the diagonal SU(2) reality contrast, while checks/independent/fsp-qcd-chemical-potential-det.py checks 1D and 2D staggered SU(3) vs SU(2) lattices.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-037 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspQcdChemicalPotentialDet.lean`

- file: [lean4/CampaignFspQcdChemicalPotentialDet.lean](../../../lean4/CampaignFspQcdChemicalPotentialDet.lean)
- sha256 (`bytes`): `cc12ac8e2f4a2fca8a4f408053d346ed18306fcd015ca1d44d023025468237eb`
- cited in: node.lean, receipt dag/research/campaign_fsp-qcd-chemical-potential-det_lean_replay.json (CampaignFspQcdChemicalPotentialDet), record TFQ-1201
- replay: `verified`
  - receipt [dag/research/campaign_fsp-qcd-chemical-potential-det_lean_replay.json](../../../dag/research/campaign_fsp-qcd-chemical-potential-det_lean_replay.json) (module `CampaignFspQcdChemicalPotentialDet`): recorded sha256 `cc12ac8e2f4a2fca8a4f408053d346ed18306fcd015ca1d44d023025468237eb` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspQcdChemicalPotentialDet`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspQcdChemicalPotentialDet.det_conj_by_involution` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspQcdChemicalPotentialDet.det_conj_by_involution` |
| `CampaignFspQcdChemicalPotentialDet.diracMu_det_conj` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspQcdChemicalPotentialDet.diracMu_det_conj` |
| `CampaignFspQcdChemicalPotentialDet.diracMu_gamma5_adjoint` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspQcdChemicalPotentialDet.diracMu_gamma5_adjoint` |
| `CampaignFspQcdChemicalPotentialDet.gamma5_imag_mu_det_im_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspQcdChemicalPotentialDet.gamma5_imag_mu_det_im_zero` |
| `CampaignFspQcdChemicalPotentialDet.gamma5_mu_intertwine_det_conj` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspQcdChemicalPotentialDet.gamma5_mu_intertwine_det_conj` |
| `CampaignFspQcdChemicalPotentialDet.gamma5_real_mu_det_conj` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspQcdChemicalPotentialDet.gamma5_real_mu_det_conj` |
| `CampaignFspQcdChemicalPotentialDet.gamma5_zero_mu_det_im_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspQcdChemicalPotentialDet.gamma5_zero_mu_det_im_zero` |
| `CampaignFspQcdChemicalPotentialDet.staggeredDiracMu_det_conj` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspQcdChemicalPotentialDet.staggeredDiracMu_det_conj` |
| `CampaignFspQcdChemicalPotentialDet.staggeredDiracMu_gamma5_adjoint` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspQcdChemicalPotentialDet.staggeredDiracMu_gamma5_adjoint` |
| `CampaignFspQcdChemicalPotentialDet.su2DiagLink_block_det_im_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspQcdChemicalPotentialDet.su2DiagLink_block_det_im_zero` |
| `CampaignFspQcdChemicalPotentialDet.su3ClockLink_det` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspQcdChemicalPotentialDet.su3ClockLink_det` |
| `CampaignFspQcdChemicalPotentialDet.su3ClockLink_trace_im_ne_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspQcdChemicalPotentialDet.su3ClockLink_trace_im_ne_zero` |
| `CampaignFspQcdChemicalPotentialDet.su3ClockLink_unitary` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspQcdChemicalPotentialDet.su3ClockLink_unitary` |
| `CampaignFspQcdChemicalPotentialDet.su3FugacityDirac_complex_det_witness` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspQcdChemicalPotentialDet.su3FugacityDirac_complex_det_witness` |
| `CampaignFspQcdChemicalPotentialDet.su3FugacityDirac_det_at_half` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspQcdChemicalPotentialDet.su3FugacityDirac_det_at_half` |
| `CampaignFspQcdChemicalPotentialDet.su3FugacityDirac_det_at_two` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspQcdChemicalPotentialDet.su3FugacityDirac_det_at_two` |
| `CampaignFspQcdChemicalPotentialDet.su3FugacityDirac_gamma5_intertwine` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspQcdChemicalPotentialDet.su3FugacityDirac_gamma5_intertwine` |

- counts toward the grade: yes

### Python: `checks/independent/fsp-qcd-chemical-potential-det.py`

- file: [checks/independent/fsp-qcd-chemical-potential-det.py](../../../checks/independent/fsp-qcd-chemical-potential-det.py)
- sha256 (`bytes`): `17f0f67942ac258c9a36f504a0848e6097cd8a6ecd3f7cb62c0af0555f2d51da`
- cited in: record TFQ-1201

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1201_fsp_qcd_chemical_potential_det.md`

- file: [dag/derivations/26_fsp/tfq_1201_fsp_qcd_chemical_potential_det.md](../../../dag/derivations/26_fsp/tfq_1201_fsp_qcd_chemical_potential_det.md)
- sha256 (`lf-normalised`): `067e02e8062c5252d03c0a9ab23ce53d8abb95c2411479e2beff5e4239e80fe7`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1201
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-qcd-chemical-potential-det.md`

- file: [dag/derivations/independent/fsp-qcd-chemical-potential-det.md](../../../dag/derivations/independent/fsp-qcd-chemical-potential-det.md)
- sha256 (`lf-normalised`): `5069031e4fc0ac18fd3b688861fec1781bc4de2efccbb7b6d9f17d9857f05c49`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-QCD-CHEMICAL-POTENTIAL-DET` `CONDITIONAL_ON_IMPORT`: [FSP-SU2-ADJOINT-REAL-DET](FSP-SU2-ADJOINT-REAL-DET.md) (IMPORTED_ASSUMPTION)

Outgoing (2):

- `APP-R-FSP-IMAGINARY-MU-REAL-DET` `CONDITIONAL_ON_IMPORT`: [FSP-IMAGINARY-MU-REAL-DET](FSP-IMAGINARY-MU-REAL-DET.md) (IMPORTED_ASSUMPTION)
- `APP-R-FSP-TRIALITY-CENTER-PROJECTION` `GAP_NO_DERIVATION`: [FSP-TRIALITY-CENTER-PROJECTION](FSP-TRIALITY-CENTER-PROJECTION.md) (OPEN)
