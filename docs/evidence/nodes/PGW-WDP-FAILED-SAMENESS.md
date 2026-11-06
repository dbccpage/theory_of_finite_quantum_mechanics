# PGW-WDP-FAILED-SAMENESS

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> WDP-CH01-P01: within a fixed comparison family K, a failed declared sameness comparison Same_K(p, q) = 0 exhibits that the two compared presentations are not interchangeable under that comparison. The statement is local: it does not say the presentations differ under every comparison, does not make the failure intrinsic to the tokens, and supplies no order. A failed comparison is a residual at the level of predicates; encoding it as p − q is a stronger step that presupposes subtraction, scalars and a zero.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- Declared comparison family K and sameness predicate Same_K on presentations (assumption)

## Bottleneck

Local to the declared comparison; mechanized in Lean 4 (failed_sameness_not_interchangeable, failed_sameness_is_local, failed_sameness_supplies_no_order, algebraic_difference_separation in WdpBatch2.lean) and checked in Python ground.py.

## Source status

WDP monograph §1.2 WDP-CH01-P01 mechanized in Lean 4 (WdpBatch2.lean) and checked in Python ground.py

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch2.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch2.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch2.lean)
- sha256 (`bytes`): `b40aa3e8417cf931d7fe83e997f927c00648d0bcdced7873735a60f8212c0413`
- cited in: node.lean, record TFQ-0536
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch2.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch2.algebraic_difference_separation` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch2.algebraic_difference_separation` |
| `WitnessedDifference.WdpBatch2.failed_sameness_is_local` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch2.failed_sameness_is_local` |
| `WitnessedDifference.WdpBatch2.failed_sameness_not_interchangeable` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch2.failed_sameness_not_interchangeable` |
| `WitnessedDifference.WdpBatch2.failed_sameness_supplies_no_order` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch2.failed_sameness_supplies_no_order` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_exact_ground_outcomes.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_exact_ground_outcomes.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_exact_ground_outcomes.py)
- sha256 (`bytes`): `9ca5d16f10b21ab8f112233a29f3239b7cf38fa7eae04a23b000d2cd56c0611e`
- cited in: record TFQ-0536
- check: `python -m pytest atlas/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_exact_ground_outcomes.py::test_primitive_difference_and_triangle_identity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_primitive_difference_and_triangle_identity` (python_test) | yes | yes | yes | - | `python -m pytest atlas/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_exact_ground_outcomes.py::test_primitive_difference_and_triangle_identity` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/ground.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/ground.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/ground.py)
- sha256 (`bytes`): `9e0f14edbfb258210fbb6e7e77ca1aca2464b8aaa38e3949c9a92d91952f961d`
- cited in: record TFQ-0536

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `primitive_difference` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md)
- sha256 (`lf-normalised`): `753d1c99c799f84f9a71912b98082d590c89c531f980c112b62ee2a86ab2726b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0536_wdp_failed_sameness.md`

- file: [dag/derivations/06_wdp/tfq_0536_wdp_failed_sameness.md](../../../dag/derivations/06_wdp/tfq_0536_wdp_failed_sameness.md)
- sha256 (`lf-normalised`): `6e7d40182bb51fad7e350a18b67d95307b153b08d5fb48adbd976cd201b5c42e`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0536
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:39e988784c38613df38c5f88b06efee27f73f0a7a02b8069458d6e2168e498b8::primitive_difference`
- `external:sha256:b3182646c084a1d31b4c382572524489dcfa76f74bf74ee0863573424d048c65:111-123`
- `external:upstream/external:sha256:39e988784c38613df38c5f88b06efee27f73f0a7a02b8069458d6e2168e498b8::primitive_difference`

## Routes

Incoming (1):

- `PGW-R-WDP-FAILED-SAMENESS` `DERIVED_LEAN`: [PG-ADMISSION-FLOOR](PG-ADMISSION-FLOOR.md) (PROVED_LEAN)

Outgoing (3):

- `PGW-R-WD2-WORD-KERNEL-AGREEMENT` `DERIVED_LEAN`: [PGW-WD2-WORD-KERNEL-AGREEMENT](PGW-WD2-WORD-KERNEL-AGREEMENT.md) (PROVED_LEAN)
- `PGW-R-WDP-ASYMMETRY-INJECTION-LEDGER` `DERIVED_PROSE`: [PGW-WDP-ASYMMETRY-INJECTION-LEDGER](PGW-WDP-ASYMMETRY-INJECTION-LEDGER.md) (DEFINITION)
- `PGW-R-WDP-QUOTIENT-DEFECT-ROOT-P` `DERIVED_PROSE`: [PGW-WDP-QUOTIENT-DEFECT-ROOT-P](PGW-WDP-QUOTIENT-DEFECT-ROOT-P.md) (DEFINITION)
