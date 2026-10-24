# [TFQ-0500] isomorphism-soundness-in-lean

> **Stage**: `GENESIS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `227af173-29ef-5b89-9ba9-89e345667a6c`  
> **Parent Derivation**: [TFQ-0486](tfq_0486_genesis_freeze_endpoint_ledger.md)

---

## 1. Abstract & Formal Statement

Narrowed boundary, status left OPEN. U0 and U1 are well-formed duplicate-free regimes with data count 2, one form of arity 1, and requirement (0, 1). BL is well-formed and duplicate-free with form arity 2 and instance arguments 0 and 1. Each exhaustive candidate list has length 2. The datum swap is an isomorphism from U0 to U1, and the exhaustive keys of U0 and U1 are equal. No isomorphism from U0 to BL exists, and those exhaustive keys differ.

### Governing Obligation
Keep this finite check separate from the implemented Python key. A Python key procedure, a budget-truncated search, and a comparison of Python orbits with Lean orbits on exported runs stay open.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> These facts are the exhaustive Lean search on U0, U1, and BL. They are not a Python key cross-check and not an orbit comparison on exported runs. Status stays OPEN.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/CampaignPgwIsomorphismSoundnessInLean.lean::pgwIso_BL_wf`](../../../lean4/CampaignPgwIsomorphismSoundnessInLean.lean)
- [`lean4/CampaignPgwIsomorphismSoundnessInLean.lean::pgwIso_U0_U1`](../../../lean4/CampaignPgwIsomorphismSoundnessInLean.lean)
- [`lean4/CampaignPgwIsomorphismSoundnessInLean.lean::pgwIso_U0_not_BL`](../../../lean4/CampaignPgwIsomorphismSoundnessInLean.lean)
- [`lean4/CampaignPgwIsomorphismSoundnessInLean.lean::pgwIso_U0_wf`](../../../lean4/CampaignPgwIsomorphismSoundnessInLean.lean)
- [`lean4/CampaignPgwIsomorphismSoundnessInLean.lean::pgwIso_U1_wf`](../../../lean4/CampaignPgwIsomorphismSoundnessInLean.lean)
- [`lean4/CampaignPgwIsomorphismSoundnessInLean.lean::pgwIso_candidate_counts`](../../../lean4/CampaignPgwIsomorphismSoundnessInLean.lean)
- [`lean4/CampaignPgwIsomorphismSoundnessInLean.lean::pgwIso_keys_eq`](../../../lean4/CampaignPgwIsomorphismSoundnessInLean.lean)
- [`lean4/CampaignPgwIsomorphismSoundnessInLean.lean::pgwIso_keys_ne`](../../../lean4/CampaignPgwIsomorphismSoundnessInLean.lean)
- [`lean4/CampaignPgwIsomorphismSoundnessInLean.lean::pgwIso_set_collections`](../../../lean4/CampaignPgwIsomorphismSoundnessInLean.lean)

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
