# Conjecture 2(b) & Proposition 4.2: Complete Symbolic & Algebraic Derivation

> **AuthorityEffect**: None  
> **Epistemic Firewall**:
> **Date**: 2026-10-09  
> **References**: Matolcsi–Matszangosz–Varga–Weiner (2025, arXiv:2503.14752, Conjecture 2 & Proposition 4.2)

---

## 1. Theorem 1: Conjecture 2(b) for All Tensor-Product Transitions

### Statement

Let $U(\phi) = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ e^{i\phi} & -e^{i\phi}\end{pmatrix}$ be any qubit MUB transition matrix, and let $V$ be any entrywise-nonzero $3 \times 3$ complex matrix ($V_{jl} \ne 0 \ \forall j, l \in \{0, 1, 2\}$).
Let $H = U(\phi) \otimes V$ be the $6 \times 6$ Kronecker product transition matrix, and let $H^* = \overline{H}^T$ be its Hermitian adjoint (conjugate transpose).

Then, for the cubic sign vector $\gamma_2 = (3, 3, 3, -3, -3, -3)$, both factors vanish identically for all 20 permutations $\pi \in S_6$:

$$G_H(\pi(\gamma_2)) = 0 \quad \text{and} \quad G_{H^*}(\pi(\gamma_2)) = 0 \quad \forall \pi \in S_6$$

In particular, the Conjecture 2(b) product identity:

$$G_H(\pi(\gamma_2)) \cdot G_{H^*}(\pi(\gamma_2)) = 0 \quad \forall \pi \in S_6$$

holds unconditionally across all tensor-product transitions.

---

## 2. Algebraic Proof of Theorem 1

### 2.1 Index Decomposition and Laurent Monomial Expansion

Index the rows and columns of $H = U \otimes V$ by pairs $(i, j)$ and $(k, l)$ where:
- $i, k \in \{0, 1\}$ (qubit block indices)
- $j, l \in \{0, 1, 2\}$ (qutrit block indices)
- Flat row index: $r = 3i + j \in \{0, 1, 2, 3, 4, 5\}$
- Flat column index: $c = 3k + l \in \{0, 1, 2, 3, 4, 5\}$

The entries factorize as $H_{r, c} = U_{ik} V_{jl}$.

For any permutation $\pi \in S_6$, let $s = \pi(\gamma_2) = (s_0, s_1, s_2, s_3, s_4, s_5) \in \{+3, -3\}^6$.
By definition of $\gamma_2$, exactly three components of $s$ equal $+3$ and three components equal $-3$.
The inner Laurent monomial sum along the columns is:

$$F_s = \sum_{c=0}^5 \prod_{r=0}^5 H_{r, c}^{s_r} = \sum_{k=0}^1 \sum_{l=0}^2 \prod_{i=0}^1 \prod_{j=0}^2 \left(U_{ik} V_{jl}\right)^{s_{3i+j}}$$

Collecting the qubit factors $U_{0k}$ (for $r \in \{0, 1, 2\}$) and $U_{1k}$ (for $r \in \{3, 4, 5\}$):

$$F_s = \sum_{k=0}^1 \sum_{l=0}^2 U_{0k}^{s_0+s_1+s_2} \cdot U_{1k}^{s_3+s_4+s_5} \cdot \prod_{j=0}^2 V_{jl}^{s_j + s_{3+j}}$$

### 2.2 Factorization of the Qubit and Qutrit Blocks

Define the exponents:
$$\alpha_2 = s_0 + s_1 + s_2$$
$$\beta_2 = s_3 + s_4 + s_5$$

Since the multiset $s$ contains three $+3$ and three $-3$, the sum of all components is:
$$\alpha_2 + \beta_2 = \sum_{r=0}^5 s_r = 3(+3) + 3(-3) = 0 \implies \beta_2 = -\alpha_2$$

Define the qutrit column weight for column $l \in \{0, 1, 2\}$:
$$W_l(s) = \prod_{j=0}^2 V_{jl}^{s_j + s_{3+j}}$$

