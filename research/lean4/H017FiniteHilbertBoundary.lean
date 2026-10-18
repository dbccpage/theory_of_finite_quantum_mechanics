/-
  H017 -- finite Hilbert boundary theorem. AuthorityEffect: None.
  Candidate only. Not PROVEN. Kind: ASSEMBLY.

  Claim identifier: HW-H017
  Source-paper contact: assembles selected witness theorems from the
  walk; it does not import every H000-H016 rung into this theorem.
  Every conjunct is justified only by its named theorem below.

  Target proposition (a CONJUNCTION of rung witnesses -- NOT a
  connected presented-carrier derivation; see STRUCTURE below)
    This theorem does NOT prove "a finite presented carrier with
    reversible report dynamics admits ... a representation" as one
    threaded object. It CONJOINS the separately-proved rung
    witnesses, whose informal reading is: a permutation-ISOMETRY
    envelope over any pack/enumeration/reversible map
    (permutation_isometry -- "unitary" only up to the
    positive-definite-host specialization, H006); a phase-blind
    quadratic presentation with fibers holding equal-L1 states
    (relative_phase_in_fiber) that a supplied mixing presentation
    separates (mix_separates, no_descent_through_fiber); and the
    named boundaries left OPEN -- complex phase
    (int_no_descent: the witness runs on the sign group), Born
    uniqueness (a positive non-proportional rival, quartic_rival --
    NOT a same-contract non-uniqueness proof; open O-6), tensor
    composition (bell_not_product entanglement witness +
    sum_component_embedding_surjective; this assembly predates the
    weaker same-host rival proved separately in H014Interface),
    general quantum channels (collapse_no_isometry,
    dilations_distinct), and continuous dynamics
    (no_report_half_step, interpolant_not_unique) -- each a separate
    import unless discharged by additional theorems.

  Imports added at this rung
    None. Assembly only: every conjunct names an earlier theorem.

  Theorem or counterexample
    finite_hilbert_boundary: the conjunction below.
    import_ledger_gate: the SpinePack-style predicate showing which
    import flags remain down.

  Nonclaim boundary
    This theorem does NOT say quantum mechanics is derived, forced,
    unique, or complete. Each residual import is named; closing any
    one of them is future theorem work priced in FRONTIER.md.

    STRUCTURE (adversarial-review response, 2026-08-19): this is a
    CONJUNCTION of separately-proved rung witnesses over a shared
    Bool/Int/GaussInt substrate and the phase-blind presentation.
    It is NOT a single carrier/quotient object threaded through
    H000->H016: conjunct (1) is general over any pack/enumeration/
    reversible map, but conjuncts (2)-(8) are fixed fixtures, and
    H000's PresentedCarrier is not the object they transform. The
    genuine cross-rung thread the layers DO support -- phase-blind
    equivariance intertwining the H006 isometry, the H002/H003
    pushforward, and one reversible report map -- is proved
    separately in HWThread.phaseBlind_intertwines. Full end-to-end
    threading through one object is open residue R0 (FRONTIER.md).

  AuthorityEffect: None
-/

import HWKernel
import Core
import H003ReversibilityGate
import H004FreeLinearization
import H005InnerProductAdmission
import H006PermutationUnitary
import H008PhaseBlindPresentation
import H009PhaseFiber
import H010InterferenceNonDescent
import H013BornPairingBoundary
import H014TensorCompositionBoundary
import H015IrreversibleFork
import H016ContinuousDynamicsFork

namespace FableHilbertWalk20260819.H017

open GrokPdNight20260814.Core (ZeroRel)
open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H003
open FableHilbertWalk20260819.H004
open FableHilbertWalk20260819.H005
open FableHilbertWalk20260819.H006
open FableHilbertWalk20260819.H008
open FableHilbertWalk20260819.H009
open FableHilbertWalk20260819.H010
open FableHilbertWalk20260819.H013
open FableHilbertWalk20260819.H014
open FableHilbertWalk20260819.H015
open FableHilbertWalk20260819.H016

/-- Remaining-import ledger. METADATA, not a theorem-bound gate:
    the flags are hand-set and `AllDischarged ... = false` is rfl
    over them, binding nothing on its own -- the binding evidence
    is the named theorems in the conjunction below. A true flag is
    a hand-assertion that a local theorem discharges that rung;
    every false flag is priced future work. -/
structure ImportLedger where
  permutation_isometry_envelope_flag : Bool
  phase_fiber_nonempty : Bool
  interference_non_descent : Bool
  complex_phase_selected : Bool
  born_uniqueness : Bool
  tensor_composition_forced : Bool
  channels_canonical : Bool
  continuum_dynamics : Bool

def walkLedger : ImportLedger where
  permutation_isometry_envelope_flag := true
  phase_fiber_nonempty := true
  interference_non_descent := true
  complex_phase_selected := false
  born_uniqueness := false
  tensor_composition_forced := false
  channels_canonical := false
  continuum_dynamics := false

