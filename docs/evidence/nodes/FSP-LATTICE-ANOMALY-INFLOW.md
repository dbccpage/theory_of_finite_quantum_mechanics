# FSP-LATTICE-ANOMALY-INFLOW

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Target: on a finite slab lattice the chiral variation of the boundary fermion determinant cancels the bulk Chern-Simons variation. Not established in this checkout. One tested candidate does not realize it, as expected: on open Wilson slabs with U(1) links, the gauge change acts on the Wilson matrix by a diagonal similarity, so the full, interior, boundary Schur and fixed site-matched chiral-block determinants are gauge invariant by construction, while a lifted cup-product CS term whose coefficient is not derived from the fermions changes by 1/32. This is a fixed-basis truncation of a vector-like regulator, not an obstruction to lattice inflow.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 19
- distinct cited Lean declarations covered by a current replay receipt: 18
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Callan-Harvey continuum anomaly inflow (literature)

## Bottleneck

Construct a regulated chiral boundary determinant whose projector, basis or measure depends on the gauge field (domain-wall or overlap/Ginsparg-Wilson type), derive from the same fermions the bulk Chern-Simons term they induce, and show that the two gauge variations cancel. The fixed-basis Wilson-slab test cannot register an anomaly, because site-matched fixed bases give similarity-invariant determinants; its bare lifted CS candidate is neither induced by the fermions nor well defined on U(1) links (an integer lift of the same links changes it by 1/8). The continuum Callan-Harvey mechanism remains a literature import.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-035 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/FermionSignLatticeAnomalyInflow.lean`

- file: [lean4/FermionSignLatticeAnomalyInflow.lean](../../../lean4/FermionSignLatticeAnomalyInflow.lean)
- sha256 (`bytes`): `cc2e2d8e2b63de8c4fe5f349ba20e6a3bf75a48be27f1f81957668c4f48da1a1`
- cited in: node.lean, receipt dag/research/campaign_fsp-lattice-anomaly-inflow_lean_replay.json (FermionSignLatticeAnomalyInflow), record TFQ-1199
- replay: `verified`
  - receipt [dag/research/campaign_fsp-lattice-anomaly-inflow_lean_replay.json](../../../dag/research/campaign_fsp-lattice-anomaly-inflow_lean_replay.json) (module `FermionSignLatticeAnomalyInflow`): recorded sha256 `cc2e2d8e2b63de8c4fe5f349ba20e6a3bf75a48be27f1f81957668c4f48da1a1` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FermionSignLatticeAnomalyInflow`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FermionSignLatticeAnomalyInflow.bianchi` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignLatticeAnomalyInflow.bianchi` |
| `FermionSignLatticeAnomalyInflow.chiral_fixed_basis_det` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignLatticeAnomalyInflow.chiral_fixed_basis_det` |
| `FermionSignLatticeAnomalyInflow.cs_cell_variation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignLatticeAnomalyInflow.cs_cell_variation` |
| `FermionSignLatticeAnomalyInflow.cs_chain_variation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignLatticeAnomalyInflow.cs_chain_variation` |
| `FermionSignLatticeAnomalyInflow.curvature_gauge` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignLatticeAnomalyInflow.curvature_gauge` |
| `FermionSignLatticeAnomalyInflow.det_transport` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignLatticeAnomalyInflow.det_transport` |
| `FermionSignLatticeAnomalyInflow.finite_variation_nonzero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignLatticeAnomalyInflow.finite_variation_nonzero` |
| `FermionSignLatticeAnomalyInflow.hopping_covariant` | yes | yes | yes | Quot.sound, propext | `#print axioms FermionSignLatticeAnomalyInflow.hopping_covariant` |
| `FermionSignLatticeAnomalyInflow.phase_obstruction` | yes | yes | yes | Quot.sound, propext | `#print axioms FermionSignLatticeAnomalyInflow.phase_obstruction` |
| `FermionSignLatticeAnomalyInflow.phase_times_det_ne` | yes | yes | yes | Quot.sound, propext | `#print axioms FermionSignLatticeAnomalyInflow.phase_times_det_ne` |
| `FermionSignLatticeAnomalyInflow.schur_covariant` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignLatticeAnomalyInflow.schur_covariant` |
| `FermionSignLatticeAnomalyInflow.slab_four_cs` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignLatticeAnomalyInflow.slab_four_cs` |
| `FermionSignLatticeAnomalyInflow.slab_three_cs` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignLatticeAnomalyInflow.slab_three_cs` |
| `FermionSignLatticeAnomalyInflow.transport_eq_conjugate` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignLatticeAnomalyInflow.transport_eq_conjugate` |
| `FermionSignLatticeAnomalyInflow.transport_inverse` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignLatticeAnomalyInflow.transport_inverse` |
| `FermionSignLatticeAnomalyInflow.transport_mul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignLatticeAnomalyInflow.transport_mul` |
| `FermionSignLatticeAnomalyInflow.transport_one` | yes | yes | yes | Quot.sound, propext | `#print axioms FermionSignLatticeAnomalyInflow.transport_one` |
| `FermionSignLatticeAnomalyInflow.transport_sub` | yes | yes | yes | Quot.sound, propext | `#print axioms FermionSignLatticeAnomalyInflow.transport_sub` |

- counts toward the grade: yes

### Python: `checks/independent/fsp-lattice-anomaly-inflow.py`

- file: [checks/independent/fsp-lattice-anomaly-inflow.py](../../../checks/independent/fsp-lattice-anomaly-inflow.py)
- sha256 (`bytes`): `2a2ad3b9fde58a676054711f0c64c387fab7018ae75754be59cadc668e28aecc`
- cited in: record TFQ-1199

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1199_fsp_lattice_anomaly_inflow.md`

- file: [dag/derivations/26_fsp/tfq_1199_fsp_lattice_anomaly_inflow.md](../../../dag/derivations/26_fsp/tfq_1199_fsp_lattice_anomaly_inflow.md)
- sha256 (`lf-normalised`): `0bbd8d529e39fcd81dc8ecd3fdc6462911b048e57bd27409e3775ac38169b311`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1199
- counts toward the grade: no

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign.md)
- sha256 (`lf-normalised`): `f894f295fb17dc831f4e961602bea56223bf79ae6b34c3350cfa6fe358789808`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md)
- sha256 (`lf-normalised`): `0a97b32d187a99450605943866d6d4285f0bfd73dcc021c2b69911243066f2f3`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `5a72c2f6006ea18c3362f0a63e8525b65d41898e8f1bd437b7e4c2e368c7e102`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-LATTICE-ANOMALY-INFLOW` `GAP_NO_DERIVATION`: [FSP-WILSON-DIRAC-GAMMA5](FSP-WILSON-DIRAC-GAMMA5.md) (IMPORTED_ASSUMPTION)

Outgoing (2):

- `APP-R-FSP-MASTER-DICHOTOMY-REFUTED` `DERIVED_PROSE`: [FSP-MASTER-DICHOTOMY-REFUTED](FSP-MASTER-DICHOTOMY-REFUTED.md) (REFUTED)
- `APP-R-FSP-SU2-ADJOINT-REAL-DET` `CONDITIONAL_ON_IMPORT`: [FSP-SU2-ADJOINT-REAL-DET](FSP-SU2-ADJOINT-REAL-DET.md) (IMPORTED_ASSUMPTION)
