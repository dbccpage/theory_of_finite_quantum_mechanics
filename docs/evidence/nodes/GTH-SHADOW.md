# GTH-SHADOW

Stage: [GENESIS_TO_HIGHER](../stages/GENESIS_TO_HIGHER.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> No construction turns PGW-GO-ADMISSION-GATE into a finite semi-simplicial set or a finite globular set. That gate keeps a two-valued admission record with a reached result: reaching leaves not-admitted, and admission is not one of the four kinds of change. A finite semi-simplicial set of dimension at most N is finite sets X_0, ..., X_N and face maps d_i from X_n to X_{n-1} such that d_i composed with d_j equals d_{j-1} composed with d_i whenever i \< j. It carries no degeneracy maps. A finite globular set is finite sets with source and target maps s, t from X_{n+1} to X_n such that s composed with s equals s composed with t, and t composed with t equals t composed with s. Neither family is defined from the admission record.

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

### Lean: `lean4/GenesisToHigherShadow.lean`

- file: [lean4/GenesisToHigherShadow.lean](../../../lean4/GenesisToHigherShadow.lean)
- sha256 (`bytes`): `cbad9678093f3a25d85cd823e16b4aa521350e1a61c798ada1aa3628f8c884a7`
- cited in: node.source, receipt dag/research/campaign_gth-shadow_lean_replay.json (GenesisToHigherShadow), receipt dag/research/pr_362_review_replay.json (GenesisToHigherShadow)
- replay: `verified`
  - receipt [dag/research/campaign_gth-shadow_lean_replay.json](../../../dag/research/campaign_gth-shadow_lean_replay.json) (module `GenesisToHigherShadow`): recorded sha256 `cbad9678093f3a25d85cd823e16b4aa521350e1a61c798ada1aa3628f8c884a7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/pr_362_review_replay.json](../../../dag/research/pr_362_review_replay.json) (module `GenesisToHigherShadow`): recorded sha256 `cbad9678093f3a25d85cd823e16b4aa521350e1a61c798ada1aa3628f8c884a7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build GenesisToHigherShadow`

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
- sha256 (`lf-normalised`): `2e53daa908c8c8441472e14ce9d22ff5b212ab177ec8f72be73730d8975c8597`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2400
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/gth-shadow.md`

- file: [dag/derivations/independent/gth-shadow.md](../../../dag/derivations/independent/gth-shadow.md)
- sha256 (`lf-normalised`): `ac1b8ece8aa1b54e55b006c2aef4cd51534f873573bf76dabe429f788f162165`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/independent/gth_shadow.md`

- file: [dag/derivations/independent/gth_shadow.md](../../../dag/derivations/independent/gth_shadow.md)
- sha256 (`lf-normalised`): `ac1b8ece8aa1b54e55b006c2aef4cd51534f873573bf76dabe429f788f162165`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_gth-shadow_lean_replay.json`

- file: [dag/research/campaign_gth-shadow_lean_replay.json](../../../dag/research/campaign_gth-shadow_lean_replay.json)
- sha256 (`lf-normalised`): `1c0bb185dbd079697ab4e89c49409fde1b3d3f5bc3cb6cbed0deacdadbf36c78`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `GTH-R-GTH-SHADOW` `GAP_NO_DERIVATION`: [PGW-GO-ADMISSION-GATE](PGW-GO-ADMISSION-GATE.md) (DEFINITION)

Outgoing (1):

- `GTH-R-GTH-TRUNC` `GAP_NO_DERIVATION`: [GTH-TRUNC](GTH-TRUNC.md) (OPEN)
