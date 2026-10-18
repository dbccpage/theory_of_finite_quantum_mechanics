# Finite QM Guide Map

**Citation:** `sealed-derivation-v1` (`3100c4e`). Canonical synthesis reference across finite and algebraic quantum formulations.

## 1. Five Distinct Meanings of "Finite" in Quantum Mechanics

To maintain analytical clarity and prevent invalid cross-domain deductions (such as inferring an obstruction to discrete quantum representations from an obstruction to a single continuous functional), we distinguish five mathematically precise notions of "finiteness":

1. **Finite Hilbert Space Dimension ($\dim \mathcal{H} < \infty$)**:
   - The state vector lives in $\mathbb{C}^d$ for finite $d$.
   - For $d \ge 2$, the pure-state space $\mathbb{C}P^{d-1}$ is an uncountable compact manifold; at $d=1$ it is a point.
   - Operations include continuous unitary groups $U(d)$ and standard density matrices.
   - *Scope boundary*: Finite dimension does not imply a finite state set, finite field, or finite discrete group of operations.

2. **Finite Algorithmic Description / Exact Algebraic Representation**:
   - States, observables, and parameters admit exact finite representation (e.g. algebraic numbers in a declared number field $K$, rational coordinates, or finite bit-strings).
   - The set of all algebraic complex rays is countably infinite and dense in $\mathbb{C}P^{d-1}$. A particular fixed carrier and admitted normalization operations need a separate density argument.
   - Operations are exact symbolic manipulations without floating-point truncation.
   - *Scope boundary*: Countable algebraic representation does not imply finite cardinality of the physical state space.

3. **Finite Physical State Space ($|\mathcal{S}| < \infty$)**:
   - The system is restricted to a finite set of allowed physical states.
   - Examples: discrete stabilizer states under Clifford operations, finite orbit closures, discrete phase-space models.
   - *Scope boundary*: True finite state spaces strictly exclude continuous superpositions; universality requires non-Clifford resources that extend beyond the finite set.

4. **Finite Scalar Field ($\mathbb{F}_q$)**:
   - Probability amplitudes and state vectors are defined over a Galois field $\mathbb{F}_q = \mathrm{GF}(p^k)$.
   - Examples: modal quantum mechanics, $\mathbb{F}_2$ parity carriers.
   - *Scope boundary*: Finite fields admit no total order compatible with field operations and no non-trivial positive definite inner product. The field alone supplies no ordered Born probabilities; qualitative/modal valuations or a separately supplied real probability carrier must be distinguished.

5. **Algebraic Number Field Carrier ($K = \mathbb{Q}(\zeta_n)$ or $K^+$)**:
   - Amplitudes lie in a fixed cyclotomic number field $K = \mathbb{Q}(\zeta_n)$ or its maximal totally real subfield $K^+$.
   - $K$ is a countably infinite algebraic extension of $\mathbb{Q}$ of characteristic zero, embedding naturally into $\mathbb{C}$.
   - Matrix entries and characteristic polynomials have coefficients in $K$; eigenvalues lie in a finite algebraic extension $L/K$.
   - *Scope boundary*: An algebraic number field is not a finite set; it possesses characteristic zero and embeds into $\mathbb{C}$.

## 2. Decision Map Table

