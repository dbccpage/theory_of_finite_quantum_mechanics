import Mathlib.Tactic
import FiniteQFTAndGravity

/-!
# Campaign TFQ-0199: Do Not Treat the GR Holonomy Scaffold or the 2D Regge Sum as the 4D Gravity Shadow

Formalizes the finite rational gravity proxy vs. 2D/scaffold gravity separation certificate for
`TFQ-0199` (`IMPLEMENTATION_SIBLING`):

1. **4D Exact Rational Regge Proxy (`exact_regge::action::rational_regge_proxy`)**:
   On an orthogonal 4-simplex (pentatope) with $\binom{5}{3} = 10$ triangular hinges $h$ of
   exact rational squared area $A_h^2 \in \mathbb{Q}_{\ge 0}$ and rational defect parameter
   $\kappa_h \in \mathbb{Q}$, the 4D rational proxy action is
   $$S_{\text{proxy}} = \sum_{h=0}^{9} A_h^2 \, \kappa_h \in \mathbb{Q}, \qquad
     K_{\text{tot}} = \sum_{h=0}^{9} \kappa_h \in \mathbb{Q},$$
   with flat decision `flat_chart_admitted(S_proxy) ↔ S_proxy = 0` (`flat_einstein_hilbert() = 0`).
   For an orthogonal right pentatope with legs $1$ at vertex $0$, the $6$ right-triangle hinges
   incident to $0$ have $A_h^2 = 1/4$ (from $16 A^2 = 4(1)(1) - (1+1-2)^2 = 4$), and the $4$
   equilateral hinges on the opposite tetrahedron (edge squared $2$) have
   $A_h^2 = 3/4$ (from $16 A^2 = 4(2)(2) - (2+2-2)^2 = 12$).

2. **Exact Flat Admission Rejects Float Cutoffs (`10^{-9}` Defect Witness)**:
   Assigning $\kappa_{h_0} = 1 / 10^9$ on a single right hinge ($A_{h_0}^2 = 1/4$) gives
   $S_{\text{proxy}} = 1 / 4000000000 \ne 0$, so `flatChartAdmitted` is false even though
   $|S_{\text{proxy}}| < 10^{-6}$.

3. **2D Vertex-Deficit Regge Calculus (`regge_calculus.rs` / `einstein_hilbert_action.rs`)**:
   In 2D Regge calculus on a fan of $n$ equilateral triangles around an interior vertex $v_0$,
   each triangle contributes interior angle $\pi / 3$ (a transcendental arccosine $\arccos(1/2)$),
   and the normalized rational-angle proxy $\delta_{\pi}(n) = 2 - n/3$ (in units of $\pi$) vanishes
   at $n = 6$ and equals $+1$ (representing $\pi$) at $n = 3$. Its carrier has dimension $d = 2$
   with hinges on $0$-simplices (vertices, where hinge volume is $1$), whereas the 4D proxy has
   dimension $d = 4$ with hinges on $2$-simplices (triangles, weighted by $A_h^2$).

4. **Carrier & Scaffold Fence (`discrete_spacetime.rs`, `majorana/holonomy.rs`, `FiniteQFTAndGravity.lean`)**:
   - `discrete_spacetime.rs` provides only the combinatorial $f$-vector and Euler characteristic
     $\chi(\Delta^n) = \sum_{k=0}^n (-1)^k \binom{n+1}{k+1} = 1$, with zero metric or curvature data.
   - `majorana/holonomy.rs` evaluates $\mathbb{F}_2$ face residuals $d_1 A \pmod 2$ and $\mathbb{Z}[\zeta_{16}]$
     walks on 2-complexes, not $\mathrm{SO}(4, \mathbb{Q})$ hinge holonomies on 4-simplices.
   - `FiniteQFTAndGravity.lean` keeps $\pi$ and square roots out of its exact rational identities
     (`grDeflection gm c b = 2 * newtonDeflection gm c b` and `mercuryPerOrbitArcsec` using exact
     integer arcseconds $6 \times 648000 = 3888000$).

AuthorityEffect: None
-/

namespace CampaignTfq0199ImplementationSibling

