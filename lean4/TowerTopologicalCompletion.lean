

namespace HilbertWalk.TowerTopologicalCompletion


inductive LimitTopology where
  | AlgebraicDirectColimit
  | CStarNormCompletion
  | NormalizedTracialMoments
  | MomentConvergence
  | QuantumMetricRieffel
  deriving DecidableEq, Repr

theorem algebraic_colimit_ne_norm_completion :
    LimitTopology.AlgebraicDirectColimit ≠ LimitTopology.CStarNormCompletion := by
  intro h
  nomatch h

theorem tracial_moment_label_ne_norm_completion :
    LimitTopology.NormalizedTracialMoments ≠ LimitTopology.CStarNormCompletion := by
  intro h
  nomatch h

theorem moment_ne_quantum_metric :
    LimitTopology.MomentConvergence ≠ LimitTopology.QuantumMetricRieffel := by
  intro h
  nomatch h



theorem bound_numerator_le_dim (d : Nat) (h : d ≥ 2) : 2 ≤ d := h

theorem bound_cross_products_increase {d1 d2 : Nat} (h : d1 < d2) :
    2 * d1 < 2 * d2 := Nat.mul_lt_mul_of_pos_left h (by decide)

theorem fuzzy_sphere_dim_steps : (2 : Nat) < 4 ∧ (4 : Nat) < 8 := by decide

def fuzzyCommutatorNum (d : Nat) : Nat := 2 * (d - 1)
def fuzzyCommutatorDen (d : Nat) : Nat := d * d

theorem two_over_d_bounds_commutator (d : Nat) (_hd : 2 ≤ d) :
    fuzzyCommutatorNum d * d ≤ 2 * fuzzyCommutatorDen d := by
  unfold fuzzyCommutatorNum fuzzyCommutatorDen
  have hle : d - 1 ≤ d := Nat.sub_le d 1
  have hmul : (d - 1) * d ≤ d * d := Nat.mul_le_mul_right d hle
  have h2 : 2 * ((d - 1) * d) ≤ 2 * (d * d) := Nat.mul_le_mul_left 2 hmul
  simpa [Nat.mul_assoc] using h2

theorem casimir_below_one (d : Nat) (hd : 2 ≤ d) :
    d * d - 1 < d * d := by
  have hd0 : 0 < d := Nat.lt_of_lt_of_le (by decide) hd
  exact Nat.sub_lt (Nat.mul_pos hd0 hd0) (by decide)



inductive ConvergenceVerdict where
  | ConvergesToZero
  | DoesNotConvergeToZero
  | Undetermined
  deriving DecidableEq, Repr

def declared_rank1_moment_verdict : LimitTopology → ConvergenceVerdict
  | LimitTopology.NormalizedTracialMoments => ConvergenceVerdict.ConvergesToZero
  | LimitTopology.MomentConvergence => ConvergenceVerdict.ConvergesToZero
  | LimitTopology.CStarNormCompletion => ConvergenceVerdict.DoesNotConvergeToZero
  | LimitTopology.AlgebraicDirectColimit => ConvergenceVerdict.Undetermined
  | LimitTopology.QuantumMetricRieffel => ConvergenceVerdict.Undetermined

theorem declared_moment_and_norm_verdicts_differ :
    declared_rank1_moment_verdict LimitTopology.NormalizedTracialMoments ≠
    declared_rank1_moment_verdict LimitTopology.CStarNormCompletion := by
  intro h
  nomatch h



inductive CompletionFamily where
  | AlgebraicUncompletedQab
  | ArchimedeanComplex
  | NonArchimedeanPadic
  deriving DecidableEq, Repr

theorem declared_algebraic_and_archimedean_labels_differ :
    CompletionFamily.AlgebraicUncompletedQab ≠ CompletionFamily.ArchimedeanComplex := by
  intro h
  nomatch h

theorem declared_archimedean_and_padic_labels_differ :
    CompletionFamily.ArchimedeanComplex ≠ CompletionFamily.NonArchimedeanPadic := by
  intro h
  nomatch h

theorem declared_algebraic_and_padic_labels_differ :
    CompletionFamily.AlgebraicUncompletedQab ≠ CompletionFamily.NonArchimedeanPadic := by
  intro h
  nomatch h



#print axioms algebraic_colimit_ne_norm_completion
#print axioms tracial_moment_label_ne_norm_completion
#print axioms moment_ne_quantum_metric
#print axioms bound_numerator_le_dim
#print axioms bound_cross_products_increase
#print axioms fuzzy_sphere_dim_steps
#print axioms declared_moment_and_norm_verdicts_differ
#print axioms declared_algebraic_and_archimedean_labels_differ
#print axioms declared_archimedean_and_padic_labels_differ
#print axioms declared_algebraic_and_padic_labels_differ

end HilbertWalk.TowerTopologicalCompletion

private def l5aProvenance : String :=
  "Origin: lean4/TowerTopologicalCompletion.lean Claim: algebraic_colimit_ne_norm_completion AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
