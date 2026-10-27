# [TFQ-0217] A replay digest does not widen the statement

> **Stage**: `ENGINE_CUSTODY` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `3f1384ab-9e52-5f71-ad2f-d4aae03a4ec8`  
> **Parent Derivation**: [TFQ-0216](tfq_0216_replay_custody_keeps_the_run_folder_sealed.md)

---

## 1. Abstract & Formal Statement

A replay digest does not widen the finite statement it covers. SHA-256 of a proposal, a run-folder manifest, or a prime receipt shows byte agreement with an earlier record. It does not add a carrier, erase a loss-ledger entry, or turn a Lean hypothesis into an independent conclusion. The Q ledger appends descent results in memory, which is a log of what was recorded, not a new finite relation. If the payload still holds a float trace, the hash preserves that trace and does not make it an exact rational. Replay travels with the statement; it is not a substitute for the three-language name.

### Governing Obligation
Treat a digest as byte agreement only, not as an added carrier or relation.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: no local lean twin located for atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/GenesisConstruction.lean`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:d607354d8f84e955b89d65e58983964ef43675f69b92bfdf8a16da4b21f3b1ec`](../../code/rust/src/)
- [`code/rust/src/wdp/coda/q/ledger.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for external:sha256:d9f6e028e9c671a6320cd8ab4ab3cd36513fadd234056de98f0570c48e26a5c7`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0218](tfq_0218_prime_000_fixes_declaration_order.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F003.S000`, `F000.S001:001_authorization_an_incompleteness_theory`, `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:5d358f5062016c742016b891fa7891bb0f0e19ef`
  - `external:git-tree:5ab26ee1f8e4e10cf2fbf7a36dd731d31fbf4a44`
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
