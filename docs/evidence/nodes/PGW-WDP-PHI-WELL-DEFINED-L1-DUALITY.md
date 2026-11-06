# PGW-WDP-PHI-WELL-DEFINED-L1-DUALITY

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> WDP-CH04-P01: Φ_J(\[δ\]) = inf_f J(δ − d₀f) is independent of the representative, because δ' = δ + d₀g turns the infimum into one over h = f − g, a bijection of C⁰. WDP-CH04-P02 (conditional): when the repair space is finite-dimensional over ℝ or ℂ and J is a norm, the infimum is attained after quotienting ker d₀; the hypotheses cannot be dropped silently for seminorms or infinite carriers. WDP-CH04-C01 (conditional): with positive weights w, Φ_{1,w}(\[δ\]) = max{⟨y, δ⟩ : d₀*y = 0, |y_e| ≤ w_e}, an imported finite-dimensional convex-duality result (REF-MATH-005, Rockafellar, Convex Analysis) specialized to the declared weighted graph complex. In code, finite_quotient_l1 minimizes over an explicit candidate list, and exact_quotient_l1 solves the weighted ℓ¹ programme over Fraction and reports a value only after an independent certificate check.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 28
- distinct cited Lean declarations covered by a current replay receipt: 16
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Finite-dimensional convex (linear-programming) strong duality, REF-MATH-005 Rockafellar Convex Analysis, specialized to the declared weighted graph complex (assumption)
- Attainment hypothesis: repair space finite-dimensional over R or C and J a norm, not a seminorm (assumption)

## Bottleneck

The checked slice is the integer triangle coboundary: linearity, residual identity under a vertex shift, and minimum absolute residual sum 2 for delta = (1, 1, 0) and for each integer coboundary shift of that one triple. Representative independence for a general cost, attainment on a real or complex repair space, weighted duality on an arbitrary complex, rational repairs, and a general coefficient field stay open. The weak direction of the duality is not imported (WDP-CH04-P07, TFQ-0348, Lean dual_certificate_lower_bound), and C01 is not shown for arbitrary coefficient spaces.

## Source status

WDP-CH04-P01, WDP-CH04-P07, and certified primal-dual optimality mechanized in PregenesisWdpPhiWellDefinedL1Duality.lean and WdpBatch4.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch4.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch4.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch4.lean)
- sha256 (`bytes`): `5139307750119e0e6f022ae813972e4625d02908d37d9067e6942e532181b6dd`
- cited in: node.lean, record TFQ-0544
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch4.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch4.certified_primal_dual_optimality` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch4.certified_primal_dual_optimality` |
| `WitnessedDifference.WdpBatch4.weighted_l1_weak_duality_triangle` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch4.weighted_l1_weak_duality_triangle` |
| `WitnessedDifference.WdpBatch4.weighted_residual_shift_invariant` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch4.weighted_residual_shift_invariant` |

- counts toward the grade: yes

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean)
- sha256 (`bytes`): `b5adb85d12297d203151348422a0400482d6cac0397e8fcc5381c9c8a54c9885`
- cited in: node.lean, record TFQ-0544
- replay: `verified`
  - receipt [evidence/lean_receipts/lean_replay_campaign_wdp.json](../../../evidence/lean_receipts/lean_replay_campaign_wdp.json) (module `Imported.WitnessedDifference.WitnessedDifference.Obstruction`): recorded sha256 `b5adb85d12297d203151348422a0400482d6cac0397e8fcc5381c9c8a54c9885` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `dual_certificate_lower_bound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms dual_certificate_lower_bound` |

- counts toward the grade: yes

### Lean: `lean4/PregenesisWdpPhiWellDefinedL1Duality.lean`

- file: [lean4/PregenesisWdpPhiWellDefinedL1Duality.lean](../../../lean4/PregenesisWdpPhiWellDefinedL1Duality.lean)
- sha256 (`bytes`): `cd7f4e4e6124de5b4cbf24d392371e953ca23b74d7b28d877e14df0559d06a17`
- cited in: node.lean, receipt evidence/lean_receipts/campaign_pgw-wdp-phi-well-defined-l1-duality_lean_replay.json (PregenesisWdpPhiWellDefinedL1Duality), receipt evidence/lean_receipts/pr_377_round2_replay.json (PregenesisWdpPhiWellDefinedL1Duality), record TFQ-0544
- replay: `verified`
  - receipt [evidence/lean_receipts/campaign_pgw-wdp-phi-well-defined-l1-duality_lean_replay.json](../../../evidence/lean_receipts/campaign_pgw-wdp-phi-well-defined-l1-duality_lean_replay.json) (module `PregenesisWdpPhiWellDefinedL1Duality`): recorded sha256 `cd7f4e4e6124de5b4cbf24d392371e953ca23b74d7b28d877e14df0559d06a17` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
  - receipt [evidence/lean_receipts/pr_377_round2_replay.json](../../../evidence/lean_receipts/pr_377_round2_replay.json) (module `PregenesisWdpPhiWellDefinedL1Duality`): recorded sha256 `cd7f4e4e6124de5b4cbf24d392371e953ca23b74d7b28d877e14df0559d06a17` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build PregenesisWdpPhiWellDefinedL1Duality`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `PregenesisWdpPhiWellDefinedL1Duality.absSum` | yes | yes | yes | none | `#print axioms PregenesisWdpPhiWellDefinedL1Duality.absSum` |
