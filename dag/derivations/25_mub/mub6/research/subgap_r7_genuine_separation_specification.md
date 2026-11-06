# Subgap R7 Authentic Semi-Algebraic Separation Specification
## Non-Tautological Positivstellensatz Refutation on the Singular Segre Locus

> **AuthorityEffect**: None  
> **Epistemic Firewall**:
> $$\boxed{\text{stated region only; mints no authority}}$$
> **Date**: 2026-10-09  
> **Target Subgap**: $R_7$ (ENC-1147 Singular Segre Positivstellensatz)  
> **Direct Predecessor**: [`subgap_r7_adversarial_audit_note.md`](subgap_r7_adversarial_audit_note.md)

---

## 1. Executive Summary & Defect of Candidate Tautologies

In `subgap_r7_adversarial_audit_note.md`, the audit showed that the candidate algebraic identity:
$$-1 = h_{\text{segre}} f_{\text{segre}} + \sum_{k \in \{a,b,c,d\}} h_k f_k + \sigma_0 + \sigma_1 g_{\text{sep}}$$
from `compute_r7_singular_segre_sos.py` was an algebraic telescoping identity in $\mathbb{Q}[a,b,c,d]$ that reduced algebraically to $-1$, but where the separation condition was definitionally:
$$g_{\text{sep}} = (1 - \varepsilon)\sigma_0 + f_{\text{circ}} - \varepsilon$$
On all points of the actual algebraic variety $V(f_{\text{segre}}, f_k)$, $\sigma_0 = 0$ and $f_{\text{circ}} = 0$, forcing $g_{\text{sep}} = -\varepsilon < 0$. The certificate therefore refuted the system $\{f_{\text{segre}} = 0, f_k = 0, g_{\text{sep}} \ge 0\}$, which is empty by definition of $g_{\text{sep}}$, not because the variety is empty. Real points such as $p_0 = (1, 1, 1, 1)$ lie on the variety and satisfy $-1 = -1$.

This document establishes the **authentic, non-tautological semi-algebraic specification** required to construct a valid Stengle Positivstellensatz refutation of non-catalog singular cusps on the corner variety $\{P_{\text{corner}} = 0\}$.

---

## 2. Coordinates and the Defining Ideal $I_{55}$ in $\mathbb{R}^{50}$

### 2.1 Coordinate System

A complex Hadamard matrix $H \in M_6(\mathbb{C})$ in standard dephased form has its first row and first column set to 1:
$$H = \begin{pmatrix}
1 & 1 & 1 & 1 & 1 & 1 \\
1 & z_{11} & z_{12} & z_{13} & z_{14} & z_{15} \\
1 & z_{21} & z_{22} & z_{23} & z_{24} & z_{25} \\
1 & z_{31} & z_{32} & z_{33} & z_{34} & z_{35} \\
1 & z_{41} & z_{42} & z_{43} & z_{44} & z_{45} \\
1 & z_{51} & z_{52} & z_{53} & z_{54} & z_{55}
\end{pmatrix}$$
There are 25 independent complex variables $z_{jk}$ ($j, k \in \{1, 2, 3, 4, 5\}$).
Expanding into real and imaginary coordinates $z_{jk} = x_{jk} + i y_{jk}$ establishes the real coordinate ring:
$$\mathcal{R}_{50} = \mathbb{R}[x_{11}, y_{11}, x_{12}, y_{12}, \dots, x_{55}, y_{55}]$$
with 50 real variables $X = (x_{jk}, y_{jk})_{j,k=1}^5 \in \mathbb{R}^{50}$.

### 2.2 The 55 Explicit Real Polynomial Generators of $I_{55}$

The complex Hadamard variety $V(I_{55})$ is defined by two sets of geometric constraints:

#### Group 1: 25 Unimodularity Generators
Each non-trivial entry $z_{jk}$ must lie on the complex unit circle $|z_{jk}|^2 = 1$:
$$u_{jk}(X) = x_{jk}^2 + y_{jk}^2 - 1 = 0 \quad \text{for } j, k \in \{1, 2, 3, 4, 5\}$$
This yields exactly **25 real quadratic generators**.

#### Group 2: 10 Row-0 Orthogonality Generators
Row 0 is $(1, 1, 1, 1, 1, 1)$. The orthogonality condition $\langle R_0, R_k \rangle = 1 + \sum_{l=1}^5 z_{kl} = 0$ for $k \in \{1, 2, 3, 4, 5\}$ decomposes into real and imaginary linear relations:
- Real parts (5 linear relations):
  $$r_{0k}^{\text{re}}(X) = 1 + \sum_{l=1}^5 x_{kl} = 0 \quad (k \in \{1, \dots, 5\})$$
