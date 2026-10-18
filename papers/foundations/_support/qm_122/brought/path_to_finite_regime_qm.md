# Path to Finite-Regime Quantum Mechanics: Derivation Steps, Paper Map, and Import Boundary

> **Authority Firewall & Nonclaim Box (`AuthorityEffect: None`)**
>
> 1. **What this document supports:** A finite step-by-step derivation roadmap and paper mapping connecting classical $\ell^1$ obstruction geometry to finite-regime quantum mechanics across the 6-rung ingredient ladder (`QM_121`) and the 5-group obligation register (`QM_211`).
> 2. **What this document does NOT support:** It does not claim that Quantum Mechanics is derived "from nothing", nor that the Born rule or $\mathbb{C}/U(1)$ phase carrier are derived without imported hypotheses (Gleason non-contextuality, continuous reversible transport, local tomography).
> 3. **Narrowest Defensible Claim:** Finite-regime quantum mechanics decomposes into classical $\ell^1$ bookkeeping (Rungs 1–4), a phase fiber (Rung 5), a single non-$\ell^1$ interference resource (Rung 6), and exactly 3 (or 5) imported structural selections, each proven irreducible or conditionally forced under named axiom sets.
> 4. **Next Test Needed:** Mechanize Rung 5 (`PL-QM043-1`) in Lean 4 and adjudicate the 3-import vs 5-import basis reconciliation between `QM_121` and `QM_211`.

**Basement freeze (binding attachment points, not a proof):**  
`omega_engine/research/proof_packets/finite_l1_qm_freeze_20260730.md` (`FINITE-L1-FREEZE-20260730` **v0.1** — v0 body, v0.1 clarification pass).  
**Ordered derivation programme:**  
`omega_engine/research/proof_packets/derivation_master_order_20260730.md`.  
**Fin-3 toy + import reconciliation (Wave-0 companions):**  
`finite_l1_qm_fin3_toy_20260730.md`, `finite_l1_import_reconciliation_20260730.md`.  
Index: `omega_engine/research/proof_packets/readme.md`.

---

## 1. Executive Summary & The 6-Rung Ingredient Ladder

The Omega Engine Quantum Foundations estate demonstrates that quantum mechanics over finite sectors decomposes into two parts:
1. **Classical $\ell^1$ Bookkeeping (Rungs 1–4):** Probability, density matrices, stochastic channels, and path-sums are ordinary finite $\ell^1$ measure calculations over residual weight vectors.
2. **The Non-$\ell^1$ Quantum Surplus (Rungs 5–6 + Ceiling):** Superposition phase fibers, non-$\ell^1$ interference cross-terms, and imported structural selections ($\mathbb{C}/U(1)$ phase carrier, Born-quadratic uniqueness, continuum limit).

$$
\underbrace{L^1(E)}_{\text{probability / classical shadow}}\ \oplus\ \underbrace{\mathrm{Fiber}_{L^2}(E)}_{\text{interference / non-}\ell^1\text{ resource}}
$$

```text
L¹(E)              finite additive residual mass over sectors E
   │ normalize
   ▼
Δ(E)               the ordinary probability simplex            ← Rung 1: P = w / Σ w
   │ diagonal embedding
   ▼
Diag(Δ(E))         diagonal density / classical shadow         ← Rung 2: ρ = diag(p), Rung 3: CPTP shadow
   │ licensed L² lift
   ▼
Fiber_L²(E)        phase · coherence · interference            ← Rung 5: U(1)^{|E_w|-1} fiber, Rung 6: cross term
   │ non-L¹ resource appears
   ▼
quantum advantage  = NOT the probability law; IS the non-L¹ interference cross-term
```

---

## 2. Rung-by-Rung Derivation Steps & Paper/Code Map

