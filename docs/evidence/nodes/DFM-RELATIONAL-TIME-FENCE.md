# DFM-RELATIONAL-TIME-FENCE

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For U = \[\[0, -1\], \[1, 0\]\] over Q, U^2 = -I, U^4 = I, and U^T U = I. For each t in {0, 1, 2, 3}, (U^{t+1})^T U U^t = I. For psi = (3/5, 4/5), psi·psi = 1 and (U^t)^T (U^t psi) = psi for each such t, while the first components of U psi and of U^2 psi differ from 3/5. A continuous-time reading, a Stone generator, and a Wheeler-DeWitt constraint stay unproved. For a supplied group-valued schedule, cumulative transport conjugates under frame change, and a periodic frame cancels all edges iff total transport is identity. Normalized cycle blocks are identity on interior edges and total transport on the closing edge. A checked positive-period constructor returns a closure certificate or a distinct zero-period/nonclosure error. Supplied group actions admit an invertible change of history coordinates preserving the evolution law.

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

- continuous time and Stone generator
- Hamiltonian constraint of a physical theory

## Bottleneck

The group, links, action, step and vector are supplied. General finite-cycle transport and its closure criterion are established for these inputs; deriving them from primitive difference, continuous time, a one-parameter unitary group and a Hamiltonian constraint stay open.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.5-FENCE claims COMPUTATIONALLY_CHECKED; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignDfmRelationalTimeFence.lean`

- file: [lean4/CampaignDfmRelationalTimeFence.lean](../../../lean4/CampaignDfmRelationalTimeFence.lean)
- sha256 (`bytes`): `925ab7156f2b9b115b7579b723af0573327434e4111f56a9ac677d62be591e98`
- cited in: node.lean, node.source, receipt dag/research/campaign_dfm-relational-time-fence_lean_replay.json (CampaignDfmRelationalTimeFence), record TFQ-1117
- replay: `verified`
  - receipt [dag/research/campaign_dfm-relational-time-fence_lean_replay.json](../../../dag/research/campaign_dfm-relational-time-fence_lean_replay.json) (module `CampaignDfmRelationalTimeFence`): recorded sha256 `925ab7156f2b9b115b7579b723af0573327434e4111f56a9ac677d62be591e98` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignDfmRelationalTimeFence`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignDfmRelationalTimeFence.Clock.ClosedCycle.blocks` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignDfmRelationalTimeFence.Clock.ClosedCycle.blocks` |
| `CampaignDfmRelationalTimeFence.Clock.cycleBlock_normal_form` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignDfmRelationalTimeFence.Clock.cycleBlock_normal_form` |
| `CampaignDfmRelationalTimeFence.Clock.evolves_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignDfmRelationalTimeFence.Clock.evolves_iff` |
| `CampaignDfmRelationalTimeFence.Clock.frame_constant` | yes | yes | yes | propext | `#print axioms CampaignDfmRelationalTimeFence.Clock.frame_constant` |
| `CampaignDfmRelationalTimeFence.Clock.frame_dress` | yes | yes | yes | propext | `#print axioms CampaignDfmRelationalTimeFence.Clock.frame_dress` |
| `CampaignDfmRelationalTimeFence.Clock.interior` | yes | yes | yes | propext | `#print axioms CampaignDfmRelationalTimeFence.Clock.interior` |
| `CampaignDfmRelationalTimeFence.Clock.periodic_trivialization_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignDfmRelationalTimeFence.Clock.periodic_trivialization_iff` |
| `CampaignDfmRelationalTimeFence.Clock.seam_eq` | yes | yes | yes | propext | `#print axioms CampaignDfmRelationalTimeFence.Clock.seam_eq` |
| `CampaignDfmRelationalTimeFence.Clock.stationary_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignDfmRelationalTimeFence.Clock.stationary_iff` |
| `CampaignDfmRelationalTimeFence.Clock.trivial_iff_recurrence` | yes | yes | yes | propext | `#print axioms CampaignDfmRelationalTimeFence.Clock.trivial_iff_recurrence` |
| `CampaignDfmRelationalTimeFence.Clock.validate_nonclosing` | yes | yes | yes | propext | `#print axioms CampaignDfmRelationalTimeFence.Clock.validate_nonclosing` |
| `CampaignDfmRelationalTimeFence.Clock.validate_period` | yes | yes | yes | propext | `#print axioms CampaignDfmRelationalTimeFence.Clock.validate_period` |
| `CampaignDfmRelationalTimeFence.Clock.validate_roundtrip` | yes | yes | yes | propext | `#print axioms CampaignDfmRelationalTimeFence.Clock.validate_roundtrip` |
| `CampaignDfmRelationalTimeFence.Clock.validate_success_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignDfmRelationalTimeFence.Clock.validate_success_iff` |
| `CampaignDfmRelationalTimeFence.Clock.validate_zero` | yes | yes | yes | propext | `#print axioms CampaignDfmRelationalTimeFence.Clock.validate_zero` |
| `CampaignDfmRelationalTimeFence.four_blocks` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmRelationalTimeFence.four_blocks` |
| `CampaignDfmRelationalTimeFence.psi_recover` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmRelationalTimeFence.psi_recover` |
| `CampaignDfmRelationalTimeFence.rationalClock_blocks` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmRelationalTimeFence.rationalClock_blocks` |
| `CampaignDfmRelationalTimeFence.rotation_apply` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmRelationalTimeFence.rotation_apply` |
| `CampaignDfmRelationalTimeFence.rotation_four` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmRelationalTimeFence.rotation_four` |
| `CampaignDfmRelationalTimeFence.step_square_and_order` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmRelationalTimeFence.step_square_and_order` |
| `four_blocks` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms four_blocks` |
| `psi_recover` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms psi_recover` |
| `step_square_and_order` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms step_square_and_order` |
- counts toward the grade: yes

### Python: `checks/independent/dfm-relational-time-fence.py`

- file: [checks/independent/dfm-relational-time-fence.py](../../../checks/independent/dfm-relational-time-fence.py)
- sha256 (`bytes`): `b959e5e2567577710cf96d6d7e0cdfec57424675e2a04157a8736c0f93d60199`
- cited in: node.source, record TFQ-1117
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1117_dfm_relational_time_fence.md`

- file: [dag/derivations/24_dressing_field/tfq_1117_dfm_relational_time_fence.md](../../../dag/derivations/24_dressing_field/tfq_1117_dfm_relational_time_fence.md)
- sha256 (`lf-normalised`): `c808b5a4cdc8116fb930621910e47ae5cd9495cae51d0e2591713385fdfa957a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1117
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/dfm-relational-time-fence.md`

- file: [dag/derivations/independent/dfm-relational-time-fence.md](../../../dag/derivations/independent/dfm-relational-time-fence.md)
- sha256 (`lf-normalised`): `d59c1e15c357dff66b7db5beb0bef95b9b4642542904cf32f3477c68299a3229`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-RELATIONAL-TIME-FENCE` `GAP_NO_DERIVATION`: [DFM-CLOCK-DRESSING-INTERTWINER](DFM-CLOCK-DRESSING-INTERTWINER.md) (PROVED_PROSE), [DFM-CONTINUUM-INTERFACE](DFM-CONTINUUM-INTERFACE.md) (OPEN)

Outgoing (0):

