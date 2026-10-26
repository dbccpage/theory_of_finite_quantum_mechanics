# [TFQ-0492] candidate-extension-generator

> **Stage**: `GENESIS` | **Status**: `DEFINITION`  
> **UUID**: `663344b2-9f35-5f90-b220-eb90c7893e49`  
> **Parent Derivation**: [TFQ-0488](tfq_0488_declared_challenge_import_per_level.md)

---

## 1. Abstract & Formal Statement

Declared here as the map from an unresolved residual, a demand given as source node, target pair, measure and bounds, to a legal proposal space, in the Alpha harness's three phases. Propose: a Proposal is Supply-shaped and no offering is ever executed. Evaluate: evaluate enumerates the sealed min_responses, groups them by canonical key and returns an EvalResult that is evidence only and is recomputed on the admission path. License: an authorization is bound to the source history digest, the target, the measure and the bounds, reuse with any field changed is refused, and uniqueness is not authorization (M3, M4). Endogenous demand generation stays OPEN (AE-DEMAND-OPEN): the generator answers a host-supplied demand and chooses none.

### Governing Obligation
Given a host-supplied demand, return the retained classes as evidence only, admit nothing without a License bound to that source, target, measure and bounds, and never emit a next demand.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Alpha harness trust boundary of closeout §7: the host builds each License with make_license and the host's call is the authorization (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The generator ranges over the sealed candidate space within declared bounds, where 'minimum' and 'iso class' are relative to those bounds; the passage system's extensionProposals is a separate carrier with no checked bridge to the harness (S7).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/Genesis19l57g1/Derivation/PrimitivePassage.lean::two_rule`](../../../lean4/Imported/Genesis19l57g1/Derivation/PrimitivePassage.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/outside.rs::Proposal`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/outside.rs)

### Python Oracles & Numerical Evaluators
- [`github:dbccpage/19L57G1@85a83ae7c/research/alpha_engine/driver_a.py::apply_licensed`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/alpha_engine/driver_a.py)
- [`github:dbccpage/19L57G1@85a83ae7c/research/alpha_engine/evaluate.py::evaluate`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/alpha_engine/evaluate.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0493](tfq_0493_four_gate_active_obstruction.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt:119-128`
  - `github:dbccpage/19L57G1@85a83ae7c/docs/ALPHA_HANDOFF.md:101-116`
  - `omega_engine_education/documentation/001_oegen/archive/genesis_pre_2026-10-09.md:1103`
