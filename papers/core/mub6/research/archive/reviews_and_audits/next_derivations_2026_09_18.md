# Five next derivations for MUB6

Date: 2026-09-18. Baseline inspected: `11415b48271946743997462a3dc199f3420cccfd`.

AuthorityEffect: None.

`stated region only; mints no authority`

All five prioritized derivations proposed in this document on 2026-09-18 have been accomplished, verified in Lean 4 (with zero custom axioms), and discharged from the active derivation queue:

1. **Concrete cross-ratio and corner determinant identities**: Fully accomplished in [`CornerDeterminantCrossRatio.lean`](../../../../../../lean4/CornerDeterminantCrossRatio.lean) (`det3_dephased_corner`, `singular_corner_iff_det_zero`, `cross_ratio_gauge_inv_2x2`, `orthog_rows_iff_cross_ratio_neg_one`).
2. **Reflected cell certificate implies actual residual bound**: Fully accomplished in [`KernelReflectionBisection.lean`](../../../../../../lean4/KernelReflectionBisection.lean) and [`L1CellBisectionBridge.lean`](../../../../../../lean4/L1CellBisectionBridge.lean) (`concrete_cell_certificate_accepted` by `rfl`, `soundness_of_cell_acceptance`, `weak_duality_theorem`, `cell_pruning_theorem`).
3. **Common-gauge compatibility on genuine corner reconstruction chart**: Fully accomplished in [`NormalizedTriplesChart.lean`](../../../../../../lean4/NormalizedTriplesChart.lean) and [`Target3NormalizedTriples.lean`](../../../../../../lean4/Target3NormalizedTriples.lean) (`ConcreteNormalizedTriple`, shared left gauge $V = U_0^\dagger$, `ZeroDenominatorLocus` isolation, regular corner charts non-degeneracy).
4. **Quantitative propagation of a residual gap into a collar or cusp patch**: Fully accomplished in [`LipschitzGapPropagation.lean`](../../../../../../lean4/LipschitzGapPropagation.lean), [`Target4GapPropagation.lean`](../../../../../../lean4/Target4GapPropagation.lean) ($L=85/9$, $\delta = 1/1000 < \delta_{\text{crit}} = 37249/850000$, $\varepsilon - L\delta = 12133/30000 > 0$), and [`Conjecture3GlobalClosure.lean`](../../lean4/research_programs/mub6/Conjecture3GlobalClosure.lean) (deltoid cusp blow-ups).
5. **Candidate-dependent Gram positivity and regional dual obstruction**: Fully accomplished in [`CandidateGramPositivity.lean`](../../../../../../lean4/CandidateGramPositivity.lean) (`gramian_psd_constructive`, `dual_witness_trace_nonneg`, `regional_dual_obstruction`).

Zero open derivation obligations remain from the 2026-09-18 prioritization. Active frontier obligations are tracked in [`mub6_gap_registry.json`](mub6_gap_registry.json).