def AllDischarged (L : ImportLedger) : Bool :=
  L.permutation_isometry_envelope_flag && L.phase_fiber_nonempty &&
    L.interference_non_descent && L.complex_phase_selected &&
    L.born_uniqueness && L.tensor_composition_forced &&
    L.channels_canonical && L.continuum_dynamics

/-- The gate records honestly that the walk did NOT discharge the
    upper imports. -/
theorem import_ledger_gate :
    AllDischarged walkLedger = false ∧
      (walkLedger.permutation_isometry_envelope_flag &&
        walkLedger.phase_fiber_nonempty &&
        walkLedger.interference_non_descent) = true :=
  ⟨rfl, rfl⟩

#print axioms import_ledger_gate

/-- The finite Hilbert boundary theorem: the strongest statement
    licensed by the walk, as one conjunction of named theorems. -/
theorem finite_hilbert_boundary :
    -- (1) permutation-ISOMETRY envelope under explicit imports:
    --     general over every coefficient pack, enumeration, and
    --     reversible report map (permutation_isometry itself;
    --     "unitary" only up to the positive-definite host, H006)
    (∀ {K Q : Type} (P : StarRingPack K) [DecidableEq Q]
      (E : Enum Q) {τ : Q → Q} (R : Reversible τ) (u v : Vec K Q),
      sesq P E (permU P R u) (permU P R v) = sesq P E u v) ∧
    -- (2) the phase fiber holds states with equal L1 data
    (ZeroRel (phasePD Bool) psi1 psi2 ∧ psi1 ≠ psi2) ∧
    -- (3) a supplied mixing presentation separates the fiber
    (¬(∀ q : Bool, readout psi1 q = readout psi2 q)) ∧
    (¬ ∃ f : (Bool → Int) → (Bool → Int),
      ∀ v : Vec GaussInt Bool, readout v = f (phaseBlind v)) ∧
    -- (4) complex phase is NOT selected: the witness runs on signs
    (¬ ∃ f : (Bool → Int) → (Bool → Int),
      ∀ v : Vec Int Bool, iReadout v = f (iWeights v)) ∧
    -- (5) a positive rival readout (quartic) disagrees pointwise
    --     with the quadratic one and is not a rescaling of it.
    --     This is NOT a same-normalization-contract Born
    --     non-uniqueness proof (open O-6); it only shows the
    --     quadratic rule is not the unique positive scale-distinct
    --     readout.
    (∀ q : Bool, 0 ≤ quartic psi21 q) ∧
    (¬(∀ q : Bool, phaseBlind psi21 q = quartic psi21 q)) ∧
    -- (6) ENTANGLEMENT witness: the tensor host carries a
    --     non-product vector, and the direct-sum host is exhausted
    --     by its component embedding (structurally inequivalent
    --     rules). NOT a "tensor not forced" claim -- that is the
    --     undischarged H014 boundary.
    (¬ ∃ u v : Bool → Int,
      ∀ p : Bool × Bool, bell p = tensor u v p) ∧
    (∀ w : Sum Bool Bool → Int, sumJoin (sumSplit w) = w) ∧
    -- (7) channels are NOT canonical: no isometric collapse, and
    --     distinct reversible dilations share a reduction
    (¬ ∃ U : Vec Int Bool → Vec Int Bool,
      (∀ u v : Vec Int Bool,
        sesq intPack enumBool (U u) (U v) =
          sesq intPack enumBool u v) ∧
      U (delta intPack false) = delta intPack false ∧
      U (delta intPack true) = delta intPack false) ∧
    ((∀ a b : Bool, (dil1 (a, b)).1 = (dil2 (a, b)).1) ∧
      ¬(∀ a b : Bool, dil1 (a, b) = dil2 (a, b))) ∧
    -- (8) the continuum is NOT reached: no report half-step, while
    --     amplitude interpolants exist at declared scale and are
    --     not unique
    (¬ ∃ σ : Bool → Bool, ∀ q : Bool, σ (σ q) = toggle q) ∧
    (∀ (v : Vec GaussInt Bool) (q : Bool),
      sqrtSwap (sqrtSwap v) q = scale4 (ampSwap v) q) ∧
    (¬(∀ v : Vec GaussInt Bool, ∀ q : Bool,
      sqrtSwap v q = sqrtSwapNeg v q)) := by
  refine ⟨?_, relative_phase_in_fiber, mix_separates,
    no_descent_through_fiber, int_no_descent, quartic_rival.1,
    quartic_rival.2.2.2, bell_not_product,
    sum_component_embedding_surjective,
    collapse_no_isometry, ⟨same_reduction, dilations_distinct⟩,
    no_report_half_step,
    fun v q => sqrtSwap_squares_to_scaled_swap v q,
    interpolant_not_unique⟩
  intro K Q P inst E τ R u v
  exact permutation_isometry P E R u v

#print axioms finite_hilbert_boundary

end FableHilbertWalk20260819.H017
