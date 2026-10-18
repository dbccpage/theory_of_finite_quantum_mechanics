import Mathlib.Tactic

/-!
# QMUnitaryAntiunitaryGauge — W5.10 (within-class gauge)

Programme target: DERIV-MASTER W5.10 (QMREG-57): unitary vs antiunitary /
conjugation gauge inside the complex Hilbert lift.

Discrete Gaussian-integer toy for $\mathbb{Z}[i]$ amplitudes $(a,b)\leftrightarrow a+bi$:

1. **Unitary phase $i$:** $(a,b)\mapsto(-b,a)$ preserves $\lvert z\rvert^2=a^2+b^2$.
2. **Complex conjugation (antiunitary core):** $(a,b)\mapsto(a,-b)$ preserves
   $\lvert z\rvert^2$ and is **not** the same map as phase-$i$.
3. **Born readout** on a single amplitude depends only on $\lvert z\rvert^2$ — hence
   invariant under both gauges.
4. **Two-component state:** apply gate componentwise; total $\ell^2$ mass conserved;
   computational probabilities $p_k \propto \lvert z_k\rvert^2$ unchanged.
5. **Wigner-style sesquilinear residual (TOY-MECH):** $\langle u,v\rangle=\overline{u}v$;
   unitary phase-$i$ **preserves** the form; conjugation **sends** $\langle u,v\rangle$
   to its conjugate; composition algebra (mulI²=-1, conj²=id; noncommute).

**Not claimed:** full Wigner theorem for all symmetries of Hilbert space; continuous
   $U(1)$; time-reversal dynamics; authority; uniqueness of gauge presentation.

AuthorityEffect: None.
-/

namespace QM
namespace UnitaryAntiunitaryGauge

/-! ## Gaussian integer amplitudes -/

structure GaussInt where
  re : Int
  im : Int
deriving DecidableEq, Repr

namespace GaussInt

def normSq (z : GaussInt) : Int := z.re * z.re + z.im * z.im

/-- Unitary multiplication by $i$: $i(a+bi)= -b + ai$. -/
def mulI (z : GaussInt) : GaussInt :=
  { re := -z.im, im := z.re }

/-- Complex conjugation (antiunitary / conjugation gauge core). -/
def conj (z : GaussInt) : GaussInt :=
  { re := z.re, im := -z.im }

/-- Ring multiplication in $\mathbb{Z}[i]$. -/
def mul (z w : GaussInt) : GaussInt :=
  { re := z.re * w.re - z.im * w.im
    im := z.re * w.im + z.im * w.re }

theorem mulI_preserves_normSq (z : GaussInt) :
    (mulI z).normSq = z.normSq := by
  unfold mulI normSq
  ring

theorem conj_preserves_normSq (z : GaussInt) :
    (conj z).normSq = z.normSq := by
  unfold conj normSq
  ring

/-- The two gauges are distinct as maps on a non-real amplitude. -/
def sample : GaussInt := { re := 1, im := 1 }

theorem gauges_disagree_on_sample :
    mulI sample ≠ conj sample := by
  intro h
  -- mulI (1,1) = (-1,1); conj (1,1) = (1,-1)
  simp [mulI, conj, sample] at h

theorem sample_norm : sample.normSq = 2 := rfl

theorem both_gauges_same_born_sample :
    (mulI sample).normSq = sample.normSq ∧
    (conj sample).normSq = sample.normSq :=
  ⟨mulI_preserves_normSq sample, conj_preserves_normSq sample⟩

/-! ### Wigner-style sesquilinear distinction (TOY-MECH residual)

Standard complex inner product on 1-d: $\langle u,v\rangle = \overline{u}\,v$.
* Unitary $U$: $\langle Uu,Uv\rangle=\langle u,v\rangle$.
* Antiunitary $A$: $\langle Au,Av\rangle=\overline{\langle u,v\rangle}$.
This is the discrete Wigner hallmark without claiming the full theorem.
-/

/-- Sesquilinear form $\langle u,v\rangle=\overline{u}\,v$ as a $\mathbb{Z}[i]$ value. -/
def sesqui (u v : GaussInt) : GaussInt := mul (conj u) v