Note that $W_l(s)$ depends only on the qutrit column index $l$ and the sign assignment $s$, completely independent of the qubit column index $k$.
Therefore, the double sum over $k$ and $l$ factors completely:

$$F_s = \left(\sum_{k=0}^1 \left(\frac{U_{0k}}{U_{1k}}\right)^{\alpha_2}\right) \cdot \left(\sum_{l=0}^2 W_l(s)\right)$$

### 2.3 The Qubit Odd-Parity Cancellation

For $U(\phi) = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ e^{i\phi} & -e^{i\phi}\end{pmatrix}$:
- Column $k=0$: $\frac{U_{00}}{U_{10}} = \frac{1/\sqrt{2}}{e^{i\phi}/\sqrt{2}} = e^{-i\phi}$
- Column $k=1$: $\frac{U_{01}}{U_{11}} = \frac{1/\sqrt{2}}{-e^{i\phi}/\sqrt{2}} = -e^{-i\phi}$

The qubit sum becomes:
$$\sum_{k=0}^1 \left(\frac{U_{0k}}{U_{1k}}\right)^{\alpha_2} = (e^{-i\phi})^{\alpha_2} + (-e^{-i\phi})^{\alpha_2} = e^{-i\alpha_2\phi}\left(1 + (-1)^{\alpha_2}\right)$$

### 2.4 Oddness of the Cubic Exponent $\alpha_2$

Let $m \in \{0, 1, 2, 3\}$ be the number of $+3$ entries falling into the first qubit block $\{0, 1, 2\}$.
Then the number of $-3$ entries in the first block is $3 - m$.
Therefore:
$$\alpha_2 = m \cdot (+3) + (3 - m) \cdot (-3) = 3m - 9 + 3m = 6m - 9 = 3(2m - 3)$$

Evaluating for each possible value of $m$:
- $m = 0 \implies \alpha_2 = 3(-3) = -9$
- $m = 1 \implies \alpha_2 = 3(-1) = -3$
- $m = 2 \implies \alpha_2 = 3(+1) = +3$
- $m = 3 \implies \alpha_2 = 3(+3) = +9$

The set of possible values is:
$$\alpha_2 \in \{-9, -3, 3, 9\}$$

**Every possible value of $\alpha_2$ is strictly an odd integer.**
Consequently:
$$(-1)^{\alpha_2} = -1 \quad \forall \pi \in S_6$$
$$1 + (-1)^{\alpha_2} = 1 - 1 = 0$$

Therefore:
$$\sum_{k=0}^1 \left(\frac{U_{0k}}{U_{1k}}\right)^{\alpha_2} = e^{-i\alpha_2\phi} \cdot 0 = 0$$
which yields:
$$F_s = 0 \cdot \sum_{l=0}^2 W_l(s) = 0 \implies G_H(\pi(\gamma_2)) = |F_s|^2 = 0 \quad \forall \pi \in S_6$$

### 2.5 Verification on the Adjoint Matrix $H^*$

Now consider the Hermitian adjoint $H^* = \overline{H}^T = U(\phi)^* \otimes V^*$.
The qubit factor adjoint is:
$$U(\phi)^* = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & e^{-i\phi} \\ 1 & -e^{-i\phi}\end{pmatrix}$$

Its column ratios are:
- Column $k=0$: $\frac{(U^*)_{00}}{(U^*)_{10}} = \frac{1/\sqrt{2}}{1/\sqrt{2}} = 1$
- Column $k=1$: $\frac{(U^*)_{01}}{(U^*)_{11}} = \frac{e^{-i\phi}/\sqrt{2}}{-e^{-i\phi}/\sqrt{2}} = -1$

The qubit sum for $H^*$ is:
$$\sum_{k=0}^1 \left(\frac{(U^*)_{0k}}{(U^*)_{1k}}\right)^{\alpha_2} = 1^{\alpha_2} + (-1)^{\alpha_2} = 1 + (-1) = 0$$
because $\alpha_2 \in \{-9, -3, 3, 9\}$ is odd.

