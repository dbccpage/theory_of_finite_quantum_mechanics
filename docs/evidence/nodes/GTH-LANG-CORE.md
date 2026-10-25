# GTH-LANG-CORE

Stage: [GENESIS_TO_HIGHER](../stages/GENESIS_TO_HIGHER.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Narrowed boundary, status left OPEN. One regime carrier has data 1 and forms, instances, rules and requirements all 0, and the sum of those five slots is 1. The same carrier with its rule slot set to 1 differs from it, and that rule slot is 1. The reach map sends 0 and 1 to 0.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

No syntax, typing judgement or deep embedding of a priced admission language is defined. The two boxed laws, the MSS-N alphabet, and every regime other than this one carrier stay open. The node lean list stays empty because this stage rejects a Lean citation.

## Source status

Open. One integer regime carrier is recorded in CampaignGthLangCore. The priced admission language still has no syntax. The node lean list stays empty.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignGthLangCore.lean`

- file: [lean4/CampaignGthLangCore.lean](../../../lean4/CampaignGthLangCore.lean)
- sha256 (`bytes`): `57cb0bcf3599400870ca47f0e0f11c87f3dabe90f04752f964f0ee0f591eef5f`
- cited in: node.source, receipt dag/research/campaign_gth-lang-core_lean_replay.json (CampaignGthLangCore), receipt dag/research/pr_363_review_replay.json (CampaignGthLangCore)
- replay: `verified`
  - receipt [dag/research/campaign_gth-lang-core_lean_replay.json](../../../dag/research/campaign_gth-lang-core_lean_replay.json) (module `CampaignGthLangCore`): recorded sha256 `57cb0bcf3599400870ca47f0e0f11c87f3dabe90f04752f964f0ee0f591eef5f` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/pr_363_review_replay.json](../../../dag/research/pr_363_review_replay.json) (module `CampaignGthLangCore`): recorded sha256 `57cb0bcf3599400870ca47f0e0f11c87f3dabe90f04752f964f0ee0f591eef5f` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignGthLangCore`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `carrier_slots` | yes | yes | yes | none | `#print axioms carrier_slots` |
| `carrier_sum` | yes | yes | yes | none | `#print axioms carrier_sum` |
| `reach_collapses` | yes | yes | yes | none | `#print axioms reach_collapses` |
| `withRule_differs` | yes | yes | yes | none | `#print axioms withRule_differs` |
| `withRule_slots` | yes | yes | yes | none | `#print axioms withRule_slots` |
- counts toward the grade: yes

### Python: `checks/independent/gth-lang-core.py`

- file: [checks/independent/gth-lang-core.py](../../../checks/independent/gth-lang-core.py)
- sha256 (`bytes`): `cbcb89d0299d1cfc204c0fcdca6b43edf7d23313d37033c15dde65eebd487c4e`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/34_genesis_to_higher/tfq_2407_gth_lang_core.md`

- file: [dag/derivations/34_genesis_to_higher/tfq_2407_gth_lang_core.md](../../../dag/derivations/34_genesis_to_higher/tfq_2407_gth_lang_core.md)
- sha256 (`lf-normalised`): `410aa93d68fc2caa3b12fb9b3190f4ed11ad649859a3f998339b00e3f7609f36`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2407
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/gth-lang-core.md`

- file: [dag/derivations/independent/gth-lang-core.md](../../../dag/derivations/independent/gth-lang-core.md)
- sha256 (`lf-normalised`): `6ce894d42d022e47de467153129bbe72db4f40d5153ee0947186f6ba22f4d7a0`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/independent/gth_lang_core.md`

- file: [dag/derivations/independent/gth_lang_core.md](../../../dag/derivations/independent/gth_lang_core.md)
- sha256 (`lf-normalised`): `6ce894d42d022e47de467153129bbe72db4f40d5153ee0947186f6ba22f4d7a0`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_gth-lang-core_lean_replay.json`

- file: [dag/research/campaign_gth-lang-core_lean_replay.json](../../../dag/research/campaign_gth-lang-core_lean_replay.json)
- sha256 (`lf-normalised`): `de3044a046db59586dc0e9e7120ba3d3a2e29c5ec02e79e2ec650a0f5f7e6457`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `GTH-R-GTH-LANG-CORE` `GAP_NO_DERIVATION`: [PGW-GO-ADMISSION-GATE](PGW-GO-ADMISSION-GATE.md) (DEFINITION), [PG-GEN-REGIME-EVENTS](PG-GEN-REGIME-EVENTS.md) (DEFINITION), [PGW-SN-TWO-BOXED-LAWS](PGW-SN-TWO-BOXED-LAWS.md) (DEFINITION)

Outgoing (1):

- `GTH-R-GTH-LANG-REFLECT` `GAP_NO_DERIVATION`: [GTH-LANG-REFLECT](GTH-LANG-REFLECT.md) (OPEN)
