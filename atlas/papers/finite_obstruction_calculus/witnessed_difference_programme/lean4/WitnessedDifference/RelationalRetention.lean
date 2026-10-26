/-!
# Declared relational retention: strong bisimulation and succession

A labelled transition relation is explicit additional input. It may branch,
be partial, or contain cycles. Exact report-respecting strong bisimilarity is
an equivalence, the greatest bisimulation, and supports a set-level quotient.
Finite descending refinement has a separate native implementation; the formal
fixed-point theorem states exactly what stabilization must establish.

The graph succession result concerns generated nonempty reachability, not
physical time. None of these statements assert HoTT equivalence, higher
coherence, Kan fibrancy, or a transition-selection rule from reports alone.
-/

namespace WitnessedDifference.RelationalRetention

universe u v w

def IsBisimulation {State : Type u} {Label : Type v} {Report : Type w}
    (step : Label → State → State → Prop) (report : State → Report)
    (R : State → State → Prop) : Prop :=
  ∀ x y, R x y →
    report x = report y ∧
    (∀ label x', step label x x' → ∃ y', step label y y' ∧ R x' y') ∧
    (∀ label y', step label y y' → ∃ x', step label x x' ∧ R x' y')

def Bisimilar {State : Type u} {Label : Type v} {Report : Type w}
    (step : Label → State → State → Prop) (report : State → Report) (x y : State) : Prop :=
  ∃ R : State → State → Prop, IsBisimulation step report R ∧ R x y

theorem identity_bisimulation
    {State : Type u} {Label : Type v} {Report : Type w}
    (step : Label → State → State → Prop) (report : State → Report) :
    IsBisimulation step report (fun x y => x = y) := by
  intro x y hxy
  subst y
  refine ⟨rfl, ?_, ?_⟩
  · intro label x' hx'
    exact ⟨x', hx', rfl⟩
  · intro label y' hy'
    exact ⟨y', hy', rfl⟩

theorem converse_bisimulation
    {State : Type u} {Label : Type v} {Report : Type w}
    {step : Label → State → State → Prop} {report : State → Report}
    {R : State → State → Prop} (hR : IsBisimulation step report R) :
    IsBisimulation step report (fun x y => R y x) := by
  intro x y hxy
  obtain ⟨hreport, hforth, hback⟩ := hR y x hxy
  refine ⟨hreport.symm, ?_, ?_⟩
  · intro label x' hx'
    obtain ⟨y', hy', hpair⟩ := hback label x' hx'
    exact ⟨y', hy', hpair⟩
  · intro label y' hy'
    obtain ⟨x', hx', hpair⟩ := hforth label y' hy'
    exact ⟨x', hx', hpair⟩

theorem composite_bisimulation
    {State : Type u} {Label : Type v} {Report : Type w}
    {step : Label → State → State → Prop} {report : State → Report}
    {R T : State → State → Prop}
    (hR : IsBisimulation step report R) (hT : IsBisimulation step report T) :
    IsBisimulation step report (fun x z => ∃ y, R x y ∧ T y z) := by
  intro x z hcomp
  obtain ⟨y, hxy, hyz⟩ := hcomp
  obtain ⟨hreportR, hforthR, hbackR⟩ := hR x y hxy
  obtain ⟨hreportT, hforthT, hbackT⟩ := hT y z hyz
  refine ⟨hreportR.trans hreportT, ?_, ?_⟩
  · intro label x' hx'
    obtain ⟨y', hy', hxy'⟩ := hforthR label x' hx'
    obtain ⟨z', hz', hyz'⟩ := hforthT label y' hy'
    exact ⟨z', hz', y', hxy', hyz'⟩
  · intro label z' hz'
    obtain ⟨y', hy', hyz'⟩ := hbackT label z' hz'
    obtain ⟨x', hx', hxy'⟩ := hbackR label y' hy'
    exact ⟨x', hx', y', hxy', hyz'⟩

theorem bisimilar_refl
    {State : Type u} {Label : Type v} {Report : Type w}
    (step : Label → State → State → Prop) (report : State → Report) (x : State) :
    Bisimilar step report x x :=
  ⟨fun a b => a = b, identity_bisimulation step report, rfl⟩