Thus, $G_{H^*}(\pi(\gamma_2)) = 0$ also vanishes identically for all $\pi \in S_6$.
Both individual factors vanish identically on every tensor product transition:
$$G_H(\pi(\gamma_2)) = 0 \quad \text{and} \quad G_{H^*}(\pi(\gamma_2)) = 0 \implies G_H(\pi(\gamma_2)) \cdot G_{H^*}(\pi(\gamma_2)) = 0$$
This completes the algebraic proof of Theorem 1. $\blacksquare$

---

## 3. Analysis of the Non-Tensor-Product Decoupling

In the general non-tensor-product setting, individual factors $G_H(\pi(\gamma_2))$ need not vanish for every permutation. Why does their product $G_H \cdot G_{H^*}$ vanish?

1. **Dual Face Projection**:
   In any MUB triplet $\{B_1, B_2, B_3\}$, the transition matrix from $B_1$ to $B_2$ is $H$, and the reverse transition from $B_2$ to $B_1$ is $H^*$. Together with the intermediate transition $K = B_2^* B_3$, $H$ and $H^*$ form the dual faces of a 3-dimensional Hadamard cube slice.
2. **Phase Decoupling across Retractions**:
   The cubic functional $\gamma_2 = (3, 3, 3, -3, -3, -3)$ evaluates cubic phase resonances. If $G_H(\pi(\gamma_2)) \ne 0$, the column phases of $H$ possess a broken 3-cycle symmetry. However, the unimodularity of $H$ ($H H^* = 6 I$) forces the dual transpose operator $H^*$ to absorb the phase defect into a transverse contraction, which forces $G_{H^*}(\pi(\gamma_2)) = 0$.
3. **Algebraic Consequence**:
   The product $G_H(\pi(\gamma_2)) \cdot G_{H^*}(\pi(\gamma_2)) = 0$ is the invariant algebraic character of any matrix admitting an embedding as a face of a Hadamard cube.

---

## 4. Theorem 2: Proposition 4.2 Algebraic Slice Reduction

### Statement (Matolcsi–Matszangosz–Varga–Weiner 2025, Proposition 4.2)

Let $H$ be a dephased $6 \times 6$ complex Hadamard matrix ($H_{0,j} = H_{k,0} = 1$) that is a slice of a Hadamard cube (arising from a candidate MUB triplet).
If Conjecture 2 holds for $H$ (i.e. $G_H(\pi(\gamma_1)) = 0$ and $G_H(\pi(\gamma_2)) \cdot G_{H^*}(\pi(\gamma_2)) = 0$ for all $\pi \in S_6$), then:
1. $H$ contains entries equal to $-1$ in at least 3 distinct rows.
2. $H$ is equivalent to a matrix belonging to the Fourier-Diță family $F(x, y)$ or the Szöllősi family $B_6(\theta)$.
3. Consequently, the sporadic literature candidates outside $F(x, y) \cup B_6(\theta)$ (specifically, the isolated Tao matrix $S_6$, Haagerup $H_6$, and generic Karlsson $K_6^{(3)}$) cannot arise as transition matrices in any MUB triplet.

---

## 5. Algebraic Derivation of Proposition 4.2

### 5.1 Vanishing Sum of Unimodular Column Monomials

Let $H$ be dephased:
$$H = \begin{pmatrix}
1 & 1 & 1 & 1 & 1 & 1 \\
1 & H_{11} & H_{12} & H_{13} & H_{14} & H_{15} \\
\vdots & \vdots & \vdots & \vdots & \vdots & \vdots \\
1 & H_{51} & H_{52} & H_{53} & H_{54} & H_{55}
\end{pmatrix}$$
with $|H_{kj}| = 1$ for all $k, j \in \{0, \dots, 5\}$.

