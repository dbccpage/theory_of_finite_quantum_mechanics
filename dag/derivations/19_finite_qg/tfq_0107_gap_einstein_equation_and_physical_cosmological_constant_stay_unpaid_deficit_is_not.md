# [TFQ-0107] GAP: Einstein equation and physical cosmological constant stay unpaid; deficit is not

> **Stage**: `FINITE_QG` | **Status**: `GAP`  
> **UUID**: `5a31525e-8d87-55bd-89b1-a4252574d09e`  
> **Parent Derivation**: [TFQ-0106](tfq_0106_gap_the_physical_cosmological_constant_is_not_discharged_the_rust_carrier_is.md)

---

## 1. Abstract & Formal Statement

field_equation.rs and hamiltonian_constraint.rs write discrete Einstein-Regge and Wheeler-DeWitt formulae, including a Lambda term, over floating edge lengths and dihedral angles. Those comments describe algebraic scaffolds and a vanishing condition for a discrete operator. They do not discharge the Einstein equation, which remains GAP, and they do not select a physical cosmological constant. What is finite is a triangulation with floating edge data when a caller supplies one. What is not discharged is a continuum field equation and any claim that a deficit equals smooth curvature. AuthorityEffect is None.

Narrowed in Lean 4 (`lean4/FieldEquationConstraintReplay.lean`) and an independent Python verifier (`checks/independent/tfq-0107.py`) to three exact rational algebraic components and scope fences over $\mathbb{Q}$:
1. **Exact Rational Replay of `field_equation.rs`**: replays `cosmoGrad`, `reggeEdgeResidual`, `discreteEinsteinTensor`, and `reggeRelaxationStepSq`, proving the zero-residual equivalence $C = \lambda V_{\text{grad}}$ (`regge_edge_residual_zero_iff`), the flat-interior unit-test replay (`flat_interior_regge_residual_replay`), and the gradient-relaxation fixed-point equivalence (`regge_relaxation_fixed_point_iff`).
2. **Exact Rational Replay of `hamiltonian_constraint.rs`**: replays `vertexDualVolumeShare`, `vertexKineticTerm`, `vertexCurvaturePotential`, `vertexCosmologicalPotential`, and `vertexHamiltonianResidual`, proving the 4-vertex tetrahedral dual-volume partition and zero-momentum kinetic vanishing (`single_tetrahedron_zero_momentum_replay`) and the null/negative-mode indefinite signature of the discrete DeWitt kinetic quadratic form (`dewitt_kinetic_null_and_negative_modes`).
3. **Scope Fences ($\Lambda$ Underdetermination, 3D Scaling Mismatch, and Multi-Hinge Cancellation)**: proves that caller-supplied $\lambda$ is underdetermined by both discrete operators (`hamiltonian_lambda_underdetermination`, `regge_edge_lambda_underdetermination`), uniform 3D edge rescaling $\ell \mapsto s\ell$ breaks static Hamiltonian balance with residual $U_v s(s^2 - 1)$ (`static_hamiltonian_scaling_mismatch`), and two hinges with opposite nonzero deficits $(+\delta, -\delta)$ cancel in the edge curvature gradient while retaining positive squared deficit $2\delta^2 > 0$ (`two_hinge_curvature_grad_cancellation_fence`, `two_hinge_deficit_zero_iff_sq_norm_zero`).

### Governing Obligation
GAP: Einstein equation and physical cosmological constant stay unpaid; deficit is not smooth curvature.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Formalization
- [`lean4/FieldEquationConstraintReplay.lean`](../../../lean4/FieldEquationConstraintReplay.lean):
  - `FieldEquationConstraintReplay.regge_edge_residual_zero_iff`
  - `FieldEquationConstraintReplay.flat_interior_regge_residual_replay`
  - `FieldEquationConstraintReplay.regge_relaxation_fixed_point_iff`
  - `FieldEquationConstraintReplay.single_tetrahedron_zero_momentum_replay`
  - `FieldEquationConstraintReplay.dewitt_kinetic_null_and_negative_modes`
  - `FieldEquationConstraintReplay.hamiltonian_lambda_underdetermination`
  - `FieldEquationConstraintReplay.regge_edge_lambda_underdetermination`
  - `FieldEquationConstraintReplay.static_hamiltonian_scaling_mismatch`
  - `FieldEquationConstraintReplay.two_hinge_curvature_grad_cancellation_fence`
  - `FieldEquationConstraintReplay.two_hinge_deficit_zero_iff_sq_norm_zero`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/general_relativity/field_equation.rs`](../../code/rust/src/)
- [`code/rust/src/general_relativity/hamiltonian_constraint.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`checks/independent/tfq-0107.py`](../../../checks/independent/tfq-0107.py) (`checks=825 regge=225 ham=100 fence=500 failures=0`)
- [`dag/derivations/independent/tfq-0107.md`](../independent/tfq-0107.md)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0108](tfq_0108_gap_caller_supplied_lambda_is_not_the_physical_cosmological_constant_and_the_grid.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:6c3ddd228c139e91dd74dc2ea348d97cc54608a0`
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
