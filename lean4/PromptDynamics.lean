import PromptStructure
import DynamicsDichotomy
import RationalSector
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic.NormNum.IsSquare
import Mathlib.Data.Rat.Lemmas

/- Exact identities on admitted carriers. Each native matrix interpretation has
   its own transport obligation; no continuum or physical selection is inferred. -/
namespace QuantumMechanics.PromptDynamics

theorem graded_powers (A : Matrix (Fin 2) (Fin 2) ℚ) (m n : ℕ) :
    A^(m+n)=A^m*A^n := pow_add A m n

theorem transfer_associative (a b c d e f : ℚ) :
    a*(c*e+d*f)+b*(d*e+c*f)=(a*c+b*d)*e+(a*d+b*c)*f := by ring

theorem overcount_mixed (a b d : ℚ) :
    (2*d+3*a*b)-3*(d+a*b) = -d := by ring

theorem refinement_composition (n m k u : ℚ) :
    (u+(m-k))+(n-m)=u+(n-k) := by ring

theorem refinement_singleton_compatible (n k : ℚ) :
    k+(n-k)=n := by ring

theorem histories_cross_term (p q : ℚ) :
    (p+q)^2-(p^2+q^2)=2*p*q := by ring

theorem held_phase_control (a b : ℚ) :
    (-b)^2=b^2 ∧ (a+b)^2-(a-b)^2=4*a*b := by constructor <;> ring

-- hbar multiplication clears a declared nonzero hbar, without introducing time.
theorem schrodinger_rate (h0 h1 u v a b c d : ℚ) :
    a*(h0*b+u*d+v*c)-b*(h0*a+u*c-v*d)+
    c*(u*b-v*a+h1*d)-d*(u*a+v*b+h1*c)=0 := by ring

theorem euler_drift (a b c d x y z w t : ℚ)
    (h : a*x+b*y+c*z+d*w=0) :
    (a+t*x)^2+(b+t*y)^2+(c+t*z)^2+(d+t*w)^2-
    (a^2+b^2+c^2+d^2)=t^2*(x^2+y^2+z^2+w^2) := by
  calc
    _ = t^2*(x^2+y^2+z^2+w^2)+2*t*(a*x+b*y+c*z+d*w) := by ring
    _ = _ := by rw [h]; ring

theorem cayley_cleared (t : ℚ) :
    (1-t^2)^2+(2*t)^2=(1+t^2)^2 := by ring

theorem clifford_control :
    (1:ℚ)*0+0*(-1)=0 ∧ (1:ℚ)^2=(-1)^2 := by norm_num

-- The diagonal entries of [lambda1,lambda2] are ±2 i r².
-- The remaining entries and two cyclic permutations are native matrix gates.
theorem lambda_diagonal (r : ℚ) : r*r-(-r*r)=2*r*r := by ring

theorem heisenberg_pairing (a b c r s v w : ℚ) :
    a*(r*v+s*w)^2+2*b*(r*v+s*w)*(-s*v+r*w)+c*(-s*v+r*w)^2 =
    (a*r^2-2*b*r*s+c*s^2)*v^2+
    2*(a*r*s+b*(r^2-s^2)-c*r*s)*v*w+
    (a*s^2+2*b*r*s+c*r^2)*w^2 := by ring

theorem decoherence_positive (a b x y : ℚ) :
    0 ≤ a^2*x^2+2*a*b*x*y+b^2*y^2 := by
  nlinarith [sq_nonneg (a*x+b*y)]

theorem decoherence_completeness_distinction :
    (1/2:ℚ)+1/2=1 ∧ (1/2:ℚ)^2+(1/2)^2≠1 ∧
    (3/5:ℚ)^2+(4/5)^2=1 ∧ ((3/5:ℚ)+4/5)^2≠1 := by norm_num

theorem global_offdiagonal (a b c : ℚ) :
    (a+2*b+c)-(a+c)=2*b := by ring

theorem finite_ccr (n : ℕ) (hn : 0<n)
    (A B : Matrix (Fin n) (Fin n) ℚ) (l : ℚ)
    (h : A*B-B*A=l • (1 : Matrix (Fin n) (Fin n) ℚ)) : l=0 := by
  have ht := congrArg Matrix.trace h
  rw [Matrix.trace_sub, Matrix.trace_mul_comm A B, sub_self,
    Matrix.trace_smul, Matrix.trace_one] at ht
  simp only [Fintype.card_fin, smul_eq_mul] at ht
  have hnq : (n:ℚ)≠0 := by exact_mod_cast (Nat.ne_of_gt hn)
  exact (mul_eq_zero.mp ht.symm).resolve_right hnq

theorem dichotomy_integer_numerator (n : ℕ) :
    (HilbertWalk.DynamicsDichotomy.pythPower n).2≠0 :=
  HilbertWalk.DynamicsDichotomy.pythPower_im_ne_zero n

theorem stone_no_report_root : ¬ ∃ f : Bool → Bool,
    ∀ b, f (f b)=HilbertWalk.DiscreteDynamicsStone.toggle b :=
  HilbertWalk.DiscreteDynamicsStone.no_bool_half_step