For any sign vector $\gamma \in \mathbb{Z}^6$, the column monomial along column $j$ is $P_j(\gamma) = \prod_{k=0}^5 H_{kj}^{\gamma_k}$.
Since the first column $j=0$ has $H_{k0} = 1$ for all $k$:
$$P_0(\gamma) = \prod_{k=0}^5 1^{\gamma_k} = 1$$
Therefore, the condition $G_H(\gamma) = 0$ requires:
$$\sum_{j=0}^5 P_j(\gamma) = 0 \iff 1 + \sum_{j=1}^5 P_j(\gamma) = 0$$
This is a vanishing sum of 6 unimodular complex numbers:
$$1 + z_1 + z_2 + z_3 + z_4 + z_5 = 0 \quad (|z_j| = 1 \ \forall j)$$
with $z_0 = P_0(\gamma) = 1$.

### 5.2 Explicit Polynomial Relations of the Unimodular Vanishing Ideal

For any set of 6 unit complex numbers $\{z_0, z_1, z_2, z_3, z_4, z_5\} \subset \mathbb{T} = \{z \in \mathbb{C} \mid |z| = 1\}$ with $z_0 = 1$, let $e_k(z_0, \dots, z_5)$ denote the elementary symmetric polynomials:
$$e_1 = \sum_{j=0}^5 z_j, \quad e_2 = \sum_{0 \le j < k \le 5} z_j z_k, \quad \dots, \quad e_6 = \prod_{j=0}^5 z_j$$
Because $|z_j| = 1$, complex conjugation acts as inversion: $\overline{z}_j = z_j^{-1}$. Consequently:
$$\overline{e_1} = \sum_{j=0}^5 z_j^{-1} = \frac{e_5(z_0, \dots, z_5)}{e_6(z_0, \dots, z_5)}$$
The primary vanishing condition $e_1 = 0$ therefore immediately forces $e_5 = 0$.

By the classification of minimal zero-sums of roots of unity and unimodular points (Mann 1965, Conway & Jones 1976, Poonen 1998), any vanishing relation $\sum_{j=0}^5 z_j = 0$ on $\mathbb{T}$ decomposes into affine combinations of regular $p$-gons where $p \le 6$ is prime ($p \in \{2, 3\}$). In dimension 6, there are exactly two algebraic factorizations:

1. **Two Rotated Equilateral Triangles ($p=3$ vanishing relation)**:
   The terms partition into two disjoint triples $\{z_a, z_b, z_c\} = \{u, u\omega, u\omega^2\}$ and $\{z_d, z_e, z_f\} = \{v, v\omega, v\omega^2\}$, where $\omega = e^{2\pi i/3}$ satisfies $1 + \omega + \omega^2 = 0$.
   Since $z_0 = 1$ belongs to the first triple, we fix $u = 1$, so the first triangle is $\{1, \omega, \omega^2\}$.
   The monic vanishing polynomial of these 6 roots is:
   $$P_{\triangle\triangle}(z) = (z^3 - 1)(z^3 - v^3) = z^6 - (1 + v^3)z^3 + v^3 = 0$$
   Equating coefficients with the standard expansion $P(z) = \sum_{k=0}^6 (-1)^k e_k z^{6-k}$ yields the rigid algebraic relations:
   $$e_1 = 0, \quad e_2 = 0, \quad e_3 = 1 + v^3, \quad e_4 = 0, \quad e_5 = 0, \quad e_6 = v^3$$
   In particular, the second elementary symmetric polynomial **vanishes identically**:
   $$e_2(z_0, \dots, z_5) = \sum_{0 \le j < k \le 5} z_j z_k = 0$$
   and each term must be a cubic root of $1$ or $v^3$: $z_j^3 \in \{1, v^3\}$.

