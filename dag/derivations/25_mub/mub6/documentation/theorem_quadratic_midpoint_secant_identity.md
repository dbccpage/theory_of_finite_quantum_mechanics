# Exact Quadratic Midpoint Secant Identity and Rectangular Enclosure

Type: theorem
Confidence: high
Source: Candidates strategy_L00_N00, strategy_L00_N01, strategy_L00_N04, strategy_L00_N05, strategy_L00_N07 (Level 0)
Relevant to: Sound interval exclusion of candidate boxes for overdetermined quadratic polynomial systems without higher-order Taylor truncation error.

## Statement
Let $p: \mathbb{R}^n \to \mathbb{R}$ be a polynomial of total degree at most two:
$$p(x) = \frac{1}{2} x^T Q x + b^T x + d,$$
where $Q \in \mathbb{R}^{n \times n}$ is symmetric, $b \in \mathbb{R}^n$, and $d \in \mathbb{R}$.
For any two vectors $c, r \in \mathbb{R}^n$, let $m = \frac{c + r}{2}$ be their algebraic midpoint. Then the difference $p(r) - p(c)$ satisfies:
$$p(r) - p(c) = \nabla p(m) \cdot (r - c)$$
identically, with zero remainder.

For any vector mapping $F: \mathbb{R}^n \to \mathbb{R}^m$ of quadratic polynomials, closed box $B \subset \mathbb{R}^n$, expansion center $c \in B$, and preconditioner matrix $A \in \mathbb{Q}^{n \times m}$, every root $r \in B$ with $F(r) = 0$ satisfies:
$$r \in K(c, B) := c - A F(c) + (I_n - A [J_F(B)]) (B - c),$$
where $[J_F(B)]$ is the outward-rounded interval Jacobian enclosure over $B$.
Consequently, if there exists an index $k \in \{1, \dots, n\}$ such that:
$$K(c, B)_k \cap B_k = \emptyset,$$
then the polynomial system $F(x) = 0$ has no solution in $B$.

## Proof
Expanding $p(r) - p(c)$:
$$p(r) - p(c) = \frac{1}{2} (r^T Q r - c^T Q c) + b^T (r - c).$$
Using the symmetry of $Q$:
$$r^T Q r - c^T Q c = (r - c)^T Q (r + c) = 2 (r - c)^T Q m = 2 m^T Q (r - c).$$
Substituting this back:
$$p(r) - p(c) = (Q m + b)^T (r - c) = \nabla p(m) \cdot (r - c).$$
Because $p$ has degree at most two, higher derivatives vanish identically.
Now let $F(r) = 0$ with $r \in B$. Componentwise application gives:
$$-F(c) = F(r) - F(c) = J_F\left(\frac{c + r}{2}\right) (r - c).$$
Multiplying by $A$ and adding $r - c$:
$$r = c - A F(c) + (I_n - A J_F(m)) (r - c).$$
Since $B$ is convex, $m \in B$, so $J_F(m) \in [J_F(B)]$. By the inclusion property of interval arithmetic, $r \in K(c, B)$.
If $K(c, B)_k \cap B_k = \emptyset$ for some $k$, then no such root $r \in B$ can exist.

## Hypotheses / Conditions
1. Every component equation in $F$ must have total polynomial degree at most two.
2. The domain box $B$ must be convex (standard axis-aligned intervals).
3. The evaluation of $[J_F(B)]$ and $K(c, B)$ must use outward interval bounds.

## How It Applies
This theorem provides the sound contractor foundation for checking whether candidate boxes contain any MUB solutions in the 440-variable, 666-equation formulation.
- What it supports: Supports sound leaf exclusion whenever interval coordinate disjointness is achieved.
- What it does not support: Does not guarantee that contraction or separation occurs without suitable center selection and fine subdivision.
- Narrowest defensible claim: Any root of a quadratic polynomial system within a convex box belongs to its rectangular Krawczyk enclosure.
- Next test needed: Identify non-degenerate expansion centers $c$ where candidate columns of $J_F(c)$ have full rank.

## Caveats
Mechanized in Lean 4 (`RectangularQuadraticExclusion.lean`, theorems `root_in_image` and `exclusion_sound`). When evaluated at the box center $x_0 = 0$ where linear terms vanish, the Jacobian columns for candidate coordinates vanish identically, yielding zero contraction without off-center evaluation.
