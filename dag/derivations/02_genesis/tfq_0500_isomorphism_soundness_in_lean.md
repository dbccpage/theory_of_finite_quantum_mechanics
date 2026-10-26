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
- [`lean4/CampaignPgwIsomorphismSoundnessInLean.lean::pgwIsoConstants`](../../../lean4/CampaignPgwIsomorphismSoundnessInLean.lean)
- [`lean4/CampaignPgwIsomorphismSoundnessInLean.lean::pgwIsoFour`](../../../lean4/CampaignPgwIsomorphismSoundnessInLean.lean)
- [`lean4/CampaignPgwIsomorphismSoundnessInLean.lean::pgwIsoKeyIff`](../../../lean4/CampaignPgwIsomorphismSoundnessInLean.lean)
- [`lean4/CampaignPgwIsomorphismSoundnessInLean.lean::pgwIsoKeySwap`](../../../lean4/CampaignPgwIsomorphismSoundnessInLean.lean)
- [`lean4/CampaignPgwIsomorphismSoundnessInLean.lean::pgwIsoKeysOfFour`](../../../lean4/CampaignPgwIsomorphismSoundnessInLean.lean)
- [`lean4/CampaignPgwIsomorphismSoundnessInLean.lean::pgwIsoMixed`](../../../lean4/CampaignPgwIsomorphismSoundnessInLean.lean)
- [`lean4/CampaignPgwIsomorphismSoundnessInLean.lean::pgwIsoSwapInvolutive`](../../../lean4/CampaignPgwIsomorphismSoundnessInLean.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/canonical.rs::canonical_bruteforce`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/canonical.rs)

### Python Oracles & Numerical Evaluators
- [`checks/independent/pgw-isomorphism-soundness-in-lean.py::main`](../../../checks/independent/pgw-isomorphism-soundness-in-lean.py)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/iso.py::canonical_bruteforce`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/iso.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt:60`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt:379`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt:1045-1059`
  - `dag/derivations/independent/pgw-isomorphism-soundness-in-lean.md:5`
  - `dag/research/campaign_pgw-isomorphism-soundness-in-lean_lean_replay.json:6`