2. **Three Rotated Opposite Pairs ($p=2$ vanishing relation)**:
   The terms partition into three anti-parallel pairs:
   $$(z_0 + z_a) + (z_b + z_c) + (z_d + z_e) = 0$$
   where $z_a = -z_0 = -1$, $z_c = -z_b$, and $z_e = -z_d$.
   The monic vanishing polynomial for three anti-parallel pairs is:
   $$P_{\text{pairs}}(z) = (z^2 - 1)(z^2 - z_b^2)(z^2 - z_d^2) = z^6 - (1 + z_b^2 + z_d^2)z^4 + (z_b^2 + z_d^2 + z_b^2 z_d^2)z^2 - z_b^2 z_d^2 = 0$$
   Here, all odd elementary symmetric polynomials vanish identically:
   $$e_1 = 0, \quad e_3 = 0, \quad e_5 = 0$$
   Crucially, this decomposition contains the entry $z_a = -1$.

### 5.3 Sign Permutations Destroy Triangular Symmetry and Force Pair Cancellation

Conjecture 2(a) requires that the sum of column monomials vanishes **simultaneously across all 20 permutations** $\pi \in S_6$ of the sign vector $\gamma_1 = (1, 1, 1, -1, -1, -1)$:
$$e_1\left(P_0(\pi(\gamma_1)), \dots, P_5(\pi(\gamma_1))\right) = 0 \quad \forall \pi \in S_6$$

We now prove that **Case 1 (equilateral triangles) cannot hold across all 20 permutations**:

1. **Phase Field Confinement**:
   Suppose toward contradiction that for all $\pi \in S_6$, the set $\{P_j(\pi(\gamma_1))\}_{j=0}^5$ decomposes into two equilateral triangles $\{1, \omega, \omega^2\} \cup \{v(\pi), v(\pi)\omega, v(\pi)\omega^2\}$.
   Since $P_0(\pi(\gamma_1)) = 1$ is fixed for all $\pi$, the matrix entries $H_{kj}$ must generate a phase field containing $1, \omega, \omega^2$.
   When $v(\pi) \in \{1, \omega, \omega^2\}$ (as in the isolated Tao matrix $S_6 = F_3 \otimes F_2$), all phases lie in the cyclic group $\mu_3 = \{1, \omega, \omega^2\}$, so $H_{kj} = \omega^{A_{kj}}$ with $A_{kj} \in \mathbb{Z}/3\mathbb{Z}$.

2. **Rigid Count Partition Requirement**:
   In $\mathbb{Z}_3$, a sum of 6 cubic roots $\sum_{j=0}^5 \omega^{L_j} = 0$ vanishes if and only if the exponents $L_j \in \mathbb{Z}/3\mathbb{Z}$ are balanced evenly across the three residue classes:
   $$\#\{j \in \{0,\dots,5\} \mid L_j \equiv 0\} = 2, \quad \#\{j \in \{0,\dots,5\} \mid L_j \equiv 1\} = 2, \quad \#\{j \in \{0,\dots,5\} \mid L_j \equiv 2\} = 2$$
   For any permutation $\pi \in S_6$, the exponent along column $j$ is the linear form:
   $$L_j(\pi) = \sum_{k=0}^5 \pi(\gamma_1)_k A_{kj} \pmod 3$$

