---
documentation_contract: symbol-game-documentation/v1
title: "11. The Three Prime Algorithms: Protocol Stages, Halting Laws & Carrier Honesty"
kind: mathematical-reference
audience:
  - engineers
  - researchers
  - coding-agents
status: active
maturity: production
claim_status: source-grounded
authority_effect: "None"
source_paths:
  - omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/source_archive/prime_algorithm_package/oe_prime_algorithms.md
  - omega_engine_education/documentation/13_three_prime_algos/levels/
  - omega_engine/crates_rs/omega_wdp/src/prime_algos/prime_algorithm_0.rs
  - omega_engine/crates_rs/omega_wdp/src/prime_algos/prime_algorithm_1.rs
  - omega_engine/crates_rs/omega_wdp/src/prime_algos/prime_algorithm_2.rs
  - omega_engine/crates_rs/omega_wdp/src/prime_algos/descent_engine.rs
  - omega_engine/crates_rs/omega_wdp/src/prime_algos/prime_scope.rs
  - omega_engine/crates_rs/omega_wdp/src/prime_algos/licensed_lift_gate.rs
  - omega_engine/crates_rs/omega_types/src/prime.rs
last_verified: 2026-10-01
---

# 11. The Three Prime Algorithms: Protocol Stages, Halting Laws & Carrier Honesty

**AuthorityEffect:** None.

This document serves as the canonical navigational entry point and formal specification for the **Algorithm Prime Triad** (Prime -1, Prime 000, Prime 001, Prime 002), the 7-step local runtime declaration order, the six anti-cheat halting laws, and primitive difference honesty.

For the sequential educational curriculum, see the [**Levels Guide**](../../levels/prime/README.md).

---

## 1. Executive Architecture: Protocol Stages vs. Pure Types

A fundamental architectural invariant governs the Prime Algorithms:

> **Protocol Stages vs Domain Types:**
>
> 1. "Prime 000" and its sister stages are **protocol stages**, NOT domain data types.
> 2. All noun-shaped, immutable data structures (`CandidatePacket`, `DeclarationPacket`, `AdmissionDecision`, `AdapterStatus`, `LossEntry`, `LossLedger`, `AdapterCheck`, `AntiCheatFlags`, `CanContinueInput`, `CanContinueResult`, `IntakeTraceRecord`) live in domain crates (`omega_types::prime`, `omega_types::causal_trace`).
> 3. Behavioral operations (`propose_candidate`, `admit_declaration`, `check_adapter`, `can_continue`, `IntakeTrace`, `PrimeDescentCoordinator`) live under the dedicated runtime crate [`omega_prime_algos`](../../../../../omega_engine/crates_rs/omega_wdp/src/prime_algos/) (with bridge adapters in `omega_discrete_deformation_calculus` and `omega_symbol_game::prime`).

### The Prime Triad Sequence:

1. **Prime -1: Candidate Proposal Engine (`OE001-01`):**
   - Ingests raw external proposals and emits strongly-typed `CandidatePacket` objects.
   - Pre-admission refusals are committed exclusively to an `IntakeTrace` (`enters_dda_trace: false`), preventing unadmitted candidate carrier hypotheses from contaminating the operational execution trace.
2. **Prime 000: 7-Step Local Runtime Declaration Order (`OE001-02`):**
   - Governs the sequential admission of primitive differences onto declared carriers.
   - Emits strictly scoped status $\mathsf{LOCAL\_GREEN\_FOR\_SCOPE}$, never an unscoped global green (`OE001-04`).
3. **Prime 001: Dual Boundary Placement & Sound Adapter Invariants (`OE002-01`, `OE002-02`):**
   - Stands guard at two boundary points:
     - **Intake Adapter Check:** Validates external inputs before Prime 000 admission.
     - **Transport Adapter Check:** Validates transitions whenever a DDA step shifts between distinct carriers.
   - Requires explicit loss ledgers $L_{\text{adapter}}$ whenever information is dropped.
4. **Prime 002: Master Continuation Predicate $\mathsf{CanContinue}_n$ (`OE003-01`):**
   - Evaluates whether higher-order ascent $C^n \to C^{n+1}$ is lawful under the six anti-cheat halting laws.

---

## 2. Prime 000: The 7-Step Local Runtime Declaration Order

Every admitted packet must execute the exact 7-step declaration sequence without reordering or step omissions:

