# Uniqueness ledger — W5.8

**AuthorityEffect: None**
**Date:** 2026-07-31 (LT d=3 deepen: explicit product vs composite witnesses)
**Axiom bind:** `AX-LIFT-V0`

| ID | Statement | Status | Evidence |
|---|---|---|---|
| UNIQ-REG-IFF | On registry: `satisfiesAxLiftV0 L ↔ L = complexHilbert` | **TOY-MECH** | Lean `satisfies_v0_iff_complex` |
| UNIQ-REG-COND | `satisfiesAxLiftV0 L → L = complexHilbert` | **TOY-MECH** | Lean `conditional_uniqueness_registry` |
| UNIQ-REG-EXIST | `satisfiesAxLiftV0 complexHilbert` | **TOY-MECH** | Lean `complex_exists_on_v0` |
| UNIQ-MIN-LT | Without LT, uniqueness fails | **TOY-MECH** | Lean `uniqueness_fails_without_lt` |
| UNIQ-LT3-IFF | LT3 iff complex on registry | **TOY-MECH** | Lean `satisfies_lt3_iff_complex` |
| UNIQ-LT3-NUM | LT3 explicit: ℂ 64=64, ℝ 27≠36, ℍ 216≠120 | **TOY-MECH** | Lean `complex_lt3_numbers` / `rebit_lt3_numbers` / `quat_lt3_numbers` |
| UNIQ-LT-D3 | LT bipartite d=3 iff complex | **TOY-MECH** | Lean `satisfies_lt_d3_iff_complex` |
| UNIQ-LT-D3-NUM | d=3 explicit: ℂ 81=81, ℝ 36≠45, ℍ 225≠153 | **TOY-MECH** | Lean `complex_lt_d3_numbers` / `rebit_lt_d3_numbers` / `quat_lt_d3_numbers` |
| UNIQ-LT-D3-PKG | d=3 deepen package + OPEN absolute/continuum fence | **TOY-MECH** | Lean `uniqueness_lt_d3_deepen_package` |
| UNIQ-C-LT-ID | Complex LT identity all $d_A,d_B$ | **TOY-MECH** | Lean `complex_lt_identity` |
| UNIQ-R-LIFT | R_LIFT pathway under V0 package host | **TOY-MECH / CONDITIONAL** | Lean `r_lift_conditional_on_v0_package` |
| UNIQ-R-LIFT-FINL1 | R_LIFT from FinL1 alone | **UNDERIVABLE** (toy) | Lean `r_lift_underivable_from_finL1` |
| UNIQ-ABS-OPEN | Absolute uniqueness outside registry | **OPEN** | fence flag |
| UNIQ-ABS-REFUSE | Absolute uniqueness claim | **REFUSED** | Lean `absolute_uniqueness_refused` |
| UNIQ-BIND | Relative to `AX-LIFT-V0` | **DOC-FROZEN** | freeze bind |

**Whole-row status for master table:**

`PARTIAL (TOY-MECH): registry iff under AX-LIFT-V0; LT minimality; LT3+LT d=3 explicit counts + uniqueness; R_LIFT pathway CONDITIONAL on V0 package; absolute OPEN/REFUSED; continuum OPEN/import`

## Nonclaims

- Not Jordan / Koecher–Vinberg uniqueness.
- Not W7.1 full recovery.
- Not Wave-5 exit.
- AuthorityEffect: None.