/-- Number of $k$-simplices in the standard $n$-simplex $\Delta^n$: $\binom{n+1}{k+1}$. -/
def standardSimplexCount (n k : Nat) : Nat :=
  Nat.choose (n + 1) (k + 1)

/-- Theorem 1: Combinatorial simplex counts differentiate the 2D triangle $\Delta^2$
    (`discrete_spacetime::tests::triangle_has_three_edges`, max dimension $2$, $3$ vertices,
    $3$ edges, $1$ triangle, $0$ pentatopes) from the 4D pentatope $\Delta^4$
    (max dimension $4$, $5$ vertices, $10$ edges, $10$ triangular hinges, $5$ tetrahedra,
    $1$ pentatope). -/
theorem simplex_carrier_dimension_separation :
    standardSimplexCount 2 0 = 3 ∧
    standardSimplexCount 2 1 = 3 ∧
    standardSimplexCount 2 2 = 1 ∧
    standardSimplexCount 2 4 = 0 ∧
    standardSimplexCount 4 0 = 5 ∧
    standardSimplexCount 4 1 = 10 ∧
    standardSimplexCount 4 2 = 10 ∧
    standardSimplexCount 4 3 = 5 ∧
    standardSimplexCount 4 4 = 1 ∧
    standardSimplexCount 2 2 ≠ standardSimplexCount 4 2 := by
  decide

/-- Euler characteristic of $\Delta^2$ and $\Delta^4$ from alternating face counts. -/
def eulerCharDelta2 : Int :=
  (standardSimplexCount 2 0 : Int) - (standardSimplexCount 2 1 : Int) + (standardSimplexCount 2 2 : Int)

def eulerCharDelta4 : Int :=
  (standardSimplexCount 4 0 : Int) - (standardSimplexCount 4 1 : Int) +
  (standardSimplexCount 4 2 : Int) - (standardSimplexCount 4 3 : Int) +
  (standardSimplexCount 4 4 : Int)

/-- Theorem 2: Both $\Delta^2$ and $\Delta^4$ have Euler characteristic $\chi = 1$,
    showing that `DiscreteSpacetime::euler_characteristic` is a topological invariant of
    contractible simplices and does not distinguish 2D from 4D Regge geometry. -/
theorem euler_characteristic_contractible_invariance :
    eulerCharDelta2 = 1 ∧
    eulerCharDelta4 = 1 ∧
    eulerCharDelta2 = eulerCharDelta4 := by
  decide

/-- Cayley-Menger squared area of a triangle with squared edge lengths $(s_{01}, s_{02}, s_{12})$:
    $A^2 = \frac{2(s_{01}s_{02} + s_{01}s_{12} + s_{02}s_{12}) - (s_{01}^2 + s_{02}^2 + s_{12}^2)}{16}$. -/
def cayleyMengerAreaSq (s01 s02 s12 : ℚ) : ℚ :=
  (2 * (s01 * s02 + s01 * s12 + s02 * s12) - (s01 * s01 + s02 * s02 + s12 * s12)) / 16

/-- Theorem 3: In the orthogonal right pentatope (`exact_regge::sphere::orthogonal_pentatope`),
    each of the $6$ right triangles at the origin $(s_{01}=1, s_{02}=1, s_{12}=2)$ has exact
    rational squared area $A_{\text{right}}^2 = 1/4$, and each of the $4$ base equilateral
    triangles $(s_{01}=2, s_{02}=2, s_{12}=2)$ has exact rational squared area
    $A_{\text{equil}}^2 = 3/4$ (whose side area $\sqrt{3}/2 \notin \mathbb{Q}$ requires no square root
    when working with $A^2$). -/
theorem orthogonal_pentatope_hinge_areas_squared :
    cayleyMengerAreaSq 1 1 2 = 1 / 4 ∧
    cayleyMengerAreaSq 2 2 2 = 3 / 4 ∧
    6 * cayleyMengerAreaSq 1 1 2 + 4 * cayleyMengerAreaSq 2 2 2 = 9 / 2 := by
  norm_num [cayleyMengerAreaSq]

