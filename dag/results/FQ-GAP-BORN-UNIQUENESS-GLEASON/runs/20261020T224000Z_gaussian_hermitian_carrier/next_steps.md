# Next derivations after review

1. Cyclotomic carriers: replace ℚ(i) by ℚ(ζ_n) with a declared real place (the `H058EffectFrameBusch`
   setting); `GaussRat` would become a general quadratic or cyclotomic extension with `star` the
   complex conjugation of that place, and the carrier proofs go through with `normSq` replaced by the
   place's norm.
2. Operational justification of effect additivity (unchanged obligation; see the effect-valuation
   run's next steps).
3. Unify the two carriers: a single `StarOrderedCarrier` structure instantiated by ℚ (trivial star)
   and ℚ(i), so that `BornMatrixCarrier` becomes the trivial-star instance of
   `BornHermitianCarrier`.
4. Tensor products over ℚ(i): compose Hermitian carriers and check that product effects and product
   states give the product valuation (connects to the tensor modules added in #115).
5. Host review of the DAG node status for the Gaussian-rational case; the node remains CONDITIONAL
   because the carrier and effect additivity are supplied.
