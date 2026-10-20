# Comprehensive Technical Analysis: Top 5 Most Difficult Remaining Derivations in Finite Quantum Mechanics

**Author**: Project Orchestrator (`orchestrator_dag`)  
**Scope**: Derivation DAG Master Ledger (`dag/theory_of_finite_qm.jsonl`, `TFQ-0000`–`TFQ-0396`), `dag/derivation_dag.json`, and staged PFP operads (`dag/operads/`)  
**Claim Posture**: Strict Claim Discipline (`AuthorityEffect: None`, zero forbidden tokens)  
**Date**: 2026-10-20  

---

## Executive Summary & Frontier Landscape

Across the 397 derivation nodes in `dag/theory_of_finite_qm.jsonl`, 250 records represent closed finite algebraic controls, verified discrete shadows, and historical source records (`COMPUTATIONAL_CONTROL`, `SOURCE_RECORD`), while 147 records represent open obligations, theoretical bridges, and formal gaps (`OPEN_OBLIGATION`, `GAP`).

An empirical cross-audit of the DAG topology, mathematical obstruction theorems, and multi-tier repository witnesses establishes that the most difficult remaining derivations are not caused by coding or verification deficits, but by non-trivial structural, topological, and measure-theoretic divides between discrete/finite algebraic structures and continuum physical quantum theory.

Below is the technical ranking, obstruction breakdown, finite control analysis, and concrete multi-language attack plan for the next top 5 most difficult derivations remaining in the repository.

---

## 1. Rank 1: Gleason's Theorem & Born Rule Uniqueness from Discrete Partitions

### 1.1 Node & Stage Identity
- **Master Ledger Node**: `TFQ-0307` (`A03-029`)
- **Stage**: `FINITE_HILBERT` (Folder: `dag/derivations/09_finite_hilbert/`)
- **Status**: `GAP`
- **Associated Nodes**:
  - `TFQ-0306` (Born rule uniqueness imported as declared axiom)
  - `TFQ-0241` (Projection postulate imported as conditional measurement bridge)
  - `TFQ-0274` (Tier-3 QM uniqueness gap)
- **DAG Target IDs**:
  - `FQ-GAP-BORN-UNIQUENESS-GLEASON`
  - `L1-QM020-THM6-P2-GLEASON`
  - `DS-QM030-PROJECTION-POSTULATE-AND-BORN-PAIRING-IMPORT`
- **Operad Collections**: `dag/operads/fq_gap_born_uniqueness_gleason.yaml`, `dag/operads/qm020_born_rule_probabilistic_uniqueness.yaml`

### 1.2 Mathematical & Physical Bottleneck
Gleason's theorem in dimension $d \ge 3$ establishes that every finitely additive probability measure $\mu$ on the projection lattice $\mathcal{P}(\mathcal{H})$ of a separable Hilbert space is uniquely represented by a positive trace-class density operator $\rho$ with $\text{Tr}(\rho) = 1$, such that $\mu(P) = \text{Tr}(\rho P)$.

In finite discrete mechanics formulated over rational or algebraic number fields (such as $\mathbb{Q}$ or $\mathbb{Q}(i)$), Gleason's theorem fails unconditionally:
1. **Rational Sphere Discrepancy**: Over the rational unit sphere $S^2_\mathbb{Q}$, there exist non-continuous, non-linear frame functions and Kochen-Specker two-coloring functions $f: S^2_\mathbb{Q} \to \{0, 1\}$ that assign disjoint orthogonal triads sum 1 without admitting a bilinear quadratic extension.
2. **Topological Incompleteness**: Standard proofs of Gleason's theorem require the metric completeness and compactness of the continuous unit sphere $S^{n-1}$ to integrate frame functions against spherical harmonics and establish quadratic form continuity. Discrete combinatorial cochains provide no continuous integration measure.
3. **The Qubit ($d=2$) Failure**: In dimension $d=2$, Gleason's theorem fails even over $\mathbb{C}$: the projection lattice $\mathcal{P}(\mathbb{C}^2)$ contains non-interlocking orthogonal pairs, admitting uncountably many non-Bornian probability assignments unless extended to positive operator-valued measures (POVMs, Busch's theorem) or supplemented by external continuity postulates.

