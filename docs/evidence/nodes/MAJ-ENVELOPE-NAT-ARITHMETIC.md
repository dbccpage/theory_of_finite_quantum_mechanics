# MAJ-ENVELOPE-NAT-ARITHMETIC

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Over Nat: products and sums of positive naturals are positive, p \> 0 gives p + 2 \> 0, p \> q gives p + 2 \> q + 2, M \>= 4 gives M (M - 1) / 2 \> 0, and a \> b gives a - b \> 0.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 11
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 11 Lean reference(s) cited, 11 in this checkout (replay: none 11). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

These lemmas do not bear on any physical envelope; MAJ-C18..C20 stay open.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-LEAN-ENVELOPE-NAT claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/majorana/lean4/MajoranaCore.lean`

- file: [papers/core/majorana/lean4/MajoranaCore.lean](../../../papers/core/majorana/lean4/MajoranaCore.lean)
- sha256 (`bytes`): `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071`
- cited in: node.lean, record TFQ-1180
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `disorder_gap_degradation_lower_bound` | yes | yes | yes | - | `#print axioms disorder_gap_degradation_lower_bound` |
| `multiterminal_crosstalk_channels_pos` | yes | yes | yes | - | `#print axioms multiterminal_crosstalk_channels_pos` |
| `multiterminal_pareto_defect_pos` | yes | yes | yes | - | `#print axioms multiterminal_pareto_defect_pos` |
| `multiterminal_transfer_defect_pos` | yes | yes | yes | - | `#print axioms multiterminal_transfer_defect_pos` |
| `non_markovian_pareto_defect_pos` | yes | yes | yes | - | `#print axioms non_markovian_pareto_defect_pos` |
| `non_markovian_transfer_defect_pos` | yes | yes | yes | - | `#print axioms non_markovian_transfer_defect_pos` |
| `pareto_denominator_pos` | yes | yes | yes | - | `#print axioms pareto_denominator_pos` |
| `sub_ohmic_exponent_shift` | yes | yes | yes | - | `#print axioms sub_ohmic_exponent_shift` |
| `transfer_defect_lower_bound_pos` | yes | yes | yes | - | `#print axioms transfer_defect_lower_bound_pos` |
| `transfer_gap_strictly_positive` | yes | yes | yes | - | `#print axioms transfer_gap_strictly_positive` |
| `transfer_pareto_defect_pos` | yes | yes | yes | - | `#print axioms transfer_pareto_defect_pos` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1180_maj_envelope_nat_arithmetic.md`

- file: [dag/derivations/28_majorana/tfq_1180_maj_envelope_nat_arithmetic.md](../../../dag/derivations/28_majorana/tfq_1180_maj_envelope_nat_arithmetic.md)
- sha256 (`lf-normalised`): `53e938fbbc4491cf8ede3b4974af5d40c1958e833fa0d02d2159dc1539d3a99f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1180
- counts toward the grade: no

### Documents and data: `papers/core/majorana/lean4/axiom_report.txt`

- file: [papers/core/majorana/lean4/axiom_report.txt](../../../papers/core/majorana/lean4/axiom_report.txt)
- sha256 (`lf-normalised`): `ec4465011fdd2b18f2c9df263004e9050f8c394dece1841835ff0bcd1e00df79`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `e92416bb1739e51de20a8ad6a26d4b5f3d76b974d7556507b13149b29e8edb47`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-ENVELOPE-NAT-ARITHMETIC` `DERIVED_LEAN`: [MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE](MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE.md) (OPEN)

Outgoing (0):

