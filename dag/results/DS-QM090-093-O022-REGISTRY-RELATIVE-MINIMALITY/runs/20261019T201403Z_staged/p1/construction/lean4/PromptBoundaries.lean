import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Ext
import Mathlib.Data.ZMod.Basic
import Mathlib.Algebra.Order.Ring.Abs

/- All fields, norms, gates and finite groups are declared carriers. These
   statements neither supply physical imports nor authorize terminalization. -/
namespace QuantumMechanics.PromptBoundaries
def relativeMinimum (registry : List ℕ) (candidate : ℕ) : Prop :=
  candidate ∈ registry ∧ ∀ q ∈ registry,candidate≤q
theorem registry_scope : relativeMinimum [7] 7 ∧ ¬ relativeMinimum [5,7] 7 := by
  simp [relativeMinimum]
theorem registry_conjunction (a b c d : Bool) :
    (a && b && c && d)=true ↔ a=true ∧ b=true ∧ c=true ∧ d=true := by
  cases a <;> cases b <;> cases c <;> cases d <;> decide
theorem uniqueness_odd_cycle : ∀ a b c : Bool, ¬ (a≠b ∧ b≠c ∧ c≠a) := by decide
theorem spectator_recovery (p n : ℚ) (h : n≠0) : (p/n)*n=p := by field_simp
theorem cochain_telescope (a b c : ℚ) : (b-a)+(c-b)+(a-c)=0 := by ring
theorem cochain_gauge_pairing (a b d e f g r s : ℚ) (h : r^2+s^2=1) :
    (r^2*a-2*r*s*b+s^2*d)*(r^2*e-2*r*s*f+s^2*g)+
    2*(r*s*(a-d)+(r^2-s^2)*b)*(r*s*(e-g)+(r^2-s^2)*f)+
    (s^2*a+2*r*s*b+r^2*d)*(s^2*e+2*r*s*f+r^2*g)=a*e+2*b*f+d*g := by
  calc
    _ = (r^2+s^2)^2*(a*e+2*b*f+d*g) := by ring
    _ = _ := by rw [h]; ring
def survivalGate (i v s : Bool) : Bool := i && v && s
theorem survival_is_conditional (i v s : Bool) : survivalGate i v s=true ↔
    i=true ∧ v=true ∧ s=true := by cases i <;> cases v <;> cases s <;> decide
theorem survival_missing_seal : survivalGate true true false=false := rfl
theorem relative_orthogonal (a b : ℚ) : a*b*0=0 := by ring
theorem relative_off_bound (a b c v : ℚ) : |2*v*a*b*c|=|v|*(2*|a*b*c|) := by
  rw [show 2*v*a*b*c=v*(2*(a*b*c)) by ring]
  simp [abs_mul]
theorem threshold_queue (q la mu : ℕ) (h : la≤mu) : q+la-mu≤q := by omega
theorem threshold_gate (a b c d e : Bool) : (a && b && c && d && e)=true ↔
    a=true ∧ b=true ∧ c=true ∧ d=true ∧ e=true := by
  cases a <;> cases b <;> cases c <;> cases d <;> cases e <;> decide
theorem syndrome_distance (d : ℕ) (h : 0<d) : 2*((d-1)/2)<d := by omega
def weight3 (a b c : Bool) : ℕ := (if a then 1 else 0)+(if b then 1 else 0)+(if c then 1 else 0)
theorem syndrome_repetition3 : ∀ a b c : Bool,
    weight3 a b c≤1 → decide (1<weight3 a b c)=false := by decide
theorem syndrome_silent_logical :
    Bool.xor true true=false ∧ decide (1<weight3 true true true)=true := by decide
theorem packet_fields_are_not_validation : ¬ (∀ present valid : Prop,present→valid) := by
  intro h; exact h True False True.intro
theorem packet_zero_missing (a b c d : Bool) :
    ((if a then 0 else 1)+(if b then 0 else 1)+(if c then 0 else 1)+(if d then 0 else 1) : ℕ)=0 ↔
      a=true ∧ b=true ∧ c=true ∧ d=true := by
  cases a <;> cases b <;> cases c <;> cases d <;> decide

