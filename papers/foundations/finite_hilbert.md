# 122 — Finite Hilbert Boundary from Primitive Difference

**Subtitle:** How far a finite presented carrier reaches toward Hilbert language, one named lift at a time

```text
Canonical ID: QM_122
Canonical title: Finite Hilbert Boundary from Primitive Difference
Canonical version: v0.2.0 (Consolidated Finite QM Organizing Chapter)
Rights License: Creative Commons Attribution 4.0 International (CC-BY-4.0)
AuthorityEffect: None
```

**Author:** Jeremy H. Carroll  
**Date:** 2026-08-20 (Consolidated 2026-10-17)  
**Rights License:** CC-BY-4.0  
**Status:** preprint — ceiling bound; organizing chapter for finite quantum foundations  
**Series:** Quantum Foundations 122  
**Companions:** QM_120 (Contextuality), QM_212 (Cochain Parity & Majorana Algebra)  
**Authority:** None. Mathematical derivations and finite models only.

---

## Bindings in this paper

| Slot | Binding |
|---|---|
| Primitive difference | Two points are equivalent under a report when a supplied report map sends them to the same value. Two amplitude vectors are equivalent under readout when they yield the same phase-blind weights. |
| Carrier | A finite list of report labels, with a supplied report map. Coefficients, inner products, and dynamic updates are added as explicit extra structure. |
| Leftover | After a report, residual structure remains: escape from the selected section, failure of dynamics to descend, motion of labels, failure of projected updates to compose, or phase information made visible through subsequent mixing. |
| Repair | None in this chapter. Residuals and obstructions are classified, not repaired into continuum Hilbert space. |
| Witnesses | Finite matrix and graph certifiers; vectors $(1,1)$ and $(1,-1)$; integer, Gaussian-integer, and complex matrix hosts. |
| Authority | None. Formally verified code and finite models do not authorize a physical ontology. |

---

## Abstract

We establish the mathematical boundary between finite classical report-fiber structures and quantum mechanics on finite-dimensional hosts. Starting from a finite set of report labels and a reversible permutation update, every such update extends linearly to an isometry once an inner product and coefficient ring are supplied. On coordinatewise squared-modulus reports $q(z) = (|z_1|^2, \dots, |z_n|^2)$, both global and relative coordinate phases preserve the report fiber: $q(D\psi) = q(\psi)$ for all diagonal unit-modulus $D$. Relative phase becomes observable exclusively through a subsequent non-diagonal change of presentation (mixing).

We prove an exact row-intensity descent criterion: a transformed readout $q(Az)$ can be computed from $q(z)$ alone if and only if each row of $A$ contains at most one non-zero entry. For unitary transformations, this restricts report-descending dynamics to permutation matrices with coordinatewise phases. Mixing maps (such as the Hadamard scaled isometry $M^* M = 2I$) fail to descend, demonstrating failure of intermediate classical report reconstruction.

We consolidate the sound mathematical kernels of the finite-QM sequence:
1. Diagonal embedding $p \mapsto \operatorname{Diag}(p)$ and the population channel action $\operatorname{diag}(\Phi(\operatorname{Diag}(p))) = K_\Phi p$, showing by explicit counterexample ($K_H^2 = K_H \ne K_{H^2} = I$) that population summaries fail to preserve channel composition.
2. The exact trace-zero duality theorem: $\frac{1}{2}\sum_i |x_i| = \max_{\operatorname{diam}(m) \le 1}\sum_i m_i x_i$ for $\sum_i x_i = 0$, attained by $m_i = \frac{1}{2}\operatorname{sign}(x_i)$.
3. Stochastic $\ell^1$ contraction and scoped state-effect pairing factorization.
4. A finite-transport treatment of cycle holonomy, path composition, Bianchi identities, and quaternion commutators whose central $-1$ acts trivially in the adjoint representation.

---

## 1. Introduction and Three Organizing Questions

Earlier drafts cataloged quantum postulates as isolated ingredient lists. This consolidated text organizes finite quantum foundations around three precise mathematical questions:

1. **Can a later readout be computed from an earlier report?**  
   *Mathematical test:* Constancy on report fibers (report descent).  
   *Main witness:* Coordinatewise intensity reports, scaled Hadamard mixing, and channel population composition failure.

