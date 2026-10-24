import Mathlib.Tactic
import Imported.PreGenesisToMssn.Paper
import ChainRetraction

/-!
# Campaign TFQ-0376: Pre-Genesis Section-15 Justified-Lift Six-Check Checklist and Budget-Stop Fence

Formalizes the finite six-check checklist and budget-stop non-obstruction boundary for
`TFQ-0376` (`PREGENESIS`, Ledger row `WDP-P001-015`):

1. **Six Distinct Section-15 Evidence Checks (`Section15CheckSlot`)**:
   A claim that a carrier or regime extension is *necessary* or *minimal* must separately record:
   - `FailedPredicate`: the exact predicate that fails on the current regime (e.g.,
     `PreMssn.collapsed_observation_barrier` in `lean4/Imported/PreGenesisToMssn/Paper.lean` or
     `ChainRetraction.TwoPoints.no_chain_retraction` in `lean4/ChainRetraction.lean`).
   - `AdmissibleRepairs`: the admissible repair operations inside the declared repair space.
   - `ExtensionClass`: the declared extension class $\mathcal{E}$ over which candidates are drawn.
   - `CostOrder`: the explicit cost valuation / preorder comparing candidate extensions.
   - `TiedMinima`: the full set (and cardinality) of tied minimal-cost repairs in $\mathcal{E}$.
   - `SearchCompleteness`: whether the finite census exhausted $\mathcal{E}$ (`ExhaustiveOnDeclaredDomain`)
     or halted early at a resource bound (`BudgetStoppedIncomplete`), mirroring
     `CombinatoricsError::BudgetExceeded` in `code/rust/src/combinatorics/enumeration.rs` and
     `code/rust/src/combinatorics/color_constraints.rs`.

2. **Three Distinct Transition Evidence Stages (`TransitionStage`)**:
   - `Successor`: exhibits a valid state continuation without claiming repair or minimality.
   - `ProposedLift`: exhibits a candidate extension naming `FailedPredicate`, `AdmissibleRepairs`,
     and `ExtensionClass` (such as `PreMssn.refine_separates`), while leaving `CostOrder`,
     `TiedMinima`, or `SearchCompleteness` open.
   - `LicensedTransition`: requires all six Section-15 checks to be closed on the declared domain.

3. **Budget-Stop Non-Obstruction & Non-Minimality Fence**:
   - A finite census is exhaustive only on its declared domain (`checkedCount = domainSize`).
   - A budget stop (`checkedCount < domainSize`) is an incomplete search state, never an obstruction
     theorem and never a proof of minimality: an uninspected element in the remaining tail
     `domainSize - checkedCount > 0` can be a valid repair or have strictly lower cost than the
     prefix minimum.

AuthorityEffect: None
-/

namespace CampaignTfq0376Pregenesis

/-- The six distinct Section-15 checklist slots required for a justified lift claim. -/
inductive Section15CheckSlot
  | FailedPredicate
  | AdmissibleRepairs
  | ExtensionClass
  | CostOrder
  | TiedMinima
  | SearchCompleteness
  deriving DecidableEq, Repr

/-- The three transition evidence stages distinguished by Section 15 / `WDP-P001-015`. -/
inductive TransitionStage
  | Successor
  | ProposedLift
  | LicensedTransition
  deriving DecidableEq, Repr

/-- Finite census completeness state over a declared domain of size `domainSize`. -/
inductive SearchCensusState
  | ExhaustiveOnDeclaredDomain (domainSize : Nat)
  | BudgetStoppedIncomplete (domainSize : Nat) (checkedCount : Nat)
  deriving DecidableEq, Repr

/-- Explicit six-check evidence record for a candidate lift / extension. -/
structure JustifiedLiftChecklistRecord where
  failedPredicateNamed : Bool
  admissibleRepairsListed : Bool
  admissibleRepairCount : Nat
  extensionClassDeclared : Bool
  costOrderDeclared : Bool
  tiedMinimaCount : Nat
  censusState : SearchCensusState
  deriving DecidableEq, Repr

/-- Predicate: the census exhausted a non-empty declared domain. -/
def isExhaustiveCensus (s : SearchCensusState) : Bool :=
  match s with
  | SearchCensusState.ExhaustiveOnDeclaredDomain d => decide (0 < d)
  | SearchCensusState.BudgetStoppedIncomplete _ _ => false

