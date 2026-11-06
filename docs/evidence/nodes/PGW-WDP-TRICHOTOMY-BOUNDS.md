# PGW-WDP-TRICHOTOMY-BOUNDS

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> WDP-CH04-P04: in a window with d₁d₀ = 0 and a norm J meeting the norm hypothesis, every class \[h\] ∈ Q¹ has exactly one of ExactClass (\[h\] = 0), ClosedResidual (\[h\] ≠ 0 and Γ₂ = 0) or ActiveClosureFailure (Γ₂ \> 0); Φ₁ = 0 exactly on ExactClass, and every active class has Φ₁ \> 0. WDP-CH04-P05: Φ₁, Γ₂ ≥ 0, Γ₂ = 0 iff \[h\] ∈ H¹, Γ₂ ≤ ‖d₁‖_{J→1}Φ₁ (repair invariance of d₁h, then the infimum), no constant c \> 0 gives Γ₂ ≥ cΦ₁ when H¹ ≠ 0, and Γ₂ is a norm on Q¹/H¹. WDP-CH04-P06: if Φ₁ \> 0 then 0 ≤ R_cl ≤ ‖d₁‖_{J→1}, and the normalized ratio is undefined (0/0) when d₁ = 0. The norm hypothesis (ℝ, ℂ, or ℚ with J restricted from a norm on the real extension) is needed: J(x) = |x₀₁ + √2 x₁₂ + √3 x₀₂| is a norm on ℚ³, yet on the filled triangle with δ = (1, 1, 0) its repair values accumulate at 0, so Φ₁ = 0 while Γ₂ = 2.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 5 Lean reference(s) cited, 5 in this checkout (replay: none 5). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- Norm hypothesis: F = R or C, or F = Q with J the restriction of a norm on the real extension (assumption)

## Bottleneck

Mechanized in Lean 4 (closure_charge_le_opnorm_mul_phi in Obstruction.lean plus diagnostic_trichotomy_exclusive_exhaustive, no_reverse_bound_when_h1_nontrivial, gamma2_quotient_norm_laws, and irrational_weight_accumulation_violates_trichotomy in WdpBatch2.lean) and checked in Python core.py.

## Source status

WDP monograph §4.4-§4.5 WDP-CH04-P04/P05/P06 mechanized in Lean 4 (Obstruction.lean, WdpBatch2.lean) and checked in Python core.py

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean)
- sha256 (`bytes`): `3d970ea9cc3ed97c56f7f002b31a96f5989e91bb2698f3785d887d9eb9369a22`
- cited in: node.lean, record TFQ-0547
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.closure_charge_le_opnorm_mul_phi` | yes | yes | yes | - | `#print axioms WitnessedDifference.closure_charge_le_opnorm_mul_phi` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch2.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch2.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch2.lean)
- sha256 (`bytes`): `b40aa3e8417cf931d7fe83e997f927c00648d0bcdced7873735a60f8212c0413`
- cited in: node.lean, record TFQ-0547
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch2.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch2.diagnostic_trichotomy_exclusive_exhaustive` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch2.diagnostic_trichotomy_exclusive_exhaustive` |
| `WitnessedDifference.WdpBatch2.gamma2_quotient_norm_laws` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch2.gamma2_quotient_norm_laws` |
| `WitnessedDifference.WdpBatch2.irrational_weight_accumulation_violates_trichotomy` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch2.irrational_weight_accumulation_violates_trichotomy` |
| `WitnessedDifference.WdpBatch2.no_reverse_bound_when_h1_nontrivial` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch2.no_reverse_bound_when_h1_nontrivial` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py)
- sha256 (`bytes`): `2c39d5d66e90bfe5675526a4018e66a8290aa1daef019fdaceb85c4326a356d1`
- cited in: record TFQ-0547

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `classify_signature` (python_symbol) | yes | yes | yes | - | - |
| `obstruction_signature` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md)
- sha256 (`lf-normalised`): `753d1c99c799f84f9a71912b98082d590c89c531f980c112b62ee2a86ab2726b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0547_wdp_trichotomy_bounds.md`

- file: [dag/derivations/06_wdp/tfq_0547_wdp_trichotomy_bounds.md](../../../dag/derivations/06_wdp/tfq_0547_wdp_trichotomy_bounds.md)
- sha256 (`lf-normalised`): `aa21b7e6a4d6b2c70f0481a0fe17afd331d4844c09394667e2d02fb4dd4401f7`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0547
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:3301e36106cfe1fb4415d4f6218951cd83516f0a714d773fcb477ea3dce63814::TriadSignature`
- `external:sha256:f444bcaa3ae162d185a3a8a21cf0b59606958107ac5510e84015090750d5c3cc:309-312`
- `external:upstream/external:sha256:3301e36106cfe1fb4415d4f6218951cd83516f0a714d773fcb477ea3dce63814::TriadSignature`

## Routes

Incoming (1):

- `PGW-R-WDP-TRICHOTOMY-BOUNDS` `DERIVED_LEAN`: [PGW-WDP-EXACT-SEQUENCE-H1-Q1](PGW-WDP-EXACT-SEQUENCE-H1-Q1.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-SYNTHESIS-TRUNK-TIERS` `DERIVED_PROSE`: [PGW-WDP-SYNTHESIS-TRUNK-TIERS](PGW-WDP-SYNTHESIS-TRUNK-TIERS.md) (DEFINITION)
