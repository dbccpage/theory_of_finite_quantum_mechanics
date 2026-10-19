import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Fintype.Pi
import WeylCommutant
import LggrFiniteResults

/- Literal finite/algebraic interfaces only. Native array interpretation and
   original target transports are separately recorded obligations. -/
namespace QuantumMechanics.PromptGenesisImplementation

theorem weyl_scalar {K : Type} [Lean.Grind.Field K] {n : Nat}
    (A : Fin (n+1) → Fin (n+1) → K) (e : Fin (n+1) → K)
    (distinct : ∀ i j, e i=e j → i=j)
    (clock : ∀ i j, e i*A i j=A i j*e j)
    (shift : ∀ i : Fin n,A i.succ i.succ=A i.castSucc i.castSucc) :
    ∀ i j,A i j=if i=j then A 0 0 else 0 :=
  FiniteQm.WeylCommutant.clock_shift_commutant_scalar A e distinct clock shift

def cyclMul (z w : ℚ × ℚ) : ℚ × ℚ :=
  (z.1*w.1-z.2*w.2,z.1*w.2+z.2*w.1-z.2*w.2)

theorem weyl_cubic_root : cyclMul (cyclMul (0,1) (0,1)) (0,1)=(1,0) ∧
    ((0,1) : ℚ × ℚ)≠(1,0) := by norm_num [cyclMul]

theorem duality_positive_witness (a b : ℚ) (ha : 0≤a) (hb : 0≤b) :
    a+b=|a|+|b| := by rw [abs_of_nonneg ha,abs_of_nonneg hb]

theorem duality_triangle (a b : ℚ) : |a+b|≤|a|+|b| := abs_add_le a b

def firstSep (hasForm hasInstance uniform : Bool) : Bool := hasForm && hasInstance && !uniform

theorem separation_needs_two : ∀ f i u : Bool,firstSep f i u=true → f=true ∧ i=true := by decide

theorem separation_unary_tie : firstSep true true false=true ∧ firstSep true false true=false := by decide

theorem distinct_irreflexive {T : Type} (R : T→T→Prop) (h : ∀ x,¬ R x x)
    (a b : T) (hab : R a b) : a≠b := by rintro rfl; exact h a hab

theorem distinct_two_readings :
    (false≠true ∧ true≠false) ∧ ¬ (true=false ∧ false=true) := by decide