### 1.3 Why Current Finite/Algebraic Controls Fall Short
- **Python Controls** (`code/python/src/qm/campaigns/born_gleason.py`, `code/python/src/qm/textbook_problems.py` Q61/Q64):
  Verify the Cabello 18-ray 9-context finite graph obstruction and evaluate the falsification of quartic rivals ($I \propto |\psi|^4$) on discrete rotated $d=3$ triads. These controls verify that polynomial rivals of degree $\ne 2$ fail on specific test frames, but they do not establish that quadratic forms are the unique non-negative solutions over all possible partitions.
- **Rust Controls** (`code/rust/src/qm/campaigns/born_gleason.rs`, `code/rust/src/dag_witnesses.rs` Tranche 9):
  Execute exact rational matrix evaluations for finite projection families, certifying that specific 18-vector systems admit no non-contextual $\{0, 1\}$ valuations. This establishes contextuality on finite subgraphs, but leaves open whether an arbitrary measure on a dense rational lattice uniquely extends to the continuum Born trace.
- **Lean 4 Controls** (`lean4/GleasonRationalPlane.lean`, `lean4/H017Gleason.lean`):
  Formally mechanize the $d=2$ binary non-Bornian countermodel (`d2_binary_non_bornian_obstruction`), showing in this model that in $d=2$ discrete projection lattice additivity does not imply the Born rule.
- **Remaining Gap**: Establishing Born rule uniqueness requires either asserting continuous spherical completeness as an imported axiom or replacing projection lattices with convex operational effect algebras (POVMs).

### 1.4 Attack Plan
1. **Lean 4 Formalization**:
   Formalize Busch's theorem on effect algebras in `lean4/BuschEffectAlgebra.lean`: establish that any generalized probability measure on the effect algebra $\mathcal{E}(\mathcal{H}) = \{E : 0 \le E \le I\}$ for $d \ge 2$ is uniquely determined by a density operator $\rho$ without requiring $d \ge 3$, circumventing the 2D Gleason obstruction.
2. **Exact Rational Rust Certifier**:
   Construct an exact rational convex polytope solver in `code/rust/src/qm/campaigns/born_gleason.rs` that takes dense rational sphere configurations and certifies that the intersection of all finite Cabello-like rational sub-configurations forces the density-matrix state space to within $\epsilon$-rational bounds.
3. **Operad Binding**:
   Define and compose the operad presentation in `dag/operads/fq_gap_born_uniqueness_gleason.yaml` mapping effect algebra frames to convex density operators with exact rational coefficients.

---

## 2. Rank 2: Continuum Hilbert Space Limit & Path Integral Convergence

### 2.1 Node & Stage Identity
- **Master Ledger Node**: `TFQ-0085` (`A01-085`)
- **Stage**: `CONTINUUM_INTERFACE` (Folder: `dag/derivations/20_continuum_interface/`)
- **Status**: `GAP`
- **Associated Nodes**:
  - `TFQ-0114` (`GAP-F000-F002-001`, no limit object constructed)
  - `TFQ-0115` (`GAP-F002-LIMIT`, unbounded spectral divergence)
  - `TFQ-0073` (Continuum Hilbert lift)
  - `TFQ-0124` (Continuum limit gap)
- **DAG Target IDs**:
  - `FQ-GAP-CONTINUUM-HILBERT-LIFT`
  - `DS-R-CONTINUUM-LIMIT`
  - `DS-QM032-CONTINUUM-LIMIT-CONDITIONAL`
  - `DS-QM033-064-074-083-QHELD-CONTINUUM`
- **Operad Collections**: `dag/operads/fq_gap_continuum_hilbert_lift.yaml`, `dag/operads/ds_r_continuum_limit.yaml`

### 2.2 Mathematical & Physical Bottleneck
The foundational transition from finite combinatorial cochains $(C_0, C_1, C_2, d_0, d_1)$ to standard continuum quantum mechanics requires the construction of a limit functor:
$$\mathcal{L}: \mathbf{FinCochain} \longrightarrow \mathbf{Hilb}_\infty$$
mapping discrete finite-dimensional state spaces $\mathcal{H}_N = \ell^2(V_N)$ into an infinite-dimensional separable Hilbert space (such as $L^2(\mathbb{R}^n)$ or Fock space $\mathcal{F}$).

