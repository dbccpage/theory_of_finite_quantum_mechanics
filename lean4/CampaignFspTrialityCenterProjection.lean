import Mathlib.Tactic

/-!
# Campaign: FSP-TRIALITY-CENTER-PROJECTION (TFQ-1202 / FSP-DERIV-038)

Formalizes the canonical-ensemble $\mathbb{Z}_3$ center projection in the
Eisenstein-cyclotomic ring $\mathbb{Z}[\omega]$ ($\omega^2 + \omega + 1 = 0$),
what fractional-triality phases it removes vs what zero-triality baryon signs persist,
simplicial Y-junction coboundary nilpotence $d_1 \circ d_0 = 0$ and 2-cochain curvature,
Polyakov loop center action shifts, and `GIN-C10` / `GIN-C11` scope fences for
`FSP-TRIALITY-CENTER-PROJECTION` (`TFQ-1202`, stage `FERMION_SIGN`, status `OPEN`).
-/

namespace CampaignFspTrialityCenterProjection

/-- Elements $a + b\omega$ of the Eisenstein-cyclotomic ring $\mathbb{Z}[\omega]$
    where $\omega = e^{i 2\pi / 3}$ satisfies $\omega^2 = -1 - \omega$ and $\omega^3 = 1$. -/
@[ext]
structure ZOmega where
  a : Int
  b : Int
  deriving DecidableEq, Repr

/-- Addition in $\mathbb{Z}[\omega]$. -/
def zomegaAdd (x y : ZOmega) : ZOmega :=
  { a := x.a + y.a, b := x.b + y.b }

/-- Scalar multiplication in $\mathbb{Z}[\omega]$. -/
def zomegaScale (c : Int) (x : ZOmega) : ZOmega :=
  { a := c * x.a, b := c * x.b }

/-- Multiplication in $\mathbb{Z}[\omega]$ using $\omega^2 = -1 - \omega$:
    $(a_1 + b_1\omega)(a_2 + b_2\omega) = (a_1 a_2 - b_1 b_2) + (a_1 b_2 + b_1 a_2 - b_1 b_2)\omega$. -/
def zomegaMul (x y : ZOmega) : ZOmega :=
  { a := x.a * y.a - x.b * y.b
    b := x.a * y.b + x.b * y.a - x.b * y.b }

/-- Zero and cube roots of unity $1, \omega, \omega^2 \in \mathbb{Z}[\omega]$. -/
def zomegaZero : ZOmega := { a := 0, b := 0 }
def zomegaOne : ZOmega := { a := 1, b := 0 }
def zomegaOmega : ZOmega := { a := 0, b := 1 }
def zomegaOmegaSq : ZOmega := { a := -1, b := -1 }

/-- $\mathbb{Z}_3$ center phase $\omega^{n \bmod 3} \in \mathbb{Z}[\omega]$. -/
def z3Phase (n : Int) : ZOmega :=
  match n % 3 with
  | 0 => zomegaOne
  | 1 => zomegaOmega
  | _ => zomegaOmegaSq

/-- Unnormalized canonical-ensemble $\mathbb{Z}_3$ center projector sum
    $\Pi_{\mathbb{Z}_3}(q) = \sum_{k \in \{0, 1, 2\}} \omega^{q k} \in \mathbb{Z}[\omega]$. -/
def z3CenterProjectorSum (q : Int) : ZOmega :=
  zomegaAdd (zomegaAdd (z3Phase (q * 0)) (z3Phase (q * 1))) (z3Phase (q * 2))

/-- Theorem 1: In $\mathbb{Z}[\omega]$, the primitive cube root $\omega$ satisfies
    $\omega^2 = -1 - \omega$, $\omega^3 = 1$, and the cyclotomic character sum
    $1 + \omega + \omega^2 = 0$. -/
theorem z3_roots_of_unity_group_law :
    zomegaMul zomegaOmega zomegaOmega = zomegaOmegaSq ∧
    zomegaMul zomegaOmega zomegaOmegaSq = zomegaOne ∧
    zomegaAdd (zomegaAdd zomegaOne zomegaOmega) zomegaOmegaSq = zomegaZero := by
  decide

