# WDP-APPM-T4

Goal id: WDP-APPM-T4

Selected scope for WDP-APPM-T4 is recorded in this note.

## Selected scope

Labelled finite carrier: the right 4-simplex (pentatope) $\Delta^4 \subset \mathbb{Q}^4$ with vertices $v_0 = (0,0,0,0)$ and $v_a = e_a$ ($a \in \{1, 2, 3, 4\}$), $5$ boundary tetrahedra $\tau_k = \Delta^4 \setminus \{v_k\}$, and $10$ oriented triangular hinges $h_{ijk} = [v_i, v_j, v_k]$ ($0 \le i < j < k \le 4$).

1. Explicit doubled area bivectors $B_{ijk} = (v_j - v_i) \wedge (v_k - v_i) \in \Lambda^2 \mathbb{Q}^4 \cong \mathbb{Q}^6$: the 6 coordinate hinges $[v_0, v_a, v_b]$ have $\|B_{0ab}\|^2 = 1$ and exact rational area $A_{0ab} = 1/2$; the 4 outer hinges $[v_a, v_b, v_c]$ have $\|B_{abc}\|^2 = 3$ and squared area $A_{abc}^2 = 3/4$.
2. Exact Barrett-Crane simplicity via the Pfaffian $\mathrm{Pf}(B) = B_{12} B_{34} - B_{13} B_{24} + B_{14} B_{23}$: all 10 hinge bivectors satisfy $\mathrm{Pf}(B_h) = 0$, and all 30 edge-sharing (intra-tetrahedral) hinge pairs satisfy $\mathrm{Pf}(B_h + B_{h'}) = 0$, whereas all $5 \times 3 = 15$ vertex-only opposite-hinge pairs (including the 3 opposite coordinate-hinge pairs at $v_0$) satisfy $|\mathrm{Pf}(B_h + B_{h'})| = 1 \neq 0$ ($30 + 15 = \binom{10}{2} = 45$).
3. Exact tetrahedral bivector closure $\sum_{m=0}^3 (-1)^m B_{\partial_m \tau_k} = 0 \in \mathbb{Q}^6$ on all 5 boundary tetrahedra, exact simplicial chain/cochain identity $\partial_3 \partial_4 = 0 \in \mathbb{Z}^{10}$ ($d_3 d_2 = 0$), an explicit rational $\mathrm{SO}(4, \mathbb{Q})$ Cayley transport $U = (I - A)(I + A)^{-1}$ with $U^T U = I_4$ and $\det U = 1$, and exact turn Regge action $S_{\mathrm{turn}} = 6 \cdot (1/2) \cdot (1/12) = 1/4$ on the 6 coordinate hinges at declared turn deficit $1/12$ ($\pi/6$ radians).

Not the pinned literal zero constants in `compute_t4_receipt`, and not the uncomputed continuum Einstein-Hilbert error bound $|S_{\mathrm{Regge}} - S_{\mathrm{EH}}| \le C a^2$.

## Hypotheses

The hypotheses are selected for this finite 4-simplex carrier. Appendix M.5 states that the pinned T4 record supplies zero simplicity and Bianchi defects as constants, and the bridge audit notes that `compute_t4_receipt` assigns `simplicity_defect = Fraction(0)` and `bianchi_defect = Fraction(0)` without computing bivectors, frame transports, or action from simplicial coordinates.

H1. The 4-simplex $\Delta^4$ has ordered vertices $v_0 = (0,0,0,0)$, $v_1 = (1,0,0,0)$, $v_2 = (0,1,0,0)$, $v_3 = (0,0,1,0)$, and $v_4 = (0,0,0,1)$ in $\mathbb{Q}^4$.

H2. In the lexicographic basis $(e_{12}, e_{13}, e_{14}, e_{23}, e_{24}, e_{34})$ of $\Lambda^2 \mathbb{Q}^4$, the wedge product of $u, w \in \mathbb{Q}^4$ has components $(u_a w_b - u_b w_a)_{1 \le a < b \le 4}$. For each oriented 2-simplex $h_{ijk} = [v_i, v_j, v_k]$ ($0 \le i < j < k \le 4$), the doubled area bivector is $B_{ijk} = (v_j - v_i) \wedge (v_k - v_i) = 2 \Sigma_{ijk}$, with squared Euclidean area $A_{ijk}^2 = \frac{1}{4}\|B_{ijk}\|^2$.

