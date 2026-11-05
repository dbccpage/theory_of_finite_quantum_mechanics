# DeepSeek Sprint 4: Gate D — Complex Winding Phases, Parity Sector Stability, and Lee-Yang Zero Obstruction

**Context & Baseline:**
- In Sprint 3, you proved **Theorem A** (continuous-time Gaussian field on $\mathbb{T}^2$ via spatial CLT) and accepted the Gate E refutation (finite-$M$ response matrix $G^{(2)}_{L,M}$ is strictly indefinite with $\lambda_{\min} \sim -(1/9)r^4 < 0$).
- Sakana Fugu Ultra v2 has independently closed **G4** by establishing the continuous-time thermodynamic two-point function via connected-interval linked-cluster expansion, proving strictly positive Matsubara modes $\hat k_\theta(j) = \frac{\theta^2}{8\pi^2 j^2} + O(\theta^3) > 0$ and static susceptibility $\chi(\theta) = 1/4 + \theta/8 + O(\theta^2)$.
- The sole remaining gate blocking **Theorem B** (discrete-to-continuum Meron spacetime field limit) and discrete **G3** is **Gate D**: ruling out or establishing complex winding phases and Lee-Yang zeros on the polydisk.

---

## The Task for Sprint 4

Work strictly on **Gate D**: prove or refute whether the discrete partition function $X_{L,M}(z)$ has zeros on the complex polydisk $|z_{j,x}| \le R_*$ ($R_* = 1/64$) for even $L \ge 4$, $M \ge 1$, and $0 \le r/M \le 1/192$.

### Mathematical Setting

On the periodic CAR Fock space $\mathcal{F} = (\mathbb{C}^2)^{\otimes L}$ of even length $L \ge 4$, with staggered charges $a_x = (-1)^x(n_x - 1/2)$, checkerboard transfer layers $T_j$, and independent sources:
\[
X_{L,M}(z) = q^{-LM/4} \operatorname{Tr}\left[ \prod_{j=2M-1}^0 T_j e^{V_j(z)} \right], \qquad V_j(z) = \frac{1}{2M}\sum_{x=0}^{L-1} z_{j,x} a_x, \quad q = 1 + \frac{r}{M}.
\]
The trace decomposes into even ($+$) and odd ($-$) fermion parity sectors:
\[
X_{L,M}(z) = X_{L,M,+}(z) + X_{L,M,-}(z), \qquad \xi_{L,M}(z) := \frac{X_{L,M,-}(z)}{X_{L,M,+}(z)}.
\]
For real sources $z=0$, both $X_+(0) > 0$ and $X_-(0) > 0$.

---

## Required Deliverables

Please address the following four specific questions with explicit derivations, bounds, and constants:

### 1. Parity Sector Ratio on the Complex Polydisk
Determine the behavior of the sector ratio $\xi_{L,M}(z) = X_{L,M,-}(z) / X_{L,M,+}(z)$ for $z \in \mathbb{C}^{2M \times L}$ with $\sup_{j,x} |z_{j,x}| \le 1/64$:
- Is $|\xi_{L,M}(z)|$ exponentially suppressed in $L$, i.e., $|\xi_{L,M}(z)| \le C e^{-c(\theta) L}$ for some $c(\theta) > 0$?
- If so, derive explicit constants $C$ and $c(\theta)$. (Notice that if $|\xi_{L,M}(z)| < 1$, then $X_{L,M}(z) = X_{L,M,+}(z)(1 + \xi_{L,M}(z)) \ne 0$ as long as the bulk sector $X_{L,M,+}$ is zero-free).
- If exponential suppression fails or if $|\xi_{L,M}(z)| \approx 1$, determine whether the complex phase $\operatorname{Arg}(\xi_{L,M}(z))$ can reach $\pm \pi$, creating destructive Lee-Yang cancellation.

### 2. Bulk Sector Zero-Freeness ($X_{L,M,+}$)
For the bulk sector $X_{L,M,+}(z)$:
- Does the Kotecký-Preiss or Dobrushin polymer criterion hold on the 2D spacetime checkerboard lattice for $r/M \le 1/192$ and $|z_{j,x}| \le 1/64$?
- State the polymer activity $\zeta(P)$ and demonstrate that the cluster condition $\sum_{P' \sim P} |\zeta(P')| e^{c|P'|} \le c|P|$ is satisfied.

### 3. Concrete Finite Check ($L=4, M=1$)
For the minimal system $L=4, M=1$ at $r=1/10$ and $r=1/192$:
- Can $X_{4,1}(z) = 0$ be achieved for any $|z_{j,x}| \le 1/64$?
- What is $\inf_{|z| \le 1/64} |X_{4,1}(z)| / X_{4,1}(0)$?

### 4. Gate D Verdict & Implications for Lemma A
- If Gate D is established (zero-free polydisk): does this suffice to extract MIMO's **Lemma A** (spacetime Ursell bound $\sum |G_n| \le A^{n-1}(n-1)!$) on the discrete lattice?
- If Gate D fails or remains open: state the exact obstruction and the minimal open lemma needed to resolve it.

**Rules:** State explicit assumptions, constants, and inequalities. No external files or web searches. Claim discipline: `AuthorityEffect: None`. Return **ESTABLISHED**, **REFUTED**, or **OPEN** with checkable derivations.
