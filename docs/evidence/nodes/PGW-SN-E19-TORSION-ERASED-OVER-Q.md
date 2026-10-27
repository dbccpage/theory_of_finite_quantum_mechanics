# PGW-SN-E19-TORSION-ERASED-OVER-Q

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_PROSE`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Example E19 takes the free chain complex C₂ = ℤ → C₁ = ℤ → C₀ = ℤ with ∂₂(1) = 2 and ∂₁ = 0. The cycle z = 1 is nonzero in H₁ = ℤ/2 because no integer c has 2c = 1. After tensoring with ℚ, ∂₂(1/2) = 1, so H₁(C;ℚ) = 0, but the rational primitive 1/2 is not an integral repair witness. Adjoining one integer generator f with ∂₂f = 1 removes the class over ℤ at a cost of one new generator, against zero new generators for the coefficient change; replacing 2 by m ≥ 2 gives H₁ = ℤ/m over ℤ and 0 over ℚ.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_prose_no_in_repo_document`: no in-repo non-generated document among the counted sources. PROVED_PROSE with no in-repo source document cited.

## Imported structure

None recorded.

## Bottleneck

Erasing a class by changing coefficients supplies no integral repair, and a rational fraction 1/m offered as an integral repair receipt is refused; the page is a written finite example that grammar cases do not verify, and compute_integral_homology computes torsion factors for supplied integer matrices without a recorded run of this complex.

## Source status

002_oesn levels/level_19 (E19 written finite example); curriculum.md Lesson 7

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `education/minimal_symbol_systems/code/rust/src/smith_normal_form.rs`

- file: [education/minimal_symbol_systems/code/rust/src/smith_normal_form.rs](../../../education/minimal_symbol_systems/code/rust/src/smith_normal_form.rs)
- sha256 (`bytes`): `78cf459f4d860074ecad10cffdc415f211995b06e002bf7dd61f7bed216e0278`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `compute_integral_homology` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0525_sn_e19_torsion_erased_over_q.md`

- file: [dag/derivations/05_mssn_sn/tfq_0525_sn_e19_torsion_erased_over_q.md](../../../dag/derivations/05_mssn_sn/tfq_0525_sn_e19_torsion_erased_over_q.md)
- sha256 (`lf-normalised`): `18c708aef9f7e580fac876277e3868baba1c45a99949a869f5906a4115c71a30`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0525
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:5aef105ec34fddc0f0092687564bcbbf1a27ccde32e756b3050c2edbb23b6e9d:46-49`
- `external:sha256:5aef105ec34fddc0f0092687564bcbbf1a27ccde32e756b3050c2edbb23b6e9d:51-54`
- `external:sha256:a51ceb8d0d5703baac230c14caa4638cf25f3ae46fdc77013c7e09f27caaa1e9:146-147`
- `external:upstream/education/minimal_symbol_systems/code/rust/src/smith_normal_form.rs::compute_integral_homology`

## Absences recorded by the TFQ records

- TFQ-0525 lean4: no Lean statement of E19; MssnSmithNormalForm.lean checks supplied invariant-factor records only
- TFQ-0525 python: no Python check of E19 in the S(n) strand

## Routes

Incoming (1):

- `PGW-R-SN-E19-TORSION-ERASED-OVER-Q` `DERIVED_PROSE`: [PGW-SN-E12-CIRCULATION-FUNCTIONAL](PGW-SN-E12-CIRCULATION-FUNCTIONAL.md) (PROVED_LEAN)

Outgoing (0):

