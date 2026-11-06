# PGW-WDP-MERON-M3-SPECTRAL-GAP-BYPASS

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Meron Field-Limit Target M3: establish the all-M transfer-matrix spectral gap statement or prove that the fixed-carrier response theorem bypasses all-M spectral separation.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Open target; Gate E refutes naive finite-M positivity at a specific parameter point, so any spectral or bypass argument must respect that obstruction.

## Source status

Meron Target M3 open in docs/02_requiring_derivation/meron_field_limit_derivations/README.md

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13.lean)
- sha256 (`bytes`): `a963d75f41109cf2955ef9129b6aceee3d2edc0203995d36d457bffc366b747a`
- cited in: node.lean, record TFQ-0584
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch13.m3_margin_positivity_bypass` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch13.m3_margin_positivity_bypass` |
| `WitnessedDifference.WdpBatch13.wdp_meron_m3_gate_e_obstruction_and_margin_bypass` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch13.wdp_meron_m3_gate_e_obstruction_and_margin_bypass` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13Rep.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13Rep.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13Rep.lean)
- sha256 (`bytes`): `6975782b2e706d331e81b6ee766fba2b94bf25cff0e66a2af837a49b8863635c`
- cited in: node.lean, record TFQ-0584
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13Rep.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch13Rep.wdp_meron_m3_gate_e_obstruction_and_margin_bypass` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch13Rep.wdp_meron_m3_gate_e_obstruction_and_margin_bypass` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/meron_field_limit_derivations/code/gate_e_exact_counterexample.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/meron_field_limit_derivations/code/gate_e_exact_counterexample.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/meron_field_limit_derivations/code/gate_e_exact_counterexample.py)
- sha256 (`bytes`): `6bc13e77d4615e1b8150cad5f34bbc9d3ef461301145a65a06ba14613e4b2003`
- cited in: record TFQ-0584

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/meron_field_limit_derivations/README.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/meron_field_limit_derivations/README.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/meron_field_limit_derivations/README.md)
- sha256 (`lf-normalised`): `ce2465556f7ae8df7f142f69227596b99164f48968e97ad7b746599c9215d602`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0584_wdp_meron_m3_spectral_gap_bypass.md`

- file: [dag/derivations/06_wdp/tfq_0584_wdp_meron_m3_spectral_gap_bypass.md](../../../dag/derivations/06_wdp/tfq_0584_wdp_meron_m3_spectral_gap_bypass.md)
- sha256 (`lf-normalised`): `9b971f9a745222cb02a978293874f4f940e69e1b0d23126feb1c703eaa508de3`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0584
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0584 lean4: all-M spectral gap or bypass theorem is open
- TFQ-0584 rust: no Rust certifier for all-M transfer spectrum yet

## Routes

Incoming (1):

- `PGW-R-WDP-MERON-M3-SPECTRAL-GAP-BYPASS` `DERIVED_LEAN`: [PGW-WDP-MERON-M2-CUMULANT-BOUNDS](PGW-WDP-MERON-M2-CUMULANT-BOUNDS.md) (PROVED_LEAN)

Outgoing (2):

- `PGW-R-WDP-MERON-M4-NATIVE-ADAPTERS` `DERIVED_LEAN`: [PGW-WDP-MERON-M4-NATIVE-ADAPTERS](PGW-WDP-MERON-M4-NATIVE-ADAPTERS.md) (PROVED_LEAN)
- `PGW-R-WDP-MERON-SPACETIME-LIMIT` `DERIVED_LEAN`: [PGW-WDP-MERON-SPACETIME-LIMIT](PGW-WDP-MERON-SPACETIME-LIMIT.md) (PROVED_LEAN)
