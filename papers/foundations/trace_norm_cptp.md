# 081 Trace Norm Cptp Transport Audit

## GTOC Foundations — Quantum Contact Series (qm_081_trace_norm_cptp_transport_audit)

**Date:** 2026-07-29 · **Version:** v1.0  
**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)  
**Status:** RELEASED  
**Authority:** `AuthorityEffect::None`  

## Mechanism inventory

| Slot | Value / Description |
| --- | --- |
| **Primitive Differences** | $\delta c = \text{{defect mass}}$ |
| **Carriers / Structure** | Finite Graph 0-Cochain / Hilbert Space |
| **Cochain complex** | $C^0 \to C^1 \to C^2$ |
| **Coboundary maps** | $\delta^0, \delta^1$ |
| **ZeroRel** | Preserved under $L_1$ quotient |
| **Licensed repairs** | None |
| **Quotient / Q1** | Banach Quotient |
| **Residuals** | $\delta c \neq 0$ boundary defect |
| **Witnesses** | Replayable Python / Rust Certifiers |
| **Observers / profiles** | Operational Observer |
| **Anomalons** | None |
| **CompletionLaw** | Finite Cochain Completion |
| **Terminal / route** | Route to 003 Quantum Foundations |
| **AuthorityEffect** | None |

QM_081 — CPTP Monotonicity Does Not Select Trace Distance
=========================================================

**A trace-norm transport audit under declared quantum-interface imports**

