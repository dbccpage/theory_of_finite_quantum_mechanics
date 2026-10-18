# Consolidated Account: Classical Independence, Finite-Catalogue Hull Obstruction, and Quantum Separability

## GTOC Foundations — Quantum Contact Series (qm_071_entanglement_as_a_separability_obstruction)

**Date:** 2026-10-17 · **Version:** v2.0 (Consolidated Packaging)  
**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)  
**Status:** RELEASED / CONSOLIDATED  
**Authority:** `AuthorityEffect::None`  

## Mechanism Inventory

| Slot | Value / Description |
| --- | --- |
| **Primitive Differences** | $\delta_{\mathrm{prod}}(w) = w - \frac{w_A \otimes w_B}{W}$ (classical table); $\delta_{\mathrm{sep}}(w, \lambda) = w - \sum_k \lambda_k P_k$ (convex hull) |
| **Carriers / Structure** | Finite Nonnegative Joint Tables $w \in \mathbb{Q}_{\ge 0}^{A \times B}$; Rational Coordinate Vectors $\iota \to \mathbb{Q}$; Bipartite Density Operators $\rho \in \mathcal{H}_A \otimes \mathcal{H}_B$ |
| **Cochain Complex** | $C^0 \to C^1$ marginal-product assembly and convex-combination simplex maps |
| **ZeroRel** | Exact product tables ($\delta_{\mathrm{prod}} \equiv 0$); Convex product-hull members ($\delta_{\mathrm{sep}} \equiv 0$) |
| **Licensed Repairs** | None |
| **Quotient / Q1** | Nonlinear set quotient by equal defect; Convex feasible hull $\operatorname{conv}(P)$ |
| **Residuals** | $\Phi(w) = \|\delta_{\mathrm{prod}}(w)\|_1$; Dual witness violation gap $t - \varphi(w) > 0$ |
| **Witnesses** | Exact LP Dual Separators (`omega_solvers::solver_convex_finite_hull`); Universal Bell Witness $F = \frac{1}{2}I - \rho_B = Q^{T_B}$ (`omega_quantum_physics::bipartite_operator`) |
| **Observers / Profiles** | Marginal observers, joint table observers, linear witness functionals $\varphi$ |
| **Anomalons** | None |
| **CompletionLaw** | Finite LP Duality / Separation Theorem |
| **Terminal / Route** | Route to 003 Quantum Foundations (Consolidated Archive) |
| **AuthorityEffect** | None |

---

# Abstract & Executive Consolidation Summary

This consolidated account establishes the exact mathematical hierarchy between three distinct concepts that were conflated in earlier literature:
1. **Classical Table Independence (QM_070):** A property of a single nonnegative measurement table $w$, decided by the vanishing of the product defect $\delta_{\mathrm{prod}}(w) = w - \frac{w_A \otimes w_B}{W}$.
2. **Finite-Catalogue Hull Membership ($P$-Nonseparability, QM_071):** A linear feasibility condition relative to an explicitly declared finite set of product generators $P$, certified by a separating linear functional $\varphi$.
3. **Genuine Quantum Separability:** Membership in the convex hull of *all* admissible product density operators $\alpha \otimes \beta$, certified by universal entanglement witnesses (such as the partial-transpose witness $F = Q^{T_B}$).

Following this consolidation, standalone drafts **QM_070** and **QM_071** are retired into redirect stubs. All mandatory mathematical derivations are preserved herein, backed by compiled, sovereign Rust certifiers. Unresolved backlog tasks concerning finite-hull completeness and Bell state instantiations are formally closed and pruned.

---

# 1. Classical Independence and the Observation-Loss Boundary (QM_070 Core)

### 1.1 Carrier and Product Defect
Let $A, B$ be finite index sets and $w : A \times B \to \mathbb{Q}_{\ge 0}$ a nonnegative joint weight table with positive total mass $W = \sum_{a,b} w(a,b) > 0$. The marginals are $w_A(a) = \sum_b w(a,b)$ and $w_B(b) = \sum_a w(a,b)$. The canonical marginal product is $\mathrm{prod}(a,b) = \frac{w_A(a) w_B(b)}{W}$, defining the **product defect**:

$$
\delta_{\mathrm{prod}}(w)(a,b) = w(a,b) - \frac{w_A(a)\,w_B(b)}{W}.
$$

