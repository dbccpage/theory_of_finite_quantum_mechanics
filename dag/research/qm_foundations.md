# Foundations Roadmap — Primitive Difference Through Channels

**Scope:** Foundational theory connecting primitive difference, quantum states, Born/Gleason measures, phase and superposition, entanglement, and quantum channels across the `finite_quantum_mechanics` estate.  
**Target:** `qm_foundations.md`  
**Updated:** 2026-10-11  

---

## 1. Foundational Architecture

The foundational architecture investigates how quantum mechanics can be constructed from discrete differences on finite carriers, identifying where algebraic methods suffice and where continuous functional analysis interfaces are required.

### 1.1 The Rung-by-Rung Analysis

1. **Primitive Difference (Rung 1):**  
   - Formalized in `lean4/PrimitiveDifference.lean` via the abstract `OmegaCore.PrimitiveDifference` structure and concrete integer difference kernel $D(x, y) = y - x$.
   - Verified properties: reflexivity (`diff_self`), symmetry/antisymmetry (`diff_antisymm`), and the 1-cocycle condition (`diff_cocycle`).
   - Cochain differential $\delta^0 \alpha(u, v) = \alpha(v) - \alpha(u)$ on finite graph complexes verified in `FiniteCochain.lean`.

2. **States, Pairings, and Density Operators (Rung 2):**  
   - Formalized in `FiniteDensity.lean` for 2-state diagonal spectra and normalized probability measures.
   - Off-diagonal coherence: Represented algebraically over number fields $K = \mathbb{Q}(\zeta_n)$ or Gaussian integers $\mathbb{Z}[i]$.
   - Positivity of mixed states: Evaluated via declared real embedding $\iota: \mathbb{Q}(\zeta_n)^+ \hookrightarrow \mathbb{R}$ (`GAP-F001-S000-012`).

3. **Born Rule and Gleason Frame Valuations (Rung 3):**  
   - Two-state normalization verified in `BornNormalization.lean`.
   - Dimension $d = 2$ non-Bornian obstruction proved in `GleasonTheorem.lean` (`d2_binary_non_bornian_obstruction`), demonstrating that binary valuations on $S^1$ cannot be represented by density operators.
   - Dimension $d \ge 3$ Gleason uniqueness: Open question on dense cyclotomic sub-spheres $\mathcal{S}(\mathbb{Q}(\zeta_n)^d)$ (`GAP-F001-S000-004`, `010`).
   - Generalized POVM measurements: Additive effect-frame representations over number fields established in `EffectFrameBusch.lean` and `use_cases/busch_effects.py`.

4. **Phase, Superposition, and Interference (Rung 4):**  
   - Superposition non-descent verified in `MixingObstruction.no_descent_through_quotient`.
   - Algebraic interference: Exact signed-rational witnesses and higher-order Sorkin identity $I_3 = 0$ verified in `Superposition.lean`.
   - Phase groups: Discrete roots of unity $\mu_n \subset U(1)$ and Gaussian unit lattices $\mathbb{Z}[i]$ provide exact algebraic phase representations, interfacing with continuous $U(1)$ via archimedean completion.

5. **Entanglement and Tensor Composition (Rung 5):**  
   - Integer Bell state $|\Phi^+\rangle$ Schmidt rank and minor non-vanishing verified in `Entanglement.lean`.
   - Bilinear tensor composition: Formulated under four operational axioms (bilinearity, local unitary covariance, product-state marginals, no-signalling) in `GAP-F001-S000-006`.
   - CHSH Bell inequalities: Classical bound $|S| \le 2$ and Pythagorean rational point $S = 14/5$ verified in `DiscretePythagoreanBellChsh.lean`; Tsirelson bound $2\sqrt{2}$ attained over $\mathbb{Q}(\zeta_8)$.

6. **Measurement Updates and Quantum Channels (Rungs 6–7):**  
   - CPTP maps: Choi-Jamiolkowski isomorphism defined over cyclotomic matrix algebras $M_d(\mathbb{Q}(\zeta_n))$ with positivity checked under declared real embeddings (`GAP-F001-S000-007`).
   - Stinespring dilations: Require algebraic field extensions for purification eigenvalues.
   - Time evolution: Discrete unitary steps $U^n$ and periodic/aperiodic orbit dichotomy proved in `DynamicsDichotomy.lean`, interfacing with continuous time $U(t) = \exp(-iHt)$ via Stone's theorem (`GAP-F001-S000-008`).

---

## 2. Structural Foundations Gap Inventory

### 2.1 Algebraic Foundations & Measurement