/-- Theorem 2: The canonical-ensemble $\mathbb{Z}_3$ center projector sum
    $\Pi_{\mathbb{Z}_3}(q) = \sum_{k=0}^2 \omega^{q k}$ equals $3$ when $q \equiv 0 \pmod 3$
    (zero-triality color-singlet meson/baryon sectors) and vanishes identically ($0$)
    when $q \equiv 1, 2 \pmod 3$ (fractional-triality quark and diquark sectors). -/
theorem canonical_z3_center_projection_identity (q : Int) :
    (q % 3 = 0 → z3CenterProjectorSum q = { a := 3, b := 0 }) ∧
    (q % 3 = 1 → z3CenterProjectorSum q = zomegaZero) ∧
    (q % 3 = 2 → z3CenterProjectorSum q = zomegaZero) := by
  refine ⟨fun h0 => ?_, fun h1 => ?_, fun h2 => ?_⟩
  · have hq0 : (q * 0) % 3 = 0 := by omega
    have hq1 : (q * 1) % 3 = 0 := by omega
    have hq2 : (q * 2) % 3 = 0 := by omega
    dsimp [z3CenterProjectorSum, z3Phase]
    rw [hq0, hq1, hq2]
    decide
  · have hq0 : (q * 0) % 3 = 0 := by omega
    have hq1 : (q * 1) % 3 = 1 := by omega
    have hq2 : (q * 2) % 3 = 2 := by omega
    dsimp [z3CenterProjectorSum, z3Phase]
    rw [hq0, hq1, hq2]
    decide
  · have hq0 : (q * 0) % 3 = 0 := by omega
    have hq1 : (q * 1) % 3 = 2 := by omega
    have hq2 : (q * 2) % 3 = 1 := by omega
    dsimp [z3CenterProjectorSum, z3Phase]
    rw [hq0, hq1, hq2]
    decide

/-- Theorem 3: For every triality charge $q \in \mathbb{Z}$, the unnormalized $\mathbb{Z}_3$
    center projector satisfies $\Pi_{\mathbb{Z}_3}(q)^2 = 3 \Pi_{\mathbb{Z}_3}(q)$
    (so $\frac{1}{3} \Pi_{\mathbb{Z}_3}$ is idempotent). -/
theorem z3_center_projector_idempotence (q : Int) :
    zomegaMul (z3CenterProjectorSum q) (z3CenterProjectorSum q) =
      zomegaScale 3 (z3CenterProjectorSum q) := by
  have hmod : q % 3 = 0 ∨ q % 3 = 1 ∨ q % 3 = 2 := by omega
  have hproj := canonical_z3_center_projection_identity q
  rcases hmod with h0 | h1 | h2
  · rw [hproj.1 h0]
    decide
  · rw [hproj.2.1 h1]
    decide
  · rw [hproj.2.2 h2]
    decide

/-- Grand-canonical partition decomposition $Z(z_k) = Z_0 + \omega^k Z_1 + \omega^{2k} Z_2$
    at center element $z_k = \omega^k$ ($k \in \{0, 1, 2\}$). -/
def centerTwistedPartition (Z0 Z1 Z2 : Int) (k : Int) : ZOmega :=
  zomegaAdd
    (zomegaAdd (zomegaScale Z0 (z3Phase 0)) (zomegaScale Z1 (z3Phase k)))
    (zomegaScale Z2 (z3Phase (2 * k)))

/-- Sum of center-twisted partition functions $\sum_{k=0}^2 Z(z_k)$. -/
def centerProjectedPartitionSum (Z0 Z1 Z2 : Int) : ZOmega :=
  zomegaAdd
    (zomegaAdd (centerTwistedPartition Z0 Z1 Z2 0) (centerTwistedPartition Z0 Z1 Z2 1))
    (centerTwistedPartition Z0 Z1 Z2 2)

/-- Theorem 4: Averaging $Z(z_k) = Z_0 + \omega^k Z_1 + \omega^{2k} Z_2$ over the three
    $\mathbb{Z}_3$ center sectors $k \in \{0, 1, 2\}$ removes the fractional-triality
    amplitudes $Z_1$ and $Z_2$ completely and isolates $3 Z_0$. -/