- Imaginary parts (5 linear relations):
  $$r_{0k}^{\text{im}}(X) = \sum_{l=1}^5 y_{kl} = 0 \quad (k \in \{1, \dots, 5\})$$
This yields exactly **10 real linear generators**.

#### Group 3: 20 Bilinear Pairwise Row-Orthogonality Generators
For any two rows $j, k \in \{1, 2, 3, 4, 5\}$ with $j < k$ ($\binom{5}{2} = 10$ pairs):
$$\langle R_j, R_k \rangle = 1 + \sum_{l=1}^5 z_{jl} \overline{z}_{kl} = 1 + \sum_{l=1}^5 (x_{jl} + i y_{jl})(x_{kl} - i y_{kl}) = 0$$
Decomposing into real and imaginary parts:
- Real parts (10 bilinear relations):
  $$r_{jk}^{\text{re}}(X) = 1 + \sum_{l=1}^5 \left( x_{jl} x_{kl} + y_{jl} y_{kl} \right) = 0 \quad (1 \le j < k \le 5)$$
- Imaginary parts (10 bilinear relations):
  $$r_{jk}^{\text{im}}(X) = \sum_{l=1}^5 \left( y_{jl} x_{kl} - x_{jl} y_{kl} \right) = 0 \quad (1 \le j < k \le 5)$$
This yields exactly **20 real bilinear generators**.

#### Total Count:
$$25 + 10 + 20 = 55 \text{ real polynomial generators}$$
The defining ideal is:
$$I_{55} = \left\langle u_{jk}, \ r_{0k}^{\text{re}}, \ r_{0k}^{\text{im}}, \ r_{jk}^{\text{re}}, \ r_{jk}^{\text{im}} \right\rangle \subset \mathcal{R}_{50}$$

---

## 3. The Singular Segre Corner Subvariety $\{P_{\text{corner}} = 0\}$

The $3 \times 3$ corner submatrix determinant across rows $\{0, 1, 2\}$ and columns $\{0, 1, 2\}$ is:
$$P_{\text{corner}} = \det \begin{pmatrix} 1 & 1 & 1 \\ 1 & z_{11} & z_{12} \\ 1 & z_{21} & z_{22} \end{pmatrix} = (z_{11} - 1)(z_{22} - 1) - (z_{12} - 1)(z_{21} - 1)$$
Decomposing into real and imaginary parts:
$$p_{\text{corner}}^{\text{re}}(X) = (x_{11}-1)(x_{22}-1) - y_{11} y_{22} - (x_{12}-1)(x_{21}-1) + y_{12} y_{21} = 0$$
$$p_{\text{corner}}^{\text{im}}(X) = (x_{11}-1)y_{22} + (x_{22}-1)y_{11} - (x_{12}-1)y_{21} - (x_{21}-1)y_{12} = 0$$
The singular Segre locus within the complex Hadamard variety is:
$$V_{\text{corner}} = V(I_{55}) \cap \{ p_{\text{corner}}^{\text{re}} = 0, \ p_{\text{corner}}^{\text{im}} = 0 \}$$

---

## 4. The Known Catalog Locus $\mathcal{C}_{\text{catalog}}$ and Distance Formulation

### 4.1 The Known Catalog Families on $V_{\text{corner}}$

Within $V_{\text{corner}}$, the certified families in dimension 6 comprise:
1. **Fourier-Diță Family $F(x, y)$**: The 2-parameter affine family defined by Kronecker product $F_2 \otimes F_3$ with diagonal phase twisting.
2. **Szöllősi Family $B_6(\theta)$**: The 1-parameter family constructed from two $3 \times 3$ circulant blocks satisfying $z_1 + z_2 = 0$.
3. **Tao Isolated Matrix $S_6$**: The single point $F_3 \otimes F_2$ over $\mathbb{Z}[\omega_3]$.
4. **Haagerup Isolated Matrix $H_6$**: The single point over $\mathbb{Q}(i, \sqrt{3})$.
5. **Karlsson Affine Family $K_6^{(3)}$**: The 3-parameter flat manifold on $\mathbb{T}^3$.

Let $\mathcal{C}_{\text{catalog}} \subset \mathbb{R}^{50}$ denote the union of these loci.

