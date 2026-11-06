# [TFQ-2614] Uniform quantum circuits and BQP

AuthorityEffect: None.

Stage: `COMPUTATION`. Status: `DEFINITION`. DAG node: `QC-UNIFORM-CIRCUITS-BQP`.
Parent record: `TFQ-2610`. Parent is an index link; all prerequisites below apply.

## Statement

With the admitted quantum model and an efficiently specified finite gate set, BQP consists of languages decided by polynomial-time uniform polynomial-size circuit families with acceptance at least 2/3 for yes instances and at most 1/3 for no instances.

## Prerequisites and imports

- `QI-MODEL-ADMISSION`
- `COMP-COST-MODEL-IMPORT`
- `COMP-REVERSIBLE-BOOLEAN-EMBEDDING`
- Supplied: uniform classical circuit generator.
- Supplied: polynomial gate count.
- Supplied: ancilla preparation.
- Supplied: finite gate specification.
- Supplied: Born measurement.

## Argument or unresolved obligation

Uniformity, input encoding, gate resources and bounded error are part of the definition. Classical control and quantum model admission are both prerequisites; the P versus NP open node is not a prerequisite.

## Evidence

[Combined source and derivation](../../../atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md#6-quantum-circuits-and-bqp).
No new Lean theorem or execution receipt is claimed by this paper.
