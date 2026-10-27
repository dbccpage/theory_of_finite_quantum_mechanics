# [TFQ-0240] Ungraded overcount and multiplicative gauge residual

> **Stage**: `FINITE_QM_DYNAMICS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `fb49c9d5-abad-580b-8890-00fb8d7cde11`  
> **Parent Derivation**: [TFQ-0239](tfq_0239_finite_path_sum_on_a_unique_intermediate_cut.md)

---

## 1. Abstract & Formal Statement

The same QM_030 redirect records two corrections that the path-sum obligation must keep. Splitting one history at every vertex counts it more than once, while a fixed intermediate cut counts it once, and a vanishing first cohomology group does not certify unique counting. Exponentiating an angle cochain also loses integral periods: multiplicative weights can be gauge-trivial while the angle assignment still needs an integer winding. The retained criterion is trivial phase holonomy around every cycle. Endpoint potentials telescope; a general additive action need not be an exact coboundary.

### Governing Obligation
Refuse ungraded multi-cut counting and the forward exponentiation test as certificates of unique histories or trivial phase holonomy.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `commutative semiring of weights (assumption)`
- **Admitted**: `finite fibers (assumption)`
- **Admitted**: `grading / time-slicing of the category (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Single finite witness; role is to show grading is needed.

> [!WARNING]
> Lean file FinitePathSum.lean cited by QM-031 not located by me under lean4/quantum_mechanics; the WDP SemiringTransport lemma is the only receipted algebra I could check.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/DerivationDagQMClosure.lean`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:f51cea05c639d8d39b42c50d466f3fdf2ef0bb52291a1196d9ff27bc5e4111a1`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
