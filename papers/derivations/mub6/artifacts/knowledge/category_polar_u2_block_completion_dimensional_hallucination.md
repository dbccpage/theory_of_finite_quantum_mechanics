# Category: polar_u2_block_completion_dimensional_hallucination

Type: failed_approach_category
Pattern: Claiming finite cell covers of 9-to-13 dimensional moduli spaces with ~10^5 cells when coarse diameter yields non-excluding interval widths, coupled with tolerance graph edge saturation.
Count: 16

## Entries
| # | Original File | One-line Summary |
|---|---------------|------------------|
| 1 | strategy_L00_N02 | In 9 dimensions, 10^5 cells yield coordinate diameter 1.75 rad and interval half-width 1.85, excluding zero cells |
| 2 | strategy_L00_N06 | Dimension miscount of orthogonality equations (15 complex vs 30 real) and seed remainder ||Delta D|| >= 0.70 rad contradict claimed 0.03 rad phase balls |
| 3 | strategy_L01_N01 | Claiming 22,379 phase balls of radius 0.016 cover H_6 is refuted by 2D Hausdorff measure (F_6(a,b) alone requires >= 49,089 balls); and Frobenius cell displacement z >= 0.899 is 56x larger than phase ball radius 0.016 |
| 4 | strategy_L01_N02 | 22,379 phase balls cover < 46% of a single 2D family and omit the 3D Karlsson manifold (> 14.4M balls required); and Stage C Lloyd clustering at M=24 has bin diagonals (0.0932) exceeding cluster diameters (0.084) |
| 5 | strategy_L01_N03 | Stage C Lloyd clustering at M in {12, 24} has bin corner distances (0.0932 and 0.0466) exceeding cluster radius 0.042, allowing feasible candidate vectors in bin corners to escape graph representation |
| 6 | strategy_L02_N00 | Stage C Lloyd clustering with multi-bin clusters at M=48 has corner distances 0.0477 > s=0.042, leaking candidate vectors from the graph |
| 7 | strategy_L02_N01 | 22,379 phase balls cover < 45.6% of 2D Fourier-Dita family and < 0.16% of 3D Karlsson family, leaving over 99.8% of parameter volume uncovered |
| 8 | strategy_L02_N03 | Stage C Lloyd clustering at M=48 leaks candidates beyond cluster radius s=0.042, and phase ball atlas lacks measure to cover higher-dimensional moduli |
| 9 | strategy_L02_N05 | Parameterizing 60 real variables only captures a single candidate basis (a 3-MUB triplet); a 4-MUB search requires 120 real variables |
| 10 | strategy_L02_N07 | Phase ball atlas covers < 0.16% of 3D Karlsson manifold and Lloyd clustering allows candidate phases to escape in bin corners |
| 11 | strategy_L03_N00 | Midpoint greedy clustering at M=48 leaks diagonal neighbor corners (d=0.0477 > s=0.042), and Frobenius displacement z >= 0.899 causes Taylor remainder (1/2)z^2 >= 0.404 to dominate dual separation thresholds |
| 12 | strategy_L03_N01 | Minimax set covering at M >= 48 with r_allow = 0.01871 < 1/M limits cluster capacity to 1-8 bins, requiring > 2,000 to 5,000 clusters for realistic bin counts, blowing past the C++ pipeline's 2048-vertex cap |
| 13 | strategy_L03_N02 | 5D ball volume of radius 0.01871 is 1.21e-8, requiring > 829,000 cluster balls to cover 1% of the surviving phase domain, rendering bipartite 12-clique search computationally intractable |
| 14 | strategy_L03_N03 | Multi-bin clusters of diameter 2s=0.084 at M >= 96 leak corners beyond s=0.042 whenever bin center distance exceeds 0.03035 (for distance 0.035, corner distance is 0.0466 > 0.042) |
| 15 | strategy_L03_N04 | Multi-bin clustering at M=48 leaks corners for diagonal neighbors (0.0477 > 0.042), axis spans k=4 (0.0466 > 0.042), and 3-diagonals (0.0561 > 0.042), omitting candidate vectors and risking false-negative clique destruction |
| 16 | strategy_L04_N00 | Certified single-bin clustering at M=48 requires thousands of clusters (N_bin ~ 2000-10000), instantly exceeding the C++ pipeline's 2048-vertex cap, while multi-bin grouping leaks diagonal corners (0.0477 > 0.042, ratio 1.137x); certified clustering was never executed across the 23,506 records |

