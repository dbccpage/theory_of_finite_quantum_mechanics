import WitnessedDifference.RootGaugeNormalization
import WitnessedDifference.Source25PairTransport

/-!
# Actual marked diagnostics and carrier-changing non-descent

Use the existing source-25 partial step's raw natural tables, cyclic triple
normalization and fiber aggregation. Prove fixed-mark gradient classification
and diagnostic descent at arbitrary integer magnitude. The explicit source
add-term and identify countermodels start with raising-equivalent raw states
and produce different balance answers after the same legal source operation.
Concrete programs, orbit minima and storage are separate differential evidence.
-/
namespace WitnessedDifference.MarkedGaugeTransport
abbrev Triple := Source25PairTransport.Triple
abbrev Table := Nat → Nat → Int

def diagnostic (e : Table) (t : Triple) : Int :=
  e t.1 t.2.1 + e t.2.1 t.2.2 + e t.2.2 t.1

theorem cyclic_diagnostic (e : Table) (x y z : Nat) :
    diagnostic e (Source25PairTransport.wayRound x y z) = diagnostic e (x,y,z) := by
  by_cases first : x<y ∧ x<z
  · simp [Source25PairTransport.wayRound,diagnostic,first]
  · by_cases second : y<z <;>
      simp [Source25PairTransport.wayRound,diagnostic,first,second] <;> omega

theorem diagnostic_after_shift (e : Table) (g : Nat → Int) (t : Triple) :
    diagnostic (RootGaugeNormalization.shifted e g) t = diagnostic e t := by
  unfold diagnostic RootGaugeNormalization.shifted
  omega

theorem diagnostic_after_normal (e : Table) (root : Nat) (t : Triple) :
    diagnostic (RootGaugeNormalization.normal root e) t = diagnostic e t :=
  RootGaugeNormalization.normal_preserves_round_sums root e t.1 t.2.1 t.2.2

def renameTriple (f : Nat → Nat) (t : Triple) :=
  Source25PairTransport.wayRound (f t.1) (f t.2.1) (f t.2.2)

theorem diagnostic_pullback_rename (e : Table) (f : Nat → Nat) (t : Triple) :
    diagnostic (RootGaugeNormalization.pullback f e) t = diagnostic e (renameTriple f t) := by
  rw [renameTriple,cyclic_diagnostic]
  rfl

def balanceRecord (e : Table) (filled : List Triple) : List (Triple × Bool) :=
  filled.map (fun t => (t,decide (diagnostic e t = 0)))

theorem balance_record_after_shift (e : Table) (g : Nat → Int) (filled : List Triple) :
    balanceRecord (RootGaugeNormalization.shifted e g) filled = balanceRecord e filled := by
  simp only [balanceRecord,diagnostic_after_shift]

theorem balance_record_after_normal (e : Table) (root : Nat) (filled : List Triple) :
    balanceRecord (RootGaugeNormalization.normal root e) filled = balanceRecord e filled := by
  simp only [balanceRecord,diagnostic_after_normal]

def SameFixed (n : Nat) (e f : Table) (filled targetFilled : List Triple) : Prop :=
  filled=targetFilled ∧ ∀ x y, x<n → y<n → RootGaugeNormalization.normal 0 e x y = RootGaugeNormalization.normal 0 f x y

theorem same_fixed_iff_gradient (n : Nat) (e f : Table) (filled targetFilled : List Triple) :
    SameFixed n e f filled targetFilled ↔
      filled=targetFilled ∧ ∃ g : Nat → Int, ∀ x y, x<n → y<n → f x y=e x y+g x-g y := by
  constructor
  · rintro ⟨marks,same⟩
    refine ⟨marks,fun x => RootGaugeNormalization.potential 0 f x-RootGaugeNormalization.potential 0 e x,?_⟩
    intro x y hx hy
    have h := same x y hx hy
    simp only [RootGaugeNormalization.normal] at h
    dsimp
    omega
  · rintro ⟨marks,g,hg⟩
    refine ⟨marks,?_⟩
    intro x y hx hy
    have hn : 0<n := by omega
    have hp : ∀ a, a<n → RootGaugeNormalization.potential 0 f a=RootGaugeNormalization.potential 0 e a+g a-g 0 := by
      intro a ha
      by_cases same : a=0
      · subst a; simp [RootGaugeNormalization.potential]
      · simp only [RootGaugeNormalization.potential,if_neg same]
        exact hg a 0 ha hn
    simp only [RootGaugeNormalization.normal]
    rw [hp x hx,hp y hy,hg x y hx hy]
    omega

