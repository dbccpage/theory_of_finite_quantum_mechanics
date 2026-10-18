# Target G1 Problem Digest: 50-Variable Hadamard Variety $\mathcal{H}_6$ Decomposition

**AuthorityEffect:** None  
**Firewall Line:** `stated region only; mints no authority`  
**Target:** Premise G1 Foundation & Orbit Exhaustiveness

---

## 1. Problem Definition & Ambient Coordinates

A complex Hadamard matrix $H \in M_6(\mathbb{C})$ satisfies:
1. $|H_{jk}| = 1$ for all $j, k \in \{0, \dots, 5\}$.
2. $H H^\dagger = 6 I_6$.

In dephased canonical gauge, row 0 and column 0 are fixed to 1:
$$H = \begin{pmatrix}
1 & 1 & 1 & 1 & 1 & 1 \\
1 & z_{11} & z_{12} & z_{13} & z_{14} & z_{15} \\
1 & z_{21} & z_{22} & z_{23} & z_{24} & z_{25} \\
1 & z_{31} & z_{32} & z_{33} & z_{34} & z_{35} \\
1 & z_{41} & z_{42} & z_{43} & z_{44} & z_{45} \\
1 & z_{51} & z_{52} & z_{53} & z_{54} & z_{55}
\end{pmatrix}$$

Setting $z_{jk} = x_{jk} + i y_{jk}$ gives $25 \times 2 = 50$ real coordinates:
$$\mathbf{v} = (x_{11}, y_{11}, x_{12}, y_{12}, \dots, x_{55}, y_{55}) \in \mathbb{R}^{50}$$

### 1.1 Defining Polynomial System (55 Equations in 50 Variables)
1. **25 Unit Modulus Equations**:
   $$p_{jk}(\mathbf{v}) = x_{jk}^2 + y_{jk}^2 - 1 = 0 \quad \forall j, k \in \{1, \dots, 5\}$$
2. **30 Column Orthogonality Equations** ($\binom{6}{2} = 15$ complex inner products):
   For columns $k < l \in \{0, \dots, 5\}$:
   $$\langle C_k, C_l \rangle = \sum_{j=0}^5 H_{jk} \overline{H_{jl}} = 1 + \sum_{j=1}^5 z_{jk} \overline{z_{jl}} = 0$$
   Expanding into real and imaginary parts:
   - $\text{Re}(\langle C_k, C_l \rangle) = 1 + \sum_{j=1}^5 (x_{jk} x_{jl} + y_{jk} y_{jl}) = 0$ (15 equations)
   - $\text{Im}(\langle C_k, C_l \rangle) = \sum_{j=1}^5 (y_{jk} x_{jl} - x_{jk} y_{jl}) = 0$ (15 equations)

The real algebraic variety is:
$$\mathcal{H}_6 = V_{\mathbb{R}}(p_1, \dots, p_{25}, q_1, \dots, q_{30}) \subset \mathbb{R}^{50}$$

---

## 2. Decomposition into Known Orbits

The variety $\mathcal{H}_6$ decomposes into five known geometric components:
1. **Fourier Component $F_6$**: The discrete cyclic character table, defect 4, sitting at the origin of the Diță affine chart.
2. **Diță Family $D_6(\alpha, \beta)$**: Affine 2-parameter torus $T^2$, defect 4.
3. **Chernyavsky-Tao Isolated Point $S_6$**: Characterized by third roots of unity $\omega = e^{2\pi i / 3}$, defect $d(S_6) = 0$.
4. **Szöllősi 1-Parameter Family $B_6(\theta)$**: Non-affine curve with algebraic phase functions, defect 1, containing Haagerup $H_6$ at $\cos\theta = (\sqrt{3}-1)/2$.
5. **Karlsson 3-Parameter Manifold $K_6^{(3)}$**: Connects the Diță family and boundary branches of $B_6$.

---

## 3. The Open Mathematical Obligations

### Obligation G1.1: Orbit Catalog Exhaustiveness
Prove that the real algebraic variety $\mathcal{H}_6$ possesses **zero** irreducible components or isolated points outside the known catalog $\{F_6, D_6, S_6, B_6, K_6\}$.
- **Attack Vector**: Finite-incidence algebraic corner reconstruction. Prove that every dephased $6 \times 6$ CHM is algebraically determined by a $3 \times 3$ corner submatrix, and that all viable corner determinants factor into the known algebraic families.

### Obligation G1.2: Triad Compatibility Obstruction & Pigeonhole Closure
Prove that even if an unknown orbit were to exist, it could not support a complete 7-basis MUB configuration:
1. Any mutually unbiased triple $(I_6, H_1, H_2)$ requires $H_{12} = H_1^\dagger H_2 \in \mathcal{H}_6$.
2. The isolated Tao orbit $\mathcal{O}(S_6)$ admits no distinct partner $H_2 \in \mathcal{O}(S_6)$ with $S_6^\dagger H_2 \in \mathcal{H}_6$.
3. The Szöllősi family $B_6(\theta)$ admits no pairs with $B_6(\theta_1)^\dagger B_6(\theta_2) \in \mathcal{H}_6$.
4. **Pigeonhole Lemma**: In any hypothetical complete set of 7 MUBs, at most 1 basis can belong to $S_6$ and at most 1 can belong to $B_6$. Thus, at least $7 - 2 = 5$ bases must belong to the Diță/Fourier component. By the pigeonhole principle, any 5 bases contain $\binom{5}{3} = 10$ triples, all of which are purely Diță/Fourier and land in the certified moduli atlas!
