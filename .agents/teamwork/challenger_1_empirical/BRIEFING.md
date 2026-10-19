# BRIEFING — 2026-10-19T03:54:00Z

## Mission
Adversarial empirical challenge of Python and Rust implementations across MUB(6), FSP, and Majorana domains.

## 🔒 My Identity
- Archetype: EMPIRICAL CHALLENGER
- Roles: critic, specialist
- Working directory: c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\challenger_1_empirical
- Original parent: 2f7c2b5c-0caf-47df-b59c-b0d9e7b0ab22
- Milestone: Final / Adversarial Hardening (F31)
- Instance: 1 of 1

## 🔒 Key Constraints
- Review-only — do NOT modify implementation code (find bugs by writing and executing tests, report failures)
- Never place source code, tests, or data files in `.agents/teamwork/` (only agent metadata: plan.md, progress.md, handoff.md, briefing.md)
- Do not trust claims or logs — independently run and verify all tests
- Strictly adhere to Claim Hygiene (narrow claims, no hype verbs, state assumptions)
- Explicit verdict required: APPROVE or REQUEST_CHANGES

## Current Parent
- Conversation ID: 2f7c2b5c-0caf-47df-b59c-b0d9e7b0ab22
- Updated: 2026-10-19T03:29:33Z

## Review Scope
- **Files to review**: `code/python/src/` (`mub`, `fsp`, `majorana`), `code/rust/src/` (`mub`, `fsp`, `majorana`), `code/python/tests/`
- **Interface contracts**: `PROJECT.md` Section "Interface Contracts"
- **Review criteria**: Mathematical and algorithmic correctness, genuine non-mocked execution, numerical/algebraic stability under perturbation, edge case handling.

## Attack Surface
- **Hypotheses tested**:
  - MUB(6): Unitarity of dephased Hadamard matrices, complex modulus invariance, ray obstruction invariants, Cyc24 arithmetic. (PASSED across 11 adversarial tests).
  - FSP: BQNF routing edge cases, Kitaev chain Majorana zero mode parity, exact rational Hubbard determinants ($4\times 4$ plaquette, attractive Hubbard square-root symmetry, palindromic spectra). (PASSED across 9 adversarial tests).
  - Majorana: GF(2) symplectic geometry, Clifford algebra commutation relations, braid representation invariants, tetron transfer envelopes. (PASSED across 12 adversarial tests).
  - Cross-cutting: `test_dual_face_majorana_mub_fsp.py` stress testing and mock/stub auditing. (PASSED across 6 adversarial tests).
- **Vulnerabilities found**:
  1. `code/python/src/fsp/fermion_sign_nf_evaluator.py:11`: Un-prefixed import `from bqnf_sign_evaluator ...` crashes on external import with `ModuleNotFoundError`, masked by test `conftest.py`.
  2. `code/python/src/mub/__init__.py:57-63` & `code/rust/src/mub/mod.rs:18-25`: `verify_mub_crate_invariants()` is a dummy mock/tautology checking `1/6 == 1/6`.
  3. `code/python/src/fsp/__init__.py:72`: `checked = 64` and `removing = 0` are hardcoded rather than dynamically computed as in Rust.
  4. `code/python/src/mub/mub_verify/cyclotomic.py:140`: `Cyc24.abs_sq()` docstring claims $|z|^2 \in \mathbb{Q}$, but it is in maximal totally real subfield $\mathbb{Q}(\sqrt{2}, \sqrt{3})$.
- **Untested angles**: Continuous manifold residue exhaustive search in unoptimized debug mode (known long-running task).

## Loaded Skills
- None specified by orchestrator

## Key Decisions Made
- [2026-10-19T03:30:00Z] Initialized briefing, attack surface, and empirical test strategy.
- [2026-10-19T03:44:00Z] Authored `test_adversarial_mub6_stress.py` (11 tests passed).
- [2026-10-19T03:47:00Z] Authored `test_adversarial_fsp_stress.py` (9 tests passed).
- [2026-10-19T03:49:00Z] Authored `test_adversarial_majorana_stress.py` (12 tests passed).
- [2026-10-19T03:50:30Z] Authored `test_adversarial_cross_cutting_stress.py` (6 tests passed).
- [2026-10-19T03:53:30Z] Emitted formal handoff report with verdict REQUEST_CHANGES based on import bug and mock pass findings.

## Artifact Index
- `DISPATCH.md` — Inbound instructions
- `BRIEFING.md` — Working memory and identity
- `progress.md` — Execution heartbeat
- `handoff.md` — Final challenge report
- `code/python/tests/test_adversarial_mub6_stress.py` — MUB(6) stress harness
- `code/python/tests/test_adversarial_fsp_stress.py` — FSP stress harness
- `code/python/tests/test_adversarial_majorana_stress.py` — Majorana stress harness
- `code/python/tests/test_adversarial_cross_cutting_stress.py` — Cross-cutting dual-face stress harness
