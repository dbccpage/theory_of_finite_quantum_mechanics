# TEST_ONLY duals — not a product package

**Banner:** `TEST_ONLY_DUAL — not a product package`

These harnesses are **prototype duals** of named Lean finite-QM obligations
(e.g. monoidal composition, finite matrix recovery). Models may live inside
test files.

| Rule | Detail |
| --- | --- |
| AuthorityEffect | Always **None** |
| Product import | **Forbidden** from non-test `omega_engine_py` runtime modules |
| PROD path | Rust `omega_engine/crates/omega_q/src/finite_shadow_exact.rs` + `fixtures/finite_shadow/` |
| Not | GlobalGreen evidence, customer claims, or Python = PROD |

Sealed under D1-B (PARITY-001 hygiene). Do not extract to a shipped package
without a multi-harness reuse need and a contract consumer.
