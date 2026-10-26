# PGW-WDP-CLOSURE-NEEDS-DEGREE

Stage: [WDP](../stages/WDP.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Given d₁: C¹ → C² from a finite 2-cell structure, the closure diagnostic Γ(δ) = J₂(d₁δ) descends to Q¹ exactly when d₁d₀ = 0 on the admissible repairs if J₂ is a norm (for a seminorm, exactly when im(d₁d₀) ⊆ ker J₂): necessity by comparing a repair with the zero representative, sufficiency by linearity. Otherwise K = d₁d₀ is itself a typed curvature or composition defect, calling Q¹ cohomology while K ≠ 0 is an error, and none of the window results of §§4.8–4.11 applies. WDP-CH04-D01 makes the d₁d₀ = 0 certificate part of the degree-1 window: automatic on the simplicial nerve route, verified for any hand-declared pair; degree_one_window multiplies the exact matrices and refuses a nonzero product with CERTIFICATE_MISMATCH.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared d₁ from a finite 2-cell structure and closure norm J₂ (assumption)

## Bottleneck

A typing rule for the window; it does not select which d₁ to declare, and a zero K does not derive the window from Genesis admission (TFQ-0344).

## Source status

WDP monograph §4.4 closure requires another degree; §4.7 WDP-CH04-D01 certificate

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean)
- sha256 (`bytes`): `bef8623978d7c0735b4a02db686664b03b61e18bba0e5ef6bcce81ff4234dd0a`
- cited in: node.lean, record TFQ-0545
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_wdp.json](../../../dag/research/lean_replay_campaign_wdp.json) (module `Imported.WitnessedDifference.WitnessedDifference.Obstruction`): recorded sha256 `bef8623978d7c0735b4a02db686664b03b61e18bba0e5ef6bcce81ff4234dd0a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `kappa_well_defined` | yes | yes | yes | none | `#print axioms kappa_well_defined` |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py)
- sha256 (`bytes`): `2c39d5d66e90bfe5675526a4018e66a8290aa1daef019fdaceb85c4326a356d1`
- cited in: record TFQ-0545

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `degree_one_window` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md)
- sha256 (`lf-normalised`): `753d1c99c799f84f9a71912b98082d590c89c531f980c112b62ee2a86ab2726b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0545_wdp_closure_needs_degree.md`

- file: [dag/derivations/06_wdp/tfq_0545_wdp_closure_needs_degree.md](../../../dag/derivations/06_wdp/tfq_0545_wdp_closure_needs_degree.md)
- sha256 (`lf-normalised`): `36fdb9c8c968045d5c561227c345ce33ec13b9f94099e9c2e1353055e18d7107`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0545
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/006_oewdp/levels/level_03_discrete_complex_cochains.md`

- file: `omega_engine_education/documentation/006_oewdp/levels/level_03_discrete_complex_cochains.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0545 rust: no omega_wdp Rust check of the window-level composition defect K = d1 d0; the Python degree_one_window carries it

## Routes

Incoming (1):

- `PGW-R-WDP-CLOSURE-NEEDS-DEGREE` `DERIVED_PROSE`: [PGW-WDP-GRAPH-COCHAIN-HOST](PGW-WDP-GRAPH-COCHAIN-HOST.md) (DEFINITION)

Outgoing (0):

