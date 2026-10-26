# Sparse chain transport: verification record

AuthorityEffect: None. Recorded 2026-10-09.

[Appendix P.23](../witnessed_difference_programme.md#p23-sparse-integral-transport-and-polynomial-bounds-at-fixed-degree)
and the [full proof](sparse_guarded_chain_transport.md) establish the
minimum-sweep construction and fixed-degree polynomial bounds. This record
separates that written theorem from formal algebra, executable instances and
publication checks.

## Written proof and independent reviews

The [mathematical audit](../manifests/sparse_chain_transport_math_audit.json)
binds the exact supplement and P.23 bytes. It checks the signed sweep identity,
carrier legality, strict retraction, capacity compatibility, output bounds,
work recurrences, coefficient bits and the distinction between implicit and
explicit cochains. It does not audit the other manuscript appendices.

The [code audit](../manifests/sparse_chain_transport_code_audit.json) is an
independent static review of the contraction, adapter and source-bound CLI.
Its receipt includes the corrected orchestration controls: the binary digest
is stable across replay, and exclusive receipt creation prevents overwriting
existing inputs. Runtime evidence is attributed to the actual runs below,
not to that read-only reviewer.

The first-descent and minimum-sweep algorithms are named separately. The
polynomial proof belongs to `MinimumSweepV2`; `FirstDescentV1` retains its
original coordinates and exponential general majorant. Both have the same
chain-map and homotopy contract.

## Selected Lean results

Two fresh core Lean 4.33.1 Lake builds passed, with all 143 explicit
declarations audited and axiom union exactly `{propext, Quot.sound}`:

| Module | Theorems | Explicit declarations | Scope |
| --- | ---: | ---: | --- |
| `GuardedChainTransport` | 46 | 78 | Finite basis-check soundness, chain-map identities, filling reconstruction, strict retraction and pairing transport. |
| `SparseChainTransportBounds` | 53 | 65 | Conditional geometric recurrences, integer mass/support bounds, sweep growth and fixed-degree polynomial majorants. |

[Chain algebra receipt](../manifests/guarded_chain_transport_lean.json),
[bound receipt](../manifests/sparse_chain_transport_lean.json),
[chain build output](guarded_chain_transport_lean_build.txt), and
[bound build output](sparse_chain_transport_lean_build.txt) retain hashes and
commands. These builds do not mechanize the signed geometry, the complete
carrier construction, the Rust implementation, or its bit-level runtime.
They do not refresh the older paper-wide Mathlib census.

## Native checks

The [targeted validation receipt](../manifests/sparse_chain_transport_validation.json)
records 48 passing Rust tests: seven first-descent contraction tests, seventeen
generic integral equivalence tests, six minimum-sweep tests, and eighteen
adapter tests. None was skipped. Sweep checks cover all 5,316 full
permutohedral cells on one through six labels, selected nontrivial orders,
a sixteen-label reverse-vertex path with 120 output edges, and refusal cases.
The adapter checks all small map identities, V1 column equality against its
complete constructor, V2 capacity naturality, and sparse requests beyond the
old four-task enumeration limit. V1 and V2 are not compared for column equality.

The [native replay](../manifests/sparse_chain_transport_native.json) has eighteen
cases: task counts 4, 8, 16, 32, 64 and 128, at cycle degrees 0, 1 and 2. Every
case constructs a sparse native filling and then invokes a separate CLI
checker on the supplied certificate. Nine mutated certificates are refused:
wrong signs, missing filling, duplicated terms, Boolean coefficient, invalid
label, changed problem, changed capacity, floating degree and a supplied
verification flag. The retained 32-task degree-2 certificate is embedded in
the receipt.

For degree two, the supplied cycle is the six-face boundary of the legal cell
`[r0,r1] | [a0,r2] | [a1,a2]`, followed by sequential remaining task pairs.
Its capacity is three. Each run requests 27 projection, one inclusion and 26
homotopy columns, with 48 cached output terms; no ambient complex is built.
The reconstructed filling has one cell. The full legal complex has at least
`n!` vertices, since every sequential ordering of task pairs is legal.

The following are single debug-build observations, not asymptotic estimates:

| Tasks | Construction (microseconds) | Local check (microseconds) | Certificate bytes |
| ---: | ---: | ---: | ---: |
| 4 | 2221 | 88 | 487 |
| 8 | 4163 | 166 | 753 |
| 16 | 7584 | 237 | 1314 |
| 32 | 19454 | 485 | 2434 |
| 64 | 58135 | 1006 | 4870 |
| 128 | 189126 | 1834 | 10247 |

The direct baseline checks the known original one-cell filler. It is faster
on these fixtures and requires no search. These runs demonstrate sparse
execution and independent verification; they establish no search advantage.
The proof supplies the asymptotic bound separately.

## Reproduction

From the repository root, with the declared Rust dependencies available:

```sh
cargo test -j1 --locked --manifest-path omega_engine/crates_rs/Cargo.toml -p omega_homology --test permutohedral_contraction
cargo test -j1 --locked --manifest-path omega_engine/crates_rs/Cargo.toml -p omega_homology --test integral_chain_equivalence
cargo test -j1 --locked --manifest-path omega_engine/crates_rs/Cargo.toml -p omega_homology --test minimum_sweep_contraction
cargo test -j1 --locked --manifest-path omega_engine/crates_rs/Cargo.toml -p omega_wdp --test guarded_chain_transport
cargo build -j1 --locked --manifest-path omega_engine/crates_rs/Cargo.toml -p omega_wdp --example sparse_guarded_transport
```

Run `scripts/verify_sparse_chain_transport.py` from the paper package with
`--binary` pointing to the built example and `--output` naming a new JSON file.
It launches only native calculations, checks process outcomes, binds source
and executable hashes, and refuses to overwrite an existing output. If
`CARGO_TARGET_DIR` is set, use its `debug/examples` directory. No external model
or paid service is invoked.

`SparseTransport::new_minimum_sweep` evaluates supplied chains. Its separate
`verify_sparse_event_filling` accepts the caller's original cycle and proposed
filling, validates every cell and checks the exact boundary equation. The
CLI demonstration fixes its own explicit source problem from `N` and `DEGREE`;
a certificate cannot change that problem by changing its payload.

Native coefficients are checked `i64`; overflow and configured resource limits
produce typed refusals. The existing poset implementation admits at most 256
labels, and default contraction settings are smaller. Raising the caller's
label allowance admits the displayed 128-task instances but does not remove
the implementation ceiling. The mathematical proof uses unbounded integers
and finite label sets of arbitrary size.

## Paper checks and limitations

All 62 targeted paper-contract tests pass with the exact section count 428.
This is a scoped verification increment. It does not certify every historical
archive, settle previously recorded publication-gate debt, or publish a release.
The local cocycle/coface criterion is proved in the supplement; the newly
implemented independent native checker checks fillings. A full cochain table,
all-degree polynomial complexity, and the search for a reduced filler are
outside the claimed computation bound.

The final integration includes remote main `efeb4fb0d`. Its dependency change
was followed by a fresh adapter test run, native rebuild and complete sparse
replay. The audited mathematical and native source bytes are unchanged; the
integration record retains the initial run separately through commit history.
