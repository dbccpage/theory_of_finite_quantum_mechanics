<div align="center">

# Exact Relational Mechanics and Certified Sign Boundaries of the Fermi-Hubbard Model: Diagonal Sign Gauges, Auxiliary-Field Palindromic Symmetries, and Explicit Negative Witnesses

Jeremy H. Carroll\
2026-10-02 · Version 0.1.0 · Preprint · Research Package

</div>

## Abstract

This paper formalizes the exact relational mechanics and certified sign-problem boundaries of the spinful Fermi-Hubbard model on finite graphs. Using exact rational arithmetic over SQLite with step-wise GCD reduction and zero floating-point operations, we evaluate both the real-space occupation Hamiltonian and the discrete-time auxiliary-field determinant representation.

In the occupation basis, we analyze whether diagonal sign gauges can eliminate negative matrix elements. While open hopping paths admit consistent diagonal sign gauges that make all off-diagonal transitions nonpositive, both the 4-site periodic ring and the 3-leaf star graph encounter negative configuration cycles in their integer Fock occupation masks. Because the 3-leaf star is a physical tree without spatial loops, this establishes in this setting that the absence of spatial cycles does not prevent many-body exchange-loop sign obstructions.

In the auxiliary-field representation, we construct an exact symmetric kinetic matrix $T$ as a palindromic product of bond exponentials, satisfying $\det(T) = 1$ and the particle-hole inversion relation $\eta T \eta = T^{-1}$ on bipartite graphs. For the repulsive model at half filling ($z = 1$), this symmetry enforces $\det(I + P_\downarrow) = \det(I + P_\uparrow) / \det(P_\uparrow)$, ensuring that every field configuration has a non-negative weight $w(s) \ge 0$. For the attractive model ($U < 0$), spin symmetry yields identical propagation matrices, ensuring that the field weight is a non-negative determinant square $w(s) = h^{-\sum s} \det(I + P_\uparrow)^2 \ge 0$ across all geometries, including geometrically frustrated clusters.

Beyond these protected boundaries, we provide explicit rational existence witnesses of negative determinant weights. For the 4-site ring with 4 time slices at fugacity $z = 2$, field mask 15721 produces an exact positive up determinant and a strictly negative down determinant. For the 3-site frustrated triangle at $z = 1$, field mask 1281 yields an exact negative determinant product. Finally, by propagating logarithmic fugacity derivatives in the ring of dual numbers, we evaluate total particle number expectations without requiring singular matrix inversions or division by zero-determinant fields.

This monograph assigns no authorization and changes no jurisdiction. It carries no operational authority or institutional standing.

---

## 1. Introduction

The Fermi-Hubbard model represents a central paradigm in condensed matter physics for studying strong electronic correlations, Mott metal-insulator transitions, and high-temperature superconductivity [1]. In Quantum Monte Carlo (QMC) simulations, fermionic antisymmetry introduces negative weights in configuration expansions, leading to the fermionic sign problem [2, 3]. In its severe manifestations, the average configuration sign $\langle\sigma\rangle$ decays exponentially with spatial volume $V$ and inverse temperature $\beta$:
\[
\langle\sigma\rangle = \frac{\sum_x \sigma(x) W(x)}{\sum_x W(x)} = \frac{Z}{Z_{\mathrm{abs}}} \sim e^{-\beta V \Delta f},
\]
which inflates statistical sampling variance exponentially and limits simulations to high temperatures or small clusters [3].

The sign problem, however, is a property of a *declared mathematical representation*, not an intrinsic attribute of the underlying quantum Hamiltonian. A model may be severely obstructed in the real-space occupation basis while possessing an auxiliary-field representation where all configuration weights are strictly non-negative [2, 4, 7].

This paper provides an exact relational and algebraic investigation of the Fermi-Hubbard sign boundary:
1. **Occupation-Basis Sign Gauges (Section 2)**: Formulating diagonal sign gauges as 1-cochains and demonstrating how many-fermion exchange paths on physical trees generate negative cycles in Fock configuration graphs.
2. **Auxiliary-Field Kinetic Palindrome (Section 3)**: Constructing the kinetic matrix $T$ as a palindromic Suzuki product and verifying the particle-hole inversion symmetry $\eta T \eta = T^{-1}$.
3. **Protected Determinant Sectors (Section 4)**: Verifying exact non-negativity for repulsive half-filled bipartite systems and attractive systems on arbitrary graphs.
4. **Relational SQLite Implementation & Observables (Section 5)**: Implementing matrix products and recursive permutation determinant folds in SQLite with arbitrary-precision rational arithmetic, evaluating particle numbers via dual-number fugacity derivatives.
5. **Explicit Negative Field Witnesses (Section 6)**: Providing exact rational witnesses of negative field weights outside protected symmetry sectors.
6. **Scope, Defensible Claims, and Future Extensions (Section 7)**: Bounding the epistemic conclusions and delineating remaining questions.

