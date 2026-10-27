# [TFQ-0493] four-gate-active-obstruction

> **Stage**: `GENESIS` | **Status**: `DEFINITION`  
> **UUID**: `4d46dc1e-1af7-5eb6-8ecc-df675e9be6c0`  
> **Parent Derivation**: [TFQ-0492](tfq_0492_candidate_extension_generator.md)

---

## 1. Abstract & Formal Statement

Declared here as the test a residual must pass before it counts as an active obstruction: obstP = retainedP ∧ protectedP ∧ declaredP ∧ zeroDeclP, that is, the pair is retained in the witness store, carries a protected demand, an observation is declared, and the declared observation does not separate the pair. In the sealed passage system this is an identity of Bool-valued functions at every state and pair (PrimitivePassage.obstP_factors), with sufficiency obst_of_gates and necessity gates_of_obst; the source calls the factorization near-definitional, gives the four-way reading content through the four gate_*_independent theorems, and refutes joint freedom of the gates (obs_gates_not_both_false). zeroDeclP answers true before any observation by a declared convention that never makes anything obstructed (obst_requires_observation). The education module MssnObstructionDetector restates the factorization over supplied observation columns.

### Governing Obligation
Report a residual as an active obstruction only when all four gates hold at the stated state and pair, and keep a collapsed pair that fails a gate as an observation, not a demand.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Necessity is relative to this predicate, not to any notion of obstruction, and the decomposition is not claimed unique; the education archive's label apnf does not match the current nf.derivation.apnf.yaml, which is the apartness normal form.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/GenesisDerivation/Derivation/PrimitivePassage.lean::gates_of_obst`](../../../lean4/Imported/GenesisDerivation/Derivation/PrimitivePassage.lean)
- [`lean4/Imported/GenesisDerivation/Derivation/PrimitivePassage.lean::obstP_factors`](../../../lean4/Imported/GenesisDerivation/Derivation/PrimitivePassage.lean)
- [`lean4/Imported/GenesisDerivation/Derivation/PrimitivePassage.lean::obst_of_gates`](../../../lean4/Imported/GenesisDerivation/Derivation/PrimitivePassage.lean)
- [`lean4/Imported/MinimalSymbolSystems/MssnObstructionDetector.lean::obstP_factors`](../../../lean4/Imported/MinimalSymbolSystems/MssnObstructionDetector.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust port of the passage-system obstP; obstruction.rs::obstructed is the kernel's exhausted-menu notion, a different predicate`

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/genesis/code/derivation/primitive_passage.py::obst_p`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/primitive_passage.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0494](tfq_0494_stage_change_contract_proposal_record.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `lean4/Imported/GenesisDerivation/Derivation/PrimitivePassage.lean:216-226`
  - `lean4/Imported/MinimalSymbolSystems/MssnObstructionDetector.lean:63-66`
  - `external:sha256:0d098004a566c40656af6035d6e66ff13f7e873b11966677df080686a1b29cf9:1105-1107`
