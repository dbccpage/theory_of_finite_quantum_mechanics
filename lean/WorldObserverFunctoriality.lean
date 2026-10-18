import PrimitiveDifference

/-!
# W3.5 observer functoriality: exact relation-level quotient core

This file proves the finite, relation-level core of observer functoriality.
A proof-bearing `SysMorph` is exactly a state map that preserves the zero
relation of the source and target primitive differences.  Such a map descends
uniquely to residual quotients; identity and composition descend functorially.

The explicit `Fin 2` identity below is deliberately a `RawMapCandidate`, not a
`SysMorph`: the source observer is constant and the target observer separates
the two points.  It is the coordinatewise-smallest heterogeneous non-descent
witness.  The returning-action adapter is only the same-system endomap special
case of that heterogeneous witness; no PCC theorem is imported.

This does not construct the full action/probe morphism from the historical
W3.5 packet, prove target-context coverage, treat partial actions, discharge an
estate-wide refactor, or establish a cohomological or authority claim.

AuthorityEffect: None.
-/

namespace OmegaWorld
namespace ObserverFunctorialityW35

open OmegaCore
open OmegaCore.PrimitiveDifference

universe u v w z

/-- A relation-level observer system.  The residual is Boolean, while its
`Zero` predicate and induced equivalence are carried by the shared kernel. -/
structure ObserverSystem where
  State : Type u
  difference : PrimitiveDifference State Bool

namespace ObserverSystem

abbrev Residual (S : ObserverSystem.{u}) : Type u :=
  S.difference.ResidualQuotient

abbrev classOf (S : ObserverSystem.{u}) (x : S.State) : S.Residual :=
  S.difference.classOf x

abbrev ZeroRel (S : ObserverSystem.{u}) (x y : S.State) : Prop :=
  S.difference.ZeroRel x y

end ObserverSystem

/-- The exact relation-preservation obligation for quotient descent. -/
def PreservesZeroRel
    {S : ObserverSystem.{u}} {T : ObserverSystem.{v}}
    (toFun : S.State → T.State) : Prop :=
  ∀ x y : S.State, S.ZeroRel x y → T.ZeroRel (toFun x) (toFun y)

/-- A proof-bearing relation-level system morphism.  A raw map becomes a
`SysMorph` only after its zero-relation preservation proof is supplied. -/
structure SysMorph (S : ObserverSystem.{u}) (T : ObserverSystem.{v}) where
  toFun : S.State → T.State
  preservesZeroRel : PreservesZeroRel toFun

namespace SysMorph

def identity (S : ObserverSystem.{u}) : SysMorph S S where
  toFun := id
  preservesZeroRel := by
    intro x y hxy
    exact hxy

def compose
    {S : ObserverSystem.{u}} {T : ObserverSystem.{v}}
    {U : ObserverSystem.{w}}
    (g : SysMorph T U) (f : SysMorph S T) : SysMorph S U where
  toFun := g.toFun ∘ f.toFun
  preservesZeroRel := by
    intro x y hxy
    exact g.preservesZeroRel (f.toFun x) (f.toFun y)
      (f.preservesZeroRel x y hxy)

@[ext]
theorem ext
    {S : ObserverSystem.{u}} {T : ObserverSystem.{v}}
    {f g : SysMorph S T} (h : f.toFun = g.toFun) : f = g := by
  cases f with
  | mk f hf =>
      cases g with
      | mk g hg =>
          dsimp at h
          subst g
          rfl

theorem identity_toFun (S : ObserverSystem.{u}) (x : S.State) :
    (identity S).toFun x = x :=
  rfl

theorem compose_toFun
    {S : ObserverSystem.{u}} {T : ObserverSystem.{v}}
    {U : ObserverSystem.{w}}
    (g : SysMorph T U) (f : SysMorph S T) (x : S.State) :
    (compose g f).toFun x = g.toFun (f.toFun x) :=
  rfl

theorem identity_comp
    {S : ObserverSystem.{u}} {T : ObserverSystem.{v}}
    (f : SysMorph S T) : compose (identity T) f = f := by
  apply ext
  rfl

theorem comp_identity
    {S : ObserverSystem.{u}} {T : ObserverSystem.{v}}
    (f : SysMorph S T) : compose f (identity S) = f := by
  apply ext
  rfl

theorem comp_assoc
    {S : ObserverSystem.{u}} {T : ObserverSystem.{v}}
    {U : ObserverSystem.{w}} {V : ObserverSystem.{z}}
    (h : SysMorph U V) (g : SysMorph T U) (f : SysMorph S T) :
    compose h (compose g f) = compose (compose h g) f := by
  apply ext
  rfl

end SysMorph

