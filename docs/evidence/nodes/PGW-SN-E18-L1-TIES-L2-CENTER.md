# PGW-SN-E18-L1-TIES-L2-CENTER

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_PROSE`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Example E18 keeps the unfilled triangle with x = (1,0,0) and I(x) = 1, so every residual r = x − d₀g has I(r) = 1. Under ℓ¹ the bound ‖r‖₁ ≥ |I(r)| = 1 is attained by r = (1,0,0) and by ties such as (1/2,1/2,0), with dual certificate y = (1,1,1) satisfying d₀ᵀy = 0, ‖y‖∞ ≤ 1 and xᵀy = 1. Under ℓ² over ℚ, Σ(r_i − 1/3)² = ‖r‖₂² − 1/3 ≥ 0 gives the unique minimizer h = (1/3,1/3,1/3) with squared norm 1/3, from g = (0,2/3,1/3) with x = d₀g + h and d₀ᵀh = 0. Both optimal representatives keep I = 1: optimization selects a representative and does not remove the obstruction.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

- `proved_prose_no_in_repo_document`: no in-repo non-generated document among the counted sources. PROVED_PROSE with no in-repo source document cited.

## Imported structure

- Standard inner product on ℚ³ as the declared ℓ² structure (assumption)

## Bottleneck

A written finite example: grammar cases SN_001 to SN_085 check spelling only and do not verify it, DiscreteHodge.verify_dimension_sum checks dimension arithmetic and is not a Hodge decomposition, and adjoining a 2-face changes the complex instead of supplying a potential.

## Source status

002_oesn levels/level_18 (E18 written finite example)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0524_sn_e18_l1_ties_l2_center.md`

- file: [dag/derivations/05_mssn_sn/tfq_0524_sn_e18_l1_ties_l2_center.md](../../../dag/derivations/05_mssn_sn/tfq_0524_sn_e18_l1_ties_l2_center.md)
- sha256 (`lf-normalised`): `1ed6897c4c8f997a8cccba7ff3d1d7260ac4fccf753108d256fb502b60828059`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0524
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/002_oesn/levels/level_18_discrete_hodge_decomposition.md`

- file: `omega_engine_education/documentation/002_oesn/levels/level_18_discrete_hodge_decomposition.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0524 lean4: no Lean statement of the l1 ties or the l2 minimizer for E18
- TFQ-0524 python: DiscreteHodge in sn_realizations.py checks a dimension sum only, not this example
- TFQ-0524 rust: no Rust check of E18 in the S(n) strand

## Routes

Incoming (1):

- `PGW-R-SN-E18-L1-TIES-L2-CENTER` `DERIVED_PROSE`: [PGW-SN-E08-WEIGHTED-L1-DUALITY](PGW-SN-E08-WEIGHTED-L1-DUALITY.md) (CONDITIONAL)

Outgoing (0):

