# Lean 4 Build Provenance Receipt for GS-002

**AuthorityEffect:** None
**Package:** `gs002` (library target: `GS002`)
**Date:** 2026-09-28
**Final Build Command:** `set LEAN_NUM_THREADS=4&&lake build GS002`
**Toolchain:** `leanprover/lean4:v4.34.0-rc1`
**Lean Version:** `Lean (version 4.34.0-rc1, x86_64-w64-windows-gnu, commit 3447a668783dbce1a8fdb97101dd067687b2b418, Release)`
**Lake Version:** `Lake version 5.0.0-src+3447a66 (Lean version 4.34.0-rc1)`
**Mathlib Pinned Revision:** `de5ce8a9a66a4aa68a9bdbb35b63a06d34d9ca11`
**Status:** Fresh-worktree dependency build plus bounded cache-preserving resume completed mechanically (final exit code: 0; 1678 jobs)
**Declaration Census:** 39 theorem/lemma declarations plus `SO2Matrix`; 40 of 40 explicit targets reported
**Sorries:** 0
**Admits:** 0
**Custom Axioms:** 0

---

## Dependency and Configuration Hash Manifest

| File | SHA-256 Digest |
| --- | --- |
| `lean-toolchain` | `cdbc6c372a2b37ad94430a6cec69cedfa4d36f255bfd968773fd91bf7a1746bf` |
| `lakefile.lean` | `fec94ad4282faa0fb85dbac9d573f4852cb9b9024abbab6c8dcd90bcce5228ba` |
| `lake-manifest.json` | `a7f4d6238688cd0df6d6046bdd7732db26f745e992a83033d69bf765b58b8b07` |

---

## Source Hash Manifest

| Source File | SHA-256 Digest |
| --- | --- |
| `gs002_core.lean` | `f3600594808f07a932e1d66ccbb63177f50dacc85ac8dbc40e0e46c3046994fe` |
| `gs002_l003_01_triangle_separation.lean` | `4e8ec317704d05ef108c4f0f45eb844971257c98a09a23c320d656339ecfc2d9` |
| `gs002_l003_02_s_ok_local_gauge.lean` | `1929085abe788ac8a2ecd12ad406280bc4ddfd774a663ad6670ef6f9377c13e8` |
| `gs002_l003_03_weighted_cycle_quotient.lean` | `339a2fec774e212e747e582a9c9085da47c54fc9342999bb484baaab8ef43b07` |
| `gs002_l003_04_edge_decomposition.lean` | `5acae8a1717259b200a02f066de835027af83903f21cdc370c20a8cd87881d31` |
| `gs002_l003_05_mixed_closure_bound.lean` | `bd5b04e170a19c480c8b9e26fe0843a09315dade353fedf8183ad6917df3b440` |
| `gs002_l003_06_mixed_duality_weak.lean` | `aa7dacff0a02e7a68f53c5e20665e51dc3e1cd43a88b8272fe4217d00f0fbb37` |
| `gs002_l003_07_cycle_exactness.lean` | `b2bbcd223f6cda9be91e7f9a37274becae258ce2a25e5291d38554e47a282fb3` |

---

## Complete Axiom Audit

Every `theorem` and `lemma` declaration in roots 01 through 07 is an explicit
`#print axioms` target. The additional public definition `SO2Matrix` remains an
audited target. All 40 results use only the scoped standard Lean 4 axioms; no
target requires `native_decide` or a synthetic custom axiom.

