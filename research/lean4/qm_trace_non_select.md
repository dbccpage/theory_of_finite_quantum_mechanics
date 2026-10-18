/-!
LT-L — CPTP-monotone ⊬ trace-norm selection (the metric firewall).

Paper: `10_trace_norm_cptp_transport_audit.md` §3; `005` Theorem 2(ii);
`11_finite_weighted_transport_calculus_for_qm.md` T5.

A functional on a finite difference space is modelled as `V → Nat`. It is
**CPTP-monotone** relative to a declared family of data-processing contractions if
it is non-increasing under each. The firewall fact is that **scaling preserves
monotonicity**: from any nonzero CPTP-monotone functional `j`, both `j` and `2·j`
are CPTP-monotone and distinct. Hence CPTP monotonicity alone does **not** select a
unique (normalized) functional — in particular it does not single out the
trace-norm shadow. This mechanizes the `005` Theorem 2(ii) scalar-family
counterexample.

No real trace-norm theory is needed for the non-selection direction; no metric is
selected; no authority minted. Mathlib-free (core `Nat`/`List`/`omega`).
-/

namespace QM

/-- A functional on a finite difference space. -/
abbrev Functional (V : Type) := V → Nat

/-- `j` does not increase under the contraction `T` (one data-processing step). -/
def MonotoneUnder {V : Type} (T : V → V) (j : Functional V) : Prop :=
  ∀ x, j (T x) ≤ j x

/-- `j` is CPTP-monotone relative to a declared family of contractions. -/
def CPTPMonotone {V : Type} (Ts : List (V → V)) (j : Functional V) : Prop :=
  ∀ T ∈ Ts, MonotoneUnder T j

/-- Scaling a CPTP-monotone functional by a constant preserves monotonicity. -/
theorem scale_monotone {V : Type} (Ts : List (V → V)) (j : Functional V) (c : Nat)
    (h : CPTPMonotone Ts j) : CPTPMonotone Ts (fun x => c * j x) := by
  intro T hT x
  show c * j (T x) ≤ c * j x
  exact Nat.mul_le_mul (Nat.le_refl c) (h T hT x)

/-- **Metric firewall.** CPTP monotonicity does not select a unique functional: from
any CPTP-monotone `j` nonzero somewhere, `j` and `2·j` are two distinct
CPTP-monotone functionals. -/
theorem cptp_monotone_not_select {V : Type} (Ts : List (V → V)) (j : Functional V)
    (hj : CPTPMonotone Ts j) (x0 : V) (hx0 : j x0 ≠ 0) :
    ∃ j1 j2 : Functional V, CPTPMonotone Ts j1 ∧ CPTPMonotone Ts j2 ∧ j1 ≠ j2 := by
  refine ⟨j, (fun x => 2 * j x), hj, scale_monotone Ts j 2 hj, ?_⟩
  intro hEq
  have h : j x0 = 2 * j x0 := congrFun hEq x0
  omega

/-- **Trace-norm non-selection.** For a designated trace-norm shadow `tn` that is
CPTP-monotone and nonzero somewhere, `2·tn` is a CPTP-monotone functional distinct
from `tn`; hence CPTP monotonicity does not single out `tn`. -/
theorem cptp_monotone_not_select_traceNorm {V : Type} (Ts : List (V → V))
    (tn : Functional V) (htn : CPTPMonotone Ts tn) (x0 : V) (hx0 : tn x0 ≠ 0) :
    ∃ j : Functional V, CPTPMonotone Ts j ∧ j ≠ tn := by
  refine ⟨(fun x => 2 * tn x), scale_monotone Ts tn 2 htn, ?_⟩
  intro hEq
  have h : 2 * tn x0 = tn x0 := congrFun hEq x0
  omega

/-- A genuine concrete contraction: the identity functional over `ℕ` is CPTP-monotone
under the halving step `x ↦ x / 2` (a non-increasing data-processing step). -/
theorem id_cptpMonotone_halving :
    CPTPMonotone [fun x : Nat => x / 2] (id : Functional Nat) := by
  intro T hT x
  simp only [List.mem_singleton] at hT
  subst hT
  show x / 2 ≤ x
  exact Nat.div_le_self x 2

/-- Concrete seal: under a genuine non-increasing contraction the trace-norm shadow
(`id`) is not selected — `2·id` is also CPTP-monotone and distinct. -/
example : ∃ j : Functional Nat,
    CPTPMonotone [fun x : Nat => x / 2] j ∧ j ≠ (id : Functional Nat) :=
  cptp_monotone_not_select_traceNorm _ id id_cptpMonotone_halving 1 (by decide)

end QM

#print axioms QM.scale_monotone
#print axioms QM.cptp_monotone_not_select
#print axioms QM.cptp_monotone_not_select_traceNorm
#print axioms QM.id_cptpMonotone_halving
