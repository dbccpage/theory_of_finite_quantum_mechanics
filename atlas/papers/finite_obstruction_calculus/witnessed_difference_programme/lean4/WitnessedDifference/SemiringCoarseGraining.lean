/- CH17 finite path-power intertwining. AuthorityEffect: None.
   Conditional on a declared associative multiplication with identity.
   For block matrices, use square padded matrices if domains differ. Actual
   finite semiring matrix multiplication satisfies these laws by distributivity.
   This lemma does not assert pathwise preservation or physical adequacy. -/
namespace WitnessedDifference.SemiringCoarseGraining

variable {M : Type}

def power (mul : M → M → M) (one : M) (a : M) : Nat → M
  | 0 => one
  | n + 1 => mul a (power mul one a n)

theorem powers_intertwine
    (mul : M → M → M) (one : M)
    (assoc : ∀ a b c, mul (mul a b) c = mul a (mul b c))
    (leftUnit : ∀ a, mul one a = a)
    (rightUnit : ∀ a, mul a one = a)
    (a h b : M) (step : mul a h = mul h b) :
    ∀ n, mul (power mul one a n) h = mul h (power mul one b n) := by
  intro n
  induction n with
  | zero => simp only [power, leftUnit, rightUnit]
  | succ n ih =>
      simp only [power]
      rw [assoc, ih, ← assoc, step, assoc]

theorem length_one_necessary
    (mul : M → M → M) (one : M)
    (rightUnit : ∀ a, mul a one = a)
    (a h b : M)
    (allLengths : ∀ n, mul (power mul one a n) h = mul h (power mul one b n)) :
    mul a h = mul h b := by
  have atOne := allLengths 1
  simpa only [power, rightUnit] using atOne

theorem all_lengths_iff_length_one
    (mul : M → M → M) (one : M)
    (assoc : ∀ a b c, mul (mul a b) c = mul a (mul b c))
    (leftUnit : ∀ a, mul one a = a)
    (rightUnit : ∀ a, mul a one = a)
    (a h b : M) :
    (∀ n, mul (power mul one a n) h = mul h (power mul one b n)) ↔
      mul a h = mul h b := by
  constructor
  · exact length_one_necessary mul one rightUnit a h b
  · exact powers_intertwine mul one assoc leftUnit rightUnit a h b

#print axioms powers_intertwine
#print axioms length_one_necessary
#print axioms all_lengths_iff_length_one

end WitnessedDifference.SemiringCoarseGraining
