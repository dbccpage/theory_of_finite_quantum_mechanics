# FSP-SU2-ADJOINT-REAL-DET

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For lattice SU(2) with Dirac fermions in the real adjoint representation, an antiunitary symmetry of the Dirac operator makes det D_adj real for every gauge configuration.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 17
- distinct cited Lean declarations covered by a current replay receipt: 16
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- lattice SU(2) gauge theory with adjoint Dirac fermions (standard)

## Bottleneck

For a single Majorana adjoint flavor the measure is a Pfaffian whose sign can change; reality is not positivity. FermionSignSu2AdjointRealDet.lean establishes the 3x3 SO(3) adjoint representation of unit quaternions, Z_2 center blindness R(-q) = R(q), the antiunitary intertwiner reality identity C conj(D) = D C -\> Im(det D) = 0, reality of the 4D lattice adjoint Wilson-Dirac determinant wilsonDiracAdjoint4_det_im_zero, a negative-determinant witness (det = -1 \< 0), and the 2x2 and 4x4 skew-symmetric Majorana Pfaffian square identities and sign-flip pairs. Full continuum SU(2) path-integral construction and general 2n x 2n Berezin Grassmann integration remain literature imports.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-036 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/FermionSignSu2AdjointRealDet.lean`

- file: [lean4/FermionSignSu2AdjointRealDet.lean](../../../lean4/FermionSignSu2AdjointRealDet.lean)
- sha256 (`bytes`): `b1f2169bb234f72a581c893a37b6a968ddaf9e121e955c66d23ac42165cf5ecf`
- cited in: node.lean, receipt dag/research/campaign_fsp-su2-adjoint-real-det_lean_replay.json (FermionSignSu2AdjointRealDet), record TFQ-1200
- replay: `verified`
  - receipt [dag/research/campaign_fsp-su2-adjoint-real-det_lean_replay.json](../../../dag/research/campaign_fsp-su2-adjoint-real-det_lean_replay.json) (module `FermionSignSu2AdjointRealDet`): recorded sha256 `b1f2169bb234f72a581c893a37b6a968ddaf9e121e955c66d23ac42165cf5ecf` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FermionSignSu2AdjointRealDet`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FermionSignSu2AdjointRealDet.antiunitary_intertwiner_det_conj` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignSu2AdjointRealDet.antiunitary_intertwiner_det_conj` |
| `FermionSignSu2AdjointRealDet.antiunitary_intertwiner_det_im_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignSu2AdjointRealDet.antiunitary_intertwiner_det_im_zero` |
| `FermionSignSu2AdjointRealDet.antiunitary_intertwiner_two_flavor_nonneg` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignSu2AdjointRealDet.antiunitary_intertwiner_two_flavor_nonneg` |
| `FermionSignSu2AdjointRealDet.chargeConj4_intertwines_gamma4d` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignSu2AdjointRealDet.chargeConj4_intertwines_gamma4d` |
| `FermionSignSu2AdjointRealDet.majorana_pfaffian2_sign_flip` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignSu2AdjointRealDet.majorana_pfaffian2_sign_flip` |
| `FermionSignSu2AdjointRealDet.majorana_pfaffian4_sign_flip` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignSu2AdjointRealDet.majorana_pfaffian4_sign_flip` |
| `FermionSignSu2AdjointRealDet.reality_not_positivity_witness` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignSu2AdjointRealDet.reality_not_positivity_witness` |
| `FermionSignSu2AdjointRealDet.skew2_det_eq_pfaffian2_sq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignSu2AdjointRealDet.skew2_det_eq_pfaffian2_sq` |
| `FermionSignSu2AdjointRealDet.skew4_det_eq_pfaffian4_sq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignSu2AdjointRealDet.skew4_det_eq_pfaffian4_sq` |
| `FermionSignSu2AdjointRealDet.su2AdjointMatrix_center_blind` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignSu2AdjointRealDet.su2AdjointMatrix_center_blind` |
| `FermionSignSu2AdjointRealDet.su2AdjointMatrix_det_eq_norm_cube` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignSu2AdjointRealDet.su2AdjointMatrix_det_eq_norm_cube` |
| `FermionSignSu2AdjointRealDet.su2AdjointMatrix_det_one` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignSu2AdjointRealDet.su2AdjointMatrix_det_one` |
| `FermionSignSu2AdjointRealDet.su2AdjointMatrix_transpose_mul_self` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignSu2AdjointRealDet.su2AdjointMatrix_transpose_mul_self` |
| `FermionSignSu2AdjointRealDet.wilsonDiracAdjoint4_det_conj` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignSu2AdjointRealDet.wilsonDiracAdjoint4_det_conj` |
| `FermionSignSu2AdjointRealDet.wilsonDiracAdjoint4_det_im_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignSu2AdjointRealDet.wilsonDiracAdjoint4_det_im_zero` |
| `FermionSignSu2AdjointRealDet.wilsonDiracAdjoint4_intertwined` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignSu2AdjointRealDet.wilsonDiracAdjoint4_intertwined` |

- counts toward the grade: yes

### Python: `checks/independent/fsp-su2-adjoint-real-det.py`

- file: [checks/independent/fsp-su2-adjoint-real-det.py](../../../checks/independent/fsp-su2-adjoint-real-det.py)
- sha256 (`bytes`): `79ffe77aa0ee9357257c7ec27e7cbaef34646961e2c2f9f41848088a20927837`
- cited in: record TFQ-1200

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1200_fsp_su2_adjoint_real_det.md`

- file: [dag/derivations/26_fsp/tfq_1200_fsp_su2_adjoint_real_det.md](../../../dag/derivations/26_fsp/tfq_1200_fsp_su2_adjoint_real_det.md)
- sha256 (`lf-normalised`): `cf08daa90d05e9d39bf509ddda5b32291972319519bc5f513ae792519d5deb22`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1200
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-su2-adjoint-real-det.md`

- file: [dag/derivations/independent/fsp-su2-adjoint-real-det.md](../../../dag/derivations/independent/fsp-su2-adjoint-real-det.md)
- sha256 (`lf-normalised`): `c31ea18c068120274a7baa1a4652bc6f392a17d89bb4630efc1a7565f86818a9`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign.md)
- sha256 (`lf-normalised`): `5f5dfaa7a3794d1fee0299865df221b6db1c14ebf6f3925b1729e784a28e3194`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `3e88f1a70b66b0b90cc915acb5c802c118775e65cc8970af6c5a423f27ddd755`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-SU2-ADJOINT-REAL-DET` `CONDITIONAL_ON_IMPORT`: [FSP-U1-WILSON-ACTION](FSP-U1-WILSON-ACTION.md) (PROVED_LEAN), [FSP-WILSON-DIRAC-GAMMA5](FSP-WILSON-DIRAC-GAMMA5.md) (IMPORTED_ASSUMPTION), [FSP-LATTICE-ANOMALY-INFLOW](FSP-LATTICE-ANOMALY-INFLOW.md) (OPEN)

Outgoing (1):

- `APP-R-FSP-QCD-CHEMICAL-POTENTIAL-DET` `CONDITIONAL_ON_IMPORT`: [FSP-QCD-CHEMICAL-POTENTIAL-DET](FSP-QCD-CHEMICAL-POTENTIAL-DET.md) (IMPORTED_ASSUMPTION)
