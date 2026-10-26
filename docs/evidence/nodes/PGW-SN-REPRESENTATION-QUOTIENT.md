# PGW-SN-REPRESENTATION-QUOTIENT

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In a supplied complex model with one coordinate at each of two sites, the balance map T sends the ordinary tensor coefficients (rr, ri, ir, ii) to (rr − ii, ri + ir), so for m = n = 1 its rows are (1,0,0,−1) and (0,1,1,0). With u = Tᵗ/2 and r = T, r u = I₂ while u r = P = TᵗT/2 is a rank-2 idempotent, and the vector (1,0,0,1) lies in ker T, so P ≠ I₄. The exact kernel of T is the complex balancing relation. The reading guide uses this as a representation quotient: it names the declared questions that survive and the information quotiented away, and it supplies no native S(n) obstruction.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared complex scalars and tensor coordinates of the WDP realification supplement (assumption)

## Bottleneck

Lean states integer coefficient laws (balance after section is doubling, and the kernel test rr = ii, ri = −ir); division by 2 and positivity are written separately. A lawful representation of the selected quantum composite gives neither a new native S(n) obstruction nor permission to advance beyond S(6).

## Source status

WDP docs/complex_tensor_balancing.md Theorem 1; 002_oesn reading_guide.md representation quotient; Lean ComplexTensorBalancing

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/ComplexTensorBalancing.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/ComplexTensorBalancing.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/ComplexTensorBalancing.lean)
- sha256 (`bytes`): `562e6c759f9bbd7546ad5e6586a52af685f1890d5f9ee54aa9748c732acbe0ac`
- cited in: node.lean, record TFQ-0521
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mssn_sn.json](../../../dag/research/lean_replay_campaign_mssn_sn.json) (module `Imported.WitnessedDifference.WitnessedDifference.ComplexTensorBalancing`): recorded sha256 `562e6c759f9bbd7546ad5e6586a52af685f1890d5f9ee54aa9748c732acbe0ac` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/ComplexTensorBalancing.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `balance_kernel_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms balance_kernel_iff` |
| `balance_section` | yes | yes | yes | Quot.sound, propext | `#print axioms balance_section` |
| `twice_project_square` | yes | yes | yes | Quot.sound, propext | `#print axioms twice_project_square` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_linear_algebra/src/exact_field/complex_tensor.rs`

- file: `omega_engine/crates_rs/omega_linear_algebra/src/exact_field/complex_tensor.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0521_sn_representation_quotient.md`

- file: [dag/derivations/05_mssn_sn/tfq_0521_sn_representation_quotient.md](../../../dag/derivations/05_mssn_sn/tfq_0521_sn_representation_quotient.md)
- sha256 (`lf-normalised`): `175a9094a1d0add0f69661d374334d90a3bda8c0cd6fbfd6244b2163da7ce373`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0521
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/complex_tensor_balancing.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/complex_tensor_balancing.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/002_oesn/reading_guide.md`

- file: `omega_engine_education/documentation/002_oesn/reading_guide.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:upstream/omega_engine/crates_rs/omega_linear_algebra/src/exact_field/complex_tensor.rs::balance_map_with_limits`
- `external:upstream/omega_engine/crates_rs/omega_linear_algebra/src/exact_field/complex_tensor.rs::balance_projector_with_limits`

## Absences recorded by the TFQ records

- TFQ-0521 python: no Python check of the balance map in the S(n) strand

## Routes

Incoming (1):

- `PGW-R-SN-REPRESENTATION-QUOTIENT` `DERIVED_LEAN`: [PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL](PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL.md) (PROVED_LEAN)

Outgoing (0):

