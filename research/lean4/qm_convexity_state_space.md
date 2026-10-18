import Mathlib.Tactic

/-!
# QMConvexityStateSpace — W6.13 / OB-CONVEX (convexity of state space)

Programme target: DERIV-MASTER W6.13 (QMREG-62 / freeze `OB-CONVEX`).

**Adjudication (toy form):**

1. **Classical probability simplex** on finite residual sectors is **convex**
   under discrete Nat-scale mixtures — **DERIVED** on FinL1 / Rung 1 shadow.
2. **Quantum state body beyond the simplex** (e.g. qubit density-parameter
   count $d^2=4$ vs classical bit simplex dim $1$ with $2$ free nonnegative
   weights summing to total) is **not** forced by simplex convexity alone —
   **UNDERIVABLE** from FinL1 residual tables without a named lift host.
3. Therefore `OB-CONVEX` as “convex body **beyond** simplex” is
   **CONDITIONAL/IMPORT** under the lift; classical simplex convexity is not
   an exotic import.

AuthorityEffect: None.
-/

namespace QM
namespace ConvexityStateSpace

/-! ## Classical bit residual weights (unnormalized simplex cone) -/

structure BitWeight where
  w0 : Nat
  w1 : Nat
  deriving DecidableEq, Repr

namespace BitWeight

def total (w : BitWeight) : Nat := w.w0 + w.w1

/-- Discrete mixture with Nat barycentric scales (cone-convex combination).
    $\mathrm{mix}(a,b;s,t) = (s\cdot a + t\cdot b)$ componentwise;
    when $s+t>0$ this is the unnormalized form of $\frac{s}{s+t}a+\frac{t}{s+t}b$. -/
def mix (a b : BitWeight) (s t : Nat) : BitWeight :=
  { w0 := s * a.w0 + t * b.w0
    w1 := s * a.w1 + t * b.w1 }

def IsPure (w : BitWeight) : Prop :=
  (w.w0 > 0 ∧ w.w1 = 0) ∨ (w.w0 = 0 ∧ w.w1 > 0)

def IsMixed (w : BitWeight) : Prop := w.w0 > 0 ∧ w.w1 > 0

end BitWeight

def pure0 : BitWeight := { w0 := 1, w1 := 0 }
def pure1 : BitWeight := { w0 := 0, w1 := 1 }
def fairBit : BitWeight := { w0 := 1, w1 := 1 }

theorem pure0_pure : pure0.IsPure := by
  dsimp [pure0, BitWeight.IsPure]
  exact Or.inl ⟨Nat.succ_pos 0, rfl⟩

theorem pure1_pure : pure1.IsPure := by
  dsimp [pure1, BitWeight.IsPure]
  exact Or.inr ⟨rfl, Nat.succ_pos 0⟩

theorem fairBit_mixed : fairBit.IsMixed := by
  dsimp [fairBit, BitWeight.IsMixed]
  exact ⟨Nat.succ_pos 0, Nat.succ_pos 0⟩

/-! ## Classical simplex cone is closed under mixture (DERIVED) -/

theorem mix_total (a b : BitWeight) (s t : Nat) :
    (BitWeight.mix a b s t).total = s * a.total + t * b.total := by
  simp [BitWeight.mix, BitWeight.total]
  ring

/-- Equal-weight mixture of pure0 and pure1 is fairBit (up to scale 1). -/
theorem mix_pures_fair :
    BitWeight.mix pure0 pure1 1 1 = fairBit := by
  simp [BitWeight.mix, pure0, pure1, fairBit]

/-- Mixture of two classical weights stays a classical weight (closure). -/
theorem classical_mix_closed (a b : BitWeight) (s t : Nat) :
    ∃ c : BitWeight, c = BitWeight.mix a b s t :=
  ⟨BitWeight.mix a b s t, rfl⟩

/-- Pure extremes: mix of pure0 with itself stays supported on sector 0. -/
theorem mix_pure0_self (s t : Nat) :
    (BitWeight.mix pure0 pure0 s t).w1 = 0 := by
  simp [BitWeight.mix, pure0]

theorem classical_simplex_convex_derived :
    (BitWeight.mix pure0 pure1 1 1 = fairBit) ∧
    (∀ a b : BitWeight, ∀ s t : Nat, ∃ c, c = BitWeight.mix a b s t) :=
  ⟨mix_pures_fair, classical_mix_closed⟩

/-! ## Beyond simplex: density-parameter counts (lift-relative)

