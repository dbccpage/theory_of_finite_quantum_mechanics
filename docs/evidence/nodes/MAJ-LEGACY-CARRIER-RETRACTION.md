# MAJ-LEGACY-CARRIER-RETRACTION

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Given the recorded measurement that legacy tetron_carrier.py had dim H1 = 0 at T = 1..4, every closed residual on it was Exact, so its results support no statement about logical sectors and are superseded by the tetron-array family.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 16
- distinct cited Lean declarations covered by a current replay receipt: 14
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The checked slice is the identity coboundary on functions Fin t to Bool: d1 after d0 is the zero function on one coordinate, every 1-cochain is exact, and none is a closed residual, including the sizes t = 1, 2, 3 and 4. The recorded measurement that tetron_carrier.py had dim H1 = 0 at those sizes is not in this checkout. A logical-sector reading of that missing file, and a comparison with the tetron-array family, stay open. The older citation legacy_carrier_obstruction assumes trivial first cohomology and does not discharge this slice.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-C13 claims PROVED_LEAN; audited status CONDITIONAL

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/MajoranaLegacyCarrierRetraction.lean`

- file: [lean4/MajoranaLegacyCarrierRetraction.lean](../../../lean4/MajoranaLegacyCarrierRetraction.lean)
- sha256 (`bytes`): `81a3d3bef75c8550de5174c37588eb346cbd705557e3bcb480023a7b3148cc06`
- cited in: node.lean, receipt dag/research/campaign_maj-legacy-carrier-retraction_lean_replay.json (MajoranaLegacyCarrierRetraction), receipt dag/research/pr_382_round2_replay.json (MajoranaLegacyCarrierRetraction), record TFQ-1154
- replay: `verified`
  - receipt [dag/research/campaign_maj-legacy-carrier-retraction_lean_replay.json](../../../dag/research/campaign_maj-legacy-carrier-retraction_lean_replay.json) (module `MajoranaLegacyCarrierRetraction`): recorded sha256 `81a3d3bef75c8550de5174c37588eb346cbd705557e3bcb480023a7b3148cc06` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/pr_382_round2_replay.json](../../../dag/research/pr_382_round2_replay.json) (module `MajoranaLegacyCarrierRetraction`): recorded sha256 `81a3d3bef75c8550de5174c37588eb346cbd705557e3bcb480023a7b3148cc06` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build MajoranaLegacyCarrierRetraction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `MajoranaLegacyCarrierRetraction.V` | yes | yes | yes | none | `#print axioms MajoranaLegacyCarrierRetraction.V` |
| `MajoranaLegacyCarrierRetraction.all_cocycle` | yes | yes | yes | none | `#print axioms MajoranaLegacyCarrierRetraction.all_cocycle` |
| `MajoranaLegacyCarrierRetraction.all_exact` | yes | yes | yes | none | `#print axioms MajoranaLegacyCarrierRetraction.all_exact` |
| `MajoranaLegacyCarrierRetraction.d0` | yes | yes | yes | none | `#print axioms MajoranaLegacyCarrierRetraction.d0` |
| `MajoranaLegacyCarrierRetraction.d0_id` | yes | yes | yes | none | `#print axioms MajoranaLegacyCarrierRetraction.d0_id` |
| `MajoranaLegacyCarrierRetraction.d1` | yes | yes | yes | none | `#print axioms MajoranaLegacyCarrierRetraction.d1` |
| `MajoranaLegacyCarrierRetraction.isClosed` | yes | yes | yes | none | `#print axioms MajoranaLegacyCarrierRetraction.isClosed` |
| `MajoranaLegacyCarrierRetraction.isCocycle` | yes | yes | yes | none | `#print axioms MajoranaLegacyCarrierRetraction.isCocycle` |
| `MajoranaLegacyCarrierRetraction.isExact` | yes | yes | yes | none | `#print axioms MajoranaLegacyCarrierRetraction.isExact` |
| `MajoranaLegacyCarrierRetraction.nilpotent` | yes | yes | yes | none | `#print axioms MajoranaLegacyCarrierRetraction.nilpotent` |
| `MajoranaLegacyCarrierRetraction.no_closed` | yes | yes | yes | none | `#print axioms MajoranaLegacyCarrierRetraction.no_closed` |
| `MajoranaLegacyCarrierRetraction.window_no_closed` | yes | yes | yes | none | `#print axioms MajoranaLegacyCarrierRetraction.window_no_closed` |
| `MajoranaLegacyCarrierRetraction.zero1` | yes | yes | yes | none | `#print axioms MajoranaLegacyCarrierRetraction.zero1` |

