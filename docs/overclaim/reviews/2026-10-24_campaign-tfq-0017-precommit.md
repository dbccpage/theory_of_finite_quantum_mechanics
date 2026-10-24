# Statement-Match Review: TFQ-0017 (`FINITE_QCD`)

- **Reviewed node**: `TFQ-0017`
- **Verdict**: `QUALIFIES`
- **Review date**: `2026-10-24`
- **Reviewer**: Campaign automated & human-guided pre-commit audit

## 1. Statement-to-Evidence Alignment

| Statement Clause | Formal / Computational Anchor | Match Assessment |
|---|---|---|
| `Q8` lies in `SU(2)` by the special-unitary check, and `Q8` is a finite subgroup of `SU(2)`, not `SU(2)` itself | `CampaignTfq0017FiniteQcd.quat_norm_multiplicative_four_square_identity`, `CampaignTfq0017FiniteQcd.q8_proper_subgroup_of_su2_pythagorean_witness` | Exact match: spinor norm multiplicativity and Pythagorean unit quaternion `(3/5, 4/5, 0, 0)` with unit norm `1` and non-integer coordinate `3/5 != 0, ±1` outside `Q_8`. |
| `su2.rs` holds quaternions, the adjoint cover, spinor norms, and binary polyhedral groups on a 2D carrier | `CampaignTfq0017FiniteQcd.su2_adjoint_cover_two_to_one_kernel`, `CampaignTfq0017FiniteQcd.binary_polyhedral_orders_and_2d_carrier` | Exact match: 2-to-1 adjoint double cover `q` vs. `-q` and binary polyhedral orders `8, 24, 48, 120` on a 2D spinor carrier. |
| They do not provide the three diagonal color labels used by the weighted Gell-Mann family; do not promote the `SU(2)` quaternion shadow to `su(3)_c` | `CampaignTfq0017FiniteQcd.su2_cartan_rank_one_vs_su3_gell_mann_cartan_rank_two_fence`, `CampaignTfq0017FiniteQcd.gell_mann_diagonal_orthogonality_and_three_color_separation`, `CampaignTfq0017FiniteQcd.su2_cartan_cannot_span_gell_mann_lambda8_fence`, `CampaignTfq0017FiniteQcd.su2_zero_d_symbol_vs_su3_lambda8_square_fence`, `CampaignTfq0017FiniteQcd.tfq0017_su2_shadow_kept_on_gauge_side_scope_ledger_fence`, `checks/independent/tfq-0017.py` | Explicit Cartan rank (`1 != 2`), 3-color weight separation, `d_{888} != 0`, and scope-ledger fences keeping the `SU(2)` shadow on the gauge side of the cut. |

## 2. Claim Hygiene & Fence Check

- **What it supports**: Quaternion four-square spinor norm multiplicativity, `Q_8 ⊂neq SU(2)`, the 2-to-1 adjoint cover `SU(2) -> SO(3)`, binary polyhedral orders `8, 24, 48, 120`, Gell-Mann diagonal orthogonality and 3-color weight separation, and non-promotion fences separating the 2D `SU(2)` shadow from `su(3)_c`.
- **What it does not support**: Promoting `Q_8` flux operators or 2D `SU(2)` spinors to `su(3)_c` color generators or continuum QCD.
- **Forbidden words scan**: Zero occurrences of banned hype terms.
