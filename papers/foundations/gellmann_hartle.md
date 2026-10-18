# Finite History Decoherence Matrices, Exact Coarse-Graining, and Probability Additivity

## GTOC Foundations — Quantum Contact Series (qm_043_gellmann_hartle_cochain_decoherence)

**AuthorityEffect:** None.  
**Document ID:** `QM_043` (incorporating results from retired `QM_041`)  
**Version:** `v2.0.0` (Consolidated Finite Histories Formulation)  
**Status:** RELEASED  
**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)

---

## Mechanism Inventory

| Slot | Value / Description |
|---|---|
| **Primitive Differences** | Trace discrepancy $\delta c = \mu(S) - \sum_{j \in S} D_{jj}$ between coherent coarse-graining and diagonal probability weights. |
| **Carriers / Structure** | Finite-dimensional complex Hilbert space $\mathcal{H}$ over $\mathbb{Q}(i)$ or $\mathbb{C}$, positive semidefinite density operator $\rho \ge 0$, and finite family of class operators $\{C_j\}_{j=1}^m$. |
| **Cochain Complex** | Discrete cochain projection paths $C_j = P_{e_{j,n}} \dots P_{e_{j,1}}$. |
| **Coboundary Maps** | $\delta^0, \delta^1$ on interaction graph $G=(V,E)$. |
| **ZeroRel** | Sum-rule consistency: $\mu(S) = \sum_{j \in S} D_{jj} \iff \sum_{j < k, j,k \in S} \operatorname{Re} D_{jk} = 0$. |
| **Licensed Repairs** | Environment-record projection (dephasing) reducing off-diagonal coherence. |
| **Quotient / Q1** | Coarse-graining quotient partition $\mathcal{P}$ of history index set $\{1, \dots, m\}$. |
| **Residuals** | Bilinear cross-term residual $2 \operatorname{Re} D_{jk}$; bounded by $L^1$ interference score $\Phi_{\mathrm{int}}(D)$. |
| **Witnesses** | Replayable Rust certifiers in `omega_functional::decoherence::DecoherenceFunctional`. |
| **Observers / Profiles** | Local diagonal evaluator reading $\{D_{jj}\}$ vs. global coherent evaluator reading $\operatorname{Tr}(C_S \rho C_S^\dagger)$. |
| **Anomalons** | None. |
| **CompletionLaw** | Complete history set completeness premise $\sum_j C_j^\dagger C_j = I$. |
| **Terminal / Route** | Route to 003 Quantum Foundations (measurement and transport calculus). |
| **AuthorityEffect** | None. Structural or formal evidence grants no authority. |

---

## Status Box (Binding)

```text
Honesty: Formalizes the finite Gell-Mann–Hartle decoherence matrix, positivity quadratic form,
         completeness normalization hypothesis, exact coarse-graining residual, weak vs. medium
         decoherence distinction, and the Diósi tensor composition stability objection.
Quarantine: Continuous path-integral limits, infinite history spaces, and master equation dissipation
            laws are quarantined [Q-HELD]. Standalone integer-only arithmetic and phase-class persistence
            are retired.
Terminal: RELEASED_v2.0.0
AuthorityEffect::None
```

---

## 0. Scope Firewall & Non-Claims

1. **Supplied Structure:** This paper analyzes the consequences of a supplied finite-dimensional operator family $\{C_j\}_{j=1}^m$ and positive state $\rho \ge 0$. It does **not** derive the Hilbert space, the complex phase fiber, or quantum kinematics from the primitive difference.
2. **Static Bounds vs. Dynamical Dissipation:** The $L^1$ interference score $\Phi_{\mathrm{int}}(D) = \sum_{j \ne k} |D_{jk}|$ provides a static arithmetic error bound on coarse-graining discrepancies. It does **not** establish a physical law of off-diagonal dissipation or continuous open-system master equation.
3. **Retired Modules:**
   - The standalone integer-only arithmetic track ($(d_{11}+d_{22}+2d_{12}) - (d_{11}+d_{22}) = 2d_{12}$) is absorbed as a finite arithmetic fixture realized in operator models.
   - The disconnected $H^1(G; U(1))$ phase-class persistence obligation (`QM_043-C5`) is removed from the required foundational derivation list.