| Proposal / Precise Claim & Scope | Status | Strongest Available Evidence & Source | Structural Analysis | Computational Interface | Recommendation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **P1. Exact Natural-Log Entropy Internal to Algebraic Carrier**<br>Claim: For all finite-dimensional density matrices with algebraic real spectrum, $S(\rho) = -\mathrm{Tr}(\rho \ln \rho) \in K$. | **TRANSCENDENTAL_EXTERNAL_INTERFACE** | Baker A1 reduction (`entropy_reduction.md`, `EntropyDichotomy.lean`). Nonzero entropy of mixed algebraic state is transcendental. $S(\rho) \in K \iff \rho$ is pure ($S=0$). | Baker's theorem on linear forms in logarithms shows transcendence over $\mathbb{Q}(\zeta_n)$. | Evaluate thermodynamic entropy via certified rational interval enclosures $[a,b] \subset \mathbb{Q}$ or continuum embeddings; monitor internal carrier purity via integer Rényi power sums $P_m = \operatorname{Tr}(\rho^m)$. | **INTERFACE**: Treat natural-log entropy as an external transcendental functional; track carrier purity algebraically using $P_m$. |
| **P2. Base-2 Entropy Internal to Algebraic Carrier**<br>Claim: $S_2(\rho) = -\sum p_i \log_2(p_i) \in K$ for all density matrices over $K$. | **DYADIC_ALGEBRAIC_SUBSECTOR** | $S_2(1/2, 1/2) = 1 \in \mathbb{Q} \subset K$ provides positive counterexample to universal transcendence under base 2. | Natural-log transcendence alone does not determine the quotient by $\log 2$; each further base-2 claim needs its own hypotheses and proof. | Restrict exact base-2 evaluations to dyadic probability trees where $p_i = 2^{-k_i}$. | **SCOPED_USE**: Valid for dyadic-power spectra; use external interval enclosures for generic algebraic distributions. |
| **P3. Bounded Rational Interval Entropy Approximation Interface**<br>Claim: Verified rational intervals $[a, b] \subset \mathbb{Q}$ of width $\le 2^{-k}$ enclose $S(\rho)$ for declared cyclotomic densities. | **CERTIFIED_INTERVAL_INTERFACE** | Implemented in T563 (`cyclotomic_density.py`, `entropy_dichotomy.rs`). Counted dyadic spectral clusters and uniform Taylor-log bounds. | Higher-degree polynomials ($d \ge 5$) utilize general algebraic root isolation (splitting algebra). | Run verified interval enclosures with certified Taylor-series remainder bounds on arbitrary cyclotomic density inputs. | **CONTINUE**: Standardize certified rational interval enclosures as the canonical numerical interface for transcendental functionals. |
| **P4. Integer-Order Rényi Power Sums as Carrier-Internal Invariants**<br>Claim: $P_m = \mathrm{Tr}(\rho^m) \in K$ for all integers $m \ge 2$, providing carrier-internal purity and purity-decay monitors. | **ALGEBRAIC_CARRIER_INTERNAL** | Matrix powers and traces rely strictly on ring operations in $K$. Implemented in C750/C1000 models. $P_2 = 1 \iff \rho$ is pure. | Power sums $P_m$ track purity and rank algebraically without requiring logarithms: $P_2 \in (1/d, 1]$ for valid states. | Exact evaluation via matrix multiplication and trace over declared cyclotomic field $K$. | **CONTINUE**: Adopt $P_m$ as the native algebraic invariant for state mixedness and entanglement decay. |
| **P5. Quantum Mechanics over Finite Fields ($\mathbb{F}_q$)**<br>Claim: Predictive physical quantum mechanics can be formulated with probability amplitudes in $\mathbb{F}_q$. | **MODAL_COMBINATORIAL_DOMAIN** | Absence of total ordering and positive-definiteness in $\mathbb{F}_q$ precludes standard metric probabilities. Adits null state vectors ($v^\dagger v = 0$ for $v \ne 0$). | Consistent as a modal logic toy model (evaluating "permitted" vs "forbidden" transitions). | Map state transitions to discrete incidence geometries and modal transition systems. | **SPECIALIZED_DOMAIN**: Maintain $\mathbb{F}_q$ for combinatorial and modal logic studies; use an ordered real subfield for probabilities and a declared complex field with conjugation for amplitudes. |
| **P6. Strictly Finite State Spaces ($|\mathcal{S}| < \infty$) via Stabilizers**<br>Claim: Physical quantum subsystems can be restricted to finite discrete state orbits without loss of quantum advantage. | **SUB_UNIVERSAL_STABILIZER_SECTOR** | Gottesman-Knill theorem: Clifford circuits on stabilizer states admit efficient classical simulation. | A suitable universal gate set, such as Clifford+T with appropriate entangling gates, can generate an infinite projectively dense orbit. The T gate alone has finite order; non-Clifford status alone does not prove universality. | Characterize contextuality (e.g. Mermin-Peres magic square) achievable within stabilizer sub-theories. | **REFINED_SCOPE**: Model stabilizer mechanics as exact sub-universal resource theories; explicitly delineate the injection of non-stabilizer resources. |
| **P7. Cyclotomic Number Field Carriers for Topological Phases**<br>Claim: Discrete spacetime models and topological anyonic braid groups close exactly over $K = \mathbb{Q}(\zeta_n)$. | **ALGEBRAIC_TOPOLOGICAL_PHASES** | Validated finite rotation and fusion-category examples use declared exact fields; required square roots and normalizations are checked per example. | Selected rational boosts have unbounded denominators; density and topological completion require separate hypotheses. | Test discrete light-cone causal orderings preserving local no-signalling without continuum boost closure. | **CONTINUE**: Utilize cyclotomic carriers for discrete rotational, anyonic, and topological systems while recording field closure and topological completion separately. |

