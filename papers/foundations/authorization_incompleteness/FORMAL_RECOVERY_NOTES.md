# Formal and code recovery notes: Authorization as an Incompleteness Theory

**AuthorityEffect:** None.

**Recovered:** 2026-10-21, branch `auth-formal` (based on `lean-v4-35`; Lean `leanprover/lean4:v4.35.0`, Mathlib `v4.35.0` pin).

**Source:** `C:\.ana\coda_university\coda_research\authorization_an_incompleteness_theory` (42 files, read-only; no
PowerShell or other script from it was executed). This note covers the FORMAL and CODE half: `formal/` (11 Lean files),
`code/`, `evidence/`, the JSON files, `formal_binding_manifest.md` and the `.ps1`/`.psm1` tooling. The prose half is
recovered by a second agent.

Verbatim evidence and the replay record are in [`evidence/README.md`](evidence/README.md). The Lean port is
`lean4/AuthIncompleteness/` (root `lean4/AuthIncompleteness.lean`, `lean_lib AuthIncompleteness`, not a default target).

## 1. Inventory

### Lean (11 files, 197 declarations, no `sorry`, no `axiom`, no `native_decide`)

| Module (ported) | Source file | def | theorem | structure | inductive | abbrev | total | `#print axioms` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Core.lean` | `authorization_incompleteness_core.lean` | 5 | 5 | 1 | 0 | 0 | 11 | 4 |
| `DirectTM.lean` | `direct_turing_machine_models.lean` | 19 | 9 | 4 | 3 | 1 | 36 | 9 |
| `TokenCode.lean` | `direct_turing_machine_token_code_models.lean` | 9 | 8 | 0 | 0 | 0 | 17 | 8 |
| `GlobalLift.lean` | `global_computability_lift_models.lean` | 3 | 2 | 1 | 0 | 0 | 6 | 2 |
| `Terminal.lean` | `terminal_authorization_boundary_models.lean` | 7 | 10 | 0 | 1 | 0 | 18 | 5 |
| `PDModels.lean` | `primitive_difference_authorization_models.lean` | 3 | 5 | 2 | 0 | 0 | 10 | 4 |
| `Externality.lean` | `logical_externality_models.lean` | 3 | 7 | 1 | 0 | 0 | 11 | 4 |
| `Replay.lean` | `replay_packet_binding_models.lean` | 14 | 9 | 3 | 7 | 0 | 33 | 7 |
| `TapeControl.lean` | `tape_control_authorization_models.lean` | 10 | 9 | 3 | 4 | 0 | 26 | 6 |
| `TapeTransition.lean` | `tape_transition_invariant_models.lean` | 8 | 10 | 2 | 1 | 0 | 21 | 9 |
| `PDBridge.lean` | `primitive_difference_p0_bridge.lean` | 3 | 5 | 0 | 0 | 0 | 8 | 4 |
| total | 11 files | 84 | 79 | 17 | 16 | 1 | 197 | 62 |

No `lemma`, `axiom` or `sorry` occurs in the source. Ten modules (189 declarations, 58 printed theorems) build; `PDBridge`
(8 declarations, 4 printed theorems) cannot be built here.

### Code, evidence and JSON

| File | What it computes or records |
| --- | --- |
| `code/replay_packet/replay_packet.psm1` | `Test-ReplayPacket`: exact-key manifest checks, licensed roles, paths, kinds, SHA-256 of eight bound artifacts, duplicate-key and UTF-8 rejection. `Invoke-ReplayPacket`: parses proposal, contract and terminal policy; enumerates the four-configuration table; tests the clean-terminal contract; lists marked-cell countertraces; compares the full-configuration report with the control-outcome report; returns terminal `open`. |
| `code/replay_packet/verify_transition_packet.ps1` | Entry point; optional `-RunFormalReplay` compiles the bound dependency then model with `elan run leanprover/lean4:v4.32.2 lean`. |
| `code/replay_packet/{packet_manifest,transition_proposal,transition_contract,terminal_policy}.json` | Manifest (8 SHA-256 bindings, assumptions, execution profile), the 4-row proposal, the contract with `expected` results, and the leave-open policy. |
| `code/tests/test_replay_packet.ps1` | 23 cases: 1 good packet, 1 self-pass-flag check, 21 refused mutations. |
| `code/tests/test_computability_carrier_candidates.ps1` | 6 cases: 1 good record, 5 refused promotion or malformed-record mutations; also greps the unrecovered PO-022/PO-023 scaffolds. |
| `code/integration_tests/test_transition_packet_integration.ps1` | Runs the verifier with the formal replay and asserts `verified`, `open`, `pass`, control-only inadequate. |
| `computability_carrier_candidates.json` | Four candidates (`AIT-DTM0`, `PO-022`, `PO-023`, `AIT-PACKET4`) against eight admission fields; globally `open`, nothing selected. |
| `formal_binding_manifest.md` | 21 SHA-256 bindings, claim-to-declaration table (AIT-1 to AIT-G5c), recompute checklist. |
| `evidence/source_map.md` | What the folder inspected and did not use. |

## 2. Comparison against the repository

Searched `lean4/`, `papers/`, `code/`, `dag/` (tracked files) for every declaration name and for the code identifiers
(`Test-ReplayPacket`, `packet_manifest`, `AIT-DTM`, `NoTotalDecider`, `FactorsThrough`, `decodeMachine`, ...).

| Class | Items |
| --- | --- |
| PRESENT | none. No declaration, code identifier, JSON record or hash of this folder exists in the repository. |
| PARTIAL (concept only) | The report-fibre obstruction: `PG-HISTORY-REPORT-CRITERION`, `PGW-WDP-BRIDGE-REPORT-FIBER-OBSERVER`, `PGW-REPLAY-NECESSITY` state the same criterion for histories and decisions. The terminal vocabulary: `TFQ-0330`. The authorization chapter `TFQ-0327` to `TFQ-0332` and `DS-QM090-092-AUTHORITY-FIREWALL` name the programme but cite later Atlas files, all marked "absent" in the checkout. |
| ABSENT | all 197 Lean declarations; the evaluator, verifier, tests and JSON; `Atlas` files `ReportFactorization.lean`, `TuringBarrier.lean`, `replay_fiber.py`, `report_factorization.py` that `TFQ-0330`, `TFQ-0331`, `TFQ-0332` cite are a LATER lineage and are not in the recovered folder either. |

## 3. Port results

* **Lean.** All ten modules compile under Lean 4.35.0 with the module names changed and a provenance header added;
  statements and proofs are byte-identical to the originals. `lake build AuthIncompleteness`: 13 jobs, exit 0, no error.
  The unported originals also compile unchanged with `lean` v4.35.0, and their 58 `#print axioms` lines equal the ported
  ones. One deprecation warning (`if_neg` in `Replay.lean`, use `ite_eq_right`) was left in place.