theorem canonical_z3_sector_fourier_isolation (Z0 Z1 Z2 : Int) :
    centerProjectedPartitionSum Z0 Z1 Z2 = { a := 3 * Z0, b := 0 } := by
  have h0 : z3Phase 0 = zomegaOne := by decide
  have h1 : z3Phase 1 = zomegaOmega := by decide
  have h2 : z3Phase 2 = zomegaOmegaSq := by decide
  have h4 : z3Phase 4 = zomegaOmega := by decide
  dsimp [centerProjectedPartitionSum, centerTwistedPartition]
  rw [h0, h1, h2, h4]
  dsimp [zomegaAdd, zomegaScale, zomegaOne, zomegaOmega, zomegaOmegaSq]
  ext <;> ring

/-- Theorem 5: While $\mathbb{Z}_3$ center projection eliminates the fractional-triality
    sectors $Z_1$ and $Z_2$, if the zero-triality baryon sector $Z_0 = w_{B,+} - w_{B,-}$
    contains opposite-sign baryon contributions with $w_{B,-} > w_{B,+} > 0$, the center-projected
    partition sum $3(w_{B,+} - w_{B,-}) < 0$ remains strictly negative (showing that center
    projection does not eliminate sign oscillations inside the zero-triality baryon sector). -/
theorem zero_triality_baryon_sector_sign_persistence (wBPos wBNeg Z1 Z2 : Int)
    (hPos : 0 < wBPos) (hDom : wBPos < wBNeg) :
    (centerProjectedPartitionSum (wBPos - wBNeg) Z1 Z2).b = 0 ∧
    (centerProjectedPartitionSum (wBPos - wBNeg) Z1 Z2).a = 3 * (wBPos - wBNeg) ∧
    (centerProjectedPartitionSum (wBPos - wBNeg) Z1 Z2).a < 0 ∧
    0 < wBPos + wBNeg := by
  rw [canonical_z3_sector_fourier_isolation]
  dsimp
  refine ⟨rfl, rfl, by omega, by omega⟩

/-- Simplicial Y-junction coboundary $d_0 : \mathbb{Z}^4 \to \mathbb{Z}^6$ and
    $d_1 : \mathbb{Z}^6 \to \mathbb{Z}^3$ from `SU3SimplicialYJunction` in
    `code/python/src/fsp/su3_baryon_triality.py`. -/
def yJunctionD0 (v0 v1 v2 v3 : Int) : Int × Int × Int × Int × Int × Int :=
  (v1 - v0, v2 - v0, v3 - v0, v2 - v1, v3 - v2, v1 - v3)

def yJunctionD1 (e0 e1 e2 e3 e4 e5 : Int) : Int × Int × Int :=
  (e0 - e1 + e3, e1 - e2 + e4, -e0 + e2 + e5)

/-- Theorem 6: On the 4-vertex, 6-edge, 3-face simplicial Y-junction complex,
    the boundary/coboundary operators satisfy exact nilpotence $d_1(d_0(v)) = (0, 0, 0)$
    for every 0-cochain $(v_0, v_1, v_2, v_3) \in \mathbb{Z}^4$. -/
theorem y_junction_simplicial_nilpotence_d1_d0 (v0 v1 v2 v3 : Int) :
    let (e0, e1, e2, e3, e4, e5) := yJunctionD0 v0 v1 v2 v3
    yJunctionD1 e0 e1 e2 e3 e4 e5 = (0, 0, 0) := by
  dsimp [yJunctionD0, yJunctionD1]
  ext <;> ring

/-- L1 norm of a 2-cochain on the 3 triangular plaquettes of the Y-junction. -/
def yJunctionL1Curvature (f0 f1 f2 : Int) : Nat :=
  Int.natAbs f0 + Int.natAbs f1 + Int.natAbs f2

/-- Theorem 7: On the Y-junction complex, a uniform spoke cochain $(s, s, s, 0, 0, 0)$
    has zero 2-cochain curvature $d_1 c = (0, 0, 0)$, whereas the color-singlet 3-spoke
    cochain $(2, 1, -3, 0, 0, 0)$ (scaled by 2 from $(1.0, 0.5, -1.5)$ in
    `su3_baryon_triality.py`) satisfies color-singlet closure $2 + 1 + (-3) = 0$ and
    has non-zero 2-cochain coboundary $(1, 4, -5)$ with L1 norm $10 > 0$. -/
theorem su3_cartan_singlet_y_junction_curvature (s : Int) :
    yJunctionD1 s s s 0 0 0 = (0, 0, 0) ∧
    (2 : Int) + 1 + (-3) = 0 ∧
    yJunctionD1 2 1 (-3) 0 0 0 = (1, 4, -5) ∧
    yJunctionL1Curvature 1 4 (-5) = 10 := by
  refine ⟨?_, by decide, by decide, by decide⟩
  dsimp [yJunctionD1]
  ext <;> ring

