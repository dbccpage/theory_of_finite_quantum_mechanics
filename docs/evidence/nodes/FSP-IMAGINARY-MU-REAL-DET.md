# FSP-IMAGINARY-MU-REAL-DET

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> At mu = i mu_I with real mu_I, gamma5 D(i mu_I) gamma5 = D(i mu_I)^dagger, so det D(i mu_I) is real; nonnegativity needs two degenerate flavors (or a staggered operator m + K with K anti-Hermitian, m \> 0), and Z(mu_I) has Roberge-Weiss periodicity 2 pi T / 3.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 22
- distinct cited Lean declarations covered by a current replay receipt: 16
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- imaginary chemical potential and Roberge-Weiss periodicity (literature)

## Bottleneck

Analytic continuation from imaginary to real mu is an extrapolation, not a sign-free route to real mu; not established in this checkout. FermionSignImaginaryMuRealDet covers arbitrary finite bipartite transport blocks at unit fugacity: staggered adjoint symmetry, determinant reality, two-flavor nonnegativity and positive-mass staggered positivity. Its centerSum_periodic concerns a declared finite center-orbit sum only; it supplies no QCD measure, spin-taste reconstruction, phase transition or analytic-continuation theorem. The full node remains imported.

## Source status

dag/derivations/26_fsp/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-039 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/FermionSignImaginaryMuRealDet.lean`

- file: [lean4/FermionSignImaginaryMuRealDet.lean](../../../lean4/FermionSignImaginaryMuRealDet.lean)
- sha256 (`bytes`): `fa5f4b2f76560be37d6fccff11842fa7edf1504c4488dd8b1bb2b7d09267504c`
- cited in: node.lean, receipt evidence/lean_receipts/campaign_fsp-imaginary-mu-real-det_lean_replay.json (FermionSignImaginaryMuRealDet), record TFQ-1203
- replay: `verified`
  - receipt [evidence/lean_receipts/campaign_fsp-imaginary-mu-real-det_lean_replay.json](../../../evidence/lean_receipts/campaign_fsp-imaginary-mu-real-det_lean_replay.json) (module `FermionSignImaginaryMuRealDet`): recorded sha256 `fa5f4b2f76560be37d6fccff11842fa7edf1504c4488dd8b1bb2b7d09267504c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FermionSignImaginaryMuRealDet`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FermionSignImaginaryMuRealDet.bipartite_adjoint` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignImaginaryMuRealDet.bipartite_adjoint` |
| `FermionSignImaginaryMuRealDet.bipartite_det_pos` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignImaginaryMuRealDet.bipartite_det_pos` |
| `FermionSignImaginaryMuRealDet.bipartite_one_det` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignImaginaryMuRealDet.bipartite_one_det` |
| `FermionSignImaginaryMuRealDet.bipartite_one_det_pos` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignImaginaryMuRealDet.bipartite_one_det_pos` |
| `FermionSignImaginaryMuRealDet.bipartite_scale` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignImaginaryMuRealDet.bipartite_scale` |
| `FermionSignImaginaryMuRealDet.centerSum_periodic` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignImaginaryMuRealDet.centerSum_periodic` |
| `FermionSignImaginaryMuRealDet.det_real_of_involution` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignImaginaryMuRealDet.det_real_of_involution` |
| `FermionSignImaginaryMuRealDet.gamma_hermitian_negative` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignImaginaryMuRealDet.gamma_hermitian_negative` |
| `FermionSignImaginaryMuRealDet.inverse_eq_star` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignImaginaryMuRealDet.inverse_eq_star` |
| `FermionSignImaginaryMuRealDet.parity_hermitian` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignImaginaryMuRealDet.parity_hermitian` |
| `FermionSignImaginaryMuRealDet.parity_sq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignImaginaryMuRealDet.parity_sq` |
| `FermionSignImaginaryMuRealDet.staggered_adjoint` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignImaginaryMuRealDet.staggered_adjoint` |
| `FermionSignImaginaryMuRealDet.staggered_det_pos` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignImaginaryMuRealDet.staggered_det_pos` |
| `FermionSignImaginaryMuRealDet.staggered_det_real` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignImaginaryMuRealDet.staggered_det_real` |
| `FermionSignImaginaryMuRealDet.staggered_unit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignImaginaryMuRealDet.staggered_unit` |
| `FermionSignImaginaryMuRealDet.two_flavor_nonneg` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignImaginaryMuRealDet.two_flavor_nonneg` |
| `centerSum_periodic` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms centerSum_periodic` |
| `det_real_of_involution` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms det_real_of_involution` |
| `gamma_hermitian_negative` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms gamma_hermitian_negative` |
| `staggered_adjoint` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms staggered_adjoint` |
| `staggered_det_pos` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms staggered_det_pos` |
| `two_flavor_nonneg` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms two_flavor_nonneg` |

- counts toward the grade: yes

### Python: `checks/independent/fsp-imaginary-mu-real-det.py`

- file: [checks/independent/fsp-imaginary-mu-real-det.py](../../../checks/independent/fsp-imaginary-mu-real-det.py)
- sha256 (`bytes`): `ab094f550383685c6198ab4a2ffc96e707c9ef75d18d704dada8872b4ead374a`
- cited in: record TFQ-1203
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/fsp/theory_of_finite_fsp.md`

- file: [dag/derivations/26_fsp/fsp/theory_of_finite_fsp.md](../../../dag/derivations/26_fsp/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `7945c7b1530510f48a0acc7c484332febe5003b2f99b1e2755f4706d224b330f`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1203_fsp_imaginary_mu_real_det.md`

- file: [dag/derivations/26_fsp/tfq_1203_fsp_imaginary_mu_real_det.md](../../../dag/derivations/26_fsp/tfq_1203_fsp_imaginary_mu_real_det.md)
- sha256 (`lf-normalised`): `5bd1cfdabded1e7a232e684bf15110d2045dd6947f1c3d579ae378356c13c35b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1203
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-FSP-IMAGINARY-MU-REAL-DET` `CONDITIONAL_ON_IMPORT`: [FSP-QCD-CHEMICAL-POTENTIAL-DET](FSP-QCD-CHEMICAL-POTENTIAL-DET.md) (IMPORTED_ASSUMPTION)

Outgoing (2):

- `APP-R-FSP-LATTICE-WESS-ZUMINO-SUSY` `GAP_NO_DERIVATION`: [FSP-LATTICE-WESS-ZUMINO-SUSY](FSP-LATTICE-WESS-ZUMINO-SUSY.md) (OPEN)
- `APP-R-FSP-MASTER-DICHOTOMY-REFUTED` `DERIVED_PROSE`: [FSP-MASTER-DICHOTOMY-REFUTED](FSP-MASTER-DICHOTOMY-REFUTED.md) (REFUTED)
