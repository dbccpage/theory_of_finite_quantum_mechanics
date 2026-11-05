/-!
# Component completion: rational square-root bisection

Lean-core statements for the finite parts of the derivation proposal DP-5
(`coda_wdp_derivations_20261006`). Only `Init` is imported; arithmetic is Lean
core `Rat` and `Nat`.

* The bracket invariant `0 ≤ l ≤ u`, `l² ≤ a ≤ u²` holds at the start
  `(0, max 1 a)` and is preserved by one bisection step.
* Each step keeps the new bracket inside the old one and halves its width;
  after `n` steps the width times `2ⁿ` is the initial width.
* Every nonnegative rational square root of `a` lies in every bracket, and the
  midpoint is within half the width of every point of the bracket.
* The `a = 2` table `(0,2), (1,2), (1,3/2), (5/4,3/2), (11/8,3/2),
  (11/8,23/16), (45/32,23/16)` and its midpoint `91/64` are replayed.
* Control: without `0 ≤ l` the invariant does not locate the root
  (`a = 1`, `l = u = -1`).
* No rational squares to `2` (Nat descent `n² = 2d² → n = d = 0`), so the
  nested rational brackets for `a = 2` contain no common rational root.

Scope: the statement that the nested brackets have empty rational
intersection needs an Archimedean step (width tending to zero) that is not
formalized here; only the absence of a rational root is. AuthorityEffect: None.
-/
namespace WitnessedDifference.ComponentCompletion

/-- Absolute value on `Rat`. -/
def qabs (x : Rat) : Rat := if x < 0 then -x else x

/-- A bracket `[l, u]`. -/
structure Bracket where
  l : Rat
  u : Rat

/-- The midpoint of a bracket. -/
def Bracket.mid (b : Bracket) : Rat := (b.l + b.u) / 2

/-- The width of a bracket. -/
def Bracket.width (b : Bracket) : Rat := b.u - b.l

/-- One bisection step for `√a`. -/
def step (a : Rat) (b : Bracket) : Bracket :=
  if b.mid * b.mid ≤ a then ⟨b.mid, b.u⟩ else ⟨b.l, b.mid⟩

/-- `n` bisection steps. -/
def iter (a : Rat) : Nat → Bracket → Bracket
  | 0, b => b
  | n + 1, b => step a (iter a n b)

/-- The bracket invariant. -/
def Inv (a : Rat) (b : Bracket) : Prop :=
  0 ≤ b.l ∧ b.l ≤ b.u ∧ b.l * b.l ≤ a ∧ a ≤ b.u * b.u

/-- The start bracket `(0, max 1 a)`. -/
def start (a : Rat) : Bracket := ⟨0, if a ≤ 1 then 1 else a⟩

/-- DP-5: the invariant holds at the start for `a ≥ 0`. -/
theorem inv_start (a : Rat) (ha : 0 ≤ a) : Inv a (start a) := by
  unfold Inv start
  simp only
  split
  · grind
  · have hm : 0 ≤ a * (a - 1) := Rat.mul_nonneg ha (by grind)
    grind

/-- DP-5: one step preserves the invariant. -/
theorem inv_step (a : Rat) (b : Bracket) (h : Inv a b) : Inv a (step a b) := by
  obtain ⟨h0, h1, h2, h3⟩ := h
  unfold step
  split
  · rename_i hm
    refine ⟨?_, ?_, hm, h3⟩ <;> unfold Bracket.mid <;> grind
  · rename_i hm
    refine ⟨h0, ?_, h2, ?_⟩
    · unfold Bracket.mid; grind
    · grind

/-- DP-5: the invariant holds after any number of steps. -/
theorem inv_iter (a : Rat) (b : Bracket) (h : Inv a b) (n : Nat) :
    Inv a (iter a n b) := by
  induction n with
  | zero => exact h
  | succ n ih => exact inv_step a _ ih

/-- DP-5: one step halves the width. -/
theorem width_step (a : Rat) (b : Bracket) :
    (step a b).width = b.width / 2 := by
  unfold step
  split <;> (unfold Bracket.width Bracket.mid; grind)