| Rung | QM Concept | Classical $\ell^1$ Reading | Canonical Paper / Note | Lean 4 Module / Code | Derivation Step & Math Proof Target |
|---|---|---|---|---|---|
| **Rung 1** | **Probability & Born Square** | $\ell^1$ normalization $P=w/\sum w$; Born square $\|c\|^2/\sum\|c\|^2$ is redundant | `pub-010` (Thms 1, 4) | `PaperQF002.L010_01_BornRedundancy` | Prove $P_\gamma = w_\gamma/W$ requires no Hilbert space; show complex lift $c_\gamma=\sqrt{w_\gamma}e^{i\theta_\gamma}$ yields $\|c_\gamma\|^2/\sum\|c_\eta\|^2 = w_\gamma/W$, making Born square a redundant re-encoding. |
| **Rung 2** | **Density Matrix & Purity** | Diagonal weight distribution $\rho = \operatorname{diag}(p)$; PSD, trace-1; purity $\sum p_\gamma^2$ | `QM_007` (ENC-1126) | `QM.DiagonalDensity` (`PL-QM038-1`) | Embed normalized weights on diagonal $\rho_{\gamma\gamma'} = [\gamma=\gamma']p_\gamma$. Prove $\rho \ge 0$, $\operatorname{tr}\rho = 1$, purity $\operatorname{tr}\rho^2 = \sum p_\gamma^2 \in (0,1]$. Pure $\iff$ single sector weight. |
| **Rung 3** | **Channels & CPTP Shadow** | Stochastic kernel $K(\gamma'\mid\gamma) \ge 0, \sum K=1$; CPTP population shadow | `QM_082` (ENC-1127), `pub-005` | `QM.StochasticChannel` (`PL-QM041-1`), `QM.StochasticL1` | Prove CPTP map $\rho \mapsto \sum_k A_k \rho A_k^\dagger$ under declared basis induces column-stochastic shadow $K(\gamma'\mid\gamma) = \sum_k \|\langle\gamma'\|A_k\|\gamma\rangle\|^2$. |
| **Rung 4** | **Path Integral (Finite)** | Path-sum $M^n$; Chapman–Kolmogorov $M^{m+n} = M^m M^n$ | `QM_111` (ENC-1128), `QM_010` (ENC-1072) | `QM.FinitePathSum` (`PL-QM042-1`), `FiniteFeynmanShadow` | Prove $(M^n)(b\mid a) = \sum \prod M(v_i\mid v_{i-1})$ and $M^{m+n} = M^m M^n$ over any finite index type and commutative semiring. |
| **Rung 5** | **Superposition & Phase Fiber** | Quotient fiber $U(1)^{\|E_w\|-1}$ over nonzero weight support | `QM_060` (ENC-1129) | `PaperQF002` / `QM.SuperpositionFiber` (`PL-QM043-1`) | Prove superposition relative-phase content equals the fiber of the phase-blind quotient over $E_w$. Phases carry zero probability mass. |
| **Rung 6** | **Interference Cross-Term** | Non-$\ell^1$ cross-term $2\operatorname{Re}(c_i\overline{c_j})$; QC buildability set $S$ | `QM_061` (ENC-1135) | `QM.InterferenceBuildability` (`useful_qc_iff_setS`) | Prove cross-term $\|c_i+c_j\|^2 - \|c_i\|^2 - \|c_j\|^2$ is non-$\ell^1$ computable (lifts $(1,1)$ and $(1,-1)$ share identical $\ell^1$ law but mix to outcomes $4$ vs $0$). |
| **Ceiling** | **Imported Ingredients** | $\mathbb{C}/U(1)$ carrier, Born uniqueness, continuum | `QM_062`, `QM_120`, `QM_090`, `pub-010` | `BornQuadraticCountermodel` | Quarantined imports: (1) $\mathbb{C}/U(1)$ (QM_062); (2) Born quadratic uniqueness via Gleason non-contextuality (QM_120); (3) continuum limit (QM_090). |

---

## 3. The 5-Group Derivation & Obligation Register

To construct a fully finite-regime Quantum Mechanics, execute the following 47 derivation steps across 7 logical groups:

### Group 0 — Prerequisites (Foundation & Alignment)
1. **Import Reconciliation:** Adjudicate the 3-import (`QM_121`) vs 5-import (`QM_211`) parameterization; produce one canonical import basis.
2. **Markov Embedding Repair:** Repair `QM_211` Theorem 1.1 by citing the stochastic matrix embedding problem (Elfving 1937; Kingman 1962).
3. **Carrier Freeze:** Freeze a single formal definition of the "finite $\ell^1$ world": carrier, sector set, weight type, admitted transports, and readouts.
4. **Continuum & Field Audit:** Prove the frozen definition contains no hidden continuum and no hidden $\mathbb{C}$.

### Group A — The Carrier and Observer Layer
5. **Typed Probe Family:** Formalize residual sector basis as a declared typed probe family ($d : (i : I) \to X \to O_i$).
6. **Observer Shadow:** Prove the phase-blind quotient is precisely $B_I$ for the modulus-only probe family (L1 shadow is a WGOC observer).
7. **Basis Relativity:** Prove basis-relativity is observer-relativity: different sector bases yield incomparable observers (PCC template).
8. **Transport Closure:** Prove the $\ell^1$ world is closed under admitted monoid action transports.

### Group B — Complete the Derivable Rungs
9. **Superposition Mechanization:** Mechanize Rung 5 (`PL-QM043-1`, superposition phase content = quotient fiber).
10. **Phase Fiber Exactness:** Prove the phase fiber is exactly $U(1)^{|E_w|-1}$ over nonzero support $E_w$.
11. **Rung Re-Verification:** Re-verify Rungs 1–4 against the frozen Group-0 carrier.
12. **Classical Exhaustiveness:** Prove Rungs 1–4 are jointly exhaustive of classical $\ell^1$ bookkeeping.

