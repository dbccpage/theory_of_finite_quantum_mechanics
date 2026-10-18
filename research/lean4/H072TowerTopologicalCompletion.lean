/-
  H072TowerTopologicalCompletion.lean
  AuthorityEffect: None.
  Citation: sealed-derivation-v1 (3100c4e)

  Campaign C500 Block 05: Limit Semantics and Finite-State Convergence.
  Scope: natural-number arithmetic for a 2/d upper bound, plus comparisons of
  declared topology/verdict/completion labels. There are no spin matrices,
  analytic topologies, limits or completed fields in these theorem types.
  Python's normalized spin coordinates X_i=2J_i/d have exact commutator norm
  2(d-1)/d^2 and Casimir 1-1/d^2; 2/d is only an upper bound.
  Tracial moments on varying matrix algebras are not a weak-* state-space limit.
  No identification of the p-adic completion of Q^ab with C_p is asserted.
-/

namespace FableHilbertWalk20260819.H072

-- ===========================================================================
-- Section 1: Typed Limit and Topology Registry
-- ===========================================================================

inductive LimitTopology where
  | AlgebraicDirectColimit
  | CStarNormCompletion
  | NormalizedTracialMoments
  | MomentConvergence
  | QuantumMetricRieffel
  deriving DecidableEq, Repr

/-- The authored algebraic and norm-completion labels differ. -/
theorem algebraic_colimit_ne_norm_completion :
    LimitTopology.AlgebraicDirectColimit ≠ LimitTopology.CStarNormCompletion := by
  intro h
  nomatch h

/-- The authored moment-comparison and norm-completion labels differ. -/
theorem tracial_moment_label_ne_norm_completion :
    LimitTopology.NormalizedTracialMoments ≠ LimitTopology.CStarNormCompletion := by
  intro h
  nomatch h

/-- Two authored comparison labels differ; no equivalence or separation of limits is proved. -/
theorem moment_ne_quantum_metric :
    LimitTopology.MomentConvergence ≠ LimitTopology.QuantumMetricRieffel := by
  intro h
  nomatch h


-- ===========================================================================
-- Section 2: Fuzzy Sphere Commutator Norm Bound
-- ===========================================================================

/-- Arithmetic restatement of the supplied dimension bound. -/
theorem bound_numerator_le_dim (d : Nat) (h : d ≥ 2) : 2 ≤ d := h

/-- Strict monotonicity of the fuzzy sphere denominator:
    d1 < d2 implies d1 < d2, ensuring 2/d2 < 2/d1. -/
theorem bound_cross_products_increase {d1 d2 : Nat} (h : d1 < d2) :
    2 * d1 < 2 * d2 := Nat.mul_lt_mul_of_pos_left h (by decide)

/-- For concrete dimensions 2, 4, 8: 2 < 4 and 4 < 8. -/
theorem fuzzy_sphere_dim_steps : (2 : Nat) < 4 ∧ (4 : Nat) < 8 := by decide

/-- Numerator of the finite commutator `2(d-1)/d^2`. The comparison
    `2(d-1)/d^2 ≤ 2/d` is the whole claim; no norm completion is taken. -/
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


-- ===========================================================================
-- Section 3: Countermodel to Topology-Free Convergence
-- ===========================================================================

inductive ConvergenceVerdict where
  | ConvergesToZero
  | DoesNotConvergeToZero
  | Undetermined
  deriving DecidableEq, Repr

/-- Declared verdict table. Actual projections/moments and convergence are not encoded. -/
def declared_rank1_moment_verdict : LimitTopology → ConvergenceVerdict
  | LimitTopology.NormalizedTracialMoments => ConvergenceVerdict.ConvergesToZero
  | LimitTopology.MomentConvergence => ConvergenceVerdict.ConvergesToZero
  | LimitTopology.CStarNormCompletion => ConvergenceVerdict.DoesNotConvergeToZero
  | LimitTopology.AlgebraicDirectColimit => ConvergenceVerdict.Undetermined
  | LimitTopology.QuantumMetricRieffel => ConvergenceVerdict.Undetermined

/-- Two entries of the declared verdict table differ. -/
theorem declared_moment_and_norm_verdicts_differ :
    declared_rank1_moment_verdict LimitTopology.NormalizedTracialMoments ≠
    declared_rank1_moment_verdict LimitTopology.CStarNormCompletion := by
  intro h
  nomatch h


-- ===========================================================================
-- Section 4: Separation of Algebraic Union Q^ab from Analytic Completions
-- ===========================================================================

inductive CompletionFamily where
  | AlgebraicUncompletedQab
  | ArchimedeanComplex
  | NonArchimedeanPadic
  deriving DecidableEq, Repr

/-- Distinct algebraic and Archimedean labels, not a theorem about fields. -/
theorem declared_algebraic_and_archimedean_labels_differ :
    CompletionFamily.AlgebraicUncompletedQab ≠ CompletionFamily.ArchimedeanComplex := by
  intro h
  nomatch h

/-- Distinct Archimedean and non-Archimedean labels. -/
theorem declared_archimedean_and_padic_labels_differ :
    CompletionFamily.ArchimedeanComplex ≠ CompletionFamily.NonArchimedeanPadic := by
  intro h
  nomatch h

/-- Distinct algebraic and non-Archimedean labels. -/
theorem declared_algebraic_and_padic_labels_differ :
    CompletionFamily.AlgebraicUncompletedQab ≠ CompletionFamily.NonArchimedeanPadic := by
  intro h
  nomatch h


-- ===========================================================================
-- Section 5: Axiom Census & Auditing
-- ===========================================================================

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

end FableHilbertWalk20260819.H072
