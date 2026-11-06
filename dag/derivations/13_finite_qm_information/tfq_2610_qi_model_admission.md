# [TFQ-2610] Operational quantum information model

AuthorityEffect: None.

Stage: `FINITE_QM_INFORMATION`. Status: `IMPORTED_ASSUMPTION`. DAG node: `QI-MODEL-ADMISSION`.
Parent record: `TFQ-1008`. Parent is an index link; all prerequisites below apply.

## Statement

Admit finite-dimensional complex Hilbert systems, tensor composition, positive trace-one states, effects, the Born pairing, and an available class of CPTP operations. These premises define the standard operational quantum information setting.

## Prerequisites and imports

- `FQ-POSITIVE-WEIGHTS-ADMITTED`
- `FQ-GAP-BORN-UNIQUENESS-GLEASON`
- `FQ-GAP-TENSOR-UNIQUENESS`
- `FQ-CPTP-CLASS-DEFINITION`
- Supplied: complex Hilbert systems.
- Supplied: tensor composition.
- Supplied: positive state and effect cones.
- Supplied: Born pairing.
- Supplied: CPTP operation availability.

## Argument or unresolved obligation

The earlier finite and conditional reconstruction results inform these premises but do not select all of them from <>. State exactly which operational availability assumptions a downstream theorem uses.

## Evidence

[Combined source and derivation](quantum_information.md).
No new Lean theorem or execution receipt is claimed by this paper.
