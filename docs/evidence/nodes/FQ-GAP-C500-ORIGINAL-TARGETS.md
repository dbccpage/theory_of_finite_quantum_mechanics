# FQ-GAP-C500-ORIGINAL-TARGETS

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For each of ten C500 blocks the original target contract remains open; closure is recorded only for a scoped statement backed by evidence files (open or invalid bet clauses listed per block, e.g. M2, M5, M7, J1, J2 in Block 10).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 18
- distinct cited Lean declarations covered by a current replay receipt: 9
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Not run here: a fresh reading of each original target contract, the evidence files named beside the ten blocks, and any claim that a scoped receipt discharges a block. The gap-register titles say the original contracts remain open. These counts of register names do not discharge a block.

## Source status

GAP-C500-B01..B10 RESOLVED_WITH_SCOPED_EVIDENCE: "original target contract remains open"

## Review

- PFP review: [dag/results/FQ-GAP-C500-ORIGINAL-TARGETS/reviews/20261019_next_ten_audit/review_result.json](../../../dag/results/FQ-GAP-C500-ORIGINAL-TARGETS/reviews/20261019_next_ten_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_block_numeral_slice_reviewed`; scope effect `caveat_added`; prior status `OPEN`; qualifies for E4: yes.
  - narrowest claim: For every natural number k, the numerals from 276 + 25 * k through 300 + 25 * k are a run of 25, and the next run starts at the next numeral. The ten runs for k from 1 through 10 begin at 301 and end at 550, covering 250 numerals, and 10 * 25 = 250. The ten clause-list lengths 0, 2, 4, 2, 4, 1, 1, 1, 1, 5 sum to 21, and the last length 5 is strictly greater than each earlier length. The five labels M2, M5, M7, J1 and J2 are pairwise distinct.
  - does not support: A fresh reading of each original target contract, the evidence files named beside the ten blocks, or a claim that a scoped receipt discharges a block.
  - next test: Read each original target contract and the evidence files named beside the ten blocks before treating any block as discharged.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFqGapC500OriginalTargets.lean`

- file: [lean4/CampaignFqGapC500OriginalTargets.lean](../../../lean4/CampaignFqGapC500OriginalTargets.lean)
- sha256 (`bytes`): `b0b2c3723f85472fd6099601c25bdd6c8650302e4c8047ab11aa89e705630090`
- cited in: node.lean, receipt dag/research/campaign_fq-gap-c500-original-targets_lean_replay.json (CampaignFqGapC500OriginalTargets), record TFQ-1025
- replay: `verified`
  - receipt [dag/research/campaign_fq-gap-c500-original-targets_lean_replay.json](../../../dag/research/campaign_fq-gap-c500-original-targets_lean_replay.json) (module `CampaignFqGapC500OriginalTargets`): recorded sha256 `b0b2c3723f85472fd6099601c25bdd6c8650302e4c8047ab11aa89e705630090` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFqGapC500OriginalTargets`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFqGapC500OriginalTargets.abut` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFqGapC500OriginalTargets.abut` |
| `CampaignFqGapC500OriginalTargets.block10ClauseCount` | yes | yes | yes | none | `#print axioms CampaignFqGapC500OriginalTargets.block10ClauseCount` |
| `CampaignFqGapC500OriginalTargets.block10ClausesNodup` | yes | yes | yes | none | `#print axioms CampaignFqGapC500OriginalTargets.block10ClausesNodup` |
| `CampaignFqGapC500OriginalTargets.clauseCountSum` | yes | yes | yes | none | `#print axioms CampaignFqGapC500OriginalTargets.clauseCountSum` |
| `CampaignFqGapC500OriginalTargets.clauseCountsLength` | yes | yes | yes | none | `#print axioms CampaignFqGapC500OriginalTargets.clauseCountsLength` |
| `CampaignFqGapC500OriginalTargets.lastClauseCountStrict` | yes | yes | yes | none | `#print axioms CampaignFqGapC500OriginalTargets.lastClauseCountStrict` |
| `CampaignFqGapC500OriginalTargets.spanLen` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFqGapC500OriginalTargets.spanLen` |
| `CampaignFqGapC500OriginalTargets.tenRunCover` | yes | yes | yes | none | `#print axioms CampaignFqGapC500OriginalTargets.tenRunCover` |
| `CampaignFqGapC500OriginalTargets.tenRunEndpoints` | yes | yes | yes | none | `#print axioms CampaignFqGapC500OriginalTargets.tenRunEndpoints` |
| `abut` | yes | yes | yes | Quot.sound, propext | `#print axioms abut` |
| `block10ClauseCount` | yes | yes | yes | none | `#print axioms block10ClauseCount` |
| `block10ClausesNodup` | yes | yes | yes | none | `#print axioms block10ClausesNodup` |
| `clauseCountSum` | yes | yes | yes | none | `#print axioms clauseCountSum` |
| `clauseCountsLength` | yes | yes | yes | none | `#print axioms clauseCountsLength` |
| `lastClauseCountStrict` | yes | yes | yes | none | `#print axioms lastClauseCountStrict` |
| `spanLen` | yes | yes | yes | Quot.sound, propext | `#print axioms spanLen` |
| `tenRunCover` | yes | yes | yes | none | `#print axioms tenRunCover` |
| `tenRunEndpoints` | yes | yes | yes | none | `#print axioms tenRunEndpoints` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1025
- counts toward the grade: no

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1025_fq_gap_c500_original_targets.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1025_fq_gap_c500_original_targets.md](../../../dag/derivations/10_finite_qm_core/tfq_1025_fq_gap_c500_original_targets.md)
- sha256 (`lf-normalised`): `86ca9f9f761cebf2a297a2684fded7c51236b7349c2cf138046559f60b301a31`
- generated view: listed, not counted
- cited in: record TFQ-1025
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
