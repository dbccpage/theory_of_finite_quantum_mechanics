# [TFQ-0422] presentation-not-expressive-lift

> **Stage**: `PREGENESIS` | **Status**: `CONDITIONAL`  
> **UUID**: `a0fea856-b6d9-5667-93c6-369972539fa7`  
> **Parent Derivation**: [TFQ-0421](tfq_0421_observational_equivalence.md)

---

## 1. Abstract & Formal Statement

Write P for the presented inscriptions and O for the internal observations. Supplying <a> after <> changes P from {<>} to {<a>} and leaves O_1 = O_0 = ∅, so no new internal distinction is available. With q : P → N sending an inscription to the distinctions the regime has, x ≠ y in P can hold while q(x) = q(y) in N, so a new presentation does not imply a new internal class, and in the other direction q(x) = q(y) does not imply x = y. Under the opaque convention <a> is a new presentation state in the same internal class as <>; the statement holds under that convention only.

### Governing Obligation
Keep the presentation P and the internal quotient N as separate records, so that supplying <a> with O empty adds a presentation state and no internal class, and never infer x = y from q(x) = q(y).

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Opaque identity convention: a state is what the regime can tell apart, so internal identity is the quotient by ≈ₙ (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Under the exact-inscription convention <a> is a new state; the statement concerns discriminating power, not meaning, since a regime can gain a syntactic distinction such as empty versus nonempty payload without assigning a a referent. Reviewed in PR 185: lean4/CampaignPgwPresentationLift.lean checks a two-inscription model (Inscription = {nil, markA}, convention comparison, P0 = {nil} against P1 = {nil, markA}) in which the distinction map q is the constant empty map by definition and the exact-inscription convention is defined as equality, so O_0 = O_1 = empty, the non-injectivity of q and the statement that the collapse holds under the opaque convention only are properties of those definitions. Not proved: an observation family O_n and q derived from it, supplying <a> as an operation that leaves O unchanged, P changing to {<a>} as the statement words it (the model has P1 = {<>, <a>}), the link between q and the Genesis regime model of the module, and the opaque identity convention itself, which stays an import.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/CampaignPgwPresentationLift.lean::CampaignPgwPresentationLift.statement_holds_under_opaque_only`](../../../lean4/CampaignPgwPresentationLift.lean)
- [`lean4/Imported/PreGenesisToMssn/Observation.lean::empty_profiles_equal`](../../../lean4/Imported/PreGenesisToMssn/Observation.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust record separating presentation state from internal class`

### Python Oracles & Numerical Evaluators
- [`checks/independent/pgw-presentation-not-expressive-lift.py::main`](../../../checks/independent/pgw-presentation-not-expressive-lift.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0423](tfq_0423_identity_convention_undecidable.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_education/documentation/000_oepregen/sources/analysis_derivation_v1.md:110-135`
  - `omega_engine_education/documentation/000_oepregen/sources/analysis_derivation_v1.md:925-975`
  - `omega_engine_education/documentation/000_oepregen/03_results_and_arguments.md:29-43`