H3. The exterior square $B \wedge B = 2\,\mathrm{Pf}(B)\, e_1 \wedge e_2 \wedge e_3 \wedge e_4$ is determined by the rational Pfaffian

$$
\mathrm{Pf}(B) = B_{12} B_{34} - B_{13} B_{24} + B_{14} B_{23}.
$$

Two bivectors $B, B'$ satisfy cross-simplicity $B \wedge B' = 0$ if and only if $\mathrm{Pf}(B + B') - \mathrm{Pf}(B) - \mathrm{Pf}(B') = 0$.

H4. For an antisymmetric generator $A \in \mathfrak{so}(4, \mathbb{Q})$ with $\det(I + A) \neq 0$, the rational Cayley transform $U = (I - A)(I + A)^{-1}$ defines an exact frame transport in $\mathrm{SO}(4, \mathbb{Q})$. On the 6 coordinate hinges $[v_0, v_a, v_b]$ where $A_{0ab} = 1/2 \in \mathbb{Q}$, a declared uniform turn deficit $\epsilon_{\mathrm{turn}} = 1/12$ ($\pi/6$ radians) contributes $S_{\mathrm{turn}} = \sum_{1 \le a < b \le 4} A_{0ab} \epsilon_{\mathrm{turn}}$.

## Derivation

### 1. Explicit hinge bivectors and simplicity on $\Delta^4$

For the 6 coordinate hinges $[v_0, v_a, v_b]$ ($1 \le a < b \le 4$), $v_a - v_0 = e_a$ and $v_b - v_0 = e_b$, so

$$
B_{0ab} = e_a \wedge e_b, \qquad \|B_{0ab}\|^2 = 1, \qquad A_{0ab}^2 = \frac{1}{4}, \qquad A_{0ab} = \frac{1}{2}.
$$

For the 4 outer hinges $[v_a, v_b, v_c]$ ($1 \le a < b < c \le 4$),

$$
B_{abc} = (e_b - e_a) \wedge (e_c - e_a) = e_a \wedge e_b - e_a \wedge e_c + e_b \wedge e_c, \qquad \|B_{abc}\|^2 = 3, \qquad A_{abc}^2 = \frac{3}{4}.
$$

Evaluating $\mathrm{Pf}(B)$ on each of the 10 hinges gives $\mathrm{Pf}(B_{ijk}) = 0$: each coordinate hinge has only one nonzero basis component, and each outer hinge $B_{abc}$ lies in the 3-dimensional subspace $\Lambda^2 \operatorname{span}(e_a, e_b, e_c)$, where one coordinate index in $\{1, 2, 3, 4\} \setminus \{a, b, c\}$ vanishes in every term of $\mathrm{Pf}$.

