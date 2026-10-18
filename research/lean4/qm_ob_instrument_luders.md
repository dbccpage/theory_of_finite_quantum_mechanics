import Mathlib.Tactic

/-!
# QMObInstrumentLuders — W6.12 / OB-INSTRUMENT (classical + density Lüders toy)

Programme target: DERIV-MASTER W6.12 (QMREG-61 / freeze `OB-INSTRUMENT` / recovery T13).

Upstream capital (do not re-prove as new dream debt):
* `qm_021` measurement update as idempotent conditioning on finite outcome weights;
* W6.10 spectral projectors / density sandwich $P\rho P$ (bind, do not re-prove spectral).

Mechanized:

1. **Projective / sector update (classical):** conditioned weight on measured sector.
2. **Idempotence / repeatability / classical Born match** on bit residual weights.
3. **Density Lüders under spectral projectors (TOY-MECH, lift host):** sandwich
   $P\rho P$ for diagonal $P_0,P_1$ and scaled $\sigma_x$ projectors; diagonal
   population recovers classical `update`; classical host erases coherence fence.
4. **Fence:** full POVM / Kraus instrument catalogue remains **OPEN**; density
   Lüders is not FinL1-derived (requires `complexHilbertLift` host).
5. **Kraus / soft / ternary instrument bind (TOY-MECH residual, W6.10 capital):**
   soft effects as instrument outcome masses; projective Kraus channel dephase;
   non-Hermitian damp Kraus instrument; ternary instrument declaration (3 outcomes);
   full general catalogue still **OPEN**.

AuthorityEffect: None.
-/

namespace QM
namespace ObInstrument

/-! ## Bit residual weights -/

structure BitWeight where
  w0 : Nat
  w1 : Nat
deriving DecidableEq, Repr

namespace BitWeight

def total (w : BitWeight) : Nat := w.w0 + w.w1

def IsSupportedOn0 (w : BitWeight) : Prop := w.w1 = 0
def IsSupportedOn1 (w : BitWeight) : Prop := w.w0 = 0

end BitWeight

inductive Outcome where
  | o0
  | o1
deriving DecidableEq, Repr

/-- Classical projective / Lüders-style sector update (Bayesian conditioning on weights). -/
def update (w : BitWeight) : Outcome → BitWeight
  | .o0 => { w0 := w.w0, w1 := 0 }
  | .o1 => { w0 := 0, w1 := w.w1 }

/-- Outcome probability mass (unnormalized Born on classical shadow). -/
def outcomeMass (w : BitWeight) : Outcome → Nat
  | .o0 => w.w0
  | .o1 => w.w1

theorem outcome_mass_matches_prior (w : BitWeight) :
    outcomeMass w .o0 = w.w0 ∧ outcomeMass w .o1 = w.w1 :=
  ⟨rfl, rfl⟩

theorem update_o0_support (w : BitWeight) :
    (update w .o0).IsSupportedOn0 := by
  simp [update, BitWeight.IsSupportedOn0]

theorem update_o1_support (w : BitWeight) :
    (update w .o1).IsSupportedOn1 := by
  simp [update, BitWeight.IsSupportedOn1]

/-- Idempotence of sector update (textbook Lüders hallmark on classical shadow). -/
theorem update_idempotent (w : BitWeight) (o : Outcome) :
    update (update w o) o = update w o := by
  cases o <;> simp [update]

/-- Repeatability: after update to o0 with positive mass, re-read mass is full total. -/
theorem repeatable_o0 (w : BitWeight) (_h : 0 < w.w0) :
    outcomeMass (update w .o0) .o0 = (update w .o0).total := by
  simp [outcomeMass, update, BitWeight.total]

theorem repeatable_o1 (w : BitWeight) (_h : 0 < w.w1) :
    outcomeMass (update w .o1) .o1 = (update w .o1).total := by
  simp [outcomeMass, update, BitWeight.total]

/-- Worked example from `qm_021`: w=(3,1), update on sector 1 → (0,1). -/
def examplePrior : BitWeight := { w0 := 3, w1 := 1 }

