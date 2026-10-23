# [TFQ-0543] wdp-incidence-orientation-transport

> **Stage**: `WDP` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `f37c8c13-16b2-5692-94eb-e7cc41619357`  
> **Parent Derivation**: [TFQ-0542](tfq_0542_wdp_graph_cochain_host.md)

---

## 1. Abstract & Formal Statement

GenesisIncidence.lean reads the declared incidence complex on vertices 0, 1, 2 with signed boundary maps on the edge basis (01, 02, 12), the admitted face 012 entering as the column (1, −1, 1), and establishes that the boundary of that face has zero boundary (boundary_boundary_filled). The WDP window instead uses coboundaries with the simplicial edge order (01, 12, 02), d₀f = (f₁ − f₀, f₂ − f₁, f₂ − f₀) and d₁x = x₀₁ + x₁₂ − x₀₂ (Obstruction.lean), while the cyclic presentation (01, 12, 20) negates the reversed component. The monograph states that every window quantity is invariant once the cochain is transported with its edges, but no declared map takes the GenesisIncidence chains, with their edge order and boundary convention, to the WDP cochain window.

### Governing Obligation
Declare and check the transport from GenesisIncidence's boundary convention on (01, 02, 12) to the WDP coboundary convention on (01, 12, 02): a coordinate permutation after which d₀ and d₁ are the transposes of the boundary maps, with a sign for any edge reoriented as 20, verified by d₁d₀ = 0 and the filled-triangle signature after transport.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Further Prerequisites
- [TFQ-0460](../02_genesis/tfq_0460_incidence_construction_betti.md) incidence-construction-betti

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Neither file states the transport; boundary_boundary_filled is a chain-level fact in the incidence edge order, the incidence construction (TFQ-0460) does not derive the WDP window from Genesis admission (TFQ-0344), and the orientation test in Python stays inside the WDP convention.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/OeWdp/GenesisIncidence.lean::boundary_boundary_filled`](../../../lean4/Imported/OeWdp/GenesisIncidence.lean)
- [`lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean::triD1`](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust transport between the GenesisIncidence boundary convention and the WDP coboundary window`

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/unit_tests/test_obstruction.py::test_reversed_edge_orientation_changes_signs_not_the_signature`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/unit_tests/test_obstruction.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `lean4/Imported/OeWdp/GenesisIncidence.lean:19-23`
  - `lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean:291-293`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md:1478-1483`
