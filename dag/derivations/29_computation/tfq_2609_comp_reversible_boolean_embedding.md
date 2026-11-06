# [TFQ-2609] A reversible Boolean permutation embeds as a unitary

AuthorityEffect: None.

Stage: `COMPUTATION`. Status: `CONDITIONAL`. DAG node: `COMP-REVERSIBLE-BOOLEAN-EMBEDDING`.
Parent record: `TFQ-1284`. Parent is an index link; all prerequisites below apply.

## Statement

For any Boolean function f on a fixed finite input domain, (x,y) maps to (x,y XOR f(x)) by an involutive permutation. Its permutation matrix is unitary in the admitted standard complex inner product.

## Prerequisites and imports

- `COMP-C1-CANONICAL-SEPARATED-ALPHABET`
- Supplied: finite Boolean domain.
- Supplied: standard complex basis and inner product.

## Argument or unresolved obligation

Applying the map twice cancels the two XOR copies of f(x). A permutation matrix has orthonormal columns. This is a representation theorem; efficient implementation additionally requires a circuit and resource bound for f, and no physical quantum structure is selected.

## Evidence

[Combined source and derivation](../../../atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md#5-reversible-classical-gates-meet-an-admitted-quantum-model).
This proof sketch awaits independent replay or Lean formalization. No new Lean theorem or execution receipt is claimed by this paper.
