# [TFQ-0184] Do not read paper 009 reflexivity declarations as measured tetron homology

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `2e873733-5133-5d75-9759-7b5e3584f9e2`  
> **Parent Derivation**: [TFQ-0181](tfq_0181_keep_tfqm_majorana_a_gf_2_diagnostic_and_do_not_treat_it_as_an.md)

---

## 1. Abstract & Formal Statement

Paper 009 README title is 026_microsoft_majorana_problem: Majorana Parity Obstruction Calculus & Topological Computing Apparatus. That README says Lean gaussian_elimination_cubic_bound is Nat.le_refl of n times n times n, and that enum rfl declarations are not measured tetron homology. The F004 register calls the program a Majorana realization-packet gap and says noise sweeps are a separate program. The obligation is to withhold a tetron-homology reading from those reflexivity declarations. majorana_evaluator.py is a companion control, not a closure of that gap.

The paragraph above stays the open reading. A later Nat module, `lean4/CubicReflexivityCount.lean`, checks a narrower count and does not discharge that reading. For every natural number n, n * n * n is at most n * n * n. For every natural number n at least 1, twice the cube equals (n - 1) * n * (2 * n - 1) plus n * (3 * n - 1), that first product is strictly below twice the cube, and the gap n * (3 * n - 1) is at least 2. At n = 4 the cube is 64, the sum 1 * 1 + 2 * 2 + 3 * 3 is 14, the quotient (3 * 4 * (2 * 4 - 1)) / 6 is 14, and 14 is strictly below 64. Status stays OPEN.

### Governing Obligation
Do not read paper 009 reflexivity declarations as measured tetron homology.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Syntactic Reflexivity vs Actual Elimination & Homology Computation**: `Nat.le_refl (n*n*n)` is a tautological inequality $n^3 \le n^3$, whereas actual $n \times n$ Gaussian elimination row-operation counts follow $\sum_{k=1}^{n-1} k^2 = \frac{(n-1)n(2n-1)}{6} < \frac{n^3}{3}$; similarly, enum `rfl` declarations do not compute $\dim H_1 = (|C_1| - \operatorname{rank}_{\mathbb{F}_2}(d_1)) - \operatorname{rank}_{\mathbb{F}_2}(d_0)$ and are not measured tetron homology.
- **Companion Control Scope of `majorana_evaluator.py`**: `code/python/src/majorana/majorana_evaluator.py` re-exports finite algebraic companion controls (`F2CochainComplex`, `build_tetron_carrier`, `verify_norm_equivalence`, `KitaevSweetSpotChain`, `IsingFusionAlgebra`, `ParityAlgebraModel`) under `AuthorityEffect: None`, while the `F004` Majorana realization-packet gap remains open and separate from noise sweeps.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `lean4/MajoranaEvaluatorControls.lean`:
  - `MajoranaEvaluatorControls.gaussian_elimination_exact_flop_count_vs_cubic_reflexivity_bound`
  - `MajoranaEvaluatorControls.tetron_gf2_homology_requires_boundary_rank_difference_not_enum_rfl`
  - `MajoranaEvaluatorControls.kitaev_sweet_spot_boundary_isolation_and_ising_quantum_dimensions`
  - `MajoranaEvaluatorControls.fermion_parity_involutive_sector_splitting`
  - `MajoranaEvaluatorControls.binary_carrier_lp_norm_equals_hamming_weight`
  - `MajoranaEvaluatorControls.reflexivity_declaration_is_not_measured_tetron_homology_fence`
  - `MajoranaEvaluatorControls.f004_realization_packet_gap_remains_open_and_separate_from_noise_sweeps_fence`
  - `MajoranaEvaluatorControls.majorana_evaluator_is_companion_control_not_gap_closure_fence`
  - `MajoranaEvaluatorControls.wdp_carrier_manifest_homology_conversion_fence`
  - `MajoranaEvaluatorControls.tfq0184_paper009_reflexivity_and_evaluator_scope_ledger_fence`
- `lean4/CubicReflexivityCount.lean` (narrower Nat count; does not discharge the open reading above):
  - `CubicReflexivityCount.cubicReflexivity`
  - `CubicReflexivityCount.eliminationSplit`
  - `CubicReflexivityCount.gapAtLeastTwo`
  - `CubicReflexivityCount.eliminationBelowTwiceCube`
  - `CubicReflexivityCount.fourCube`
  - `CubicReflexivityCount.fourSumOfSquares`
  - `CubicReflexivityCount.fourClosedForm`
  - `CubicReflexivityCount.fourCountBelowCube`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `code/rust/src/wdp/lib.rs`:
  - `to_homology_carrier`

### Python Oracles & Numerical Evaluators
- `code/python/src/majorana/majorana_evaluator.py`:
  - `KitaevSweetSpotChain`
  - `IsingFusionAlgebra`
  - `ParityAlgebraModel`
- `checks/independent/tfq-0184.py`:
  - `run_all_checks`

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `lean4/MajoranaEvaluatorControls.lean`
  - `code/rust/src/wdp/lib.rs`
  - `code/python/src/majorana/majorana_evaluator.py`
  - `checks/independent/tfq-0184.py`
