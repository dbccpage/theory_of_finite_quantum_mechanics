# Primitive Difference, Fermionic Hamiltonians, and Certified Sign-Problem Boundaries

**Subtitle:** A Conditional Derivation from Inscription Cuts to Exterior Algebras, Admitted Many-Body Dynamics, Signed Statistical Estimators, and Certified Algorithmic Boundaries
**Author:** Jeremy H. Carroll and the Omega Engine Retinue
**Date:** 2026-10-02
**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)
**Status:** Unified Master Monograph Volume (v2.5.0, research extension)
**Primary Reference:** `sealed-derivation-v1` (commit `3100c4e`)
**AuthorityEffect:** None

---

## Executive Summary & Epistemic Scope

This monograph investigates the conditional mathematical connection between foundational discrete distinctions, fermionic operator algebras, admitted many-body Hamiltonians, and the Quantum Monte Carlo (QMC) fermion sign problem.

Under strict claim discipline, we establish the following epistemic boundaries:

1. **The Inscription is Not Physics**: The primitive bracket inscription $\langle\rangle$ is an opaque syntactic mark. It does not inherently supply a geometry, a spacetime manifold, a physical vacuum, or a dynamical Hamiltonian.
2. **Conditional Construction**: To obtain physical fermionic physics, specific mathematical structures must be explicitly *admitted*: a complex vector space $V$ with an inner product, an exterior Fock algebra $\mathcal{F}_-(V)$, and a Hermitian operator $H = H^\dagger$ satisfying particle conservation and spatial locality constraints.
3. **Non-Uniqueness of Dynamics**: The canonical anticommutation relations (CAR) do not select a unique Hamiltonian. $H=0$, free hopping networks, and interacting Fermi-Hubbard models all respect the identical CAR algebra. A physical Hamiltonian requires empirical selection principles, not deductive emergence from $\langle\rangle$ alone.
4. **Representation-Dependent Negativity**: A negative sign in a path expansion is a property of a *declared representation*, not an intrinsic property of the underlying quantum state. For example, the 3-site free fermion triangle is frustrated in the occupation basis, but exactly solvable in polynomial time ($O(N^3)$) via single-particle eigenmode diagonalization.
5. **Exact Certification**: We construct exact normal forms for two declared equivalence relations, reconstruct a physical meron transfer sum using SQL, and certify determinant positivity for protected Hubbard representations. Exact negative Hubbard witnesses delimit those protections. Finite enumeration, sign elimination, and efficient sampling are separate conclusions.

The monograph develops across ten systematic sections:

1. **The Operational Distinction Matrix**: Separating supply, admission, witness, and observation.
2. **Genesis of Distinction & The Assumption Ledger**: Tracing $D_2$ and $S_2$, exterior Fock construction, and pricing every admitted structure.
3. **Discrete Fermionic Hamiltonians & Non-Uniqueness**: Constructing $H$, demonstrating non-uniqueness, and separating thermal evolution from the Wheeler-DeWitt constraint.
4. **Signed Statistical Estimators & The Free Triangle Benchmark**: Exact thermal oracles, Trotter discretization error bounds, and basis-dependent solvability.
5. **Part I–III: Cochains, Involution Packets, and Banach Quotients**: The $L^1$ quotient norm $\Phi_1 = \|q\|_{Q^1}$ and five-fold deterministic terminal routing.
6. **Part IV: Computational Complexity & Representation Models**: Formal definitions of $\mathbf{P}$, $\mathbf{NP}$, and withdrawal of unproved cochain arity theorems.
7. **Part V: The Troyer-Wiese Theorem**: Exact formulation as an energy-threshold decision problem under controlled approximation promise.
8. **Part VI: The Ascent Ladder & Relational Pricing Walk**: 17-row pricing audit tracking the passage from void to complexity walls.
9. **Hamiltonian GIN Architecture & Advanced Physics Modules**: Relational inverted indices over bipartite rings, frustrated clusters, sweet-spot Kitaev chains, non-abelian gauge sectors, and supersymmetric doublets.
10. **Formal Mechanization and New Extensions**: Conditional Lean lemmas, exact normal-form proofs, model-derived SQL reconstructions and explicit remaining algorithmic questions (Sections 11–17).

---

## Section 1: Unified Mechanism Matrix

Every structural component in this monograph is registered in the CODA Mechanism Matrix under strict claim discipline:

| Mechanism Slot | Binding Across the Monograph Sequence |
| :--- | :--- |
| **Primitive Differences** | Witnessed distinction under irreflexivity: $\delta c = \text{defect mass}$ in cochains; operational divergence between execution paths; asymmetric boundary $\partial(u \to v) = v - u \neq 0$; sign flip $\sigma \mapsto -\sigma$. |
| **Carriers / Structure** | Finite carriers throughout: one-point carrier at the void; two-point oriented carrier at first difference; finite graphs; discrete Fock spaces $\mathcal{F}$; finite Trotter slices $\mathcal{P}$. Unbounded carriers enter strictly as priced imports. |
| **Cochain Complex** | Rational complexes $C^0 \xrightarrow{d_0} C^1 \xrightarrow{d_1} C^2$ over $\mathbb{Q}$ (and parity cochains over $\mathbb{F}_2$). Nilpotency $d_1 \circ d_0 = 0$ holds natively. |
| **Coboundary Maps** | $d_0$ acts as gauge repair; $d_1$ acts as closure detector. |
| **ZeroRel** | Two configurations or paths are equivalent under observation when all admitted tests yield identical readouts. Preserved under $L^1$ quotient. |
| **Licensed Repairs** | Explicit gauge shifts $\alpha \in C^0$; involution partner cancellations supported by certified finite witnesses $\Xi$. |
| **Quotient / $Q^1$** | Banach quotient $Q^1 = C^1 / \mathrm{im}(d_0)$ equipped with the quotient $L^1$ norm $\|q\|_{Q^1} = \inf_{c^0} \|c^1 - d_0 c^0\|_{C^1}$. |
| **Residuals** | $\Phi_1 = \|q\|_{Q^1}$ (residual sign defect mass); $\overline{d}_1(q)$ (closure obstruction); $\Gamma_2(q) = \|\overline{d}_1(q)\|_{C^2}$ (scalar obstruction). |
| **Witnesses** | Involution witness $\Xi$ (fixed-point-free, sign-reversing, weight-preserving); gauge witness $\alpha$; GIN posting list inverted index; replayable Lean 4, Python, and SQL certifiers. |
| **Observers / Profiles** | Operational observer with visibility window, weight readout $W$, and sign evaluation $h_{\mathrm{sign}}$. |
| **Anomalons** | None declared in this sequence. |
| **CompletionLaw** | Finite cochain completion; stepwise GCD-reduced exact rational folding. |
| **Terminal / Route** | Deterministic routing: `ExactRepair`, `ExactCancellation`, `StabilizedSurvivor`, `OpenSignObstruction`, `SplitBrainRefusal`, `Refused`. |
| **AuthorityEffect** | `None`. All results operate under declared finite settings without ungrounded authority promotion. |

---

## Section 2: Genesis of Distinction, Assumption Ledger, and Exterior Algebra

### 2.1 The Four Epistemic Operations: Supply, Admission, Witness, and Observation

To eliminate category errors, we distinguish four distinct mathematical operations:

1. **Supply**: The syntactic marks provided initially (e.g., the inscription $\langle\rangle$, the discrete labels $a, b$).
2. **Admission**: Postulated structures added by definition (e.g., admitting a complex field $\mathbb{C}$, an inner product, an exterior Fock space $\mathcal{F}_-(V)$, a Hamiltonian $H$, or a thermodynamic temperature $\beta$).
3. **Witness**: An executable or verifiable finite certificate establishing a mathematical relation (e.g., an explicit matrix diagonalization, an exact involution bijection $\Xi$, or a closed cycle path).
4. **Observation**: Readouts obtained by applying an admitted operator to a state or ensemble (e.g., the average sign $\langle\text{Sign}\rangle$, energy expectation $\langle E \rangle$, or occupation number $\langle n_i \rangle$).

### 2.2 The Inscription $\langle\rangle$ and The Genesis Walk

The derivation begins with the bare inscription:

- **Stage 0 (The Inscription $\langle\rangle$)**: $\langle\rangle$ is an uninterpreted mark. It possesses no metric, no state space, no vacuum expectation, and no equations of motion.
- **Stage 1 (The Lone Mark $\langle a\rangle$)**: An isolated distinction is marked: $X_1 = \{a\}$.
- **Stage 2 (The Unmarked Pair $\langle ab\rangle$)**: Two distinct marks are admitted: $X_2 = \{a, b\}$. In the absence of a relation, set membership cannot distinguish $a$ from $b$.
- **Stage 3 (The Directed Cut $\langle arb\rangle$ — The Directed Branch $D_2$)**:
  Admitting an irreflexive relation $R = \{(a, b)\}$ yields the directed 1-simplex edge $e = (a \to b)$.
  Its oriented 1-chain boundary is:
  $$\partial_1(e) = b - a \neq 0$$
  The automorphism group is rigid: $\mathrm{Aut}(D_2) = \{\mathrm{id}\}$.
  Under edge reversal $\mathrm{rev}(e) = (b \to a)$, the boundary flips sign:
  $$\partial_1(\mathrm{rev}(e)) = a - b = -\partial_1(e)$$
  *Crucial Scope Note*: This sign flip is an identity on **oriented 1-chains**. It is an algebraic analogy for antisymmetry, not yet a physical fermion.
- **Stage 4 (The Symmetrized Link $\langle a=b\rangle$ — The Symmetric Branch $S_2$)**:
  Admitting the symmetric relation $R_{\mathrm{sym}} = \{(a, b), (b, a)\}$ yields the unoriented link:
  $$\mathrm{Aut}(S_2) = \mathbb{Z}_2$$
  Exchange leaves the relation invariant: $\tau(S_2) = S_2$.
  *Preservation of Both Branches*: A disciplined foundation must retain both $D_2$ and $S_2$. The directed relation must not eliminate the relational symmetric branch without proof.
- **Stage 5 (Swap-Invariant Predicate Blindness)**:
  Any observer testing only symmetric properties (e.g., edge count, vertex degree, unoriented connectivity) is completely blind to the orientation difference between $D_2$ and $\mathrm{rev}(D_2)$ (`Lean 4: swap_invariant_blind`). Detecting orientation requires coupling to an oriented cochain differential.

### 2.3 The Assumption Ledger

Every structure admitted to bridge the primitive cut to quantum statistical mechanics is priced explicitly in the **Assumption Ledger**:

| Structure Admitted | Mathematical Motivation | Alternatives Retained | Mathematical Consequence | Formal Evidence |
| :--- | :--- | :--- | :--- | :--- |
| **Carrier Distinction $X = \{a, b\}$** | Witnessing non-empty points | Trivial empty carrier $X_0 = \emptyset$ | Distinct endpoints $a \neq b$ under irreflexivity | `cut_endpoints_distinct` |
| **Dual Branches $D_2$ & $S_2$** | Algebraic classification of 2-point relations | Discarding symmetric branch (refused) | $D_2$: oriented cut ($\mathrm{Aut}=\{\mathrm{id}\}$); $S_2$: unoriented link ($\mathrm{Aut}=\mathbb{Z}_2$) | `swap_invariant_blind` |
| **Complex Mode Space $V \cong \mathbb{C}^N$ & $\langle \cdot, \cdot \rangle$** | Linear modal representation of sites/orbitals | Real vector spaces; non-metric graphs; quaternions | Orthonormal basis $\{e_i\}_{i=1}^N$ defining creation/annihilation operators | Admitted Mode Basis |
| **Exterior Fock Space $\mathcal{F}_-(V) = \bigoplus_{k=0}^N \bigwedge^k V$** | Constructing multi-mode antisymmetric states | Symmetric Fock space $\mathcal{F}_+(V)$ (bosons); para-statistics | Creation $c_i^\dagger = e_i \wedge -$ and interior annihilation $c_i = \iota_{e_i}$ satisfy CAR: $\{c_i, c_j^\dagger\} = \delta_{ij}$, $\{c_i, c_j\} = 0$ | Exterior CAR Theorem |
| **Hermitian Operator $H = H^\dagger$** | Real physical spectra and unitary time evolution | Non-Hermitian / dissipative Liouvillians | Real eigenvalues $\lambda_k$; strictly positive thermal trace $\operatorname{Tr}(e^{-\beta H}) > 0$ | Spectral decomposition |
| **Particle Number Conservation $[H, N] = 0$** | $U(1)$ phase invariance | Superconducting pairing ($c_i^\dagger c_j^\dagger + \text{h.c.}$) | Block-diagonal sector structure $\mathcal{F}_-(V) = \bigoplus_{n=0}^N \mathcal{H}_n$ | Sector projections |
| **Locality Graph $G = (V_G, E_G)$ and Real Hopping $t$** | Spatial geometric connectivity | All-to-all random coupling (SYK); non-local models | Hopping matrix $h_{ij} = -t$ for $(i, j) \in E_G$ | Graph Laplacian structure |
| **Hubbard Interaction $U$** | On-site Coulomb correlation | Long-range Coulomb; zero interaction ($U=0$) | Diagonal energy shift $U \sum_i n_{i\uparrow} n_{i\downarrow}$ in Fock basis | Diagonal matrix entries |
| **Thermal Parameter $\beta > 0$** | Finite-temperature canonical ensemble | Zero-temperature ground state; real-time dynamics | Well-defined partition trace $Z(\beta) = \operatorname{Tr}(e^{-\beta H})$ | Exact thermal oracle |

### 2.4 Construction of the Exterior Fock Algebra & Canonical Anticommutation Relations (CAR)

Given the admitted $N$-dimensional complex vector space $V$ with orthonormal basis $\{e_1, \dots, e_N\}$:

1. The **exterior Fock space** is defined as:
   $$\mathcal{F}_-(V) = \bigoplus_{k=0}^N \bigwedge^k V, \quad \dim \mathcal{F}_-(V) = 2^N$$
2. For each basis vector $e_i$, the **creation operator** $c_i^\dagger: \bigwedge^k V \to \bigwedge^{k+1} V$ acts by exterior multiplication:
   $$c_i^\dagger(\omega) = e_i \wedge \omega$$
3. The **annihilation operator** $c_i: \bigwedge^k V \to \bigwedge^{k-1} V$ is defined as the adjoint with respect to the induced inner product, acting as interior contraction $\iota_{e_i}$.
4. From the antisymmetry of the exterior product $e_i \wedge e_j = -e_j \wedge e_i$, the operators satisfy the **Canonical Anticommutation Relations (CAR)**:
   $$\{c_i^\dagger, c_j^\dagger\} = c_i^\dagger c_j^\dagger + c_j^\dagger c_i^\dagger = 0$$
   $$\{c_i, c_j\} = c_i c_j + c_j c_i = 0$$
   $$\{c_i, c_j^\dagger\} = \langle e_i, e_j \rangle \mathbf{1} = \delta_{ij} \mathbf{1}$$

*The Bosonic Contrast*: Had we instead chosen the symmetric tensor algebra $\mathcal{F}_+(V) = \bigoplus_{k=0}^\infty \operatorname{Sym}^k(V)$, creation by symmetrized tensor product would yield the **Canonical Commutation Relations (CCR)** $[b_i, b_j^\dagger] = \delta_{ij}$. This explicitly isolates where the statistics choice enters: it is an admitted algebraic postulate, not a theorem proved by a 2-point directed graph.

*Separating Exchange Antisymmetry from Physical Spin-Statistics*: The algebraic CAR $\{c_i, c_j^\dagger\} = \delta_{ij}$ describes abstract mode anticommutation. Identifying these mathematical modes with physical spin-1/2 particles requires additional physical structure: a 4D Minkowski spacetime, the Lorentz group $\mathrm{SO}(1, 3)$, microcausality, and the relativistic spin-statistics theorem (Pauli 1940). This physical bridge remains outside the scope of discrete finite graph inscriptions.

### 2.5 Discrete Fermionic Hamiltonians: Allowed Form, Exact 2-Site Hand Calculation, and Non-Uniqueness

Given the CAR algebra generated by $\{c_i, c_i^\dagger\}_{i=1}^N$ on $\mathcal{F}_-(V)$, any operator $H$ is an element of the endomorphism algebra $\operatorname{End}(\mathcal{F}_-(V))$. We derive the allowed form under explicitly priced constraints:

1. **Admitted Constraints**:
   - **Constraint 1 (Hermiticity)**: $H = H^\dagger$ ensures real eigenvalues $E_k \in \mathbb{R}$ and unitary time evolution $e^{-iHt}$.
   - **Constraint 2 (Particle Number Conservation)**: $[H, N] = 0$ with $N = \sum_{i=1}^N c_i^\dagger c_i$. This restricts $H$ to monomials with equal numbers of creation and annihilation operators. **Separately admit a one- and two-body truncation and suppress the scalar identity term** to obtain:
     $$H = \sum_{i,j=1}^N h_{ij} c_i^\dagger c_j + \frac{1}{2} \sum_{i,j,k,l=1}^N V_{ijkl} c_i^\dagger c_j^\dagger c_l c_k$$
     where $h_{ji} = h_{ij}^*$ and $V_{klij}^* = V_{ijkl}$.
   - **Constraint 3 (Spatial Locality Graph)**: For a declared graph $G = (V_G, E_G)$, single-particle hopping is restricted to edges: $h_{ij} = -t$ for $(i, j) \in E_G$ and $0$ otherwise.
   - **Constraint 4 (Spin & On-Site Interaction)**: Adding spin $\sigma \in \{\uparrow, \downarrow\}$ and local on-site Coulomb repulsion yields the Fermi-Hubbard Hamiltonian:
     $$H = -t \sum_{\langle i, j \rangle, \sigma} (c_{i\sigma}^\dagger c_{j\sigma} + \text{h.c.}) + U \sum_{i=1}^{N_{\text{sites}}} n_{i\uparrow} n_{i\downarrow}$$

