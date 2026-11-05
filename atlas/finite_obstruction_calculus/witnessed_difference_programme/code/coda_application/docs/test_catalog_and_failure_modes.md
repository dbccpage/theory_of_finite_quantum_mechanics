# CODA test scope and failure modes

AuthorityEffect: None.

The maintained application runs declared finite rational data through evaluation and a separate local authorization contract. Tests are executable examples and counterexamples, not architectural necessity theorems or a proof of security against hostile code in the interpreter.

## Current checks

| Files under `tests/` | What is checked |
| --- | --- |
| `test_pipeline_flow.py`, `test_triad_and_foundations.py` | Zero and positive defects, failed layers, distinct authorized/residual/refusal outcomes, and source-bound external grants. |
| `test_coda_firewall.py`, `adversarial/test_adv_firewall_engine.py` | Refusal of forged, missing, or inconsistent evidence; a grant alone cannot replace mathematical checks. |
| `adversarial/test_adv_registry_tokens.py` | Digest binding, immutable public fields, persistent records, token replay and ordinary API misuse. |
| `test_high_dim_stress.py` | Exact certificates for bounded graph examples; construction of 1,000/1,500-vertex fixtures; budget exhaustion. Large fixture construction is not large-instance solver validation. |
| `test_rust_bridge.py`, `adversarial/test_adv_foc_quotient.py` | Native transport, malformed input, certificate replay and fixed mathematical counterexamples. Adapter agreement uses one functional owner and is not independent solver agreement. |
| `adversarial/test_adv_arch_cli_packaging.py` | Inward dependency rules, CLI exit behavior, metadata construction and audit fault injection. Workspace discovery requires a monorepo checkout. |

Functional values and primal/dual verification delegate to `omega_functional`. The solver proposes candidate repairs. The application composition root supplies the trusted evaluator; proposals cannot supply it. A missing executable or exhausted evaluation budget produces refusal, not an invented value. The CLI reports measured elapsed time and does not promise a universal three-second solve.

## Routing and authority conditions

The firewall checks caller role, exact source-bound evidence, a complete primal/dual certificate, closure, grant binding, budget and declared refusal flags. Zero defect without a grant is `REFUSED`. A checked positive quotient defect with zero closure defect is retained as `CLOSED_RESIDUAL`. Authorization requires zero checked defects, successful layer records and a one-use HMAC grant under the operator-configured keyring. The grant binds the problem, evidence and licensee.

These conditions define the local contract. The keyring is a trust input and does not establish institutional standing. HMAC requires a shared secret; it is not public-key independent verification. The Python process and filesystem owner remain trusted. Hashes detect byte changes but establish neither authorship nor mathematical validity. Persistence does not stop a file owner from deleting the register.

A positive quotient distance is relative to the supplied repair operator and norm. It is not automatically a topological invariant or a physical fact. The profile stage checks a total map between declared labels; it does not prove protected-answer preservation. Interval checks establish order and diameter, not containment of an unknown answer. No machine check of a flag solves undecidability or validates an external specification.

## Historical evidence

The [superseded catalog](../../../docs/source_archive/superseded_derivations_20261008/coda_test_catalog.md) is retained for provenance. Its runtime tables, broad security statements, natural-transformation nonexistence claim and old terminal labels are withdrawn as descriptions of current code. The [dated September review](adversarial_review_2026-09-23.md) records its own source revision. Current validation must cite a fresh receipt and its exact source inventory; historical PASS labels do not certify this revision.
