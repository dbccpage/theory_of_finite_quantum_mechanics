# FQ-GAP-CUSTODY-AND-RECEIPTS

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The named untyped-row numerals satisfy 48 - 24 = 24. The named coverage numerals satisfy 53 - 22 = 31 and 22 \< 53.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Not run here: a recount of the ledger rows behind the numeral 48, a check that the GAP-FQM-002 text says 24, a search for the QM_208-211 libraries, the eight Mathlib claims of GAP-FQM-019, the Classical.choice dependency named H019.basisGen8_eval_pos, the GAP-FQM-022 provenance pointers, the Zenodo status of QM_020 and QM_080, and the README code-companion check. A stale receipt over H000..H018 coexists with Lean headers that say Candidate only. The three Nat identities do not discharge that inventory.

## Source status

gap_register GAP-FQM-002/003/004/006..010/012/014/017/019/020/022 (statuses absent or stale in several)

## Review

- PFP review: [dag/results/FQ-GAP-CUSTODY-AND-RECEIPTS/reviews/20261019_scope_audit/review_result.json](../../../dag/results/FQ-GAP-CUSTODY-AND-RECEIPTS/reviews/20261019_scope_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_numeral_slice_reviewed`; scope effect `statement_narrowed`; prior status `OPEN`; qualifies for E4: yes.
  - narrowest claim: The named untyped-row numerals satisfy 48 - 24 = 24. The named coverage numerals satisfy 53 - 22 = 31 and 22 \< 53.
  - does not support: A recount of ledger rows, missing libraries, Mathlib promotion, the named Classical.choice dependency, provenance pointers, Zenodo publication status, or the README code-companion check.
  - next test: Recount the ledger rows, the named libraries, the Mathlib claims, the Classical.choice dependency, the provenance pointers, the Zenodo records, and the README check on a clean tree.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFqGapCustodyAndReceipts.lean`

- file: [lean4/CampaignFqGapCustodyAndReceipts.lean](../../../lean4/CampaignFqGapCustodyAndReceipts.lean)
- sha256 (`bytes`): `c33d992442c75c81cad274e786a8f34ae95fb666ba10298e89f5a2332011e012`
- cited in: node.lean, receipt dag/research/campaign_fq-gap-custody-and-receipts_lean_replay.json (CampaignFqGapCustodyAndReceipts), record TFQ-1023
- replay: `verified`
  - receipt [dag/research/campaign_fq-gap-custody-and-receipts_lean_replay.json](../../../dag/research/campaign_fq-gap-custody-and-receipts_lean_replay.json) (module `CampaignFqGapCustodyAndReceipts`): recorded sha256 `c33d992442c75c81cad274e786a8f34ae95fb666ba10298e89f5a2332011e012` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFqGapCustodyAndReceipts`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFqGapCustodyAndReceipts.coverageIsProper` | yes | yes | yes | none | `#print axioms CampaignFqGapCustodyAndReceipts.coverageIsProper` |
| `CampaignFqGapCustodyAndReceipts.coverageNumeralRemainder` | yes | yes | yes | none | `#print axioms CampaignFqGapCustodyAndReceipts.coverageNumeralRemainder` |
| `CampaignFqGapCustodyAndReceipts.untypedRowNumeralGap` | yes | yes | yes | none | `#print axioms CampaignFqGapCustodyAndReceipts.untypedRowNumeralGap` |
| `coverageIsProper` | yes | yes | yes | none | `#print axioms coverageIsProper` |
| `coverageNumeralRemainder` | yes | yes | yes | none | `#print axioms coverageNumeralRemainder` |
| `untypedRowNumeralGap` | yes | yes | yes | none | `#print axioms untypedRowNumeralGap` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1023
- counts toward the grade: no

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1023_fq_gap_custody_and_receipts.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1023_fq_gap_custody_and_receipts.md](../../../dag/derivations/10_finite_qm_core/tfq_1023_fq_gap_custody_and_receipts.md)
- sha256 (`lf-normalised`): `d075d79feba00257d72ea21de197535e85f57240aa21e3999a0734e249d9b8dc`
- generated view: listed, not counted
- cited in: record TFQ-1023
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml`

- file: [sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml](../../../sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `16a418a93748cef695fad3c1fab0fd14dd95c6985b23ee8a814b171eca60a445`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (0):


Outgoing (0):


No incoming route.
