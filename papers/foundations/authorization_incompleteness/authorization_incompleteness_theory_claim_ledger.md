> **Recovered file.** Source: `C:\.ana\coda_university\coda_research\authorization_an_incompleteness_theory\authorization_incompleteness_theory_claim_ledger.md` (external, read-only).
> Recovery date: 2026-10-21. Recovered verbatim; statuses below are the source's, not audited.
> Audit and comparison with this repository: [RECOVERY_NOTES.md](RECOVERY_NOTES.md).

---

# Claim ledger: Authorization as an Incompleteness Boundary

**Paper key:** `authorization_an_incompleteness_theory`

**Version:** v0.14

**Date:** 2026-08-21

**AuthorityEffect:** None.

The ledger separates a finite Lean theorem from standard external
results, architectural definitions, and planned formalizations. A green
Lean command for AIT-1 or AIT-2 does not discharge any later row.

<!-- markdownlint-disable MD013 -->
| ID | Statement | Class | Status | Evidence / boundary |
| --- | --- | --- | --- | --- |
| AIT-0 | `total certainty` means soundness and completeness for an explicitly named domain and predicate. | Definition | defined | Paper §2, immediately after the three-level table; no semantic result follows from the definition. |
| AIT-PD0 | A minimal Bool Primitive Difference analogue has two extensions with the same primitive index but different validity and terminal-policy values. | Lean finite model | proved | `primitive_interface_has_distinct_authorization_extensions`; this is finite non-uniqueness, not the full J011 general theorem. |
| AIT-PD1 | For J011's actual `PrimitiveDifference P` quotient report `pdProj P`, a supplied validity predicate that splits a `ZeroRel P` class cannot factor through the quotient; a ZeroRel-constant validity predicate has a quotient decision. | Lean theorem | proved, rooted target | `primitive_difference_p0_bridge.lean`; `pd_quotient_split_blocks_report_only_authorization` and `pd_quotient_decision_if_zeroRel_constant`; built by `lake build AuthorizationIncompletenessTheory` on 2026-08-20. Negative statements depend on `propext` and `Quot.sound`; the positive lift has no axiom dependencies. This is statement-level P0 specialization, not a direct P0 import. |
| AIT-P0 | A validity predicate splitting a report fiber cannot be decided by a function of the report alone. | Lean theorem | established in PO-000 | `AuthorizationBoundary.no_report_decision` in PO-000. P0 is unchanged. |
| AIT-1 | If a validity predicate splits a report fiber, no function of the report is correct on every proposal. | Lean theorem | proved | `split_fiber_blocks_total_authorization` restates P0's finite theorem in this directory. It is corroborating evidence, not a replacement for P0. |
| AIT-2 | A constant self-receipt for a packet that can be valid or invalid cannot decide that packet validity; a report retaining the bit can decide this toy contract. | Lean theorem / finite model | proved | `self_receipt_blocks_authorization` and `complete_receipt_decides_toy_contract`. It is a toy, not a theorem about all receipts. |
| AIT-E0 | Physical separation is neither necessary nor sufficient for bounded authorization in the stated finite models: co-located complete reporting can authorize, while separate sites with a collapsed report cannot. | Lean finite model | proved, rooted target | `physical_separation_neither_needed_nor_sufficient_for_toy_authorization` in `logical_externality_models.lean`; axiom-free. `Site` is only a label and does not model custody, security, or semantic truth. |
| AIT-TC0 | A declared blank/marked tape-control model permits two halting presentations with the same control report but different supplied contract values; `unread` is distinct from an alphabet symbol and can hide a contract-relevant cell; a read token and a halt outcome each admit different supplied semantic adapters or terminal policies. | Lean finite model | proved | `same_read_token_allows_distinct_semantic_adapters`, `unread_report_blocks_content_decider`, `same_halt_control_blocks_control_only_decider`, and `syntactic_halt_does_not_select_terminal_policy`, all axiom-free. This is not a general Turing-machine theorem. |
| AIT-TC1 | A frozen single-prompt, no-literature derivation run is a provenance and countermodel-discovery experiment, not evidence of novelty, formal validity, or external authorization. | Research protocol | defined | `controlled_turing_derivation_series.md` specifies frozen provenance, post-seal literature audit, a positive witness, and a failed-descent control for each lift. |
| AIT-TC2 | One declared four-configuration transition table realizes advance, stay, and halt; it preserves one supplied Boolean contract, violates a different supplied Boolean contract on a named countertrace, and distinguishes full-report adequacy from inadequate control-only reporting. | Lean finite model | proved, rooted target | `tape_transition_invariant_models.lean`: `transition_preserves_clean_terminal_contract`, `marked_contract_countertrace`, `transition_does_not_preserve_marked_cell_contract`, `full_configuration_report_adequate_for_marked_cell_contract`, and `control_report_not_adequate_for_marked_cell_contract`, all axiom-free. This is a finite table/contract result, not a Turing-machine or semantic-invariant theorem. |
| AIT-DTM0 | A finite rule-list machine with a total mathematical tape and a fuel-bounded evaluator distinguishes declared halt, stuck, and fuel exhaustion; a declared halt is a designated control state and does not select a terminal policy. | Lean operational seed | proved; partial carrier only | direct_turing_machine_models.lean. Blank/absence and write/reaches-halt fixtures have no axioms; generic terminal/policy declarations and closed stuck/fuel fixtures depend on propext. No byte parser, universal machine, extensional property, reduction, halting-decider, or P versus NP claim follows. |
| AIT-DTM1 | The DTM0 finite rule-list machine has a declared natural-number token grammar: a halt-state token plus complete five-token rule frames. Its decoder rejects empty, truncated, invalid-symbol, and invalid-movement code and recovers every machine from its emitted token code. | Lean finite syntax lift | proved; partial carrier only | `direct_turing_machine_token_code_models.lean`. Symbol/movement tag round trips have no axioms; rule-list/machine parser round trips and malformed-code fixtures print `propext`. The result is not source bytes, input/configuration encoding, parser-to-execution agreement, universality, reduction, or an authorization theorem. |
| AIT-G3a | In a finite structural replay model, a supplied trust root and exact submission bind a receipt; source-controlled self-attestation, checker/schema/contract substitutions, and payload substitution are rejected, while terminal policy remains a separate input. | Lean finite model | proved, rooted target | `replay_packet_binding_models.lean`: `self_pass_cannot_authorize_invalid_content`, `checker_substitution_is_binding_rejected`, `replayed_status_requires_bound_submission`, and `terminal_policy_is_not_selected_by_verification`, all axiom-free. Structural equality is not cryptographic binding, verifier soundness, custody, or deployment security. |
| AIT-G3 | A concrete finite packet binds proposal, contract, policy, evaluator, entrypoint, Lean model, direct formal dependency, and toolchain with SHA-256; source pass fields and tested substitutions do not determine the result. | Executable bounded packet | replayed; bounded scope | `code/replay_packet/`; 23 unit cases, 21 rejected mutations, and one target-local Lean-closure integration replay. The manifest is a declared trust root, not self-authentication. Collision resistance, custody, runtime integrity, and evaluator soundness remain assumptions. |
| AIT-G4 | The full configuration report is adequate for the finite marked-cell contract, while the control-only report is not; the executable control-only route returns open_due_to_inadequate_report. | Lean finite theorem plus executable model | proved; bounded scope | `full_configuration_report_adequate_for_marked_cell_contract`, `control_report_not_adequate_for_marked_cell_contract`, and the AIT-G3 packet. The terminal policy stays open. This is not an authority result or a general semantic theorem. |
| AIT-G5a | A source no-decider boundary transfers to total proposal authorization when a validity-preserving reduction and decision-class closure are supplied. | Lean theorem | proved, rooted target | `GlobalComputabilityLift.no_source_decider_blocks_total_authorizer`, axiom-free. It does not instantiate a computable decision class, prove source undecidability, or prove Rice's theorem. |
| AIT-G5c | Given an explicit class-relative no-total-decider premise and allowed acceptance-bit membership, no terminalizer can be both acceptance-sound and acceptance-complete; if it is also rejection-sound and never unresolved, it would be acceptance-complete. A Boolean fixture remains a closed sound/complete local terminalizer. | Lean theorem / finite scope fence | proved, rooted target | `terminal_authorization_boundary_models.lean`: `acceptance_bit_decides_of_sound_complete`, `no_total_decider_blocks_sound_complete_authorization`, `closed_two_sided_terminalization_is_acceptance_complete`, `no_total_decider_blocks_closed_two_sided_terminalization`, and `finite_closed_terminalizer_remains_possible`. The first, second, fourth, and fifth print `propext`; the third prints no axioms. This is conditional on supplied `NoTotalDecider` plus allowed membership, not a Rice, LLM, or physical-externality theorem. |
| AIT-G5b | A global arbitrary-program claim is not admitted until its syntax, execution semantics, universality, extensionality, nontrivial witnesses, reduction plan, report/policy split, and replay boundary are frozen. | Research admission gate | defined; open | computability_lift_admission.md and computability_carrier_candidates.json. The validation test rejects premature candidate selection or admission. A finite trace, AIT-DTM0, PO-022, PO-023, or a blind derivation run may supply candidates, but none is thereby a Turing-complete carrier or a Rice proof. |
| AIT-3 | A logical authorization boundary is a fixed contract, checker, semantics, and replay root outside proposal-controlled content; it need not be a separate physical machine. | Definition / architecture requirement | defined | Paper §2 and §5. Requires an implementation-specific custody audit. |
| AIT-4 | A local proof checker can decide a fixed proof-object language relative to its trusted implementation and declared semantics. | Standard construction | cited | Necula 1997; this is the constructive local case, not a global semantic oracle. |
| AIT-5 | No total computable procedure is sound and complete for a nontrivial extensional semantic property of arbitrary programs in a Turing-complete language. | Standard external theorem | cited; local formalization open | Rice 1953. `AIT-G5a` formalizes only the class-relative reduction transport; the future Rice target must still define the language, computable decision class, semantic predicate, nontrivial witnesses, source theorem, and reduction. |
| AIT-6 | Under the standard hypotheses, a consistent recursively axiomatized theory cannot establish its own consistency internally. | Standard external theorem | cited; local formalization open | Goedel 1931 and Loeb 1955. This is a metatheoretic boundary, not a claim that no proposition can be proved. |
| AIT-7 | A computable LLM acting only as a proposal source cannot itself supply globally total semantic authorization for arbitrary proposals. | Derived conditional conclusion | pending AIT-5 model binding | Requires a precise LLM execution model, a proposal embedding, and the exact decision claim. |
| AIT-8 | A passing replay can license only the policy scope named by an independently fixed checker and trust boundary. | Architecture corollary | bounded packet replayed; deployment protocol open | AIT-G3 now supplies a bounded receipt manifest, explicit cryptographic/custody assumptions, and a replay/adversarial test packet. AIT-G8 still requires an independently controlled deployment protocol and review. |
| AIT-9 | The sealed `19L57G1@sealed-derivation-v1` record is evidence about eight mechanical gates, not a proof of semantic claim correspondence. | Source classification | established by source record | No sealed code or paper text is imported into this directory. |
<!-- markdownlint-enable MD013 -->