-- Q8 and the five-context witnesses are inserted below from declared finite
-- tables. Kernel checks verify their actual multiplication/parity equations.
def q8mul (a b : Fin 8) : Fin 8 :=
  match a.val,b.val with
  | 0,0 => 0
  | 0,1 => 1
  | 0,2 => 2
  | 0,3 => 3
  | 0,4 => 4
  | 0,5 => 5
  | 0,6 => 6
  | 0,7 => 7
  | 1,0 => 1
  | 1,1 => 4
  | 1,2 => 3
  | 1,3 => 6
  | 1,4 => 5
  | 1,5 => 0
  | 1,6 => 7
  | 1,7 => 2
  | 2,0 => 2
  | 2,1 => 7
  | 2,2 => 4
  | 2,3 => 1
  | 2,4 => 6
  | 2,5 => 3
  | 2,6 => 0
  | 2,7 => 5
  | 3,0 => 3
  | 3,1 => 2
  | 3,2 => 5
  | 3,3 => 4
  | 3,4 => 7
  | 3,5 => 6
  | 3,6 => 1
  | 3,7 => 0
  | 4,0 => 4
  | 4,1 => 5
  | 4,2 => 6
  | 4,3 => 7
  | 4,4 => 0
  | 4,5 => 1
  | 4,6 => 2
  | 4,7 => 3
  | 5,0 => 5
  | 5,1 => 0
  | 5,2 => 7
  | 5,3 => 2
  | 5,4 => 1
  | 5,5 => 4
  | 5,6 => 3
  | 5,7 => 6
  | 6,0 => 6
  | 6,1 => 3
  | 6,2 => 0
  | 6,3 => 5
  | 6,4 => 2
  | 6,5 => 7
  | 6,6 => 4
  | 6,7 => 1
  | 7,0 => 7
  | 7,1 => 6
  | 7,2 => 1
  | 7,3 => 0
  | 7,4 => 3
  | 7,5 => 2
  | 7,6 => 5
  | 7,7 => 4
  | _,_ => 0
def q8inv (a : Fin 8) : Fin 8 := if a.val%4=0 then a else ⟨(a.val+4)%8,Nat.mod_lt _ (by decide)⟩
theorem q8_associative : ∀ a b c : Fin 8,q8mul (q8mul a b) c=q8mul a (q8mul b c) := by decide
theorem q8_identity_inverse : ∀ a : Fin 8,q8mul 0 a=a ∧ q8mul a 0=a ∧ q8mul a (q8inv a)=0 ∧ q8mul (q8inv a) a=0 := by decide
theorem q8_pure_gauge : ∀ a b c : Fin 8,
    q8mul (q8mul (q8mul (q8inv a) b) (q8mul (q8inv b) c)) (q8mul (q8inv c) a)=0 := by decide
theorem q8_commutator : q8mul (q8mul (q8mul 1 2) (q8inv 1)) (q8inv 2)=4 := by decide
theorem parity_no_global : ∀ a b c d e f g h i : Fin 2,
    ¬ ((a.val+b.val+c.val)%2=0 ∧ (d.val+e.val+f.val)%2=0 ∧ (g.val+h.val+i.val)%2=0 ∧
      (a.val+d.val+g.val)%2=0 ∧ (b.val+e.val+h.val)%2=0 ∧ (c.val+f.val+i.val)%2=1) := by decide
def mpParity (n : ℕ) : ℕ :=
  (((n/1)%2+(n/2)%2+(n/4)%2)%2)*1+
  (((n/8)%2+(n/16)%2+(n/32)%2)%2)*2+
  (((n/64)%2+(n/128)%2+(n/256)%2)%2)*4+
  (((n/1)%2+(n/8)%2+(n/64)%2)%2)*8+
  (((n/2)%2+(n/16)%2+(n/128)%2)%2)*16+
  (((n/4)%2+(n/32)%2+(n/256)%2)%2)*32
def mpSelected (mask : ℕ) (n : Fin 512) : Bool := decide (Nat.land (Nat.xor (mpParity n.val) 32) mask=0)
def droppedWitness (o : Fin 6) : Fin 512 :=
  match o.val with
  | 0 => 4
  | 1 => 13
  | 2 => 69
  | 3 => 5
  | 4 => 6
  | 5 => 0
  | _ => 0
theorem parity_every_drop : ∀ o : Fin 6,mpSelected (63-2^o.val) (droppedWitness o)=true := by decide