theorem bisimilar_symm
    {State : Type u} {Label : Type v} {Report : Type w}
    {step : Label → State → State → Prop} {report : State → Report}
    {x y : State} (h : Bisimilar step report x y) : Bisimilar step report y x := by
  obtain ⟨R, hR, hxy⟩ := h
  exact ⟨fun a b => R b a, converse_bisimulation hR, hxy⟩

theorem bisimilar_trans
    {State : Type u} {Label : Type v} {Report : Type w}
    {step : Label → State → State → Prop} {report : State → Report}
    {x y z : State} (hxy : Bisimilar step report x y) (hyz : Bisimilar step report y z) :
    Bisimilar step report x z := by
  obtain ⟨R, hR, hxy⟩ := hxy
  obtain ⟨T, hT, hyz⟩ := hyz
  exact ⟨fun a c => ∃ b, R a b ∧ T b c, composite_bisimulation hR hT, y, hxy, hyz⟩

theorem greatest_bisimulation
    {State : Type u} {Label : Type v} {Report : Type w}
    (step : Label → State → State → Prop) (report : State → Report) :
    IsBisimulation step report (Bisimilar step report) := by
  intro x y h
  obtain ⟨R, hR, hxy⟩ := h
  obtain ⟨hreport, hforth, hback⟩ := hR x y hxy
  refine ⟨hreport, ?_, ?_⟩
  · intro label x' hx'
    obtain ⟨y', hy', hpair⟩ := hforth label x' hx'
    exact ⟨y', hy', R, hR, hpair⟩
  · intro label y' hy'
    obtain ⟨x', hx', hpair⟩ := hback label y' hy'
    exact ⟨x', hx', R, hR, hpair⟩

def bisimulationSetoid
    {State : Type u} {Label : Type v} {Report : Type w}
    (step : Label → State → State → Prop) (report : State → Report) : Setoid State where
  r := Bisimilar step report
  iseqv := ⟨bisimilar_refl step report, bisimilar_symm, bisimilar_trans⟩

def quotientReport
    {State : Type u} {Label : Type v} {Report : Type w}
    (step : Label → State → State → Prop) (report : State → Report) :
    Quotient (bisimulationSetoid step report) → Report :=
  Quotient.lift report (fun x y h => (greatest_bisimulation step report x y h).1)

