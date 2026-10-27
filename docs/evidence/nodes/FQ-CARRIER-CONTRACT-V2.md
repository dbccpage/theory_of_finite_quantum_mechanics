# FQ-CARRIER-CONTRACT-V2

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Declared carrier: cyclotomic fields Q(zeta_n) with directed tower law (m | n gives Q(zeta_m) \<= Q(zeta_n)), declared target conductor LCM 120 (distinct conductors 1,2,3,4,5,8,12; 23 targets), Born weights |psi_j|^2 in the real subfield Q(zeta_n)^+. The colimit Q^ab is named but not constructed; Kronecker-Weber is DECLARED.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- complex/cyclotomic scalar field Q(zeta_n) (assumption)
- Kronecker-Weber theorem cited, not proved (assumption)
- target conductor 120 chosen, minimality not proved (assumption)

## Bottleneck

Q^ab colimit not constructed; no proof that 120 is minimal; amplitude embedding for all 23 targets not verified.

## Source status

REVIEWED_DECLARATIONS (carrier_contract.yaml); minimality_proved: false; all_target_amplitudes_embedding_verified: false

## Review

- PFP review: [dag/results/FQ-CARRIER-CONTRACT-V2/reviews/20261019_next_ten_audit/review_result.json](../../../dag/results/FQ-CARRIER-CONTRACT-V2/reviews/20261019_next_ten_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `DEFINITION`; qualifies for E4: yes.
  - narrowest claim: LCM120 on the actual inventory, literal conductor directedness and star-compatible RingHom theorem signatures, and seven independently checked quotient computations.
  - does not support: Constructed Q^ab colimit, proved Kronecker-Weber, field minimality, or verification of all amplitudes in all targets.
  - next test: Audit retained contract flags, complete coefficient arrays, actual Phi120 and optimized guard refusal.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CyclotomicTowerDirected.lean`

- file: [lean4/CyclotomicTowerDirected.lean](../../../lean4/CyclotomicTowerDirected.lean)
- sha256 (`bytes`): `9cd7c2e1e7fee5a2878cdf6cbf1603b4cef4b3e0654b9261f2c087e36b027695`
- cited in: node.lean, record TFQ-1006
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `CyclotomicTowerDirected`): recorded sha256 `9cd7c2e1e7fee5a2878cdf6cbf1603b4cef4b3e0654b9261f2c087e36b027695` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CyclotomicTowerDirected`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `cyclotomic_tower_is_directed` | yes | yes | yes | none | `#print axioms cyclotomic_tower_is_directed` |

- counts toward the grade: yes

### Lean: `lean4/HigherDimConductorBounds.lean`

- file: [lean4/HigherDimConductorBounds.lean](../../../lean4/HigherDimConductorBounds.lean)
- sha256 (`bytes`): `584e51cd0f1ed41d0f3b7fad0b4d235a6ce77e0d1ff41040379d1de748d124bc`
- cited in: node.lean, record TFQ-1006
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `HigherDimConductorBounds`): recorded sha256 `584e51cd0f1ed41d0f3b7fad0b4d235a6ce77e0d1ff41040379d1de748d124bc` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build HigherDimConductorBounds`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `css_horodecki_conductor_1_div_120` | yes | yes | yes | propext | `#print axioms css_horodecki_conductor_1_div_120` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1006_fq_carrier_contract_v2.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1006_fq_carrier_contract_v2.md](../../../dag/derivations/10_finite_qm_core/tfq_1006_fq_carrier_contract_v2.md)
- sha256 (`lf-normalised`): `7df51157931450301bbd5cd53c0b983bba69dd33bd2ebc4f14437a61007dc56c`
- generated view: listed, not counted
- cited in: record TFQ-1006
- counts toward the grade: no

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/claims/carrier_contract.yaml`

- file: [sources/atlas/papers/finite_quantum_mechanics/claims/carrier_contract.yaml](../../../sources/atlas/papers/finite_quantum_mechanics/claims/carrier_contract.yaml)
- sha256 (`lf-normalised`): `a1c709630c5a79fef6a8638e8fd9ee2d081643405a1ef49796e99c3b83ab8cb8`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md`

