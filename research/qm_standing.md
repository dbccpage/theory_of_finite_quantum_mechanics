# Program Census & Research Standing

**Scope:** Technical program status across the `006_finite_qm` estate, encompassing foundational theory, algebraic carriers, formal verification, and computational engines.  
**Updated:** 2026-10-11  

---

## 1. Program Objectives & Status Summary

The research program investigates the extent to which quantum mechanics can be rigorously presented on discrete, algebraic carriers, and precisely characterizes the mathematical interfaces where continuum and infinite-dimensional structures emerge.

### Current Research Status
- **Core Results:** Exact algebraic models over cyclotomic number fields $\mathbb{Q}(\zeta_n)$, verified finite cochain complexes, discrete Weyl-Heisenberg representations, and exact integer/rational combinatorial proofs.
- **Continuous & Functional Interfaces:** Identified and characterized via rigorous mathematical theorems (Wintner-Wielandt trace obstruction for CCR, Stone's theorem for continuous unitary groups, Baker's theorem for transcendental von Neumann entropy).
- **Active Open Frontiers:** Gleason frame uniqueness on dense cyclotomic sub-spheres $\mathcal{S}(\mathbb{Q}(\zeta_n)^d)$ for $d \ge 3$, algebraic Busch effect-frame representations, and exact CHSH field extrema.

---

## 2. Register Census & Gap Inventory

The primary gap register (`claims/gap_register.yaml`, schema version 1.0.0) tracks open and resolved questions across the program:

- **Gaps List Structure:** The `gaps:` block contains **39 primary IDs** (matching the foundational paper §5 classification table). The full YAML file contains **57 total gap keys** including discharged foundational items and nested campaign milestones.
- **Continuum and Functional Interfaces:** Seven gaps address interfaces with continuous or infinite-dimensional models:
  - `GAP-F001-S000-002`: Continuum Hilbert lift & canonical commutation relations (CCR).
  - `GAP-F001-S000-004`: Gleason frame function uniqueness on dense cyclotomic spheres ($d \ge 3$).
  - `GAP-F001-S000-008`: Continuous time evolution and Stone's theorem.
  - `GAP-F001-S000-010`: Gleason dimension separation ($d = 2$ obstruction vs $d \ge 3$).
  - `GAP-F001-S000-011`: Branch fine-graining and Everett counting for non-rational algebraic weights.
  - `GAP-F001-S000-012`: Declared real embedding $\iota: \mathbb{Q}(\zeta_n)^+ \hookrightarrow \mathbb{R}$ for mixed-state spectral positivity.
  - `GAP-FQM-023`: Transcendental von Neumann entropy evaluation via certified interval enclosures.
- **Open Algebraic Bridges:** 18 active bridges under investigation, including tensor product uniqueness under declared operational axioms (`006`) and CPTP channel Choi representations (`007`).

---

## 3. Verified Code Assets & Formal Mechanics

### 3.1 Formalized Theorems in Lean 4
Active formalization is located in `lean4/quantum_mechanics/` (toolchain `leanprover/lean4:v4.34.0`):

- **Primitive Difference & Cochains:**
  - `PrimitiveDifference.lean`: Defines abstract difference operators, zero-relation quotients, and concrete integer difference kernels ($D(x, y) = y - x$) verifying antisymmetry, sameness certification, and 1-cocycle identities.
  - `FiniteCochain.lean`: Verifies the fundamental cochain complex identity $\delta^1 \delta^0 = 0$ on discrete simplicial complexes.
  - `ContextualityObstruction.lean`: Verifies that the differential squares to zero and checks global section existence/obstruction over $\mathbb{Z}_2$.
- **Foundational Quantum Mechanics:**
  - `BornNormalization.lean`: Proves unit-sum normalization for finite POVMs.
  - `GleasonTheorem.lean`: Verifies the $d = 2$ non-Bornian obstruction (`d2_binary_non_bornian_obstruction`), demonstrating that binary valuations on $S^1$ cannot be represented by density operators.
  - `Entanglement.lean`: Verifies non-zero Schmidt rank and minors for integer Bell states $|\Phi^+\rangle$.
  - `H032DiscretePythagoreanBellChsh.lean`: Proves classical CHSH bound $|S| \le 2$ and establishes the exact rational Pythagorean point $S = 14/5$ at height $H = 5$.
  - `H058EffectFrameBusch.lean`: Establishes Busch effect-frame uniqueness under coordinate-matching conditions for POVMs.
  - `H059RationalSector.lean`: Analyzes rational-sector Born weight representations and verifies algebraic irreducibility of conductor-5 polynomials ($5x^2 - 5x + 1$).
  - `H061DynamicsDichotomy.lean`: Proves the periodic vs aperiodic dynamics dichotomy for discrete unitary operators.

### 3.2 Computational Kernels (Python & Rust)
- **Rust Crates:** Canonical high-performance and exact rational implementations reside in `omega_engine/crates_rs/omega_quantum_physics/src/finite_qm/`:
  - `continuum.rs`: Exact rational Wintner-Wielandt witness and commutator trace analysis.
  - `mub/`: Mutually unbiased basis constructions across finite prime-power dimensions.
- **Python Engines:** Domain and use-case solvers reside in `omega_engine/crates/finite_qm/`:
  - `domain/primitive_difference.py`: Difference graph solvers.
  - `use_cases/continuum_lift.py`: Continuum boundary numerical diagnostics.
  - `use_cases/tensor_commuting_correlation_frontier.py`: Commuting-operator and tensor correlation frontier analysis.
  - `use_cases/busch_effects.py`: Effect frame algebraic reconstruction.

---

## 4. Campaign History & Milestones

The program has advanced through several focused research campaigns:

| Campaign | Primary Scope | Technical Milestone Achieved | Current Status |
| :--- | :--- | :--- | :--- |
| **C250** | Finite algebraic models & counterexamples | Mapped discrete state spaces, verified finite POVMs, and isolated non-Bornian $d=2$ frame functions. | Archived; findings integrated into foundational papers. |
| **C500** | Scaled discrete dynamics & Trotterization | Investigated discrete lattice dynamics, local Hamiltonian commutators, and rational Lieb-Robinson bounds. | Scoped evidence recorded; continuous thermodynamic limits handled via asymptotic scaling. |
| **C750** | Entropy dichotomy & algebraic invariants | Established Baker's theorem reduction for natural-log entropy; implemented integer Rényi power sums $P_m = \operatorname{Tr}(\rho^m)$ and certified rational interval enclosures. | Core algorithms operational in Python and Rust. |
| **C1000** | Spacetime causal orders & cyclotomic correlations | Analyzed causal poset structures, cyclotomic unit circle CHSH maxima, and contextuality cohomology. | Active; focused on unconstrained cyclotomic field extrema. |

---

## 5. Architectural Layout & Environment

- **Lean 4 Environment:** `lean4/quantum_mechanics/` consists of a flat library containing over 150 Lean source files compiling under Lake.
- **Rust Architecture:** Crate `omega_quantum_physics` provides native compiled solvers, with `omega_finite_qm` serving as a public API facade.
- **Python Architecture:** Structured package in `omega_engine/crates/finite_qm/` supporting symbolic algebra and rapid prototyping.