- counts toward the grade: yes

### Lean: `papers/core/majorana/lean4/MajoranaCore.lean`

- file: [papers/core/majorana/lean4/MajoranaCore.lean](../../../papers/core/majorana/lean4/MajoranaCore.lean)
- sha256 (`bytes`): `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071`
- cited in: node.lean, record TFQ-1154
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_majorana.json](../../../dag/research/lean_replay_campaign_majorana.json) (module `papers.core.majorana.lean4.MajoranaCore`): recorded sha256 `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `legacy_carrier_obstruction` | yes | yes | yes | none | `#print axioms legacy_carrier_obstruction` |

- counts toward the grade: yes

### Python: `code/python/src/majorana/majorana_mzm_ising.py`

- file: [code/python/src/majorana/majorana_mzm_ising.py](../../../code/python/src/majorana/majorana_mzm_ising.py)
- sha256 (`bytes`): `a4ac5734a5ab1a872aeaafd3835ed71261f069dfb29c17c9b5572a03e63b1310`
- cited in: record TFQ-1154

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `audit_legacy_carrier` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/src/majorana/test_tetron_surface_codes.py`

- file: [code/python/src/majorana/test_tetron_surface_codes.py](../../../code/python/src/majorana/test_tetron_surface_codes.py)
- sha256 (`bytes`): `6577a59d6a74b23a3f5a356b1ffaf308140451939f7541f472ac0de58bf6747e`
- cited in: record TFQ-1154
- check: `python -m pytest code/python/src/majorana/test_tetron_surface_codes.py::test_audit_legacy_carrier_retraction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_audit_legacy_carrier_retraction` (python_test) | yes | yes | yes | - | `python -m pytest code/python/src/majorana/test_tetron_surface_codes.py::test_audit_legacy_carrier_retraction` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1154_maj_legacy_carrier_retraction.md`

- file: [dag/derivations/28_majorana/tfq_1154_maj_legacy_carrier_retraction.md](../../../dag/derivations/28_majorana/tfq_1154_maj_legacy_carrier_retraction.md)
- sha256 (`lf-normalised`): `1d63d0acf863861711578ae65d0c4e0cd96bcbd506252232712f22dd94fab63b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1154
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `2f55c0f24f87388cfa9d7a4a7d832f34c0fa30b857d344811f4336f634c1684b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/majorana/the_majorana_problem_change_log.md`

- file: [papers/core/majorana/the_majorana_problem_change_log.md](../../../papers/core/majorana/the_majorana_problem_change_log.md)
- sha256 (`lf-normalised`): `4592b207071a2c05f46a6ffdd890a2332f957a7e6b805e9aa6c6988e451e9fa8`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/majorana/the_majorana_problem_claim_ledger.md`

- file: [papers/core/majorana/the_majorana_problem_claim_ledger.md](../../../papers/core/majorana/the_majorana_problem_claim_ledger.md)
- sha256 (`lf-normalised`): `37cc191a881cbb0f8fb52e30c2b865f9e9e70e235b4530df7bdd7d1b5728cb86`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-LEGACY-CARRIER-RETRACTION` `CONDITIONAL_ON_IMPORT`: [MAJ-TRIVIAL-H1-NO-CLOSED](MAJ-TRIVIAL-H1-NO-CLOSED.md) (PROVED_LEAN), [MAJ-TETRON-ARRAY-CARRIER](MAJ-TETRON-ARRAY-CARRIER.md) (DEFINITION)

Outgoing (0):

