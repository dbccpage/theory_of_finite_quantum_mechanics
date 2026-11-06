# [TFQ-2612] A common unitary cannot clone distinct nonorthogonal rays

AuthorityEffect: None.

Stage: `FINITE_QM_INFORMATION`. Status: `CONDITIONAL`. DAG node: `QI-NO-CLONING-PAIR`.
Parent record: `TFQ-2610`. Parent is an index link; all prerequisites below apply.

## Statement

In the admitted Hilbert tensor model, no single unitary with a fixed normalized blank clones two normalized vectors whose overlap has modulus strictly between zero and one.

## Prerequisites and imports

- `QI-MODEL-ADMISSION`
- Supplied: Hilbert inner product.
- Supplied: tensor product.
- Supplied: unitary map.
- Supplied: same blank.

## Argument or unresolved obligation

Inner-product preservation would give z=z squared, with z the overlap, for exact vector cloning. Allowing output phases still implies |z|=|z| squared. For 0<|z|<1 this is a contradiction. Orthogonal basis copying remains allowed.

## Evidence

[Combined source and derivation](quantum_information.md).
This proof sketch awaits independent replay or Lean formalization. No new Lean theorem or execution receipt is claimed by this paper.