| ID | Domain | Technical Question | Current Status & Mechanization |
| :--- | :--- | :--- | :--- |
| `GAP-F001-S000-004` | Gleason ($d \ge 3$) | Uniqueness of quadratic Born measures on dense cyclotomic spheres $\mathcal{S}(\mathbb{Q}(\zeta_n)^d)$. | Open. $d=2$ obstruction verified in Lean 4; finite Cabello/Peres configurations checked numerically. |
| `GAP-F001-S000-010` | Gleason dimension separation | Formal separation of the $d=2$ non-Bornian obstruction from $d \ge 3$ frame additivity. | Formulated. Frame additivity verified on finite triad systems. |
| `NEW-H058-BUSCH` | Busch POVM effect frames | Full algebraic representation of additive effect frame functions on $d=2, 3$ cyclotomic carriers. | In progress. Coordinate-conditional uniqueness proved in `EffectFrameBusch.lean`; numerical recovery verified. |
| `GAP-F001-S000-012` | Mixed-state spectral positivity | Declared real embedding $\iota: \mathbb{Q}(\zeta_n)^+ \hookrightarrow \mathbb{R}$ for mixed-state PSD verification. | Standard algebraic number theory; embedding parameter formalized across tests. |
| `NEW-DENSITY-COHERENCE` | Off-diagonal density coherence | Exact algebraic conditions forcing off-diagonal density entries from generalized cochain statistics. | Formulated over cyclotomic matrices $M_d(\mathbb{Q}(\zeta_n))$. |
| `NEW-LUDERS-COHERENCE` | Operator Lüders rule | Exact rational Lüders update $\rho \mapsto P\rho P / \operatorname{Tr}(P\rho)$ preserving within-sector coherence. | Implemented in symbolic kernels; formalization in progress. |

### 2.2 Phase, Superposition, and Symmetry

| ID | Domain | Technical Question | Current Status & Mechanization |
| :--- | :--- | :--- | :--- |
| `GAP-F001-S000-005` | Phase group representations | Algebraic roots of unity $\mu_n \subset U(1)$ and discrete J-algebras vs continuous $U(1)$ Lie group. | Discrete phase representations verified; continuous $U(1)$ characterized as topological closure. |
| `GAP-FQM-010` | $U(1)$ selector & $J$-algebra | Formalization of discrete complex carrier selection and Gaussian integer $J$-algebras. | Discrete algebraic identities operational; formal replay in progress. |
| `NEW-PHASE-060-LEDGER` | Superposition fiber | Non-descent of coherent states through classical quotients. | Proved in `MixingObstruction.no_descent_through_quotient`. |

### 2.3 Composition, Entanglement, and Nonlocality

| ID | Domain | Technical Question | Current Status & Mechanization |
| :--- | :--- | :--- | :--- |
| `GAP-F001-S000-006` | Tensor product uniqueness | Uniqueness of the Kronecker tensor product among bilinear maps under operational axioms. | Axiomatic characterization formulated (`CompositionTensorMub.lean`). |
| `GAP-C1000-006` | CHSH cyclotomic supremum | Exact supremum of CHSH correlation over unit vectors in cyclotomic fields $\mathbb{Q}(\zeta_n)^2$. | At height $H=5$, max is $14/5$ on $\mathbb{Q}, \mathbb{Q}(i)$; Tsirelson bound $2\sqrt{2}$ attained over $\mathbb{Q}(\zeta_8)$. |
| `GAP-F001-S000-001` | Duality gap certificates | Exact primal/dual linear programming certificates for cochain boundary operators $\Phi_1$. | Implemented in exact rational solvers; formal pairing bounds in `DualWitness.lean`. |
| `NEW-MUB-D6-FOURTH` | Mutually Unbiased Bases ($d=6$) | Existence of a fourth MUB in dimension $d=6$. | Open mathematical research problem across quantum information theory. |

### 2.4 Dynamics, Channels, and Field Theory Interfaces

| ID | Domain | Technical Question | Current Status & Mechanization |
| :--- | :--- | :--- | :--- |
| `GAP-F001-S000-007` | CPTP Choi representation | Exact Choi matrix representation and Stinespring dilation over cyclotomic fields. | Choi PSD defined under real embedding; Stinespring purifications require radical extensions. |
| `GAP-F001-S000-008` | Unitary time evolution & Stone | Discrete unitary steps $U^n$ vs continuous Hamiltonian generators $H = i \log U$. | Discrete periodic/aperiodic orbit dichotomy proved; Stone's theorem characterized as continuous interface. |
| `GAP-C500-B06` | Finite-lattice Trotter / LR bounds | Certified Trotter product formula error bounds and Lieb-Robinson velocities on finite lattices. | Denominator bounds proved in `H073`; local commutator bounds under verification. |
| `NEW-QM-CHANNELS-033` | Continuous Schrödinger equation | Discrete cochain transport networks converging to continuous Schrödinger equations. | Discrete transport operational; continuum scaling limits mapped. |
| `NEW-QM-CHANNELS-050` | Dirac equation on spacetime | Discrete lattice-Dirac approximations vs continuous Dirac spinor fields on Minkowski spacetime. | Discrete Clifford algebra representations operational. |

---

## 3. Core Mathematical Trajectories

1. **Gleason Frame Analysis on Dense Cyclotomic Sub-Spheres:**  
   Focus analytical effort on establishing whether dense algebraic subsets $\mathcal{S}(\mathbb{Q}(\zeta_n)^d)$ enforce quadratic Born measures under noncontextual frame additivity, or whether number-theoretic colorings (analogous to Meyer's rational sphere theorem) can be constructed.

2. **Busch POVM Effect Frame Formalization:**  
   Extend `EffectFrameBusch.lean` to provide general homogeneity constructors for all effects in $\operatorname{Eff}_d$, completing the algebraic recovery of density operators from POVM measurements.

3. **Certified Rational Interval Numerics:**  
   Maintain verified interval algorithms for transcendental spectral quantities ($S(\rho)$, relative entropy, quantum capacity), decoupling algebraic carrier purity from external continuum thermodynamic calculations.