theorem example_update_o1 :
    update examplePrior .o1 = { w0 := 0, w1 := 1 } := rfl

theorem example_idempotent :
    update (update examplePrior .o1) .o1 = update examplePrior .o1 :=
  update_idempotent examplePrior .o1

theorem example_born_o1 : outcomeMass examplePrior .o1 = 1 := rfl

/-! ## Instrument interface (import-shaped) -/

inductive InstrumentHost where
  | finL1Classical
  | complexHilbertLift
deriving DecidableEq, Repr

structure DeclaredInstrument where
  host : InstrumentHost
  /-- Number of outcomes in the declared instrument. -/
  nOutcomes : Nat
  n_pos : 0 < nOutcomes

def classicalBitInstrument : DeclaredInstrument :=
  { host := .finL1Classical
    nOutcomes := 2
    n_pos := by decide }

def qubitProjectiveInstrument : DeclaredInstrument :=
  { host := .complexHilbertLift
    nOutcomes := 2
    n_pos := by decide }

theorem classical_instrument_host :
    classicalBitInstrument.host = InstrumentHost.finL1Classical := rfl

theorem qubit_projective_host :
    qubitProjectiveInstrument.host = InstrumentHost.complexHilbertLift := rfl

/-! ## Density Lüders under spectral projectors (W6.10 capital bind)

Unnormalized sandwich $P\rho P$ under a lift host. Classical `update` is the
population shadow of diagonal density Lüders. Coherent densities are not
FinL1-native (classical host erases off-diagonals).

General POVM / Kraus instruments remain **OPEN**.
-/

structure Mat2 where
  a00 : Int
  a01 : Int
  a10 : Int
  a11 : Int
  deriving DecidableEq, Repr

namespace Mat2

def mul (m n : Mat2) : Mat2 :=
  { a00 := m.a00 * n.a00 + m.a01 * n.a10
    a01 := m.a00 * n.a01 + m.a01 * n.a11
    a10 := m.a10 * n.a00 + m.a11 * n.a10
    a11 := m.a10 * n.a01 + m.a11 * n.a11 }

def smul (k : Int) (m : Mat2) : Mat2 :=
  { a00 := k * m.a00, a01 := k * m.a01, a10 := k * m.a10, a11 := k * m.a11 }

def zero : Mat2 := { a00 := 0, a01 := 0, a10 := 0, a11 := 0 }

end Mat2

/-- Unnormalized Lüders sandwich $P\,\rho\,P$. -/
def luders (p ρ : Mat2) : Mat2 := Mat2.mul p (Mat2.mul ρ p)

def diagDensity (ρ00 ρ11 : Int) : Mat2 :=
  { a00 := ρ00, a01 := 0, a10 := 0, a11 := ρ11 }

/-- Rank-1 computational projectors (W6.10 capital). -/
def proj0 : Mat2 := { a00 := 1, a01 := 0, a10 := 0, a11 := 0 }
def proj1 : Mat2 := { a00 := 0, a01 := 0, a10 := 0, a11 := 1 }

/-- Scaled $\sigma_x$ spectral projectors $2P_\pm$ (W6.10 capital). -/
def twoPplus : Mat2 := { a00 := 1, a01 := 1, a10 := 1, a11 := 1 }
def twoPminus : Mat2 := { a00 := 1, a01 := -1, a10 := -1, a11 := 1 }

/-- Coherent pure-support densities $\propto |+\rangle\langle+|$, $\propto |-\rangle\langle-|$. -/
def rhoPlus : Mat2 := twoPplus
def rhoMinus : Mat2 := twoPminus

theorem proj0_luders_diag (ρ00 ρ11 : Int) :
    luders proj0 (diagDensity ρ00 ρ11) = diagDensity ρ00 0 := by
  simp [luders, Mat2.mul, proj0, diagDensity]

theorem proj1_luders_diag (ρ00 ρ11 : Int) :
    luders proj1 (diagDensity ρ00 ρ11) = diagDensity 0 ρ11 := by
  simp [luders, Mat2.mul, proj1, diagDensity]

