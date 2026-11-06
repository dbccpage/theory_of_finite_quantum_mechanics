# PGW-WDP-MERON-M4-NATIVE-ADAPTERS

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Meron Field-Limit Target M4: on the 3-rung two-plaquette bond window, the explicit native syndrome-to-repair adapter clears every plaquette defect using a physical bond operator of weight at most 1 and recovers every single-bond fault, while distinct physical operators in the same quotient class have unequal support weights.

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

Mechanized in Lean 4 (meron_plaquette_syndrome_adapter_sound, meron_single_bond_exact_recovery, and meron_quotient_class_ne_physical_operator in WdpBatch6.lean alongside decoder_iff in LocalObservationCompletion.lean); physical laboratory actuation remains external.

## Source status

Meron Target M4 finite syndrome-to-repair adapter and quotient-vs-operator separation mechanized in LocalObservationCompletion.lean and WdpBatch6.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/LocalObservationCompletion.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/LocalObservationCompletion.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/LocalObservationCompletion.lean)
- sha256 (`bytes`): `1687f785167cc2bcf37b1d83ee245f45b65627a94cce3789d3b24abfbc522768`
- cited in: node.lean, record TFQ-0585
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/LocalObservationCompletion.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `decoder_iff` | yes | yes | yes | - | `#print axioms decoder_iff` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean)
- sha256 (`bytes`): `1bf7c1e971d501d47ce848a7d7c8149dd75542ace9fa09b229da2b5cc67f580c`
- cited in: node.lean, record TFQ-0585
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch6.meron_plaquette_syndrome_adapter_sound` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch6.meron_plaquette_syndrome_adapter_sound` |
| `WitnessedDifference.WdpBatch6.meron_quotient_class_ne_physical_operator` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch6.meron_quotient_class_ne_physical_operator` |
| `WitnessedDifference.WdpBatch6.meron_single_bond_exact_recovery` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch6.meron_single_bond_exact_recovery` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py)
- sha256 (`bytes`): `2c39d5d66e90bfe5675526a4018e66a8290aa1daef019fdaceb85c4326a356d1`
- cited in: record TFQ-0585

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `obstruction_signature` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/meron_field_limit_derivations/README.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/meron_field_limit_derivations/README.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/meron_field_limit_derivations/README.md)
- sha256 (`lf-normalised`): `ce2465556f7ae8df7f142f69227596b99164f48968e97ad7b746599c9215d602`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0585_wdp_meron_m4_native_adapters.md`

- file: [dag/derivations/06_wdp/tfq_0585_wdp_meron_m4_native_adapters.md](../../../dag/derivations/06_wdp/tfq_0585_wdp_meron_m4_native_adapters.md)
- sha256 (`lf-normalised`): `7e0be2763e4079481004ed97424f1bffb7d1de545fcd27ab425d9c57c35485ad`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0585
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0585 rust: checked in Lean 4 and Python obstruction signature witnesses

## Routes

Incoming (1):

- `PGW-R-WDP-MERON-M4-NATIVE-ADAPTERS` `DERIVED_LEAN`: [PGW-WDP-MERON-M3-SPECTRAL-GAP-BYPASS](PGW-WDP-MERON-M3-SPECTRAL-GAP-BYPASS.md) (OPEN), [PGW-WDP-BRIDGE-O02-OBSERVER-REPAIR](PGW-WDP-BRIDGE-O02-OBSERVER-REPAIR.md) (OPEN)

Outgoing (1):

- `PGW-R-WDP-MERON-M5-TORIC-NOISE-REPAIR` `DERIVED_LEAN`: [PGW-WDP-MERON-M5-TORIC-NOISE-REPAIR](PGW-WDP-MERON-M5-TORIC-NOISE-REPAIR.md) (PROVED_LEAN)
