# SO(k)-Invariant Gauge Rigidity for Declared Euclidean Stalks: Local ℓ² Selection and Outer ℓ¹ Aggregation (GS-002)

Subtitle: Structural Rigidity, Mixed-Norm Cohomological Obstruction Duality, and Finite Anomaly Separation

## Abstract

In categorical and cohomological obstruction theory over finite cell complexes, diagnostic metrics measure the failure of local data to patch into global sections. For scalar-valued cochains, maximal linear-functional symmetry combined with edge-decomposable aggregation uniquely singles out the ℓ¹ coboundary norm. This paper analyzes the geometric regime where cochain edge defects take values in finite-dimensional vector stalks ℝ^k (for dimension k ≥ 2) equipped with declared continuous rotational symmetry SO(k).

We establish an explicit two-part structural boundary for vector-valued obstruction diagnostics:

1. Local Rigidity: Declaring continuous rotational invariance SO(k) on Euclidean stalks uniquely forces each local gauge to be strictly proportional to the Euclidean norm ℓ² (Theorem 3.1).
2. Outer Aggregation: Theorem 3.2 is conditional/definitional. Once the strong edgewise rule J(ω) = ∑_{e ∈ E} j_e(ω_e) is declared, substituting the local rigidity factors produces J_{2,1,c}(ω) = ∑_{e ∈ E} c_e ‖ω_e‖₂. SO(k) symmetry alone does not supply the outer sum.

We formulate the quotient obstruction problem Φ_{2,1,c}([ω]) = inf_α ∑_{e ∈ E} c_e ‖ω_e − (d₀ α)_e‖₂ as a second-order cone program (SOCP) and prove its Lagrange dual representation (Theorem 4.2): dual witnesses are divergence-free vector circulations (d₀* φ = 0) satisfying local Euclidean ball bounds ‖φ_e‖₂ ≤ c_e. We extend this geometry to 2-cell complexes, establishing the mixed closure bound Γ_{2,1,u}([h]) ≤ ‖d₁‖ Φ_{2,1,c}([h]) (Theorem 6.1). Finally, we demonstrate that coordinate-separable scalar observers and SO(k)-invariant vector observers assign strictly separated obstruction values of 2 and √2 to the identical cycle class on a minimal directed triangle network (Theorem 5.2).

## Why This Matters

In distributed optimization, structural mechanics, network flow calibration, and topological data analysis, defect fields frequently appear as multi-channel vector residuals—such as displacement anomalies, force-balance mismatches, or multi-sensor calibration errors. Practitioners face a primary modeling choice: evaluate vector components independently via coordinate-wise norms (such as coordinate ℓ¹) or treat them as unified geometric vectors under rotational invariance.

This paper identifies the exact observer axiom that licenses the Euclidean treatment: continuous SO(k) rotational invariance of the local gauge. It explicitly decouples that internal symmetry choice from the outer network aggregation logic, establishing that ℓ¹(E; ℓ²) is a conditional observer geometry rather than a global metric. Furthermore, it provides floating-point primal-dual candidates with explicit tolerance checks; the analytical theorem, numerical diagnostics, and exact Lean kernels have separate evidentiary scopes.

## Core Theorems

