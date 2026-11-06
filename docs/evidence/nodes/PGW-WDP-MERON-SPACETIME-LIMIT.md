# PGW-WDP-MERON-SPACETIME-LIMIT

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Periodic full-Fock U=t chain spacetime response synthesis: connect finite-volume occupation-basis signed SQL history sums to continuum Euclidean response functions without substituting an unrestricted spin trace.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Terminal open continuum-limit node for the WDP Meron branch; meron_spacetime_proof.md is explicitly marked Status: OPEN and claims no spatial scaling limit or new Lean credit.

## Source status

Open spacetime response draft in docs/02_requiring_derivation/open_derivations/meron_spacetime_limit/meron_spacetime_proof.md

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13.lean)
- sha256 (`bytes`): `3377cf9964df63977e7ecbd78fdcef5e5f7168469b06c3eafbe13e23929c74b2`
- cited in: node.lean, record TFQ-0587
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch13.finite_history_sum_eq_ordered_trace` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch13.finite_history_sum_eq_ordered_trace` |
| `WitnessedDifference.WdpBatch13.signed_vs_unsigned_trace_discrepancy` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch13.signed_vs_unsigned_trace_discrepancy` |
| `WitnessedDifference.WdpBatch13.wdp_meron_spacetime_finite_history_trace_and_sign_discrepancy` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch13.wdp_meron_spacetime_finite_history_trace_and_sign_discrepancy` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13Rep.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13Rep.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13Rep.lean)
- sha256 (`bytes`): `e0759f7adc6c5c4ebf06628f24c88a7cf0e84d24720dcf526b006a774318a3b9`
- cited in: node.lean, record TFQ-0587
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13Rep.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch13Rep.wdp_meron_spacetime_finite_history_trace_and_sign_discrepancy` | yes | yes | no | - | `#print axioms WitnessedDifference.WdpBatch13Rep.wdp_meron_spacetime_finite_history_trace_and_sign_discrepancy` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/open_derivations/meron_spacetime_limit/meron_spacetime_finite_checks.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/open_derivations/meron_spacetime_limit/meron_spacetime_finite_checks.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/open_derivations/meron_spacetime_limit/meron_spacetime_finite_checks.py)
- sha256 (`bytes`): `1da2df9c0b6fed4b735286cc782df54bf3abcd6692c5742e410bff5cd3a4fe9e`
- cited in: record TFQ-0587

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `layer_transfer` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/open_derivations/meron_spacetime_limit/meron_spacetime_proof.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/open_derivations/meron_spacetime_limit/meron_spacetime_proof.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/open_derivations/meron_spacetime_limit/meron_spacetime_proof.md)
- sha256 (`lf-normalised`): `17783ce7a773d9725ff43cf45d306e69301388906dcadcc4c9cbcd7b58e7b0f3`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0587_wdp_meron_spacetime_limit.md`

- file: [dag/derivations/06_wdp/tfq_0587_wdp_meron_spacetime_limit.md](../../../dag/derivations/06_wdp/tfq_0587_wdp_meron_spacetime_limit.md)
- sha256 (`lf-normalised`): `cf6ef4133a1691d5f771c493d6e78904dfceb32a606466f7c48a85fe2185a9b0`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0587
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0587 lean4: continuum spacetime response limit of periodic full-Fock U=t chain is open
- TFQ-0587 rust: finite checks executed in Python (meron_spacetime_finite_checks.py)

## Routes

Incoming (1):

- `PGW-R-WDP-MERON-SPACETIME-LIMIT` `DERIVED_LEAN`: [PGW-WDP-MERON-M5-TORIC-NOISE-REPAIR](PGW-WDP-MERON-M5-TORIC-NOISE-REPAIR.md) (PROVED_LEAN), [PGW-WDP-MERON-M1-CORRELATION-ESTIMATES](PGW-WDP-MERON-M1-CORRELATION-ESTIMATES.md) (PROVED_LEAN), [PGW-WDP-MERON-M2-CUMULANT-BOUNDS](PGW-WDP-MERON-M2-CUMULANT-BOUNDS.md) (PROVED_LEAN), [PGW-WDP-MERON-M3-SPECTRAL-GAP-BYPASS](PGW-WDP-MERON-M3-SPECTRAL-GAP-BYPASS.md) (PROVED_LEAN)

Outgoing (0):

