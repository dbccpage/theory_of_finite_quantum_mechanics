# WDP-APPM-T2

Goal id: WDP-APPM-T2

Selected scope for WDP-APPM-T2 is recorded in this note.

## Selected scope

Labelled finite carrier: a five-triangle vertex star $K_5$ around an interior apex $v_0$ with cyclic boundary pentagon $(v_1, v_2, v_3, v_4, v_5)$ and unit squared edge lengths $s_i = d(v_0, v_i)^2 = 1$, $b_i = d(v_i, v_{i+1})^2 = 1$ for $i \in \{1, 2, 3, 4, 5\}$ (indices modulo 5), compared against the flat six-triangle equilateral star $K_6$. On each 2-simplex $(v_0, v_i, v_{i+1})$, the $4 \times 4$ Cayley-Menger matrix $M_i$ has exact determinant $\det(M_i) = -3$, signed volume factor $(-1)^3 \det(M_i) = 3 = 16 A_i^2 > 0$, squared area $A_i^2 = 3/16$, apex cosine $\cos \theta_i = 1/2$, and $\sin^2 \theta_i = 3/4$. Under the turn normalization where $\arccos(1/2) \in (0, \pi)$ is $1/6$ of a full turn ($2\pi$), the five-triangle star has total turn sum $5/6$, positive turn deficit $\epsilon_{\mathrm{turn}}(K_5) = 1 - 5/6 = 1/6$ (radian deficit $\pi/3 \in [1047197551/10^9, 1047197552/10^9]$), and discrete Regge curvature-area ratio $\epsilon_{\mathrm{turn}}(K_5)/A_{\mathrm{star}}$ with squared value $(1/6)^2 / (5^2 \cdot 3/16) = 4/2025$, whereas the six-triangle star $K_6$ has turn deficit $0$. Not the pinned positive Cayley-Menger determinant $+3$, and not an uncomputed continuum Ricci scalar error bound $|E(a)| \le (1/6)a^2$.

## Hypotheses

The hypotheses are selected for this finite simplicial carrier. Appendix M.5 states that the pinned T2 record encloses the declared angle $\pi/3$ for a five-triangle toy geometry, and the bridge audit notes that the displayed unit-triangle Cayley-Menger matrix has determinant $-3$ while the pinned receipt assigns $+3$.

H1. The 2-complex $K_n$ ($n \in \{5, 6\}$) consists of an apex vertex $v_0$, boundary vertices $v_1, \dots, v_n$ ordered cyclically modulo $n$, radial edges $e_i = \{v_0, v_i\}$ with squared length $s_i > 0$, and boundary edges $f_i = \{v_i, v_{i+1}\}$ with squared length $b_i > 0$.

H2. For each triangle $\tau_i = (v_0, v_i, v_{i+1})$ with squared side lengths $(s_i, s_{i+1}, b_i)$, the $4 \times 4$ Cayley-Menger matrix is

$$
M(s_i, s_{i+1}, b_i) =
\begin{pmatrix}
0 & 1 & 1 & 1 \\
1 & 0 & s_i & s_{i+1} \\
1 & s_i & 0 & b_i \\
1 & s_{i+1} & b_i & 0
\end{pmatrix}.
$$

Nondegeneracy of the Euclidean 2-simplex requires $(-1)^{2+1} \det M(s_i, s_{i+1}, b_i) = -\det M(s_i, s_{i+1}, b_i) > 0$.

H3. On a nondegenerate triangle $\tau_i$, the rational squared cosine and squared sine of the apex angle $\theta_i$ at $v_0$ are defined by the Euclidean law of cosines:

$$
\cos \theta_i = \frac{s_i + s_{i+1} - b_i}{2\sqrt{s_i s_{i+1}}}, \qquad \sin^2 \theta_i = 1 - \cos^2 \theta_i = \frac{-\det M(s_i, s_{i+1}, b_i)}{4 s_i s_{i+1}}.
$$

H4. For unit equilateral triangles $s_i = s_{i+1} = b_i = 1$, $\cos \theta_i = 1/2$ and $\sin^2 \theta_i = 3/4$, so $\theta_i = \pi/3$ radians, which is $1/6$ of the declared full turn $2\pi$.

## Derivation

Expand the $4 \times 4$ determinant of $M(s_i, s_{i+1}, b_i)$ directly over $\mathbb{Q}$:

$$
\det M(s_i, s_{i+1}, b_i) = s_i^2 + s_{i+1}^2 + b_i^2 - 2 s_i s_{i+1} - 2 s_i b_i - 2 s_{i+1} b_i.
$$

