




namespace ObserverWorld
namespace FiniteToInfiniteQ11

inductive Q11AuthorityEffect where
  | none
  deriving DecidableEq

inductive Atom16 where
  | a00 | a01 | a02 | a03
  | a04 | a05 | a06 | a07
  | a08 | a09 | a10 | a11
  | a12 | a13 | a14 | a15
  deriving DecidableEq

def atomIndex : Atom16 -> Nat
  | .a00 => 0
  | .a01 => 1
  | .a02 => 2
  | .a03 => 3
  | .a04 => 4
  | .a05 => 5
  | .a06 => 6
  | .a07 => 7
  | .a08 => 8
  | .a09 => 9
  | .a10 => 10
  | .a11 => 11
  | .a12 => 12
  | .a13 => 13
  | .a14 => 14
  | .a15 => 15

inductive Window where
  | one
  | two
  | four
  | eight
  | sixteen
  deriving DecidableEq

def windowRank : Window -> Nat
  | .one => 0
  | .two => 1
  | .four => 2
  | .eight => 3
  | .sixteen => 4

def windowCapacity : Window -> Nat
  | .one => 1
  | .two => 2
  | .four => 4
  | .eight => 8
  | .sixteen => 16

def WindowLE (source target : Window) : Prop :=
  windowRank source <= windowRank target

def prefixContains (window : Window) (atom : Atom16) : Bool :=
  decide (atomIndex atom < windowCapacity window)

def indicator (value : Bool) : Nat := if value then 1 else 0

def countAtoms (membership : Atom16 -> Bool) : Nat :=
  indicator (membership .a00) + indicator (membership .a01) +
  indicator (membership .a02) + indicator (membership .a03) +
  indicator (membership .a04) + indicator (membership .a05) +
  indicator (membership .a06) + indicator (membership .a07) +
  indicator (membership .a08) + indicator (membership .a09) +
  indicator (membership .a10) + indicator (membership .a11) +
  indicator (membership .a12) + indicator (membership .a13) +
  indicator (membership .a14) + indicator (membership .a15)

theorem prefix_cardinality (window : Window) :
    countAtoms (prefixContains window) = windowCapacity window := by
  cases window <;> decide

theorem prefix_conservative (source target : Window) (atom : Atom16) :
    WindowLE source target ->
      prefixContains source atom = true ->
        prefixContains target atom = true := by
  intro order member
  cases source <;> cases target <;> cases atom <;>
    simp [WindowLE, windowRank, prefixContains, atomIndex, windowCapacity]
      at order member ⊢

theorem final_prefix_covers (atom : Atom16) :
    prefixContains .sixteen atom = true := by
  cases atom <;> decide

structure PrefixPresentation where
  window : Window
  membership : Atom16 -> Bool
  membershipIsDeclared : membership = prefixContains window
  cardinality : countAtoms membership = windowCapacity window

def geometricPrefix (window : Window) : PrefixPresentation where
  window := window
  membership := prefixContains window
  membershipIsDeclared := rfl
  cardinality := prefix_cardinality window

def observerPrice : Window -> Nat
  | .one => 0
  | .two => 8
  | .four => 12
  | .eight => 14
  | .sixteen => 15

def observerError : Window -> Nat
  | .one => 16
  | .two => 8
  | .four => 4
  | .eight => 2
  | .sixteen => 1

theorem price_plus_error (window : Window) :
    observerPrice window + observerError window = 16 := by
  cases window <;> decide

inductive ProperSuccessor : Window -> Window -> Prop where
  | oneTwo : ProperSuccessor .one .two
  | twoFour : ProperSuccessor .two .four
  | fourEight : ProperSuccessor .four .eight
  | eightSixteen : ProperSuccessor .eight .sixteen

theorem geometric_error_halves {source target : Window}
    (step : ProperSuccessor source target) :
    observerError source = 2 * observerError target := by
  cases step <;> rfl

theorem geometric_capacity_doubles {source target : Window}
    (step : ProperSuccessor source target) :
    windowCapacity target = 2 * windowCapacity source := by
  cases step <;> rfl

inductive Precision where
  | half
  | quarter
  | eighth
  deriving DecidableEq

def tolerance : Precision -> Nat
  | .half => 8
  | .quarter => 4
  | .eighth => 2

def modulus : Precision -> Window
  | .half => .two
  | .quarter => .four
  | .eighth => .eight