/-- Scaled Polyakov-loop effective fermion action shifts $S_F(k)$ in center sector
    $k \in \{0, 1, 2\}$ from `su3_polyakov_loop.py` ($S_F(0) = -12 h P$, $S_F(1) = S_F(2) = 6 h P$). -/
def polyakovSectorAction (h P : Int) (k : Fin 3) : Int :=
  if k = 0 then -12 * h * P else 6 * h * P

/-- Theorem 8: Across the three $\mathbb{Z}_3$ Polyakov-loop sectors $k \in \{0, 1, 2\}$,
    the effective action shifts sum to zero ($S_F(0) + S_F(1) + S_F(2) = 0$), and for
    $h > 0, P > 0$, the center action gap between $k = 1, 2$ and $k = 0$ is
    $\Delta S = S_F(1) - S_F(0) = 18 h P > 0$. -/
theorem polyakov_center_sector_action_sum_and_gap (h P : Int) (hh : 0 < h) (hP : 0 < P) :
    polyakovSectorAction h P 0 + polyakovSectorAction h P 1 + polyakovSectorAction h P 2 = 0 ∧
    polyakovSectorAction h P 1 - polyakovSectorAction h P 0 = 18 * h * P ∧
    0 < 18 * h * P := by
  dsimp [polyakovSectorAction]
  have h_prod : 0 < h * P := mul_pos hh hP
  refine ⟨by ring, by ring, by linarith⟩

/-- Theorem 9: Scope fence (`GIN-C11`) — in the confined limit $P = 0$ where the
    Polyakov-loop action gap vanishes ($\Delta S = 0$) and each sector has equal magnitude
    weight $w > 0$, the 1 positive ($k = 0$) vs 2 negative ($k = 1, 2$) sector multiplicity
    leaves net unpartnered weight $w - 2 w = -w \neq 0$. -/
theorem gin_c11_confined_sector_multiplicity_imbalance (w : Int) (hw : 0 < w) :
    polyakovSectorAction 1 0 1 - polyakovSectorAction 1 0 0 = 0 ∧
    w - 2 * w = -w ∧
    w - 2 * w < 0 := by
  dsimp [polyakovSectorAction]
  refine ⟨by decide, by omega, by omega⟩

/-- Scope fence structure (`GIN-C10` / `GIN-C11`): separates finite $\mathbb{Z}_3$ center
    projection and Y-junction cochain fixtures from dense lattice QCD sign-problem resolution. -/
structure TrialityFixtureInterpretation where
  z3ProjectorIsolatesZeroTriality : Bool
  yJunctionNilpotent : Bool
  solvesDenseQcdSignProblem : Bool
  deriving DecidableEq, Repr

/-- Projection retaining only the verified $\mathbb{Z}_3$ algebraic and cochain invariants. -/
def trialityVerifiedCore (x : TrialityFixtureInterpretation) : Bool × Bool :=
  (x.z3ProjectorIsolatesZeroTriality, x.yJunctionNilpotent)

/-- Theorem 10: Scope fence (`GIN-C10` / `GIN-C11`) — the verified $\mathbb{Z}_3$ center
    projection and Y-junction cochain identities are compatible with both asserting and
    withholding a dense lattice QCD sign-problem solution, justifying keeping status `OPEN`. -/
theorem gin_c10_c11_historical_fixture_scope_fence :
    let overclaimedInterp : TrialityFixtureInterpretation :=
      { z3ProjectorIsolatesZeroTriality := true
        yJunctionNilpotent := true
        solvesDenseQcdSignProblem := true }
    let scopedInterp : TrialityFixtureInterpretation :=
      { z3ProjectorIsolatesZeroTriality := true
        yJunctionNilpotent := true
        solvesDenseQcdSignProblem := false }
    trialityVerifiedCore overclaimedInterp = trialityVerifiedCore scopedInterp ∧
    overclaimedInterp ≠ scopedInterp ∧
    overclaimedInterp.solvesDenseQcdSignProblem ≠ scopedInterp.solvesDenseQcdSignProblem := by
  decide

end CampaignFspTrialityCenterProjection