* **Axioms** (`evidence/axiom_reports/`): every ceiling recorded in the source README and manifest reproduces. `Core`,
  `GlobalLift`, `PDModels`, `Externality`, `Replay`, `TapeControl`, `TapeTransition`: no axioms for all printed theorems.
  `DirectTM`: none for `blank_symbol_is_not_option_absence`, `write_and_halt_transition_writes_mark`,
  `write_and_halt_transition_reaches_declared_halt`; `propext` for the other six. `TokenCode`: none for the two tag round
  trips, `propext` for the other six. `Terminal`: none for `closed_two_sided_terminalization_is_acceptance_complete`,
  `propext` for the other four. No `Classical.choice`, no `Quot.sound` in any built module.
* **Not portable.** `PDBridge.lean` imports `J011_minimal_publication` (namespace `GrokPdNight20260814`). Its source is not
  in this repository or the recovered folder (the neighbouring `coda_research/_support` tree holds only `J011_minimal_publication.md`, which cites it). The file is
  kept with its import verbatim and a header saying NOT BUILT, and is excluded from the lakefile roots. The source records
  `propext` and `Quot.sound` for its negative theorems; that cannot be reproduced. The staged `PrimitiveDifference.lean` copies
  under `dag/results/*/construction/lean4/` have a different API (`P.ZeroRel`, `classOf`), so substituting them would change
  the statements; this was not done.
