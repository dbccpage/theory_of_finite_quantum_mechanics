# [TFQ-2616] Scalable physical quantum computation

AuthorityEffect: None.

Stage: `COMPUTATION`. Status: `OPEN`. DAG node: `QC-FAULT-TOLERANCE-OPEN`.
Parent record: `TFQ-2614`. Parent is an index link; all prerequisites below apply.

## Statement

Connect the circuit family to available gates, preparation, measurement, recovery and a specified noise model with error and resource bounds uniform in computation size.

## Prerequisites and imports

- `QC-UNIFORM-CIRCUITS-BQP`
- `QC-GATE-ERROR-BUDGET`
- `QI-ENTROPY-CODING-OBLIGATIONS`
- Supplied: noise model.
- Supplied: fault-tolerant gadgets.
- Supplied: uniform decoding and scheduling.

## Argument or unresolved obligation

Finite code-distance, queue and recurrence witnesses retain their stated scope. They do not establish a physical threshold without gadget and noise assumptions and a scaling theorem.

## Evidence

[Combined source and derivation](../13_finite_qm_information/quantum_information.md).
No new Lean theorem or execution receipt is claimed by this paper.
