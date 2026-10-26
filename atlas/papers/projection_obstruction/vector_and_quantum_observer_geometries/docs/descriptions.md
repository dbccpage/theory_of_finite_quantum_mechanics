# Vector and Quantum Observer Geometries: Gauge Relativity and Trace Metric Bounds (GS-003)

Subtitle: Non-Scalar Observer Geometries, Trace Distance Duality, and the CPTP Metric Non-Selection Boundary

## Abstract

Scalar-valued edge defects are not universal. The local defect carrier may be vector- or operator-valued, while the declared observer gauge maps its residual class to a scalar magnitude. In finite obstruction calculus, the residual class may be algebraically fixed relative to the declared repair quotient while its measured scalar magnitude depends on the observer gauge used to measure local defects. A three-edge cycle already shows the split: coordinate-channel sensing gives $\Phi=2$ (scalar $\ell^1$), while Euclidean vector-displacement sensing gives $\Phi=\sqrt{2}$ ($\ell^1(E;\ell^2)$). This note develops two non-scalar observer geometries — the Euclidean vector gauge and a quantum trace-distance gauge — as the worked realization of the branches Paper 001 §4.6 names but leaves undeveloped, with explicit dual-witness theory and a shared $\Phi\Gamma R$ closure signature. All results are finite-dimensional and finite-graph.

## Why This Matters

Anyone building a diagnostic over vector- or operator-valued bond data — mechanical/synchronization loops, or quantum state-comparison networks — needs to know that the number reported is not intrinsic to the defect: it is fixed by the gauge declared. The same irreducible closure mismatch reads as $2$ to a coordinate-channel detector and $\sqrt{2}$ to a Euclidean-strain detector.

This monograph also marks the honest boundary between a gauge selected by a symmetry theorem and one chosen or conditionally selected by an operational measurement axiom:
1. Vector Branch: The Euclidean stalk gauge $\ell^2$ is mathematically forced by $SO(k)$ rotational symmetry on vector-valued stalks.
2. Quantum Branch: Monotonicity under Completely Positive Trace-Preserving (CPTP) channels does not select the trace-distance gauge (due to scale invariance and the existence of families of monotone metrics such as Petz metrics and relative entropies). Instead, trace distance is conditionally selected by the operational Helstrom binary state-discrimination axiom.

## Core Theorems