theorem born_pair_normalization (A B : ℚ) (h : A+B≠0) : A/(A+B)+B/(A+B)=1 := by
  field_simp
  <;> ring
theorem born_norm_rotation (a b r s : ℚ) (h : r^2+s^2=1) :
    (r*a-s*b)^2+(s*a+r*b)^2=a^2+b^2 := by
  calc
    _ = (r^2+s^2)*(a^2+b^2) := by ring
    _ = _ := by rw [h]; ring
theorem born_quartic_divergence : (3/5:ℚ)^2≠(3/5:ℚ)^4/((3/5:ℚ)^4+(4/5:ℚ)^4) := by norm_num
theorem synthesis_hom (a b : ZMod 4) : 2*(a+b)=2*a+2*b := by ring
theorem synthesis_nonfaithful : (2*(0:ZMod 4)=2*2) ∧ (0:ZMod 4)≠2 := by decide
theorem synthesis_nonfull : ∀ k : ZMod 4,2*k≠1 := by decide
theorem cascade_mass_gap (a b : ℚ) : (a^2+b^2)^2-(a^4+b^4)=2*a^2*b^2 := by ring
theorem cascade_cross (a b : ℚ) : (a+b)^2-a^2-b^2=2*a*b := by ring

@[ext] structure Mat2 where
  a : ℚ
  b : ℚ
  c : ℚ
  d : ℚ
  deriving DecidableEq
def Mat2.mul (A B : Mat2) : Mat2 :=
  ⟨A.a*B.a+A.b*B.c,A.a*B.b+A.b*B.d,A.c*B.a+A.d*B.c,A.c*B.b+A.d*B.d⟩
def Mat2.add (A B : Mat2) : Mat2 := ⟨A.a+B.a,A.b+B.b,A.c+B.c,A.d+B.d⟩
def Mat2.transpose (A : Mat2) : Mat2 := ⟨A.a,A.c,A.b,A.d⟩
def Mat2.det (A : Mat2) : ℚ := A.a*A.d-A.b*A.c
def Mat2.trace (A : Mat2) : ℚ := A.a+A.d
def Mat2.quad (A : Mat2) (x y : ℚ) : ℚ := A.a*x*x+(A.b+A.c)*x*y+A.d*y*y
theorem majorana_clifford (a b : ℚ) :
    Mat2.mul ⟨a,0,0,-a⟩ ⟨a,0,0,-a⟩=⟨a^2,0,0,a^2⟩ ∧
    Mat2.mul ⟨0,b,b,0⟩ ⟨0,b,b,0⟩=⟨b^2,0,0,b^2⟩ ∧
    Mat2.add (Mat2.mul ⟨a,0,0,-a⟩ ⟨0,b,b,0⟩) (Mat2.mul ⟨0,b,b,0⟩ ⟨a,0,0,-a⟩)=⟨0,0,0,0⟩ ∧
    Mat2.mul ⟨0,a*b,-(a*b),0⟩ ⟨0,a*b,-(a*b),0⟩=⟨-(a*b)^2,0,0,-(a*b)^2⟩ := by
  constructor
  · ext <;> simp [Mat2.mul] <;> ring
  constructor
  · ext <;> simp [Mat2.mul] <;> ring
  constructor <;> ext <;> simp [Mat2.add,Mat2.mul] <;> ring
theorem majorana_scaled_braid (c : ℚ) :
    Mat2.mul ⟨1,c,-c,1⟩ ⟨1,c,-c,1⟩=⟨1-c^2,2*c,-2*c,1-c^2⟩ := by
  ext <;> simp [Mat2.mul] <;> ring
theorem busch_roundtrip (a b c d : ℚ) :
    3*((a+d+2*b)/6-(a+d-2*b)/6)/2=b ∧
    3*((a+d+2*c)/6-(a+d-2*c)/6)/2=c ∧
    (a+d+3*(a/3-d/3))/2=a ∧ (a+d-3*(a/3-d/3))/2=d := by
  constructor
  · ring
  constructor
  · ring
  constructor <;> ring
