import Mathlib.Tactic

/-!
# Campaign Module: `MAJ-OPEN-LIEB-ROBINSON-LOCALITY` (`TFQ-1149`)

Formalizes the discrete Lieb-Robinson light-cone support expansion model,
syndrome-recovery viability horizon inequalities, logical-cycle collision
thresholds, discrete commutator tail suppression outside the causal cone,
and explicit scope fences for `MAJ-OPEN-LIEB-ROBINSON-LOCALITY` (`TFQ-1149`,
stage `MAJORANA`, status `OPEN` preserved).

**Scope boundary**: This module formalizes the discrete algebraic relationship
between Lieb-Robinson causal-cone growth $\mathrm{wt}(t) = w_0 + 2 v_{\mathrm{LR}} t$
and the Theorem 4.4 / Corollary 4.5 syndrome recovery threshold $2\,\mathrm{wt}(t) < d$.
It does not derive continuous-time Banach-algebra Lieb-Robinson bounds for
microscopic superconducting Hamiltonians and does not claim a general verdict
on physical quantum computing viability (`OPEN` status preserved).
-/

namespace CampaignMajOpenLiebRobinsonLocality

/-- One-sided Lieb-Robinson causal radius after `t` discrete steps at velocity `vLR`
starting from initial radius `r0`. -/
def lrCausalRadius (r0 vLR t : ℕ) : ℕ :=
  r0 + vLR * t

/-- Two-sided 1D contiguous cluster support diameter after `t` discrete steps
at velocity `vLR` starting from initial fault weight `w0`. -/
def lrSupportWeight1D (w0 vLR t : ℕ) : ℕ :=
  w0 + 2 * vLR * t

/-- Scaled discrete Lieb-Robinson commutator tail numerator `c0 * g^t`. -/
def lrTailNum (c0 g t : ℕ) : ℕ :=
  c0 * g ^ t

/-- Spatial decay denominator `mu^dist` at lattice separation `dist`. -/
def lrSpaceDenom (mu dist : ℕ) : ℕ :=
  mu ^ dist

/-- Theorem 1: One-sided Lieb-Robinson causal radius composes additively over
sequential evolution intervals `t1` and `t2` and is monotone non-decreasing. -/
theorem lieb_robinson_causal_radius_additive (r0 vLR t1 t2 : ℕ) :
    lrCausalRadius (lrCausalRadius r0 vLR t1) vLR t2 =
      lrCausalRadius r0 vLR (t1 + t2) ∧
    r0 ≤ lrCausalRadius r0 vLR t1 := by
  dsimp [lrCausalRadius]
  constructor
  · ring
  · omega

/-- Theorem 2: Two-sided 1D support weight composes additively across time steps
and grows strictly by `2 * vLR` per step whenever `0 < vLR`. -/
theorem lieb_robinson_1d_support_diameter_growth (w0 vLR t1 t2 : ℕ)
    (hv : 0 < vLR) :
    lrSupportWeight1D (lrSupportWeight1D w0 vLR t1) vLR t2 =
      lrSupportWeight1D w0 vLR (t1 + t2) ∧
    lrSupportWeight1D w0 vLR t1 < lrSupportWeight1D w0 vLR (t1 + 1) := by
  dsimp [lrSupportWeight1D]
  constructor
  · ring
  · nlinarith

/-- Theorem 3: For any two errors `e1, e2` propagated for `t` steps with weights
`w1, w2 ≤ lrSupportWeight1D w0 vLR t` and difference weight `wDiff ≤ w1 + w2`,
the difference weight is bounded by `2 * w0 + 4 * vLR * t`. -/
theorem lieb_robinson_pair_difference_weight_bound
    (w0 vLR t w1 w2 wDiff : ℕ)
    (hw1 : w1 ≤ lrSupportWeight1D w0 vLR t)
    (hw2 : w2 ≤ lrSupportWeight1D w0 vLR t)
    (hdiff : wDiff ≤ w1 + w2) :
    wDiff ≤ 2 * lrSupportWeight1D w0 vLR t ∧
    2 * lrSupportWeight1D w0 vLR t = 2 * w0 + 4 * vLR * t := by
  dsimp [lrSupportWeight1D] at *
  constructor
  · omega
  · ring

