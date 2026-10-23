/-!
# Constrained pointwise observer descent

An explicit context selector supplies the cover witness, avoiding choice. Fixed
compatible sections assignments have a unique pointwise union. They glue in a
constrained target family exactly when that union is admissible. The Bool
countermodel shows that compatibility alone does not force target admissibility.
This core-only file proves structural gluing, not finite algorithm enumeration,
partial-map completion, cohomology, contextuality or physical observer adequacy.
-/
namespace WitnessedDifference.ObserverDescent

universe u v w

/-- The abstract restriction map lands in the already checked matching families. -/
def CoverExistence {Global : Type u} {Matching : Type v}
    (restrict : Global → Matching) : Prop := ∀ m, ∃ g, restrict g = m

def CoverSeparated {Global : Type u} {Matching : Type v}
    (restrict : Global → Matching) : Prop :=
  ∀ g h, restrict g = restrict h → g = h

def CoverSheaf {Global : Type u} {Matching : Type v}
    (restrict : Global → Matching) : Prop :=
  ∀ m, ∃ g, restrict g = m ∧ ∀ h, restrict h = m → h = g

theorem sheaf_iff_existence_and_separated {Global : Type u} {Matching : Type v}
    (restrict : Global → Matching) :
    CoverSheaf restrict ↔ CoverExistence restrict ∧ CoverSeparated restrict := by
  constructor
  · intro sheaf
    constructor
    · intro m
      obtain ⟨g, hg, _⟩ := sheaf m
      exact ⟨g, hg⟩
    · intro g h equal
      obtain ⟨k, _, unique⟩ := sheaf (restrict g)
      exact (unique g rfl).trans (unique h equal.symm).symm
  · intro ⟨existsGlue, separated⟩ m
    obtain ⟨g, hg⟩ := existsGlue m
    exact ⟨g, hg, fun h hh => separated h g (hh.trans hg.symm)⟩

def UnionReport {Point : Type u} {Context : Type v} {Value : Type w}
    (owner : Point → Context) (sections : Context → Point → Value) : Point → Value :=
  fun x => sections (owner x) x

def Compatible {Point : Type u} {Context : Type v} {Value : Type w}
    (member : Context → Point → Prop) (sections : Context → Point → Value) : Prop :=
  ∀ i j x, member i x → member j x → sections i x = sections j x

def Restricts {Point : Type u} {Context : Type v} {Value : Type w}
    (member : Context → Point → Prop) (sections : Context → Point → Value)
    (global : Point → Value) : Prop :=
  ∀ i x, member i x → global x = sections i x

theorem union_restricts {Point : Type u} {Context : Type v} {Value : Type w}
    (member : Context → Point → Prop) (owner : Point → Context)
    (sections : Context → Point → Value)
    (covers : ∀ x, member (owner x) x) (compatible : Compatible member sections) :
    Restricts member sections (UnionReport owner sections) := by
  intro i x hx
  exact compatible (owner x) i x (covers x) hx

theorem glued_report_unique {Point : Type u} {Context : Type v} {Value : Type w}
    (member : Context → Point → Prop) (owner : Point → Context)
    (sections : Context → Point → Value) (covers : ∀ x, member (owner x) x)
    (g h : Point → Value) (hg : Restricts member sections g)
    (hh : Restricts member sections h) : g = h := by
  funext x
  exact (hg (owner x) x (covers x)).trans (hh (owner x) x (covers x)).symm

theorem constrained_glue_iff_union_admissible
    {Point : Type u} {Context : Type v} {Value : Type w}
    (member : Context → Point → Prop) (owner : Point → Context)
    (sections : Context → Point → Value) (admissible : (Point → Value) → Prop)
    (covers : ∀ x, member (owner x) x) (compatible : Compatible member sections) :
    (∃ g, admissible g ∧ Restricts member sections g) ↔
      admissible (UnionReport owner sections) := by
  constructor
  · intro ⟨g, hg, restrictions⟩
    have eq := glued_report_unique member owner sections covers g
      (UnionReport owner sections) restrictions
      (union_restricts member owner sections covers compatible)
    rw [← eq]
    exact hg
  · intro admissibility
    exact ⟨UnionReport owner sections, admissibility,
      union_restricts member owner sections covers compatible⟩

def SingletonMember (i x : Bool) : Prop := i = x

def OppositeLocalReports (i _x : Bool) : Bool := i

theorem equality_constraint_countermodel_compatible :
    Compatible SingletonMember OppositeLocalReports := by
  intro i j x hi hj
  exact hi.trans hj.symm

theorem equality_constraint_countermodel_no_global :
    ¬ ∃ g : Bool → Bool, g false = g true ∧
      Restricts SingletonMember OppositeLocalReports g := by
  intro ⟨g, constant, restrictions⟩
  have left : g false = false := restrictions false false rfl
  have right : g true = true := restrictions true true rfl
  have impossible : false = true := left.symm.trans (constant.trans right)
  cases impossible

#print axioms sheaf_iff_existence_and_separated
#print axioms union_restricts
#print axioms glued_report_unique
#print axioms constrained_glue_iff_union_admissible
#print axioms equality_constraint_countermodel_compatible
#print axioms equality_constraint_countermodel_no_global

end WitnessedDifference.ObserverDescent
