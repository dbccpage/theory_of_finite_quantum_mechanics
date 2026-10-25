# MAJ-LEGACY-CARRIER-RETRACTION

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For every natural number t, a 1-cochain is a function from Fin t to Bool. The coboundary d0 is the identity on those functions, and d1 sends each of them to the zero function Fin 1 to Bool. For every vertex function a, d1(d0(a)) equals that zero function. Every 1-cochain is a cocycle and is exact. A closed residual is a cocycle that is not exact, so no 1-cochain is a closed residual. In particular this holds for t = 1, t = 2, t = 3 and t = 4.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 9
- distinct cited Lean declarations covered by a current replay receipt: 7
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Standing text is the identity coboundary on functions Fin t to Bool: d1 after d0 is the zero function on one coordinate, every 1-cochain is exact, and none is a closed residual, including the sizes t = 1, 2, 3 and 4. The recorded measurement that tetron_carrier.py had dim H1 = 0 at those sizes is not in this checkout. A logical-sector reading of that missing file, and a comparison with the tetron-array family, stay open. The older citation legacy_carrier_obstruction assumes trivial first cohomology and does not discharge this slice.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-C13 claims PROVED_LEAN; audited status CONDITIONAL

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignMajLegacyCarrierRetraction.lean`

- file: [lean4/CampaignMajLegacyCarrierRetraction.lean](../../../lean4/CampaignMajLegacyCarrierRetraction.lean)
- sha256 (`bytes`): `36efdd4ee153a69c519b7e42ec12364ce21dff737faf0d5545b11efcf3eb76d9`
- cited in: node.lean, receipt dag/research/campaign_maj-legacy-carrier-retraction_lean_replay.json (CampaignMajLegacyCarrierRetraction), record TFQ-1154
- replay: `verified`
  - receipt [dag/research/campaign_maj-legacy-carrier-retraction_lean_replay.json](../../../dag/research/campaign_maj-legacy-carrier-retraction_lean_replay.json) (module `CampaignMajLegacyCarrierRetraction`): recorded sha256 `36efdd4ee153a69c519b7e42ec12364ce21dff737faf0d5545b11efcf3eb76d9` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignMajLegacyCarrierRetraction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `all_cocycle` | yes | yes | yes | none | `#print axioms all_cocycle` |
| `all_exact` | yes | yes | yes | none | `#print axioms all_exact` |
| `d0_id` | yes | yes | yes | none | `#print axioms d0_id` |
| `nilpotent` | yes | yes | yes | none | `#print axioms nilpotent` |
| `no_closed` | yes | yes | yes | none | `#print axioms no_closed` |
| `window_no_closed` | yes | yes | yes | none | `#print axioms window_no_closed` |

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

### Python: `papers/core/majorana/code/majorana_evaluator.py`

- file: [papers/core/majorana/code/majorana_evaluator.py](../../../papers/core/majorana/code/majorana_evaluator.py)
- sha256 (`bytes`): `86798eabea510363b59e164c516625c6055df24b4e12086cfe2fde5db16835c3`
- cited in: record TFQ-1154

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `audit_legacy_carrier` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `papers/core/majorana/code/tests/integration/test_tetron_surface_codes.py`

- file: [papers/core/majorana/code/tests/integration/test_tetron_surface_codes.py](../../../papers/core/majorana/code/tests/integration/test_tetron_surface_codes.py)
- sha256 (`bytes`): `613eb90331749cead532af34aa06a1d61ff5c01a8cc6fd4bdce4bdb9923f7e32`
- cited in: record TFQ-1154
- check: `python -m pytest papers/core/majorana/code/tests/integration/test_tetron_surface_codes.py::test_audit_legacy_carrier_retraction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_audit_legacy_carrier_retraction` (python_test) | yes | yes | yes | - | `python -m pytest papers/core/majorana/code/tests/integration/test_tetron_surface_codes.py::test_audit_legacy_carrier_retraction` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1154_maj_legacy_carrier_retraction.md`

- file: [dag/derivations/28_majorana/tfq_1154_maj_legacy_carrier_retraction.md](../../../dag/derivations/28_majorana/tfq_1154_maj_legacy_carrier_retraction.md)
- sha256 (`lf-normalised`): `511ae36994c3360403f44b89da360ad628f0f479c6fcce702aee0a0241eb9d62`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1154
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `e92416bb1739e51de20a8ad6a26d4b5f3d76b974d7556507b13149b29e8edb47`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/majorana/the_majorana_problem_change_log.md`

- file: [papers/core/majorana/the_majorana_problem_change_log.md](../../../papers/core/majorana/the_majorana_problem_change_log.md)
- sha256 (`lf-normalised`): `c37871232dd6ea91a271c77fa1e6f92d37b5b27e0b5f7517420cded3aee4bd38`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/majorana/the_majorana_problem_claim_ledger.md`

- file: [papers/core/majorana/the_majorana_problem_claim_ledger.md](../../../papers/core/majorana/the_majorana_problem_claim_ledger.md)
- sha256 (`lf-normalised`): `2d2b91881568780f56d7cdb53c97eec42bbfa09c21b2f1c6302665a79aad7565`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-LEGACY-CARRIER-RETRACTION` `CONDITIONAL_ON_IMPORT`: [MAJ-TRIVIAL-H1-NO-CLOSED](MAJ-TRIVIAL-H1-NO-CLOSED.md) (PROVED_LEAN), [MAJ-TETRON-ARRAY-CARRIER](MAJ-TETRON-ARRAY-CARRIER.md) (DEFINITION)

Outgoing (0):

