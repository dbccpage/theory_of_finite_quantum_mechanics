# Conjecture 2(a) — Algebraic Proof for Tensor-Product MUB-Triples

**Date**: 2026-09-27
**AuthorityEffect**: None

---

## Theorem

Let $U(\phi) = \frac{1}{\sqrt{2}}\begin{pmatrix}1 & 1 \\ e^{i\phi} & -e^{i\phi}\end{pmatrix}$ be any qubit MUB transition and let $V$ be any entrywise-nonzero $3\times 3$ matrix. Then the tensor product $H = U(\phi) \otimes V$ satisfies

$$G_H(\pi(\gamma_1)) = 0 \quad \forall \pi \in S_6$$

where $\gamma_1 = (1,1,1,-1,-1,-1)$ and $G_H(\gamma) = \left|\sum_{j} \prod_{k} H_{kj}^{\gamma_k}\right|^2$. Entrywise nonzero is required because negative components of $\gamma$ denote Laurent powers.

## Proof

### Setup
Index the rows and columns of the $6\times 6$ matrix $H = U \otimes V$ as $(i,j)$ where $i \in \{0,1\}$ (qubit index) and $j \in \{0,1,2\}$ (qutrit index), with flat index $r = 3i + j$.

The entries factorize: $H_{(i,j),(k,l)} = U_{ik} \cdot V_{jl}$.

### Inner Sum Expansion
For any sign vector $s = (s_0, \ldots, s_5)$ with $s_r = \pm 1$:

$$F_s = \sum_{c=0}^{5} \prod_{r=0}^{5} H_{r,c}^{s_r}
= \sum_{k=0}^{1}\sum_{l=0}^{2} \prod_{i=0}^{1}\prod_{j=0}^{2} (U_{ik} V_{jl})^{s_{3i+j}}$$

Collecting the $U$ and $V$ factors:

$$F_s = \sum_{k=0}^{1}\sum_{l=0}^{2} U_{0k}^{s_0+s_1+s_2} \cdot U_{1k}^{s_3+s_4+s_5} \cdot \prod_{j=0}^{2} V_{jl}^{s_j + s_{3+j}}$$

### Key Cancellation
Define $\alpha = s_0 + s_1 + s_2$ and $\beta = s_3 + s_4 + s_5$. Since exactly 3 of the 6 signs are $+1$ and 3 are $-1$, we have $\alpha + \beta = 0$, so $\beta = -\alpha$.

The V-factor for each column $l$ is:

$$W_l = \prod_{j=0}^{2} V_{jl}^{s_j + s_{3+j}}$$

This depends only on $l$ and the sign pattern, not on $k$. Therefore the finite double sum factors:

$$F_s = \left(\sum_{k=0}^{1} \left(\frac{U_{0k}}{U_{1k}}\right)^{\alpha}\right) \cdot \left(\sum_{l=0}^{2} W_l(s)\right)$$

### The Qubit Cancellation
For $U = \frac{1}{\sqrt{2}}\begin{pmatrix}1 & 1 \\ e^{i\phi} & -e^{i\phi}\end{pmatrix}$:

$$\frac{U_{00}}{U_{10}} = e^{-i\phi}, \quad \frac{U_{01}}{U_{11}} = -e^{-i\phi}$$

So:

$$\sum_{k=0}^{1} \left(\frac{U_{0k}}{U_{1k}}\right)^{\alpha} = e^{-i\alpha\phi} + (-e^{-i\phi})^{\alpha} = e^{-i\alpha\phi}\left(1 + (-1)^{\alpha}\right)$$

For $\gamma_1 = (1,1,1,-1,-1,-1)$, the possible values of $\alpha = s_0 + s_1 + s_2$ range over $\{-3, -1, 1, 3\}$ depending on the permutation $\pi$. All these values are **odd**.

Since $\alpha$ is odd: $(-1)^{\alpha} = -1$, and $1 + (-1)^{\alpha} = 0$.

**Therefore $F_s = 0$ for every permutation of $\gamma_1$.** $\square$

### Why α Is Always Odd

Among the 6 positions $\{0,1,2,3,4,5\}$, exactly 3 are assigned $+1$. The first qubit block is $\{0,1,2\}$ and the second is $\{3,4,5\}$.

If $m$ of the 3 positive signs fall in $\{0,1,2\}$, then $3-m$ fall in $\{3,4,5\}$, with $m \in \{0,1,2,3\}$.

$\alpha = s_0 + s_1 + s_2 = m \cdot (+1) + (3-m) \cdot (-1) = 2m - 3$

For $m \in \{0,1,2,3\}$: $\alpha \in \{-3, -1, 1, 3\}$. All odd. $\square$

---

## Scope and Implications

### What this theorem supports
- Conjecture 2(a) from arXiv:2503.14752 holds for **all** $6\times 6$ matrices with $\mathbb{Z}_2 \otimes \mathbb{Z}_3$ tensor-product structure where the $\mathbb{Z}_2$ factor is a qubit MUB transition.
- It applies to any catalog transition that is separately shown to have this tensor structure.
- The $3\times 3$ factor $V$ need not be unitary, Hadamard, or invertible, but each entry must be nonzero so the Laurent monomials are defined.

### What this theorem does NOT support
- This does not cover non-tensor-product CHMs (e.g., if a MUB-triple transition matrix lacks the $2 \otimes 3$ product structure).
- It does not address Conjecture 2(b) (the $\gamma_2 = (3,3,3,-3,-3,-3)$ case).
- It does not prove Conjecture 2 for all CHMs in dimension 6 — only for tensor-product transitions.
- It does not establish MUB(6) = 3 (the paper's chain also requires Conjecture 3).

### Narrowest defensible claim
Conjecture 2(a) is proved algebraically for the class of $6\times 6$ matrices of the form $U_{qubit} \otimes V_{entrywise\text{-}nonzero}$. The proof uses only the $\pm$ sign structure of the qubit MUB transition and does not otherwise constrain the qutrit factor.

### Next test needed
1. Prove Conjecture 2(b) ($\gamma_2$ case) for tensor-product transitions.
2. Determine whether non-tensor-product MUB-triple transitions exist in dimension 6.
3. If yes, prove Conjecture 2(a) for those transitions separately.

---

## Verification

- **Symbolic corroboration**: SymPy with 10 formal variables ($\phi, v_{00}, \ldots, v_{22}$), with every $v_{ij}$ declared nonzero; all 20 $\gamma_1$ permutations reduce to 0 using Laurent powers.
- **Finite exact check**: Rust Cyc24 verifier on 7 catalog triples and 21 transition matrices. It performs 840 permutation checks and 1,260 evaluations of $G$ across both conjecture clauses; all checked products are zero.
- **Discriminant**: 12/13 catalog candidates individually pass γ₁ (Tao S6 is the sole failure — expected for isolated CHMs).

## Files
- [`conj2_tensor_product_proof.py`](conj2_tensor_product_proof.py): Complete symbolic proof script
- [`conj2_fourier_family_proof.py`](conj2_fourier_family_proof.py): Symbolic check on the Fourier-family CHMs themselves
- [`mub6_matolcsi_weiner_conj2.rs`](../../../../omega_engine/crates_rs/omega_mub/src/native/mub6_matolcsi_weiner_conj2.rs): Rust exact finite verifier
