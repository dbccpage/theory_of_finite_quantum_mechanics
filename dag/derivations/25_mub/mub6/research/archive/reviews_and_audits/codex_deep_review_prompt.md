# Master Codex Audit & Architectural Review Prompt: MUB(6) Formal Verification Stack

**AuthorityEffect**: None  
**Firewall Line**: `stated region only; mints no authority`  
**Repository**: `https://github.com/dbccpage/MUB6` (Local path: `C:\Users\a343o\source\repos\MUB6`)  
**Target Reviewer**: OpenAI Codex / Advanced Reasoning LLM Reviewer  
**Date**: September 2026

---

## 1. Context & Purpose of this Audit

You are invited to perform an exhaustive, adversarial, and uncompromising mathematical and software architecture review of the **MUB(6) formal derivations and computational verification repository**.

The central open problem under investigation is the existence of mutually unbiased bases in dimension 6: specifically, whether the maximal number of pairwise mutually unbiased bases is $\mathrm{MUB}(6) = 3$ (**Branch A: Obstruction Confirmation**) or $\mathrm{MUB}(6) \ge 4$ (**Branch B: Numerical Counterexample Discovery**).

Over five phases and 19 formal milestones, this repository has constructed a multi-engine formal verification and exact algebraic geometry stack spanning:
- **Lean 4 Formal Proofs**: 30+ formal modules across `lean4/gluing/` and `lean4/012_mutually_unbiased_bases/MUB/`.
- **Exact Rational Rust Engines**: Zero-float native computation across 14 crates in `omega_engine/crates_rs/omega_mub/`.
- **Exact Rational Python Verifiers**: 17 verification harnesses and 505 unit/regression tests in `omega_engine/crates/mub_verify/` and `tests/mub_verify/`.
- **Certified Artifacts & Receipts**: 10 canonical JSON receipts in `artifacts/` plus Phase 5 algebraic geometry manifests in `research/g1_foundation/`.

Your mission is to perform a deep, objective audit:
1. **Identify any mathematical, logical, or software engineering mistakes**, circularities, vacuous proofs, or cancellation laundering in the repository.
2. **Critique the roadmap**: determine whether this program can genuinely resolve $\mathrm{MUB}(6) = 3$ unconditionally, identify where previous researchers failed, and evaluate what vulnerabilities remain.
3. **Architect the integration of the PO-032 Symbol Game**: specify how the simplicial $L_1$ governor, Network Simplex duality, and proposer/host architecture can be directly embedded into the continuous moduli solver engine.

---

## 2. Core Repository Architecture & Key Files to Inspect

Before beginning your analysis, inspect the following primary entry points:

### 2.1 The Synthesis Preprint & Roadmaps
- `research/paper.md`: The complete 22-section synthesis preprint manuscript documenting all 19 milestones, the 7-class epistemic ledger, and the certified artifact matrix.
- `research/mub6_roadmap.md`: The complete roadmap and dependency graph tracking discharged targets and research debt.
- `research/g1_foundation/g1_elimination_receipt.md`: The receipt documenting the algebraic geometry elimination of Premise G1.
- `research/g1_foundation/classification_manifest.json`: Machine-readable manifest cataloging the 5 moduli components and 4 eliminated subvarieties.

### 2.2 Primary Lean 4 Formalizations
- **Phase 5 Moduli Classification**: `lean4/MasterClassification.lean` (5 certified components, `master_classification_theorem`, `comprehensive_moduli_exhaustiveness`).
- **Algebraic Geometry Branches**: `lean4/CaseCoverage.lean` (`master_case_routing`), `lean4/GroebnerBranch.lean` (Nullstellensatz refutations), `lean4/CADBranch.lean` (Stengle Positivstellensatz SOS bounds).
- **Semantics & Encoding**: `lean4/ConcreteSemantics.lean` (constructive dephasing), `lean4/PolynomialEncoding.lean` (50 real vars, 55 eqns), `lean4/CertificatePilot.lean`.
- **Discrete & Continuous Gluing**: `lean4/TargetA11OrbitExhaustiveness.lean` (`target_c3_unconditional_grand_synthesis`, `target_c3_no_fourth_basis_unconditional`).
- **Global Continuous Moduli Integration**: `lean4/TargetB3ManifoldIntegration.lean`, `TargetB2GlobalGluing.lean`, `TargetB1ContinuousChaining.lean`, `TargetA13GrandSynthesis.lean`, `TargetA10GlobalCover.lean`, `TargetA12SmaleSentry.lean`.

