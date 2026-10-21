# Executed commands and retained outcomes

The complete final command vectors, working directories, UTC starts, durations,
exit codes and output SHA-256 values are in `commit_verified/commands.json`. Each listed
output file retains stdout and stderr. These are executed local checks, not
hosted CI claims.

| Check | Command (from repository root unless noted) | Final receipt |
|---|---|---|
| Lean | `lake build ComplexFieldSelection` (cwd `lean4`) | `commit_verified/lean.log` and `commit_verified/axioms.json` |
| Rust | `cargo test --manifest-path code/rust/Cargo.toml --offline -p tfqm_finite_probability --lib complex_selection` | `commit_verified/rust.log` |
| Python | `py -3.12 -X utf8 -m pytest code/python/tests/test_complex_selection.py -q` | `commit_verified/python.log` |
| Candidate | `py -3.12 -I -X utf8 code/python/src/qm/complex_selection.py <run>/p1/candidate.json` | `commit_verified/candidate.log` |
| DAG | `py -3.12 -I -X utf8 dag/validate_derivation_dag.py --no-files` | `commit_verified/dag.log` |
| Unified sync | `py -3.12 -I -X utf8 dag/sync_unified_dag.py --check` | `commit_verified/sync_unified.log` |
| Applications sync | `py -3.12 -I -X utf8 dag/sync_application_branches.py --check` | `commit_verified/sync_applications.log` |
| Pregenesis sync | `py -3.12 -I -X utf8 dag/sync_pregenesis_to_wdp.py --check` | `commit_verified/sync_pregenesis.log` |
| Companions | `py -3.12 -X utf8 scripts/contract_scores.py check` | `commit_verified/contracts.log` |
| Whitespace | `git diff --check` | `commit_verified/whitespace.log` |

The driver invokes Python 3.12 by its resolved executable; the literal executable
paths are in commands.json. `CARGO_TARGET_DIR=C:/t/cfs-target` keeps Windows paths
short. No dependencies were downloaded for the Rust tests.

## Retained failures and repairs

* `lake build ComplexFieldSelection`, `lean_attempt_01.log`: exit 1. The inherited
  draft had an unexpanded matrix-vector product in a trace proof and missing
  definition unfolding in state-symmetry proofs. Fixed without weakening statements.
* Same command, `lean_attempt_02.log`: exit 1. The new Gaussian imaginary-part
  definition introduced an unreduced Gaussian inverse. Replaced multiplication
  by Gaussian 1/2 with rational scalar multiplication; same mathematical value.
* Same command, `lean_attempt_03.log`: exit 0. All then-listed headline axioms
  passed. Final receipts also print seven additional supporting theorems.
* Initial Python candidate construction through `from qm.complex_selection import
  make_candidate`: failed with package relative-import error. Direct path loading
  via `runpy.run_path` generated `p1/candidate.json`; no candidate was accepted
  from the failed invocation.
* `py -3.9 -X utf8 -m pytest code/python/tests/test_complex_selection.py -q`,
  `python_attempt_01.log`: exit 4, before collection. The existing conftest imports
  unrelated code using Python 3.10 union type syntax.
* `py -3.9 -X utf8 -m pytest --noconftest code/python/tests/test_complex_selection.py
  -q`, `python_attempt_02.log`: interrupted by the researcher (exit -1) during
  repeated mutant recomputation. No passing-suite claim. The checker now caches
  only immutable, independently recomputed expected JSON within the process.
* `py -3.12 -X utf8 -m pytest code/python/tests/test_complex_selection.py -q`,
  `python_attempt_03.log`: exit 0, 15 passed in 5.54s. The normal conftest is enabled.
* Requested Rust command, `rust_attempt_01.log`: exit 0, 6 passed, 324 filtered out.
* First aggregate replay, `final/commands.json`: every command exited 0 except
  isolated `python -I ... scripts/contract_scores.py check`, exit 1 because -I
  hides user-site PyYAML. All mathematical checks passed. The corrected replay
  removes -I only from that metadata checker, for which isolation was not requested.
  The requested DAG validator still runs with -I.
* Diagnostic `py -3.12 --version`: Python 3.12.10; `py -3.12 -m pytest --version`:
  pytest 8.3.5; nonisolated `import yaml`: 6.0.3. Both Python 3.9 and 3.12 lack
  PyYAML in isolated mode. Sandbox-only attempts to invoke the Windows Store
  Python executable were unavailable; authorized worktree execution succeeded.

## Version and Git probes

* `git ls-remote origin refs/heads/lean-v4-35 refs/heads/complex-field-selection`:
  base was `5c6887bf881af025540653b95c5ba345df73b0a4`; new remote head absent.
* `gh pr list --head complex-field-selection --state all --json
  number,url,state,headRefOid,baseRefName`: empty before publication.
* `git -C lean4/.lake/packages/mathlib rev-parse HEAD`:
  `56a005855ea17e0b0958f73ec801ae140b0a1679`.
* `lake env lean --version` (cwd lean4): Lean 4.35.0,
  commit `eb6cafb7290e8bd5f2937522d8d804f58f02bafc`, x86_64-w64-windows-gnu.
* `cargo --version`: cargo 1.99.0 (5f94df478 2026-08-27).
* `rustfmt --edition 2021 code/rust/src/finite_probability/complex_selection.rs`:
  exit 0. Final Rust source was tested after formatting.

Read-only source inspection used Get-Content/rg and Git status/log/diff/worktree
queries. Permission-restricted Git access to C:/t/cfs failed before the authorized
worktree access was granted; no Git mutation resulted from those failed probes.
Publication details are reported in the PR and final chat response. No merge was requested.

Final exact-byte replay: `py -3.12 -X utf8 <run>/p2/replay_commit.py --output <run>/p2/commit_verified` exited 0. All ten command exits are 0; 22 axiom audits, 291 mutants, and source custody passed. The earlier `verified/` replay also passed; p3 records the sole intervening CRLF-to-LF change. A subsequent Git filter audit found no source-pin mismatch and no byte change under Git filters.
