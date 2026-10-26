# WDP-APPM-T1

Goal id: WDP-APPM-T1

Selected scope for WDP-APPM-T1 is recorded in this note.

## Selected scope

Labelled finite carrier: all 24 distinct simple 4-cycles on the torus (Z/4Z)^2, 16 sites, periodic nearest-neighbour grid. They are 16 facial 4-cycles of winding (0,0) and 4 horizontal plus 4 vertical winding 4-cycles. Each undirected cycle is one orbit U=(Z/2Z)^1 with constant weight A=1 and baseline sign s=+1. The meron bit is m=(W_x+W_y) mod 2. The ensemble is the disjoint union of these 24 orbits, 48 orientations. Exact signed partition Z=32; for O(u)=(-1)^u, numerator N=16. Not the 1D value 912, not longer cycles, and not a continuum limit.

## Hypotheses

The hypotheses are selected for this carrier. Appendix M.1 states that a complete orbit, invariant weights, and the character law must be established for the selected model. The pinned T1 receipt does not supply them.

H1. Sites are pairs (x, y) in {0, 1, 2, 3}^2. Undirected edges join (x, y) to (x±1, y) and to (x, y±1), with coordinates mod 4.

H2. Configurations are the two orientations of each simple 4-cycle. Each step lifts to one vector in {±e_x, ±e_y}. The winding is the lift displacement in Z^2 divided by 4.

H3. Each undirected cycle is the complete orbit U=(Z/2Z)^1. The weight A=1 is constant, and the baseline sign is s=+1.

H4. The sign character is chi_m(u)=(-1)^{m u}, with m=(W_x+W_y) mod 2. Thus m=0 on faces and m=1 on the eight generator cycles. The declared observable is O(u)=(-1)^u on that group coordinate.

## Derivation

A closed walk of length 4 has lift displacement (Δx, Δy) with |Δx|+|Δy| ≤ 4 and with both coordinates in 4Z. The only such displacements are (0, 0), (±4, 0), and (0, ±4). Hence W lies in {(0, 0), (±1, 0), (0, ±1)}.

Write n(+x), n(-x), n(+y), and n(-y) for the step counts. They sum to 4, Δx = n(+x)-n(-x), and Δy = n(+y)-n(-y). The pairs above are the only closing counts:

- W=(±1, 0) uses four equal horizontal steps. The support is one of 4 rows, and each row is one undirected 4-cycle.
- W=(0, ±1) uses four equal vertical steps. The support is one of 4 columns.
- W=(0, 0) has n(+x)=n(-x) and n(+y)=n(-y). The solutions are two steps each horizontal way, two steps each vertical way, or one step in each of the four directions.

If W is nonzero, the opposite orientation negates W and keeps the edge set. In both orientations, (W_x+W_y) mod 2 equals 1.

If the walk is purely horizontal, the six sequences with two steps each way have lift positions

++--: {0, 1, 2}; +-+-: {0, 1}; +--+: {0, 1, -1}; -++-: {0, -1, 1}; -+-+ : {0, -1}; --++: {0, -1, -2}.

Each image lies in an integer interval of length at most 2, so it has at most 3 points. The diameter is less than 4, so the projection to one row of the torus still has at most 3 points. The pure vertical case is the same after swapping axes. Neither is a simple 4-cycle.

A simple null-homologous 4-cycle therefore uses one step in each direction. An immediate reversal repeats a vertex, so +x is opposite -x and +y is opposite -y. Up to rotation, the two cyclic orders are (+x, +y, -x, -y) and (+x, -y, -x, +y).

Based at (x, y), the first order has edge set

E(x, y) = {((x, y), (x+1, y)), ((x+1, y), (x+1, y+1)), ((x+1, y+1), (x, y+1)), ((x, y+1), (x, y))}.

The second order based at (x, y) is E(x, y-1). As (x, y) runs through the 16 sites, these are 16 edge sets. They are distinct because (x, y) is the only vertex of E(x, y) that is the tail of both the positively oriented horizontal edge and the positively oriented vertical edge of that face. Each has W=(0, 0), hence m=0. Reversal is the other orientation of the same edge set, and rotation only moves the base point.

A face uses two horizontal edges and two vertical edges. A generator cycle uses four edges of one direction. The 16 faces, 4 row cycles, and 4 column cycles are therefore 24 distinct edge sets. No other step multiset closes in 4Z^2, and no other balanced multiset gives a simple 4-cycle.

H3 and H4 place each edge set in its own orbit of order 2. The signed weight of orientation u is A s chi_m(u). With A=1 and s=+1, that weight is chi_m(u).

Appendix M.1 gives Z_U = A s 2^k when m=0, and Z_U = 0 when m is nonzero. Here k=1, so each face contributes 2 and each of the eight generator orbits contributes 0. The disjoint union has

