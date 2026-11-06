# Authorization Incompleteness Formal Binding Manifest

**Recorded:** 2026-08-21

**Status:** producer-side binding manifest, not an independent receipt or
authority-bearing artifact.

**AuthorityEffect:** None.

This manifest binds the working paper's finite claims to current source
bytes, named declarations, imports, and the current Lake target. A later
independent evaluator must recompute every hash, statement comparison,
build, and axiom report. A matching source hash does not establish the
global Rice, Goedel, or LLM conclusion.

## Build binding

```powershell
Set-Location lean4\genx
lake build AuthorizationIncompletenessTheory
```

**Current producer-side result:** succeeded on 2026-08-21 with 40 Lake
jobs. The target roots the eleven files below and the J011 candidate import
closure needed by the quotient bridge. It is not a default target and
does not establish an estate-close result.

## DTM1 mutation sensitivity

The producer ran three source mutations against the isolated DTM1 module,
then restored the checked source before the recorded build.

1. Changing the `marked` encoder tag from `1` to `0` made
   `decodeTapeSymbol_encodeTapeSymbol` fail.
2. Changing the decoder's invalid-tag branch from `none` to
   `some blank` made `invalid_symbol_tag_is_rejected` fail.
3. Changing the movement decoder's invalid-tag branch from `none` to
   `some stay` made `invalid_move_tag_is_rejected` fail.

These failures show that the positive tag law and negative malformed-code
fixture are sensitive to the corresponding parser behavior. They do not
establish a byte-level parser, semantic adequacy, or a global carrier.

<!-- markdownlint-disable MD013 -->
| Bound object | SHA-256 |
| --- | --- |
| `lean4/genx/lakefile.lean` | `effb0d05e11f801d91b9fe0f038b6be787d731517ddd0a29b6dc67e244c36577` |
| `lean4/genx/lean-toolchain` | `2bdc48adfa58d0017e538a0ad117c5d73d35deec879978f909406a80c8037273` |
| `lean4/genx/lake-manifest.json` | `f1e22d27087fb5b1bf9752a4a8a670c253f9f37564232d4a341345249f0ba14c` |
| `formal/authorization_incompleteness_core.lean` | `80776d087b1800e0c917fd0cc9dfd6068126f49f38bf7376a6e956b5d0ad2991` |
| `formal/direct_turing_machine_models.lean` | `0fb0e2bd0688bd926904235e3e666504b82ab45d4a72f7d53e3ddfcec46402c9` |
| `formal/direct_turing_machine_token_code_models.lean` | `6d3aecf402c15951b53eccf49e1609180346bac425496f3cd85264e6ba527153` |
| `formal/global_computability_lift_models.lean` | `c3a3d2a9ba5fb5a78f1a36ebdb3e3e754510956143097a8af4831df74fddb18d` |
| `formal/logical_externality_models.lean` | `4955e53d4dfedb619b9da91eefcc510975a7ecbeffad2d9dc804dd3ce496f35a` |
| `formal/primitive_difference_authorization_models.lean` | `4178e928eac8f349a98cc03d7f9b13604296f12d57f5f221d09fc6436c410d47` |
| `formal/primitive_difference_p0_bridge.lean` | `205df3a04fbf7e6850e919e9f40b635c14b23b1e2bccda71bba35390bd2b7e51` |
| `formal/replay_packet_binding_models.lean` | `a0d50e28e7c5fb67468ecc34f24ccf6b101542e94377969e97c963f02310ebdb` |
| `formal/tape_control_authorization_models.lean` | `c6d4e136cd5e0c8f696383518cee4657bd58e3354b07960f5525216b28af87df` |
| `formal/tape_transition_invariant_models.lean` | `5d6467c5b88a3955bd78f55a6629fe5c204a004bfe4e68c11b24e11544e1fab0` |
| `formal/terminal_authorization_boundary_models.lean` | `a0ac0eec152cf48147a6294c3e4c84d933b71c3032e76e19ea51e10735d954d3` |
| `code/replay_packet/packet_manifest.json` | `c4447fd3a86c4763c51b67f759d3ee9af58772b672f2ee6b5685396fab721b08` |
| `code/replay_packet/replay_packet.psm1` | `7b55c23f76d76da4b43b3a20618f5d927becbe8057ac78f557eaef3845076edc` |
| `code/replay_packet/verify_transition_packet.ps1` | `8281bb577bba3947a0577860e7592bb966133f64953c7839c23001c81ad654fd` |
| `code/tests/test_replay_packet.ps1` | `47178b94b33d690d7bfbc1ae3141e90e1a63ed70c00091ac319bd7abe596284a` |
| `code/integration_tests/test_transition_packet_integration.ps1` | `a9f55e60791238ccb1319b825e1c68340ce7fdc2ab31bfb6b6fc6db603c80305` |
| `computability_carrier_candidates.json` | `8f951b3afd30a62ffe0a6e667b8a171ee513e821cb75bc3aaa0552eca0c39f29` |
| `code/tests/test_computability_carrier_candidates.ps1` | `bb8f3ab228c887a0dcea97eecbfdb27231b72b252c8f06c52b6ca618a6b230e7` |
| PO-000 source, not imported | `fb7d2436f1e5da5969c8c4d9b1a143b4a2a0ba8024748568733f4290414d701e` |
| J011 candidate source imported by bridge | `7ee3a63b154220f82b76a49a045ca074afa899f4d6a087bcb29c93cd0698d6f4` |
<!-- markdownlint-enable MD013 -->

