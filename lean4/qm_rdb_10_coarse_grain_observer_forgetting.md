/-!
RDB-10: coarse-grained observer forgetting.

RDB-05 gives the quotient/marginal LGGR theorem. This file records the
diagonal residual-density version: a coarse observer may merge residual sectors
into one local diagnostic label while a hidden/global coordinate still
distinguishes the sectors.

This is the finite model behind "partial trace as observer forgetting" for
plan002. It is intentionally not a physical QM claim.
-/

namespace QM

namespace RDB10

/-- A coarse residual observer reads a local label from each residual sector and
may forget a hidden/global coordinate. -/
structure CoarseResidualObserver where
  Sector : Type
  Local : Type
  Hidden : Type
  localLabel : Sector -> Local
  hiddenLabel : Sector -> Hidden

def LocalDiagnosticGreen (obs : CoarseResidualObserver) : Prop :=
  ∀ x y : obs.Sector, obs.localLabel x = obs.localLabel y

def GlobalObstructionRed (obs : CoarseResidualObserver) : Prop :=
  ∃ x y : obs.Sector, obs.hiddenLabel x ≠ obs.hiddenLabel y

inductive TwoResidualSector where
  | left
  | right
deriving DecidableEq

def twoSectorCoarseObserver : CoarseResidualObserver where
  Sector := TwoResidualSector
  Local := Unit
  Hidden := Bool
  localLabel := fun _ => ()
  hiddenLabel := fun
    | TwoResidualSector.left => false
    | TwoResidualSector.right => true

theorem coarseObserver_local_green_global_red_witness :
    LocalDiagnosticGreen twoSectorCoarseObserver ∧
      GlobalObstructionRed twoSectorCoarseObserver := by
  constructor
  · intro x y
    cases twoSectorCoarseObserver.localLabel x
    cases twoSectorCoarseObserver.localLabel y
    rfl
  · refine ⟨TwoResidualSector.left, TwoResidualSector.right, ?_⟩
    intro h
    cases h

/-- Local diagnostic greenness under coarse-graining does not imply global
obstruction absence. -/
theorem not_localDiagnosticGreen_implies_not_globalRed :
    ¬ (∀ obs : CoarseResidualObserver,
      LocalDiagnosticGreen obs -> ¬ GlobalObstructionRed obs) := by
  intro h
  exact
    (h twoSectorCoarseObserver
      coarseObserver_local_green_global_red_witness.1)
        coarseObserver_local_green_global_red_witness.2

end RDB10

end QM

#print axioms QM.RDB10.coarseObserver_local_green_global_red_witness
#print axioms QM.RDB10.not_localDiagnosticGreen_implies_not_globalRed