### 2.3 Exact Computational Engines
- **Receipt Auditing**: `omega_engine/crates/mub_verify/verify_all_receipts.py` (audits all receipts with zero float tolerance).
- **Phase 5 Verifiers**: `omega_engine/crates/mub_verify/g1_classification_verifier.py`, `g1_case_verifier.py`.
- **Continuous Gluing Verifiers**: `omega_engine/crates/mub_verify/target_b3_manifold_integration.py`, `target_b2_global_gluing.py`, `target_b1_continuous_chaining.py`.
- **Rust Engines**: `omega_engine/crates_rs/omega_mub/src/omega_native/` (`mub6_manifold_integration.rs`, `mub6_global_gluing.rs`, `mub6_continuous_chaining.rs`, `mub6_smale_sentry.rs`, `network_simplex.rs`, `exact_simplex.rs`).

---

## 3. Mandatory Audit Dimensions

Execute your review across four rigorous audit dimensions:

### Audit Dimension 1: Mathematical & Logical Soundness (Mistake Hunting)

1. **Premise Vacuity & Contradiction Detection**:
   - Inspect Lean 4 theorem statements across `TargetA11OrbitExhaustiveness.lean`, `TargetA13GrandSynthesis.lean`, `TargetB3ManifoldIntegration.lean`, and `MUB.MasterClassification`.
   - Are any theorems proved from vacuous hypotheses (e.g., $A \land \neg A \implies B$)?
   - Does `master_case_routing` in `CaseCoverage.lean` form a true exhaustive partition over $\mathbb{C}$, or could a complex Hadamard matrix exist where $P_{\text{corner}}$ is ill-defined or falls outside the disjunction?
2. **Definitional Trivialization & Kernel Reflection**:
   - Inspect the reflection proofs `by rfl` in `TargetA10GlobalCover.lean` and `TargetB3ManifoldIntegration.lean`.
   - Does the boolean decision procedure `checkGlobalUnifiedCover` genuinely check the required volume conservation and positive margin properties, or does it evaluate trivially?
3. **Axiom Footprint Integrity**:
   - Audit the axiom dependencies of all synthesis theorems.
   - Confirm that no custom axioms or `sorryAx` / `admit` are present, and that synthesis theorems depend strictly on standard foundational axioms (`[propext, Classical.choice, Quot.sound]`, with master synthesis depending solely on `[propext]`).
4. **Algebraic Geometry Elimination Soundness**:
   - Audit the Nullstellensatz identities in `GroebnerBranch.lean` and Positivstellensatz SOS certificates in `CADBranch.lean`.
   - In the upper boundary certificate:
     $$-1 \equiv \left(-\frac{1}{3}\right)(x^2 + y^2 - 1) + \left[\frac{1}{3}(x - 2)^2 + \frac{1}{3}y^2\right] + \left(\frac{4}{3}\right)(x - 2)$$
     verify that the algebra holds identically in $\mathbb{Q}[x, y]$ and that the multiplier non-negativity $\sigma_0 \ge 0, \sigma_1 \ge 0$ is mathematically sound.
   - Does eliminating $x \ge 2$ and $x \le -2$ suffice to prove coordinate boundedness in $[-1, 1]$, or does the proof in `CaseCoverage.lean` (`x_abs_le_one`) require additional assumptions?
5. **Moduli Orbit Exhaustiveness**:
   - Does the 5-component inductive type `ModuliComponent` in `MasterClassification.lean` genuinely capture all order-6 complex Hadamard orbits?
   - Is the dephasing $D_{ij} = \overline{H_{i0}} H_{ij} H_{00} \overline{H_{0j}}$ guaranteed to preserve complex Hadamardness and mutual unbiasedness without loss of generality?

---

### Audit Dimension 2: Software Engineering & Numerical Discipline

1. **Zero-Float Policy Enforcement**:
   - The repository strictly forbids floating-point types (`f32`, `f64`, `float`, `complex`) in certifiers and receipts.
   - Audit Python verifiers for any inadvertent floating-point operations, particularly in division `/` vs `//` or trigonometric/exponential evaluations.
   - Audit Rust crates for any usage of `f32`/`f64`.
2. **Cancellation Laundering Audit**:
   - Ensure that no certifier performs an approximate floating-point calculation and subsequently casts the result to `Fraction(...)` to give the appearance of an exact rational certificate.
3. **Integer Overflow & Exact Arithmetic Bounds**:
   - In Rust `num_rational::BigRational` and Python `Fraction`, are there points where unbounded coefficient growth could lead to performance exhaustion or stack overflow?
4. **Receipt Hash & Digest Verification**:
   - Verify that all SHA-256 digests in `artifacts/manifest.json` and `research/g1_foundation/classification_manifest.json` correctly hash the exact canonical LF-normalized file bytes.

---

### Audit Dimension 3: Roadmap Critique & Genuine Solvability Assessment

