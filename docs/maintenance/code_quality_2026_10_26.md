# Python/Rust quality improvement attempt, 2026-10-26

Status: AI-drafted, awaiting human review.
AuthorityEffect: None.

The audit covers all 7,253 governed Python/Rust sources under `code/`, including
4,216 generated governance twins. It repairs concrete regressions and contract
identity/schema errors. **It does not establish L5 for these sources.** In
`SCORING.md`, L5 describes foundational proof/certificate architecture and E
means a demonstrated defect. Passing a test or changing a score label cannot
supply the missing architecture or verification.

The machine-readable [receipt](../../evidence/quality/code_2026_10_26/receipt.json),
[per-file inventory](../../evidence/quality/code_2026_10_26/scope/sources.tsv) and
[scope audit](../../evidence/quality/code_2026_10_26/scope/audit.json) bind the
observations to exact source bytes. The base is
`4fea09ae176aae31115e38bb2b21819237055811`; observations include working-tree
repairs on top of that base. This is a scope audit plus targeted repair review,
not a semantic review of a million lines of code.

| Check | Before | After |
|---|---:|---:|
| Valid source identity/schema or pinned boilerplate coverage | 7,112 | 7,253 |
| Missing/invalid current companions | 141 | 0 |
| Completed scores | 12 | 12 |
| Incomplete scores | 7,221 | 7,221 |
| Python suite failures | 24 | 0 |
| Python suite passes | 2,637 | 2,672 |
| Rust fixture suite failures | 1 | 0 |
| Rust fixture suite passes | 13 | 15 |

Python has two skips and 87 passing subtests in both full runs. The five later
module-docstring corrections have a separate 35-test replay; executable ASTs
are unchanged. All 5,522 Python sources pass syntax compilation and all 1,731
Rust sources pass `syn` parsing. Rust parsing does not check types, imports,
macro expansion or the full dependency build. The Rust parser's eight
calibration tests pass. Fixture checks pass in debug and release, and Clippy
passes with warnings denied.

## Repairs and their boundaries

- Exact scalar entry points reject booleans, floats, overridden scalar classes,
  oversized rational components and exponent text. The declared 1,024-bit,
  sequence-length and file-read budgets are engineering choices. Domain checks
  in `l1_import_exact` survive `python -O`; arities are checked before indexing.
- F2 elimination rejects malformed matrices and mismatched right-hand sides.
  Ledger records are checked before key access. The DAG witness queue releases
  the globally least ready node. The rational Bell support result exposes its
  expected compatibility name.
- Hermitian effects require membership in the Hermitian carrier. The shared
  extension layer uses the Hermitian projection for that model, while the
  rational model retains its quadratic preorder. These finite computations do
  not derive a general Gleason theorem.
- The doubled-trace calculation uses `abs(trace(M))**2`, avoiding cancellation
  into a tiny negative value. A zero-trace control makes the nonnegative bound
  explicit. Diagnostic route names are not proofs of a physical sign repair.
- Posting-list lookup now applies every required-mode intersection, even after
  a singleton remains. The historical source demonstrably returned a candidate
  missing a required mode. Its G2/E finding is retained in score history with
  the [counterexample](../../evidence/quality/code_2026_10_26/gin-singleton-counterexample.log).
  Benchmark timing remains an observation; a deterministic candidate-comparison
  budget replaces the unreliable one-shot wall-clock threshold.
- Mutation harnesses compile mutants before counting behavioral kills. Stale
  Gate 5 metrics are withdrawn for changed helpers and preserved in history.
  Fixture, provenance and atlas line links resolve to the current tree.
- The working publication verifier accepts different valid DEFLATE encodings
  while checking member hashes, the archive sidecar and the complete ZIP32
  envelope. Tampered contents, metadata, prefixes and suffixes are refused.
  The sealed inner preprint, ZIP and sidecar remain byte-identical.
- Rust custody tests verify a separate current fixture register. Four receipts
  had acquired `NOT_A_CERTIFICATE` warnings in commit `ef0c2df1`; their old bytes,
  historical register and exact annotation-only transitions are retained. The
  historical register still refuses the changed current bytes. No fixture is
  promoted to computed mathematical evidence.

The 141 companion repairs comprise 131 legacy score-schema migrations, seven
stale source bindings and three missing companions. Valid existing contracts
are retained during schema migration; all prior raw contract/score history is
preserved. The 32 changed sources in `code/`, the working publication verifier
and the audit tool receive current source-bound repair contracts. Their
assessments remain incomplete rather than receiving invented gate grades.

## Remaining limits and acceptance

- Governance correctly rejects the 32 changed governed sources because their
  G1–G5 assessments are incomplete. This is a draft, not a merge-ready change.
  No baseline, exception pin, acceptance floor or DAG status is changed.
- The complete Rust workspace cannot resolve the unpublished `finite_qm_native`
  dependency. Optional dependency flags do not remove Cargo's resolution
  requirement. No fake dependency or stub substitutes for this missing build.
- The scope audit lists 330 runtime-assert review candidates. These are locations
  for further inspection, not established defects. It does not claim exhaustive
  Python test coverage or execution of unregistered Rust sources.
- The outer MUB deposit manifest already has 54 missing-path/digest mismatches.
  Only this task's working-verifier bindings are updated; those earlier
  mismatches remain visible in the [limitations record](../../evidence/quality/code_2026_10_26/outer-manifest-limitations.json).
  Its full manifest check still fails. The separately sealed inner publication
  is unchanged and passes its tests.

Further work toward L5 requires per-module claim-to-implementation mappings,
explicit trust and resource boundaries, certificate producers with independent
checkers where the algorithm warrants them, and evidence for all five gates.
Small helpers and tests should retain their actual architectural level. A
blanket score promotion or a blanket exception cannot supply that evidence.

## Reproduce

Use Python 3.12 with the repository test dependencies and Rust stable. From the
repository root, choose fresh `/tmp` report/target locations:

```sh
python -I -X utf8 -m pytest code/python/tests -q -p no:cacheprovider
cargo test --locked --manifest-path code/rust/quality/fixture_register/Cargo.toml
cargo test --release --locked --manifest-path code/rust/quality/fixture_register/Cargo.toml
cargo clippy --locked --manifest-path code/rust/quality/fixture_register/Cargo.toml --all-targets -- -D warnings
cargo test --locked --manifest-path code/rust/quality/category_homology/rust_metrics/Cargo.toml
cargo build --locked --manifest-path code/rust/quality/category_homology/rust_metrics/Cargo.toml --target-dir /tmp/tfqm-rust-metrics
python -I -X utf8 scripts/audit_code_quality.py --output /tmp/tfqm-code-audit --rust-metrics-bin /tmp/tfqm-rust-metrics/debug/tfqm_rust_metrics
python -I -X utf8 scripts/score_scope_contracts.py check --changed-since 4fea09ae176aae31115e38bb2b21819237055811
python -I -X utf8 scripts/contract_scores.py check --changed-since 4fea09ae176aae31115e38bb2b21819237055811
```

The audit refuses to replace an existing output directory. Omitting the Rust
parser reports that check as unrun and returns a nonzero audit status. History
and scope checks validate records; they do not enforce or certify a completed
engineering grade. Use `governance-check` as documented in `governance/README.md`
to reproduce the acceptance failure separately. Baseline, intermediate and
final test logs are retained in the receipt directory.