The mathematical obstructions include:
1. **Unbounded Operator Domain Convergence**: On discrete graphs, the discrete Laplacian $L = D - A$ and momentum operators are bounded. In the continuum limit $\Delta x \to 0$, $L / (\Delta x)^2 \to -\nabla^2$, which is an unbounded operator. Establishing strong resolvent convergence $R_\lambda(L_{\Delta x}) \to R_\lambda(-\nabla^2)$ requires Sobolev embedding theorems and uniform domain identification.
2. **Measure Equicontinuity & Path Sum Divergence**: The discrete path sum over graph trajectories $\sum_{\gamma} e^{i S[\gamma] / \hbar}$ lacks a uniform measure as the number of time slices $N \to \infty$. Constructing the continuum Feynman path integral or Wiener measure requires establishing tightness of the discrete transition measures and equicontinuity under mesh refinement.
3. **Absence of a Non-Perturbative Limit Object**: Currently, the repository contains no constructed limit object; `TFQ-0114` honestly records that the limit object remains unconstructed.

### 2.3 Why Current Finite/Algebraic Controls Fall Short
- **Python Controls** (`code/python/src/qm/campaigns/cochain_limit.py`, `code/python/src/qm/textbook_problems.py` Q58):
  Mechanize discrete Sturm-Liouville Dirichlet eigenvalues for finite $N=3$, evaluating the node sequence $[0, 1, 2]$ and confirming exact rational eigenvalues in $\mathbb{Q}(\sqrt{2})$. However, discrete matrix eigenvalues on finite grids do not establish functional convergence to continuous eigenfunctions $\sin(n\pi x)$.
- **Rust Controls** (`code/rust/src/qm/campaigns/continuum_lift.rs`):
  Certify that discrete Cayley transforms $U = (I - \frac{i \Delta t}{2} H)(I + \frac{i \Delta t}{2} H)^{-1}$ preserve the discrete $\ell^2$ norm exactly, whereas explicit forward-Euler methods diverge as $1 + \mathcal{O}(\Delta t^2)$. This confirms algebraic unitarity preservation for fixed $N$, but does not address the $N \to \infty$ completion.
- **Lean 4 Controls** (`lean4/DerivationDagQMClosure.lean::qm032_continuum_limit_conditional_witness`):
  Records conditional hypotheses with natural-number defect counters. In `ContinuumLimit.lean`, the statement asserts boundedness only by assuming boundedness as a hypothesis, documenting an unclosed gap rather than a derived convergence theorem.

### 2.4 Attack Plan
1. **Lean 4 Directed Inductive System**:
   Formalize a directed system of finite-dimensional Hilbert spaces $(\mathcal{H}_n, \iota_{n,m})$ with isometric embeddings $\iota_{n,m}: \mathcal{H}_n \hookrightarrow \mathcal{H}_m$ in `lean4/InductiveHilbertLimit.lean`, showing in this model that its metric completion is a separable Hilbert space isomorphic to $L^2([0, 1])$.
2. **Exact Rational Rust Operator Norm Certifier**:
   Implement in `code/rust/src/qm/campaigns/continuum_lift.rs` an algorithm certifying the strong resolvent convergence $\|(L_{\Delta x} - zI)^{-1} - (-\nabla^2 - zI)^{-1}\| \le C \Delta x$ over dyadic piecewise-constant basis functions.
3. **Python Operad Boundary**:
   Bind the operad collection `dag/operads/fq_gap_continuum_hilbert_lift.yaml` to formalize the grafting of finite Cayley unitaries into convergent Trotter-Kato product sequences.

---

## 3. Rank 3: Continuous-Time Dynamics & Stone's Theorem from Discrete Transitions

### 3.1 Node & Stage Identity
- **Master Ledger Node**: `TFQ-0246` (`A04-013`)
- **Stage**: `FINITE_QM_DYNAMICS` (Folder: `dag/derivations/11_finite_qm_dynamics/`)
- **Status**: `OPEN_OBLIGATION`
- **Associated Nodes**:
  - `TFQ-0245` (Unitary finite shadow reserved)
  - `TFQ-0008` (Finite dynamics, channels, Kraus representations)
  - `TFQ-0083` (Discrete-to-continuous dynamics bridge)
- **DAG Target IDs**:
  - `FQ-GAP-STONE-CONTINUOUS-TIME`
  - `FQ-DISCRETE-TIME-STONE-AMBIGUITY`
  - `DS-CONTINUOUS-TIME-EXP-GENERATOR`
