# [TFQ-0539] wdp-seven-witness-roles

> **Stage**: `WDP` | **Status**: `DEFINITION`  
> **UUID**: `3b6acf08-795d-531f-8426-d409992edcae`  
> **Parent Derivation**: [TFQ-0538](tfq_0538_wdp_quotient_defect_root_p.md)

---

## 1. Abstract & Formal Statement

WDP-CH02-D01 defines a residual-locus witness as a typed locus L with evidence that the residual's component at L is nonzero under the declared test; the locus is a witness to a proposition, not a memory, observer, agent or apparatus. Section 2.2 replaces the one word witness by seven typed roles, ResidualLocusWitness, RetentionWitness, RepairWitness, ContextWitness, DualCertificateWitness, DescentReceipt and CounterexampleWitness, written Witness_k[P](x, e) with the proposition P and kind k in the type. WDP-CH02-P01 states that in the nominal typed interface no role tag coerces to another unless an explicit adapter and its hypotheses are declared. On the oriented triangle the circulation functional ℓ vanishes on im d₀ and gives ℓ(1,1,1) = 3, a dual certificate that observes, retains and decides nothing.

### Governing Obligation
Carry the role and the proposition in every witness type, refuse a change of role without a declared adapter, and keep certificates, stored marks, repairs and counterexamples apart.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> A syntactic fence, not the 42 directed semantic non-implications between roles; the executable check (adapt_quotient and adapt_operational refusing MISSING_ADAPTER or ADAPTER_MISMATCH) covers observer representations and does not enumerate the seven tags.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `missing obligation: the claim map lists WDP-CH02-D01 and WDP-CH02-P01 without an exact Lean declaration`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `omega_engine/crates_rs/omega_wdp/src/observer.rs::adapt_quotient` (private upstream source, not in this repository)

### Python Oracles & Numerical Evaluators
- `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/observer.py::adapt_quotient` (private upstream source, not in this repository)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0541](tfq_0541_wdp_retention_packet.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md:566-599`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md:601-609`
  - `omega_engine_education/documentation/006_oewdp/levels/level_01_witness_function.md:123-159`