/-- Diagonal density Lüders zeros the unmeasured sector (classical support shape). -/
theorem diag_luders_sector_support (ρ00 ρ11 : Int) :
    (luders proj0 (diagDensity ρ00 ρ11)).a11 = 0 ∧
    (luders proj0 (diagDensity ρ00 ρ11)).a00 = ρ00 ∧
    (luders proj1 (diagDensity ρ00 ρ11)).a00 = 0 ∧
    (luders proj1 (diagDensity ρ00 ρ11)).a11 = ρ11 := by
  rw [proj0_luders_diag, proj1_luders_diag]
  simp [diagDensity]

/-- Worked diagonal density example aligned with classical (3,1)→o1→(0,1). -/
theorem example_diag_luders_o1 :
    luders proj1 (diagDensity 3 1) = diagDensity 0 1 :=
  proj1_luders_diag 3 1

/-- Density diagonal population matches classical `update` on the qm_021 example. -/
theorem example_diag_luders_matches_classical_population :
    (luders proj1 (diagDensity 3 1)).a00 = 0 ∧
    (luders proj1 (diagDensity 3 1)).a11 = 1 ∧
    update examplePrior .o1 = { w0 := 0, w1 := 1 } ∧
    (update examplePrior .o1).w0 = 0 ∧
    (update examplePrior .o1).w1 = 1 := by
  refine ⟨?_, ?_, example_update_o1, rfl, rfl⟩
  · rw [example_diag_luders_o1]; rfl
  · rw [example_diag_luders_o1]; rfl

theorem proj0_luders_idempotent (ρ : Mat2) :
    luders proj0 (luders proj0 ρ) = luders proj0 ρ := by
  cases ρ
  simp [luders, Mat2.mul, proj0]

theorem proj1_luders_idempotent (ρ : Mat2) :
    luders proj1 (luders proj1 ρ) = luders proj1 ρ := by
  cases ρ
  simp [luders, Mat2.mul, proj1]

/-- Scaled + sandwich on coherent support: $(2P_+)\rho_+(2P_+)=4\cdot(2P_+)$. -/
theorem twoPplus_luders_rhoPlus :
    luders twoPplus rhoPlus = Mat2.smul 4 twoPplus := by
  -- rhoPlus := twoPplus; expand all cells
  simp [luders, Mat2.mul, Mat2.smul, twoPplus, rhoPlus]

/-- Orthogonal kill: $(2P_-)\rho_+(2P_-)=0$. -/
theorem twoPminus_luders_rhoPlus_zero :
    luders twoPminus rhoPlus = Mat2.zero := by
  simp [luders, Mat2.mul, Mat2.zero, twoPminus, twoPplus, rhoPlus]

theorem twoPplus_luders_rhoMinus_zero :
    luders twoPplus rhoMinus = Mat2.zero := by
  simp [luders, Mat2.mul, Mat2.zero, twoPplus, twoPminus, rhoMinus]

theorem rhoPlus_not_classical_diagonal : rhoPlus.a01 ≠ 0 := by
  decide

/-- Classical sector update erases coherence (population-only carrier). -/
theorem classical_update_erases_coherence :
    rhoPlus.a01 ≠ 0 ∧
    (update { w0 := 1, w1 := 1 } .o0).w1 = 0 ∧
    (update { w0 := 1, w1 := 1 } .o0).w0 = 1 := by
  refine ⟨by decide, ?_, ?_⟩
  · simp [update]
  · simp [update]

/-- Density Lüders requires lift host; classical host is population-only. -/
def densityLudersRequiresLiftHost : InstrumentHost → Bool
  | .finL1Classical => false
  | .complexHilbertLift => true

theorem density_luders_host_fence :
    densityLudersRequiresLiftHost .finL1Classical = false ∧
    densityLudersRequiresLiftHost .complexHilbertLift = true ∧
    qubitProjectiveInstrument.host = .complexHilbertLift :=
  ⟨rfl, rfl, rfl⟩