- **Operad Collections**: `dag/operads/fq_gap_stone_continuous_time.yaml`, `dag/operads/fq_discrete_time_stone_ambiguity.yaml`

### 3.2 Mathematical & Physical Bottleneck
Stone's theorem on one-parameter unitary groups states that every strongly continuous one-parameter family of unitaries $U(t)$ ($t \in \mathbb{R}$) on a Hilbert space is uniquely generated by a self-adjoint operator $H$ via $U(t) = e^{-i H t}$.

In discrete mechanics, time evolution is provided by a discrete transition operator $U \in U(n, \mathbb{Q}(i))$ or a rational Cayley step $U_{\Delta t}$. The structural obstructions are:
1. **Multi-Valued Matrix Logarithm & Time Aliasing**:
   For any discrete unitary matrix $U$, the matrix logarithm is infinitely multi-valued:
   $$\ln U = -i H \Delta t + 2\pi i k I \quad (k \in \mathbb{Z})$$
   A single step $U$ does not determine $H$; energy eigenvalues $E$ are indistinguishable from $E + \frac{2\pi k}{\Delta t}$. Without a continuous parameter $t \in \mathbb{R}$ and strong continuity $\lim_{t \to 0} \|U(t)\psi - \psi\| = 0$, the Hamiltonian operator cannot be uniquely extracted.
2. **Absence of Half-Steps in Discrete Logics**:
   As proved in discrete dynamics, given a discrete unitary permutation or swap $U = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$, there exists no real involution square root in the discrete algebra without adjoining complex phases.
3. **Continuous One-Parameter Subgroup Embedding**:
   Embedding an arbitrary discrete unitary $U$ into a continuous 1-parameter subgroup $\{U(t)\}_{t \in \mathbb{R}}$ requires selecting a distinguished branch of the logarithm, which cannot be derived from combinatorial transitions alone.

### 3.3 Why Current Finite/Algebraic Controls Fall Short
- **Python Controls** (`code/python/src/qm/campaigns/discrete_dynamics.py`, `code/python/src/qm/textbook_problems.py` Q65):
  Evaluate discrete Poincaré recurrence and Heisenberg revival times for discrete Cayley evolutions, verifying that short-time transition probabilities match $4\tau^2$ without numerical drift. However, these checks compute discrete powers $U^m$, leaving the continuous generator $e^{-i H t}$ as an imported representation.
- **Rust Controls** (`code/rust/src/qm/campaigns/discrete_dynamics.rs`, `code/rust/src/finite_probability/dynamics_exact.rs`):
  Certify that discrete rational Cayley iterations preserve rational unitarity and compute exact commutator traces. They document that discrete rotations over $\mathbb{Q}(i)$ generate infinite cyclic subgroups without containing the continuous logarithm angle.
- **Lean 4 Controls** (`lean4/H055DiscreteDynamicsStone.lean`):
  Theorems `stone_discrete_generator_ambiguity` and `no_bool_half_step` formally establish that discrete time transitions admit multiple generator solutions and that boolean step logics cannot admit square roots without complex phase extensions.
- **Remaining Gap**: Establishing a unique physical Hamiltonian requires introducing an explicit spectral cutoff condition ($|E| < \frac{\pi}{\Delta t}$) or showing in this model that continuous time emerges as the projective limit of refined step dividers.

### 3.4 Attack Plan
1. **Lean 4 Rational Cayley-Padé Approximant**:
   Formalize in `lean4/RationalCayleyLogarithm.lean` the rational Padé approximation to $\ln U$, showing under the declared spectral window constraint $\|H\| < \frac{\pi}{\Delta t}$ that the principal branch logarithm is unique and rational.
2. **Rust Exact Branch Certifier**:
   Implement an exact rational branch selector in `code/rust/src/qm/campaigns/discrete_dynamics.rs` using Gershgorin circle bounds to certify that all spectrum eigenvalues lie strictly within the unaliased fundamental domain $(-\pi, \pi)$.
3. **Operad Generator**:
   Complete operad relation `OP-FINITE_QM_DYNAMICS-FQ-DISCRETE-TIME-STONE-AMBIGUITY` in `dag/operads/fq_discrete_time_stone_ambiguity.yaml` binding finite unitary step sequences to unaliased rational semigroup generators.

---

## 4. Rank 4: Emergence of Continuous $U(1)$ Unit Group & Complex Field $\mathbb{C}$ from Discrete Carrier

