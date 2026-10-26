# [TFQ-0474] c1-engine-class-144

> **Stage**: `GENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `9f9ccb57-f88a-5bbe-b2c3-6230ca5cd3fb`  
> **Parent Derivation**: [TFQ-0473](tfq_0473_rung10_responder_adjacency_reach.md)

---

## 1. Abstract & Formal Statement

Continuation attempt one (pull request 267), authorized by the author after the original twelve attempts, takes Challenge 3, the engine: a generator (one of the nine stake rules, read in a plain or flipped mode), a responder (one sealed measure and one of rung one's two validity members, answering a demand by every tied minimum), a continuation (a subset of growth and switch fired only at a demand-free state, the empty subset named HALT) and the sealed replay extended by the switch marker. The class has 144 members, 108 of them without HALT, with capability counts from six to ten, so no member is one declaration. Probed to depth two from both readings (288 probes), 64 members are LIVE and 16 TWO-KINDED; a count-minimal and inclusion-minimal member exists in every declared subclass, none of the minima is unique up to probe-isomorphism, and no member is initial under inclusions of declarations. No engine is run forward.

### Governing Obligation
Enumerate the declared engine class and its capability counts, probe every member to depth two from both readings, and decide existence, uniqueness up to probe-isomorphism and initiality of minimal members under inclusions of declarations.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Lean declaration SecondEngine.Census.class_size at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`
- **Admitted**: `Lean declaration SecondEngine.Census.no_initial at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`
- **Admitted**: `Lean declaration SecondEngine.EngineDef.run_named at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`
- **Admitted**: `Author ruling of 2026-09-25 authorizing at most two continuation attempts outside the original budget (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The Lean response relation is not constrained to be a minimum and no theorem ties the finite list of declarations to the Engine structure; minima_differ_at_genL states only that E4 demands and E1 does not at reading L's genesis, the non-isomorphism going through the Python probe; no census row is decided, and initiality is refused for inclusion morphisms only.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_engine/lean/SecondEngine/Census.lean::class_size`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_engine/lean/SecondEngine/Census.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_engine/lean/SecondEngine/Census.lean::literal_size`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_engine/lean/SecondEngine/Census.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_engine/lean/SecondEngine/Census.lean::no_initial`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_engine/lean/SecondEngine/Census.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_engine/lean/SecondEngine/Engine.lean::run_named`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_engine/lean/SecondEngine/Engine.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_engine/lean/SecondEngine/Genesis.lean::minima_differ_at_genL`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_engine/lean/SecondEngine/Genesis.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: the second-derivation rung trees hold no Rust`

### Python Oracles & Numerical Evaluators
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_engine/engine_decl.py::count_minimal`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_engine/engine_decl.py)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_engine/engine_decl.py::engine_class`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_engine/engine_decl.py)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_engine/engine_probe.py::build_probe`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_engine/engine_probe.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0475](tfq_0475_c2_run_forward_every_history.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:261`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:228-236`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:877-888`
