> **Recovered file.** Source: `C:\.ana\coda_university\coda_research\authorization_an_incompleteness_theory\README.md` (external, read-only).
> Recovery date: 2026-10-21. Recovered verbatim; statuses below are the source's, not audited.
> Audit and comparison with this repository: [RECOVERY_NOTES.md](RECOVERY_NOTES.md).

---

# Authorization as an Incompleteness Theory

**Status:** research prospectus, proof program, rooted finite Lean
results, bounded replay packet, and finite token-code syntax lift, v0.9

**AuthorityEffect:** None.

This directory develops a theorem program about the boundary between a
proposal source, an evaluator, a replay checker, and a final authorizer.
It starts at the Primitive Difference interface and builds toward a
future impossibility theorem through a series of separately sealed,
replayable derivations. It is not yet that final paper.

## Central result

The program targets the following two-layer result.

1. A report-only authorizer cannot be both sound and complete for a
   validity predicate that distinguishes two proposals with the same
   report. PO-000 is the fixed formal anchor; this directory carries a
   corroborating self-contained finite seed that replayed on 2026-08-20.
2. For arbitrary programs in a Turing-complete proposal language, no
   total computable authorizer can be both sound and complete for a
   nontrivial semantic property. This is the Rice-theorem lift and is
   an explicit next proof obligation, not yet a local Lean theorem.

The practical conclusion is deliberately precise: an LLM can propose,
can run bounded checks, and can participate in a replay. The target
theorem says that it cannot, by source-controlled output alone, provide
total semantic authorization of arbitrary proposals. A bounded
authorization may be real, but it is conditional on an independently
fixed contract, checker, and trust boundary.

## Contents

| File | Role |
| --- | --- |
| [authorization_incompleteness_theory.md](authorization_incompleteness_theory.md) | Research-paper draft and direct answer to the externality question |
| [authorization_incompleteness_theory_claim_ledger.md](authorization_incompleteness_theory_claim_ledger.md) | Claim status, evidence, and nonclaims |
| [authorization_incompleteness_theory_change_log.md](authorization_incompleteness_theory_change_log.md) | Version history and current formal-scope changes |
| [formal_binding_manifest.md](formal_binding_manifest.md) | Producer-side source/hash/declaration binding for finite Lean claims |
| [proof_program.md](proof_program.md) | Strictly ordered proof goals and closure criteria |
| [goals.yaml](goals.yaml) | Machine-readable dependency graph for the proof program |
| [computability_lift_admission.md](computability_lift_admission.md) | Gate that freezes a real program carrier before any Rice-style lift |
| [computability_carrier_candidates.json](computability_carrier_candidates.json) | Candidate inventory whose test forbids premature admission |
| [seal_derivation_series.md](seal_derivation_series.md) | Proposed Primitive Difference to authorization series |
| [controlled_turing_derivation_series.md](controlled_turing_derivation_series.md) | Tape/read/move/halt control experiments and their proof ceilings |
| [evidence/source_map.md](evidence/source_map.md) | What existing CODA and sealed-tag material supports, and what it does not |
| [formal/authorization_incompleteness_core.lean](formal/authorization_incompleteness_core.lean) | Small, axiom-free finite information core |
| [formal/direct_turing_machine_models.lean](formal/direct_turing_machine_models.lean) | Direct finite-rule syntax and fuel-bounded execution seed; not a universal machine |
| [formal/direct_turing_machine_token_code_models.lean](formal/direct_turing_machine_token_code_models.lean) | Finite token-code grammar and parser round trip for the DTM0 rule-list carrier; not bytes or an input encoding |
| [formal/global_computability_lift_models.lean](formal/global_computability_lift_models.lean) | Axiom-free class-relative transport from source undecidability to authorization impossibility |
| [formal/logical_externality_models.lean](formal/logical_externality_models.lean) | Finite model showing physical separation is neither necessary nor sufficient for a bounded authorization |
| [formal/primitive_difference_authorization_models.lean](formal/primitive_difference_authorization_models.lean) | Finite same-primitive / different-policy countermodel |
| [formal/primitive_difference_p0_bridge.lean](formal/primitive_difference_p0_bridge.lean) | J011 Primitive Difference quotient specialized to the P0 factorization boundary |
| [formal/replay_packet_binding_models.lean](formal/replay_packet_binding_models.lean) | Finite structural trust-root, receipt-binding, replay, and terminal-policy model; not cryptographic or custodial security |
| [formal/tape_control_authorization_models.lean](formal/tape_control_authorization_models.lean) | Finite read-control, halt-control, semantic-adapter, and content-contract countermodel |
| [formal/tape_transition_invariant_models.lean](formal/tape_transition_invariant_models.lean) | Finite transition table with one proved supplied-contract invariant, one named countertrace, and a control-report P0 boundary |
| [formal/terminal_authorization_boundary_models.lean](formal/terminal_authorization_boundary_models.lean) | Conditional no-decider terminalization consequence, fenced by a finite closed Boolean terminalizer |
| [formal/README.md](formal/README.md) | Lean replay command and evidence boundary |
| [code/replay_packet/README.md](code/replay_packet/README.md) | Bounded SHA-256 replay packet, evaluator, tamper corpus, and trust boundary |
| [code/tests/test_computability_carrier_candidates.ps1](code/tests/test_computability_carrier_candidates.ps1) | Validates candidate ceilings and rejects premature admission mutations |