Its gauge is the $\ell^1$ mass:

$$
\Phi(w) = \|\delta_{\mathrm{prod}}(w)\|_1 = \sum_{a,b} \left|w(a,b) - \frac{w_A(a)\,w_B(b)}{W}\right|.
$$

**Theorem (Exact Independence Diagnostic).**
$$
\Phi(w) = 0 \quad\Longleftrightarrow\quad \forall a,b,\; w(a,b) = \frac{w_A(a)\,w_B(b)}{W}.
$$
*Proof.* $\Phi(w)$ is a sum of absolute values over a finite set. A sum of nonnegative terms vanishes if and only if each term vanishes identically.

### 1.2 Scale-Independent Total-Variation Distance
For the normalized probability distribution $p = w / W$:

$$
\frac{\Phi(w)}{W} = \|p - p_A \otimes p_B\|_1.
$$

Thus $\frac{\Phi(w)}{2W} = \frac{1}{2}\|p - p_A \otimes p_B\|_1$ is the scale-independent **total-variation distance** from $p$ to its own marginal product. It is not, in general, the minimum distance to the entire manifold of product distributions.

### 1.3 Contraction Under Independent Stochastic Maps
Let $K_A : \mathbb{Q}^A \to \mathbb{Q}^{A'}$ and $K_B : \mathbb{Q}^B \to \mathbb{Q}^{B'}$ be independent column-stochastic maps (so $\sum_{a'} (K_A)_{a',a} = 1$ and $\sum_{b'} (K_B)_{b',b} = 1$). Then:

$$
\delta_{\mathrm{prod}}((K_A \otimes K_B)w) = (K_A \otimes K_B)\delta_{\mathrm{prod}}(w).
$$

Because any column-stochastic matrix contracts the $\ell^1$ norm ($\|K v\|_1 \le \|v\|_1$):

$$
\Phi((K_A \otimes K_B)w) \le \Phi(w).
$$

*Critical Scope Fence:* The hypothesis of **independent** stochastic maps is essential. A shared random variable (convex mixture of local maps) can prepare correlated states from product states, increasing classical correlation without entanglement.

### 1.4 Observation-Loss Boundary
Every product-basis probability table $p_{ab}$ admits the separable diagonal quantum realization:

$$
\rho_{\mathrm{diag}} = \sum_{a,b} p_{ab} |a\rangle\langle a| \otimes |b\rangle\langle b|.
$$

Consequently, a single classical measurement table alone can never certify entanglement.

- **Collision Witness:** The maximally entangled Bell state $\rho_B = |\Phi^+\rangle\langle\Phi^+|$ and the classical mixture $\rho_C = \frac{1}{2}|00\rangle\langle00| + \frac{1}{2}|11\rangle\langle11|$ yield the identical computational-basis table $p = (1/2, 0, 0, 1/2)$ and identical defect $\Phi = 1$, despite $\rho_C$ being manifestly separable.
- **Converse Failure Witness:** The state $|\psi\rangle = \frac{1}{2}(|00\rangle + |01\rangle + |10\rangle - |11\rangle)$ is entangled (its coefficient matrix has rank 2), yet its computational-basis table is uniform $(1/4, 1/4, 1/4, 1/4)$, yielding $\Phi = 0$.

$\Phi(w)$ evaluates the statistical independence of the observation table, not the entanglement of the quantum state.

---

# 2. Finite Convex-Hull Obstructions and Separating Witnesses (QM_071 Core)

### 2.1 State Carrier and Declared Product Family
Let $w : \iota \to \mathbb{Q}$ be a finite rational state-coordinate packet over coordinates $\iota$. Let $P : \kappa \to (\iota \to \mathbb{Q})$ be an explicitly declared finite family of product generators $\{P_k\}_{k \in \kappa}$.

The **separability defect** relative to mixing weights $\lambda$ is:

$$
\delta_{\mathrm{sep}}(w, \{\lambda_k\}) = w - \sum_{k \in \kappa} \lambda_k P_k, \qquad \lambda_k \ge 0, \quad \sum_k \lambda_k = 1.
$$

A state $w$ is **$P$-separable** if $\exists \lambda \ge 0, \sum_k \lambda_k = 1$ such that $\delta_{\mathrm{sep}}(w, \lambda) = 0$. Otherwise, $w$ is **$P$-nonseparable**.

