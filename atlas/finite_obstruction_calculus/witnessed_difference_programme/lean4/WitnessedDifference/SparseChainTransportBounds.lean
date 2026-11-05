import Init

/-!
# Conditional size bounds for sparse chain transport

The theorems here concern explicit finite arithmetic. A bounded-branching or
coefficient-mass recurrence is a hypothesis, not a theorem about a particular
schedule-complex implementation. No full schedule complex is enumerated by
these definitions. The all-capacity carrier construction, its rank decrease,
and the correspondence between its implementation and these recurrences are
separate proof obligations.

`geometricSum D r` is the sum of `D^j` for `0 ≤ j < r`. The zero-start and
nonzero-start recurrence bounds keep the root contribution distinct. All
arithmetic is over unbounded natural numbers, with no overflow assumption.
-/

namespace WitnessedDifference.SparseChainTransportBounds

/-- Number of nodes through `r` levels in the complete `D`-ary expansion. -/
def geometricSum (D : Nat) : Nat → Nat
  | 0 => 0
  | r + 1 => 1 + D * geometricSum D r

@[simp] theorem geometricSum_zero (D : Nat) : geometricSum D 0 = 0 := rfl

@[simp] theorem geometricSum_succ (D r : Nat) :
    geometricSum D (r + 1) = 1 + D * geometricSum D r := rfl

/-- A forward sum of powers, used to identify the recursive majorant. -/
def powerSum (D : Nat) : Nat → Nat
  | 0 => 0
  | r + 1 => powerSum D r + D ^ r

theorem geometricSum_balance (D r : Nat) :
    D * geometricSum D r + 1 = geometricSum D r + D ^ r := by
  induction r with
  | zero => simp [geometricSum]
  | succ r ih =>
    have multiplied := congrArg (fun x => D * x) ih
    simp only [Nat.mul_add, Nat.mul_one] at multiplied
    simp only [geometricSum_succ, Nat.pow_succ, Nat.mul_add, Nat.mul_one]
    rw [Nat.mul_comm (D ^ r) D]
    omega

theorem geometricSum_eq_powerSum (D r : Nat) : geometricSum D r = powerSum D r := by
  induction r with
  | zero => rfl
  | succ r ih =>
    change 1 + D * geometricSum D r = powerSum D r + D ^ r
    rw [← ih, Nat.add_comm 1]
    exact geometricSum_balance D r

theorem geometricSum_add_term (D r : Nat) :
    geometricSum D (r + 1) = geometricSum D r + D ^ r := by
  rw [geometricSum_succ, Nat.add_comm 1]
  exact geometricSum_balance D r

theorem geometricSum_step_le (D r : Nat) :
    geometricSum D r ≤ geometricSum D (r + 1) := by
  rw [geometricSum_add_term]
  exact Nat.le_add_right _ _

theorem geometricSum_mono_depth (D : Nat) {r s : Nat} (h : r ≤ s) :
    geometricSum D r ≤ geometricSum D s := by
  induction h with
  | refl => exact Nat.le_refl _
  | @step s _ ih => exact Nat.le_trans ih (geometricSum_step_le D s)

theorem geometricSum_mono_branch {D E : Nat} (h : D ≤ E) (r : Nat) :
    geometricSum D r ≤ geometricSum E r := by
  induction r with
  | zero => exact Nat.le_refl 0
  | succ r ih =>
    exact Nat.add_le_add_left (Nat.mul_le_mul h ih) 1

@[simp] theorem geometricSum_one (r : Nat) : geometricSum 1 r = r := by
  induction r with
  | zero => rfl
  | succ r ih => simp only [geometricSum_succ, Nat.one_mul, ih]; omega

@[simp] theorem geometricSum_zero_branch (r : Nat) : geometricSum 0 (r + 1) = 1 := by
  simp only [geometricSum_succ, Nat.zero_mul, Nat.add_zero]

