# Category: sos_degree4_tractability_and_pseudo_moment_gap

Type: failed_approach_category
Pattern: Equating variety emptiness with degree-4 SOS Positivstellensatz refutation overlooks potential non-flat pseudo-moments, while degree-4 SDP in 72 variables exceeds rational purification tractability.
Count: 15

## Entries
| # | Original File | One-line Summary |
|---|---------------|------------------|
| 1 | strategy_L00_N03 | Conflates non-convex flat rank equality with degree-2 convex SDP relaxation, facing a 2701x2701 PSD cone and 1.28 million constraints |
| 2 | strategy_L00_N07 | Degree-2 moment relaxation admits feasible pseudo-moment states on empty varieties, precluding dual degree-2 SOS refutations in Q |
| 3 | strategy_L00_N12 | Quartic elimination yields degree-4 polynomial system exceeding exact rational SOS SDP tractability across 128 eliminated variables |
| 4 | strategy_L00_N15 | Degree-4 SOS in 60 variables requires 635,376 equality constraints and 1891x1891 PSD cone, intractable for exact rational LDL^T factorization |
| 5 | strategy_L00_N16 | Putinar Positivstellensatz refutation in 440 real variables requires degree-2 SOS basis of 97,461 monomials, a 97,461x97,461 Gram matrix (70.8 GB), and over 1.597 billion degree-4 equality constraints |
| 6 | strategy_L01_N00 | Degree-4 moment relaxation assumes zero duality gap, but dropping the non-convex flat rank condition allows non-flat pseudo-moments that prevent SOS refutation; and rational Cholesky projection in 60 variables with 635,376 constraints is computationally intractable |
| 7 | strategy_L01_N04 | Degree-4 SOS in 440 variables requires a 97,461 x 97,461 Gram matrix with ~9.50 billion entries, which is computationally impossible to solve or certify in exact rational arithmetic |
| 8 | strategy_L01_N05 | Degree-2 SOS in 72 variables requires 1,282,975 monomial constraints and a 2701 x 2701 Gram matrix, intractable in SymPy; and continuous parameter perturbation bound has a wrong-sided sign where negative Delta(x) satisfies lambda_min(Q) > 0 without contradiction |
| 9 | strategy_L01_N14 | Conflating Curto-Fialkow flat extension (requiring non-convex rank(M_2) = rank(M_1)) with convex degree-4 SDP infeasibility overlooks non-flat pseudo-moments, while degree-4 SOS in 72 variables requires a 2701x2701 Gram matrix and 1,282,975 monomial constraints (intractable for rational certification) |
| 10 | strategy_L01_N15 | Conflating fixed-triple single-basis search (72 variables) with two-basis quartet search (120 free coordinates) distorts SOS polynomial degree and dimension, where full quartet certification exceeds SDP tractability limits |
| 11 | strategy_L02_N00 | Formulating degree-4 SOS in 60 variables only searches for a 3-MUB triplet; the true 4-MUB search requires 120 variables, a 7381x7381 Gram matrix, and 9.38M constraints |
| 12 | strategy_L02_N02 | Degree-4 SOS in 120 variables requires a 7381x7381 Gram matrix with 54.5M entries and 9.38M constraints, exceeding rational SDP solvers, while pseudo-moments may exist |
| 13 | strategy_L02_N04 | Degree-4 SOS Positivstellensatz certificates for two candidate bases face intractable polynomial sizing (120 real variables, 9.38M affine constraints) |
| 14 | strategy_L02_N05 | Parameterizing 60 variables searches only for known triplets; full 120-variable SOS relaxation requires a 7381x7381 PSD cone, making rational certification intractable |
| 15 | strategy_L03_N04 | Formulating two-basis quartet extension in Backup Route D requires 120 real variables (7,381 x 7,381 PSD cone with 54.5M entries and 9.38M constraints), where convex SDP relaxations drop Curto-Fialkow flat rank equality and permit non-flat pseudo-moments on empty varieties |

