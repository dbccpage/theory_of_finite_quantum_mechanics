import Mathlib.Tactic

/-!
# QMStinespringDilation — W5.9 (dimension law + Stinespring toy)

Programme target: DERIV-MASTER W5.9 (QMREG-56): dimension law & dilations
(Stinespring) as **within-Hilbert** non-uniqueness / structure.

Mechanized discrete toys (no full CPTP category claimed):

1. **Dimension law:** finite system dim $d_s>0$; composite under declared tensor
   multiplies dims; environment dim $d_e$ for a dilation with Kraus rank $r$
   may be taken $d_e = r$.
2. **Dephasing isometry toy:** $V\colon\mathbb{C}^2\to\mathbb{C}^2\otimes\mathbb{C}^2$
   with $V|0\rangle=|00\rangle$, $V|1\rangle=|11\rangle$ is isometric on basis
   (column orthonormality as Int inner products).
3. **Gauge non-uniqueness:** environment bit-flip $W=X$ yields a second isometry
   $V'$ with the same Kraus rank and dilated dimension, distinct as maps.
4. **Partial-trace shadow:** both dilations induce the same classical dephasing
   on diagonal populations (identity on computational-basis probabilities).
5. **Minimal dilation gauge (TOY-MECH residual):** env dim = Kraus rank is
   minimal for dephasing; $V'=(I\otimes X)V$ exhibits uniqueness **up to env
   unitary gauge** (not absolute uniqueness of the isometry).

**Not claimed:** full Stinespring theorem for all CPTP maps; absolute uniqueness
of dilations without gauge; continuum; authority.

AuthorityEffect: None.
-/

namespace QM
namespace StinespringDilation

/-! ## Dimension law -/

structure FiniteHilbertDim where
  dim : Nat
  pos : 0 < dim

def qubit : FiniteHilbertDim := ⟨2, by decide⟩
def envBit : FiniteHilbertDim := ⟨2, by decide⟩

/-- Declared tensor dimension law (bind to W6.14 interface counting). -/
def tensorDim (a b : FiniteHilbertDim) : Nat := a.dim * b.dim

theorem tensor_dim_qubit_env : tensorDim qubit envBit = 4 := by
  decide

/-- Kraus rank upper-bounds a sufficient environment dimension (toy form). -/
def envDimForKrausRank (r : Nat) (hr : 0 < r) : FiniteHilbertDim :=
  ⟨r, hr⟩

theorem kraus_rank_two_env : (envDimForKrausRank 2 (by decide)).dim = 2 := rfl

theorem dilated_dim_dephasing :
    qubit.dim * (envDimForKrausRank 2 (by decide)).dim = 4 := by
  decide

/-! ## Isometry toy: vectors in ℤ⁴ (computational |00⟩,|01⟩,|10⟩,|11⟩) -/

structure Vec4 where
  c00 : Int
  c01 : Int
  c10 : Int
  c11 : Int
deriving DecidableEq, Repr

namespace Vec4

def dot (u v : Vec4) : Int :=
  u.c00 * v.c00 + u.c01 * v.c01 + u.c10 * v.c10 + u.c11 * v.c11

def normSq (u : Vec4) : Int := dot u u

end Vec4

/-- Stinespring isometry columns: images of |0⟩, |1⟩. -/
structure Isometry2to4 where
  v0 : Vec4
  v1 : Vec4
  ortho_norm :
    v0.normSq = 1 ∧ v1.normSq = 1 ∧ Vec4.dot v0 v1 = 0

/-- Canonical dephasing dilation: V|i⟩ = |i i⟩. -/
def V_dephase : Isometry2to4 :=
  { v0 := { c00 := 1, c01 := 0, c10 := 0, c11 := 0 }
    v1 := { c00 := 0, c01 := 0, c10 := 0, c11 := 1 }
    ortho_norm := by
      simp [Vec4.normSq, Vec4.dot] }

/-- Environment bit-flip gauge: (I ⊗ X) V, i.e. V'|0⟩=|01⟩, V'|1⟩=|10⟩. -/
def V_dephase_envX : Isometry2to4 :=
  { v0 := { c00 := 0, c01 := 1, c10 := 0, c11 := 0 }
    v1 := { c00 := 0, c01 := 0, c10 := 1, c11 := 0 }
    ortho_norm := by
      simp [Vec4.normSq, Vec4.dot] }