def excess (state : Source25PairTransport.State) : Table :=
  fun x y => (state.r x y : Int)-(state.s x y : Int)
def zeroState (n : Nat) (filled : List Triple) : Source25PairTransport.State :=
  {n:=n,r:=fun _ _=>0,s:=fun _ _=>0,filled:=filled}
def oneRaise (n term : Nat) (filled : List Triple) : Source25PairTransport.State :=
  {n:=n,r:=fun x y=>if x=term ∧ x≠y then 1 else 0,
   s:=fun x y=>if y=term ∧ x≠y then 1 else 0,filled:=filled}
def raisePotential (term x : Nat) : Int := if x=term then 1 else 0

theorem one_raise_excess (n term : Nat) (filled : List Triple) :
    excess (oneRaise n term filled) = RootGaugeNormalization.shifted (excess (zeroState n filled)) (raisePotential term) := by
  funext x y
  by_cases same : x=y
  · subst y
    simp [excess,oneRaise,zeroState,RootGaugeNormalization.shifted]
  · by_cases hx : x=term <;> by_cases hy : y=term <;>
      simp_all [excess,oneRaise,zeroState,raisePotential,RootGaugeNormalization.shifted,eq_comm]

theorem one_raise_same_fixed (n term : Nat) (filled : List Triple) :
    SameFixed n (excess (zeroState n filled)) (excess (oneRaise n term filled)) filled filled := by
  refine ⟨rfl,?_⟩
  intro x y _ _
  rw [one_raise_excess,RootGaugeNormalization.normal_after_shift]

def addTerm (state : Source25PairTransport.State) : Source25PairTransport.State :=
  {n:=state.n+1,r:=Source25PairTransport.fiberPush (List.range state.n) id state.r,
   s:=Source25PairTransport.fiberPush (List.range state.n) id state.s,filled:=state.filled}
def identify01 (state : Source25PairTransport.State) : Source25PairTransport.State :=
  let q := Source25PairTransport.identificationMap 0 1
  {n:=state.n-1,r:=Source25PairTransport.fiberPush (List.range state.n) q state.r,
   s:=Source25PairTransport.fiberPush (List.range state.n) q state.s,filled:=Source25PairTransport.carry q state.filled}

theorem add_term_is_source_step (state : Source25PairTransport.State) :
    Source25PairTransport.sourceStep state .addTerm = some (addTerm state) := by
  simp [Source25PairTransport.sourceStep,Source25PairTransport.stepWith,Source25PairTransport.enabled,addTerm]

theorem identify_01_is_source_step (state : Source25PairTransport.State) (enabled : 1<state.n) :
    Source25PairTransport.sourceStep state (.identify 0 1) = some (identify01 state) := by
  simp [Source25PairTransport.sourceStep,Source25PairTransport.stepWith,Source25PairTransport.enabled,identify01,enabled]

theorem added_term_triangle_obstruction :
    diagnostic (excess (addTerm (oneRaise 2 0 []))) (0,1,2) = 1 := by
  decide

theorem identified_triangle_obstruction :
    diagnostic (excess (identify01 (oneRaise 4 2 [(0,2,3),(1,2,3)]))) (0,1,2) = -1 := by
  decide

theorem original_marked_triangles_balanced :
    balanceRecord (excess (oneRaise 4 2 [(0,2,3),(1,2,3)])) [(0,2,3),(1,2,3)] =
      [((0,2,3),true),((1,2,3),true)] := by
  decide

