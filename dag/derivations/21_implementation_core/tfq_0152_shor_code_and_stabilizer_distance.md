# [TFQ-0152] Shor code and stabilizer distance

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `4bb8efcd-9534-58a8-969b-8fbe13b8e0b1`  
> **Parent Derivation**: [TFQ-0151](tfq_0151_grover_reflections_and_quantum_walks.md)

---

## 1. Abstract & Formal Statement

Covers shor.rs, stabilizer_code_distance.rs, toric_code.rs, cochain_repair_code.rs, repair_capacity.rs, and threshold_repair_certificate.rs. shor.rs is the Shor nine-qubit code in exact binary Pauli algebra, with syndrome extraction and recovery of the 27 single-qubit Pauli errors. It is a code control, not a factoring procedure. The other files compute stabilizer distance, a rectangular toric CSS code with no asserted gap, and conditional repair bounds. A Python replay and a Lean 4 declaration would still have to match the nine-qubit syndrome table.

### Governing Obligation
Match the nine-qubit stabilizer syndrome table and recovery of the 27 single-qubit Pauli errors.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: no local lean twin located for lean4/quantum_mechanics`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:b62ab9003d85d1d44d2f6bcc176b2080054e652534be2615f0c777c319030676`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:5e3fd1edf72e8f1056c51c5b5e86bf5fc82f8d203f4cff925ce19857eb4c8be7`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:18a4dc1ca3a6770620ae1052c15115527d101914c7a984bc359605f26fd06034`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:0afca57b5b9d44930fdafc79b2199989c1617b63981a2718bcfd3960a957dfd0`](../../code/rust/src/)
- [`code/rust/src/majorana/repair_capacity.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:1278d82569648290cc95532c1c1d6376f6b9aa07b98e04d267d8b32906fdaad9`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`code/python/src/majorana/tests/support/finite_qm/use_cases/stabilizer_codes.py`](../../code/python/)
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
