# DFM-GRIBOV-CONTINUUM-FENCE

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For the rational matrices I = diag(1, 1, 1), Omega1 = diag(1, -1, -1), H23 with ones in positions (2, 3) and (3, 2), and H12 with ones in positions (1, 2) and (2, 1), H23^2 = diag(0, 1, 1), H12^2 = diag(1, 1, 0), Omega1^2 = I, the product of Omega1's diagonal entries is 1, Tr(I) = 3, Tr(Omega1) = -1, Tr(I H23^2) = 2, Tr(Omega1 H23^2) = -2, and Tr(Omega1 H12^2) = 0, so those two Omega1 forms differ. Continuum Gribov-Singer, a Faddeev-Popov operator spectrum, ghost-free quantization, and a Yang-Mills mass gap stay unproved.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 10
- cited Lean declarations covered by a current replay receipt: 10
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- continuum Yang-Mills theory
- Faddeev-Popov quantization

## Bottleneck

The recorded comparison is this pair of quadratic forms on two generators of one diagonal matrix. A refinement family of lattices, an operator spectrum, and a limit theorem stay open before any continuum transport.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.8-FENCE claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignDfmGribovContinuumFence.lean`

- file: [lean4/CampaignDfmGribovContinuumFence.lean](../../../lean4/CampaignDfmGribovContinuumFence.lean)
- sha256 (`bytes`): `705525af66b273006ad1d0cd2418242640d8ffd5102be3169e74e6688e12d8a6`
- cited in: node.lean, node.source, receipt dag/research/campaign_dfm-gribov-continuum-fence_lean_replay.json (CampaignDfmGribovContinuumFence), record TFQ-1132
- replay: `verified`
  - receipt [dag/research/campaign_dfm-gribov-continuum-fence_lean_replay.json](../../../dag/research/campaign_dfm-gribov-continuum-fence_lean_replay.json) (module `CampaignDfmGribovContinuumFence`): recorded sha256 `705525af66b273006ad1d0cd2418242640d8ffd5102be3169e74e6688e12d8a6` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignDfmGribovContinuumFence`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignDfmGribovContinuumFence.forms_differ` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmGribovContinuumFence.forms_differ` |
| `CampaignDfmGribovContinuumFence.h12_square` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmGribovContinuumFence.h12_square` |
| `CampaignDfmGribovContinuumFence.h23_square` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmGribovContinuumFence.h23_square` |
| `CampaignDfmGribovContinuumFence.omega1_square_and_det` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmGribovContinuumFence.omega1_square_and_det` |
| `CampaignDfmGribovContinuumFence.trace_pair` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmGribovContinuumFence.trace_pair` |
| `forms_differ` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms forms_differ` |
| `h12_square` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms h12_square` |
| `h23_square` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms h23_square` |
| `omega1_square_and_det` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms omega1_square_and_det` |
| `trace_pair` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms trace_pair` |
- counts toward the grade: yes

### Python: `checks/independent/dfm-gribov-continuum-fence.py`

- file: [checks/independent/dfm-gribov-continuum-fence.py](../../../checks/independent/dfm-gribov-continuum-fence.py)
- sha256 (`bytes`): `b2a5328cbb201230cb6d2fa5d3eb58cd1f357cfffe41924076671da06a9286bb`
- cited in: node.source, record TFQ-1132
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1132_dfm_gribov_continuum_fence.md`

- file: [dag/derivations/24_dressing_field/tfq_1132_dfm_gribov_continuum_fence.md](../../../dag/derivations/24_dressing_field/tfq_1132_dfm_gribov_continuum_fence.md)
- sha256 (`lf-normalised`): `0dea892a3f36320cefc16fcd10b1886c568f69ec83e44fc22e890d77c526d952`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1132
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/dfm-gribov-continuum-fence.md`

- file: [dag/derivations/independent/dfm-gribov-continuum-fence.md](../../../dag/derivations/independent/dfm-gribov-continuum-fence.md)
- sha256 (`lf-normalised`): `30efabc8fefb717e838a46d81cda47c89f27a736091363d49e8ed36675fac79e`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-GRIBOV-CONTINUUM-FENCE` `GAP_NO_DERIVATION`: [DFM-SU3-GRIBOV-COPIES-DIAMOND](DFM-SU3-GRIBOV-COPIES-DIAMOND.md) (COMPUTATIONALLY_CHECKED), [DFM-CONTINUUM-INTERFACE](DFM-CONTINUUM-INTERFACE.md) (OPEN)

Outgoing (0):