| Module | Declaration | Axioms |
| --- | --- | --- |
| `01_triangle_separation` | `coordinate_separable_triangle_cost` | `[propext, Classical.choice, Quot.sound]` |
| `01_triangle_separation` | `euclidean_triangle_squared_cost` | `[propext, Classical.choice, Quot.sound]` |
| `01_triangle_separation` | `coordinate_separable_triangle_cost_squared` | `[propext, Classical.choice, Quot.sound]` |
| `01_triangle_separation` | `triangle_separation` | `[propext, Classical.choice, Quot.sound]` |
| `01_triangle_separation` | `normalized_triangle_observer_separation` | `[propext, Classical.choice, Quot.sound]` |
| `02_s_ok_local_gauge` | `SO2Matrix` | `[propext, Classical.choice, Quot.sound]` |
| `02_s_ok_local_gauge` | `sphere_const_of_unit_transitive` | `[propext, Classical.choice, Quot.sound]` |
| `02_s_ok_local_gauge` | `so_k_local_gauge_simplified` | `[propext, Classical.choice, Quot.sound]` |
| `02_s_ok_local_gauge` | `so_k_local_gauge_from_unit_transitive` | `[propext, Classical.choice, Quot.sound]` |
| `02_s_ok_local_gauge` | `so2_transitive_on_circle` | `[propext, Classical.choice, Quot.sound]` |
| `02_s_ok_local_gauge` | `so2_unit_transitive` | `[propext, Classical.choice, Quot.sound]` |
| `02_s_ok_local_gauge` | `so2_circle_const` | `[propext, Classical.choice, Quot.sound]` |
| `03_weighted_cycle_quotient` | `cycleCirculation_sub` | `[propext, Classical.choice, Quot.sound]` |
| `03_weighted_cycle_quotient` | `cycleCirculation_sub_eq_zero_of_eq` | `[propext, Classical.choice, Quot.sound]` |
| `03_weighted_cycle_quotient` | `cycleCirculation_eq_of_sub_eq_zero` | `[propext, Classical.choice, Quot.sound]` |
| `03_weighted_cycle_quotient` | `same_cycle_circulation_iff_zero_difference` | `[propext, Classical.choice, Quot.sound]` |
| `03_weighted_cycle_quotient` | `circulation_singleEdgeCochain` | `[propext, Classical.choice, Quot.sound]` |
| `03_weighted_cycle_quotient` | `cost_singleEdgeCochain` | `[propext, Classical.choice, Quot.sound]` |
| `03_weighted_cycle_quotient` | `cost_singleEdgeCochain_normalized` | `[propext, Classical.choice, Quot.sound]` |
| `03_weighted_cycle_quotient` | `normalized_cycle_lower_bound` | `[propext, Classical.choice, Quot.sound]` |
| `03_weighted_cycle_quotient` | `normalized_cycle_quotient` | `[propext, Classical.choice, Quot.sound]` |
| `03_weighted_cycle_quotient` | `weighted_cycle_lower_bound` | `[propext, Classical.choice, Quot.sound]` |
| `03_weighted_cycle_quotient` | `weighted_cycle_quotient` | `[propext, Classical.choice, Quot.sound]` |
| `04_edge_decomposition` | `restrictEdges_empty` | `[propext, Classical.choice, Quot.sound]` |
| `04_edge_decomposition` | `restrictEdges_univ` | `[propext, Classical.choice, Quot.sound]` |
| `04_edge_decomposition` | `edge_decomposition_on_finset` | `[propext, Classical.choice, Quot.sound]` |
| `04_edge_decomposition` | `separable_of_finite_disjoint_additive` | `[propext, Classical.choice, Quot.sound]` |
| `05_mixed_closure_bound` | `closure_repair_invariant_add` | `[]` |
| `05_mixed_closure_bound` | `closure_repair_invariant_sub` | `[propext]` |
| `05_mixed_closure_bound` | `closure_bound_from_minimizer` | `[propext, Classical.choice, Quot.sound]` |
| `05_mixed_closure_bound` | `closure_bound_from_cofinal_scaled_repairs` | `[propext, Classical.choice, Quot.sound]` |
| `06_mixed_duality_weak` | `dual_witness_repair_invariant_sub` | `[propext, Classical.choice, Quot.sound]` |
| `06_mixed_duality_weak` | `dual_witness_bound_from_minimizer` | `[propext, Classical.choice, Quot.sound]` |
| `06_mixed_duality_weak` | `dual_witness_bound_from_cofinal_repairs` | `[propext, Classical.choice, Quot.sound]` |
| `07_cycle_exactness` | `cycleCirculation_anchoredCycleCochain` | `[propext, Classical.choice, Quot.sound]` |
| `07_cycle_exactness` | `cycleCirculation_add` | `[propext, Classical.choice, Quot.sound]` |
| `07_cycle_exactness` | `cycleCirculation_sub_anchoredCycleCochain` | `[propext, Classical.choice, Quot.sound]` |
| `07_cycle_exactness` | `zero_circulation_iff_anchored_cycle` | `[propext, Classical.choice, Quot.sound]` |
| `07_cycle_exactness` | `same_circulation_iff_difference_anchored_cycle` | `[propext, Classical.choice, Quot.sound]` |
| `07_cycle_exactness` | `same_circulation_iff_anchored_cycle_coset` | `[propext, Classical.choice, Quot.sound]` |

---

## Build Output Summary

The build began from the exact PR worktree without dependency artifacts.
Unbounded host concurrency exposed transient Windows reads of existing Lean
toolchain and dependency artifacts. The same build cache was preserved and
resumed with bounded worker counts; the final cap never exceeded four.

```text
Final command: set LEAN_NUM_THREADS=4&&lake build GS002
Built gs002_l003_01_triangle_separation
Built gs002_l003_02_s_ok_local_gauge
Built gs002_l003_03_weighted_cycle_quotient
Built gs002_l003_04_edge_decomposition
Built gs002_l003_05_mixed_closure_bound
Built gs002_l003_06_mixed_duality_weak
Built gs002_l003_07_cycle_exactness
Built gs002_core
Build completed successfully (1678 jobs).
```

## Retained evidence note (2026-10-02)

This remains the dated 2026-09-28 receipt. All eight Lean sources and the three dependency/configuration files are unchanged and their recorded hashes match. The review host has no usable pinned `lake` command, so this review does not claim a fresh Lean build. The required release verifier still requires one and compares the exact axiom dependency sets. See `../docs/publication_review.md`.
