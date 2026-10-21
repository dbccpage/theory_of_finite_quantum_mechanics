import Mathlib.Algebra.Order.Archimedean.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith

/-!
# Self-obstructing repair: the net-rate backlog and the fresh-supply budget

Origin: dag/research/quantum_computation_self_obstruction.md (QCV-Q1, QCV-Q5, QCV-Q6)
Claim: in the declared backlog model `q_{t+1} = max 0 (q_t + lam + g * mu - mu)` (the DS-QM101 queue
with the repair step's own residual `g * mu` added to the generation rate), the backlog stays
bounded exactly when the net repair rate `(1 - g) * mu` covers the computation's generation rate
`lam`.  If every unit of repair generates at least one unit of new residual (`1 <= g`) no repair
rate bounds the backlog.  When the repair rate is the capacity of a fresh-ancilla supply,
`mu = kappa * r`, the supply `r` must reach `lam / ((1 - g) * kappa)`; with no fresh supply the
backlog grows linearly.  A fresh-mark budget `B` bounds the number of rounds by `B / rmin`.
AuthorityEffect: None
Scope Fence: the rates `lam`, `g`, `kappa`, `r` are declared inputs of a finite model.  Nothing
here measures a device, derives `g` for any code, or says that any supply is available.
-/

namespace QcSelfObstruction

/-- Backlog of unrepaired residual, measured in a fixed unit (the `Phi_1` repair cost of the
declared packet): each round the computation adds `lam`, the repair step removes `mu` and, being a
noisy circuit, adds `g * mu` of its own; the backlog cannot go negative. -/
def backlog (lam g mu q0 : ℚ) : ℕ → ℚ
  | 0 => q0
  | t + 1 => max 0 (backlog lam g mu q0 t + (lam + g * mu - mu))

/-- Net drift per round. -/
def drift (lam g mu : ℚ) : ℚ := lam + g * mu - mu

theorem backlog_nonneg {lam g mu q0 : ℚ} (h : 0 ≤ q0) (t : ℕ) : 0 ≤ backlog lam g mu q0 t := by
  cases t with
  | zero => simpa [backlog] using h
  | succ t => exact le_max_left _ _

/-- Drift at most zero: the backlog never exceeds its initial value. -/
theorem backlog_le_initial {lam g mu q0 : ℚ} (hq : 0 ≤ q0) (hd : drift lam g mu ≤ 0) (t : ℕ) :
    backlog lam g mu q0 t ≤ q0 := by
  induction t with
  | zero => simp [backlog]
  | succ t ih =>
    unfold drift at hd
    simp only [backlog]
    refine max_le hq ?_
    linarith

/-- Positive drift: the backlog grows exactly linearly, `q_t = q_0 + t * drift`. -/
theorem backlog_linear {lam g mu q0 : ℚ} (hq : 0 ≤ q0) (hd : 0 < drift lam g mu) (t : ℕ) :
    backlog lam g mu q0 t = q0 + t * drift lam g mu := by
  induction t with
  | zero => simp [backlog]
  | succ t ih =>
    have hd' : drift lam g mu = lam + g * mu - mu := rfl
    simp only [backlog]
    rw [ih, ← hd']
    have ht : (0 : ℚ) ≤ t := Nat.cast_nonneg t
    rw [max_eq_right (by nlinarith)]
    push_cast; ring

/-- A backlog is bounded (by a constant) for all rounds. -/
def BacklogBounded (lam g mu q0 : ℚ) : Prop := ∃ B : ℚ, ∀ t, backlog lam g mu q0 t ≤ B

/-- Net-rate dichotomy (Q1): for `0 <= g`, `0 <= mu`, `0 <= q0`, the backlog is bounded iff
`lam <= (1 - g) * mu`. -/
theorem backlog_bounded_iff {lam g mu q0 : ℚ} (hq : 0 ≤ q0) :
    BacklogBounded lam g mu q0 ↔ lam ≤ (1 - g) * mu := by
  constructor
  · rintro ⟨B, hB⟩
    by_contra hlt
    have hlt := not_le.1 hlt
    have hd : 0 < drift lam g mu := by unfold drift; linarith
    obtain ⟨n, hn⟩ := exists_nat_gt ((B - q0) / drift lam g mu)
    have h1 := hB n
    rw [backlog_linear hq hd] at h1
    have h2 : (B - q0) < n * drift lam g mu := by
      rwa [div_lt_iff₀ hd] at hn
    linarith
  · intro h
    exact ⟨q0, backlog_le_initial hq (by unfold drift; linarith)⟩

/-- Self-limiting repair (Q1): if each unit of repair generates at least one unit of new residual
(`1 <= g`) and the computation generates any residual (`0 < lam`), no repair rate `mu >= 0` keeps
the backlog bounded. -/
theorem no_bounded_backlog_if_unit_gain {lam g q0 : ℚ} (hq : 0 ≤ q0) (hlam : 0 < lam) (hg : 1 ≤ g)
    (mu : ℚ) (hmu : 0 ≤ mu) : ¬ BacklogBounded lam g mu q0 := by
  rw [backlog_bounded_iff hq]
  nlinarith

/-- Efficient repair (`g < 1`): the least sufficient repair rate is `lam / (1 - g)`. -/
theorem capacity_threshold {lam g mu q0 : ℚ} (hq : 0 ≤ q0) (hg : g < 1) :
    BacklogBounded lam g mu q0 ↔ lam / (1 - g) ≤ mu := by
  rw [backlog_bounded_iff hq, div_le_iff₀ (by linarith)]
  constructor <;> intro h <;> linarith

/-- Fresh-ancilla supply: repair capacity is `kappa` units per fresh ancilla and `r` fresh ancillas
arrive per round, `mu = kappa * r`.  The supply must reach `lam / ((1 - g) * kappa)`. -/
theorem fresh_supply_threshold {lam g kappa r q0 : ℚ} (hq : 0 ≤ q0) (hg : g < 1) (hk : 0 < kappa) :
    BacklogBounded lam g (kappa * r) q0 ↔ lam / ((1 - g) * kappa) ≤ r := by
  rw [backlog_bounded_iff hq, div_le_iff₀ (by nlinarith)]
  constructor <;> intro h <;> nlinarith

/-- No fresh supply (`r = 0`): any positive generation rate makes the backlog grow linearly. -/
theorem no_supply_linear_growth {lam g kappa q0 : ℚ} (hq : 0 ≤ q0) (hlam : 0 < lam) (t : ℕ) :
    backlog lam g (kappa * 0) q0 t = q0 + t * lam := by
  have hd : 0 < drift lam g (kappa * 0) := by unfold drift; simpa using hlam
  rw [backlog_linear hq hd]
  unfold drift
  simp

/-- A budget of `B` fresh marks in total, with each completed round consuming at least `rmin > 0`
of them, bounds the number of completed rounds by `B / rmin`.  (The common shape with a computation
that needs an unbounded stream of fresh marks.) -/
theorem rounds_le_budget {rmin B : ℚ} (hr : 0 < rmin) (use : ℕ → ℚ) (huse : ∀ t, rmin ≤ use t)
    (T : ℕ) (hB : ∑ t ∈ Finset.range T, use t ≤ B) : (T : ℚ) ≤ B / rmin := by
  rw [le_div_iff₀ hr]
  have : (T : ℚ) * rmin ≤ ∑ t ∈ Finset.range T, use t := by
    have h := Finset.sum_le_sum (s := Finset.range T) (f := fun _ => rmin) (g := use)
      (fun t _ => huse t)
    simpa using h
  linarith

/-- Conversely a fixed per-round consumption `u > 0` makes the total supply needed for `T` rounds
`T * u`, which exceeds every finite budget for large `T`. -/
theorem budget_exhausted {u B : ℚ} (hu : 0 < u) : ∃ T : ℕ, B < T * u := by
  obtain ⟨T, hT⟩ := exists_nat_gt (B / u)
  exact ⟨T, by rwa [div_lt_iff₀ hu] at hT⟩

end QcSelfObstruction