/-- The quotient map induced by a proof-bearing system morphism. -/
def quotientMap
    {S : ObserverSystem.{u}} {T : ObserverSystem.{v}}
    (f : SysMorph S T) : S.Residual → T.Residual :=
  S.difference.invariantFactorMod
    f.toFun T.difference.zeroSetoid f.preservesZeroRel

theorem quotientMap_classOf
    {S : ObserverSystem.{u}} {T : ObserverSystem.{v}}
    (f : SysMorph S T) (x : S.State) :
    quotientMap f (S.classOf x) = T.classOf (f.toFun x) :=
  S.difference.invariantFactorMod_classOf
    f.toFun T.difference.zeroSetoid f.preservesZeroRel x

/-- Relation preservation is necessary and sufficient for the existence of a
quotient factor satisfying the commuting class equation. -/
theorem preserves_iff_exists_quotient_factor
    {S : ObserverSystem.{u}} {T : ObserverSystem.{v}}
    (toFun : S.State → T.State) :
    PreservesZeroRel toFun ↔
      ∃ factor : S.Residual → T.Residual,
        ∀ x : S.State, factor (S.classOf x) = T.classOf (toFun x) := by
  change S.difference.InvariantCongruentMod toFun T.difference.zeroSetoid ↔ _
  exact
    (S.difference.invariantFactorMod_exists_iff_invariantCongruentMod
      toFun T.difference.zeroSetoid).symm

theorem quotient_factor_unique
    {S : ObserverSystem.{u}} {T : ObserverSystem.{v}}
    (toFun : S.State → T.State) (hpres : PreservesZeroRel toFun)
    (factor : S.Residual → T.Residual)
    (hfactor : ∀ x : S.State,
      factor (S.classOf x) = T.classOf (toFun x)) :
    factor = quotientMap ⟨toFun, hpres⟩ := by
  funext q
  refine Quotient.inductionOn q ?_
  intro x
  change factor (S.classOf x) =
    quotientMap ⟨toFun, hpres⟩ (S.classOf x)
  rw [hfactor x, quotientMap_classOf]

/-- An explicit core-only encoding of unique existence; no library-specific
unique-existence notation is required. -/
def UniqueQuotientFactor
    {S : ObserverSystem.{u}} {T : ObserverSystem.{v}}
    (toFun : S.State → T.State) : Prop :=
  ∃ factor : S.Residual → T.Residual,
    (∀ x : S.State, factor (S.classOf x) = T.classOf (toFun x)) ∧
    ∀ other : S.Residual → T.Residual,
      (∀ x : S.State, other (S.classOf x) = T.classOf (toFun x)) →
      other = factor

/-- The stronger exact statement: the commuting quotient factor exists
uniquely iff the raw map preserves the two zero relations. -/
theorem preserves_iff_existsUnique_quotient_factor
    {S : ObserverSystem.{u}} {T : ObserverSystem.{v}}
    (toFun : S.State → T.State) :
    PreservesZeroRel toFun ↔ UniqueQuotientFactor toFun := by
  constructor
  · intro hpres
    refine ⟨quotientMap ⟨toFun, hpres⟩,
      quotientMap_classOf ⟨toFun, hpres⟩, ?_⟩
    intro factor hfactor
    exact quotient_factor_unique toFun hpres factor hfactor
  · rintro ⟨factor, hfactor, _⟩
    exact (preserves_iff_exists_quotient_factor toFun).mpr
      ⟨factor, hfactor⟩

theorem quotientMap_identity (S : ObserverSystem.{u}) :
    quotientMap (SysMorph.identity S) = id := by
  funext q
  refine Quotient.inductionOn q ?_
  intro x
  rfl

theorem quotientMap_compose
    {S : ObserverSystem.{u}} {T : ObserverSystem.{v}}
    {U : ObserverSystem.{w}}
    (g : SysMorph T U) (f : SysMorph S T) :
    quotientMap (SysMorph.compose g f) = quotientMap g ∘ quotientMap f := by
  funext q
  refine Quotient.inductionOn q ?_
  intro x
  rfl

/-- A raw state function is named separately so that a non-preserving map
cannot be mistaken for a proof-bearing `SysMorph`. -/
structure RawMapCandidate (S : ObserverSystem.{u}) (T : ObserverSystem.{v}) where
  toFun : S.State → T.State

/-- Exact heterogeneous witness that a raw map fails quotient descent. -/
structure DescentFailure
    (S : ObserverSystem.{u}) (T : ObserverSystem.{v})
    (toFun : S.State → T.State) where
  left : S.State
  right : S.State
  sourceZero : S.ZeroRel left right
  targetNonzero : ¬ T.ZeroRel (toFun left) (toFun right)

namespace DescentFailure

theorem not_preserves
    {S : ObserverSystem.{u}} {T : ObserverSystem.{v}}
    {toFun : S.State → T.State} (witness : DescentFailure S T toFun) :
    ¬ PreservesZeroRel toFun := by
  intro hpres
  exact witness.targetNonzero
    (hpres witness.left witness.right witness.sourceZero)

