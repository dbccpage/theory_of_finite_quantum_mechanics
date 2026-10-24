# [TFQ-0543] wdp-incidence-orientation-transport

> **Stage**: `WDP` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `f37c8c13-16b2-5692-94eb-e7cc41619357`  
> **Parent Derivation**: [TFQ-0542](tfq_0542_wdp_graph_cochain_host.md)

---

## 1. Abstract & Formal Statement

On the one triangle with vertices 0, 1, 2, swapping Genesis edge slots (01, 02, 12) into WDP slots (01, 12, 02) is an involution; the admitted face column (1, -1, 1) becomes (1, 1, -1), matching triD1Row, and negating the 02 component sends that triple to (1, 1, 1). The swapped column has vertex boundary 0 at each vertex, triD1 of triD0 is 0 for every rational vertex triple, and triD1 of the swapped face row is 3.

### Governing Obligation
The finite check on vertices 0, 1, 2 records the slot swap from (01, 02, 12) to (01, 12, 02), the face column from (1, -1, 1) to (1, 1, -1), the 02 sign change to (1, 1, 1), vertex boundary 0, and triD1 of triD0 equal to 0. A coordinate transport for a general window, with d0 and d1 the transposes of the boundary maps, stays open.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Further Prerequisites
- [TFQ-0460](../02_genesis/tfq_0460_incidence_construction_betti.md) incidence-construction-betti

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Neither file states a general transport of window quantities, and monograph invariance under reorientation stays open. boundary_boundary_filled is a chain-level fact in the incidence edge order (01, 02, 12); the incidence construction (TFQ-0460) does not derive the WDP window from Genesis admission (TFQ-0344); the Python orientation test stays inside the WDP convention. The vertex cycle of the swapped face column is separate from triD1 of that row, which equals 3. A declared map for a general cochain, and a theorem that d0 and d1 of the whole WDP window are the transposes of the Genesis boundary maps, stay open.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/CampaignPgwWdpIncidenceOrientationTransport.lean::pgwInc_d1_d0`](../../../lean4/CampaignPgwWdpIncidenceOrientationTransport.lean)
- [`lean4/CampaignPgwWdpIncidenceOrientationTransport.lean::pgwInc_face_cyclic`](../../../lean4/CampaignPgwWdpIncidenceOrientationTransport.lean)
- [`lean4/CampaignPgwWdpIncidenceOrientationTransport.lean::pgwInc_face_is_row`](../../../lean4/CampaignPgwWdpIncidenceOrientationTransport.lean)
- [`lean4/CampaignPgwWdpIncidenceOrientationTransport.lean::pgwInc_face_swapped`](../../../lean4/CampaignPgwWdpIncidenceOrientationTransport.lean)
- [`lean4/CampaignPgwWdpIncidenceOrientationTransport.lean::pgwInc_face_tri`](../../../lean4/CampaignPgwWdpIncidenceOrientationTransport.lean)
- [`lean4/CampaignPgwWdpIncidenceOrientationTransport.lean::pgwInc_swap_involutive`](../../../lean4/CampaignPgwWdpIncidenceOrientationTransport.lean)
- [`lean4/CampaignPgwWdpIncidenceOrientationTransport.lean::pgwInc_transported_cycle`](../../../lean4/CampaignPgwWdpIncidenceOrientationTransport.lean)
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
  - `lean4/CampaignPgwWdpIncidenceOrientationTransport.lean:92-96`
  - `dag/derivations/independent/pgw-wdp-incidence-orientation-transport.md:1`
  - `dag/research/campaign_pgw-wdp-incidence-orientation-transport_lean_replay.json:2-4`
