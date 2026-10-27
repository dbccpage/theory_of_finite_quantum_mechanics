# PGW-MSSN-L1-CUTS-HODGE-ROWS

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `DEFINITION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Atlas row MSS-8 specifies exact primal-dual ℓ¹ cochain cuts over ℚ: the primal Φ₁(c) = min over g of ‖c − d₀g‖_{1,ω}, the dual max ⟨c, y⟩ subject to d₀ᵀy = 0 and |y_e| ≤ ω_e, certified when primal and dual masses agree, and a zero-gap string without dual feasibility is refused. Row MSS-18 specifies the rational ℓ² Hodge split c = d_{k−1}p + h + d_k* q with d_k* = M_k⁻¹ d_kᵀ M_{k+1} for symmetric positive-definite rational weights, unique in its three components while the potentials p and q need not be. Both rows are specified with lift status unlicensed, and their evaluators ConcentricDispatcher and HodgeProjector are proposed labels.

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

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- External MSS atlas row specifications MSS-8 and MSS-18 (assumption)

## Bottleneck

An ℓ¹ cut is a minimal representative modulo exact cochains, not an ℓ² Hodge decomposition; MSS-18 implies no smooth Riemannian or de Rham-Hodge statement, the evaluator label is not an implementation receipt, and the worked triangle values are in TFQ-0524.

## Source status

003_oemssn levels/level_08 and level_18 (specified rows, lift unlicensed)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0535_mssn_l1_cuts_hodge_rows.md`

- file: [dag/derivations/05_mssn_sn/tfq_0535_mssn_l1_cuts_hodge_rows.md](../../../dag/derivations/05_mssn_sn/tfq_0535_mssn_l1_cuts_hodge_rows.md)
- sha256 (`lf-normalised`): `a6b71c5172383d9f7097048cd903867582de1e83002a9de87328bf3805466da9`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0535
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:2e8d3a73acde99fa958aebc35782e04482da4bd3e02496770588b9b28cdb9c73:63-67`
- `external:sha256:584042f0b0371f95e96e81c58a5f4c3e24fe37dc20103464999b3bbde4e461f6:40`
- `external:sha256:584042f0b0371f95e96e81c58a5f4c3e24fe37dc20103464999b3bbde4e461f6:77-78`

## Absences recorded by the TFQ records

- TFQ-0535 lean4: no Lean statement of the MSS-8 or MSS-18 row obligations
- TFQ-0535 python: no Python evaluator for the MSS-8 or MSS-18 packets
- TFQ-0535 rust: no Rust ConcentricDispatcher or HodgeProjector implementation is linked from the rows

## Routes

Incoming (1):

- `PGW-R-MSSN-L1-CUTS-HODGE-ROWS` `DERIVED_PROSE`: [PGW-MSSN-CIRCULATION-OBSTRUCTION](PGW-MSSN-CIRCULATION-OBSTRUCTION.md) (PROVED_LEAN)

Outgoing (0):

