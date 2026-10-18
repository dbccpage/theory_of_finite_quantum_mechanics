/-
  H015 -- irreversible dynamics fork. AuthorityEffect: None.
  Candidate only. Not PROVEN. Kind: IMPORT BOUNDARY.

  Claim identifier: HW-H015
  Source-paper contact: QM_203 and QM_205 (audited as proposals).
  Work order hard obligation 8. H003 collapse countermodel below.

  Target proposition
    A non-bijective report update has NO form-preserving
    implementation acting the same way on the declared basis
    (obligation 8, proved from two basis values and one inner
    product, no linearity assumption needed). Dilating instead is
    possible but not canonical: two distinct reversible ambient
    dynamics induce the same reduced report dynamics.

  Imports added at this rung
    The fork itself: refuse isometric (unitary-style) realization, or import an
    environment and a dilation choice, or import a channel class.
    Each option is priced; none is taken.

  Theorem or counterexample
    collapse_no_isometry: no sesq-preserving map sends both basis
    vectors to delta_false (obligation 8).
    dilations_distinct: identity-on-reports is induced by two
    distinct reversible dynamics on the extended carrier.

  Nonclaim boundary
    No CPTP machinery: channels are an import this host does not
    contain. No claim that dilation is impossible -- only that a
    selected dilation is not canonical without further structure.

  AuthorityEffect: None
-/

import HWKernel
import H003ReversibilityGate
import H004FreeLinearization
import H005InnerProductAdmission

namespace FableHilbertWalk20260819.H015

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H003 (Reversible collapse collapse_not_reversible)
open FableHilbertWalk20260819.H004
open FableHilbertWalk20260819.H005 (sesq)

/-- Obligation 8: no form-preserving map implements the collapse on
    the declared basis. Two basis values and one pairing suffice;
    linearity is not even needed. -/
theorem collapse_no_isometry :
    ¬ ∃ U : Vec Int Bool → Vec Int Bool,
      (∀ u v : Vec Int Bool,
        sesq intPack enumBool (U u) (U v) = sesq intPack enumBool u v) ∧
      U (delta intPack false) = delta intPack false ∧
      U (delta intPack true) = delta intPack false := by
  intro h
  rcases h with ⟨U, hiso, hf, ht⟩
  have h1 := hiso (delta intPack false) (delta intPack true)
  rw [hf, ht] at h1
  have h2 : sesq intPack enumBool (delta intPack false)
      (delta intPack false) = 1 := by decide
  have h3 : sesq intPack enumBool (delta intPack false)
      (delta intPack true) = 0 := by decide
  rw [h2, h3] at h1
  cases h1

#print axioms collapse_no_isometry

/-! ## Dilation non-uniqueness: same reduced dynamics, two distinct
    reversible ambient dynamics. -/

def dil1 (x : Bool × Bool) : Bool × Bool := x

def dil2 (x : Bool × Bool) : Bool × Bool := (x.1, !x.2)

theorem dil1_reversible : ∀ x, dil1 (dil1 x) = x := fun _ => rfl

theorem dil2_reversible : ∀ a b : Bool, dil2 (dil2 (a, b)) = (a, b) := by
  decide

/-- Both dilations reduce to the identity on reports. -/
theorem same_reduction :
    ∀ a b : Bool, (dil1 (a, b)).1 = (dil2 (a, b)).1 := by
  decide

#print axioms same_reduction

theorem dilations_distinct : ¬(∀ a b : Bool, dil1 (a, b) = dil2 (a, b)) := by
  decide

#print axioms dilations_distinct

/-- H015 punchline: irreversibility forces the fork -- no isometric
    realization on the same basis, and dilation is not canonical. -/
theorem irreversible_fork :
    ¬ Nonempty (Reversible collapse) ∧
      (¬ ∃ U : Vec Int Bool → Vec Int Bool,
        (∀ u v : Vec Int Bool,
          sesq intPack enumBool (U u) (U v) =
            sesq intPack enumBool u v) ∧
        U (delta intPack false) = delta intPack false ∧
        U (delta intPack true) = delta intPack false) ∧
      (∀ a b : Bool, (dil1 (a, b)).1 = (dil2 (a, b)).1) ∧
      ¬(∀ a b : Bool, dil1 (a, b) = dil2 (a, b)) :=
  ⟨collapse_not_reversible, collapse_no_isometry,
    same_reduction, dilations_distinct⟩

#print axioms irreversible_fork

end FableHilbertWalk20260819.H015
