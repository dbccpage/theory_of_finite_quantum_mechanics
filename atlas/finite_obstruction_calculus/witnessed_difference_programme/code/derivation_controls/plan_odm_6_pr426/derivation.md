# PLAN-ODM-6-PR426: Independent audit of PR #426 finite 2D/3D Meron demos and MSP-35/36 rows

**AuthorityEffect:** None.

## Scope

Finite PR #426 Meron demo and MSP-35/36 row audit control: independently checks configuration weights, sign rules, and transfer-matrix trace parity before any theorem import.

- Python witness: `witness_plan_odm_6_pr426` in `witness.py`
- Rust witness test: `test_plan_odm_6_pr426_scoped_control` in `omega_engine/crates_rs/tests/omega_wdp/derivation_controls/plan_odm_6_pr426.rs`