/-- Theorem 4: Syndrome recovery viability within the Lieb-Robinson horizon:
if `2 * lrSupportWeight1D w0 vLR t < d`, then no pair of propagated errors
with weights `w1, w2 ≤ lrSupportWeight1D w0 vLR t` and difference weight
`wDiff ≤ w1 + w2` can reach the minimum non-stabilizer logical distance `d`. -/
theorem syndrome_recovery_viability_within_lr_horizon
    (w0 vLR t d w1 w2 wDiff : ℕ)
    (h_viable : 2 * lrSupportWeight1D w0 vLR t < d)
    (hw1 : w1 ≤ lrSupportWeight1D w0 vLR t)
    (hw2 : w2 ≤ lrSupportWeight1D w0 vLR t)
    (hdiff : wDiff ≤ w1 + w2) :
    wDiff < d ∧ ¬ (d ≤ wDiff) := by
  dsimp [lrSupportWeight1D] at *
  omega

/-- Theorem 5: Monotonicity of the repair viability window: if syndrome recovery
is viable at extraction latency `tHi`, then it is viable at every earlier latency
`tLo ≤ tHi`, with strictly larger distance margin when `tLo < tHi` and `0 < vLR`. -/
theorem critical_repair_horizon_monotonicity
    (w0 vLR tLo tHi d : ℕ)
    (hv : 0 < vLR)
    (hlt : tLo < tHi)
    (h_viable_hi : 2 * lrSupportWeight1D w0 vLR tHi < d) :
    2 * lrSupportWeight1D w0 vLR tLo < 2 * lrSupportWeight1D w0 vLR tHi ∧
    2 * lrSupportWeight1D w0 vLR tLo < d ∧
    2 * lrSupportWeight1D w0 vLR tLo + 4 * vLR * (tHi - tLo) =
      2 * lrSupportWeight1D w0 vLR tHi := by
  dsimp [lrSupportWeight1D] at *
  have hsub : tLo + (tHi - tLo) = tHi := Nat.add_sub_of_le (le_of_lt hlt)
  refine ⟨by nlinarith, by nlinarith, ?_⟩
  nlinarith

/-- Theorem 6: Horizon overflow logical collision: when propagation time `t`
causes `d ≤ 2 * lrSupportWeight1D w0 vLR t`, a weight-`d` logical cycle splits
into two error weights `w1 = d / 2` and `w2 = d - d / 2` that both lie inside
the propagated ball `lrSupportWeight1D w0 vLR t` and sum to `d`. -/
theorem lieb_robinson_horizon_exceeded_logical_collision
    (w0 vLR t d : ℕ)
    (h_overflow : d ≤ 2 * lrSupportWeight1D w0 vLR t) :
    let w1 := d / 2
    let w2 := d - d / 2
    w1 + w2 = d ∧
    w1 ≤ lrSupportWeight1D w0 vLR t ∧
    w2 ≤ lrSupportWeight1D w0 vLR t := by
  dsimp [lrSupportWeight1D] at *
  omega

/-- Theorem 7: Discrete Lieb-Robinson commutator tail suppression outside the
light cone: for `0 < c0`, `1 < g`, and `g ≤ mu`, whenever `t < dist`, the tail
numerator `c0 * g^t` is strictly smaller than `c0 * mu^dist`. -/
theorem discrete_commutator_tail_decay_recurrence
    (c0 g mu t dist : ℕ)
    (hc0 : 0 < c0)
    (hg : 1 < g)
    (hgmu : g ≤ mu)
    (hcone : t < dist) :
    lrTailNum c0 g t < c0 * lrSpaceDenom mu dist := by
  dsimp [lrTailNum, lrSpaceDenom]
  have h1 : g ^ t ≤ mu ^ t := Nat.pow_le_pow_left hgmu t
  have hmu_gt1 : 1 < mu := lt_of_lt_of_le hg hgmu
  have h2 : mu ^ t < mu ^ dist := (Nat.pow_lt_pow_iff_right hmu_gt1).mpr hcone
  have h3 : g ^ t < mu ^ dist := lt_of_le_of_lt h1 h2
  exact Nat.mul_lt_mul_of_pos_left h3 hc0