theorem busch_finite_probes_not_psd :
    (0≤(1+2*(1/2:ℚ))/6 ∧ 0≤(1-2*(1/2:ℚ))/6) ∧
    (1/2:ℚ)*(1/2)-(1/2)^2-(1/2)^2<0 ∧
    (1/2:ℚ)+2*(1/2)-2*(1/2)-2*(1/2)<0 := by norm_num
theorem choi_eigenvalue_interval (p : ℚ) :
    (0≤(1+3*p)/2 ∧ 0≤(1-p)/2) ↔ (-1/3≤p ∧ p≤1) := by constructor <;> rintro ⟨h0,h1⟩ <;> constructor <;> linarith
theorem choi_trace (p : ℚ) : (1+3*p)/2+3*((1-p)/2)=2 := by ring

structure Proxy where
  localParams : ℕ
  joint : ℕ
  i3 : ℚ
  A : Mat2
  B : Mat2
  rho : Mat2
  clock : Mat2
def proxyFor (k : Fin 5) : Proxy :=
  { localParams := if k.val=0 then 8 else 15
    joint := if k.val=0 then 9 else 15
    i3 := if k.val=1 then 3^4-3*2^4+3 else 3^2-3*2^2+3
    A := if k.val=2 then ⟨1,0,0,-1⟩ else ⟨0,1,1,0⟩
    B := if k.val=2 then ⟨2,0,0,3⟩ else ⟨1,0,0,-1⟩
    rho := if k.val=3 then ⟨1/2,3/4,3/4,1/2⟩ else ⟨1/2,0,0,1/2⟩
    clock := if k.val=4 then ⟨1,0,0,0⟩ else ⟨0,-1,1,0⟩ }
def proxyAdmits (m : Proxy) (i : Fin 5) : Prop :=
  match i.val with
  | 0 => m.localParams=m.joint
  | 1 => m.i3=0
  | 2 => Mat2.mul m.A m.B≠Mat2.mul m.B m.A
  | 3 => Mat2.trace m.rho=1 ∧ 0≤Mat2.quad m.rho 1 0 ∧ 0≤Mat2.quad m.rho 0 1 ∧ 0≤Mat2.quad m.rho 1 (-1)
  | _ => Mat2.mul (Mat2.transpose m.clock) m.clock=⟨1,0,0,1⟩ ∧ Mat2.det m.clock=1
instance (m : Proxy) (i : Fin 5) : Decidable (proxyAdmits m i) := by
  unfold proxyAdmits; split <;> infer_instance
theorem proxy_separation : ∀ k i : Fin 5,proxyAdmits (proxyFor k) i ↔ k≠i := by decide
theorem proxy_three_rays_incomplete :
    Mat2.quad ⟨1/2,-3/4,-3/4,1/2⟩ 1 0≥0 ∧
    Mat2.quad ⟨1/2,-3/4,-3/4,1/2⟩ 0 1≥0 ∧
    Mat2.quad ⟨1/2,-3/4,-3/4,1/2⟩ 1 (-1)≥0 ∧
    Mat2.quad ⟨1/2,-3/4,-3/4,1/2⟩ 1 1<0 := by norm_num [Mat2.quad]
theorem maps_completed_square (z : ℚ) : z^2-(27/8)*z=(z-27/16)^2-729/256 := by ring
theorem maps_polynomial_bound (z : ℚ) : -729/256≤z^2-(27/8)*z := by
  rw [maps_completed_square]; linarith [sq_nonneg (z-27/16)]
theorem maps_virial : 2*(27/16:ℚ)^2+(-4*(27/16)+(5/8)*(27/16))=0 := by norm_num
theorem tensor_no_dump_action : ¬ ∃ F : ℚ→ℚ,∀ c d : ℚ,F (c+d)=c-d := by
  rintro ⟨F,h⟩
  have a := h 1 0
  have b := h 0 1
  norm_num at a b
  linarith
theorem tensor_kronecker_expansion (a b c d : ℚ) :
    a*c+a*d=a*(c+d) ∧ b*c+b*d=b*(c+d) := by constructor <;> ring
theorem torsion_gauge_cycles {n : ℕ} (a b c d e g0 g1 g2 g3 : ZMod n) :
    (a+g1-g0)+(b+g2-g1)+(c+g3-g2)+(d+g0-g3)=a+b+c+d ∧
    (e+g2-g0)-(a+g1-g0)-(b+g2-g1)=e-a-b := by constructor <;> ring
