import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Algebra.Order.Ring.Abs
import Mathlib.Tactic.FieldSimp
import BuildabilitySetS
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Algebra.Order.BigOperators.Group.Finset

/- Literal statements on supplied rational carriers. Native matrix/coordinate
   interpretations and physical imports remain separate obligations. -/
namespace QuantumMechanics.PromptResources
open scoped BigOperators

theorem projection_scalar (e : ℚ) : e*e=e ↔ e=0 ∨ e=1 := by
  constructor
  · intro h
    have hz : e*(e-1)=0 := by nlinarith
    rcases mul_eq_zero.mp hz with h0 | h1
    · exact Or.inl h0
    · exact Or.inr (by linarith)
  · rintro (rfl | rfl) <;> norm_num
theorem pairing_ambiguity : (1/(1+2):ℚ) ≠ 1^2/(1^2+2^2) := by norm_num

theorem fiber_global_i (a b : ℚ) : (-b)^2+a^2=a^2+b^2 := by ring
theorem interference_cross (a b c d : ℚ) :
    (a+c)^2+(b+d)^2-(a^2+b^2+c^2+d^2)=2*(a*c+b*d) := by ring
theorem interference_no_descent :
    ¬ ∃ f : ℚ × ℚ → ℚ, ∀ a b : ℚ, f (a^2,b^2)=(a+b)^2 := by
  rintro ⟨f,h⟩
  have hp := h 1 1
  have hm := h 1 (-1)
  norm_num at hp hm
  linarith

theorem buildability_alias (d : InterferenceNonL1Resource.DeviceModel) :
    InterferenceNonL1Resource.is_useful_quantum_computer d =
      InterferenceNonL1Resource.satisfies_Set_S d := rfl
theorem buildability_conjunction (a b c d : Bool) :
    (a && b && c && d)=true ↔ a=true ∧ b=true ∧ c=true ∧ d=true := by
  cases a <;> cases b <;> cases c <;> cases d <;> decide

theorem torsion_compatible (k : ℕ) : (k+4)%4=k%4 := Nat.add_mod_right k 4
theorem torsion_fourth :
    (0*0-1*1:ℚ) = -1 ∧ ((-1)*(-1):ℚ)=1 := by norm_num
theorem selector_product (a b c d : ℚ) :
    (a*c-b*d)^2+(a*d+b*c)^2=(a^2+b^2)*(c^2+d^2) := by ring
theorem selector_conjugation (a b c d : ℚ) :
    a*c-(-b)*(-d)=a*c-b*d ∧ a*(-d)+(-b)*c=-(a*d+b*c) := by constructor <;> ring

theorem holonomy_gauge (a b c d r s : ℚ) (h : r^2+s^2=1) :
    (r*a-s*b)*(r*c-s*d)+(s*a+r*b)*(s*c+r*d)=a*c+b*d ∧
    (r*a-s*b)*(s*c+r*d)-(s*a+r*b)*(r*c-s*d)=a*d-b*c := by
  constructor
  · calc
      _ = (r^2+s^2)*(a*c+b*d) := by ring
      _ = _ := by rw [h]; ring
  · calc
      _ = (r^2+s^2)*(a*d-b*c) := by ring
      _ = _ := by rw [h]; ring
theorem annex_triangle (a b c f g h : ℚ) :
    (g-f)+(h-g)+(f-h)=0 ∧
    (a+g-f)+(b+h-g)+(c+f-h)=a+b+c := by constructor <;> ring

theorem product_residuals (a b c d : ℚ) :
    (a+b+c+d)*a-(a+b)*(a+c)=a*d-b*c ∧
    (a+b+c+d)*b-(a+b)*(b+d)=-(a*d-b*c) ∧
    (a+b+c+d)*c-(c+d)*(a+c)=-(a*d-b*c) ∧
    (a+b+c+d)*d-(c+d)*(b+d)=a*d-b*c := by
  constructor
  · ring
  constructor
  · ring
  constructor <;> ring
theorem product_defect_zero (t : ℚ) : 4*t^2=0 ↔ t=0 := by
  constructor
  · intro h; nlinarith [sq_nonneg t]
  · rintro rfl; norm_num
theorem product_fidelity_gap (a b c d : ℚ)
    (ha : a^2+b^2=1) (hb : c^2+d^2=1) :
    1/2-(a*c+b*d)^2/2=(a*d-b*c)^2/2 := by
  have h : (a*c+b*d)^2+(a*d-b*c)^2=1 := by
    calc
      _ = (a^2+b^2)*(c^2+d^2) := by ring
      _ = 1 := by rw [ha,hb]; norm_num
  linarith
