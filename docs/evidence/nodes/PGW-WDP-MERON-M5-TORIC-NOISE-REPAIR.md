# PGW-WDP-MERON-M5-TORIC-NOISE-REPAIR

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Meron Field-Limit Target M5 (Chapter 23): the primal-dual completion criterion ((E - E) intersect ker Q_D subset B) characterizes exact recovery, the 4-vertex star syndrome on a square cycle has rank 3 and is injective on tree-supported errors while vanishing on the 4-edge cycle, and worst-case adaptive transcripts cannot distinguish errors differing by an undetected logical cycle.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 5 Lean reference(s) cited, 5 in this checkout (replay: none 5). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Mechanized in Lean 4 (toric_completion_criterion_iff, toric_star_syndrome_sum_zero, toric_restricted_tree_error_injective, toric_cycle_error_in_syndrome_kernel, and toric_adaptive_transcript_indistinguishable in WdpBatch6.lean) and checked in Python plan_odm_toric_boundary.py.

## Source status

Meron Target M5 / Chapter 23 finite toric-code kernel, tree-error injectivity, and adaptive non-improvement mechanized in WdpBatch6.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean)
- sha256 (`bytes`): `1bf7c1e971d501d47ce848a7d7c8149dd75542ace9fa09b229da2b5cc67f580c`
- cited in: node.lean, record TFQ-0586
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch6.toric_adaptive_transcript_indistinguishable` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch6.toric_adaptive_transcript_indistinguishable` |
| `WitnessedDifference.WdpBatch6.toric_completion_criterion_iff` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch6.toric_completion_criterion_iff` |
| `WitnessedDifference.WdpBatch6.toric_cycle_error_in_syndrome_kernel` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch6.toric_cycle_error_in_syndrome_kernel` |
| `WitnessedDifference.WdpBatch6.toric_restricted_tree_error_injective` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch6.toric_restricted_tree_error_injective` |
| `WitnessedDifference.WdpBatch6.toric_star_syndrome_sum_zero` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch6.toric_star_syndrome_sum_zero` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/plan_odm_toric_boundary.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/plan_odm_toric_boundary.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/plan_odm_toric_boundary.py)
- sha256 (`bytes`): `f46c48bc2fe43b208b01e540ba1576d0ace4f4191be767124c55467dd0bc243c`
- cited in: record TFQ-0586

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `toric_boundary_witness` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/meron_field_limit_derivations/README.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/meron_field_limit_derivations/README.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/meron_field_limit_derivations/README.md)
- sha256 (`lf-normalised`): `ce2465556f7ae8df7f142f69227596b99164f48968e97ad7b746599c9215d602`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0586_wdp_meron_m5_toric_noise_repair.md`

- file: [dag/derivations/06_wdp/tfq_0586_wdp_meron_m5_toric_noise_repair.md](../../../dag/derivations/06_wdp/tfq_0586_wdp_meron_m5_toric_noise_repair.md)
- sha256 (`lf-normalised`): `d958a3eff41850c6c2bfa4c8d0409725010bb5217f5de7e6255b996deba7a8e4`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0586
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0586 rust: checked by Lean 4 theorems and Python toric boundary witness

## Routes

Incoming (1):

- `PGW-R-WDP-MERON-M5-TORIC-NOISE-REPAIR` `DERIVED_LEAN`: [PGW-WDP-MERON-M4-NATIVE-ADAPTERS](PGW-WDP-MERON-M4-NATIVE-ADAPTERS.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-MERON-SPACETIME-LIMIT` `GAP_NO_DERIVATION`: [PGW-WDP-MERON-SPACETIME-LIMIT](PGW-WDP-MERON-SPACETIME-LIMIT.md) (OPEN)
