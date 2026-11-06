# Next derivations after review

1. Operational source of the two laws. Sector additivity of the quadratic readout is transcribed from
   the l1 additivity of sector weights; state and prove the lift lemma "a readout that reproduces the
   l1 sector weights on every sector-supported vector is sector additive" on the H004 free
   linearisation, so that the hypothesis is discharged from L1-GS000 rather than assumed. For the
   symmetry law, identify the finite-theory primitive (report relabelling, H006 `Reversible`) that
   forces readout invariance, or record which sector labels are distinguished and keep the orbit-wise
   statement.
2. Linear isometric dynamics (L1-IMP-LINEAR-ISOMETRIC-DYNAMICS). With the form now fixed up to scale,
   every readout-preserving linear map is an isometry of the standard form; prove that the permutation
   envelope of H006 and the rational Cayley steps of the Stone run preserve it, closing the route
   L1-R-DYNAMICS-GAP from this result.
3. Effect additivity for the Born runs. Combine `eq_one_of_normalized` with the orthogonality of the
   sector basis to derive additivity of the Born valuation on orthogonal rank-one effects from
   additivity on sectors, which is item 2 of the effect-valuation run's next steps.
4. Cyclotomic carriers: repeat `SectorFormHermitian` over ℚ(ζ_n) with a declared real place (the
   `H058EffectFrameBusch` setting); the two-direction argument becomes a φ(n)-direction argument over
   a ℚ-basis of the field.
5. Host review of the DAG nodes: L1-IMP-HILBERT-INNER-PRODUCT and L1-IMP-ORTHOGONAL-ADDITIVITY are
   recorded as CONDITIONAL on the two laws; a reviewer may split the orthogonality statement (derived
   from sector additivity alone) from the scalar-form statement (which also needs symmetry).