2. **Explicit 2-Site Hand Calculation**:
   Consider a 2-site lattice with 1 spin-up and 1 spin-down fermion ($N_{\text{sites}} = 2, n_\uparrow = 1, n_\downarrow = 1$). The physical Fock sector has dimension $\binom{2}{1} \times \binom{2}{1} = 4$:
   - Basis states:
     - $|1\rangle = c_{1\uparrow}^\dagger c_{1\downarrow}^\dagger |0\rangle = |\uparrow\downarrow, 0\rangle$ (doubly occupied site 1)
     - $|2\rangle = c_{1\uparrow}^\dagger c_{2\downarrow}^\dagger |0\rangle = |\uparrow, \downarrow\rangle$
     - $|3\rangle = c_{2\uparrow}^\dagger c_{1\downarrow}^\dagger |0\rangle = |\downarrow, \uparrow\rangle$
     - $|4\rangle = c_{2\uparrow}^\dagger c_{2\downarrow}^\dagger |0\rangle = |0, \uparrow\downarrow\rangle$ (doubly occupied site 2)
   - Matrix elements:
     - On-site interaction: $\langle 1|H|1\rangle = U$, $\langle 4|H|4\rangle = U$, $\langle 2|H|2\rangle = 0$, $\langle 3|H|3\rangle = 0$.
     - Hopping transitions:
       $$c_{2\downarrow}^\dagger c_{1\downarrow} |1\rangle = c_{2\downarrow}^\dagger c_{1\downarrow} c_{1\uparrow}^\dagger c_{1\downarrow}^\dagger |0\rangle = + c_{1\uparrow}^\dagger c_{2\downarrow}^\dagger |0\rangle = |2\rangle \implies \langle 2|H|1\rangle = -t$$
       $$c_{2\uparrow}^\dagger c_{1\uparrow} |1\rangle = c_{2\uparrow}^\dagger c_{1\uparrow} c_{1\uparrow}^\dagger c_{1\downarrow}^\dagger |0\rangle = c_{2\uparrow}^\dagger c_{1\downarrow}^\dagger |0\rangle = |3\rangle \implies \langle 3|H|1\rangle = -t$$
     - The complete Hamiltonian matrix is real and symmetric:
       $$H = \begin{pmatrix} U & -t & -t & 0 \\ -t & 0 & 0 & -t \\ -t & 0 & 0 & -t \\ 0 & -t & -t & U \end{pmatrix}$$
     - For $U=0, t=1$:
       The eigenvalues are $\lambda \in \{-2, 0, 0, 2\}$.
       The exact thermal partition function is strictly positive for any finite real $\beta$:
       $$Z_{\text{exact}} = \operatorname{Tr}(e^{-\beta H}) = e^{2\beta} + 2 + e^{-2\beta} = (e^\beta + e^{-\beta})^2 > 0$$

3. **Proof of Hamiltonian Non-Uniqueness**:
   The CAR algebra $\{c_i, c_j^\dagger\} = \delta_{ij}$ alone does not select a unique Hamiltonian. For example:
   - The trivial operator $H_0 = 0$ satisfies CAR, Hermiticity, and particle conservation.
   - The free hopping operator $H_{\text{free}} = -t \sum_{\langle i, j \rangle} c_i^\dagger c_j$ satisfies the exact same CAR.
   - The interacting Hubbard operator $H(t, U)$ satisfies the exact same CAR for any $t, U \in \mathbb{R}$.
   Because $\|H_0 - H(t, U)\| > 0$ for non-zero parameters, the algebraic structure of $\mathcal{F}_-(V)$ admits infinitely many inequivalent dynamics. The choice of a physical Hamiltonian requires an external physical selection principle, not deduction from the primitive inscription $\langle\rangle$.

4. **Distinctness of Thermal Evolution and Wheeler-DeWitt Gravitational Constraints**:
   - The **thermal Hamiltonian** $H$ acts on a state vector space $\mathcal{F}_-(V)$ to generate canonical ensemble weights $e^{-\beta H}$ in imaginary time $\tau$. Its physical states are unconstrained vectors in Fock space.
   - The **Wheeler-DeWitt constraint** $H_\perp$ is an operator constraint on the space of 3-geometries in canonical quantum gravity, encoding normal deformations of a spatial hypersurface via the formal constraint $H_\perp |\Psi\rangle = 0$.
   - Conflating the two mistakes statistical thermodynamic ensembles with quantum gravitational gauge constraints.

### 2.6 Signed Statistical Estimators, Observable Preservation, and The Free Triangle Benchmark

1. **The Sampling Representation**:
   Any numerical Monte Carlo evaluation requires a declared representation: an orbital basis $\{|s\rangle\}$ and an operator expansion (e.g., discrete Trotter slices $e^{-\Delta\tau H} \approx I - \Delta\tau H$).
   - Closed path weight: $W(c) = \langle s_0 | T | s_{M-1} \rangle \dots \langle s_1 | T | s_0 \rangle$.
   - Sign: $\sigma(c) = \operatorname{sgn}(W(c)) \in \{+1, -1\}$.
   - Operational absolute ensemble: $Z_{\text{abs}} = \sum_c |W(c)|$. Note that $Z_{\text{abs}}$ is defined operationally by taking the absolute value of the path amplitudes; it is not generally a separately realizable physical bosonic system.
   - Average sign:
     $$\langle \text{Sign} \rangle = \frac{Z}{Z_{\text{abs}}} = \frac{\sum_c \sigma(c) |W(c)|}{\sum_c |W(c)|}$$
   - Independent Monte Carlo sign estimator $\overline{\sigma} = \frac{1}{M_s} \sum_{k=1}^{M_s} \sigma(c_k)$ with samples $c_k \sim |W(c)| / Z_{\text{abs}}$.
   - Variance and Relative Error:
     $$\operatorname{Var}(\overline{\sigma}) = \frac{1 - \langle\text{Sign}\rangle^2}{M_s} \implies \frac{\sqrt{\operatorname{Var}(\overline{\sigma})}}{\langle\text{Sign}\rangle} = \frac{\sqrt{1 - \langle\text{Sign}\rangle^2}}{\sqrt{M_s} \langle\text{Sign}\rangle}$$
     If $\langle\text{Sign}\rangle = e^{-\beta N \Delta f}$ with an extensive free-energy density gap $\Delta f > 0$, achieving fixed relative error requires $M_s = \Omega(e^{2\beta N \Delta f})$ independent samples.

2. **Observable Preservation Requirement**:
   When estimating a physical observable $A$:
   $$\langle A \rangle = \frac{\sum_c A(c) \sigma(c) |W(c)|}{\sum_c \sigma(c) |W(c)|}$$
   Suppose an involution pairs opposite-sign configurations $(c_+, c_-)$ with equal weight $W(c_+) = W(c_-)$ and $\sigma(c_+) = -\sigma(c_-)$.
   In the partition function denominator, their sum cancels identically:
   $$\sigma(c_+) W(c_+) + \sigma(c_-) W(c_-) = 0$$
   However, in the observable numerator, their contribution is:
   $$A(c_+) W(c_+) - A(c_-) W(c_-) = [A(c_+) - A(c_-)] W(c_+)$$
   Unless the observable is strictly invariant under the pairing ($A(c_+) = A(c_-)$), pair cancellation in the denominator does not cancel the numerator! Deleting cancelling pairs from the ensemble modifies the expectation value $\langle A \rangle$. Pair cancellation alone is a partition function property, not a complete thermal observable solver.

3. **The Free Triangle as the Canonical Benchmark of Representation-Dependent Negativity**:
   Consider a 3-site spinless triangle cluster ($t=1.0, U=0.0$) with 2 identical fermions.
   - The single-particle Hamiltonian matrix is:
     $$h = \begin{pmatrix} 0 & -t & -t \\ -t & 0 & -t \\ -t & -t & 0 \end{pmatrix}$$
     with single-particle eigenvalues $\epsilon \in \{-2t, t, t\}$.
   - In the 2-fermion sector (basis $|110\rangle, |101\rangle, |011\rangle$), the many-body eigenvalues are sums of two distinct single-particle energies:
     $$E_1 = -2t + t = -t, \quad E_2 = -2t + t = -t, \quad E_3 = t + t = 2t$$
     For $t=1.0$, the eigenvalues are $\{-1, -1, 2\}$.
   - The exact thermal partition function at $\beta=2.0$ is:
     $$Z_{\text{exact}} = 2 e^2 + e^{-4} \approx 14.796427836750041$$
   - In the real-space occupation basis, Trotter paths traversing the frustrated odd cycle have negative Jordan-Wigner signs ($w_- = 0.296296$ vs $w_+ \in \{0.444444, 1.0\}$).
   - In the single-particle eigenmode basis, $H$ is diagonal, all off-diagonal transitions vanish, and the model is solved exactly in $O(N^3)$ polynomial time.
   - **Definite Epistemic Finding**: The triangle is NOT an NP-hard problem; it is the primary benchmark demonstrating that the sign problem is representation-dependent and solved by changing bases.

---

## Section 3: Part I — Binary Computational Projections and the Halting Quotient

The foundational obstruction of computational observation begins with how machine executions are summarized at terminal boundaries.

### 3.1 Operational Behavior Space

Let $\mathcal{B}$ denote the space of machine execution behaviors. In any expressive operational model, $\mathcal{B}$ includes witnesses of distinct operational termination classes:

- $\mathrm{Completed}(v, \tau)$: Execution finishes with returned value $v$ and finite trace $\tau$.
- $\mathrm{Refused}(r, \tau)$: Execution is formally rejected with typed refusal reason $r$.
- $\mathrm{Exhausted}(k, \tau)$: Execution exceeds declared resource bound $k$ (fuel, memory, or depth).
- $\mathrm{Awaiting}(w, \tau)$: Execution pauses awaiting an external witness or authorization $w$.
- $\mathrm{Quiescent}(s, \tau)$: Execution enters a live, non-terminating equilibrium state.
- $\mathrm{Absorbed}(t, \tau)$: Execution is trapped in a terminal cycle.

### 3.2 The Non-Faithful Halting Projection

The classical halting abstraction projects this rich operational space via a binary map:
$$\pi_{\mathrm{halt}}: \mathcal{B} \to \{0, 1\}$$
where $\pi_{\mathrm{halt}}(b) = 1$ if execution reaches a selected terminal state, and $0$ otherwise.