/-- Forth and back make successor existence in each equivalence class
independent of the chosen source representative. -/
theorem quotient_successor_representative_independence
    {State : Type u} {Label : Type v} {Report : Type w}
    (step : Label → State → State → Prop) (report : State → Report)
    (label : Label) {x y z : State} (hxy : Bisimilar step report x y) :
    (∃ x', step label x x' ∧ Bisimilar step report x' z) ↔
      (∃ y', step label y y' ∧ Bisimilar step report y' z) := by
  constructor
  · intro hx
    obtain ⟨x', hx', hxz⟩ := hx
    obtain ⟨y', hy', hpair⟩ := (greatest_bisimulation step report x y hxy).2.1 label x' hx'
    exact ⟨y', hy', bisimilar_trans (bisimilar_symm hpair) hxz⟩
  · intro hy
    obtain ⟨y', hy', hyz⟩ := hy
    obtain ⟨x', hx', hpair⟩ := (greatest_bisimulation step report x y hxy).2.2 label y' hy'
    exact ⟨x', hx', bisimilar_trans hpair hyz⟩

def quotientStep
    {State : Type u} {Label : Type v} {Report : Type w}
    (step : Label → State → State → Prop) (report : State → Report) (label : Label)
    (p q : Quotient (bisimulationSetoid step report)) : Prop :=
  ∃ x y, Quotient.mk (bisimulationSetoid step report) x = p ∧
    Quotient.mk (bisimulationSetoid step report) y = q ∧ step label x y

/-- The quotient transition is represented by successors of *any* chosen
source representative. This is the back condition for the quotient map. -/
theorem quotient_step_from_representative
    {State : Type u} {Label : Type v} {Report : Type w}
    (step : Label → State → State → Prop) (report : State → Report)
    (label : Label) (x z : State) :
    quotientStep step report label (Quotient.mk (bisimulationSetoid step report) x)
      (Quotient.mk (bisimulationSetoid step report) z) ↔
      ∃ y, step label x y ∧ Bisimilar step report y z := by
  constructor
  · intro h
    obtain ⟨a, b, ha, hb, hab⟩ := h
    have hax : Bisimilar step report a x := Quotient.exact ha
    have hbz : Bisimilar step report b z := Quotient.exact hb
    obtain ⟨y, hxy, hby⟩ := (greatest_bisimulation step report a x hax).2.1 label b hab
    exact ⟨y, hxy, bisimilar_trans (bisimilar_symm hby) hbz⟩
  · intro h
    obtain ⟨y, hxy, hyz⟩ := h
    exact ⟨x, y, rfl, Quotient.sound hyz, hxy⟩

/-- Every equivalence bisimulation quotient maps to the greatest quotient.
The map direction is from a finer congruence quotient to the coarsest one. -/
def comparisonMap
    {State : Type u} {Label : Type v} {Report : Type w}
    (step : Label → State → State → Prop) (report : State → Report)
    (R : Setoid State) (hR : IsBisimulation step report R.r) :
    Quotient R → Quotient (bisimulationSetoid step report) :=
  Quotient.lift (Quotient.mk (bisimulationSetoid step report))
    (fun _ _ hxy => Quotient.sound ⟨R.r, hR, hxy⟩)

theorem comparison_unique
    {State : Type u} {Label : Type v} {Report : Type w}
    (step : Label → State → State → Prop) (report : State → Report)
    (R : Setoid State) (hR : IsBisimulation step report R.r)
    (g : Quotient R → Quotient (bisimulationSetoid step report))
    (hg : ∀ x, g (Quotient.mk R x) = Quotient.mk (bisimulationSetoid step report) x) :
    g = comparisonMap step report R hR := by
  funext q
  refine Quotient.inductionOn q ?_
  intro x
  exact hg x

def Refinement
    {State : Type u} {Label : Type v} {Report : Type w}
    (step : Label → State → State → Prop) (report : State → Report)
    (R : State → State → Prop) (x y : State) : Prop :=
  R x y ∧ report x = report y ∧
    (∀ label x', step label x x' → ∃ y', step label y y' ∧ R x' y') ∧
    (∀ label y', step label y y' → ∃ x', step label x x' ∧ R x' y')

/-- A stable descending refinement is a bisimulation. -/
theorem refinement_fixed_point_is_bisimulation
    {State : Type u} {Label : Type v} {Report : Type w}
    (step : Label → State → State → Prop) (report : State → Report)
    (R : State → State → Prop)
    (hstable : ∀ x y, R x y → Refinement step report R x y) :
    IsBisimulation step report R := by
  intro x y hxy
  exact (hstable x y hxy).2

/-- Every stable relation is contained in the greatest bisimulation. -/
theorem refinement_fixed_point_below_bisimilar
    {State : Type u} {Label : Type v} {Report : Type w}
    (step : Label → State → State → Prop) (report : State → Report)
    (R : State → State → Prop)
    (hstable : ∀ x y, R x y → Refinement step report R x y) :
    ∀ x y, R x y → Bisimilar step report x y := by
  intro x y hxy
  exact ⟨R, refinement_fixed_point_is_bisimulation step report R hstable, hxy⟩

/-- Descending refinement starting at report equality. -/
def Approximation
    {State : Type u} {Label : Type v} {Report : Type w}
    (step : Label → State → State → Prop) (report : State → Report) :
    Nat → State → State → Prop
  | 0 => fun x y => report x = report y
  | depth + 1 => Refinement step report (Approximation step report depth)

/-- Two-sided relational refinement preserves equivalence, including with
empty successor sets. This justifies partition-based finite refinement. -/
theorem refinement_preserves_equivalence
    {State : Type u} {Label : Type v} {Report : Type w}
    (step : Label → State → State → Prop) (report : State → Report)
    (R : State → State → Prop) (hR : Equivalence R) :
    Equivalence (Refinement step report R) := by
  refine ⟨?_, ?_, ?_⟩
  · intro x
    refine ⟨hR.refl x, rfl, ?_, ?_⟩
    · intro label x' hx'
      exact ⟨x', hx', hR.refl x'⟩
    · intro label x' hx'
      exact ⟨x', hx', hR.refl x'⟩
  · intro x y hxy
    obtain ⟨hxyR, hreport, hforth, hback⟩ := hxy
    refine ⟨hR.symm hxyR, hreport.symm, ?_, ?_⟩
    · intro label y' hy'
      obtain ⟨x', hx', hpair⟩ := hback label y' hy'
      exact ⟨x', hx', hR.symm hpair⟩
    · intro label x' hx'
      obtain ⟨y', hy', hpair⟩ := hforth label x' hx'
      exact ⟨y', hy', hR.symm hpair⟩
  · intro x y z hxy hyz
    obtain ⟨hxyR, hreportXY, hforthXY, hbackXY⟩ := hxy
    obtain ⟨hyzR, hreportYZ, hforthYZ, hbackYZ⟩ := hyz
    refine ⟨hR.trans hxyR hyzR, hreportXY.trans hreportYZ, ?_, ?_⟩
    · intro label x' hx'
      obtain ⟨y', hy', hxy'⟩ := hforthXY label x' hx'
      obtain ⟨z', hz', hyz'⟩ := hforthYZ label y' hy'
      exact ⟨z', hz', hR.trans hxy' hyz'⟩
    · intro label z' hz'
      obtain ⟨y', hy', hyz'⟩ := hbackYZ label z' hz'
      obtain ⟨x', hx', hxy'⟩ := hbackXY label y' hy'
      exact ⟨x', hx', hR.trans hxy' hyz'⟩

theorem approximation_equivalence
    {State : Type u} {Label : Type v} {Report : Type w}
    (step : Label → State → State → Prop) (report : State → Report) (depth : Nat) :
    Equivalence (Approximation step report depth) := by
  induction depth with
  | zero => exact ⟨fun _ => rfl, fun h => h.symm, fun hxy hyz => hxy.trans hyz⟩
  | succ depth ih =>
    exact refinement_preserves_equivalence step report
      (Approximation step report depth) ih

theorem bisimilar_below_approximation
    {State : Type u} {Label : Type v} {Report : Type w}
    (step : Label → State → State → Prop) (report : State → Report) (depth : Nat) :
    ∀ x y, Bisimilar step report x y → Approximation step report depth x y := by
  induction depth with
  | zero =>
    intro x y hxy
    exact (greatest_bisimulation step report x y hxy).1
  | succ depth ih =>
    intro x y hxy
    obtain ⟨hreport, hforth, hback⟩ := greatest_bisimulation step report x y hxy
    refine ⟨ih x y hxy, hreport, ?_, ?_⟩
    · intro label x' hx'
      obtain ⟨y', hy', hpair⟩ := hforth label x' hx'
      exact ⟨y', hy', ih x' y' hpair⟩
    · intro label y' hy'
      obtain ⟨x', hx', hpair⟩ := hback label y' hy'
      exact ⟨x', hx', ih x' y' hpair⟩

/-- Stabilization of the actual approximation chain entails greatestness,
not merely stability of an arbitrary overrefined relation. -/
theorem stabilized_approximation_iff_bisimilar
    {State : Type u} {Label : Type v} {Report : Type w}
    (step : Label → State → State → Prop) (report : State → Report) (depth : Nat)
    (hstable : ∀ x y, Approximation step report depth x y →
      Approximation step report (depth + 1) x y) (x y : State) :
    Approximation step report depth x y ↔ Bisimilar step report x y := by
  constructor
  · exact refinement_fixed_point_below_bisimilar step report
      (Approximation step report depth) hstable x y
  · exact bisimilar_below_approximation step report depth x y

/-- Nonempty paths generated only from declared directed edges. -/
inductive Reach {State : Type u} (edge : State → State → Prop) : State → State → Prop
  | edge {x y} : edge x y → Reach edge x y
  | concat {x y z} : Reach edge x y → Reach edge y z → Reach edge x z

def Acyclic {State : Type u} (edge : State → State → Prop) : Prop :=
  ∀ x, ¬ Reach edge x x

/-- Generated reachability supports strict succession exactly when cycles
are absent. This assertion is independent of any enumeration or clock. -/
theorem reachability_strict_iff_acyclic
    {State : Type u} (edge : State → State → Prop) :
    ((∀ x, ¬ Reach edge x x) ∧
      (∀ x y z, Reach edge x y → Reach edge y z → Reach edge x z)) ↔ Acyclic edge := by
  constructor
  · intro h
    exact h.1
  · intro h
    exact ⟨h, fun _ _ _ hxy hyz => Reach.concat hxy hyz⟩

/-- A witnessed directed cycle refutes every irreflexive transitive relation
containing the declared edges, not just this reachability presentation. -/
theorem cycle_refutes_any_strict_extension
    {State : Type u} {edge order : State → State → Prop}
    (hcontains : ∀ x y, edge x y → order x y)
    (htrans : ∀ x y z, order x y → order y z → order x z)
    (hirrefl : ∀ x, ¬ order x x) {x : State} (hcycle : Reach edge x x) : False := by
  have hpath : ∀ a b, Reach edge a b → order a b := by
    intro a b h
    induction h with
    | edge h => exact hcontains _ _ h
    | concat _ _ ih1 ih2 => exact htrans _ _ _ ih1 ih2
  exact hirrefl x (hpath x x hcycle)

/-- Symmetry-breaking is necessary to orient a pair whose swapping symmetry
is retained. This does not require a pre-existing order or chosen clock. -/
theorem swapping_symmetry_forbids_asymmetric_pair
    {State : Type u} (order : State → State → Prop) (swap : State → State)
    (hasym : ∀ x y, order x y → ¬ order y x)
    (hinvariant : ∀ x y, order x y → order (swap x) (swap y))
    (x y : State) (hswapx : swap x = y) (hswapy : swap y = x) : ¬ order x y := by
  intro hxy
  have hyx := hinvariant x y hxy
  rw [hswapx, hswapy] at hyx
  exact hasym x y hxy hyx

end WitnessedDifference.RelationalRetention

#print axioms WitnessedDifference.RelationalRetention.IsBisimulation
#print axioms WitnessedDifference.RelationalRetention.Bisimilar
#print axioms WitnessedDifference.RelationalRetention.bisimulationSetoid
#print axioms WitnessedDifference.RelationalRetention.quotientReport
#print axioms WitnessedDifference.RelationalRetention.quotientStep
#print axioms WitnessedDifference.RelationalRetention.comparisonMap
#print axioms WitnessedDifference.RelationalRetention.Refinement
#print axioms WitnessedDifference.RelationalRetention.Approximation
#print axioms WitnessedDifference.RelationalRetention.Reach
#print axioms WitnessedDifference.RelationalRetention.Reach.edge
#print axioms WitnessedDifference.RelationalRetention.Reach.concat
#print axioms WitnessedDifference.RelationalRetention.Acyclic
#print axioms WitnessedDifference.RelationalRetention.identity_bisimulation
#print axioms WitnessedDifference.RelationalRetention.converse_bisimulation
#print axioms WitnessedDifference.RelationalRetention.composite_bisimulation
#print axioms WitnessedDifference.RelationalRetention.bisimilar_refl
#print axioms WitnessedDifference.RelationalRetention.bisimilar_symm
#print axioms WitnessedDifference.RelationalRetention.bisimilar_trans
#print axioms WitnessedDifference.RelationalRetention.greatest_bisimulation
#print axioms WitnessedDifference.RelationalRetention.quotient_successor_representative_independence
#print axioms WitnessedDifference.RelationalRetention.quotient_step_from_representative
#print axioms WitnessedDifference.RelationalRetention.comparison_unique
#print axioms WitnessedDifference.RelationalRetention.refinement_fixed_point_is_bisimulation
#print axioms WitnessedDifference.RelationalRetention.refinement_fixed_point_below_bisimilar
#print axioms WitnessedDifference.RelationalRetention.bisimilar_below_approximation
#print axioms WitnessedDifference.RelationalRetention.refinement_preserves_equivalence
#print axioms WitnessedDifference.RelationalRetention.approximation_equivalence
#print axioms WitnessedDifference.RelationalRetention.stabilized_approximation_iff_bisimilar
#print axioms WitnessedDifference.RelationalRetention.reachability_strict_iff_acyclic
#print axioms WitnessedDifference.RelationalRetention.cycle_refutes_any_strict_extension
#print axioms WitnessedDifference.RelationalRetention.swapping_symmetry_forbids_asymmetric_pair