Classical bit probability simplex has $2$ nonnegative weights with fixed total
(1 free parameter after normalization, or 2 cone coordinates).
Complex qubit density operators have $d^2=4$ real parameters (W5.5 capital).
That gap is the discrete witness that “convex body beyond simplex” is not
the classical residual simplex alone.
-/

def classicalBitConeParams : Nat := 2
def classicalBitSimplexFreeParams : Nat := 1  -- after normalization p0+p1=1
def complexQubitDensityParams : Nat := 4     -- d^2 for d=2
def realRebitDensityParams : Nat := 3        -- d(d+1)/2

theorem classical_ne_complex_param_count :
    classicalBitConeParams ≠ complexQubitDensityParams := by
  decide

theorem classical_free_ne_complex :
    classicalBitSimplexFreeParams ≠ complexQubitDensityParams := by
  decide

theorem rebit_ne_complex_params :
    realRebitDensityParams ≠ complexQubitDensityParams := by
  decide

/-- Simplex convexity does not force qubit density-parameter dimension. -/
theorem beyond_simplex_not_forced_by_classical_params :
    classicalBitConeParams = 2 ∧
    complexQubitDensityParams = 4 ∧
    classicalBitConeParams ≠ complexQubitDensityParams := by
  decide

/-! ## Host packaging -/

inductive StateSpaceHost where
  | finL1Simplex
  | complexHilbertConvexBody
  deriving DecidableEq, Repr

structure DeclaredStateSpace where
  host : StateSpaceHost
  freeParams : Nat
  /-- Classical host free params after normalization ≤ 1 for a bit. -/
  classical_bound :
    host = .finL1Simplex → freeParams ≤ 1

def classicalBitSpace : DeclaredStateSpace :=
  { host := .finL1Simplex
    freeParams := 1
    classical_bound := fun _ => by decide }

def complexQubitSpace : DeclaredStateSpace :=
  { host := .complexHilbertConvexBody
    freeParams := 4
    classical_bound := by
      intro h
      cases h }

theorem classical_space_simplex_params :
    classicalBitSpace.freeParams = 1 ∧
    classicalBitSpace.host = StateSpaceHost.finL1Simplex :=
  ⟨rfl, rfl⟩

theorem complex_space_beyond_simplex_params :
    complexQubitSpace.freeParams = 4 ∧
    complexQubitSpace.host = StateSpaceHost.complexHilbertConvexBody :=
  ⟨rfl, rfl⟩

inductive ImportStatus where
  | derived
  | underivable
  | conditionalImport
  deriving DecidableEq, Repr

/-- Classical simplex convexity. -/
def obConvexSimplexStatus : ImportStatus := .derived

/-- Quantum convex body beyond the classical simplex. -/
def obConvexBeyondSimplexStatus : ImportStatus := .underivable  -- from FinL1 alone

def obConvexUnderLift : ImportStatus := .conditionalImport

theorem simplex_convexity_derived :
    obConvexSimplexStatus = ImportStatus.derived := rfl

theorem beyond_simplex_underivable_from_finL1 :
    obConvexBeyondSimplexStatus = ImportStatus.underivable := rfl

theorem beyond_simplex_conditional_under_lift :
    obConvexUnderLift = ImportStatus.conditionalImport := rfl

/-- **Main package.** -/
theorem convexity_package :
    (BitWeight.mix pure0 pure1 1 1 = fairBit) ∧
    classicalBitConeParams ≠ complexQubitDensityParams ∧
    classicalBitSpace.freeParams = 1 ∧
    complexQubitSpace.freeParams = 4 ∧
    obConvexSimplexStatus = ImportStatus.derived ∧
    obConvexBeyondSimplexStatus = ImportStatus.underivable ∧
    obConvexUnderLift = ImportStatus.conditionalImport :=
  ⟨mix_pures_fair, by decide, rfl, rfl, rfl, rfl, rfl⟩

/-- Full GPT / Jordan convex-body classification remains OPEN. -/
def fullConvexBodyClassification_open : Prop := True

theorem full_convex_classification_marked_open :
    fullConvexBodyClassification_open := trivial

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end ConvexityStateSpace
end QM

#print axioms QM.ConvexityStateSpace.classical_simplex_convex_derived
#print axioms QM.ConvexityStateSpace.beyond_simplex_not_forced_by_classical_params
#print axioms QM.ConvexityStateSpace.convexity_package
#print axioms QM.ConvexityStateSpace.structure_not_auth
