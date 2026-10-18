# 120 — Mermin-Peres Contextuality as a Parity Cochain Obstruction

**Subtitle:** A finite linear-algebraic proof of state-independent contextuality

```text
Canonical ID: QM_120
Canonical title: Mermin-Peres Contextuality as a Parity Cochain Obstruction
Canonical version: v0.2.0 (Consolidated Worked Example)
Rights License: Creative Commons Attribution 4.0 International (CC-BY-4.0)
AuthorityEffect: None
```

**Author:** Jeremy H. Carroll  
**Date:** 2026-07-29 (Consolidated 2026-10-17)  
**Rights License:** CC-BY-4.0  
**Status:** preprint — worked contextuality chapter  
**Series:** Quantum Foundations 120  
**Companions:** QM_122 (Organizing Chapter)  
**Authority:** None. Finite linear algebra over $\mathbb{F}_2$.

---

## Abstract

We present a self-contained, finite, linear-algebraic treatment of the Mermin–Peres contextuality obstruction. A noncontextual hidden-variable assignment requires assigning a deterministic value $v(O) \in \{\pm 1\}$ to each observable $O$ independently of the measurement context, preserving operator product identities within each commuting context. 

We formalize this requirement as the solvability of an affine linear system over $\mathbb{F}_2$:
$$\mathbb{F}_2^9 \xrightarrow{A} \mathbb{F}_2^6 \xrightarrow{\ell} \mathbb{F}_2.$$
Because every observable appears in exactly two contexts (one row and one column), the incidence map satisfies $\ell A = 0$. The quantum target vector $s = (0,0,0,0,0,1)^T$ satisfies $\ell(s) = 1$, which proves immediately that $s \notin \operatorname{im} A$. We provide an exact rank proof showing $\operatorname{rank} A = 5$ and $\operatorname{im} A = \ker \ell$, and locate the obstruction in $\operatorname{coker} A \cong \mathbb{F}_2$.

---

## 1. The Operator Square

The Mermin–Peres magic square consists of nine two-qubit observables arranged in a $3 \times 3$ grid:

$$\begin{array}{ccc}
X \otimes I & I \otimes X & X \otimes X \\
I \otimes Z & Z \otimes I & Z \otimes Z \\
X \otimes Z & Z \otimes X & Y \otimes Y
\end{array}$$

Each observable $O_{ij}$ is self-adjoint with eigenvalues in $\{+1, -1\}$. The observables in each row and in each column mutually commute:
1. Row products:
   $$(X \otimes I)(I \otimes X)(X \otimes X) = X^2 \otimes X^2 = I \otimes I = I,$$
   $$(I \otimes Z)(Z \otimes I)(Z \otimes Z) = Z^2 \otimes Z^2 = I,$$
   $$(X \otimes Z)(Z \otimes X)(Y \otimes Y) = (XZY) \otimes (ZXY) = (-iY^2) \otimes (iY^2) = (-iI) \otimes (iI) = I.$$
2. Column products:
   $$(X \otimes I)(I \otimes Z)(X \otimes Z) = X^2 \otimes Z^2 = I,$$
   $$(I \otimes X)(Z \otimes I)(Z \otimes X) = Z^2 \otimes X^2 = I,$$
   $$(X \otimes X)(Z \otimes Z)(Y \otimes Y) = (XZY) \otimes (XZY) = (-iI) \otimes (-iI) = -I.$$

All three rows and the first two columns multiply to $+I$, while the third column multiplies to $-I$.

---

## 2. Formulation as an $\mathbb{F}_2$ Linear Complex

A noncontextual value assignment is a mapping $v: \{O_{ij}\} \to \{+1, -1\}$ satisfying the product constraints. Under the isomorphism $(\{\pm 1\}, \times) \cong (\mathbb{F}_2, +)$ via $(-1)^{x_{ij}}$, the 9 observables form a vector $x \in \mathbb{F}_2^9$.

The 6 measurement contexts (3 rows, 3 columns) define a parity incidence matrix $A \in \mathbb{F}_2^{6 \times 9}$:
$$A = \begin{pmatrix}
1 & 1 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 1 & 1 & 1 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 1 & 1 & 1 \\
1 & 0 & 0 & 1 & 0 & 0 & 1 & 0 & 0 \\
0 & 1 & 0 & 0 & 1 & 0 & 0 & 1 & 0 \\
0 & 0 & 1 & 0 & 0 & 1 & 0 & 0 & 1
\end{pmatrix}.$$