def absDiff (left right : Nat) : Nat :=
  (left - right) + (right - left)

theorem finite_error_modulus (precision : Precision) (window : Window) :
    WindowLE (modulus precision) window ->
      observerError window <= tolerance precision := by
  intro tail
  cases precision <;> cases window <;>
    simp [WindowLE, windowRank, modulus, observerError, tolerance] at tail ⊢

theorem finite_cauchy_modulus (precision : Precision)
    (left right : Window) :
    WindowLE (modulus precision) left ->
      WindowLE (modulus precision) right ->
        absDiff (observerPrice left) (observerPrice right) <=
          tolerance precision := by
  intro leftTail rightTail
  cases precision <;> cases left <;> cases right <;>
    simp [WindowLE, windowRank, modulus, observerPrice, absDiff, tolerance]
      at leftTail rightTail ⊢

theorem half_modulus_is_nontrivial :
    WindowLE (modulus .half) .two /\
      WindowLE (modulus .half) .sixteen /\
      observerPrice .two ≠ observerPrice .sixteen /\
      absDiff (observerPrice .two) (observerPrice .sixteen) <=
        tolerance .half := by
  simp [WindowLE, windowRank, modulus, observerPrice, absDiff, tolerance]

inductive Polarity where
  | signal
  | null
  deriving DecidableEq

abbrev Point32 := Polarity × Atom16

def balancedMid (point : Point32) : Bool :=
  decide (atomIndex point.2 < 8)

def sparseMid : Point32 -> Bool
  | (.signal, _) => true
  | (.null, _) => false

def fullCarrier (_point : Point32) : Bool := true

def countPolarity (polarity : Polarity)
    (membership : Point32 -> Bool) : Nat :=
  indicator (membership (polarity, .a00)) +
  indicator (membership (polarity, .a01)) +
  indicator (membership (polarity, .a02)) +
  indicator (membership (polarity, .a03)) +
  indicator (membership (polarity, .a04)) +
  indicator (membership (polarity, .a05)) +
  indicator (membership (polarity, .a06)) +
  indicator (membership (polarity, .a07)) +
  indicator (membership (polarity, .a08)) +
  indicator (membership (polarity, .a09)) +
  indicator (membership (polarity, .a10)) +
  indicator (membership (polarity, .a11)) +
  indicator (membership (polarity, .a12)) +
  indicator (membership (polarity, .a13)) +
  indicator (membership (polarity, .a14)) +
  indicator (membership (polarity, .a15))

def pointCount (membership : Point32 -> Bool) : Nat :=
  countPolarity .signal membership + countPolarity .null membership

def signalCount (membership : Point32 -> Bool) : Nat :=
  countPolarity .signal membership

theorem balanced_mid_cardinality : pointCount balancedMid = 16 := by
  decide

theorem sparse_mid_cardinality : pointCount sparseMid = 16 := by
  decide

theorem balanced_mid_signal_count : signalCount balancedMid = 8 := by
  decide

theorem sparse_mid_signal_count : signalCount sparseMid = 16 := by
  decide

theorem full_carrier_cardinality : pointCount fullCarrier = 32 := by
  decide

theorem full_carrier_signal_count : signalCount fullCarrier = 16 := by
  decide

theorem balanced_mid_embeds_full (point : Point32) :
    balancedMid point = true -> fullCarrier point = true := by
  intro _membership
  rfl

theorem sparse_mid_embeds_full (point : Point32) :
    sparseMid point = true -> fullCarrier point = true := by
  intro _membership
  rfl

theorem balanced_sparse_observer_dependence :
    pointCount balancedMid = pointCount sparseMid /\
      signalCount balancedMid ≠ signalCount sparseMid /\
      absDiff (signalCount balancedMid) (signalCount sparseMid) = 8 := by
  decide

structure FiniteExhaustionDependenceWitness where
  balanced : Point32 -> Bool
  sparse : Point32 -> Bool
  commonFinal : Point32 -> Bool
  balancedIsDeclared : balanced = balancedMid
  sparseIsDeclared : sparse = sparseMid
  finalIsDeclared : commonFinal = fullCarrier
  matchedMidCardinality : pointCount balanced = pointCount sparse
  differentMidObserver : signalCount balanced ≠ signalCount sparse
  exactObserverDifference :
    absDiff (signalCount balanced) (signalCount sparse) = 8
  balancedConservative : forall point,
    balanced point = true -> commonFinal point = true
  sparseConservative : forall point,
    sparse point = true -> commonFinal point = true
  commonFinalCardinality : pointCount commonFinal = 32
  commonFinalSignalCount : signalCount commonFinal = 16
  infiniteLimitClaimed : Bool
  infiniteLimitNotClaimed : infiniteLimitClaimed = false
  authorityEffect : Q11AuthorityEffect
  authorityNone : authorityEffect = .none

