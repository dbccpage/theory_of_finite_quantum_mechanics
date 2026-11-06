# [TFQ-2607] P versus NP

AuthorityEffect: None.

Stage: `COMPUTATION`. Status: `OPEN`. DAG node: `COMP-P-VS-NP-OPEN`.
Parent record: `TFQ-2603`. Parent is an index link; all prerequisites below apply.

## Statement

Determine whether every language in NP is in P, or exhibit an NP language outside P. The existing machine construction, finite checks and exponential search enumeration do not settle either alternative.

## Prerequisites and imports

- `COMP-P-DEFINITION`
- `COMP-NP-VERIFIER-EQUIVALENCE`
- `COMP-COOK-LEVIN-IMPORT`

## Argument or unresolved obligation

A proof must quantify over uniform algorithms and unbounded input lengths. An upper bound for enumeration is not a lower bound for all algorithms. The official Clay statement lists the problem as unsolved.

## Evidence

[Combined source and derivation](../../../atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md#4-p-versus-np-encodings-and-search).
No new Lean theorem or execution receipt is claimed by this paper.
