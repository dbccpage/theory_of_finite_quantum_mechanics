---
documentation_contract: education-documentation/v1
title: "02: DDC Complete Claim Ledger & Mechanization Map"
kind: mathematical-reference
audience:
  - researchers
  - engineers
  - coding-agents
status: active
maturity: production
claim_status: source-grounded
authority_effect: "None"
source_paths:
  - omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/source_archive/discrete_deformation_calculus_package/discrete_deformation_calculus_claim_ledger.md
  - omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/source_archive/discrete_deformation_calculus_package/docs/lean_claim_map.md
  - omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/source_archive/discrete_deformation_calculus_package/docs/claim_code_map.yaml
last_verified: 2026-09-30
---

# 02: DDC Complete Claim Ledger & Mechanization Map

**AuthorityEffect:** None. Complete claim ledger, formal Lean 4 declarations, and Python test bindings only; no authorization is conferred.

---

## 1. Epistemic Status Vocabulary

Every claim in the Discrete Deformation Calculus is assigned an explicit, un-promoted epistemic status:

- **Definition:** Declared mathematical construct, convention, or notation.
- **Finite Theorem:** Mechanized in Lean 4 without Mathlib axioms (strictly using $\{`propext`, `Quot.sound`\}$), or verified by an exact finite proof over $\mathbb{Q}$ and bound to a unit test.
- **Conditional Theorem:** Mathematically proved strictly under stated finite assumptions.
- **Computed Fixture:** Exact numerical or algebraic result verified for explicitly supplied finite data.
- **Model Consequence:** Follows within a declared software architecture or simulation harness.
- **Positioning:** Grounding relative to adjacent academic literature; not claimed as an empirical result.
- **Scope:** Operational boundary or domain delimiter.
- **Open Problem:** Stated conjecture or unproven research direction; zero proof or empirical validity is claimed.

---

## 2. Complete Claim Ledger & Mechanization Map

### Part I — The Calculus & Topological Invariants

| Claim ID | Epistemic Status | Formal Statement | Lean 4 Declaration | Python Test / Proof Binding |
| :--- | :--- | :--- | :--- | :--- |
| **OE010-01** | Finite theorem | Over $\mathbb{Q}$, $C^1 = \operatorname{im} d_0 \oplus \operatorname{im} d_1^\top \oplus \mathcal{H}^1$ with $\mathcal{H}^1 = \ker d_1 \cap \ker d_0^\top$. | Written proof; `cochain.hodge_split` | `test_cochain.py::test_hodge_split_is_orthogonal_and_matches_the_classes` |
| **OE010-02** | Scope | CODA primitives are used strictly in their defined sense. | Scope definition | Monograph §1, §3 |
| **OE010-03** | Finite theorem | Replay composes; empty tape is identity; lawful tapes form a category. | `Ddc.run_append`<br>`Ddc.lawful_append`<br>`Ddc.lawful_nil` | `test_automaton.py::test_lawful_append` |
| **OE010-04** | Finite theorem | Every emitted step receipt unconditionally carries `AuthorityEffect: None`. | `Ddc.authority_effect_none` | `test_automaton.py::test_run_tape_stops_at_the_first_unlawful_step_and_chains_receipts` |
| **OE010-05** | Finite theorem | A deformation preserves complex exactness iff Maurer–Cartan condition vanishes ($d_1 \mu_0 + \mu_1 d_0 + \mu_1 \mu_0 = 0$). | Written proof; `cochain.deformation_obstruction` | `test_cochain.py::test_maurer_cartan_obstruction_detects_unlawful_deformations` |
| **OE010-09** | Definition | DDC regime, step, tape, and lawfulness definitions. | `Ddc.run`<br>`Ddc.stepLaw` | `code/ddc/automaton.py` |
| **OE010-10** | Finite theorem | Terminal absorption: nothing is admitted following terminalization letter `T`. | `Ddc.terminal_absorbing`<br>`Ddc.lawful_T_is_last` | `test_automaton.py::test_terminal_and_refusal_absorption` |
| **DDC-TAPE-10** | Finite theorem | $\Gamma_2 > 0 \iff x_C \neq 0$; $\Phi_1 = 0 \iff x_C = 0 \land x_H = 0$. | Written proof | `test_cochain.py::test_hodge_split_is_orthogonal_and_matches_the_classes` |
| **DDC-TAPE-11** | Finite theorem | $\Phi_1$ on a finite graph is attained at a spanning-forest potential; exact over $\mathbb{Q}$. | Dual witness optimization | `test_cochain.py::test_phi1_is_gauge_invariant_and_matches_brute_force_on_small_grids`<br>`test_cochain.py::test_phi1_certificates_close_the_duality_gap_exactly` |
| **DDC-TAPE-03** | Finite theorem | Every paper-lawful step refines the deposited historical comparison specification. | `Ddc.paper_refines_engine` | `test_automaton.py::test_paper_laws_refine_the_engine_laws_on_every_step` |