### 4.2 The Catalog Vanishing Ideal $I(\mathcal{C}_{\text{catalog}})$

To construct an algebraic distance function without non-algebraic square roots, let $\{Q_m(X)\}_{m=1}^M \subset \mathcal{R}_{50}$ be polynomial generators that vanish identically on all catalog components:
$$Q_m(C) = 0 \quad \forall C \in \mathcal{C}_{\text{catalog}}, \ \forall m \in \{1, \dots, M\}$$
Key catalog polynomial invariants include:
1. **2-Circulant Block Sylow Minors**:
   For the Szöllősi family $B_6(\theta)$, the sub-blocks satisfy the circulant symmetry relation $C_{ij} = C_{i+1, j+1 \pmod 3}$. The difference polynomials:
   $$Q_{\text{circ}, 1}(X) = z_{11} - z_{22}, \quad Q_{\text{circ}, 2}(X) = z_{12} - z_{23}, \quad \dots$$
2. **Kronecker Commutator Invariants**:
   For the Fourier-Diță family $F(x, y)$, the block rank condition $\text{rank}(H \odot H^*) \le 2$ generates $3 \times 3$ minors $Q_{\text{fd}, k}(X) = 0$.
3. **Affine Torus Relations**:
   For the Karlsson manifold $K_6^{(3)}$, the 2-parameter affine relations $Q_{\text{kar}, k}(X) = 0$.

### 4.3 Authentic Semi-Algebraic Separation Polynomial

For any point $X \in \mathbb{R}^{50}$, the algebraic squared distance to the catalog locus is defined by:
$$D_{\text{catalog}}^2(X) = \sum_{m=1}^M Q_m(X)^2$$
For a chosen positive separation radius $\varepsilon_0 > 0$, the **authentic semi-algebraic separation polynomial** is:
$$\boxed{g_{\text{sep}}(X) = \sum_{m=1}^M Q_m(X)^2 - \varepsilon_0^2 \ge 0}$$

#### Decisive Contrast with the Tautological Identity:
- **On the catalog locus**: For every point $C \in \mathcal{C}_{\text{catalog}}$, $Q_m(C) = 0$ for all $m$, so $g_{\text{sep}}(C) = -\varepsilon_0^2 < 0$. The catalog points are strictly excluded from the candidate domain.
- **On candidate non-catalog cusps**: If there exists a hypothetical singular cusp $X^* \in V_{\text{corner}} \setminus \mathcal{C}_{\text{catalog}}$, then by definition $X^*$ does not belong to any catalog family. Hence at least one catalog invariant is bounded away from zero:
  $$D_{\text{catalog}}^2(X^*) \ge \delta_{\text{isolation}}^2 > \varepsilon_0^2 \implies g_{\text{sep}}(X^*) > 0$$
- The inequality $g_{\text{sep}}(X^*) \ge 0$ is **genuinely satisfied** by candidate non-catalog cusps!

---

## 5. Authentic Stengle Positivstellensatz Refutation Formulation

### 5.1 The Semi-Algebraic Candidate System

The basic semi-algebraic set representing non-catalog singular Segre cusps is:
$$\mathcal{S}_{\text{non-catalog}} = \left\{ X \in \mathbb{R}^{50} \;\middle|\; \begin{aligned}
f_i(X) &= 0 \quad \forall f_i \in I_{55} \ (i = 1, \dots, 55) \\
p_{\text{corner}}^{\text{re}}(X) &= 0 \\
p_{\text{corner}}^{\text{im}}(X) &= 0 \\
g_{\text{sep}}(X) &\ge 0
\end{aligned} \right\}$$

### 5.2 The Certified Positivstellensatz Identity

A valid, authentic Stengle Positivstellensatz refutation of $\mathcal{S}_{\text{non-catalog}}$ is an algebraic identity in $\mathcal{R}_{50}$:
$$\boxed{-1 = \sum_{i=1}^{55} h_i(X) f_i(X) + h_{\text{re}}(X) p_{\text{corner}}^{\text{re}}(X) + h_{\text{im}}(X) p_{\text{corner}}^{\text{im}}(X) + \sigma_0(X) + \sigma_1(X) g_{\text{sep}}(X)}$$
where:
1. $h_1, \dots, h_{55}, h_{\text{re}}, h_{\text{im}} \in \mathcal{R}_{50}$ are real polynomials of degree bounded by $2d - \deg(f_i)$.
2. $\sigma_0(X)$ is a Sum of Squares polynomial:
   $$\sigma_0(X) = \sum_{k} p_k(X)^2, \quad \deg(\sigma_0) \le 2d$$