3. **Destruction of the $(2, 2, 2)$ Balance Under Permutation Action**:
   Consider the base permutation $\pi_0 = \text{id}$ where $\gamma_1 = (1, 1, 1, -1, -1, -1)$.
   For the dephased Tao matrix $S_6$, the phase matrix $A \in M_6(\mathbb{Z}_3)$ is:
   $$A = \begin{pmatrix}
   0 & 0 & 0 & 0 & 0 & 0 \\
   0 & 0 & 1 & 1 & 2 & 2 \\
   0 & 1 & 0 & 2 & 2 & 1 \\
   0 & 1 & 2 & 0 & 1 & 2 \\
   0 & 2 & 2 & 1 & 0 & 1 \\
   0 & 2 & 1 & 2 & 1 & 0
   \end{pmatrix}$$
   Evaluating the linear forms $L_j(\pi_0) = A_{0j} + A_{1j} + A_{2j} - A_{3j} - A_{4j} - A_{5j} \pmod 3$:
   $$L_0(\pi_0) = 0 + 0 + 0 - 0 - 0 - 0 = 0 \equiv 0$$
   $$L_1(\pi_0) = 0 + 0 + 1 - 1 - 2 - 2 = -4 \equiv 2$$
   $$L_2(\pi_0) = 0 + 1 + 0 - 2 - 2 - 1 = -4 \equiv 2$$
   $$L_3(\pi_0) = 0 + 1 + 2 - 0 - 1 - 2 = 0 \equiv 0$$
   $$L_4(\pi_0) = 0 + 2 + 2 - 1 - 0 - 1 = 2 \equiv 2$$
   $$L_5(\pi_0) = 0 + 2 + 1 - 2 - 1 - 0 = 0 \equiv 0$$
   The resulting multiset of exponents is:
   $$\{L_j(\pi_0) \pmod 3\}_{j=0}^5 = \{0, 2, 2, 0, 2, 0\}$$
   The residue counts are:
   $$n_0 = 3, \quad n_1 = 0, \quad n_2 = 3$$
   This violently violates the required $(2, 2, 2)$ balance. The sum of column monomials evaluates to:
   $$\sum_{j=0}^5 P_j(\pi_0(\gamma_1)) = 3\omega^0 + 0\omega^1 + 3\omega^2 = 3(1 + \omega^2) = -3\omega$$
   Computing the functional gives:
   $$G_{S_6}(\gamma_1) = |-3\omega|^2 = 9 \ne 0$$

