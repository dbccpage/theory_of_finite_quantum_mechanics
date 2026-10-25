# PGW-SN-E20-OBSERVER-COMPLETION

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_PROSE`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Example E20 works over V = ℚ³ with B = im d₀ = ker I. For linear Q: V → W with K = ker Q, the induced map V/B → W/Q(B) has kernel (B + K)/B ≅ K/(K ∩ B), so quotient observation is injective exactly when K ⊆ B. The defective observer Q_bad(x) = x₁ hides z = (0,1,0), which has Q_bad(z) = 0 and I(z) = 1. Adding the coordinate I(x) gives Q_complete(x) = (x₁, I(x)) with kernel {(0,t,−t)} ⊆ B; the hidden part K/(K ∩ B) has dimension 1 while ker Q_bad has dimension 2, so one added linear functional is necessary and sufficient, and the first projection recovers x₁.

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

- `proved_prose_no_in_repo_document`: no in-repo non-generated document among the counted sources. PROVED_PROSE with no in-repo source document cited.

## Imported structure

None recorded.

## Bottleneck

Linear observers on ℚ³ only; it does not treat nonlinear measurement maps or noise, and the page is a written finite example that grammar cases do not verify.

## Source status

002_oesn levels/level_20 (E20 written finite example); curriculum.md Lesson 8

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0526_sn_e20_observer_completion.md`

- file: [dag/derivations/05_mssn_sn/tfq_0526_sn_e20_observer_completion.md](../../../dag/derivations/05_mssn_sn/tfq_0526_sn_e20_observer_completion.md)
- sha256 (`lf-normalised`): `a1cf22a06fbdd47bbb37ba53843f311901795d838f426fb86d7e8bcfbc820725`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0526
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/002_oesn/curriculum.md`

- file: `omega_engine_education/documentation/002_oesn/curriculum.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/002_oesn/levels/level_20_autopoietic_reflection.md`

- file: `omega_engine_education/documentation/002_oesn/levels/level_20_autopoietic_reflection.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0526 lean4: no Lean statement of E20 in the S(n) strand
- TFQ-0526 python: no Python check of E20 in the S(n) strand
- TFQ-0526 rust: no Rust check of E20 in the S(n) strand

## Routes

Incoming (1):

- `PGW-R-SN-E20-OBSERVER-COMPLETION` `DERIVED_PROSE`: [PGW-SN-E12-CIRCULATION-FUNCTIONAL](PGW-SN-E12-CIRCULATION-FUNCTIONAL.md) (PROVED_LEAN)

Outgoing (0):

