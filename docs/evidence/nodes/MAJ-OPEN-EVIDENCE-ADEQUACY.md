# MAJ-OPEN-EVIDENCE-ADEQUACY

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Whether a declared laboratory protocol's measurement map M separates topological zero modes from trivial Andreev bound states, i.e. whether rho_topo - rho_ABS lies outside ker M.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

No laboratory protocol, device model, density operator, or measurement map from a physical apparatus is supplied. These two coordinate maps are not that protocol. Whether any declared laboratory map separates topological zero modes from Andreev bound states stays open.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-OPEN-EVIDENCE-ADEQUACY claims OPEN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/MajoranaOpenEvidenceAdequacy.lean`

- file: [lean4/MajoranaOpenEvidenceAdequacy.lean](../../../lean4/MajoranaOpenEvidenceAdequacy.lean)
- sha256 (`bytes`): `e45c6ff6876596edb3c629299079c5a0c9007299e2972eddc183447f7e2bfc64`
- cited in: node.lean, receipt dag/research/campaign_maj-open-evidence-adequacy_lean_replay.json (MajoranaOpenEvidenceAdequacy), receipt dag/research/pr_361_review_replay.json (MajoranaOpenEvidenceAdequacy), record TFQ-1182
- replay: `verified`
  - receipt [dag/research/campaign_maj-open-evidence-adequacy_lean_replay.json](../../../dag/research/campaign_maj-open-evidence-adequacy_lean_replay.json) (module `MajoranaOpenEvidenceAdequacy`): recorded sha256 `e45c6ff6876596edb3c629299079c5a0c9007299e2972eddc183447f7e2bfc64` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/pr_361_review_replay.json](../../../dag/research/pr_361_review_replay.json) (module `MajoranaOpenEvidenceAdequacy`): recorded sha256 `e45c6ff6876596edb3c629299079c5a0c9007299e2972eddc183447f7e2bfc64` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build MajoranaOpenEvidenceAdequacy`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `diff_is_zero_neg_one` | yes | yes | yes | none | `#print axioms diff_is_zero_neg_one` |
| `first_coord_kernel` | yes | yes | yes | none | `#print axioms first_coord_kernel` |
| `second_coord_separates` | yes | yes | yes | none | `#print axioms second_coord_separates` |

- counts toward the grade: yes

### Python: `checks/independent/maj-open-evidence-adequacy.py`

- file: [checks/independent/maj-open-evidence-adequacy.py](../../../checks/independent/maj-open-evidence-adequacy.py)
- sha256 (`bytes`): `65239125adba7ab68743d194e0c9146b7566d59bfa89562f2331f6e3dfec1197`
- cited in: record TFQ-1182
- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1182_maj_open_evidence_adequacy.md`

- file: [dag/derivations/28_majorana/tfq_1182_maj_open_evidence_adequacy.md](../../../dag/derivations/28_majorana/tfq_1182_maj_open_evidence_adequacy.md)
- sha256 (`lf-normalised`): `53021315432fb47c3a7921b819fe15cfd4ed3ae716afb15cdcd143c6f3b1ee01`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1182
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/maj-open-evidence-adequacy.md`

- file: [dag/derivations/independent/maj-open-evidence-adequacy.md](../../../dag/derivations/independent/maj-open-evidence-adequacy.md)
- sha256 (`lf-normalised`): `3b347492ed972cf1ab733d47b642013236189b0e264eae91b8969c2a49f74fd3`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_maj-open-evidence-adequacy_lean_replay.json`

- file: [dag/research/campaign_maj-open-evidence-adequacy_lean_replay.json](../../../dag/research/campaign_maj-open-evidence-adequacy_lean_replay.json)
- sha256 (`lf-normalised`): `ac9a8bc4a2a09f521c43e6afa331c699120cd9fe5b4ee5bb7c032036136a375b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `2f55c0f24f87388cfa9d7a4a7d832f34c0fa30b857d344811f4336f634c1684b`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-OPEN-EVIDENCE-ADEQUACY` `GAP_NO_DERIVATION`: [MAJ-DETECTOR-INADEQUATE](MAJ-DETECTOR-INADEQUATE.md) (DEFINITION)

Outgoing (0):

