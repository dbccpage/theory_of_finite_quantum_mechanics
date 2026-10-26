# [TFQ-0432] challenge0-inertia-second-token

> **Stage**: `GENESIS` | **Status**: `PROVED_LEAN`  
> **UUID**: `fc192bea-7a4c-54f8-84bd-feeb622012dc`  
> **Parent Derivation**: [TFQ-0430](tfq_0430_metatheory_object_language_split.md)

---

## 1. Abstract & Formal Statement

At Challenge 0 the only object-language inscription is the opaque whole <>. In the token-erased Lean model nothing is derivable at genesis (genesis_underivable), and nothing is derivable in any regime with no instances and no rules (underivable_of_empty); the Challenge 0 computation records zero contexts and an empty derivable set in both readings. That no successor is internally forced is a property of the declared grammar, whose only state changes are external-event-indexed admissions, not a theorem about a forcing predicate. In the token-aware model a history whose datum admissions all carry one token leaves at most one admitted datum (single_token_carrier_bound), so a state with two data needs the admission of a second, different token (second_token_required).

### Governing Obligation
Show that genesis and every instance-free, rule-free regime derive nothing, and that two admitted data require a datum admission of a token different from the first.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Further Prerequisites
- [TFQ-0379](tfq_0379_supply_does_not_admit.md) supply-does-not-admit

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> No forcing predicate is defined, so no forced successor is a model-scoped definition and not a theorem, and nothing here excludes a successor in an extension of the language; supply_no_op itself is recorded under TFQ-0379.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/Genesis19l57g1/Derivation/Bridge.lean::second_token_required`](../../../lean4/Imported/Genesis19l57g1/Derivation/Bridge.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Bridge.lean::single_token_carrier_bound`](../../../lean4/Imported/Genesis19l57g1/Derivation/Bridge.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean::genesis_underivable`](../../../lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean::underivable_of_empty`](../../../lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/reading.rs::challenge0_generates_nothing`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/reading.rs)

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/genesis/code/derivation/engine.py::challenge0_report`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/engine.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt:203-217`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt:218-224`
  - `lean4/Imported/Genesis19l57g1/Derivation/Bridge.lean:155-157`
