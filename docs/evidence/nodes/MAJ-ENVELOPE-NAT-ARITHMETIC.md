# MAJ-ENVELOPE-NAT-ARITHMETIC

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Over Nat: products and sums of positive naturals are positive, p \> 0 gives p + 2 \> 0, p \> q gives p + 2 \> q + 2, M \>= 4 gives M (M - 1) / 2 \> 0, and a \> b gives a - b \> 0.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 11
- cited Lean declaration references covered by a current replay receipt: 11
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

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
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_majorana.json](../../../dag/research/lean_replay_campaign_majorana.json) (module `papers.core.majorana.lean4.MajoranaCore`): recorded sha256 `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `disorder_gap_degradation_lower_bound` | yes | yes | yes | Quot.sound, propext | `#print axioms disorder_gap_degradation_lower_bound` |
| `multiterminal_crosstalk_channels_pos` | yes | yes | yes | Quot.sound, propext | `#print axioms multiterminal_crosstalk_channels_pos` |
| `multiterminal_pareto_defect_pos` | yes | yes | yes | Quot.sound, propext | `#print axioms multiterminal_pareto_defect_pos` |
| `multiterminal_transfer_defect_pos` | yes | yes | yes | none | `#print axioms multiterminal_transfer_defect_pos` |
| `non_markovian_pareto_defect_pos` | yes | yes | yes | Quot.sound, propext | `#print axioms non_markovian_pareto_defect_pos` |
| `non_markovian_transfer_defect_pos` | yes | yes | yes | none | `#print axioms non_markovian_transfer_defect_pos` |
| `pareto_denominator_pos` | yes | yes | yes | Quot.sound, propext | `#print axioms pareto_denominator_pos` |
| `sub_ohmic_exponent_shift` | yes | yes | yes | Quot.sound, propext | `#print axioms sub_ohmic_exponent_shift` |
| `transfer_defect_lower_bound_pos` | yes | yes | yes | none | `#print axioms transfer_defect_lower_bound_pos` |
| `transfer_gap_strictly_positive` | yes | yes | yes | none | `#print axioms transfer_gap_strictly_positive` |
| `transfer_pareto_defect_pos` | yes | yes | yes | Quot.sound, propext | `#print axioms transfer_pareto_defect_pos` |

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

