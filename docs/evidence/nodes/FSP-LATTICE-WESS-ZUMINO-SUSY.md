# FSP-LATTICE-WESS-ZUMINO-SUSY

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claimed: a finite-lattice 2D N=1 Wess-Zumino model with supercharges obeying {Q_a, Q_b} = 2 delta_ab H, H \>= 0 and exact boson-fermion pairing of nonzero levels; no such lattice construction exists in this checkout, and lattice discretizations generally keep at most a subalgebra exact.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 27
- distinct cited Lean declarations covered by a current replay receipt: 26
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Full interacting 2D continuum/lattice super-Poincare restoration remains open; lean4/CampaignFspLatticeWessZuminoSusy.lean establishes the exact Z_2-graded block supercharge algebra (Q(A)^2 = 0, {Q_a, Q_b} = 2 delta_ab H(A, A^dagger), \[Gamma_F, H\] = 0, \[Q, H\] = 0), quadratic-form nonnegativity of A^T A and A A^T, supertrace vanishing Tr(Gamma_F H) = 0, exact nonzero-energy boson-fermion eigenstate pairing, the explicit 2-site lattice Wess-Zumino block wz2SiteBlock, and the 3-site discrete cubic Leibniz defect witness (-2 != 0), while checks/independent/fsp-lattice-wess-zumino-susy.py checks 1D and rectangular lattice Wess-Zumino models.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-040 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspLatticeWessZuminoSusy.lean`

- file: [lean4/CampaignFspLatticeWessZuminoSusy.lean](../../../lean4/CampaignFspLatticeWessZuminoSusy.lean)
- sha256 (`bytes`): `66e430ef4fb48d2fdcd5e41f12d06351c9880793a607f9472d67d89567b9e090`
- cited in: node.lean, receipt dag/research/campaign_fsp-lattice-wess-zumino-susy_lean_replay.json (CampaignFspLatticeWessZuminoSusy), record TFQ-1204
- replay: `verified`
  - receipt [dag/research/campaign_fsp-lattice-wess-zumino-susy_lean_replay.json](../../../dag/research/campaign_fsp-lattice-wess-zumino-susy_lean_replay.json) (module `CampaignFspLatticeWessZuminoSusy`): recorded sha256 `66e430ef4fb48d2fdcd5e41f12d06351c9880793a607f9472d67d89567b9e090` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspLatticeWessZuminoSusy`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspLatticeWessZuminoSusy.bosonBlock_quadForm_eq_sum_sq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.bosonBlock_quadForm_eq_sum_sq` |
| `CampaignFspLatticeWessZuminoSusy.bosonBlock_quadForm_nonneg` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.bosonBlock_quadForm_nonneg` |
| `CampaignFspLatticeWessZuminoSusy.boson_eq_fermion_trace` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.boson_eq_fermion_trace` |
| `CampaignFspLatticeWessZuminoSusy.boson_partner_ne_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.boson_partner_ne_zero` |
| `CampaignFspLatticeWessZuminoSusy.boson_to_fermion_eigenstate` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.boson_to_fermion_eigenstate` |
| `CampaignFspLatticeWessZuminoSusy.brokenSupercharge_sq_ne_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.brokenSupercharge_sq_ne_zero` |
| `CampaignFspLatticeWessZuminoSusy.fermionBlock_quadForm_nonneg` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.fermionBlock_quadForm_nonneg` |
| `CampaignFspLatticeWessZuminoSusy.fermionParity_sq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.fermionParity_sq` |
| `CampaignFspLatticeWessZuminoSusy.fermion_to_boson_eigenstate` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.fermion_to_boson_eigenstate` |
| `CampaignFspLatticeWessZuminoSusy.hermSupercharge1_hermitian` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.hermSupercharge1_hermitian` |
| `CampaignFspLatticeWessZuminoSusy.hermSupercharge1_sq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.hermSupercharge1_sq` |
| `CampaignFspLatticeWessZuminoSusy.hermSupercharge2_hermitian` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.hermSupercharge2_hermitian` |
| `CampaignFspLatticeWessZuminoSusy.hermSupercharge2_sq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.hermSupercharge2_sq` |
| `CampaignFspLatticeWessZuminoSusy.hermSupercharge_anticomm` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.hermSupercharge_anticomm` |
| `CampaignFspLatticeWessZuminoSusy.leibnizCubicDefect3_witness` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.leibnizCubicDefect3_witness` |
| `CampaignFspLatticeWessZuminoSusy.superchargeAdj_anticommutes_parity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.superchargeAdj_anticommutes_parity` |
| `CampaignFspLatticeWessZuminoSusy.superchargeAdj_commutes_susyHamiltonian` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.superchargeAdj_commutes_susyHamiltonian` |
| `CampaignFspLatticeWessZuminoSusy.superchargeAdj_sq_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.superchargeAdj_sq_zero` |
| `CampaignFspLatticeWessZuminoSusy.supercharge_anticommutes_parity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.supercharge_anticommutes_parity` |
| `CampaignFspLatticeWessZuminoSusy.supercharge_commutes_susyHamiltonian` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.supercharge_commutes_susyHamiltonian` |
| `CampaignFspLatticeWessZuminoSusy.supercharge_sq_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.supercharge_sq_zero` |
| `CampaignFspLatticeWessZuminoSusy.supertrace_susyHamiltonian_eq_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.supertrace_susyHamiltonian_eq_zero` |
| `CampaignFspLatticeWessZuminoSusy.susyHamiltonian_commutes_parity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.susyHamiltonian_commutes_parity` |
| `CampaignFspLatticeWessZuminoSusy.susyHamiltonian_eq_fromBlocks` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.susyHamiltonian_eq_fromBlocks` |
| `CampaignFspLatticeWessZuminoSusy.wz2SiteBlock_boson_eq_fermion` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.wz2SiteBlock_boson_eq_fermion` |
| `CampaignFspLatticeWessZuminoSusy.wz2SiteBlock_det` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspLatticeWessZuminoSusy.wz2SiteBlock_det` |

- counts toward the grade: yes

### Python: `checks/independent/fsp-lattice-wess-zumino-susy.py`

- file: [checks/independent/fsp-lattice-wess-zumino-susy.py](../../../checks/independent/fsp-lattice-wess-zumino-susy.py)
- sha256 (`bytes`): `ce644eca4c637c8210f4770bc9cae339c1bbdd14bd87edd11a34204951408da4`
- cited in: record TFQ-1204

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1204_fsp_lattice_wess_zumino_susy.md`