**Date:** June 6, 2026
**Version:** v0.1.0 Pre-Print
**Status:** Conditional selector audit under declared imports (O025)
**Series numbering:** this paper is **QM_081** in the current repo; "O025" is its legacy series label (it follows O024 = `QM_101` and the O025a KCS pentagon). Both labels denote this paper; cross-references below use the legacy O-labels where the sibling papers do.
**Lean backing:** `QM.TraceNonSelect` (LT-L, §3 non-selection — Mathlib-free) and `QM.StochasticL1` (LT-M, §5.1 classical ℓ¹-contraction shadow — `import Mathlib`). Both `Lean replay QM`-checked (2026-06-14); axioms standard (`propext`, `Classical.choice`, `Quot.sound`; LT-L's `scale_monotone` axiom-free); no authority minted.
**Mechanization:** MECHANIZED (ENC-0226: `lean4/research_programs/003_quantum_foundations/003_qm_stochastic_channel.lean`, `lean4/shared_kernel/primitive_difference.lean`)

1. Abstract and Claim Discipline


**Monotonicity under quantum channels (CPTP maps) is *necessary but not sufficient* to single out the trace distance as the distinguishability metric of a quantum interface.** This document makes that non-selection precise and machine-checks it as a finite counterexample (a CPTP-monotone functional and its rescaling are both monotone and distinct), while separately confirming — only once state-discrimination axioms are *imported* — that trace distance is contractive under CPTP maps. It executes the next step in the Quantum Transport series (following the O025a Kraus–Choi–Stinespring pentagon and the O024 Born-Compatible Pairing Audit), auditing whether the half-trace norm is preserved under CPTP maps when the space is equipped with a declared quantum interface.

**Why a researcher should care.** In quantum information the trace distance $D(\rho,\sigma)=\tfrac12\|\rho-\sigma\|_1$ is routinely treated as *the* canonical operational metric because it contracts under every CPTP map (the data-processing inequality). This audit shows that CPTP-monotonicity *alone* underdetermines the metric: a whole family of distinguishability measures (relative entropies, fidelity-derived quantities, monotone Riemannian metrics, and any positive rescaling of a monotone) contracts under CPTP maps, so the trace norm's operational primacy rides on an *imported* single-shot state-discrimination axiom, not on the CPTP structure itself. Anyone arguing that channel dynamics "force" a particular metric — in QIT, in resource theories, or in foundational derivations of the Born rule — needs to know exactly which extra axiom is doing the selecting.

**Strict Non-Claims** *(this is the "What this does NOT claim" fence):*

1. This is **not** a derivation of the Born rule or CPTP dynamics. `[SCOPE FENCE]`
2. This is **not** a claim that trace distance is the unique metric for operational distinguishability. `[SCOPE FENCE]`
3. This is **not** a physical assertion about channel authority. `[SCOPE FENCE]`

GTLA's model-facing finite-descent layer checks evidence and terminal policy; it is not an origin theory or an authority-minting mechanism. All structures are audited as interfaces against finite replay requirements. A checked CODA-FDA-Q `Pi_sharp` receipt remains non-authoritative; any bounded promotion requires a separate external authenticated human decision.

### 1.1 Related work and positioning

The nearest neighbors, and how this audit differs:

* **Trace distance and contractivity (data-processing).** Nielsen & Chuang, *Quantum Computation and Quantum Information* (Ch. 9) `[STANDARD]` and Wilde, *Quantum Information Theory* `[STANDARD]` establish that $D(\rho,\sigma)$ is non-increasing under CPTP maps. We *import* this as §5 rather than re-derive it, and isolate the separate question of *uniqueness*.
* **Contractivity of the trace norm under stochastic/CP maps.** That the trace norm contracts under CP/stochastic maps is classical and underlies the §5 bound (Nielsen & Chuang Ch. 9) `[STANDARD]`.
* **CPTP-monotone distinguishability functionals.** Many CPTP-monotone distinguishability functionals exist, including divergences, fidelity-derived quantities, monotone Riemannian metrics, and scalar rescalings. They do not all satisfy the same norm or metric axioms; the structural classification of monotone metrics (Petz; Morozova–Chentsov) `[STANDARD]` is the reason the non-selection firewall (§3) reflects structure rather than a contingent gap. Note §3 is mechanized via scaling and does **not** itself depend on this classification.
* **Sheaf-theoretic contextuality.** Abramsky–Brandenburger `[STANDARD]` — a neighboring "what is forced by structure vs. imported" program at the level of empirical models, contrasted here at the level of metric selection.
* **Series companions.** O024 Born-pairing audit (`qm_101_state_effect_pairing_audit`) and the O025a KCS transport pentagon; the realization-spine firewall in `qm_030_gtq_quantum_realization_spine` §4.7, of which §3 below is the finite, mechanized instance.

### Exact References

* Nielsen, M. A., & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*. (Trace norm contractivity under CPTP)
* Wilde, M. M. (2013). *Quantum Information Theory*. (Data processing inequality)
* Helstrom, C. W. (1969). Quantum detection and estimation theory. (Optimal binary state discrimination)
* Holevo, A. S. (1973). Statistical decision theory for quantum systems.
* Petz, D. (1996). Monotone metrics on matrix spaces. (Classification of monotone metrics)
* Morozova, E. A., & Chentsov, N. N. (1990). Markov invariant geometry on state manifolds.

### 1.2 Notation pointer

$\|X\|_1$ = operator trace norm (sum of singular values); $M_n(\mathbb{C})$ = $n\times n$ complex matrices; CPTP = completely positive, trace-preserving; $D(\rho,\sigma)=\tfrac12\|\rho-\sigma\|_1$ = trace distance. Tower symbols ($Q^1$, $\Phi_1$, $\kappa^1$) are **not** used in this audit; for them see the canonical definitions in `qm_030_gtq_quantum_realization_spine`.

Status Overview

| Claim | Status |
|---|---|
| **CPTP trace-norm contraction on $M_n(\mathbb{C})$** | `[STANDARD]` / imported |
| **Column-stochastic $\ell^1$ contraction** | `[MECHANIZED]` finite classical shadow |
| **CPTP monotonicity non-selection** | `[MECHANIZED]` abstract scalar-family firewall |
| **Trace-distance operational selection** | `[STANDARD]` / conditional on Helstrom-style discrimination axiom |

2. Premise Separation: Four Declared Imports


To audit trace-norm transport, we explicitly separate the imported formal structure from the resulting operational metric. The audit depends on four specific declarations. *Each is a `[DEFINITION]` / `[SCOPE FENCE]`, not a theorem — they are the imported interface, and the audit's conclusions are conditional on them.*

1. **Quantum Interface:** The carrier is explicitly declared as $M_n(\mathbb{C})$ with Hermitian density operators (Trace = 1, PSD). `[DEFINITION]`
2. **Binary single-shot discrimination axiom:** The distinguishability functional must reproduce optimal binary state-discrimination advantage (Helstrom operational axiom). `[DEFINITION]`
3. **CPTP Compatibility:** The operational dynamics are declared as Completely Positive Trace-Preserving (CPTP) maps over the quantum interface. `[DEFINITION]`
4. **Edge Additivity:** Orthogonal states under the pairing sum additively in the distinguishing metric. `[DEFINITION]`

3. Metric Non-Selection Firewall


As established in the `qm_030_gtq_quantum_realization_spine` §4.7 firewall, monotonic preservation under CPTP maps **does not uniquely select** the trace norm.

**Firewall Theorem (non-selection).** `[PROVEN]` *(Lean: `QM.cptp_monotone_not_select`, `QM.cptp_monotone_not_select_traceNorm`, abstract finite monotone-functional model; encyclopedia [[ENC-0247]] "CPTP Monotonicity Is Necessary but Not Sufficient", `lean_status` MECHANIZED-PARTIAL)*
$$ \mathsf{CPTPMonotone}(j) \not\Longrightarrow j(X) = \frac{1}{2}\|X\|_1 $$

*Mechanized proof (scalar-family counterexample).* Model a distinguishability functional on a finite difference space as $j:V\to\mathbb{N}$, and call it **CPTP-monotone** relative to a declared family of data-processing contractions $\{T\}$ when $j(Tx)\le j(x)$ for every declared $T$. The key fact, mechanized in `QM.scale_monotone`, is that **scaling preserves monotonicity**: if $j$ is CPTP-monotone then so is $c\cdot j$ for every constant $c$. Hence from any CPTP-monotone $j$ that is nonzero somewhere, $j$ and $2\cdot j$ are two *distinct* CPTP-monotone functionals (`QM.cptp_monotone_not_select`), so CPTP-monotonicity underdetermines the distinguishability functional (and while scaling changes the normalization, other distinct normalized monotone functionals exist as noted in Section 1.1) — in particular it does not single out the trace-norm shadow without additional operational axioms (`QM.cptp_monotone_not_select_traceNorm`). This is exactly the 005 Theorem 2(ii) scalar-family counterexample, now axiom-free in the non-selection direction.

*Scope of the mechanization.* The Lean model establishes the **non-selection direction** abstractly (it exhibits two distinct monotone functionals); it does **not** mechanize the full analytic claim that infinitely many *unitarily invariant norms / relative entropies* are CPTP-monotone — that broader statement remains `[STANDARD]` (Morozova–Chentsov / Petz, §1.1). Selecting the trace norm requires importing the operational requirement that maximal trace-distance corresponds to optimal single-shot state discrimination; monotonicity is necessary, not sufficient.

4. Trace-Norm Conditional Admission


Given finite quantum states, effects/measurements, and the operational binary-discrimination axiom (§2), the Helstrom expression selects half trace norm: `[STANDARD, CONDITIONAL]` *(the Holevo–Helstrom single-shot discrimination fact, conditional on imports H1–H4 of §2; an admission of a standard result, not a new derivation; the conditional spectral selection theorem is encyclopedia [[ENC-0246]] "Conditional Trace-Distance Selection")*
$$ D(\rho, \sigma) = \frac{1}{2}\|\rho - \sigma\|_1 $$

This admission is strictly conditioned on the explicitly imported state-discrimination axioms. It is **not** derived from first principles or from the CPTP property alone (that is exactly what §3 forbids).

### 4.1 Worked example (reproducible)

`[WORKED EXAMPLE]` Take the qubit interface $M_2(\mathbb{C})$ and the two orthogonal pure states $\rho=\operatorname{diag}(1,0)$, $\sigma=\operatorname{diag}(0,1)$. Then $\rho-\sigma=\operatorname{diag}(1,-1)$, so $\|\rho-\sigma\|_1=|1|+|-1|=2$ and the trace distance is $D(\rho,\sigma)=\tfrac12\cdot 2=1$ (the maximal value, as expected for orthogonal states).

Now compare two functionals on this difference: the trace-norm shadow $j(X)=\tfrac12\|X\|_1$ gives $j(\rho-\sigma)=1$, while the rescaling $2j$ gives $2$. **Both are CPTP-monotone** (monotonicity is scale-invariant, `QM.scale_monotone`), yet they are distinct — so CPTP-monotonicity alone cannot select between them. This instantiates `QM.cptp_monotone_not_select` with $x_0=\rho-\sigma$, $j(x_0)=1\neq 0$.

The mechanized seal uses a *genuine* non-increasing contraction so the counterexample is not vacuous: over $\mathbb{N}$ the halving step $x\mapsto x/2$ is non-increasing (`QM.id_cptpMonotone_halving`), and under it both $\mathrm{id}$ and $2\cdot\mathrm{id}$ are CPTP-monotone and distinct.

5. Trace-Norm CPTP Transport Audit


Following the **QM_101** state–effect pairing non-selection audit (which establishes that compatibility alone does not select Born), the O025a Kraus–Choi–Stinespring (KCS) transport pentagon proved the equivalence of finite representation structures for quantum channels without selecting a metric. We now extend this to audit trace-norm transport.

**Audit Target.** For any declared CPTP map $\Phi$ (represented equivalently as Kraus operators, Choi matrix, or Stinespring dilation) and any two density states $\rho, \sigma$:
$$ \|\Phi(\rho) - \Phi(\sigma)\|_1 \le \|\rho - \sigma\|_1 $$

**Result.** `[STANDARD]` *(operator trace-norm contractivity under CPTP = data-processing inequality; Nielsen & Chuang Ch. 9, Wilde — imported, not a new transport theorem)* The trace norm is non-increasing under any declared CPTP map. This is the standard data-processing inequality; the audit *imports* it (it is not derived here), and the finite mechanized evidence in this paper is its **classical ℓ¹ shadow** (§5.1, LT-M). The operator-level trace-norm contractivity on $M_n(\mathbb{C})$ is the proposed Lean-hardening target PL-O025-1 (not yet mechanized); it is not honesty-gating, since §5 is imported `[STANDARD]` and the paper's own proven content is the §3 non-selection firewall.

### 5.1 Finite ℓ¹ contraction shadow (mechanized precursor)

`[PROVEN]` *(Lean: `QM.stochastic_l1_contraction`, over $\mathbb{Q}$; encyclopedia [[ENC-1055]] "Column-Stochastic ℓ¹ Contraction", `lean_status` MECHANIZED)* The division-algebra-free precursor of the §5 bound is mechanized: a finite **column-stochastic** kernel $S$ (nonnegative entries, every column summing to $1$) does not increase the ℓ¹ norm, $\|Sx\|_1\le\|x\|_1$. This is the contractivity *shape* that the quantum data-processing inequality specialises; it selects no metric and (with §3) confirms that contractivity/CPTP-monotonicity alone does not pin the trace norm.

*Worked number.* `[WORKED EXAMPLE]` Take $S=\begin{pmatrix}1/2&1/2\\1/2&1/2\end{pmatrix}$ (column-stochastic) and $x=(1,-1)$. Then $Sx=(0,0)$, so $\|Sx\|_1=0\le 2=\|x\|_1$ — contraction, here strict.

### 5.2 Falsifiability

**This audit fails if** (i) a proof shows the structural declared imports of Section 2 (excluding the Trace-Distance Axioms of Import 2) *together with* CPTP-monotonicity uniquely fix $j(X)=\tfrac12\|X\|_1$ (i.e. no other CPTP-monotone functional is consistent with those structural imports), **or** (ii) the mechanized counterexample `QM.cptp_monotone_not_select` is shown unsound, **or** (iii) a CPTP map $\Phi$ and states $\rho,\sigma$ are exhibited with $\|\Phi(\rho)-\Phi(\sigma)\|_1 > \|\rho-\sigma\|_1$.

6. Handoff (O026 = the open multi-interface census, not a paper)


With the trace-norm and CPTP transport audited under declared imports (O025), the sequence moves to the multi-interface census (O026). The next proof obligation must declare the admitted proper sub-interface registry and replay the failure of each weaker interface against the certified finite transport. (A finite multi-interface census prototype is replayed in the O026 audit — see the survival-interface companion `qm_081_quantum_realization_requires_finite_descent`, which absorbed the retired QM_070; QM_061 was archived to `qm_archived_stubs_022_026`.)

7. Claim Ledger (this paper)


The full per-claim ledger (status + support-ledger upgrade paths + encyclopedia foundation) lives in the companion file `qm_081_trace_norm_cptp_transport_audit Claim Ledger`. The quick index below is retained in-paper for convenience.

| # | Claim | Type | Where / evidence |
|---|-------|------|------------------|
| C1 | CPTP-monotonicity does not select the trace norm | `[PROVEN]` | §3; Lean `QM.cptp_monotone_not_select(_traceNorm)`, `QM.scale_monotone`; ENC-0247 |
| C2 | Genuine non-increasing contraction makes the counterexample non-vacuous | `[PROVEN]` | §4.1; Lean `QM.id_cptpMonotone_halving`; ENC-0247 |
| C3 | Half-trace-norm is the admitted operational metric under imports H1–H4 | `[STANDARD, CONDITIONAL]` | §4; Holevo–Helstrom, conditional on §2; ENC-0246 |
| C4 | Trace norm contracts under CPTP maps (data-processing) | `[STANDARD]` | §5; Nielsen–Chuang, Wilde |
| C5 | Column-stochastic kernels contract the ℓ¹ norm (finite shadow of C4) | `[PROVEN]` | §5.1; Lean `QM.stochastic_l1_contraction`; ENC-1055 |
| C6 | Many CPTP-monotone metrics exist, not just trace norm (basis of C1) | `[STANDARD]` | §1.1, §3; Petz / Morozova–Chentsov |

Changelog

Version Note: v1.0-audit (2026-06-21)** — hygiene-pipeline pass.

<!-- claim-id-body-index:begin -->

Claim-ID body index (packaging)

| ID | Home |
|---|---|
| `QM-081-C1` | sibling `qm_081_trace_norm_cptp_transport_audit_claim_ledger.md` |
| `QM-081-C2` | sibling `qm_081_trace_norm_cptp_transport_audit_claim_ledger.md` |
| `QM-081-C3` | sibling `qm_081_trace_norm_cptp_transport_audit_claim_ledger.md` |
| `QM-081-C4` | sibling `qm_081_trace_norm_cptp_transport_audit_claim_ledger.md` |
| `QM-081-C5` | sibling `qm_081_trace_norm_cptp_transport_audit_claim_ledger.md` |
| `QM-081-C6` | sibling `qm_081_trace_norm_cptp_transport_audit_claim_ledger.md` |
| `QM-091-D1` | sibling `qm_081_trace_norm_cptp_transport_audit_claim_ledger.md` |
| `QM-091-N1` | sibling `qm_081_trace_norm_cptp_transport_audit_claim_ledger.md` |
| `QM-091-N2` | sibling `qm_081_trace_norm_cptp_transport_audit_claim_ledger.md` |
| `ENC` | sibling `qm_081_trace_norm_cptp_transport_audit_claim_ledger.md` |
| `ENC-0247` | sibling `qm_081_trace_norm_cptp_transport_audit_claim_ledger.md` |
| `ENC-0246` | sibling `qm_081_trace_norm_cptp_transport_audit_claim_ledger.md` |
| `ENC-1055` | sibling `qm_081_trace_norm_cptp_transport_audit_claim_ledger.md` |

<!-- claim-id-body-index:end -->