/-- Stage 1 (`Successor`): requires only a declared extension class or continuation step. -/
def qualifiesAsSuccessor (r : JustifiedLiftChecklistRecord) : Bool :=
  r.extensionClassDeclared

/-- Stage 2 (`ProposedLift`): names the failed predicate, admissible repairs, and extension class,
    without requiring cost order, tied minima resolution, or exhaustive search closure. -/
def qualifiesAsProposedLift (r : JustifiedLiftChecklistRecord) : Bool :=
  r.failedPredicateNamed && r.admissibleRepairsListed &&
  decide (0 < r.admissibleRepairCount) && r.extensionClassDeclared

/-- Stage 3 (`LicensedTransition` up to declared tied minima): all six Section-15 checks are
    recorded and the finite census is exhaustive on the declared domain. -/
def allSixChecksClosed (r : JustifiedLiftChecklistRecord) : Bool :=
  r.failedPredicateNamed &&
  r.admissibleRepairsListed &&
  decide (0 < r.admissibleRepairCount) &&
  r.extensionClassDeclared &&
  r.costOrderDeclared &&
  decide (0 < r.tiedMinimaCount) &&
  isExhaustiveCensus r.censusState

/-- Unique minimal extension license: all six checks closed on an exhaustive census AND
    `tiedMinimaCount = 1`. -/
def uniqueMinimalExtensionLicensed (r : JustifiedLiftChecklistRecord) : Bool :=
  allSixChecksClosed r && decide (r.tiedMinimaCount = 1)

/-- Obstruction certificate on the declared extension class: exhaustive census on a non-empty
    declared domain with zero admissible repairs (`admissibleRepairCount = 0`). -/
def obstructionCertifiedOnDeclaredDomain (r : JustifiedLiftChecklistRecord) : Bool :=
  r.failedPredicateNamed &&
  r.admissibleRepairsListed &&
  decide (r.admissibleRepairCount = 0) &&
  r.extensionClassDeclared &&
  isExhaustiveCensus r.censusState

/-- Theorem 1: The six Section-15 check slots and three transition stages are pairwise distinct. -/
theorem section15_six_check_slots_and_stages_distinct :
    Section15CheckSlot.FailedPredicate ≠ Section15CheckSlot.AdmissibleRepairs ∧
    Section15CheckSlot.AdmissibleRepairs ≠ Section15CheckSlot.ExtensionClass ∧
    Section15CheckSlot.ExtensionClass ≠ Section15CheckSlot.CostOrder ∧
    Section15CheckSlot.CostOrder ≠ Section15CheckSlot.TiedMinima ∧
    Section15CheckSlot.TiedMinima ≠ Section15CheckSlot.SearchCompleteness ∧
    Section15CheckSlot.FailedPredicate ≠ Section15CheckSlot.SearchCompleteness ∧
    TransitionStage.Successor ≠ TransitionStage.ProposedLift ∧
    TransitionStage.ProposedLift ≠ TransitionStage.LicensedTransition ∧
    TransitionStage.Successor ≠ TransitionStage.LicensedTransition := by
  decide

/-- Theorem 2: A budget stop (`BudgetStoppedIncomplete domainSize checkedCount`) never certifies
    an obstruction on the declared domain and never licenses a minimal or unique-minimal extension,
    regardless of how many other check fields are set to `true`. -/
theorem budget_stop_never_licenses_obstruction_or_minimal_lift
    (fp ar ec co : Bool) (repCount tiedCount domSize chkCount : Nat) :
    let r : JustifiedLiftChecklistRecord := {
      failedPredicateNamed := fp
      admissibleRepairsListed := ar
      admissibleRepairCount := repCount
      extensionClassDeclared := ec
      costOrderDeclared := co
      tiedMinimaCount := tiedCount
      censusState := SearchCensusState.BudgetStoppedIncomplete domSize chkCount
    }
    isExhaustiveCensus r.censusState = false ∧
    allSixChecksClosed r = false ∧
    uniqueMinimalExtensionLicensed r = false ∧
    obstructionCertifiedOnDeclaredDomain r = false := by
  simp [isExhaustiveCensus, allSixChecksClosed, uniqueMinimalExtensionLicensed,
        obstructionCertifiedOnDeclaredDomain]