### 4.1 Node & Stage Identity
- **Master Ledger Node**: `TFQ-0294` (`A03-016`)
- **Stage**: `L1_TO_L2` (Folder: `dag/derivations/08_l1_to_l2/`)
- **Status**: `GAP`
- **Associated Nodes**:
  - `TFQ-0293` (Complex field as declared carrier; non-unit norm obstruction)
  - `TFQ-0055` (Missing square root in gauge cochains)
  - `TFQ-0253` (Conditional complex carrier selector)
- **DAG Target IDs**:
  - `FQ-GAP-U1-CIRCLE`
  - `L1-IMP-U1-PHASES`
  - `L1-IMP-COMPLEX-FIELD`
  - `DS-QM062-U1-SELECTOR-LAYERS`
- **Operad Collections**: `dag/operads/fq_gap_u1_circle.yaml`, `dag/operads/l1_imp_complex_field.yaml`

### 4.2 Mathematical & Physical Bottleneck
Starting from primitive pregenesis distinction $(<>, \text{Diff}, \text{Struct})$ over integer counts $\mathbb{Z}$, the field of complex numbers $\mathbb{C}$ and its unit circle $U(1) = \{z \in \mathbb{C} : |z| = 1\}$ are absent:
1. **No Integer Square Root of $-1$**: The equation $x^2 + 1 = 0$ has no integer solution in $\mathbb{Z}$.
2. **Incompleteness of $\mathbb{Q}(i)$ and Pythagorean Phases**: Adjoining an imaginary unit $i$ yields the Gaussian rationals $\mathbb{Q}(i)$. However, the unit group of $\mathbb{Q}(i)$ is the group of Pythagorean phases:
   $$\text{Unit}(\mathbb{Q}(i)) = \left\{ \frac{a + bi}{c} : a^2 + b^2 = c^2, \; a, b, c \in \mathbb{Z} \right\}$$
   The Pythagorean phase group is infinite, discrete, and non-divisible:
   - It has no algebraic square roots (e.g. the 8th root of unity $\zeta_8 = \frac{1+i}{\sqrt{2}}$ requires $\sqrt{2} \notin \mathbb{Q}(i)$).
   - It possesses no continuous invariant Haar measure.
   - It does not form a compact connected 1-manifold.
3. **Ad Hoc Import of Phase Symmetries**: Continuous phase invariance $\psi \mapsto e^{i\theta} \psi$ and gauge covariance cannot be derived from finite combinatorial cochains without asserting continuous field completion or importing $\mathbb{C}$ as an external postulate.

### 4.3 Why Current Finite/Algebraic Controls Fall Short
- **Python Controls** (`code/python/src/qm/campaigns/cancellations.py`, `code/python/src/qm/textbook_problems.py` Q64):
  Verify discrete Pancharatnam-Berry phases on discrete octant triangles using rational Pythagorean phases, evaluating $\tan \Phi = 1$ for the 3-vertex loop. These controls verify that discrete phases cancel algebraically on rational triangles, but they assume $\mathbb{Q}(i)$ as a given background.
- **Rust Controls** (`code/rust/src/qm/campaigns/cancellations.rs`):
  Mechanize the rational Cayley stereographic parameterization $t \mapsto \frac{1-t^2}{1+t^2} + i \frac{2t}{1+t^2}$ and demonstrate the half-angle algebraic defect (e.g., $a^2 - b^2 = 15, 2ab = 20$ has no integer solution in $\mathbb{Z}$).
- **Lean 4 Controls** (`lean4/H011Circle.lean`):
  Theorem `sign_excluded_circle_still_imported` shows in this model that binary sign distinctions $\{+1, -1\}$ do not generate $U(1)$ and that continuous phase rotations remain an imported assumption.
- **Remaining Gap**: Constructing a continuous $U(1)$ action from discrete distinctions requires establishing an exact cyclotomic direct limit $\varinjlim \mathbb{Q}(\zeta_{2^n})$ or asserting the continuum field $\mathbb{C}$ as a declared boundary condition.

### 4.4 Attack Plan
1. **Lean 4 Formalization of Cyclotomic Phase Tower**:
   In `lean4/CyclotomicPhaseTower.lean`, construct the direct limit $\mathbb{Q}(\zeta_{2^\infty}) = \bigcup_{n=1}^\infty \mathbb{Q}(\zeta_{2^n})$, formalizing exact dyadic phase subdivision and showing in this model that its group of units forms a dense subgroup of $U(1)$ with exact rational cyclotomic arithmetic.