/-- Density Lüders toy package (not full POVM catalogue). -/
theorem density_luders_instrument_package :
    luders proj0 (diagDensity 3 1) = diagDensity 3 0 ∧
    luders proj1 (diagDensity 3 1) = diagDensity 0 1 ∧
    luders twoPplus rhoPlus = Mat2.smul 4 twoPplus ∧
    luders twoPminus rhoPlus = Mat2.zero ∧
    rhoPlus.a01 ≠ 0 ∧
    densityLudersRequiresLiftHost .complexHilbertLift = true ∧
    densityLudersRequiresLiftHost .finL1Classical = false :=
  ⟨proj0_luders_diag 3 1, proj1_luders_diag 3 1, twoPplus_luders_rhoPlus,
    twoPminus_luders_rhoPlus_zero, by decide, rfl, rfl⟩

/-! ## Kraus / soft / ternary instrument bind (W6.10 catalogue capital)

Instrument-side packaging of W6.10 residual capital (do not re-prove spectral
reconstruction). Registry-relative TOY-MECH; full general catalogue **OPEN**.
-/

def Mat2.add (m n : Mat2) : Mat2 :=
  { a00 := m.a00 + n.a00, a01 := m.a01 + n.a01
    a10 := m.a10 + n.a10, a11 := m.a11 + n.a11 }

def mat2Transpose (m : Mat2) : Mat2 :=
  { a00 := m.a00, a01 := m.a10, a10 := m.a01, a11 := m.a11 }

def id2 : Mat2 := { a00 := 1, a01 := 0, a10 := 0, a11 := 1 }

/-- Soft non-projective instrument effects (W6.10 capital). -/
def softEffect0 : Mat2 := { a00 := 2, a01 := 1, a10 := 1, a11 := 2 }
def softEffect1 : Mat2 := { a00 := 2, a01 := -1, a10 := -1, a11 := 2 }

theorem soft_instrument_effects_resolution :
    Mat2.add softEffect0 softEffect1 = Mat2.smul 4 id2 := by
  simp [Mat2.add, Mat2.smul, softEffect0, softEffect1, id2]

def Mat2.IsProjector (p : Mat2) : Prop := Mat2.mul p p = p

theorem softEffect0_not_instrument_projector :
    ¬ Mat2.IsProjector softEffect0 := by
  intro h
  have : Mat2.mul softEffect0 softEffect0 = softEffect0 := h
  simp [Mat2.mul, softEffect0] at this

/-- Soft instrument outcome mass $\mathrm{Tr}(E\rho)$ (real Frobenius package). -/
def softOutcomeMass (E ρ : Mat2) : Int :=
  E.a00 * ρ.a00 + E.a01 * ρ.a10 + E.a10 * ρ.a01 + E.a11 * ρ.a11

theorem soft_instrument_mass_resolution :
    softOutcomeMass softEffect0 rhoPlus = 6 ∧
    softOutcomeMass softEffect1 rhoPlus = 2 ∧
    softOutcomeMass softEffect0 rhoPlus + softOutcomeMass softEffect1 rhoPlus = 8 := by
  decide

/-- Soft instruments require lift host (off-diagonal effects). -/
def softInstrumentHost : InstrumentHost := .complexHilbertLift

theorem soft_instrument_needs_lift :
    softInstrumentHost = .complexHilbertLift ∧ softEffect0.a01 ≠ 0 :=
  ⟨rfl, by decide⟩

/-- Projective Kraus instrument channel $\sum_i P_i\rho P_i$ (Z-measure). -/
def projectiveKrausChannel (ρ : Mat2) : Mat2 :=
  Mat2.add (luders proj0 ρ) (luders proj1 ρ)

theorem projective_kraus_dephases_rhoPlus :
    projectiveKrausChannel rhoPlus = id2 := by
  simp [projectiveKrausChannel, luders, Mat2.mul, Mat2.add, proj0, proj1, rhoPlus,
    twoPplus, id2]

/-- Amplitude-damping non-Hermitian Kraus instrument (W6.10 capital). -/
def dampKraus0 : Mat2 := { a00 := 1, a01 := 0, a10 := 0, a11 := 0 }
def dampKraus1 : Mat2 := { a00 := 0, a01 := 1, a10 := 0, a11 := 0 }