theorem geometricSum_positive (D r : Nat) : 1 ≤ geometricSum D (r + 1) := by
  rw [geometricSum_succ]
  exact Nat.le_add_right _ _

theorem positive_base_power (D r : Nat) : 1 ≤ (D + 1) ^ r := by
  induction r with
  | zero => exact Nat.le_refl 1
  | succ r ih =>
    rw [Nat.pow_succ]
    have h := Nat.mul_le_mul ih (Nat.le_add_left 1 D)
    simpa only [Nat.one_mul] using h

/-- A uniform bound also covering zero and unit branching. -/
theorem geometricSum_le_successor_power (D r : Nat) :
    geometricSum D r ≤ (D + 1) ^ r := by
  induction r with
  | zero => exact Nat.zero_le _
  | succ r ih =>
    calc
      geometricSum D (r + 1) = 1 + D * geometricSum D r := rfl
      _ ≤ (D + 1) ^ r + D * ((D + 1) ^ r) :=
        Nat.add_le_add (positive_base_power D r) (Nat.mul_le_mul_left D ih)
      _ = (D + 1) ^ (r + 1) := by
        rw [Nat.pow_succ, Nat.mul_comm ((D + 1) ^ r) (D + 1), Nat.add_mul, Nat.one_mul]
        exact Nat.add_comm _ _

/-- Sharper exponential bound when there are at least two possible branches. -/
theorem geometricSum_add_one_le_power {D : Nat} (hD : 2 ≤ D) (r : Nat) :
    geometricSum D r + 1 ≤ D ^ r := by
  induction r with
  | zero => exact Nat.le_refl 1
  | succ r ih =>
    have multiplied := Nat.mul_le_mul_left D ih
    simp only [Nat.mul_add, Nat.mul_one] at multiplied
    rw [Nat.pow_succ, Nat.mul_comm (D ^ r) D]
    change 1 + D * geometricSum D r + 1 ≤ D * D ^ r
    omega

/-- An expansion with zero initial mass and additive cost at most `A` per
node is bounded by `A` times the geometric sum. -/
theorem zero_start_recurrence_bound (D A : Nat) (t : Nat → Nat)
    (initial : t 0 = 0)
    (step : ∀ r, t (r + 1) ≤ A + D * t r) :
    ∀ r, t r ≤ A * geometricSum D r := by
  intro r
  induction r with
  | zero => simp only [initial, geometricSum_zero, Nat.mul_zero, Nat.le_refl]
  | succ r ih =>
    calc
      t (r + 1) ≤ A + D * t r := step r
      _ ≤ A + D * (A * geometricSum D r) :=
        Nat.add_le_add_left (Nat.mul_le_mul_left D ih) A
      _ = A * geometricSum D (r + 1) := by
        simp only [geometricSum_succ, Nat.mul_add, Nat.mul_one]
        rw [← Nat.mul_assoc D A, Nat.mul_comm D A, Nat.mul_assoc A D]

/-- The root contribution accounts for the extra level in the majorant. -/
theorem root_recurrence_bound (D A : Nat) (t : Nat → Nat)
    (initial : t 0 ≤ A)
    (step : ∀ r, t (r + 1) ≤ A + D * t r) :
    ∀ r, t r ≤ A * geometricSum D (r + 1) := by
  intro r
  induction r with
  | zero => simpa only [geometricSum_succ, geometricSum_zero, Nat.mul_zero,
      Nat.add_zero, Nat.mul_one] using initial
  | succ r ih =>
    calc
      t (r + 1) ≤ A + D * t r := step r
      _ ≤ A + D * (A * geometricSum D (r + 1)) :=
        Nat.add_le_add_left (Nat.mul_le_mul_left D ih) A
      _ = A * geometricSum D (r + 1 + 1) := by
        simp only [geometricSum_succ, Nat.mul_add, Nat.mul_one]
        rw [← Nat.mul_assoc D A, Nat.mul_comm D A, Nat.mul_assoc A D]

