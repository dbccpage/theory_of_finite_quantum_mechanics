# Lean evidence for PO-023

Toolchain: `leanprover/lean4:v4.35.0`. AuthorityEffect: None.

Run `lake build` here. The roots are listed in `lakefile.lean`. Building the roots is distinct from auditing physical interpretations.

- `MeronCharacter.lean`: general finite Boolean character-sum compression, zero-meron sum, and counterexamples to overbroad cancellation claims.
- `NormalFormLaws.lean`: soundness, idempotence and completeness for an integral quotient and a binary triangle, plus cycle invariance and obstruction.

The new files print their theorem axiom dependencies. Their compiled statements use at most `{propext, Quot.sound}`. The general RREF and graph algorithms have written proofs and finite tests; these Lean examples do not verify the whole Python implementation. The Hubbard transfer and determinant proofs are not mechanized here.

**Withdrawal in place.** Earlier descriptions of `GenesisFspBridge` as a deductive ladder from the sealed inscription to Troyer–Wiese hardness are withdrawn. Its structures are independently admitted fixtures. `BqnfSignPacket` supplies scalar/Boolean routing abstractions and does not verify the validated Python witness router. Advanced physics-labelled modules establish only their actual conditional algebraic statements. A reflexive theorem about a status string is not evidence of physical or implementation correctness.

See [provenance.md](provenance.md) and the package [verification receipt](../verification.md).
