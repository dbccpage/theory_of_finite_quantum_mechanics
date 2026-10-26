# Lean 4 provenance and verification receipt for GS-000

Date: 2026-09-28

## Environment and build status

- Build command: `cmd.exe /d /c "set LEAN_NUM_THREADS=2&&lake build PaperGS003"`
- Build location: short Windows scratch copy at `C:\wt\p009l`
- Build result: exit 0, `Build completed successfully (915 jobs)`
- Module target: `PaperGS003`
- Lean: `4.34.0-rc1`, commit
  `3447a668783dbce1a8fdb97101dd067687b2b418`
- Lake: `5.0.0-src+3447a66`
- mathlib pin: `de5ce8a9a66a4aa68a9bdbb35b63a06d34d9ca11`
- Standard axioms appearing in the 43 declared theorem reports:
  `{propext, Classical.choice, Quot.sound}`
- Custom axioms: 0
- Sorries: 0 across the listed proof sources
- Admits: 0 across the listed proof sources

The checked command compiles the named library target and emits the
`#print axioms` results declared in its source files. The receipt attests only
to those exact declarations at the digests below; it does not establish the
open manuscript LGGR specialization or upgrade any publication status.

## File digests (SHA-256)

- `primitive_difference.lean`:
  `73b5b468e5f64a8bdfb778822536e732a01183de02947594b352ea2c6ba12a95`
  (789 lines, 0 sorries)
- `gs003_core.lean`:
  `19e986f3ab9c061ccd5c1c0aab74e79e7848456e2c1fb9b124c48a6a37df91ab`
  (3 lines, 0 sorries)
- `gs003_coordinate_l1.lean`:
  `167995fc4b15e64d0b383d40798c44fa5bdb858ba1ff86cbb20fc7e0195e3d8c`
  (1,343 lines, 0 sorries)
- `gs003_su2_curvature.lean`:
  `21500c03ecdd77c9acd45688a1cb894c1165497805f1d481a7648bc5cbccb7a9`
  (202 lines, 0 sorries)
- `gs003_schatten_orthogonal.lean`:
  `cdae00f003a7fafe59707c825f1c1687ffb41f3e5b0b8a102e8db499ad4a7fa0`
  (261 lines, 0 sorries)

## Mechanized scope

- Theorem 1 finite real scalar core (`coord_real_l1_weighted_sum`,
  `coord_real_l1_scalar_sum_succ`, `coord_real_l1_exists_scalar_succ`,
  `coord_real_l1_norm_scalar_positive_succ`).
- Theorem 2 declared-orbit aggregation cores
  (`orbit_weighted_l1_aggregation`, `single_edge_weighted_l1_total`).
- Theorem 3 edge-uniformity collapse bridges
  (`orbit_uniform_l1_collapse`, `edge_uniformity_collapses_finite_l1`).
- Counterexamples CE1-CE4 and the narrow CE5 helper
  (`ce5_lp_not_homogeneous`). The helper fixes `p = 2` and shows a natural-number
  scaling inequality; it does **not** verify manuscript CE5, which remains
  `OPEN / NOT_VERIFIED`.
- LGGR and EPK quotient boundary artifacts
  (`lggr_edgewise_uniformity_obstruction`,
  `scalar_total_lggr_obstruction_succ`). These finite obstruction lemmas do
  **not** close the manuscript's cross-graph/real-cochain LGGR step in section
  3.5.
- Non-Abelian SU(2) plaquette curvature defect and gauge-invariance lemmas.
- Schatten 1-norm orthogonal additivity and the listed finite-dimensional
  comparison lemmas.

The companion `axiom_report.txt` records the exact 43 declared theorem-level
outputs from this build.

## Scope clarification, 2026-10-02 (no new build)

The proof sources and their recorded digests are unchanged. CE1's helper is
a quadratic arithmetic model, not the real Euclidean norm; CE3's helper is a
coupled polynomial, not the real cancellation seminorm. The LGGR helpers use
records whose diagnostic and weight fields can vary independently. They do
not contradict descent of a weighted total through per-edge diagnostic
equality when the graph and weight profile are fixed. This clarification
does not attest a fresh Lean compilation.