theorem stone_two_scaled_roots :
    HilbertWalk.DiscreteDynamicsStone.mat2g_mul
      HilbertWalk.DiscreteDynamicsStone.neg_M_scaled
      HilbertWalk.DiscreteDynamicsStone.neg_M_scaled =
      HilbertWalk.DiscreteDynamicsStone.four_X ∧
    HilbertWalk.DiscreteDynamicsStone.neg_M_scaled≠
      HilbertWalk.DiscreteDynamicsStone.M_scaled :=
  HilbertWalk.DiscreteDynamicsStone.interpolant_not_unique

theorem everett_finegraining (p0 p1 D : ℕ) (hD : D>0) (hs : p0+p1=D) :
    ∃ fg : HilbertWalk.RationalSector.FineGraining2,
      HilbertWalk.RationalSector.ReproducesPair fg p0 p1 D :=
  HilbertWalk.RationalSector.rational_finegraining_exists p0 p1 D hD hs

-- Full rational domain, not four hand-picked rational candidates.
theorem everett_no_rational_root (x : ℚ) : 5*x^2-5*x+1≠0 := by
  intro h
  have h5 : ¬ IsSquare (5:ℚ) := by norm_num
  apply h5
  exact ⟨10*x-5, by nlinarith [h]⟩

theorem embedding_interval (s : ℝ) (hs : s^2=5) (hp : 0<s) :
    2<s ∧ s<3 := by constructor <;> nlinarith

theorem embedding_mixed (s : ℝ) (hs : s^2=5) (hp : 0<s) :
    0<s-2 ∧ 0<3-s ∧ -s-2<0 := by
  obtain ⟨h2,h3⟩ := embedding_interval s hs hp
  constructor
  · linarith
  constructor <;> linarith

theorem embedding_gram_positive (a b s x : ℝ) :
    0≤((a+b*s)*x)^2 := sq_nonneg _

theorem embedding_reject_fake_root : (9/4:ℚ)^2-5=1/16 := by norm_num

theorem stone_gap_alias (n k : ℤ) :
    (n*(k+4))%4=(n*k)%4 := by
  have h : n*(k+4)=n*k+n*4 := by ring
  rw [h]
  simp [Int.add_emod, Int.mul_emod]

theorem cptp_bell_positive (t x w : ℚ) (ht : 0≤t) :
    0≤t/2*(x+w)^2 := mul_nonneg (div_nonneg ht (by norm_num)) (sq_nonneg _)

theorem cptp_partial_transpose_negative (t : ℚ) (ht : 0<t) :
    t/2*((1:ℚ)*(-1)+(-1)*1) = -t ∧ -t<0 := by
  constructor
  · ring
  · linarith

theorem condition_normalization {ι : Type} (s : Finset ι) (w : ι → ℚ)
    (h : (∑ i ∈ s, w i)≠0) :
    (∑ i ∈ s, w i / (∑ j ∈ s, w j))=1 := by
  simp_rw [div_eq_mul_inv]
  rw [← Finset.sum_mul, mul_inv_cancel₀ h]

theorem condition_idempotence (p : ℚ) : p/1=p := div_one p

end QuantumMechanics.PromptDynamics

#print axioms QuantumMechanics.PromptDynamics.graded_powers
#print axioms QuantumMechanics.PromptDynamics.transfer_associative
#print axioms QuantumMechanics.PromptDynamics.overcount_mixed
#print axioms QuantumMechanics.PromptDynamics.refinement_composition
#print axioms QuantumMechanics.PromptDynamics.refinement_singleton_compatible
#print axioms QuantumMechanics.PromptDynamics.histories_cross_term
#print axioms QuantumMechanics.PromptDynamics.held_phase_control
#print axioms QuantumMechanics.PromptDynamics.schrodinger_rate
#print axioms QuantumMechanics.PromptDynamics.euler_drift
#print axioms QuantumMechanics.PromptDynamics.cayley_cleared
#print axioms QuantumMechanics.PromptDynamics.clifford_control
#print axioms QuantumMechanics.PromptDynamics.lambda_diagonal
#print axioms QuantumMechanics.PromptDynamics.heisenberg_pairing
#print axioms QuantumMechanics.PromptDynamics.decoherence_positive
#print axioms QuantumMechanics.PromptDynamics.decoherence_completeness_distinction
#print axioms QuantumMechanics.PromptDynamics.global_offdiagonal
#print axioms QuantumMechanics.PromptDynamics.finite_ccr
#print axioms QuantumMechanics.PromptDynamics.dichotomy_integer_numerator
#print axioms QuantumMechanics.PromptDynamics.stone_no_report_root
#print axioms QuantumMechanics.PromptDynamics.stone_two_scaled_roots
#print axioms QuantumMechanics.PromptDynamics.everett_finegraining
#print axioms QuantumMechanics.PromptDynamics.everett_no_rational_root
#print axioms QuantumMechanics.PromptDynamics.embedding_interval
#print axioms QuantumMechanics.PromptDynamics.embedding_mixed
#print axioms QuantumMechanics.PromptDynamics.embedding_gram_positive
#print axioms QuantumMechanics.PromptDynamics.embedding_reject_fake_root
#print axioms QuantumMechanics.PromptDynamics.stone_gap_alias
#print axioms QuantumMechanics.PromptDynamics.cptp_bell_positive
#print axioms QuantumMechanics.PromptDynamics.cptp_partial_transpose_negative
#print axioms QuantumMechanics.PromptDynamics.condition_normalization
#print axioms QuantumMechanics.PromptDynamics.condition_idempotence
