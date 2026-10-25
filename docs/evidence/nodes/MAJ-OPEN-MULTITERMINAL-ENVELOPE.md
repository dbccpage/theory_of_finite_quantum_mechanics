# MAJ-OPEN-MULTITERMINAL-ENVELOPE

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For an M-terminal junction (M \>= 4) with Delta_eff = Delta_0 (1 - sigma_V/sigma_crit), the transfer envelope adds C(M,2) \>= 6 pairwise splitting channels, its minimum rises with sigma_V on (0, sigma_crit), and the gap closes for sigma_V \>= sigma_crit.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- linear gap-degradation model Delta_eff(sigma_V)
- exponential overlap splitting delta E_ij

## Bottleneck

Derive the envelope and the monotonicity in sigma_V; the gap-degradation law is posited.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-C20 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/majorana/lean4/MajoranaCore.lean`

- file: [papers/core/majorana/lean4/MajoranaCore.lean](../../../papers/core/majorana/lean4/MajoranaCore.lean)
- sha256 (`bytes`): `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071`
- cited in: node.lean, record TFQ-1179
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_majorana.json](../../../dag/research/lean_replay_campaign_majorana.json) (module `papers.core.majorana.lean4.MajoranaCore`): recorded sha256 `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `MultiTerminalTransferBound` | yes | yes | yes | module-level | `#print axioms MultiTerminalTransferBound` |
| `disorder_gap_degradation_lower_bound` | yes | yes | yes | Quot.sound, propext | `#print axioms disorder_gap_degradation_lower_bound` |
| `multiterminal_crosstalk_channels_pos` | yes | yes | yes | Quot.sound, propext | `#print axioms multiterminal_crosstalk_channels_pos` |
| `multiterminal_pareto_defect_pos` | yes | yes | yes | Quot.sound, propext | `#print axioms multiterminal_pareto_defect_pos` |
| `multiterminal_transfer_defect_pos` | yes | yes | yes | none | `#print axioms multiterminal_transfer_defect_pos` |

- counts toward the grade: yes

### Python: `papers/core/majorana/code/majorana_evaluator.py`

- file: [papers/core/majorana/code/majorana_evaluator.py](../../../papers/core/majorana/code/majorana_evaluator.py)
- sha256 (`bytes`): `86798eabea510363b59e164c516625c6055df24b4e12086cfe2fde5db16835c3`
- cited in: record TFQ-1179

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ContinuumCrossJunctionFemModel` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1179_maj_open_multiterminal_envelope.md`

- file: [dag/derivations/28_majorana/tfq_1179_maj_open_multiterminal_envelope.md](../../../dag/derivations/28_majorana/tfq_1179_maj_open_multiterminal_envelope.md)
- sha256 (`lf-normalised`): `1d43d6711088707a8de19a810832dae1bd912b202eac30f2f9e0f4c319aac6d2`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1179
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `e92416bb1739e51de20a8ad6a26d4b5f3d76b974d7556507b13149b29e8edb47`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/majorana/the_majorana_problem_claim_ledger.md`

- file: [papers/core/majorana/the_majorana_problem_claim_ledger.md](../../../papers/core/majorana/the_majorana_problem_claim_ledger.md)
- sha256 (`lf-normalised`): `2d2b91881568780f56d7cdb53c97eec42bbfa09c21b2f1c6302665a79aad7565`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-OPEN-MULTITERMINAL-ENVELOPE` `GAP_NO_DERIVATION`: [MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE](MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE.md) (OPEN)

Outgoing (1):

- `APP-R-MAJ-OPEN-POISSON-SCHRODINGER` `GAP_NO_DERIVATION`: [MAJ-OPEN-POISSON-SCHRODINGER](MAJ-OPEN-POISSON-SCHRODINGER.md) (OPEN)
