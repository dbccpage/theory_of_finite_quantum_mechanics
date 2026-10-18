
import PrimitiveDifference
import WorldObserverFunctoriality






namespace OmegaWorld
namespace ObserverDirectedColimitNoGoW84

open OmegaCore
open OmegaCore.PrimitiveDifference
open ObserverFunctorialityW35

universe u v


def asSystem {X : Type u} (P : PrimitiveDifference X Bool) :
    ObserverSystem where
  State := X
  difference := P

def ZeroRefines {X : Type u}
    (fine coarse : PrimitiveDifference X Bool) : Prop :=
  ∀ x y : X, fine.ZeroRel x y → coarse.ZeroRel x y

def SameZeroRelation {X : Type u}
    (left right : PrimitiveDifference X Bool) : Prop :=
  ∀ x y : X, left.ZeroRel x y ↔ right.ZeroRel x y

namespace ZeroRefines

theorem refl {X : Type u} (P : PrimitiveDifference X Bool) :
    ZeroRefines P P := by
  intro x y hxy
  exact hxy

theorem trans {X : Type u}
    {fine middle coarse : PrimitiveDifference X Bool}
    (hfm : ZeroRefines fine middle) (hmc : ZeroRefines middle coarse) :
    ZeroRefines fine coarse := by
  intro x y hxy
  exact hmc x y (hfm x y hxy)

end ZeroRefines

def reverseIdentityMorphism {X : Type u}
    {fine coarse : PrimitiveDifference X Bool}
    (href : ZeroRefines fine coarse) :
    SysMorph (asSystem fine) (asSystem coarse) where
  toFun := id
  preservesZeroRel := by
    intro x y hxy
    exact href x y hxy

theorem reverseIdentityMorphism_refl {X : Type u}
    (P : PrimitiveDifference X Bool) :
    reverseIdentityMorphism (ZeroRefines.refl P) =
      SysMorph.identity (asSystem P) := by
  apply SysMorph.ext
  rfl

theorem reverseIdentityMorphism_trans {X : Type u}
    {fine middle coarse : PrimitiveDifference X Bool}
    (hfm : ZeroRefines fine middle) (hmc : ZeroRefines middle coarse) :
    reverseIdentityMorphism (ZeroRefines.trans hfm hmc) =
      SysMorph.compose (reverseIdentityMorphism hmc)
        (reverseIdentityMorphism hfm) := by
  apply SysMorph.ext
  rfl

theorem reverse_unique_factor {X : Type u}
    {fine coarse : PrimitiveDifference X Bool}
    (href : ZeroRefines fine coarse) :
    UniqueQuotientFactor
      (S := asSystem fine) (T := asSystem coarse) id := by
  apply (preserves_iff_existsUnique_quotient_factor
    (S := asSystem fine) (T := asSystem coarse) id).mp
  intro x y hxy
  exact href x y hxy

theorem reverse_quotient_map_classOf {X : Type u}
    {fine coarse : PrimitiveDifference X Bool}
    (href : ZeroRefines fine coarse) (x : X) :
    quotientMap (reverseIdentityMorphism href)
        ((asSystem fine).classOf x) =
      (asSystem coarse).classOf x := by
  exact quotientMap_classOf (reverseIdentityMorphism href) x

theorem reverse_quotient_map_identity {X : Type u}
    (P : PrimitiveDifference X Bool) :
    quotientMap (reverseIdentityMorphism (ZeroRefines.refl P)) = id := by
  rw [reverseIdentityMorphism_refl]
  exact quotientMap_identity (asSystem P)

theorem reverse_quotient_map_compose {X : Type u}
    {fine middle coarse : PrimitiveDifference X Bool}
    (hfm : ZeroRefines fine middle) (hmc : ZeroRefines middle coarse) :
    quotientMap (reverseIdentityMorphism (ZeroRefines.trans hfm hmc)) =
      quotientMap (reverseIdentityMorphism hmc) ∘
        quotientMap (reverseIdentityMorphism hfm) := by
  rw [reverseIdentityMorphism_trans]
  exact quotientMap_compose (reverseIdentityMorphism hmc)
    (reverseIdentityMorphism hfm)