* **Python** (`code/python/src/qm/auth_incompleteness/`): `replay_packet.py` (port of the `.psm1` and `.ps1`),
  `carrier_candidates.py` (port of the candidate validator), `finite_models.py` (new executable twins of the DTM0 evaluator,
  DTM1 token code and transition table; not a recovered file). Tests in `code/python/tests/test_auth_incompleteness_*.py`:
  55 pass, including the 23-case replay corpus (21 refused mutations), the 6-case candidate corpus (5 refused mutations) and
  a formal replay of the two bound original Lean files.
* **New, not recovered.** `lean4/AuthIncompleteness/MathlibBridge.lean` (4 theorems) instantiates the recovered `GlobalLift`
  transport with Mathlib's `Computable` and `ComputablePred.halting_problem`: `halting_has_no_computable_decider`,
  `computable_closed_under_computable_reduction`, `no_computable_authorizer_of_computable_reduction`,
  `halting_transport_instance`. Compiled with `lean` v4.35.0 against the Mathlib v4.35.0 build, exit 0, no warning; axioms are
  `propext`, `Classical.choice`, `Quot.sound` (Mathlib's). It is not a lakefile root (the isolated recovery environment has
  no Mathlib build, so it was not run through `lake`).
* **Evidence.** 18 recovered files hash-match the manifest; the toolchain pin was reconstructed and matches; lakefile,
  lake-manifest, PO-000 and J011 digests cannot be checked. Details in `evidence/README.md`.

## 4. Audit: what is actually stated

### 4.1 Theorem by theorem

| Claim (manifest id) | What the declarations state | Prose or manifest reading |
| --- | --- | --- |
| AIT-1 `split_fiber_blocks_total_authorization` | For any `report : P -> R`, `valid : P -> Bool`: if two proposals share a report and differ in validity, no `R -> Bool` function agrees with `valid` on all proposals. Proof is `congrArg`. | Matches. It is the Bool form of the fibre criterion already in the DAG (`PG-HISTORY-REPORT-CRITERION`); necessity only. |
| AIT-2 `self_receipt_blocks_authorization`, `complete_receipt_decides_toy_contract` | The one-bit `Packet` with a `Unit` receipt: no decider; identity report: a decider. | Matches; a toy. |
| AIT-PD0 `primitive_interface_has_distinct_authorization_extensions` | Two functions over `Bool` disagree at `true`. | The fields `mark` and `zero` of `RawPrimitiveDifference` are never used by `AuthorizationExtension`; the "primitive difference" content is decorative, so "non-uniqueness for AIT-PD0" is the existence of two different functions. |
| AIT-PD1 `pd_quotient_split_blocks_report_only_authorization` | The same equality chain on J011's quotient `pdProj P`. | Cannot be checked here (J011 missing). |
| AIT-E0 `physical_separation_neither_needed_nor_sufficient_for_toy_authorization` | Two `Presentation`s over `Bool`: identity report with equal labels authorizes; `Unit` report with distinct labels does not. | `Site` never occurs in `CanAuthorize`, so the theorem has no content about physical placement beyond "authorization depends on report and validity only". The headline answer to the externality question rests on that modelling choice. |
| AIT-TC0 tape-control | `unread` and control-only reports cannot decide a supplied `contentContract` on six presentations; two supplied adapters disagree. | Matches; supplied examples. |
| AIT-TC2 transition | Table preserves `cleanTerminalContract`, violates `markedCellContract` at `runningMarked`; identity report adequate, control report not. | Matches. The Python evaluator finds a second countertrace, `haltedMarked`. |
| AIT-DTM0 | Evaluator consistency lemmas (`step_halted_iff_declared_halt`, `execute_halted_of_declared_halt`) and three `rfl` fixtures. | Matches. Halting of runs is not defined; fuel exhaustion is not non-halting (the manifest says so). |
| AIT-DTM1 | `decodeMachine (encodeMachine m) = some m`; four malformed lists rejected. | Matches. One direction only; "mutation sensitivity" (3 mutants) is a recorded run, not re-executed. |
| AIT-G3a replay model | Fixed `rfl` facts and `replayed_status_requires_bound_submission`. | Matches; structural equality, not a digest. |
| AIT-G4 / AIT-G3 packet | Lean adequacy theorems plus the packet evaluator. | The evaluator is not related to the Lean model by any theorem (the manifest says so); `full_report_adequate` is a constant `true`. |
| AIT-G5a `no_source_decider_blocks_total_authorizer` | Contrapositive of composing a decider with a reduction, relative to arbitrary predicates `allowedHard`, `allowedProposal`. | Matches. With `allowed` equal to all Bool functions the premise `NoTotalDecider` is false for every predicate (classical `decide`), so the theorem has content only after instantiation with a computability class, which is exactly the missing step. |
| AIT-G5c terminal boundary | Acceptance bit decides if sound and complete; closed, rejection-sound terminalizers are acceptance-complete; Bool fixture. | Matches; conditional on a supplied `NoTotalDecider`. |

