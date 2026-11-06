# DeepSeek Sprint 6: Final Closure of G3 — Boundary CAR String Polymer Representation & Spacetime Correlation Length

**Context & Baseline:**
- **G4 is 100% closed** by Sakana Fugu Ultra v2 (connected-interval linked-cluster expansion, uniform spatial moment summability, positive Matsubara modes, and static susceptibility).
- **Theorems A and B are established** (convergence in law to the continuous Gaussian field on $\mathbb{T}^2$ with quantitative rate $O(1/M) + O(1/L)$ for $C^1$ profiles).
- To achieve **100% formal acceptance on Prompt G3**, two specific model-specific derivations must be explicitly displayed rather than cited:
  1. The explicit handling of the range-$L$ boundary CAR string $\prod_{x < L-1}(1 - 2n_x)$ in the polymer expansion.
  2. The explicit discrete spacetime correlation lengths $\xi_x, \xi_\tau$ and the constant $A$ in MIMO's Lemma A.

---

## The Task for Sprint 6

Deliver the final, rigorous closure of **G3** by resolving the following three specific deliverables:

### 1. Polymer Expansion with the Periodic CAR Boundary String
On the periodic ring, the boundary bond operator is:
\[
P_{L-1} = \frac{1}{2}\left( n_{L-1} + n_0 - 2n_{L-1}n_0 + c_{L-1}^\dagger c_0 + c_0^\dagger c_{L-1} \right).
\]
In terms of local Fermi creation/annihilation operators, the hopping term across the boundary carries the parity string $c_0^\dagger c_{L-1} = \psi_0^\dagger \left( \prod_{x=1}^{L-2} (1 - 2n_x) \right) \psi_{L-1}$.
- Define the polymer activity $\zeta(P)$ for a polymer $P$ that wraps or intersects the boundary bond $(L-1, 0)$.
- Prove that the trace of the string operator $\prod_{x < L-1}(1 - 2n_x)$ against the bulk transfer layers satisfies the Kotecký-Preiss criterion without extensive $2^L$ norm explosions.
- Show explicitly that the non-local string factorizes or resums into the parity sector difference $\frac{X_+ - X_-}{X_+ + X_-} = O(e^{-c L})$, preserving the convergence radius $R_* = 1/64$ and free energy bound $|\log Z(z) - \log Z(0)| \le CL$.

### 2. Explicit Discrete Spacetime Correlation Decay & MIMO's Constant A
For the discrete two-point Ursell function $G_2\left((j, x), (k, y)\right) = (2M)^2 \frac{\partial^2 \log Z}{\partial z_{j,x} \partial z_{k,y}}\Big|_{z=0}$:
- Derive an explicit exponential decay bound in both space and time:
  \[
  \left| G_2\left((j, x), (k, y)\right) \right| \le C_0 \exp\left( - \frac{d_L(x, y)}{\xi_x} - \frac{d_{2M}(j, k)}{\xi_\tau} \right),
  \]
  valid for all $L \ge 4$, $M \ge 1$, and $0 \le r/M \le 1/192$.
- Give explicit numerical values or formulas for $\xi_x$ and $\xi_\tau$ in terms of $\theta = r$.
- Show that summing over all spacetime points $(k, y)$ yields the uniform bound:
  \[
  \sum_{(k, y) \ne (j, x)} \left| G_2\left((j, x), (k, y)\right) \right| \le A,
  \]
  with an explicit constant $A < \infty$ independent of $L$ and $M$.

### 3. Definitive Statement of the G3 Mixed-Cumulant Theorem
Display the complete, self-contained G3 theorem satisfying all clauses of the original prompt:
- Zero-free polydisk radius $R_* > 0$ and constant $C < \infty$ for $|\log Z(z) - \log Z(0)| \le CL$.
- Bound on mixed cumulants: $|\kappa_n(\Phi_{L,M}(\Psi))| \le C_n \|\Psi\|_\infty^n L^{1 - n/2}$ for all $n \ge 3$, uniformly in $M$.
- Exact statement regarding second moments: strict positivity and convergence to $Q_\theta(\Psi, \Psi)$ for $\Psi \in C^1$, alongside the finite-$M$ high-frequency negative mode bound $O(M^{-6})$.

**Rules:** State explicit assumptions, constants, and inequalities. No external files or web searches. Claim discipline: `AuthorityEffect: None`. Return **ESTABLISHED**, **REFUTED**, or **OPEN** with checkable derivations.