$$0.\ \text{Source Locus / Grounding Hash} \longrightarrow 1.\ \text{Candidate Carrier } C^0 \longrightarrow 2.\ \text{Observer Probe } J_L \longrightarrow 3.\ \text{Admitted Primitive Difference } \omega \in C^1 \longrightarrow 4.\ \text{ZeroRel } \Delta(s)=0 \longrightarrow 5.\ \text{Witness / Refusal } \chi \longrightarrow 6.\ \text{Quotient / Lift Policy}$$

### Declaration Steps Breakdown:

| Step | Formal Name | Operational Obligation |
| :---: | :--- | :--- |
| **0** | **Source Locus** | Binds grounding SHA-256 hash and context identifier. Enforces non-conflation of locus and carrier ($L \neq C_L$). |
| **1** | **Candidate Carrier ($C^0$)** | Declares the discrete base point set and topology. |
| **2** | **Observer Probe ($J_L$)** | Binds explicit, finite measurement probes; forbids cosmic unindexed observers. |
| **3** | **Primitive Difference ($\omega \in C^1$)** | Admits witnessed differences satisfying strict irreflexivity ($a \neq b$). |
| **4** | **ZeroRel ($\Delta(s) = 0$)** | Declares the gauge equivalence kernel and null relation. |
| **5** | **Witness / Refusal ($\chi$)** | Emits deterministic dual witness certificate or typed refusal code. |
| **6** | **Quotient / Lift Policy** | Defines projection to cohomology quotient or sets lift boundary $\Lambda$. |

---

## 3. Prime 001: Adapter Soundness & Loss Ledgers

An adapter $\alpha: C_{\text{source}} \to C_{\text{target}}$ transitions data between differing carriers. An adapter is sound if and only if:

1. **Operation Preservation:** Commutes with declared differentials ($d_{\text{target}} \circ \alpha = \alpha \circ d_{\text{source}}$).
2. **Witness Preservation:** Dual certificates in the source remain valid or are deterministically mapped.
3. **Loss Accounting:** All dropped coordinates, forgotten phases, or collapsed dimensions are recorded in an explicit `LossLedger`:
   $$L_{\text{adapter}} = \{(\text{dim}, \text{dropped\_basis}, \text{norm\_loss})\}$$
4. **Promotion Freeze:** If $L_{\text{adapter}} \neq \varnothing$, the adapter emits `ADAPTER_DEBT` and halts automatic promotion. Smuggling mathematical structures without explicit adapters is strictly forbidden (`HANDOFF-002`).

---

## 4. Prime 002: Master Continuation Predicate & Anti-Cheat Laws

Continuation from stage $n$ to $n+1$ is lawful if and only if $\mathsf{CanContinue}_n$ evaluates to `True`:

$$\mathsf{CanContinue}_n :\iff \mathsf{OutstandingObligation} \wedge \mathsf{HigherObligationWitness} \wedge \mathsf{NextCarrierDeclared} \wedge \mathsf{AdapterSound} \wedge \mathsf{DetectorAdequate} \wedge \mathsf{MinimalLicensedLift} \wedge \mathsf{SkeletonPreserved} \wedge \mathsf{BudgetAvailable} \wedge \neg\mathsf{GTLARefusal}$$

### The Six Anti-Cheat Halting Laws:

1. **Law 1 (No Degree Laundering):** Adding higher degree complex $C^{n+1}$ requires an exhibited, unresolved $(n+1)$-dimensional obligation on $C^n$.
2. **Law 2 (No Lift Laundering):** Extending carrier representation requires proving that no same-carrier repair exists ($\Phi_1 > 0, \Gamma_2 = 0$).
3. **Law 3 (No Anomalon Evasion):** Stable residuals cannot be renamed, repacketized, or retried to evade terminalization.
4. **Law 4 (Old-Skeleton Preservation):** Higher-order continuation must preserve certified lower-degree data or emit an audited loss ledger.
5. **Law 5 (Detector Revalidation):** Repacketization must revalidate detector adequacy at degree $n+1$.
6. **Law 6 (First-Unresolved-Degree Honesty):** If $n_0$ is unresolved, all claims above $n_0$ are strictly conditional.

Under finite budget $B_{\text{tot}} < \infty$ and cost floor $\delta_{\text{control}} > 0$, total operations are strictly bounded:
$$\#\mathrm{ops} \le \lfloor B_{\text{tot}} / \delta_{\text{control}} \rfloor$$

---