theorem forward_factor_iff_same {X : Type u}
    {fine coarse : PrimitiveDifference X Bool}
    (href : ZeroRefines fine coarse) :
    (∃ factor : (asSystem coarse).Residual → (asSystem fine).Residual,
        ∀ x : X,
          factor ((asSystem coarse).classOf x) =
            (asSystem fine).classOf x) ↔
      SameZeroRelation fine coarse := by
  constructor
  · intro hfactor
    have hfactor' :
        ∃ factor : (asSystem coarse).Residual → (asSystem fine).Residual,
          ∀ x : (asSystem coarse).State,
            factor ((asSystem coarse).classOf x) =
              (asSystem fine).classOf (id x) := by
      simpa [asSystem] using hfactor
    have hpres := (preserves_iff_exists_quotient_factor
      (S := asSystem coarse) (T := asSystem fine) id).mpr hfactor'
    intro x y
    exact ⟨href x y, hpres x y⟩
  · intro hsame
    have hpres : PreservesZeroRel
        (S := asSystem coarse) (T := asSystem fine) id := by
      intro x y hcoarse
      exact (hsame x y).mpr hcoarse
    have hfactor := (preserves_iff_exists_quotient_factor
      (S := asSystem coarse) (T := asSystem fine) id).mp hpres
    simpa [asSystem] using hfactor

theorem forward_unique_factor_iff_same {X : Type u}
    {fine coarse : PrimitiveDifference X Bool}
    (href : ZeroRefines fine coarse) :
    UniqueQuotientFactor
        (S := asSystem coarse) (T := asSystem fine) id ↔
      SameZeroRelation fine coarse := by
  constructor
  · intro hfactor
    have hpres :=
      (preserves_iff_existsUnique_quotient_factor
        (S := asSystem coarse) (T := asSystem fine) id).mpr hfactor
    intro x y
    exact ⟨href x y, hpres x y⟩
  · intro hsame
    apply (preserves_iff_existsUnique_quotient_factor
      (S := asSystem coarse) (T := asSystem fine) id).mp
    intro x y hcoarse
    exact (hsame x y).mpr hcoarse

structure StrictRefinement {X : Type u}
    (fine coarse : PrimitiveDifference X Bool) where
  refines : ZeroRefines fine coarse
  left : X
  right : X
  coarseZero : coarse.ZeroRel left right
  fineNonzero : ¬fine.ZeroRel left right

namespace StrictRefinement

theorem no_forward_unique_factor {X : Type u}
    {fine coarse : PrimitiveDifference X Bool}
    (witness : StrictRefinement fine coarse) :
    ¬UniqueQuotientFactor
      (S := asSystem coarse) (T := asSystem fine) id := by
  intro hfactor
  have hsame :=
    (forward_unique_factor_iff_same witness.refines).mp hfactor
  exact witness.fineNonzero
    ((hsame witness.left witness.right).mpr witness.coarseZero)

theorem no_forward_factor {X : Type u}
    {fine coarse : PrimitiveDifference X Bool}
    (witness : StrictRefinement fine coarse) :
    ¬(∃ factor : (asSystem coarse).Residual → (asSystem fine).Residual,
      ∀ x : X,
        factor ((asSystem coarse).classOf x) =
          (asSystem fine).classOf x) := by
  intro hfactor
  have hpres := (preserves_iff_exists_quotient_factor
    (S := asSystem coarse) (T := asSystem fine) id).mpr hfactor
  exact witness.fineNonzero
    (hpres witness.left witness.right witness.coarseZero)

theorem impossible_of_subsingleton {X : Type u} [Subsingleton X]
    {fine coarse : PrimitiveDifference X Bool} :
    ¬Nonempty (StrictRefinement fine coarse) := by
  rintro ⟨witness⟩
  have hxy : witness.left = witness.right := Subsingleton.elim _ _
  apply witness.fineNonzero
  rw [hxy]
  exact fine.zeroRel_refl _

end StrictRefinement


def fin2StrictRefinement :
    StrictRefinement (observerDifference fin2SeparatingObserve)
      (observerDifference fin2ConstantObserve) where
  refines := by
    intro x y _
    rw [observerDifference_zeroRel_iff]
    rfl
  left := (0 : Fin 2)
  right := (1 : Fin 2)
  coarseZero := fin2_source_zero
  fineNonzero := fin2_target_nonzero

theorem fin2_witness_points_distinct :
    fin2StrictRefinement.left ≠ fin2StrictRefinement.right := by
  decide

