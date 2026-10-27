# [TFQ-0500] isomorphism-soundness-in-lean

> **Stage**: `GENESIS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `227af173-29ef-5b89-9ba9-89e345667a6c`  
> **Parent Derivation**: [TFQ-0486](tfq_0486_genesis_freeze_endpoint_ledger.md)

---

## 1. Abstract & Formal Statement

CL-ISO-SOUND, soundness of the implemented isomorphism key, is a finite computation only: the Python key procedure's classes are cross-checked against a brute-force minimum over bijections, and the Lean side is unresolved (D3: no Lean evidence). Attempt two leaves 482 regimes above the brute-force limit of the key cross-check (H-4), and attempt one's check of the Python orbit against the Lean orbit (G-9) is not done.

### Governing Obligation
State and prove in Lean that equal implemented keys imply isomorphic regimes (and the converse where it is used), and check the Python automorphism orbits against the Lean orbits on the exported regimes. The implemented key, the regimes past the brute-force limit, and the orbit comparison stay open.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Open; the run trees are quotiented by the implemented isomorphism, whose soundness is computational at the regimes cross-checked. Narrowed in Lean 4 to colorings of two data, where equal keys hold exactly when one coloring is the other or its swap. The implemented key, the regimes past the brute-force limit, and the orbit comparison stay open.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/PregenesisIsomorphismSoundness.lean::pgwIsoConstants`](../../../lean4/PregenesisIsomorphismSoundness.lean)
- [`lean4/PregenesisIsomorphismSoundness.lean::pgwIsoFour`](../../../lean4/PregenesisIsomorphismSoundness.lean)
- [`lean4/PregenesisIsomorphismSoundness.lean::pgwIsoKeyIff`](../../../lean4/PregenesisIsomorphismSoundness.lean)
- [`lean4/PregenesisIsomorphismSoundness.lean::pgwIsoKeySwap`](../../../lean4/PregenesisIsomorphismSoundness.lean)
- [`lean4/PregenesisIsomorphismSoundness.lean::pgwIsoKeysOfFour`](../../../lean4/PregenesisIsomorphismSoundness.lean)
- [`lean4/PregenesisIsomorphismSoundness.lean::pgwIsoMixed`](../../../lean4/PregenesisIsomorphismSoundness.lean)
- [`lean4/PregenesisIsomorphismSoundness.lean::pgwIsoSwapInvolutive`](../../../lean4/PregenesisIsomorphismSoundness.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/canonical.rs::canonical_bruteforce`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/canonical.rs)

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/genesis/code/derivation/iso.py::canonical_bruteforce`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/iso.py)
- [`checks/independent/pgw-isomorphism-soundness-in-lean.py::main`](../../../checks/independent/pgw-isomorphism-soundness-in-lean.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt:60`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt:379`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:1045-1059`
  - `dag/derivations/independent/pgw-isomorphism-soundness-in-lean.md:5`
  - `dag/research/campaign_pgw-isomorphism-soundness-in-lean_lean_replay.json:6`
