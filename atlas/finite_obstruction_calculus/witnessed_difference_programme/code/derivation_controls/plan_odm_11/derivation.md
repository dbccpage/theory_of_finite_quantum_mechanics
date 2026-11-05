# PLAN-ODM-11: AutoP/PTIR-to-SQL interface evaluation on a second distinct relational domain

**AuthorityEffect:** None.

## Scope

Finite AutoP/PTIR-to-SQL second-domain control: verifies query lowering, theory-preservation, and fail-closed refusal rules on a second distinct relational schema without introducing a second grammar.

- Python witness: `witness_plan_odm_11` in `witness.py`
- Rust witness test: `test_plan_odm_11_scoped_control` in `omega_engine/crates_rs/tests/omega_wdp/derivation_controls/plan_odm_11.rs`