theorem fin2_coordinatewise_minimal :
    fin2IdentityFailure.left ≠ fin2IdentityFailure.right ∧
      fin2IdentityCandidate.toFun fin2IdentityFailure.left ≠
        fin2IdentityCandidate.toFun fin2IdentityFailure.right :=
  fin2_failure_coordinatewise_minimal

theorem fin2_no_forward_unique_factor :
    ¬UniqueQuotientFactor
      (S := asSystem (observerDifference fin2ConstantObserve))
      (T := asSystem (observerDifference fin2SeparatingObserve)) id :=
  fin2StrictRefinement.no_forward_unique_factor

theorem fin2_no_forward_commuting_factor :
    ¬(∃ factor : fin2ConstantSystem.Residual →
        fin2SeparatingSystem.Residual,
      ∀ x : fin2ConstantSystem.State,
        factor (fin2ConstantSystem.classOf x) =
          fin2SeparatingSystem.classOf (fin2IdentityCandidate.toFun x)) :=
  fin2_identity_no_quotient_factor


def allPairs (n : Nat) : List (Fin n × Fin n) :=
  (List.finRange n).flatMap fun x =>
    (List.finRange n).map fun y => (x, y)

theorem sum_replicate_nat (m n : Nat) :
    (List.replicate m n).sum = m * n := by
  induction m with
  | zero => simp
  | succ m ih =>
      change n + (List.replicate m n).sum = (m + 1) * n
      rw [ih]
      calc
        n + m * n = m * n + n := Nat.add_comm _ _
        _ = (m + 1) * n := (Nat.succ_mul m n).symm

theorem allPairs_length (n : Nat) : (allPairs n).length = n * n := by
  simp only [allPairs, List.length_flatMap, List.length_map,
    List.length_finRange]
  have hmap := @List.map_const (Fin n) Nat (List.finRange n) n
  change List.map (fun _ : Fin n => n) (List.finRange n) =
    List.replicate (List.finRange n).length n at hmap
  rw [hmap, sum_replicate_nat, List.length_finRange]

theorem allPairs_mem (n : Nat) (pair : Fin n × Fin n) :
    pair ∈ allPairs n := by
  rcases pair with ⟨x, y⟩
  simp [allPairs]

theorem filter_sublist_filter_of_imp
    {A : Type v} (p q : A → Bool) (values : List A)
    (himp : ∀ a, q a = true → p a = true) :
    (values.filter q).Sublist (values.filter p) := by
  induction values with
  | nil => exact List.Sublist.refl []
  | cons a values ih =>
      rw [List.filter_cons, List.filter_cons]
      by_cases hq : q a = true
      · have hp : p a = true := himp a hq
        rw [if_pos hq, if_pos hp]
        exact List.Sublist.cons_cons a ih
      · rw [if_neg hq]
        by_cases hp : p a = true
        · rw [if_pos hp]
          exact List.Sublist.cons a ih
        · rw [if_neg hp]
          exact ih

theorem filter_length_strict_of_imp_witness
    {A : Type v} (p q : A → Bool) (values : List A)
    (himp : ∀ a, q a = true → p a = true)
    (a : A) (ha : a ∈ values) (hp : p a = true) (hq : q a = false) :
    (values.filter q).length + 1 ≤ (values.filter p).length := by
  have hsub := filter_sublist_filter_of_imp p q values himp
  have hpa : a ∈ values.filter p := (List.mem_filter).2 ⟨ha, hp⟩
  have hnqa : a ∉ values.filter q := by
    intro hmem
    have hqt : q a = true := (List.mem_filter).1 hmem |>.2
    rw [hq] at hqt
    exact Bool.noConfusion hqt
  have hneq : values.filter q ≠ values.filter p := by
    intro heq
    apply hnqa
    rw [heq]
    exact hpa
  have hlenLe : (values.filter q).length ≤
      (values.filter p).length := hsub.length_le
  have hlenNe : ¬(values.filter q).length =
      (values.filter p).length := by
    intro hlen
    exact hneq (hsub.eq_of_length hlen)
  exact Nat.lt_iff_add_one_le.mp
    (Nat.lt_of_le_of_ne hlenLe hlenNe)

