# DFM-ELECTROWEAK-CONTINUUM-FENCE

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For every z in Q(i) and every doublet Phi in Q(i)^2, the un-normalized dressing U(Phi) = \[\[conj phi2, phi1\], \[-conj phi1, phi2\]\] satisfies U(z Phi) = U(Phi) diag(conj z, z). When the squared modulus of z is 1 and a rational s with s*s equal to the squared norm of Phi is supplied, dividing every entry by that same s preserves the identity and s*s equals the squared norm of z Phi. On Phi = (1, 0), the unit z = 3/5 + (4/5)i with s = 1 has normalized (1, 2) entry 3/5 + (4/5)i. On the same Phi, z = 2 has squared norms 1 and 4. The (1, 2) entry of U(2 Phi)/2 is 1, whereas the (1, 2) entry of (U(Phi)/1) diag(2, 2) is 2; these two sides of the proposed normalized covariance law differ. Continuum phases, the dressed derivative term, and an electroweak reading without a declared rational square root stay unproved.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 26
- cited Lean declarations covered by a current replay receipt: 26
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- continuum gauge fields W_mu and derivatives
- U(1)_Y phases outside Q(i)

## Bottleneck

The normalized residual law is recorded when z lies in Q(i), the squared modulus of z is 1, and a rational s with s*s equal to the doublet squared norm is supplied. Continuum gauge fields W_mu, derivatives, phases outside Q(i), and the Elitzur or symmetry-breaking reading stay open.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.6-FENCE claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignDfmElectroweakContinuumFence.lean`

- file: [lean4/CampaignDfmElectroweakContinuumFence.lean](../../../lean4/CampaignDfmElectroweakContinuumFence.lean)
- sha256 (`bytes`): `4e50c53a72e2404c2985a6af0b8c71b7a7a061e3f510e72ae3aad4c41f2d4ed2`
- cited in: node.lean, node.source, receipt dag/research/campaign_dfm-electroweak-continuum-fence_lean_replay.json (CampaignDfmElectroweakContinuumFence), record TFQ-1122
- replay: `verified`
  - receipt [dag/research/campaign_dfm-electroweak-continuum-fence_lean_replay.json](../../../dag/research/campaign_dfm-electroweak-continuum-fence_lean_replay.json) (module `CampaignDfmElectroweakContinuumFence`): recorded sha256 `4e50c53a72e2404c2985a6af0b8c71b7a7a061e3f510e72ae3aad4c41f2d4ed2` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignDfmElectroweakContinuumFence`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignDfmElectroweakContinuumFence.Dub.v2_scale` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmElectroweakContinuumFence.Dub.v2_scale` |