theorem identification_changes_marked_balance :
    (identify01 (oneRaise 4 2 [(0,2,3),(1,2,3)])).filled = [(0,1,2)] ∧
    balanceRecord (excess (identify01 (oneRaise 4 2 [(0,2,3),(1,2,3)]))) [(0,1,2)] =
      [((0,1,2),false)] ∧
    balanceRecord (excess (identify01 (zeroState 4 [(0,2,3),(1,2,3)]))) [(0,1,2)] =
      [((0,1,2),true)] := by
  constructor
  · simp [identify01,oneRaise,Source25PairTransport.carry,
      Source25PairTransport.normalize,Source25PairTransport.identificationMap,
      Source25PairTransport.wayRound,List.eraseDups_cons,List.mergeSort]
  · constructor <;> decide

def directionState : Source25PairTransport.State :=
  { n := 3, r := (fun x y => if x=0 ∧ y=1 then 1 else 0),
    s := (fun _ _ => 0), filled := [] }

theorem filled_direction_changes_balance :
    diagnostic (excess directionState) (0,1,2) = 1 ∧
    diagnostic (excess directionState) (0,2,1) = 0 := by
  decide

theorem nonzero_cycle_forbids_gradient (n : Nat) (e : Table) (x y z : Nat)
    (hx : x<n) (hy : y<n) (hz : z<n) (nonzero : diagnostic e (x,y,z)≠0) :
    ¬∃ g : Nat → Int, ∀ a b, a<n → b<n → e a b=g a-g b := by
  rintro ⟨g,hg⟩
  have hxy := hg x y hx hy
  have hyz := hg y z hy hz
  have hzx := hg z x hz hx
  simp only [diagnostic] at nonzero
  omega

theorem term_addition_result_not_gradient :
    ¬∃ g : Nat → Int, ∀ x y, x<3 → y<3 →
      excess (addTerm (oneRaise 2 0 [])) x y = g x-g y := by
  apply nonzero_cycle_forbids_gradient 3 _ 0 1 2 (by decide) (by decide) (by decide)
  rw [added_term_triangle_obstruction]
  decide

theorem identification_result_not_gradient :
    ¬∃ g : Nat → Int, ∀ x y, x<3 → y<3 →
      excess (identify01 (oneRaise 4 2 [(0,2,3),(1,2,3)])) x y = g x-g y := by
  apply nonzero_cycle_forbids_gradient 3 _ 0 1 2 (by decide) (by decide) (by decide)
  rw [identified_triangle_obstruction]
  decide

end WitnessedDifference.MarkedGaugeTransport

#print axioms WitnessedDifference.MarkedGaugeTransport.cyclic_diagnostic
#print axioms WitnessedDifference.MarkedGaugeTransport.diagnostic_after_shift
#print axioms WitnessedDifference.MarkedGaugeTransport.diagnostic_after_normal
#print axioms WitnessedDifference.MarkedGaugeTransport.diagnostic_pullback_rename
#print axioms WitnessedDifference.MarkedGaugeTransport.balance_record_after_shift
#print axioms WitnessedDifference.MarkedGaugeTransport.balance_record_after_normal
#print axioms WitnessedDifference.MarkedGaugeTransport.same_fixed_iff_gradient
#print axioms WitnessedDifference.MarkedGaugeTransport.one_raise_excess
#print axioms WitnessedDifference.MarkedGaugeTransport.one_raise_same_fixed
#print axioms WitnessedDifference.MarkedGaugeTransport.add_term_is_source_step
#print axioms WitnessedDifference.MarkedGaugeTransport.identify_01_is_source_step
#print axioms WitnessedDifference.MarkedGaugeTransport.added_term_triangle_obstruction
#print axioms WitnessedDifference.MarkedGaugeTransport.identified_triangle_obstruction
#print axioms WitnessedDifference.MarkedGaugeTransport.original_marked_triangles_balanced
#print axioms WitnessedDifference.MarkedGaugeTransport.identification_changes_marked_balance
#print axioms WitnessedDifference.MarkedGaugeTransport.filled_direction_changes_balance
#print axioms WitnessedDifference.MarkedGaugeTransport.nonzero_cycle_forbids_gradient
#print axioms WitnessedDifference.MarkedGaugeTransport.term_addition_result_not_gradient
#print axioms WitnessedDifference.MarkedGaugeTransport.identification_result_not_gradient