structure FiniteObserverChain (n steps : Nat) where
  stage : Nat → PrimitiveDifference (Fin n) Bool
  decideZero : Nat → Fin n → Fin n → Bool
  decideZero_spec : ∀ j x y,
    decideZero j x y = true ↔ (stage j).ZeroRel x y
  descends : ∀ j, j < steps → ∀ x y,
    (stage (j + 1)).ZeroRel x y → (stage j).ZeroRel x y
  strict : ∀ j, j < steps →
    ∃ x y, (stage j).ZeroRel x y ∧
      ¬(stage (j + 1)).ZeroRel x y

namespace FiniteObserverChain

def relatedPairs {n steps : Nat} (chain : FiniteObserverChain n steps)
    (j : Nat) : List (Fin n × Fin n) :=
  (allPairs n).filter fun pair =>
    chain.decideZero j pair.1 pair.2

def relatedPairCount {n steps : Nat} (chain : FiniteObserverChain n steps)
    (j : Nat) : Nat :=
  (chain.relatedPairs j).length

theorem relatedPairCount_le_sq {n steps : Nat}
    (chain : FiniteObserverChain n steps) (j : Nat) :
    chain.relatedPairCount j ≤ n * n := by
  have h := List.length_filter_le
    (fun pair : Fin n × Fin n =>
      chain.decideZero j pair.1 pair.2)
    (allPairs n)
  rw [allPairs_length] at h
  exact h

theorem relatedPairCount_step {n steps : Nat}
    (chain : FiniteObserverChain n steps)
    {j : Nat} (hj : j < steps) :
    chain.relatedPairCount (j + 1) + 1 ≤
      chain.relatedPairCount j := by
  rcases chain.strict j hj with ⟨x, y, hxy, hnxy⟩
  let p : Fin n × Fin n → Bool :=
    fun pair => chain.decideZero j pair.1 pair.2
  let q : Fin n × Fin n → Bool :=
    fun pair => chain.decideZero (j + 1) pair.1 pair.2
  have himp : ∀ pair, q pair = true → p pair = true := by
    intro pair hp
    apply (chain.decideZero_spec j pair.1 pair.2).2
    exact chain.descends j hj pair.1 pair.2
      ((chain.decideZero_spec (j + 1) pair.1 pair.2).1 hp)
  have hp : p (x, y) = true :=
    (chain.decideZero_spec j x y).2 hxy
  have hq : q (x, y) = false :=
    Bool.eq_false_iff.mpr fun htrue =>
      hnxy ((chain.decideZero_spec (j + 1) x y).1 htrue)
  exact filter_length_strict_of_imp_witness p q (allPairs n) himp
    (x, y) (allPairs_mem n (x, y)) hp hq

theorem strict_nat_budget (count : Nat → Nat) :
    ∀ steps : Nat,
      (∀ j, j < steps → count (j + 1) + 1 ≤ count j) →
      steps + count steps ≤ count 0 := by
  intro steps
  induction steps generalizing count with
  | zero => simp
  | succ steps ih =>
      intro hstep
      have htail : ∀ j, j < steps →
          count ((j + 1) + 1) + 1 ≤ count (j + 1) := by
        intro j hj
        exact hstep (j + 1) (by omega)
      have hih := ih (fun j => count (j + 1)) htail
      have hzero := hstep 0 (by omega)
      omega

theorem strict_refinement_pair_budget {n steps : Nat}
    (chain : FiniteObserverChain n steps) :
    steps + chain.relatedPairCount steps ≤ n * n := by
  have hbudget : steps + chain.relatedPairCount steps ≤
      chain.relatedPairCount 0 :=
    strict_nat_budget chain.relatedPairCount steps fun j hj =>
      chain.relatedPairCount_step hj
  exact Nat.le_trans hbudget (chain.relatedPairCount_le_sq 0)

theorem strict_refinement_steps_le_sq {n steps : Nat}
    (chain : FiniteObserverChain n steps) :
    steps ≤ n * n := by
  exact Nat.le_trans
    (Nat.le_add_right steps (chain.relatedPairCount steps))
    chain.strict_refinement_pair_budget

end FiniteObserverChain


def codeDifference {X : Type u} {O : Type v} [DecidableEq O]
    (code : X → O) : PrimitiveDifference X Bool where
  δ x y := if code x = code y then false else true
  Zero b := b = false
  zero_refl x := by simp
  zero_symm x y h := by
    by_cases hxy : code x = code y
    · simp [hxy.symm]
    · simp [hxy] at h
  zero_trans x y z hxy hyz := by
    by_cases h₁ : code x = code y
    · by_cases h₂ : code y = code z
      · have h₃ : code x = code z := h₁.trans h₂
        simp [h₃]
      · simp [h₂] at hyz
    · simp [h₁] at hxy