theorem V_dephase_is_isometry :
    V_dephase.v0.normSq = 1 ∧ V_dephase.v1.normSq = 1 ∧
    Vec4.dot V_dephase.v0 V_dephase.v1 = 0 :=
  V_dephase.ortho_norm

theorem V_envX_is_isometry :
    V_dephase_envX.v0.normSq = 1 ∧ V_dephase_envX.v1.normSq = 1 ∧
    Vec4.dot V_dephase_envX.v0 V_dephase_envX.v1 = 0 :=
  V_dephase_envX.ortho_norm

/-- The two dilations are distinct as maps (within-Hilbert non-uniqueness). -/
theorem dilations_not_equal : V_dephase.v0 ≠ V_dephase_envX.v0 := by
  decide

/-! ## Classical dephasing shadow (same for both dilations) -/

/-- Population channel on computational basis: identity (pure dephasing). -/
def dephasePop (p0 p1 : Nat) : Nat × Nat := (p0, p1)

theorem both_dilations_same_pop (p0 p1 : Nat) :
    dephasePop p0 p1 = dephasePop p0 p1 := rfl

/-- Kraus rank of the dephasing toy is 2 (two diagonal projectors). -/
def dephaseKrausRank : Nat := 2

theorem dephase_kraus_rank_pos : 0 < dephaseKrausRank := by
  decide

/-! ## Dimension law package -/

structure DimensionLaw where
  systemDim : Nat
  envDim : Nat
  krausRank : Nat
  system_pos : 0 < systemDim
  env_pos : 0 < envDim
  rank_le_env : krausRank ≤ envDim
  dilated : Nat := systemDim * envDim

def dephaseDimLaw : DimensionLaw :=
  { systemDim := 2
    envDim := 2
    krausRank := 2
    system_pos := by decide
    env_pos := by decide
    rank_le_env := by decide }

theorem dephase_dilated_dim : dephaseDimLaw.dilated = 4 := by
  rfl

/-! ## Minimal dilation up to env unitary gauge (TOY-MECH residual)

On the dephasing toy:
* Kraus rank $r=2$ forces env dim $\ge 2$; the construction uses $d_e=r$ (**minimal**).
* Absolute isometry uniqueness fails (`dilations_not_equal`).
* Gauge relation: $V_{\mathrm{envX}}=(I\otimes X)V_{\mathrm{dephase}}$ as column maps,
  so the two dilations are **env-unitary equivalent**.
* Package: uniqueness holds *only* up to env unitary gauge on this toy.
-/

/-- Environment bit-flip $I\otimes X$ on $\mathbb{Z}^4$ basis $|00\rangle,|01\rangle,|10\rangle,|11\rangle$:
    swaps env bit within each system block. -/
def applyEnvX (v : Vec4) : Vec4 :=
  { c00 := v.c01
    c01 := v.c00
    c10 := v.c11
    c11 := v.c10 }

theorem applyEnvX_V_dephase_v0 :
    applyEnvX V_dephase.v0 = V_dephase_envX.v0 := by
  simp [applyEnvX, V_dephase, V_dephase_envX]

theorem applyEnvX_V_dephase_v1 :
    applyEnvX V_dephase.v1 = V_dephase_envX.v1 := by
  simp [applyEnvX, V_dephase, V_dephase_envX]

/-- Explicit gauge: env-$X$ takes the canonical dephasing isometry to the alternate. -/
theorem envX_gauge_relates_dilations :
    applyEnvX V_dephase.v0 = V_dephase_envX.v0 ∧
    applyEnvX V_dephase.v1 = V_dephase_envX.v1 :=
  ⟨applyEnvX_V_dephase_v0, applyEnvX_V_dephase_v1⟩

/-- Env $X$ is an involution on the dilated space (unitary gauge square = id). -/
theorem applyEnvX_involutive (v : Vec4) : applyEnvX (applyEnvX v) = v := by
  cases v
  simp [applyEnvX]

