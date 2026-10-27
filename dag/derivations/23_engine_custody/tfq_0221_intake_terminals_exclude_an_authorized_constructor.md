# [TFQ-0221] Intake terminals exclude an authorized constructor

> **Stage**: `ENGINE_CUSTODY` | **Status**: `SOURCE_RECORD`  
> **UUID**: `26327c2c-2091-5b24-a35d-a1692257f58b`  
> **Parent Derivation**: [TFQ-0220](tfq_0220_prime_002_stops_when_continuation_is_unauthorized.md)

---

## 1. Abstract & Formal Statement

The intake contract keeps an authorized terminal out of the status vocabulary. Python TerminalStatus lists evidence_only, unresolved, refused, and not_admitted. RefusalClass names a failed gate. Lean repeats those four constructors and comments that no constructor is named authorized. The prime book's firewall chapter separates identity and scope while the ceiling stays None. A finished prime cycle therefore lands on evidence, an unresolved mark, a refusal, or a not-admitted mark. The firewall records that landing and does not mint a stronger effect.

### Governing Obligation
Land a finished prime cycle on evidence, unresolved, refused, or not-admitted.

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
- [`absent: no local rust twin located for external:sha256:326075e024188a875a1445388e96f2b22c0e4e76c82f1ca28003edf167bded7b`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for external:sha256:033198650df7db94b49b2b91d275fb2308db7460db00bd06ac591218d127de43`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0222](tfq_0222_a_finite_receipt_records_local_checks_only.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F003.S000:000_omega_engine_prime_algorithms_and_runtime`, `F003.S000`
- **Primary Source Paths**:
  - `external:git-tree:e03ce30c258cf9ca164637ea387b5267bad58df9`
  - `external:git-tree:5d358f5062016c742016b891fa7891bb0f0e19ef`