Similarly, any two hinges $h, h'$ sharing an edge lie in a common boundary tetrahedron $\tau_k = \Delta^4 \setminus \{v_k\}$ and have edge vectors inside the 3-dimensional affine hyperplane of $\tau_k$, so $B_h + B_{h'}$ has rank at most 2 and $\mathrm{Pf}(B_h + B_{h'}) = 0$ across all $10 \times \binom{3}{2} = 30$ edge-sharing pairs.

By contrast, any two hinges sharing only a single vertex span all 5 vertices of $\Delta^4$. Across the 5 vertices there are $5 \times 3 = 15$ such opposite-hinge pairs ($30 + 15 = \binom{10}{2} = 45$), and every one satisfies $|\mathrm{Pf}(B_h + B_{h'})| = 1$. In particular, for the 3 pairs of opposite coordinate hinges sharing only $v_0$:

$$
\mathrm{Pf}(B_{012} + B_{034}) = +1, \qquad \mathrm{Pf}(B_{013} + B_{024}) = -1, \qquad \mathrm{Pf}(B_{014} + B_{023}) = +1.
$$

Thus cross-simplicity holds on all 30 intra-tetrahedral pairs and fails on all 15 opposite-hinge pairs of $\Delta^4$.

### 2. Tetrahedral closure and discrete Bianchi identity

For each 3-simplex $\tau = [v_{i_0}, v_{i_1}, v_{i_2}, v_{i_3}]$ ($0 \le i_0 < i_1 < i_2 < i_3 \le 4$), expanding the signed boundary sum of its 4 face bivectors gives

$$
B_{i_1 i_2 i_3} - B_{i_0 i_2 i_3} + B_{i_0 i_1 i_3} - B_{i_0 i_1 i_2}
= (v_{i_2} - v_{i_1}) \wedge (v_{i_3} - v_{i_1}) - (v_{i_2} - v_{i_0}) \wedge (v_{i_3} - v_{i_0}) + (v_{i_1} - v_{i_0}) \wedge (v_{i_3} - v_{i_0}) - (v_{i_1} - v_{i_0}) \wedge (v_{i_2} - v_{i_0}) = 0 \in \mathbb{Q}^6.
$$

In the simplicial chain complex of $\Delta^4$, the boundary matrix $\partial_3 : C_3(\Delta^4) \to C_2(\Delta^4)$ is $10 \times 5$ and $\partial_4 : C_4(\Delta^4) \to C_3(\Delta^4)$ is $[1, -1, 1, -1, 1]^T$. For every hinge $h_{ijk}$, exactly two boundary tetrahedra contain $h_{ijk}$, with opposite induced orientations in $\partial_4(\Delta^4)$, so

$$
\partial_3 \partial_4(\Delta^4) = 0 \in \mathbb{Z}^{10}, \qquad d_3 d_2(\Omega) = (\partial_3 \partial_4)^T \Omega = 0
$$

for every hinge curvature 2-cochain $\Omega \in C^2(\Delta^4)$.

### 3. Rational $\mathrm{SO}(4, \mathbb{Q})$ frame transport and coordinate-hinge Regge action

Take the antisymmetric generator $A = \frac{1}{2} (E_{12} - E_{21}) \in \mathfrak{so}(4, \mathbb{Q})$. Its Cayley transform is the block-diagonal rational orthogonal matrix

$$
U = (I_4 - A)(I_4 + A)^{-1} =
\begin{pmatrix}
3/5 & -4/5 & 0 & 0 \\
4/5 & 3/5 & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{pmatrix} \in \mathrm{SO}(4, \mathbb{Q}),
$$

satisfying $U^T U = I_4$, $\det U = 1$, and $\operatorname{tr}(U) = 16/5$.

On the 6 coordinate hinges $[v_0, v_a, v_b]$, each area is the exact rational $A_{0ab} = 1/2$. With the declared turn deficit $\epsilon_{\mathrm{turn}} = 1/12$ ($\pi/6$ radians) per coordinate hinge, the coordinate-hinge turn Regge action is

$$
S_{\mathrm{turn}} = \sum_{1 \le a < b \le 4} A_{0ab} \epsilon_{\mathrm{turn}} = 6 \cdot \frac{1}{2} \cdot \frac{1}{12} = \frac{1}{4},
$$

corresponding to radian action $6 \cdot (1/2) \cdot (\pi/6) = \pi/2 \in [1570796326/10^9, 1570796327/10^9]$ (hinge deficit $\pi/6 \in [523598775/10^9, 523598776/10^9]$). The 4 outer hinges have irrational area $\sqrt{3}/2$ and are kept distinct via their exact squared area $A_{abc}^2 = 3/4$.

## Claims this note does not make

- It does not accept the literal constant assignment `simplicity_defect = Fraction(0)` and `bianchi_defect = Fraction(0)` in `compute_t4_receipt` as a bivector calculation.
- It does not claim that arbitrary sums of hinge bivectors on $\Delta^4$ are simple; the 3 opposite coordinate-hinge pairs have $|\mathrm{Pf}(B_h + B_{h'})| = 1$.
- It does not derive the continuum Einstein-Hilbert action $\frac{1}{16\pi G}\int R\sqrt{-g}\,d^4x$ or the string bound `|S_Regge - S_EH| <= C * a^2`.
- It does not treat the declared hinge angle $\pi/6$ as a metric dihedral angle of the Euclidean 4-simplex $\Delta^4$.
- A finite calculation on one 4-simplex does not establish a continuum limit, a physical law, or a closed theorem outside the selected scope.