2. **Can one global assignment realize a target set of local constraints?**  
   *Mathematical test:* Membership in the image of a linear map ($\operatorname{im} A$).  
   *Main witness:* The Mermin–Peres contextuality parity obstruction (detailed in companion [QM-120](file:///c:/Users/a343o/source/repos/the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/qm_120_mermin_peres_contextuality_cochain_obstruction.md)).

3. **Is a closed residual exact, and what does its class cost?**  
   *Mathematical test:* Kernel/image classification followed by resource-bounded optimization.  
   *Main witness:* Cochain parity, 1-cycle decoding, and minimum-weight optimization (detailed in companion [QM-212](file:///c:/Users/a343o/source/repos/the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/qm_212_microsoft_majorana_problem.md)).

---

## 2. Setup: Carriers, Reports, and Scaled Mass

### 2.1 The Report-Fiber Framework
Let $S$ be a finite set of states (carrier) and $Q$ a finite set of report labels. A report map $p: S \to Q$ partitions $S$ into fibers $p^{-1}(q)$. A dynamics $T: S \to S$ descends to a well-defined label update $\bar{T}: Q \to Q$ if and only if $p(s_1) = p(s_2) \implies p(T(s_1)) = p(T(s_2))$. When $T$ fails this condition, the dynamics does not descend through the report.

### 2.2 Finite Weights and Normalization
Assigning nonnegative weights $w \in \mathbb{R}_{\ge 0}^n$ defines a total mass $W = \sum_i w_i$. Normalization $P = w/W$ maps non-zero weights into the probability simplex $\Delta^n$. This normalization is purely an $\ell^1$ operation. The diagonal embedding:
$$p \mapsto \operatorname{Diag}(p)$$
embeds probability distributions into the space of diagonal density matrices.

---

## 3. The Core Theorems: Readouts, Isometries, and Descent

### 3.1 The Phase Leftover and Relative Phase
For an amplitude vector $\psi \in \mathbb{C}^n$, let $q(\psi) = (|\psi_1|^2, \dots, |\psi_n|^2)$ be the coordinatewise squared-modulus report.

**Proposition 3.1 (Phase Fiber Invariance).** For any diagonal matrix $D = \operatorname{diag}(e^{i\theta_1}, \dots, e^{i\theta_n})$ with unit-modulus entries:
$$q(D\psi) = q(\psi).$$
*Significance:* Both global phase ($\theta_1 = \dots = \theta_n$) and relative coordinate phases ($\theta_j \neq \theta_k$) leave the coordinatewise intensity report completely unchanged. The report fiber over a strictly positive probability vector $p \in \Delta^n$ is a torus $\mathbb{T}^{n-1} = U(1)^{n-1}$. For mixed states, the fiber of density matrices having diagonal $p$ is convex and higher-dimensional (for $n=2$, a disk of radius $\sqrt{p_1 p_2}$, with pure states on its boundary). Relative phase becomes observable exclusively through subsequent mixing and readout.

### 3.2 Scaled Integer Mixing
Consider the vectors over $\mathbb{Z}$:
$$\psi_+ = (1, 1), \qquad \psi_- = (1, -1).$$
Their coordinatewise squared reports are identical:
$$q(\psi_+) = (1, 1), \qquad q(\psi_-) = (1, 1).$$
Now apply the integer Hadamard mixing matrix:
$$M = \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}.$$
Note that $M^* M = 2I$, so $M$ is a scaled isometry ($M/\sqrt{2}$ is unitary over $\mathbb{R}$). The transformed vectors and their reports are:
$$M\psi_+ = (2, 0) \implies q(M\psi_+) = (4, 0),$$
$$M\psi_- = (0, 2) \implies q(M\psi_-) = (0, 4).$$
Since $q(\psi_+) = q(\psi_-)$ but $q(M\psi_+) \ne q(M\psi_-)$, no function $F$ satisfying $q(M\psi) = F(q(\psi))$ can exist. The relative sign $\pm 1$ in $\psi_\pm$ is invisible to $q$, but is converted into distinct report weights by $M$. This obstruction holds over the integers $\mathbb{Z}$ and requires neither complex numbers nor the circle group $U(1)$.

### 3.3 The Row-Intensity Descent Characterization Theorem
We characterize exactly which linear transformations permit report-level prediction of intensities.

**Theorem 3.2 (Row-Intensity Descent Characterization).** Let $A: \mathbb{C}^n \to \mathbb{C}^m$ be a complex matrix, and let $q(z) = (|z_1|^2, \dots, |z_k|^2)$ denote the coordinatewise squared-modulus report. There exists a function $F: \mathbb{R}^n \to \mathbb{R}^m$ satisfying:
$$q(Az) = F(q(z)) \qquad \forall z \in \mathbb{C}^n$$
if and only if each row of $A$ has at most one non-zero entry.

*Proof.*  
**Sufficiency ($\Leftarrow$):** Suppose row $b$ of $A$ has at most one non-zero entry, say at column $j$ with value $A_{bj}$. Then the $b$-th component of $Az$ is $(Az)_b = A_{bj} z_j$. Its squared magnitude is:
$$|(Az)_b|^2 = |A_{bj}|^2 |z_j|^2 = |A_{bj}|^2 q(z)_j.$$
Defining $F_b(w) = \sum_{j=1}^n |A_{bj}|^2 w_j$ (where at most one term in the sum is non-zero) yields $q(Az)_b = F_b(q(z))$ for all $z$.

**Necessity ($\Rightarrow$):** Suppose such a function $F$ exists. Fix an output row $b \in \{1, \dots, m\}$. For any pair of distinct column indices $j \neq k$, test the vector:
$$z(\theta) = e_j + e^{i\theta} e_k, \qquad \theta \in [0, 2\pi),$$
where $e_j, e_k$ are standard basis vectors. The report $q(z(\theta))$ has entries:
$$q(z(\theta))_l = \begin{cases} 1 & \text{if } l = j \text{ or } l = k, \\ 0 & \text{otherwise}, \end{cases}$$
which is strictly independent of $\theta$. Consequently, $F(q(z(\theta)))$ must be constant in $\theta$.

However, the $b$-th coordinate of $A z(\theta)$ is $A_{bj} + A_{bk} e^{i\theta}$. Its squared magnitude is:
$$|(Az(\theta))_b|^2 = |A_{bj} + A_{bk} e^{i\theta}|^2 = |A_{bj}|^2 + |A_{bk}|^2 + 2\operatorname{Re}\left(A_{bj}\overline{A_{bk}} e^{-i\theta}\right).$$
For this quantity to be constant for all $\theta \in [0, 2\pi)$, the oscillating term must vanish:
$$A_{bj}\overline{A_{bk}} = 0.$$
Since this holds for every pair $j \neq k$, row $b$ cannot contain two non-zero entries. Thus each row contains at most one non-zero entry. $\blacksquare$

**Corollary 3.3 (Invertible and Unitary Descents).**  
1. An invertible square matrix $A \in \operatorname{GL}_n(\mathbb{C})$ descends through $q$ if and only if $A = D P$, where $D$ is an invertible diagonal matrix and $P$ is a permutation matrix.  
2. A unitary matrix $U \in U(n)$ descends through $q$ if and only if $U$ is a generalized permutation matrix (a permutation with unit-modulus diagonal phases).

**Corollary 3.4 (Standard-Form Isometries of $\mathbb{Z}[i]^n$).** Every standard-form linear isometry of $\mathbb{Z}[i]^n$ (preserving $\sum_j |\psi_j|^2$) is a permutation matrix with Gaussian unit coefficients $\{\pm 1, \pm i\}$. The group of all such isometries has order:
$$|G| = 4^n n!$$
For $n=2$, this gives exactly $4^2 \cdot 2! = 32$ isometries. This provides an exact characterization of the discrete isometry group on this host.

---

## 4. Quantum Channels and Population Transport

### 4.1 Population Action of Channels
Let $\Phi: M_n(\mathbb{C}) \to M_n(\mathbb{C})$ be a completely positive trace-preserving (CPTP) map with Kraus representation $\Phi(\rho) = \sum_k A_k \rho A_k^*$. For a classical probability vector $p \in \Delta^n$, its diagonal embedding is $\operatorname{Diag}(p)$. The output diagonal report is given by a column-stochastic matrix $K_\Phi$:
$$\operatorname{diag}(\Phi(\operatorname{Diag}(p))) = K_\Phi p,$$
where the transition kernel elements are:
$$K_\Phi(j \mid i) = \sum_k |\langle j | A_k | i \rangle|^2.$$

### 4.2 Failure of Population Summaries to Preserve Composition
While individual channels induce population transitions on diagonal inputs, the population summary map $\Phi \mapsto K_\Phi$ does not preserve channel composition:
$$K_{\Phi_2 \circ \Phi_1} \ne K_{\Phi_2} K_{\Phi_1} \quad \text{in general}.$$

**Counterexample (Hadamard Evolution):** Let $H = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$. As a unitary channel $\Phi_H(\rho) = H \rho H^*$, its population kernel is:
$$K_H = \frac{1}{2}\begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}.$$
Since $H^2 = I$, the two-step channel is the identity: $\Phi_{H^2} = \operatorname{id}$, so $K_{H^2} = I$. However, the product of the population summaries is idempotent:
$$K_H^2 = \left[\frac{1}{2}\begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}\right]^2 = \frac{1}{2}\begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix} = K_H \ne I.$$
Multiplying population summaries models complete dephasing between stages, discarding the off-diagonal coherence necessary to reconstruct the identity return.

