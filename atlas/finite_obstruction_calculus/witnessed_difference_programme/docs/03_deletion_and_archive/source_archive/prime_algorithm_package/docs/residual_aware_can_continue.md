# Residual-Aware Continuation and Locus Self-Examination

**Paper:** Algorithm Prime Triad (`OE-000`) · **Document:** `docs/residual_aware_can_continue.md`  
**AuthorityEffect:** None

This document provides the canonical reconciliation of continuation conjunct counts (9 vs 3 vs 11),
specifies the quantitative potential descent bound for $\mathsf{CanContinue}_n$ (`OE003-06`),
and establishes the engine self-examination protocol (`OE004-07`, `OE004-08`).

---

## 1. Reconciliation of Continuation Conjunct Counts (9 / 3 / 11)

In the Calculus of Obstruction, Descent, and Authority (CODA) and Algorithm Prime 002, the continuation
predicate $\mathsf{CanContinue}_n$ evaluates whether execution may lawfully proceed from stage $n$ to
stage $n+1$. Different documents and prototypes in the Anomalon archive reference 3, 9, or 11 conditions.
This section settles their relationship:

### 1.1 The Nine Canonical Conjuncts (Canonical Form)

The nine conjuncts defined in the runtime contract (`oeprmalg2::CONTINUATION_CONJUNCTS`) are the canonical
form of $\mathsf{CanContinue}_n$:

1. **`has_obligation`:** A non-zero residual cochain or unresolved proof obligation exists at stage $n$.
2. **`has_witness`:** A dual witness certificate $\chi$ or replay certificate certifies the current step.
3. **`next_carrier_declared`:** The target carrier $C_{n+1}$ for the next operation is explicitly declared.
4. **`adapter_sound`:** An adapter check certifies soundness with an explicit loss ledger $L_{\text{adapter}}$.
5. **`detector_adequate`:** The observer detector $J_{n+1}$ has sufficient resolution to observe defects.
6. **`minimal_lift`:** Any dimension expansion $\Lambda$ is strictly minimal and licensed.
7. **`skeleton_preserved`:** Prior certified invariants are preserved without silent mutation.
8. **`budget_remains`:** Unallocated operational budget satisfies $B_n \ge \delta_{\text{control}} > 0$.
9. **`not_gtla_refusal`:** The system has not entered an absorbing terminal failure or GTLA refusal state.

$$\mathsf{CanContinue}_n \iff \bigwedge_{i=1}^9 C_i$$

### 1.2 The Three-Condition Form (Weakened Summary Form)

The 3-condition form is a coarse grouping or weakening used in informal exposition:
1. **Structural validity:** $C_1 \wedge C_2 \wedge C_3 \wedge C_4 \wedge C_5 \wedge C_6 \wedge C_7$.
2. **Resource availability:** $C_8$ ($B_n \ge \delta$).
3. **Absence of terminal stop:** $C_9$ ($\neg \text{Refusal}$).

The formal relationship is established by the theorem:
$$\text{Theorem (Weakening): } \mathsf{CanContinue}_9 \implies \mathsf{CanContinue}_3$$
Formalized in Lean 4: `Prime.cc9_implies_cc3`.

### 1.3 The Eleven-Condition Form (Extended Authorized Form)

The 11-condition form consists of the nine canonical conjuncts plus two separate host governance
and licensing conjuncts:
10. **`external_license_valid`:** Host execution license permits external interaction.
11. **`governance_quorum_satisfied`:** Human author or multi-agent quorum confirms continuation policy.

Under default $\mathrm{AuthorityEffect} = \mathrm{None}$, the external governance conjuncts are inert,
and the eleven-condition form reduces identically to the canonical nine.

---

## 2. Residual-Aware Continuation with Quantitative Descent (`OE003-06`)

In addition to boolean gate evaluation, residual-aware continuation requires a quantitative monotonicity
condition on the potential defect $\Phi_1$:

$$\Delta \Phi_1 = \Phi_1(s_{n+1}) - \Phi_1(s_n) \le 0$$

Continuation to stage $n+1$ is refused if an operation attempts to claim progress while inflating the
quotient residual mass. If an operation causes $\Delta \Phi_1 > 0$, it must be accompanied by an explicit
licensed structural lift $\Lambda$ or be refused as `REFUSED_INFLATIONARY_STEP`.

---

## 3. Engine Self-Examination Re-Entry Path (`OE004-07`)

Algorithm Prime 000 may recursively re-enter the engine itself:
$$\Omega_{000}(L_{\text{self}})$$
where $L_{\text{self}}$ is the engine's internal operational state, trace log, or rule table.

1. **Carrier Proposal:** Prime -1 proposes a carrier $C_{\text{self}}$ (e.g. state transition complex or dependency graph).
2. **Distinction of Locus and Carrier:** The engine state $L_{\text{self}}$ is not identical to its mathematical carrier $C_{\text{self}}$.
3. **Standard Declaration Order:** The self-examination packet must pass all 7 steps of Prime 000 declaration order without exemption.
4. **Authority Invariance:** Self-examination runs under $\mathrm{AuthorityEffect} = \mathrm{None}$. It cannot mint self-authorizing execution tokens.

---

## 4. Anti-Cheat Halting Laws for Self-Proposal & Queue Upgrade (`OE004-08`)

To prevent self-referential deadlock and priority inversion during self-examination:
1. **Law of Non-Self-Elevation:** A self-examination candidate cannot elevate its own queue priority over pending domain obligations.
2. **Law of Bounded Self-Recursion:** Self-examination re-entry is bounded to recursion depth $d \le 1$. An engine examining itself cannot spawn a second recursive self-examination of the observer.
3. **Law of Independent Witness:** The dual witness $\chi$ for a self-examination turn must be computed by an independent verifier, not asserted by the candidate itself.
