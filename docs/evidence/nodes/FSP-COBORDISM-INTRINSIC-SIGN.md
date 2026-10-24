# FSP-COBORDISM-INTRINSIC-SIGN

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claimed: a 4D boundary fermion theory with nontrivial invariant exp(2 pi i eta) in Omega_5^Spin(B Z2) has an unremovable sign problem curable only by a 5D bulk; no computation of the bordism group, eta invariant or sign obstruction exists in this checkout.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 8
- cited Lean, Rust or Python symbols found in their in-repo files: 10
- cited Lean declarations covered by a current replay receipt: 10
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Narrowed algebraic checks only. The integer spectral-sign function is odd; the declared 2x2 block has determinant m^2-s; two four-entry sign sums are 2 and -2. The exact supplied ZMod 2 formula is a3*arf+w1*sigmaDiv16, not n1+arf*c2+n2*w2. The Ward lemma concerns two nonnegative integer weights under the supplied equation w0+w1=-(w0+w1); it does not derive that equation from an anomaly or quantify over a configuration involution. P*H*P=2*D and equality of H/D traces/determinants do not assert trace preservation for P*H*P. Arithmetic in ZMod 16 computes no Pin bordism group. No manifold, AHSS, mapping-torus Dirac construction, anomaly classification, or bulk-boundary no-go theorem is formalized. Status is unchanged. The original physical or operational bridge remains open.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-047 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspCobordismIntrinsicSign.lean`

- file: [lean4/CampaignFspCobordismIntrinsicSign.lean](../../../lean4/CampaignFspCobordismIntrinsicSign.lean)
- sha256 (`bytes`): `be8a115911db61211f437136c8db75dfcfa0262af23ff050a890ddc4f644dfc8`
- cited in: node.lean, record TFQ-1211
- replay: `verified`
  - receipt [dag/research/campaign_fsp-cobordism-intrinsic-sign_lean_replay.json](../../../dag/research/campaign_fsp-cobordism-intrinsic-sign_lean_replay.json) (module `CampaignFspCobordismIntrinsicSign`): recorded sha256 `be8a115911db61211f437136c8db75dfcfa0262af23ff050a890ddc4f644dfc8` matches the current file; exit code 0; Lean None; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspCobordismIntrinsicSign`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspCobordismIntrinsicSign.ahss_5d_spin_cobordism_pairing_sectors` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspCobordismIntrinsicSign.ahss_5d_spin_cobordism_pairing_sectors` |
| `CampaignFspCobordismIntrinsicSign.anomaly_odd_ward_identity_rules_out_positive_weights_in_class` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspCobordismIntrinsicSign.anomaly_odd_ward_identity_rules_out_positive_weights_in_class` |
| `CampaignFspCobordismIntrinsicSign.arf_gaussian_sign_sum_dichotomy` | yes | yes | yes | propext | `#print axioms CampaignFspCobordismIntrinsicSign.arf_gaussian_sign_sum_dichotomy` |
| `CampaignFspCobordismIntrinsicSign.basis_change_removes_sign_outside_constrained_class_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspCobordismIntrinsicSign.basis_change_removes_sign_outside_constrained_class_fence` |
| `CampaignFspCobordismIntrinsicSign.five_d_bulk_inflow_cancels_boundary_anomaly_sign` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspCobordismIntrinsicSign.five_d_bulk_inflow_cancels_boundary_anomaly_sign` |
| `CampaignFspCobordismIntrinsicSign.mapping_torus_fermion_det_sign_reversal` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspCobordismIntrinsicSign.mapping_torus_fermion_det_sign_reversal` |
| `CampaignFspCobordismIntrinsicSign.pin_minus_z16_order_sixteen_fence` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFspCobordismIntrinsicSign.pin_minus_z16_order_sixteen_fence` |
| `CampaignFspCobordismIntrinsicSign.single_eigenvalue_crossing_eta_jump_by_two` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFspCobordismIntrinsicSign.single_eigenvalue_crossing_eta_jump_by_two` |
| `CampaignFspCobordismIntrinsicSign.spectralSign_odd_and_symmetric_pair_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspCobordismIntrinsicSign.spectralSign_odd_and_symmetric_pair_zero` |
| `CampaignFspCobordismIntrinsicSign.thermal_orientation_weight_asymmetry_fence` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFspCobordismIntrinsicSign.thermal_orientation_weight_asymmetry_fence` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1211_fsp_cobordism_intrinsic_sign.md`

- file: [dag/derivations/26_fsp/tfq_1211_fsp_cobordism_intrinsic_sign.md](../../../dag/derivations/26_fsp/tfq_1211_fsp_cobordism_intrinsic_sign.md)
- sha256 (`lf-normalised`): `05dea286393b8e86770ef9a8209182d1ea77d765c04549a2a57b6baf5084c5a1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1211
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-cobordism-intrinsic-sign.md`

- file: [dag/derivations/independent/fsp-cobordism-intrinsic-sign.md](../../../dag/derivations/independent/fsp-cobordism-intrinsic-sign.md)
- sha256 (`lf-normalised`): `467544e03924762c90c9369d433975493eaa059b38b3240debc62192d98c5e1c`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-cobordism-intrinsic-sign_independent.json`

- file: [dag/research/campaign_fsp-cobordism-intrinsic-sign_independent.json](../../../dag/research/campaign_fsp-cobordism-intrinsic-sign_independent.json)
- sha256 (`lf-normalised`): `bd260c8ae136f0f37e7fd9e207c5c34ab231104aa87df3ff1c21ca517d7f0359`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-cobordism-intrinsic-sign_lean_mutation.json`

- file: [dag/research/campaign_fsp-cobordism-intrinsic-sign_lean_mutation.json](../../../dag/research/campaign_fsp-cobordism-intrinsic-sign_lean_mutation.json)
- sha256 (`lf-normalised`): `d05bf4fe305d0b4a7afb09ba108a08ab018b9a7da64b2fafbd52df2b81bdbd9d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-cobordism-intrinsic-sign_lean_replay.json`

- file: [dag/research/campaign_fsp-cobordism-intrinsic-sign_lean_replay.json](../../../dag/research/campaign_fsp-cobordism-intrinsic-sign_lean_replay.json)
- sha256 (`lf-normalised`): `88fa85403ae08127c5a6e3dbd8e06ef2ffe26ebcb4051e4d0603fafde46a6c27`
- cited in: node.source
- counts toward the grade: yes

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
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-COBORDISM-INTRINSIC-SIGN` `GAP_NO_DERIVATION`: [FSP-BF-2GROUP-SIGN-CLAIM](FSP-BF-2GROUP-SIGN-CLAIM.md) (OPEN)

Outgoing (2):

- `APP-R-FSP-MASTER-DICHOTOMY-REFUTED` `DERIVED_PROSE`: [FSP-MASTER-DICHOTOMY-REFUTED](FSP-MASTER-DICHOTOMY-REFUTED.md) (REFUTED)
- `APP-R-FSP-REGGE-DEFICIT-ACTION` `CONDITIONAL_ON_IMPORT`: [FSP-REGGE-DEFICIT-ACTION](FSP-REGGE-DEFICIT-ACTION.md) (IMPORTED_ASSUMPTION)
