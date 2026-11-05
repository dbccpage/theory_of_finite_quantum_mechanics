import Mathlib.Data.Real.Basic

/-!
# cptp_monotonicity

Formalization of CPTP Quotient Monotonicity under Cochain Homomorphisms (Requirement R5).

Given two quantum cochain complexes:
  C^0 --(d_0)--> C^1
  C'^0 --(d_0')--> C'^1
equipped with quantum trace/gauge functionals J_Q, J_Q' and quotient obstructions:
  Φ_Q([δ]) = inf_{α ∈ C^0} J_Q(δ - d_0 α)
  Φ_Q'([δ']) = inf_{α' ∈ C'^0} J_Q'(δ' - d_0' α')

Let (Λ^0, Λ^1) be a cochain homomorphism satisfying:
  1. Intertwining: Λ^1(d_0 α) = d_0'(Λ^0 α)
  2. Subtraction linearity: Λ^1(x - y) = Λ^1 x - Λ^1 y
  3. CPTP Contractivity: J_Q'(Λ^1 r) ≤ J_Q(r)

Then for any candidate repair α in C^0, α' = Λ^0 α in C'^0 satisfies:
  J_Q'(Λ^1 δ - d_0'(Λ^0 α)) ≤ J_Q(δ - d_0 α)
and the quotient obstruction descends monotonically:
  Φ_Q'([Λ^1 δ]) ≤ Φ_Q([δ]).

AuthorityEffect: None.
-/

namespace QuantumObserverGeometry

