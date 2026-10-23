# Deposit maintenance validation — 2026-10-02

AuthorityEffect: None. Package version remains 1.0.0; this is repository
maintenance, without a Zenodo publication or DOI reservation.

## Baseline and repairs

The package was retrieved from `dbccpage/the_symbol_game` at commit
`f1037ccebb4d29d78ee88647079963ed827d446a`, package tree
`fa92a7b630dd64a552b684a0ce2f4dcff0f01a8c`. All 46 committed package files
were checked against their Git blob hashes before editing.

The 35 algorithm tests passed. Both checksum lists were stale for six files:
`code/test_oe_prime_algorithms.py`, `docs/claim_code_map.yaml`,
`docs/claim_ir.yaml`, `docs/lean_claim_map.md`, `oe_prime_algorithms.tex` and
`oe_prime_algorithms_claim_ledger.yaml`. The previous ZIP contained those
six older versions, despite its outer hash matching `SHA256SUMS`.

The previous mutation audit stopped at the carrier-validation mutation
because its source anchor no longer matched the implementation. It also
treated every nonzero pytest exit code as a kill without first establishing
a passing baseline. The repaired audit checks an isolated unchanged suite,
then requires actual JUnit-reported test failures; collection and runner
errors abort. The carrier anchor now matches the existing validation rule.

The default gate checks exact archive membership and payload bytes in
addition to both checksum lists. `--extracted` explicitly verifies an
unpacked deposit using its internal manifest, preserving all payload,
claim, link, test and coverage checks without requiring the external ZIP
and `SHA256SUMS`. This avoids including the ZIP in itself. Coverage now
measures the implementation module rather than including test code. Local
linter cache files are excluded from deposit discovery and archive creation.

Replaying the introductory notebook exposed an outdated assertion that a
step without diagnostics returns `LOCAL_GREEN_FOR_SCOPE`. The current
implementation correctly returns `STEP_EXECUTED`; the notebook assertion
now agrees. Both notebooks' ordinary Python cells have regression coverage.

## Fresh checks

Host: Python 3.12.14; pytest 8.3.5; pytest-cov 7.1.0; coverage 7.16.2.

| Check | Result |
|---|---|
| Package tests with `--cov=oe_prime_algorithms --cov-fail-under=95` | 58 passed: 35 existing algorithm tests and 23 tooling/notebook regressions; 96.75% implementation line coverage |
| `scripts/mutation_audit.py` | Unchanged 35-test suite passed; 20/20 mutants killed by test failures |
| `scripts/build_claim_maps.py --check` | Current; all 21 claims retain their existing maps |
| Ruff on changed Python files | Passed |
| `git diff --check` | Passed |
| Notebook code cells in separate CPython subprocesses | Five cells in each of two notebooks completed; execution did not write notebook outputs |
| `verify_deposit.py` | Passed, including archive payload, hashes, claims, links, tests and coverage |
| Deterministic ZIP rebuild | Reproduced byte for byte; 46 members with exactly the 45 payload files and internal manifest |
| Fresh unpacked copy: `verify_deposit.py --extracted` | Passed; 58 tests, with neither the external ZIP nor `SHA256SUMS` present |

The tooling regressions reject stale payloads even after updating the outer
ZIP checksum, missing/extra/duplicate ZIP members, an invalid ZIP, changed
or missing extracted payload files, failing mutation baselines, and
collection/runner failures. Two small subprocess fixtures distinguish an
assertion failure from a syntax error during collection. Every mutation
anchor must match the current implementation exactly once.
Linter cache files are checked to stay outside the manifest and ZIP.

The manifest, ZIP and checksums were regenerated together. Final integrity
checks run the default gate, reproduce the ZIP byte for byte, and run
`verify_deposit.py --extracted` from a fresh unpacked copy. The deposit file
set has exactly 48 files, including the ZIP and external checksum list.

## Validation boundary

This maintenance changes deposit tooling, its regression tests,
documentation, one notebook assertion, checksums and the ZIP. The algorithm
implementation, manuscript, TeX, PDF, Lean sources and saved axiom report
retain their retrieved bytes. The existing algorithm tests and exact arithmetic
results have been rechecked; this is not a new correctness theorem.

No fresh Lean kernel replay was possible: `lake` and `lean` were absent.
No Jupyter kernel execution or PDF rebuild was performed. Ordinary Python
cell execution does not validate notebook kernel behavior or rich output.
Consequently `--lean` and `--full` are outside this validation scope, and
the saved Lean report remains historical evidence.
