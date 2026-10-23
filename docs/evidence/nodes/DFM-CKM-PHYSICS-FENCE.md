# DFM-CKM-PHYSICS-FENCE

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For every rational n, (n - 1)^2 - n(n - 1)/2 = (n - 1)(n - 2)/2 and (n - 1)(n - 2)/2 + (n - 1) = n(n - 1)/2. At n = 1, 2, 3, 4 the first expression is 0, 1, 4, 9 and the CP expression is 0, 0, 1, 3; they agree at n = 1 and differ at n = 2, 3, 4. At n = 3 the three values are 4, 3, and 1. The quartet of four ones in Q(i) has imaginary part 0, and the quartet with second factor i has imaginary part 1, so the CP value 1 matches only the second. Derivation of a mixing matrix from Yukawa couplings, a unitarity identification of these counts, and measured CP values stay unproved.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 24
- cited Lean declarations covered by a current replay receipt: 24
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Yukawa couplings and mass-basis diagonalization
- measured CKM parameters

## Bottleneck

The recorded gap is the rational relation among the three counting expressions and the two quartet imaginary parts 0 and 1. Yukawa couplings, mass-basis diagonalization, a unitarity identification, and measured CKM values stay open.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.7-FENCE claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignDfmCkmPhysicsFence.lean`

- file: [lean4/CampaignDfmCkmPhysicsFence.lean](../../../lean4/CampaignDfmCkmPhysicsFence.lean)
- sha256 (`bytes`): `48b09120433b79ced896d35224010a77af3d755517b0e2177662be0c86d78963`
- cited in: node.lean, node.source, receipt dag/research/campaign_dfm-ckm-physics-fence_lean_replay.json (CampaignDfmCkmPhysicsFence), record TFQ-1128
- replay: `verified`
  - receipt [dag/research/campaign_dfm-ckm-physics-fence_lean_replay.json](../../../dag/research/campaign_dfm-ckm-physics-fence_lean_replay.json) (module `CampaignDfmCkmPhysicsFence`): recorded sha256 `48b09120433b79ced896d35224010a77af3d755517b0e2177662be0c86d78963` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignDfmCkmPhysicsFence`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignDfmCkmPhysicsFence.Rephasing.act_compose` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignDfmCkmPhysicsFence.Rephasing.act_compose` |
| `CampaignDfmCkmPhysicsFence.Rephasing.act_inverse` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignDfmCkmPhysicsFence.Rephasing.act_inverse` |
| `CampaignDfmCkmPhysicsFence.Rephasing.checkedLabel_none_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmCkmPhysicsFence.Rephasing.checkedLabel_none_iff` |
| `CampaignDfmCkmPhysicsFence.Rephasing.checkedLabel_value` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmCkmPhysicsFence.Rephasing.checkedLabel_value` |
| `CampaignDfmCkmPhysicsFence.Rephasing.coordinatesEquiv` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignDfmCkmPhysicsFence.Rephasing.coordinatesEquiv` |
| `CampaignDfmCkmPhysicsFence.Rephasing.decideRelated_correct` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmCkmPhysicsFence.Rephasing.decideRelated_correct` |
| `CampaignDfmCkmPhysicsFence.Rephasing.free_coordinate_count` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmCkmPhysicsFence.Rephasing.free_coordinate_count` |
| `CampaignDfmCkmPhysicsFence.Rephasing.normalize_boundary` | yes | yes | yes | propext | `#print axioms CampaignDfmCkmPhysicsFence.Rephasing.normalize_boundary` |
| `CampaignDfmCkmPhysicsFence.Rephasing.normalize_idempotent` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignDfmCkmPhysicsFence.Rephasing.normalize_idempotent` |
| `CampaignDfmCkmPhysicsFence.Rephasing.normalize_invariant` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignDfmCkmPhysicsFence.Rephasing.normalize_invariant` |
| `CampaignDfmCkmPhysicsFence.Rephasing.related_iff_normalize` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignDfmCkmPhysicsFence.Rephasing.related_iff_normalize` |
| `CampaignDfmCkmPhysicsFence.constraintCount_sum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmCkmPhysicsFence.constraintCount_sum` |
| `CampaignDfmCkmPhysicsFence.count_misses_one_quartet` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmCkmPhysicsFence.count_misses_one_quartet` |
| `CampaignDfmCkmPhysicsFence.count_table` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmCkmPhysicsFence.count_table` |
| `CampaignDfmCkmPhysicsFence.cpCount_from_difference` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmCkmPhysicsFence.cpCount_from_difference` |
| `CampaignDfmCkmPhysicsFence.quartet_imag_value` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmCkmPhysicsFence.quartet_imag_value` |
| `CampaignDfmCkmPhysicsFence.quartet_real_value` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmCkmPhysicsFence.quartet_real_value` |
| `CampaignDfmCkmPhysicsFence.quartets_differ` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmCkmPhysicsFence.quartets_differ` |
| `CampaignDfmCkmPhysicsFence.three_generation_split` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmCkmPhysicsFence.three_generation_split` |
| `constraintCount_sum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms constraintCount_sum` |
| `count_misses_one_quartet` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms count_misses_one_quartet` |
| `count_table` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms count_table` |
| `cpCount_from_difference` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms cpCount_from_difference` |
| `three_generation_split` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms three_generation_split` |
- counts toward the grade: yes

### Python: `checks/independent/dfm-ckm-physics-fence.py`

- file: [checks/independent/dfm-ckm-physics-fence.py](../../../checks/independent/dfm-ckm-physics-fence.py)
- sha256 (`bytes`): `c892785ddff595611d83acaade1166e5d755e00a42d84104d60fdad3b793c48b`
- cited in: node.source, record TFQ-1128
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1128_dfm_ckm_physics_fence.md`

- file: [dag/derivations/24_dressing_field/tfq_1128_dfm_ckm_physics_fence.md](../../../dag/derivations/24_dressing_field/tfq_1128_dfm_ckm_physics_fence.md)
- sha256 (`lf-normalised`): `4442d43bff78dfd330e869e2ea5ee576a25c49cc832150755141dd0247cc480b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1128
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/dfm-ckm-physics-fence.md`

- file: [dag/derivations/independent/dfm-ckm-physics-fence.md](../../../dag/derivations/independent/dfm-ckm-physics-fence.md)
- sha256 (`lf-normalised`): `d6ff942e33e8ff1b0477bc606a4ffe76e3bd6adabd1cdb604a08f3bb80057769`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-CKM-PHYSICS-FENCE` `GAP_NO_DERIVATION`: [DFM-JARLSKOG-PYTHAGOREAN-WITNESS](DFM-JARLSKOG-PYTHAGOREAN-WITNESS.md) (COMPUTATIONALLY_CHECKED), [DFM-ELECTROWEAK-CONTINUUM-FENCE](DFM-ELECTROWEAK-CONTINUUM-FENCE.md) (OPEN)

Outgoing (0):