---

## 1. The Positive History Matrix

Let $\mathcal{H}$ be a finite-dimensional inner-product space over $\mathbb{C}$ (or $\mathbb{Q}(i)$). Let $\rho$ be a positive semidefinite density operator ($\rho \ge 0$), and let $\{C_1, \dots, C_m\}$ be a finite family of history class operators on $\mathcal{H}$.

### Definition (Decoherence Functional / History Matrix)

The **Gell-Mann–Hartle Decoherence Matrix** $D \in \mathbb{C}^{m \times m}$ is defined componentwise by:

$$
D_{jk} := \operatorname{Tr}\!\left(C_j \rho C_k^\dagger\right).
$$

### Hermiticity

Using cyclicity and adjoint properties of trace:

$$
D_{kj} = \operatorname{Tr}\!\left(C_k \rho C_j^\dagger\right) = \operatorname{Tr}\!\left(\left(C_j \rho C_k^\dagger\right)^\dagger\right) = \left(\operatorname{Tr}\!\left(C_j \rho C_k^\dagger\right)\right)^* = D_{jk}^*.
$$

Thus $D = D^\dagger$ is Hermitian.

### Positivity Proof

**Theorem.** *If $\rho \ge 0$, then $D$ is positive semidefinite ($D \ge 0$).*

*Proof.* For any complex vector $z = (z_1, \dots, z_m)^T \in \mathbb{C}^m$, define the composite linear combination operator:

$$
A_z := \sum_{j=1}^m \overline{z_j} C_j.
$$

Evaluating the quadratic form $z^\dagger D z$:

$$
z^\dagger D z = \sum_{j=1}^m \sum_{k=1}^m \overline{z_j} z_k D_{jk} = \sum_{j=1}^m \sum_{k=1}^m \operatorname{Tr}\!\left( \overline{z_j} C_j \rho z_k C_k^\dagger \right) = \operatorname{Tr}\!\left( \left(\sum_{j=1}^m \overline{z_j} C_j\right) \rho \left(\sum_{k=1}^m \overline{z_k} C_k\right)^\dagger \right).
$$

Substituting $A_z$:

$$
z^\dagger D z = \operatorname{Tr}\!\left( A_z \rho A_z^\dagger \right).
$$

Since $\rho \ge 0$, its spectral decomposition $\rho = \sum_\alpha p_\alpha |\psi_\alpha\rangle\langle\psi_\alpha|$ has non-negative eigenvalues $p_\alpha \ge 0$. Therefore:

$$
\operatorname{Tr}\!\left( A_z \rho A_z^\dagger \right) = \sum_\alpha p_\alpha \langle\psi_\alpha| A_z^\dagger A_z |\psi_\alpha\rangle = \sum_\alpha p_\alpha \| A_z |\psi_\alpha\rangle \|^2 \ge 0.
$$

Since $z^\dagger D z \ge 0$ for all $z \in \mathbb{C}^m$, $D$ is positive semidefinite. $\blacksquare$

### Structural Consequence

Positive semidefiniteness yields more than non-negative diagonal elements ($D_{jj} \ge 0$): it constrains every $2 \times 2$ principal minor, providing the Cauchy–Schwarz interference bound:

$$
|D_{jk}|^2 \le D_{jj} D_{kk}.
$$

---

## 2. Diagonal Normalization and the Completeness Hypothesis

The trace of $D$ (sum of diagonal history weights) satisfies:

$$
\sum_{j=1}^m D_{jj} = \sum_{j=1}^m \operatorname{Tr}\!\left(C_j \rho C_j^\dagger\right) = \operatorname{Tr}\!\left( \rho \sum_{j=1}^m C_j^\dagger C_j \right).
$$

### Normalization Theorem

If the state is normalized ($\operatorname{Tr}(\rho) = 1$) and the history family satisfies the **completeness premise**:

$$
\sum_{j=1}^m C_j^\dagger C_j = I,
$$

then the diagonal history weights form a normalized discrete probability distribution:

$$
\sum_{j=1}^m D_{jj} = \operatorname{Tr}(\rho I) = \operatorname{Tr}(\rho) = 1.
$$

### Load-Bearing Distinction

The completeness premise $\sum_j C_j^\dagger C_j = I$ is strictly required. The weaker condition $\sum_j C_j = I$ does **not** imply diagonal normalization unless the operators are pairwise orthogonal projections.

Furthermore, diagonal normalization $\sum_j D_{jj} = 1$ is mathematically distinct from whole-family coherent grouping normalization:

$$
\mu(\Omega) := \operatorname{Tr}\!\left[ \left(\sum_{j=1}^m C_j\right) \rho \left(\sum_{k=1}^m C_k\right)^\dagger \right] = \sum_{j=1}^m D_{jj} + 2 \sum_{j < k} \operatorname{Re} D_{jk}.
$$

For an arbitrary list of class operators, $\mu(\Omega)$ and $\sum_j D_{jj}$ differ by the total off-diagonal interference. Exhaustive projective-history decompositions enforce both identities, but arbitrary families require hypotheses to be declared explicitly.

---

## 3. Exact Coarse-Graining Identity

Let $S \subseteq \{1, \dots, m\}$ be an arbitrary subset of histories. Define the coherently coarse-grained class operator $C_S$ and its weight $\mu(S)$ by:

$$
C_S := \sum_{j \in S} C_j, \qquad \mu(S) := \operatorname{Tr}\!\left(C_S \rho C_S^\dagger\right).
$$

Expanding the product under the trace:

$$
\mu(S) = \operatorname{Tr}\!\left( \left(\sum_{j \in S} C_j\right) \rho \left(\sum_{k \in S} C_k^\dagger\right) \right) = \sum_{j,k \in S} \operatorname{Tr}\!\left( C_j \rho C_k^\dagger \right) = \sum_{j,k \in S} D_{jk}.
$$

Splitting the summation into diagonal and off-diagonal index pairs:

$$
\mu(S) = \sum_{j \in S} D_{jj} + \sum_{\substack{j \ne k \\ j,k \in S}} D_{jk} = \sum_{j \in S} D_{jj} + \sum_{\substack{j < k \\ j,k \in S}} (D_{jk} + D_{kj}).
$$

Since $D_{kj} = D_{jk}^*$, $D_{jk} + D_{kj} = 2 \operatorname{Re} D_{jk}$. This yields the fundamental coarse-graining residual identity:

$$
\boxed{ \mu(S) - \sum_{j \in S} D_{jj} = 2 \sum_{\substack{j < k \\ j,k \in S}} \operatorname{Re} D_{jk}. }
$$

This identity determines exactly when evaluating the weight of coherently grouped operators agrees with summing the individual diagonal probabilities.

---

## 4. Weak vs. Medium Decoherence

The coarse-graining identity establishes a formal distinction between two criteria:

1. **Weak Decoherence (Probability Additivity Criterion):**
   $$
   \operatorname{Re} D_{jk} = 0 \quad \text{for all } j \ne k.
   $$
   - **Necessity:** Inspecting every two-element subset $S = \{j, k\}$ gives $\mu(\{j, k\}) - D_{jj} - D_{kk} = 2 \operatorname{Re} D_{jk}$. Additivity on all pairs requires $\operatorname{Re} D_{jk} = 0$.
   - **Sufficiency:** If $\operatorname{Re} D_{jk} = 0$ for all pairs, the right-hand sum vanishes for every subset $S \subseteq \{1, \dots, m\}$, ensuring exact probability sum rules across all coarse-grainings.

2. **Medium Decoherence (Vanishing Off-Diagonal Coherence):**
   $$
   D_{jk} = 0 \quad \text{for all } j \ne k.
   $$
   This condition requires the complete vanishing of both the real and imaginary parts of the off-diagonal history matrix.

**Observation:** Medium decoherence implies weak decoherence, but the converse is not true. A decoherence matrix with purely imaginary off-diagonal entries ($D_{jk} = i b \ne 0$) satisfies weak decoherence and all probability sum rules, but violates medium decoherence.

