# PGW-SN-E08-WEIGHTED-L1-DUALITY

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `CONDITIONAL`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Example E08 takes finite rational cochain spaces, d₀: C⁰ → C¹ and positive rational weights ω_e, and states that the minimum over g of Σ_e ω_e |c_e − (d₀g)_e| equals the maximum of cᵀy subject to d₀ᵀy = 0 and |y_e| ≤ ω_e, as finite linear-programming duality for the stated feasible bounded problem. Matching primal and dual feasible values certify optimality. An ℓ¹ minimizer need not be unique and is not in general the ℓ² harmonic residual. The page separately defines a categorical adjunction by functors, unit, counit and triangle identities, and says these maps are not the matrix pair d₀, d₀ᵀ.

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

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Strong duality for finite feasible bounded linear programs over ℚ, cited by E08 and not proved there (assumption)

## Bottleneck

E08 is a declared mathematical construction that grammar cases do not verify; AdjunctionCochain implements only x ↦ (x,0) and first-coordinate projection, and no adjunction is claimed until objects, functors, naturality and triangle laws are supplied.

## Source status

002_oesn levels/level_08 (declared construction; LP duality cited)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0522_sn_e08_weighted_l1_duality.md`

- file: [dag/derivations/05_mssn_sn/tfq_0522_sn_e08_weighted_l1_duality.md](../../../dag/derivations/05_mssn_sn/tfq_0522_sn_e08_weighted_l1_duality.md)
- sha256 (`lf-normalised`): `b8f03c987eb676a7ecd0663344870966f6d0fa63ad6ecb87e3139e70f22a626b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0522
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/002_oesn/levels/README.md`

- file: `omega_engine_education/documentation/002_oesn/levels/README.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/002_oesn/levels/level_08_monadic_adjunction_cochains.md`

- file: `omega_engine_education/documentation/002_oesn/levels/level_08_monadic_adjunction_cochains.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0522 lean4: no Lean statement of the weighted l1 duality in the S(n) strand
- TFQ-0522 python: AdjunctionCochain in sn_realizations.py implements a product section and projection, not this linear program
- TFQ-0522 rust: no Rust LP solver in the S(n) strand; the page assigns evaluation to existing mathematics owners

## Routes

Incoming (1):

- `PGW-R-SN-E08-WEIGHTED-L1-DUALITY` `CONDITIONAL_ON_IMPORT`: [PGW-SN4-POLICY-CLOSURE-CYCLE-SPACE](PGW-SN4-POLICY-CLOSURE-CYCLE-SPACE.md) (PROVED_PROSE)

Outgoing (3):

- `PGW-R-SN-E12-CIRCULATION-FUNCTIONAL` `DERIVED_LEAN`: [PGW-SN-E12-CIRCULATION-FUNCTIONAL](PGW-SN-E12-CIRCULATION-FUNCTIONAL.md) (PROVED_LEAN)
- `PGW-R-SN-E18-L1-TIES-L2-CENTER` `DERIVED_PROSE`: [PGW-SN-E18-L1-TIES-L2-CENTER](PGW-SN-E18-L1-TIES-L2-CENTER.md) (PROVED_PROSE)
- `PGW-R-WDP-PHI-WELL-DEFINED-L1-DUALITY` `CONDITIONAL_ON_IMPORT`: [PGW-WDP-PHI-WELL-DEFINED-L1-DUALITY](PGW-WDP-PHI-WELL-DEFINED-L1-DUALITY.md) (CONDITIONAL)
