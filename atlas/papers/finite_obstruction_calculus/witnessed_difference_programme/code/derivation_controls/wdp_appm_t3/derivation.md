# WDP-APPM-T3

Goal id: WDP-APPM-T3

Selected scope for WDP-APPM-T3 is recorded in this note.

## Selected scope

Labelled finite carriers on the 3D periodic torus $(\mathbb{Z}/4\mathbb{Z})^3$ ($64$ sites) and finite $\mathbb{Z}^3$ cubic chains:

1. All $240$ distinct undirected simple 4-cycles on $(\mathbb{Z}/4\mathbb{Z})^3$: $192$ elementary coordinate plaquettes of lift winding $W = (0, 0, 0)$ ($m = 0$) and $48$ axis-aligned generator 4-cycles of lift winding $W \in \{(\pm 1, 0, 0), (0, \pm 1, 0), (0, 0, \pm 1)\}$ ($m = 1$). With constant weight $A = 1$, baseline sign $s = +1$, and character $\chi_m(u) = (-1)^{m u}$ where $m = (W_x + W_y + W_z) \bmod 2$, the $480$ oriented 4-cycles give exact signed partition $Z = 384$, observable numerator $N = 96$ for $O(u) = (-1)^u$, average sign $4/5$, and expectation $N/Z = 1/4$.
2. Exact integer intersection linking number $\mathrm{Lk}(C_1, C_2) = \langle \Sigma_1, C_2 \rangle \in \mathbb{Z}$ for an explicit pair of disjoint cubic loops in $\mathbb{Z}^3$, giving $\mathrm{Lk}(C_1, C_2) = +1$, orientation-reversed $\mathrm{Lk}(C_1, -C_2) = -1$, and shifted unlinked $\mathrm{Lk}(C_1, C_2^{\mathrm{shift}}) = 0$.
3. Exact parity-character sums $\sum_{x \in (\mathbb{Z}/4\mathbb{Z})^3} (-1)^{k \cdot x} = 64 \delta_{k, 0}$ across all $k \in \{0, 1\}^3$, with exact residual $0$.

Not the pinned narrative strings in `compute_t3_receipt`, not the uncomputed residual bound $10^{-25}$, and not a continuum Dirac determinant on $T^3 \times S^1$.

## Hypotheses

The hypotheses are selected for these finite carriers. Appendix M.5 states that the pinned T3 record only records proposed winding and linking data, and the bridge audit notes that `compute_t3_receipt` assigns string descriptions, a supplied residual bound $10^{-25}$, and `odd_winding_cancellation = True` without supplying 3D loop configurations or computing their invariants.

H1. Sites of the 3-torus carrier are triples $(x, y, z) \in \{0, 1, 2, 3\}^3$. Nearest-neighbour undirected edges connect sites differing by $\pm 1 \bmod 4$ in one coordinate and agreeing in the other two.

H2. Configurations of the 4-cycle ensemble are the two orientations $u \in \{0, 1\}$ of each simple 4-cycle on $(\mathbb{Z}/4\mathbb{Z})^3$. Lifting a directed 4-cycle to $\mathbb{Z}^3$ produces a displacement $4 W$ with $W = (W_x, W_y, W_z) \in \mathbb{Z}^3$ and meron parity bit $m = (W_x + W_y + W_z) \bmod 2$.

H3. Each undirected simple 4-cycle is one complete orbit $U = (\mathbb{Z}/2\mathbb{Z})^1$ with constant weight $A = 1$, baseline sign $s = +1$, sign character $\chi_m(u) = (-1)^{m u}$, and orientation observable $O(u) = (-1)^u$.

H4. For discrete linking in $\mathbb{Z}^3$, let $\Sigma_1$ be the oriented 2-chain of four unit $xy$-plaquettes tiling $[0, 2] \times [0, 2] \times \{0\}$, whose boundary $\partial \Sigma_1 = C_1$ is the counterclockwise 8-edge perimeter loop. A closed 1-cycle $C_2$ on the dual-shifted vertical line $(x, y) \in \mathbb{Z}^2$ disjoint from $C_1$ has linking number $\mathrm{Lk}(C_1, C_2) = \sum_{e \in C_2} I(\Sigma_1, e)$, where $I(\Sigma_1, e) = \pm 1$ when $e$ crosses an interior vertex $(1, 1, 0)$ of $\Sigma_1$ from $z = 0$ to $z = 1$ (or $+1$ for upward crossing through $(1, 1, 0)$ and $-1$ for downward crossing) and $0$ otherwise.

## Derivation

### 1. Simple 4-cycles and winding parity on $(\mathbb{Z}/4\mathbb{Z})^3$

A closed walk of length 4 on $(\mathbb{Z}/4\mathbb{Z})^3$ has lift displacement $4 W = (\Delta x, \Delta y, \Delta z) \in (4\mathbb{Z})^3$ with $|\Delta x| + |\Delta y| + |\Delta z| \le 4$. Thus either:

- Four steps lie along a single positive or negative coordinate direction, giving $W \in \{(\pm 1, 0, 0), (0, \pm 1, 0), (0, 0, \pm 1)\}$ and $m = 1$. For each of the 3 coordinate axes there are $4 \times 4 = 16$ transverse grid lines, yielding $3 \times 16 = 48$ distinct undirected generator 4-cycles.
- Or $W = (0, 0, 0)$ and $m = 0$. As in the 2D analysis, a simple null-homologous 4-cycle cannot use four collinear steps ($\pm e_i, \pm e_i$) without repeating a vertex and staying within diameter $\le 2$. It must use one positive and one negative step in each of two distinct coordinate directions, lying in a single coordinate plane ($xy$, $yz$, or $zx$). In each of the 3 coordinate planes there are 4 parallel slices of $4 \times 4 = 16$ elementary squares, giving $3 \times 4 \times 16 = 192$ distinct undirected plaquette 4-cycles.

Hence there are $192 + 48 = 240$ distinct undirected simple 4-cycles and $480$ oriented 4-cycles. By Appendix M.1:

- On each of the $192$ plaquette orbits ($m = 0$), $Z_U = 1 + 1 = 2$ and $N_U = 1 + (-1) = 0$.
- On each of the $48$ generator string orbits ($m = 1$), orientation reversal $u \mapsto u + 1$ preserves $A = 1$ and flips $\chi_1(u) = (-1)^u$, so $Z_U = 1 + (-1) = 0$, while $\chi_1(u) O(u) = (-1)^{2u} = 1$ gives $N_U = 1 + 1 = 2$.

Summing over all $240$ orbits gives

$$
Z = 192 \cdot 2 + 48 \cdot 0 = 384, \qquad N = 192 \cdot 0 + 48 \cdot 2 = 96,
$$

with average sign $384 / 480 = 4/5$ and normalized expectation $N / Z = 96 / 384 = 1/4$.

### 2. Explicit 3D linking number on cubic 1-cycles

Let $\Sigma_1$ be the $2 \times 2$ square surface in the $z = 0$ plane with corners $(0,0,0), (2,0,0), (2,2,0), (0,2,0)$ and interior lattice vertex $(1,1,0)$. Its boundary $C_1 = \partial \Sigma_1$ lies on $x \in \{0, 2\}$ or $y \in \{0, 2\}$ at $z = 0$.

Define the closed 1-cycle $C_2$ in the $y = 1$ plane by the polygonal loop

$$
(1, 1, -1) \to (1, 1, 0) \to (1, 1, 1) \to (3, 1, 1) \to (3, 1, 0) \to (3, 1, -1) \to (1, 1, -1).
$$

No vertex of $C_2$ lies on $C_1$: at $z = 0$, $C_2$ visits only $(1, 1, 0)$ (strictly inside $\Sigma_1$) and $(3, 1, 0)$ (strictly outside $\Sigma_1$). The upward step $(1, 1, 0) \to (1, 1, 1)$ pierces $\Sigma_1$ positively once, and the downward step $(3, 1, 1) \to (3, 1, 0)$ misses $\Sigma_1$. Therefore

$$
\mathrm{Lk}(C_1, C_2) = +1.
$$

Reversing every directed edge of $C_2$ replaces the piercing step by $(1, 1, 1) \to (1, 1, 0)$ and gives $\mathrm{Lk}(C_1, -C_2) = -1$. Translating $C_2$ by $(+2, 0, 0)$ to $x \in [3, 5]$ moves both $z = 0$ crossings outside $[0, 2] \times [0, 2]$, giving $\mathrm{Lk}(C_1, C_2^{\mathrm{shift}}) = 0$.

### 3. Exact parity-character orthogonality

For each binary wavevector $k = (k_x, k_y, k_z) \in \{0, 1\}^3$ on $(\mathbb{Z}/4\mathbb{Z})^3$, the character sum factors as

$$
\sum_{(x,y,z) \in (\mathbb{Z}/4\mathbb{Z})^3} (-1)^{k_x x + k_y y + k_z z} = \prod_{j \in \{x,y,z\}} \left(\sum_{n=0}^{3} (-1)^{k_j n}\right).
$$

Since $\sum_{n=0}^{3} 1 = 4$ and $\sum_{n=0}^{3} (-1)^n = 1 - 1 + 1 - 1 = 0$, the 3D sum equals $4^3 = 64$ when $k = (0, 0, 0)$ and $0$ for all 7 nonzero $k \in \{0, 1\}^3$. The maximum non-zero-mode residual is the exact integer $0$, not the pinned interval endpoint $10^{-25}$.

## Claims this note does not make

- It does not treat the string labels `W(c) in Z^3`, `I(c) = (Wx + Wy + Wz) mod 2`, or `Lk(c_i, c_j) in Z` in `compute_t3_receipt` as a construction of 3D strings.
- It does not use the arbitrary interval endpoint $10^{-25}$ as a character-orthogonality residual.
- It does not derive a relativistic Dirac functional determinant on $T^3 \times S^1$ or a polynomial-time 3D cluster Monte Carlo algorithm.
- It does not claim that cancelling the 48 odd-winding 4-cycle orbits preserves an observable whose odd-character Fourier coefficient is nonzero; for $O(u) = (-1)^u$, the numerator $N = 96$ comes entirely from those 48 odd orbits.
- A finite model on $(\mathbb{Z}/4\mathbb{Z})^3$ does not establish a continuum limit, a physical law, or a closed theorem outside the selected scope.
