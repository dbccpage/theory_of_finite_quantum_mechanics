Claim Ledger — GS-003: Vector and Quantum Observer Geometries
=============================================================

**Paper Key:** `projection_obstruction/vector_and_quantum_observer_geometries`  
**Paper Identity:** `GS-003` (`vector_and_quantum_observer_geometries.md`, canonical version: `v0.4`)  
**Authority:** None.

This ledger catalogs every claim in `GS-003` with its type, governing hypotheses, proof location, mechanization status, and open obligations.

---

1. Claim-by-Claim Matrix

---

| ID | Claim | Type | Hypotheses | Proof / support | Mechanization | Open obligation |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | Quotient obstruction class is fixed relative to repair quotient; magnitude is observer-gauge-relative. | PROVEN, CONDITIONAL | Declared observer gauge | Abstract, Architectural Lesson | Structural | None |
| A2 | Vector branch: $\ell^2$ stalk gauge selected by $SO(k)$ symmetry. | IMPORTED | Paper GS-002 Theorem 3.1 | Paper GS-002 §3.2 | Imported | None |
| A3 | Quantum branch: trace-distance gauge is conditionally selected by Helstrom discrimination; not selected by CPTP monotonicity alone. | DEFINITION | Declared quantum observer geometry | Positioning, Model II §2 | Defined | None |
| A4 | Operational selection of trace-distance gauge: $j(X) = \frac{1}{2}\|X\|_1$ uniquely selected on Hermitian trace-zero operators. | PROVEN, CONDITIONAL | Unitary invariance + classical total-variation reduction / Helstrom binary discrimination | Model II §2.2, Technical Appendix; ENC-0246 | Prose-proved (ENC-0246) | None (PL-000BN-1 discharged conditionally) |
| B1 | Cycle circulation $c=(1,1)$ preserved modulo repair ($\sum_{\text{cycle}}(\omega-d_0\alpha)=c$). | STANDARD | $d_0\alpha$ telescopes to 0 on cycle | §1 | Standard | None |
| B2 | Single-cycle fixture quotient norm $\Phi_J([\omega]) = j(c)$. | PROVEN | Single-cycle, equal-weight | Analytic Proof | Single-cycle kernel | None |
| B3 | Finite triangle separation: $\Phi_{1,1}=2$ vs $\Phi_{2,1}=\sqrt{2}$. | PROVEN, NUMERICAL | Closed form + Python replay | §5 | Replay receipt / `L003_01` | None |
| B4 | Mixed vector obstruction duality $\Phi_{2,1}([\omega]) = \max_\varphi \sum_e \langle \varphi_e, \omega_e \rangle$. | PROVEN | Finite-dim Fenchel & Hahn–Banach separation duality | Generalization section | MECHANIZED (`mixed_vector_duality` & `strong_vector_duality`: `weak_vector_duality_pointwise`, `weak_vector_duality_quotient`, `duality_gap_zero_certificate`, `subgradient_attainment`, `dual_witness_is_maximizer`, `strong_duality_minimax_identity`, `complementary_slackness_edge_alignment`, `strong_vector_duality_of_stationary_subgradient`, `hahn_banach_separation_existence`) | None |
| B5 | Mixed closure bound $\Gamma_2([h]) \le \|d_1\| \Phi_{2,1}([h])$. | PROVEN, CONDITIONAL | Declared 2-cell $d_1$, $d_1 d_0 = 0$ | Generalization section | `mixed_closure_bound` | None |
| C1 | Model II quantum carrier & trace-distance gauge $\frac{1}{2}\|\cdot\|_1$. | DEFINITION | Quantum state/channel framework | Model II, §§1-6 | Defined | None |
| C2 | Trace distance CPTP contractivity & Helstrom dual representation $\frac{1}{2}\|X\|_1 = \max_{0 \le E \le I} \mathrm{Tr}(EX)$. | STANDARD | Standard quantum information | Model II, §5 | Standard | None |
| C3 | Marginal triangle telescopes: $\Phi_Q = 0$. | PROVEN, DIRECT | Direct state evaluation | Model II, §7 | Direct | None |
| C4 | Non-telescoping quantum signal $\Phi_Q = 3/2$. | PROVEN, NUMERICAL | Single-cycle equal weight | Model II, §7 | Direct | None |
| C5 | Quantum dual witness $\varphi_e = \frac{1}{2}\mathrm{sign}(A)$ attains bound. | PROVEN, DIRECT | Divergence-free witness | Model II, §8 | Direct / Mechanized (`quantum_trace_duality`: `single_cycle_qubit_fixture_exact`) | None |
| C6 | Quantum trace-norm obstruction duality $\Phi_Q([\delta]) = \max_\varphi \sum_e \mathrm{Tr}(\varphi_e \delta_e)$. | PROVEN | Helstrom binary POVM decision observables + Schatten trace-norm subgradient alignment | Technical Appendix | MECHANIZED (`quantum_trace_duality`: `helstromStalkObservable_specNorm_le`, `helstromStalkObservable_inner_eq`, `helstrom_slack_nonneg`, `canonicalHelstromCochain_bounded`, `canonicalHelstromCochain_pairing_eq`, `dualPairing_Q_sub`, `dualPairing_Q_repair_invariance`, `weak_quantum_duality_pointwise`, `weak_quantum_duality_quotient`, `helstrom_attainment`, `quantum_dual_witness_is_maximizer`, `quantum_strong_duality_minimax_identity`, `quantum_complementary_slackness`, `strong_quantum_duality_of_stationary_helstrom`, `single_cycle_qubit_fixture_exact`) | None |
| C7 | CPTP raw monotonicity $J_Q(\Lambda \delta) \le J_Q(\delta)$. | PROVEN | CPTP contractivity on traceless Hermitian differences | Model II, §2.3, Technical Appendix | Prose-proved | None |
| C8 | CPTP quotient monotonicity $\Phi_Q'([\Lambda^1\delta]) \le \Phi_Q([\delta])$. | PROVEN, CONDITIONAL | Typed cochain transformation $\Lambda^1 d_0 = d_0' \Lambda^0$ | Technical Appendix | Prose-proved | None |
| C9 | Quantum $\Phi\Gamma R$ signature bounds. | PROVEN, CONDITIONAL | Declared 2-cell $d_1$, $d_1 d_0 = 0$ | Technical Appendix | Prose-proved | None |
| D1 | Trace distance is *the* selected quantum gauge without operational axioms. | REFUSED / PROVEN FALSE | CPTP monotonicity alone | What This Does Not Claim, Model II §2; ENC-0247 | Mechanized (ENC-0247) | None |
| D2 | Architectural lesson: gauge is part of observer geometry. | INTERPRETIVE | Conceptual lesson | Framework | None | None |
| D3 | Falsifiability fork (detector reading 2 vs $\sqrt{2}$). | FALSIFIABILITY | Testable attribution | §5 | Replay test | None |
| QM-081-C1 | CPTP-monotonicity does not select the trace norm ($\mathsf{CPTPMonotone}(j) \not\Longrightarrow j(X) = \frac{1}{2}\|X\|_1$). | PROVEN | Scale-invariance of monotonicity | Model II §2, Technical Appendix; Lean `QM.cptp_monotone_not_select` | Mechanized (ENC-0247) | None |
| QM-081-C2 | Genuine non-increasing halving contraction ensures non-vacuous counterexample. | PROVEN | Finite difference model | Model II §2, Technical Appendix; Lean `QM.id_cptpMonotone_halving` | Mechanized (ENC-0247) | None |
| QM-081-C3 | Half-trace-norm is the conditionally selected operational metric under Helstrom discrimination. | PROVEN, CONDITIONAL | Unitary invariance + classical total-variation reduction | Model II §2.2, Technical Appendix; ENC-0246 | Prose-proved (ENC-0246) | None |
| QM-081-C4 | Trace norm contracts under CPTP maps (quantum data-processing inequality). | STANDARD | CPTP channel dynamics on $M_n(\mathbb{C})$ | Model II §2, Technical Appendix; Nielsen-Chuang, Wilde | Standard / imported | None |
| QM-081-C5 | Column-stochastic kernels contract the $\ell^1$ norm (classical shadow of C4). | PROVEN | Nonnegative column-stochastic matrix $S$ | Model II §2.1, Technical Appendix; Lean `QM.stochastic_l1_contraction` | Mechanized (ENC-1055) | None |
| QM-081-C6 | Many CPTP-monotone metrics exist (Petz monotone metrics, relative entropies, fidelity). | STANDARD | Matrix geometry | Model II §2; Petz (1996), Morozova-Chentsov (1990) | Standard / imported | None |
| QM-082-C1 | Stochastic kernels preserve finite distributions and compose as a monoid. | PROVEN | Finite outcome distributions on $\Gamma$ | Model II §2.1, Technical Appendix; Lean `QM.StochasticChannel` | Mechanized (ENC-1127) | None |
| QM-082-C2 | Finite CPTP channels induce column-stochastic population shadows on output diagonal: $K(\gamma'\mid\gamma) = \sum_k \|\langle\gamma'\|A_k\|\gamma\rangle\|^2$. | PROVEN | Kraus completeness $\sum_k A_k^\dagger A_k = I$ | Model II §2.1, Technical Appendix; Lean `QM.StochasticChannel` | Mechanized (ENC-1127) | None |
| QM-082-C3 | Population shadow records population transport only; complete positivity and coherence transport constitute the non-commutative lift. | DEFINITION / SCOPE FENCE | Declared basis readout | Model II §2.1, What This Does Not Claim | Structural fence | None |

<!-- claim-id-body-only-sync:begin -->

Body-only ID sync (packaging)
---

**AuthorityEffect:** None. Packaging hygiene; no OPEN→PROVED.

| ID | Claim | Type | Status |
|---|---|---|---|
| ENC-0246 | Body claim-shaped ID registered for bijection packaging only; conditional trace-distance selection | DEFINITION | packaging |
| ENC-0247 | Body claim-shaped ID registered for bijection packaging only; CPTP monotonicity necessary but not sufficient | DEFINITION | packaging |
| ENC-1055 | Body claim-shaped ID registered for bijection packaging only; column-stochastic l1 contraction | DEFINITION | packaging |
| ENC-1127 | Body claim-shaped ID registered for bijection packaging only; CPTP population shadow stochastic kernel | DEFINITION | packaging |
| GS-003 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| OB-E19-2 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| OB-E19-5 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| OB-E19-6 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| OB-E19-7 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| OB-E19-8 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| PKT-20260722-RES-EPOCH19 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |

<!-- claim-id-body-only-sync:end -->