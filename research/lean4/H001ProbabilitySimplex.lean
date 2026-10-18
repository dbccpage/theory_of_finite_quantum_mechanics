/-
  H001 -- scaled-integer simplex shadow over reports. AuthorityEffect: None.
  Candidate only. Not PROVEN. Kind: LIFT RUNG.

  Claim identifier: HW-H001
  Source-paper contact: QM_020 (L1 sector weights), QM_121 rung
  "finite L1 sector weights". J011 trunk: weights live on the report
  quotient, not on the raw carrier.

  Target proposition
    Nonnegative integer weights at a declared positive scale over a
    finite report enumeration form an M-scaled integer simplex grid,
    not the ordinary rational/real probability simplex exactly. The
    mass carrier, nonnegativity, and normalization are three separate
    imports; none is supplied by bare unequal marks.

  Imports added at this rung
    Int as the exact mass carrier at declared scale M (an import).
    Nonnegativity. Normalization to total mass M.

    BOUNDARY (corrected 2026-08-19, review round 3): the host's Rat
    laws AS SHIPPED depend on Classical.choice (receipts printed in
    HWKernel), so assembling a dense mass carrier from the core
    lemmas as they stand pulls in choice. This is NOT an
    impossibility: `#print axioms` reports what the shipped proofs
    use, not what is necessary; a choice-free Q is reprovable
    (FRONTIER R5), and R is simply unavailable in this host. So a
    dense carrier is a priced IMPORT here, not inadmissible.
    Scaled-integer masses are the fragment the host supports
    choice-free; they are a modelling choice, not a forced one.
    A separate choice-free exact-fraction pack now lives in
    H001Rats (`fracPack`); this module keeps the integer grid.

  Theorem or counterexample
    pointMass packs at scale 1; a signed vector and an unnormalized
    vector are each excluded by exactly one named field (refusal:
    probability semantics are not supplied by bare unequal marks).

  Nonclaim boundary
    No claim that Int scaling, Q, or R is forced. No frequency or
    propensity interpretation is derived. L1 distance is defined,
    not selected over rivals.

  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import HWKernel

namespace FableHilbertWalk20260819.H001

open FableHilbertWalk20260819.HWKernel

/-- Scaled probability vector over an enumerated report set: exact
    integer weights, total mass equal to the declared scale. Every
    field is an import. -/
structure ScaledProb (Q : Type) (E : Enum Q) (M : Int) where
  w : Q → Int
  scale_pos : 0 < M
  nonneg : ∀ q : Q, 0 ≤ w q
  mass_eq : rsum intPack (E.elems.map w) = M

/-- Total mass of an arbitrary integer weight vector. -/
def mass {Q : Type} (E : Enum Q) (w : Q → Int) : Int :=
  rsum intPack (E.elems.map w)

/-- Absolute value, defined locally to keep the axiom footprint
    visible. -/
def iabs (a : Int) : Int :=
  if a < 0 then -a else a

/-- L1 distance between integer weight vectors. Defined, not
    selected: no claim that L1 is the canonical distance. -/
def l1dist {Q : Type} (E : Enum Q) (v w : Q → Int) : Int :=
  rsum intPack (E.elems.map (fun q => iabs (v q - w q)))

theorem iabs_zero : iabs 0 = 0 := by decide

theorem l1dist_self {Q : Type} (E : Enum Q) (v : Q → Int) :
    l1dist E v v = 0 := by
  unfold l1dist
  have h : E.elems.map (fun q => iabs (v q - v q)) =
      E.elems.map (fun _ => (0 : Int)) := by
    apply map_congr_mem
    intro q _
    rw [Int.sub_self, iabs_zero]
  rw [h]
  exact rsum_map_zero intPack E.elems

#print axioms l1dist_self

/-! ## Positive finite witness: the point mass on Bool, scale 1. -/

def pointW (q : Bool) : Int :=
  if q then 0 else 1

def pointMass : ScaledProb Bool enumBool 1 where
  w := pointW
  scale_pos := by decide
  nonneg := fun q => by cases q <;> decide
  mass_eq := by decide

#print axioms pointMass

/-! ## Refusal countermodels: each excluded by one named field. -/

/-- Signed weights: mass one holds, nonnegativity fails. -/
def signedW (q : Bool) : Int :=
  if q then 2 else -1

theorem signed_mass_one : mass enumBool signedW = 1 := by decide

theorem signed_not_nonneg : ¬(∀ q : Bool, 0 ≤ signedW q) := by
  intro h
  exact absurd (h false) (by decide)

#print axioms signed_not_nonneg

/-- Uniform weights at the wrong mass for scale 1. -/
def doubleW (_ : Bool) : Int := 1

theorem double_nonneg : ∀ q : Bool, 0 ≤ doubleW q := by decide

theorem double_mass_two : mass enumBool doubleW = 2 := by decide

theorem double_not_normalized : mass enumBool doubleW ≠ 1 := by decide

#print axioms double_not_normalized

/-- H001 punchline: the scaled simplex inhabits, and each constraint
    is a separate import with its own finite separator. -/
theorem probability_simplex :
    (pointMass.w = pointW) ∧
      mass enumBool signedW = 1 ∧
      ¬(∀ q : Bool, 0 ≤ signedW q) ∧
      (∀ q : Bool, 0 ≤ doubleW q) ∧
      mass enumBool doubleW ≠ 1 :=
  ⟨rfl, signed_mass_one, signed_not_nonneg, double_nonneg,
    double_not_normalized⟩

#print axioms probability_simplex

end FableHilbertWalk20260819.H001