### 2.2 Soundness of Separating Witnesses
**Theorem (Witness Soundness).** If a linear functional $\varphi : \mathbb{Q}^\iota \to \mathbb{Q}$ and threshold $t \in \mathbb{Q}$ satisfy:
1. $\varphi(P_k) \ge t$ for every declared generator $P_k \in P$, and
2. $\varphi(w) < t$,

then $w \notin \operatorname{conv}(P)$ ($w$ is $P$-nonseparable).

*Proof.* Suppose $w \in \operatorname{conv}(P)$, so $w = \sum_k \lambda_k P_k$ with $\lambda_k \ge 0$ and $\sum_k \lambda_k = 1$. By linearity:
$$
\varphi(w) = \sum_k \lambda_k \varphi(P_k) \ge \sum_k \lambda_k t = t \sum_k \lambda_k = t,
$$
which directly contradicts $\varphi(w) < t$.

### 2.3 The Critical P-Nonseparability Boundary
The soundness theorem certifies exclusion from the declared hull $\operatorname{conv}(P)$. It connects to quantum separability through the inclusion:

$$
P \subseteq \{\text{valid product density matrices}\} \implies \operatorname{conv}(P) \subseteq \mathrm{Sep}.
$$

Therefore:
1. A verified decomposition into valid product states certifies quantum separability.
2. A witness separating $w$ from a finite catalogue $P$ certifies exclusion from that catalogue's hull ($P$-nonseparability).
3. A genuine entanglement witness must satisfy $\varphi(\sigma) \ge t$ for **all** admissible product states $\sigma = \alpha \otimes \beta$.

---

# 3. Rational Counterexample: Pure Product State Excluded by a Finite Catalogue

To show that $P$-nonseparability does not imply quantum entanglement, we present an exact rational counterexample.

Let the declared family $P$ consist of the four computational-basis product projectors in a 2-qubit system:
$$
P = \{|00\rangle\langle00|, |01\rangle\langle01|, |10\rangle\langle10|, |11\rangle\langle11|\}.
$$

Consider the state:
$$
w = |++\rangle\langle++|, \qquad |+\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}.
$$
In the computational basis, every matrix entry of $w$ is $1/4$:
$$
w = \frac{1}{4} \sum_{i,j,k,l \in \{0,1\}} |ij\rangle\langle kl|.
$$

Define the linear functional $\varphi$ and threshold $t = 0$:
$$
\varphi(\rho) = -\operatorname{Re}(\rho_{00,11}), \qquad t = 0.
$$

Evaluating $\varphi$ on the generators of $P$:
- For each $P_k \in P$, the off-diagonal coherence $(P_k)_{00,11} = 0$, so $\varphi(P_k) = 0 \ge 0$.

Evaluating $\varphi$ on $w$:
- $\varphi(w) = -\operatorname{Re}(w_{00,11}) = -1/4 < 0$.

By the witness theorem, $w \notin \operatorname{conv}(P)$ ($w$ is $P$-nonseparable). Yet $w = |+\rangle\langle+| \otimes |+\rangle\langle+|$ is manifestly a pure product state!

### Geometric Origin
Every pure product state is an **extreme point** of the convex set of quantum density operators. A finite list $P$ omits infinitely many pure product states. An omitted pure product state cannot be expressed as a convex combination of other states. Thus, no finite catalogue can ever exhaust the product state space of finite-dimensional quantum mechanics.

---

# 4. Classical Tables Cannot Be Given a Trivial Convex-Product Test

In earlier drafts, it was suggested that table non-factorization could be upgraded to separability by testing membership in a convex hull of product tables.

This is trivial on the classical carrier: for every normalized joint probability table $p \in \mathbb{Q}_{\ge 0}^{A \times B}$, $p$ decomposes as:
$$
p = \sum_{a \in A, b \in B} p_{ab} \,(\delta_a \otimes \delta_b),
$$
where each $\delta_a \otimes \delta_b$ is an elementary classical product distribution.

Thus, **every classical joint distribution already lies in the convex hull of classical product distributions**. A convex-product test on classical tables has zero discriminative power; it becomes nontrivial only when the state space carries off-diagonal coherences and the factors are restricted to admissible quantum state vectors.

---

# 5. The Universal Bell Witness (Replacing Toy Models)