Z = 16·2 + 8·0 = 32.

For m nonzero, the same appendix cancels the orbit by u ↦ u+1: the weight is preserved and the sign flips, so the two orientations contribute +1 and -1.

For the declared O, Appendix M.1 sets

hat O(m) = 2^{-k} sum_{u in U} chi_m(u) O(u), and N_U = A s 2^k hat O(m).

Swapping which orientation is called u=0 replaces u by u+1. On a face the sum of O remains 0. On a generator orbit, chi_m(u) O(u) remains 1. The orbit numerators do not depend on that label.

On a face, m=0, so sum_u O(u) = 1+(-1) = 0, hence hat O(0)=0 and N_U=0. On a generator orbit, m=1, so chi_m(u) O(u)=1 for both orientations, the sum is 2, hat O(1)=1, and N_U=2. Thus

N = 8·2 + 16·0 = 16.

Each of these eight odd orbits is the k=1 counterexample in M.1: with A=1, s=1, and O(u)=(-1)^u, the partition contribution is 0 and the numerator is 2. The Fourier coefficient at m=1 is 1, not 0, so deleting the odd orbits does not preserve this numerator.

Each orientation has absolute weight 1, so the absolute weight sum is 48. The average sign on this carrier is 32/48 = 2/3. The signed partition is nonzero, so the normalized expectation of this O is N/Z = 16/32 = 1/2 on this carrier only. One orientation does not represent the face average of O, because O takes both values on each face.

The integer 912 is not an input to these sums. Appendix M.4 records Z(4)=912, Z(6)=33012, and Z(8)=973824 from the occupation-basis checkerboard transfer at repetitions=2 and q=3. That trace sums all 2^L occupation states and does not project to a fixed particle number. In the opened implementation, meron_transfer_trace builds a matrix of dimension 2^sites and updates it once for each of 2·repetitions checkerboard steps. The value 912 is the call sites=4, repetitions=2, q=3. meron_database sets times=2·repetitions and inserts one node for each pair (t, x), hence 16 spacetime nodes of the periodic even chain, not a labelled 16-site spatial torus. The same constructor rejects a site count other than 4 or 6 and rejects sites·repetitions>12.

Appendix M.5 states that the pinned T1 record reuses the 1D value 912 and does not construct its labelled 16-site torus model, and that T1–T5 are a useful order of work rather than a prerequisite chain. The bridge row for T1 says the pinned source assigns Z=912 and sites=16 together with fixed winding counts, and that the 1D trace is not that calculation. The opened function compute_t1_receipt sets dimension 2 and sites 16, then assigns exact_partition_z=912, odd_winding_clusters_cancelled=192, zero_odd_subgraphs_retained=64, and duality_gap 0, together with a thermodynamic_limit_f_inf_interval taken from the Wilsonian bridge. Its test asserts dimension 2, sites 16, exact_partition_z equal to 912, odd_winding_clusters_cancelled equal to 192, and duality_gap equal to the string 0. Those integers are not indexed by these 24 edge sets. Appendix M.4 says that the Neville width is interpolation width and that three samples do not bound an unrestricted limit.

The opened generator build_canonical_2d_gn_ensemble(4, 4) returns six hand-specified clusters, with weights 100, 50, 25, 25, 35, and 35. The opened test records zero-meron sum 150. Appendix M.5 requires later 2D implementations to carry their own source correspondence and model-error proofs, so that list is not this carrier.

## Claims this note does not make

- It does not identify the partition of this 16-site torus with 912.
- It does not place 192 cancelled odd clusters, or 64 retained zero-odd subgraphs, on these sites.
- It does not take 912, 192, 64, the f_inf interval, or the six-cluster sum 150 as an orbit sum of these 24 cycles.
- It does not assert weight invariance or sign inversion for an ensemble other than these 24 orbits under H3 and H4.
- It does not identify the six-cluster Gross-Neveu list with this ensemble.
- It does not call f_inf a 2D free-energy density or a continuum limit.
- It does not derive a fermion determinant, half-filling, or reflection positivity.
- It does not treat the order T1–T5 as a prerequisite chain.
- It does not treat wire syntax or receipt hashes as a physical law.
- It does not state a thermodynamic limit, a field equation, or any result about cycles longer than 4.
- It does not extend the constant weight A=1 to non-constant bond weights.
- It does not say that cancelling an odd orbit preserves an arbitrary observable. Appendix M.1 keeps the numerator if and only if the Fourier coefficient at that character vanishes. For this O, the coefficient on each odd orbit is 1, not 0.
- It does not say that one orientation represents the face average of O. On each face, O takes both values +1 and -1.
- A finite model on this carrier does not establish a continuum limit, a physical law, or a closed theorem outside the selected scope.
