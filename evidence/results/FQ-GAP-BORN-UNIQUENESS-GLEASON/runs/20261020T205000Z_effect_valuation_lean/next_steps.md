# Next derivations after review

1. Gaussian-rational Hermitian carrier: repeat `BornMatrixCarrier` and `BornTraceRepresentation`
   for matrices over ℚ(i) with the Hermitian form `x* A x`; the rank-one effects and the trace
   representation go through verbatim, the Gram decomposition needs conjugate pivots.
2. Operational justification of effect additivity: identify which finite-theory primitives
   (report maps, phase-blind descent, coarse-graining) give additivity on effects rather than on
   projections only; this is the hypothesis the result actually consumes (GF-5, L1-QM020 list).
3. Projection-only route: `parity_frame_function` shows additivity on orthogonal triples of
   rational rays is insufficient in `d = 3`; find the weakest finite hypothesis that restores the
   quadratic form (a rational continuity surrogate, or closure under all rational rotations), or
   show none exists below the continuum.
4. Connect with `H058EffectFrameBusch.lean` (cyclotomic real places): instantiate `OrderedQUnit`
   with the declared-place effect algebras there and reuse `linear_extension`.
5. Host review of the DAG node: the status is left `CONDITIONAL`; a reviewer may split the node
   into the effect-additive statement (kernel-checked) and the projection-lattice statement
   (import plus countermodel).
6. Python mutation harness: add a `Certificate` row for `born_effect_valuation.py` in
   `code/python/src/qm/tests/test_isolated_certificates.py` if the campaign banner convention is
   adopted for it.
7. Atlas: an optional Q-row for the effect-valuation route in `docs/QM_PROBLEM_AND_PROOF_ATLAS.md`
   with matching `textbook_problems` entries in Python and Rust.
