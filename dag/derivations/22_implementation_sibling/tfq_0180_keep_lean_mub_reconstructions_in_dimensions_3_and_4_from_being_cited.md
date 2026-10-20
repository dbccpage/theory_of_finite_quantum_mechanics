# [TFQ-0180] Keep Lean MUB reconstructions in dimensions 3 and 4 from being cited

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `bead05bb-328f-55c6-8b89-b2b4f99e2e14`  
> **Parent Derivation**: [TFQ-0177](tfq_0177_leave_the_existence_of_seven_mutually_unbiased_bases_in_dimension_6_open.md)

---

## 1. Abstract & Formal Statement

Lean MUB files in quantum_mechanics reconstruct small dimensions and do not close dimension 6. H050MubTomographyInversion.lean states four mutually unbiased bases in dimension 3 under exact rational inversion. H051Mub4GaloisFieldContextuality.lean states five in dimension 4 over GF(4). H030OctahedralMubCliftonKent.lean is an integer octahedron frame, not a d=6 census. H062CompositionTensorMub.lean says product-MUB counts are recorded inputs and an exhaustive d=6 MUB theorem is not established. The obligation is to leave that d=6 question on the open node.

### Governing Obligation
Keep Lean MUB reconstructions in dimensions 3 and 4 from being cited as a dimension-6 existence result.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/H050MubTomographyInversion.lean`](../../lean4/)
- [`lean4/H051Mub4GaloisFieldContextuality.lean`](../../lean4/)
- [`lean4/H030OctahedralMubCliftonKent.lean`](../../lean4/)
- [`lean4/H062CompositionTensorMub.lean`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/wdp/lib.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
