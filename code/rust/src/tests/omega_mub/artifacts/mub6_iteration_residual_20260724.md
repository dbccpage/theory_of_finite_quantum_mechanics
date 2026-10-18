MUB(6) iteration residual — 2026-07-24s (Y2Q2 POINT covers COMPLETE)
====================================================================

Branch / worktree: `grok/mub6-f6-external-b3`.

★ Y2⊗Q2 point covers — dual-orbit parity locked
-----------------------------------------------

| Seed | Point (presplit6 depth32) | Certified | Status |
|---|---|---|---|
| **(0,16)** | 64/64 + merged | **1_035_821** | **COMPLETE** |
| **(8,8)** | 64/64 + merged | **1_035_821** | **COMPLETE** |
| **(16,0)** | 64/64 + merged | **1_035_821** | **COMPLETE** |

Merged artifacts:

* `artifacts/dita_seed_F6_0_16_gauge_fixed_5_torus_presplit6_merged_complete.json`
* `artifacts/dita_seed_F6_8_8_gauge_fixed_5_torus_presplit6_merged_complete.json`
* `artifacts/dita_seed_F6_16_0_gauge_fixed_5_torus_presplit6_merged_complete.json`

**Dual-orbit cover parity (on disk):** all six genuine Dita seeds
`{Y2⊗Q1: (0,8),(8,0),(16,16)} ∪ {Y2⊗Q2: (0,16),(8,8),(16,0)}` share identical
POINT full-torus statistics:

```text
certified   = 1_035_821
off_torus   = 858_895
uncertified = 0
max_depth   = 32
min_gap     = 84790… / 69419…  (identical rational)
```

CLI: `mub_dita_seed_cover --merge` loads 64 on-disk chunks → `*_merged_complete.json`.

Unit test: `on_disk_presplit6_chunks_merge_all_three_y2q2_seeds_identical_to_y2q1`.

Prior landings
--------------

* Y2Q1 three seeds: point + δ=1/1000 full-torus covers complete (cert 1035821 / 1138055)
* C2 pairwise neighborhood disjointness charted (Y2Q1 only so far)
* ζ24 lattice 24×24 exhaustion locks dual orbits Q1/Q2
* ENC-1147 registry; kernel-reflection narrow/wide pilots

```text
AuthorityEffect: None
discrete lattice complete for base-MU class
all 6 genuine seed POINT covers complete with dual-orbit parity
Y2Q2 neighborhood (δ=1/1000) NOT yet farmed
continuous residual / basis-gluing still open
```

Next
----

1. Farm δ=1/1000 neighborhood covers for all three Y2Q2 seeds (presplit6 depth32).
2. Register dual-seed covers in moduli atlas + extend C2 distances to full 6-seed set.
3. ENC-1147 continuous families / basis-gluing theorem; full-torus kernel-reflection.
