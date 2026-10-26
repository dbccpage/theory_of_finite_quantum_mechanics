# FSP-RATIONAL-QUOTIENT-NORMAL-FORM

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `PROVED_PROSE`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For d0 in Q^{m x n} and W = im d0, N_W(x) = x - sum_i x_{p_i} r_i (nonzero RREF rows r_i of d0^T with pivots p_i) is sound, idempotent and complete for x ~ y iff x - y in W, and is independent of the generating matrix; Lean checks the three laws for the fixed integral image span(1, 2) in Z^2.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 3
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- fixed rational coboundary matrix d0 and coordinate order

## Bottleneck

N_W is not an l1 minimizer (span(1,2), x = (1,0) gives norm 2 versus 1); the quotient norm is a separate exact linear program with a refusal budget (NF-003). A valid YAML contract or routing label is not a normalizer.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-030 claims PROVED_LEAN; audited status PROVED_PROSE

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/fsp/lean4/NormalFormLaws.lean`

- file: [papers/core/fsp/lean4/NormalFormLaws.lean](../../../papers/core/fsp/lean4/NormalFormLaws.lean)
- sha256 (`bytes`): `dc82b0698c3db4b4e7d61b75c69f150910e89a71cbfe6a14dcfec046b8e76021`
- cited in: node.lean, record TFQ-1195
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains papers/core/fsp/lean4/NormalFormLaws.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `integral_complete` | yes | yes | yes | - | `#print axioms integral_complete` |
| `integral_idempotent` | yes | yes | yes | - | `#print axioms integral_idempotent` |
| `integral_sound` | yes | yes | yes | - | `#print axioms integral_sound` |

- counts toward the grade: yes

### Python: `code/python/src/fsp/bqnf_sign_evaluator.py`

- file: [code/python/src/fsp/bqnf_sign_evaluator.py](../../../code/python/src/fsp/bqnf_sign_evaluator.py)
- sha256 (`bytes`): `6bbc7a71841797e537bf4f62308124325c6f39848c08ee914dfb96187f892f92`
- cited in: record TFQ-1195

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `normalize_cochain` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/tests/fsp/test_normal_form_laws.py`

- file: [code/python/tests/fsp/test_normal_form_laws.py](../../../code/python/tests/fsp/test_normal_form_laws.py)
- sha256 (`bytes`): `a8cd7a31a7c283efd112f89d8c2a12f4a258e8dbbe360247a50e72cb02da9aaa`
- cited in: record TFQ-1195

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_l1_section_is_not_l1_minimizer_and_exact_distance_is` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/fsp/test_normal_form_laws.py::test_l1_section_is_not_l1_minimizer_and_exact_distance_is` |
| `test_rational_completeness_against_independent_annihilator` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/fsp/test_normal_form_laws.py::test_rational_completeness_against_independent_annihilator` |
| `test_rational_section_soundness_idempotence_and_gauge_invariance` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/fsp/test_normal_form_laws.py::test_rational_section_soundness_idempotence_and_gauge_invariance` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1195_fsp_rational_quotient_normal_form.md`

- file: [dag/derivations/26_fsp/tfq_1195_fsp_rational_quotient_normal_form.md](../../../dag/derivations/26_fsp/tfq_1195_fsp_rational_quotient_normal_form.md)
- sha256 (`lf-normalised`): `568b2a1a7e5cd8e25364c89c5a888870c5f903d434db651ff1b41e3c9de5854d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1195
- counts toward the grade: no

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign.md)
- sha256 (`lf-normalised`): `f894f295fb17dc831f4e961602bea56223bf79ae6b34c3350cfa6fe358789808`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md)
- sha256 (`lf-normalised`): `0a97b32d187a99450605943866d6d4285f0bfd73dcc021c2b69911243066f2f3`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `5a72c2f6006ea18c3362f0a63e8525b65d41898e8f1bd437b7e4c2e368c7e102`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-RATIONAL-QUOTIENT-NORMAL-FORM` `DERIVED_PROSE`: [L1-WDP-WINDOW-PHI1-GAMMA2](L1-WDP-WINDOW-PHI1-GAMMA2.md) (DEFINITION), [FSP-SWITCHING-NORMAL-FORM](FSP-SWITCHING-NORMAL-FORM.md) (PROVED_LEAN)

Outgoing (0):

