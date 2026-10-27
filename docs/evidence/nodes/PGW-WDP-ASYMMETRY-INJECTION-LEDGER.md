# PGW-WDP-ASYMMETRY-INJECTION-LEDGER

Stage: [WDP](../stages/WDP.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For any proposed selection the injection ledger records the first input that breaks the relevant symmetry: a named element or base point, an orientation, an order or clock, a measure or weighting, a boundary condition, a representation, an observer profile, a stochastic device with its distribution, or a physical law outside the root package. WDP-CH03-D01 defines the asymmetry-price frontier, relative to a specified implementation class and dependency preorder, as the family of inclusion-minimal declared input sets whose removal restores a symmetry that moves the output; a scalar price needs a stated cost function, and frontier elements may tie or be incomparable. In the declare-then-assert search, a refinement can leave a single class made of two responses exchanged by the swap of the data, so choosing one is a further declared input recorded in the ledger.

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

- Declared implementation class and dependency preorder for the frontier (assumption)

## Bottleneck

Definition only: no uniqueness or global-minimality theorem holds for the frontier in general; it rests on the nonselection row WDP-CH03-P01 (TFQ-0340), and the declare-then-assert separation row CH03-P03 takes no Lean credit.

## Source status

WDP monograph §3.2 injection ledger and WDP-CH03-D01 definition

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/Symmetry.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/Symmetry.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Symmetry.lean)
- sha256 (`bytes`): `3ce0aff3e18ce1934e1aba37e3a0f0e1687c8c9cff2bac911e0727c112e912b9`
- cited in: node.lean, record TFQ-0540
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_wdp.json](../../../dag/research/lean_replay_campaign_wdp.json) (module `Imported.WitnessedDifference.WitnessedDifference.Symmetry`): recorded sha256 `3ce0aff3e18ce1934e1aba37e3a0f0e1687c8c9cff2bac911e0727c112e912b9` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/Symmetry.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `no_invariant_oriented_edge` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms no_invariant_oriented_edge` |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/symmetry.py`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/symmetry.py](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/symmetry.py)
- sha256 (`bytes`): `a2b16bc67bc3c996ac3fbcbe03eb409b45d7865634c9a0003059976f792a40f0`
- cited in: record TFQ-0540

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `exhaustive_relation_audit` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md)
- sha256 (`lf-normalised`): `753d1c99c799f84f9a71912b98082d590c89c531f980c112b62ee2a86ab2726b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0540_wdp_asymmetry_injection_ledger.md`

- file: [dag/derivations/06_wdp/tfq_0540_wdp_asymmetry_injection_ledger.md](../../../dag/derivations/06_wdp/tfq_0540_wdp_asymmetry_injection_ledger.md)
- sha256 (`lf-normalised`): `c15e41d8d355fea1204acc5c9feb3bf543d50c3ecb1851d6f3738a807c17c8dd`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0540
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/006_oewdp/levels/level_02_residuals_obstructions.md`

- file: `omega_engine_education/documentation/006_oewdp/levels/level_02_residuals_obstructions.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0540 rust: no Rust implementation of the injection ledger or the asymmetry-price frontier

## Routes

Incoming (1):

- `PGW-R-WDP-ASYMMETRY-INJECTION-LEDGER` `DERIVED_PROSE`: [PGW-WDP-FAILED-SAMENESS](PGW-WDP-FAILED-SAMENESS.md) (PROVED_PROSE), [PG-WDP-PROTECTED-QUESTIONS](PG-WDP-PROTECTED-QUESTIONS.md) (PROVED_LEAN)

Outgoing (0):

