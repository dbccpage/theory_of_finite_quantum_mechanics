# Target A2: Singular Cusp Branching & Variety Decomposition

AuthorityEffect: None.
Firewall: `stated region only; mints no authority`

## 1. Exact Algebraic Factorization

The $3 \times 3$ corner determinant factors as a shifted $2 \times 2$ determinant:
$$\det(M) = \det \begin{pmatrix} 1 & 1 & 1 \\ 1 & a & b \\ 1 & c & d \end{pmatrix} = (a - 1)(d - 1) - (b - 1)(c - 1)$$

The singular locus $\det(M) = 0$ is exactly the Segre quadric:
$$(a - 1)(d - 1) = (b - 1)(c - 1)$$

## 2. Rational Parameterization of the Non-Trivial Branch

For $a \neq 1$, the non-trivial variety ($a \neq c, b \neq d$) is parameterized by:
$$d = 1 + \frac{(b - 1)(c - 1)}{a - 1}$$

### Symbol Game Verification on Non-Trivial Points

| $a$ | $b$ | $c$ | $d$ | Non-Trivial? | $\det$ | $\Phi_1$ | Verdict |
|---|---|---|---|---|---|---|---|
| `2` | `3` | `4` | `7` | True | `0` | `0` | **ADMITTED** |
| `3/2` | `5/3` | `7/5` | `23/15` | True | `0` | `0` | **ADMITTED** |
| `-1` | `2` | `-3` | `3` | True | `0` | `0` | **ADMITTED** |
| `1/3` | `2/5` | `3/7` | `17/35` | True | `0` | `0` | **ADMITTED** |
| `4/5` | `6/7` | `8/9` | `58/63` | True | `0` | `0` | **ADMITTED** |

## 3. Negative Controls (Off-Variety Perturbations)

Perturbing $d$ away from the variety by $\delta$ induces non-zero determinant and non-zero $\Phi_1 = |\det|$:

| $\delta$ | $\det$ | $\Phi_1$ | $\Phi_1 = |\det|$ | Verdict |
|---|---|---|---|---|
| `1/10` | `1/10` | `1/10` | True | **REFUSED** |
| `-1/5` | `-1/5` | `1/5` | True | **REFUSED** |
| `1` | `1` | `1` | True | **REFUSED** |
| `2` | `2` | `2` | True | **REFUSED** |

## 4. Connection to Deltoid Cusp Confluence

When $(a, b, c, d)$ lie on the unit circle $e^{i \theta_j}$, the condition $(a - 1)(d - 1) = (b - 1)(c - 1)$ reduces via $e^{i \theta} - 1 = 2i e^{i \theta / 2} \sin(\theta / 2)$ to:
$$\sin(\theta_1 / 2) \sin(\theta_4 / 2) = \sin(\theta_2 / 2) \sin(\theta_3 / 2)$$
$$\theta_1 + \theta_4 \equiv \theta_2 + \theta_3 \pmod{2\pi}$$

This specifies the singular boundary locus where corner coordinates degenerate, completing the algebraic foundation of Target A2.