## Claim bindings

<!-- markdownlint-disable MD013 -->
| Claim | Lean declaration | Import / axiom ceiling | Exact prose ceiling |
| --- | --- | --- | --- |
| AIT-1 | `AuthorizationIncompleteness.split_fiber_blocks_total_authorization` | No imports; no axioms | A split report fiber blocks a total report-only Boolean decision. It does not name an LLM, a physical machine, or arbitrary program semantics. |
| AIT-2 | `AuthorizationIncompleteness.self_receipt_blocks_authorization` and `complete_receipt_decides_toy_contract` | No imports; no axioms | A constant `Unit` receipt is inadequate for one Boolean packet contract; retaining the bit is adequate for that toy contract. |
| AIT-PD0 | `PrimitiveDifferenceModels.primitive_interface_has_distinct_authorization_extensions` | No imports; no axioms | A minimal Boolean analogue admits different supplied validity and terminal values. It is not J011's full interface. |
| AIT-PD1 | `PrimitiveDifferenceP0Bridge.pd_quotient_split_blocks_report_only_authorization` and `pd_quotient_decision_if_zeroRel_constant` | `import J011_minimal_publication`; negative theorem: `propext`, `Quot.sound`; positive theorem: no axioms | J011 candidate `pdProj P` is a report whose fibers are `ZeroRel P`; supplied validity must be ZeroRel-constant to factor. This is statement-level correspondence to PO-000, not a direct P0 module import. |
| AIT-E0 | `LogicalExternalityModels.physical_separation_neither_needed_nor_sufficient_for_toy_authorization` | `import authorization_incompleteness_core`; no axioms | In the stated finite `Site`-label models, physical separation alone is neither necessary nor sufficient. It says nothing about real-world custody or security. |
| AIT-TC0 | `TapeControlModels.same_read_token_allows_distinct_semantic_adapters`, `unread_report_blocks_content_decider`, `same_halt_control_blocks_control_only_decider`, and `syntactic_halt_does_not_select_terminal_policy` | No imports; no axioms | A tiny declared tape-control model keeps tape symbols, observation control, supplied semantic adapters, syntactic halt, content contract, and policy distinct. It is not a full Turing-machine theorem. |
| AIT-TC2 | `TapeTransitionInvariantModels.transition_preserves_clean_terminal_contract`, `marked_contract_countertrace`, `transition_does_not_preserve_marked_cell_contract`, `full_configuration_report_adequate_for_marked_cell_contract`, and `control_report_not_adequate_for_marked_cell_contract` | `import tape_control_authorization_models`; no axioms | One finite table preserves one named supplied Boolean contract and violates another on a named countertrace. Full configuration is adequate for the marked-cell contract while the shared control report is not. This is not a Turing-machine or semantic-invariant theorem. |
| AIT-DTM0 | `DirectTuringMachineModels.step_halted_iff_declared_halt`, `execute_halted_of_declared_halt`, `write_and_halt_transition_writes_mark`, `write_and_halt_transition_reaches_declared_halt`, `empty_rule_fixture_is_stuck`, `looping_fixture_exhausts_bounded_fuel`, `write_and_halt_executes_to_syntactic_halt`, and `syntactic_halt_does_not_select_direct_machine_policy` | No local imports; blank/absence and closed write/reaches-halt fixture: no axioms; generic terminal, bounded-halt, closed stuck/fuel, closed-execution, and policy declarations: `propext` | Finite rule syntax and a fuel-bounded operational interpreter distinguish declared halt, stuck, and fuel exhaustion. This is neither a byte parser nor a universal-machine, Rice, halting-decider, or complexity theorem. |
| AIT-DTM1 | `DirectTuringMachineTokenCodeModels.decodeTapeSymbol_encodeTapeSymbol`, `decodeMove_encodeMove`, `decodeRules_encodeRules`, `decodeMachine_encodeMachine`, `empty_machine_code_is_rejected`, `truncated_rule_code_is_rejected`, `invalid_symbol_tag_is_rejected`, and `invalid_move_tag_is_rejected` | `import direct_turing_machine_models`; tag round trips: no axioms; rule-list/machine round trips and malformed-code fixtures: `propext` | The DTM0 finite rule list has a complete natural-number token grammar and an all-consuming parser that recovers encoded machines and rejects named malformed forms. It is not source bytes, input/configuration encoding, trace agreement, a universal machine, or an authorization result. |
| AIT-G3a | `ReplayPacketBindingModels.self_pass_cannot_authorize_invalid_content`, `checker_substitution_is_binding_rejected`, `replayed_status_requires_bound_submission`, and `terminal_policy_is_not_selected_by_verification` | No imports; no axioms | A supplied `TrustRoot` and exact `Submission` bind a finite receipt. Source self-attestation and selected substitutions are rejected, while terminal policy remains separate. Structural equality is not a cryptographic, custody, or verifier-soundness result. |
| AIT-G3 | `code/replay_packet/packet_manifest.json` and its PowerShell verifier | SHA-256 bindings, PowerShell 7.6.3, and Lean 4.32.2 are explicit inputs | A concrete bounded packet rejects named byte, path, schema, parser, command, evaluator, and policy substitutions, then compiles its two-source local Lean closure. The manifest is not self-authenticating and does not prove custody, collision resistance, or evaluator soundness. |
| AIT-G4 | `full_configuration_report_adequate_for_marked_cell_contract`, `control_report_not_adequate_for_marked_cell_contract`, and the bounded packet evaluator | Lean theorems have no axioms; evaluator correspondence remains an explicit import | One finite full report supports a declared decision; the inadequate control-only route returns open. No general semantic-authority result follows. |
| AIT-G5a | `GlobalComputabilityLift.no_source_decider_blocks_total_authorizer` | No imports; no axioms | A source no-decider premise transfers through a supplied validity-preserving reduction and decision-class closure. It is not a Rice theorem and does not instantiate computability. |
| AIT-G5c | `TerminalAuthorizationBoundary.acceptance_bit_decides_of_sound_complete`, `no_total_decider_blocks_sound_complete_authorization`, `closed_two_sided_terminalization_is_acceptance_complete`, `no_total_decider_blocks_closed_two_sided_terminalization`, and `finite_closed_terminalizer_remains_possible` | `import global_computability_lift_models`; first, second, fourth, and fifth: `propext`; third: no axioms | Given a supplied `NoTotalDecider` and allowed acceptance-bit membership, no terminalizer is jointly acceptance-sound and acceptance-complete; closed two-sided soundness entails acceptance completeness. A finite Boolean fixture permits closed local terminalization. Not Rice, LLM, physical-externality, or custody. |
<!-- markdownlint-enable MD013 -->

