# PGW-WDP-MERON-SPACETIME-LIMIT

Stage: [WDP](../stages/WDP.md). Status: `OPEN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Periodic full-Fock U=t chain spacetime response synthesis: connect finite-volume occupation-basis signed SQL history sums to continuum Euclidean response functions without substituting an unrestricted spin trace.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

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
- sha256 (`lf-normalised`): `fd7ec715d743f53bf26e240e96a0345854d6153fa4192dd3dc2ebd89a2a7d94f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0587
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0587 lean4: continuum spacetime response limit of periodic full-Fock U=t chain is open
- TFQ-0587 rust: finite checks executed in Python (meron_spacetime_finite_checks.py)

## Routes

Incoming (1):

- `PGW-R-WDP-MERON-SPACETIME-LIMIT` `GAP_NO_DERIVATION`: [PGW-WDP-MERON-M5-TORIC-NOISE-REPAIR](PGW-WDP-MERON-M5-TORIC-NOISE-REPAIR.md) (PROVED_LEAN), [PGW-WDP-MERON-M1-CORRELATION-ESTIMATES](PGW-WDP-MERON-M1-CORRELATION-ESTIMATES.md) (OPEN), [PGW-WDP-MERON-M2-CUMULANT-BOUNDS](PGW-WDP-MERON-M2-CUMULANT-BOUNDS.md) (OPEN), [PGW-WDP-MERON-M3-SPECTRAL-GAP-BYPASS](PGW-WDP-MERON-M3-SPECTRAL-GAP-BYPASS.md) (OPEN)

Outgoing (0):