theorem noreturn_strict (a b c : Nat) (h : a<b) (h' : b≤c) : c≠a := by omega

theorem noreturn_cycle (a b : Nat) (h : a≤b) (h' : b≤a) : a=b := by omega

theorem fewest_edit_identity (kept lost added fresh : Nat) :
    (kept+added+fresh)+2*lost=(kept+lost)+(lost+added+fresh) := by omega

theorem fewest_lower_bound (size lost base steps : Nat)
    (h : size+2*lost≤base+steps) : size+2*lost-base≤steps := by omega

theorem obstruction_loop {T : Type} (R : T→T→Prop) (x : T) :
    ¬ (∀ a,¬ (R a a ∨ a=x)) := by intro h; exact h x (Or.inr rfl)

theorem obstruction_two_directions : ∀ a b : Bool,
    (!(a||b))=true ↔ a=false ∧ b=false := by decide

def replay {S A : Type} (step : S→A→S) : List (Option A)→S→S
  | [],s => s
  | none::h,s => replay step h s
  | some a::h,s => replay step h (step s a)

theorem events_append {S A : Type} (step : S→A→S) (h k : List (Option A)) (s : S) :
    replay step (h++k) s=replay step k (replay step h s) := by
  induction h generalizing s with
  | nil => rfl
  | cons e h ih => cases e <;> simp [replay,ih]

theorem events_admission (s a : Nat) : replay (fun s a : Nat => s+a) [some a] s=s+a := rfl

def merge (u v x : Nat) : Nat := if x=v then u else x

theorem rename_merge (f : Nat→Nat) (hf : Function.Injective f) (u v x : Nat) :
    f (merge u v x)=merge (f u) (f v) (f x) := by
  by_cases h : x=v
  · subst x; simp [merge]
  · have h' : f x≠f v := fun e => h (hf e)
    simp [merge,h,h']

theorem rename_composition (f g : Nat→Nat) (x : Nat) : (g∘f) x=g (f x) := rfl

theorem sameness_paired_addition (r s : Int) : (r+1)-(s+1)=r-s := by ring

theorem sameness_cancel_cost (r s : Nat) : r+s=(r-s)+(s-r)+2*min r s := by omega

theorem erasure_filter {S A : Type} (step : S→A→S) (h : List (Option A)) (s : S) :
    replay step h s=(h.filterMap id).foldl step s := by
  induction h generalizing s with
  | nil => rfl
  | cons e h ih => cases e <;> simp [replay,ih]

theorem erasure_supply_prefix {S A : Type} (step : S→A→S) (h : List (Option A)) (s : S) :
    replay step (none::h) s=replay step h s := rfl

theorem supply_noop {S A : Type} (step : S→A→S) (s : S) : replay step [none] s=s := rfl

theorem supply_not_admission : replay (fun s a : Nat => s+a) [none] 0≠
    replay (fun s a : Nat => s+a) [some 1] 0 := by decide

def stageEligible (stage node : Nat) : Bool := decide (0<stage ∨ node=0)

theorem mss0_only_inscription (node : Nat) : stageEligible 0 node=true ↔ node=0 := by simp [stageEligible]

theorem mss0_structural_ceiling : ∀ admitted : Bool, (admitted && false)=false := by decide

def roundedAt53 (k : Nat) : Nat :=
  (k/2+if k%2=1 ∧ (k/2)%2=1 then 1 else 0)*2

theorem float_exact_distinct : (2^53+1 : Nat)≠2^53 := by omega

theorem float_declared_round_collision : roundedAt53 (2^53+1)=roundedAt53 (2^53) := by decide

theorem pairing_off_diagonal (a b d u v : ℚ) :
    (a*u^2+2*b*u*v+d*v^2)-(a*u^2+d*v^2)=2*b*u*v := by ring

theorem pairing_nonlinear_negative : 2*(1/4:ℚ)^2-1/4<0 := by norm_num

theorem realify_product (a b c d : ℚ) :
    (a*c-b*d,a*d+b*c)=((a*c+(-b)*d),(b*c+a*d)) := by congr 1 <;> ring

theorem realify_balanced (a b c d : ℚ) :
    (-b*c-a*d,-b*d+a*c)=(-a*d-b*c,a*c-b*d) := by congr 1 <;> ring

theorem amplitude_gauge_cycle (a b c g0 g1 g2 : Int) :
    (a+g1-g0)+(b+g2-g1)+(c+g0-g2)=a+b+c := by ring

theorem amplitude_norm_mul (a b c d : ℚ) :
    (a*c-b*d)^2+(a*d+b*c)^2=(a^2+b^2)*(c^2+d^2) := by ring

def modGaussMul (z w : ZMod 5 × ZMod 5) : ZMod 5 × ZMod 5 :=
  (z.1*w.1-z.2*w.2,z.1*w.2+z.2*w.1)

def residuePower : Nat→(ZMod 5 × ZMod 5)
  | 0 => (1,0)
  | n+1 => modGaussMul (residuePower n) (3,4)

theorem amplitude_residue_all (n : Nat) : residuePower (n+1)=(3,4) := by
  induction n with
  | zero => decide
  | succ n ih => rw [residuePower,ih]; decide

theorem normal_cycle_switch : ∀ a b c x y z : Bool,
    xor (xor (xor (xor a x) y) (xor (xor b y) z)) (xor (xor c z) x)=xor (xor a b) c := by decide

theorem normal_form_count (b : Nat) : Fintype.card (Fin b→Bool)=2^b := by simp

theorem lggr_gate_equivalence (n : Nat) (hn : 0<n) (b : Nat→Bool) (M : Nat) :
    LggrFiniteResults.lggrCycleGateAdmits n b M=true ↔
      (M=0 ∨ ∃ g,LggrFiniteResults.IsSection n b g) :=
  LggrFiniteResults.lggrCycleGateAdmits_iff_section_or_zero_mass n hn b M

theorem lggr_triangle_attainment : 6*(1/6:ℚ)=1 ∧ 4*(1/6:ℚ)=2/3 := by norm_num

theorem thymus_count_zero {U : Type} (d : U→Bool) (panel : List U)
    (h : ∀ x∈panel,d x=false) : (panel.filter d).length=0 := by
  induction panel with
  | nil => rfl
  | cons a panel ih =>
    have ha := h a (by simp)
    have hp : ∀ x∈panel,d x=false := fun x hx => h x (by simp [hx])
    simp [ha,ih hp]

theorem thymus_changed_execution : (false=false) ∧ (true=true) ∧ false≠true := by decide

end QuantumMechanics.PromptGenesisImplementation

#print axioms QuantumMechanics.PromptGenesisImplementation.weyl_scalar
#print axioms QuantumMechanics.PromptGenesisImplementation.weyl_cubic_root
#print axioms QuantumMechanics.PromptGenesisImplementation.duality_positive_witness
#print axioms QuantumMechanics.PromptGenesisImplementation.duality_triangle
#print axioms QuantumMechanics.PromptGenesisImplementation.separation_needs_two
#print axioms QuantumMechanics.PromptGenesisImplementation.separation_unary_tie
#print axioms QuantumMechanics.PromptGenesisImplementation.distinct_irreflexive
#print axioms QuantumMechanics.PromptGenesisImplementation.distinct_two_readings
#print axioms QuantumMechanics.PromptGenesisImplementation.noreturn_strict
#print axioms QuantumMechanics.PromptGenesisImplementation.noreturn_cycle
#print axioms QuantumMechanics.PromptGenesisImplementation.fewest_edit_identity
#print axioms QuantumMechanics.PromptGenesisImplementation.fewest_lower_bound
#print axioms QuantumMechanics.PromptGenesisImplementation.obstruction_loop
#print axioms QuantumMechanics.PromptGenesisImplementation.obstruction_two_directions
#print axioms QuantumMechanics.PromptGenesisImplementation.events_append
#print axioms QuantumMechanics.PromptGenesisImplementation.events_admission
#print axioms QuantumMechanics.PromptGenesisImplementation.rename_merge
#print axioms QuantumMechanics.PromptGenesisImplementation.rename_composition
#print axioms QuantumMechanics.PromptGenesisImplementation.sameness_paired_addition
#print axioms QuantumMechanics.PromptGenesisImplementation.sameness_cancel_cost
#print axioms QuantumMechanics.PromptGenesisImplementation.erasure_filter
#print axioms QuantumMechanics.PromptGenesisImplementation.erasure_supply_prefix
#print axioms QuantumMechanics.PromptGenesisImplementation.supply_noop
#print axioms QuantumMechanics.PromptGenesisImplementation.supply_not_admission
#print axioms QuantumMechanics.PromptGenesisImplementation.mss0_only_inscription
#print axioms QuantumMechanics.PromptGenesisImplementation.mss0_structural_ceiling
#print axioms QuantumMechanics.PromptGenesisImplementation.float_exact_distinct
#print axioms QuantumMechanics.PromptGenesisImplementation.float_declared_round_collision
#print axioms QuantumMechanics.PromptGenesisImplementation.pairing_off_diagonal
#print axioms QuantumMechanics.PromptGenesisImplementation.pairing_nonlinear_negative
#print axioms QuantumMechanics.PromptGenesisImplementation.realify_product
#print axioms QuantumMechanics.PromptGenesisImplementation.realify_balanced
#print axioms QuantumMechanics.PromptGenesisImplementation.amplitude_gauge_cycle
#print axioms QuantumMechanics.PromptGenesisImplementation.amplitude_norm_mul
#print axioms QuantumMechanics.PromptGenesisImplementation.amplitude_residue_all
#print axioms QuantumMechanics.PromptGenesisImplementation.normal_cycle_switch
#print axioms QuantumMechanics.PromptGenesisImplementation.normal_form_count
#print axioms QuantumMechanics.PromptGenesisImplementation.lggr_gate_equivalence
#print axioms QuantumMechanics.PromptGenesisImplementation.lggr_triangle_attainment
#print axioms QuantumMechanics.PromptGenesisImplementation.thymus_count_zero
#print axioms QuantumMechanics.PromptGenesisImplementation.thymus_changed_execution