---

## 2. Occupation Hamiltonians and Diagonal Sign-Gauge Obstructions

### 2.1 The Spinful Fermi-Hubbard Hamiltonian

We consider the standard spinful Fermi-Hubbard Hamiltonian defined on a finite graph $G = (V_G, E_G)$:
\[
H = -t \sum_{\langle ij\rangle, \sigma} (c_{i\sigma}^\dagger c_{j\sigma} + c_{j\sigma}^\dagger c_{i\sigma}) + U \sum_{i} n_{i\uparrow} n_{i\downarrow} - \mu \sum_{i, \sigma} n_{i\sigma},
\]
where $c_{i\sigma}^\dagger$ and $c_{i\sigma}$ satisfy the canonical anticommutation relations (CAR):
\[
\{c_{i\sigma}, c_{j\sigma'}^\dagger\} = \delta_{ij}\delta_{\sigma\sigma'}, \quad \{c_{i\sigma}, c_{j\sigma'}\} = \{c_{i\sigma}^\dagger, c_{j\sigma'}^\dagger\} = 0.
\]
We adopt a canonical orbital ordering: all spin-up orbitals precede all spin-down orbitals:
\[
\phi = (\uparrow_0, \dots, \uparrow_{L-1}, \downarrow_0, \dots, \downarrow_{L-1}).
\]
The Fock state is represented as an integer bitmask $s = s_\uparrow | (s_\downarrow \ll L)$. The matrix element for a hopping transition between site $a$ and site $b$ carries the Jordan-Wigner CAR sign:
\[
\operatorname{sgn}(s, a, b) = (-1)^{\operatorname{popcount}(s \, \cap \, [a+1, b-1])}.
\]

### 2.2 Diagonal Sign Gauges

In quantum Monte Carlo simulations based on path integrals in the discrete configuration basis, off-diagonal elements $H_{xy}$ ($x \neq y$) contribute with weight proportional to $-H_{xy}$. If all off-diagonal elements satisfy $-H_{xy} \ge 0$ (i.e. $H_{xy} \le 0$), the path expansion is sign-problem free.

A diagonal sign gauge transformation is an assignment of a local sign $d_x \in \{+1, -1\}$ to each basis state $|x\rangle$, inducing the transformed Hamiltonian $\widetilde{H}_{xy} = d_x H_{xy} d_y$. The condition that all off-diagonal elements become non-positive translates to:
\[
d_x H_{xy} d_y \le 0 \iff d_y = a_{xy} d_x, \quad \text{where } a_{xy} = -\operatorname{sgn}(H_{xy}).
\]
This defines a 1-cochain $a \in C^1(G_{\mathrm{Fock}}, \mathbb{F}_2)$. A consistent gauge $d \in C^0(G_{\mathrm{Fock}}, \mathbb{F}_2)$ exists if and only if the cocycle condition holds along every closed cycle $C = (x_0, x_1, \dots, x_k = x_0)$:
\[
\prod_{i=0}^{k-1} a_{x_i x_{i+1}} = +1.
\]

### 2.3 Exact Graph Obstruction Experiments

Using our SQLite evaluator, we test gauge consistency by constructing the signed double cover graph $(x, \pm 1)$. A component where $(x, -1)$ is reachable from $(x, +1)$ witnesses an obstruction and yields the shortest negative configuration cycle.

For $L = 4$ sites, in the interacting sector $(N_\uparrow = 2, N_\downarrow = 1)$ with $U = 4, t = 1, \mu = 0$ (24 basis states), the exact relational results are:

| Hopping Graph Geometry | Bonds | Diagonal Sign Gauge | Negative Configuration Cycle in Fock Masks |
| :--- | :--- | :--- | :--- |
| **Open Path** | $(0,1), (1,2), (2,3)$ | Exists (all $d_x = +1$) | None |
| **Periodic Ring** | $(0,1), (1,2), (2,3), (0,3)$ | Obstructed | $[19, 21, 22, 26, 19]$ (length 4) |
| **3-Leaf Star Tree** | $(0,1), (0,2), (0,3)$ | Obstructed | $[19, 22, 21, 28, 25, 26, 19]$ (length 6) |

**Key Finding:** The 3-leaf star graph contains zero spatial cycles (it is a topological tree). Nevertheless, its many-fermion configuration graph admits an exchange loop of length 6 with an odd product of CAR signs:
\[
\prod_{e \in \text{cycle}} (-1) \cdot \operatorname{sgn}(H_e) = -1.
\]
This demonstrates in this model that the absence of spatial cycles on the physical lattice does not prevent fermionic sign obstructions in the occupation basis. Furthermore, because the obstruction depends solely on off-diagonal hopping signs, it is independent of the value of the on-site interaction $U$.

---

## 3. Auxiliary-Field Representation and Palindromic Symmetries

### 3.1 Discrete Hubbard-Stratonovich Transformation

To bypass the occupation-basis obstruction, we formulate the partition function in the auxiliary-field path integral representation [2, 5]. We adopt the particle-hole symmetric interaction:
\[
H_U = U \sum_i (n_{i\uparrow} - \tfrac{1}{2})(n_{i\downarrow} - \tfrac{1}{2}).
\]
The ordinary chemical potential relates to the centered potential via $\mu_{\mathrm{ord}} = \mu + U/2$.

For repulsive interactions ($U > 0$), the discrete Hubbard-Stratonovich identity decouples the interaction at each site $i$ and time slice $\ell$ via a discrete Ising field $s_{i\ell} \in \{+1, -1\}$:
\[
e^{-\Delta\tau U(n_{i\uparrow} - 1/2)(n_{i\downarrow} - 1/2)} = C \sum_{s_{i\ell} = \pm 1} e^{\lambda s_{i\ell}(n_{i\uparrow} - n_{i\downarrow})},
\]
where the coupling $\lambda$ and normalization $C$ satisfy:
\[
\cosh\lambda = \frac{h + h^{-1}}{2} = e^{\Delta\tau U/2}, \quad C = \frac{1}{2} e^{-\Delta\tau U/4}, \quad h = e^\lambda \ge 1.
\]

For attractive interactions ($U = -|U| < 0$), the decoupling couples to the total charge:
\[
e^{-\Delta\tau U(n_{i\uparrow} - 1/2)(n_{i\downarrow} - 1/2)} = C \sum_{s_{i\ell} = \pm 1} e^{\lambda s_{i\ell}(n_{i\uparrow} + n_{i\downarrow} - 1)}.
\]
This requires a positive field-dependent scalar factor $h^{-\sum s}$ upon factoring into spin determinants.

### 3.2 The Palindromic Suzuki Kinetic Matrix $T$

For each bond $b = (i, j)$, the single-particle hopping exponential with rational parameter $r = e^{\Delta\tau t/2} > 0$ forms the $2 \times 2$ matrix block:
\[
R_{ij}(r) = \begin{pmatrix} (r + r^{-1})/2 & (r - r^{-1})/2 \\ (r - r^{-1})/2 & (r + r^{-1})/2 \end{pmatrix}.
\]
To maintain exact time-reversal invariance and unimodularity, we apply all bond exponentials in lexicographical order followed by their reverse order:
\[
T = \left(\prod_{b \in E_G}^{\to} R_b\right) \left(\prod_{b \in E_G}^{\leftarrow} R_b\right).
\]
By construction, $T$ is real symmetric positive definite, has $\det(T) = 1$, and represents a second-order symmetric Suzuki product.

---

## 4. Protected Determinant Sectors

### 4.1 Particle-Hole Positivity at Half Filling

Let $G$ be a bipartite graph, and let $\eta = \operatorname{diag}(\eta_1, \dots, \eta_L)$ denote the diagonal sublattice operator with $\eta_i = +1$ on sublattice $A$ and $\eta_i = -1$ on sublattice $B$. Because every hopping bond connects opposite sublattices, conjugation by $\eta$ inverts each bond factor: $\eta R_b \eta = R_b^{-1}$. The palindromic product ensures:
\[
\eta T \eta = T^{-1} = T^{-T}.
\]
For $M$ time slices, the one-particle propagation matrices are:
\[
B_{\ell\uparrow} = z T D_\ell, \quad B_{\ell\downarrow} = z T D_\ell^{-1},
\]
where $z = e^{\Delta\tau\mu} > 0$ is the fugacity, and $D_\ell = \operatorname{diag}(h^{s_{1\ell}}, \dots, h^{s_{L\ell}})$. The full propagation matrix is $P_\sigma = B_{M-1,\sigma} \dots B_{0,\sigma}$.

At half filling ($\mu = 0 \implies z = 1$), conjugation by $\eta$ relates the down and up propagation matrices:
\[
B_{\ell\downarrow} = \eta B_{\ell\uparrow}^{-T} \eta \implies P_\downarrow = \eta (P_\uparrow^T)^{-1} \eta.
\]
Using the determinant identity $\det(I + \eta (P^T)^{-1} \eta) = \det(I + P^{-1}) = \det(I + P)/\det(P)$, we obtain:
\[
\det(I + P_\downarrow) = \frac{\det(I + P_\uparrow)}{\det(P_\uparrow)}.
\]
Since $\det(P_\uparrow) = (\det T)^M \prod_{\ell} \det(D_\ell) = h^{\sum s} > 0$, the total configuration weight is:
\[
w(s) = \det(I + P_\uparrow) \det(I + P_\downarrow) = \frac{[\det(I + P_\uparrow)]^2}{\det(P_\uparrow)} \ge 0.
\]
This shows in this setting that every auxiliary-field configuration weight is non-negative, eliminating the sign problem for the repulsive Hubbard model at half filling on bipartite lattices [2].

### 4.2 Attractive Pairing on General Graphs

For the attractive Hubbard model ($U < 0$), the discrete field couples with identical sign to up and down spins: $V_\uparrow = V_\downarrow = z D_\ell$. Consequently, $P_\uparrow = P_\downarrow$, and the field weight is:
\[
w(s) = h^{-\sum s} [\det(I + P_\uparrow)]^2 \ge 0.
\]
Because this result relies solely on spin-inversion symmetry rather than spatial bipartiteness, it yields non-negative weights across all lattice geometries, including non-bipartite and geometrically frustrated clusters.

---

## 5. Relational SQLite Implementation and Non-Singular Observables

### 5.1 Arbitrary-Precision Rational SQLite Evaluator

The evaluation pipeline is implemented in SQLite using custom scalar UDFs (`qadd`, `qmul`, `qdiv`, `qabs`, `qsign`, `qpow`) and a custom aggregate `qsum` that accumulates fractions using Python's arbitrary-precision `fractions.Fraction` class.

Determinants of $(I + P_\sigma)$ are evaluated via a recursive Common Table Expression (CTE) implementing the full permutation expansion:
\[
\det(A) = \sum_{\pi \in S_L} \operatorname{sgn}(\pi) \prod_{i=1}^L A_{i, \pi(i)}.
\]
This provides an inspectable, independent algebraic verification oracle free of numerical roundoff or floating-point instability.

### 5.2 Non-Singular Number Observables via Dual Numbers

Traditional DQMC computes particle density via the Green's function $G = (I + P)^{-1}$, which diverges when $\det(I + P) = 0$. In our relational formulation, we propagate the logarithmic fugacity derivative directly through the permutation expansion in the ring of dual numbers $\mathbb{Q}[\epsilon]/(\epsilon^2)$:
\[
z \frac{d P_{ij}}{dz} = M P_{ij}.
\]
Applying the product rule to the determinant product yields the exact particle number numerator:
\[
N_{\mathrm{num}} = \frac{1}{M} z \frac{d\widetilde{Z}}{dz}, \quad \langle N \rangle = \frac{N_{\mathrm{num}}}{\widetilde{Z}}.
\]
This evaluates exact particle number expectations without matrix inversions, correctly accounting for zero-determinant configurations.

---

## 6. Exact Computational Evidence and Explicit Negative Witnesses

### 6.1 Census of Protected Ensembles

Exhaustive evaluations over complete configuration ensembles confirm non-negativity within the protected sectors:

| Ensemble | Parameters | Total Fields | Average Sign $\langle\sigma\rangle$ | Total Particle Number $\langle N \rangle$ | Independent Trace Verification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Repulsive 4-Site Ring** | $M=2, r=3/2, h=2, z=1$ | 256 | $1$ | $4$ (exact integer) | Auxiliary-field census only; dense Fock replay admits at most three sites |
| **Attractive 3-Site Triangle** | $M=2, r=3/2, h=2, z=3/2$ | 64 | $1$ | $\frac{1776585892008474078571024122583556}{557308765039728024001166872319977}$ | Verified against full Fock trace |
| **Two-Site Repulsive HS** | $M=2, r=3/2, h=2, z=3/2$ | 16 | $1$ | $\frac{412347680162}{172283601361}$ | $\frac{172283601361}{21233664}$ (matches Fock) |
| **Two-Site Attractive HS** | $M=2, r=3/2, h=2, z=3/2$ | 16 | $1$ | $\frac{452633269922}{180365586961}$ | $\frac{180365586961}{21233664}$ (matches Fock) |

### 6.2 Explicit Negative Field Witnesses Outside Protected Sectors

Outside the protected symmetry sectors, configuration weights can be strictly negative. We isolate explicit rational existence witnesses:

1. **Doped 4-Site Bipartite Ring ($z = 2 \neq 1$):**
   For $L = 4, M = 4, r = 2, h = 8, z = 2$, field configuration mask **15721** yields:
   \[
   \det(I + P_\uparrow) = \frac{11072073737867929807204939234025}{2305843009213693952} > 0,
   \]
   \[
   \det(I + P_\downarrow) = -\frac{1034021712177776419381618902295}{147573952589676412928} < 0.
   \]
   The resulting weight product is strictly negative: $w(15721) < 0$.

2. **Frustrated Repulsive 3-Site Triangle at Centered Chemical Potential ($z = 1$):**
   For $L = 3, M = 4, r = 2, h = 8, z = 1$, field configuration mask **1281** yields an exact negative determinant product, demonstrating that non-bipartite frustration breaks the particle-hole determinant pairing.

---

## 7. Scope, Claim Discipline, and Open Questions

In accordance with strict claim hygiene:

1. **What this work supports:**
   - Demonstrates that diagonal sign gauges cannot eliminate many-body exchange loops on physical tree lattices.
   - Shows in this finite model that the palindromic Suzuki construction yields exact determinant pairing $\det(I+P_\downarrow) = \det(I+P_\uparrow)/\det P_\uparrow$ on bipartite graphs at half filling.
   - Records explicit rational witnesses (masks 15721 and 1281) of negative field weights when doping bipartite systems or introducing triangular frustration.

2. **What this work does not support:**
   - Does not establish a polynomial-time sampling algorithm for the general Fermi-Hubbard model away from half filling.
   - Does not prove that all representations of frustrated Hubbard models are NP-hard.
   - Does not claim thermodynamic limit convergence from finite $M$-slice Trotter products without continuum extrapolation.

3. **The Narrowest Defensible Claim:**
   Under exact rational arithmetic, the discrete auxiliary-field Fermi-Hubbard model on bipartite graphs has strictly non-negative weights at half filling ($z=1$), while doped bipartite rings and frustrated triangles admit explicit negative field witnesses that violate determinant positivity.

4. **Next Test Needed:**
   Formulate a topological cluster involution or multi-meron fermion bag pairing in the auxiliary-field space to test whether negative fields can be cancelled pairwise in low-doped regimes.

---

## References

1. J. Hubbard, *Electron Correlations in Narrow Energy Bands*, Proc. R. Soc. Lond. A 276, 238-257 (1963).
2. C. Wu and S.-C. Zhang, *Sufficient condition for absence of the sign problem in the fermionic quantum Monte Carlo algorithm*, Phys. Rev. B 71, 155115 (2005).
3. M. Troyer and U.-J. Wiese, *Computational Complexity and Fundamental Limitations to Fermionic Quantum Monte Carlo Simulations*, Phys. Rev. Lett. 95, 170201 (2005).
4. S. Chandrasekharan and U.-J. Wiese, *Meron-Cluster Solution of a Fermion Sign Problem*, Phys. Rev. Lett. 83, 3116-3119 (1999).
5. R. Blankenbecler, D. J. Scalapino, and R. L. Sugar, *Monte Carlo calculations of coupling of electrons to the order parameter of a two-dimensional system*, Phys. Rev. D 24, 2278-2286 (1981).
6. M. Suzuki, *Fractal decomposition of exponential operators with applications to many-body theories and Monte Carlo simulations*, Phys. Lett. A 146, 319-323 (1990).
7. J. H. Carroll and the Omega Engine Retinue, *Primitive Difference, Fermionic Hamiltonians, and Certified Sign-Problem Boundaries*, Volume I of the FSP Monograph Series (2026).