Under primitive projection obstruction, the equivalence relation $\sim_{\pi}$ induced by $\pi_{\mathrm{halt}}$ conflates behaviors with incompatible operational semantics:
$$\mathrm{Completed}(v, \tau) \sim_{\pi} \mathrm{Refused}(r, \tau')$$
$$\mathrm{Quiescent}(s, \tau) \sim_{\pi} \mathrm{Absorbed}(t, \tau')$$

Consequently, no binary observation can faithfully carry any target functional that separates three or more distinct operational outcome classes. The loss of trace distinction is an intrinsic defect of binary projection quotients, independent of undecidability.

---

## Section 4: Part II — Topological Meron Clusters and Involution Cancellations

In quantum statistical mechanics, thermodynamic expectation values are evaluated via path integrals over configuration spaces $\mathcal{S}$:
$$\langle A \rangle = \frac{\sum_{x \in \mathcal{S}} A(x) \sigma(x) W(x)}{\sum_{x \in \mathcal{S}} \sigma(x) W(x)}$$
where $W(x) \ge 0$ and $\sigma(x) \in \{+1, -1\}$. When positive and negative contributions nearly cancel, the average sign:
$$\langle \sigma \rangle = \frac{\sum_{x} \sigma(x) W(x)}{\sum_{x} W(x)} = \frac{Z}{Z_{\mathrm{abs}}} \sim e^{-\beta V \Delta f}$$
decays exponentially with spatial volume $V$ and inverse temperature $\beta$. The relative variance of the average-sign estimator grows as $\sim e^{2\beta V \Delta f}/M_s$ under this extensive-gap assumption; the variance of one sign sample remains at most one.

### 4.1 Meron Cluster Solutions

For models admitting independent weight-preserving cluster flips, a factorized sign character, and a positive zero-meron sector, meron-cluster decompositions eliminate negative orbit weights. Half filling or bipartiteness alone does not establish these hypotheses. The configuration space $\mathcal{S}$ is partitioned into independent topological clusters. A cluster with an odd topological charge (a meron) flips the global sign $\sigma \to -\sigma$ under a local coordinate transformation.

### 4.2 The Involution Theorem

Part II establishes the formal conditions under which sign cancellation is achieved:

**Withdrawal in place (2026-09-22).** The previous “if and only if” between zero signed mass and an equal-weight involution is false. The three weights $+2,-1,-1$ sum to zero but admit no equal-weight opposite-sign partner for the positive term.

**Proposition (sufficient pair cancellation).** On a finite subset $S_0$ of a configuration space, let $\Xi:S_0\to S_0$ be an involution with no fixed points, opposite signs and equal nonnegative magnitudes. Partitioning $S_0$ into doublets gives $\sum_{x\in S_0}\sigma(x)W(x)=0$. The observable numerator also vanishes when $A\circ\Xi=A$ on $S_0$; otherwise retain its signed orbit sum. This theorem requires no cochain closure assumption.

There is an exact converse for the **specified pairing class**: every negative configuration can be paired injectively with an equal-weight positive configuration iff, for every magnitude $w>0$, the count of positive configurations of magnitude $w$ is at least the corresponding negative count. Necessity follows from injectivity in each weight fiber; sufficiency follows by ordering and pairing within each fiber. Unmatched positive configurations survive. This is a finite matching theorem, not a theorem selecting a physical symmetry or a polynomial algorithm in lattice size. If no positive mass survives, the partition sum is zero and there is no normalized residual probability ensemble.

---

## Section 5: Part III — Finite Sign Obstruction Packets and the Rational Quotient

Part III formalizes the canonical finite sign obstruction packet architecture:

```text
       d0                 d1
C^0 --------> C^1 -----------------> C^2
(0-cochains)  (1-cochains)        (2-cochains)
```

### 5.1 Cohomological Structure and Quotient Metrics

- $C^0$: Configurations with local gauge transformations.
- $C^1$: Edge differences carrying signed weights.
- $C^2$: Faces measuring non-trivial flux or closure failures.
- Nilpotency: $d_1 \circ d_0 = 0$ holds natively on all cellular carriers.

For a declared linear cochain model, measure the quotient residual by:
$$Q^1 = C^1 / \mathrm{im}(d_0), \quad \|q\|_{Q^1} = \inf_{c^0 \in C^0} \|c^1 - d_0 c^0\|_{C^1}$$

The closure defect is defined on classes $q = [c^1] \in Q^1$ by:
$$\overline{d}_1(q) = d_1(c^1)$$
which is well-defined because $d_1(\mathrm{im}(d_0)) = 0$. The scalar curvature is $\Gamma_2(q) = \|\overline{d}_1(q)\|_{C^2}$.

Over $\mathbb Q$ this is a rational normed quotient, not a Banach space: $\mathbb Q$ is not complete. A finite-dimensional real scalar extension is Banach and has the same exact rational linear-program optimum on rational input. Neither the quotient norm nor $d_1c$ becomes a physical sign severity without a proved adapter relating it to the signed ensemble. In particular $d_1c=0$ does not imply $c\in\operatorname{im}d_0$.

### 5.2 Deterministic Five-Fold Terminal Routing

The following are operational routing labels after validating the supplied complex and witnesses. They are not themselves normal forms, physical sign theorems, or exhaustive algorithmic possibilities:

1. **`ExactRepair`** ($\Phi_1 = 0$): Sign fluctuations are gauge artifacts removable by a shift $c^0 \in C^0$.
2. **`ExactCancellation`** ($\Phi_1 > 0, \Gamma_2 = 0$, witness $\Xi$ present): Closed survivor cancelled by an explicit involution pairing.
3. **`StabilizedSurvivor`** ($\Phi_1 > 0, \Gamma_2 = 0$, no involution): A non-vanishing closed defect with no validated cancellation witness in the supplied packet; lack of a witness is not a nonexistence proof.
4. **`OpenSignObstruction`** ($\Phi_1 > 0, \Gamma_2 > 0$): Higher-cell curvature defect indicating a structural boundary obstruction.
5. **`Refused`**: The packet violates typing boundaries or declarations.

---

## Section 6: Part IV — Computational Complexity Classes and Representation Models

### 6.1 Formal Definitions: Decision Languages, Certificates, and Reductions

Computational complexity is defined in terms of input bit length $|x|$ on a universal Turing machine, not cochain dimension:

1. **Class $\mathbf{P}$ (Polynomial Time)**:
   A language $L \subseteq \{0, 1\}^*$ belongs to $\mathbf{P}$ if there exists a deterministic Turing machine $M$ and a constant $k \ge 1$ such that for every input $x \in \{0, 1\}^*$, $M(x)$ halts in at most $O(|x|^k)$ steps and outputs $1$ if and only if $x \in L$.
2. **Class $\mathbf{NP}$ (Nondeterministic Polynomial Time)**:
   A language $L \subseteq \{0, 1\}^*$ belongs to $\mathbf{NP}$ if there exists a deterministic polynomial-time verifier $V(x, w)$ and a polynomial $p$ such that:
   $$x \in L \iff \exists w \in \{0, 1\}^* \text{ with } |w| \le p(|x|) \text{ such that } V(x, w) = 1$$
   The string $w$ is a certificate (witness).
3. **$\mathbf{NP}$-Hardness and $\mathbf{NP}$-Completeness**:
   A language $L'$ is $\mathbf{NP}$-hard if for every language $L \in \mathbf{NP}$, there exists a polynomial-time computable function $f: \{0, 1\}^* \to \{0, 1\}^*$ such that $x \in L \iff f(x) \in L'$ (polynomial-time Many-One reduction $L \le_P L'$). If $L'$ is additionally in $\mathbf{NP}$, it is $\mathbf{NP}$-complete.
4. **Distinction of Algorithmic Tasks**:
   - **Decision**: Does a configuration with energy $E \le E_0$ exist?
   - **Search**: Find a configuration achieving energy $E \le E_0$.
   - **Counting**: Compute the exact number of states with energy $E$.
   - **Sampling**: Draw configurations according to the Boltzmann probability measure $e^{-\beta E(s)} / Z$.
   - **Estimation**: Estimate the expectation value $\langle A \rangle$ to within additive error $\epsilon$ with confidence $1 - \delta$.

### 6.2 Withdrawal of the Cochain-Arity NP-Hardness Theorem

> **Withdrawal Notice (Claim Discipline):**
> An earlier version of this monograph claimed: *"For problems in class $\mathbf{P}$, the minimal cochain arity satisfies $k^*(N) = O(\log N)$; for $\mathbf{NP}$-hard problems, $k^*(N) = \Omega(N^c)$ for $c > 0$, establishing the combinatorial origin of $\mathbf{NP}$-hardness."*
> **WITHDRAWN:** A growth rate of $N^c$ is polynomial in $N$; a lower bound of that form does not establish superpolynomial growth. Furthermore, no formal complexity reduction or representation model was provided connecting cochain arity directly to Turing machine time complexity. Minimal cochain arity is retained strictly as an open research question concerning restricted representation models, not an established complexity theorem.

---

## Section 7: Part V — The Troyer-Wiese Theorem and Algorithmic Hardness

### 7.1 The Actual Troyer-Wiese Formulation: The Energy-Threshold Decision Problem

In 2005, Troyer and Wiese demonstrated that the generic fermion sign problem is $\mathbf{NP}$-hard (cond-mat/0408370, PRL 94, 170201).

> **Epistemic Correction on the Decision Problem:**
> A previous phrasing in this work characterized Troyer-Wiese as deciding whether the partition sum $Z$ is strictly positive or zero. For any non-empty, finite-dimensional Hermitian quantum Hamiltonian and finite real temperature $\beta > 0$, the thermal trace:
> $$Z = \operatorname{Tr}(e^{-\beta H}) = \sum_k e^{-\beta E_k} > 0$$
> is strictly positive! The decision question is not whether $Z > 0$ versus $Z = 0$.

Instead, Troyer and Wiese reduce the canonical $\mathbf{NP}$-complete problem of finding the ground-state energy of a 3-dimensional Ising spin glass:
$$H_{\text{glass}} = - \sum_{\langle i, j \rangle} J_{ij} s_i s_j, \quad s_i \in \{-1, +1\}, \quad J_{ij} \in \{-1, 0, +1\}$$
to the problem of estimating quantum thermal expectation values.
The decision problem asks: *"Is the ground state energy $E_0 \le E_{\text{threshold}}$?"*
The cited construction uses $\beta J\ge N\ln2+\ln(12N)$ and separates thermal-energy cases below $E_{\mathrm{threshold}}+J/2$ and above $E_{\mathrm{threshold}}+J$. The earlier attributed formula $\beta=2N\ln2$, $\epsilon=1/(4N)$ is withdrawn as an inaccurate quotation of that construction. Its explicit quantum model is a frustrated **spin** Hamiltonian $-\sum J_{ij}\sigma_i^x\sigma_j^x$, not a proved reduction specifically to the Hubbard model. [Troyer–Wiese, equations (10)–(11) and footnote 9](https://arxiv.org/html/cond-mat/0408370).

### 7.2 Directionality of the Reduction and The P/BPP Distinction

1. **Direction of Reduction**:
   The reduction runs strictly from the known $\mathbf{NP}$-complete problem to the quantum statistical evaluation:
   $$\text{3D Ising Spin Glass Instance } (J, E_{\text{threshold}}) \xrightarrow{\text{poly-time}} \text{Fermion Simulation Instance } (\mathcal{H}, \beta, \epsilon)$$
   Thus, evaluating the quantum thermal expectation value is $\mathbf{NP}$-hard.
2. **Deterministic vs. Randomized Solvers**:
   - If an algorithm could deterministically evaluate $\langle E \rangle$ in time polynomial in $V$ and $1/\epsilon$, it would imply $\mathbf{P} = \mathbf{NP}$.
   - If a polynomial-time Monte Carlo sampler could evaluate $\langle E \rangle$ with bounded error probability, it would imply $\mathbf{NP} \subseteq \mathbf{BPP}$ (Troyer & Wiese 2005, Footnote 9).
3. **Worst-Case Scope**:
   The Troyer-Wiese result is a **worst-case** hardness theorem for generic Hamiltonians admitting frustrated interactions. It does not imply that every fermionic Hamiltonian is intractable. Quadratic fermion systems admit polynomial single-particle methods. Protected Hubbard determinant representations have nonnegative weights, but that fact alone supplies no polynomial mixing-time guarantee.

---

## Section 8: Part VI — The Ascent Ladder: From the Void to Troyer-Wiese (The SQL Pricing Walk)

Part VI constructs the complete ladder of presentation obstructions, starting from the primitive distinction at the void and ascending through arithmetic, Turing computability, and the fermion sign problem.

### 8.1 The Six Structural Rungs

1. **Rung 0 (The Void)**: One-point carrier, no distinction possible.
2. **Rung 1 (Primitive Difference)**: Two-point carrier, irreflexive distinction $\delta(a, b) \neq 0$.
3. **Rung 2 (Natural Arithmetic)**: Successor relations and Peano counting.
4. **Rung 3 (Turing Computability)**: Unbounded tapes and non-faithful halting projections (Part I).
5. **Rung 4 (Sign Packets & Cancellation)**: Finite cochain complexes and involution witnesses (Parts II & III).
6. **Rung 5 (Computational Intractability)**: Externally cited worst-case hardness under a specified representation and precision model; no cochain-arity theorem is inferred.

### 8.2 The 17-Row Pricing Audit

The original three-row SQLite fixture (`code/sign_sql/seed.sql`) checks the following **supplied bookkeeping data**, not a Hamiltonian-derived meron transformation. Its physical interpretation is withdrawn; the model-derived replacement is in Section 15:

- Exactly 17 admissions from the void to Rung 7: 10 licensed rungs vs 7 priced imports.
- Presentation A (frustrated): Cancellation severity ratio is exactly $1/15$.
- Presentation B (meron repaired): All weights are non-negative ($EXISTS = 1$), restoring the cancellation ratio to $1/1$.
- Both presentations agree on the net total ($1/2$): the re-presentation changes the writing, not the thing written.
- The Wheeler-DeWitt boundary is verified as a declared boundary, not an ungrounded derivation.

---

## Section 9: The Hamiltonian GIN Index — Finite Pairing Experiments

This implementation enumerates finite Euler-transfer paths, indexes their mode support, and matches equal rational magnitudes. Its finite partition cancellation is distinct from an efficient thermal solver.

### 9.1 Many-Body Quantum Hamiltonians and Trotter Paths

Let $H$ be a discrete fermionic Hamiltonian on a lattice $\Lambda$ with creation/annihilation operators $c_i^\dagger, c_i$:
$$H = -t \sum_{\langle i, j \rangle, \sigma} (c_{i\sigma}^\dagger c_{j\sigma} + c_{j\sigma}^\dagger c_{i\sigma}) + U \sum_{i} n_{i\uparrow} n_{i\downarrow}$$

Using the Trotter-Suzuki decomposition of the imaginary-time evolution operator $e^{-\beta H}$:
$$e^{-\beta H} = \lim_{M \to \infty} \left( e^{-\frac{\beta}{M} H_0} e^{-\frac{\beta}{M} H_I} \right)^M$$
we generate the ensemble of closed imaginary-time paths $\mathcal{P} = \{p_1, \dots, p_K\}$ where each path $p = (|n_0\rangle \to |n_1\rangle \to \dots \to |n_M = n_0\rangle)$ carries a weight $W(p) \ge 0$ and a permutation parity sign $\sigma(p) \in \{+1, -1\}$ governed by the Jordan-Wigner transformation.

### 9.2 The Generalized Inverted Index (GIN) Architecture

In high-dimensional many-body configuration spaces, finding an involution partner $\Xi(p)$ for a negative path $p$ with identical spectator occupations requires exhaustive combinatorial search.

We construct a **Generalized Inverted Index (GIN)** over the fermionic orbital modes:
$$\mathcal{M}: m \mapsto \{p \in \mathcal{P} \mid m \in \mathrm{OccupiedModes}(p)\}$$

The posting list maps each mode $m \in \{1, \dots, 2N_{\mathrm{sites}}\}$ to the set of configurations containing it. Finding the involution partner of a state under a hopping transposition $(u \leftrightarrow v)$ while preserving all spectator modes $S = \mathrm{OccupiedModes}(p) \setminus \{u\}$ reduces to an inverted set intersection:
$$\mathrm{Partner}(p) = \left( \bigcap_{m \in S} \mathcal{M}(m) \right) \cap \mathcal{M}(v) \cap \left( \mathcal{P} \setminus \mathcal{M}(u) \right)$$
This expression uses $k$ posting-list operations, not $O(k)$ total time. Intersections depend on posting lengths and outputs; materializing $P$ paths already costs at least $\Omega(P)$. Moreover the current bridge matches equal-weight fibers, not the displayed spectator-preserving query: a union of occupied modes along a path does not preserve its time-resolved spectator trajectory.

### 9.3 The Duality of Bipartite Resolution vs. Frustrated Complexity

The following two fixed finite inputs have different equal-weight matching outcomes. This is not a dichotomy theorem for bipartite and frustrated models.

#### Case 1: Noninteracting spin-polarized sector (4-site periodic ring)

- We simulate a 4-site periodic ring with 2 identical spin-up fermions ($t=1.0, U=0.0, \beta=1.5, M=4$).
- The Hamiltonian generates 230 closed imaginary-time Trotter paths, containing **32 negative paths** ($w = 0.019775$).
- The GIN mode posting lists immediately reveal that **96 positive paths share this exact same weight** $0.019775$.
- The bridge pairs all 32 negative paths with exact equal-weight positive partners ($w_+ = w_-$) in the same exact-weight fiber. No spectator-preserving symmetry is certified.
- Inside the GIN partition quotient, every negative path cancels identically:
  $$w \cdot (+1) + w \cdot (-1) \equiv 0 \quad (\text{Lean 4: } \texttt{involution\_pair\_cancels\_sign})$$
- **Audit Verdict**: Uncancelled sign mass $\Phi_1 = 0.0$, quotiented average sign $\langle\text{Sign}\rangle_{\text{GIN}} = 1.0$, routing to **`TerminalRoute.Repair`**. The sign problem is dissolved at the Hamiltonian level.

#### Case 2: Representation-Dependent Negativity (3-Site Free Triangle)

- We simulate a 3-site triangle cluster with 2 identical spin-up fermions ($t=1.0, U=0.0, \beta=2.0, M=3$).
- In the declared **real-space occupation basis Trotter expansion**, the Hamiltonian generates 27 paths with **6 negative paths** ($w = 0.296296$) corresponding to odd-cycle permutation windings around the triangle loop.
- The positive paths in this basis have weights strictly in $\{0.444444, 1.0\}$.
- The GIN index reveals that for this specific representation, **the negative and positive weight spectra are disjoint**:
  $$\operatorname{supp}(w_-) \cap \operatorname{supp}(w_+) = \emptyset$$
- Consequently, no weight-preserving involution can exist *in this declared real-space representation*. The bridge isolates the 6 unpartnered negative paths, leaving uncancelled defect mass $\Phi_1 > 0.0$ and routing to **`TerminalRoute.SplitBrainRefusal`**.
- **Crucial Epistemic Finding — Not a Hardness Witness**: Because $U=0$, the system is quadratic (free fermions). Diagonalizing the $3 \times 3$ one-body hopping matrix yields single-particle orbital energies $\varepsilon \in \{-2, 1, 1\}$. In the single-particle eigenmode basis, the 2-fermion many-body eigenvalues are $E_n \in \{-1, -1, 2\}$, and the exact thermal partition function is:
  $$Z(\beta=2) = 2e^2 + e^{-4} \approx 14.796428$$
  which is evaluated in $O(N^3)$ operations with zero sign problem. The negative Trotter path weights are an artifact of the real-space occupation representation, demonstrating that path negativity by itself does not imply computational hardness.

### 9.4 Kitaev 1D Majorana Chain

We evaluate a sweet-spot Kitaev chain with $L=4$ sites (8 Majorana modes $\gamma_1, \dots, \gamma_8$).

- Sweet-spot bulk Hamiltonian bonds $h_j = (2j, 2j+1)$ pair modes $\{2, 3, 4, 5, 6, 7\}$ into bulk Dirac fermions with zero sign residual.
- Boundary edge modes $\gamma_1$ and $\gamma_8$ are audited via `ViewMajoranaZeroModeAudit` as strictly decoupled from the bulk, confirming **`MZM_TOPOLOGICALLY_PROTECTED`**.

> **Scope correction, 2026-09-22 (Sections 9.5–9.19).** The following historical physics-labelled modules are illustrative finite fixtures. Their supplied traces, gaps, curvatures and cancellation parameters do not establish the named physical theories, a model-to-cochain equivalence, phase transitions, or sign-solvability theorems for those theories. Such general interpretations are withdrawn. Doubling a trace into its modulus square changes the target unless an observable-preserving representation identity is proved. These fixtures are retained for inspection and are not premises of the meron/Hubbard results below.

### 9.5 Non-Abelian Gauge Theory: $SU(2)$ Lattice Plaquette and Topological Flux Sectors

To address whether non-abelian gauge degrees of freedom modify the GIN spectral structure, we implement an exact Kogut-Susskind $SU(2)$ lattice gauge model coupled to color-doublet fermions (`code/su2_lattice_gauge.py`):

- **Gauge Links & Representations**: 4 directed links around a square plaquette with truncated representation spaces $j \in \{0, 1/2\}$.
- **Hamiltonian Structure**:
  $$H = \frac{g^2}{2} \sum_{l=1}^4 \mathbf{J}_l^2 - \frac{1}{g^2} \operatorname{Tr}(U_\square) - t \sum_{\langle x, y \rangle} (c_x^\dagger U_{xy} c_y + \text{h.c.})$$
  satisfying exact non-abelian Gauss law invariance $[H, \mathbf{G}_v] = 0$ at all vertices $v \in \{1, 2, 3, 4\}$.
- **Topological Center Flux Sectors**:
  Topological sectors are classified by the trace of the Wilson loop $\frac{1}{2}\operatorname{Tr}(U_\square) \in \{+1, -1\}$ (center vortex / instanton winding $Q \in \{0, 1\}$). At topological angle $\theta = \pi$, paths acquire an alternating sign factor $\sigma(p) = (-1)^{Q(p)}$.
- **Action Gap & Spectral Disjointness**:
  The non-trivial center vortex ($Q=1$) incurs a finite magnetic action gap:
  $$\Delta S = E_B(Q=1) - E_B(Q=0) = \frac{4}{g^2} > 0$$
  Because $\Delta S > 0$, the path weights in the negative sector ($Q=1$) are exponentially suppressed relative to the positive vacuum sector ($Q=0$):
  $$\operatorname{supp}(W_+) \cap \operatorname{supp}(W_-) = \emptyset$$
  The GIN mode posting lists reveal **strictly disjoint weight spectra** within this declared representation. No equal-weight partner can exist within this class of local sector pairings. Unpartnered negative paths persist, yielding uncancelled defect mass $\Phi_1 > 0$ and routing deterministically to **`TerminalRoute.SplitBrainRefusal`**.
- **Sign-Free Control**:
  At $\theta = 0$ or under an exact color-reflection symmetry that equates sector energies ($\Delta S = 0$), the negative paths vanish or overlap identically, routing to **`TerminalRoute.Repair`**.

### 9.6 Non-Abelian Triality: $SU(3)$ Baryonic Y-Junctions and Higher-Order Cochain Curvature ($\Gamma_2 > 0$)

To establish whether 3-body color constraints induce higher-order cochain curvature, we construct an exact simplicial model of the 3-quark Y-shaped flux junction (`code/su3_baryon_triality.py`):

- **Simplicial Complex & Nilpotence**:
  The geometry is modeled as a 2-simplex simplicial complex:
  - **$C^0$ (4 vertices)**: Central Fermat-Steiner flux junction $J$ (index 0) and 3 quark loci $x_1, x_2, x_3$ (indices 1, 2, 3).
  - **$C^1$ (6 links)**: 3 junction spokes $e_0 = (J \to x_1), e_1 = (J \to x_2), e_2 = (J \to x_3)$ and 3 perimeter links $e_3 = (x_1 \to x_2), e_4 = (x_2 \to x_3), e_5 = (x_3 \to x_1)$.
  - **$C^2$ (3 triangular plaquettes)**: $\Delta_1 = (J, x_1, x_2), \Delta_2 = (J, x_2, x_3), \Delta_3 = (J, x_3, x_1)$.
  The discrete boundary operators $d_0: C^0 \to C^1$ and $d_1: C^1 \to C^2$ satisfy exact nilpotence $d_1 \circ d_0 = 0$.
- **$SU(3)$ Color Weight Geometry**:
  Quark color states belong to the fundamental triplet $\mathbf{3}$ of $SU(3)$ with Cartan weights in $\mathbb{R}^2$:
  $$\mu_R = \left(\frac{1}{2}, \frac{1}{2\sqrt{3}}\right), \quad \mu_G = \left(-\frac{1}{2}, \frac{1}{2\sqrt{3}}\right), \quad \mu_B = \left(0, -\frac{1}{\sqrt{3}}\right)$$
  satisfying the color singlet closure $\sum_{c \in \{R, G, B\}} \mu_c = (0, 0)$. Root vectors $\alpha_{ij} = \mu_i - \mu_j$ have unit Euclidean length $\|\alpha_{RG}\| = \|\alpha_{GB}\| = \|\alpha_{BR}\| = 1.0$. The center symmetry is the triality group $Z(SU(3)) = \mathbb{Z}_3$.
- **Meson (Arity $k=2$) vs. Baryon (Arity $k=3$) Curvature Comparison**:
  1. **Meson ($q\bar{q}$ pair, arity 2)**: Flux flows along closed 1-chains between quark and antiquark, yielding zero cochain boundary:
     $$d_1 c_{\text{meson}}^1 = 0 \implies \Gamma_2 = \|d_1 c_{\text{meson}}^1\|_{C^2} = 0.0$$
     The meson cochain is closed, routing deterministically to **`TerminalRoute.ExactRepair`**.
  2. **Baryon ($qqq$ triplet, arity 3)**: The 3 quarks are bound through the invariant Levi-Civita tensor $\epsilon_{abc}$ at the Y-junction $J$. Because each spoke carries distinct fundamental color flux with net cancellation only at $J$, the circulation around each individual face $\Delta_k$ evaluates to a non-zero root vector $\alpha_{ij} \neq 0$:
     $$\Gamma_2 = \|d_1 c_{\text{baryon}}^1\|_{C^2} = 5.0 > 0.0$$
     Coupled with non-vanishing sign residual $\Phi_1 = 5/2 > 0.0$, the BQNF evaluator confirms that **non-abelian triality intrinsically induces higher-order cochain curvature ($\Gamma_2 > 0$)**.
  3. **Deterministic Routing**: Because $\Gamma_2 > 0$ and $\Phi_1 > 0$, the sign defect is an open cochain obstruction, routing deterministically to:
     $$\textbf{TerminalRoute.OpenSignObstruction}$$
- **GIN Mode Posting Lists**:
  The 9 color-spatial modes ($3 \text{ vertices} \times 3 \text{ colors}$) are indexed into `GinModePostingList`. The baryonic state occupies modes $\{1, 5, 9\}$, verifying that 3-cochain arity constraints produce an topologically uncontractible flux defect.

### 9.7 Finite-Temperature $SU(3)$ Polyakov Loop Holonomies and $\mathbb{Z}_3$ Center Symmetry Breaking

To evaluate whether thermodynamic deconfinement restores spectral overlap between center-rotated flux sectors, we construct an exact model of finite-temperature $SU(3)$ lattice gauge theory coupled to fundamental fermions (`code/su3_polyakov_loop.py`):

- **Polyakov Loop Holonomies & $\mathbb{Z}_3$ Center Transformations**:
  The Polyakov loop (temporal Wilson line) at spatial locus $\mathbf{x}$ is defined by:
  $$P(\mathbf{x}) = \frac{1}{3} \operatorname{Tr} \left( \prod_{\tau=0}^{N_\tau - 1} U_0(\tau, \mathbf{x}) \right)$$
  Under global center transformations $U_0 \to z^k U_0$ with $z = e^{i 2\pi/3}$ ($k \in \{0, 1, 2\}$), the loop transforms as $P \to z^k P = e^{i \frac{2\pi k}{3}} P$.
  - **Confined Phase ($\beta < \beta_c \approx 5.69$)**: The center symmetry $\mathbb{Z}_3$ is unbroken; the thermal expectation value vanishes: $\langle |P| \rangle = 0$.
  - **Deconfined Phase ($\beta > \beta_c$)**: Center symmetry $\mathbb{Z}_3$ is spontaneously broken; the Polyakov loop condenses: $\langle |P| \rangle = P_0 > 0$.
- **Coupled Matter & Center Action Gap**:
  Fundamental fermions satisfy antiperiodic temporal boundary conditions $\psi(\tau + N_\tau) = - \psi(\tau)$. Coupling to the temporal holonomy yields the effective action shift:
  $$S_F(k) = - 12 h |P| \cos\left( \frac{2\pi k}{3} \right)$$
  - Sector $k=0$ (real vacuum sector, positive parity $\sigma = +1$): $\cos(0) = +1 \implies S_F(0) = - 12 h |P|$.
  - Sectors $k=1, 2$ (center-rotated sectors, negative parity $\sigma = -1$): $\cos(2\pi/3) = -0.5 \implies S_F(1, 2) = + 6 h |P|$.
  The resulting action gap between center sectors is:
  $$\Delta S = S_F(k) - S_F(0) = 18 h |P|$$
- **Spectral Overlap Analysis Across the Deconfining Phase Transition**:
  1. **Confined Phase ($\beta = 4.0 < \beta_c$)**: Because $\langle |P| \rangle = 0$, the action gap vanishes ($\Delta S = 0.0$). The positive and negative weight spectra share identical numerical magnitudes ($W_+ = W_- = 0.11080316$). However, because of $\mathbb{Z}_3$ triality multiplicity (1 real positive sector vs 2 complex negative sectors), negative paths outnumber positive paths by $2:1$ (16 negative vs 8 positive paths). The GIN index pairs 8 paths, leaving 8 unpartnered negative paths, resulting in uncancelled defect mass $\Phi_1 > 0$ and routing to **`TerminalRoute.SplitBrainRefusal`**.
  2. **Deconfined Phase ($\beta = 8.0 > \beta_c$)**: Polyakov loop condensation $\langle |P| \rangle = 0.7029 > 0$ induces a macroscopic action gap $\Delta S = 1.26529 > 0$. The path weights in sectors $k=1, 2$ are exponentially suppressed ($W_- = 0.00983544$) relative to the vacuum sector ($W_+ = 0.03485799$).
  3. **Core Finding**: The positive and negative weight supports become **strictly disjoint**:
     $$\operatorname{supp}(W_+) \cap \operatorname{supp}(W_-) = \emptyset$$
     The deconfining phase transition **does NOT restore spectral overlap**; rather, it **destroys** the degenerate weight overlap of the confined phase and **amplifies** spectral separation, maintaining deterministic routing to:
     $$\textbf{TerminalRoute.SplitBrainRefusal}$$
- **GIN Mode Posting Lists**:
  All 6 color-spatial modes ($2 \text{ sites} \times 3 \text{ colors}$) are indexed into `GinModePostingList`, verifying that color-spatial mode resolution across center-rotated flux sectors witnesses the persistence of the sign obstruction in the deconfined plasma.

### 9.8 Multi-Flavor $SU(N_c)$ Color Flux Tubes: Adjoint Representation, Zero $N$-ality, and String Breaking

To establish whether representation-theoretic $N$-ality controls cochain curvature and involution pairing, we evaluate multi-flavor $SU(N_c)$ color flux tubes with adjoint versus fundamental matter (`code/su_nc_adjoint_flux.py`):

- **Representation $N$-ality & Center Transformations**:
  In $SU(N_c)$ gauge theories with center $Z(SU(N_c)) = \mathbb{Z}_{N_c}$, representations transform as $R \to z^k R$, where $k \in \{0, 1, \dots, N_c - 1\}$ is the $N$-ality:
  - **Fundamental Representation $\mathbf{N_c}$ ($N$-ality $k = 1 \pmod{N_c}$)**: Carries non-zero center charge. Flux tubes ending on fundamental charges cannot be screened by dynamic gluons. In 3-quark baryonic Y-junctions, the Levi-Civita tensor enforces non-contractible 3-spoke circulation, yielding strictly positive cochain curvature ($\Gamma_2 = 2.0 \text{ to } 5.0 > 0$) and routing to `OpenSignObstruction`.
  - **Adjoint Representation $\mathbf{N_c^2 - 1}$ ($N$-ality $k = 0 \pmod{N_c}$)**: Transforms trivially under the center ($X \to z X z^{-1} = X$). Because adjoint fields share the color quantum numbers of gluons, dynamic adjoint pairs screen the flux completely.
- **Dynamical String Breaking & Simplicial Cochain Closure**:
  For flux tubes exceeding the breaking threshold $R \ge R_{\text{break}} \approx 2 m_\lambda / \sigma$, dynamic adjoint fermion pairs $\lambda \bar{\lambda}$ pop from the vacuum ($\mathbf{Adj} \otimes \mathbf{Adj} \supset \mathbf{1}$). The open flux tube breaks into two localized color-singlet states ("gluinoballs" / adjoint mesons), pinching off the open bridge link. On the simplicial complex ($C^0 \xrightarrow{d_0} C^1 \xrightarrow{d_1} C^2$ with $d_1 \circ d_0 = 0$):
  $$d_1 c_{\text{adj}}^1 = 0 \implies \Gamma_2 = \|d_1 c_{\text{adj}}^1\|_{C^2} = 0.0$$
  Zero $N$-ality and adjoint string breaking **identically eliminate 2-cochain curvature** ($\Gamma_2 = 0.0$).
- **GIN Involution Pairing & Sign Restoration**:
  For $N_f$ flavors of adjoint Majorana fermions $\lambda_f^a$ ($a \in 1..N_c^2 - 1, f \in 1..N_f$), the Hamiltonian admits an exact charge-conjugation / flavor-reflection involution $\Xi$ with $[H, \Xi] = 0$:
  - Because $N$-ality is zero, every negative Trotter path $p_-$ generated by fermion permutations matches an equal-weight partner $p_+ = \Xi p_-$ ($w_+ = w_-$) with identical spectator mode occupations.
  - The GIN mode posting lists achieve **100% involution pairing** (`involution_pairing_rate = 1.0`).
  - In the GIN quotient, $w \cdot (+1) + w \cdot (-1) \equiv 0$, yielding uncancelled defect mass $\Phi_1 = 0.0$ and quotiented average sign $\langle\text{Sign}\rangle_{\text{GIN}} = 1.0$.
  - **Deterministic Routing**: Because $\Gamma_2 = 0.0$ and $\Phi_1 = 0.0$, the sign problem is completely dissolved at the Hamiltonian level, routing deterministically to:
    $$\textbf{TerminalRoute.ExactRepair}$$

### 9.9 4D Simplicial Quantum Gravity: Regge-Wheeler-DeWitt Constraints and Pachner Moves ($2 \to 4$ and $3 \to 3$)

To determine whether the cochain and GIN involution architecture extends to discrete quantum gravity and diffeomorphism invariance, we analyze 4D simplicial quantum gravity formulated on Regge triangulations under direct-sum Wheeler-DeWitt (WDW) gauge cochains (`code/regge_pachner_wdw.py`).

- **Combinatorial 4-Manifolds and Bistellar Pachner Moves**:
  The discrete 4-manifold $K$ is initialized as the boundary of a 5-simplex ($\partial \Delta^5$, the combinatorial 4-sphere $S^4$), with $N_0 = 6$ vertices, $N_1 = 15$ edges, $N_2 = 20$ triangles, $N_3 = 15$ tetrahedra, and $N_4 = 6$ four-simplices, satisfying Euler-Poincaré characteristic:
  $$\chi = N_0 - N_1 + N_2 - N_3 + N_4 = 6 - 15 + 20 - 15 + 6 = 2$$
  Topological surgeries proceed via Pachner bistellar moves in 4 dimensions:
  1. **$1 \to 5$ Move (Subdivision)**: Inserts an interior vertex into a 4-simplex, subdividing it into 5 simplices ($\Delta N_0 = +1, \Delta N_4 = +4, \Delta \chi = 0$).
  2. **$2 \to 4$ Move (Growth Surgery)**: Selects two 4-simplices $\{s_1, s_2\}$ sharing an interior tetrahedron $t = s_1 \cap s_2$, removes them, and replaces them with 4 simplices formed by inserting the transverse edge $(u, v)$ connecting the opposite vertices $u = s_1 \setminus t$ and $v = s_2 \setminus t$ ($\Delta N_4 = +2, \Delta \chi = 0$).
  3. **$3 \to 3$ Move (Topological Flip)**: Selects three 4-simplices sharing an interior triangle $\tau$, removes them, and replaces them with 3 simplices sharing the dual triangle connecting the 3 opposite vertices ($\Delta N_4 = 0, \Delta \chi = 0$).
  Throughout the entire surgery sequence ($6 \xrightarrow{1 \to 5} 10 \xrightarrow{2 \to 4} 12 \xrightarrow{3 \to 3} 12$), the Euler characteristic is preserved identically ($\chi \equiv 2$).

- **Direct-Sum Wheeler-DeWitt Gauge Cochain Block System**:
  The discrete Wheeler-DeWitt constraints couple the link-momentum cochain $p_{\text{edge}} \in C^1(K)$ (supermomentum constraint $H_i$) and vertex scalar curvature cochain $H_\perp \in C^0(K)$ (Hamiltonian scalar constraint $H_\perp = \sqrt{g} (R - 2\Lambda)$) into a joint direct-sum cochain space:
  $$\Omega = \begin{bmatrix} p_{\text{edge}} \\ H_\perp \end{bmatrix} \in C^1(K) \oplus C^0(K)$$
  The gauge coboundary operator acts from scalar vertex potentials $C^0(K)$:
  $$D_{\text{joint}} = \begin{bmatrix} d_0 \\ 0 \end{bmatrix} : C^0(K) \to C^1(K) \oplus C^0(K)$$
  where $d_0 : C^0(K) \to C^1(K)$ is the simplicial incidence coboundary, and $D_{\text{joint}}^T = [d_0^T, 0]$ enforces the discrete divergence-free momentum constraint $d_0^T W_1 = 0$.

- **Primal-Dual $L^1$ Duality Certification**:
  The Wheeler-DeWitt constraint defect mass $\Phi_{\text{WDW}}$ is formulated as an exact primal-dual $L^1$ linear program:
  $$\Phi_{\text{WDW}} = \min_\alpha \|\Omega - D_{\text{joint}} \alpha\|_1$$
  $$\text{Dual Objective: } \max_W \langle W, \Omega \rangle \quad \text{s.t.} \quad D_{\text{joint}}^T W = 0, \quad \|W\|_\infty \le 1$$
  The duality gap is certified to zero ($|\Phi_{\text{primal}} - \Phi_{\text{dual}}| \le 10^{-7}$) across all triangulations.

- **Constraint Closure vs. Pachner Defect Mass Findings**:
  1. **Flat Triangulations ($\epsilon_t = 0$)**:
     In flat Euclidean triangulations where all triangle deficit angles vanish ($\epsilon_t = 2\pi - \sum \theta_t = 0$) and momentum is a pure gauge coboundary ($p_{\text{edge}} = d_0 \alpha_{\text{exact}}, H_\perp = 0$):
     $$\Phi_{\text{WDW}} = 0.0, \quad \text{Duality Gap } \le 10^{-7}$$
     Exact diffeomorphism constraint closure holds:
     $$H_{\text{WDW}} |\Psi\rangle = 0 \implies \textbf{TerminalRoute.ExactRepair}$$
  2. **Curved Triangulations under Pachner Surgery ($2 \to 4$ and $3 \to 3$)**:
     When $2 \to 4$ growth surgery and $3 \to 3$ topological flips are performed on curved geometries with non-zero deficit angles ($\epsilon_t \neq 0$), the insertion of transverse edges and relocation of curvature allocate non-vanishing scalar curvatures $R(v) = H_\perp(v) > 0$ to vertices.
     Because the scalar constraint block $H_\perp$ lies in $C^0(K)$ while $\mathrm{im}(D_{\text{joint}}) = \mathrm{im}(d_0) \oplus \{0\}$, the vertex curvature cannot be absorbed by any gauge transformation $\alpha \in C^0(K)$:
     $$\Phi_{\text{WDW}} = \min_\alpha \left( \|p_{\text{edge}} - d_0 \alpha\|_1 + \|H_\perp\|_1 \right) \ge \|H_\perp\|_1 > 0.0$$
     The dual certificate $W = [0, \operatorname{sign}(H_\perp)]^T$ satisfies $D_{\text{joint}}^T W = d_0^T (0) = 0$ and $\|W\|_\infty \le 1$, certifying the exact lower bound $\langle W, \Omega \rangle = \|H_\perp\|_1 > 0.0$.
  3. **Epistemic Conclusion**:
     Pachner moves ($2 \to 4$ and $3 \to 3$) on curved 4D simplicial manifolds **induce non-vanishing constraint defect mass** ($\Phi_{\text{WDW}} > 0.0$), breaking exact diffeomorphism constraint closure ($H_{\text{WDW}} |\Psi\rangle \neq 0$). Under BQNF cochain evaluation, this defect enforces deterministic routing to:
     $$\textbf{TerminalRoute.SplitBrainRefusal}$$

### 9.10 3D Weyl Semimetals and Chiral Superconductors: Chiral Chemical Potential $\mu_5 > 0$, Callan-Harvey Anomaly Inflow, and Cochain Holonomy

To determine whether non-zero spectral flow preserves exact fermion sign cancellation or induces non-contractible cochain holonomy, we analyze 3D Weyl semimetal and superconductor slab lattices under chiral chemical potential $\mu_5 > 0$ and adiabatic Callan-Harvey anomaly inflow (`code/chiral_anomaly_inflow.py`).

- **3D Weyl Slab Geometry & Chiral Zero Modes**:
  A 3D slab of dimensions $L_x \times L_y \times L_z$ with open boundaries along $z$ ($z=0$ [bottom], $z=L_z-1$ [top]) and periodic in $x, y$ hosts two bulk Weyl nodes with opposite chiralities $\chi = \pm 1$ at $\mathbf{k}_0 = (0, 0, \pm k_0)$, satisfying the Nielsen-Ninomiya no-go theorem:
  $$\sum_{i} \chi_i = (+1) + (-1) = 0$$
  In momentum slices $k_z \in (-k_0, k_0)$, 2D Chern numbers evaluate to $C(k_z) = 1$, terminating on the slab boundaries as top and bottom surface Majorana Fermi arcs connecting the node projections.

- **Callan-Harvey Anomaly Inflow & Adiabatic Spectral Flow**:
  Under adiabatic threading of chiral gauge flux $\theta(t) \in [0, 2\pi]$, chiral anomaly inflow transports charge between bulk and boundary:
  $$Q_{\text{bulk}}(\theta) = \frac{\theta}{2\pi}, \quad Q_{\text{surf}}(\theta) = -\frac{\theta}{2\pi} \implies Q_{\text{net}}(\theta) = Q_{\text{bulk}} + Q_{\text{surf}} \equiv 0$$
  Callan-Harvey conservation holds identically: the bulk anomaly is cancelled by the boundary inflow of the surface Majorana Fermi arcs.

- **Chiral Chemical Potential $\mu_5$ and Exponential Weight Asymmetry**:
  The chiral chemical potential couples to the axial charge operator $\hat{N}_5 = N_R - N_L$:
  $$H(\mu_5) = H_0 - \mu_5 (P_+ - P_-)$$
  shifting the Fermi levels of right- and left-handed Weyl nodes to $E_R = E_0 - \mu_5$ and $E_L = E_0 + \mu_5$.
  Under imaginary-time Trotter discretization at inverse temperature $\beta$:
  $$w_+ = e^{-\beta(E_0 - \mu_5)}, \quad w_- = e^{-\beta(E_0 + \mu_5)} \implies \frac{w_+}{w_-} = e^{2\beta \mu_5}$$

- **1-Cochain Holonomy & Fermion Sign Defect Evaluation**:
  Around the adiabatic flux cycle $\theta \in [0, 2\pi]$, the 1-cochain holonomy evaluates to:
  $$\operatorname{Hol}(c^1) = \exp\left(i \cdot 2\pi \frac{\mu_5}{\omega_0}\right) = \cos\left(2\pi \frac{\mu_5}{\omega_0}\right) + i \sin\left(2\pi \frac{\mu_5}{\omega_0}\right)$$
  1. **Chiral-Symmetric Limit ($\mu_5 = 0.0$)**:
     - The chiral involution $\Xi$ strictly commutes with the Hamiltonian ($[H, \Xi] = 0$).
     - Equal weights: $w_+ = w_- \implies \Delta w = 0.0$.
     - Cochain holonomy is contractible: $\operatorname{Hol}(c^1) = 1.0 + 0.0i$, with vanishing cochain curvature: $\Gamma_2 = 0.0$.
     - Exact cancellation in the GIN quotient yields uncancelled defect mass $\Phi_1 = 0.0$, routing deterministically to:
       $$\textbf{TerminalRoute.ExactRepair}$$
  2. **Broken Chiral Symmetry ($\mu_5 > 0.0$)**:
     - Exponential weight asymmetry: $w_+ \neq w_-$, creating an uncancelled weight discrepancy:
       $$\Phi_1 = |w_+ - w_-| = w_+ (1 - e^{-2\beta \mu_5}) > 0.0$$
     - For $\mu_5 \not\equiv 0 \pmod{\omega_0}$, the cochain holonomy is **non-contractible** ($\operatorname{Hol}(c^1) \neq 1.0$), inducing strictly positive cochain curvature:
       $$\Gamma_2 = \left|\operatorname{Arg}(\operatorname{Hol}(c^1))\right| > 0.0$$
     - The combination of exponential weight asymmetry and non-contractible cochain holonomy destroys exact sign cancellation in the GIN quotient, leaving irreducible defect mass $\Phi_1 > 0$ and routing deterministically to:
       $$\textbf{TerminalRoute.SplitBrainRefusal}$$

### 9.11 2D Fractional Quantum Hall States ($\nu = 1/3$): Laughlin Wavefunctions, Anyonic Braiding Holonomy, and Abelian Involution Obstruction

To determine whether fractional topological exchange statistics preserve exact fermion sign cancellation or induce non-contractible cochain holonomy, we analyze 2D Fractional Quantum Hall (FQH) states at filling fraction $\nu = 1/3$ under anyonic quasiparticle braiding and GIN mode indexing (`code/fqh_laughlin_braiding.py`).

- **Laughlin Ground State & Quasiparticle Statistics**:
  In a 2D electron gas subject to high perpendicular magnetic field $B$, electrons at filling factor $\nu = 1/m = 1/3$ condense into the incompressible Laughlin ground state:
  $$\Psi_m(z_1, \dots, z_N) = \prod_{1 \le j < k \le N} (z_j - z_k)^m \exp\left( -\sum_{j=1}^N \frac{|z_j|^2}{4 \ell_B^2} \right), \quad m = 3$$
  Elementary quasiholes and quasielectrons carry fractional electric charge $e^* = e / m = e / 3$.
  Under elementary spatial exchange (transposition $\tau = (1 \leftrightarrow 2)$), the state accumulates a fractional statistical phase:
  $$\theta_{\text{stat}} = \frac{\pi}{m} = \frac{\pi}{3} \quad (60^\circ), \quad \eta_{\text{stat}} = \exp\left(i \frac{\pi}{3}\right) = \frac{1}{2} + i \frac{\sqrt{3}}{2} \notin \{+1, -1\}$$
  A full adiabatic braiding cycle (one quasiparticle encircled completely around another, representing two counter-clockwise exchanges) accumulates the monodromy phase:
  $$\theta_{\text{braid}} = 2 \theta_{\text{stat}} = \frac{2\pi}{3} \quad (120^\circ), \quad \eta_{\text{braid}} = \exp\left(i \frac{2\pi}{3}\right) = -\frac{1}{2} + i \frac{\sqrt{3}}{2}$$

- **Modular $S$-Matrix Unitarity & Monodromy Consistency**:
  The anyon superselection sectors are governed by the modular $S$-matrix ($m \times m$ unitary matrix over $\mathbb{Z}_m$):
  $$S_{a,b} = \frac{1}{\sqrt{m}} \exp\left(i \cdot 2\pi \frac{a b}{m}\right), \quad a, b \in \{0, 1, \dots, m-1\}$$
  Satisfying exact unitarity $\|S^\dagger S - I\|_\infty \le 10^{-12}$. The monodromy between fundamental quasiparticles extracts identically:
  $$M_{1,1} = \frac{S_{1,1} S_{0,0}}{S_{0,1} S_{1,0}} = \exp\left(i \cdot 2\pi \frac{1}{m}\right) = \exp\left(i \frac{2\pi}{3}\right)$$

- **1-Cochain Holonomy & Non-Contractible Cochain Curvature**:
  Around the closed braiding loop $\gamma \in Z_1(K)$, the 1-cochain holonomy evaluates to:
  $$\operatorname{Hol}(c^1) = \exp\left(i \oint_\gamma \mathcal{A}_{\text{Berry}} \cdot d\mathbf{x}\right) = \exp\left(i \frac{2\pi}{3}\right) = -\frac{1}{2} + i \frac{\sqrt{3}}{2} \neq 1.0 + 0.0i$$
  Because $\operatorname{Hol}(c^1) \neq 1.0$, the braiding cycle is **non-contractible**, inducing strictly positive scalar cochain curvature:
  $$\Gamma_2 = \|\overline{d}_1(q)\|_{C^2} = \left|\operatorname{Arg}\left(\operatorname{Hol}(c^1)\right)\right| = \frac{2\pi}{3} \approx 2.094395 > 0$$

- **Obstruction of Exact Abelian Involution Pairing $\Xi$**:
  Evaluating whether an exact involution pairing witness $\Xi$ can restore average sign in the GIN quotient reveals two obstructions:
  1. *Order Mismatch ($\mathbb{Z}_2$ vs. $\mathbb{Z}_3$)*: Any involution satisfies $\Xi^2 = \mathrm{id}$, restricting its action to signs $\pm 1$. The anyonic braiding phase belongs to $\mathbb{Z}_3$. Because $\gcd(2, 3) = 1$, no $\mathbb{Z}_2$ involution can generate or cancel the $\mathbb{Z}_3$ phase.
  2. *Boltzmann Energy Asymmetry*: In background magnetic field $B > 0$, the quasielectron creation gap exceeds the quasihole gap ($\Delta_{\text{qe}} \approx 0.073 e^2 / \epsilon \ell_B > \Delta_{\text{qh}} \approx 0.026 e^2 / \epsilon \ell_B$), inducing an exponential thermal weight discrepancy:
     $$w_{\text{qh}} = e^{-\beta \Delta_{\text{qh}}} > w_{\text{qe}} = e^{-\beta \Delta_{\text{qe}}} \implies \Phi_1 = |w_{\text{qh}} - w_{\text{qe}}| > 0$$
  Consequently, fractional anyonic statistics break exact sign cancellation and cannot be repaired by abelian involution pairing. Under Boundary-Quotient Normal Form (BQNF), non-contractible holonomy ($\Gamma_2 > 0$) with uncancelled defect mass routes deterministically to:
  $$\textbf{TerminalRoute.OpenSignObstruction}$$

### 9.12 Non-Abelian Fibonacci Anyon Braiding, Pentagon Equations, & Quantum State Leakage

Beyond abelian fractional statistics, non-abelian topological phases (such as the Fibonacci anyon model realized in $\mathbb{Z}_3$ Read-Rezayi quantum Hall states or non-abelian topological quantum computation platforms) feature fusion spaces whose dimension grows with particle number, permitting universal quantum computation via braid operations:

- **Fusion Rules & Golden Ratio Quantum Dimensions**:
  The Fibonacci anyon category contains the vacuum $\mathbf{1}$ and a single non-abelian anyon $\tau$ governed by the fusion rules:
  $$\mathbf{1} \otimes \mathbf{1} = \mathbf{1}, \quad \mathbf{1} \otimes \tau = \tau \otimes \mathbf{1} = \tau, \quad \tau \otimes \tau = \mathbf{1} \oplus \tau$$
  The quantum dimensions satisfy $d_1 = 1$ and $d_\tau^2 = d_1 + d_\tau = 1 + d_\tau$, uniquely fixing $d_\tau$ to the golden ratio:
  $$d_\tau = \phi = \frac{1 + \sqrt{5}}{2} \approx 1.6180339887...$$
  The total quantum dimension of the modular tensor category evaluates to:
  $$\mathcal{D} = \sqrt{d_1^2 + d_\tau^2} = \sqrt{2 + \phi} = \sqrt{\frac{5 + \sqrt{5}}{2}} \approx 1.902113$$

- **$F$-Matrix & Mac Lane Pentagon Equation**:
  In the basis $\{|\mathbf{1}\rangle, |\tau\rangle\}$ for the fusion $\tau \otimes \tau \otimes \tau \to \tau$, the associator $F$-matrix is:
  $$F = F^{\tau\tau\tau}_\tau = \begin{pmatrix} \phi^{-1} & \phi^{-1/2} \\ \phi^{-1/2} & -\phi^{-1} \end{pmatrix}$$
  The $F$-matrix is an orthogonal involution ($F = F^\dagger = F^T = F^{-1}$, $F^2 = I$). Across all 4-anyon fusion trees, $F$ satisfies the 5-term Mac Lane pentagon equation:
  $$(F^{f c d}_e)_{g, l} (F^{a b l}_e)_{f, k} = \sum_m (F^{a b c}_g)_{f, m} (F^{a m d}_e)_{g, k} (F^{b c d}_k)_{m, l}$$
  to exact machine precision ($\max |\Delta| < 1.12 \times 10^{-16}$).

- **Braiding Generators & Artin Braid Relations**:
  The topological exchange matrix is $R = \operatorname{diag}(e^{-i 4\pi/5}, e^{i 3\pi/5})$. On the single topological qubit space $\mathcal{H}_3 = \operatorname{span}\{|0\rangle \equiv |(\tau\tau)_1\rangle, |1\rangle \equiv |(\tau\tau)_\tau\rangle\}$, the braid generators are:
  $$\sigma_1 = R = \begin{pmatrix} e^{-i 4\pi/5} & 0 \\ 0 & e^{i 3\pi/5} \end{pmatrix}, \quad \sigma_2 = F R F$$
  The Artin braid relation holds identically:
  $$\sigma_1 \sigma_2 \sigma_1 = \sigma_2 \sigma_1 \sigma_2 \quad \left(\|\sigma_1 \sigma_2 \sigma_1 - \sigma_2 \sigma_1 \sigma_2\|_\infty < 10^{-15}\right)$$
  However, the braid operations are strictly non-commutative:
  $$[\sigma_1, \sigma_2] = \sigma_1 \sigma_2 - \sigma_2 \sigma_1 \neq 0, \quad \|[\sigma_1, \sigma_2]\|_F \approx 1.798907 > 0$$

- **1-Cochain Matrix Holonomy & Non-Contractible Cochain Curvature**:
  Along the closed commutator braiding loop $\gamma_{\text{comm}} = \sigma_1 \sigma_2 \sigma_1^{-1} \sigma_2^{-1} \in U(2)$, the 1-cochain holonomy evaluates to:
  $$\operatorname{Hol}(\gamma_{\text{comm}}) = \sigma_1 \sigma_2 \sigma_1^{-1} \sigma_2^{-1} = \begin{pmatrix} 0.190983 + 0.587785i & -0.636010 - 0.462088i \\ 0.636010 - 0.462088i & 0.190983 - 0.587785i \end{pmatrix} \neq I$$
  yielding strictly positive scalar cochain curvature:
  $$\Gamma_2 = \|\operatorname{Hol}(\gamma_{\text{comm}}) - I\|_F \approx 1.798907 > 0$$

- **Commutative Quotient Projection & Exact Quantum State Leakage**:
  When attempting to project the non-abelian quantum states into a classical scalar mode posting list or 1D ray via $P_0 = |0\rangle\langle 0|$, the braid operation rotates state vectors out of the projection ray. For the elementary braid generator $\sigma_2$, the quantum state leakage into the orthogonal channel $|1\rangle$ is given in exact closed form by:
  $$\mathcal{L}_{\text{leak}}(\sigma_2) = 1 - |\langle 0 | \sigma_2 | 0 \rangle|^2 = |\langle 1 | \sigma_2 | 0 \rangle|^2 = \phi^{-3}(2 + \phi^{-1}) = \phi^{-1} = \frac{\sqrt{5}-1}{2} \approx 0.6180339887... > 0$$

- **Schur's Lemma Obstruction to Exact Involution Pairing $\Xi$**:
  Because the braid group representation of Fibonacci anyons is irreducible (dense in $SU(2)$), by Schur's Lemma the only operators commuting with all braid generators are scalar multiples of the identity ($c I$). Consequently, no non-trivial involution witness $\Xi$ (with $\Xi^2 = I$ and eigenvalues $\pm 1$) can commute with both $\sigma_1$ and $\sigma_2$:
  $$\|[\sigma_2, \sigma_z]\|_F \approx 2.223572 > 0$$
  Any attempt to construct an abelian sign-pairing involution is disrupted by the non-abelian rotation. Under BQNF, non-contractible matrix holonomy ($\Gamma_2 > 0$) with uncancelled defect mass $\Phi_1 = \|[\sigma_1, \sigma_2]\|_F + \mathcal{L}_{\text{leak}} \approx 2.416941 > 0$ routes deterministically to:
  $$\textbf{TerminalRoute.OpenSignObstruction}$$

### 9.13 Non-Abelian Ising Anyon / Majorana Braiding, Clifford Stability, & Non-Clifford Magic State Defect

While universal non-abelian anyons (such as Fibonacci anyons) suffer from generic quantum state leakage and non-abelian cochain holonomy, Ising anyons and Majorana zero modes generate a discrete subgroup of unitaries that reveals the exact boundary between sign-free classical simulation and the fermion sign problem:

- **Ising Fusion Category & Quantum Dimensions**:
  The Ising anyon model consists of the vacuum $\mathbf{1}$, a non-abelian anyon $\sigma$ (Majorana zero mode), and a Dirac fermion $\psi$, governed by the fusion algebra:
  $$\sigma \otimes \sigma = \mathbf{1} \oplus \psi, \quad \sigma \otimes \psi = \psi \otimes \sigma = \sigma, \quad \psi \otimes \psi = \mathbf{1}$$
  with quantum dimensions $d_1 = 1$, $d_\psi = 1$, and $d_\sigma = \sqrt{2}$, yielding total quantum dimension $\mathcal{D} = \sqrt{1^2 + (\sqrt{2})^2 + 1^2} = 2.0$.

- **Majorana Braiding & Clifford Group Equivalence**:
  In a 4-Majorana qubit encoding with fixed fermion parity $P = \gamma_1 \gamma_2 \gamma_3 \gamma_4 = +1$, the topological qubit space is $\mathcal{H}_1 = \operatorname{span}\{|0\rangle, |1\rangle\}$. The elementary braid operators:
  $$\tau_1 = \exp\left(\frac{\pi}{4} \gamma_2 \gamma_1\right) = \frac{1}{\sqrt{2}} (1 + \gamma_2 \gamma_1) = e^{-i \frac{\pi}{4} Z}, \quad \tau_2 = \exp\left(\frac{\pi}{4} \gamma_3 \gamma_2\right) = e^{-i \frac{\pi}{4} X}$$
  generate the single-qubit Clifford group $\mathcal{C}_1$ (isomorphic to the octahedral group modulo phases). Under conjugation, Clifford braid operators map Pauli operators to Pauli operators ($U P U^\dagger \in \mathcal{P}_1$ for all $P \in \{X, Y, Z\}$).

- **Clifford Stabilizer Sign-Free Exact Repair**:
  Under pure Clifford braiding circuits, states remain within the discrete set of stabilizer states on the Bloch sphere vertices with $L^1$ norm $\|r\|_1 = |r_x| + |r_y| + |r_z| = 1.0$. Stabilizer states possess non-negative discrete Wigner quasi-probability distributions ($W(p, q) \ge 0$), permitting polynomial-time classical simulation via the Gottesman-Knill theorem. Cochains on the stabilizer complex satisfy $\Gamma_2 = 0.0$ and uncancelled defect mass $\Phi_{\text{magic}} = 0.0$, recovering average sign $\langle\text{Sign}\rangle_{\text{GIN}} = 1.0$ and routing deterministically to:
  $$\textbf{TerminalRoute.ExactRepair}$$

- **Non-Clifford Gate Synthesis ($T$-Gate Injection & Magic State Defect)**:
  Universal topological quantum computation with Majorana zero modes requires non-Clifford gate synthesis (magic state injection and distillation). Injecting a non-Clifford $T$-gate ($T = \operatorname{diag}(1, e^{i \pi/4}) \notin \mathcal{C}_1$) creates the magic state:
  $$|T\rangle = T |+\rangle = \frac{1}{\sqrt{2}} \left(|0\rangle + e^{i \pi/4}|1\rangle\right)$$
  which violates Pauli closure under conjugation:
  $$T X T^\dagger = \frac{1}{\sqrt{2}} (X + Y) \notin \mathcal{P}_1 \quad \left(\min_{P \in \mathcal{P}_1} \|T X T^\dagger - P\|_F \approx 1.082392 > 1.0\right)$$
  The Bloch vector $r = (1/\sqrt{2}, 1/\sqrt{2}, 0)$ punctures the stabilizer octahedron:
  $$\|r\|_1 = \frac{1}{\sqrt{2}} + \frac{1}{\sqrt{2}} = \sqrt{2} \approx 1.414214 > 1.0 \implies \mathcal{R}(|T\rangle) = \sqrt{2} - 1 \approx 0.414214$$
  inducing negative discrete Wigner quasi-probabilities:
  $$\mathcal{N}(|T\rangle) = \frac{\sqrt{2} - 1}{2} \approx 0.207107 > 0$$

- **Non-Stabilizer Cochain Holonomy & Resurgent Sign Obstruction**:
  Around a closed loop containing $T$-gate injection ($\gamma_T = T H T^\dagger H^\dagger \in U(2)$), the 1-cochain holonomy breaks contractibility ($\operatorname{Hol}(\gamma_T) \neq I$), yielding positive non-stabilizer cochain curvature:
  $$\Gamma_2 = \|\operatorname{Hol}(\gamma_T) - I\|_F \approx 0.765367 > 0$$
  The negative quasi-probabilities in the magic state directly manifest as the fermion sign problem in stabilizer path integrals, with uncancelled defect mass:
  $$\Phi_1 = \mathcal{N}(|T\rangle) + \Gamma_2 \approx 0.207107 + 0.765367 = 0.972474 > 0$$
  Under BQNF, non-stabilizer cochain curvature ($\Gamma_2 > 0$) with uncancelled magic defect mass routes deterministically to:
  $$\textbf{TerminalRoute.OpenSignObstruction}$$

### 9.14 3D Topological BF Theory, Linked Flux Loops, & Higher-Dimensional Abelian Braiding Statistics

Extending topological exchange statistics from point particles in 2D to one-dimensional extended string and flux loop excitations in 3D spatial manifolds, we evaluate 3D topological BF theory at discrete level $k \in \mathbb{Z}_{\ge 2}$ under linked loop braiding and GIN mode indexing (`code/bf_topological_braiding.py` and `code/bf_linked_flux_braiding.py`).

- **Action & Dual Topological Gauge Invariance**:
  On a 3D spatial cell complex $K$, topological BF theory couples a 1-form gauge field $A \in C^1(K, \mathbb{R}/2\pi\mathbb{Z})$ and a 2-form gauge field $B \in C^2(K, \mathbb{R}/2\pi\mathbb{Z})$ with level $k$:
  $$S_{BF} = \frac{k}{2\pi} \int_{M^3} B \wedge dA$$
  Electric quasiparticles carry integer charge $q \in \mathbb{Z}_k$ coupled along 1D closed cycles $\gamma$, while magnetic flux tubes carry quantized flux $\Phi = \frac{2\pi p}{k}$ ($p \in \mathbb{Z}_k$) coupled across 2D Seifert surfaces $\Sigma$.

- **Gauss Linking Numbers on Polygonal Complexes**:
  The topological interaction between two disjoint oriented closed loops $\gamma_1, \gamma_2 \subset \mathbb{R}^3$ is determined by the integer Gauss linking integral:
  $$\operatorname{Lk}(\gamma_1, \gamma_2) = \frac{1}{4\pi} \oint_{\gamma_1} \oint_{\gamma_2} \frac{(\mathbf{r}_1 - \mathbf{r}_2) \cdot (d\mathbf{r}_1 \times d\mathbf{r}_2)}{|\mathbf{r}_1 - \mathbf{r}_2|^3} \in \mathbb{Z}$$
  For unlinked loops, $\operatorname{Lk} = 0$; for the standard interlocking Hopf link, $\operatorname{Lk} = +1$; under loop orientation inversion $\tau: \gamma_2 \mapsto -\gamma_2$, the linking number reverses sign: $\operatorname{Lk}(\gamma_1, -\gamma_2) = -\operatorname{Lk}(\gamma_1, \gamma_2) = -1$; for Whitehead-type clasp loops, the net pairwise linking vanishes ($\operatorname{Lk} = 0$).

- **Topological Monodromy & 2-Cochain Holonomy**:
  When a unit charge loop $\gamma_1$ ($q=1$) completely braids through a unit flux loop $\gamma_2$ ($p=1$), the system accumulates the abelian topological monodromy phase:
  $$\theta_{BF} = \frac{2\pi}{k} q p \operatorname{Lk}(\gamma_1, \gamma_2) \pmod{2\pi}$$
  yielding the 2-cochain holonomy factor:
  $$\operatorname{Hol}(c^2) = \exp(i \theta_{BF}) = \cos\left(\frac{2\pi}{k} \operatorname{Lk}\right) + i \sin\left(\frac{2\pi}{k} \operatorname{Lk}\right)$$
  For unlinked configurations ($\operatorname{Lk} = 0$), $\operatorname{Hol}(c^2) = 1.0 + 0.0i$ is strictly contractible, with zero cochain curvature ($\Gamma_2 = 0.0$). For linked configurations ($\operatorname{Lk} \neq 0$), $\operatorname{Hol}(c^2) \neq 1.0$, producing non-zero scalar cochain curvature $\Gamma_2 = |\theta_{BF}| > 0$.

- **Discrete Level Parity Trichotomy ($k=2$ vs $k \ge 3$)**:
  Evaluating whether an exact involution pairing witness $\Xi$ can eliminate sign oscillations reveals a sharp trichotomy governed by the level $k$:
  1. *$\mathbb{Z}_2$ BF Theory ($k = 2$ / 3D Toric Code)*:
     The braiding phase evaluates to $\theta_{BF} = \pi \cdot \operatorname{Lk} \equiv \pi \pmod{2\pi}$, producing a strictly real sign factor $\eta_{BF} = e^{i\pi} = -1.0 \in \{+1, -1\}$. Under symmetric orientation weights ($\Delta E_{\text{orient}} = 0 \implies w_+ = w_-$), an exact $\mathbb{Z}_2$ involution pairing $\Xi$ pairs the negative flux configuration with its orientation-reversed partner, cancelling sign oscillations ($\langle\text{Sign}\rangle_{\text{GIN}} = 1.0, \Phi_1 = 0.0$) and routing deterministically to:
     $$\textbf{TerminalRoute.ExactRepair}$$
  2. *$\mathbb{Z}_k$ Fractional BF Theory ($k \ge 3$, e.g. $k = 3$)*:
     The braiding phase $\theta_{BF} = 2\pi/3$ yields complex holonomy $\eta_{BF} = -1/2 + i \sqrt{3}/2 \notin \mathbb{R}$. Because $\gcd(2, 3) = 1$, no real $\mathbb{Z}_2$ involution can generate or cancel the $\mathbb{Z}_3$ phase; averaging across orientation-paired loops yields $\frac{1}{2}(e^{i 2\pi/3} + e^{-i 2\pi/3}) = \cos(2\pi/3) = -0.5 < 1.0$. The uncancelled defect mass evaluates to $\Phi_1 = |1 - \cos(2\pi/k)| + \Gamma_2 > 0$, routing deterministically to:
     $$\textbf{TerminalRoute.OpenSignObstruction}$$
  3. *Orientation Energy Asymmetry ($\Delta E_{\text{orient}} > 0$)*:
     When background fields (such as a chiral 3-form or external magnetic gradient) break orientation degeneracy, the thermal weights satisfy $w_+ = e^{-\beta E_0} \neq w_- = e^{-\beta(E_0 + \Delta E_{\text{orient}})}$. The resulting weight gap $\Delta w = |w_+ - w_-| > 0$ obstructs weight-preserving involution pairing, routing deterministically to:
     $$\textbf{TerminalRoute.SplitBrainRefusal}$$

### 9.15 (3+1)D Non-Abelian Topological BF Theory, Wang-Levin 3-Loop Braiding, & Quantum Double Projection Repair

Extending beyond abelian loop braiding, we formulate and mechanize (3+1)D non-abelian topological BF theory with gauge group $SU(2)_k$ ($k \in \mathbb{Z}_{\ge 2}$) coupled to 1D Wilson loops $\gamma_i$ and 2D 't Hooft surface flux sheets $\Sigma_i$ under GIN mode indexing (`code/bf_nonabelian_3loop_braiding.py`, `code/tests/integration/test_bf_nonabelian_3loop_braiding.py`, and `lean4/NonAbelianBfBraiding.lean`).

- **$SU(2)_k$ Modular Category & Fusion Associativity**:
  Objects are labeled by spin $j \in \{0, 1/2, 1, \dots, k/2\}$. The quantum dimensions evaluate to:
  $$d_j = \frac{\sin\left(\frac{(2j+1)\pi}{k+2}\right)}{\sin\left(\frac{\pi}{k+2}\right)}, \qquad \mathcal{D} = \sqrt{\sum_{2j=0}^k d_j^2}$$
  with conformal weights $h_j = \frac{j(j+1)}{k+2}$ and topological twists $\theta_j = \exp(2\pi i h_j)$. Fusion tensor associativity is governed by the Racah-Wigner $6j$ symbols ($F$-matrix), which for fundamental representations $j=1/2$ forms an orthogonal $2 \times 2$ matrix:
  $$F = \begin{pmatrix} \frac{1}{d_{1/2}} & \frac{\sqrt{d_1}}{d_{1/2}} \\ \frac{\sqrt{d_1}}{d_{1/2}} & -\frac{1}{d_{1/2}} \end{pmatrix}$$

- **Wang-Levin Borromean 3-Loop Braiding Invariants**:
  In a 3D spatial slice, three loop excitations $(\gamma_1, \gamma_2, \gamma_3)$ carrying flux representations $(j_1, j_2, j_3)$ interact through 3-loop braiding (Wang & Levin 2014). For three fundamental spin-1/2 loops, the internal fusion space $V_{1/2, 1/2, 1/2}^{1/2}$ is 2-dimensional (singlet $j_{12}=0$ and triplet $j_{12}=1$). The 3-loop braiding operator is defined by the Borromean commutator:
  $$M_{\text{WL}} = B_1 B_2 B_1^{-1} B_2^{-1} \in \operatorname{End}(V)$$
  where $B_1 = R^2$ and $B_2 = F R^2 F^{-1}$ represent mutual loop monodromies across alternate fusion channels.

- **Non-Abelian Sign Obstruction**:
  1. *Abelian Limit ($j=0$ / commuting loops)*: When loop fluxes are trivial or braiding operators commute ($[B_1, B_2] = 0$), $M_{\text{WL}} = \mathbb{I}$, yielding contractible curvature ($\Gamma_2 = 0.0$), zero defect mass ($\Phi_1 = 0.0$), and routing deterministically to:
     $$\textbf{TerminalRoute.ExactRepair}$$
  2. *Non-Abelian Obstruction ($k \ge 2$, $j=1/2$)*: For $SU(2)_2$ (Ising level), the Borromean commutator evaluates to $M_{\text{WL}} = -\mathbb{I}$, yielding trace $\operatorname{Tr}(M_{\text{WL}}) = -2.0$, normalized trace $\tau = -1.0 < 0$, non-contractible curvature $\Gamma_2 = \pi$, and uncancelled defect mass $\Phi_1 = 2.0 > 0$. For $SU(2)_3$ (Fibonacci level), $F$-matrix non-commutativity yields an indefinite trace $\operatorname{Tr}(M_{\text{WL}}) \approx -1.09$. Because non-abelian matrix holonomies cannot be diagonalized into real involution doublets under abelian $\mathbb{Z}_2$ pairing, the sign problem is irreducible, routing deterministically to:
     $$\textbf{TerminalRoute.OpenSignObstruction}$$
  3. *Orientation Energy Gap ($\Delta E_{\text{orient}} > 0$)*: Thermal weight asymmetry ($w_+ \neq w_-$) produces disjoint weight spectra, routing to:
     $$\textbf{TerminalRoute.SplitBrainRefusal}$$

- **Quantum Double Projection Repair ($P_{\text{QD}}$)**:
  Folding the chiral non-abelian BF sector with an antichiral conjugate sector via the Drinfeld double projector $P_{\text{QD}} : SU(2)_k \boxtimes \overline{SU(2)}_k \to \mathcal{Z}(SU(2)_k) \cong D(SU(2)_k)$ constructs the doubled operator:
  $$M_{\text{QD}} = M_{\text{WL}} \otimes M_{\text{WL}}^\dagger$$
  The trace evaluates to the modulus squared of the chiral trace:
  $$\operatorname{Tr}(M_{\text{QD}}) = \operatorname{Tr}(M_{\text{WL}}) \cdot \overline{\operatorname{Tr}(M_{\text{WL}})} = |\operatorname{Tr}(M_{\text{WL}})|^2 \ge 0$$
  which is identically real and positive-semidefinite. The normalized trace satisfies $\tau_{\text{QD}} = 1.0$, completely nullifying the cochain curvature ($\Gamma_2 = 0.0$) and defect mass ($\Phi_1 = 0.0$), restoring $\langle\operatorname{Sign}\rangle_{\text{GIN}} = 1.0$, and routing deterministically to:
  $$\textbf{TerminalRoute.ExactRepair}$$

### 9.16 4D Higher-Categorical 2-Group Gauge Theory, Postnikov Invariant $[a] \in H^3(BG, H)$, and Higher 2-Double Sign Repair

To probe the ultimate dimensional boundary of topological sign cancellation, we formulate 4D higher-categorical 2-group gauge theory $\mathbb{G} = (G, H, \partial, \alpha)$ on 4-complexes, coupling 1-form gauge connections $A \in C^1(K, G)$ to 2-form surface defects $B \in C^2(K, H)$ under GIN mode indexing (`code/higher_2group_gauge_bf.py`):

- **Strict Crossed Module Structure & 4-Complex Geometry**:
  A strict 2-group is specified by the crossed module $(G, H, \partial, \alpha)$ where $G$ acts on directed 1-cells (edges), $H$ acts on directed 2-cells (faces), $\partial : H \to G$ is a group homomorphism, and $\alpha : G \to \operatorname{Aut}(H)$ is an action ($g \triangleright h$) satisfying:
  - *Peiffer Identity*: $\partial(g \triangleright h) = g \partial(h) g^{-1}$.
  - *Crossed Module Condition*: $\partial(h_1) \triangleright h_2 = h_1 h_2 h_1^{-1}$.
  On a 4-simplex complex $\Delta^4$ with vertices $\{0, 1, 2, 3, 4\}$, boundary operators $\partial_1, \partial_2, \partial_3$ and coboundaries $d_0, d_1, d_2$ satisfy exact nilpotence ($d_1 d_0 = 0, d_2 d_1 = 0$).

- **Fake Flatness & The Postnikov 3-Cocycle Defect**:
  A 2-connection $(A, B)$ satisfies fake flatness on each 2-cell $f$:
  $$F_A(f) = \prod_{e \in \partial f} g_e \cdot \partial(h_f)^{-1} = 1 \in G.$$
  On each 3-simplex (tetrahedron $\tau = (i, j, k, l)$), the 2-connection 3-curvature is constrained by the Postnikov invariant $[a] \in H^3(BG, H)$:
  $$(\delta_A B)(\tau) = h_{jkl} - h_{ikl} + h_{ijl} - h_{ijk} = a(g_{ij}, g_{jk}, g_{kl}) \in H.$$
  The 3-cocycle $a \in Z^3(BG, H)$ satisfies the cocycle condition $\delta_G a = 0$ on all 4-simplices. For $G = \mathbb{Z}_2, H = \mathbb{Z}_2$, the non-trivial generator is the cup product $a = w_1^3$ ($a(g_1, g_2, g_3) = g_1 g_2 g_3 \pmod 2$).

- **Linked 2-Surface / Wilson Loop Braiding & 1-Form Quantum Double Obstruction**:
  In 4D, 1D Wilson loops $\mathcal{W}(\gamma_1)$ and 2D 't Hooft surface defects $\mathcal{U}(\Sigma_2)$ exhibit non-trivial 4D linking and braiding.
  1. *Trivial Postnikov Class ($[a] = 0$)*: Bare holonomy is sign-free ($+1$), $\Phi_1 = 0.0$, routing to `TerminalRoute.ExactRepair`.
  2. *Non-Trivial Postnikov Class ($[a] \neq 0$)*: Under non-trivial linking ($\operatorname{Lk} = 1$), the 3-cocycle defect induces a topological sign phase $(-1)^{[a]} = -1$, yielding bare holonomy $-1$, cochain curvature $\Gamma_2 = \pi$, and defect mass $\Phi_1 = 2.0$.
  3. *Failure of 1-Form Quantum Double Projection ($P_{\text{QD}}^{(1)} = D(G)$)*: Applying the ordinary 1-form quantum double doubles only the 1-gauge group $G \times G^{\text{op}}$. It **fails** to cancel the 2-surface 3-cocycle phase, leaving the negative sign invariant uncancelled ($\operatorname{Tr}(M_{\text{QD}}^{(1)}) = -1 < 0, \Phi_1 = 2.0 > 0$), routing deterministically to:
     $$\textbf{TerminalRoute.OpenSignObstruction}$$
  4. *Thermal Weight Asymmetry ($\Delta E_{\text{orient}} > 0$)*: Boltzmann splitting ($w_+ \neq w_-$) routes to `TerminalRoute.Refused`.

- **Higher-Categorical 2-Double Crossed-Module Repair ($P_{2\text{-QD}}$)**:
  To eliminate the Postnikov obstruction, the system must be projected via the **higher 2-double** $\mathbb{D}(\mathbb{G}) = \operatorname{DrinfeldCenter}(2\operatorname{Rep}(\mathbb{G}))$, which pairs $\mathbb{G} = (G, H, \partial, \alpha, [a])$ with its crossed-module conjugate $\bar{\mathbb{G}} = (G, H, \partial, \alpha, -[a])$.
  Because the 3-cocycle phase inverts on the conjugate sector ($a(A) - a(\bar{A}) = 0$), the doubled 2-surface holonomy satisfies:
  $$\mathcal{U}_{2\text{-QD}}(\Sigma) = \mathcal{U}(\Sigma) \otimes \mathcal{U}(\Sigma)^\dagger$$
  The trace evaluates to $\operatorname{Tr}(M_{2\text{-QD}}) = |\mathcal{U}(\Sigma)|^2 \ge 0$, which is positive-semidefinite. This nullifies the defect mass ($\Phi_1 = 0.0$) and cochain curvature ($\Gamma_2 = 0.0$), recovering $\langle\operatorname{Sign}\rangle_{\text{GIN}} = 1.0$, and routing deterministically to:
  $$\textbf{TerminalRoute.ExactRepair}$$

### 9.17 5D Cobordism Invariants $\Omega_5^{\text{Spin}}(B\mathbb{G})$ and Non-Perturbative Gravitational Sign Obstructions

To determine whether higher 2-double sign cancellation remains valid on non-orientable or spin-cobordant 4-manifolds, we formulate 5D cobordism invariants and higher anomaly matching under GIN mode indexing (`code/cobordism_5d_higher_anomaly.py`):

- **5D Spin Cobordism Classification $\Omega_5^{\text{Spin}}(B\mathbb{G})$**:
  For a 2-group $\mathbb{G}$ with classifying space $B\mathbb{G}$, anomalies are classified by the Atiyah-Hirzebruch spectral sequence (AHSS) with $E_2^{p, q} = H^p(B\mathbb{G}, \Omega_q^{\text{Spin}}(\text{pt})) \implies \Omega_{p+q}^{\text{Spin}}(B\mathbb{G})$. The $p+q=5$ strata decompose as:
  - $E_2^{5, 0} = H^5(B\mathbb{G}, \mathbb{Z})$: pure 5D gauge topological terms.
  - $E_2^{3, 2} = H^3(B\mathbb{G}, \mathbb{Z}_2) \otimes \Omega_2^{\text{Spin}}$: higher Postnikov-Arf anomaly ($a(A) \cup \operatorname{Arf}$).
  - $E_2^{1, 4} = H^1(B\mathbb{G}, \mathbb{Z}_2) \otimes \Omega_4^{\text{Spin}}$: mixed gauge-gravitational anomaly ($w_1(A) \cup p_1(TM)/2$, where $K3$ surface has $\sigma/16 = 1 \pmod 2$).

- **5D Mapping Torus $M_f^4 = (M^4 \times S^1)_f$ & Large Diffeomorphism Holonomy**:
  For a 4-manifold $M^4$ equipped with a large diffeomorphism $f \in \pi_0(\operatorname{Diff}(M^4))$, the 5D mapping torus evaluates the total mod-2 cobordism invariant $\nu_5(M_f^4) \in \{0, 1\}$. Under mapping torus holonomy, physical states acquire the global phase:
  $$U(f) |\Psi\rangle = (-1)^{\nu_5(M_f^4)} |\Psi\rangle.$$

- **Sign Cancellation vs. Gravitational Anomaly Obstruction**:
  1. *Anomaly-Free Cobordism Sector ($\nu_5 = 0$)*: On 4-manifolds with vanishing 5D cobordism invariant (e.g. $T^4$ with $\nu_5 = 0$), $U(f) = +1$, $[U(f), \Xi] = 0$, and higher 2-double projection $P_{2\text{-QD}}$ restores positive trace ($\Phi_1 = 0.0, \Gamma_2 = 0.0, \langle\text{Sign}\rangle_{\text{GIN}} = 1.0$), routing to:
     $$\textbf{TerminalRoute.ExactRepair}$$
  2. *Non-Perturbative Global Gravitational Anomaly ($\nu_5 = 1$)*: On 4-manifolds with non-trivial cobordism invariant (e.g. $K3$ surface with $\sigma/16 = 1$ and non-trivial gauge flux $w_1 = 1$, or non-trivial Postnikov-Arf coupling), the mapping torus holonomy is strictly negative: $U(f) = -I$.
     Even under higher 2-double projection, the mapping torus twists chiral and antichiral bundles by the large diffeomorphism $f$, producing an uncancelled sign phase:
     $$\operatorname{Tr}(M_f) = -1.0 < 0.$$
     This demonstrates that non-perturbative global gravitational anomalies in $\Omega_5^{\text{Spin}}(B\mathbb{G})$ strictly **obstruct** higher 2-double sign cancellation ($\Phi_1 = 2.0 > 0, \Gamma_2 = \pi$), routing deterministically to:
     $$\textbf{TerminalRoute.OpenSignObstruction}$$
  3. *Non-Orientable $\operatorname{Pin}^-$ Anomaly ($\Omega_5^{\operatorname{Pin}^-}$)*: On non-orientable manifolds such as $\mathbb{R}P^4$, time-reversal anomalies $\nu_{16} \in \mathbb{Z}_{16}$ generate non-real complex phases $\exp(2\pi i \nu_{16}/16)$, routing to `TerminalRoute.OpenSignObstruction`.
  4. *Thermal Weight Asymmetry ($\Delta E_{\text{orient}} > 0$)*: Boltzmann splitting ($w_+ \neq w_-$) routes to `TerminalRoute.Refused`.

### 9.18 Semiclassical Instanton-Dyon Topological Gas Expansions and Monopole Loop Braiding

To evaluate whether semiclassical non-perturbative topological fluctuations generate sign frustration or admit involution repairs, we formulate the instanton-dyon (caloron) topological gas and 't Hooft-Polyakov monopole loop braiding in 4D compact gauge theories under GIN mode indexing (`code/instanton_dyon_gas_braiding.py`, `code/tests/integration/test_instanton_dyon_gas_braiding.py`, `lean4/InstantonDyonGas.lean`).

#### 1. KvBLL Fractional Instanton-Dyons

In 4D $SU(2)$ compact gauge theory on $\mathbb{R}^3 \times S^1$ with Polyakov loop holonomy $P_\infty = \operatorname{diag}(e^{i\pi\nu}, e^{-i\pi\nu})$, instantons fractionalize into Kraan-van Baal - Lee-Lu (KvBLL) constituent dyons:

- $M$-dyon (magnetic monopole): magnetic charge $m_M = +1$, fractional topological charge $Q_M = \nu$, core action $S_M = \frac{8\pi^2\nu}{g^2}$.
- $L$-dyon (twisted KK monopole): magnetic charge $m_L = -1$, fractional topological charge $Q_L = 1 - \nu$, core action $S_L = \frac{8\pi^2(1-\nu)}{g^2}$.
- Anti-dyons ($\bar{M}, \bar{L}$): opposite charges $Q_{\bar{M}} = -\nu, Q_{\bar{L}} = -(1-\nu)$, satisfying topological charge conservation $Q_M + Q_L = 1.0$ and action sum $S_M + S_L = S_0 = \frac{8\pi^2}{g^2}$.

At non-zero vacuum angle $\theta = \pi$, Euclidean configurations acquire the topological phase factor $\cos(\pi Q_{\text{net}})$.

#### 2. Inter-Dyon Coulomb Interactions and Regimes

The pairwise dyon interaction potential includes regulated 3D Coulomb magnetic interaction:
$$V(r_{ij}) = \frac{4\pi}{g^2} \frac{m_i m_j}{\max(r_{ij}, r_{\text{core}})}$$

- Like magnetic charges repel ($V > 0$), while opposite charges attract ($V < 0$).
- **Molecular Cluster Regime**: Dyons bind into neutral dipoles $(M\bar{M})$ and $(L\bar{L})$ or quartets $(M\bar{M}L\bar{L})$ with $m_{\text{net}} = 0, Q_{\text{net}} = 0$. The dyonic charge-conjugation / reflection involution $\Xi_{\text{dyon}}: M \leftrightarrow \bar{M}, L \leftrightarrow \bar{L}, \vec{r} \to -\vec{r}$ preserves action ($S[\Xi(c)] = S[c]$) and topological weight ($w_+ = w_-$), yielding uncancelled defect mass $\Phi_1 = 0.0$ and cochain curvature $\Gamma_2 = 0.0$, routing to `TerminalRoute.ExactRepair`.
- **Ionized Plasma Regime**: At high temperature or low density, dyons unbind into isolated charges ($N_M \neq N_{\bar{M}}$). Coulomb repulsion between isolated like charges generates an action gap $\Delta S > 0$ that forces positive and negative weight spectra into disjoint supports ($\operatorname{supp}(w_+) \cap \operatorname{supp}(w_-) = \emptyset$), routing to `TerminalRoute.SplitBrainRefusal`.

#### 3. 't Hooft-Polyakov Monopole Loop Braiding

When monopole worldlines $\gamma_M$ form closed loops linked with center vortex lines or electric Wilson loops $\gamma_W$, the Gauss linking integral evaluates to $\operatorname{Lk}(\gamma_M, \gamma_W) \in \mathbb{Z}$:
$$\operatorname{Lk} = \frac{1}{4\pi} \oint_{\gamma_M} \oint_{\gamma_W} \frac{d\vec{r}_M \times d\vec{r}_W \cdot (\vec{r}_M - \vec{r}_W)}{|\vec{r}_M - \vec{r}_W|^3}$$

- For linked loops ($\operatorname{Lk} = 1$), the Dirac-Aharonov-Bohm phase evaluates to $\Phi_{AB} = (-1)^{\operatorname{Lk}} = -1.0$.
- In non-abelian gauge theory, internal zero-mode Berry holonomies evaluate to $M_{\text{mono}} = -\mathbb{I}$, with negative trace $\operatorname{Tr}(M_{\text{mono}}) = -2.0 < 0$.
- This topological sign inversion cannot be screened or repaired by local dyonic clustering, producing an irreducible defect mass $\Phi_1 = 2.0 > 0$ and cochain curvature $\Gamma_2 = \pi$, routing deterministically to:
$$\textbf{TerminalRoute.OpenSignObstruction}$$

### 9.19 Higher-Form 2-Gauge Defect Networks, Continuous Foliated Fracton Order, & Foliated Categorical Projections

To determine whether non-abelian subsystem symmetries and mobility-restricted excitations generate infinite-order cochain curvature obstructions or admit foliated categorical projection repairs, we formulate higher-form 2-gauge defect networks and continuous foliated fracton order under GIN mode indexing (`code/foliated_fracton_2gauge_defects.py`, `code/tests/integration/test_foliated_fracton_2gauge_defects.py`, `lean4/FoliatedFracton2Gauge.lean`).

#### 1. Foliated Foliation Leaves & Mobility-Restricted Excitations

In a 3D spatial manifold with three orthogonal foliation directions ($\Sigma_{xy}, \Sigma_{yz}, \Sigma_{zx}$), fracton topological order exhibits mobility-restricted excitations:

- **0D Fractons**: Completely immobile point defects. An isolated fracton cannot hop without creating an extensive membrane string across multiple foliation leaves.
- **1D Lineons**: Excitations mobile only along the 1D intersection lines (hinges) of two orthogonal foliation leaves (e.g. $\Sigma_{xy}(z_0) \cap \Sigma_{yz}(x_0)$).
- **2D Planons**: Excitations mobile within an individual 2D foliation leaf.

The system possesses extensive subsystem symmetries whose conserved charges scale with the linear dimension:
$$N_{\text{charges}} = L_x + L_y + L_z$$
where charges on each leaf $\Sigma_{xy}(z), \Sigma_{yz}(x), \Sigma_{zx}(y)$ are independently conserved.

#### 2. Subsystem Regimes & Sign Frustration

Evaluating these structures under GIN mode indexing reveals three distinct topological regimes:

1. *Leaf-Decoupled Neutral Planon Dipoles*:
   When planons form neutral bound dipoles $(f\bar{f})$ strictly confined to a single leaf $\Sigma_{xy}(z_0)$, all other foliation leaves remain uncharged ($Q_{\text{leaf}} = 0$). An exact leaf-preserving involution $\Xi_{\text{fol}}^{(z)}$ pairs positive and negative Trotter paths ($w_+ = w_-$), yielding zero uncancelled defect mass ($\Phi_1 = 0.0$) and contractible curvature ($\Gamma_2 = 0.0$), recovering $\langle\text{Sign}\rangle_{\text{GIN}} = 1.0$ and routing to:
   $$\textbf{TerminalRoute.ExactRepair}$$
2. *Isolated Fracton Separation & Extensive Action Gap*:
   Hopping an isolated 0D fracton across $R$ parallel foliation leaves breaks $R$ independent leaf conservation laws. In continuous foliations or large lattices, the extensive subsystem action gap scales as:
   $$\Delta S_{\text{subsystem}} = \kappa R > 0$$
   This gap strictly separates positive and negative Trotter path weights into disjoint supports ($\operatorname{supp}(w_+) \cap \operatorname{supp}(w_-) = \emptyset$), leaving uncancelled defect mass $\Phi_1 = \kappa R > 0$ with zero curvature ($\Gamma_2 = 0.0$), routing deterministically to:
   $$\textbf{TerminalRoute.SplitBrainRefusal}$$
3. *Intersecting Non-Abelian 2-Gauge Defect Sheets*:
   Coupling 1-form gauge fields to non-abelian 2-gauge defect sheets on intersecting leaves ($\Sigma_{xy}$ and $\Sigma_{yz}$) induces non-trivial commutator holonomy on the 1D hinge line:
   $$M_{\text{hinge}} = B_{xy} B_{yz} B_{xy}^{-1} B_{yz}^{-1} \in \operatorname{End}(V)$$
   At non-abelian level $k=2$ (Ising level), $M_{\text{hinge}} = -\mathbb{I}$, with negative trace $\operatorname{Tr}(M_{\text{hinge}}) = -2.0 < 0$. This induces uncancelled defect mass $\Phi_1 = 2.0 > 0$ and non-contractible 2-cochain curvature $\Gamma_2 = \pi$, routing deterministically to:
   $$\textbf{TerminalRoute.OpenSignObstruction}$$

#### 3. Foliated Categorical Projections & Corner Lineon Obstruction

In foliated quantum field theory, the state space can be factored by leaf-wise decoupled 2D topological layers via the foliated quantum double projector:
$$P_{\text{fol-QD}} = \prod_{z=1}^{L_z} D\left(G_{xy}^{(z)}\right) \otimes \prod_{x=1}^{L_x} D\left(G_{yz}^{(x)}\right) \otimes \prod_{y=1}^{L_y} D\left(G_{zx}^{(y)}\right)$$

- *Decoupled Foliation Sheets*: When defect sheets remain parallel or decoupled across leaves, $P_{\text{fol-QD}}$ projects each leaf into a positive semi-definite trace $\operatorname{Tr}(M_{\text{fol}}) = |\operatorname{Tr}(M)|^2 \ge 0$, completely nullifying defect mass ($\Phi_1 = 0.0, \Gamma_2 = 0.0$) and restoring `TerminalRoute.ExactRepair`.
- *Corner Lineon Obstruction*: When excitations turn corners at the 1D hinge line by scattering with a 1D lineon, the corner operator non-locally couples the orthogonal foliation planes $\Sigma_{xy}$ and $\Sigma_{yz}$. The product of decoupled 2D quantum doubles $P_{\text{fol-QD}}$ fails to factorize the corner lineon junction, preserving the negative trace $\operatorname{Tr}(M) = -2.0 < 0$, uncancelled defect mass $\Phi_1 = 2.0 > 0$, and curvature $\Gamma_2 = \pi$, routing deterministically to:
$$\textbf{TerminalRoute.OpenSignObstruction}$$

---

## Section 10: Relational SQL Engine & Normal Forms Architecture

The historical GIN display schema uses SQLite REAL fields (`databases/fermion_gin_index_schema.sql`):

```sql
CREATE TABLE IF NOT EXISTS FermionConfigurations (
    cfg_id INT PRIMARY KEY,
    model_name TEXT NOT NULL,
    num_particles INT NOT NULL,
    total_modes INT NOT NULL,
    weight REAL NOT NULL,
    jw_sign INT NOT NULL CHECK (jw_sign IN (-1, 1)),
    parity_sector INT NOT NULL CHECK (parity_sector IN (-1, 1))
);

CREATE TABLE IF NOT EXISTS GinModePostingList (
    mode_id INT NOT NULL,
    cfg_id INT NOT NULL REFERENCES FermionConfigurations(cfg_id),
    is_occupied INT NOT NULL CHECK (is_occupied IN (0, 1)),
    PRIMARY KEY (mode_id, cfg_id)
);
```

### 10.1 Auditing CTE Views

1. `ViewFspInvolutionSignCancellationAudit`: Historical floating-point display. Its tolerance is not an exactness certificate. The repaired Hamiltonian bridge checks authoritative rational path records; Section 15 uses exact SQL arithmetic.
2. `ViewAverageSignRecoveryAudit`: Evaluates raw average sign versus GIN quotiented average sign, routing to `Repair` or `SplitBrainRefusal`.
3. `ViewMajoranaZeroModeAudit`: Validates the isolation of edge modes $\gamma_1, \gamma_{2L}$ from all bulk bonds.

### 10.2 Normal Forms Architecture

The historical YAML collection mixes database schema predicates and operational contracts. Contract validation does not establish a normalizer. The audited normal forms and their exact equivalence relations are developed in Section 13 and `docs/normal_form_audit.md`:

- `BQNF-FSIGN` (`nf.change.bqnf.fermion_sign.yaml`): Standardizes the 5-fold routing of sign cochains.
- `WDWNF` (`nf.physics.wdwnf.yaml`): Governs the Wheeler-DeWitt constraint defect evaluation.

---

## Section 11: Formal Mechanization and Its Scope

The Lean package contains conditional algebraic lemmas and finite fixtures. A theorem name or `rfl` status string does not certify a physical interpretation. In particular, `GenesisFspBridge.lean` does not formalize a reduction from the sealed inscription to a Hubbard Hamiltonian or the Troyer–Wiese theorem; that interpretation is withdrawn. Its positivity theorem for a product of natural numbers is not an exponential variance or computational hardness proof.

`MeronCharacter.lean` adds a general theorem for **all finite Boolean flip lists**: an admitted sign character sums to zero when a meron bit occurs, and to $2^k$ otherwise. It compares an explicitly expanded list of orbit signs with the compressed result. It also checks the unequal-weight cancellation and observable counterexamples. The physical transfer-matrix decomposition, rational normalizers and Hubbard determinant identities have handwritten proofs and executable evidence; the local verification receipt states precisely which Lean declarations were compiled.

## Section 12: Current Claim Boundary

**Withdrawal in place, 2026-09-22.** The earlier “narrowest defensible claim” generalized GIN repair to non-abelian gauge theories, anomalies, higher categorical doubles and fracton systems from finite fixtures. That generalization is withdrawn. Likewise a commutator condition $[H,\Xi]=0$, overlap of weight supports, or zero cochain curvature alone does not establish a sign-reversing, observable-preserving configuration involution.

The supported extension consists of explicit equivalence-class representatives, finite rational cancellation certificates, a meron transfer reconstruction, and protected Hubbard determinant identities. A finite sign-free representation does not establish an efficient sampler. The remaining questions are the construction cost in physical input size, observable preservation, Markov-chain mixing, controlled time-step limits, and unprotected interacting Hubbard regimes. No continuum or generic polynomial-time FSP solution is claimed. AuthorityEffect: None.

## Section 13: Normal Forms with Specified Equivalence Relations

### 13.1 What must be proved

A normalizer on a declared domain $D$ and equivalence relation $\sim$ is a map $N:D\to D$ satisfying
\[
N(x)\sim x,\qquad N(N(x))=N(x),\qquad
N(x)=N(y)\Longleftrightarrow x\sim y.
\]
The last law is completeness **for that relation**, not for all physical representations. A deterministic verdict, a contract schema, a small optimization residual, and a list of database functional dependencies do not establish these laws. Fixed vertex labels, coordinate order, coefficient field and admissible transformations form part of the input specification.

### 13.2 Rational cochain quotient representative

Let $d_0\in\mathbb Q^{m\times n}$ and $W=\operatorname{im}d_0$. Set $x\sim y$ iff $x-y\in W$. Compute the nonzero reduced-row-echelon rows $r_1,\ldots,r_s$ of $d_0^T$, with pivot columns $p_1,\ldots,p_s$, and define
\[
N_W(x)=x-\sum_{i=1}^{s}x_{p_i}r_i.
\]
**Proof of the three laws.** The subtracted vector is in $W$, establishing soundness. Every pivot coordinate of $N_W(x)$ is zero since $(r_i)_{p_j}=\delta_{ij}$; applying $N_W$ again changes nothing. Every $w\in W$ has the unique expansion $\sum_iw_{p_i}r_i$, hence $N_W(w)=0$. It follows that $x-y\in W$ implies equal representatives. Conversely equal representatives imply $x-y$ is a difference of the subtracted vectors, hence lies in $W$. This also shows that changing a generating matrix without changing its column span leaves the normalizer unchanged. RREF arithmetic is exact rational arithmetic.

The section $N_W$ is generally **not an $L^1$ minimizer**. For $W=\operatorname{span}(1,2)$ and $x=(1,0)$ it returns $(0,-2)$, with norm 2, although $x$ itself has norm 1 and is optimal. The quotient norm is a separate linear-program value. The implementation uses guarded exact finite vertex enumeration for that value and explicitly refuses inputs beyond its declared work bound. Budget exhaustion is not a positive residual certificate.

### 13.3 Signed configuration graphs

For a finite labelled graph, let $\epsilon\in\mathbb F_2^E$ record negative off-diagonal transfer signs. The admissible equivalence is
<!-- markdownlint-disable MD049 -->
\[
\epsilon\sim\epsilon'\quad\Longleftrightarrow\quad
\epsilon'_{uv}=\epsilon_{uv}+g_u+g_v
\quad\text{for some }g\in\mathbb F_2^V.
\]
<!-- markdownlint-enable MD049 -->
Choose a deterministic rooted spanning forest from the fixed labels. Set each root potential to zero, propagate $g$ by tree-path parity, and output $N(\epsilon)=\epsilon+\delta g$. Forest edges become zero; chord values are the fundamental-cycle parities.

**Proof.** The returned $g$ establishes soundness. A second pass propagates zero potentials, giving idempotence. Gauge changes telescope around every cycle. Equal fundamental-cycle parities therefore give equal representatives, and equality of representatives expresses the original difference as a coboundary. These are precisely the three normal-form laws. A nonzero chord supplies an odd sign-parity cycle obstruction to this gauge class. Parallel edges and disconnected components must retain their declared identity; graph isomorphism and general orbital unitary transformations are different equivalence relations.

The [normal-form audit](docs/normal_form_audit.md) classifies the historical contracts and records executable laws and counterexamples. A zero rational cochain residual does not bound the average sign of an unrelated signed dataset. The $\mathbb Q$ and $\mathbb F_2$ constructions must not be identified without a model-specific map preserving their different operations.

## Section 14: The Earliest Hamiltonian Bridge and the Origin of a Sign

The pinned source investigation is detailed in [Hamiltonian origin](docs/hamiltonian_origin.md). At `sealed-derivation-v1` (`3100c4e`), alternating boundary signs are admitted and double-boundary cancellation is established. A finite Hodge operator $B_k^\dagger B_k+B_{k+1}B_{k+1}^\dagger$ becomes available after adding complex inner-product spaces and adjoints. Its physical interpretation remains an additional choice.

The more direct hopping construction occurs in post-seal research, pinned separately to `30805c5c6598310a4b6cef76e800a9015c9ef56a`: `research/natural_sections/lean/NaturalSections/HopFixture.lean` and `research/exchange_coefficients/lean/ExchangeCoefficients.lean`. The first supplies two-occupant exchange loops; the second compares their coefficients with explicitly admitted CAR removal/insertion conventions. Neither selects dynamics or a general many-occupant physical theory.

Supply symmetric positive edge magnitudes $a_{xy}$, symmetric parities $\epsilon_{xy}=\epsilon_{yx}$, real diagonal energies $V_x$, and an orthonormal configuration basis. The conditional construction
\[
H_{xx}=V_x,\qquad H_{xy}=-a_{xy}(-1)^{\epsilon_{xy}}
\]
is self-adjoint. For $\beta\ge0$, with $E_*\ge\max V_x$ and $K=E_*I-H$,
\[
Z=e^{-\beta E_*}\sum_{m\ge0}\frac{\beta^m}{m!}
\sum_{x_m=x_0}\prod_{j<m}K_{x_{j+1},x_j}.
\]
This follows by the absolutely convergent finite-matrix exponential series. Every nonzero closed hopping term has sign $(-1)^{\sum\epsilon}$. Thus an odd exchange loop becomes a negative statistical weight only after transition magnitudes and a thermal representation have been supplied. The final thermal trace remains positive. The normal-form theorem in Section 13 says exactly when vertex signs remove the negative hopping entries.

A three-leaf star already distinguishes site geometry from configuration geometry. The physical site graph $G = \{0, 1, 2, 3\}$ with edges $\{0,1\}, \{0,2\}, \{0,3\}$ is connected, acyclic, and bipartite, having cycle rank $|E| - |V| + 1 = 3 - 4 + 1 = 0$. In particular, the physical interaction graph contains zero cycles.

However, in the antisymmetric two-particle occupation basis, the six-step sequence
\[
\{1,2\}\to\{0,2\}\to\{2,3\}\to\{0,3\}
\to\{1,3\}\to\{0,1\}\to\{1,2\}
\]
uses the six directed transitions:
\[
1\to0, \quad 0\to3, \quad 2\to0, \quad 0\to1, \quad 3\to0, \quad 0\to2.
\]
In the canonical increasing occupation ordering $|i,j\rangle = c_i^\dagger c_j^\dagger |0\rangle$ ($i < j$), the CAR signs for these elementary hops evaluate to $+1, -1, +1, +1, -1, -1$. Their product is:
\[
(+1)(-1)(+1)(+1)(-1)(-1) = -1 \quad (\text{holonomy around the configuration cycle } \operatorname{Hol}_{\mathrm{FS}}(C) = -1).
\]
After one complete traversal, the particle occupations return to their initial state, but the antisymmetric representation acquires a minus sign. Therefore, “bipartite” and even “acyclic” at the physical site level do not ensure sign removal on configuration space.

This distinction is central when connecting fermionic signs to locality and quantum computational complexity:
> *There is a precise connection, and Lieb–Robinson gives it a promising quantitative extension: which distinctions can a local system detect, preserve, or repair within a specified time? That can support conditional statements about quantum computing’s viability and how to establish it. The papers do not yet justify a general verdict.*

Specifically, Lieb–Robinson bounds govern information propagation on the *physical interaction geometry* (the site graph), whereas the sign obstruction resides on the *many-body configuration-space geometry*. Because the mapping from physical sites to antisymmetric configuration space is non-local in tensor factors, physical Lieb–Robinson locality does not automatically imply locality or positive holonomy in the configuration carrier. Connecting those two carriers—and proving whether a declared representation and transformation family removes signs while preserving the requested physical observables—remains the formal mathematical requirement. SQL witnesses below check the corresponding obstruction with an additional down-spin particle and nonzero Hubbard interaction.

## Section 15: Model-Derived Meron Cancellation in SQL

### 15.1 Local transfer identity and exact arithmetic

Use the spinless nearest-neighbor bond Hamiltonian
\[
h_{ij}=-\frac t2(c_i^\dagger c_j+c_j^\dagger c_i)
       +U(n_i-\tfrac12)(n_j-\tfrac12),\qquad U=t>0.
\]
After dividing $e^{-\varepsilon h_{ij}}$ by its positive scalar $e^{-\varepsilon t/4}$, the $00,11$ diagonal weights are 1 and the one-particle block has diagonal $(q+1)/2$ and hopping magnitude $(q-1)/2$, where $q=e^{\varepsilon t}\ge1$. This follows by diagonalizing its $2\times2$ block. Jordan–Wigner signs accompany hops in the chosen occupation ordering. The two nonnegative local breakup weights are therefore $1$ and $(q-1)/2$. Choosing rational $q$ makes this normalized transfer identity exact; $\varepsilon t=\log q$ is a real parameter identification, not a rational approximation to the exponential.

On an even periodic chain, the implementation joins these plaquette breakups into spacetime clusters using a recursive SQL connected-component query. It reconstructs occupations for each cluster orientation and evaluates signs from the CAR hopping rule. It checks that each orbit has $2^k$ distinct orientations, common magnitude, and the admitted independent sign character. The independent oracle multiplies local occupation-basis transfer matrices without using the cluster decomposition.

The method follows the restricted meron construction of [Chandrasekharan–Wiese](https://arxiv.org/abs/cond-mat/9902128). It is not asserted for arbitrary Hubbard couplings. SQL implements graph joins, orientations and orbit grouping; registered rational scalar operations and a GCD-reduced rational aggregate provide arbitrary-precision arithmetic. This is executable SQLite with disclosed arithmetic extensions, not portable unextended ANSI SQL.

### 15.2 Orbit theorem and observable preservation

Write an orbit as $f\in\mathbb F_2^k$, with common magnitude $W_g$ and sign
\(\sigma_g(f)=\sigma_g(0)(-1)^{m_g\cdot f}\).
Then
\[
\sum_fW_g\sigma_g(f)
=W_g\sigma_g(0)\prod_{j=1}^k(1+(-1)^{m_{gj}})
=\begin{cases}2^kW_g\sigma_g(0)&m_g=0,\\0&m_g\ne0.\end{cases}
\]
Distributivity gives the product identity; one negative-character factor annihilates the product. A nonnegative partition representation additionally requires $\sigma_g(0)=+1$ on every zero-meron orbit of nonzero magnitude. `MeronCharacter.lean` checks the finite sign-list identity for arbitrary $k$. The SQL experiment verifies the physical decomposition's hypotheses rather than assuming the meron flag from its name.

For an observable $A_g(f)$ define its Boolean Fourier coefficient
\[
\widehat A_g(m)=2^{-k}\sum_f A_g(f)(-1)^{m\cdot f}.
\]
The exact numerator is $2^kW_g\sigma_g(0)\widehat A_g(m_g)$. Hence retaining only zero-meron orbits is justified for the partition function but can destroy an observable. If $A_g$ has Fourier degree at most $d$, only orbits with at most $d$ merons contribute to its numerator. In particular the squared sum of signed cluster occupations has degree at most two and admits an estimator using zero- and two-meron sectors. This is an observable-preservation theorem under the stated flip coordinates; it does not infer the observable's degree from a model label.

### 15.3 Exact finite result

For four sites, two repetitions of the even/odd bond schedule and $q=3$, SQL generates 256 breakup graphs and 1,296 oriented configurations, including 192 negative contributions. The normalized partition sum is 912, the absolute sum is 1,296, and the original average sign is $19/27$. The nonnegative zero-meron reduction and independent transfer-matrix trace both equal 912. The omitted global scalar is $(e^{-\varepsilon t/4})^{P}$ for $P$ local plaquettes.

For the implemented squared staggered spacetime occupancy, the raw numerator and the zero-/two-meron improved numerator both equal 36,864, giving $768/19$. The observable omits conventional time-integration normalization factors, as recorded in the code. This is a finite exact reconstruction, including a nonconstant observable. Enumerating all breakups remains exponential. The algebraic orbit compression is efficient once its factorization is supplied; this implementation supplies no general mixing-time theorem for sampling the surviving graphs.

### 15.4 Six-site census and a three-point chain note

For six sites ($L = 6$, two repetitions, $q = 3$), the companion meron package records 4,096 breakup graphs, 33,396 configurations, 192 configurations with sign $-1$ and positive weight, and 4,024 graphs whose meron count is 0, so 72 graphs have a positive meron count. The signed partition is $Z = 33{,}012$, matching the occupation transfer trace. That census is the companion's recorded run, not a new measurement in this monograph. The multi-stage wire trace for the four-site host remains in the companion's Section 6.4.

The same companion bridge records $Z(4) = 912$, $Z(6) = 33{,}012$, and $Z(8) = 973{,}824$ for repetitions $2$ and $q = 3$. The log-densities are not monotone in $L$. A three-point Neville extrapolation on $L \in \{4, 6, 8\}$ has a midpoint that agrees with $1.69411$ through four digits, and the $L = 4$ log-density width is below $10^{-18}$. This is not a theorem for every larger chain, and it does not include $L = 12$.

## Section 16: Hubbard Determinants, Protected Cases and Negative Witnesses

### 16.1 The represented Hamiltonian and time slice

Consider real spin-independent hopping on a declared graph and the centered Hubbard Hamiltonian
\[
H=-t\sum_{\{i,j\},s}(c_{is}^\dagger c_{js}+c_{js}^\dagger c_{is})
+U\sum_i(n_{i\uparrow}-\tfrac12)(n_{i\downarrow}-\tfrac12)
-\mu\sum_i(n_{i\uparrow}+n_{i\downarrow}).
\]
Here $\mu=0$ denotes the particle-hole symmetric value; in the uncentered convention the corresponding chemical potential is $U/2$.

The exact finite-slice model uses palindromic products of bond exponentials. Each half-bond matrix has entries $\cosh a=(r+r^{-1})/2$, $\sinh a=(r-r^{-1})/2$, with $r=e^{\Delta\tau t/2}>0$. A forward sweep followed by its reverse is a symmetric kinetic matrix $T$ with determinant one. Rational $r$ gives exact rational entries. This is a bond-split approximation to the full thermal exponential when bonds do not commute; finite-slice exactness does not assert zero Trotter error.

For $U>0$, the discrete Hubbard–Stratonovich identity uses
\[
e^{-\Delta\tau U(n_\uparrow-1/2)(n_\downarrow-1/2)}
=C\sum_{s=\pm1}e^{\lambda s(n_\uparrow-n_\downarrow)},\quad
\cosh\lambda=e^{\Delta\tau U/2},\quad C=e^{-\Delta\tau U/4}/2.
\]
Let $h=e^\lambda>0$, $z=e^{\Delta\tau\mu}>0$, and $D_\ell=\operatorname{diag}(h^{s_{i\ell}})$. The slice matrices are $B_{\ell\uparrow}=zTD_\ell$ and $B_{\ell\downarrow}=zTD_\ell^{-1}$. For $P_s=B_{Ls}\cdots B_{1s}$ the field weight, apart from the global positive $C^{NL}$, is
\(w(s)=\det(I+P_\uparrow)\det(I+P_\downarrow)\).
The identity $\operatorname{Tr}_{\mathcal F}\Gamma(P)=\det(I+P)$ follows by summing all principal minors, one for each occupation subset. An independent full-Fock reconstruction checks that the resulting field sum represents the declared transfer product.

### 16.2 Repulsive half-filled bipartite positivity

Let $\eta$ be the diagonal sublattice sign matrix. A bond connects opposite sublattices, so conjugation by $\eta$ inverts each bond exponential. Palindromic ordering gives $\eta T\eta=T^{-1}=T^{-T}$. At $z=1$,
\[
B_{\ell\downarrow}=\eta B_{\ell\uparrow}^{-T}\eta,
\qquad P_\downarrow=\eta P_\uparrow^{-T}\eta.
\]
The second identity preserves slice order: inverse transpose reverses multiplication order twice. Therefore
\[
\det(I+P_\downarrow)=\frac{\det(I+P_\uparrow)}{\det P_\uparrow},
\qquad w(s)=\frac{\det(I+P_\uparrow)^2}{\det P_\uparrow}\ge0,
\]
because $\det P_\uparrow>0$. A zero determinant $\det(I+P_\uparrow)$ produces zero weight; the denominator $\det P_\uparrow$ remains strictly positive. This proof applies to every field configuration under the stated hypotheses, not just the enumerated sample. It eliminates determinant signs, not the need to analyze sampling cost. See the standard positivity framework of [Wu–Zhang](https://arxiv.org/abs/cond-mat/0407272).

For $U<0$, a charge-channel decomposition gives identical real spin matrices at any shared chemical potential. The field weight is a determinant square multiplied by the positive, **field-dependent** factor $h^{-\sum_{i\ell}s_{i\ell}}$. That factor is included in the implementation; dropping it would preserve positivity but change the partition sum. Spin imbalance or complex spin-dependent hopping requires a separate argument.

### 16.3 SQL results and the boundary of the protection

SQL performs matrix products by joins and exact rational aggregation, and computes determinants by a recursive permutation expansion with inversion parity. The determinant is not supplied by a floating-point routine or determinant UDF. This simple determinant evaluator costs $N!$ terms; it is an audit implementation, not a competitive DQMC engine.

| Experiment | Exact evidence | Scope |
|---|---|---|
| Repulsive four-site ring, two slices, $r=3/2,h=2,z=1$ | All 256 fields have nonnegative weight; particle-hole determinant relation verified | Protected finite-slice representation |
| Attractive three-site triangle, two slices, $r=3/2,h=2,z=3/2$ | All 64 fields have nonnegative weight; field-dependent scalar retained | Identical-spin determinant-square protection |
| Two-site HS reconstruction at $z=3/2$ | Repulsive trace $172283601361/21233664$; attractive trace $180365586961/21233664$, each equal to its independently built full-Fock trace | The actual transfer sum is preserved |
| Repulsive doped four-site ring, four slices, $r=2,h=8,z=2$, field mask 15721 | Up determinant positive, down determinant negative in exact rational arithmetic | Explicit negative field; no full-ensemble average-sign claim |
| Repulsive frustrated triangle, four slices, $r=2,h=8,z=1$, field mask 1281 | Exact negative determinant product at the centered chemical potential | Bipartite protection unavailable |
| Interacting four-site star, $N_\uparrow=2,N_\downarrow=1,U=4$ | SQL returns a six-hop negative configuration cycle | Site-tree structure does not imply occupation-basis sign freedom |

All parameters, large rational witness values, field coverage and reconstruction checks are saved in [the exact model receipt](code/sign_sql/exact_models_receipt.json); [the SQL derivation](docs/sql_meron_hubbard.md) specifies the replay command and encoding. A single selected negative field is an existence witness. Its sign is not the average sign of the entire model. Conversely positive weights on a finite tested subset are not a theorem outside the symmetry hypotheses. The complete research manuscript, claim ledger, and automated reproducibility tests for this model are packaged in the standalone companion deposit: [`hubbard_sign_problem/`](hubbard_sign_problem/paper.md) (*Exact Relational Mechanics and Certified Sign Boundaries of the Fermi-Hubbard Model*).

### 16.4 A Hubbard observable without singular determinant division

For $L$ slices and a common fugacity $z$, each one-spin propagation matrix has the form $P_s(z)=z^L P_s(1)$. Differentiate the SQL determinant permutation fold in the ring of dual numbers, propagating the logarithmic derivative with each rational term. The product rule computes the derivative of the full field weight without an inverse matrix or division by $\det(I+P_s)$. It therefore retains contributions from zero determinants with nonzero derivatives. Because the Hubbard Hamiltonian conserves number,
\[
\langle N\rangle=\frac{1}{LZ}\frac{\partial Z}{\partial\log z}.
\]
The omitted global HS scalar is independent of $z$ and cancels in this ratio. The same identity follows from inserting the number operator into the full-Fock trace, providing an independent oracle. The protected four-site ring gives exactly 4. The two-site repulsive and attractive expectations are respectively $412347680162/172283601361$ and $452633269922/180365586961$, each matching the independent Fock-number trace. These are total particle numbers; density additionally divides by site count.

## Section 17: What Has Been Extended and What Is Still Open

The normal forms now have explicit domains, witness maps, equivalence relations and laws. The meron lane removes signs from a Hamiltonian-derived transfer representation and preserves both a partition sum and a nonconstant observable. The Hubbard lane connects the standard protected determinant identities to exact SQL calculations, checks the HS-to-Fock reconstruction, and exhibits negative fields when those protections fail. The source investigation identifies the signed hopping interface at which one can first add an actual many-body Hamiltonian, while keeping that addition separate from the sealed derivation. Together with the companion packages [`meron_sign_problem/`](meron_sign_problem/paper.md) and [`hubbard_sign_problem/`](hubbard_sign_problem/paper.md), this establishes an exact, multi-model benchmark suite for fermionic sign research.

### 17.1 Foliated Fracton Order, 1D Hinge Lineons, and Higher-Form 2-Gauge Defect Commutators

In three-dimensional foliated lattice architectures with spatial foliation planes $\Sigma_{xy}, \Sigma_{yz}, \Sigma_{zx}$, excitations exhibit directional mobility constraints: immobile 0D fractons, 2D planar planons, and 1D lineons mobile strictly along intersection hinges $\mathcal{H}_{ij} = \Sigma_i \cap \Sigma_j$.

Under declared discrete line lattice assumptions:
1. **Collision-Free 1D Ordering**: Two lineons on a discrete 1D hinge line with initial ordering $x_1(0) < x_2(0)$ satisfy $x_1(t) < x_2(t)$ at all steps under collision-avoiding discrete hops (`lean4/FoliatedFracton2Gauge.lean::hinge_path_preserves_relative_order`). By the discrete Intermediate Value Theorem, exchanging positions requires passing through an identical site or edge crossing (`hinge_lineon_exchange_collision_obstruction`). Consequently, collision-free worldlines on isolated hinges carry trivial permutation parity $(-1)^{\operatorname{sgn}(\sigma)} = +1$.
2. **Intersecting Hinge Commutator Curvature**: At the intersection of orthogonal 2-gauge defect sheets, non-abelian gauge holonomies $M_{\text{hinge}} = B_{xy} B_{yz} B_{xy}^{-1} B_{yz}^{-1}$ produce negative trace $\operatorname{Tr}(M) = -2 < 0$, uncancelled defect mass $\Phi_1 = 2 > 0$, and curvature $\Gamma_2 = \pi$ (`nonabelian_hinge_commutator_curvature_obstruction`).
3. **Foliated Categorical Projection**: Decoupled straight lineon sheets restore non-negative trace under foliated quantum double projection $\operatorname{Tr}(M_{\text{fol}}) = |\operatorname{Tr}(M)|^2 \ge 0$ (`decoupled_foliated_lineon_sign_free`), whereas corner lineon turns obstruct factorization and leave an uncancelled sign defect.
4. **Multi-Hinge Y-Junction Exchange vs. Hinge-Axis Conservation**: On a 3-prong multi-hinge Y-junction (`YJunctionVertex`) where three 1D hinges meet at a corner vertex and branch-hopping across the junction is permitted, two defects starting at `(branchX, branchY)` admit an explicit 6-step collision-free exchange trajectory to `(branchY, branchX)` via `branchZ` (`y_junction_collision_free_exchange_exists`), inducing a negative worldline permutation sign $-1 < 0$ (`y_junction_exchange_induces_negative_sign`). Conversely, when strict foliated dipole conservation preserves each lineon's 1D hinge-axis label (`AxisConservingPath`), cross-branch exchange between distinct hinge axes is impossible (`foliated_lineon_axis_conservation_forbids_branch_exchange`).

These results establish that sub-dimensional lineon confinement eliminates spatial braid permutations on isolated hinges, while isolating the precise non-abelian curvature obstruction at intersecting sheets.

Three next derivations are concrete. First, replace exhaustive field and breakup enumeration with a sampler whose observable estimator, ergodicity and mixing behavior are measured on growing systems. Second, retain rational local transfer parameters while proving a controlled approach to fixed physical $(\beta,t,U,\mu)$ as the time step shrinks. Third, search for additional meron or antiunitary structures for the unprotected Hubbard inputs, returning either an observable-preserving representation identity or a witness that rules out the specifically searched transformation class. The existing negative examples do not rule out all representations, and SQL query syntax alone supplies no complexity shortcut.