def finiteExhaustionDependenceWitness :
    FiniteExhaustionDependenceWitness where
  balanced := balancedMid
  sparse := sparseMid
  commonFinal := fullCarrier
  balancedIsDeclared := rfl
  sparseIsDeclared := rfl
  finalIsDeclared := rfl
  matchedMidCardinality := by decide
  differentMidObserver := by decide
  exactObserverDifference := by decide
  balancedConservative := balanced_mid_embeds_full
  sparseConservative := sparse_mid_embeds_full
  commonFinalCardinality := full_carrier_cardinality
  commonFinalSignalCount := full_carrier_signal_count
  infiniteLimitClaimed := false
  infiniteLimitNotClaimed := rfl
  authorityEffect := .none
  authorityNone := rfl

structure FiniteToInfiniteSlice where
  prefixFamily : Window -> PrefixPresentation
  prefixFamilyIsDeclared : prefixFamily = geometricPrefix
  conservative : forall source target atom,
    WindowLE source target ->
      (prefixFamily source).membership atom = true ->
        (prefixFamily target).membership atom = true
  finiteCoverage : forall atom,
    (prefixFamily .sixteen).membership atom = true
  exactPriceError : forall window,
    observerPrice window + observerError window = 16
  geometricCapacity : forall {source target},
    ProperSuccessor source target ->
      windowCapacity target = 2 * windowCapacity source
  geometricError : forall {source target},
    ProperSuccessor source target ->
      observerError source = 2 * observerError target
  errorModulus : forall precision window,
    WindowLE (modulus precision) window ->
      observerError window <= tolerance precision
  cauchyModulus : forall precision left right,
    WindowLE (modulus precision) left ->
      WindowLE (modulus precision) right ->
        absDiff (observerPrice left) (observerPrice right) <=
          tolerance precision
  dependence : FiniteExhaustionDependenceWitness
  completionHostImported : Bool
  compactnessImported : Bool
  coercivityImported : Bool
  generalLimitClaimed : Bool
  exhaustionIndependenceClaimed : Bool
  completionHostOpen : completionHostImported = false
  compactnessOpen : compactnessImported = false
  coercivityOpen : coercivityImported = false
  generalLimitOpen : generalLimitClaimed = false
  exhaustionIndependenceOpen : exhaustionIndependenceClaimed = false
  authorityEffect : Q11AuthorityEffect
  authorityNone : authorityEffect = .none

def finiteToInfiniteSlice : FiniteToInfiniteSlice where
  prefixFamily := geometricPrefix
  prefixFamilyIsDeclared := rfl
  conservative := by
    intro source target atom order member
    exact prefix_conservative source target atom order member
  finiteCoverage := final_prefix_covers
  exactPriceError := price_plus_error
  geometricCapacity := geometric_capacity_doubles
  geometricError := geometric_error_halves
  errorModulus := finite_error_modulus
  cauchyModulus := finite_cauchy_modulus
  dependence := finiteExhaustionDependenceWitness
  completionHostImported := false
  compactnessImported := false
  coercivityImported := false
  generalLimitClaimed := false
  exhaustionIndependenceClaimed := false
  completionHostOpen := rfl
  compactnessOpen := rfl
  coercivityOpen := rfl
  generalLimitOpen := rfl
  exhaustionIndependenceOpen := rfl
  authorityEffect := .none
  authorityNone := rfl

#print axioms prefix_conservative
#print axioms geometric_capacity_doubles
#print axioms geometric_error_halves
#print axioms finite_error_modulus
#print axioms finite_cauchy_modulus
#print axioms half_modulus_is_nontrivial
#print axioms balanced_sparse_observer_dependence
#print axioms finiteExhaustionDependenceWitness
#print axioms finiteToInfiniteSlice

end FiniteToInfiniteQ11
end ObserverWorld

private def l5aProvenance : String :=
  "Origin: lean4/WorldFiniteToInfinite.lean Claim: prefix_cardinality AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
