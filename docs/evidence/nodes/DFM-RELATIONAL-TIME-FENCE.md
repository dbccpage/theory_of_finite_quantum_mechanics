# DFM-RELATIONAL-TIME-FENCE

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reading the finite clock-dressed history as emergent time evolution for a reparameterization-invariant physical system, or as a Wheeler-DeWitt constraint, is outside the finite intertwining identity.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 24
- distinct cited Lean declarations covered by a current replay receipt: 21
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- continuous time and Stone generator
- Hamiltonian constraint of a physical theory
- group-valued schedule and group action

## Bottleneck

The group, links, action, step and vector are supplied. General finite-cycle transport and its closure criterion are established for these inputs; deriving them from primitive difference, continuous time, a one-parameter unitary group and a Hamiltonian constraint stay open.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.5-FENCE claims COMPUTATIONALLY_CHECKED; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DressingFieldRelationalTimeFence.lean`

- file: [lean4/DressingFieldRelationalTimeFence.lean](../../../lean4/DressingFieldRelationalTimeFence.lean)
- sha256 (`bytes`): `0a6ce2dcad77e401ace44109d9fa453443e03a418e10d79915181ad9dd1833d5`
- cited in: node.lean, node.source, receipt dag/research/campaign_dfm-relational-time-fence_lean_replay.json (DressingFieldRelationalTimeFence), record TFQ-1117
- replay: `verified`
  - receipt [dag/research/campaign_dfm-relational-time-fence_lean_replay.json](../../../dag/research/campaign_dfm-relational-time-fence_lean_replay.json) (module `DressingFieldRelationalTimeFence`): recorded sha256 `0a6ce2dcad77e401ace44109d9fa453443e03a418e10d79915181ad9dd1833d5` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DressingFieldRelationalTimeFence`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `DressingFieldRelationalTimeFence.Clock.ClosedCycle.blocks` | yes | yes | yes | Quot.sound, propext | `#print axioms DressingFieldRelationalTimeFence.Clock.ClosedCycle.blocks` |
| `DressingFieldRelationalTimeFence.Clock.cycleBlock_normal_form` | yes | yes | yes | Quot.sound, propext | `#print axioms DressingFieldRelationalTimeFence.Clock.cycleBlock_normal_form` |
| `DressingFieldRelationalTimeFence.Clock.evolves_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms DressingFieldRelationalTimeFence.Clock.evolves_iff` |
| `DressingFieldRelationalTimeFence.Clock.frame_constant` | yes | yes | yes | propext | `#print axioms DressingFieldRelationalTimeFence.Clock.frame_constant` |
| `DressingFieldRelationalTimeFence.Clock.frame_dress` | yes | yes | yes | propext | `#print axioms DressingFieldRelationalTimeFence.Clock.frame_dress` |
| `DressingFieldRelationalTimeFence.Clock.interior` | yes | yes | yes | propext | `#print axioms DressingFieldRelationalTimeFence.Clock.interior` |
| `DressingFieldRelationalTimeFence.Clock.periodic_trivialization_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms DressingFieldRelationalTimeFence.Clock.periodic_trivialization_iff` |
| `DressingFieldRelationalTimeFence.Clock.seam_eq` | yes | yes | yes | propext | `#print axioms DressingFieldRelationalTimeFence.Clock.seam_eq` |
| `DressingFieldRelationalTimeFence.Clock.stationary_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms DressingFieldRelationalTimeFence.Clock.stationary_iff` |
| `DressingFieldRelationalTimeFence.Clock.trivial_iff_recurrence` | yes | yes | yes | propext | `#print axioms DressingFieldRelationalTimeFence.Clock.trivial_iff_recurrence` |
| `DressingFieldRelationalTimeFence.Clock.validate_nonclosing` | yes | yes | yes | propext | `#print axioms DressingFieldRelationalTimeFence.Clock.validate_nonclosing` |
| `DressingFieldRelationalTimeFence.Clock.validate_period` | yes | yes | yes | propext | `#print axioms DressingFieldRelationalTimeFence.Clock.validate_period` |
| `DressingFieldRelationalTimeFence.Clock.validate_roundtrip` | yes | yes | yes | propext | `#print axioms DressingFieldRelationalTimeFence.Clock.validate_roundtrip` |
| `DressingFieldRelationalTimeFence.Clock.validate_success_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms DressingFieldRelationalTimeFence.Clock.validate_success_iff` |
| `DressingFieldRelationalTimeFence.Clock.validate_zero` | yes | yes | yes | propext | `#print axioms DressingFieldRelationalTimeFence.Clock.validate_zero` |
| `DressingFieldRelationalTimeFence.four_blocks` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldRelationalTimeFence.four_blocks` |
| `DressingFieldRelationalTimeFence.psi_recover` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldRelationalTimeFence.psi_recover` |
| `DressingFieldRelationalTimeFence.rationalClock_blocks` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldRelationalTimeFence.rationalClock_blocks` |
| `DressingFieldRelationalTimeFence.rotation_apply` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldRelationalTimeFence.rotation_apply` |
| `DressingFieldRelationalTimeFence.rotation_four` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldRelationalTimeFence.rotation_four` |
| `DressingFieldRelationalTimeFence.step_square_and_order` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldRelationalTimeFence.step_square_and_order` |
| `four_blocks` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms four_blocks` |
| `psi_recover` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms psi_recover` |
| `step_square_and_order` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms step_square_and_order` |

- counts toward the grade: yes

### Python: `checks/independent/dfm-relational-time-fence.py`

- file: [checks/independent/dfm-relational-time-fence.py](../../../checks/independent/dfm-relational-time-fence.py)
- sha256 (`bytes`): `cb011f2b1d9f811d83462d65b8540a2c5965abed525a5edda99e1c9a061f734c`
- cited in: node.source, record TFQ-1117
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1117_dfm_relational_time_fence.md`

- file: [dag/derivations/24_dressing_field/tfq_1117_dfm_relational_time_fence.md](../../../dag/derivations/24_dressing_field/tfq_1117_dfm_relational_time_fence.md)
- sha256 (`lf-normalised`): `71a3178c571abf14d03a20faf9fda5009da646d98e800b8300bb166d575cec91`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1117
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/dfm-relational-time-fence.md`

- file: [dag/derivations/independent/dfm-relational-time-fence.md](../../../dag/derivations/independent/dfm-relational-time-fence.md)
- sha256 (`lf-normalised`): `4a1a34f4e5afab64cf78f6304d256f8a244f23c856168122f483be15b5d83bae`
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