/-- Exact rational 4D Regge proxy action on the orthogonal pentatope for uniform right-hinge
    defect $\kappa_{\text{right}}$ and base-hinge defect $\kappa_{\text{base}}$:
    $S_{\text{proxy}} = 6 \cdot (1/4) \kappa_{\text{right}} + 4 \cdot (3/4) \kappa_{\text{base}}$. -/
def pentatopeReggeProxyAction (kappaRight kappaBase : ℚ) : ℚ :=
  6 * cayleyMengerAreaSq 1 1 2 * kappaRight + 4 * cayleyMengerAreaSq 2 2 2 * kappaBase

/-- Single-hinge 4D Regge proxy action when only one right hinge carries defect $\kappa_0$. -/
def singleRightHingeProxyAction (kappa0 : ℚ) : ℚ :=
  cayleyMengerAreaSq 1 1 2 * kappa0

/-- Exact flat Einstein-Hilbert decision (`exact_regge::action::flat_chart_admitted`). -/
def flatChartAdmitted (sProxy : ℚ) : Prop :=
  sProxy = 0

/-- Naive float-cutoff flatness check with tolerance $\varepsilon = 10^{-6}$. -/
def naiveCutoffFlat (sProxy : ℚ) : Prop :=
  |sProxy| < (1 : ℚ) / 1000000

/-- Theorem 4: Mirroring `einstein_hilbert_fence_decision_equals_proxy_action` in
    `code/rust/src/general_relativity/exact_regge/action.rs`, a single-hinge defect
    $\kappa_0 = 1 / 10^9$ produces $S_{\text{proxy}} = 1 / 4000000000 \ne 0$, which is
    rejected by `flatChartAdmitted` even though $|S_{\text{proxy}}| < 10^{-6}$ passes a float cutoff. -/
theorem exact_flat_fence_rejects_sub_cutoff_curvature :
    singleRightHingeProxyAction 0 = 0 ∧
    flatChartAdmitted (singleRightHingeProxyAction 0) ∧
    singleRightHingeProxyAction ((1 : ℚ) / 1000000000) = (1 : ℚ) / 4000000000 ∧
    ¬ flatChartAdmitted (singleRightHingeProxyAction ((1 : ℚ) / 1000000000)) ∧
    naiveCutoffFlat (singleRightHingeProxyAction ((1 : ℚ) / 1000000000)) := by
  norm_num [singleRightHingeProxyAction, cayleyMengerAreaSq, flatChartAdmitted, naiveCutoffFlat]

/-- Exact rational defect bound check (`exact_regge::action::defect_bound_holds`):
    $c \ge 0 \land a^2 \ge 0 \land (S_{\text{Regge}} - S_{\text{EH}})^2 \le (c \cdot a^2)^2$. -/
def defectBoundHolds (sRegge sEh c aSq : ℚ) : Prop :=
  0 ≤ c ∧ 0 ≤ aSq ∧ (sRegge - sEh) * (sRegge - sEh) ≤ (c * aSq) * (c * aSq)

/-- Theorem 5: Exact rational verification of `defect_bound_holds_on_exact_rationals` in
    `code/rust/src/general_relativity/exact_regge/action.rs`. -/
theorem defect_bound_exact_rational_witnesses :
    defectBoundHolds (1 / 3) (1 / 4) 2 (1 / 16) ∧
    ¬ defectBoundHolds 1 0 1 (1 / 4) ∧
    ¬ defectBoundHolds 1 0 (-1) 1 := by
  norm_num [defectBoundHolds]

/-- 2D equilateral fan interior vertex deficit in units of $\pi$:
    each equilateral triangle contributes angle $\pi/3$, so the central deficit is
    $\delta(n)/\pi = 2 - n/3$, and each of the $n$ boundary vertices (shared by $2$ triangles)
    has deficit $\delta_{\text{bdry}}/\pi = 2 - 2/3 = 4/3$, giving total 2D Regge action
    $S_{2\text{D}}(n)/\pi = (2 - n/3) + n \cdot (4/3) = 2 + n$. -/
def fan2DCenterDeficitPiUnits (n : ℚ) : ℚ :=
  2 - n / 3

def fan2DTotalActionPiUnits (n : ℚ) : ℚ :=
  fan2DCenterDeficitPiUnits n + n * (2 - 2 / 3)

