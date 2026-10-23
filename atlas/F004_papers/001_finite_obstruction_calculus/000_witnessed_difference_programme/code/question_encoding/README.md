# Question-preserving encoding experiment

The native `omega_wdp::question_preserving_encoding` module owns this bounded
integer-quadratic experiment. This Python directory transports requests and
compares the deposited receipt with a fresh native replay; it computes no
cochain functional. Closure arithmetic calls `omega_functional::Gamma2Functional`.

From the monorepo root, build the native example:

```console
cargo build --manifest-path omega_engine/crates_rs/Cargo.toml --locked -p omega_wdp --example question_preserving_encoding
export WDP_QUESTION_ENCODING_BINARY="$PWD/omega_engine/crates_rs/target/debug/examples/question_preserving_encoding"
```

If `CARGO_TARGET_DIR` is configured, use the executable under that directory
instead. From this paper's `code/` directory:

```console
python -m question_encoding.replay --check
```

`--write` intentionally refreshes the receipt after a reviewed implementation
change. Both modes require the canonical monorepo sources and compiled native
example. A standalone deposit retains the result and its source hashes but
does not contain the monorepo dependency graph. Missing native capability is
an error, and never selects a Python solver.

The experiment exhausts 225 derivative/initial-value tasks and 125 candidate
polynomials. It separately runs lexicographic enumeration, direct algebraic
reconstruction, and anchored cochain reconstruction. Every proposed answer
passes through the same exact polynomial checker. The stronger direct
reconstruction baseline prevents attributing the benefit of solving linear
equations to the cochain representation.

The JSON driver also accepts `verify_direct` or `verify_cochain`, each with an
independently supplied `expected_task` and a `report` JSON string. A valid but
wrong candidate returns `accepted: false`; malformed reports and task
mismatches return a typed refusal and exit 2. No result authorizes an action.