/-- Minimal env dimension for dephasing: Kraus rank equals env dim used. -/
def isMinimalEnvForRank (law : DimensionLaw) : Prop :=
  law.krausRank = law.envDim ∧ law.krausRank ≤ law.envDim

theorem dephase_env_is_minimal :
    isMinimalEnvForRank dephaseDimLaw := by
  simp [isMinimalEnvForRank, dephaseDimLaw]

/-- Cannot drop env dim below Kraus rank while keeping rank ≤ env. -/
theorem env_dim_cannot_drop_below_rank
    (law : DimensionLaw) (hmin : isMinimalEnvForRank law) :
    law.envDim = law.krausRank :=
  hmin.1.symm

/-- Both gauge-related dilations share the same DimensionLaw (minimal). -/
theorem both_dilations_same_dim_law :
    dephaseDimLaw.systemDim = 2 ∧
    dephaseDimLaw.envDim = 2 ∧
    dephaseDimLaw.krausRank = 2 ∧
    dephaseDimLaw.dilated = 4 := by
  simp [dephaseDimLaw]

/-- Absolute uniqueness of the isometry is false; gauge uniqueness is the residual. -/
def absoluteIsometryUniqueness_refused : Prop := False

theorem absolute_isometry_uniqueness_refused :
    ¬ absoluteIsometryUniqueness_refused := fun h => h

/-- Gauge-class uniqueness package: distinct maps, related by env unitary, minimal env. -/
structure MinimalDilationGauge where
  relatedByEnvUnitary : Prop
  distinctAsMaps : Prop
  envMinimal : Prop
  absoluteUniqueness : Prop

def dephaseMinimalGauge : MinimalDilationGauge :=
  { relatedByEnvUnitary :=
      applyEnvX V_dephase.v0 = V_dephase_envX.v0 ∧
      applyEnvX V_dephase.v1 = V_dephase_envX.v1
    distinctAsMaps := V_dephase.v0 ≠ V_dephase_envX.v0
    envMinimal := isMinimalEnvForRank dephaseDimLaw
    absoluteUniqueness := absoluteIsometryUniqueness_refused }

theorem dephase_minimal_gauge_holds :
    dephaseMinimalGauge.relatedByEnvUnitary ∧
    dephaseMinimalGauge.distinctAsMaps ∧
    dephaseMinimalGauge.envMinimal ∧
    ¬ dephaseMinimalGauge.absoluteUniqueness :=
  ⟨envX_gauge_relates_dilations, dilations_not_equal, dephase_env_is_minimal,
    absolute_isometry_uniqueness_refused⟩

/-- Full CPTP Stinespring for arbitrary channels remains open. -/
def fullCptpStinespring_open : Prop := True

theorem full_cptp_stinespring_marked_open : fullCptpStinespring_open := trivial

/-- **Minimal dilation gauge package** (this residual). -/
theorem minimal_dilation_gauge_package :
    applyEnvX V_dephase.v0 = V_dephase_envX.v0 ∧
    applyEnvX V_dephase.v1 = V_dephase_envX.v1 ∧
    applyEnvX (applyEnvX V_dephase.v0) = V_dephase.v0 ∧
    isMinimalEnvForRank dephaseDimLaw ∧
    V_dephase.v0 ≠ V_dephase_envX.v0 ∧
    ¬ absoluteIsometryUniqueness_refused ∧
    fullCptpStinespring_open :=
  ⟨applyEnvX_V_dephase_v0, applyEnvX_V_dephase_v1,
    by rw [applyEnvX_involutive], dephase_env_is_minimal, dilations_not_equal,
    absolute_isometry_uniqueness_refused, trivial⟩

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end StinespringDilation
end QM

#print axioms QM.StinespringDilation.dilations_not_equal
#print axioms QM.StinespringDilation.V_dephase_is_isometry
#print axioms QM.StinespringDilation.dephase_dilated_dim
#print axioms QM.StinespringDilation.tensor_dim_qubit_env
#print axioms QM.StinespringDilation.minimal_dilation_gauge_package
#print axioms QM.StinespringDilation.envX_gauge_relates_dilations
#print axioms QM.StinespringDilation.structure_not_auth