theorem unit_root_recurrence_bound (D : Nat) (t : Nat → Nat)
    (initial : t 0 ≤ 1)
    (step : ∀ r, t (r + 1) ≤ 1 + D * t r) :
    ∀ r, t r ≤ geometricSum D (r + 1) := by
  intro r
  simpa only [Nat.one_mul] using root_recurrence_bound D 1 t initial step r

theorem recurrence_bound_at_rank (D A R : Nat) (t : Nat → Nat)
    (initial : t 0 ≤ A) (step : ∀ r, t (r + 1) ≤ A + D * t r)
    {r : Nat} (rank_bound : r ≤ R) : t r ≤ A * geometricSum D (R + 1) := by
  exact Nat.le_trans (root_recurrence_bound D A t initial step r)
    (Nat.mul_le_mul_left A (geometricSum_mono_depth D (Nat.add_le_add_right rank_bound 1)))

theorem recurrence_exponential_bound (D A : Nat) (t : Nat → Nat)
    (initial : t 0 ≤ A) (step : ∀ r, t (r + 1) ≤ A + D * t r) (r : Nat) :
    t r ≤ A * (D + 1) ^ (r + 1) := by
  exact Nat.le_trans (root_recurrence_bound D A t initial step r)
    (Nat.mul_le_mul_left A (geometricSum_le_successor_power D (r + 1)))

/-- Per-level growth and cumulative work are separate quantities. -/
theorem level_branching_bound (D A : Nat) (width : Nat → Nat)
    (initial : width 0 ≤ A)
    (step : ∀ r, width (r + 1) ≤ D * width r) :
    ∀ r, width r ≤ A * D ^ r := by
  intro r
  induction r with
  | zero => simpa only [Nat.pow_zero, Nat.mul_one] using initial
  | succ r ih =>
    calc
      width (r + 1) ≤ D * width r := step r
      _ ≤ D * (A * D ^ r) := Nat.mul_le_mul_left D ih
      _ = A * D ^ (r + 1) := by
        rw [Nat.pow_succ, ← Nat.mul_assoc D A, Nat.mul_comm D A]
        simp only [Nat.mul_assoc, Nat.mul_comm D (D ^ r)]

def cumulative (width : Nat → Nat) : Nat → Nat
  | 0 => 0
  | r + 1 => cumulative width r + width r

theorem cumulative_branching_bound (D A : Nat) (width : Nat → Nat)
    (initial : width 0 ≤ A)
    (step : ∀ r, width (r + 1) ≤ D * width r) :
    ∀ r, cumulative width r ≤ A * geometricSum D r := by
  intro r
  induction r with
  | zero => simp only [cumulative, geometricSum_zero, Nat.mul_zero, Nat.le_refl]
  | succ r ih =>
    calc
      cumulative width (r + 1) = cumulative width r + width r := rfl
      _ ≤ A * geometricSum D r + A * D ^ r :=
        Nat.add_le_add ih (level_branching_bound D A width initial step r)
      _ = A * geometricSum D (r + 1) := by
        rw [geometricSum_add_term, Nat.mul_add]

/-- Ranks recorded along one recursive branch decrease at every edge. -/
def DescendingRanks : List Nat → Prop
  | [] => True
  | [_] => True
  | r :: s :: rest => s < r ∧ DescendingRanks (s :: rest)

theorem descending_path_length {r : Nat} {rest : List Nat}
    (descending : DescendingRanks (r :: rest)) : (r :: rest).length ≤ r + 1 := by
  induction rest generalizing r with
  | nil => simp only [List.length_cons, List.length_nil]; omega
  | cons s rest ih =>
    obtain ⟨less, tail_descending⟩ := descending
    have tail_bound := ih tail_descending
    simp only [List.length_cons] at tail_bound ⊢
    omega