For the unit equilateral triangle $s_i = s_{i+1} = b_i = 1$,

$$
\det M(1, 1, 1) = 1 + 1 + 1 - 2 - 2 - 2 = -3.
$$

The Cayley-Menger volume identity for a 2-simplex relates the squared area $A_i^2$ to $\det M$ with the sign factor $(-1)^{2+1} = -1$:

$$
16 A_i^2 = (-1)^3 \det M(1, 1, 1) = -(-3) = 3, \qquad A_i^2 = \frac{3}{16}.
$$

In `symbol_game_coda_meron_ladder.py`, `compute_t2_receipt` comments `det(CM) = 3 > 0, (-1)^3 * det(CM) = -3` and stores `cayley_menger_det_2simplex = "3"`. That reverses the sign of the $4 \times 4$ determinant: $\det M(1, 1, 1)$ is $-3$, and it is $(-1)^3 \det M(1, 1, 1)$ that equals $+3$. A degenerate collinear triple with side lengths $(1, 1, 2)$ and squared lengths $(1, 1, 4)$ gives

$$
\det M(1, 1, 4) = 1 + 1 + 16 - 2 - 8 - 8 = 0,
$$

and a triangle-inequality violation with squared lengths $(1, 1, 9)$ gives $\det M(1, 1, 9) = 45 > 0$, so $(-1)^3 \det M(1, 1, 9) = -45 < 0$. Thus Euclidean 2-simplex nondegeneracy requires $\det M < 0$, not $\det M > 0$.

For each of the 5 unit equilateral triangles in $K_5$, the radial lengths are $s_i = s_{i+1} = 1$, so $\sqrt{s_i s_{i+1}} = 1$ is rational, and

$$
\cos \theta_i = \frac{1 + 1 - 1}{2} = \frac{1}{2}, \qquad \sin^2 \theta_i = 1 - \frac{1}{4} = \frac{3}{4} = \frac{-\det M(1, 1, 1)}{4}.
$$

Under H4, each apex angle is $1/6$ of a turn ($\pi/3$ radians). Summing over the 5 triangles of $K_5$ yields

$$
\Theta_{\mathrm{turn}}(K_5) = \sum_{i=1}^{5} \frac{1}{6} = \frac{5}{6}, \qquad \epsilon_{\mathrm{turn}}(K_5) = 1 - \frac{5}{6} = \frac{1}{6}.
$$

In radians, $\epsilon(K_5) = 2\pi - 5(\pi/3) = \pi/3$. From the certified rational enclosure

$$
\pi \in \left[\frac{3141592653}{10^9}, \frac{3141592654}{10^9}\right],
$$

dividing by $3$ encloses $\epsilon(K_5) = \pi/3$ in

$$
\left[\frac{1047197551}{10^9}, \frac{1047197552}{10^9}\right] = \left[\frac{1047197551}{1000000000}, \frac{130899694}{125000000}\right],
$$

of exact rational width $1/10^9$.

The total star area of $K_5$ is $A_{\mathrm{star}}(K_5) = 5 A_1$, with exact rational square

$$
A_{\mathrm{star}}(K_5)^2 = 25 A_1^2 = \frac{75}{16}.
$$

For the flat six-triangle equilateral star $K_6$, the six apex angles sum to $6 \cdot (1/6) = 1$ full turn, so $\epsilon_{\mathrm{turn}}(K_6) = 0$ and the radian deficit interval is $[0, 0]$.

The pinned receipt also attaches the string `discretization_defect_bound = "|E(a)| <= (1/6) * a^2"` without a smooth comparison surface, mesh parameter $a$, or remainder proof. Evaluating one five-triangle star at edge length $1$ does not derive a quadratic continuum curvature bound.

## Claims this note does not make

- It does not assign $+3$ as the determinant of the $4 \times 4$ unit-triangle Cayley-Menger matrix; the determinant is $-3$, and $(-1)^3 \det M = +3$.
- It does not claim that $\det M > 0$ certifies Euclidean 2-simplex nondegeneracy.
- It does not derive the string `|E(a)| <= (1/6) * a^2` or a convergence bound to the continuum Ricci scalar integral $\frac{1}{2}\int R\sqrt{g}\,d^2x$.
- It does not claim that rational interval enclosures for $\pi/3$ make $\pi$ rational or select the circle from an $\ell_1$ obstruction.
- A finite calculation on this five-triangle star does not establish a continuum limit, a general Delaunay triangulation theorem, or a physical law outside the selected scope.