### 4.3 Complexity Scope Fence
The two-sign mixing example demonstrates failure of classical report reconstruction; it does not demonstrate quantum computational advantage. Stabilizer circuits (such as Clifford group operations on stabilizer states) generate interference and non-descending readouts, yet admit efficient classical simulation in polynomial time by the Gottesman–Knill theorem.

---

## 5. Trace-Zero Duality and Contraction

### 5.1 Exact Trace-Zero Duality
In $\ell^1$ transport geometry, differences of normalized probability distributions live in the trace-zero subspace $V_0 = \{x \in \mathbb{R}^n : \sum_i x_i = 0\}$.

**Theorem 5.1 (Trace-Zero $\ell^1$ / Diameter Duality).** For any $x \in \mathbb{R}^n$ satisfying $\sum_i x_i = 0$:
$$\frac{1}{2}\sum_{i=1}^n |x_i| = \max_{\operatorname{diam}(m) \le 1} \sum_{i=1}^n m_i x_i,$$
where $\operatorname{diam}(m) = \max_i m_i - \min_i m_i \le 1$.

*Proof.*  
For any $m$ with $\operatorname{diam}(m) \le 1$, let $c = \frac{1}{2}(\max_i m_i + \min_i m_i)$ be its midpoint. Then $|m_i - c| \le 1/2$ for all $i$. Since $\sum_i x_i = 0$, we have $\sum_i c x_i = 0$, so:
$$\sum_i m_i x_i = \sum_i (m_i - c) x_i \le \sum_i |m_i - c| |x_i| \le \frac{1}{2}\sum_i |x_i|.$$
Attainment: Set $m_i = \frac{1}{2}\operatorname{sign}(x_i)$ (with $\operatorname{sign}(0) = 1$). Then $\max m_i \le 1/2$ and $\min m_i \ge -1/2$, so $\operatorname{diam}(m) \le 1$. Its pairing evaluates to:
$$\sum_i m_i x_i = \sum_i \frac{1}{2}\operatorname{sign}(x_i) x_i = \frac{1}{2}\sum_i |x_i|.$$
This completes the proof. $\blacksquare$