/-- DP-5: the new bracket lies inside the old one. -/
theorem step_nested (a : Rat) (b : Bracket) (h : b.l ≤ b.u) :
    b.l ≤ (step a b).l ∧ (step a b).u ≤ b.u := by
  unfold step
  split <;> (unfold Bracket.mid; constructor <;> grind)

/-- DP-5: after `n` steps, width times `2ⁿ` is the initial width. -/
theorem width_iter (a : Rat) (b : Bracket) (n : Nat) :
    (iter a n b).width * 2 ^ n = b.width := by
  induction n with
  | zero => show b.width * 2 ^ 0 = b.width; rw [Rat.pow_zero]; grind
  | succ n ih =>
    show (step a (iter a n b)).width * 2 ^ (n + 1) = b.width
    rw [width_step, Rat.pow_succ, ← ih]
    grind

/-- DP-5: a nonnegative root of `a` lies in every bracket satisfying the
invariant. -/
theorem root_in_bracket (a r : Rat) (b : Bracket) (h : Inv a b)
    (hr : 0 ≤ r) (hra : r * r = a) : b.l ≤ r ∧ r ≤ b.u := by
  obtain ⟨h0, h1, h2, h3⟩ := h
  constructor
  · apply Classical.byContradiction
    intro hlt
    have hlt' : r < b.l := by grind
    have := Rat.mul_pos (show 0 < b.l - r by grind) (show 0 < b.l + r by grind)
    grind
  · apply Classical.byContradiction
    intro hlt
    have hlt' : b.u < r := by grind
    have := Rat.mul_pos (show 0 < r - b.u by grind) (show 0 < r + b.u by grind)
    grind

/-- DP-5: the midpoint is within half the width of any point of the
bracket. -/
theorem mid_close (b : Bracket) (x : Rat) (hl : b.l ≤ x) (hu : x ≤ b.u) :
    qabs (x - b.mid) ≤ b.width / 2 := by
  unfold qabs Bracket.mid Bracket.width
  split <;> grind

/-- DP-5 control: dropping `0 ≤ l`, the bracket `[-1,-1]` satisfies
`l² ≤ 1 ≤ u²` but does not contain the root `1`. -/
theorem negative_endpoint_control :
    (-1 : Rat) * -1 ≤ 1 ∧ (1 : Rat) ≤ -1 * -1 ∧ ¬ ((1 : Rat) ≤ -1) := by
  refine ⟨?_, ?_, ?_⟩ <;> grind

/-- The step outcome when the midpoint square is at most `a`. -/
theorem step_of_le (a : Rat) (b : Bracket) (h : b.mid * b.mid ≤ a) :
    step a b = ⟨b.mid, b.u⟩ := by
  unfold step; rw [if_pos h]

/-- The step outcome when the midpoint square exceeds `a`. -/
theorem step_of_gt (a : Rat) (b : Bracket) (h : ¬ b.mid * b.mid ≤ a) :
    step a b = ⟨b.l, b.mid⟩ := by
  unfold step; rw [if_neg h]

/-- Bracket equality from endpoint equalities. -/
theorem bracket_eq {b : Bracket} {l u : Rat} (hl : b.l = l) (hu : b.u = u) :
    b = ⟨l, u⟩ := by
  cases b; simp only at hl hu; rw [hl, hu]

/-- DP-5: the `a = 2` table, row by row. -/
theorem table_row1 : step 2 ⟨0, 2⟩ = ⟨1, 2⟩ := by
  rw [step_of_le _ _ (by unfold Bracket.mid; grind)]
  exact bracket_eq (by unfold Bracket.mid; grind) rfl

theorem table_row2 : step 2 ⟨1, 2⟩ = ⟨1, 3 / 2⟩ := by
  rw [step_of_gt _ _ (by unfold Bracket.mid; grind)]
  exact bracket_eq rfl (by unfold Bracket.mid; grind)

theorem table_row3 : step 2 ⟨1, 3 / 2⟩ = ⟨5 / 4, 3 / 2⟩ := by
  rw [step_of_le _ _ (by unfold Bracket.mid; grind)]
  exact bracket_eq (by unfold Bracket.mid; grind) rfl