theorem descending_path_length_at_rank {r R : Nat} {rest : List Nat}
    (descending : DescendingRanks (r :: rest)) (bound : r ≤ R) :
    (r :: rest).length ≤ R + 1 :=
  Nat.le_trans (descending_path_length descending) (Nat.add_le_add_right bound 1)

theorem descending_path_edges_at_rank {r R : Nat} {rest : List Nat}
    (descending : DescendingRanks (r :: rest)) (bound : r ≤ R) : rest.length ≤ R := by
  have h := descending_path_length_at_rank descending bound
  simp only [List.length_cons] at h
  omega

/-- A finite list of independently checked column costs has the stated total
bound; the number of requested columns is explicit. -/
theorem column_cost_sum_bound (costs : List Nat) (perColumn : Nat)
    (bounded : ∀ a, a ∈ costs → a ≤ perColumn) :
    costs.sum ≤ costs.length * perColumn := by
  induction costs with
  | nil => simp only [List.sum_nil, List.length_nil, Nat.zero_mul, Nat.le_refl]
  | cons a tail ih =>
    have ha := bounded a List.mem_cons_self
    have ht := ih (fun b hb => bounded b (List.mem_cons_of_mem a hb))
    simp only [List.sum_cons, List.length_cons, Nat.add_mul, Nat.one_mul]
    have h := Nat.add_le_add ha ht
    omega

/-- Total absolute coefficient mass, before or after collecting equal labels. -/
def coefficientMass : List Int → Nat
  | [] => 0
  | a :: rest => a.natAbs + coefficientMass rest

def nonzeroCount : List Int → Nat
  | [] => 0
  | a :: rest => (if a = 0 then 0 else 1) + nonzeroCount rest

theorem coefficient_le_mass (coefficients : List Int) {a : Int}
    (present : a ∈ coefficients) : a.natAbs ≤ coefficientMass coefficients := by
  induction coefficients with
  | nil => cases present
  | cons b rest ih =>
    have cases_mem := List.mem_cons.mp present
    cases cases_mem with
    | inl same =>
      subst a
      exact Nat.le_add_right _ _
    | inr in_rest =>
      exact Nat.le_trans (ih in_rest) (Nat.le_add_left _ _)

/-- Nonzero integer coefficients each contribute at least one unit of mass.
Zero entries need not have been removed for this inequality. -/
theorem support_le_mass (coefficients : List Int) :
    nonzeroCount coefficients ≤ coefficientMass coefficients := by
  induction coefficients with
  | nil => exact Nat.le_refl 0
  | cons a rest ih =>
    by_cases ha : a = 0
    · simp only [nonzeroCount, coefficientMass, ha, if_pos, Int.natAbs_zero, Nat.zero_add]
      exact ih
    · have positive : 1 ≤ a.natAbs := by
        have nonzero : a.natAbs ≠ 0 := fun h => ha (Int.natAbs_eq_zero.mp h)
        omega
      simpa only [nonzeroCount, coefficientMass, if_neg ha] using Nat.add_le_add positive ih

/-- A proven mass bound simultaneously bounds the number of stored nonzero
terms and every integer coefficient magnitude. -/
theorem mass_bound_controls_support_and_coefficients (coefficients : List Int)
    {bound : Nat} (mass_bound : coefficientMass coefficients ≤ bound) :
    nonzeroCount coefficients ≤ bound ∧
      ∀ a, a ∈ coefficients → a.natAbs ≤ bound := by
  exact ⟨Nat.le_trans (support_le_mass coefficients) mass_bound,
    fun a ha => Nat.le_trans (coefficient_le_mass coefficients ha) mass_bound⟩

