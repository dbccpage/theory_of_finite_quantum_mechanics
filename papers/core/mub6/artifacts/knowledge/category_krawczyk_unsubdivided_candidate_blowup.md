# Category: krawczyk_unsubdivided_candidate_blowup

Type: failed_approach_category
Pattern: Vanishing derivatives of purely quadratic candidate constraints at box centers cause preconditioner row-annihilation, yielding uncontracted intervals and astronomical subdivision requirements.
Count: 31

## Entries
| # | Original File | One-line Summary |
|---|---------------|------------------|
| 1 | strategy_L00_N00 | Centering at origin yields vanishing candidate Jacobian columns and non-invertible Schur normal matrices due to continuous Hadamard defect |
| 2 | strategy_L00_N01 | Bilinear cross-products have zero gradients at midpoint c=0, giving rank 0 on candidate coordinates and zero contraction |
| 3 | strategy_L00_N04 | Moore-Penrose pseudo-inverse has identically zero rows for candidate coordinates at origin center, precluding derivative contraction |
| 4 | strategy_L00_N05 | Sparse preconditioner with under 300 nonzeros has at least 140 zero rows, forcing unit eigenvalue in error matrix |
| 5 | strategy_L00_N07 | Phase-only bisection leaves candidate coordinates at full width, causing operator norm to reach 59.87 and precluding separation |
| 6 | strategy_L00_N08 | Vanishing quadratic derivatives at candidate center force zero preconditioner rows and wide interval wrap, requiring astronomical subdivision depth |
| 7 | strategy_L00_N09 | Unsubdivided candidate coordinates maintain full [-1, 1] width, preventing contractive Krawczyk enclosure and failing radius test |
| 8 | strategy_L00_N10 | Dyadic bisection over 8 phase parameters leaves 432 candidate variables uncontracted, causing combinatorial fiber explosion |
| 9 | strategy_L00_N11 | Quartic elimination fails to prevent Krawczyk norm divergence across 128 auxiliary coordinates; interval Jacobian expands by over 10x |
| 10 | strategy_L00_N12 | Eliminating auxiliary variables raises polynomial degree to 4, expanding interval widths and failing contraction radius |
| 11 | strategy_L00_N13 | 8-parameter bisection fails to contract 120 free candidate coordinates in 440-variable variety, leaving off-diagonal interval bounds wide |
| 12 | strategy_L00_N17 | Direct interval residual evaluation on cusp collar boxes without preconditioning evaluates to [-6, 282] over [-1, 1]^{144}, containing zero in all coordinate ranges |
| 13 | strategy_L00_N19 | Rectangular Krawczyk on 440 real variables suffers severe dependency inflation and wrapping; all six native candidate charts return UNRESOLVED_BOX |
| 14 | strategy_L00_N20 | Bilinear coupling Jacobian vanishes at midpoint x_0 = 0 (d T_{ij} / d W = 0); bisecting only 12 transition coordinates leaves 120 raw coordinates with width 2, giving residual uncertainty >= 20 |
| 15 | strategy_L00_N23 | Partitioning only the 1D parameter theta into 56 cells leaves 416 candidate coordinates at full box width [-1, 1]^{144} x [-3, 3]^{216}, leading to either 2^{416} ~ 10^{125} subboxes or catastrophic wrapping |
| 16 | strategy_L00_N25 | 440-variable Krawczyk exhibits severe wrapping; bisecting 6 transition coordinates leaves 434 coordinates wide (radius 1 or 3), creating an interval Jacobian expansion factor > 10 to 10^{14} and zero separation |
| 17 | strategy_L00_N26 | Minimum Krawczyk interval image radius across all 440 variables exceeds 98.7 (median 179.6) due to 432 unsubdivided candidate variables (width 2 to 6), swamping box bounds and precluding separation |
| 18 | strategy_L00_N27 | 144 candidate coordinates of width 2 cause interval Jacobian width > 15, and at candidate midpoint x_c = 0 all quadratic derivatives vanish identically, giving a 408-dimensional nullspace |
| 19 | strategy_L00_N28 | Rank-416 Jacobian in 440 variables has a 24-dimensional gauge nullspace forcing eigenvalue 1 with multiplicity 24 (spectral radius >= 1), making strict contraction ||I - A J||_infty < 1 strictly impossible; unsubdivided candidate coordinates expand by 66x in radius |
| 20 | strategy_L00_N30 | Monolithic 440-coordinate Krawczyk contractor returns CONTRACTED_UNRESOLVED_BOX on full box and UNRESOLVED_BOX on all 6 candidate charts due to severe dependency inflation and residual gauge freedom |
| 21 | strategy_L00_N31 | Unfixed continuous phase gauge orbits cause unavoidable rank deficiency in 440-variable Jacobian midpoints, trapping rectangular Krawczyk bisection in CONTRACTED_UNRESOLVED_BOX across 416 unresolved coordinates |
| 22 | strategy_L01_N02 | Retaining sparse preconditioners with <= 300 nonzeros has >= 140 zero rows, forcing eigenvalue 1.0 and precluding strict Krawczyk contraction |
| 23 | strategy_L01_N06 | Uniform off-origin rational centers (e.g. (3/5, 4/5)) cause row-unitarity gradients to become linearly dependent, dropping candidate Jacobian rank to 35/60 (nullity 25); and 440D interval wrapping inflates error radius to > 2818, requiring ~10^{357} subboxes |
| 24 | strategy_L01_N07 | Rational box midpoints c=(l+u)/2 fail to break derivative symmetry because transition variables appear linearly with coefficient 1 in Z_{12} - H_1^dagger H_2, so free candidate basis derivatives remain identically zero; and HC4-revise achieves 0.0% contraction on basis intervals |
| 25 | strategy_L01_N08 | Transverse 416-variable projection eliminates 24 gauge directions, but unsubdivided candidate coordinates across 120 variables expand radii > 25x, causing Krawczyk operator to fail contractivity |
| 26 | strategy_L01_N09 | Phantom coupling between polar U(2) block isometry and 416-variable Krawczyk operator leaves candidate coordinates evaluated over Cartesian interval boxes in R^{416}, incurring a 119.58x interval wrapping inflation factor and leaving a 2D phase nullspace |
| 27 | strategy_L01_N10 | Unsubdivided 120 candidate basis coordinates induce 25x to 66x wrapping inflation, requiring ~10^{192} subboxes to contract under rectangular Krawczyk |
| 28 | strategy_L01_N11 | At domain midpoint x_0 = 0, quadratic candidate Jacobian rank is <= 32 (nullity >= 408), making depth-16 branch-and-bound with uncontracted candidate coordinates fail completely |
| 29 | strategy_L01_N12 | Manifold-centered preconditioning on T^{144} yields operator norm > 40 on subboxes of width delta = 1/8 due to >= 18 null dimensions from continuous symmetries |
| 30 | strategy_L01_N13 | Degree-4 mutual overlap polynomials between two variable candidate bases violate the quadratic midpoint secant identity, introducing nonzero higher-order Taylor remainders that invalidate exact rectangular Krawczyk enclosure |
| 31 | strategy_L02_N06 | Unsubdivided candidate coordinates across 120 variables suffer derivative rank collapse at origin midpoints and catastrophic wrapping expansion |
