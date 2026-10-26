# [TFQ-0468] rung5-symmetry-along-history

> **Stage**: `GENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `1933f5e5-ad73-5418-8874-993dac785521`  
> **Parent Derivation**: [TFQ-0467](tfq_0467_rung4_index_up_to_isomorphism.md)

---

## 1. Abstract & Formal Statement

Rung five (pull request 258) takes Y-3, symmetry along a history. In Lean a supply keeps every automorphism, datum and form admissions at a well-formed regime lose none, and an instance, rule or requirement admission keeps exactly the automorphisms fixing the added element. Each of the three adding kinds loses automorphisms at some regime and gains them at another, so the automorphism count moves both ways; on the rectangle the largest rise is five, at datum edges, and the largest fall 24, at instance edges. Every event keeps the regime or raises the element count by exactly one, so no history returns to a regime it left after a changing event.

### Governing Obligation
Characterise per event kind which automorphisms survive, exhibit loss and gain for each adding kind, and carry the element-count step law and no-return along every replayed history.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Lean declaration SecondSymmetry.Aut.inst_meet at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`
- **Admitted**: `Lean declaration SecondSymmetry.Aut.kinds_move_both_ways at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`
- **Admitted**: `Lean declaration SecondSymmetry.Aut.size_counts_changes at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Which automorphisms survive is proved, never how many: no theorem counts an automorphism set, the numeric fixer and multiplication laws (Z-2, Z-3) are finite computation only, and that isomorphic regimes share an element count is left to rung eight for clean regimes.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_symmetry/lean/SecondSymmetry/Grow.lean::no_return`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_symmetry/lean/SecondSymmetry/Grow.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_symmetry/lean/SecondSymmetry/Grow.lean::size_counts_changes`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_symmetry/lean/SecondSymmetry/Grow.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_symmetry/lean/SecondSymmetry/Meet.lean::inst_meet`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_symmetry/lean/SecondSymmetry/Meet.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_symmetry/lean/SecondSymmetry/Witness.lean::kinds_move_both_ways`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_symmetry/lean/SecondSymmetry/Witness.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: the second-derivation rung trees hold no Rust`

### Python Oracles & Numerical Evaluators
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_symmetry/symmetry.py::brute_automorphisms`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_symmetry/symmetry.py)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_symmetry/symmetry.py::edge_report`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_symmetry/symmetry.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0469](tfq_0469_rung6_succession_element_count.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:306`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:409-419`
  - `github:dbccpage/19L57G1@85a83ae7c/research/second/claim_ledger.md:183`