theorem finite_hull_separator {n : ℕ} (w f : Fin n → ℚ) (t : ℚ)
    (hw : ∀ i, 0≤w i) (hn : ∑ i,w i=1) (hf : ∀ i, t≤f i) :
    t≤∑ i,w i*f i := by
  calc
    t = ∑ i,w i*t := by rw [← Finset.sum_mul,hn]; ring
    _ ≤ _ := Finset.sum_le_sum fun i _ => mul_le_mul_of_nonneg_left (hf i) (hw i)
theorem qubit_phase_readout (c : ℚ) :
    (1/2+c)-(1/2-c)=2*c := by ring
theorem qubit_purity (p c : ℚ) :
    (p^2+(1-p)^2+2*c^2)-(p^2+(1-p)^2)=2*c^2 := by ring

theorem bell_table_readout (v : ℚ) : v+v+v-(-v)=4*v := by ring
theorem bell_admission_counterexample : (4:ℚ)>2 ∧ (4:ℚ)^2>8 := by norm_num
theorem chsh_deterministic (a b c d : Bool) :
    let s : Bool → ℚ := fun z => if z then 1 else -1
    |s a*(s c+s d)+s b*(s c-s d)|=2 := by
  cases a <;> cases b <;> cases c <;> cases d <;> norm_num
theorem convex_abs_bound {n : ℕ} (w f : Fin n → ℚ) (B : ℚ)
    (hw : ∀ i,0≤w i) (hn : ∑ i,w i=1) (hf : ∀ i,|f i|≤B) :
    |∑ i,w i*f i|≤B := by
  calc
    _ ≤ ∑ i,|w i*f i| := Finset.abs_sum_le_sum_abs _ _
    _ = ∑ i,w i*|f i| := by
      apply Finset.sum_congr rfl; intro i _; rw [abs_mul,abs_of_nonneg (hw i)]
    _ ≤ ∑ i,w i*B := Finset.sum_le_sum fun i _ => mul_le_mul_of_nonneg_left (hf i) (hw i)
    _ = B := by rw [← Finset.sum_mul,hn]; ring
theorem nosignal_family (v : ℚ) :
    (1+v)/4+(1-v)/4=1/2 := by ring
theorem nosignal_not_product : (1/2:ℚ) ≠ (1/2)*(1/2) := by norm_num

theorem trace_diagonal (p q : ℚ) : (|p-q| +|q-p|)/2=|p-q| := by
  rw [abs_sub_comm q p]; ring
theorem dual_shift (r s t k : ℚ) : r*(s+k)-r*(t+k)=r*s-r*t := by ring
theorem dual_bound (r s t : ℚ) (hs : |s|≤1) (ht : |t|≤1) :
    |r*s-r*t|≤2*|r| := by
  calc
    _ ≤ |r*s| +|r*t| := abs_sub _ _
    _ = |r| *|s| +|r| *|t| := by rw [abs_mul,abs_mul]
    _ ≤ |r| *1+|r| *1 := add_le_add (mul_le_mul_of_nonneg_left hs (abs_nonneg r)) (mul_le_mul_of_nonneg_left ht (abs_nonneg r))
    _ = _ := by ring
theorem dual_attained (r : ℚ) : ∃ s t : ℚ, |s|≤1 ∧ |t|≤1 ∧ r*s-r*t=2*|r| := by
  by_cases h : 0≤r
  · refine ⟨1,-1,by norm_num,by norm_num,?_⟩
    rw [abs_of_nonneg h]; ring
  · have hr : r≤0 := le_of_not_ge h
    refine ⟨-1,1,by norm_num,by norm_num,?_⟩
    rw [abs_of_nonpos hr]; ring
theorem monotone_rescaling (a b c : ℚ) (h : a≤b) (hc : 0≤c) : c*a≤c*b :=
  mul_le_mul_of_nonneg_left h hc
theorem monotone_distinct (a : ℚ) (h : 0<a) : a≠2*a := by linarith