## 3. Boundary Theorems and Structural Distinctions

1. **Transcendental Entropy Boundary (Baker's Theorem)**:
   - For any mixed density matrix $\rho$ with algebraic eigenvalues, the natural-log von Neumann entropy $S(\rho) = -\mathrm{Tr}(\rho \ln \rho)$ is transcendental over $\mathbb{Q}(\zeta_n)$ whenever $\operatorname{rank}(\rho) > 1$.
   - This mathematical fact delineates carrier-internal polynomial invariants ($P_m = \mathrm{Tr}(\rho^m)$) from transcendental thermodynamic quantities, which are evaluated via certified interval enclosures or continuum embeddings.

2. **Base-Dependent Logarithmic Behavior**:
   - The transcendence of natural-log entropy does not universally preclude rational values for all logarithmic bases.
   - For example, dyadic probability distributions yield exact rational base-2 entropies (e.g. $S_2(1/2, 1/2) = 1$).
   - Gelfond-Schneider can settle specific logarithm ratios under its hypotheses; no universal base-2 classification is asserted here.

3. **Field Characteristics and Metric Structure**:
   - Finite fields $\mathbb{F}_q$ lack compatible total ordering and non-trivial positive definite inner products.
   - They provide rigorous combinatorial and modal frameworks for possibility/impossibility logic, while positivity uses an ordered real carrier or a chosen real embedding of the conjugation-fixed subfield. Nonreal $\mathbb{Q}(\zeta_n)$ itself is not an ordered field.

4. **Symmetry Group Closures**:
   - Each rotation or braid example requires its own validated coefficient field; the finite catalog is not a classification of all rotation or braid representations.
   - An exact rational Lorentz transformation can have infinite order while every finite product stays rational. Topological closure and field closure are different operations; noncompactness alone establishes neither a required field extension nor density of a chosen subgroup.


## 4. Preserved Algebraic Core and Continuum Interfaces

1. **Algebraic Number Field State and Observable Representations**:
   - Declared finite-dimensional matrix models over $K = \mathbb{Q}(\zeta_n)$ support exact operations that stay in that field. Spectral decomposition, normalization and purification may require extensions; operational closure must be checked.
   - Density matrices, unitary transformations, projection operators, and expectation values of algebraic observables evaluate strictly within $K$ or algebraic extensions $L/K$.

2. **Carrier-Internal Rényi Power Sums ($P_m = \mathrm{Tr}(\rho^m)$)**:
   - Integer-order traces $P_m = \sum_i p_i^m$ evaluate strictly within $K$.
   - For a positive trace-one density matrix, purity is characterized by $P_2 = 1$ and $P_2 \in [1/d, 1]$; the maximally mixed state attains the lower endpoint.

3. **Certified Rational Interval Enclosures ($[a, b] \subset \mathbb{Q}$)**:
   - Exact rational interval arithmetic provides provable error bounds $|S(\rho) - m| \le 2^{-k}$ for transcendental functionals without requiring algebraic field containment.
   - Counted spectral clusters and uniform Taylor-log approximations cleanly decouple numerical evaluation from field confinement.

4. **Stabilizer Sub-Theories and Finite Causal Orders**:
   - Discrete stabilizer mechanics and discrete poset causal orders preserve exact algebraic closure, local no-signalling, and contextuality bounds while interfacing naturally with continuum field theories.

## 5. Research Trajectories and Numerical Interfaces

1. **Entanglement and Purity Tracking**:
   - Evaluate the operational sensitivity of $P_2 = \mathrm{Tr}(\rho^2)$ under partial trace against standard von Neumann entropy across parameter families such as two-qubit Werner states $\rho(p) = p |\Phi^+\rangle\langle\Phi^+| + \frac{1-p}{4} I$ for $p \in \mathbb{Q} \cap [0, 1]$.
   - Establish monotonicity properties of algebraic invariants as computable surrogates for transcendental entropy.

2. **Asymptotic Scaling and Enclosure Verification**:
   - Utilize certified interval arithmetic for transcendental spectral functions rather than attempting to factor general quintic splitting fields.
   - Investigate asymptotic large-$d$ limits connecting discrete Weyl-Heisenberg groups to continuous CCR algebras.