To certify genuine entanglement across the continuous family of all admissible product states, we utilize the partial-transpose witness already verified in the repository.

### 5.1 Universal Separating Functional
Define the bipartite Hermitian operator:
$$
F = \frac{1}{2}I - \rho_B, \qquad \rho_B = |\Phi^+\rangle\langle\Phi^+| = \frac{1}{2}(|00\rangle+|11\rangle)(\langle00|+\langle11|).
$$

For any normalized pure product vector $|a \otimes b\rangle = |a\rangle \otimes |b\rangle$ with $\|a\|_2 = \|b\|_2 = 1$:
$$
|\langle\Phi^+|a \otimes b\rangle|^2 = \frac{1}{2} |a_0 b_0 + a_1 b_1|^2 \le \frac{1}{2} (|a_0|^2 + |a_1|^2)(|b_0|^2 + |b_1|^2) = \frac{1}{2},
$$
by Cauchy–Schwarz. Consequently:
$$
\langle a \otimes b | F | a \otimes b \rangle = \frac{1}{2}\langle a \otimes b | I | a \otimes b \rangle - |\langle\Phi^+|a \otimes b\rangle|^2 = \frac{1}{2} - |\langle\Phi^+|a \otimes b\rangle|^2 \ge 0.
$$

By convex linearity, for **every** separable state $\rho \in \mathrm{Sep}$:
$$
\operatorname{Tr}(F \rho) \ge 0.
$$

### 5.2 Decisive Evaluation on Bell State and Mixture
Evaluating $F$ on the two candidate states from Section 1.4:
1. **Bell State $\rho_B$:**
   $$
   \operatorname{Tr}(F \rho_B) = \frac{1}{2}\operatorname{Tr}(\rho_B) - \operatorname{Tr}(\rho_B^2) = \frac{1}{2}(1) - 1 = -\frac{1}{2} < 0.
   $$
   This strictly negative value certifies that $\rho_B$ is entangled.
2. **Classical Mixture $\rho_C = \frac{1}{2}|00\rangle\langle00| + \frac{1}{2}|11\rangle\langle11|$:**
   $$
   \operatorname{Tr}(F \rho_C) = \frac{1}{2}\operatorname{Tr}(\rho_C) - \frac{1}{2}\left[\frac{1}{2}|\langle\Phi^+|00\rangle|^2 + \frac{1}{2}|\langle\Phi^+|11\rangle|^2\right] = \frac{1}{2} - \frac{1}{2}\left[\frac{1}{4} + \frac{1}{4}\right] = \frac{1}{4} > 0.
   $$
   (Note: in the unnormalized partial transpose representation $F = Q^{T_B}$ with $Q = |\Psi^-\rangle\langle\Psi^-|$, $\operatorname{Tr}(F\rho_B) = -1/2$ and $\operatorname{Tr}(F\rho_C) = 0$).

This universal witness directly resolves the ambiguity: it separates states that produce identical classical measurement tables.

---

# 6. Preservation of Convex Constraints vs. Linear-Quotient Pitfall

A crucial structural principle must be enforced:
The mixing weights must satisfy:
$$
\lambda_k \ge 0, \qquad \sum_k \lambda_k = 1.
$$

The separable state set is a **convex set**, not a linear subspace.

### The Linear Subspace Trap
The real linear span of all product density matrices $\operatorname{span}_{\mathbb{R}}\{\alpha \otimes \beta\}$ equals the **entire vector space of bipartite Hermitian operators**:
$$
\operatorname{span}_{\mathbb{R}}(\mathrm{Prod}) = \mathcal{H}_A \otimes \mathcal{H}_B.
$$

If convex combinations were relaxed to arbitrary real linear combinations (as in an unconstrained linear cochain quotient), the Bell state $\rho_B$ would be represented as a linear combination of product states:
$$
\rho_B = \frac{1}{2}(|00\rangle\langle00| + |11\rangle\langle11| + |00\rangle\langle11| + |11\rangle\langle00|),
$$
where $|00\rangle\langle11| + |11\rangle\langle00| = 2 |++\rangle\langle++| - 2 |--\rangle\langle--| - \dots$
Relaxing convexity would erase the entire concept of entanglement. Convex feasibility is mathematically indispensable.

---

# 7. Backlog Pruning: Finite-Hull Completeness and Bell Instantiation