theorem no_quotient_factor
    {S : ObserverSystem.{u}} {T : ObserverSystem.{v}}
    {toFun : S.State → T.State} (witness : DescentFailure S T toFun) :
    ¬ (∃ factor : S.Residual → T.Residual,
      ∀ x : S.State, factor (S.classOf x) = T.classOf (toFun x)) := by
  intro hfactor
  exact witness.not_preserves
    ((preserves_iff_exists_quotient_factor toFun).mpr hfactor)

theorem source_points_distinct
    {S : ObserverSystem.{u}} {T : ObserverSystem.{v}}
    {toFun : S.State → T.State} (witness : DescentFailure S T toFun) :
    witness.left ≠ witness.right := by
  intro h
  apply witness.targetNonzero
  rw [h]
  exact T.difference.zeroRel_refl _

theorem target_images_distinct
    {S : ObserverSystem.{u}} {T : ObserverSystem.{v}}
    {toFun : S.State → T.State} (witness : DescentFailure S T toFun) :
    toFun witness.left ≠ toFun witness.right := by
  intro h
  apply witness.targetNonzero
  rw [h]
  exact T.difference.zeroRel_refl _

end DescentFailure

theorem preserves_of_subsingleton_source
    (S : ObserverSystem.{u}) (T : ObserverSystem.{v})
    [Subsingleton S.State] (toFun : S.State → T.State) :
    PreservesZeroRel toFun := by
  intro x y _
  have hxy : x = y := Subsingleton.elim x y
  subst y
  exact T.difference.zeroRel_refl _

theorem preserves_of_subsingleton_target
    (S : ObserverSystem.{u}) (T : ObserverSystem.{v})
    [Subsingleton T.State] (toFun : S.State → T.State) :
    PreservesZeroRel toFun := by
  intro x y _
  have hxy : toFun x = toFun y := Subsingleton.elim _ _
  rw [hxy]
  exact T.difference.zeroRel_refl _

/-- A Boolean observer produces `false` exactly when the observations agree. -/
def observerDifference {X : Type u} (observe : X → Bool) :
    PrimitiveDifference X Bool where
  δ x y := if observe x = observe y then false else true
  Zero b := b = false
  zero_refl x := by simp
  zero_symm x y h := by
    by_cases hxy : observe x = observe y
    · simp [hxy.symm]
    · simp [hxy] at h
  zero_trans x y z hxy hyz := by
    by_cases h₁ : observe x = observe y
    · by_cases h₂ : observe y = observe z
      · have h₃ : observe x = observe z := h₁.trans h₂
        simp [h₃]
      · simp [h₂] at hyz
    · simp [h₁] at hxy

theorem observerDifference_zeroRel_iff
    {X : Type u} (observe : X → Bool) (x y : X) :
    (observerDifference observe).ZeroRel x y ↔ observe x = observe y := by
  change (if observe x = observe y then false else true) = false ↔
    observe x = observe y
  by_cases h : observe x = observe y <;> simp [h]

def fin2ConstantObserve (_ : Fin 2) : Bool := false

def fin2SeparatingObserve (x : Fin 2) : Bool :=
  if x = 0 then false else true

def fin2ConstantSystem : ObserverSystem where
  State := Fin 2
  difference := observerDifference fin2ConstantObserve

def fin2SeparatingSystem : ObserverSystem where
  State := Fin 2
  difference := observerDifference fin2SeparatingObserve

/-- The candidate is raw on purpose: no proof-bearing morphism is forged. -/
def fin2IdentityCandidate : RawMapCandidate fin2ConstantSystem fin2SeparatingSystem where
  toFun := id

theorem fin2_source_zero :
    fin2ConstantSystem.ZeroRel (0 : Fin 2) (1 : Fin 2) := by
  rw [show fin2ConstantSystem.ZeroRel (0 : Fin 2) (1 : Fin 2) =
    (observerDifference fin2ConstantObserve).ZeroRel 0 1 by rfl]
  rw [observerDifference_zeroRel_iff]
  rfl

theorem fin2_target_nonzero :
    ¬ fin2SeparatingSystem.ZeroRel (0 : Fin 2) (1 : Fin 2) := by
  rw [show fin2SeparatingSystem.ZeroRel (0 : Fin 2) (1 : Fin 2) =
    (observerDifference fin2SeparatingObserve).ZeroRel 0 1 by rfl]
  rw [observerDifference_zeroRel_iff]
  decide

def fin2IdentityFailure :
    DescentFailure fin2ConstantSystem fin2SeparatingSystem
      fin2IdentityCandidate.toFun where
  left := (0 : Fin 2)
  right := (1 : Fin 2)
  sourceZero := fin2_source_zero
  targetNonzero := fin2_target_nonzero

