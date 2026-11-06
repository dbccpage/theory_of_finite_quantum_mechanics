# [TFQ-2611] A stochastic kernel has a quantum measure-and-prepare lift

AuthorityEffect: None.

Stage: `FINITE_QM_INFORMATION`. Status: `CONDITIONAL`. DAG node: `QI-CLASSICAL-CHANNEL-LIFT`.
Parent record: `TFQ-2610`. Parent is an index link; all prerequisites below apply.

## Statement

In the admitted complex matrix model every column-stochastic kernel K has a CPTP map with Kraus operators sqrt(K(j|i)) times |j><i|, sending diagonal probabilities p to diagonal probabilities Kp.

## Prerequisites and imports

- `QI-MODEL-ADMISSION`
- Supplied: complex square roots of nonnegative entries.
- Supplied: standard basis.
- Supplied: K(j|i) nonnegative with each column summing to one.

## Argument or unresolved obligation

Summing A_ji adjoint times A_ji gives the identity by column normalization. The operator-sum formula is completely positive and its output on a diagonal state is diag(Kp). It erases off-diagonal entries. Thus it is one lift, not a unique coherence-preserving reconstruction of K.

## Evidence

[Combined source and derivation](QUANTUM_INFORMATION.md).
This proof sketch awaits independent replay or Lean formalization. No new Lean theorem or execution receipt is claimed by this paper.
