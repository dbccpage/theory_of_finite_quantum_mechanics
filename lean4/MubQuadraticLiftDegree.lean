import MubQuadraticLiftPolynomials
import Mathlib.Algebra.MvPolynomial.CommRing

/-!
# Checked total degrees of the explicit quartet lift

AuthorityEffect: None. The bound concerns the actual rational polynomials.
-/
noncomputable section
namespace MUB.QuadraticLiftPolynomials
open QuadraticLift BoundedBlockChart
open BoundedCoordinates (fillE fillB fillC fillBasis)
open scoped BigOperators

def DegreeLE (p : CPoly) (n : ℕ) : Prop := p.re.totalDegree ≤ n ∧ p.im.totalDegree ≤ n

theorem degree_mono {p : CPoly} {m n : ℕ} (h : DegreeLE p m) (hmn : m ≤ n) :
    DegreeLE p n := ⟨h.1.trans hmn,h.2.trans hmn⟩
theorem degree_zero (n : ℕ) : DegreeLE 0 n := by simp [DegreeLE]
theorem degree_one (n : ℕ) : DegreeLE 1 n := by
  simp [DegreeLE, QuadraticAlgebra.re_one, QuadraticAlgebra.im_one]
theorem degree_add {p q : CPoly} {n : ℕ} (hp : DegreeLE p n) (hq : DegreeLE q n) :
    DegreeLE (p + q) n := by
  exact ⟨(MvPolynomial.totalDegree_add _ _).trans (max_le hp.1 hq.1),
    (MvPolynomial.totalDegree_add _ _).trans (max_le hp.2 hq.2)⟩
theorem degree_sub {p q : CPoly} {n : ℕ} (hp : DegreeLE p n) (hq : DegreeLE q n) :
    DegreeLE (p - q) n := by
  exact ⟨(MvPolynomial.totalDegree_sub _ _).trans (max_le hp.1 hq.1),
    (MvPolynomial.totalDegree_sub _ _).trans (max_le hp.2 hq.2)⟩
theorem degree_star {p : CPoly} {n : ℕ} (hp : DegreeLE p n) : DegreeLE (star p) n := by
  simpa [DegreeLE] using hp
theorem degree_mul {p q : CPoly} {m n : ℕ} (hp : DegreeLE p m) (hq : DegreeLE q n) :
    DegreeLE (p * q) (m + n) := by
  have hmul (x y : Poly) (hx : x.totalDegree ≤ m) (hy : y.totalDegree ≤ n) :
      (x * y).totalDegree ≤ m + n := (MvPolynomial.totalDegree_mul _ _).trans (Nat.add_le_add hx hy)
  constructor
  · have h := (MvPolynomial.totalDegree_sub (p.re * q.re) (p.im * q.im)).trans
      (max_le (hmul _ _ hp.1 hq.1) (hmul _ _ hp.2 hq.2))
    simpa [QuadraticAlgebra.re_mul, sub_eq_add_neg] using h
  · simpa [QuadraticAlgebra.im_mul] using
      (MvPolynomial.totalDegree_add (p.re * q.im) (p.im * q.re)).trans
        (max_le (hmul _ _ hp.1 hq.2) (hmul _ _ hp.2 hq.1))
theorem degree_sum {ι : Type*} (s : Finset ι) (f : ι → CPoly) (n : ℕ)
    (h : ∀ i ∈ s, DegreeLE (f i) n) : DegreeLE (∑ i ∈ s, f i) n := by
  classical
  induction s using Finset.induction_on with
  | empty => simpa using degree_zero n
  | @insert a s ha ih =>
    rw [Finset.sum_insert ha]
    exact degree_add (h a (Finset.mem_insert_self _ _))
      (ih (fun i hi => h i (Finset.mem_insert_of_mem hi)))

theorem variable_degree (s : LiftSlot) : DegreeLE (coordinatePoly s) 1 := by
  simp [DegreeLE, coordinatePoly]
theorem oldVariable_degree (s : BoundedCoordinates.Slot) : DegreeLE (oldVariable s) 1 :=
  variable_degree (.inl s)

theorem pE_degree (i j : I3) : DegreeLE (pE i j) 1 := by
  refine Fin.cases ?_ (fun k => ?_) i
  · exact degree_one 1
  · refine Fin.cases ?_ (fun l => ?_) j
    · exact degree_one 1
    · exact oldVariable_degree _
theorem pB_degree (i j : I3) : DegreeLE (pB i j) 1 := by
  refine Fin.cases ?_ (fun k => ?_) i
  · exact degree_one 1
  · exact oldVariable_degree _
theorem pC_degree (i j : I3) : DegreeLE (pC i j) 1 := by
  refine Fin.cases ?_ (fun k => ?_) j
  · exact degree_one 1
  · exact oldVariable_degree _