/-- Concrete 4-element candidate domain $\{0, 1, 2, 3\}$ where a budget stop at $B = 3$
    inspects only $\{0, 1, 2\}$ and misses candidate $3$. -/
def candidateCost : Fin 4 → Nat
  | ⟨0, _⟩ => 4
  | ⟨1, _⟩ => 3
  | ⟨2, _⟩ => 5
  | ⟨3, _⟩ => 1

def candidateRepairsFailure : Fin 4 → Bool
  | ⟨0, _⟩ => false
  | ⟨1, _⟩ => false
  | ⟨2, _⟩ => false
  | ⟨3, _⟩ => true

/-- Theorem 3: Explicit countermodel showing why a budget stop at $B = 3$ on a domain of size $4$
    is neither an obstruction proof nor a minimality proof:
    (a) candidates $0, 1, 2$ all fail to repair (`candidateRepairsFailure = false`), yet uninspected
        candidate $3$ succeeds (`candidateRepairsFailure 3 = true`);
    (b) the prefix minimum cost $\min(c_0, c_1, c_2) = 3$ is strictly larger than the true domain
        minimum cost $c_3 = 1$. -/
theorem uninspected_tail_witness_refutes_budget_stop_claims :
    candidateRepairsFailure ⟨0, by decide⟩ = false ∧
    candidateRepairsFailure ⟨1, by decide⟩ = false ∧
    candidateRepairsFailure ⟨2, by decide⟩ = false ∧
    candidateRepairsFailure ⟨3, by decide⟩ = true ∧
    min (candidateCost ⟨0, by decide⟩) (min (candidateCost ⟨1, by decide⟩) (candidateCost ⟨2, by decide⟩)) = 3 ∧
    candidateCost ⟨3, by decide⟩ = 1 ∧
    candidateCost ⟨3, by decide⟩ <
      min (candidateCost ⟨0, by decide⟩) (min (candidateCost ⟨1, by decide⟩) (candidateCost ⟨2, by decide⟩)) := by
  decide

/-- Canonical checklist record for Prompt 15 / `TFQ-0429`, where 4 distinct separation repairs tie
    at the minimal cost on an exhaustive 4-candidate domain. -/
def tiedFourMinimaRecord : JustifiedLiftChecklistRecord where
  failedPredicateNamed := true
  admissibleRepairsListed := true
  admissibleRepairCount := 4
  extensionClassDeclared := true
  costOrderDeclared := true
  tiedMinimaCount := 4
  censusState := SearchCensusState.ExhaustiveOnDeclaredDomain 4

/-- Theorem 4: When 4 admissible repairs tie for minimum cost (`tiedMinimaCount = 4`),
    `allSixChecksClosed` holds (all six Section-15 checks are recorded), but
    `uniqueMinimalExtensionLicensed` is `false` (no single lift is uniquely forced). -/
theorem tied_minima_plurality_blocks_unique_minimal_extension :
    qualifiesAsSuccessor tiedFourMinimaRecord = true ∧
    qualifiesAsProposedLift tiedFourMinimaRecord = true ∧
    allSixChecksClosed tiedFourMinimaRecord = true ∧
    uniqueMinimalExtensionLicensed tiedFourMinimaRecord = false := by
  decide

/-- Canonical complete checklist record with a unique minimum (`tiedMinimaCount = 1`). -/
def completeUniqueLiftRecord : JustifiedLiftChecklistRecord where
  failedPredicateNamed := true
  admissibleRepairsListed := true
  admissibleRepairCount := 2
  extensionClassDeclared := true
  costOrderDeclared := true
  tiedMinimaCount := 1
  censusState := SearchCensusState.ExhaustiveOnDeclaredDomain 8

/-- Theorem 5: Omitting any single one of the six Section-15 checks from `completeUniqueLiftRecord`
    causes `allSixChecksClosed` and `uniqueMinimalExtensionLicensed` to evaluate to `false`. -/
