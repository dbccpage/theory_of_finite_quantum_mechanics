# Finite-QM Roadmaps — Index

**Scope:** Guide and architectural index for the `006_finite_qm` research monographs and technical roadmaps.  
**Updated:** 2026-10-11  

This directory contains the core technical roadmaps evaluating the presentation of quantum mechanics on finite and algebraic carriers and characterizing the interfaces to continuum quantum mechanics.

---

## 1. Roadmap Architecture

The roadmaps are structured systematically across six key domains:

| File | Domain & Role |
| :--- | :--- |
| [qm_standing.md](qm_standing.md) | **Program Census & Standing:** Census of assets, verified Lean theorems, active code kernels, and campaign status. |
| [qm_foundations.md](qm_foundations.md) | **Foundational Theory:** Primitive difference, quantum states, Born/Gleason measures, phase, entanglement, and channels. |
| [qm_cohomology.md](qm_cohomology.md) | **Cohomology & Obstructions:** Cochain complex analysis, $\Phi_1 / \Gamma_2$ optimization, contextuality cohomology, and duality. |
| [qm_finite_to_infinite.md](qm_finite_to_infinite.md) | **Finite-to-Infinite Architecture:** Operator algebras (CCR), Stone's theorem, transcendental entropy, and continuum scaling limits. |
| [qm_implementation.md](qm_implementation.md) | **Implementation & Verification:** Compiled Rust crates, Python symbolic kernels, Lean 4 formalizations, and test suites. |
| [qm_gaps_and_effort.md](qm_gaps_and_effort.md) | **Master Gap Inventory:** Comprehensive register of continuum interfaces, open algebraic questions, and verification tasks. |
| [qm_crazy_ideas.md](qm_crazy_ideas.md) | **Speculative Research & Frontiers:** Exploratory models, exact cochain solvers, and frontier selection algorithms. |

---

## 2. Research Overview

The program investigates the boundary between discrete algebraic quantum mechanics and continuous infinite-dimensional quantum mechanics:
- **Discrete & Algebraic Core:** Exact models over cyclotomic number fields $\mathbb{Q}(\zeta_n)$, verified finite cochains with $\delta^1 \delta^0 = 0$, discrete Weyl-Heisenberg groups, and integer/rational Bell/CHSH witnesses.
- **Continuum & Functional Interfaces:** Precise mathematical interfaces identified via Wintner-Wielandt trace identity (CCR), Stone's theorem (continuous time & Hamiltonians), and Baker's theorem (transcendental von Neumann entropy).
- **Active Open Frontiers:** Gleason frame uniqueness on dense cyclotomic sub-spheres $\mathcal{S}(\mathbb{Q}(\zeta_n)^d)$ for $d \ge 3$, algebraic Busch effect-frame representations, and exact CHSH cyclotomic field extrema.

---

## 3. Focused Research Derivations & Monographs

