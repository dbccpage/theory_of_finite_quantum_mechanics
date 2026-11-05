# Exact Refutation of Finite-M Positivity (Gate E)

**AuthorityEffect:** None.

## Witnessed Point
The local receipt `code/gate_e_exact_counterexample_receipt.json` records one point: $L=4$, $M=1$, $r=1/10$. At that point the discrete response matrix
\[
G^{(2)}_{4,1}(j, x; k, y) = 4\,\partial_{z_{j,x}}\partial_{z_{k,y}} \log X_{4,1}(z)\Big|_{z=0}
\]
is not positive semidefinite. The receipt eigenvalue is $\lambda_{\min} = -1/706440$. The receipt does not record $\lambda_{\min} \sim -\frac{1}{9} r^4$ on $(0, 1/192]$, and it does not record indefiniteness for every finite $M$.

---

## Exact Rational Proof on 16-Dimensional Fock Space

Let the 16 basis states of $\mathcal{F} = (\mathbb{C}^2)^{\otimes 4}$ be labeled by occupation numbers $|n_0, n_1, n_2, n_3\rangle$.
The operators are:
- $P_x = \frac{1}{2}(n_x + n_{x+1} - 2n_x n_{x+1} + c_x^\dagger c_{x+1} + c_{x+1}^\dagger c_x)$, with periodic CAR boundary conditions.
- $a_x = (-1)^x(n_x - 1/2)$.
- $T_0(q) = (1 + r P_0)(1 + r P_2)$, $T_1(q) = (1 + r P_1)(1 + r P_3)$, with $q = 1 + r$.
- $D_j(z) = \exp[\frac{1}{2}\sum_x z_{j,x} a_x]$.

### Characteristic Polynomial Evaluation at $r = 1/10$ ($q = 11/10$)
Evaluating $X_0 = q^{-1} \operatorname{Tr}[T_1 T_0] = \frac{17661}{1100}$ and the second derivatives $G^{(2)}_{4,1}$, the exact characteristic polynomial over $\mathbb{Q}$ factors into roots:
\[
\operatorname{Roots}(G^{(2)}_{4,1}) = \left\{ \frac{21}{40}, \; \frac{10}{21}, \; \frac{420}{841} \text{ (mult 2)}, \; 0 \text{ (mult 3)}, \; \mathbf{-\frac{1}{706440}} \right\}.
\]

### Explicit Counterexample Vector
The eigenvector corresponding to $\lambda_{\min} = -\frac{1}{706440}$ is the spatially uniform, temporally staggered test vector:
\[
v = (-1, -1, -1, -1, \; +1, +1, +1, +1)^T \in \mathbb{R}^8.
\]
The exact rational quadratic form is:
\[
v^\top G^{(2)}_{4,1} v = -\frac{1}{88305} \approx -1.1324 \times 10^{-5} < 0.
\]

---

## Conclusion
1. **Witnessed refutation.** At $L=4$, $M=1$, $r=1/10$, $G^{(2)}_{4,1}$ has eigenvalue $-1/706440$ and $v^\top G v = -1/88305$ for $v = (-1,-1,-1,-1,+1,+1,+1,+1)^\top$. The receipt field `is_positive_semidefinite` is false.
2. **Not in the receipt.** The receipt does not show that no finite-$M$ discrete Gaussian exists, and it does not show $\lambda_{\min} \sim -r^4/9$ on $(0, 1/192]$. Values at $r=1/20$ and $r=1/40$ are not in the receipt.