- file: [dag/derivations/26_fsp/tfq_1204_fsp_lattice_wess_zumino_susy.md](../../../dag/derivations/26_fsp/tfq_1204_fsp_lattice_wess_zumino_susy.md)
- sha256 (`lf-normalised`): `48bde3ecd3c7dfe1a191920a7164c42fb07a792a1ee09a7c5d99d0eb99e07194`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1204
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-lattice-wess-zumino-susy.md`

- file: [dag/derivations/independent/fsp-lattice-wess-zumino-susy.md](../../../dag/derivations/independent/fsp-lattice-wess-zumino-susy.md)
- sha256 (`lf-normalised`): `c74791f2124ec0a5b81f1398b50544076794c201fcc2da025861a6240cd9b780`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `5a72c2f6006ea18c3362f0a63e8525b65d41898e8f1bd437b7e4c2e368c7e102`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-LATTICE-WESS-ZUMINO-SUSY` `GAP_NO_DERIVATION`: [FSP-CAR-EXTERIOR-FOCK](FSP-CAR-EXTERIOR-FOCK.md) (PROVED_PROSE), [FSP-IMAGINARY-MU-REAL-DET](FSP-IMAGINARY-MU-REAL-DET.md) (IMPORTED_ASSUMPTION)

Outgoing (2):

- `APP-R-FSP-NICOLAI-MAP-CLAIM` `GAP_NO_DERIVATION`: [FSP-NICOLAI-MAP-CLAIM](FSP-NICOLAI-MAP-CLAIM.md) (OPEN)
- `APP-R-FSP-WITTEN-INDEX-INVARIANCE` `CONDITIONAL_ON_IMPORT`: [FSP-WITTEN-INDEX-INVARIANCE](FSP-WITTEN-INDEX-INVARIANCE.md) (IMPORTED_ASSUMPTION)