*(Correction note: Earlier summaries claiming that the half-$\ell^1$ ball is the "greatest bounded trace-zero set" are false, as arbitrary singletons in $V_0$ are bounded and their union is unbounded. Theorem 5.1 is the verified mathematical statement.)*

### 5.2 Stochastic $\ell^1$ Contraction
Every column-stochastic matrix $T$ is a non-expansion on $\ell^1$: $\|Tx\|_1 \le \|x\|_1$. On trace-zero vectors $x \in V_0$, $T$ contracts according to the Dobrushin coefficient:
$$\|Tx\|_1 \le \eta(T) \|x\|_1, \qquad \eta(T) = \frac{1}{2} \max_{j, k} \sum_i |T_{ij} - T_{ik}| \le 1.$$
Strict contraction ($\eta(T) < 1$) holds if and only if $T$ has no disjoint supports across columns.

---

## 6. Finite Transport Appendix: Cycles, Commutators, and Holonomy

We consolidate the finite algebraic transport constructions:

### 6.1 Flatness versus Global Path Independence
Let $G = (V, E)$ be a finite cell complex with 1-cochain connection $a \in C^1(G, G_{\text{gauge}})$.  
1. Local flatness is the condition $d_1 a = 0$ on all 2-cells (faces).  
2. Local flatness guarantees path independence for homotopy-equivalent paths, but does not imply global path independence when the 1-homology $H_1(G)$ is non-trivial (e.g. on a discrete torus). The holonomy around a non-contractible loop $\gamma \in Z_1(G)$ can be non-trivial even when $d_1 a = 0$ everywhere. Global path independence requires $a \in \operatorname{im}(d_0)$ (global pure gauge).