---

## 5. Tensor Composition Stability & The Diósi Objection

While weak decoherence suffices for probability additivity within a single fixed family, it exhibits a failure mode under independent tensor composition:

### Tensor Factorization for Independent Systems

For two independent, non-interacting systems $A$ and $B$, history operators and states factor as tensor products:

$$
C_{(j_A, j_B)}^{AB} = C_{j_A}^A \otimes C_{j_B}^B, \qquad \rho^{AB} = \rho^A \otimes \rho^B.
$$

The composite decoherence matrix factors as the Kronecker product:

$$
D^{AB} = D^A \otimes D^B, \qquad D_{(j_A, j_B), (k_A, k_B)}^{AB} = D_{j_A k_A}^A \cdot D_{j_B k_B}^B.
$$

### Diósi's Composition Objection

Suppose system $A$ and system $B$ both satisfy weak decoherence, but have non-vanishing imaginary off-diagonal entries. Specifically, let $j \ne k$ with:

$$
D_{jk}^A = i b_A, \qquad D_{jk}^B = i b_B \qquad (b_A, b_B \in \mathbb{R} \setminus \{0\}).
$$

For the composite history index pairs $(j, j)$ and $(k, k)$, the off-diagonal entry of the composite matrix is:

$$
D_{(j, j), (k, k)}^{AB} = D_{jk}^A \cdot D_{jk}^B = (i b_A)(i b_B) = - b_A b_B.
$$

The real part of this composite off-diagonal entry is strictly non-zero:

$$
\operatorname{Re}\!\left( D_{(j, j), (k, k)}^{AB} \right) = - b_A b_B \ne 0.
$$

Consequently, the composite family breaks the probability sum rule:

$$
\mu(\{(j, j), (k, k)\}) - D_{(j, j)(j, j)}^{AB} - D_{(k, k)(k, k)}^{AB} = 2 \operatorname{Re}\!\left( D_{(j, j), (k, k)}^{AB} \right) = -2 b_A b_B \ne 0.
$$

### Stability of Medium Decoherence

In contrast, **medium decoherence ($D_{jk} = 0$) is preserved under tensor composition**. If $D_{j_A k_A}^A = 0$ for all $j_A \ne k_A$, then every off-diagonal element of $D^{AB}$ vanishes identically.

This finite algebraic result demonstrates why medium decoherence is necessary when independent subsystem composition is admitted.

---

## 6. $L^1$ Interference Score Error Bound

Define the total **$L^1$ Off-Diagonal Interference Score**:

$$
\Phi_{\mathrm{int}}(D) := \sum_{j \ne k} |D_{jk}|.
$$

### Bounding the Coarse-Graining Discrepancy

Applying the triangle inequality to the exact coarse-graining identity:

$$
\left| \mu(S) - \sum_{j \in S} D_{jj} \right| = \left| 2 \sum_{\substack{j < k \\ j,k \in S}} \operatorname{Re} D_{jk} \right| \le 2 \sum_{\substack{j < k \\ j,k \in S}} |D_{jk}| \le \sum_{j \ne k} |D_{jk}| = \Phi_{\mathrm{int}}(D).
$$

Therefore:

$$
\boxed{ \left| \mu(S) - \sum_{j \in S} D_{jj} \right| \le \Phi_{\mathrm{int}}(D). }
$$

**Significance:** $\Phi_{\mathrm{int}}(D)$ provides an explicit upper bound on the error incurred when approximating coherent coarse-graining with classical diagonal addition.

---

## 7. Code Descendants & Replayable Witnesses

The finite history results are implemented and certified in sovereign Rust crates:

