# PGW-WDP-FAILED-SAMENESS

Stage: [WDP](../stages/WDP.md). Status: `PROVED_PROSE`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> WDP-CH01-P01: within a fixed comparison family K, a failed declared sameness comparison Same_K(p, q) = 0 exhibits that the two compared presentations are not interchangeable under that comparison. The statement is local: it does not say the presentations differ under every comparison, does not make the failure intrinsic to the tokens, and supplies no order. A failed comparison is a residual at the level of predicates; encoding it as p − q is a stronger step that presupposes subtraction, scalars and a zero.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared comparison family K and sameness predicate Same_K on presentations (assumption)

## Bottleneck

Local to the declared comparison; it orders nothing, says nothing about other comparisons, and the ledger binds it to prose plus the Python ground.py check with no Lean declaration.

## Source status

WDP monograph §1.2 WDP-CH01-P01 finite proposition (prose; Python ground.py)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_exact_ground_outcomes.py`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_exact_ground_outcomes.py](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_exact_ground_outcomes.py)
- sha256 (`bytes`): `9ca5d16f10b21ab8f112233a29f3239b7cf38fa7eae04a23b000d2cd56c0611e`
- cited in: record TFQ-0536
- check: `python -m pytest atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_exact_ground_outcomes.py::test_primitive_difference_and_triangle_identity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_primitive_difference_and_triangle_identity` (python_test) | yes | yes | yes | - | `python -m pytest atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_exact_ground_outcomes.py::test_primitive_difference_and_triangle_identity` |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/ground.py`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/ground.py](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/ground.py)
- sha256 (`bytes`): `9e0f14edbfb258210fbb6e7e77ca1aca2464b8aaa38e3949c9a92d91952f961d`
- cited in: record TFQ-0536

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `primitive_difference` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md)
- sha256 (`lf-normalised`): `753d1c99c799f84f9a71912b98082d590c89c531f980c112b62ee2a86ab2726b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0536_wdp_failed_sameness.md`

- file: [dag/derivations/06_wdp/tfq_0536_wdp_failed_sameness.md](../../../dag/derivations/06_wdp/tfq_0536_wdp_failed_sameness.md)
- sha256 (`lf-normalised`): `41cc2d041bf8a53a53d36f615ce2ca304d8beb9fb185bce4dba315a25d635484`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0536
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:39e988784c38613df38c5f88b06efee27f73f0a7a02b8069458d6e2168e498b8::primitive_difference`
- `external:sha256:b3182646c084a1d31b4c382572524489dcfa76f74bf74ee0863573424d048c65:111-123`
- `external:upstream/external:sha256:39e988784c38613df38c5f88b06efee27f73f0a7a02b8069458d6e2168e498b8::primitive_difference`

## Absences recorded by the TFQ records

- TFQ-0536 lean4: the claim map lists WDP-CH01-P01 as prose-only; no Lean declaration states it

## Routes

Incoming (1):

- `PGW-R-WDP-FAILED-SAMENESS` `DERIVED_PROSE`: [PG-ADMISSION-FLOOR](PG-ADMISSION-FLOOR.md) (PROVED_LEAN)

Outgoing (2):

- `PGW-R-WDP-ASYMMETRY-INJECTION-LEDGER` `DERIVED_PROSE`: [PGW-WDP-ASYMMETRY-INJECTION-LEDGER](PGW-WDP-ASYMMETRY-INJECTION-LEDGER.md) (DEFINITION)
- `PGW-R-WDP-QUOTIENT-DEFECT-ROOT-P` `DERIVED_PROSE`: [PGW-WDP-QUOTIENT-DEFECT-ROOT-P](PGW-WDP-QUOTIENT-DEFECT-ROOT-P.md) (DEFINITION)
