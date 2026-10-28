# [TFQ-0216] Replay custody keeps the run folder sealed

> **Stage**: `ENGINE_CUSTODY` | **Status**: `SOURCE_RECORD`  
> **UUID**: `d158438e-20e1-50e7-96d4-e086cf2c1dc7`  
> **Parent Derivation**: [TFQ-0215](tfq_0215_finite_quantum_shelf_is_a_custody_binding.md)

---

## 1. Abstract & Formal Statement

Replay custody means a later reader can reopen the bytes the runtime accepted. replay exports run-folder sealing and AUTHORITY_EFFECT_NONE, and run_folder.rs rejects a receipt whose authority effect is not that constant. ReplayHash and the append log sit beside the seal so a trace can be named without being rewritten in place. The authorization book adds ReplayFiber, which hashes proposal bytes, and its docstring says the helper is not certification or authorization. Prime issue_finite_receipt builds a digest from the local packet checks. Custody keeps the sealed folder, the hash, and the None marker.

### Governing Obligation
Seal the accepted bytes with a replay hash and with authority effect None.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: no local lean twin located for external:sha256:19e794086b88a7edc2c69799cb7d3c3339abc6c5801043d311a13333cd0b2881`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/wdp/lib.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:02639231a7e2985fb581adedc4455415ce6ad641e736b98ca20063edb6beff98`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:d607354d8f84e955b89d65e58983964ef43675f69b92bfdf8a16da4b21f3b1ec`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for external:sha256:d9f6e028e9c671a6320cd8ab4ab3cd36513fadd234056de98f0570c48e26a5c7`](../../code/python/)
- [`absent: no local python twin located for external:sha256:118b9549a600eee604e58f81e4d692d85eacc23649fb6d451821820ca6f89911`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0217](tfq_0217_a_replay_digest_does_not_widen_the_statement.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F003.S000`, `F003.S000:000_prime_algorithms_and_runtime`, `F000.S001:001_authorization_an_incompleteness_theory`
- **Primary Source Paths**:
  - `external:git-tree:5d358f5062016c742016b891fa7891bb0f0e19ef`
  - `external:git-tree:e03ce30c258cf9ca164637ea387b5267bad58df9`
  - `external:git-tree:5ab26ee1f8e4e10cf2fbf7a36dd731d31fbf4a44`
