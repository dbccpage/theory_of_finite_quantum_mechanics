# PGW-SN-E08-WEIGHTED-L1-DUALITY

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Example E08 takes finite rational cochain spaces, d₀: C⁰ → C¹ and positive rational weights ω_e, and states that the minimum over g of Σ_e ω_e |c_e − (d₀g)_e| equals the maximum of cᵀy subject to d₀ᵀy = 0 and |y_e| ≤ ω_e, as finite linear-programming duality for the stated feasible bounded problem. Matching primal and dual feasible values certify optimality. An ℓ¹ minimizer need not be unique and is not in general the ℓ² harmonic residual. The page separately defines a categorical adjunction by functors, unit, counit and triangle identities, and says these maps are not the matrix pair d₀, d₀ᵀ.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 25
- distinct cited Lean declarations covered by a current replay receipt: 14
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

002_oesn levels/level_08 (declared construction); Lean WeightedL1Duality (Fourier-Motzkin LP strong duality over Q)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/WeightedL1Duality.lean`

- file: [lean4/WeightedL1Duality.lean](../../../lean4/WeightedL1Duality.lean)
- sha256 (`bytes`): `d817dcb21291f1ca63d5f7b3761c9921506a029105073a4202af19026ea794bd`
- cited in: node.lean, receipt dag/research/campaign_pgw-sn-e08-weighted-l1-duality_lean_replay.json (WeightedL1Duality), record TFQ-0522
- replay: `verified`
  - receipt [dag/research/campaign_pgw-sn-e08-weighted-l1-duality_lean_replay.json](../../../dag/research/campaign_pgw-sn-e08-weighted-l1-duality_lean_replay.json) (module `WeightedL1Duality`): recorded sha256 `d817dcb21291f1ca63d5f7b3761c9921506a029105073a4202af19026ea794bd` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build WeightedL1Duality`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WeightedL1Duality.adjunctionCochain_not_cycD_transpose` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WeightedL1Duality.adjunctionCochain_not_cycD_transpose` |
| `WeightedL1Duality.adjunctionCochain_section_retraction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WeightedL1Duality.adjunctionCochain_section_retraction` |
| `WeightedL1Duality.certificate_optimal` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WeightedL1Duality.certificate_optimal` |
| `WeightedL1Duality.cyc_dual_feasible` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WeightedL1Duality.cyc_dual_feasible` |
| `WeightedL1Duality.cyc_harmonic` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WeightedL1Duality.cyc_harmonic` |
| `WeightedL1Duality.cyc_optimum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WeightedL1Duality.cyc_optimum` |
| `WeightedL1Duality.cyc_residuals_differ` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WeightedL1Duality.cyc_residuals_differ` |
| `WeightedL1Duality.e08_rational` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WeightedL1Duality.e08_rational` |
| `WeightedL1Duality.farkas` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WeightedL1Duality.farkas` |
| `WeightedL1Duality.farkas_fintype` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WeightedL1Duality.farkas_fintype` |
| `WeightedL1Duality.lp_strong_duality` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WeightedL1Duality.lp_strong_duality` |
| `WeightedL1Duality.lp_weak_duality` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WeightedL1Duality.lp_weak_duality` |
| `WeightedL1Duality.weak_duality` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WeightedL1Duality.weak_duality` |
| `WeightedL1Duality.weighted_l1_strong_duality` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WeightedL1Duality.weighted_l1_strong_duality` |
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
- sha256 (`lf-normalised`): `4471a458f38dbd7b80b533f3069a3486a0e2b82a054388fbc95467ca465c74c6`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0522
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-sn-e08-weighted-l1-duality.md`

- file: [dag/derivations/independent/pgw-sn-e08-weighted-l1-duality.md](../../../dag/derivations/independent/pgw-sn-e08-weighted-l1-duality.md)
- sha256 (`lf-normalised`): `223b8b17c00279a4a630cdc23323badfa4103e5918a3ab89369fa733f5a6b1bd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `education/symmetric_group_presentations/levels/README.md`

- file: [education/symmetric_group_presentations/levels/README.md](../../../education/symmetric_group_presentations/levels/README.md)
- sha256 (`lf-normalised`): `58f41876692a51be940c4e0f44bd2e1ef72cd873c70b4726ef3d5f0639137165`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:9edec90b2c87518d8a33cb78cbf439fe11ce6e4f33a3f613148b9137771649d6:19-29`
- `external:sha256:9edec90b2c87518d8a33cb78cbf439fe11ce6e4f33a3f613148b9137771649d6:40-44`

## Absences recorded by the TFQ records

- TFQ-0522 rust: no Rust LP solver in the S(n) strand; the page assigns evaluation to existing mathematics owners

## Routes

Incoming (1):

- `PGW-R-SN-E08-WEIGHTED-L1-DUALITY` `DERIVED_LEAN`: [PGW-SN4-POLICY-CLOSURE-CYCLE-SPACE](PGW-SN4-POLICY-CLOSURE-CYCLE-SPACE.md) (PROVED_PROSE)

Outgoing (3):

- `PGW-R-SN-E12-CIRCULATION-FUNCTIONAL` `DERIVED_LEAN`: [PGW-SN-E12-CIRCULATION-FUNCTIONAL](PGW-SN-E12-CIRCULATION-FUNCTIONAL.md) (PROVED_LEAN)
- `PGW-R-SN-E18-L1-TIES-L2-CENTER` `DERIVED_PROSE`: [PGW-SN-E18-L1-TIES-L2-CENTER](PGW-SN-E18-L1-TIES-L2-CENTER.md) (PROVED_PROSE)
- `PGW-R-WDP-PHI-WELL-DEFINED-L1-DUALITY` `CONDITIONAL_ON_IMPORT`: [PGW-WDP-PHI-WELL-DEFINED-L1-DUALITY](PGW-WDP-PHI-WELL-DEFINED-L1-DUALITY.md) (CONDITIONAL)