The quantum product conditions demand $A x = s$, where the target parity syndrome is:
$$s = \begin{pmatrix} 0 \\ 0 \\ 0 \\ 0 \\ 0 \\ 1 \end{pmatrix} \in \mathbb{F}_2^6.$$

Let $\ell: \mathbb{F}_2^6 \to \mathbb{F}_2$ be the total parity functional $\ell(y) = \sum_{k=1}^6 y_k$.
Since each entry $x_{ij}$ belongs to exactly one row and one column, each column of $A$ contains exactly two $1$s. Over $\mathbb{F}_2$:
$$\ell(A x) = \sum_{k=1}^6 (Ax)_k = 2 \sum_{i,j} x_{ij} \equiv 0 \pmod 2.$$
Therefore:
$$\ell A = 0 \implies \operatorname{im} A \subseteq \ker \ell.$$

Evaluating $\ell$ on the target vector $s$ gives:
$$\ell(s) = 0 + 0 + 0 + 0 + 0 + 1 = 1 \ne 0.$$
Consequently, $s \notin \operatorname{im} A$. No global noncontextual assignment exists.

---

## 3. Rank Analysis and Exhaustive Characterization

**Theorem 3.1 (Rank and Image of the Context Matrix).**  
1. $\operatorname{rank} A = 5$.  
2. $\operatorname{im} A = \ker \ell$.  
3. A parity target $y \in \mathbb{F}_2^6$ is realizable if and only if $\ell(y) = 0$.

*Proof.*  
Let $u \in \mathbb{F}_2^3$ be row coefficients and $v \in \mathbb{F}_2^3$ be column coefficients such that:
$$\sum_{i=1}^3 u_i \operatorname{row}_i(A) + \sum_{j=1}^3 v_j \operatorname{col-context}_j(A) = 0.$$
Evaluating this linear combination at the cell $(i, j)$ yields:
$$u_i + v_j = 0 \implies u_i = v_j \qquad \forall i, j \in \{1, 2, 3\}.$$
Fixing $i=1$ forces $v_1 = v_2 = v_3 = u_1$, which in turn forces $u_2 = u_3 = u_1$. Thus the only non-trivial linear dependence among the six rows of $A$ is the all-ones vector $(1, 1, 1, 1, 1, 1)$, which corresponds to $\ell$.  
Hence $\dim \ker A^T = 1$, so by the rank-nullity theorem:
$$\operatorname{rank} A = 6 - 1 = 5.$$
Since $\dim \ker \ell = 6 - 1 = 5$ and $\operatorname{im} A \subseteq \ker \ell$, equality $\operatorname{im} A = \ker \ell$ follows. $\blacksquare$

### Enumeration Census ($2^9 = 512$ Assignments)
Direct evaluation across all $512$ binary assignments $x \in \mathbb{F}_2^9$ confirms:
- **Assignments satisfying full target $s$:** $0$
- **Assignments satisfying any 5-context subsystem:** $2^{9-5} = 16$
- **Distinct attainable syndromes ($\operatorname{im} A$):** $2^5 = 32$
- **Fiber size per attainable syndrome:** $16$

---

## 4. Cohomological Location of the Obstruction

For the 2-step sequence:
$$\mathbb{F}_2^9 \xrightarrow{A} \mathbb{F}_2^6 \xrightarrow{\ell} \mathbb{F}_2,$$
we compute the cohomology spaces:
$$H^1 = \ker \ell / \operatorname{im} A = 0 \quad (\text{since } \operatorname{im} A = \ker \ell),$$
$$H^2 = \operatorname{coker} \ell = \mathbb{F}_2 / \operatorname{im} \ell = \mathbb{F}_2 / \mathbb{F}_2 = 0.$$

The obstruction is an **image failure** ($\text{target } s \notin \operatorname{im} A$), meaning $s$ is not a coboundary. Because $\ell(s) = 1 \ne 0$, $s$ is non-closed with respect to $\ell$, and its non-zero quotient class lives in:
$$\operatorname{coker} A = \mathbb{F}_2^6 / \operatorname{im} A \cong \mathbb{F}_2.$$
This clarifies that Mermin–Peres contextuality on this complex is an image obstruction in $\operatorname{coker} A$, not a non-zero $H^2$ cohomology class.

---

## 5. Implementation Reference

The mechanized $\mathbb{F}_2$ incidence verification and 512-state exhaustive certificate are implemented in `omega_engine/crates_rs/omega_quantum_physics/src/` and verified in `tests/`.
