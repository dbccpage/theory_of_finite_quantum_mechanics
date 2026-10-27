# L1-DENSITY-LIFT-SIGNED-SQRT-PUB009

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For an l1 residual v with mass M(v) \> 0, psi(v)_i = sgn(v_i) sqrt(|v_i| / M(v)) gives the rank-one real projector rho(v) = psi psi^T, a real L2 lift. The alignment statistic Xi = (1/2) ||rho(h*) - rho(phi*)||_tr is strictly below 1 by complementary slackness. Xi depends on coordinate order and is undefined at zero residual. It does not derive QM.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- distinct cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- real square roots (real field): lift
- trace norm on real symmetric matrices: lift

## Bottleneck

The bound Xi \< 1 is not in Lean. The cited Lean states only that a sum of squared differences of three integers is nonnegative and vanishes on a constant triple. The construction of psi(v) and rho(v) is a definition.

## Source status

PUB-009 signed-sqrt lift and Cauchy-Schwarz Xi bound mechanized in DerivationDagQMClosure.lean and Rust BigRational witness

## Review

- PFP review: [dag/results/L1-DENSITY-LIFT-SIGNED-SQRT-PUB009/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/L1-DENSITY-LIFT-SIGNED-SQRT-PUB009/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Exact signed-square density projectors, overlap/Xi², zero-mass refusal, saturation and positive-support controls; general normalized Cauchy algebra and zero-weight strictness counterexample in Lean.
  - does not support: Prove the full real-square-root/trace-distance transport and conditional KKT overlap theorem under positive weights. Only Xi² is reported; no fabricated decimal Xi or unconditional Xi\<1 is admitted.
  - next test: Prove the full real-square-root/trace-distance transport and conditional KKT overlap theorem under positive weights. Only Xi² is reported; no fabricated decimal Xi or unconditional Xi\<1 is admitted.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.signed_sqrt_density_lift_cauchy_schwarz` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.signed_sqrt_density_lift_cauchy_schwarz` |

- counts toward the grade: yes

### Lean: `lean4/Imported/ConditionalDensityLift/Xi.lean`

- file: [lean4/Imported/ConditionalDensityLift/Xi.lean](../../../lean4/Imported/ConditionalDensityLift/Xi.lean)
- sha256 (`bytes`): `39768ebfef137380ba5af96445973d5d2777476867eb0a0edab787d9d961bbee`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `Imported.ConditionalDensityLift.Xi`): recorded sha256 `39768ebfef137380ba5af96445973d5d2777476867eb0a0edab787d9d961bbee` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/ConditionalDensityLift/Xi.lean`
- counts toward the grade: yes

### Documents and data: `dag/derivations/07_l1_emergence/tfq_0355_stop_at_the_open_residual_to_weight_gap_and_do_not_import_a_hilbert.md`

- file: [dag/derivations/07_l1_emergence/tfq_0355_stop_at_the_open_residual_to_weight_gap_and_do_not_import_a_hilbert.md](../../../dag/derivations/07_l1_emergence/tfq_0355_stop_at_the_open_residual_to_weight_gap_and_do_not_import_a_hilbert.md)
- sha256 (`lf-normalised`): `e1bfd7a9b858c861d7e13fcda4ae9aa97f3636eb276192cafed99d5d81c16937`
- generated view: listed, not counted
- cited in: record TFQ-0355 (shared)
- counts toward the grade: no

### Documents and data: `papers/009_conditional_density_lift_and_dual_witness_xi_functional/density_lift.md`

- file: [papers/009_conditional_density_lift_and_dual_witness_xi_functional/density_lift.md](../../../papers/009_conditional_density_lift_and_dual_witness_xi_functional/density_lift.md)
- sha256 (`lf-normalised`): `39b240b2592290928123eb7f457c8e0ceacfb513a59042eba77418841a6bdb37`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_l1_sector_weights_and_density_lift_witness`
- `external:sha256:ee8cc328a4002a16738b268758f63f60c3ce2d23632ab39a6cd65382cd457c2f::DensityLift`
- `external:sha256:ee8cc328a4002a16738b268758f63f60c3ce2d23632ab39a6cd65382cd457c2f::XiResult`

## Routes

Incoming (1):

- `L1-R-DENSITY-LIFT-PUB009` `GAP_NO_DERIVATION`: [L1-QM002-O022A-PHI1-QUOTIENT](L1-QM002-O022A-PHI1-QUOTIENT.md) (OPEN), [L1-FRAMEWORK-KKT-CERT](L1-FRAMEWORK-KKT-CERT.md) (PROVED_LEAN), [L1-IMP-SQRT-FIELD](L1-IMP-SQRT-FIELD.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `L1-R-QM003-C17-FACTORIZATION` `COMPUTED`: [L1-QM003-C17-COMPOSABLE-FACTORIZATION](L1-QM003-C17-COMPOSABLE-FACTORIZATION.md) (COMPUTATIONALLY_CHECKED)
