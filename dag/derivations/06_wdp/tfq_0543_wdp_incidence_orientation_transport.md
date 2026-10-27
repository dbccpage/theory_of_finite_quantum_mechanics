# [TFQ-0543] wdp-incidence-orientation-transport

> **Stage**: `WDP` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `f37c8c13-16b2-5692-94eb-e7cc41619357`  
> **Parent Derivation**: [TFQ-0542](tfq_0542_wdp_graph_cochain_host.md)

---

## 1. Abstract & Formal Statement

GenesisIncidence.lean reads the declared incidence complex on vertices 0, 1, 2 with signed boundary maps on the edge basis (01, 02, 12), the admitted face 012 entering as the column (1, −1, 1), and establishes that the boundary of that face has zero boundary (boundary_boundary_filled). The WDP window instead uses coboundaries with the simplicial edge order (01, 12, 02), d₀f = (f₁ − f₀, f₂ − f₁, f₂ − f₀) and d₁x = x₀₁ + x₁₂ − x₀₂ (Obstruction.lean), while the cyclic presentation (01, 12, 20) negates the reversed component. The monograph states that every window quantity is invariant once the cochain is transported with its edges, but no declared map takes the GenesisIncidence chains, with their edge order and boundary convention, to the WDP cochain window.

### Governing Obligation
Declare and check the transport from GenesisIncidence's boundary convention on (01, 02, 12) to the WDP coboundary convention on (01, 12, 02): a coordinate permutation after which d0 and d1 are the transposes of the boundary maps, with a sign for any edge reoriented as 20, verified by d1 d0 = 0 and the filled-triangle signature after transport. A transport for every window quantity, a derivation of the WDP window from Genesis admission, and the external orientation test stay open.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Further Prerequisites
- [TFQ-0460](../02_genesis/tfq_0460_incidence_construction_betti.md) incidence-construction-betti

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Open. One triangle is transported. The reorder, the transpose identity, the sign for edge 20, the charge 2, and the residual lower bound 2 are checked. A transport for every window quantity, a derivation of the WDP window from Genesis admission, and the external orientation test stay open.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean::triD1`](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean)
- [`lean4/Imported/WitnessedDifferenceProgramme/GenesisIncidence.lean::boundary_boundary_filled`](../../../lean4/Imported/WitnessedDifferenceProgramme/GenesisIncidence.lean)
- [`lean4/PregenesisWdpIncidenceTransport.lean::defect_charge`](../../../lean4/PregenesisWdpIncidenceTransport.lean)
- [`lean4/PregenesisWdpIncidenceTransport.lean::face_reorders`](../../../lean4/PregenesisWdpIncidenceTransport.lean)
- [`lean4/PregenesisWdpIncidenceTransport.lean::incidence_face_boundary_zero`](../../../lean4/PregenesisWdpIncidenceTransport.lean)
- [`lean4/PregenesisWdpIncidenceTransport.lean::residual_at_least_two`](../../../lean4/PregenesisWdpIncidenceTransport.lean)
- [`lean4/PregenesisWdpIncidenceTransport.lean::residual_at_repair`](../../../lean4/PregenesisWdpIncidenceTransport.lean)
- [`lean4/PregenesisWdpIncidenceTransport.lean::reverse_edge_20`](../../../lean4/PregenesisWdpIncidenceTransport.lean)
- [`lean4/PregenesisWdpIncidenceTransport.lean::transport_matches_transpose`](../../../lean4/PregenesisWdpIncidenceTransport.lean)
- [`lean4/PregenesisWdpIncidenceTransport.lean::wdp_d1_d0`](../../../lean4/PregenesisWdpIncidenceTransport.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust transport between the GenesisIncidence boundary convention and the WDP coboundary window`

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_obstruction.py::test_reversed_edge_orientation_changes_signs_not_the_signature`](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_obstruction.py)
- [`checks/independent/pgw-wdp-incidence-orientation-transport.py::main`](../../../checks/independent/pgw-wdp-incidence-orientation-transport.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `lean4/Imported/WitnessedDifferenceProgramme/GenesisIncidence.lean:19-23`
  - `lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean:291-293`
  - `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md:1478-1483`
  - `dag/derivations/independent/pgw-wdp-incidence-orientation-transport.md:5`
  - `dag/research/campaign_pgw-wdp-incidence-orientation-transport_lean_replay.json:6`
