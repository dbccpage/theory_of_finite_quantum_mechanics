# PGW-SN-E08-WEIGHTED-L1-DUALITY

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Example E08 takes finite rational cochain spaces, d₀: C⁰ → C¹ and positive rational weights ω_e, and states that the minimum over g of Σ_e ω_e |c_e − (d₀g)_e| equals the maximum of cᵀy subject to d₀ᵀy = 0 and |y_e| ≤ ω_e, as finite linear-programming duality for the stated feasible bounded problem. Matching primal and dual feasible values certify optimality. An ℓ¹ minimizer need not be unique and is not in general the ℓ² harmonic residual. The page separately defines a categorical adjunction by functors, unit, counit and triangle identities, and says these maps are not the matrix pair d₀, d₀ᵀ.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 25
- cited Lean declarations covered by a current replay receipt: 23
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

E08 is a declared mathematical construction that grammar cases do not verify; AdjunctionCochain implements only x ↦ (x,0) and first-coordinate projection, and no adjunction is claimed until objects, functors, naturality and triangle laws are supplied.

## Source status

002_oesn levels/level_08 (declared construction); Lean CampaignSnE08WeightedL1Duality (Fourier-Motzkin LP strong duality over Q)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignSnE08WeightedL1Duality.lean`

- file: [lean4/CampaignSnE08WeightedL1Duality.lean](../../../lean4/CampaignSnE08WeightedL1Duality.lean)
- sha256 (`bytes`): `2627f12d8eaa545ba5bf63ee9d792eda2f0c8c262db6906523b1aedd4fc6e1ff`
- cited in: node.lean, receipt dag/research/campaign_pgw-sn-e08-weighted-l1-duality_lean_replay.json (CampaignSnE08WeightedL1Duality), record TFQ-0522
- replay: `verified`
  - receipt [dag/research/campaign_pgw-sn-e08-weighted-l1-duality_lean_replay.json](../../../dag/research/campaign_pgw-sn-e08-weighted-l1-duality_lean_replay.json) (module `CampaignSnE08WeightedL1Duality`): recorded sha256 `2627f12d8eaa545ba5bf63ee9d792eda2f0c8c262db6906523b1aedd4fc6e1ff` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignSnE08WeightedL1Duality`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignSnE08WeightedL1Duality.adjunctionCochain_not_cycD_transpose` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignSnE08WeightedL1Duality.adjunctionCochain_not_cycD_transpose` |
| `CampaignSnE08WeightedL1Duality.adjunctionCochain_section_retraction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignSnE08WeightedL1Duality.adjunctionCochain_section_retraction` |
| `CampaignSnE08WeightedL1Duality.certificate_optimal` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignSnE08WeightedL1Duality.certificate_optimal` |
| `CampaignSnE08WeightedL1Duality.cyc_dual_feasible` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignSnE08WeightedL1Duality.cyc_dual_feasible` |
| `CampaignSnE08WeightedL1Duality.cyc_harmonic` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignSnE08WeightedL1Duality.cyc_harmonic` |
| `CampaignSnE08WeightedL1Duality.cyc_optimum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignSnE08WeightedL1Duality.cyc_optimum` |
| `CampaignSnE08WeightedL1Duality.cyc_residuals_differ` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignSnE08WeightedL1Duality.cyc_residuals_differ` |
| `CampaignSnE08WeightedL1Duality.e08_rational` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignSnE08WeightedL1Duality.e08_rational` |
| `CampaignSnE08WeightedL1Duality.farkas` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignSnE08WeightedL1Duality.farkas` |
| `CampaignSnE08WeightedL1Duality.farkas_fintype` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignSnE08WeightedL1Duality.farkas_fintype` |
| `CampaignSnE08WeightedL1Duality.lp_strong_duality` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignSnE08WeightedL1Duality.lp_strong_duality` |
| `CampaignSnE08WeightedL1Duality.lp_weak_duality` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignSnE08WeightedL1Duality.lp_weak_duality` |
| `CampaignSnE08WeightedL1Duality.weak_duality` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignSnE08WeightedL1Duality.weak_duality` |
| `CampaignSnE08WeightedL1Duality.weighted_l1_strong_duality` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignSnE08WeightedL1Duality.weighted_l1_strong_duality` |
| `adjunctionCochain_not_cycD_transpose` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms adjunctionCochain_not_cycD_transpose` |
| `certificate_optimal` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms certificate_optimal` |
| `cyc_harmonic` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms cyc_harmonic` |
| `cyc_optimum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms cyc_optimum` |
| `cyc_residuals_differ` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms cyc_residuals_differ` |
| `e08_rational` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms e08_rational` |
| `farkas` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms farkas` |
| `lp_strong_duality` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms lp_strong_duality` |
| `weighted_l1_strong_duality` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms weighted_l1_strong_duality` |
- counts toward the grade: yes

### Python: `checks/independent/pgw-sn-e08-weighted-l1-duality.py`

- file: [checks/independent/pgw-sn-e08-weighted-l1-duality.py](../../../checks/independent/pgw-sn-e08-weighted-l1-duality.py)
- sha256 (`bytes`): `3adc125971f302abdc6c7330041d660a690dddfab61441a3510414845093ea55`
- cited in: record TFQ-0522

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `solve_dual` (python_symbol) | yes | yes | yes | - | - |
| `solve_primal` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0522_sn_e08_weighted_l1_duality.md`

- file: [dag/derivations/05_mssn_sn/tfq_0522_sn_e08_weighted_l1_duality.md](../../../dag/derivations/05_mssn_sn/tfq_0522_sn_e08_weighted_l1_duality.md)
- sha256 (`lf-normalised`): `d019f1a9fbcf147c29064ef17e6dd5572aa0b0716aaf297bc657275f8c133cc5`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0522
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-sn-e08-weighted-l1-duality.md`

- file: [dag/derivations/independent/pgw-sn-e08-weighted-l1-duality.md](../../../dag/derivations/independent/pgw-sn-e08-weighted-l1-duality.md)
- sha256 (`lf-normalised`): `588891092b44fc6a7f39f2c8b131d0c3c81caca960ecf8a3b513e70e0f41192d`
- cited in: node.source
- counts toward the grade: yes

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

- TFQ-0522 rust: no Rust LP solver in the S(n) strand; the page assigns evaluation to existing mathematics owners

## Routes

Incoming (1):

- `PGW-R-SN-E08-WEIGHTED-L1-DUALITY` `DERIVED_LEAN`: [PGW-SN4-POLICY-CLOSURE-CYCLE-SPACE](PGW-SN4-POLICY-CLOSURE-CYCLE-SPACE.md) (PROVED_PROSE)

Outgoing (3):

- `PGW-R-SN-E12-CIRCULATION-FUNCTIONAL` `DERIVED_LEAN`: [PGW-SN-E12-CIRCULATION-FUNCTIONAL](PGW-SN-E12-CIRCULATION-FUNCTIONAL.md) (PROVED_LEAN)
- `PGW-R-SN-E18-L1-TIES-L2-CENTER` `DERIVED_PROSE`: [PGW-SN-E18-L1-TIES-L2-CENTER](PGW-SN-E18-L1-TIES-L2-CENTER.md) (PROVED_PROSE)
- `PGW-R-WDP-PHI-WELL-DEFINED-L1-DUALITY` `CONDITIONAL_ON_IMPORT`: [PGW-WDP-PHI-WELL-DEFINED-L1-DUALITY](PGW-WDP-PHI-WELL-DEFINED-L1-DUALITY.md) (CONDITIONAL)
