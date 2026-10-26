# MIMO-V2.6-PRO: Volume- and Time-Slice-Uniform Mixed-Cumulant Bound for the Meron Chain (G3)

**AuthorityEffect:** None.

## Verdict: OPEN

The target bound is *not* established. The reduction of the cumulant claim to a uniform analyticity/clustering statement is complete and checkable (Sections 2–3, with explicit constants). What fails is the model-specific step: the uniform connected-correlation (Ursell) estimate for the source-inserted, wrapping, checkerboard transfer product with independent half-step time labels, uniform in $L$ and $M$.

---

## 1. Definitions and Conventions

$$L \in 2\mathbb{Z}_{\ge 4}, \qquad M \ge 1, \qquad q = 1 + \frac{r}{M}, \quad 0 \le r \le \frac{1}{192}.$$

Full Fock space $\mathcal{F} = (\mathbb{C}^2)^{\otimes L}$, $\dim \mathcal{F} = 2^L$.
Staggered bounded operators:
$$a_x = (-1)^x \left(n_x - \frac{1}{2}\right), \qquad a_x = a_x^\dagger, \qquad \|a_x\| = \frac{1}{2}, \qquad a_x^2 = \frac{1}{4}\mathbb{1}.$$

Checkerboard transfer layers $T_j$, $j=0, \dots, 2M-1$ with periodic CAR hop signs.
Sources inserted before layer $j$:
$$Z_{L,M}(z) = q^{-LM/4} \operatorname{Tr} \prod_{j=2M-1}^0 \left[ T_j e^{V_j(z)} \right], \qquad V_j(z) = \frac{1}{2M}\sum_x z_{j,x} a_x.$$

Algebraic cumulants:
$$G_n\left((j_1, x_1), \dots, (j_n, x_n)\right) := (2M)^n \frac{\partial^n \log Z}{\partial z_{j_1,x_1} \dots \partial z_{j_n,x_n}}\Big|_{z=0}.$$

Smeared field:
$$\Phi_{L,M}(\Psi) = \frac{1}{2M\sqrt{L}}\sum_{j,x} \Psi\left(\frac{j}{2M}, \frac{x}{L}\right) a_x(s_j), \qquad \kappa_n(\Phi_{L,M}(\Psi)) = \frac{1}{(2M\sqrt{L})^n}\sum_{\text{tuples}} \Psi_1 \dots \Psi_n G_n.$$

---

## 2. What Analyticity Alone Gives — And Why It Is NOT Enough

Assume provisionally the requested analyticity statement (A):
$\exists R_* > 0, C < \infty$ independent of $L, M$ with $Z(z) \ne 0$ for $|z_{j,x}| \le R_*$, a consistently branched $\log Z$, and $|\log Z(z) - \log Z(0)| \le CL$.

Multivariate Cauchy estimate on the polydisk of radius $R_*$:
$$\left| \frac{\partial^n \log Z}{\partial z_{j_1,x_1} \dots \partial z_{j_n,x_n}}(0) \right| \le \frac{n! C L}{R_*^n}.$$

Summing over all $(2ML)^n$ tuples **without any decay in separations**:
$$\big|\kappa_n(\Phi_{L,M}(\Psi))\big| \le L^{-n/2}(2M L B)^n \frac{n! C L}{R_*^n} = n! C \left(\frac{2MB}{R_*}\right)^n L^{1 + n/2}.$$

The target is $O(L^{1 - n/2})$; this estimate is worse by $(2M)^n L^n$. **Hence (A) alone does not imply the cumulant bound.** Spacetime cluster decay is irreplaceable.

---

## 3. The Missing Lemma (Lemma A)

> **Lemma A (missing).** There exist $A < \infty$ and, for every $n \ge 1$ and every spacetime site $a_1$, the uniform Ursell bound:
> $$\sum_{a_2, \dots, a_n} |G_n(a_1, \dots, a_n)| \le A^{n-1}(n-1)!, \quad a_i = (j_i, x_i) \text{ distinct},$$
> with $A$ independent of $L \ge 4$ and $M \ge 1$.

- **Corollary 1 (Lemma A $\implies$ Analyticity A):**
  $$|\log Z(z) - \log Z(0)| \le CL, \qquad C = \frac{R_*}{1 - \frac{A R_*}{2M}} \le 2R_* \quad \text{for } R_* \le \frac{1}{A}.$$
- **Corollary 2 (Lemma A $\implies$ Cumulant Bound):**
  $$|\kappa_n(\Phi_{L,M}(\Psi))| \le 2(n-1)!(A\|\Psi\|_\infty)^{n-1}\|\Psi\|_\infty L^{1 - n/2} \quad (n \ge 2),$$
  uniformly in $M$. In particular, $\kappa_n = O(L^{1 - n/2})$ for $n \ge 3$, and $|\kappa_2| = O(1)$.

---

## 4. The Five Structural Obstructions

1. **Signed Histories:** The weights are signed; operator norm bounds grow like $2^L e^{R_* L/2}$.
2. **Range-$L$ CAR String:** The wrapping gate on $(L-1, 0)$ is $(2\text{-site gate}) \times \prod_{x < L-1}(1 - 2n_x)$, an extensive range-$L$ operator that defeats finite-range zero-free theorems.
3. **Parity Sector Instability:** $Z = Z_+ + Z_-$. Zero-freeness is not stable under addition; destructive complex phase interference can create Lee-Yang zeros.
4. **Independent Time Labels:** Destroys the repeated transfer matrix $\mathcal{T}^M$ / Perron-Frobenius mechanism of the static-source theorem.
5. **No Implied Gaussianity:** The $(n-1)!$ growth does not control the moment generating function; no convergence in law is implied.
