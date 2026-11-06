# Discrete evolution versus continuous time on the finite carrier — specification and exact obstruction

Status: **constructed, compiled, sealed, stopped for review**. AuthorityEffect: None.

Target: DAG node `FQ-GAP-STONE-CONTINUOUS-TIME` ("specify continuity, generator selection, and the
relationship between discrete evolution and continuous time"). The finite carrier has no topology, so
"continuous time" is specified as the strongest finite notion available — a ℚ-parameter group — and
the relationship to discrete evolution and the exact obstruction are kernel-checked.

- [DiscreteTimeStoneSpec.lean](DiscreteTimeStoneSpec.lean) (26 receipts, Lean 4.33.1, pinned Mathlib cache):
  - **Specification.** `QParamGroup G` (`U : ℚ → G`, `U 0 = 1`, `U (s+t) = U s * U t`); `discreteEvolution u k = u ^ k` (the ℤ-action of one step).
  - **Relationship.** `U_eq_discreteEvolution`: a ℚ-parameter group restricts to the ℤ-action of its unit step; `U_inv_nat`, `roots_of_all_orders`: it requires an m-th root of the unit step in the carrier for every m.
  - **Generator selection.** `sq_root_neg`, `half_step_not_unique`, `matrix_half_step_not_unique`: if `V·V = U` with `V ≠ 0` then `−V` is a second half-step — a generator is a choice, not a derivation.
  - **Discrete evolution exists.** `R345 = [[3/5,−4/5],[4/5,3/5]]` is orthogonal with determinant one and every power is orthogonal (`R345_pow_orthogonal`): a reversible ℤ-action on ℚ².
  - **Obstruction.** `no_rational_half_step`: any `V` with `V·V = R345` commutes with `R345`, hence `V = [[p,−r],[r,p]]` and `p² = 4/5`, whose denominator 5 is not a square (`four_fifths_not_rat_square`); `no_qparam_group_through_R345`: no ℚ-parameter group of invertible rational 2×2 matrices has the Pythagorean rotation as its unit step. Continuous time through this step requires extending the carrier (√5).
- Exact twins: [code/python/src/qm/discrete_time_stone.py](../../../../../code/python/src/qm/discrete_time_stone.py) (12 tests) and [code/rust/src/qm/discrete_time_stone.rs](../../../../../code/rust/src/qm/discrete_time_stone.rs) (11 inline tests): orbit orthogonality, the half-angle criterion (a rational rotation `(c,s)` has a rational half-step iff `(1+c)/2` is a rational square — false for `3/5`, true for `R345² = (−7/25, 24/25)` whose half-steps are exactly `±R345`), root pairs, rotation orders, and the specification statements. The module is also installed as `lean4/DiscreteTimeStoneSpec.lean` and registered in the lakefile.
- [Compile receipt](verification/discrete_time_spec_01/), [kernel axioms](verification/kernel_axioms.json), [5 operation records](operad_delta.json), [claim statuses](claim_status.json), [review and boundaries](review.md), [next steps](next_steps.md), [provenance](provenance.json), [validation](validation.json), [seal](manifest.json).

All 26 receipts are within `[propext, Classical.choice, Quot.sound]` (several need no axiom at all); no `sorry`, `axiom`, `opaque` or `unsafe`; no compile warnings. The DAG node keeps status `CONDITIONAL`; its `source_status`, `lean` references, `imported_structure` and `bottleneck` were updated.

**Review boundaries.** No topology, no real completion and no exponential are constructed; "continuity" is not derived, it is replaced by the exact necessary condition (roots of every order) that the carrier violates. The scalar facts on the rational circle (no square root of (3+4i)/5, no hom (ℚ,+) → U(1)(ℚ(i)) through it, infinite order) exist in uncommitted working-copy modules `U1PythagoreanObstruction.lean` / `U1PowerMapInjectivity.lean`; this run is self-contained and does not import them. The general theorem that every ℚ-parameter group of matrices over ℚ(i) is trivial is not proved (it needs unique factorisation in ℤ[i]) and is recorded as the open obligation. See [review.md](review.md).

Replay: `python tools/replay.py DiscreteTimeStoneSpec.lean NEW_LABEL --lean PINNED_LEAN --project CONFIGURED_LEAN4_PROJECT`, then `python tools/seal.py receipts` and `python tools/seal.py verify`.
