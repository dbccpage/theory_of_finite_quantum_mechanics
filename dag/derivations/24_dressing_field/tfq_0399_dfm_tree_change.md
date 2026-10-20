# [TFQ-0399] Tree-change covariance of the residual connection

**Stage:** `DRESSING_FIELD` | **Status:** `PROVED_LEAN` | **AuthorityEffect:** None.

**Parent:** [TFQ-0398](../24_dressing_field/tfq_0398_dfm_general_graph_dressing.md)
**DAG node:** `DFM-TREE-CHANGE`
**Required DAG inputs:** `DFM-GENERAL-GRAPH-DRESSING`

## Statement and derivation

Let u=T^{-1} and u'=T'^{-1} be dressings from two rooted spanning forests.
Set C(v)=u'(v)u(v)^{-1}=T'_v^{-1}T_v. Direct cancellation gives

    R'_e = C(t) R_e C(s)^{-1}.

Indeed the right side is
u'_t u_t^{-1} (u_t U_e u_s^{-1}) (u'_s u_s^{-1})^{-1}
=u'_t U_e (u'_s)^{-1}. Associativity and adjacent inverse cancellation are the
only group laws used. Lean `change_dressing` establishes the identity for arbitrary
u,u', so tree change is a specialization.

For a closed walk based at v the factors telescope to
H_{R'}(p)=C(v)H_R(p)C(v)^{-1}. Thus conjugacy classes, and trace when a matrix
representation supplies one, are unchanged. Individual edge residuals need not
be equal or individually conjugate. With the same normalized root, based-loop
transport at that root is equal. If the original connection is changed by a gauge
g, then T^g_v=g(v)T_v g(r)^{-1}; its residual is g(r)R_e g(r)^{-1}. Root-fixing
gauges therefore leave each residual unchanged.

Python and Rust test these formulas over a noncommutative S3 carrier and different
forests. Those tests check finite instances; the algebraic identity is general.

## Evidence and next obligation

- [dag/research/finite_graph_dressing.py](../../../dag/research/finite_graph_dressing.py)
- [dag/research/finite_graph_dressing.rs](../../../dag/research/finite_graph_dressing.rs)
- [lean4/FiniteGraphDressing.lean::change_dressing](../../../lean4/FiniteGraphDressing.lean)
- [dag/research/finite_graph_dressing.rs::forest_dressing](../../../dag/research/finite_graph_dressing.rs)
- [lean4/FiniteGraphDressing.lean](../../../lean4/FiniteGraphDressing.lean)
- [dag/research/test_finite_graph_dressing.py](../../../dag/research/test_finite_graph_dressing.py)

Use the same multiplication convention in all three languages; distinguish edge residuals from conjugacy-invariant closed-loop observables.
