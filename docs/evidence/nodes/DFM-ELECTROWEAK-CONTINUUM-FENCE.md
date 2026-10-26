# DFM-ELECTROWEAK-CONTINUUM-FENCE

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The residual U(1)_Y covariance u(e^{i alpha/2} Phi) = u(Phi) diag(e^{-i alpha/2}, e^{i alpha/2}), the dressed gauge field with derivative term, and the reading as an electroweak model without spontaneous symmetry breaking are not established by the finite artifacts.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 26
- distinct cited Lean declarations covered by a current replay receipt: 22
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
- sha256 (`bytes`): `4c8ff3cf3c8bb851b02f6bd248b2c19793357cf71d4cbbdcb611f7d84f116dd0`
- cited in: node.source, record TFQ-1122
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1122_dfm_electroweak_continuum_fence.md`

- file: [dag/derivations/24_dressing_field/tfq_1122_dfm_electroweak_continuum_fence.md](../../../dag/derivations/24_dressing_field/tfq_1122_dfm_electroweak_continuum_fence.md)
- sha256 (`lf-normalised`): `bf7266db5f9206624ae2cb2fdeba59df18eed04a37862c537faa423f9b415ec4`
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