---

### Part II — The Operational Letters ($\mathcal{A}_{\mathrm{DDC}}$)

| Claim ID | Epistemic Status | Formal Statement | Lean 4 Declaration | Python Test / Proof Binding |
| :--- | :--- | :--- | :--- | :--- |
| **DDC-E-01** | Finite theorem | Exact defect has potential unique up to one constant per component. | Spanning tree potential | `test_letter_modules.py::test_exact_potentials_are_unique_up_to_a_constant_per_component` |
| **DDC-E-02** | Finite theorem | Repairing with a potential of the defect leaves zero. | `Ddc.E_gauge_repair_discharges` | `test_exact_repair.py::test_exact_repair_cycle_zero_curl` |
| **DDC-E-03** | Finite theorem | Gauge moves preserve $d_1 x$ and exactness; cannot cross classes. | `Ddc.E_gauge_preserves_closure`<br>`Ddc.E_gauge_preserves_exactness` | `test_exact_repair.py::test_gauge_preserves_diagnostics` |
| **DDC-E-04** | Finite theorem | Defect not in $\operatorname{im} d_0$ is refused with `REFUSED_NON_ZERO_CURL`. | `Ddc.E_triangle_open_not_exact` | `test_exact_repair.py::test_exact_repair_refusal_non_zero_curl` |
| **DDC-E-05** | Finite theorem | Exact repair is idempotent. | `Ddc.E_repair_idempotent` | `test_exact_repair.py::test_exact_repair_idempotent` |
| **DDC-R-01** | Finite theorem | Unique three-way Hodge split into exact, co-exact, and harmonic components. | Direct sum decomposition | `test_cochain.py::test_hodge_split_is_orthogonal_and_matches_the_classes` |
| **DDC-R-02** | Finite theorem | Canonical `R` move preserves $\Gamma_2$, $\Phi_1$, and diagnostic class. | `Ddc.R_gauge_move_is_lawful`<br>`Ddc.R_keeps_diagnostics`<br>`Ddc.R_keeps_class` | `test_letter_modules.py::test_graph_projector_keeps_one_coordinate_per_independent_cycle` |
| **DDC-R-03** | Finite theorem | Exact component plus residual component equals raw defect. | Defect conservation | `test_letter_modules.py::test_projection_conserves_the_defect` |
| **DDC-R-04** | Finite theorem | Residual projection is idempotent. | Coordinate projection | `test_letter_modules.py::test_graph_projector_keeps_one_coordinate_per_independent_cycle` |
| **DDC-R-05** | Finite theorem | Terminalizing an unchanged non-exact state cannot yield `CheckPassed`. | Residual terminal seal | `test_automaton.py::test_run_tape_stops_at_the_first_unlawful_step_and_chains_receipts` |
| **DDC-R-06** | Finite theorem | Register has $b_1$ cycle coordinates, all zero iff defect is exact. | Betti number computation | `test_cochain.py::test_a_hollow_cycle_carries_a_closed_residual` |
| **DDC-C-01** | Finite theorem | Internal, boundary, and external edges partition edge set disjointly. | Set partition proof | `test_context_exposure.py::test_context_window_disjoint_partition` |
| **DDC-C-02** | Finite theorem | Internal edits leave boundary interface cochain invariant. | Boundary immobility | `test_letter_modules.py::test_exposure_is_read_only_and_internal_edits_keep_the_boundary` |
| **DDC-C-03** | Finite theorem | Agreeing exposures glue uniquely; disagreement is refused. | Sheaf gluing property | `test_letter_modules.py::test_context_exposure_glues_agreeing_windows_uniquely` |
| **DDC-C-04** | Finite theorem | Exposure is strictly read-only; never mutates ambient cochain. | Projection immobility | `test_context_exposure.py::test_exposure_is_read_only` |
| **DDC-C-05** | Finite theorem | $\partial_E(W_1 \cap W_2) \subseteq \partial_E W_1 \cup \partial_E W_2$. | `Ddc.C_boundary_of_intersection` | `test_letter_modules.py::test_boundary_of_an_intersection_lies_in_the_union_of_boundaries` |
| **DDC-C-06** | Finite theorem | Lawful `C` modifies carrier and never lowers $\Phi_1$ or $\Gamma_2$ (Law 8). | `Ddc.C_is_not_repair`<br>`Ddc.C_changes_carrier` | `test_automaton.py::test_context_exposure_cannot_lower_defect` |
| **DDC-I-01** | Finite theorem | Tape and replay receipts grow monotonically (prefix growth). | `Ddc.I_commit_prefix`<br>`Ddc.I_receipts_prefix`<br>`Ddc.receipts_prefix` | `test_automaton.py::test_replay_is_deterministic` |
| **DDC-I-02** | Model consequence | Checkpoint verification detects tail truncation, rehashed replacement, and corruption. | Preimage resistance | `test_review_regressions.py::test_tape_checkpoint_detects_rehashed_replacement_and_truncation` |
| **DDC-I-03** | Finite theorem | Replay is completely deterministic, head hash included. | Deterministic replay | `test_automaton.py::test_replay_is_deterministic`<br>`test_fsm_and_demos.py` |
| **DDC-I-04** | Finite theorem | Unlawful steps are not committed; `I` requires an explicit receipt. | `Ddc.I_needs_receipt` | `test_automaton.py::test_run_tape_stops_at_the_first_unlawful_step_and_chains_receipts` |
| **DDC-L-01** | Finite theorem | Zero-padding inclusion preserves $\ell^1$ norm and old inner products. | `Ddc.L_pad_preserves_l1` | `test_letter_modules.py::test_lift_trigger_law_and_norm_preservation` |
| **DDC-L-02** | Finite theorem | Lawful `Λ` strictly requires both an explicit licence and a Law 4 trigger. | `Ddc.L_needs_licence_and_trigger` | `test_letter_modules.py::test_lift_trigger_law_and_norm_preservation` |
| **DDC-L-03** | Finite theorem | Newly introduced coordinates are orthogonal to image of lift. | Disjoint support proof | `test_letter_modules.py::test_new_lift_coordinates_are_orthogonal_to_the_old_image` |
| **DDC-L-04** | Finite theorem | Unlicensed or untriggered lift fails closed, returning original vector. | Fail-closed security | `test_structural_lift.py::test_unlicensed_lift_refusal` |
| **DDC-TAPE-09** | Finite theorem | Commuting extension: lifted residual exact $\implies$ pre-lift residual exact. Extending lift cannot exactify non-exact residual. | `Ddc.L_cannot_exactify` | `test_letter_modules.py::test_lift_cannot_exactify_a_non_exact_residual` |
| **DDC-D-01** | Finite theorem | Loss scalar $L(x) \ge 0$. | `Ddc.loss` | `test_letter_modules.py::test_loss_is_never_negative` |
| **DDC-D-02** | Finite theorem | Descent is lossless iff dropped tail coordinates are all zero. | `Ddc.D_lossless_iff`<br>`Ddc.l1_eq_zero_iff` | `test_descent.py::test_lossless_descent_iff_dropped_zero` |
| **DDC-D-03** | Finite theorem | Projecting twice equals projecting once ($\pi \circ \pi = \pi$). | `Ddc.D_projection_idempotent` | Projection idempotent |
| **DDC-D-04** | Finite theorem | Non-zero loss never yields `LOSSLESS_DESCENT`; lawful `D` carries ledger. | `Ddc.D_needs_ledger` | `test_descent.py::test_descent_with_positive_loss`<br>`test_letter_modules.py::test_descent_books_its_ledger` |
| **DDC-M-01** | Finite theorem | Lawful `M` leaves state unchanged, names a closed reason, and transitions control to `Refused`. | `Ddc.M_preserves_state`<br>`Ddc.M_refuses` | `test_typed_refusal.py::test_refusal_preserves_state` |
| **DDC-M-02** | Definition | Ungrounded locus is an intake refusal and never enters the execution tape. | Pre-admission gate | `test_letter_modules.py::test_ungrounded_locus_is_an_intake_refusal_that_never_enters_the_tape` |
| **DDC-M-03** | Computed fixture | Missing witness produces `REFUSED_INVALID_WITNESS`. | Refusal mapping | `test_typed_refusal.py::test_refusal_invalid_witness` |
| **DDC-M-04** | Computed fixture | Cost above budget produces `REFUSED_BUDGET_EXHAUSTED`. | Budget gate | `test_typed_refusal.py::test_refusal_budget_exhausted` |
| **DDC-T-01** | Conditional theorem | Per-step charge $\ge \varepsilon > 0 \implies \le \lfloor B_0 / \varepsilon \rfloor$ charged steps. | Bounded descent | `test_letter_modules.py::test_budget_bounds_the_number_of_charged_steps` |
| **DDC-T-02** | Computed fixture | Zero residual, $\Gamma_2 = 0$, adequate detector yields `LOCAL_GREEN_FOR_SCOPE` with unlicensed authority terminal. | Simple terminal policy | `test_terminalization.py::test_terminal_local_green`<br>`test_letter_modules.py::test_terminal_evaluator_refuses_to_seal_open_or_blind_states` |
| **DDC-T-03** | Computed fixture | Non-decreasing residual over lookback window halts with `HALTED_STAGNANT_PROGRESS`. | Stagnation detector | `test_terminalization.py::test_terminal_stagnant_progress` |
| **DDC-T-04** | Finite theorem | `T` seals: control becomes `Terminalized` and admits nothing. | `Ddc.T_seals`<br>`Ddc.terminal_absorbing` | `test_automaton.py::test_terminal_absorbing` |
| **DDC-T-05** | Finite theorem | Lawful `T` keeps state, requires $\Gamma_2 = 0$, adequate detector, lands on exact or closed class. | `Ddc.T_never_seals_open`<br>`Ddc.T_routing` | `test_automaton.py::test_t_never_seals_open_obstruction` |
| **DDC-T-06** | Finite theorem | `CanContinue_n` holds iff all 9 conjuncts hold; conjuncts are strict booleans. | `Ddc.canContinue_iff` | `test_letter_modules.py::test_can_continue_is_the_conjunction_of_the_nine_named_conjuncts`<br>`test_review_regressions.py::test_explicit_continuation_facts_gate_terminal_admission` |

