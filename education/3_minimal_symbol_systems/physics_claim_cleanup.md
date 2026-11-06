# Physics claim and implementation cleanup

AuthorityEffect: None. Review date: 2026-10-08 (America/New_York).

> Historical record: the commands and outcomes below describe the October 8 cleanup.
> Subsequent manuscript consolidation and October 9 checks are recorded in
> [publication_review.md](publication_review.md). Earlier verification limits are
> not current failure claims.

Initial review baseline: `bf0dde5a93a9b9ffeca2dfc592584a4530c1ab0f`.
The cleanup incorporates subsequent main commit `dd3d9583c49d3a318eb5a04c30a0704a852fe618`
(PR #624), preserving its valid finite-algebra additions.
Scope: `002_s_n` and `003_minimal_symbol_system_n_mssn`. This is not a
repository-wide validation or a physical correctness certificate.

## Decision rule

Withdraw a claim when the cited artifact does not establish it. Remove an
implementation when its advertised result is manufactured from labels, supplied
verdicts or expected answers and no useful independent calculation would remain.
Preserve valid finite mathematics and numerical routines, with narrower names and
claims. A passing fixture, SQL comparison or Lean elaboration proves only its
stated proposition. A continuum disclaimer does not repair a false finite-model
claim.

The [file manifest](physics_claim_cleanup_manifest.json) records all 16 deleted
files and the reason for each. Four additional path changes preserve or replace
retained finite examples; they are listed separately from removals.

## Removed implementations and supporting artifacts

| Implementation family | Concrete defect | Disposition |
| --- | --- | --- |
| Supersymmetric CDT / Super-WDW | Sign and residual assigned as 1 and 0; a branch-selected formula presented as a solved constraint. | Evaluator, dependent tests and SQL/proof wrappers removed. |
| Topological charge / tunnelling | Target-charge matrix prescribed; claimed WDW defect selected by `is_tearing`. | Evaluator and its dependent certificate paths removed. |
| CDT sampler | Three-variable quadratic potential called Regge action; simplex counters changed without triangulation moves. | Sampler and verdict tests removed. Actual simplicial move routines remain elsewhere. |
| Kähler-Dirac doubling | Nonzero commutator computed, then residual overwritten with zero for a geometry label. | Evaluator and dependent verdict tests removed; boundary-matrix calculations retained. |
| Fermion sign suppression | Manufactured opposite-sign determinants have average sign zero, contradicting the claimed bound/certification. | Physics wrapper removed; finite sign-pairing arithmetic repaired and retained in Rust. |
| Chiral superconductor | Chern charges, surface modes and anomaly cancellation prescribed rather than obtained from a BdG/Berry calculation. | Evaluator, bridge, schema, premise-restating Lean wrapper and dependent tests removed. |
| Honeycomb braiding bridge | “Measured” phase copied from the theoretical phase; parity inferred by counting eigenvalue signs instead of calculating a Pfaffian. | Fabricated routines and bridge removed; lattice, link, flux and skew-matrix calculations retained. |

Mixed files were edited rather than deleted. Removed sections include the
analytical AJL-reproduction formula, fabricated sub-cubic benchmark, label-driven
locality certificate, supplied GR-002 recovery verdicts, and causal-firewall /
M-theory aggregate receipts. Obsolete SQL views and proof wrappers were removed
with their producers. Two tests referencing nonexistent `mssn_sn_tower/contracts`
paths were removed; those assertions provided no executable contract evidence in
this tree. Numerical checks and their negative cases remain.

## Repaired retained computations

- **Anyon matrices:** missing, partial or malformed stored F/R data cannot pass.
  The involution test is named for `F²=I`; it is not a pentagon equation. The B3
  relation is recomputed from stored matrices, including unitarity checks. Empty
  fusion evidence is rejected. The bridge reports fixture checks, not bisimulation.
- **Overlap matrices:** the index uses `Tr Gamma (I - a D/2)` for the declared
  `n_plus - n_minus` convention. Chirality is evaluated on the SVD nullspace,
  independently of coordinate parity and basis rotation.
- **Diffusion:** all start vertices contribute to the normalized graph trace;
  isolated vertices retain probability. Matter-example slopes come from the
  supplied graph, not a preset curve or collapse flag.
- **Finite histories:** empty, zero-state and non-finite inputs are rejected.
  The computed residual is an adjacent-step recurrence residual. Clock marginal
  Shannon entropy is labelled correctly; it is not entanglement entropy or a
  Wheeler-DeWitt Hamiltonian certificate.
- **Rational sign approximation:** the recorded error is a sampled error, not a
  rigorous supremum bound or minimax certificate. An independent sample grid is
  tested separately.
- **Finite orders:** comparable-pair fractions and link cuts remain; the heuristic
  dimension estimator is removed. Boundary nilpotence is recomputed before it is
  recorded. Scenario flags are described as scenario flags, not physical results.
- **Rust algebra:** opposite equal-weight signs cancel to average sign zero;
  empty ensembles, malformed signs and duplicate identifiers are rejected.
  Determinants, commutators, trace examples and the PR #624 so(3) calculations
  survive in `finite_algebra.rs`. Fixed-width rational/integer arithmetic remains
  subject to representation limits.
- **PR #624:** its trace and commutator-norm calculations are preserved. The
  declared quarter-sum of squared commutator norms is not labelled a BFSS/IKKT
  simulator. Its unsupported SQL bisimulation and six-stage quantum-gravity
  verification claims are withdrawn.

These are intentional API/schema changes. Consumers of removed certificate
methods, renamed receipt fields or the old `feynman_matrix_m_theory` module must
migrate to the scoped finite examples. Old persistent SQLite databases are not
migrated by this change; validation used fresh in-memory databases.

## Manuscripts

`000_mssn` retains the chain-map retraction obstruction theorem. Its graph paragraph
now distinguishes edges joining separate components from edges within a component,
and permits self-loops when characterizing the maximum number of components.

`001_pregenesis_through_mssn` is rewritten as an architectural crosswalk. It corrects
the binary/decimal free-monoid claim, separates alphabet/stage/atlas indices,
withdraws finite-univalence certification, supplies the missed CHSH orientation
counterexample, and distinguishes actual computations from required behavior.
PGM-001 through PGM-038 have explicit dispositions. The papers remain separate;
use `000_mssn` as the mathematical backbone before consolidating them.

## Validation actually performed

Run from this MSS-N directory:

```sh
python -m pytest code/tests/test_physics_claim_regressions.py domains/physics/tests domains/ansi_sql/tests/test_nonabelian_anyon_bisimulation.py domains/ansi_sql/tests/test_honeycomb_flux.py -q -k 'not lean and not full_nonabelian'
python -m pytest domains/cosmology_astrophysics/tests -q
cargo test --manifest-path code/rust/Cargo.toml
```

Results: **82 Python tests passed**, with four Lean-dependent checks deselected;
**24 cosmology/order tests passed**; **49 Rust tests passed**, including the
preserved PR #624 additions. The two Python commands use separate processes because
these domain examples reuse top-level module names.

The 12 counterexample cases in `test_physics_claim_regressions.py` were observed
failing before their fixes (eight initial cases, then four additional cases), then
passing. Four new Rust sign-pair tests pass; their initial pre-fix execution was
blocked by missing dependencies, so no observed Rust red run is claimed.

All 92 retained Python files parse. The three edited SQL schemas load into fresh
SQLite databases and all 17 retained views resolve. Modified-document links into
the two reviewed strands and `git diff --check` were checked before publication.

**Remaining verification limits:** Lean 4.34.0 was downloaded, but its executable
failed at startup in this environment with `error: failed to locate application`.
No successful Lean compilation is claimed for this revision; the four excluded
checks and the renamed Lean library remain a required verification step. A broader
codec test collection also required `check_grammars` outside this two-strand
snapshot and was not completed. Full-repository CI and downstream API consumers
have not been validated here. The pull request is a draft for these outstanding
checks and review of the substantial withdrawals.