/-- Explicit power-of-two envelope; it supplies a magnitude-bit bound once
the encoding convention is fixed outside this arithmetic module. -/
theorem binary_envelope {A D a b : Nat} (hA : A ≤ 2 ^ a) (hD : D ≤ 2 ^ b)
    (r : Nat) : A * D ^ r ≤ 2 ^ (a + b * r) := by
  calc
    A * D ^ r ≤ 2 ^ a * (2 ^ b) ^ r := Nat.mul_le_mul hA (Nat.pow_le_pow_left hD r)
    _ = 2 ^ (a + b * r) := by rw [← Nat.pow_mul, ← Nat.pow_add]

theorem binary_envelope_strict {A D a b : Nat} (hA : A ≤ 2 ^ a) (hD : D ≤ 2 ^ b)
    (r : Nat) : A * D ^ r < 2 ^ (a + b * r + 1) := by
  have envelope := binary_envelope hA hD r
  have positive : 1 ≤ 2 ^ (a + b * r) := positive_base_power 1 _
  rw [Nat.pow_succ]
  omega

theorem coefficient_binary_bound (coefficients : List Int) {A D a b r : Nat}
    (mass_bound : coefficientMass coefficients ≤ A * D ^ r)
    (hA : A ≤ 2 ^ a) (hD : D ≤ 2 ^ b) {z : Int} (present : z ∈ coefficients) :
    z.natAbs < 2 ^ (a + b * r + 1) := by
  exact Nat.lt_of_le_of_lt (Nat.le_trans (coefficient_le_mass coefficients present) mass_bound)
    (binary_envelope_strict hA hD r)

/-- Safe facet-count majorant for a degree-`q` ordered-partition cell.
The geometric meaning of this expression is proved in the written derivation. -/
def facetMajorant (q : Nat) : Nat := q * 2 ^ (q + 1)

def branchingMajorant (q : Nat) : Nat := 1 + facetMajorant (q + 1) + facetMajorant q

def rankMajorant (m : Nat) : Nat := m * (m - 1) / 2

@[simp] theorem facetMajorant_zero : facetMajorant 0 = 0 := rfl

@[simp] theorem branchingMajorant_zero : branchingMajorant 0 = 5 := rfl

@[simp] theorem rankMajorant_zero : rankMajorant 0 = 0 := rfl

@[simp] theorem rankMajorant_one : rankMajorant 1 = 0 := rfl

theorem branchingMajorant_at_least_two (q : Nat) : 2 ≤ branchingMajorant q := by
  have positive : 1 ≤ 2 ^ (q + 1 + 1) := positive_base_power 1 _
  have term := Nat.mul_le_mul (Nat.le_add_left 1 q) positive
  simp only [Nat.one_mul] at term
  unfold branchingMajorant facetMajorant
  omega

/-- Specialization to the stated sparse-transport majorants; the local
recurrence and rank bound remain visible hypotheses. -/
theorem sparse_transport_bound (m q A : Nat) (t : Nat → Nat)
    (initial : t 0 ≤ A)
    (step : ∀ r, t (r + 1) ≤ A + branchingMajorant q * t r)
    {r : Nat} (rank_bound : r ≤ rankMajorant m) :
    t r ≤ A * geometricSum (branchingMajorant q) (rankMajorant m + 1) :=
  recurrence_bound_at_rank (branchingMajorant q) A (rankMajorant m) t
    initial step rank_bound

theorem sparse_transport_exponential_bound (m q A : Nat) (t : Nat → Nat)
    (initial : t 0 ≤ A)
    (step : ∀ r, t (r + 1) ≤ A + branchingMajorant q * t r)
    {r : Nat} (rank_bound : r ≤ rankMajorant m) :
    t r ≤ A * branchingMajorant q ^ (rankMajorant m + 1) := by
  have geometric := sparse_transport_bound m q A t initial step rank_bound
  have power := geometricSum_add_one_le_power (branchingMajorant_at_least_two q)
    (rankMajorant m + 1)
  have weaker : geometricSum (branchingMajorant q) (rankMajorant m + 1) ≤
      branchingMajorant q ^ (rankMajorant m + 1) := by omega
  exact Nat.le_trans geometric (Nat.mul_le_mul_left A weaker)

