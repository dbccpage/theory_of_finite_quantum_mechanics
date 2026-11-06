# [TFQ-2619] An adjoint-preserving matrix derivation is Hamiltonian

AuthorityEffect: None.

Stage: `FINITE_QM_DYNAMICS`. Status: `CONDITIONAL`. DAG node: `DYN-ALGEBRAIC-HAMILTON`.
Parent record: `TFQ-1002`. Parent is an index link; all prerequisites below apply.

## Statement

Every Q(i)-linear adjoint-preserving derivation of the full algebra M_d(Q(i)), for positive d, has the form delta(A)=-i[H,A] for a Hermitian H, unique modulo a rational scalar identity.

## Prerequisites and imports

- `L1-WDP-REALIFICATION-J`
- Supplied: full matrix algebra over Q(i).
- Supplied: positive dimension.
- Supplied: Leibniz derivation.
- Supplied: adjoint preservation.

## Argument or unresolved obligation

Set S=sum_j delta(E_j1)E_1j. Leibniz on E_ab E_j1 shows [S,E_ab]=delta(E_ab). Adjoint preservation makes S+S adjoint central, so replace S by its anti-Hermitian part. H=iS works. The commutant of the full matrix algebra is scalar, and Hermitian scalars in Q(i) are rational. This gives no time parameter or flow.

## Evidence

[Combined source and derivation](dynamics_hamilton_noether.md#algebraic-hamiltonian).
This proof sketch awaits independent replay or Lean formalization. No new Lean theorem or execution receipt is claimed by this paper.