2. **Exact Algebraic Rust Solver**:
   Implement an exact cyclotomic arithmetic package in `code/rust/src/qm/campaigns/cancellations.rs` supporting dyadic angle bisections and certifying destructive interference bounds without floating-point approximations.
3. **Operad Presentation**:
   Update `dag/operads/fq_gap_u1_circle.yaml` with generator `cayley_phase_graft` and relation `OP-FQ-CAYLEY-U1-PUNCTURED-CIRCLE` certifying that rational phase mixtures approximate continuous $U(1)$ within specified algebraic error bounds.

---

## 5. Rank 5: Simplicial Regge Curvature to Einstein Field Equations & Cosmological Constant $\Lambda$

### 5.1 Node & Stage Identity
- **Master Ledger Node**: `TFQ-0084` (`A01-084`)
- **Stage**: `FINITE_QG` (Folder: `dag/derivations/19_finite_qg/`)
- **Status**: `OPEN_OBLIGATION`
- **Associated Nodes**:
  - `TFQ-0090` (Regge deficit uncoupled from cochain curvature)
  - `TFQ-0096` (Einstein equation Q-held)
  - `TFQ-0110` (GAP on continuum limit, Einstein equation, physical $\Lambda$)
  - `TFQ-0108` (Caller-supplied $\Lambda$ is an arbitrary parameter, not physical $\Lambda$)
- **DAG Target IDs**:
  - `DS-QM110-111-LQG-GR-KINEMATICAL-SHADOWS`
  - `WDP-JOINT-CONTINUUM`
  - `WDP-JOINT-CONTINUUM-CONTROL`
- **Operad Collections**: `dag/operads/ds_qm110_111_lqg_gr_kinematical_shadows.yaml`

### 5.2 Mathematical & Physical Bottleneck
In discrete quantum gravity, spacetime is modeled as a 4-dimensional simplicial complex. The curvature on a 2-dimensional hinge (triangle) $h$ is given by the Regge deficit angle:
$$\epsilon_h = 2\pi - \sum_{\sigma \supset h} \theta_{h,\sigma}$$
where $\theta_{h,\sigma}$ is the dihedral angle of 4-simplex $\sigma$ at hinge $h$. The discrete Regge action is $S_{\text{Regge}} = \sum_h A_h \epsilon_h$.

The structural obstructions preventing a derived closure of the Einstein field equations are:
1. **Broken Diffeomorphism Invariance on Fixed Triangulations**: On a discrete triangulation, continuous general coordinate covariance is broken. Diffeomorphisms correspond to vertex displacements, but the discrete deficit angles do not transform as tensors; diffeomorphism constraints fail to close off-shell.
2. **Coupling Deficit to Cochain Gauge Curvature**: In finite quantum mechanics, gauge cochains satisfy $d_1 d_0 = 0$, but the metric Regge deficit $\epsilon_h$ is not the exterior derivative of a connection 1-form without introducing a discrete spin connection (Barbero-Immirzi parameter, Ashtekar-Barbero connection).
3. **The Cosmological Constant $\Lambda$ Obstruction**: In discrete formulations, the cosmological term $\Lambda \sum_\sigma V_\sigma$ does not emerge from microscopic cochains. `TFQ-0108` documents that $\Lambda$ is only a caller-supplied input float, not a derived physical value.

### 5.3 Why Current Finite/Algebraic Controls Fall Short
- **Python Controls** (`code/python/src/qm/campaigns/l1_regge.py`):
  Calculate dihedral angles and deficit angles using floating-point trigonometry on small toy triangulations (e.g. 5-cell 4-simplex or 16-cell). These numerical checks verify that flat Euclidean space has zero deficit, but cannot establish diffeomorphism closure or evaluate the non-perturbative continuum limit.
- **Rust Controls** (`code/rust/src/dag_witnesses.rs` Tranches 18 & 19):
  Execute discrete Regge deficit evaluations on fixed simplicial complexes, confirming that discrete deficits act as local curvature proxies on retained finite tables.
