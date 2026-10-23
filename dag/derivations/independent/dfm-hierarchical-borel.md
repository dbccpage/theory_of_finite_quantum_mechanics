Status: AI-drafted, awaiting human review.

# Derivation note: DFM-HIERARCHICAL-BOREL

AuthorityEffect: None.

Outcome: Narrowed. The proved node statement is restricted to supplied rooted-tree data and the explicitly defined scalar commutative cochain operators. A bundled incidence DGA, arbitrary-graph tree construction and noncommutative matrix-valued curvature remain unpaid.

## 1. What is being extended

The diamond control factors an invertible upper-triangular matrix and dresses five fixed edges in two stages. The same algebra does not use the number of edges. This note states it for every rooted tree presented by a parent pointer and a depth, and states the incidence curvature identities for one specified pair of operators. The operators are extra data. A parent pointer does not contain a cochain.

## 2. The group

Write a matrix as [[d1, b], [0, d2]] with rational entries. It is invertible exactly when d1 and d2 are nonzero. Multiplication is

[[d1, b], [0, d2]] [[d1', b'], [0, d2']] = [[d1 d1', d1 b' + b d2'], [0, d2 d2']].

The inverse is [[d1^{-1}, -b/(d1 d2)], [0, d2^{-1}]].

Let T be the set of invertible diagonal matrices, and let N be the set of matrices [[1, x], [0, 1]]. Every invertible matrix factors as D n, where D = [[d1, 0], [0, d2]] and n = [[1, b/d1], [0, 1]]. If D' n' is another such factorization, the diagonal entries force D' = D and the off-diagonal entry forces n' = n.

For M invertible and n in N, the conjugate M n M^{-1} has both diagonal entries equal to 1, so it lies in N. The diagonal projection π(M) = D is a homomorphism. The map that replaces the bottom-right entry by 1 is not: [[2, 1], [0, 3]] squared is [[4, 5], [0, 9]], and the two ways of applying that map give bottom-row-free matrices whose off-diagonal entries are 5 and 3.

The factorization identity itself fails for [[0, 1], [0, 1]]. Its diagonal projection times the unit matrix is [[0, 0], [0, 1]].

## 3. Rooted transport

Let V be any vertex type, r a root, and parent a function with parent(r) = r. Let depth take nonnegative integer values, with depth(r) = 0, and depth(parent(v)) < depth(v) whenever v is not r. This is a rooted tree: following parent reaches r, and there are no cycles.

Assign to each non-root vertex v an invertible label U(v). Define the transport by T(r) = I and

T(v) = U(v) T(parent(v)).

Invertibility of the labels implies invertibility of every T(v), by induction on depth. Write T(v) = D(v) n(v) for the unique factorization of section 2, and set

u_N(v) = [[1, -b(v)/d2(v)], [0, 1]],

where b(v) and d2(v) are the off-diagonal and bottom-right entries of T(v). This matrix lies in N. When T(v) is invertible it equals the conjugate D(v) n(v)^{-1} D(v)^{-1}, so the same membership is the normality statement of section 2 applied to n(v)^{-1}. A direct multiplication gives u_N(v) T(v) = D(v).

On the tree edge from parent(v) to v,

u_N(v) U(v) u_N(parent(v))^{-1} = D(v) D(parent(v))^{-1}.

The right-hand side is diagonal. The same identity is the reason a further diagonal vertex field keeps those edges diagonal: a product of diagonal matrices is diagonal.

For an arbitrary label g between any two vertices s and t, not necessarily a tree edge,

π(u_N(t) g u_N(s)^{-1}) = π(g),

because both dressing factors lie in N and π kills N.

Set u_T(v) = D(v)^{-1}. Then u_T(v) u_N(v) = T(v)^{-1}. For every label g from s to t,

u_T(t) (u_N(t) g u_N(s)^{-1}) u_T(s)^{-1} = T(t)^{-1} g T(s).

In particular, each tree label satisfies U(v) = T(v) T(parent(v))^{-1}, so the right-hand side on that edge is I.

A supplied label g from s to t dresses to I if and only if g = T(t) T(s)^{-1}. One direction substitutes the coboundary. The other multiplies the dressed equation on the left by T(t) and on the right by T(s)^{-1}.

If a vertex field g has g(r) = I, takes invertible values, and satisfies U(v) = g(v) g(parent(v))^{-1} at every non-root vertex, then g = T. The proof is induction on depth, using the transport recurrence.

## 4. A path that is not the diamond

Take vertices 0, 1, 2, root 0, parent(1) = 0, parent(2) = 1, and labels

U(1) = [[2, 6], [0, 3]], U(2) = [[4, 1], [0, 5]].

The transport is T(0) = I, T(1) = U(1), and T(2) = [[8, 27], [0, 15]]. The stage-one fields are u_N(1) = [[1, -2], [0, 1]] and u_N(2) = [[1, -9/5], [0, 1]]. The chord label [[1, 7], [0, 1]] from 0 to 2 dresses to [[1/8, 13/20], [0, 1/15]], which is not I. The coboundary T(2) T(0)^{-1} dresses to I. The same checks hold for the four-vertex parent function with parents (0, 0, 0, 2) and the three rational labels used by the independent script. That parent function is the diamond tree: the transport at vertex 3 is the product of the labels at 3 and at 2.

## 5. Incidence curvature, as extra data

On a commutative ring, for a function A of two arguments, set

(bA)(u, v, w) = -A(u, w), (A ⌣ A)(u, v, w) = A(u, v) A(v, w),

and K(A) = bA + A ⌣ A. Then K(A)(u, v, w) = A(u, v) A(v, w) - A(u, w). Extending b to functions of three arguments by (bK)(u, v, w, z) = -K(u, w, z) + K(u, v, z), the composite b(bA) is 0. The covariant combination

bK + A ⌣ K - K ⌣ A

is 0 when K = K(A). If a vertex function g has a pointwise inverse g_inv and A^g(x, y) = g(x) A(x, y) g_inv(y), then

K(A^g)(u, v, w) = g(u) K(A)(u, v, w) g_inv(w).

Source-only multiplication is a different rule. For A(0,1) = 1, A(1,2) = 1, A(0,2) = 0 and multipliers g(0) = 1, g(1) = 2, the source-only expression (g0 A01)(g1 A12) - g0 A02 equals 2, while g0 (A01 A12 - A02) equals 1. Their difference is 1, so the two expressions are not equal. The endpoint rule with g(2) = 1 and g(1)^{-1} = 1/2 returns equal values on this same tuple.

The comparison 2 ≠ 3 is the size of these matrices against the integer 3. No declaration in the Lean module names a color group.

## What is proved

Unique factorization, normality, the diagonal projection homomorphism, the rooted transport recurrence, stage-one membership in N by the conjugate formula, diagonal stage-one tree edges, invariance of the diagonal projection, equality of the two-stage field with the inverse transport, reproduction of T(t)^{-1} g T(s), the coboundary criterion, uniqueness of the anchored vertex field, refusal of the singular matrix [[0, 1], [0, 1]], refusal of the bottom-right replacement map, b² = 0, the Bianchi identity for these operators, endpoint covariance, the source-only numerical split 2 against 1, the comparison 2 ≠ 3, and the diamond transport identity T(3) = U(3) U(2).

## What is assumed

The rooted tree is supplied as a parent function and a depth function. Each non-root tree label is assumed invertible. Comparing a vertex with the root uses classical excluded middle. The curvature statements assume a commutative ring and the two operators written above. No continuum field, no smooth patching, and no color representation is assumed.

## What is open

The argument does not build a spanning tree out of an arbitrary graph, does not name the coboundary criterion as a computed cohomology group, and does not construct a 2-plaquette prism. Continuum gauge theory remains a separate obligation.