theorem degree_zero_transport_bound (m A : Nat) (t : Nat → Nat)
    (initial : t 0 ≤ A) (step : ∀ r, t (r + 1) ≤ A + 5 * t r)
    {r : Nat} (rank_bound : r ≤ rankMajorant m) :
    t r ≤ A * geometricSum 5 (rankMajorant m + 1) :=
  recurrence_bound_at_rank 5 A (rankMajorant m) t initial step rank_bound

/-! ## Conditional degree bounds from a signed sweep

The following sharper majorants assume the written sweep's column-mass
recurrences. They do not establish those recurrences for the cellular maps.
`B` is one common facet bound for the degrees under consideration, and `R` is
the sweep length bound. The geometric-series theorems above remain independent
of this additional hypothesis.
-/

def sweepGrowth (R B : Nat) : Nat := max 2 (R * B)

/-- A zero extension lets a finite range of recurrence checks use the generic
induction theorem without requiring bounds in unqueried higher degrees. -/
def truncateAfter (limit : Nat) (mass : Nat → Nat) (k : Nat) : Nat :=
  if k ≤ limit then mass k else 0

theorem finite_recurrence_extension (limit : Nat) (mass : Nat → Nat)
    (F : Nat → Nat → Nat)
    (step : ∀ k, k < limit → mass (k + 1) ≤ F k (mass k)) :
    ∀ k, truncateAfter limit mass (k + 1) ≤ F k (truncateAfter limit mass k) := by
  intro k
  by_cases inside : k + 1 ≤ limit
  · have previous : k ≤ limit := by omega
    have smaller : k < limit := by omega
    simpa only [truncateAfter, if_pos inside, if_pos previous] using step k smaller
  · simp only [truncateAfter, if_neg inside]
    exact Nat.zero_le _

theorem sweepGrowth_ge_two (R B : Nat) : 2 ≤ sweepGrowth R B := Nat.le_max_left _ _

theorem sweepGrowth_ge_product (R B : Nat) : R * B ≤ sweepGrowth R B :=
  Nat.le_max_right _ _

/-- A single map's column mass grows at most geometrically in degree. -/
theorem map_degree_bound {M C : Nat} (hMC : M ≤ C) (mass : Nat → Nat)
    (initial : mass 0 ≤ 1) (step : ∀ k, mass (k + 1) ≤ M * mass k) (k : Nat) :
    mass k ≤ C ^ k := by
  have bounded := level_branching_bound M 1 mass initial step k
  simp only [Nat.one_mul] at bounded
  exact Nat.le_trans bounded (Nat.pow_le_pow_left hMC k)

theorem map_degree_bound_up_to {M C : Nat} (hMC : M ≤ C) (mass : Nat → Nat) (q : Nat)
    (initial : mass 0 ≤ 1)
    (step : ∀ k, k < q → mass (k + 1) ≤ M * mass k) : mass q ≤ C ^ q := by
  have extended := finite_recurrence_extension q mass (fun _ x => M * x) step
  have initial' : truncateAfter q mass 0 ≤ 1 := by
    simpa only [truncateAfter, if_pos (Nat.zero_le q)] using initial
  have result := map_degree_bound hMC (truncateAfter q mass) initial' extended q
  simpa only [truncateAfter, if_pos (Nat.le_refl q)] using result

theorem sweep_map_degree_bound (R B : Nat) (mass : Nat → Nat)
    (initial : mass 0 ≤ 1) (step : ∀ k, mass (k + 1) ≤ R * B * mass k) (k : Nat) :
    mass k ≤ sweepGrowth R B ^ k :=
  map_degree_bound (sweepGrowth_ge_product R B) mass initial step k

