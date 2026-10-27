# [TFQ-0258] Qubit not derived from the bit-shadow

> **Stage**: `FINITE_QM_STRUCTURE` | **Status**: `GAP`  
> **UUID**: `be89867a-1ff9-56d8-b278-f8cbd87f4906`  
> **Parent Derivation**: [TFQ-0257](tfq_0257_separability_witness_relative_to_a_declared_family.md)

---

## 1. Abstract & Formal Statement

QM_072 corrects the hoped identity between a two-locus bit-shadow and a qubit. The opened main claim says the two-locus one-edge carrier supports a bit-shadow, that three minimality readings disagree, and that four imports separate the bit-shadow from a qubit: a phase fiber, an l2 readout, contextual operator structure, and continuous reversible dynamics. The non-claim box says no qubit, Hilbert space, Bloch sphere, Born pairing, or measurement postulate is derived. The derivation-graph reading note lists the qubit node with the Bell-theorem node as a place where no derivation was found.

### Governing Obligation
Record the bit-shadow and the Q1-Q4 import list, and do not treat that list as a derivation of a qubit.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> None (obstruction and import-separation theorem P7-C1..C10 mechanized in ds_qm072_bit_shadow_q1_q4_obstruction_and_p7_c10_bloch_refutation and ds_qm072_and_c10_hadamard_coherence_separation_vs_pinched_mixture).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/DerivationDagQMClosure.lean`](../../lean4/)

### Sovereign Rust Certifiers
*Computational witness tracked under `theory_of_finite_qm` crate.*

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