## Exact theorem statements presently formalized

```text
split_fiber_blocks_total_authorization
  If there exist x and y with report x = report y and valid x != valid y,
  then no authorize : Report -> Bool has
  authorize (report z) = valid z for every z.

self_receipt_blocks_authorization
  The constant Unit receipt of a packet with a Bool semantic field cannot
  decide the field on every packet.

unread_report_blocks_content_decider
  A report that always says `unread` cannot decide the supplied content
  contract for every tiny tape-control presentation.

replayed_status_requires_bound_submission
  In the finite structural model, a replayed status can succeed only for
  the exact submission bound into its receipt.

transition_preserves_clean_terminal_contract
  The named four-state transition table preserves its named
  clean-terminal Boolean contract.

transition_does_not_preserve_marked_cell_contract
  The same table fails to preserve the separately supplied marked-cell
  Boolean contract on its named running-marked countertrace.

full_configuration_report_adequate_for_marked_cell_contract
  The identity report on the finite configuration carrier is adequate
  for the supplied marked-cell Boolean contract.

control_report_not_adequate_for_marked_cell_contract
  The control report has a shared stay fiber that splits the supplied
  marked-cell Boolean contract.

no_source_decider_blocks_total_authorizer
  A class-relative source no-decider premise transfers through a supplied
  validity-preserving reduction and supplied decision-class closure.

decodeMachine_encodeMachine
  Decoding the declared finite token code emitted for a DTM0 finite
  rule-list machine recovers that same machine.
```

