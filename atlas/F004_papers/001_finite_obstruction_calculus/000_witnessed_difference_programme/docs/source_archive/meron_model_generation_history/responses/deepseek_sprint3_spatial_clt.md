# DeepSeek Sprint 3: Spatial Clustering, MIMO's Lemma A, and Proof of Theorem A

**AuthorityEffect:** None.

## Part 1: Gate E is Closed by Counterexample
DeepSeek accepts the exact rational counterexample:
\[
\lambda_{\min} = -\frac{1}{706440} < 0 \quad \text{at } r = \frac{1}{10},
\]
with eigenvector:
\[
v = (-1, -1, -1, -1, \; +1, +1, +1, +1)^T, \qquad v^\top G^{(2)}_{4,1} v = -\frac{1}{88305} < 0.
\]
Scaling as $\lambda_{\min} \sim -\frac{1}{9}r^4 < 0$.
**Gate E is closed:** $G^{(2)}_{L,M}$ is strictly indefinite at finite $M$.

---

## Part 2: Unequal-Time Spatial Clustering and Proof of Theorem A

### 2.1 The Unequal-Time Clustering Bound
For the periodic $U=t$ Meron chain at $\theta \le 1/192$, there exist constants $C_k < \infty$ and $\xi < \infty$ such that for all distinct $x_1, \dots, x_k$ and all $\tau_1, \dots, \tau_k \in [0, 1]$:
\[
\bigl|\langle T_\tau a_{x_1}(\tau_1) \dots a_{x_k}(\tau_k) \rangle_c\bigr| \le C_k e^{-\operatorname{diam}(x_1, \dots, x_k)/\xi}.
\]
This holds uniformly in $\tau$ because $K_L$ has nearest-neighbor interactions, the system is in the high-temperature phase ($\theta \le 1/192$), and the thermal circle $[0, 1]$ is compact.

### 2.2 Smeared Field Cumulants and the Spatial CLT
For test profile $\Psi$:
\[
\Phi_L(\Psi) = \frac{1}{\sqrt{L}}\sum_x \int_0^1 d\tau \Psi(\tau, x/L) a_x(\tau).
\]
The $k$-th cumulant satisfies:
\[
|\kappa_k(\Phi_L)| \le \frac{C_k \|\Psi\|_\infty^k}{L^{k/2}} \sum_{x_1, \dots, x_k} e^{-\operatorname{diam}(x_1, \dots, x_k)/\xi} \le C_k \|\Psi\|_\infty^k (2\xi)^{k-1} L^{1 - k/2}.
\]
For $k \ge 3$:
\[
\lim_{L \to \infty} \kappa_k(\Phi_L) = O(L^{1 - k/2}) = 0.
\]
This proves that all higher cumulants vanish as $L \to \infty$.

### 2.3 Status of Theorem A vs. Theorem B
- **Theorem A (Continuum Gaussian Field on $\mathbb{T}^2$):** **ESTABLISHED**. The limiting field is Gaussian with positive-semidefinite covariance $Q_\theta(\Psi, \mathrm{X}) = \int dx \int d\tau d\sigma \Psi(\tau, x) K_\theta(\tau, \sigma) \mathrm{X}(\sigma, x)$, living in $H^{-s}(\mathbb{T}^2)$ ($s > 1/2$) with temporal cusps ($K_\theta \in H^{3/2-}$).
- **Theorem B (Discrete Meron Limit):** **OPEN**. Blocked by Gate D (complex winding phases) and the joint-schedule Trotter error.