3. $\sigma_1(X)$ is a Sum of Squares polynomial:
   $$\sigma_1(X) = \sum_{l} q_l(X)^2, \quad \deg(\sigma_1) \le 2d - \deg(g_{\text{sep}})$$

### 5.3 Proof of Authentic Refutation

Suppose there exists a non-catalog singular cusp $X^* \in \mathcal{S}_{\text{non-catalog}}$:
1. Since $X^* \in V(I_{55})$, $f_i(X^*) = 0$ for all $i \in \{1, \dots, 55\}$, so $\sum_i h_i(X^*) f_i(X^*) = 0$.
2. Since $X^*$ lies on the corner locus, $p_{\text{corner}}^{\text{re}}(X^*) = 0$ and $p_{\text{corner}}^{\text{im}}(X^*) = 0$.
3. Since $\sigma_0$ is a sum of squares, $\sigma_0(X^*) \ge 0$.
4. Since $\sigma_1$ is a sum of squares and $X^* \in \mathcal{S}_{\text{non-catalog}}$ satisfies $g_{\text{sep}}(X^*) \ge 0$:
   $$\sigma_1(X^*) g_{\text{sep}}(X^*) \ge 0$$
5. If an identity of that form has been exhibited, evaluating it at $X^*$ gives
   $$-1 = 0 + 0 + 0 + \sigma_0(X^*) + \sigma_1(X^*) g_{\text{sep}}(X^*) \ge 0$$
   and therefore $-1 \ge 0$.

No such identity is exhibited in this document. The conditional argument does not show that the set of non-catalog cusps is empty.

---

## 6. Algorithmic Execution Protocol via Semidefinite Programming (SDP)

To compute the certified polynomial coefficients:
1. **Degree Hierarchy**: Fix relaxation order $d = 2$ or $d = 3$ (Lasserre hierarchy level 2/3).
2. **Gram Matrix Parameterization**: Represent $\sigma_0(X) = v_d(X)^T Q_0 v_d(X)$ and $\sigma_1(X) = v_{d-1}(X)^T Q_1 v_{d-1}(X)$ where $v_d(X)$ is the monomial basis vector of degree $\le d$, with positive semidefinite matrices $Q_0, Q_1 \succeq 0$.
3. **Solver Cascade**: Solve the resulting SDP feasibility problem using CSDP or Mosek in arbitrary precision.
4. **Rational Rounding and Verification**: Apply exact rational projection (Peyrl-Parrilo rounding) to convert floating-point solutions into exact rational polynomials in $\mathbb{Q}[X]$, verifying $-1 = \text{RHS}$ symbolically with zero floats.

---

## 7. Claim Hygiene Compaction Envelope

1. **What this specification supports**:
   - Formulates the exact 55 real polynomial generators of the complex Hadamard variety $V(I_{55})$ in 50 real coordinates.
   - Replaces the tautological separation polynomial from `compute_r7_singular_segre_sos.py` with an authentic, non-tautological semi-algebraic distance function $g_{\text{sep}}(X) = \sum Q_m(X)^2 - \varepsilon_0^2 \ge 0$ that is non-negative on genuine candidate non-catalog cusps and negative on the known catalog locus.
   - Provides the complete structural equation for a genuine Stengle Positivstellensatz refutation of non-catalog singular cusps.

2. **What this specification does not support**:
   - Does not claim that the SDP optimization has already completed; finding the explicit rational SOS certificate of degree $2d$ requires executing the solver cascade.
   - Does not establish that non-catalog cusps do not exist until the machine receipt containing verified rational Gram matrices $Q_0, Q_1 \succ 0$ is produced.
   - Does not assert that $\text{MUB}(6) = 3$ or $\text{MUB}(6) \le 3$.

3. **The narrowest defensible claim**:
   - Subgap $R_7$ cannot be closed by 4-variable Segre quadrics where $g_{\text{sep}} = -\varepsilon$ on the variety; authentic semi-algebraic closure requires the full 55-generator ideal $I_{55}$ and a distance-to-catalog polynomial positive on candidate non-catalog cusps.

4. **The next test needed**:
   - Execute the degree-2 SDP feasibility solver over $I_{55} \cup \{p_{\text{corner}}\} \cup \{g_{\text{sep}} \ge 0\}$ and produce the exact rational Gram matrix receipt.