- **Lean 4 Controls** (`lean4/DerivationDagQMClosure.lean::qm110_111_lqg_gr_kinematical_witness`, `lean4/GR002.lean`):
  Formalize the kinematic shadow of loop quantum gravity and Regge geometry, but mark the dynamical Einstein field equations as Q-held (`qm110_111_lqg_gr_kinematical_witness`), explicitly showing in this model that kinematics does not imply dynamical field equations.
- **Remaining Gap**: Deriving the continuum Einstein equations $G_{\mu\nu} + \Lambda g_{\mu\nu} = 8\pi G T_{\mu\nu}$ requires a rigorous implementation of simplicial coarse-graining (barycentric subdivision) and showing that the Hamiltonian constraint converges to the Wheeler-DeWitt equation.

### 5.4 Attack Plan
1. **Lean 4 Exact Simplicial Variation**:
   In `lean4/ReggeVariationExact.lean`, formalize the exact variation of the discrete Regge action on a 4-simplex, establishing the discrete Regge equation $\sum_h \epsilon_h \frac{\partial A_h}{\partial l_e} = 0$ using exact algebraic field extensions over $\mathbb{Q}(\sqrt{2}, \sqrt{3}, \sqrt{5})$.
2. **Exact Algebraic Rust Certifier**:
   Replace floating-point trigonometric evaluations in `code/rust/src/qm/` with an exact rational/algebraic certifier using squared dihedral angle formulas and Cayley-Menger determinants.
3. **Operad Subdivision Composition**:
   Formulate the operad relation in `dag/operads/ds_qm110_111_lqg_gr_kinematical_shadows.yaml` establishing that under 4D barycentric subdivision, the integrated Regge deficit converges to the Ricci scalar curvature density $\int R \sqrt{g} d^4x$.

---

## 6. Synthesis Matrix of the Top 5 Derivation Frontiers

| Rank | Node ID | DAG Target ID | Stage | Mathematical Bottleneck | Current Finite Control | Required Next Formal Step |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | `TFQ-0307` | `FQ-GAP-BORN-UNIQUENESS-GLEASON` | `FINITE_HILBERT` | Rational sphere countermodels; $d=2$ failure | Cabello 18-ray contextuality; quartic rival elimination | Formalize Busch's POVM effect-algebra extension in Lean 4 |
| **2** | `TFQ-0085` / `TFQ-0114` | `FQ-GAP-CONTINUUM-HILBERT-LIFT` | `CONTINUUM_INTERFACE` | No limit object; unbounded operator domain convergence | Cayley norm preservation; finite grid Dirichlet modes | Construct directed inductive system of Hilbert spaces in Lean 4 |
| **3** | `TFQ-0246` | `FQ-GAP-STONE-CONTINUOUS-TIME` | `FINITE_QM_DYNAMICS` | Multi-valued matrix logarithm; discrete time aliasing | Discrete Poincaré recurrence; Cayley unitary steps | Formalize Padé branch selector with spectral window cutoff |
| **4** | `TFQ-0294` | `FQ-GAP-U1-CIRCLE` | `L1_TO_L2` | Pythagorean unit group lacks half-angles and Haar measure | Algebraic half-angle defect; Cayley rational circle | Formalize direct limit cyclotomic phase tower $\mathbb{Q}(\zeta_{2^\infty})$ |
| **5** | `TFQ-0084` / `TFQ-0110` | `DS-QM110-111-LQG-GR-KINEMATICAL-SHADOWS` | `FINITE_QG` | Broken diffeomorphisms; uncoupled cochains; arbitrary $\Lambda$ | Small triangulation deficit sums; Q-held kinematics | Formalize exact 4-simplex Regge variation and discrete Bianchi identity |

---

## 7. Claim Hygiene & Epistemic Boundary Notice

In accordance with repository Claim Hygiene rules and `AuthorityEffect: None`:
1. **What this analysis supports**: Demonstrates in this model the exact mathematical, algebraic, and topological reasons why current finite controls cannot be promoted to unconditional continuum theorems.
2. **What this analysis does not support**: Does not claim that the 5 frontiers cannot be closed or that quantum mechanics cannot be formulated discretely; rather, it identifies the explicit mathematical bridges and hypotheses required to make progress.
3. **Narrowest defensible claim**: Under the declared finite/algebraic hypotheses of the repository, the 5 derivations detailed above represent the primary structural gaps between discrete cochains and continuum physics.
4. **Next test needed**: Dispatch specialized implementation and formalization swarms to execute the Attack Plans outlined for Ranks 1 through 5.