The historical backlog items associated with QM_071 are resolved as follows:
1. **Finite-Hull Completeness:** For a declared finite rational catalogue $P$, deciding membership is the linear program:
   $$
   P \lambda = w, \quad \mathbf{1}^T \lambda = 1, \quad \lambda \ge 0.
   $$
   Finite LP duality ensures that exactly one of two conditions holds: either a primal convex decomposition exists, or a dual separating hyperplane separates $w$ from $\operatorname{conv}(P)$. This is implemented and certified in sovereign Rust (`omega_solvers::solver_convex_finite_hull`). Algorithmic iteration limits (pivot budgets) are operational boundaries, not unresolved mathematical conjectures.
2. **General Separability Completeness:** The existence of a witness for every entangled state in finite dimensions is the classical theorem of Horodecki et al. (1996), derived from the Hahn–Banach separation theorem on compact convex sets.
3. **Backlog Pruning:** The tasks "prove finite-hull completeness" and "construct Bell state density matrix instantiation" are fully superseded by existing code and are formally removed from the active research backlog.

---

# 8. Verified Rust Implementations and Test References

| Mathematical Object | Sovereign Implementation | Test Suite |
| --- | --- | --- |
| Joint table, product defect $\delta_{\mathrm{prod}}$, $\ell^1$ mass $\Phi(w)$ | [`omega_quantum_physics::joint_table`](../../../omega_engine/crates_rs/omega_quantum_physics/src/joint_table.rs) | [`tests/entanglement/product_non_factorization.rs`](../../../omega_engine/crates_rs/tests/omega_quantum_physics/entanglement/product_non_factorization.rs) |
| Independent stochastic map contraction | [`JointTable::apply_local_maps`](../../../omega_engine/crates_rs/omega_quantum_physics/src/joint_table.rs) | `product_non_factorization::test_stochastic_contraction` |
| Finite convex-hull LP solver and certifier | [`omega_solvers::solver_convex_finite_hull`](../../../omega_engine/crates_rs/omega_solvers/src/solver_convex_finite_hull.rs) | [`tests/entanglement/separability_witness.rs`](../../../omega_engine/crates_rs/tests/omega_quantum_physics/entanglement/separability_witness.rs) |
| Universal Bell witness $F = Q^{T_B}$ | [`omega_quantum_physics::bipartite_operator`](../../../omega_engine/crates_rs/omega_quantum_physics/src/bipartite_operator.rs) | `product_non_factorization::test_bell_vs_separable_mixture` |
| Rational counterexample $\|++\rangle\langle++\|$ | `separability_witness.rs` | `separability_witness::test_declared_family_counterexample` |

---

# Scope Fences and Non-Claims

1. **What this account supports:**
   - Exact decidability of classical table independence via $\Phi(w) = 0$.
   - Scale-independent total-variation interpretation $\Phi/(2W)$ and contraction under independent stochastic maps.
   - Rigorous certification of $P$-nonseparability via separating linear functionals.
   - Exact mathematical separation between classical correlation, finite-catalogue exclusion, and genuine entanglement.
2. **What this account does not support:**
   - Does not solve the general NP-hard quantum separability problem over arbitrary dimensions.
   - Does not claim that a single measurement table can diagnose entanglement.
   - Does not derive quantum mechanics from classical probability.
   - Mints zero operational authority (`AuthorityEffect::None`).

---

# Historical Claim Index

| Consolidated ID | Historical Source ID | Status | Mechanized Verification |
| --- | --- | --- | --- |
| `QM-SEP-001` | `QM-070-C1`..`C5` | PROVEN | `omega_quantum_physics::joint_table` |
| `QM-SEP-002` | `QM-070-C8` | PROVEN | `JointTable::apply_local_maps` |
| `QM-SEP-003` | `QM-070-C7` | SCOPE FENCE | Information-loss boundary ($\rho_{\mathrm{diag}}$) |
| `QM-SEP-004` | `QM-071-C3`..`C5` | PROVEN | `SeparatingWitness::verify` |
| `QM-SEP-005` | `QM-071-C10` | PROVEN | Extreme-point counterexample $\|++\rangle\langle++\|$ |
| `QM-SEP-006` | `QM-071-C6` | PROVEN | Universal Bell witness $F = \frac{1}{2}I - \rho_B$ |