## Bounded packet binding

The concrete V4 packet manifest has the producer-side hash
`c4447fd3a86c4763c51b67f759d3ee9af58772b672f2ee6b5685396fab721b08`.
It carries the individual artifact digests for the proposal, contract,
policy, evaluator, entrypoint, Lean model, direct Lean dependency, and
toolchain, plus explicit assumptions for SHA-256 collision resistance,
evaluator correspondence, runtime integrity, and custody. Its entrypoint
returns a verified finite evaluation with terminal `open`; it does not
emit an authority-bearing result.

The current producer-side replay ran:

1. the 23-case PowerShell unit corpus, including 21 rejected mutations;
2. the PowerShell integration replay, including its target-local
   two-source Lean closure;
3. the separate named 40-job Lean target build; and
4. the six-case computability-candidate inventory test, including five
   rejected premature-promotion or malformed-record mutations.

These executions show that the current bytes follow the bounded
protocol. They do not make the manifest self-authenticating or supply
the independent custody required for a real deployment.

## Statement correspondence for the P0 bridge

PO-000's `AuthorizationBoundary.no_report_decision` has the shape:

```text
p : X -> M, valid : X -> Bool,
split report fiber -> no M -> Bool decision factors valid through p.
```

`pd_quotient_split_blocks_report_only_authorization` specializes it as:

```text
X := α
M := ResidualQuotient (pdSetoid P)
p := pdProj P
report-fiber equality := ZeroRel P, by J011 pdProj_eq_iff_zeroRel
valid := supplied α -> Bool predicate
```

The P0 source has no Lake module in the current repository layout. The
bridge repeats the equality-chain proof against the J011 quotient rather
than claiming an import it does not perform.

## Recompute requirements

Before any stronger status, recompute all of the following from the
candidate revision:

1. Each SHA-256 above.
2. The named Lake build and its import closure, separately from the V4
   target-local two-source Lean replay.
3. `sorry` / `admit` scan of the eleven Lean source files and
   a separate source review of the packet and candidate-validator
   PowerShell files.
4. Every listed `#print axioms` result.
5. Exact theorem-statement-to-paper comparison, especially the P0 bridge
   and the finite `Site` model.
6. Separate citation and scope review for Rice, Goedel, the LLM model,
   replay custody, and terminal policy.

**AuthorityEffect:** None.