| `PregenesisWdpPhiWellDefinedL1Duality.absSum_attained` | yes | yes | yes | propext | `#print axioms PregenesisWdpPhiWellDefinedL1Duality.absSum_attained` |
| `PregenesisWdpPhiWellDefinedL1Duality.absSum_ge_two` | yes | yes | yes | Quot.sound, propext | `#print axioms PregenesisWdpPhiWellDefinedL1Duality.absSum_ge_two` |
| `PregenesisWdpPhiWellDefinedL1Duality.absSum_shift` | yes | yes | yes | Quot.sound, propext | `#print axioms PregenesisWdpPhiWellDefinedL1Duality.absSum_shift` |
| `PregenesisWdpPhiWellDefinedL1Duality.add3` | yes | yes | yes | none | `#print axioms PregenesisWdpPhiWellDefinedL1Duality.add3` |
| `PregenesisWdpPhiWellDefinedL1Duality.d0` | yes | yes | yes | none | `#print axioms PregenesisWdpPhiWellDefinedL1Duality.d0` |
| `PregenesisWdpPhiWellDefinedL1Duality.d0_linear` | yes | yes | yes | Quot.sound, propext | `#print axioms PregenesisWdpPhiWellDefinedL1Duality.d0_linear` |
| `PregenesisWdpPhiWellDefinedL1Duality.natAbs_pair_le_absSum` | yes | yes | yes | Quot.sound, propext | `#print axioms PregenesisWdpPhiWellDefinedL1Duality.natAbs_pair_le_absSum` |
| `PregenesisWdpPhiWellDefinedL1Duality.pair110` | yes | yes | yes | none | `#print axioms PregenesisWdpPhiWellDefinedL1Duality.pair110` |
| `PregenesisWdpPhiWellDefinedL1Duality.pair_d0_zero` | yes | yes | yes | Quot.sound, propext | `#print axioms PregenesisWdpPhiWellDefinedL1Duality.pair_d0_zero` |
| `PregenesisWdpPhiWellDefinedL1Duality.pair_residual` | yes | yes | yes | Quot.sound, propext | `#print axioms PregenesisWdpPhiWellDefinedL1Duality.pair_residual` |
| `PregenesisWdpPhiWellDefinedL1Duality.residual_shift` | yes | yes | yes | Quot.sound, propext | `#print axioms PregenesisWdpPhiWellDefinedL1Duality.residual_shift` |
| `PregenesisWdpPhiWellDefinedL1Duality.shifted_attained` | yes | yes | yes | Quot.sound, propext | `#print axioms PregenesisWdpPhiWellDefinedL1Duality.shifted_attained` |
| `PregenesisWdpPhiWellDefinedL1Duality.shifted_ge` | yes | yes | yes | Quot.sound, propext | `#print axioms PregenesisWdpPhiWellDefinedL1Duality.shifted_ge` |
| `PregenesisWdpPhiWellDefinedL1Duality.sub3` | yes | yes | yes | none | `#print axioms PregenesisWdpPhiWellDefinedL1Duality.sub3` |
| `absSum_attained` | yes | yes | yes | propext | `#print axioms absSum_attained` |
| `absSum_ge_two` | yes | yes | yes | Quot.sound, propext | `#print axioms absSum_ge_two` |
| `absSum_shift` | yes | yes | yes | Quot.sound, propext | `#print axioms absSum_shift` |
| `d0_linear` | yes | yes | yes | Quot.sound, propext | `#print axioms d0_linear` |
| `residual_shift` | yes | yes | yes | Quot.sound, propext | `#print axioms residual_shift` |
| `shifted_attained` | yes | yes | yes | Quot.sound, propext | `#print axioms shifted_attained` |
| `shifted_ge` | yes | yes | yes | Quot.sound, propext | `#print axioms shifted_ge` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/cochains.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/cochains.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/cochains.py)
- sha256 (`bytes`): `56d2c214f55aa7fa2844792d5114656936295171cd38f4acf908df83cc9e2326`
- cited in: record TFQ-0544

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `finite_quotient_l1` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py)
- sha256 (`bytes`): `2c39d5d66e90bfe5675526a4018e66a8290aa1daef019fdaceb85c4326a356d1`
- cited in: record TFQ-0544

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `exact_quotient_l1` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md)
- sha256 (`lf-normalised`): `753d1c99c799f84f9a71912b98082d590c89c531f980c112b62ee2a86ab2726b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0544_wdp_phi_well_defined_l1_duality.md`

- file: [dag/derivations/06_wdp/tfq_0544_wdp_phi_well_defined_l1_duality.md](../../../dag/derivations/06_wdp/tfq_0544_wdp_phi_well_defined_l1_duality.md)
- sha256 (`lf-normalised`): `2f22c52a4e19ccd94af2a846e818964939ac6a291abf3379ff6884f6891f2c7c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0544
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:fc5a04df299e671184b29b3468bd5fd18b70680beadaeaf4aebd5d809976d3e1::FenchelDualityReceipt`
- `external:upstream/external:sha256:fc5a04df299e671184b29b3468bd5fd18b70680beadaeaf4aebd5d809976d3e1::FenchelDualityReceipt`

## Routes

Incoming (1):

- `PGW-R-WDP-PHI-WELL-DEFINED-L1-DUALITY` `DERIVED_LEAN`: [PGW-WDP-GRAPH-COCHAIN-HOST](PGW-WDP-GRAPH-COCHAIN-HOST.md) (DEFINITION), [PGW-WDP-QUOTIENT-DEFECT-ROOT-P](PGW-WDP-QUOTIENT-DEFECT-ROOT-P.md) (DEFINITION), [PGW-SN-E08-WEIGHTED-L1-DUALITY](PGW-SN-E08-WEIGHTED-L1-DUALITY.md) (PROVED_LEAN)

Outgoing (0):

