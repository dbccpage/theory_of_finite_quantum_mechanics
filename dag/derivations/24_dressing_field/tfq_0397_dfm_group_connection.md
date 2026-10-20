# [TFQ-0397] Group-valued connections on a finite multigraph

**Stage:** `DRESSING_FIELD` | **Status:** `DEFINITION` | **AuthorityEffect:** None.

**Parent:** [TFQ-0009](../14_finite_gauge/tfq_0009_finite_gauge_cochain.md)
**DAG node:** `DFM-GROUP-CONNECTION`
**Required DAG inputs:** `FQ-CARRIER-CONTRACT-V2`

## Statement and derivation

Let V and E be finite sets, with source and target maps s,t:E→V. Loops and
parallel edges are allowed. The underlying graph is undirected: every representative
edge e may also be traversed backwards. A supplied group G labels e by U_e; reverse
traversal has label U_e^{-1}. No commutativity, matrix representation or topology is assumed.

For a walk traversed e_1,...,e_k, transport acts on the left and is
H(p)=U_{e_k}...U_{e_1}, using inverses for backward steps. Thus
H(p followed by q)=H(q)H(p). A vertex dressing u:V→G gives

    U^u_e = u(t(e)) U_e u(s(e))^{-1}.

Choose a rooted spanning forest of the underlying multigraph. Write r(v) for the
component root, P_v for its tree path to v, and T_v=H(P_v), with T_r=1. This is
finite graph data, not a locality theorem for a physical field. For an empty graph
all edge conditions are vacuous; an isolated vertex has its own root.

The group is an additional premise. The incoming carrier-contract route records
that admission, not a derivation of G from the existing finite quantum interface.

## Evidence and next obligation

- [dag/research/hierarchical_nonabelian_dfm_finite_map.md](../../../dag/research/hierarchical_nonabelian_dfm_finite_map.md)
- [dag/research/finite_graph_dressing.py](../../../dag/research/finite_graph_dressing.py)
- [dag/research/finite_graph_dressing.rs](../../../dag/research/finite_graph_dressing.rs)
- [lean4/FiniteGraphDressing.lean](../../../lean4/FiniteGraphDressing.lean)
- [dag/research/test_finite_graph_dressing.py](../../../dag/research/test_finite_graph_dressing.py)

Keep the graph, group axioms, inverse-edge convention and multiplication order explicit.