theorem stochastic_contraction {m n : ℕ} (K : Fin m → Fin n → ℚ) (x : Fin n → ℚ)
    (hK : ∀ i j,0≤K i j) (hcol : ∀ j,∑ i,K i j=1) :
    (∑ i,|∑ j,K i j*x j|)≤∑ j,|x j| := by
  calc
    _ ≤ ∑ i,∑ j,|K i j*x j| := Finset.sum_le_sum fun i _ => Finset.abs_sum_le_sum_abs _ _
    _ = ∑ i,∑ j,K i j*|x j| := by
      apply Finset.sum_congr rfl; intro i _
      apply Finset.sum_congr rfl; intro j _; rw [abs_mul,abs_of_nonneg (hK i j)]
    _ = ∑ j,∑ i,K i j*|x j| := Finset.sum_comm
    _ = ∑ j,|x j| := by
      apply Finset.sum_congr rfl; intro j _
      rw [← Finset.sum_mul,hcol j,one_mul]
theorem channel_cayley (t : ℚ) :
    ((1-t^2)/(1+t^2))^2+(2*t/(1+t^2))^2=1 := by
  have h : 1+t^2≠0 := by nlinarith [sq_nonneg t]
  field_simp
  <;> ring
theorem channel_population (r s v w p : ℚ) (h0 : r^2+s^2=1) (h1 : v^2+w^2=1) :
    (r^2*p+v^2*(1-p))+(s^2*p+w^2*(1-p))=1 := by
  calc
    _ = (r^2+s^2)*p+(v^2+w^2)*(1-p) := by ring
    _ = 1 := by rw [h0,h1]; ring
theorem channel_shadow_not_unique : (1/2:ℚ)≠0 := by norm_num

def receiptGate (defect : ℕ) : Bool := decide (defect=0)
theorem firewall_gate (d : ℕ) : receiptGate d=true ↔ d=0 := by simp [receiptGate]
theorem firewall_nonimplication : ¬ (∀ derived auth : Prop, derived → auth) := by
  intro h; exact h True False True.intro
theorem unary_graft_assoc {A B C D : Type} (f : A→B) (g : B→C) (h : C→D) :
    (h ∘ g) ∘ f = h ∘ (g ∘ f) := rfl

end QuantumMechanics.PromptResources

#print axioms QuantumMechanics.PromptResources.projection_scalar
#print axioms QuantumMechanics.PromptResources.pairing_ambiguity
#print axioms QuantumMechanics.PromptResources.fiber_global_i
#print axioms QuantumMechanics.PromptResources.interference_cross
#print axioms QuantumMechanics.PromptResources.interference_no_descent
#print axioms QuantumMechanics.PromptResources.buildability_alias
#print axioms QuantumMechanics.PromptResources.buildability_conjunction
#print axioms QuantumMechanics.PromptResources.torsion_compatible
#print axioms QuantumMechanics.PromptResources.torsion_fourth
#print axioms QuantumMechanics.PromptResources.selector_product
#print axioms QuantumMechanics.PromptResources.selector_conjugation
#print axioms QuantumMechanics.PromptResources.holonomy_gauge
#print axioms QuantumMechanics.PromptResources.annex_triangle
#print axioms QuantumMechanics.PromptResources.product_residuals
#print axioms QuantumMechanics.PromptResources.product_defect_zero
#print axioms QuantumMechanics.PromptResources.product_fidelity_gap
#print axioms QuantumMechanics.PromptResources.finite_hull_separator
#print axioms QuantumMechanics.PromptResources.qubit_phase_readout
#print axioms QuantumMechanics.PromptResources.qubit_purity
#print axioms QuantumMechanics.PromptResources.bell_table_readout
#print axioms QuantumMechanics.PromptResources.bell_admission_counterexample
#print axioms QuantumMechanics.PromptResources.chsh_deterministic
#print axioms QuantumMechanics.PromptResources.convex_abs_bound
#print axioms QuantumMechanics.PromptResources.nosignal_family
#print axioms QuantumMechanics.PromptResources.nosignal_not_product
#print axioms QuantumMechanics.PromptResources.trace_diagonal
#print axioms QuantumMechanics.PromptResources.dual_shift
#print axioms QuantumMechanics.PromptResources.dual_bound
#print axioms QuantumMechanics.PromptResources.dual_attained
#print axioms QuantumMechanics.PromptResources.monotone_rescaling
#print axioms QuantumMechanics.PromptResources.monotone_distinct
#print axioms QuantumMechanics.PromptResources.stochastic_contraction
#print axioms QuantumMechanics.PromptResources.channel_cayley
#print axioms QuantumMechanics.PromptResources.channel_population
#print axioms QuantumMechanics.PromptResources.channel_shadow_not_unique
#print axioms QuantumMechanics.PromptResources.firewall_gate
#print axioms QuantumMechanics.PromptResources.firewall_nonimplication
#print axioms QuantumMechanics.PromptResources.unary_graft_assoc