theorem table_row4 : step 2 ⟨5 / 4, 3 / 2⟩ = ⟨11 / 8, 3 / 2⟩ := by
  rw [step_of_le _ _ (by unfold Bracket.mid; grind)]
  exact bracket_eq (by unfold Bracket.mid; grind) rfl

theorem table_row5 : step 2 ⟨11 / 8, 3 / 2⟩ = ⟨11 / 8, 23 / 16⟩ := by
  rw [step_of_gt _ _ (by unfold Bracket.mid; grind)]
  exact bracket_eq rfl (by unfold Bracket.mid; grind)

theorem table_row6 : step 2 ⟨11 / 8, 23 / 16⟩ = ⟨45 / 32, 23 / 16⟩ := by
  rw [step_of_le _ _ (by unfold Bracket.mid; grind)]
  exact bracket_eq (by unfold Bracket.mid; grind) rfl

/-- DP-5: the six-step iterate from the start `(0,2)` and its midpoint. -/
theorem table_iter6 : iter 2 6 ⟨0, 2⟩ = ⟨45 / 32, 23 / 16⟩ ∧
    (Bracket.mk (45 / 32) (23 / 16)).mid = 91 / 64 := by
  refine ⟨?_, ?_⟩
  · show step 2 (step 2 (step 2 (step 2 (step 2 (step 2 ⟨0, 2⟩))))) = _
    rw [table_row1, table_row2, table_row3, table_row4, table_row5, table_row6]
  · unfold Bracket.mid; grind

/-- The start bracket for `a = 2` is `(0,2)`. -/
theorem start_two : start 2 = ⟨0, 2⟩ := by
  unfold start
  rw [if_neg (by grind)]

theorem sq_mod_two (n : Nat) : n * n % 2 = n % 2 := by
  rw [Nat.mul_mod]
  have : n % 2 < 2 := Nat.mod_lt _ (by decide)
  match n % 2, this with
  | 0, _ => rfl
  | 1, _ => rfl

/-- DP-5: Nat descent, `n² = 2d²` forces `n = d = 0`. -/
theorem nat_sq_two_descent : ∀ n d : Nat, n * n = 2 * (d * d) → n = 0 ∧ d = 0 := by
  intro n
  induction n using Nat.strongRecOn with
  | _ n ih =>
    intro d h
    by_cases hn : n = 0
    · subst hn
      have hd : d * d = 0 := by omega
      exact ⟨rfl, by rcases Nat.mul_eq_zero.mp hd with h | h <;> exact h⟩
    · have he : n % 2 = 0 := by
        have := sq_mod_two n
        omega
      obtain ⟨k, rfl⟩ : ∃ k, n = 2 * k := ⟨n / 2, by omega⟩
      have h2 : d * d = 2 * (k * k) := by
        have : 2 * (d * d) = 2 * (2 * (k * k)) := by rw [← h]; grind
        omega
      have hd : d % 2 = 0 := by
        have := sq_mod_two d
        omega
      obtain ⟨j, rfl⟩ : ∃ j, d = 2 * j := ⟨d / 2, by omega⟩
      have h3 : k * k = 2 * (j * j) := by
        have : 2 * (k * k) = 2 * (2 * (j * j)) := by rw [← h2]; grind
        omega
      have hlt : k < 2 * k := by omega
      obtain ⟨hk, hj⟩ := ih k hlt j h3
      exact ⟨by omega, by omega⟩

/-- DP-5: no rational squares to `2`. -/
theorem no_rational_sqrt_two (q : Rat) : q * q ≠ 2 := by
  intro h
  have h2 : q ^ 2 = 2 := by
    rw [Rat.pow_succ, Rat.pow_succ, Rat.pow_zero, Rat.one_mul]; exact h
  have hn : q.num ^ 2 = 2 := by
    have := congrArg Rat.num h2
    rw [Rat.num_pow] at this
    exact this
  have hnat : q.num.natAbs * q.num.natAbs = 2 * (1 * 1) := by
    have := congrArg Int.natAbs hn
    rw [Int.natAbs_pow] at this
    rw [Nat.pow_two] at this
    exact this
  have := (nat_sq_two_descent _ _ hnat).2
  exact absurd this (by decide)

end WitnessedDifference.ComponentCompletion