## Projection Obstruction anchor

PO-000 is the constraint every later authorization lift must meet. For
each proposed map out of an underlying carrier `X` through a report
`p : X -> M`, ask whether it is constant on the fibers of `p`.

- A report-level evaluation must descend through `p`.
- A report-level authorization must descend through `p`.
- If either splits a fiber, it must retain the underlying distinction,
  refine the report, consume a separately declared input, or return
  `open`.

The new program does not push proposal, evaluation, or authorization
through the boundary by naming it so. It treats descent as a proof
obligation at every lift.

The global route has a separate carrier-admission gate. A finite tape
experiment can expose a missing distinction or prove a finite invariant,
but it cannot turn itself into an arbitrary-program theorem. The named
language, evaluator, semantic property, reduction, and replay boundary
must be frozen before the Rice lift begins.

The direct route now has a finite token grammar for its rule-list machine:
one halt-state token and complete five-token rule frames round trip through
the declared parser, while empty, truncated, invalid-symbol, and
invalid-movement code is rejected. It still has no source-byte format,
input/configuration encoding, parser-to-execution agreement, universality,
or reduction.

## Fast replay

From the repository root:

```powershell
Set-Location lean4\genx
lake build AuthorizationIncompletenessTheory
```

The named target built successfully on 2026-08-21 (40 jobs, including
the current J011 candidate quotient import closure). The three standalone
seed modules plus the logical-externality model and generic reduction
transport, structural replay-packet theorems, and finite transition-model
theorems print no axioms. The J011 quotient bridge's negative theorems
depend on `propext` and `Quot.sound`, exactly as the underlying quotient
equivalence does; its positive quotient-lift theorem prints no axioms.
The direct finite-rule Turing-style seed prints `propext` for its generic
halt equivalences and closed stuck/fuel fixtures, and no axioms for its
closed blank/write/reaches-halt fixtures; it is not a byte encoding,
universal-machine, or Rice-theorem result.
The DTM1 token-code tags round trip with no axiom dependencies; its
rule-list and machine parser round trips plus malformed-code fixtures print
`propext`. They are a finite `List Nat` grammar, not a byte parser, input
encoding, trace-agreement theorem, or universality result.
The conditional terminalization bridge prints `propext` for its
acceptance-bit/no-decider consequences and finite Boolean fixture, while
its closed-two-sided-to-acceptance-complete bridge has no axioms. It
requires a supplied no-decider premise and allowed-class membership; the
Boolean fixture confirms that a closed local terminalizer remains
possible for a decidable contract.
PO-000 remains the established formal anchor for the research program:
the bridge is a statement-level specialization, not a replacement or
amendment. No green build establishes the later Rice or Goedel lifts.

The bounded packet can be replayed from the repository root with
`code/replay_packet/verify_transition_packet.ps1`. It binds a
finite proposal, contract, policy, evaluator, entrypoint, and a Lean
model/direct-dependency closure with its exact Lean toolchain. Its
terminal remains open. The packet demonstrates a
logical replay boundary under named assumptions; it does not prove
independent custody, hash collision resistance, evaluator soundness, or
semantic correspondence to Lean.

## Relationship to existing work

This is a successor research program, not a retrofit of Paper 0 or
NSA-000.

- PO-000 supplies the already-realized report/fiber factorization
  boundary.
- NSA-000 identifies a selection boundary but explicitly leaves the
  general evaluation-and-authorization impossibility theorem open.
- The authority-firewall paper gives an architectural type separation
  and explicitly retains verifier soundness as an external trust-root
  problem.
- PO-022 and PO-023 provide the prior finite-presentation and stop-bit
  research designs; their current Lean companions are `True` scaffolds,
  not formal support for this program.
- `19L57G1@sealed-derivation-v1` is cited only as a sealed record that
  mechanical gates do not discharge semantic claim correspondence. No
  derivation material is copied from that repository.

**AuthorityEffect:** None.