---

### Part III — Tape Laws & The C·R·E·D·I·T Sequence

| Claim ID | Epistemic Status | Formal Statement | Lean 4 Declaration | Python Test / Proof Binding |
| :--- | :--- | :--- | :--- | :--- |
| **DDC-TAPE-01** | Finite theorem | After refusal `M`, only letters in $\{C, \Lambda, T\}$ are admitted. | `Ddc.refusal_absorbing` | `test_automaton.py::test_terminal_and_refusal_absorption` |
| **DDC-TAPE-02** | Finite theorem | Every step of a lawful tape satisfies its letter law. | `Ddc.well_typed_step` | Trace step induction |
| **OE010-17** | Finite theorem | Only `D` or `Λ` may lower $\Phi_1$ or $\Gamma_2$ (no free decrease). | `Ddc.no_free_decrease` | `test_automaton.py::test_no_free_decrease` |
| **DDC-TAPE-04** | Finite theorem | From $\Gamma_2 > 0$, any lawful tape without `D` or `Λ` keeps $\Gamma_2 > 0$ and never terminalizes. | `Ddc.open_needs_priced_move` | `test_automaton.py::test_open_obstruction_is_never_sealed_without_a_priced_move` |
| **DDC-TAPE-05** | Finite theorem | CREDIT tape is lawful iff each of its six steps satisfies its letter law. | `Ddc.credit_lawful_iff` | Tape conjunction proof |
| **DDC-TAPE-06** | Finite theorem | A lawful CREDIT tape must start from $\Phi_1 = 0, \Gamma_2 = 0$. | `Ddc.credit_starts_exact` | `test_automaton.py::test_credit_is_lawful_only_from_an_exact_start` |
| **DDC-TAPE-07** | Finite theorem | CREDIT without a loss ledger at `D` is not lawful. | `Ddc.credit_needs_ledger` | `test_fsm_and_demos.py::test_credit_needs_an_exact_start_and_a_booked_descent` |
| **DDC-TAPE-08** | Finite theorem | CREDIT is realizable on finite complexes. | `Ddc.credit_realizable` | `demos.credit` |
| **OE010-16** | Finite theorem | Algorithmic driver never proposes `T` on open/blind states, `E` off exact, or `Λ` without a trigger. | `Ddc.driver_never_seals_open`<br>`Ddc.driver_repairs_only_exact`<br>`Ddc.driver_lift_trigger` | `test_fsm_and_demos.py::test_driver_never_seals_open_or_blind_states_and_repairs_only_exact_ones` |

