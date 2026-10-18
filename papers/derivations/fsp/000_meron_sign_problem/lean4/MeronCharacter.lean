/-!
Finite Boolean flip-orbit cancellation for one orbit with unit weight.
`orbitSigns flags` lists the signs of all 2^k orientation assignments when
each cluster contributes an independent factor: a cluster flagged `true`
reverses the sign when flipped, a cluster flagged `false` does not. This
independence is assumed by the definition; it is not derived from a model.
-/
namespace MeronCharacter

def orbitSigns : List Bool → List Int
  | [] => [1]
  | meron :: rest =>
    orbitSigns rest ++ (orbitSigns rest).map (fun s => if meron then -s else s)

theorem sum_neg (xs : List Int) : (xs.map (fun x => -x)).sum = -xs.sum := by
  induction xs with
  | nil => simp
  | cons x xs ih => simp [ih, Int.neg_add]

theorem meron_orbit_cancels (flags : List Bool) (h : true ∈ flags) :
    (orbitSigns flags).sum = 0 := by
  induction flags with
  | nil => simp at h
  | cons flag rest ih =>
    cases flag with
    | false =>
      have hr : true ∈ rest := by simpa using h
      simp [orbitSigns, List.sum_append, ih hr]
    | true =>
      simp only [orbitSigns, List.sum_append, ↓reduceIte, sum_neg]
      omega

theorem zero_meron_orbit_positive (flags : List Bool) (h : true ∉ flags) :
    (orbitSigns flags).sum = (2 : Int) ^ flags.length := by
  induction flags with
  | nil => simp [orbitSigns]
  | cons flag rest ih =>
    cases flag with
    | false =>
      have hr : true ∉ rest := by simpa using h
      simp [orbitSigns, List.sum_append, ih hr, Int.pow_succ]
      omega
    | true => simp at h

def compressedSum (flags : List Bool) : Int :=
  if true ∈ flags then 0 else (2 : Int) ^ flags.length

theorem compression_preserves_partition (flags : List Bool) :
    (orbitSigns flags).sum = compressedSum flags := by
  unfold compressedSum
  split
  next h => exact meron_orbit_cancels flags h
  next h => exact zero_meron_orbit_positive flags h

/-- Equal total signed mass does not require equal-magnitude pairing. -/
theorem unequal_three_term_cancellation : ([2, -1, -1] : List Int).sum = 0 := by
  decide

/-- A cancelling denominator doublet can carry a nonzero observable numerator. -/
theorem observable_doublet_counterexample :
    (1 : Int) + (-1) = 0 ∧ (1 : Int) * 1 + (-1) * (-1) = 2 := by
  decide

#print axioms meron_orbit_cancels
#print axioms zero_meron_orbit_positive
#print axioms compression_preserves_partition
#print axioms unequal_three_term_cancellation
#print axioms observable_doublet_counterexample

end MeronCharacter