def krausEffect (k : Mat2) : Mat2 := Mat2.mul (mat2Transpose k) k

theorem damp_instrument_kraus_completeness :
    Mat2.add (krausEffect dampKraus0) (krausEffect dampKraus1) = id2 := by
  simp [krausEffect, mat2Transpose, Mat2.mul, Mat2.add, dampKraus0, dampKraus1, id2]

theorem dampKraus1_not_instrument_projector :
    ¬ Mat2.IsProjector dampKraus1 := by
  intro h
  have : Mat2.mul dampKraus1 dampKraus1 = dampKraus1 := h
  simp [Mat2.mul, dampKraus1] at this

def dampInstrumentChannel (ρ : Mat2) : Mat2 :=
  Mat2.add
    (Mat2.mul dampKraus0 (Mat2.mul ρ (mat2Transpose dampKraus0)))
    (Mat2.mul dampKraus1 (Mat2.mul ρ (mat2Transpose dampKraus1)))

def rho1 : Mat2 := { a00 := 0, a01 := 0, a10 := 0, a11 := 1 }

theorem damp_instrument_maps_rho1_to_proj0 :
    dampInstrumentChannel rho1 = proj0 := by
  simp [dampInstrumentChannel, Mat2.mul, Mat2.add, mat2Transpose, dampKraus0,
    dampKraus1, rho1, proj0]

/-- Ternary instrument declaration (σ_x⊕2 spectral outcomes; W6.10 capital). -/
def ternarySpectralInstrument : DeclaredInstrument :=
  { host := .complexHilbertLift
    nOutcomes := 3
    n_pos := by decide }

theorem ternary_instrument_host :
    ternarySpectralInstrument.host = .complexHilbertLift ∧
    ternarySpectralInstrument.nOutcomes = 3 :=
  ⟨rfl, rfl⟩

/-- Full general POVM / Kraus instruments not discharged. -/
def generalPovmInstrument_open : Prop := True

theorem general_povm_instrument_marked_open : generalPovmInstrument_open := trivial

/-- Soft / Kraus / ternary instrument bind package (TOY-MECH; catalogue OPEN). -/
def instrumentKrausCatalogueBindPackage_toy : Bool := true

theorem instrument_kraus_catalogue_bind_package :
    instrumentKrausCatalogueBindPackage_toy = true ∧
    Mat2.add softEffect0 softEffect1 = Mat2.smul 4 id2 ∧
    ¬ Mat2.IsProjector softEffect0 ∧
    softOutcomeMass softEffect0 rhoPlus + softOutcomeMass softEffect1 rhoPlus = 8 ∧
    projectiveKrausChannel rhoPlus = id2 ∧
    Mat2.add (krausEffect dampKraus0) (krausEffect dampKraus1) = id2 ∧
    ¬ Mat2.IsProjector dampKraus1 ∧
    dampInstrumentChannel rho1 = proj0 ∧
    ternarySpectralInstrument.nOutcomes = 3 ∧
    softInstrumentHost = .complexHilbertLift ∧
    generalPovmInstrument_open := by
  refine ⟨rfl, soft_instrument_effects_resolution, softEffect0_not_instrument_projector,
    ?_, projective_kraus_dephases_rhoPlus, damp_instrument_kraus_completeness,
    dampKraus1_not_instrument_projector, damp_instrument_maps_rho1_to_proj0,
    rfl, rfl, trivial⟩
  decide

/-- Instrument is not authority. -/
def IsAuth (_carrier : Type) : Prop := False

theorem instrument_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end ObInstrument
end QM

#print axioms QM.ObInstrument.update_idempotent
#print axioms QM.ObInstrument.example_update_o1
#print axioms QM.ObInstrument.repeatable_o0
#print axioms QM.ObInstrument.density_luders_instrument_package
#print axioms QM.ObInstrument.example_diag_luders_matches_classical_population
#print axioms QM.ObInstrument.instrument_kraus_catalogue_bind_package
#print axioms QM.ObInstrument.instrument_not_auth
