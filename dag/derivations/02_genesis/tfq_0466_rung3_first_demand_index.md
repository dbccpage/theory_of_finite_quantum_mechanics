# [TFQ-0466] rung3-first-demand-index

> **Stage**: `GENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `d85f4154-63c3-5e3e-b49f-0fa61c1d8013`  
> **Parent Derivation**: [TFQ-0464](tfq_0464_rung2a_stake_declared_label.md)

---

## 1. Abstract & Formal Statement

Rung three (pull request 239) takes leftover L-2, the first-demand index over an arbitrary run: a first count is a prefix length at which a demand stands with no shorter prefix carrying one. In Lean the first count is unique with no decidability hypothesis, every event preserves well-formedness, a successor first count never consumes a demand-inert event last, and from the empty base no count below two is a first count. Existence is proved only given a decision for a demand at a regime (X-1, OPEN). Countermodels: the first count is not a function of the reached regime (two datum admissions, and a supply followed by the same two, give counts two and three under the all-apart stake), and a demand can cease.

### Governing Obligation
Over every base, history and stake, carry uniqueness of the first count and the two countermodels, and keep its existence conditional on a decision procedure for a demand at a regime.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Lean declaration SecondIndex.Index.first_demand_unique at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`
- **Admitted**: `Lean declaration SecondIndex.Index.first_demand_exists_when_a_demand_is_decidable at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`
- **Admitted**: `Lean declaration SecondIndex.Countermodel.index_is_not_a_function_of_the_reached_regime at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`
- **Admitted**: `Declared two-sided stake of rung two track one (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Existence of a first count waits on a decision procedure over contexts (X-1), which no rung built; the rectangle results (577, 3928 and 14293 sequences) stop at four events, and nothing here concerns a run driven by a responder (I-X PENDING).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_index/lean/SecondIndex/Countermodel.lean::demand_can_cease`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_index/lean/SecondIndex/Countermodel.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_index/lean/SecondIndex/Countermodel.lean::index_is_not_a_function_of_the_reached_regime`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_index/lean/SecondIndex/Countermodel.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_index/lean/SecondIndex/Index.lean::first_demand_exists_when_a_demand_is_decidable`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_index/lean/SecondIndex/Index.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_index/lean/SecondIndex/Index.lean::first_demand_unique`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_index/lean/SecondIndex/Index.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: the second-derivation rung trees hold no Rust`

### Python Oracles & Numerical Evaluators
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_index/index.py::first_index_forward`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_index/index.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0467](tfq_0467_rung4_index_up_to_isomorphism.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:304`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:387-395`
  - `github:dbccpage/19L57G1@85a83ae7c/research/second/claim_ledger.md:161`