| File | Topic & Scope |
| :--- | :--- |
| [qm_finite_path_algebra.md](qm_finite_path_algebra.md) | **Finite Path Matrix Completion:** Regular path algebra, origin-sector star completion, and path-algebra faithfulness. |
| [qm_ancilla_capacity.md](qm_ancilla_capacity.md) | **Limited Ancilla Capacity:** Central-sector purification bounds for specified ancilla blocks and spectral grouping. |
| [qm_finite_history_groupoid.md](qm_finite_history_groupoid.md) | **Finite-History Groupoid Bridge:** Positive full groupoid algebra and conditional purification criterion. |
| [qm_native_history_cost.md](qm_native_history_cost.md) | **Native History Costs:** Source-25 loop witness, formal finite-report and inverse-cost obstructions. |
| [qm_native_history_guard.md](qm_native_history_guard.md) | **Native Future Guards:** Minimal finite-depth reports for Source-25 assertion cells and guard reflection controls. |
| [qm_primitive_readout_boundary.md](qm_primitive_readout_boundary.md) | **Primitive/Readout Boundary:** Report-fiber invariance and exact finite readout controls (linear, quadratic, quartic). |
| [phase_fiber_holonomy_bridge_finite_map.md](phase_fiber_holonomy_bridge_finite_map.md) | **QM-207 Phase Fiber and Holonomy Bridge:** U(1) cochain classification on finite carriers, and the split of imports QM-207 to QM-211 into exact cycle invariants, imported completion steps and named residual imports. |
| [quadratic_readout_finite_map.md](quadratic_readout_finite_map.md) | **QM-208 Quadratic Readout Finite Map:** Sorkin I₃ selection inside the phase-blind polynomial family, two-report cross term as the real part of the loop holonomy, and the imported composition rule. |
| [context_parity_finite_map.md](context_parity_finite_map.md) | **QM-209 Context Parity Finite Map:** Weyl commutator holonomy in μ_d, Peres–Mermin F₂ cokernel H₀(K₃,₃; F₂) and the imported second context. |
| [frame_function_finite_map.md](frame_function_finite_map.md) | **QM-210 Frame Function Finite Map:** finite linear Gleason census with nullity zero on Cabello prefixes and the Peres set, F₂ Kochen–Specker parity, and a rational positivity-gap witness. |
| [clock_tower_finite_map.md](clock_tower_finite_map.md) | **QM-211 Clock Tower Finite Map:** finite spectral theorem over Q(ζ₂₄), square-root census, refinement along divisibility, and the imported continuity and unit. |
| [dressed_graph_qed_g2_finite_map.md](dressed_graph_qed_g2_finite_map.md) | **QM-212 Dressed Graph & Rational QED g-2 Finite Map:** Symanzik spanning-tree polynomial U_G and dual Kirchhoff cofactor, Ravera DFM spanning-tree gauge dressing invariance, and 12-decimal rational interval enclosure of L = 1, 2, 3 (and 4) QED a_e over Q. |
| [hierarchical_nonabelian_dfm_finite_map.md](hierarchical_nonabelian_dfm_finite_map.md) | **QM-213 Hierarchical Non-Abelian DFM Finite Map:** Substantial-vs-artificial LocalGreen/GlobalRed patch cohomology, two-stage Borel N <| B_2(Q) tree dressing, and P_5 discrete Bianchi identity. |
| [symanzik_two_forest_bphz_finite_map.md](symanzik_two_forest_bphz_finite_map.md) | **QM-214 Second Symanzik 2-Forest & BPHZ Finite Map:** Combinatorial 2-forest polynomial F_G, Kirchhoff-Schur duality, DFM tree momentum routing, and Zimmermann BPHZ forest UV pole cancellation over Q. |
| [dirac_ward_takahashi_finite_map.md](dirac_ward_takahashi_finite_map.md) | **QM-215 Dirac / Kulish–Faddeev & Ward–Takahashi Finite Map:** Exact Cl_{1,3}(Q(i)) Dirac propagator, spanning-tree fermion dressing, 1-loop Ward–Takahashi Z_1 = Z_2 identity, and 12-decimal Kulish–Faddeev soft-photon attenuation enclosure. |
| [vacuum_polarization_lamb_shift_finite_map.md](vacuum_polarization_lamb_shift_finite_map.md) | **QM-216 Vacuum Polarization & Lamb Shift Finite Map:** Transverse Ward projector, 1-loop Clifford bubble trace, BPHZ on-shell subtraction, Uehling moments, and 12-decimal running coupling and Lamb-shift enclosures. |
| [algebraic_bound_state_spectra_finite_map.md](algebraic_bound_state_spectra_finite_map.md) | **QM-217 Algebraic Bound-State Spectra Finite Map:** Exact su(2) Kravchuk harmonic oscillator, so(4) Pauli–Runge–Lenz Hydrogen spectrum, n=2 2S/2P projectors, and 12-decimal Lyman-alpha and 2S-2P contact enclosures. |
| [page_wootters_tsirelson_wigner_finite_map.md](page_wootters_tsirelson_wigner_finite_map.md) | **QM-218 Page–Wootters, Tsirelson & Wigner Finite Map:** Relational Page–Wootters clock dressing over Q(i), cyclotomic Q(zeta_8) Tsirelson SOS decomposition, and (Z_3)^2 discrete Weyl–Wigner phase space over Q(zeta_3). |
| [foundational_derivation_closure_finite_map.md](foundational_derivation_closure_finite_map.md) | **QM-219 Foundational Derivation Closure Finite Map:** Bipartite composition triad (direct sum vs. tensor product vs. PR box), 5x5 single-system import independence countermodels, and Z[zeta_12] Sorkin I_3 = 0 readout classification. |
| [electroweak_dfm_weinberg_finite_map.md](electroweak_dfm_weinberg_finite_map.md) | **QM-220 Electroweak DFM, Weinberg Projectors & Anomaly Cancellation Finite Map:** Finite SU(2)_L scalar-doublet dressing field u(Phi) in SU(2, Q[i]), rational Weinberg spectral projectors Pi_gamma and Pi_Z, tree-level custodial rho_EW = 1 identity, Gell-Mann-Nishijima charge operator, and N_c = 3 cubic U(1)_Y^3 anomaly cancellation over Q. |
| [qcd_beta0_wilson_confinement_finite_map.md](qcd_beta0_wilson_confinement_finite_map.md) | **QM-221 QCD Beta_0 & Wilson Confinement Finite Map:** Rational-weighted su(3)_c Gell-Mann basis and 81-entry Fierz completeness over Q(i), 1-loop Gross–Wilczek–Politzer beta_0 = 11 - 2/3 n_f, 2-loop Banks–Zaks ratio 1/302, and finite-graph Wilson-loop Creutz confinement witness over Q. |
| [qm_projective_history_algebra.md](qm_projective_history_algebra.md) | **Projective History Algebras:** Unitary composition phases, commutator radicals, and exact 6D Weyl MUB6 model. |
| [qm_formal_estate_and_crate_census.md](qm_formal_estate_and_crate_census.md) | **Formal Estate & Crate Census:** Master census of 188 Lean 4 modules and 13 mathematical Rust crates. |
| [quantum_to_classical_descent/README.md](quantum_to_classical_descent/README.md) | **Quantum-to-Classical Descent:** Finite repair algebra, sufficient records, and autonomous dynamics. |
