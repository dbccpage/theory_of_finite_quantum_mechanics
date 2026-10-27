# [TFQ-0423] identity-convention-undecidable

> **Stage**: `PREGENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `6d6e7a7c-9122-57a2-8c43-6382aca0dc9f`  
> **Parent Derivation**: [TFQ-0422](tfq_0422_presentation_not_expressive_lift.md)

---

## 1. Abstract & Formal Statement

Whether <a> supplied after <> is a new state depends on an identity convention that no prompt had declared. Under the opaque convention a state is what the regime can tell apart, and with O empty <> and <a> are not told apart; under the exact-inscription convention a state is the inscription itself, the strings differ, and the regime has one more syntactic state. Trials 1 and 2 answered under the first convention and the full replay under the second, calling <a> a new state. The analysis keeps both branches and records the effect as undecidable until one convention is declared.

### Governing Obligation
Keep the observer family and identity convention declared; no preferred convention, computability theorem or authority grant follows.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `A declared identity convention, opaque or exact-inscription, chosen by the host (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The observer family and interpretation of identity are declared. This is logical dependence on a convention, not a computability undecidability theorem, a preferred identity convention, or a replay of the historical model responses. It grants no operational or physical authority. Original target retained as an obligation: Whether <a> supplied after <> is a new state depends on an identity convention that no prompt had declared. Under the opaque convention a state is what the regime can tell apart, and with O empty <> and <a> are not told apart; under the exact-inscription convention a state is the inscription itself, the strings differ, and the regime has one more syntactic state. Trials 1 and 2 answered under the first convention and the full replay under the second, calling <a> a new state. The analysis keeps both branches and records the effect as undecidable until one convention is declared. Prior boundary: Records that the answer is relative to the convention; it does not choose one, and the three replies are behaviour of one unrecorded model, not evidence for either convention.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/IdentityConvention.lean::IdentityConvention.adding_identity_separates`](../../../lean4/IdentityConvention.lean)
- [`lean4/IdentityConvention.lean::IdentityConvention.empty_family_identifies_all`](../../../lean4/IdentityConvention.lean)
- [`lean4/IdentityConvention.lean::IdentityConvention.exact_inscription_is_new`](../../../lean4/IdentityConvention.lean)
- [`lean4/IdentityConvention.lean::IdentityConvention.exact_observer_sees_new`](../../../lean4/IdentityConvention.lean)
- [`lean4/IdentityConvention.lean::IdentityConvention.forgetting_preserves_indistinguishability`](../../../lean4/IdentityConvention.lean)
- [`lean4/IdentityConvention.lean::IdentityConvention.no_convention_independent_answer`](../../../lean4/IdentityConvention.lean)
- [`lean4/IdentityConvention.lean::IdentityConvention.observational_equivalence`](../../../lean4/IdentityConvention.lean)
- [`lean4/IdentityConvention.lean::IdentityConvention.opaque_inscription_is_not_new`](../../../lean4/IdentityConvention.lean)
- [`lean4/IdentityConvention.lean::IdentityConvention.opaque_observer_sees_no_new`](../../../lean4/IdentityConvention.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust switch between identity conventions`

### Python Oracles & Numerical Evaluators
- [`checks/independent/pgw-identity-convention-undecidable.py`](../../../checks/independent/pgw-identity-convention-undecidable.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0424](tfq_0424_absence_of_rule_not_identification.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `education/pregenesis_empty_mark/sources/analysis_derivation_v1.md:731-737`
  - `external:sha256:1713d12cc07cce5f295bb69922c49e278be2277c31d4fecee6b41ecb87d639bb:36-43`
  - `external:sha256:2e49c338376d7a78a6a89cdd340c9b3c351c485c20d4127e3c455b3fb1570428:43-53`
  - `dag/derivations/independent/pgw-identity-convention-undecidable.md:5`
  - `dag/research/campaign_pgw-identity-convention-undecidable_lean_replay.json:7`
