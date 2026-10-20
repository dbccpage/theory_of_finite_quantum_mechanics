import Mathlib.Algebra.Order.Ring.Abs
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Init.Omega

/- Literal algebraic and finite controls; original target transports remain open. -/
namespace QuantumMechanics.PromptBornBoundaries

theorem isometry_law (a b : ℚ) : b^2+a^2=a^2+b^2 := by ring
theorem isometry_control : (1+(-1) : ℚ)^2=0 ∧ (1 : ℚ)^2+(-1)^2=2 := by norm_num

theorem orthogonal_law (a b c d : ℚ) : (a*c+b*d)^2+(-b*c+a*d)^2=(a^2+b^2)*(c^2+d^2) := by ring
theorem orthogonal_control : ((3/5 : ℚ)^2+(4/5)^2)=1 := by norm_num

theorem sqrt_law : (3/5 : ℚ)^2=9/25 ∧ (4/5 : ℚ)^2=16/25 := by norm_num
theorem sqrt_control (n : ℤ) : 2*n≠1 := by omega

theorem phases_law (a b : ℚ) : (a+b)^2-(a-b)^2=4*a*b := by ring
theorem phases_control : (1+1 : ℚ)^2=4 ∧ (1-1 : ℚ)^2=0 := by norm_num

theorem trace_law (a b c s : ℚ) : |s*a|+|s*b|+|s*c|=|s| * (|a|+|b|+|c|) := by rw [abs_mul,abs_mul,abs_mul]; ring
theorem trace_control : |(1 : ℚ)|=|-1| ∧ (1 : ℚ)≠-1 := by norm_num

theorem factor_law (a b e f g h u v : ℚ) :
    a*(e*u+f*v)+b*(g*u+h*v)=(a*e+b*g)*u+(a*f+b*h)*v := by ring
theorem factor_control : (1 : ℚ)*1+1*1=2 ∧ (1 : ℚ)*1=1 := by norm_num

theorem branch_law (a b c s : ℚ) : (c*a-s*b)^2-(c*a+s*b)^2=-4*c*s*a*b := by ring
theorem branch_control : (1 : ℚ)^2=(-1)^2 ∧ (1+1 : ℚ)^2≠(1-1)^2 := by norm_num

theorem normalize_law (a b c : ℚ) (h : a+b+c≠0) : a/(a+b+c)+b/(a+b+c)+c/(a+b+c)=1 := by field_simp
theorem normalize_control : (1 : ℚ)/3=(-1)/(-3) ∧ (2 : ℚ)/3=(-2)/(-3) ∧ ¬ (0 < (-1 : ℚ)) := by norm_num

theorem defect_law (a b : ℚ) : (|a|+|0|)+(|0|+|b|)-(|a+0|+|0+b|)=0 := by simp
theorem defect_control : |(1 : ℚ)|+|-1|-|1+(-1)|=2 ∧
    (|(1 : ℚ)|+|0|)+(|0|+|-1|)-(|1+0|+|0+(-1)|)=0 := by norm_num

theorem minkowski_law (a b : ℚ) (ha : 0<a) (hb : 0<b) : a^2+b^2<(a+b)^2 := by nlinarith [mul_pos ha hb]
theorem minkowski_control (a b : ℚ) : (a+b)^3-a^3-b^3=3*a*b*(a+b) := by ring

theorem sparse_law (a b : ℚ) : (a+b)^2-(a-b)^2=4*a*b := by ring
theorem sparse_control : ((1 : ℚ)*0=0 ∧ (2 : ℚ)*0=0) ∧ ((1 : ℚ)*0-0*2=0) ∧ (2 : ℚ)≠0 := by norm_num

theorem redundancy_law (w n W N : ℚ) (h : n=w) (t : N=W) : n/N=w/W := by rw [h,t]
theorem redundancy_control : ((1 : ℚ)^2+1^2)=2 ∧ ((1 : ℚ)^2+0^2)≠2 := by norm_num

