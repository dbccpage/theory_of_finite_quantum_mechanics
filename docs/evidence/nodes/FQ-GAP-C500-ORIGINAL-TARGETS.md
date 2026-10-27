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

### Lean: `lean4/OriginalTargetNumerals.lean`

- file: [lean4/OriginalTargetNumerals.lean](../../../lean4/OriginalTargetNumerals.lean)
- sha256 (`bytes`): `c7b1a08231d1dc7417cf9b12e6f76b13f24c5dfb0e6e0aa0126e3f27d2bf8be6`
- cited in: node.lean, receipt dag/research/campaign_fq-gap-c500-original-targets_lean_replay.json (OriginalTargetNumerals), record TFQ-1025
- replay: `verified`
  - receipt [dag/research/campaign_fq-gap-c500-original-targets_lean_replay.json](../../../dag/research/campaign_fq-gap-c500-original-targets_lean_replay.json) (module `OriginalTargetNumerals`): recorded sha256 `c7b1a08231d1dc7417cf9b12e6f76b13f24c5dfb0e6e0aa0126e3f27d2bf8be6` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build OriginalTargetNumerals`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `OriginalTargetNumerals.abut` | yes | yes | yes | Quot.sound, propext | `#print axioms OriginalTargetNumerals.abut` |
| `OriginalTargetNumerals.block10ClauseCount` | yes | yes | yes | none | `#print axioms OriginalTargetNumerals.block10ClauseCount` |
| `OriginalTargetNumerals.block10ClausesNodup` | yes | yes | yes | none | `#print axioms OriginalTargetNumerals.block10ClausesNodup` |
| `OriginalTargetNumerals.clauseCountSum` | yes | yes | yes | none | `#print axioms OriginalTargetNumerals.clauseCountSum` |
| `OriginalTargetNumerals.clauseCountsLength` | yes | yes | yes | none | `#print axioms OriginalTargetNumerals.clauseCountsLength` |
| `OriginalTargetNumerals.lastClauseCountStrict` | yes | yes | yes | none | `#print axioms OriginalTargetNumerals.lastClauseCountStrict` |
| `OriginalTargetNumerals.spanLen` | yes | yes | yes | Quot.sound, propext | `#print axioms OriginalTargetNumerals.spanLen` |
| `OriginalTargetNumerals.tenRunCover` | yes | yes | yes | none | `#print axioms OriginalTargetNumerals.tenRunCover` |
| `OriginalTargetNumerals.tenRunEndpoints` | yes | yes | yes | none | `#print axioms OriginalTargetNumerals.tenRunEndpoints` |
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

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1025_fq_gap_c500_original_targets.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1025_fq_gap_c500_original_targets.md](../../../dag/derivations/10_finite_qm_core/tfq_1025_fq_gap_c500_original_targets.md)
- sha256 (`lf-normalised`): `fd834ac1ba6b251bcdfdf47f8db240208339c66d9c402cc81d56fb56db0713e4`
- generated view: listed, not counted
- cited in: record TFQ-1025
- counts toward the grade: no

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml`

- file: [sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml](../../../sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `722a38e963f9ae31ac005968a71e39dff5964e452f5aca1e5cb4506dc0ece190`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche6_conditional_and_open_boundary_certificates_witness`

## Routes

Incoming (0):


Outgoing (0):


No incoming route.