- Theorem 3.1 (SO(k) Invariance Forces the Euclidean Local Gauge): Let k ≥ 2 and let j: ℝ^k → [0, ∞) be a faithful, absolutely homogeneous, convex gauge. If j is invariant under the standard action of SO(k) on ℝ^k (that is, j(Rx) = j(x) for all R ∈ SO(k)), then j is strictly proportional to the standard Euclidean norm: j(x) = c ‖x‖₂ for some constant c > 0.
- Theorem 3.2 (Weighted Mixed Norm Under Declared Strong Edge Aggregation): Let G = (V, E) be a finite directed graph with edge defects in ℝ^k (k ≥ 2). If each local edge gauge satisfies the local rigidity hypotheses and the global diagnostic is explicitly declared to be J(ω) = ∑_{e ∈ E} j_e(ω_e), then substitution gives J_{2,1,c}(ω) = ∑_{e ∈ E} c_e ‖ω_e‖₂. The unweighted form holds only when edge-exchange equivalence and singleton normalization are also declared.
- Theorem 4.2 (Mixed Vector Obstruction Duality): For any finite directed graph G = (V, E) with vector edge defects and positive edge weights c_e > 0, the primal quotient obstruction inf_α ∑_{e ∈ E} c_e ‖ω_e − (d₀ α)_e‖₂ achieves strong duality with the convex dual problem max_φ ∑_{e ∈ E} ⟨φ_e, ω_e⟩, subject to the gauge-invariance constraint d₀* φ = 0 (divergence-free vector circulation) and the weighted Euclidean bounds ‖φ_e‖₂ ≤ c_e for all e ∈ E.
- Theorem 5.2 (Finite Triangle-Anomaly Separation): On a normalized directed 3-cycle with edge defect circulation c = (1, 1), a coordinate-separable scalar observer measures an obstruction magnitude of Φ_{1,1} = 2, whereas an SO(2)-invariant vector observer measures an obstruction magnitude of Φ_{2,1} = √2. This demonstrates that local observer symmetry alters the perceived topological obstruction on finite networks. In formal verification, this separation is certified over the rationals by the algebraic inequality 2² ≠ 2 (that is, 4 ≠ 2 in ℚ).
- Theorem 6.1 (Mixed Closure Bound): For any finite obstruction complex C⁰ → C¹ → C² with boundary nilpotency d₁ d₀ = 0, the 2-cell failure metric Γ_{2,1,u}([h]) = ‖d₁ h‖_{1,2,u} satisfies Γ_{2,1,u}([h]) ≤ ‖d₁‖_{(1,2,c)→(1,2,u)} Φ_{2,1,c}([h]), bounding higher-dimensional curvature defects by lower-dimensional quotient repair norms.

## Formal Verification and Computational Artifacts

- Formal Lean 4 Mechanization: Package `gs002` contains one import root and seven theorem modules under Lean 4 toolchain `v4.34.0-rc1`. Every theorem and lemma declaration is explicitly censused; the fresh receipt reports zero `sorry`, zero `admit`, and only the scoped standard kernel axiom allowlist.
- Computational Reference Engine: The self-contained Python engine implements finite graph cochain complexes in floating-point arithmetic, numerical SOCP/subspace certifiers, and analytical single-cycle routines. Use the fresh full-suite coverage command as the evidence; no mutable test total is asserted here.
- Interactive Verification Notebooks: Standalone Jupyter review notebooks demonstrating SOCP duality gap closure, triangle separation replays, and parameter sweeps headlessly under nbclient without ambient external dependencies.

## Scope Boundaries and Non-Claims

- Declared Discrete Complex: All results are established strictly on finite directed 1-skeleta (graphs) and 2-complexes; no claims are made regarding continuous Riemannian manifolds, continuum Yang-Mills gauge fields, or smooth differential forms.
- Declared Local Symmetry: Theorem 3.1 holds when the stalk is declared to carry a Euclidean inner product and the action of SO(k) is transitive on the Euclidean unit sphere. For non-transitive representations or discrete subgroup symmetries, broad families of non-Euclidean invariant gauges exist.
- Conditional Outer Aggregation: The outer ℓ¹ sum is not an automatic mathematical consequence of internal SO(k) symmetry; it requires independent observer declarations of edge decomposability and disjoint additivity.
- Excised Conjectures: Non-Abelian holonomy inequalities (§5.3.1 of earlier drafts) and heuristic McLachlan projections (§5.3.3) are recognized as uncertified or false in this general setting and are strictly excluded from the certified claim set.

## Reproduction

Execute test suites, linters, and verification builds directly:

```bash
# Install dependencies
pip install -e .

# Run the current complete test suite and configured coverage gate
python -m pytest code/tests -n 8

# Run code linters
ruff check code/
mypy code/

# Build and verify Lean 4 formal proofs
cd lean4 && lake build GS002
```

## Related Identifiers & Citations

- Canonical Monograph: _SO(k)-Invariant Gauge Rigidity for Declared Euclidean Stalks: Local ℓ² Selection and Outer ℓ¹ Aggregation_ (Version v2.0.0, 2026-09-21)
- Zenodo Deposit: Concept DOI 10.5281/zenodo.20683681
- Upstream Derivation: CODA Research Programme
- Companion Literature: _M-Compatible Gauge Classification for Banach Presheaf Coboundaries: The ℓ¹ Maximal-Symmetry Endpoint_ (Zenodo record 20677155, Concept DOI: 10.5281/zenodo.18897080)
