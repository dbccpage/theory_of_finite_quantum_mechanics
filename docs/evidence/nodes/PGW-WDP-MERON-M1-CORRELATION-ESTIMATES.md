# PGW-WDP-MERON-M1-CORRELATION-ESTIMATES

Stage: [WDP](../stages/WDP.md). Status: `OPEN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Meron Field-Limit Target M1: establish or refute uniform spatial and time-dependent correlation estimates required for a joint (L, M) thermodynamic and Trotter continuum limit.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
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

Open continuum-limit target; fixed four-site Trotter bounds (GEN-WDP-57) do not establish uniform joint (L, M) convergence.

## Source status

Meron Target M1 open in docs/02_requiring_derivation/meron_field_limit_derivations/README.md

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/TrotterObservableFiltering.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/TrotterObservableFiltering.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/TrotterObservableFiltering.lean)
- sha256 (`bytes`): `4668cc41dcb6358f03fa103bd4e72f6607ec88aac4a5b326e7828b507db9bab5`
- cited in: node.lean, record TFQ-0582
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/TrotterObservableFiltering.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `paired_bound` | yes | yes | yes | - | `#print axioms paired_bound` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/open_derivations/meron_spacetime_limit/meron_spacetime_finite_checks.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/open_derivations/meron_spacetime_limit/meron_spacetime_finite_checks.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/open_derivations/meron_spacetime_limit/meron_spacetime_finite_checks.py)
- sha256 (`bytes`): `1da2df9c0b6fed4b735286cc782df54bf3abcd6692c5742e410bff5cd3a4fe9e`
- cited in: record TFQ-0582

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `layer_transfer` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/meron_field_limit_derivations/README.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/meron_field_limit_derivations/README.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/meron_field_limit_derivations/README.md)
- sha256 (`lf-normalised`): `ce2465556f7ae8df7f142f69227596b99164f48968e97ad7b746599c9215d602`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0582_wdp_meron_m1_correlation_estimates.md`

- file: [dag/derivations/06_wdp/tfq_0582_wdp_meron_m1_correlation_estimates.md](../../../dag/derivations/06_wdp/tfq_0582_wdp_meron_m1_correlation_estimates.md)
- sha256 (`lf-normalised`): `0a911285a7170253d96c606845073fcdd0d17403fb773c57271ea94b628fd076`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0582
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0582 rust: joint (L, M) thermodynamic correlation bound is an open analytic target

## Routes

Incoming (1):

- `PGW-R-WDP-MERON-M1-CORRELATION-ESTIMATES` `GAP_NO_DERIVATION`: [PGW-WDP-AFFINE-THICKENING-CONJECTURE](PGW-WDP-AFFINE-THICKENING-CONJECTURE.md) (OPEN), [PGW-WDP-BRIDGE-O04-TENSOR-RECONSTRUCTION](PGW-WDP-BRIDGE-O04-TENSOR-RECONSTRUCTION.md) (OPEN)

Outgoing (2):

- `PGW-R-WDP-MERON-M2-CUMULANT-BOUNDS` `GAP_NO_DERIVATION`: [PGW-WDP-MERON-M2-CUMULANT-BOUNDS](PGW-WDP-MERON-M2-CUMULANT-BOUNDS.md) (OPEN)
- `PGW-R-WDP-MERON-SPACETIME-LIMIT` `GAP_NO_DERIVATION`: [PGW-WDP-MERON-SPACETIME-LIMIT](PGW-WDP-MERON-SPACETIME-LIMIT.md) (OPEN)
