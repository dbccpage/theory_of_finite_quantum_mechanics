/-
  Corrected replica-additivity hierarchy for Paper 001.

  The paper's replica axiom says that a functional on finite edge sets is additive on
  disjoint unions. This module records the exact consequence used in the corrected
  claim ledger:

  * disjoint-replica additivity decomposes every finite value into singleton values;
  * singleton calibration identifies those values with one fixed local rule, hence the
  resulting sum is unweighted.

  No continuity, symmetry, positivity, projection, or quantum-mechanical assumptions
  enter these algebraic implications.
-/
import Mathlib.Algebra.BigOperators.Group.Finset.Basic

namespace ReplicaHierarchy

open scoped BigOperators

variable {ι R : Type*} [DecidableEq ι] [AddCancelCommMonoid R]

/-- A functional on finite replica sets is additive on disjoint unions. This is the
algebraic content of corrected axiom RE3. -/
def ReplicaAdditive (J : Finset ι → R) : Prop :=
  ∀ s t : Finset ι, Disjoint s t → J (s ∪ t) = J s + J t

/-- Disjoint-replica additivity forces decomposition into singleton contributions. -/
theorem sum_singletons_of_replicaAdditive (J : Finset ι → R)
    (hJ : ReplicaAdditive J) (s : Finset ι) :
    J s = Finset.sum s (fun e => J {e}) := by
  induction s using Finset.induction_on with
  | empty =>
      have hself : J ∅ = J ∅ + J ∅ := by
        simpa using hJ ∅ ∅ (by simp)
      have hzero : J ∅ = 0 := by
        apply add_left_cancel (a := J ∅)
        simpa using hself.symm
      simpa using hzero
  | @insert e s hes ih =>
      have hdisjoint : Disjoint ({e} : Finset ι) s := by
        exact Finset.disjoint_left.2 (by
          intro x hx_singleton hx_s
          have hxe : x = e := Finset.mem_singleton.1 hx_singleton
          subst x
          exact hes hx_s)
      calc
        J (insert e s) = J (({e} : Finset ι) ∪ s) := by simp
        _ = J {e} + J s := hJ {e} s hdisjoint
        _ = J {e} + Finset.sum s (fun x => J {x}) := by rw [ih]
        _ = Finset.sum (insert e s) (fun x => J {x}) := by rw [Finset.sum_insert hes]

/-- If every singleton is calibrated by the same local rule `j`, replica additivity gives
the corresponding unweighted finite sum. -/
theorem unweighted_sum_of_replicaAdditive_of_singleton_calibration
    (J : Finset ι → R) (j : ι → R)
    (hJ : ReplicaAdditive J) (hcal : ∀ e, J {e} = j e) (s : Finset ι) :
    J s = Finset.sum s j := by
  rw [sum_singletons_of_replicaAdditive J hJ s]
  exact Finset.sum_congr rfl (fun e _ => hcal e)

end ReplicaHierarchy

#print axioms ReplicaHierarchy.sum_singletons_of_replicaAdditive
#print axioms ReplicaHierarchy.unweighted_sum_of_replicaAdditive_of_singleton_calibration
