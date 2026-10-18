import SzollosiColumnGauge

/-!
# Linear balance equations in the column gauge

AuthorityEffect: None.

Both additional raw bases have first row one. Their transition matrix has all
row and column sums six. These are consequences of the original equations and
column gauge, rather than additional assumptions on possible quartets. At least
one real entry in each transition row is at least one. No full-domain exclusion
or curvature certificate follows from these identities.
-/

noncomputable section
namespace MUB.SzollosiGaugeBalance
open Matrix
open scoped BigOperators
open ConcreteMubPolynomialSystem SzollosiTwoCirculant SzollosiQuartetSystem
open SzollosiQuadraticSystem SzollosiColumnGauge

theorem raw_right_gram (U : Candidate)
    (hU : U.conjTranspose * U = (6 : ℂ) • (1 : Candidate)) :
    U * U.conjTranspose = (6 : ℂ) • (1 : Candidate) := by
  have hleft : ((1/6 : ℂ) • U.conjTranspose) * U = 1 := by
    rw [Matrix.smul_mul,hU,smul_smul]
    norm_num
  have hright := mul_eq_one_comm.mp hleft
  have h6 := congrArg (fun M : Candidate => (6 : ℂ) • M) hright
  norm_num [Matrix.mul_smul,smul_smul] at h6
  exact h6

theorem raw_row_sum (U : Candidate)
    (hU : U.conjTranspose * U = (6 : ℂ) • (1 : Candidate))
    (hrow : ∀ j, U 0 j = 1) (i : Fin 6) :
    ∑ j, U i j = if i = 0 then 6 else 0 := by
  have h := congrArg (fun M : Candidate => M i 0) (raw_right_gram U hU)
  simpa [Matrix.mul_apply,Matrix.conjTranspose_apply,hrow,Matrix.smul_apply,Matrix.one_apply] using h

theorem transition_row_sum (U V : Candidate)
    (hV : V.conjTranspose * V = (6 : ℂ) • (1 : Candidate))
    (hrowU : ∀ j, U 0 j = 1) (hrowV : ∀ j, V 0 j = 1) (i : Fin 6) :
    ∑ j, (U.conjTranspose * V) i j = 6 := by
  simp only [Matrix.mul_apply,Matrix.conjTranspose_apply]
  rw [Finset.sum_comm]
  simp_rw [← Finset.mul_sum,raw_row_sum V hV hrowV]
  simp [mul_ite,hrowU]

theorem transition_column_sum (U V : Candidate)
    (hU : U.conjTranspose * U = (6 : ℂ) • (1 : Candidate))
    (hrowU : ∀ j, U 0 j = 1) (hrowV : ∀ j, V 0 j = 1) (j : Fin 6) :
    ∑ i, (U.conjTranspose * V) i j = 6 := by
  calc
    ∑ i, (U.conjTranspose * V) i j = star (∑ i, (V.conjTranspose * U) j i) := by
      rw [star_sum]
      apply Finset.sum_congr rfl
      intro i _
      simp only [Matrix.mul_apply,Matrix.conjTranspose_apply,star_sum,star_mul,star_star]
    _ = 6 := by rw [transition_row_sum V U hU hrowV hrowU]; norm_num

theorem solution_product_balanced (r : Variable → ℝ)
    (h : ∀ e, realEval r (equationPolynomial e) = 0) (hg : FirstRowGauge r) :
    (∀ i, ∑ j, product r 2 i j = 6) ∧ (∀ j, ∑ i, product r 2 i j = 6) := by
  have hr := (all_equations_zero_iff r).mp h
  have hc := solution_rawCandidates r hr
  have hp : product r 2 = (basis r 1).conjTranspose * basis r 2 := hr.2.2.2.2.1 2
  rw [hp]
  exact ⟨transition_row_sum _ _ hc.2.2.2.1 (hg 0) (hg 1),
    transition_column_sum _ _ hc.1 (hg 0) (hg 1)⟩

abbrev GaugeIndex := Fin 2 × Fin 6 × Bool
abbrev BalanceIndex := Bool × Fin 6 × Bool

def gaugePolynomial (s : GaugeIndex) : QPoly :=
  MvPolynomial.X (.inr (.inl (candidateIndex s.1,0,s.2.1,s.2.2))) -
    MvPolynomial.C (if s.2.2 then 0 else 1)

def balancePolynomial (s : BalanceIndex) : QPoly :=
  (∑ j : Fin 6, component
    (if s.1 then productPolynomial 2 j s.2.1 else productPolynomial 2 s.2.1 j) s.2.2) -
    MvPolynomial.C (if s.2.2 then 0 else 6)

theorem gauge_equations_iff (r : Variable → ℝ) :
    (∀ s, realEval r (gaugePolynomial s) = 0) ↔ FirstRowGauge r := by
  constructor
  · intro h a j
    apply Complex.ext
    · simpa [gaugePolynomial,realEval,basis,basisPolynomial,complexEval,sub_eq_zero] using h (a,j,false)
    · simpa [gaugePolynomial,realEval,basis,basisPolynomial,complexEval,sub_eq_zero] using h (a,j,true)
  · intro h s
    rcases s with ⟨a,j,b⟩
    have hc := firstRowGauge_coordinate r h a j b
    cases b <;> simpa [gaugePolynomial,realEval,sub_eq_zero] using hc

theorem solution_balance_equations (r : Variable → ℝ)
    (h : ∀ e, realEval r (equationPolynomial e) = 0) (hg : FirstRowGauge r) :
    ∀ s, realEval r (balancePolynomial s) = 0 := by
  have hb := solution_product_balanced r h hg
  rintro ⟨t,i,b⟩
  cases t <;> cases b
  · have hr := congrArg Complex.re (hb.1 i)
    simpa [balancePolynomial,component,productPolynomial,product,complexEval,realEval,sub_eq_zero] using hr
  · have hi := congrArg Complex.im (hb.1 i)
    simpa [balancePolynomial,component,productPolynomial,product,complexEval,realEval,sub_eq_zero] using hi
  · have hr := congrArg Complex.re (hb.2 i)
    simpa [balancePolynomial,component,productPolynomial,product,complexEval,realEval,sub_eq_zero] using hr
  · have hi := congrArg Complex.im (hb.2 i)
    simpa [balancePolynomial,component,productPolynomial,product,complexEval,realEval,sub_eq_zero] using hi

/-- Each balanced row meets one of six rational half-space charts. -/
theorem balanced_row_chart (W : Candidate) (i : Fin 6)
    (h : ∑ j, W i j = 6) : ∃ j, 1 ≤ (W i j).re := by
  by_contra! hlt
  have hr := congrArg Complex.re h
  have hs : ∑ j : Fin 6, (W i j).re < ∑ j : Fin 6, (1 : ℝ) :=
    Finset.sum_lt_sum (fun j _ => (hlt j).le) ⟨0,Finset.mem_univ _,hlt 0⟩
  simp at hr hs
  linarith

theorem solution_six_charts (r : Variable → ℝ)
    (h : ∀ e, realEval r (equationPolynomial e) = 0) (hg : FirstRowGauge r) :
    ∃ j, 1 ≤ (product r 2 0 j).re :=
  balanced_row_chart _ 0 ((solution_product_balanced r h hg).1 0)

#print axioms raw_right_gram
#print axioms transition_row_sum
#print axioms transition_column_sum
#print axioms solution_product_balanced
#print axioms gauge_equations_iff
#print axioms solution_balance_equations
#print axioms solution_six_charts
end MUB.SzollosiGaugeBalance
