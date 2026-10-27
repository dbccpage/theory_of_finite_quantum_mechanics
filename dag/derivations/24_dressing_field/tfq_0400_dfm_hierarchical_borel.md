# [TFQ-0400] Hierarchical Borel dressing beyond the diamond control

**Stage:** `DRESSING_FIELD` | **Status:** `PROVED_LEAN` | **AuthorityEffect:** None.

**Parent:** [TFQ-0399](../24_dressing_field/tfq_0399_dfm_tree_change.md)
**DAG node:** `DFM-HIERARCHICAL-BOREL`
**Required DAG inputs:** `DFM-TREE-CHANGE`

## Statement and derivation

Let B_2(Q) be the invertible upper-triangular 2x2 matrices over Q, T the diagonal matrices and N the unit upper-triangular matrices. Every invertible element factors uniquely as D * n with D in T and n in N, and conjugation of an element of N by an invertible element stays in N. torusProj preserves multiplication. On any vertex type with a root, a parent function and a depth function that strictly decreases along parents, and for invertible labels off the root, root-to-vertex transport multiplies labels on the left: T(root) = I and T(v) = U(v) * T(parent(v)). The stage-one field u_N(v) equals D(v) * n(v)^{-1} * D(v)^{-1}, lies in N, and equals [[1, -b(v)/d2(v)], [0, 1]]. Dressing a tree edge by u_N yields D(child) * D(parent)^{-1}. For every label g and every pair of vertices, torusProj(u_N(target) * g * u_N(source)^{-1}) equals torusProj(g). A further diagonal vertex field, multiplied on the left at the child and on the right by its inverse at the parent, leaves that dressed tree edge diagonal. The stage-two field u_T(v) = D(v)^{-1} satisfies u_T(v) * u_N(v) = T(v)^{-1}, and u_T(target) * (u_N(target) * g * u_N(source)^{-1}) * u_T(source)^{-1} equals T(target)^{-1} * g * T(source). That dressed label equals I if and only if g = T(target) * T(source)^{-1}. A vertex field that is invertible at every vertex, equals I at the root, and satisfies U(v) = g(v) * g(parent(v))^{-1} off the root, equals the rooted transport. The factorization identity fails on [[0, 1], [0, 1]]. Replacing the (2, 2) entry by 1 does not preserve the product of [[2, 1], [0, 3]] with itself. On any commutative ring, the operators (bA)(u, v, w) = -A(u, w) and (A smile A)(u, v, w) = A(u, v) * A(v, w) satisfy b composed with b equal to 0, the Bianchi identity for K = bA + A smile A, and endpoint gauge covariance K(A^g) = g(u) * K(A) * g(w)^{-1} when A^g(x, y) = g(x) * A(x, y) * g(y)^{-1}. For A(0,1)=1, A(1,2)=1, A(0,2)=0, g(0)=1 and g(1)=2, the source-only expression (g(0)*A(0,1))*(g(1)*A(1,2)) - (g(0)*A(0,2)) is not equal to g(0)*(A(0,1)*A(1,2) - A(0,2)). The same values with g(2)=1 and g(1)^{-1}=1/2 satisfy the endpoint identity. The arithmetic comparison of 2 with 3 records that these integers differ. On the four-vertex tree with parents 0, 0, 0, 2, transport at vertex 3 equals U(3) * U(2).

The Lean module is `lean4/DressingFieldHierarchicalBorel.lean`. The independent check is `checks/independent/dfm-hierarchical-borel.py`. The step-by-step note is `dag/derivations/independent/dfm-hierarchical-borel.md`.

## What stays outside

The rooted tree, given by a parent function and a strictly decreasing depth, and the incidence cochain are supplied data. This record does not construct a spanning tree from an arbitrary graph, does not identify an obstruction with a computed cohomology group, and does not build a 2-plaquette prism. Continuum gauge theory, color transport and smooth patching stay outside this statement. Dossier Theorem 3.2 is wider than this record.

## Evidence

- [dag/derivations/independent/dfm-hierarchical-borel.md](../independent/dfm-hierarchical-borel.md)
- [dag/research/campaign_dfm-hierarchical-borel_lean_replay.json](../../research/campaign_dfm-hierarchical-borel_lean_replay.json)
- [checks/independent/dfm-hierarchical-borel.py](../../../checks/independent/dfm-hierarchical-borel.py)
- [dag/research/hierarchical_nonabelian_dfm_finite_map.md](../../research/hierarchical_nonabelian_dfm_finite_map.md)