These theorem statements are finite and algebraic. None states that an LLM,
an evaluator, or a theorem prover cannot check a simple contract.

## Required proof status before a public “global” sentence

The following must be present before treating AIT-7 as more than a
conditional research conclusion.

1. The AIT-PD0 bridge from Primitive Difference to the proposal and
   validity-predicate interface.
2. A per-lift P0 descent audit for proposal, evaluation, replay, and
   authorization maps.
3. A formal proposal-language model and nontrivial semantic property.
4. A local mechanization or independently audited theorem reduction for
   AIT-5, with the exact Rice hypotheses visible.
5. A formal distinction between an LLM-only route and a route containing
   a trusted external oracle, proof kernel, or policy owner.
6. The bounded replay packet and mutation corpus now present in AIT-G3,
   followed by an independently controlled custody and environment
   protocol for any deployment claim.
7. A formal or carefully cited metatheoretic treatment of AIT-6 with
   the required consistency and representability hypotheses.

## Nonclaims

- No global safety, alignment, legal, or business-policy guarantee.
- No claim that an external evaluator is automatically trustworthy.
- No claim that Goedel's theorem alone proves the full LLM conclusion.
- No claim that a finite Lean theorem settles arbitrary program
  semantics.
- No use of a test pass, hash, or a model's confidence as authorization.
- No treatment of structural equality in the finite replay model as a
  deployed cryptographic or custody guarantee.
- No treatment of the bounded SHA-256 packet as a self-authenticating
  receipt, independent custody proof, evaluator-soundness theorem, or
  global semantic authorization.

**AuthorityEffect:** None.
