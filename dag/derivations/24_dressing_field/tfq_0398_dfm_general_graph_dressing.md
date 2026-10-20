# [TFQ-0398] General finite-graph dressing and closed-walk holonomy

**Stage:** `DRESSING_FIELD` | **Status:** `PROVED_LEAN` | **AuthorityEffect:** None.

**Parent:** [TFQ-0397](../24_dressing_field/tfq_0397_dfm_group_connection.md)
**DAG node:** `DFM-GENERAL-GRAPH-DRESSING`
**Required DAG inputs:** `DFM-GROUP-CONNECTION`

## Statement and derivation

## Theorem

For the connection and conventions of TFQ-0397, the following are equivalent:

1. There exists u:V→G with U^u_e=1 for every edge.
2. Every closed walk has identity transport.
3. Every non-forest edge has residual R_e=T_t^{-1} U_e T_s=1.

When they hold, the rooted dressing u_T(v)=T_v^{-1} neutralizes every edge.

## Proof

For a forward or backward step, dressing changes transport from a to b to
u(b)H(p)u(a)^{-1}. The intermediate factors telescope under concatenation,
without commuting any factors. A closed walk at v therefore transforms by
conjugation with u(v). If all dressed edges are identity, its original transport
must also be identity. This establishes 1⇒2.

For any edge e:s→t, follow P_s, traverse e, then follow P_t backwards. This is a
closed walk at the component root, with transport T_t^{-1}U_e T_s=R_e. Under 2,
R_e=1, and dressing by T^{-1} makes the edge identity. This establishes 2⇒1
and 2⇒3. Tree edges already have U_e T_s=T_t, in either traversal orientation.
Consequently 3 makes every residual identity, establishing 3⇒1. Self-loops are
chords and are tested; parallel edges produce distinct chord conditions. Apply
the construction to each component. No relation is required between component roots.

The connected Lean theorem is `neutralizable_iff_closed_walks`; the disconnected
theorem is `neutralizable_iff_closed_walks_forest`. The latter explicitly takes
root paths and equality of the endpoint roots on every edge. `tree_dressing_iff`
checks all edge equations, while the forest construction establishes the tree
ones automatically, leaving the finite chord test.

## Uniqueness and limits

If u and u' both neutralize all edges, the pure-gauge equations give
u'(t)u(t)^{-1}=u'(s)u(s)^{-1}. It is a left constant on each component. Thus a
root normalization selects one neutralizer. This is `neutralizers_constant`.

The theorem concerns vertex gauges on a supplied graph. Trivial holonomy on only
the declared faces does not suffice on a graph with additional cycles. It does
not classify the physical locality of a dressing, construct a smooth bundle, or
derive a quantum gauge group.

## Evidence and next obligation

- [dag/research/finite_graph_dressing.py](../../../dag/research/finite_graph_dressing.py)
- [dag/research/finite_graph_dressing.rs](../../../dag/research/finite_graph_dressing.rs)
- [lean4/FiniteGraphDressing.lean::neutralizable_iff_closed_walks_forest](../../../lean4/FiniteGraphDressing.lean)
- [lean4/FiniteGraphDressing.lean::tree_dressing_iff](../../../lean4/FiniteGraphDressing.lean)
- [lean4/FiniteGraphDressing.lean::neutralizers_constant](../../../lean4/FiniteGraphDressing.lean)
- [dag/research/finite_graph_dressing.rs::forest_dressing](../../../dag/research/finite_graph_dressing.rs)
- [lean4/FiniteGraphDressing.lean](../../../lean4/FiniteGraphDressing.lean)
- [dag/research/test_finite_graph_dressing.py](../../../dag/research/test_finite_graph_dressing.py)

Preserve the supplied-group and supplied-forest hypotheses; the Python and Rust enumerations are bounded witnesses for the general Lean theorem.