/-- Phase-$i$ preserves the sesquilinear form (unitary hallmark). -/
theorem mulI_preserves_sesqui (u v : GaussInt) :
    sesqui (mulI u) (mulI v) = sesqui u v := by
  -- ⟨iu, iv⟩ = conj(iu)·(iv) = (-i ū)·(i v) = ū v = ⟨u,v⟩
  unfold sesqui mulI mul conj
  ring

/-- Conjugation sends the form to its conjugate (antiunitary hallmark). -/
theorem conj_conjugates_sesqui (u v : GaussInt) :
    sesqui (conj u) (conj v) = conj (sesqui u v) := by
  unfold sesqui mul conj
  ring

/-- Witness pair where $\langle u,v\rangle$ is non-real (so conj ≠ id on the form). -/
def sampleU : GaussInt := { re := 1, im := 0 }
def sampleV : GaussInt := { re := 0, im := 1 }

theorem sample_sesqui_nonreal :
    sesqui sampleU sampleV = { re := 0, im := 1 } := by
  simp [sesqui, mul, conj, sampleU, sampleV]

theorem conj_changes_sample_sesqui :
    sesqui (conj sampleU) (conj sampleV) ≠ sesqui sampleU sampleV := by
  -- left = conj ⟨u,v⟩ = -i; right = i
  intro h
  simp [sesqui, mul, conj, sampleU, sampleV] at h

theorem mulI_preserves_sample_sesqui :
    sesqui (mulI sampleU) (mulI sampleV) = sesqui sampleU sampleV :=
  mulI_preserves_sesqui sampleU sampleV

/-- Composition algebra of the two gauges. -/
theorem mulI_sq_neg (z : GaussInt) :
    mulI (mulI z) = { re := -z.re, im := -z.im } := by
  cases z
  simp [mulI]

theorem conj_involutive (z : GaussInt) : conj (conj z) = z := by
  cases z
  simp [conj]

theorem mulI_conj_noncommute :
    mulI (conj sample) ≠ conj (mulI sample) := by
  decide

end GaussInt

/-! ## Two-level pure-state toy (unnormalized) -/

structure Amp2 where
  z0 : GaussInt
  z1 : GaussInt
deriving DecidableEq, Repr

namespace Amp2

def totalNormSq (ψ : Amp2) : Int :=
  ψ.z0.normSq + ψ.z1.normSq

def mapAmp (f : GaussInt → GaussInt) (ψ : Amp2) : Amp2 :=
  { z0 := f ψ.z0, z1 := f ψ.z1 }

def applyUnitaryI (ψ : Amp2) : Amp2 := mapAmp GaussInt.mulI ψ
def applyConj (ψ : Amp2) : Amp2 := mapAmp GaussInt.conj ψ

theorem unitaryI_preserves_total (ψ : Amp2) :
    (applyUnitaryI ψ).totalNormSq = ψ.totalNormSq := by
  simp [applyUnitaryI, mapAmp, totalNormSq, GaussInt.mulI_preserves_normSq]

theorem conj_preserves_total (ψ : Amp2) :
    (applyConj ψ).totalNormSq = ψ.totalNormSq := by
  simp [applyConj, mapAmp, totalNormSq, GaussInt.conj_preserves_normSq]

/-- Computational-basis Born weights (unnormalized). -/
def bornWeights (ψ : Amp2) : Int × Int :=
  (ψ.z0.normSq, ψ.z1.normSq)

theorem unitaryI_preserves_born (ψ : Amp2) :
    bornWeights (applyUnitaryI ψ) = bornWeights ψ := by
  simp [bornWeights, applyUnitaryI, mapAmp, GaussInt.mulI_preserves_normSq]

theorem conj_preserves_born (ψ : Amp2) :
    bornWeights (applyConj ψ) = bornWeights ψ := by
  simp [bornWeights, applyConj, mapAmp, GaussInt.conj_preserves_normSq]

def fairSuperpos : Amp2 :=
  { z0 := { re := 1, im := 0 }
    z1 := { re := 0, im := 1 } }

