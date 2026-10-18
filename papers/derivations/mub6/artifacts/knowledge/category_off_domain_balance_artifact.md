# Category: off_domain_balance_artifact

Type: failed_approach_category
Pattern: Treating coordinate 368 separation on the artificial low-row test box as candidate exclusion, conflating an off-domain test box with candidate chart refutation.
Count: 23

## Entries
| # | Original File | One-line Summary |
|---|---------------|------------------|
| 1 | strategy_L00_N00 | Test box B_low restricts transition real parts to [-1/2, 1/2], whereas actual candidate charts require at least one entry >= 1 |
| 2 | strategy_L00_N01 | Coordinate 368 derived interval [3.5, 8.5] exceeds maximum possible Hadamard modulus sqrt(6) and is disjoint from all candidate charts |
| 3 | strategy_L00_N04 | Balance equation sum x_j = 6 is satisfied on the interior of the candidate variety (e.g. x_j = 1), generating zero balance separation |
| 4 | strategy_L00_N05 | Linear balance constraint completely overlaps any box intersecting the true balance hyperplane, failing on feasible slices |
| 5 | strategy_L00_N07 | mub_szollosi_balance_exclusion_receipt.json evaluated an artificial box with coordinate sum <= 3, contracting zero candidate coordinates |
| 6 | strategy_L00_N08 | Balance coordinate separation on [-1/2, 1/2]^6 test box does not transfer to actual candidate charts where row sum is 6 |
| 7 | strategy_L00_N09 | Claimed balance exclusion occurs solely on off-chart test box where entries cannot reach row sum 6, yielding zero separation on charts |
| 8 | strategy_L00_N10 | Test box B_test has empty intersection with all six solution charts C_k; actual chart image [-9, 21] fully covers chart domain [1, 3] |
| 9 | strategy_L00_N11 | Low-row test box separation provides zero exclusion inside actual candidate charts where symmetric solutions x_j = 1 exist |
| 10 | strategy_L00_N13 | Coordinate 368 separation on B_test is an artifact of restricting entries to [-1/2, 1/2], giving zero chart separation on C_k |
| 11 | strategy_L00_N16 | Pigeonhole condition X_{0k}^{(W)} >= 1 has zero algebraic conflict with (X_{0k}^{(W)})^2 + (Y_{0k}^{(W)})^2 = 6, since every regular complex Hadamard matrix satisfies both conditions |
| 12 | strategy_L00_N19 | Vacuous subbox exclusion on [-1/2, 1/2]^6 (sum <= 3 < 6) masks complete contractor stagnation on actual candidate charts where row sum is 6 |
| 13 | strategy_L00_N20 | Coordinate 368 separation on B_{test} was an artifact of sum <= 3 < 6; on actual candidate charts C_k, balance equations admit infinitely many solutions |
| 14 | strategy_L00_N25 | Lean low_row_box_empty exclusion is a trivial arithmetic check (6 * 0.5 = 3 < 6) disjoint from candidate charts where Re(W_{0j}) >= 1 |
| 15 | strategy_L00_N26 | Low-row box B_low (Re(W_{0j}) in [-1/2, 1/2]) is separated by trivial arithmetic (6 * 0.5 = 3 < 6), but B_low contains zero candidate solutions; all 6 actual charts retain Re(W_{0j}) >= 1 and return UNRESOLVED_BOX |
| 16 | strategy_L00_N27 | Lemma_Balance_Critical_Threshold (c < c_crit = (6 - sqrt(6))/5 approx 0.710102) excludes zero admissible points because w_0 <= sqrt(6) and sum w_k = 6 algebraically forces max_{j=1..5} w_j >= c_crit |
| 17 | strategy_L00_N28 | LowRowBox condition x_k in [-1/2, 1/2] for all k is strictly disjoint from chart domains C_j where x_j in [1, 3], meaning balance separation prunes zero leaf boxes inside any chart |
| 18 | strategy_L01_N00 | Row-permuted Hadamard matrices from the 518,400 equivalence orbits break the 24 balance identities (row sums evaluate to 3 +/- 5.2i != 6), refuting their silent absorption under general unitary equivalence |
| 19 | strategy_L01_N03 | Preserving Route A balance coordinate 368 separation as candidate exclusion overlooks that separation is an off-domain artifact failing with 100% overlap on feasible balance hyperplanes |
| 20 | strategy_L01_N04 | Claiming variety emptiness in candidate charts C_j via balance equations is refuted by explicit feasible points z_j = 1 +/- i*sqrt(5) with Re(z_0) >= 1, |z_j|^2 = 6, and sum z_j = 6 having zero residual |
| 21 | strategy_L01_N06 | Linear balance threshold x_j <= 0.71 prunes exactly 0.0000% of feasible points in Chart 0 (0 out of 77,030 samples), providing zero pruning on the interior candidate variety |
| 22 | strategy_L01_N10 | The 24 balance equations are algebraic syzygies of row-1 gauge and column unitarity (V V^dagger = 6 I_6), adding zero variety codimension and empirically worsening interval preconditioner error norms by 31.7% |
| 23 | strategy_L02_N00 | Preserving coordinate 368 balance separation treats an off-domain test box artifact as valid pruning, providing zero exclusion on actual candidate charts |
