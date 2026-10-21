# [TFQ-0488] declared-challenge-import-per-level

> **Stage**: `GENESIS` | **Status**: `DEFINITION`  
> **UUID**: `61abda58-10dc-5095-9ee3-f5cfb7202708`  
> **Parent Derivation**: [TFQ-0487](tfq_0487_endogenous_demands_exogenous_payments.md)

---

## 1. Abstract & Formal Statement

Declared here as this programme's stage-change rule: each stage change S(n) to S(n+1) consumes exactly one declared, priced and recorded challenge import, either a fresh datum (external supply) or a new requirement kind (external goal), entered as one row of the demand ledger. It is the sealed external continuation policy (the supply and admission of one fresh opaque token at the closure fixpoint, declared metatheory and not a derived transition) made a typed ledger entry, and it follows the education audit's reading that progression requires one declared challenge import per level. In the Alpha slice the import is host-supplied: the host gives the target pair, the measure and the bounds, and nothing in the harness chooses a next demand.

### Governing Obligation
Record each stage change with exactly one import row (kind fresh-datum or new-requirement-kind, its price, its source) and refuse a stage change that carries no import or an unrecorded one.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `External continuation policy of genesis_source §3 item 10, declared metatheory (assumption)`
- **Admitted**: `One-import-per-level budgeting rule, a construction declared by this programme from the education audit (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> A declared budgeting policy, not a derived law: it does not show that one import suffices for any later stage, and it supplies no endogenous demand generator (OB-1 stays open).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `missing obligation: no Lean statement of a per-level import ledger; the class-relative exclusion G1Class.g1_class_exclusion motivates it (TFQ-0487)`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/outside.rs::Outside`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/outside.rs)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/engine.py::build_tree`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/engine.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0489](tfq_0489_typed_requirement_kinds.md)
- [TFQ-0490](tfq_0490_k_item_delta_grammar.md)
- [TFQ-0491](tfq_0491_capability_stage_counter.md)
- [TFQ-0492](tfq_0492_candidate_extension_generator.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:186-190`
  - `github:dbccpage/19L57G1@85a83ae7c/docs/ALPHA_HANDOFF.md:78-88`
  - `omega_engine_education/documentation/001_oegen/archive/genesis_pre_2026-10-09.md:947`