theorem codeDifference_zeroRel_iff
    {X : Type u} {O : Type v} [DecidableEq O]
    (code : X → O) (x y : X) :
    (codeDifference code).ZeroRel x y ↔ code x = code y := by
  change (if code x = code y then false else true) = false ↔
    code x = code y
  by_cases h : code x = code y <;> simp [h]

def stageCode (k x : Nat) : Nat := Nat.min x k

theorem stageCode_realizes_bounded_code {k q : Nat} (hq : q ≤ k) :
    stageCode k q = q :=
  Nat.min_eq_left hq

def PrefixRel (k x y : Nat) : Prop :=
  stageCode k x = stageCode k y

def prefixDifference (k : Nat) : PrimitiveDifference Nat Bool :=
  codeDifference (stageCode k)

theorem prefixDifference_zeroRel_iff (k x y : Nat) :
    (prefixDifference k).ZeroRel x y ↔ PrefixRel k x y := by
  exact codeDifference_zeroRel_iff (stageCode k) x y

theorem forget_compat (k x : Nat) :
    Nat.min (stageCode (k + 1) x) k = stageCode k x := by
  simp [stageCode, Nat.min_assoc]

theorem prefix_succ_refines (k x y : Nat) :
    PrefixRel (k + 1) x y → PrefixRel k x y := by
  intro h
  have h' := congrArg (fun q => Nat.min q k) h
  simpa [PrefixRel, forget_compat] using h'

theorem prefix_pair_related (k : Nat) :
    PrefixRel k k (k + 1) := by
  simp [PrefixRel, stageCode]

theorem prefix_pair_split_next (k : Nat) :
    ¬PrefixRel (k + 1) k (k + 1) := by
  simp [PrefixRel, stageCode]

def prefixStrictRefinement (k : Nat) :
    StrictRefinement (prefixDifference (k + 1))
      (prefixDifference k) where
  refines := by
    intro x y hxy
    rw [prefixDifference_zeroRel_iff] at hxy ⊢
    exact prefix_succ_refines k x y hxy
  left := k
  right := k + 1
  coarseZero := (prefixDifference_zeroRel_iff k k (k + 1)).2
    (prefix_pair_related k)
  fineNonzero := by
    rw [prefixDifference_zeroRel_iff]
    exact prefix_pair_split_next k

theorem prefix_reverse_unique_factor (k : Nat) :
    UniqueQuotientFactor
      (S := asSystem (prefixDifference (k + 1)))
      (T := asSystem (prefixDifference k)) id :=
  reverse_unique_factor (prefixStrictRefinement k).refines

theorem prefix_no_forward_factor (k : Nat) :
    ¬(∃ factor :
        (asSystem (prefixDifference k)).Residual →
          (asSystem (prefixDifference (k + 1))).Residual,
      ∀ x : Nat,
        factor ((asSystem (prefixDifference k)).classOf x) =
          (asSystem (prefixDifference (k + 1))).classOf x) :=
  (prefixStrictRefinement k).no_forward_factor

def FullPrefixRel (x y : Nat) : Prop :=
  ∀ k, PrefixRel k x y

theorem fullPrefixRel_iff_eq (x y : Nat) :
    FullPrefixRel x y ↔ x = y := by
  constructor
  · intro h
    have hxy := h (x + y + 1)
    have hx : Nat.min x (x + y + 1) = x :=
      Nat.min_eq_left (by omega)
    have hy : Nat.min y (x + y + 1) = y :=
      Nat.min_eq_left (by omega)
    simpa [PrefixRel, stageCode, hx, hy] using hxy
  · intro h
    subst y
    intro k
    rfl

def PrefixFaithful (k : Nat) : Prop :=
  ∀ x y, PrefixRel k x y → x = y

theorem no_finite_prefix_faithful (k : Nat) :
    ¬PrefixFaithful k := by
  intro h
  have heq := h k (k + 1) (prefix_pair_related k)
  omega

structure PrefixThread where
  value : Nat → Nat
  bounded : ∀ k, value k ≤ k
  coherent : ∀ k, Nat.min (value (k + 1)) k = value k