1. **Core Functional Implementation:**
   - [`omega_functional::decoherence::DecoherenceFunctional`](file:///c:/Users/a343o/source/repos/the_symbol_game/omega_engine/crates_rs/omega_functional/src/decoherence.rs):
     - Computes $D_{jk} = \operatorname{Tr}(C_j \rho C_k^\dagger)$ over `GaussianRat` ($\mathbb{Q}(i)$).
     - Verifies `.is_complete()` ($\sum_j C_j^\dagger C_j = I$).
     - Evaluates `.sum_rule_residual()` for arbitrary history partitions.
     - Certifies `.weak_decoherence_witness()` and `.medium_decoherence_witness()`.
2. **Integration Test Suite:**
   - [`tests/omega_quantum_physics/representation/gell_mann_hartle_decoherence.rs`](file:///c:/Users/a343o/source/repos/the_symbol_game/omega_engine/crates_rs/tests/omega_quantum_physics/representation/gell_mann_hartle_decoherence.rs):
     - Validates the complex residual $2 \operatorname{Re} D_{jk}$.
     - Realizes the $(2, 1, 3)$ integer arithmetic fixture in explicit operator form.
     - Confirms that diagonal normalization fails when completeness $\sum_j C_j^\dagger C_j = I$ is omitted.
   - [`tests/omega_quantum_physics/representation/heisenberg_picture_shadow.rs`](file:///c:/Users/a343o/source/repos/the_symbol_game/omega_engine/crates_rs/tests/omega_quantum_physics/representation/heisenberg_picture_shadow.rs):
     - Verifies a finite environment-record circuit generating diagonal $D$.
     - Exhaustively checks all 15 coarse-grainings of a 4-history family.
     - Evaluates a non-trivial example with imaginary off-diagonal entries satisfying weak decoherence while violating medium decoherence.

---

## 8. Summary According to Claim Discipline

1. **What it supports:**
   - Demonstrates that for any positive state $\rho \ge 0$ and class operators $\{C_j\}$, the history matrix $D$ is positive semidefinite with non-negative diagonal.
   - Shows that $\sum_j D_{jj} = 1$ when $\operatorname{Tr}\rho = 1$ and $\sum_j C_j^\dagger C_j = I$.
   - Proves the exact coarse-graining identity $\mu(S) - \sum_{j \in S} D_{jj} = 2 \sum_{j < k} \operatorname{Re} D_{jk}$.
   - Shows that weak decoherence ($\operatorname{Re} D_{jk} = 0$) characterizes single-family additivity, but fails under tensor composition (Diósi objection), whereas medium decoherence ($D_{jk} = 0$) is tensor-stable.
   - Establishes the static error bound $|\mu(S) - \sum_{j \in S} D_{jj}| \le \Phi_{\mathrm{int}}(D)$.
2. **What it does not support:**
   - Does not derive Hilbert spaces, class operators, or states from primitive differences.
   - Does not establish a dynamic open-system dissipation law or master equation.
   - Does not support continuous path-integral limits or infinite history spaces.
3. **The narrowest defensible claim:**
   - In any finite-dimensional operator model, the Gell-Mann–Hartle history matrix is positive semidefinite; its real off-diagonal parts control probability sum-rule discrepancies via $\mu(S) - \sum_{j \in S} D_{jj} = 2 \sum_{j < k, j,k \in S} \operatorname{Re} D_{jk}$; and medium decoherence is the minimal condition preserved under tensor product composition.
4. **The next test needed:**
   - Lean 4 mechanization of the Diósi tensor composition counterexample and the exact coarse-graining residual expansion in `omega_engine/lean4/research_programs/003_quantum_foundations/`.

---

## References

1. Murray Gell-Mann and James B. Hartle, "Quantum Mechanics in the Light of Quantum Cosmology," [arXiv:1803.04605](https://arxiv.org/abs/1803.04605).
2. James B. Hartle, "The Quantum Mechanics of Closed Systems," [arXiv:gr-qc/9210006](https://arxiv.org/abs/gr-qc/9210006).
3. Lajos Diósi, "Irreversible quantum dynamics and the Gell-Mann–Hartle decoherence functional," *Phys. Rev. Lett.* 72, 1994, [arXiv:gr-qc/9409017](https://arxiv.org/abs/gr-qc/9409017).
4. H. F. Dowker and J. J. Halliwell, "Quantum mechanics of history: The decoherence functional in quantum mechanics," *Physical Review D* 46 (1992), 1580, [doi:10.1103/PhysRevD.46.1580](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.46.1580).