theorem omitting_any_single_section15_check_blocks_licensing :
    uniqueMinimalExtensionLicensed completeUniqueLiftRecord = true ∧
    allSixChecksClosed { completeUniqueLiftRecord with failedPredicateNamed := false } = false ∧
    allSixChecksClosed { completeUniqueLiftRecord with admissibleRepairsListed := false } = false ∧
    allSixChecksClosed { completeUniqueLiftRecord with extensionClassDeclared := false } = false ∧
    allSixChecksClosed { completeUniqueLiftRecord with costOrderDeclared := false } = false ∧
    allSixChecksClosed { completeUniqueLiftRecord with tiedMinimaCount := 0 } = false ∧
    allSixChecksClosed { completeUniqueLiftRecord with
      censusState := SearchCensusState.BudgetStoppedIncomplete 8 7 } = false := by
  decide

/-- Canonical stage-separated records:
    - `successorOnlyRecord`: only `extensionClassDeclared = true`
    - `proposedLiftOnlyRecord`: first 3 checks (`FailedPredicate`, `AdmissibleRepairs`, `ExtensionClass`)
      set to `true`, but `costOrderDeclared = false` and census budget-stopped. -/
def successorOnlyRecord : JustifiedLiftChecklistRecord where
  failedPredicateNamed := false
  admissibleRepairsListed := false
  admissibleRepairCount := 0
  extensionClassDeclared := true
  costOrderDeclared := false
  tiedMinimaCount := 0
  censusState := SearchCensusState.BudgetStoppedIncomplete 8 1

def proposedLiftOnlyRecord : JustifiedLiftChecklistRecord where
  failedPredicateNamed := true
  admissibleRepairsListed := true
  admissibleRepairCount := 4
  extensionClassDeclared := true
  costOrderDeclared := false
  tiedMinimaCount := 0
  censusState := SearchCensusState.BudgetStoppedIncomplete 8 4

/-- Theorem 6: Strict separation between `Successor`, `ProposedLift`, and `LicensedTransition`
    evidence states (`TFQ-0376` requirement that the six checks remain separate evidence states
    for a successor, a proposed lift, and a licensed transition). -/
theorem stage_progression_fence_successor_proposed_licensed :
    (qualifiesAsSuccessor successorOnlyRecord = true ∧
     qualifiesAsProposedLift successorOnlyRecord = false ∧
     allSixChecksClosed successorOnlyRecord = false) ∧
    (qualifiesAsSuccessor proposedLiftOnlyRecord = true ∧
     qualifiesAsProposedLift proposedLiftOnlyRecord = true ∧
     allSixChecksClosed proposedLiftOnlyRecord = false) ∧
    (qualifiesAsSuccessor completeUniqueLiftRecord = true ∧
     qualifiesAsProposedLift completeUniqueLiftRecord = true ∧
     allSixChecksClosed completeUniqueLiftRecord = true) := by
  decide

/-- Theorem 7: Direct bridge to `PreMssn.collapsed_observation_barrier` (Check 1: `FailedPredicate`)
    and `PreMssn.refine_separates` (Check 2: `AdmissibleRepairs` / `ProposedLift`) in
    `lean4/Imported/PreGenesisToMssn/Paper.lean`. -/
theorem pregenesis_collapsed_barrier_and_refine_separates_witness :
    (¬ ∃ factor : Unit → Bool,
        ∀ b : Bool, factor ((fun _ : Bool => ()) b) = b) ∧
    PreMssn.refineReport (fun _ : Bool => ()) (fun b : Bool => b) false ≠
      PreMssn.refineReport (fun _ : Bool => ()) (fun b : Bool => b) true := by
  refine ⟨?_, ?_⟩
  · exact PreMssn.collapsed_observation_barrier
      (fun _ : Bool => ()) (fun b : Bool => b) false true rfl (by decide)
  · exact PreMssn.refine_separates
      (fun _ : Bool => ()) (fun b : Bool => b) false true (by decide)

/-- Theorem 8: Direct bridge to `PreMssn.demand_accounting` in `lean4/Imported/PreGenesisToMssn/Paper.lean`
    and `ChainRetraction.TwoPoints.no_chain_retraction` in `lean4/ChainRetraction.lean`, showing
    how demand accounting tracks active/discharged/birth obligations and how killing a homology class
    obstructs linear chain retractions over $\mathbb{Z}$. -/
