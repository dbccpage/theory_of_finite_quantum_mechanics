# [TFQ-0478] go-contraction-step2-step3

> **Stage**: `GENESIS` | **Status**: `PROVED_LEAN`  
> **UUID**: `20bb6f6e-8a55-5f5d-a4a9-a619c74f0b65`  
> **Parent Derivation**: [TFQ-0477](tfq_0477_go_reach_ceiling.md)

---

## 1. Abstract & Formal Statement

The contraction family strikes changes from the base seed. The second derivation strikes removal and keeps identification, adding a term and adding an assertion (Lean Step3); every change comes with a carrying map q, the identity for an addition and a merge for an identification, sending terms to terms, each asserted xry to an asserted q(x) r q(y) and the names to the names, and carrying maps compose along every sequence (Step3.carries, Reach3.carries). The third derivation also strikes identification (Lean Step2, two kinds): Step2.toStep3 embeds each of its changes as a second-seed change and Reach2.toReach3 each sequence, so the earlier one-change and sequence theorems restrict to it, and its containment of a state in its outcome is a carrying map with the identity.

### Governing Obligation
Carry the carrying map along every second-seed sequence, and embed every third-seed change and sequence into the second seed through Step2.toStep3 and Reach2.toReach3.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The Lean names run opposite to the derivation numbers (Step3 is the second seed's three-kind step, Step2 the third seed's two-kind step); the embedding is a restriction, and no carrying map exists under the base seed, where a removal un-asserts.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/GenesisOngoing/Second/Carry.lean::Reach3.carries`](../../../lean4/Imported/GenesisOngoing/Second/Carry.lean)
- [`lean4/Imported/GenesisOngoing/Second/Carry.lean::Step3.carries`](../../../lean4/Imported/GenesisOngoing/Second/Carry.lean)
- [`lean4/Imported/GenesisOngoing/Third/Step.lean::Reach2.toReach3`](../../../lean4/Imported/GenesisOngoing/Third/Step.lean)
- [`lean4/Imported/GenesisOngoing/Third/Step.lean::Step2.toStep3`](../../../lean4/Imported/GenesisOngoing/Third/Step.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: the H3V7N5QF package holds no Rust`

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/second/reach.py::carrying_map`](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/second/reach.py)
- [`atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/third/reach.py::embedding`](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/third/reach.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0479](tfq_0479_go_multiplicity_monotone.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/second/claim_ledger.md:47`
  - `atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/third/claim_ledger.md:52`
  - `external:sha256:b9029b5bf217f6cd67b350aff6bfefe937ea4e879d7257db46c0949e33db8023:36`