/-- Theorem 8: Classical syndrome-routing communication delay constraint: if a
global decoder on an array of linear size `L` requires routing time `tComm`
satisfying `L ≤ vCl * tComm` (`0 < vCl`), then viability `2 * lrSupportWeight1D w0 vLR tComm < d`
implies `2 * w0 * vCl + 4 * vLR * L < d * vCl`. -/
theorem syndrome_measurement_communication_delay_bound
    (w0 vLR vCl L tComm d : ℕ)
    (hL : L ≤ vCl * tComm)
    (h_viable : 2 * lrSupportWeight1D w0 vLR tComm < d) :
    2 * w0 * vCl + 4 * vLR * L ≤ 2 * lrSupportWeight1D w0 vLR tComm * vCl ∧
    (0 < vCl → 2 * w0 * vCl + 4 * vLR * L < d * vCl) := by
  dsimp [lrSupportWeight1D] at *
  constructor
  · nlinarith
  · intro hvCl
    nlinarith

/-- Theorem 9: Tetron torus viability window comparison: for initial weight `w0 = 1`
and unit Lieb-Robinson velocity `vLR = 1`:
- on the `L = 4` torus (`d = 4`), `t = 1` already exceeds the recovery threshold (`6 > 4`);
- on the `L = 7` torus (`d = 7`), `t = 1` is viable (`6 < 7`) while `t = 2` overflows (`10 > 7`). -/
theorem torus_tetron_viability_window_witness :
    2 * lrSupportWeight1D 1 1 1 = 6 ∧
    4 < 2 * lrSupportWeight1D 1 1 1 ∧
    2 * lrSupportWeight1D 1 1 1 < 7 ∧
    7 < 2 * lrSupportWeight1D 1 1 2 ∧
    2 * lrSupportWeight1D 1 1 2 = 10 := by
  decide

/-- Theorem 10: Scope fence for `MAJ-OPEN-LIEB-ROBINSON-LOCALITY` (`TFQ-1149`):
packages support growth, viability vs collision dichotomy, and explicit open-scope
boundary (continuous-time Banach-algebra Lieb-Robinson bounds and physical
device viability verdicts are not claimed). -/
theorem lieb_robinson_locality_open_scope_fence
    (w0 vLR t d : ℕ) :
    (2 * lrSupportWeight1D w0 vLR t < d ↔
      2 * w0 + 4 * vLR * t < d) ∧
    (d ≤ 2 * lrSupportWeight1D w0 vLR t →
      d / 2 ≤ lrSupportWeight1D w0 vLR t ∧
      d - d / 2 ≤ lrSupportWeight1D w0 vLR t) ∧
    (2 * lrSupportWeight1D 1 1 2 - 2 * lrSupportWeight1D 1 1 1 = 4) := by
  dsimp [lrSupportWeight1D]
  have h_eq : 2 * (w0 + 2 * vLR * t) = 2 * w0 + 4 * vLR * t := by ring
  refine ⟨by rw [h_eq], ?_, by decide⟩
  intro h
  omega

#print axioms lieb_robinson_causal_radius_additive
#print axioms lieb_robinson_1d_support_diameter_growth
#print axioms lieb_robinson_pair_difference_weight_bound
#print axioms syndrome_recovery_viability_within_lr_horizon
#print axioms critical_repair_horizon_monotonicity
#print axioms lieb_robinson_horizon_exceeded_logical_collision
#print axioms discrete_commutator_tail_decay_recurrence
#print axioms syndrome_measurement_communication_delay_bound
#print axioms torus_tetron_viability_window_witness
#print axioms lieb_robinson_locality_open_scope_fence

end CampaignMajOpenLiebRobinsonLocality