Every ceiling stated in `formal/README.md` and the manifest (axioms, "not Rice", "not a universal machine", "not
cryptographic") is accurate for the code recovered. No claim in those documents exceeds its Lean statement; the places
where a headline outruns its declaration are AIT-PD0 and AIT-E0 above, and both are flagged by the source itself in
a "does not yet" sentence.

### 4.2 Turing machines, computability, halting and incompleteness

* **No Mathlib computability library is used by the recovered files.** They import nothing at all (the one exception is the unbuilt
  bridge importing J011). `Turing.TM0`, `Turing.TM1`, `Turing.TM2`, `Nat.Partrec.Code`, `Computable`, `ComputablePred`,
  `ManyOneReducible` and `ComputablePred.halting_problem` are never referenced.
* **DTM0 is a home-made deterministic machine.** It is a plausible two-symbol Turing-style machine (finite rule list, halt
  state, bidirectional integer tape, left, right and stay moves, left-biased lookup). It differs from `Turing.TM0`:
  states are `Nat`, not a type with a distinguished start; a row writes and moves in one step where `TM0.Stmt` is
  `move` or `write`; "stuck" (no row) is `TM0` halting while DTM0 also has a designated halt state; the tape is an
  arbitrary function `Int -> Symbol`, not a finitely supported `ListBlank`, so configurations include tapes that no
  computation can produce or read; the alphabet is fixed at two symbols. No theorem relates it to any standard model, no
  halting predicate (`exists fuel, execute ... = halted`) is defined, no input or output convention exists, and there is no
  simulation or universality statement. So DTM0 is not shown faithful beyond the three fixtures.
* **DTM1 is a list-of-naturals code, not a Goedel numbering.** `decode (encode m) = some m` is the only property.
* **No halting, undecidability, Rice or Goedel statement is formalized.** The title's "incompleteness" is report
  inadequacy (a split fibre), not Goedel incompleteness. The only decidability-flavoured results (`GlobalLift`,
  `Terminal`) are conditional on a supplied `NoTotalDecider` over an unspecified class. The prose ledger itself lists
  AIT-5 (Rice), AIT-6 (Goedel) and AIT-7 (LLM) as cited or pending; `computability_carrier_candidates.json` keeps universality,
  extensionality, nontriviality and effective reduction `open` for the best candidate.
* **What is established.** (i) For finite report maps, an authorizer reading only the report cannot be total unless the
  report is adequate (kernel-checked, axiom-free). (ii) A transport lemma and a terminalization consequence that become
  incompleteness-type results only once someone supplies a computability class and an undecidable source predicate.
  (iii) A fuel-bounded rule-list evaluator with three fixtures, a token codec round trip, and a bounded replay packet whose
  Python port reproduces the recorded 23 cases and 21 refused mutations.

## 5. Reusable for C1 to C8

The parallel derivation (branch `comp-utm`) builds a chain from the inert mark toward a universal machine; its files
`GenesisComputation.lean` (C1 to C4, C8) and `GenesisCompTM.lean` (C5, Mathlib `Turing.TM0` as a semi-Thue system) were
read for their headers only. Recovered declarations that could directly serve:

| Chain step | Recovered declarations | How they help | Caveat |
| --- | --- | --- | --- |
| Final undecidability transfer (the step that turns a halting or Rice source theorem into a barrier for authorization) | `GlobalComputabilityLift.{Decides, NoTotalDecider, ValidityReduction, ClosedUnderReduction, total_authorizer_yields_source_decider, no_source_decider_blocks_total_authorizer}` | Axiom-free and import-free. Instantiate `allowedHard`, `allowedProposal` with `Computable` and the reduction with a computable many-one map to reach Mathlib's `ComputablePred.halting_problem` or `ComputablePred.rice`. This is the one recovered item usable unchanged. | The instantiation is NOT in the recovered files. `MathlibBridge.lean` (new, written during recovery) supplies it for halting: `no_computable_authorizer_of_computable_reduction` and `halting_transport_instance`. A Rice instance is not written. |
| C3 (bounded regimes, three-valued verdict) and the closed-terminal barrier | `TerminalAuthorizationBoundary.{AuthorizationTerminal, AcceptanceSound, AcceptanceComplete, RejectionSound, TerminalClosed, closed_two_sided_terminalization_is_acceptance_complete, no_total_decider_blocks_closed_two_sided_terminalization}` | The C3 verdict (accept, reject, unresolved at the bound) has the same shape as `AuthorizationTerminal`; the theorem says a verdict that is sound on both sides and never unresolved would give a total decider, so unresolved past any bound is forced for an undecidable predicate. | Terminal vocabulary is three-valued only; needs mapping to the C3 `verdict` type. |
| C3 and C4 (bounded run versus unbounded supply) | `DirectTuringMachineModels.{execute, StepResult, looping_fixture_exhausts_bounded_fuel, execute_halted_of_declared_halt}` and the Python twin | A worked pattern that keeps `halted`, `stuck` and `fuelExhausted` distinct and records that exhaustion is not non-halting; the self-loop fixture is a concrete case where no finite fuel resolves the verdict. | A machine-specific evaluator, not the C2 `Reach`; could be related by `execute m fuel c = halted` iff `ReachB`-style reachability to a halt word. |
| C8 (coding a finite alphabet and its decoder) | `DirectTuringMachineTokenCodeModels.{encodeMachine, decodeMachine, decodeRules_encodeRules, decodeMachine_encodeMachine, invalid_*_rejected}` | Template for a total encoder, an all-consuming partial decoder, tag lemmas, frame-induction proof and negative fixtures. | Tokens are `Nat`, not bits, and frames are fixed width; a binary version needs the unary or binary token layer, and decode-after-encode is the only direction proved. |
| C5 (TM0 as a rewriting regime) | none directly | `Turing.TM0` is already the carrier there. DTM0 would need a bisimulation to `TM0` (write then move: two steps per row) to be reused; not recommended unless DTM0's explicit halt state is wanted. | |
| Report-erasure arguments for halting (for example, any function of `execute m n` kind cannot decide eventual halting) | `AuthorizationIncompleteness.{FactorsThrough, Adequate, split_fiber_blocks_total_authorization}` | Gives the split-fibre theorem for free once two machines with equal fuel-`n` report and different halting are exhibited. | The two-machine construction for every `n` is not recovered. |

Not useful for C1 to C8: the replay-binding, tape-control, tape-transition, externality, and primitive-difference models,
and the PowerShell-derived packet. They are authorization-protocol examples, not computation steps.

The instantiation of `GlobalLift` with Mathlib for halting is the new `MathlibBridge.lean`; the analogous Rice instance
(`ComputablePred.rice`) and the report-erasure argument for fuel-bounded halting reports are not written.

## 6. Open items and unrecoverable parts

* J011 (`J011_minimal_publication.lean`), PO-000 source, `lean4/genx/lakefile.lean`, `lake-manifest.json`, PO-022 and
  PO-023 sources: not recovered, so the P0 bridge is unbuilt and seven candidate evidence paths do not resolve.
* The recorded Lean toolchain for the packet is `v4.32.2`, which is not installed; the replay used `v4.35.0`.
* `lean-toolchain` of `genx` is reconstructed from its digest.
* The two prose evidence paths `proof_program.md` and `computability_lift_admission.md` resolve once the prose half is placed
  beside this directory.
* The later Atlas lineage (`TuringBarrier.lean`, `ReportFactorization.lean`, `replay_fiber.py`) is a different set of files
  than this folder and was not available.