### Group C — The Lift Theory (Classification of Non-Hilbert Lifts)
13. **Category of Lifts:** Define the category of lifts of an $\ell^1$ weight system: objects, morphisms, equivalence.
14. **Fiber Identification:** Prove the lift functor is well-defined and identify its fibers.
15. **Exotic Lifts:** Construct explicit non-Hilbert lifts: Real ($\mathbb{R}$), Quaternionic ($\mathbb{H}$), $\ell^p$ readouts ($p \neq 2$), finite field / cyclic carriers, and p-adic/tropical lifts.
16. **$\ell^1$ Preservation:** Prove each exotic lift reproduces the identical $\ell^1$ probability law.
17. **Separating Predictions:** Compute the exact point where each non-Hilbert lift diverges from standard QM.
18. **Classification Theorem:** Characterize all lifts satisfying a stated named axiom set.
19. **Non-Uniqueness Theorem:** Prove no canonical lift exists absent extra axioms (analogue of `no_greatest_of_three`).
20. **Conditional Uniqueness Theorem:** State the minimal axiom set forcing the complex Hilbert lift.
21. **QM_062 Extension:** Extend `QM_062` 2-level core forcing to a full $n$-level classification.
22. **$\ell^1$ Functional Independence:** Prove the lift is not determined by the $\ell^1$ data plus any purely $\ell^1$ functional.

### Group D — Discharge or Bound Each Import
23. **OB-U1 ($\mathbb{C}/U(1)$ Carrier):** Derive $\mathbb{C}/U(1)$ or prove it underivable (sub-obligations: reversible dynamics continuity & local tomography / global field-uniqueness).
24. **Signed Carrier Forcing:** Prove a signed/cyclic carrier is required for interference ($\mathbb{R}_{\ge 0}$ alone fails).
25. **OB-BORN (Born Quadratic Uniqueness):** Derive Born quadratic uniqueness from $\ell^1$ additivity without Gleason imports, or prove irreducibility.
26. **Non-Contextuality Adjudication:** Prove or refuse Gleason's non-contextuality hypothesis (`QM_120`).
27. **$\ell^2$ Readout vs Born Pairing:** Adjudicate whether quadratic $\ell^2$ readout (`QM_208`) and Born pairing (`QM_210`) are independent imports.
28. **Non-Commutativity Origin:** Prove whether non-commutativity (`QM_209`) is an import or a consequence of contextuality + lift.
29. **Continuum Irreducibility:** Prove the continuum import irreducible via the Markov embedding problem.
30. **Unitarity vs Stochasticity:** Prove unitarity is not derivable from stochastic population transport.
31. **Hermiticity Forcing:** Prove Hermiticity of Hamiltonian $H$ is forced or import it explicitly.

### Group E — Independence and Necessity (Completeness Proof)
32. **Import Independence Theorem:** Construct $N$ separating models, each failing exactly one import while satisfying all others.
33. **Necessity Theorem:** Prove no import can be derived from the frozen $\ell^1$ carrier.
34. **Sufficiency Theorem:** Prove $\ell^1$ carrier + full import set $\implies$ finite Quantum Mechanics.
35. **Minimality Theorem:** Prove no proper subset of imports suffices.
36. **Import Completeness:** Prove the import set is complete (no further hidden assumptions required).

### Group F — Operational & Physical Adequacy
37. **Finite Formalism Recovery:** Reconstruct full finite-dimensional matrix QM from $\ell^1$ + imports.
38. **Tsirelson Bound:** Recover Bell/CHSH inequalities and Tsirelson's bound ($2\sqrt{2}$) from the reconstructed theory.
39. **Contextuality Prediction:** Predict Mermin–Peres contextuality quantitatively from the reconstructed observer model.
40. **Operational Cross-Check:** Map imports to operational reconstruction frameworks (Hardy 2001; Masanes–Müller 2011; CBH).
41. **Decoherence & Classical Limit:** Prove classical limit and decoherence emerge naturally (`QM_112`, `QM_043`).
42. **Global Empirical Falsifier:** State the global empirical falsifier for the complete finite-regime QM framework.

### Group G — WGOC Observer Integration
43. **Hilbert Non-Uniqueness as Observer Selection:** Prove Hilbert-lift non-uniqueness is an instance of WGOC `no_greatest_of_three`.
44. **Contextuality as Incomparability:** Prove Mermin–Peres contextuality is observer-incomparability (`NGg.outcome_type_does_not_select_general`).
45. **Stable Quantum Claims:** Instantiate `StableClaim` on the QM carrier to map measurement failure witnesses.
46. **Basis Order Independence:** Apply `Core_C` preserves-meets ($W4a$) to prove sector-basis refinement is order-independent.
47. **Measurement Refinement Bound:** Apply `fold_strict_steps_bound` to bound measurement refinements on a finite carrier.

---

## 4. Defensible Headline Standard

$$
\boxed{
\begin{array}{c}
\text{\textbf{Finite-Regime Quantum Mechanics}} \\
= \\
\text{Finite }\ell^1\text{ Obstruction Geometry (Rungs 1--5)} \\
+ \\
\text{Non-}\ell^1\text{ Interference Resource (Rung 6)} \\
+ \\
\text{Exactly } N \text{ Mutually Independent Imported Selections (OB-U1, OB-BORN, Continuum)}
\end{array}
}
$$