theorem fin2_identity_not_preserving :
    ¬ PreservesZeroRel fin2IdentityCandidate.toFun :=
  fin2IdentityFailure.not_preserves

theorem fin2_identity_not_a_sysMorph :
    ¬ (∃ f : SysMorph fin2ConstantSystem fin2SeparatingSystem,
      f.toFun = fin2IdentityCandidate.toFun) := by
  rintro ⟨f, hfun⟩
  apply fin2_identity_not_preserving
  simpa [hfun] using f.preservesZeroRel

theorem fin2_identity_no_quotient_factor :
    ¬ (∃ factor : fin2ConstantSystem.Residual → fin2SeparatingSystem.Residual,
      ∀ x : fin2ConstantSystem.State,
        factor (fin2ConstantSystem.classOf x) =
          fin2SeparatingSystem.classOf (fin2IdentityCandidate.toFun x)) :=
  fin2IdentityFailure.no_quotient_factor

/-- This packages the coordinatewise minimality claim without a cardinality
library: a failure itself supplies two distinct source points and two distinct
target images, while either subsingleton carrier forces preservation. -/
theorem fin2_failure_coordinatewise_minimal :
    fin2IdentityFailure.left ≠ fin2IdentityFailure.right ∧
      fin2IdentityCandidate.toFun fin2IdentityFailure.left ≠
        fin2IdentityCandidate.toFun fin2IdentityFailure.right :=
  ⟨fin2IdentityFailure.source_points_distinct,
    fin2IdentityFailure.target_images_distinct⟩

/-- The returning-action witness shape is the same-system endomap
specialization of heterogeneous descent failure. -/
structure ReturningActionWitness
    (S : ObserverSystem.{u}) (Context : Type v)
    (act : Context → S.State → S.State) where
  left : S.State
  right : S.State
  context : Context
  sourceZero : S.ZeroRel left right
  returnedNonzero : ¬ S.ZeroRel (act context left) (act context right)

def ReturningActionWitness.toDescentFailure
    {S : ObserverSystem.{u}} {Context : Type v}
    {act : Context → S.State → S.State}
    (witness : ReturningActionWitness S Context act) :
    DescentFailure S S (act witness.context) where
  left := witness.left
  right := witness.right
  sourceZero := witness.sourceZero
  targetNonzero := witness.returnedNonzero

/-- Serialized scope metadata.  False fields record nonclaims made by this
file; they are not proofs of global non-derivability. -/
inductive AuthorityEffect where
  | none
deriving DecidableEq, Repr

structure ScopeFence where
  relationQuotientCoreMechanized : Bool
  fullActionProbeMorphismsClaimed : Bool
  targetContextCoverageClaimed : Bool
  partialActionsClaimed : Bool
  estateRefactorSafetyClaimed : Bool
  pccCapitalImported : Bool
  cohomologyClaimed : Bool
  authorityEffect : AuthorityEffect
deriving DecidableEq, Repr

def scopeFence : ScopeFence where
  relationQuotientCoreMechanized := true
  fullActionProbeMorphismsClaimed := false
  targetContextCoverageClaimed := false
  partialActionsClaimed := false
  estateRefactorSafetyClaimed := false
  pccCapitalImported := false
  cohomologyClaimed := false
  authorityEffect := .none

theorem scopeFence_exact :
    scopeFence =
      { relationQuotientCoreMechanized := true
        fullActionProbeMorphismsClaimed := false
        targetContextCoverageClaimed := false
        partialActionsClaimed := false
        estateRefactorSafetyClaimed := false
        pccCapitalImported := false
        cohomologyClaimed := false
        authorityEffect := .none } :=
  rfl

theorem authority_effect_none : scopeFence.authorityEffect = .none :=
  rfl

#print axioms SysMorph.identity_comp
#print axioms SysMorph.comp_identity
#print axioms SysMorph.comp_assoc
#print axioms preserves_iff_exists_quotient_factor
#print axioms quotient_factor_unique
#print axioms preserves_iff_existsUnique_quotient_factor
#print axioms quotientMap_identity
#print axioms quotientMap_compose
#print axioms DescentFailure.no_quotient_factor
#print axioms DescentFailure.source_points_distinct
#print axioms DescentFailure.target_images_distinct
#print axioms preserves_of_subsingleton_source
#print axioms preserves_of_subsingleton_target
#print axioms observerDifference_zeroRel_iff
#print axioms fin2_source_zero
#print axioms fin2_target_nonzero
#print axioms fin2_identity_not_preserving
#print axioms fin2_identity_not_a_sysMorph
#print axioms fin2_identity_no_quotient_factor
#print axioms fin2_failure_coordinatewise_minimal
#print axioms ReturningActionWitness.toDescentFailure
#print axioms scopeFence_exact
#print axioms authority_effect_none

end ObserverFunctorialityW35
end OmegaWorld
