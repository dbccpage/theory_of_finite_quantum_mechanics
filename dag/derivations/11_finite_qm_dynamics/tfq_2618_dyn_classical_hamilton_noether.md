# [TFQ-2618] Area-preserving plane flow and a Hamiltonian charge

AuthorityEffect: None.

Stage: `FINITE_QM_DYNAMICS`. Status: `CONDITIONAL`. DAG node: `DYN-CLASSICAL-HAMILTON-NOETHER`.
Parent record: `TFQ-0001`. Parent is an index link; all prerequisites below apply.

## Statement

On a simply connected plane domain with omega=dq wedge dp, a C1 area-preserving vector field has a Hamiltonian H with qdot=H_p and pdot=-H_q. For H=p squared/2 the q-translation charge p is conserved.

## Prerequisites and imports

- `PG-ROOT-DIFF-STRUCTURE`
- Supplied: oriented state plane.
- Supplied: C1 vector field and local flow.
- Supplied: area preservation.
- Supplied: simply connected domain.

## Argument or unresolved obligation

Area preservation gives u_q+v_p=0, hence alpha=u dp-v dq is closed. Exactness on the simply connected domain supplies H. For the specified H, pdot=-H_q=0. Coordinates, regularity, topology and flow are supplied, not derived from the primitive.

## Evidence

[Combined source and derivation](dynamics_hamilton_noether.md#classical-hamilton-and-noether).
This proof sketch awaits independent replay or Lean formalization. No new Lean theorem or execution receipt is claimed by this paper.
