# FINISH_DELTA_RECEIPT — QM_122 v0.1.16

**AuthorityEffect:** None. This receipt records a bounded Lean
replay plus a Python dual of named existing theorems. It is not
ordinary M_n(C), not Gleason, not CPTP, not U(1), not Stone, and
not a revision of the 2026-08-19 baseline.

## What changed

`H017Finish.remaining_import_list` records a declared disposition
for each frozen extra, paired with the narrower host facts proved
here. Field C, spectral extra, and continuous time are refused on
this host. CPTP, Gleason uniqueness, Hilbert-tensor uniqueness,
and the circle stay imported. Collapse non-reversibility and the
failure of a same-basis isometry are not CPTP obstructions; this
host defines no channel class. The table is not a requirements or
necessity theorem. SUSY and SU(3)×SU(2)×U(1) stay unassigned. Lean
axioms `{propext, Quot.sound}`.

Python dual of named existing theorems: `qm122_lib/qm122_dual.py`,
ten tests in `tests/test_qm122_dual.py`. The finite classifications
enumerate every reversible Bool or Bool×Bool map; the Gaussian-unit
check uses an exhaustive mod-two obstruction. Not a Lean theorem.

Historical drop-one OPEN verdicts at `dba1434b` are untouched.

## Source custody

`FINISH_DELTA_SOURCE_MANIFEST.txt` binds the Lean union closure of
`lake build FableHilbertWalk20260819`: 39 campaign modules, 27
J011Admitted roots, `lakefile.lean`, and `lean-toolchain` (68
sources). It does not stand for the separate Python replay inputs.

- Source-manifest SHA-256:
  `94dd40dcd1712bc4c9eb98fa1fcc65e7f51320c84187fcb75fc73f481e84e6c6`
- Aggregate closure SHA-256:
  `69cb0128cde69e9e4e24c5d155148c6f913325377a36e749b9fecff99c1512e8`

## Python replay custody

The Python replay is bound separately to these exact inputs:

| SHA-256 | Repo-relative path |
|---|---|
| `593fef377337e7f77409cf37cc1882783d69f2dbb7ab8acd88858a95d3bd9a8a` | `coda_university/coda_research/003_quantum_foundations/122_finite_hilbert_boundary_from_primitive_difference/pyproject.toml` |
| `e719426cbf90af4971bd3528bca9cf5697621d9e683d40316ebdfb363ae8ca37` | `coda_university/coda_research/003_quantum_foundations/122_finite_hilbert_boundary_from_primitive_difference/qm122_lib/__init__.py` |
| `26e3296b7ac265559bba9fe6954738a3dfe576638ef619b01751b7a7cc32ba77` | `coda_university/coda_research/003_quantum_foundations/122_finite_hilbert_boundary_from_primitive_difference/qm122_lib/qm122_dual.py` |
| `31aba883c41b14716b7cb61567f03be1e565cba9b6163dbfdeeb13808a8cecf0` | `coda_university/coda_research/003_quantum_foundations/122_finite_hilbert_boundary_from_primitive_difference/tests/test_qm122_dual.py` |

The commit that contains this receipt binds these bytes to history.

## Replay

From `lean4/genx/`, under the toolchain named by `lean-toolchain`:

```text
lake build FableHilbertWalk20260819
```

Result: **Build completed successfully (50 jobs)**. The printed
axiom reports for `remaining_import_list` and
`walk_root_remaining_import_list` contain only `propext` and
`Quot.sound`.

From the paper folder:

```text
python -m pytest tests/test_qm122_dual.py -q
```

Result: **10 passed**.

## Non-claims

- This does not recover ordinary \(M_n(\mathbb{C})\).
- This does not discharge Gleason uniqueness (R7).
- This does not construct the circle, CPTP channels, Hilbert
  tensor uniqueness, or Stone's theorem.
- This does not assign SUSY or SU(3)×SU(2)×U(1).
- This does not rewrite the historical drop-one census.
- Frozen `evidence/FRONTIER.md` stays SHA-256 `4c16a694…`.