---

### Part IV — Open Problems & Research Fences

| Claim ID | Epistemic Status | Formal Topic & Research Fence | Current State |
| :--- | :--- | :--- | :--- |
| **DDC-OPEN-01** | Open problem | Trace equivalence: conditions under which two distinct tapes denote identical handling. | Unproved; no equivalence assumed. |
| **DDC-OPEN-02** | Open problem | Normal forms: canonical reduction of finite tapes into standardized sequences. | Unproved; no universal normal form. |
| **DDC-OPEN-03** | Open problem | ZX-to-cochain adapter: $d_1 \circ d_0 = 0$ verification for affine colour term and exact finite shadow of phases. | Candidate adapter; unmechanized. |
| **DDC-OPEN-04** | Open problem | Finite dual certificate for coordinate vs rotation-invariant observer gauges. | Candidate model; open. |
| **OE010-11** | Open problem | Self-maintenance mode relating `C·R·Λ·I·T` to the $E_\infty$ page of a filtration spectral sequence. | Definition proposal; unmechanized. |
| **OE010-12** | Open problem | Formal representation of skill objects as surviving residual classes. | Definition proposal; open. |
| **OE010-13** | Open problem | Meta-skills as persistence invariants across families of carriers. | Definition proposal; open. |
| **OE010-14** | Open problem | Page-by-page spectral sequence account of licensed cell attachments. | Constrained by Demo 3 and Thm 5.5; open. |
| **OE010-15** | Open problem | Coloured operads of skills with loss-ledger composition. | Conceptual architecture; open. |

---

## 3. Epistemic Scope & Nonclaims

```text
The DDC claim ledger records verified finite theorems and explicit open boundaries.
No claim is promoted from a toy test or simulation into a universal mathematical theorem.
No authorization is conferred.
```