theorem fair_born :
    bornWeights fairSuperpos = (1, 1) := rfl

theorem fair_gauges_same_born :
    bornWeights (applyUnitaryI fairSuperpos) = (1, 1) ∧
    bornWeights (applyConj fairSuperpos) = (1, 1) := by
  constructor
  · rw [unitaryI_preserves_born, fair_born]
  · rw [conj_preserves_born, fair_born]

/-- Global unitary vs antiunitary presentations differ on the state (not only sample). -/
theorem fair_gauges_disagree :
    applyUnitaryI fairSuperpos ≠ applyConj fairSuperpos := by
  intro h
  -- mulI (1,0)=(0,1); conj (1,0)=(1,0)
  simp [applyUnitaryI, applyConj, mapAmp, GaussInt.mulI, GaussInt.conj, fairSuperpos] at h

end Amp2

/-! ## Gauge kind labels -/

inductive GaugeKind where
  | unitaryPhaseI
  | antiunitaryConj
deriving DecidableEq, Repr

theorem gauge_kinds_distinct :
    GaugeKind.unitaryPhaseI ≠ GaugeKind.antiunitaryConj := by
  decide

/-- Sesquilinear action class: preserve vs conjugate the form. -/
inductive SesquiAction where
  | preserves
  | conjugates
deriving DecidableEq, Repr

def sesquiActionOf : GaugeKind → SesquiAction
  | .unitaryPhaseI => .preserves
  | .antiunitaryConj => .conjugates

theorem sesqui_action_separates_gauges :
    sesquiActionOf .unitaryPhaseI ≠ sesquiActionOf .antiunitaryConj := by
  decide

/-- Full Wigner theorem (all Born-preserving symmetries) remains open. -/
def fullWignerTheorem_open : Prop := True

theorem full_wigner_theorem_marked_open : fullWignerTheorem_open := trivial

/-- **Wigner-style sesquilinear package** (this residual; not full Wigner). -/
theorem wigner_style_sesqui_package :
    (∀ u v : GaussInt, GaussInt.sesqui (GaussInt.mulI u) (GaussInt.mulI v) =
      GaussInt.sesqui u v) ∧
    (∀ u v : GaussInt, GaussInt.sesqui (GaussInt.conj u) (GaussInt.conj v) =
      GaussInt.conj (GaussInt.sesqui u v)) ∧
    GaussInt.sesqui (GaussInt.conj GaussInt.sampleU) (GaussInt.conj GaussInt.sampleV) ≠
      GaussInt.sesqui GaussInt.sampleU GaussInt.sampleV ∧
    GaussInt.mulI (GaussInt.conj GaussInt.sample) ≠
      GaussInt.conj (GaussInt.mulI GaussInt.sample) ∧
    sesquiActionOf .unitaryPhaseI = .preserves ∧
    sesquiActionOf .antiunitaryConj = .conjugates ∧
    fullWignerTheorem_open :=
  ⟨GaussInt.mulI_preserves_sesqui, GaussInt.conj_conjugates_sesqui,
    GaussInt.conj_changes_sample_sesqui, GaussInt.mulI_conj_noncommute,
    rfl, rfl, trivial⟩

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end UnitaryAntiunitaryGauge
end QM

#print axioms QM.UnitaryAntiunitaryGauge.GaussInt.mulI_preserves_normSq
#print axioms QM.UnitaryAntiunitaryGauge.GaussInt.gauges_disagree_on_sample
#print axioms QM.UnitaryAntiunitaryGauge.Amp2.unitaryI_preserves_born
#print axioms QM.UnitaryAntiunitaryGauge.Amp2.conj_preserves_born
#print axioms QM.UnitaryAntiunitaryGauge.Amp2.fair_gauges_disagree
#print axioms QM.UnitaryAntiunitaryGauge.wigner_style_sesqui_package
#print axioms QM.UnitaryAntiunitaryGauge.GaussInt.mulI_preserves_sesqui
#print axioms QM.UnitaryAntiunitaryGauge.structure_not_auth
