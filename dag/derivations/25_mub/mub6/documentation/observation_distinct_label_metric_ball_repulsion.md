# Metric Ball Repulsion and Distinct Label Property for Candidate MUB Vectors

Type: observation
Confidence: high
Source: Candidate strategy_L00_N18 (Level 0); Candidates strategy_L03_N00, strategy_L03_N01, strategy_L03_N02, strategy_L03_N03, strategy_L03_N04 (Level 3); Candidate strategy_L04_N00 (Level 4)
Relevant to: Branch-and-bound clustering, graph clique formulation, and discretization of candidate MUB vector search in dimension 6

## Statement
Let $u, v \in \mathbb{C}^6$ be normalized candidate vectors ($|u_j| = 1/\sqrt{6}$ and $|v_j| = 1/\sqrt{6}$ for all $j \in \{0, \dots, 5\}$). If their relative phase displacement vector $z \in [-\pi, \pi]^6$ (after removing any global phase) satisfies $\|z\| \le 2s < 0.2$ for metric ball radius $s < 0.1$, then:
$$|\langle u, v \rangle| > \frac{1}{\sqrt{6}} \quad \text{and} \quad \langle u, v \rangle \ne 0.$$
Consequently, two distinct candidate vectors lying in the same metric ball of radius $s < 0.1$ can be neither orthogonal nor mutually unbiased to one another.

## Evidence
1. **Radian Norm Bounds**:
   Writing $u_j = \frac{1}{\sqrt{6}} e^{i \alpha_j}$ and $v_j = \frac{1}{\sqrt{6}} e^{i \beta_j}$, with phase differences $z_j = \beta_j - \alpha_j$, the unscaled inner product is $\sum_{j=0}^5 e^{i z_j}$. By the reverse triangle inequality and the Taylor expansion $|1 - e^{i z_j}| \le |z_j|$:
   $$\left| \sum_{j=0}^5 e^{i z_j} \right| \ge 6 - \sum_{j=0}^5 |1 - e^{i z_j}| \ge 6 - \sum_{j=0}^5 |z_j| \ge 6 - \sqrt{6} \|z\|_2.$$
   For $\|z\|_2 < 0.2$, this gives:
   $$\left| \sum_{j=0}^5 e^{i z_j} \right| > 6 - 0.2 \sqrt{6} \approx 6 - 0.4899 = 5.5101 > \sqrt{6} \approx 2.4495.$$
2. **Level 3 Parameter Evaluations (Chordal Form in $[0, 1]^5$)**:
   In Level 3 syntheses, coordinates are expressed in turns $\beta \in [0, 1]^5$ where $e(z_j) = e^{2\pi i z_j}$. For cluster ball radius $s = 0.042$ and $\|z\|_2 \le 2s = 0.084$:
   $$\left| \sum_{j=0}^5 e^{2\pi i z_j} \right| \ge 6 - 4\pi \sqrt{6} s = 6 - 4\pi \sqrt{6} (0.042) \approx 6 - 1.292810 = 4.707190 > \sqrt{6} \approx 2.449490.$$
   The strict margin is $4.707190 - 2.449490 = 2.257700 > 0$.
   At $s = 0.08$, the lower bound evaluates to $3.537504 > 2.449490$; at $s = 0.1$, it evaluates to $2.921880 > 2.449490$.
   Normalizing by $1/6$, the inner product modulus satisfies $|\langle u, v \rangle| > \frac{\sqrt{6}}{6} = \frac{1}{\sqrt{6}} > 0$. Orthogonality requires inner product 0, and mutual unbiasedness requires inner product $1/\sqrt{6}$. Both conditions are ruled out by the strict inequality.

## Implications
1. Any two orthonormal candidate bases $U_2, U_3$ in a candidate quartet contain 12 distinct vectors that must occupy 12 distinct metric balls of radius $s = 0.042$.
2. This establishes the Distinct Label Property, enabling candidate phase bins to be clustered into graph vertices without risking that multiple basis vectors collapse into a single cluster.

## Claim Hygiene Summary
- **What it supports**: Supports that candidate vectors within distance $s \le 0.042$ in phase space cannot be orthogonal or mutually unbiased, justifying single-label bin clustering in graph reductions.
- **What it does not support**: Does not support that an arbitrary cluster cover is complete across non-convex feasible regions without checking boundary margins.
- **Narrowest defensible claim**: For any two vectors with entries of modulus $1/\sqrt{6}$ whose relative phase difference satisfies $\|z\|_2 \le 0.084$ in turn coordinates, their unscaled inner product modulus strictly exceeds $\sqrt{6} \approx 2.449490$ with margin $\ge 2.257700$.
- **Next test needed**: Evaluate outward rounding enclosures to ensure cluster balls cover all surviving phase bins without gaps.