/-- The product estimate needed for the `ip` term in the homotopy recurrence. -/
theorem composed_map_degree_bound {C p i k : Nat} (hp : p ≤ C ^ k) (hi : i ≤ C ^ k)
    {composed : Nat} (composition_bound : composed ≤ p * i) :
    composed ≤ C ^ (2 * k) := by
  have product_bound := Nat.mul_le_mul hp hi
  rw [← Nat.pow_add] at product_bound
  have exponents : k + k = 2 * k := by omega
  rw [exponents] at product_bound
  exact Nat.le_trans composition_bound product_bound

/-- Homotopy column-mass bound, conditional on the signed sweep recurrence.
The initial inequality includes the harmless zero-degree factor of two. -/
theorem sweep_homotopy_degree_bound {R B C : Nat} (hC : 2 ≤ C) (hRB : R * B ≤ C)
    (mass : Nat → Nat) (initial : mass 0 ≤ 2 * R)
    (step : ∀ k, mass (k + 1) ≤ R * (C ^ (2 * (k + 1)) + 1 + B * mass k)) :
    ∀ k, mass k ≤ 2 * R * (k + 1) * C ^ (2 * k) := by
  intro k
  induction k with
  | zero => simpa only [Nat.mul_zero, Nat.pow_zero, Nat.zero_add, Nat.mul_one] using initial
  | succ k ih =>
    have Cpos : 0 < C := by omega
    have power_positive : 1 ≤ C ^ (2 * (k + 1)) := by
      have h := Nat.pow_le_pow_right Cpos (show 0 ≤ 2 * (k + 1) from Nat.zero_le _)
      simpa only [Nat.pow_zero] using h
    have first : R * (C ^ (2 * (k + 1)) + 1) ≤ 2 * R * C ^ (2 * (k + 1)) := by
      have inner : C ^ (2 * (k + 1)) + 1 ≤ 2 * C ^ (2 * (k + 1)) := by omega
      have multiplied := Nat.mul_le_mul_left R inner
      simpa only [← Nat.mul_assoc, Nat.mul_comm R 2] using multiplied
    have power_step : C ^ (2 * k + 1) ≤ C ^ (2 * (k + 1)) :=
      Nat.pow_le_pow_right Cpos (by omega)
    have second : R * B * mass k ≤ 2 * R * (k + 1) * C ^ (2 * (k + 1)) := by
      calc
        R * B * mass k ≤ C * (2 * R * (k + 1) * C ^ (2 * k)) := Nat.mul_le_mul hRB ih
        _ = (2 * R * (k + 1)) * C ^ (2 * k + 1) := by
          rw [Nat.pow_succ]
          rw [Nat.mul_left_comm C (2 * R * (k + 1)) (C ^ (2 * k)),
            Nat.mul_comm C (C ^ (2 * k))]
        _ ≤ (2 * R * (k + 1)) * C ^ (2 * (k + 1)) :=
          Nat.mul_le_mul_left _ power_step
    calc
      mass (k + 1) ≤ R * (C ^ (2 * (k + 1)) + 1 + B * mass k) := step k
      _ = R * (C ^ (2 * (k + 1)) + 1) + R * B * mass k := by
        rw [Nat.mul_add, Nat.mul_assoc]
      _ ≤ 2 * R * C ^ (2 * (k + 1)) +
          2 * R * (k + 1) * C ^ (2 * (k + 1)) := Nat.add_le_add first second
      _ = 2 * R * (k + 1 + 1) * C ^ (2 * (k + 1)) := by
        rw [Nat.mul_add (2 * R) (k + 1) 1, Nat.mul_one, Nat.add_mul]
        exact Nat.add_comm _ _

theorem sweep_homotopy_degree_bound_with_growth (R B : Nat) (mass : Nat → Nat)
    (initial : mass 0 ≤ 2 * R)
    (step : ∀ k, mass (k + 1) ≤ R *
      (sweepGrowth R B ^ (2 * (k + 1)) + 1 + B * mass k)) (k : Nat) :
    mass k ≤ 2 * R * (k + 1) * sweepGrowth R B ^ (2 * k) :=
  sweep_homotopy_degree_bound (sweepGrowth_ge_two R B) (sweepGrowth_ge_product R B)
    mass initial step k

