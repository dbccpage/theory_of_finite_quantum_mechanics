# Executable derivation controls

The 59 former `plans/work` packages now live here. Each goal directory retains
its derivation note, Python witness and negative tests. The paired Rust controls
are private test modules in `omega_engine/crates_rs/tests/omega_wdp/derivation_controls`,
compiled by `omega_wdp`'s library test harness. Standalone Cargo manifests and
locks have been removed. These are bounded paper examples, not 59 new engine APIs.

The authoritative goal-to-code bindings are the `mechanization` fields in
[`goal_dag.jsonl`](../../../../plans/goal_dag.jsonl). Each completed goal names
Python code/tests and canonical Rust code/tests, with an explicit coverage class:

- `bounded_algorithm`: the declared finite algorithm under its input contract;
- `finite_control`: a finite calculation or counterexample supporting a written result;
- `assumption_control`: a check of explicitly admitted premises, not their derivation.

A bound source anchor does not assert that a test ran. In particular, finite
CAR or rational-constant checks do not mechanize a thermodynamic limit; finite
character examples do not prove LCA duality; MUB6 fixtures do not classify CHM(6).
Written proofs, existing Lean scope and current execution results remain separate.

Reusable finite reachability mathematics now belongs to
`omega_solvers::finite_belief_game`: positive rational costs, optimal Bellman
certificates, feasible upper bounds, initial-state losing traps, coarsest
congruence and quotient. Its verifier does not call the producer. A feasible
certificate's unclaimed states are unknown, not certified losing. The paper's
`certified_progress` Python code provides the independently implemented finite
model; its broader reporting protocol and parity games are outside this Rust API.

The old `prod-kernel-routing` Rust Boolean checker was deleted. Its pairing now
uses `omega_wdp/tests/test_finite_routing.rs`, which exercises the actual cochain
and guard owner. The Python control uses input-bound `functional_evaluate` and
`functional_verify` through the canonical host. The all-M inertia fixture uses
the existing BigRational dependency; its private bignum implementation was deleted.

From the repository root, run focused controls:

```sh
python -m pytest -q -o addopts= --import-mode=importlib omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/derivation_controls/wdp_appm_t1/test_witness.py
cargo test --manifest-path omega_engine/crates_rs/Cargo.toml -j 1 -p omega_wdp --lib paper_derivation_controls
cargo test --manifest-path omega_engine/crates_rs/Cargo.toml -j 1 -p omega_solvers --test finite_belief_game
```

Run at most three pytest files per invocation. Product adapter controls require
the repository and its Python dependencies. Routing additionally requires the
current `omega_symbol_game` executable, selected through `OMEGA_SYMBOL_GAME_HOST`.
No missing native executable is replaced by a successful mock or a skip.

The [October 14 execution receipt](../../manifests/derivation_controls_verification.json)
records the commands, source snapshots and limits of this review.

The migration's source package is a development supplement. Existing versioned
archives, manuscript/PDF bytes and historical execution receipts remain intact.
AuthorityEffect: None.
