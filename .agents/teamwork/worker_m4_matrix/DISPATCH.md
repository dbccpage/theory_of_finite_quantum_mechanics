# DISPATCH — Worker M4 (Tri-Language Traceability Matrix)

## 2026-10-18T22:07:00Z
You are Worker M4 (Tri-Language Traceability Matrix Worker).
Working directory: c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\worker_m4_matrix
Authoritative User Request: c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\ORIGINAL_REQUEST.md
Master Project Plan: c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\PROJECT.md

READ ORIGINAL_REQUEST.md and PROJECT.md first. Also inspect:
- `papers/core/mub6/mub6_claim_ledger.yaml` and `papers/core/mub6/theory_of_finite_mub6.md`
- `papers/core/fsp/claim_ledger.yaml` and `papers/core/fsp/theory_of_finite_fsp.md`
- `papers/core/majorana/claim_ledger.yaml` and `papers/core/majorana/the_majorana_problem.md`
- Canonical Python modules: `code/python/src/mub/`, `code/python/src/fsp/`, `code/python/src/majorana/`
- Native Rust crates: `code/rust/src/mub/`, `code/rust/src/fsp/`, `code/rust/src/majorana/`, `code/rust/src/wdp/`
- Consolidated Lean 4 formalization: `lean4/lakefile.lean`, `lean4/*.lean`

Exclusive File Ownership:
`TRACEABILITY_MATRIX.md` at repository root.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All claims, implementations, theorems, and proofs must be genuine and accurately documented. DO NOT fabricate file paths, symbol names, theorem names, or test statuses. A forensic auditor will independently verify your matrix.

MANDATORY CLAIM HYGIENE RULE:
You must write with strict claim discipline:
- Prefer narrow claims over broad claims. Scope all claims strictly to declared finite/algebraic premises.
- Forbid hype verbs: "proves", "guarantees", "fundamentally", "universal", "flawless", "weaponized".
- Replacement defaults: "proves" -> "supports" or "shows in this finite model", "guarantees" -> "guarantees under declared premises".
- For each paper domain (MUB6, FSP, Majorana), include the mandatory summary:
  1. What it supports.
  2. What it does not support.
  3. The narrowest defensible claim.
  4. The next test needed.

Your Tasks:
1. Construct `TRACEABILITY_MATRIX.md` at repository root.
2. Section 1: MUB(6) Traceability Matrix:
   - Map all 41 claims (`MUB6-C01` to `MUB6-C41`) and key derivations from `theory_of_finite_mub6.md`.
   - Columns: Claim ID, Claim Description, Scope/Premise, Python Implementation & Test, Rust Implementation & Test, Lean 4 Module & Theorem, Axioms (`{propext, Classical.choice, Quot.sound}` only), Verification Status.
3. Section 2: FSP (Fermion Sign Problem) Traceability Matrix:
   - Map all 35 claims (`PO-023-C1`–`C2`, `GIN-C1`–`C24`, `NF-001`–`003`, `MERON`, `HUBBARD`, `ORIGIN`) and 56 derivations from `theory_of_finite_fsp.md`.
   - Columns: Claim ID, Theoretical Invariant, Algebraic Premise, Python Implementation & Test, Rust (`tfqm_fsp`) Implementation & Test, Lean 4 Module & Theorem, Verification Status.
4. Section 3: Majorana Bound States & Topological Braiding Traceability Matrix:
   - Map all 20 claims (`MAJ-C1` to `MAJ-C20`) from `papers/core/majorana/claim_ledger.yaml` and `the_majorana_problem.md`.
   - Columns: Claim ID, Topological Invariant, Finite Lattice Premise, Python Implementation & Test, Rust (`tfqm_majorana`) Implementation & Test, Lean 4 Module (`MajoranaCore`, `MajoranaGinCore`), Verification Status.
5. Section 4: Cross-Cutting Dual-Face Synthesis & Epistemic Firewalls:
   - Map dual-face controls connecting Majorana zero modes, FSP involution doublets, and MUB(6) cochain obstructions.
   - Cross-cutting test: `code/python/tests/test_dual_face_majorana_mub_fsp.py`.
   - Document `AuthorityEffect: None` across all receipts and audit logs.
6. Section 5: Verification & Audit Census:
   - Complete census of test execution suites: E2E tests (45/45 passed), Python unit/integration tests, Rust workspace tests, Lean 4 formalization status (404 modules, 0 sorry, 0 admit, kernel axiom whitelist only).
   - Deposit verifier statuses (`verify_deposit.py` for mub6, fsp, majorana).
7. Section 6: Claim Discipline Syntheses (MUB6, FSP, Majorana):
   - Mandatory 4-point claim hygiene summary for each of the three paper programs.
8. Deliverables:
   - Write `TRACEABILITY_MATRIX.md` at repository root.
   - Write your completion report to `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\worker_m4_matrix\handoff.md`.
   - Send a completion message via `send_message` to parent orchestrator.