### 6.2 Zero Interference versus Non-Trivial Holonomy
In a two-path interference setup with phase difference $\theta$, the interference modulation is proportional to $\cos \theta$. At $\theta = \pi/2$, $\cos(\pi/2) = 0$, so the interference term vanishes. However, the connection holonomy $e^{i\pi/2} = i \ne 1$ is non-trivial. Trivial interference readout does not imply trivial holonomy.

### 6.3 Cochain Identities and Bianchi Degree
For an abelian connection $a \in C^1$, curvature $F = d_1 a \in C^2$ is gauge-invariant:
$$d_1(a + d_0 f) = d_1 a + d_1 d_0 f = d_1 a,$$
which depends on $d_1 d_0 = 0$. The Bianchi identity is a statement in degree 3:
$$d_2 F = d_2 d_1 a = 0,$$
which depends on $d_2 d_1 = 0$. The cohomology group $H^1 = \ker d_1 / \operatorname{im} d_0$ classifies flat connections modulo gauge equivalence; it does not measure curvature.

### 6.4 Quaternion Commutators and Representation Fidelity
In the quaternion group $Q_8 = \{\pm 1, \pm i, \pm j, \pm k\}$, the commutator evaluates to:
$$i j i^{-1} j^{-1} = i j (-i) (-j) = k (-k) = -1.$$
However, in the adjoint (vector) representation where quaternions act by conjugation on $\operatorname{Im}(\mathbb{H}) \cong \mathbb{R}^3$:
$$v \mapsto q v q^{-1},$$
the non-trivial element $-1$ acts as the identity: $(-1) v (-1)^{-1} = v$. Consequently, loop holonomy carrying $-1$ on the group carrier becomes invisible in the vector representation.

---

## 7. Structure of Assumptions: Three Remaining Targets

Rather than cataloging revision histories or counting external modules, we structure the remaining assumptions of quantum mechanics into three precise mathematical questions:

### 7.1 Which scalar and pairing assumptions remain to be justified?
- **Field Completeness:** Replacing $\mathbb{Z}[i]$ or exact fractions with $\mathbb{C}$ requires topological completeness and continuous limits.
- **Born Measure Uniqueness:** Normalization on a single context does not force the $p=2$ power. Gleason's theorem derives quadratic uniqueness only by imposing frame-function non-contextuality across all orthogonal bases in dimension $n \ge 3$. On a 2-label carrier, Gleason's dimension condition fails, and alternative pairings remain admissible.

### 7.2 Which transformations and composite systems are admitted?
- **Combining Systems:** On cartesian coordinate products, a bilinear integer-homogeneous Kronecker-normalized map is uniquely the tensor product. Without requiring injectivity on composite labels, weaker combining interfaces permit non-tensor rivals. Tensor product uniqueness remains an imported composition axiom.
- **Dynamics:** Discrete transitions permit matrix powers $M^k$. Generating continuous one-parameter groups $U(t) = e^{-iHt}$ requires importing continuous time $\mathbb{R}$ and self-adjoint generators $H = H^*$.

### 7.3 Which predictions can be computed from retained reports?
- **Report Predictability:** By Theorem 3.2, output intensities can be computed from input intensities if and only if each row of the evolution matrix has at most one non-zero entry. All non-trivial mixing operations destroy report-level determinism.

---

## 8. Summary of Retained Claims

| Question | Mathematical Criterion | Preserved Status |
|---|---|---|
| Report Descent | Row-sparsity ($A_{bj}\overline{A_{bk}} = 0$ for $j \ne k$) | Theorem 3.2 (exact criterion) |
| Scaled Mixing | $M^*M = 2I$, $q(M\psi_\pm) = (4,0), (0,4)$ | Preserved integer Hadamard |
| Channel Composition | $K_{\Phi_2\circ\Phi_1} \ne K_{\Phi_2} K_{\Phi_1}$ | Counterexample $K_H^2 \ne K_{H^2}$ |
| Trace-Zero Duality | $\frac{1}{2}\|x\|_1 = \max_{\operatorname{diam}(m)\le 1} \langle m, x \rangle$ | Theorem 5.1 (centered duality) |
| Contextuality | $\operatorname{coker} A \cong \mathbb{F}_2$ parity obstruction | Delegated to [QM-120](file:///c:/Users/a343o/source/repos/the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/qm_120_mermin_peres_contextuality_cochain_obstruction.md) |
| Cochain Residuals | Kernel/image exactness & minimum weight | Delegated to [QM-212](file:///c:/Users/a343o/source/repos/the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/qm_212_microsoft_majorana_problem.md) |
