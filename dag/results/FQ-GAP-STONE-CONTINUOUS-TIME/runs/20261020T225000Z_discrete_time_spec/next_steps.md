# Next derivations after review

1. Triviality of ℚ-parameter groups over ℚ(i): norms along a ℚ-parameter group in ℚ(i)* are perfect
   m-th powers for every m, hence 1; then unique factorisation in ℤ[i] (Mathlib `GaussianInt`) shows the
   unit-circle group of ℚ(i) is torsion × free abelian, so its only divisible subgroup is trivial.
   Formalise for 1×1 first, then for diagonalisable matrices.
2. Degree growth of roots: the m-th roots of (3+4i)/5 generate extensions of degree growing with m
   (Kummer); this prices "continuous time" by the field degree of the carrier extension.
3. Connect the specification to `H055DiscreteDynamicsStone` (the two scaled ℚ(i) interpolants of the
   swap are an instance of `half_step_not_unique`) and to `PromptDynamics.stone_gap_alias`.
4. Commit the working-copy modules `U1PythagoreanObstruction.lean` / `U1PowerMapInjectivity.lean` so the
   node can cite the scalar facts (currently uncommitted; not pinned by this run).
5. Host review of the node status: the specification and the 2×2 obstruction are kernel-checked; the
   node remains CONDITIONAL because strong continuity and the real completion are still imports.
