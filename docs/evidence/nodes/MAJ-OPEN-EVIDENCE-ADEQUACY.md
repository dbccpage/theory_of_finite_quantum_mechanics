# MAJ-OPEN-EVIDENCE-ADEQUACY

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Narrowed boundary, status left OPEN. For the integer readings topo = (1, 0) and andreev = (1, 1), the difference is (0, -1). The first-coordinate map sends that difference to 0 and sends both readings to 1. The second-coordinate map sends the difference to -1, the topo reading to 0, and the andreev reading to 1, and those second coordinates differ.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declaration references covered by a current replay receipt: 3
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

### Lean: `lean4/CampaignMajOpenEvidenceAdequacy.lean`

- file: [lean4/CampaignMajOpenEvidenceAdequacy.lean](../../../lean4/CampaignMajOpenEvidenceAdequacy.lean)
- sha256 (`bytes`): `81a40a01895906d43d21209fc70e5b9b2b5de09f8420670a14a11543d615c8a4`
- cited in: node.lean, receipt dag/research/campaign_maj-open-evidence-adequacy_lean_replay.json (CampaignMajOpenEvidenceAdequacy), receipt dag/research/pr_361_review_replay.json (CampaignMajOpenEvidenceAdequacy), record TFQ-1182
- replay: `verified`
  - receipt [dag/research/campaign_maj-open-evidence-adequacy_lean_replay.json](../../../dag/research/campaign_maj-open-evidence-adequacy_lean_replay.json) (module `CampaignMajOpenEvidenceAdequacy`): recorded sha256 `81a40a01895906d43d21209fc70e5b9b2b5de09f8420670a14a11543d615c8a4` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/pr_361_review_replay.json](../../../dag/research/pr_361_review_replay.json) (module `CampaignMajOpenEvidenceAdequacy`): recorded sha256 `81a40a01895906d43d21209fc70e5b9b2b5de09f8420670a14a11543d615c8a4` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignMajOpenEvidenceAdequacy`

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
- sha256 (`lf-normalised`): `fa767c974693eb47dc5dfe0c17b7f5d66bc6741068d8cc76daf811168083c071`
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
- sha256 (`lf-normalised`): `d2d50f7085b41a935240d763a558fefcaa5f3dce9ba049773516d5d4f2f4ae15`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `e92416bb1739e51de20a8ad6a26d4b5f3d76b974d7556507b13149b29e8edb47`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-OPEN-EVIDENCE-ADEQUACY` `GAP_NO_DERIVATION`: [MAJ-DETECTOR-INADEQUATE](MAJ-DETECTOR-INADEQUATE.md) (DEFINITION)

Outgoing (0):