1. **Why has MUB(6) resisted solution for decades?**:
   - Analyze the classical failure modes:
     - Numerical optimization (Zauner, Bengtsson) finding local minima near $\Psi = 0$ but unable to prove global non-existence.
     - Analytical algebraic elimination producing polynomial ideals with thousands of terms that overwhelm standard Gröbner basis engines (Singular, Macaulay2, Magma).
     - Phase-angle parameterizations introducing transcendental equations that obstruct exact polynomial certificates.
2. **Does this repository truly overcome those failure modes?**:
   - How does the combination of dephased corner charts, discrete bisection reflection, Lipschitz propagation ($L = 85/9$), and Čech holonomy obstructions circumvent the algebraic complexity explosion?
   - What are the remaining subtle gaps? Specifically:
     - Is the discrete 28-cell partition cover + continuous Szöllősi chaining + 5-chart Čech nerve *topologically dense* in the full 4-parameter moduli space $\mathcal{M}_6$?
     - Could there be isolated, measure-zero complex Hadamard orbits in dimension 6 that do not deform to any of the 5 canonical components?
3. **Smale $\alpha$-Theory & Branch B Neutrality**:
   - Target A12 implements a Smale $\alpha$-theory and Krawczyk interval contractor as a "root sentry".
   - Is this sentry genuinely capable of detecting a 4th MUB counterexample if one exists, or could a real root exist within the certified partition tree that escaped detection due to cell boundary clipping?

---

### Audit Dimension 4: Symbol Game Integration into the Solution Engine

The repository contains an in-tree port of the **PO-032 Symbol Game** (`omega_engine/crates/mub_verify/l1_governor.py`, `packet_firewall.py`, `network_simplex.rs`, `exact_simplex.rs`), implementing a three-layer sovereignty architecture:
- **Layer 1 (Proposer)**: Generates candidate algebraic witnesses, parameter substitutions, and cell bounds.
- **Layer 2 (simplicial Boundary Operator & $L_1$ Simplex Governor)**: Solves discrete minimum-cost circulation problems $\Phi_1 = \|\omega - d\alpha\|_1$ over exact rationals, verifying zero duality gap and enforcing defect descent.
- **Layer 3 (Trusted Host / Lean 4 Kernel)**: Formally checks certificates fail-closed with `AuthorityEffect: None`.

Provide a detailed, concrete engineering proposal to:
1. **Drive Automated Algebraic Branch Refutations via Simplex Duality**:
   - How can the Sparse Revised Simplex (`exact_simplex.rs`) and Network Simplex (`network_simplex.rs`) be used to search for rational Nullstellensatz multipliers $a_i(x)$ such that $\sum a_i(x) f_i(x) \equiv 1$?
2. **Optimize Dynamic Cochain Potentials across the Covering Nerve**:
   - In Target B2, loop holonomy is certified by $\Phi_1 = \|\omega - d\alpha\|_1 \ge 12133/5000 > 0$. How can the $L_1$ governor automatically compute the optimal 0-cochain $\alpha^*$ on arbitrary higher-degree nerve cycles?
3. **Token Attention Steering for Adaptive Bisection**:
   - How can LLM attention patterns over the 50 polynomial coordinates be distilled to steer adaptive bisection heuristics toward regions of maximal curvature mass?
4. **Construct an Autonomous Turn-Based Derivation Loop**:
   - Define the turn-based protocol (`ASSERT`, `CUT`, `VERIFY`, `RETRACT`) enabling a multi-agent swarm to autonomously explore open parameter charts, propose rational certificates, and verify them against the Lean 4 compiler without human intervention.

---

## 4. Deliverable Format

Structure your audit report into five distinct, clearly labeled sections:

1. **Executive Assessment & Epistemic Verdict**:
   - High-level verdict on the mathematical rigor, software discipline, and claim hygiene of the MUB6 repository.
   - Explicit confirmation or refutation of whether any blocking logical errors or cancellation laundering were found.
2. **Itemized Mistake & Vulnerability Log**:
   - Table of all identified defects, grouped by severity: `CRITICAL` (mathematical flaw/unsoundness), `WARNING` (potential gap or edge-case omission), `PEDANTIC` (notation/doc discrepancy).
   - For each finding: exact file path, line numbers, description of the vulnerability, and concrete remediation patch.
3. **Roadmap Solvability Analysis**:
   - Comprehensive analysis of whether the current architecture can unconditionally resolve $\mathrm{MUB}(6) = 3$.
   - Identification of the single most dangerous remaining theoretical bottleneck.
4. **Symbol Game Solution Engine Architecture Blueprint**:
   - Concrete specification of the integrated Proposer/Host solver engine.
   - Exact mathematical formulas, data structures, and CLI entry points.
5. **Actionable Recommendations for the Working Group**:
   - Prioritized top 5 next derivation and implementation tasks.
