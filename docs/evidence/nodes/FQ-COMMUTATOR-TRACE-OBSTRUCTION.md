# FQ-COMMUTATOR-TRACE-OBSTRUCTION

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `PROVED_PROSE`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In nonzero finite dimension, trace cyclicity gives tr\[A,B\] = 0 while tr(lambda I) = n lambda, so \[A,B\] = lambda I forces lambda = 0: canonical \[X,P\] = i hbar I has no finite-dimensional representation. Lean covers 2x2 integer matrices; Rust covers d=3 over Q(zeta_24).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- finite dimension (assumption)

## Bottleneck

The n x n argument is the prose proof in the statement and needs a scalar field in which n is nonzero (characteristic 0 suffices). Lean states only the 2x2 case (wintner_wielandt_dim2_obstruction over Z, weyl_heisenberg_finite_trace_obstruction over Q, tr_comm2_vanishes); Rust checks d = 3 over Q(zeta_24).

## Source status

paper s11/13; Wintner-Wielandt style; H056, H068

## Review

- PFP review: [dag/results/FQ-COMMUTATOR-TRACE-OBSTRUCTION/reviews/20261019_dynamics_audit/review_result.json](../../../dag/results/FQ-COMMUTATOR-TRACE-OBSTRUCTION/reviews/20261019_dynamics_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: The exact finite-dimensional scalar commutator obstruction is kernel checked for arbitrary n\>0 over Q.
  - does not support: Transport to other coefficient fields and domain/unbounded-operator settings with their actual hypotheses. The supplied finite matrix carrier is an assumption.
  - next test: Transport to other coefficient fields and domain/unbounded-operator settings with their actual hypotheses. The supplied finite matrix carrier is an assumption.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/ContinuumLiftBoundary.lean`

- file: [lean4/ContinuumLiftBoundary.lean](../../../lean4/ContinuumLiftBoundary.lean)
- sha256 (`bytes`): `2ae7ab1be60f262dea685b1ad0d16f3330cf1dec8e9babba145c17c94932a50d`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_dynamics.json](../../../dag/research/lean_replay_campaign_finite_qm_dynamics.json) (module `ContinuumLiftBoundary`): recorded sha256 `2ae7ab1be60f262dea685b1ad0d16f3330cf1dec8e9babba145c17c94932a50d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build ContinuumLiftBoundary`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `wintner_wielandt_dim2_obstruction` | yes | yes | yes | Quot.sound, propext | `#print axioms wintner_wielandt_dim2_obstruction` |

- counts toward the grade: yes

### Lean: `lean4/FiniteQM.lean`

- file: [lean4/FiniteQM.lean](../../../lean4/FiniteQM.lean)
- sha256 (`bytes`): `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qcd.json](../../../dag/research/lean_replay_campaign_finite_qcd.json) (module `FiniteQM`): recorded sha256 `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteQM`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `weyl_heisenberg_finite_trace_obstruction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms weyl_heisenberg_finite_trace_obstruction` |

- counts toward the grade: yes

### Lean: `lean4/WeylCcrResidual.lean`

- file: [lean4/WeylCcrResidual.lean](../../../lean4/WeylCcrResidual.lean)
- sha256 (`bytes`): `4ac0f1692a22ed74c01c270a089198330c610829be9f20f9d4280eb97122db07`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_dynamics.json](../../../dag/research/lean_replay_campaign_finite_qm_dynamics.json) (module `WeylCcrResidual`): recorded sha256 `4ac0f1692a22ed74c01c270a089198330c610829be9f20f9d4280eb97122db07` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build WeylCcrResidual`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `tr_comm2_vanishes` | yes | yes | yes | Quot.sound, propext | `#print axioms tr_comm2_vanishes` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/15_finite_qed/tfq_0067_each_language_must_carry_kravchuk_brackets_and_spacing_balmer_values_1_n_2_on.md`

- file: [dag/derivations/15_finite_qed/tfq_0067_each_language_must_carry_kravchuk_brackets_and_spacing_balmer_values_1_n_2_on.md](../../../dag/derivations/15_finite_qed/tfq_0067_each_language_must_carry_kravchuk_brackets_and_spacing_balmer_values_1_n_2_on.md)
- sha256 (`lf-normalised`): `ecfd79c9a67ae784a8c02be7275d29a8ce6a576970c52d044f322d03db485ed1`
- generated view: listed, not counted
- cited in: record TFQ-0067 (shared)
- counts toward the grade: no

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml`

- file: [sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml](../../../sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `722a38e963f9ae31ac005968a71e39dff5964e452f5aca1e5cb4506dc0ece190`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md`

- file: [sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md](../../../sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `85ca7b22b1c1e360a4c17ad8a9e0bddae03433592585b01d23a74cd09c82929e`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:aaa24b2955f9d6b460c2aec041d1c9ebfa58a61bf4056394a372e45942b81f40::verify_trace_cyclicity_d3`
- `external:sha256:cf5119090eb0b22a44f55374a9d37eecdbbd1877fbde75226237781aae046351::canonical_commutator_obstruction`

## Absences recorded by the TFQ records

- TFQ-0067 lean4: not located
- TFQ-0067 python: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm/use_cases/algebraic_bound_state_spectra_control.py
- TFQ-0067 rust: no local rust twin located for external:sha256:a10da92df13ef926419410d2e5c98c7366f31aa5dd28fa48718916ad8f904b62

## Routes

Incoming (1):

- `FQ-R-COMMUTATOR` `DERIVED_PROSE`: [FQ-WEYL-FINITE-SCHRODINGER-IRREDUCIBILITY](FQ-WEYL-FINITE-SCHRODINGER-IRREDUCIBILITY.md) (PROVED_LEAN)

Outgoing (2):

- `FQ-R-GAP-CONTINUUM` `CONDITIONAL_ON_IMPORT`: [FQ-GAP-CONTINUUM-HILBERT-LIFT](FQ-GAP-CONTINUUM-HILBERT-LIFT.md) (CONDITIONAL)
- `FQ-R-GAP-STONE` `CONDITIONAL_ON_IMPORT`: [FQ-GAP-STONE-CONTINUOUS-TIME](FQ-GAP-STONE-CONTINUOUS-TIME.md) (CONDITIONAL)
