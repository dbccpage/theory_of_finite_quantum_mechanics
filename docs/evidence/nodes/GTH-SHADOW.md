# GTH-SHADOW

Stage: [GENESIS_TO_HIGHER](../stages/GENESIS_TO_HIGHER.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Narrowed boundary, status left OPEN. On the triangle with vertices 0, 1 and 2, the edges are (0, 1), (0, 2) and (1, 2). The target of (0, 2) equals the target of (1, 2), the target of (0, 1) equals the source of (1, 2), and the source of (0, 1) equals the source of (0, 2). The reach map sends 0 and 1 to 0, and the pair (0, 0) differs from the edge (0, 1). For two edges labeled 0 and 1, the source map sends both to 0 and the target map sends both to 1, so the two source values agree and the two target values agree.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 6
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

No construction turns the admission gate into a finite semi-simplicial set or a finite globular set. The two-valued record's four kinds of change, degeneracy maps, and every complex other than this triangle and this pair of edges stay open. The node lean list stays empty because this stage rejects a Lean citation.

## Source status

Open. One triangle and one reach map are recorded. No finite semi-simplicial or globular set is defined from PGW-GO-ADMISSION-GATE.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignGthShadow.lean`

- file: [lean4/CampaignGthShadow.lean](../../../lean4/CampaignGthShadow.lean)
- sha256 (`bytes`): `be8ca950fdb9a59cdef48afeecf2caa751ce2959f8a09d0d757bc63098093d74`
- cited in: node.source, receipt dag/research/campaign_gth-shadow_lean_replay.json (CampaignGthShadow), receipt dag/research/pr_362_review_replay.json (CampaignGthShadow)
- replay: `verified`
  - receipt [dag/research/campaign_gth-shadow_lean_replay.json](../../../dag/research/campaign_gth-shadow_lean_replay.json) (module `CampaignGthShadow`): recorded sha256 `be8ca950fdb9a59cdef48afeecf2caa751ce2959f8a09d0d757bc63098093d74` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/pr_362_review_replay.json](../../../dag/research/pr_362_review_replay.json) (module `CampaignGthShadow`): recorded sha256 `be8ca950fdb9a59cdef48afeecf2caa751ce2959f8a09d0d757bc63098093d74` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignGthShadow`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `face_id_01` | yes | yes | yes | none | `#print axioms face_id_01` |
| `face_id_02` | yes | yes | yes | none | `#print axioms face_id_02` |
| `face_id_12` | yes | yes | yes | none | `#print axioms face_id_12` |
| `parallel_edges` | yes | yes | yes | none | `#print axioms parallel_edges` |
| `reach_collapses` | yes | yes | yes | none | `#print axioms reach_collapses` |
| `reach_pair_differs` | yes | yes | yes | none | `#print axioms reach_pair_differs` |

- counts toward the grade: yes

### Python: `checks/independent/gth-shadow.py`

- file: [checks/independent/gth-shadow.py](../../../checks/independent/gth-shadow.py)
- sha256 (`bytes`): `90e4bd98c7dc31701ed84ca6e279fc1de8dc6284fe06998dde2e871ff5b7dea0`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/34_genesis_to_higher/tfq_2400_gth_shadow.md`

- file: [dag/derivations/34_genesis_to_higher/tfq_2400_gth_shadow.md](../../../dag/derivations/34_genesis_to_higher/tfq_2400_gth_shadow.md)
- sha256 (`lf-normalised`): `e287b997595f96acd93c91b01e7e9de5113f6387ce4c73a99f7d38bbe2eaa3b0`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2400
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/gth-shadow.md`

- file: [dag/derivations/independent/gth-shadow.md](../../../dag/derivations/independent/gth-shadow.md)
- sha256 (`lf-normalised`): `875617f82a6960da3db791f8922bd9c1a1c610e75550c7eb68c63456f2f00854`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/independent/gth_shadow.md`

- file: [dag/derivations/independent/gth_shadow.md](../../../dag/derivations/independent/gth_shadow.md)
- sha256 (`lf-normalised`): `875617f82a6960da3db791f8922bd9c1a1c610e75550c7eb68c63456f2f00854`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_gth-shadow_lean_replay.json`

- file: [dag/research/campaign_gth-shadow_lean_replay.json](../../../dag/research/campaign_gth-shadow_lean_replay.json)
- sha256 (`lf-normalised`): `59bb9f976ba8f1c8e0f486d0fb312a0c2c55b890fe5ded74819ae253013bc3c8`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `GTH-R-GTH-SHADOW` `GAP_NO_DERIVATION`: [PGW-GO-ADMISSION-GATE](PGW-GO-ADMISSION-GATE.md) (DEFINITION)

Outgoing (1):

- `GTH-R-GTH-TRUNC` `GAP_NO_DERIVATION`: [GTH-TRUNC](GTH-TRUNC.md) (OPEN)
