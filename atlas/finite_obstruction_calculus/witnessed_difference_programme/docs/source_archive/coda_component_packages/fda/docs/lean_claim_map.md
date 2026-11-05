# Proof-Assistant Claim Map (Lean 4)

**Toolchain:** `leanprover/lean4:v4.34.0-rc1` via Lake (`package «coda_fda»`).
Reconstruction algebra is vendored locally (`Foundations.lean` and `FDA.lean`). The package is completely self-contained with zero external dependencies.

Source of truth for FDA-T5 through FDA-T8 is `FDA.lean`, re-exported by `Algebra.lean`. The core module `GtfdaAuthorityCore.lean` formalizes definitional firewalls: no packet (FDA-T2), no terminalizer path (FDA-T3), a refusal branch (FDA-C1), a generated candidate without path (FDA-T4), or a failed guard (FDA-T1) cannot inhabit `Authority`.

| Paper Claim | Type | Module | Formal Symbol | Kernel Axioms |
|---|---|---|---|---|
| **FDA-D1** | Definition | `GtfdaAuthorityCore.lean` | `GTFDA.DescentPacket` | (definition) |
| **FDA-D2** | Definition | `GtfdaAuthorityCore.lean` | `GTFDA.Authority` | (definition) |
| **FDA-D3** | Definition | `GtfdaAuthorityCore.lean` | `GTFDA.HaltGuards`, `GTFDA.IsAuth` | (definition) |
| **FDA-T1** | Theorem | `GtfdaAuthorityCore.lean` | `GTFDA.failed_guard_non_creation` | none (0 axioms) |
| **FDA-T2** | Theorem | `GtfdaAuthorityCore.lean` | `GTFDA.missing_supplied_packet_non_creation` | none (0 axioms) |
| **FDA-T3** | Theorem | `GtfdaAuthorityCore.lean` | `GTFDA.authority_non_construction` | none (0 axioms) |
| **FDA-C1** | Corollary | `GtfdaAuthorityCore.lean` | `GTFDA.refusal_non_creation` | none (0 axioms) |
| **FDA-T4** | Theorem | `GtfdaAuthorityCore.lean` | `GTFDA.authority_non_generation` | none (0 axioms) |
| **FDA-T5** | Theorem | `FDA.lean` | `Coda.FDA.terminal_has_history` | `{propext}` |
| **FDA-T6** | Theorem | `FDA.lean` | `Coda.FDA.routing_refusal_persists` | `{propext}` |
| **FDA-T7** | Theorem | `FDA.lean` | `Coda.FDA.standing_sound` | none (0 axioms) |
| **FDA-T8** | Theorem | `FDA.lean` | `Coda.FDA.untrusted_verifier_countermodel` | none (0 axioms) |
| (firewall) | Theorem | `FDA.lean` | `Coda.FDA.authority_not_observation` | none (0 axioms) |
| (replay) | Theorem | `FDA.lean` | `Coda.FDA.replay_standing` | none (0 axioms) |
| (binding) | Module | `Core.lean` | Imports all core and reconstruction modules | within `{propext}` |

**FDA-T9 to FDA-T12 have no Lean declarations (2026-09-23).** The ledger formerly cited `GTFDA.coproduct_separation`, `GTFDA.role_non_impersonation`, `GTFDA.authority_gap_fence` and `GTFDA.authority_typing_boundary`. None of them exists in `GtfdaAuthorityCore.lean`; those pointers are withdrawn. FDA-T9 is backed in part by FDA-C1 (`GTFDA.refusal_non_creation`, the refusal summand). FDA-T10 is a policy, and FDA-T11 and FDA-T12 are scope fences.

All proofs elaborate under `lake build` with zero `sorry` stubs. No non-kernel axioms are used. Axiom dependencies are verified by `#print axioms` in `GtfdaAuthorityCoreAudit.lean` and `Algebra.lean`.

FDA-T2 is an `Option` input theorem through `SuppliedAuthority`; it does not encode nonempty Lean carriers. The retained `uniform_non_creation` has an unsatisfiable packet-type-emptiness premise. FDA-T9 is now policy; its categorical no-map clause is withdrawn as false (constant singleton functors counterexample).
