# Native causal execution and selected local 3-witnesses

**AuthorityEffect: None.** These are finite, input-bound certificates for
Appendices P.14--P.17. The existing ideal-price and minimum-swap scripts retain
their combinatorial scope. The new integration explicitly executes
`omega_wdp::genesis_source_execution::Source25Run` through a thin Rust adapter.

## What is retained

- `five_edit_problem.json` declares an actual initial raw state, seven named
  occurrences, three unique births, precedence and protected price definitions.
  Its 24 linear extensions execute all five native kinds. Every history has
  protected totals `(3,1,2,2)` for term additions, assertion additions, source
  size difference and plain-state cost difference. The latter two are state
  differences, rather than accumulated state fees.
- `antichain_problem.json` has four independent events and 24 native histories.
  Its named births make the token-to-native alignments nontrivial.
- `execution_fixtures.json` retains both full execution certificates, every
  native intermediate state and descriptor, token maps, framed ideal boundaries,
  exact prices, and backtrack/square/braid certificates. The second execution
  certificate is shared by digest rather than copied three times.
- `native_build_receipt.json` binds the adapter, builder, explicit dependency
  source files, Rust compiler, Cargo resolution and executable. The local build
  uses the complete main checkout because this worktree omits the native crates.
  `native/Cargo.lock` retains the resolved dependency lock. The executable is
  retained locally under the ignored repository `target/causal_replay/` tree.
- `replay_receipt.json` records four accepted replays and five refusals: a valid
  poset with impossible Remove, altered alignment, wrong replacement offset,
  altered framed boundary and a braid involving comparable events.

## Replay the submitted evidence

From the repository root, set the three paths explicitly and run:

```powershell
$paper = 'atlas/papers/finite_obstruction_calculus/witnessed_difference_programme'
$sourceRoot = 'C:/Users/a343o/source/repos/the_symbol_game'
$binary = 'target/causal_replay/target/debug/wdp_causal_replay.exe'
$buildReceipt = "$paper/code/causal_certificates/native_build_receipt.json"
py -3.12 "$paper/code/causal_certificates/replay_examples.py" check `
  --native-bin $binary --native-build-receipt $buildReceipt --source-root $sourceRoot
```

The checker uses the separately supplied problem, reexecutes every complete
schedule through the actual owner, and compares the submitted certificate
without modifying it. Missing native configuration, changed source or binary
bytes, native refusals and nonzero protected price curls refuse acceptance.
There is no implicit source discovery and no Python transition fallback.

`scripts/check_causal_execution.py` also accepts `create` and `check` for one
problem/certificate pair. `scripts/check_causal_three_cells.py` checks a standalone
3-certificate against independently supplied problem and two-history boundary
request. The bundle helper restores the shared execution certificate before
calling that same verifier; it does not regenerate a replacement witness on
replay.

## Build and test profile

To build against an explicitly selected complete checkout:

```powershell
py -3.12 "$paper/code/causal_certificates/native/build_native.py" `
  --source-root $sourceRoot --build-dir target/causal_replay
```

The builder runs Cargo offline with one compilation job. A different build,
source revision or executable requires newly named evidence rather than silently
rebinding the retained literal certificate. New evidence can be generated with
`replay_examples.py create --fixtures <new-file> --output <new-receipt>` and the
same explicit native flags. It refuses to overwrite submitted fixtures.

For the two scoped integration test files, set `WDP_CAUSAL_NATIVE_BIN`,
`WDP_CAUSAL_BUILD_RECEIPT` and `WDP_CAUSAL_SOURCE_ROOT` to the corresponding paths. These tests carry the `monorepo` marker; `verify_deposit.py` deselects them because the native owner lives in the engine, not in this package.
An absent integration profile is reported as skipped, never fresh native PASS.
The recorded run used Python 3.12.14 and the actual Rust adapter: **35 passed,
zero skipped**. Tests cover the complete binding, invalid inputs, missing
birth-before-use, a native refusal after another legal order, a nonzero
source-size fee curl, all local relations and whiskering, altered boundaries,
empty/single-event cases, and distinct 3-certificates with identical boundaries.

## Scope

The certificate checks every linear extension of its supplied family, bounded
by eight events and 10000 schedules. It checks rooted complete histories and
their admissible swap-proof replacements, including prefixes and suffixes. It
does not synthesize a 3-certificate for arbitrary parallel proofs, identify
distinct 3-certificates, supply higher cells or settle general guarded-history
coherence. In particular, it does not manufacture all-order admission for the
guarded counterexample in P.18.

Token translation, frame comparison and certificate orchestration are Python
presentation machinery. State admission, enabled changes, state transitions,
native occurrence prices, source size and plain-state cost are computed by the
existing Rust owner. No source-level proof of that owner's implementation or
new Lean theorem is claimed by these replay receipts.

## Guarded families (Appendix P.20)

`guarded_compatible_*`, `guarded_p18_*` and `guarded_three_pairs_*` are
problem/certificate pairs of schema `wdp-guarded-coherence-v1`, emitted by
`cargo run -p omega_wdp --bin wdp_guarded_history -- <problem.json>`. The first
is a kind-ordered family with refused orders, a star base and three coherence
witnesses; the second is P.18's disconnected family; the third is the
within-component counterexample (54 legal histories, rational first homology of
rank one, a separating cocycle). They were replayed on 2026-10-06 against a
fresh build of this adapter, recorded in `native_build_receipt_guarded_2026_10_06.json`:

```powershell
py -3.12 "$paper/scripts/check_guarded_coherence.py" check `
  "$paper/code/causal_certificates/guarded_three_pairs_problem.json" `
  "$paper/code/causal_certificates/guarded_three_pairs_certificate.json" `
  --native-bin $binary --native-build-receipt "$paper/code/causal_certificates/native_build_receipt_guarded_2026_10_06.json" `
  --source-root $sourceRoot
```

The checker recomputes every linear extension's legality natively, the swap
complex, components, kind compatibility and each component's rational
first-homology rank (exact elimination over Q). It checks a submitted star base,
and when none is submitted it confirms that no legal history is one. It replays
each coherence witness and checks the cocycle on every legal face. Each swap edge
is checked for unchanged source and target frame boundaries only; unlike P.17's
three-cell replay it does not compare protected totals along the edge, because
P.20 claims framed boundaries only. A witness may carry at most 250,000
replacements, the same bound as the native owner. The older `native_build_receipt.json`
remains bound to the earlier binary and is not rebound.