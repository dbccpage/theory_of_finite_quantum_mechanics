# Gaps and Research Effort — Master Table

**Scope:** Master inventory of open research problems, continuum interfaces, and formalization targets across the `finite_quantum_mechanics` estate.  
**Target:** `qm_gaps_and_effort.md`  
**Updated:** 2026-10-11  

---

## 1. Classification Framework

Research items in the gap register (`claims/gap_register.yaml`) are categorized according to their mathematical domain and implementation characteristics:

| Classification | Meaning |
| :--- | :--- |
| **Continuum Interface** | Functional-analytic interface connecting finite algebraic carriers to continuous or infinite-dimensional formulations (CCR, continuous time, transcendental entropy, continuous field equations). |
| **Open Algebraic Question** | Mathematical theorem, counterexample, or representation problem formulated on declared finite or algebraic carriers. |
| **Verification & Formalization** | Bounded mechanization, proof replay, algorithm implementation, or test verification task. |
| **Open Research Problem** | Fundamental problem shared with the broader quantum information and mathematical physics community (e.g. fourth MUB in dimension 6). |

---

## 2. Master Gap Inventory

### A. Continuum and Asymptotic Interfaces

These items delineate the boundaries and asymptotic scaling limits connecting discrete algebraic carriers to continuous quantum mechanics:

| ID | Title | Domain | Mathematical Boundary & Interface | Relevant Skills & Theory |
| :--- | :--- | :--- | :--- | :--- |
| `GAP-F001-S000-002` | Continuum Hilbert lift & CCR | Operator Algebras | $\operatorname{Tr}([X, P]) = 0$ in finite dimensions vs $[X, P] = i\hbar I$; represented by discrete Weyl-Heisenberg groups over $\mathbb{Q}(\zeta_d)$ converging to CCR in the large-$d$ limit. | Functional analysis, unbounded operators, representation theory |
| `GAP-F001-S000-008` | Continuous time & Stone's theorem | Dynamics | Continuous unitary flow $U(t) = \exp(-iHt)$ requires Stone's theorem and continuous real time; discrete steps $U^n$ interface via branch-cut logarithms. | Spectral theory, strongly continuous groups, Lie algebras |
| `GAP-F001-S000-011` | Everett branch counting beyond $\mathbb{Q}$ | Measurement Theory | Equal-weight branch fine-graining reproduces rational Born weights; weights in $\mathbb{Q}(\zeta_n)^+ \setminus \mathbb{Q}$ require infinite trees or asymptotic limits. | Algebraic number theory, asymptotic probability |
| `GAP-FQM-023` | Transcendental von Neumann entropy | Information Theory | $S(\rho) = -\operatorname{Tr}(\rho \ln \rho)$ is transcendental over $\mathbb{Q}(\zeta_n)$ for mixed states by Baker's theorem; tracked algebraically via $P_m = \operatorname{Tr}(\rho^m)$ or enclosed via rational intervals $[a, b] \subset \mathbb{Q}$. | Transcendental number theory (Baker), certified interval arithmetic |
| `GAP-F001-S000-005` (Continuity) | Continuous $U(1)$ phase group | Group Theory | Continuous $S^1$ topology and one-parameter Lie group structure; realized discretely via roots of unity $\mu_n \subset U(1)$ and Gaussian unit lattices $\mathbb{Z}[i]$. | Lie groups, topological groups, Pontryagin duality |
| `NEW-CQA-CQC-MIPSTAR` | Commuting vs tensor correlations | Quantum Complexity | Commuting-operator strategies in $C_{qc}$ require infinite-dimensional $C^*$-algebras; general value undecidable (MIP\* = RE). | Operator algebras, $C^*$-tensor products, nonlocality |
| `NEW-QM-CHANNELS-033` | Continuous Schrödinger equation | Dynamics | Continuous differential equation $i\hbar \partial \psi / \partial t = H\psi$ in $L^2(\mathbb{R}^3)$ as the scaling limit of discrete cochain transport networks. | Partial differential equations, graph limits |
| `NEW-QM-CHANNELS-050` | Continuum Dirac equation | Field Theory | Continuous Dirac spinor fields on Minkowski spacetime requiring continuous Lorentz group $SO(1,3)$. | Relativistic quantum mechanics, Clifford bundles |

---

### B. Open Algebraic and Discrete Questions on Declared Carriers

These items constitute solvable mathematical and computational questions formulated on declared algebraic number fields or discrete graphs:

| ID | Title | Domain | Research Objective | Estimated Complexity | Primary Evidence / Source |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `GAP-F001-S000-004` | Gleason uniqueness on dense cyclotomic spheres | Foundations | Determine whether noncontextual frame additivity on dense cyclotomic spheres $\mathcal{S}(\mathbb{Q}(\zeta_n)^d)$ for $d \ge 3$ forces quadratic Born measures. | Advanced Research | `GleasonTheorem.lean`, `H054`, `gleason_cyclotomic.py` |
| `GAP-F001-S000-010` | Gleason dimension separation | Foundations | Formulate and prove typed Gleason uniqueness on declared cyclotomic carriers in Lean 4, separating $d = 2$ from $d \ge 3$. | Advanced Research | `HilbertWalkGleason.lean`, `HilbertWalkSameContract.lean` |
| `NEW-H058-BUSCH` | Busch effect-frame representation | Foundations | Establish full algebraic representation for additive effect frame functions on POVMs across declared cyclotomic carriers $d = 2, 3$. | Moderate | `EffectFrameBusch.lean`, `use_cases/busch_effects.py` |
| `GAP-F001-S000-012` | Ordered real embedding | Number Theory | Formalize declared real embedding $\iota: \mathbb{Q}(\zeta_n)^+ \hookrightarrow \mathbb{R}$ to resolve Galois-twist variance of mixed-state PSD. | Bounded / Standard | `EmbeddingRelativity.lean` |
| `GAP-F001-S000-006` | Hilbert tensor product uniqueness | Foundations | Characterize bilinear tensor product maps on $\mathbb{Q}(\zeta_n)^d$ under local unitary covariance and no-signalling axioms. | Moderate | `CompositionTensorMub.lean`, `c250_block05_composition.json` |
| `GAP-F001-S000-007` | CPTP Choi representation | Quantum Channels | Formalize Choi-Jamiolkowski representation and positive maps over declared cyclotomic matrix algebras $M_d(\mathbb{Q}(\zeta_n))$. | Moderate | `CptpChannelsStinespring.lean`, `cptp_channels_stinespring.py` |
| `GAP-F001-S000-001` | Exact duality gap certificates | Optimization | Implement exact primal/dual linear programming certificates for cochain boundary operators $\Phi_1$ over $\mathbb{Q}$. | Moderate | `DualWitness.lean`, `cochain.py` |
| `GAP-F001-S000-005` (Algebraic) | Discrete $U(1)$ selector / $J$-algebra | Algebra | Formalize discrete complex carrier selection and Gaussian integer $J$-algebras in Lean 4. | Moderate | `research/028_...`, `research/062_...` |
| `GAP-C1000-006` | CHSH cyclotomic field supremum | Nonlocality | Determine exact supremum of CHSH correlation over unit vectors in cyclotomic fields $\mathbb{Q}(\zeta_n)^2$ without height bounds. | Advanced Research | `QuantumCorrelation.lean`, `DiscretePythagoreanBellChsh.lean` |
| `GAP-C1000-007` | Contextuality cohomology | Cohomology | Extend contextuality obstruction cohomology calculations from $\mathbb{Z}_2$ to integer and cyclotomic coefficients. | Moderate | `ContextualityObstruction.lean`, `c1000_block07` |
| `GAP-C1000-008` | Commuting observables | Poset Theory | Formulate $k$-colorability criteria of comparability graphs for commuting observable bundles ($k > 2$). | Bounded | `commuting_observables.py` |
| `GAP-C500-B06` | Finite-lattice Trotter / LR bounds | Mathematical Physics | Establish certified finite-lattice Trotter error bounds and Lieb-Robinson velocities with exact rational enclosures. | Advanced Research | `ContinuousTimeLocalityLimit.lean`, `quantum_hamiltonian.rs` |
| `NEW-DENSITY-COHERENCE` | Off-diagonal density coherence | Quantum State Space | Characterize exact conditions forcing off-diagonal density entries from generalized cochain statistics. | Moderate | `research/012_...`, `FiniteDensity.lean` |
| `NEW-LUDERS-COHERENCE` | Operator Lüders update | Measurement Theory | Implement exact rational Lüders update $\rho \mapsto P\rho P / \operatorname{Tr}(P\rho)$ preserving within-sector coherence. | Moderate | `measure_and_update`, `research/021_...` |
| `NEW-MUB-D6-FOURTH` | Mutually Unbiased Bases ($d=6$) | Combinatorics | Existence of four mutually unbiased bases in dimension $d=6$. | Open Research Problem | `mub/`, `composition_tensor_mub.py` |

---

### C. Implementation, Formalization, and Verification Tasks

| ID | Title | Task Description | Target Environment |
| :--- | :--- | :--- | :--- |
| `GAP-FQM-019` | Lean 4 library consolidation | Restore and replay foundational quantum mechanics proofs under current Lean 4.34.0 toolchain. | `lean4/quantum_mechanics/` |
| `GAP-FQM-003` | Exact cochain algorithms | Implement four-way classifier and exact network simplex solvers over $\mathbb{Q}$ replacing floating-point LP routines. | `omega_solvers`, `omega_quantum_physics` |
| `NEW-PHASE-060-LEDGER` | Superposition non-descent | Integrate `MixingObstruction.no_descent_through_quotient` into main application library. | `lean4/quantum_mechanics/` |
| `GAP-FQM-017` | Dynamics claim mappings | Update and reconcile claim maps for discrete dynamics and unitary step operators. | `research/208_...` through `211_...` |