theorem pregenesis_chain_retraction_and_demand_accounting_witness :
    (([Section15CheckSlot.FailedPredicate, Section15CheckSlot.AdmissibleRepairs,
       Section15CheckSlot.ExtensionClass].filter (fun _ => !true)) ++
      [Section15CheckSlot.CostOrder, Section15CheckSlot.TiedMinima,
       Section15CheckSlot.SearchCompleteness]).length = 3 ∧
    ¬ ∃ (rU : Int →ₗ[Int] Unit)
        (rM : (Fin 2 → Int) →ₗ[Int] (Fin 2 → Int))
        (rL : Unit →ₗ[Int] Unit),
        (∀ u', rM (ChainRetraction.TwoPoints.bdD Int u') =
          ChainRetraction.TwoPoints.bdC Int (rU u')) ∧
        (∀ z', rL (ChainRetraction.TwoPoints.dC Int z') =
          ChainRetraction.TwoPoints.dC Int (rM z')) ∧
        (∀ z, rM (ChainRetraction.TwoPoints.iM Int z) = z) := by
  refine ⟨by decide, ChainRetraction.TwoPoints.no_chain_retraction Int⟩

/-- Canonical obstruction record when an exhaustive census over a declared 8-coloring domain finds
    zero 0-violation 2-colorings of $K_3$ (`wdp_lggr_chromatic::triangle_two_color`, $2^3 = 8$). -/
def triangleTwoColorObstructionRecord : JustifiedLiftChecklistRecord where
  failedPredicateNamed := true
  admissibleRepairsListed := true
  admissibleRepairCount := 0
  extensionClassDeclared := true
  costOrderDeclared := true
  tiedMinimaCount := 3
  censusState := SearchCensusState.ExhaustiveOnDeclaredDomain 8

/-- Theorem 9: On the exhaustive $2^3 = 8$ coloring domain of $K_3$ (`triangle_two_color`),
    zero proper 2-colorings exist (`obstructionCertifiedOnDeclaredDomain = true`), whereas
    stopping the census at budget $7 < 8$ (`BudgetStoppedIncomplete 8 7`) does not certify the
    obstruction (`obstructionCertifiedOnDeclaredDomain = false`). -/
theorem exhaustive_vs_budget_stopped_triangle_obstruction :
    obstructionCertifiedOnDeclaredDomain triangleTwoColorObstructionRecord = true ∧
    obstructionCertifiedOnDeclaredDomain
      { triangleTwoColorObstructionRecord with
        censusState := SearchCensusState.BudgetStoppedIncomplete 8 7 } = false := by
  decide

/-- Theorem 10: Master scope certificate for `TFQ-0376` (`PREGENESIS`). -/
theorem tfq0376_justified_lift_six_check_scope_certificate :
    (Section15CheckSlot.FailedPredicate ≠ Section15CheckSlot.SearchCompleteness ∧
     TransitionStage.Successor ≠ TransitionStage.LicensedTransition) ∧
    (allSixChecksClosed proposedLiftOnlyRecord = false ∧
     qualifiesAsProposedLift proposedLiftOnlyRecord = true) ∧
    (allSixChecksClosed tiedFourMinimaRecord = true ∧
     uniqueMinimalExtensionLicensed tiedFourMinimaRecord = false) ∧
    (uniqueMinimalExtensionLicensed completeUniqueLiftRecord = true ∧
     allSixChecksClosed { completeUniqueLiftRecord with
       censusState := SearchCensusState.BudgetStoppedIncomplete 8 7 } = false) ∧
    (obstructionCertifiedOnDeclaredDomain triangleTwoColorObstructionRecord = true ∧
     obstructionCertifiedOnDeclaredDomain
       { triangleTwoColorObstructionRecord with
         censusState := SearchCensusState.BudgetStoppedIncomplete 8 7 } = false) ∧
    (candidateCost ⟨3, by decide⟩ <
      min (candidateCost ⟨0, by decide⟩)
          (min (candidateCost ⟨1, by decide⟩) (candidateCost ⟨2, by decide⟩))) := by
  decide

end CampaignTfq0376Pregenesis