theorem sweep_homotopy_degree_bound_up_to {R B C : Nat} (hC : 2 ≤ C) (hRB : R * B ≤ C)
    (mass : Nat → Nat) (q : Nat) (initial : mass 0 ≤ 2 * R)
    (step : ∀ k, k < q → mass (k + 1) ≤ R * (C ^ (2 * (k + 1)) + 1 + B * mass k)) :
    mass q ≤ 2 * R * (q + 1) * C ^ (2 * q) := by
  have extended := finite_recurrence_extension q mass
    (fun k x => R * (C ^ (2 * (k + 1)) + 1 + B * x)) step
  have initial' : truncateAfter q mass 0 ≤ 2 * R := by
    simpa only [truncateAfter, if_pos (Nat.zero_le q)] using initial
  have result := sweep_homotopy_degree_bound hC hRB (truncateAfter q mass) initial' extended q
  simpa only [truncateAfter, if_pos (Nat.le_refl q)] using result

theorem rankMajorant_le_square (m : Nat) : rankMajorant m ≤ m * m := by
  unfold rankMajorant
  exact Nat.le_trans (Nat.div_le_self _ _)
    (Nat.mul_le_mul_left m (Nat.sub_le m 1))

/-- The displayed bound is polynomial in `m` when `B` and the degree are fixed;
no asymptotic cost model or implementation runtime is asserted here. -/
def fixedDegreeBase (m B : Nat) : Nat := 2 + m * m * B

theorem sweepGrowth_le_fixedDegreeBase (m B : Nat) :
    sweepGrowth (rankMajorant m) B ≤ fixedDegreeBase m B := by
  have product := Nat.mul_le_mul_right B (rankMajorant_le_square m)
  unfold sweepGrowth fixedDegreeBase
  apply Nat.max_le.mpr
  constructor
  · exact Nat.le_add_right _ _
  · exact Nat.le_trans product (Nat.le_add_left _ _)

theorem fixed_degree_map_bound (m B : Nat) (mass : Nat → Nat) (q : Nat)
    (initial : mass 0 ≤ 1)
    (step : ∀ k, k < q → mass (k + 1) ≤ rankMajorant m * B * mass k) :
    mass q ≤ fixedDegreeBase m B ^ q := by
  exact Nat.le_trans
    (map_degree_bound_up_to (sweepGrowth_ge_product (rankMajorant m) B) mass q initial step)
    (Nat.pow_le_pow_left (sweepGrowth_le_fixedDegreeBase m B) q)

theorem fixed_degree_homotopy_bound (m B : Nat) (mass : Nat → Nat) (q : Nat)
    (initial : mass 0 ≤ 2 * rankMajorant m)
    (step : ∀ k, k < q → mass (k + 1) ≤ rankMajorant m *
      (sweepGrowth (rankMajorant m) B ^ (2 * (k + 1)) + 1 + B * mass k)) :
    mass q ≤ 2 * (m * m) * (q + 1) * fixedDegreeBase m B ^ (2 * q) := by
  have original := sweep_homotopy_degree_bound_up_to
    (sweepGrowth_ge_two (rankMajorant m) B) (sweepGrowth_ge_product (rankMajorant m) B)
    mass q initial step
  have factor := Nat.mul_le_mul_right (q + 1)
    (Nat.mul_le_mul_left 2 (rankMajorant_le_square m))
  have power := Nat.pow_le_pow_left (sweepGrowth_le_fixedDegreeBase m B) (2 * q)
  exact Nat.le_trans original (Nat.mul_le_mul factor power)

end WitnessedDifference.SparseChainTransportBounds