- file: [sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md](../../../sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `85ca7b22b1c1e360a4c17ad8a9e0bddae03433592585b01d23a74cd09c82929e`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:0ba65dffd00ca2ae423a972431eb56b48d31e223d7d05b4c7e2680aa2f0502fb::CyclotomicTower`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche16_master_177_node_172_route_dag_completeness_and_operad_audit_witness`

## Routes

Incoming (0):


Outgoing (18):

- `APP-R-DFM-GROUP-CONNECTION` `CONDITIONAL_ON_IMPORT`: [DFM-GROUP-CONNECTION](DFM-GROUP-CONNECTION.md) (DEFINITION)
- `DS-R-GRADED-PATHSUM-FROM-CARRIER` `COMPUTED`: [DS-QM030-GRADED-PATHSUM](DS-QM030-GRADED-PATHSUM.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-PRODUCT-DEFECT` `COMPUTED`: [DS-QM070-PRODUCT-NONFACTORIZATION](DS-QM070-PRODUCT-NONFACTORIZATION.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-STOCHASTIC-KERNEL` `COMPUTED`: [DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL](DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-TRACE-NORM-CORE-FROM-CARRIER` `COMPUTED`: [DS-QM080-IMPORT-FREE-TRACE-NORM-CORE](DS-QM080-IMPORT-FREE-TRACE-NORM-CORE.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-UNGRADED-COUNT` `COMPUTED`: [DS-QM030-UNGRADED-OVERCOUNT](DS-QM030-UNGRADED-OVERCOUNT.md) (COMPUTATIONALLY_CHECKED)
- `FQ-R-CARRIER-TO-INTERFACE` `CONDITIONAL_ON_IMPORT`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)
- `FQ-R-CONTINUUM-HILBERT-LIFT-CONSTRUCTION` `CONDITIONAL_ON_IMPORT`: [FQ-CONTINUUM-HILBERT-LIFT-CONSTRUCTION](FQ-CONTINUUM-HILBERT-LIFT-CONSTRUCTION.md) (PROVED_LEAN)
- `FQ-R-DYN-DICHOTOMY` `COMPUTED`: [FQ-DISCRETE-DYNAMICS-DICHOTOMY](FQ-DISCRETE-DYNAMICS-DICHOTOMY.md) (COMPUTATIONALLY_CHECKED)
- `FQ-R-EMBEDDING` `COMPUTED`: [FQ-GAP-REAL-EMBEDDING-CHOICE](FQ-GAP-REAL-EMBEDDING-CHOICE.md) (COMPUTATIONALLY_CHECKED)
- `FQ-R-ENTROPY` `DERIVED_LEAN`: [FQ-ENTROPY-DICHOTOMY-BAKER](FQ-ENTROPY-DICHOTOMY-BAKER.md) (PROVED_LEAN)
- `FQ-R-EVERETT` `COMPUTED`: [FQ-EVERETT-RATIONAL-SECTOR-BOUNDARY](FQ-EVERETT-RATIONAL-SECTOR-BOUNDARY.md) (COMPUTATIONALLY_CHECKED)
- `FQ-R-GAP-CONTINUUM` `CONDITIONAL_ON_IMPORT`: [FQ-GAP-CONTINUUM-HILBERT-LIFT](FQ-GAP-CONTINUUM-HILBERT-LIFT.md) (CONDITIONAL)
- `FQ-R-QM207-231` `COMPUTED`: [FQ-QM207-231-FINITE-MAP-CONTROLS](FQ-QM207-231-FINITE-MAP-CONTROLS.md) (COMPUTATIONALLY_CHECKED)
- `FQ-R-SORKIN-CLASS` `COMPUTED`: [FQ-SORKIN-READOUT-CLASS-QM208](FQ-SORKIN-READOUT-CLASS-QM208.md) (COMPUTATIONALLY_CHECKED)
- `FQ-R-TSIRELSON` `CONDITIONAL_ON_IMPORT`: [FQ-TSIRELSON-SOS-Q-SQRT2](FQ-TSIRELSON-SOS-Q-SQRT2.md) (COMPUTATIONALLY_CHECKED)
- `FQ-R-U1` `COMPUTED`: [FQ-U1-TRANSPORT-N-TORSION](FQ-U1-TRANSPORT-N-TORSION.md) (COMPUTATIONALLY_CHECKED)
- `FQ-R-WEYL` `DERIVED_LEAN`: [FQ-WEYL-FINITE-SCHRODINGER-IRREDUCIBILITY](FQ-WEYL-FINITE-SCHRODINGER-IRREDUCIBILITY.md) (PROVED_LEAN)

No incoming route.