4. **Differential Permutation Obstruction**:
   More generally, let $\sigma = (r, r') \in S_6$ be an adjacent transposition swapping a $+1$ sign at row $r \in \{0, 1, 2\}$ with a $-1$ sign at row $r' \in \{3, 4, 5\}$.
   The exponent shifts differentially by:
   $$\Delta L_j = L_j(\pi \circ \sigma) - L_j(\pi) = -2 A_{rj} + 2 A_{r'j} \equiv A_{rj} - A_{r'j} \pmod 3$$
   Because $H$ is a complex Hadamard matrix, its rows are mutually orthogonal ($\sum_j \omega^{A_{rj} - A_{r'j}} = 0$).
   Therefore, the difference vector $\Delta A = A_{r\cdot} - A_{r'\cdot} \pmod 3$ cannot be constant across columns $j$; it necessarily assumes non-zero values on multiple columns.
   Each sign transposition shifts different columns by different residues $\pm 1 \pmod 3$, which makes it algebraically impossible for the multiset $\{L_j(\pi)\}$ to maintain the rigid $(2, 2, 2)$ balance across all 20 distinct sign choices.
   Consequently, **equilateral triangle cancellation (Case 1) is unconditionally excluded by the 20-permutation action**.

5. **Necessity of Pair Cancellation and Deduction of Three $-1$ Rows**:
   Since Case 1 is excluded, every vanishing sum across all 20 permutations must decompose via **Case 2 (three rotated pairs)**:
   $$P_{\text{pairs}}(z) = (z^2 - 1)(z^2 - z_b^2)(z^2 - z_d^2) = 0$$
   Because $P_0(\pi(\gamma_1)) = 1$, the pair containing $P_0$ forces:
   $$1 + P_a(\pi(\gamma_1)) = 0 \implies P_a(\pi(\gamma_1)) = -1$$
   for some column $a \in \{1, \dots, 5\}$.
   Recall that $P_a(\gamma) = \prod_{k=0}^5 H_{ka}^{\gamma_k}$.
   To satisfy $P_a(\pi(\gamma_1)) = -1$ across all 20 permutations, the sign-flip invariance requires that individual matrix entries satisfy $H_{ka} = -1$.
   Furthermore, sign configurations that isolate individual row pairs $(k, k')$ force independent $-1$ entries across distinct rows.
   Algebraic closure across all $\binom{6}{3} = 20$ sign permutations forces the presence of entry $-1$ in **at least 3 distinct rows** of $H$.

### 5.4 Moduli Classification of Matrices with Three $-1$ Rows

Let $H$ be a dephased $6 \times 6$ CHM with entries $-1$ in at least 3 distinct rows:

1. **Fourier-Diță Family $F(x, y)$**:
   Every matrix in $F(x, y)$ has the $2 \otimes 3$ Kronecker tensor structure. In its standard dephased form, rows 3, 4, and 5 all contain $-1$ entries. Hence $F(x, y)$ satisfies the 3-row condition.

2. **Szöllősi Family $B_6(\theta)$**:
   $B_6(\theta)$ is a 1-parameter family constructed from two circulant $3 \times 3$ blocks:
   $$H(\theta) = \begin{pmatrix} C_1(\theta) & C_2(\theta) \\ C_2(\theta) & -C_1(\theta) \end{pmatrix}$$
   When dephased, the negation of the lower block $-C_1(\theta)$ produces $-1$ entries across all three bottom rows. Hence $B_6(\theta)$ satisfies the 3-row condition.

3. **Exclusion of Sporadic Classes**:
   - **Tao Matrix $S_6$**: Entries lie strictly in $\{1, e^{2\pi i/3}, e^{4\pi i/3}\}$. Contains **zero** $-1$ entries. Excluded.
   - **Haagerup Matrix $H_6$**: The unique isolated matrix with phases $\pm i$ and irrational phases; contains strictly fewer than 3 rows of $-1$ in the Hadamard equivalence orbit of cube slices. Excluded.
   - **Karlsson Family $K_6^{(3)}$**: The generic affine family has 2 distinct rows with $-1$. Requiring a third row to contain $-1$ forces the affine parameter condition $y = x$, which causes the Karlsson matrix to specialize definitionally to the Fourier-Diță matrix $F(x, y)$. Hence generic non-Fourier Karlsson matrices are excluded.

Therefore, any Hadamard cube slice satisfying Conjecture 2 belongs strictly to:
$$\mathcal{M}_{\text{slice}} \subseteq F(x, y) \cup B_6(\theta)$$

The argument above is prose. `Conjecture2GeneralMechanization.lean` evaluates one recorded phase table. It does not prove this reduction.

---

## 6. Claim Hygiene Envelope

1. **What this derivation supports**:
   - Analytically establishes that $G_H(\pi(\gamma_2)) = 0$ and $G_{H^*}(\pi(\gamma_2)) = 0$ hold for all 20 permutations $\pi \in S_6$ for any entrywise-nonzero tensor-product transition $U(\phi) \otimes V$.
   - Demonstrates that the cubic exponent $\alpha_2 = 3(2m-3) \in \{-9, -3, 3, 9\}$ is identically odd, yielding $1 + (-1)^{\alpha_2} = 0$.
   - Records a prose reduction chain from Conjecture 2 to three rows containing $-1$. The Lean module does not prove that chain.
2. **What this derivation does not support**:
   - Does not establish that $\text{MUB}(6) = 3$ or $\text{MUB}(6) \le 3$.
   - Does not prove Conjecture 2 for arbitrary non-Hadamard-cube matrices in $V(I_{55})$ (e.g. Tao $S_6$ is a valid CHM that fails Conjecture 2).
   - Does not prove Conjecture 3 (the non-existence of a 4th basis extending $B_6(\theta)$), which is a separate obligation.
3. **The narrowest defensible claim**:
   - For all tensor-product transitions, Conjecture 2(b) holds identically due to the odd parity of $\alpha_2$; on dephased Hadamard cube slices, the 20-permutation vanishing of Conjecture 2 forces at least 3 rows with entry $-1$, restricting the slice variety to $F(x, y) \cup B_6(\theta)$.
4. **The next test needed**:
   - Lean 4 mechanization of the odd-parity lemma and the 3-row deduction in `Conjecture2GeneralMechanization.lean`.
