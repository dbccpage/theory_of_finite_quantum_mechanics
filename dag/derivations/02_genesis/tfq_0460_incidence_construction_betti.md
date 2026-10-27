# [TFQ-0460] incidence-construction-betti

> **Stage**: `GENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `b147c458-1a51-504d-9aa1-d6b262f69ead`  
> **Parent Derivation**: [TFQ-0455](tfq_0455_d2_initial_pointed.md)

---

## 1. Abstract & Formal Statement

Starting from the literal supply of <>, the WDP construction records Supply(<>) without admitting it, then supplies and admits <a>, <ab> and <c>, forms of arities 1, 2 and 3, three unary vertex instances and the edges 01, 12 and 02. Under an explicitly chosen incidence interpretation (a datum's admission index is a vertex, an arity-k form carries (k−1)-dimensional simplices, an instance lists its increasing vertex indices, and every vertex and face needs its own instance) the cycle has rational Betti numbers (1, 1), and admitting the single instance 012 gives (1, 0, 0). The education Lean module establishes these Betti numbers from explicit integer kernels and images of the boundary matrices (cycle_rational_betti, filled_rational_betti) and that its incidence reading returns the cycle and filled simplex lists (cycle_incidence_eq, filled_incidence_eq). For a general face-closed family K, that the construction's interpretation is exactly K rests on a written argument.

### Governing Obligation
Replay the literal-root walk, read admitted instances as simplices under the declared interpretation, and compute rational Betti numbers (1, 1) for the cycle and (1, 0, 0) after the filling.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared incidence interpretation of admitted forms and instances as simplices, incidence_construction.txt (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The interpretation is a construction choice, not extracted from the spelling of <>; the general construction result is a written argument, the Lean covers the worked three-vertex complex only, and no Lean refinement of the Rust implementation is claimed.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/WitnessedDifferenceProgramme/GenesisIncidence.lean::cycle_incidence_eq`](../../../lean4/Imported/WitnessedDifferenceProgramme/GenesisIncidence.lean)
- [`lean4/Imported/WitnessedDifferenceProgramme/GenesisIncidence.lean::cycle_rational_betti`](../../../lean4/Imported/WitnessedDifferenceProgramme/GenesisIncidence.lean)
- [`lean4/Imported/WitnessedDifferenceProgramme/GenesisIncidence.lean::filled_incidence_eq`](../../../lean4/Imported/WitnessedDifferenceProgramme/GenesisIncidence.lean)
- [`lean4/Imported/WitnessedDifferenceProgramme/GenesisIncidence.lean::filled_rational_betti`](../../../lean4/Imported/WitnessedDifferenceProgramme/GenesisIncidence.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `external:sha256:2252c69f4bba9c28eb9ab8a435a9a62ed96fb8314f053e8de431be4b50ed2526::cycle_construction` (private upstream source, not in this repository)
- `external:sha256:2252c69f4bba9c28eb9ab8a435a9a62ed96fb8314f053e8de431be4b50ed2526::homology` (private upstream source, not in this repository)

### Python Oracles & Numerical Evaluators
- `missing obligation: no Python implementation of the incidence reading or its homology`

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/paper.md:535-540`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/incidence_construction.txt:31-44`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/incidence_construction.txt:57-64`