theorem torsion_pair_card (n : ℕ) : Fintype.card (Fin n × Fin n)=n*n := by simp
theorem torsion_shadow_is_finite_algebra :
    (∀ k : Fin 2,(2*k.val)%2=0) ∧ (2*1)%3≠0 ∧ (2*1)%4≠0 := by decide
end QuantumMechanics.PromptBoundaries

#print axioms QuantumMechanics.PromptBoundaries.registry_scope
#print axioms QuantumMechanics.PromptBoundaries.registry_conjunction
#print axioms QuantumMechanics.PromptBoundaries.uniqueness_odd_cycle
#print axioms QuantumMechanics.PromptBoundaries.spectator_recovery
#print axioms QuantumMechanics.PromptBoundaries.cochain_telescope
#print axioms QuantumMechanics.PromptBoundaries.cochain_gauge_pairing
#print axioms QuantumMechanics.PromptBoundaries.survival_is_conditional
#print axioms QuantumMechanics.PromptBoundaries.survival_missing_seal
#print axioms QuantumMechanics.PromptBoundaries.relative_orthogonal
#print axioms QuantumMechanics.PromptBoundaries.relative_off_bound
#print axioms QuantumMechanics.PromptBoundaries.threshold_queue
#print axioms QuantumMechanics.PromptBoundaries.threshold_gate
#print axioms QuantumMechanics.PromptBoundaries.syndrome_distance
#print axioms QuantumMechanics.PromptBoundaries.syndrome_repetition3
#print axioms QuantumMechanics.PromptBoundaries.syndrome_silent_logical
#print axioms QuantumMechanics.PromptBoundaries.packet_fields_are_not_validation
#print axioms QuantumMechanics.PromptBoundaries.packet_zero_missing
#print axioms QuantumMechanics.PromptBoundaries.q8_associative
#print axioms QuantumMechanics.PromptBoundaries.q8_identity_inverse
#print axioms QuantumMechanics.PromptBoundaries.q8_pure_gauge
#print axioms QuantumMechanics.PromptBoundaries.q8_commutator
#print axioms QuantumMechanics.PromptBoundaries.parity_no_global
#print axioms QuantumMechanics.PromptBoundaries.parity_every_drop
#print axioms QuantumMechanics.PromptBoundaries.born_pair_normalization
#print axioms QuantumMechanics.PromptBoundaries.born_norm_rotation
#print axioms QuantumMechanics.PromptBoundaries.born_quartic_divergence
#print axioms QuantumMechanics.PromptBoundaries.synthesis_hom
#print axioms QuantumMechanics.PromptBoundaries.synthesis_nonfaithful
#print axioms QuantumMechanics.PromptBoundaries.synthesis_nonfull
#print axioms QuantumMechanics.PromptBoundaries.cascade_mass_gap
#print axioms QuantumMechanics.PromptBoundaries.cascade_cross
#print axioms QuantumMechanics.PromptBoundaries.majorana_clifford
#print axioms QuantumMechanics.PromptBoundaries.majorana_scaled_braid
#print axioms QuantumMechanics.PromptBoundaries.busch_roundtrip
#print axioms QuantumMechanics.PromptBoundaries.busch_finite_probes_not_psd
#print axioms QuantumMechanics.PromptBoundaries.choi_eigenvalue_interval
#print axioms QuantumMechanics.PromptBoundaries.choi_trace
#print axioms QuantumMechanics.PromptBoundaries.proxy_separation
#print axioms QuantumMechanics.PromptBoundaries.proxy_three_rays_incomplete
#print axioms QuantumMechanics.PromptBoundaries.maps_completed_square
#print axioms QuantumMechanics.PromptBoundaries.maps_polynomial_bound
#print axioms QuantumMechanics.PromptBoundaries.maps_virial
#print axioms QuantumMechanics.PromptBoundaries.tensor_no_dump_action
#print axioms QuantumMechanics.PromptBoundaries.tensor_kronecker_expansion
#print axioms QuantumMechanics.PromptBoundaries.torsion_gauge_cycles
#print axioms QuantumMechanics.PromptBoundaries.torsion_pair_card
#print axioms QuantumMechanics.PromptBoundaries.torsion_shadow_is_finite_algebra