theorem PrefixThread.coordinate_realized (thread : PrefixThread) (k : Nat) :
    ∃ x : Nat, stageCode k x = thread.value k :=
  ⟨thread.value k, stageCode_realizes_bounded_code (thread.bounded k)⟩

def stateThread (x : Nat) : PrefixThread where
  value k := stageCode k x
  bounded k := Nat.min_le_right x k
  coherent k := forget_compat k x

def ghostThread : PrefixThread where
  value k := k
  bounded k := Nat.le_refl k
  coherent k := by
    change Nat.min (k + 1) k = k
    exact Nat.min_eq_right (Nat.le_succ k)

theorem stateThread_injective : Function.Injective stateThread := by
  intro x y hxy
  apply (fullPrefixRel_iff_eq x y).mp
  intro k
  exact congrArg (fun thread => thread.value k) hxy

theorem ghost_not_stateThread (x : Nat) :
    stateThread x ≠ ghostThread := by
  intro h
  have hvalue := congrArg (fun thread => thread.value (x + 1)) h
  change Nat.min x (x + 1) = x + 1 at hvalue
  have hmin : Nat.min x (x + 1) = x :=
    Nat.min_eq_left (by omega)
  rw [hmin] at hvalue
  omega

theorem ghost_unrealized :
    ¬∃ x : Nat, stateThread x = ghostThread := by
  rintro ⟨x, hx⟩
  exact ghost_not_stateThread x hx


structure ScopeFence where
  relationVarianceMechanized : Bool
  reverseQuotientLawsMechanized : Bool
  finitePairBudgetMechanized : Bool
  natPrefixNonattainmentMechanized : Bool
  frozenDirectedColimitClaimed : Bool
  categoricalInverseLimitClaimed : Bool
  inverseLimitUniversalPropertyClaimed : Bool
  fullActionProbeMorphismsClaimed : Bool
  topologyOrPhysicsClaimed : Bool
  estateIncrementalRecomputationClaimed : Bool
  authorityEffect : AuthorityEffect
deriving DecidableEq, Repr

def scopeFence : ScopeFence where
  relationVarianceMechanized := true
  reverseQuotientLawsMechanized := true
  finitePairBudgetMechanized := true
  natPrefixNonattainmentMechanized := true
  frozenDirectedColimitClaimed := false
  categoricalInverseLimitClaimed := false
  inverseLimitUniversalPropertyClaimed := false
  fullActionProbeMorphismsClaimed := false
  topologyOrPhysicsClaimed := false
  estateIncrementalRecomputationClaimed := false
  authorityEffect := .none

theorem scopeFence_exact :
    scopeFence =
      { relationVarianceMechanized := true
        reverseQuotientLawsMechanized := true
        finitePairBudgetMechanized := true
        natPrefixNonattainmentMechanized := true
        frozenDirectedColimitClaimed := false
        categoricalInverseLimitClaimed := false
        inverseLimitUniversalPropertyClaimed := false
        fullActionProbeMorphismsClaimed := false
        topologyOrPhysicsClaimed := false
        estateIncrementalRecomputationClaimed := false
        authorityEffect := .none } :=
  rfl

theorem authority_effect_none :
    scopeFence.authorityEffect = .none :=
  rfl

#print axioms ZeroRefines.trans
#print axioms reverse_unique_factor
#print axioms reverse_quotient_map_identity
#print axioms reverse_quotient_map_compose
#print axioms forward_factor_iff_same
#print axioms forward_unique_factor_iff_same
#print axioms StrictRefinement.no_forward_factor
#print axioms StrictRefinement.impossible_of_subsingleton
#print axioms fin2_no_forward_commuting_factor
#print axioms fin2_coordinatewise_minimal
#print axioms FiniteObserverChain.strict_refinement_pair_budget
#print axioms FiniteObserverChain.strict_refinement_steps_le_sq
#print axioms codeDifference_zeroRel_iff
#print axioms prefix_reverse_unique_factor
#print axioms prefix_no_forward_factor
#print axioms fullPrefixRel_iff_eq
#print axioms no_finite_prefix_faithful
#print axioms PrefixThread.coordinate_realized
#print axioms stateThread_injective
#print axioms ghost_unrealized
#print axioms scopeFence_exact
#print axioms authority_effect_none

end ObserverDirectedColimitNoGoW84
end OmegaWorld

private def l5aProvenance : String :=
  "Origin: lean4/WorldObserverDirectedColimitNoGo.lean Claim: refl AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