- Cycle Circulation Invariance: On any directed cycle fixture, cycle circulation $c = \sum_{e \in \mathrm{cycle}} \omega_e$ is preserved modulo repair coboundary ($d_0 \alpha$ telescopes to zero on the cycle), yielding quotient norm $\Phi_J([\omega]) = j(c)$.
- Triangle Gauge Relativity Anomaly: On a 3-edge cycle with circulation $c=(1,1)$, coordinate-channel $\ell^1$ sensing yields $\Phi_{1,1}=2$, while Euclidean vector gauge sensing $\ell^1(E;\ell^2)$ yields $\Phi_{2,1}=\sqrt{2}$.
- Mixed Vector Obstruction Duality: For finite-dimensional vector cochain complexes, strong Fenchel duality establishes $\Phi_{2,1}([\omega]) = \max_\varphi \sum_e \langle \varphi_e, \omega_e \rangle$ subject to divergence-free conditions $d_0^* \varphi = 0$ and Euclidean ball capacity $\|\varphi_e\|_2 \le 1$.
- Mixed Closure Bound: For a 2-cell boundary operator $d_1$ with $d_1 d_0 = 0$, the closure defect satisfies $\Gamma_2([h]) \le \|d_1\| \Phi_{2,1}([h])$.
- CPTP Metric Non-Selection Firewall: Monotonicity under all CPTP maps does not uniquely select the trace-distance gauge: $(\forall \Lambda \in \mathrm{CPTP},\; j(\Lambda X) \le j(X)) \not\Longrightarrow j(X) = \frac{1}{2}\|X\|_1$.
- Stochastic $\ell^1$ Contraction Shadow: Reading the output diagonal of a Kraus representation in declared bases induces a column-stochastic Markov kernel $K(\gamma'\mid\gamma)$ which contracts the classical $\ell^1$ norm, serving as the classical shadow of the quantum data processing inequality.
- Conditional Helstrom Selection: Unitary invariance combined with classical total-variation reduction uniquely selects the trace-distance metric $j_n(X) = \frac{1}{2}\|X\|_1$ on traceless Hermitian operators.
- Quantum Trace-Norm Obstruction Duality: Finite-dimensional operator quotient optimization satisfies strong duality $\Phi_Q([\delta]) = \max_\varphi \sum_e \mathrm{Tr}(\varphi_e \delta_e)$ subject to divergence-free condition $d_0^* \varphi = 0$, Hermitian symmetry $\varphi_e = \varphi_e^\dagger$, and spectral norm bound $\|\varphi_e\|_\infty \le 1/2$.
- CPTP Monotonicity: Raw quantum defect load satisfies $J_Q(\Lambda \delta) \le J_Q(\delta)$ unconditionally. Quotient obstruction satisfies $\Phi'_Q([\Lambda^1 \delta]) \le \Phi_Q([\delta])$ under typed cochain intertwining $\Lambda^1 d_0 = d_0' \Lambda^0$.
- Quantum $\Phi\Gamma R$ Signature: The closure defect $\Gamma_2^Q([h]) = \sum_f \frac{1}{2}\|(d_1 h)_f\|_1$ satisfies $\Gamma_2^Q \le \|d_1\| \Phi_Q$.

## Formal Verification and Computational Artifacts

- Lean 4 Mechanization (`lean4/`):
  - `mixed_vector_duality.lean`, `strong_vector_duality.lean`: Vector gauge duality, Hahn-Banach separation, and minimax attainment.
  - `quantum_trace_duality.lean`: Quantum Helstrom observable bounds, slack nonnegativity, and single-cycle qubit fixture attainment.
  - `cptp_monotonicity.lean`: Scale-invariance of monotonicity, halving contraction, and column-stochastic $\ell^1$ contraction.
  - Axiom report (`lean4/axiom_report.txt`): Audited census certifying strict standard Lean 4 axioms (`propext`, `Quot.sound`, `Classical.choice`).
- Python Engine (`code/`):
  - `classical_geometry.py`: Classical quotient solvers, mixed $\ell^p$ vector metrics, and dual circulation extractors.
  - `quantum_geometry.py`: Helstrom dual quotient solver, Schatten norms, and operator cochain complexes.
  - `cptp_channels.py`: Completely positive trace-preserving channel simulations and quotient monotonicity verification.
  - `demonstrations.py`, `generate_figures.py`: Verification scripts and publication figure generation.
  - 50 passing unit and adversarial mutation tests in `code/tests/`.
- Interactive Notebooks (`jupyter_notebooks/`):
  - `01_intuitive_vector_quantum_geometry.ipynb`: Interactive visual exploration of gauge relativity.
  - `02_rigorous_observer_cochains.ipynb`: Formal cochain complex calculations and dual witness verifications.
  - `03_reproduction_checks.ipynb`: Clean reproduction checks for review and automated verification.

## Scope Boundaries and Non-Claims

- Finite Settings Only: All theorems apply strictly to finite-dimensional vector spaces and finite cell complexes.
- Metric Non-Selection: CPTP channel monotonicity alone underdetermines the metric; operational selection requires explicit distinguishability axioms.
- Population Shadow Fence: Output-diagonal population transitions track population transport only; they do not determine off-diagonal coherence transport.
- Single-Cycle Closed Form: The identity $\Phi_J([\omega]) = j(c)$ is valid for single-cycle fixtures; general graphs require primal-dual optimization.
- No Physical Substrate: The mathematical analogy of operator decay $e^{-t H_{\mathrm{obstr}}}$ asserts no physical quantum substrate, quantum gravity, or continuous spacetime.

## Version and DOI Chain

- Concept DOI: `10.5281/zenodo.20651283`
- Published v0.1: `10.5281/zenodo.20651284`
- This Release: `v0.4` (absorbs formal and mechanized contents of foundation notes QM_081 and QM_082).