variable {C0 C1 C0' C1' : Type*} [Sub C1] [Sub C1']

structure QuantumComplex (C0 C1 : Type*) where
  d0 : C0 → C1
  J_Q : C1 → ℝ

/-- The set of candidate repair costs for a 1-cochain δ under gauge adjustments d_0 α. -/
def repairCostSet (QC : QuantumComplex C0 C1) (δ : C1) : Set ℝ :=
  { q | ∃ α : C0, q = QC.J_Q (δ - QC.d0 α) }

/-- Pointwise repair monotonicity: every candidate repair α in C^0 pushes forward
    under Λ^0 to a candidate repair in C'^0 with weakly smaller quantum cost. -/
theorem cptp_pointwise_repair_monotonicity
    (QC : QuantumComplex C0 C1) (QC' : QuantumComplex C0' C1')
    (Λ0 : C0 → C0') (Λ1 : C1 → C1')
    (h_intertwine : ∀ α : C0, Λ1 (QC.d0 α) = QC'.d0 (Λ0 α))
    (h_sub : ∀ x y : C1, Λ1 (x - y) = Λ1 x - Λ1 y)
    (h_contract : ∀ r : C1, QC'.J_Q (Λ1 r) ≤ QC.J_Q r)
    (δ : C1) (α : C0) :
    QC'.J_Q (Λ1 δ - QC'.d0 (Λ0 α)) ≤ QC.J_Q (δ - QC.d0 α) := by
  have h_res : Λ1 δ - QC'.d0 (Λ0 α) = Λ1 (δ - QC.d0 α) := by
    rw [h_sub, h_intertwine]
  rw [h_res]
  exact h_contract (δ - QC.d0 α)

/-- Orbit dominance: for any candidate repair α in C^0, there exists a candidate repair
    in C'^0 achieving weakly smaller gauge cost. -/
theorem cptp_orbit_dominance
    (QC : QuantumComplex C0 C1) (QC' : QuantumComplex C0' C1')
    (Λ0 : C0 → C0') (Λ1 : C1 → C1')
    (h_intertwine : ∀ α : C0, Λ1 (QC.d0 α) = QC'.d0 (Λ0 α))
    (h_sub : ∀ x y : C1, Λ1 (x - y) = Λ1 x - Λ1 y)
    (h_contract : ∀ r : C1, QC'.J_Q (Λ1 r) ≤ QC.J_Q r)
    (δ : C1) (α : C0) :
    ∃ α' : C0', QC'.J_Q (Λ1 δ - QC'.d0 α') ≤ QC.J_Q (δ - QC.d0 α) :=
  ⟨Λ0 α, cptp_pointwise_repair_monotonicity QC QC' Λ0 Λ1 h_intertwine h_sub h_contract δ α⟩

/-- An optimal quotient obstruction value is a lower bound attained on the gauge orbit. -/
structure OptimalQuotientObstruction (QC : QuantumComplex C0 C1) (δ : C1) where
  val : ℝ
  attained : ∃ α_opt : C0, val = QC.J_Q (δ - QC.d0 α_opt)
  is_min : ∀ α : C0, val ≤ QC.J_Q (δ - QC.d0 α)

/-- Monotonicity of Optimal Quotient Obstruction under CPTP cochain homomorphisms:
    Φ_Q'([Λ^1 δ]) ≤ Φ_Q([δ]). -/
theorem cptp_optimal_quotient_monotonicity
    (QC : QuantumComplex C0 C1) (QC' : QuantumComplex C0' C1')
    (Λ0 : C0 → C0') (Λ1 : C1 → C1')
    (h_intertwine : ∀ α : C0, Λ1 (QC.d0 α) = QC'.d0 (Λ0 α))
    (h_sub : ∀ x y : C1, Λ1 (x - y) = Λ1 x - Λ1 y)
    (h_contract : ∀ r : C1, QC'.J_Q (Λ1 r) ≤ QC.J_Q r)
    (δ : C1)
    (opt : OptimalQuotientObstruction QC δ)
    (opt' : OptimalQuotientObstruction QC' (Λ1 δ)) :
    opt'.val ≤ opt.val := by
  rcases opt.attained with ⟨α_opt, h_opt⟩
  have h_bound := opt'.is_min (Λ0 α_opt)
  have h_mono := cptp_pointwise_repair_monotonicity QC QC' Λ0 Λ1 h_intertwine h_sub h_contract δ α_opt
  rw [h_opt]
  exact h_bound.trans h_mono

/-- Attained Monotonicity Corollary: For explicit optimal gauge choices α_opt and α'_opt,
    the optimal gauge cost contracts monotonically. -/
theorem cptp_attained_quotient_monotonicity
    (QC : QuantumComplex C0 C1) (QC' : QuantumComplex C0' C1')
    (Λ0 : C0 → C0') (Λ1 : C1 → C1')
    (h_intertwine : ∀ α : C0, Λ1 (QC.d0 α) = QC'.d0 (Λ0 α))
    (h_sub : ∀ x y : C1, Λ1 (x - y) = Λ1 x - Λ1 y)
    (h_contract : ∀ r : C1, QC'.J_Q (Λ1 r) ≤ QC.J_Q r)
    (δ : C1) (α_opt : C0)
    (α'_opt : C0')
    (h'_opt : ∀ α' : C0', QC'.J_Q (Λ1 δ - QC'.d0 α'_opt) ≤ QC'.J_Q (Λ1 δ - QC'.d0 α')) :
    QC'.J_Q (Λ1 δ - QC'.d0 α'_opt) ≤ QC.J_Q (δ - QC.d0 α_opt) := by
  calc
    QC'.J_Q (Λ1 δ - QC'.d0 α'_opt) ≤ QC'.J_Q (Λ1 δ - QC'.d0 (Λ0 α_opt)) := h'_opt (Λ0 α_opt)
    _ ≤ QC.J_Q (δ - QC.d0 α_opt) :=
      cptp_pointwise_repair_monotonicity QC QC' Λ0 Λ1 h_intertwine h_sub h_contract δ α_opt

end QuantumObserverGeometry

#print axioms QuantumObserverGeometry.cptp_pointwise_repair_monotonicity
#print axioms QuantumObserverGeometry.cptp_orbit_dominance
#print axioms QuantumObserverGeometry.cptp_optimal_quotient_monotonicity
#print axioms QuantumObserverGeometry.cptp_attained_quotient_monotonicity
