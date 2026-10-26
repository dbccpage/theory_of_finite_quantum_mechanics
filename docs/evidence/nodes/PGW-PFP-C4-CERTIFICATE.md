# PGW-PFP-C4-CERTIFICATE

Stage: [IMPLEMENTATION](../stages/IMPLEMENTATION.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On the supplied oriented 4-cycle with vertices 0 to 3, edges 01, 12, 23, 03 in that order, one declared face 01+12+23−03 and c = (2, −3, 5, 7), the potential a = (0, 2, −1, 4) gives d₀a = (2, −3, 5, 4) and residual r = (0, 0, 0, 3) with L1 norm 3, an upper bound. The dual w = (−1, −1, −1, 1) is feasible (max |wᵢ| = 1 and d₀ᵀw = 0 at all four vertices) with w·c = 3, so every potential leaves L1 cost at least 3 and φ₁ = 3. The face row d₁ = (1, 1, 1, −1) satisfies d₁d₀ = 0 and d₁c = −3, so γ₂ = 3. The fixture c4_public_input.json carries this complex, and test_native_certificate_positive_and_decisive_mutations checks the certificate through the native Rust checker, rejects a +1 change to each answer field and accepts a constant shift of the potential; it passed in the recorded receipt of 2026-10-19 (2 passed, 0 failed).

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- Supplied oriented C4 complex, L1 edge norm and rational coefficients, as declared in c4_work_unit.json (assumption)

## Bottleneck

A finite certificate for one supplied complex: φ₁ = γ₂ here does not hold on all complexes or norms, and neither the certificate nor a schema check supplies a Hilbert space, a Born rule or an authorization.

## Source status

004_oepfp level_finite_qm_certificate_walkthrough.md; omega_engine_pfp fixture c4_public_input.json; native test receipt batch_13 c4_native_actual.json (2 passed)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `omega_engine/crates_rs/omega_symbol_game_runtime/src/cochain.rs`

- file: `omega_engine/crates_rs/omega_symbol_game_runtime/src/cochain.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/04_authorization/tfq_0509_pfp_c4_certificate.md`

- file: [dag/derivations/04_authorization/tfq_0509_pfp_c4_certificate.md](../../../dag/derivations/04_authorization/tfq_0509_pfp_c4_certificate.md)
- sha256 (`lf-normalised`): `f552ade72d0b6a21330f1f877522ee5211d05ce2295f7b730045143d1f591638`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0509
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/004_oepfp/levels/level_finite_qm_certificate_walkthrough.md`

- file: `omega_engine_education/documentation/004_oepfp/levels/level_finite_qm_certificate_walkthrough.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_pfp/fixtures/finite_qm_workflow/c4_public_input.json`

- file: `omega_engine_pfp/fixtures/finite_qm_workflow/c4_public_input.json`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_product_planning_office/plans/review_remediation/evidence/batch_13/c4_native_actual.json`

- file: `omega_engine_product_planning_office/plans/review_remediation/evidence/batch_13/c4_native_actual.json`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:upstream/omega_engine/crates_rs/omega_symbol_game_runtime/src/cochain.rs::PromptCochainEvaluator`
- `external:upstream/omega_engine_pfp/infrastructure/finite_qm_cochain_judge.py::NativeCochainJudge`
- `external:upstream/omega_engine_pfp/tests/finite_qm_workflow/test_finite_qm_reference_workflow.py::test_native_certificate_positive_and_decisive_mutations`

## Absences recorded by the TFQ records

- TFQ-0509 lean4: no Lean statement of the C4 optimum

## Routes

Incoming (1):

- `PGW-R-PFP-C4-CERTIFICATE` `COMPUTED`: [TFQ-0508](TFQ-0508.md) (DEFINITION)

Outgoing (0):

