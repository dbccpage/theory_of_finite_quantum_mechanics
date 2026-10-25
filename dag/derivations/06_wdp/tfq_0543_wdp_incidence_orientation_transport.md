# [TFQ-0543] wdp-incidence-orientation-transport

> **Stage**: `WDP` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `f37c8c13-16b2-5692-94eb-e7cc41619357`  
> **Parent Derivation**: [TFQ-0542](tfq_0542_wdp_graph_cochain_host.md)

---

## 1. Abstract & Formal Statement

Narrowed in Lean 4 to one triangle. Incidence edges (01, 02, 12) reorder to (01, 12, 02) by sending (a, b, c) to (a, c, b). The face column (1, -1, 1) becomes (1, 1, -1), and the incidence boundary of that column is (0, 0, 0). Dot products with the incidence columns, read in the order 01, 12, 02, equal the coboundary (f1 - f0, f2 - f1, f2 - f0). The evaluation x01 + x12 - x02 vanishes on every such coboundary, agrees with the cyclic sum that stores edge 20 as the negation of edge 02, and sends (1, 1, 0) to 2. The unit-weight residual of (1, 1, 0) equals 2 at vertex values (0, 1, 0) and is at least 2 for every integer vertex triple. A transport for every window quantity, a derivation of the WDP window from Genesis admission, and the external orientation test stay open.

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
- [`lean4/CampaignPgwWdpIncidenceTransport.lean::defect_charge`](../../../lean4/CampaignPgwWdpIncidenceTransport.lean)
- [`lean4/CampaignPgwWdpIncidenceTransport.lean::face_reorders`](../../../lean4/CampaignPgwWdpIncidenceTransport.lean)
- [`lean4/CampaignPgwWdpIncidenceTransport.lean::incidence_face_boundary_zero`](../../../lean4/CampaignPgwWdpIncidenceTransport.lean)
- [`lean4/CampaignPgwWdpIncidenceTransport.lean::residual_at_least_two`](../../../lean4/CampaignPgwWdpIncidenceTransport.lean)
- [`lean4/CampaignPgwWdpIncidenceTransport.lean::residual_at_repair`](../../../lean4/CampaignPgwWdpIncidenceTransport.lean)
- [`lean4/CampaignPgwWdpIncidenceTransport.lean::reverse_edge_20`](../../../lean4/CampaignPgwWdpIncidenceTransport.lean)
- [`lean4/CampaignPgwWdpIncidenceTransport.lean::transport_matches_transpose`](../../../lean4/CampaignPgwWdpIncidenceTransport.lean)
- [`lean4/CampaignPgwWdpIncidenceTransport.lean::wdp_d1_d0`](../../../lean4/CampaignPgwWdpIncidenceTransport.lean)
- [`lean4/Imported/OeWdp/GenesisIncidence.lean::boundary_boundary_filled`](../../../lean4/Imported/OeWdp/GenesisIncidence.lean)
- [`lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean::triD1`](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust transport between the GenesisIncidence boundary convention and the WDP coboundary window`

### Python Oracles & Numerical Evaluators
- [`checks/independent/pgw-wdp-incidence-orientation-transport.py::main`](../../../checks/independent/pgw-wdp-incidence-orientation-transport.py)
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
  - `dag/derivations/independent/pgw-wdp-incidence-orientation-transport.md:5`
  - `dag/research/campaign_pgw-wdp-incidence-orientation-transport_lean_replay.json:6`
