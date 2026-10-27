# [TFQ-0328] Evaluate a proposal against a reporting alphabet as a separate measurement, with

> **Stage**: `AUTHORIZATION` | **Status**: `SOURCE_RECORD`  
> **UUID**: `36f4588e-841a-5d15-aecf-b72a8d5b8487`  
> **Parent Derivation**: [TFQ-0327](tfq_0327_keep_proposal_spaces_and_reporting_alphabets_separate_from_the_unjoined.md)

---

## 1. Abstract & Formal Statement

Chapter 02 of EA:000.001.001 is evaluation as a separate measurement from proposal. The shelf admission rule names proposal spaces, reporting alphabets, supplied validity bits, finite terminals, and replay packets. The exit contract asks for a typed claim ledger, source disposition, implementation inventory, local proposed gaps, and explicit P0 and walk nonclaims. Nothing in the opened shelf or book README collapses evaluation into authorization. A supplied validity bit is data for a later terminal, not itself a terminal. AuthorityEffect is None on the shelf header.

### Governing Obligation
Evaluate a proposal against a reporting alphabet as a separate measurement, with a supplied validity bit that is not yet a terminal.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: no local lean twin located for external:sha256:ca48b0074858e81772a7a2bfd00f3d6331a76a8cfcd6a71a568cc84d87d7b946`](../../lean4/)

### Sovereign Rust Certifiers
*Computational witness tracked under `theory_of_finite_qm` crate.*

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for external:sha256:d798f3c79d454a2ae94c08a0267e6540d8ae26d51eecf1f618f360cbd967de60`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0329](tfq_0329_keep_authorization_free_of_a_forced_external_host_and_keep_the_seven_flag.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000`, `F000.S001`, `F000.S001:001_authorization_an_incompleteness_theory`
- **Primary Source Paths**:
  - `external:sha256:f1e9a10038dca4d2b00b28ffe558eaa8ba74f8f893b3b8c28ff78a539f3ebddd`
  - `external:sha256:8f664cdf087dfcffc889d6b105b271d2b3f8cf955381e8e96362ecff80d5a6fc`
