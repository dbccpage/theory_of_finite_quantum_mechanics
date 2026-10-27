# [TFQ-0380] readings-left-unselected

> **Stage**: `GENESIS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `e50384e9-e0c7-5ba7-b5f5-3452fe47bb35`  
> **Parent Derivation**: [TFQ-0379](tfq_0379_supply_does_not_admit.md)

---

## 1. Abstract & Formal Statement

Chapter 1 of the S000 book, opened, says two admission readings remain unselected and that the chapter does not select reading L or reading F. The DAG statement on PG-GEN-SUPPLY-NO-OP keeps both: Reading L leaves <> supplied and not admitted, while Reading F admits it as a datum. Genesis paper.md section 7 is the heading for what minimal must include. The finite statement still required is a pair of regimes, or an explicit open branch, rather than a single chosen reading. Selecting one reading would change which datum is present at the first separation, so the branch stays open.

### Governing Obligation
Reading L and Reading F both remain available; neither admission of <> nor its non-admission is selected.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> none.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: no local lean twin located for atlas/papers/finite_obstruction_calculus/genesis/lean4/Derivation/Minimality.lean`](../../lean4/)
- [`absent: missing declaration obligation: both readings remain parameters of the first-separation statements`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/reading.rs`](../../code/rust/src/)
- [`absent: missing obligation: reading.rs was listed and not opened; it must not collapse L and F if both are represented`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: missing obligation: 000_genesis_19l57g1/code/derivation/model.py must be able to store both readings without a default choice`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0381](tfq_0381_cost_two_first_separation.md)
- [TFQ-0435](tfq_0435_challenge2_admitted_but_collapsed.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`
- **Primary Source Paths**:
  - `external:sha256:eed47042e450b5608d203687f53103f3f8f4cbc3e5056c8a3b73b9992a1811db`