theorem pU_degree (i j : I6) : DegreeLE (pU i j) 1 := by
  obtain ⟨k,rfl⟩ := blockIndex.symm.surjective i
  change DegreeLE (Fin.cases (fun _ => 1) (fun l j => oldVariable _) (blockIndex (blockIndex.symm k)) j) 1
  rw [Equiv.apply_symm_apply]
  refine Fin.cases ?_ (fun l => ?_) k
  · exact degree_one 1
  · exact oldVariable_degree _
theorem pV_degree (i j : I6) : DegreeLE (pV i j) 1 := by
  obtain ⟨k,rfl⟩ := blockIndex.symm.surjective i
  change DegreeLE (Fin.cases (fun _ => 1) (fun l j => oldVariable _) (blockIndex (blockIndex.symm k)) j) 1
  rw [Equiv.apply_symm_apply]
  refine Fin.cases ?_ (fun l => ?_) k
  · exact degree_one 1
  · exact oldVariable_degree _
theorem pH_degree (i j : I6) : DegreeLE (pH i j) 1 := by
  cases i <;> cases j
  · exact pE_degree _ _
  · exact pB_degree _ _
  · exact pC_degree _ _
  · exact variable_degree _
theorem pBases_degree (a : Fin 3) (i j : I6) : DegreeLE (pBases a i j) 1 := by
  fin_cases a
  · exact pH_degree i j
  · exact pU_degree i j
  · exact pV_degree i j
theorem pW_degree (a : Fin 3) (i j : I6) : DegreeLE (pW a i j) 1 := variable_degree _

theorem transition_degree (A B : PMat6) (hA : ∀ i j, DegreeLE (A i j) 1)
    (hB : ∀ i j, DegreeLE (B i j) 1) (i j : I6) :
    DegreeLE ((A.conjTranspose * B) i j) 2 := by
  apply degree_sum
  intro k _
  exact degree_mul (degree_star (hA k i)) (hB k j)
theorem pTransitions_degree (a : Fin 3) (i j : I6) : DegreeLE (pTransitions a i j) 2 := by
  fin_cases a
  · exact transition_degree pH pU pH_degree pU_degree i j
  · exact transition_degree pH pV pH_degree pV_degree i j
  · exact transition_degree pU pV pU_degree pV_degree i j

theorem six_degree : DegreeLE (6 : CPoly) 0 := by
  change (MvPolynomial.C (6 : ℚ)).totalDegree ≤ 0 ∧ (0 : Poly).totalDegree ≤ 0
  simp
theorem gram_degree (a : Fin 3) (i j : I6) : DegreeLE (pGram (pBases a) i j) 2 := by
  apply degree_sub (transition_degree _ _ (pBases_degree a) (pBases_degree a) i j)
  change DegreeLE ((6 : CPoly) * (1 : PMat6) i j) 2
  have hid : DegreeLE ((1 : PMat6) i j) 0 := by
    classical
    by_cases h : i = j
    · simp only [Matrix.one_apply, if_pos h]
      exact degree_one 0
    · simp only [Matrix.one_apply, if_neg h]
      exact degree_zero 0
  exact degree_mono (degree_mul six_degree hid) (by omega)
theorem graph_degree (a : Fin 3) (i j : I6) : DegreeLE ((pW a - pTransitions a) i j) 2 :=
  degree_sub (degree_mono (pW_degree a i j) (by omega)) (pTransitions_degree a i j)

theorem norm_degree {p : CPoly} (hp : DegreeLE p 1) : (normPoly p).totalDegree ≤ 2 := by
  obtain ⟨hre,him⟩ := hp
  apply (MvPolynomial.totalDegree_add _ _).trans
  exact max_le ((MvPolynomial.totalDegree_pow _ _).trans (by omega))
    ((MvPolynomial.totalDegree_pow _ _).trans (by omega))
theorem component_degree {p : CPoly} {n : ℕ} (hp : DegreeLE p n) (b : Bool) :
    (component p b).totalDegree ≤ n := by
  cases b
  · exact hp.1
  · exact hp.2

theorem equation_degree (e : Equation) : (equationPolynomial e).totalDegree ≤ 2 := by
  rcases e with ⟨a,i,j⟩ | ⟨a,i,j,b⟩ | ⟨a,i,j,b⟩ | ⟨a,i,j⟩
  · exact (MvPolynomial.totalDegree_sub_C_le _ (1 : ℚ)).trans (norm_degree (pBases_degree a i j))
  · exact component_degree (gram_degree a i j) b
  · exact component_degree (graph_degree a i j) b
  · exact (MvPolynomial.totalDegree_sub_C_le _ (6 : ℚ)).trans (norm_degree (pW_degree a i j))

#print axioms degree_mul
#print axioms pBases_degree
#print axioms pTransitions_degree
#print axioms gram_degree
#print axioms graph_degree
#print axioms equation_degree
end MUB.QuadraticLiftPolynomials
