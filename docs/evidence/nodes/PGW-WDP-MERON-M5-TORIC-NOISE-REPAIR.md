# PGW-WDP-MERON-M5-TORIC-NOISE-REPAIR

Stage: [WDP](../stages/WDP.md). Status: `OPEN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Meron Field-Limit Target M5: repair Chapter 23 toric-code kernel, restricted-error rank, and adaptivity claims under explicit finite detector and noise-support hypotheses.

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

Open finite-lattice target in meron_field_limit_derivations/README.md; unrestricted toric-code adaptivity claims are fenced in Chapter 23.

## Source status

Meron Target M5 open in docs/02_requiring_derivation/meron_field_limit_derivations/README.md

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

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
- sha256 (`lf-normalised`): `dd0b2455b50114a7468787fa7d94656d0ee5475a82338afa0bc6536fafb18280`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0586
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0586 lean4: Lean 4 formalization of Chapter 23 restricted-error toric-code rank bound is open
- TFQ-0586 rust: checked by Python toric boundary witness

## Routes

Incoming (1):

- `PGW-R-WDP-MERON-M5-TORIC-NOISE-REPAIR` `GAP_NO_DERIVATION`: [PGW-WDP-MERON-M4-NATIVE-ADAPTERS](PGW-WDP-MERON-M4-NATIVE-ADAPTERS.md) (OPEN)

Outgoing (1):

- `PGW-R-WDP-MERON-SPACETIME-LIMIT` `GAP_NO_DERIVATION`: [PGW-WDP-MERON-SPACETIME-LIMIT](PGW-WDP-MERON-SPACETIME-LIMIT.md) (OPEN)