## 5. Primitive Difference Honesty & Anti-Bias Discipline

All difference primitives must adhere to foundational honesty:

1. **Genesis-Bias Rejection:** Difference must not presuppose antecedent objects. The cut admits non-sameness directly; treating "two things differ" as an unexamined background fact is rejected.
2. **Strict Irreflexivity:** Difference forces metatheoretic inequality ($a \neq b$), forbidding 1-point self-loops (`r () ()`).
3. **No View From Nowhere:** All quantifiers must be explicitly indexed by carrier, packet, or context. Observers are finite report maps, never unindexed cosmic spectators.
4. **Autonomous Difference:** Difference representations across Rust crates and Python engines operate under Discrete Deformation Calculus (DDC) and exact simplicial cochains ($\Phi_1, \Gamma_2$).

---

## 6. The 8-Level Educational Curriculum

The Algorithm Prime Triad is broken down into eight sequential educational levels:

| Level | Document | Key Topic & Scope |
| :---: | :--- | :--- |
| [**Level 00**](../../levels/prime/level_00_prime_triad_architecture.md) | **Prime Triad Architecture** | Protocol stages vs pure domain data types; Clean Architecture separation. |
| [**Level 01**](../../levels/prime/level_01_prime_minus_one_candidate_proposal.md) | **Prime -1: Candidate Proposal** | `CandidatePacket`, `IntakeTrace` (`enters_dda_trace: false`), and intake compilation. |
| [**Level 02**](../../levels/prime/level_02_prime_000_seven_step_declaration.md) | **Prime 000: 7-Step Declaration** | Strict declaration order (Grounding to Quotient), $L \neq C_L$, and `LensSpan` model. |
| [**Level 03**](../../levels/prime/level_03_prime_000_twelve_step_fill_execution.md) | **Prime 000: 12-Step Fill Order** | Cochain packet fill, $(\Phi_1, \Gamma_2)$ measurement, `PrimeAlgorithm0Receipt`, and scoped green. |
| [**Level 04**](../../levels/prime/level_04_prime_001_intake_transport_soundness.md) | **Prime 001: Transport Soundness** | Dual boundary checks, "Translation does not confer validity", and sealed `LossLedger`. |
| [**Level 05**](../../levels/prime/level_05_prime_002_continuation_and_can_continue.md) | **Prime 002: Master Continuation** | The 9-conjunct master predicate $\mathsf{CanContinue}_n$, single-use `StepPermit`, and $\Delta \Phi \le 0$. |
| [**Level 06**](../../levels/prime/level_06_prime_002_six_anti_cheat_halting_laws.md) | **Prime 002: Anti-Cheat Laws** | The six halting laws, bounded stopping $\#\mathrm{ops} \le \lfloor B_{\mathrm{tot}} / \delta_{\mathrm{control}} \rfloor$, and `TerminalPermit`. |
| [**Level 07**](../../levels/prime/level_07_coda_cn_ascent_and_recursive_reentry.md) | **CODA $C^n$ Ascent & Re-Entry** | Recursive re-entry $\Omega_{000}(L)$, lawful $C^n$ ascent, defect linearity, and sovereign non-authority. |

For detailed navigational charts and state machine diagrams, consult the [**Levels README**](../../levels/prime/README.md).

---

## 7. Claim Hygiene Quadrant

1. **What this supports:**
   - Formal specification of the Algorithm Prime Triad protocol stages (Prime -1, 000, 001, 002).
   - Machine-checkable halting bounds through the six anti-cheat laws.
   - Exact 7-step local runtime declaration order and loss-ledger adapter contracts.
2. **What this does not support:**
   - Does not establish unmechanized physical claims or assert that finite models solve continuum conjectures.
   - Does not license global promotion from local scoped status.
3. **The narrowest defensible claim:**
   - The Prime Triad enforces finite, bounded, and audited continuation across discrete carrier complexes under `AuthorityEffect: None`.
4. **Next test needed:**
   - Run the dedicated Rust crate tests: `cargo test --manifest-path omega_engine/crates_rs/omega_wdp/src/prime_algos/Cargo.toml`.
   - Run the Prime Algorithms Python test suite via `py -3.12 -m pytest omega_engine_operations/tests/research_workbench/test_runner.py`.


## Curriculum Tracks & Interactive Laboratories

- [**Curriculum Master Index**](../../curriculum/prime_reading_route.md): Interactive laboratory notebooks, concept lessons, narration scripts, and media assets.
