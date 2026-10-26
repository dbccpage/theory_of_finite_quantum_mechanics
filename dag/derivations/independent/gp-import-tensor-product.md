Status: AI-drafted, awaiting human review.

Let Bool be the two-element set {false, true}. A vector on this host is a function from Bool to the ordinary integers. Write delta i for the function that is 1 at i and 0 at the other point. Write (u ⊗ v)(a, b) for the integer u(a) * v(b). This is the pointwise product on the four points of Bool × Bool.

Each vector splits on the two deltas. At a point q,

u(q) = u(false) * delta false(q) + u(true) * delta true(q),

and the same formula holds for v. Substitute both expansions into a map E that is additive in each argument and homogeneous for multiplication by an integer in each argument. The value E(u, v) at a point (a, b) becomes the integer combination

u(false) * (v(false) * E(delta false, delta false)(a, b) + v(true) * E(delta false, delta true)(a, b))
+ u(true) * (v(false) * E(delta true, delta false)(a, b) + v(true) * E(delta true, delta true)(a, b)).

If E sends the pair (delta i, delta j) to delta (i, j), exactly one of those four deltas is 1 at (a, b), and the combination equals u(a) * v(b). So every such map agrees with the pointwise product. The pointwise product itself satisfies the same four laws, so the class is not empty.

The dump-right map uses the same hosts and a weaker placement of the deltas. On a point whose second coordinate is false it returns u(a) * (v(false) + v(true)). On a point whose second coordinate is true it returns 0. Adding vectors or multiplying a vector by an integer on either side passes through this formula, because multiplication by a fixed integer distributes over addition. On a delta pair, v(false) + v(true) = 1, so the map returns delta i(a) when the second coordinate is false and returns 0 when the second coordinate is true. That is delta (i, false), not delta (i, j).

Take u = delta false and v = delta true, and evaluate at (false, true). The pointwise product is delta false(false) * delta true(true) = 1. The dump-right map reads the true second coordinate and returns 0. The two maps are not the same function.

What is proved

The pointwise formula, agreement of every additive integer-homogeneous identity-tagged map with that formula, the two coordinate formulas for the dump-right map, its additivity and integer homogeneity, the collapsed tag delta (i, false), and the pair of values 0 and 1 at the stated delta inputs.

What is assumed

The ring laws of the integers, the two-element set Bool, and the definitions of delta, the pointwise product, and the dump-right map. AuthorityEffect: None.

What is open

A Hilbert-space tensor product is not derived, and it is not shown to be the only way to combine systems. The agreement uses one finite host, integer coefficients, additivity, integer homogeneity, and the identity tag. The dump-right map is a rival only for a tag that forgets the second Boolean factor. A second presented carrier and a physical composition rule stay imported.
