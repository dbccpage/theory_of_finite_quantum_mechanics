# Contract governance

**AuthorityEffect:** None. This folder states and enforces a process rule. It adds no result.

## The rule

Every governed source file needs a companion `<name>.contract.score.yaml` next to it (the file is JSON, schema `tfqm.contract-score.v1`). The companion must:

1. **bind the file**: its current contract and its current score name the file's path and the SHA-256 of its exact bytes;
2. **carry a completed score**: all five gates G1 to G5 graded, `composite_grade` equal to the weakest gate, and `score_token` equal to level plus composite grade (for example `L4C`), as defined in [`SCORING.md`](../SCORING.md);
3. **meet the floor**: level L4 or L5 **and** composite grade D or better, on the order `E < D < C < B < A < A+` ([SCORING.md section 1.5](../SCORING.md#15-repository-acceptance-floor)).

Under the default floor, `L4D`, `L4C` and `L5A+` pass. `L4E`, `L3A` and any score with an unassessed gate fail. Explicit reviewed support exceptions are described below.

**Governed sources** are the populations in [`policy.json`](policy.json): `code/**/*.rs`, `code/**/*.py` and `lean4/**/*.lean`, minus build and cache directories (`target`, `__pycache__`, `.lake`, `node_modules`) and sealed snapshots (`dag/results/**`, `dag/sealed_runs/**`, `sealed_runs/**`, `atlas/**`, `papers/**/archive/**`). Discovery is `git ls-files --cached --others --exclude-standard`, the same rule as `scripts/score_scope_contracts.py`.

**Reviewed support exceptions.** The maintainer authorized lower capability levels for declarative build registrations, regression tests and byte-identical source archives, while keeping grade D and all integrity checks. `support_exceptions` pins each reviewed path and source digest, category and reason. The current reviewed paths, categories and exact digests are listed in `policy.json`. A changed hash or different path loses the exception; incomplete scores and grade E still fail. Substantive runtime and proof modules retain L4D except for the separately authorized finite-proof pins below. These are not baseline additions.

**Reviewed finite-proof examples (2026-10-25).** The user authorized 31 exact campaign-module hashes: the initial 30 in `../dag/research/approved_finite_proof_exceptions_2026_10_25.json` and the additional PR #373 pin in `../dag/research/approved_pr_373_finite_proof_exception_2026_10_25.json`. Their category is `finite_proof_example`, restricted to a single `lean4/Campaign*.lean` module path. The modules retain honest L1–L3/D scores and their open or conditional research boundaries. Each exception requires its exact digest, a completed score and grade D or better. A changed digest or an unlisted source uses the ordinary L4/D floor. The baseline and all node statuses are unchanged.

**Grandfathering.** No existing source had a completed score when this was introduced, so the floor applies to new and changed files. [`baseline.json`](baseline.json) lists every source that lacked a completed in-floor score on 2026-10-22, with the SHA-256 of its bytes then and its first deficit. A listed file with unchanged bytes is exempt. Changing it removes the exemption: the changed file must then meet the floor. The baseline only shrinks (see below).

On 2026-10-23 the maintainer also authorized `compatibility_support` for the
unchanged-purpose `code/python/src/qm/qm122_dual.py` re-export. The parser rejects
that category for every other path. Its exact source hash is pinned, its score
remains L1D, and grade E or incomplete assessments still fail. The five-test
`replica_hierarchy_validation.py` harness uses the existing regression-test
exception at L2D. Substantive runtime and proof modules retain the L4D floor;
neither exception adds a baseline entry. See the
[repair assessment](../docs/overclaim/reviews/2026-10-23_governance-blocker-repair.md).

**Pinned boilerplate.** The build hook [`hook/build.rs`](hook/build.rs) (two comment lines and a `main` that calls the macro) is copied byte for byte into every workspace package. Its SHA-256 is pinned in `policy.json`, and only identical copies are exempt from needing a companion. The code it calls is scored with the governance crate.

A pass shows that a completed, byte-bound score at or above the floor exists. It does not show that the grades are deserved. The reviewer decides that by reading the gate reasoning and the evidence the score cites.

## Where it is enforced

| Where | What runs | Effect of a violation |
|---|---|---|
| `cargo build` / `cargo check` of any workspace package | `build.rs` calls `governance::verify_crate_contracts!()` on that package's `.rs` files | depends on `TFQM_GOVERNANCE` (below) |
| CI, [`.github/workflows/governance.yml`](../.github/workflows/governance.yml), on every pull request and push to `main` | `governance-check check --changed-since origin/main` (full check on `main`), the crate tests, `contract_scores.py check`, and a comparison of the Rust and Python populations | the job fails |
| By hand | `governance-check check`, `explain <path>`, `list`, `baseline` | exit status 1 |

Python and Lean are not built by cargo, so they are covered by `governance-check` and CI only.

### Build-time modes (`TFQM_GOVERNANCE`)

| Value | Behaviour |
|---|---|
| unset, empty or `warn` | **default.** Each violation is printed as a `cargo:warning`; the build continues. |
| `new` | The build fails when a file outside the baseline fails; other violations are warnings. |
| `enforce` | The build fails with the full report on any violation. CI uses this. |
| `off` | Verification is skipped. |

**Why the default is `warn`.** A new file can only earn a completed score after its tests have run (Gate 4 needs that evidence), and its tests can only run after a successful build. Failing local builds of new files would make the rule impossible to meet. Existing code is grandfathered, so the default prints nothing for it. Nothing below the floor can merge, because CI runs `enforce` on every pull request. Set `TFQM_GOVERNANCE=new` locally if you want new files to be fatal.

A build script outside this repository (for example a packaged crate) finds no `governance/policy.json`. It warns and continues in `warn` mode and fails in `new` and `enforce` modes.

## How to add or update a score

1. **Write the code and its tests.** Run the tests. The build warns that the file has no companion; that is expected.
2. **Assess it** against [`SCORING.md`](../SCORING.md): choose the level, grade each gate G1 to G5, and write the reason for each grade. Cite the evidence (test logs, mutation results, metrics) by path and SHA-256. Unrun evidence is `null`, not a grade, and a `null` gate means the file is not accepted yet.
3. **Write two JSON records**, both with `"artifact": {"path": "<repo-relative path>", "sha256": "<sha256 of the exact bytes>", "language": "Rust" | "Python" | "Lean 4"}`:
   - a contract: `contract_urn`, `symbols`, `owned_invariants`, `boundaries`, `AuthorityEffect: "None"`;
   - a score: `schema_version: "2.0.0"`, `profile`, `level`, `level_basis`, `gates`, `basis` (the reasoning per gate), `composite_grade`, `score_token`, `is_complete: true`, `grade_ceiling`, `evaluation_timestamp`, `evidence`.
   The companions of `code/rust/src/governance/src/*.rs` are worked examples.
4. **Record them.** This appends both records to the companion's history (earlier history is kept) and makes them current:
   ```
   python -I -X utf8 scripts/score_scope_contracts.py record <path> --contract contract.json --score score.json
   ```
5. **Check it.**
   ```
   governance-check explain <path>
   governance-check check --changed-since origin/main
   ```
6. **Any later edit of the source changes its SHA-256**, so the companion must be re-bound and the score re-assessed for the new bytes.

The JSON Schema of a companion, with the extra rules the checker enforces, is [`schema/contract-score.v1.json`](schema/contract-score.v1.json).

## Running `governance-check`

The `code/rust` workspace resolves with a local `[patch]` for its native omega providers (`code/rust/.cargo/config.toml.example`). Run Cargo from `code/rust` so it discovers that configuration; see [the workspace instructions](../code/rust/README.md). With that in place:

```
cd code/rust && cargo run -p governance --bin governance-check -- check
```

Without it, use the standalone manifest, which points directly at the existing source files and has its own lockfile:

```
cargo build --locked --release --manifest-path governance/Cargo.toml
governance/target/release/governance-check --root . check --changed-since origin/main
```

This validates the governance crate. Full Rust workspace validation also needs
the configured native providers and the workspace checks above.

| Command | Purpose |
|---|---|
| `check [--changed-since REF]` | Verify every governed source, or only those changed since the merge base with `REF` (changed companions select their sources; a change to `policy.json` or `baseline.json` selects everything). With `REF`, also fails if `baseline.json` gained an entry without a `reason`. |
| `explain PATH` | Show the binding, token, each verifier's result and the baseline status of one source. |
| `list` | Print the governed population (CI compares it with `score_scope_contracts.py population`). |
| `baseline [--write]` | Recompute the baseline: keep entries that still fail with unchanged bytes, drop the rest. It never adds an entry by itself. |
| `baseline --write --allow-add --reason TEXT` | Also add the currently failing files that are not listed, each with the reason. Use only with the maintainer's agreement; CI prints every added entry and its reason. |

Run `governance-check baseline --write` after bringing grandfathered files up to the floor, so the list shrinks.

## Files

| Path | Contents |
|---|---|
| [`policy.json`](policy.json) | Floor, level and grade order, companion naming and schemas, populations, exclusions, pinned boilerplate, modes. Read by the Rust crate, every `build.rs`, `scripts/score_scope_contracts.py` and `scripts/contract_scores.py`. |
| [`baseline.json`](baseline.json) | The grandfather list, one entry per line. |
| [`schema/contract-score.v1.json`](schema/contract-score.v1.json) | JSON Schema of a companion. |
| [`hook/build.rs`](hook/build.rs) | The canonical build hook. |
| `code/rust/src/governance/` | The `governance` crate: score vocabulary (`score.rs`), policy and baseline (`policy.rs`), companion view (`descriptor.rs`), verifiers (`verify.rs`), repository access (`repo.rs`), build-script support (`buildtime.rs`), and the `governance-check` binary. |

The approved PR #433 conditional continuum module `CampaignDfmRefinementLimit` retains L3D under its exact-source `finite_proof_example` pin. This historical category also covers this conditional infinite-limit theorem; no physical continuum result or node-status promotion follows. The path, digest and user approval are recorded in [`approved_pr_433_continuum_exception_2026_10_26.json`](../dag/research/approved_pr_433_continuum_exception_2026_10_26.json).