/-- Theorem 6: In 2D equilateral fan Regge calculus (`regge_calculus.rs` and
    `einstein_hilbert_action.rs`), $n = 6$ triangles give a flat center ($\delta_0/\pi = 0$)
    while $n = 3$ gives positive cone deficit $\delta_0/\pi = 1$, and the total 2D action
    depends only on vertex angle sums with hinge weight $1$, whereas the 4D rational Regge
    proxy scales quadratically with edge length ($A_h^2 \propto L^4$). -/
theorem regge_2d_vertex_sum_vs_4d_area_sq_scaling (scaleSq : ℚ) :
    fan2DCenterDeficitPiUnits 6 = 0 ∧
    fan2DCenterDeficitPiUnits 3 = 1 ∧
    fan2DTotalActionPiUnits 3 = 5 ∧
    cayleyMengerAreaSq scaleSq scaleSq (2 * scaleSq) =
      (scaleSq * scaleSq) * cayleyMengerAreaSq 1 1 2 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · norm_num [fan2DCenterDeficitPiUnits]
  · norm_num [fan2DCenterDeficitPiUnits]
  · norm_num [fan2DTotalActionPiUnits, fan2DCenterDeficitPiUnits]
  · unfold cayleyMengerAreaSq
    ring

/-- Theorem 7: `majorana/holonomy.rs` computes $\mathbb{F}_2$ face holonomy residuals
    $r_f = \sum_{e \in \partial f} A_e \pmod 2 \in \{0, 1\}$, so traversing all $4$ edges of a
    plaquette with $A = (1, 1, 1, 1)$ gives $1 + 1 + 1 + 1 \equiv 0 \pmod 2$ (flat in $\mathbb{F}_2$,
    `plaquette_full_cycle_flat_in_f2`), whereas in `general_relativity/holonomy.rs` the unit
    rational quaternion $q_1 = (3/5, 4/5, 0, 0)$ satisfies $\|q_1\|^2 = 1$, $q_1 q_1^{-1} = 1$,
    but $q_1^4 = (-527/625, -336/625, 0, 0) \ne 1$. -/
theorem gf2_plaquette_holonomy_vs_rational_quaternion :
    ((1 + 1 + 1 + 1) % 2 = 0) ∧
    ((3 / 5 : ℚ) * (3 / 5) + (4 / 5) * (4 / 5) = 1) ∧
    ((3 / 5 : ℚ) * (3 / 5) - (4 / 5) * (-4 / 5) = 1) ∧
    ((3 / 5 : ℚ) * (-4 / 5) + (4 / 5) * (3 / 5) = 0) ∧
    ((-7 / 25 : ℚ) * (-7 / 25) - (24 / 25) * (24 / 25) = -527 / 625) ∧
    ((-527 / 625 : ℚ) ≠ 1) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · decide
  · norm_num
  · norm_num
  · norm_num
  · norm_num
  · norm_num

/-- Theorem 8: Re-verifying the exact rational gravity identities from `lean4/FiniteQFTAndGravity.lean`
    (`gr_deflection_twice_newton`, `mercury_per_orbit_arcsec`, `null_probe_traceless`) which keep
    $\pi$ and square roots out of the Lean 4 kernel by expressing perihelion shift in exact integer
    arcseconds ($6 \times 648000 = 3888000$). -/
theorem finite_qft_and_gravity_pi_sqrt_free_identities (gm c b a e : ℚ)
    (hc : c ≠ 0) (hb : b ≠ 0) :
    FiniteQFTAndGravity.grDeflection gm c b =
      2 * FiniteQFTAndGravity.newtonDeflection gm c b ∧
    FiniteQFTAndGravity.mercuryPerOrbitArcsec gm a e c =
      3888000 * gm / (a * (1 - e * e) * c * c) ∧
    FiniteQFTAndGravity.minkowskiTrace (FiniteQFTAndGravity.flowTensor e ⟨1, 1, 0, 0⟩) = 0 := by
  refine ⟨(FiniteQFTAndGravity.gr_deflection_twice_newton gm c b hc hb).1,
          FiniteQFTAndGravity.mercury_per_orbit_arcsec gm a e c,
          (FiniteQFTAndGravity.null_probe_traceless e).2.2⟩