| `CampaignDfmElectroweakContinuumFence.GR.conj_mul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmElectroweakContinuumFence.GR.conj_mul` |
| `CampaignDfmElectroweakContinuumFence.GR.div_mul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmElectroweakContinuumFence.GR.div_mul` |
| `CampaignDfmElectroweakContinuumFence.GR.mul_comm` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmElectroweakContinuumFence.GR.mul_comm` |
| `CampaignDfmElectroweakContinuumFence.GR.negConj_mul_conj` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmElectroweakContinuumFence.GR.negConj_mul_conj` |
| `CampaignDfmElectroweakContinuumFence.GR.norm2_mul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmElectroweakContinuumFence.GR.norm2_mul` |
| `CampaignDfmElectroweakContinuumFence.Normalization.Input.act` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmElectroweakContinuumFence.Normalization.Input.act` |
| `CampaignDfmElectroweakContinuumFence.Normalization.Input.normalize` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmElectroweakContinuumFence.Normalization.Input.normalize` |
| `CampaignDfmElectroweakContinuumFence.Normalization.UnitPhase.act` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmElectroweakContinuumFence.Normalization.UnitPhase.act` |
| `CampaignDfmElectroweakContinuumFence.Normalization.UnitPhase.compose` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmElectroweakContinuumFence.Normalization.UnitPhase.compose` |
| `CampaignDfmElectroweakContinuumFence.Normalization.action_composes` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmElectroweakContinuumFence.Normalization.action_composes` |
| `CampaignDfmElectroweakContinuumFence.Normalization.check_accepts` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmElectroweakContinuumFence.Normalization.check_accepts` |
| `CampaignDfmElectroweakContinuumFence.Normalization.check_preserves` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmElectroweakContinuumFence.Normalization.check_preserves` |
| `CampaignDfmElectroweakContinuumFence.Normalization.check_success_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmElectroweakContinuumFence.Normalization.check_success_iff` |
| `CampaignDfmElectroweakContinuumFence.Normalization.matrix_covariant` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmElectroweakContinuumFence.Normalization.matrix_covariant` |
| `CampaignDfmElectroweakContinuumFence.Normalization.normalize_covariant` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmElectroweakContinuumFence.Normalization.normalize_covariant` |
| `CampaignDfmElectroweakContinuumFence.div_rightDiag` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmElectroweakContinuumFence.div_rightDiag` |
| `CampaignDfmElectroweakContinuumFence.nonunit_normalized_entries_differ` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmElectroweakContinuumFence.nonunit_normalized_entries_differ` |
| `CampaignDfmElectroweakContinuumFence.unit_normalized_covariance` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmElectroweakContinuumFence.unit_normalized_covariance` |
| `CampaignDfmElectroweakContinuumFence.unit_shares_norm` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmElectroweakContinuumFence.unit_shares_norm` |
| `CampaignDfmElectroweakContinuumFence.unnormalized_covariance` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmElectroweakContinuumFence.unnormalized_covariance` |
| `CampaignDfmElectroweakContinuumFence.witness_three_fifths` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmElectroweakContinuumFence.witness_three_fifths` |
| `nonunit_normalized_entries_differ` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms nonunit_normalized_entries_differ` |
| `unit_normalized_covariance` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms unit_normalized_covariance` |
| `unnormalized_covariance` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms unnormalized_covariance` |
| `witness_three_fifths` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms witness_three_fifths` |
- counts toward the grade: yes

### Python: `checks/independent/dfm-electroweak-continuum-fence.py`

- file: [checks/independent/dfm-electroweak-continuum-fence.py](../../../checks/independent/dfm-electroweak-continuum-fence.py)
- sha256 (`bytes`): `ba9e34421140761e26defe090e6cc202d7bd74eddc6d36ac47bf558fce18d4d2`
- cited in: node.source, record TFQ-1122
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1122_dfm_electroweak_continuum_fence.md`

- file: [dag/derivations/24_dressing_field/tfq_1122_dfm_electroweak_continuum_fence.md](../../../dag/derivations/24_dressing_field/tfq_1122_dfm_electroweak_continuum_fence.md)
- sha256 (`lf-normalised`): `15ae5f65d24e40eb7bb554fee828c55bde7d5f45e0406cfff0e67966d351530d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1122
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/dfm-electroweak-continuum-fence.md`

- file: [dag/derivations/independent/dfm-electroweak-continuum-fence.md](../../../dag/derivations/independent/dfm-electroweak-continuum-fence.md)
- sha256 (`lf-normalised`): `eccb2b3cb79458f9ccebeaaddf22c0d39170e92960593a54095ba197a67ce174`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-ELECTROWEAK-CONTINUUM-FENCE` `GAP_NO_DERIVATION`: [DFM-EW-DOUBLET-REDUCTION](DFM-EW-DOUBLET-REDUCTION.md) (PROVED_LEAN), [DFM-CONTINUUM-INTERFACE](DFM-CONTINUUM-INTERFACE.md) (OPEN)

Outgoing (1):

- `APP-R-DFM-CKM-PHYSICS-FENCE` `GAP_NO_DERIVATION`: [DFM-CKM-PHYSICS-FENCE](DFM-CKM-PHYSICS-FENCE.md) (OPEN)
