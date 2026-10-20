import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Init.Omega

/- Literal scalar and finite controls. Full native-array refinement and original
   imported structures remain separate obligations in the per-prompt records. -/
namespace QuantumMechanics.PromptL1Imports

theorem chain_law (a b c : ℚ) : (b-a)+(c-b)+(a-c)=0 := by ring
theorem chain_control : (1 : ℚ)+0+(-1)=0 ∧ (1 : ℚ)≠0 := by norm_num

theorem kkt_law (P D : ℚ) (f : ℚ→ℚ) (lower : ∀ t,D≤f t)
    (gap : P=D) : ∀ t,P≤f t := by intro t; rw [gap]; exact lower t
theorem kkt_control : ¬ (|(2 : ℚ)|≤1) := by norm_num

theorem edge_law (a b p q : ℚ) : (p*b+q*a)-(p*a+q*b)=(p-q)*(b-a) := by ring
theorem edge_control : max (1 : ℚ) 1 ≠ max (1 : ℚ) 0 + max (0 : ℚ) 1 := by norm_num

theorem gauge_law (a b p : ℚ) : p*|-a|+p*|b|=p*|b|+p*|a| := by rw [abs_neg]; ring
theorem gauge_control : (3 : ℚ)^2+4^2=5^2 ∧ (3 : ℚ)+4≠5 := by norm_num

theorem observer_law (a b : ℚ) : (2*a)^2+(2*b)^2-2*(a^2+b^2)=2*(a^2+b^2) := by ring
theorem observer_control : max (1 : ℚ) 1=1 ∧ (1 : ℚ)+1=2 := by norm_num

theorem quotient_law (a b c m p q t : ℚ) (hm : 0≤m)
    (hp : m≤p) (hq : m≤q) (ht : m≤t) :
    m*|a+b+c|≤p*|a|+q*|b|+t*|c| := by
  have h1 := abs_add_le a b
  have h2 := abs_add_le (a+b) c
  have h3 := abs_nonneg a
  have h4 := abs_nonneg b
  have h5 := abs_nonneg c
  nlinarith

theorem quotient_control (a b c u v w : ℚ) :
    (a+v-u)+(b+w-v)+(c+u-w)=a+b+c := by ring

theorem replica_law (a b n : ℚ) : (n*a)^2+(n*b)^2=n^2*(a^2+b^2) := by ring
theorem replica_control : (2 : ℚ)*(3^2+4^2)=50 ∧ ((2 : ℚ)*3)^2+(2*4)^2=100 := by norm_num

theorem window_law (a b c : ℚ) : |(b-a)+(c-b)+(a-c)|=0 := by rw [chain_law]; norm_num
theorem window_control : (0 : ℚ)=0 ∧ ¬ ((0 : ℚ)≠0) := by norm_num

theorem mass_law (a b c d : ℚ) (h : a+b+c+d≠0) :
    a/(a+b+c+d)+b/(a+b+c+d)+c/(a+b+c+d)+d/(a+b+c+d)=1 := by
  field_simp

theorem mass_control : (1 : ℚ)/10+2/10+3/10+4/10=1 ∧ (0 : ℚ)=0 := by norm_num

theorem circle_law : (2*1)%3≠0 ∧ (2*1)%4≠0 ∧ (2*1)%2=0 := by decide
theorem circle_control : (1+1 : ℚ)^2=4 ∧ (1-1 : ℚ)^2=0 := by norm_num

theorem gauss_law (u v : ℤ) : ¬ (u-v=1 ∧ u+v=0) := by omega
theorem gauss_control (u : ℤ) : u*u≠2 := by
  intro h
  have hu : -1≤u ∧ u≤1 := by constructor <;> nlinarith [sq_nonneg (u-1),sq_nonneg (u+1)]
  have cases : u = -1 ∨ u = 0 ∨ u = 1 := by omega
  rcases cases with rfl | rfl | rfl <;> norm_num at h

