/-!
# Chosen COUNT aggregate laws and exact change minimum

The faithful aggregate of a source-16 state is (n, sum r, sum s, sum leftovers).
Each enabled source change has one of the eight relations below: admitting
is an assertion addition, with its own record effect. Identification preserves
all three totals and loses one term. SET and DROP are outside this model.

The lower bound holds for every finite aggregate trace. The constructive
trace adds n terms, r+l copies in r, s in s, then removes l from r; its length
is the potential. A cellwise realization produces any specified raw tables,
as proved in the accompanying source correspondence. Lean checks aggregate
relations and arithmetic here, not Python/Rust programs, pair-level enabled
predicates, canonicalization, or institutional admission.
-/

namespace WitnessedDifference.AdmissionCount

structure Totals where
  n : Nat
  r : Nat
  s : Nat
  l : Nat
  deriving DecidableEq

def potential (t : Totals) : Nat := t.n + t.r + t.s + 2*t.l
def mass (t : Totals) : Nat := t.r + t.s + t.l
def empty : Totals := ⟨0,0,0,0⟩

inductive Step : Totals → Totals → Prop
  | term (n r s l) : Step ⟨n,r,s,l⟩ ⟨n+1,r,s,l⟩
  | addR (n r s l) : Step ⟨n,r,s,l⟩ ⟨n,r+1,s,l⟩
  | addS (n r s l) : Step ⟨n,r,s,l⟩ ⟨n,r,s+1,l⟩
  | removeR (n r s l) : Step ⟨n,r+1,s,l⟩ ⟨n,r,s,l+1⟩
  | removeS (n r s l) : Step ⟨n,r,s+1,l⟩ ⟨n,r,s,l+1⟩
  | admitR (n r s l) : Step ⟨n,r,s,l+1⟩ ⟨n,r+1,s,l⟩
  | admitS (n r s l) : Step ⟨n,r,s,l+1⟩ ⟨n,r,s+1,l⟩
  | identify (n r s l) : Step ⟨n+1,r,s,l⟩ ⟨n,r,s,l⟩

theorem every_step_potential_upper (h : Step a b) : potential b ≤ potential a + 1 := by
  cases h <;> simp only [potential] <;> omega

theorem every_step_mass_monotone (h : Step a b) : mass a ≤ mass b := by
  cases h <;> simp only [mass] <;> omega

inductive Run : Totals → Totals → Nat → Prop
  | nil (a) : Run a a 0
  | snoc : Run a b k → Step b c → Run a c (k+1)

theorem runs_compose (first : Run a b k) (second : Run b c m) : Run a c (k+m) := by
  induction second with
  | nil => simpa using first
  | snoc prior one ih =>
    simpa only [Nat.add_assoc] using Run.snoc ih one

theorem every_run_potential_upper (run : Run a b k) : potential b ≤ potential a + k := by
  induction run with
  | nil => omega
  | snoc prior one ih =>
    have bound := every_step_potential_upper one
    omega

theorem every_run_mass_monotone (run : Run a b k) : mass a ≤ mass b := by
  induction run with
  | nil => omega
  | snoc prior one ih =>
    have bound := every_step_mass_monotone one
    omega

theorem from_empty_lower_bound (run : Run empty target k) : potential target ≤ k := by
  have bound := every_run_potential_upper run
  simpa [empty, potential] using bound

theorem build_terms (n : Nat) : Run empty ⟨n,0,0,0⟩ n := by
  induction n with
  | zero => exact Run.nil empty
  | succ n ih => exact Run.snoc ih (Step.term n 0 0 0)

theorem build_r (n r s l k : Nat) : Run ⟨n,r,s,l⟩ ⟨n,r+k,s,l⟩ k := by
  induction k with
  | zero => simpa using Run.nil (Totals.mk n r s l)
  | succ k ih =>
    simpa only [Nat.add_assoc] using Run.snoc ih (Step.addR n (r+k) s l)

theorem build_s (n r s l k : Nat) : Run ⟨n,r,s,l⟩ ⟨n,r,s+k,l⟩ k := by
  induction k with
  | zero => simpa using Run.nil (Totals.mk n r s l)
  | succ k ih =>
    simpa only [Nat.add_assoc] using Run.snoc ih (Step.addS n r (s+k) l)

theorem remove_r_block (n r s l k : Nat) : Run ⟨n,r+k,s,l⟩ ⟨n,r,s,l+k⟩ k := by
  induction k generalizing l with
  | zero => simpa using Run.nil (Totals.mk n r s l)
  | succ k ih =>
    have first : Run (Totals.mk n (r+(k+1)) s l) (Totals.mk n (r+k) s (l+1)) 1 := by
      exact Run.snoc (Run.nil _) (Step.removeR n (r+k) s l)
    have rest := ih (l+1)
    have joined := runs_compose first rest
    have hl : l+1+k = l+(k+1) := by omega
    have hk : 1+k = k+1 := by omega
    simpa only [hl,hk] using joined

theorem build_target (n r s l : Nat) : Run empty ⟨n,r,s,l⟩ (n+r+s+2*l) := by
  have terms := build_terms n
  have assertionsR : Run ⟨n,0,0,0⟩ ⟨n,r+l,0,0⟩ (r+l) := by
    simpa using build_r n 0 0 0 (r+l)
  have assertionsS : Run ⟨n,r+l,0,0⟩ ⟨n,r+l,s,0⟩ s := by
    simpa using build_s n (r+l) 0 0 s
  have removals : Run ⟨n,r+l,s,0⟩ ⟨n,r,s,l⟩ l := by
    simpa using remove_r_block n r s 0 l
  have joined := runs_compose (runs_compose (runs_compose terms assertionsR) assertionsS) removals
  have length : ((n+(r+l))+s)+l = n+r+s+2*l := by omega
  simpa only [Nat.zero_add,length] using joined

theorem potential_is_exact_aggregate_minimum (target : Totals) :
    Run empty target (potential target) ∧ ∀ k, Run empty target k → potential target ≤ k := by
  constructor
  · exact build_target target.n target.r target.s target.l
  · intro k run
    exact from_empty_lower_bound run

end WitnessedDifference.AdmissionCount

#print axioms WitnessedDifference.AdmissionCount.every_step_potential_upper
#print axioms WitnessedDifference.AdmissionCount.every_step_mass_monotone
#print axioms WitnessedDifference.AdmissionCount.runs_compose
#print axioms WitnessedDifference.AdmissionCount.every_run_potential_upper
#print axioms WitnessedDifference.AdmissionCount.every_run_mass_monotone
#print axioms WitnessedDifference.AdmissionCount.from_empty_lower_bound
#print axioms WitnessedDifference.AdmissionCount.build_terms
#print axioms WitnessedDifference.AdmissionCount.build_r
#print axioms WitnessedDifference.AdmissionCount.build_s
#print axioms WitnessedDifference.AdmissionCount.remove_r_block
#print axioms WitnessedDifference.AdmissionCount.build_target
#print axioms WitnessedDifference.AdmissionCount.potential_is_exact_aggregate_minimum
