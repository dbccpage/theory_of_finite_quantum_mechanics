# DFM-CKM-PHYSICS-FENCE

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For every rational n, (n - 1)^2 - n(n - 1)/2 = (n - 1)(n - 2)/2 and (n - 1)(n - 2)/2 + (n - 1) = n(n - 1)/2. At n = 1, 2, 3, 4 the first expression is 0, 1, 4, 9 and the CP expression is 0, 0, 1, 3; they agree at n = 1 and differ at n = 2, 3, 4. At n = 3 the three values are 4, 3, and 1. The quartet of four ones in Q(i) has imaginary part 0, and the quartet with second factor i has imaginary part 1, so the CP value 1 matches only the second. Derivation of a mixing matrix from Yukawa couplings, a unitarity identification of these counts, and measured CP values stay unproved.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 13
- cited Lean declarations covered by a current replay receipt: 13
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
- sha256 (`bytes`): `6cf59912891b90b93acc025f4b153d623873abe7c1e3f45824a977f306f741df`
- cited in: node.lean, node.source, receipt dag/research/campaign_dfm-ckm-physics-fence_lean_replay.json (CampaignDfmCkmPhysicsFence), record TFQ-1128
- replay: `verified`
  - receipt [dag/research/campaign_dfm-ckm-physics-fence_lean_replay.json](../../../dag/research/campaign_dfm-ckm-physics-fence_lean_replay.json) (module `CampaignDfmCkmPhysicsFence`): recorded sha256 `6cf59912891b90b93acc025f4b153d623873abe7c1e3f45824a977f306f741df` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignDfmCkmPhysicsFence`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
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
- sha256 (`bytes`): `ea9c4a2309a3183e96ba1f240a3f81502e831aba59043e32722faa8abad6b18f`
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
- sha256 (`lf-normalised`): `9d305b8aaef8ff7808d63b1b08f08526f22ab2918267de1de1e8a647283790a4`
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