theorem time_law (s : ℚ) (hs : s*s=1) :
    ((1/2 : ℚ)^2-(s/2)^2)+((1/2 : ℚ)^2-(-s/2)^2)=0 ∧
      2*((1/2 : ℚ)*(1/2)-(s/2)*(-s/2))=1 := by
  constructor <;> nlinarith

def boolSquare (a b : Bool) (q : Bool) : Bool :=
  let f := fun x : Bool => if x then b else a
  f (f q)
theorem time_control : ∀ a b : Bool,¬ (boolSquare a b false=true ∧ boolSquare a b true=false) := by decide

theorem hilbert_law (S T : ℚ) (h : S+T=1/3) : (S+3*T/4)+T/4=1/3 := by linarith
theorem hilbert_control (T : ℚ) (h : 0<T) : ¬ (T=0) := ne_of_gt h

theorem dilation_law {T : Type} (f g : T→T) (h : ∀ t,g (f t)=t) :
    Function.Injective f := by intro a b e; have := congrArg g e; simpa only [h] using this

theorem dilation_control (a d : ℚ) (h : a+d=1) : a+d=1 ∧ (a+d)*1=1 := by constructor; exact h; simpa using h

theorem gleason_law (a b : ℚ) : (a+b)^2+(a-b)^2=2*(a^2+b^2) := by ring
theorem gleason_control (a b : ℚ) : (a+b)^4+(a-b)^4-2*(a^2+b^2)^2=8*a^2*b^2 := by ring

theorem tensor_law (a b c d : ℚ) : (a*c)^2+(a*d)^2+(b*c)^2+(b*d)^2=(a^2+b^2)*(c^2+d^2) := by ring
theorem tensor_control : ((1 : ℚ)*(1+0),0) = ((1 : ℚ)*(0+1),0) ∧ ((1 : ℚ)*0,1*1) ≠ ((1 : ℚ)*1,1*0) := by norm_num

theorem lift_law (a b c d : ℚ) : (a^2+b^2)*(c^2+d^2)-(a*c+b*d)^2=(a*d-b*c)^2 := by ring
theorem lift_control : (1 : ℚ)*0+0*1=0 ∧ (1 : ℚ)-0=1 ∧ (1 : ℚ)*0+0*1=|1*0|+|0*1| := by norm_num

theorem complex_law (a b c d : ℚ) : (a*c-b*d)^2+(a*d+b*c)^2=(a^2+b^2)*(c^2+d^2) := by ring
theorem complex_control (N : ℕ) : 5*N≠1 := by omega

theorem average_law (a b : ℚ) : ((a+b)^2+(a-b)^2+2*(a^2+b^2))/4=a^2+b^2 := by ring
theorem average_control (a b : ℚ) : (a+b)^2-(a^2+b^2)=2*a*b := by ring

theorem gram_law (a b c d : ℚ) : (a*c+2*b*d)-(a*c+b*d)=b*d := by ring
theorem gram_control : ((0 : ℚ)^2+1^2)=1 ∧ ((0 : ℚ)^2+2*1^2)=2 := by norm_num

#print axioms chain_law
#print axioms chain_control
#print axioms kkt_law
#print axioms kkt_control
#print axioms edge_law
#print axioms edge_control
#print axioms gauge_law
#print axioms gauge_control
#print axioms observer_law
#print axioms observer_control
#print axioms quotient_law
#print axioms quotient_control
#print axioms replica_law
#print axioms replica_control
#print axioms window_law
#print axioms window_control
#print axioms mass_law
#print axioms mass_control
#print axioms circle_law
#print axioms circle_control
#print axioms gauss_law
#print axioms gauss_control
#print axioms time_law
#print axioms time_control
#print axioms hilbert_law
#print axioms hilbert_control
#print axioms dilation_law
#print axioms dilation_control
#print axioms gleason_law
#print axioms gleason_control
#print axioms tensor_law
#print axioms tensor_control
#print axioms lift_law
#print axioms lift_control
#print axioms complex_law
#print axioms complex_control
#print axioms average_law
#print axioms average_control
#print axioms gram_law
#print axioms gram_control
end QuantumMechanics.PromptL1Imports
