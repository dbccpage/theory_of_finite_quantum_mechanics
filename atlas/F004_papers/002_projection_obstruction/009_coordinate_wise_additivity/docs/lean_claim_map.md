# Lean claim map — GS-000 / 009

| Theme | Lean module | Status |
|---|---|---|
| Core hub | [`gs003_core.lean`](../lean4/gs003_core.lean) | hub |
| Coordinate L1 cores | [`gs003_coordinate_l1.lean`](../lean4/gs003_coordinate_l1.lean) | PARTIAL cores (CE / Thm bridges as manuscript states) |
| Full Thm 1–3 prose | — | PROSE / conditional; not fully derived in Lean |
| CE1 / CE3 prose witnesses | `ce1_quadratic_not_l1_scalar` / `ce3_cross_edge_coupling_not_edge_local` | PARTIAL arithmetic analogues; quadratic / polynomial over naturals, rather than real L2 / real cancellation |
| CE5 prose claim | `ce5_lp_not_homogeneous` | OPEN / NOT_VERIFIED; helper shows only an exact arithmetic witness |
| LGGR §3.5 prose claim | finite `Nat` quotient helpers | OPEN / NOT_VERIFIED; not the real-cochain manuscript claim |

The record helpers can vary weights. For a fixed graph and profile, equal
per-edge diagnostics imply equal weighted totals; §3.5 now states that
factorization explicitly. No Lean source was changed or freshly compiled by
the 2026-10-02 review.

Do not market as full Theorems 1–3 mechanized.