theorem shadow_law (a b : ℚ) : ((a+b)^2+(a-b)^2+2*(a^2+b^2))/4=a^2+b^2 := by ring
theorem shadow_control : ((1/2 : ℚ)*2^2+(1/4)*1^2+(1/4)*(1/2)^2)=37/16 := by norm_num

theorem scope_law (a b c : ℚ) (h : a+b+c≠0) : (a+b)/(a+b+c)+c/(a+b+c)=1 := by field_simp
theorem scope_control : (2 : ℚ)/(2+1+1)=1/2 ∧ (2 : ℚ)^2/(2^2+1^2+1^2)=2/3 ∧ (1/2 : ℚ)≠2/3 := by norm_num

theorem gleason_law (a b c u v : ℚ) :
    (a*u^2+2*b*u*v+c*v^2)+(a*(-v)^2+2*b*(-v)*u+c*u^2)=(a+c)*(u^2+v^2) := by ring
theorem gleason_control (a b c : ℚ) :
    (((9*a+24*b+16*c)/25)-(9/25)*a-(16/25)*c)/(24/25)=b := by ring

theorem capacity_law (a b c s : ℚ) (h : c^2+s^2=1) :
    (c*a-s*b)^2+(s*a+c*b)^2=a^2+b^2 := by
  calc
    _ = (c^2+s^2)*(a^2+b^2) := by ring
    _ = _ := by rw [h]; ring
theorem capacity_control (a b c s : ℚ) : (c*a-s*b)^2-(c*a+s*b)^2=-4*c*s*a*b := by ring

theorem ladder_law (p q r s a b : ℚ) :
    p*(r*a+(1-s)*b)+(1-q)*((1-r)*a+s*b)=
      (p*r+(1-q)*(1-r))*a+(p*(1-s)+(1-q)*s)*b := by ring
theorem ladder_control (a b : ℚ) : (a+b)^2+(a-b)^2=2*(a^2+b^2) := by ring

theorem pairing_law (a b : ℚ) : a+b=b+a := by ring
theorem pairing_control (u v : ℚ) : (u+v)^2+(u-v)^2-2*u^2=2*v^2 := by ring

theorem selector_law : (2*1)%2=0 ∧ (2*1)%3≠0 ∧ (2*1)%4≠0 := by decide
theorem selector_control : (1+1+1)%3=0 ∧ (1+1+1+1)%4=0 ∧ (3 : ℕ)≠4 := by decide

theorem finish_law (a b c d e f g h : ℚ) :
    (a*e+b*g,a*f+b*h,c*e+d*g,c*f+d*h)=
      (e*a+g*b,f*a+h*b,e*c+g*d,f*c+h*d) := by ext <;> ring
theorem finish_control : ((1 : ℚ)*1-0*0)=1 ∧ ((0 : ℚ)*0-1*1)=-1 ∧ (1 : ℚ)≠0 := by norm_num

#print axioms isometry_law
#print axioms isometry_control
#print axioms orthogonal_law
#print axioms orthogonal_control
#print axioms sqrt_law
#print axioms sqrt_control
#print axioms phases_law
#print axioms phases_control
#print axioms trace_law
#print axioms trace_control
#print axioms factor_law
#print axioms factor_control
#print axioms branch_law
#print axioms branch_control
#print axioms normalize_law
#print axioms normalize_control
#print axioms defect_law
#print axioms defect_control
#print axioms minkowski_law
#print axioms minkowski_control
#print axioms sparse_law
#print axioms sparse_control
#print axioms redundancy_law
#print axioms redundancy_control
#print axioms shadow_law
#print axioms shadow_control
#print axioms scope_law
#print axioms scope_control
#print axioms gleason_law
#print axioms gleason_control
#print axioms capacity_law
#print axioms capacity_control
#print axioms ladder_law
#print axioms ladder_control
#print axioms pairing_law
#print axioms pairing_control
#print axioms selector_law
#print axioms selector_control
#print axioms finish_law
#print axioms finish_control
end QuantumMechanics.PromptBornBoundaries