/-- Structure packaging the non-conflation fence between the 4D rational Regge proxy and the
    2D/scaffold modules (`holonomy.rs`, `regge_calculus.rs`, `discrete_spacetime.rs`,
    `einstein_hilbert_action.rs`). -/
structure GravityShadowFenceCertificate where
  dim2d : Nat
  dim4d : Nat
  hinges4d : Nat
  flatProxyAdmitted : Bool
  curvedProxyAdmitted : Bool
  naiveFloatAdmitted : Bool
  dimSeparated : dim2d ≠ dim4d
  hingesCountTen : hinges4d = 10
  exactFenceSound : flatProxyAdmitted = true ∧ curvedProxyAdmitted = false ∧ naiveFloatAdmitted = true

/-- Canonical witness for `TFQ-0199`. -/
def canonicalGravityShadowFence : GravityShadowFenceCertificate where
  dim2d := 2
  dim4d := 4
  hinges4d := standardSimplexCount 4 2
  flatProxyAdmitted := true
  curvedProxyAdmitted := false
  naiveFloatAdmitted := true
  dimSeparated := by decide
  hingesCountTen := by decide
  exactFenceSound := by decide

/-- Theorem 9: The canonical gravity shadow fence certificate is inhabited and separates
    the 2D deficit calculus and $\mathbb{F}_2$ holonomy scaffold from the 4D rational Regge proxy. -/
theorem canonical_gravity_shadow_fence_valid :
    canonicalGravityShadowFence.dim2d = 2 ∧
    canonicalGravityShadowFence.dim4d = 4 ∧
    canonicalGravityShadowFence.hinges4d = 10 ∧
    canonicalGravityShadowFence.flatProxyAdmitted = true ∧
    canonicalGravityShadowFence.curvedProxyAdmitted = false ∧
    canonicalGravityShadowFence.naiveFloatAdmitted = true := by
  decide

/-- Theorem 10: Master scope certificate for `TFQ-0199` (`IMPLEMENTATION_SIBLING`). -/
theorem tfq0199_gr_holonomy_regge_not_4d_gravity_shadow_scope_certificate :
    (standardSimplexCount 2 2 = 1 ∧ standardSimplexCount 4 2 = 10) ∧
    (eulerCharDelta2 = 1 ∧ eulerCharDelta4 = 1) ∧
    (cayleyMengerAreaSq 1 1 2 = 1 / 4 ∧ cayleyMengerAreaSq 2 2 2 = 3 / 4) ∧
    (¬ flatChartAdmitted (singleRightHingeProxyAction ((1 : ℚ) / 1000000000)) ∧
     naiveCutoffFlat (singleRightHingeProxyAction ((1 : ℚ) / 1000000000))) ∧
    (defectBoundHolds (1 / 3) (1 / 4) 2 (1 / 16) ∧
     ¬ defectBoundHolds 1 0 1 (1 / 4)) ∧
    (fan2DCenterDeficitPiUnits 6 = 0 ∧ fan2DCenterDeficitPiUnits 3 = 1) ∧
    (((1 + 1 + 1 + 1) % 2 = 0) ∧ ((-527 / 625 : ℚ) ≠ 1)) := by
  refine ⟨⟨by decide, by decide⟩, ⟨by decide, by decide⟩, ?_, ?_, ?_, ?_, ⟨by decide, by norm_num⟩⟩
  · exact ⟨orthogonal_pentatope_hinge_areas_squared.1, orthogonal_pentatope_hinge_areas_squared.2.1⟩
  · exact ⟨exact_flat_fence_rejects_sub_cutoff_curvature.2.2.2.1,
           exact_flat_fence_rejects_sub_cutoff_curvature.2.2.2.2⟩
  · exact ⟨defect_bound_exact_rational_witnesses.1,
           defect_bound_exact_rational_witnesses.2.1⟩
  · exact ⟨(regge_2d_vertex_sum_vs_4d_area_sq_scaling 1).1,
           (regge_2d_vertex_sum_vs_4d_area_sq_scaling 1).2.1⟩

end CampaignTfq0199ImplementationSibling
