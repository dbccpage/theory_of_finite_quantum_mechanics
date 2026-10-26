/-!
# Rational constants of the Meron Euclidean thermodynamic limit

These are the exact rational identities and inequalities that
`docs/meron_euclidean_thermodynamic_limit.md` (TL-1 to TL-9) uses. Each
rational statement is cleared of denominators and checked over `Nat`.

Scope: only arithmetic. Nothing here states or proves the polymer bound, the
Kotecky-Preiss criterion, Cauchy or Schwarz estimates, the lift, the volume
limit or positivity. Those are written proofs. The module imports only Lean
core and declares no axiom. It is not imported by any build root. It compiles
standalone with Lean 4.33.1 (`lean MeronThermoLimitConstants.lean`, exit 0), and
`#print axioms` reports that none of its theorems depends on any axiom.
-/

namespace WitnessedDifference.MeronThermoLimitConstants

/-! TL-1: label norm `1/128`, `t = e^{1/128} - 1 <= 1/127`, `e < 3`, degree 7.
    `S_1 = (3/127) / (1 - 28 * 3/127) = 3/43`. -/

/-- `4 Delta e t < 1`: `28 * 3 < 127`. -/
theorem connected_series_converges : 28 * 3 < 127 := by decide

/-- `127 - 84 = 43`, so `S_1 = 3/43`. -/
theorem s1_denominator : 127 - 28 * 3 = 43 := by decide

/-- Kotecky-Preiss: `(Delta + 1) S_1 = 24/43 < 1`. -/
theorem s1_kotecky_preiss : (7 + 1) * 3 < 43 := by decide

/-- `M_1 = 2 S_1 64^2 = 24576/43`. -/
theorem m1_numerator : 2 * 3 * (64 * 64) = 24576 := by decide

/-! TL-6, the `g` gas: label norm `1/192`, `t <= 1/191`, degree 11. -/

theorem g_series_converges : 44 * 3 < 191 := by decide

theorem sg_denominator : 191 - 44 * 3 = 59 := by decide

theorem sg_kotecky_preiss : (11 + 1) * 3 < 59 := by decide

/-- `M_g = 2 S_g 576 * 96 = 331776/59`. -/
theorem mg_numerator : 2 * 3 * 576 * 96 = 331776 := by decide

/-- `M_F = 384/43 + 1/384 = 147499/16512`. -/
theorem mf_value : 384 * 384 + 43 = 147499 ∧ 43 * 384 = 16512 := by decide

/-- `G = 6 M_g + 1/2 = 3981371/118`. -/
theorem g_value : 2 * 6 * 331776 + 59 = 3981371 ∧ 2 * 59 = 118 := by decide

/-- `theta_* (18432 M_F + 288 G) = 1/4` with `theta_* = 2537/100281465600`,
    cleared of the denominators `16512` and `118`. -/
theorem theta_star_window :
    4 * 2537 * (18432 * 147499 * 118 + 288 * 3981371 * 16512)
      = 100281465600 * 16512 * 118 := by decide

/-- The window lies inside the disks used for `F` (`1/96`) and `g` (`1/288`). -/
theorem theta_star_small : 2537 * 288 < 100281465600 := by decide

/-- `1 / (768 (3 M_1 + 1/4)) = 43/56631360`: the pointwise zero-mode radius. -/
theorem zero_mode_radius : 768 * (4 * 3 * 24576 + 43) = 4 * 56631360 := by decide

/-- TL-4: `|D_y| <= M_1 (1 + 512/175) < 4 M_1`. -/
theorem lift_constant : 175 + 512 < 4 * 175 := by decide

/-- TL-5 on `theta <= 1/192`: the lift ratio is `128/192 = 2/3 < 1`. -/
theorem lift_ratio : 128 * 3 = 192 * 2 := by decide

/-- TL-9: `omega^2 khat >= theta^2/4` gives `khat >= theta^2/(16 pi^2 m^2)`. -/
theorem positivity_factor : 4 * 4 = 16 := by decide

/-- TL-9: `theta^2 (1/2 - c theta) > 0` for `theta < 1/(2c)`. Since `theta_* c = 1/4`
    (`theta_star_window`), `1/(2c) = 2 theta_* = 2537/50140732800`, which is the
    denominator identity below. -/
theorem positivity_window_double : 2 * 50140732800 = 100281465600 := by decide

/-- TL-9: the window lies inside the disks used for `F` and `g`:
    `2 theta_* = 2537/50140732800 < 1/288`, as `2537 * 288 < 50140732800`. -/
theorem positivity_window_in_disk : 2537 * 288 < 50140732800 := by decide

end WitnessedDifference.MeronThermoLimitConstants
