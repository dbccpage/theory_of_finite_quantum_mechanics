# AGENTS.md — MUB(6) Repository Agent Rules and Epistemic Governance

**AuthorityEffect:** None.


## Progressive Disclosure & Root Governance

This project-level rules file governs the bounded context of the MUB(6) exact certification suite. All agents operating within `omega_engine_atlas/coda_atlas/F004_papers/010_mub6/` MUST strictly adhere to root workspace invariants and domain rules:

| Context | Canonical Path | Primary Governance Skills | Key Invariants |
|---|---|---|---|
| **Root Workspace Governance** | [`.agents/AGENTS.md`](../../../../.agents/AGENTS.md) | `auto-oe-autop`, `governance-host-parity` | AuthorityEffect None, No Direct Push to Main, Targeted Tests Only, No BOM, Ordinal UTF-8. |
| **Mathematical Solvers & Verification** | [`.agents/rules/math/rl_mathematical_solvers_and_exact_verification.md`](../../../../.agents/rules/math/rl_mathematical_solvers_and_exact_verification.md) | `mub6-manager`, `governance-exact-solvers` | Exact rational/cyclotomic arithmetic, zero floating-point certifiers, Lean 4 kernel reflection. |
| **Rust Engineering Standards** | [`.agents/rules/engineering/rl_rust_engineering_standards.md`](../../../../.agents/rules/engineering/rl_rust_engineering_standards.md) | `techne-*`, `governance-clean-arch` | Sovereign Rust delegation (`omega_mub`), zero uncurated test runs, bounded local execution. |
| **Python Engineering Standards** | [`.agents/rules/engineering/rl_python_engineering_standards.md`](../../../../.agents/rules/engineering/rl_python_engineering_standards.md) | `techne-*`, `governance-test-isolation` | Python dataclass discipline, linter cleanliness, and Windows pytest isolation. |
| **Python Contracts & Runtime Invariants** | [`.agents/rules/engineering/rl_python_contracts_and_runtime_invariants.md`](../../../../.agents/rules/engineering/rl_python_contracts_and_runtime_invariants.md) | `techne-*`, `governance-test-isolation` | Exact numeric boolean guards, value object hash normalization, zero-assert production checks, and subprocess safety. |
| **Python Runtime & Environment Standards** | [`.agents/rules/paths/rl_python_runtime_and_environment_standards.md`](../../../../.agents/rules/paths/rl_python_runtime_and_environment_standards.md) | `techne-*`, `governance-test-isolation` | Windows pytest tmp pre-allocation, dynamic repo root resolution, and clean async teardown. |


## 1. Epistemic Posture & Claim Discipline

You must write with strict claim discipline at all times:
- Prefer narrow claims over broad claims: "supports", "demonstrates in this certified box cover", "is consistent with" over "proves".
- Forbidden words unless explicitly proven within certified scope: `proves`, `guarantees`, `mathematically verifies`, `fundamentally`, `true intelligence`, `impossible`, `universal`, `flawless`, `perfectly`, `clearly`, `obviously`, `simply`, `merely`.
- Every mathematical claim must cite its precise receipt, box certificate, or Lean 4 theorem.

## 2. Arithmetic & Certification Constraints

- All computational solvers and certificates MUST use exact rational ($\mathbb{Q}$) or exact cyclotomic ($\mathbb{Q}(\zeta_{24})$) arithmetic.
- Zero floating-point certifiers are admitted.
- Any interval enclosure must bound errors rigorously using rational interval arithmetic.

## 3. Formal Verification Standard

- Formal proofs reside in the source monorepo at `lean4/research_programs/mub6/` (root module `Mub6.lean`). This deposit copies only three Lean export and audit files under `lean4/`.
- Zero `sorry` axioms in published modules.
- Only standard Lean kernel axioms permitted: `[propext, Classical.choice, Quot.sound]`.
- Conditional theorems must be reported as conditional, with their premises named (see section 8 of `mub6.md`).

## 4. Execution Hygiene

- The deposit test suite is `tests/` (run `py -3.12 -m pytest tests -q -p no:cacheprovider` from this directory). The Rust `omega_mub` tests run in the source monorepo (`cargo test -j 1 -p omega_mub` from `omega_engine/crates_rs`).
- Git commits must not include temporary files, `.lake/build`, `target/`, or cache directories.
- Transcripts and scratch remain in non-tracked directories.
