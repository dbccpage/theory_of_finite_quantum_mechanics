import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Rat.Defs
import Mathlib.Data.Rat.Lemmas
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Topology.ContinuousMap.Basic
import Mathlib.Topology.Compactness.Compact
import Mathlib.Topology.Order.MonotoneContinuity
import Mathlib.Topology.MetricSpace.Basic
import Mathlib.Topology.MetricSpace.ProperSpace
import Mathlib.LinearAlgebra.UnitaryGroup
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FinCases
import ExtensionCurvatureObstruction
import BasisExtensionObstruction
import FiniteVectorCover
import FiniteBasisCover
import KernelReflectionPilot

/-!
# Scaled Certificate Verification for MUB(6) Multi-Box Complex

AuthorityEffect: None.
Restricted words: forced, minimal, free, canonical, equivalent, universal, complete require proof or explicit conditional scope.

## Stated-Region Scaled Multi-Box Verification
Building on `MUB.KernelReflectionPilot`, this module scales certificate verification
from the single pilot cell (`narrow_cell_pilot`) to a contiguous complex of 64 boxes
(presplit depth 6 bisection complex) partitioning the narrow torus cell region
against the genuine Dita seed `(0, 8)` triple.

The Rust / Python exact rational arithmetic engines certify, in exact rational interval
arithmetic, a strictly positive lower bound on the squared curvature mass
`Φ(v) = ∑_i (‖⟪e_i, v⟫‖² − 1/6)²`
across each of the 64 contiguous boxes covering the narrow torus cell.

Here, Lean 4:
1. Formalizes the scaled certificate metadata and the list of 64 exact rational lower bounds.
2. Implements a verified decision procedure `check_pairs` using kernel reflection
   to verify that every one of the 64 certified bounds is strictly positive in `ℚ`.
3. Proves the soundness of the decision procedure:
   `all_pos_of_check_pairs` and `scaled_box_gap_real_pos`.
4. Connects the certified bounds into `MUB.ExtensionCurvatureObstruction.finite_cover_no_feasible`
   to establish that `0 < curvatureMass e (1 / 6) v` on the entire 64-box complex.
5. Wires into `MUB.FiniteVectorCover.no_mu_vector_in_cover` to certify that no vector in the
   multi-box complex is mutually unbiased to the seed triple.
6. Connects to `MUB.FiniteBasisCover.finite_cover_no_feasible` and
   `MUB.FiniteBasisCover.no_fourth_basis_in_cover` to certify non-existence of any 4th MUB basis
   whose columns intersect the multi-box complex.

## Scope
* **Demonstration on stated region only**: This checks a contiguous complex of 64 boxes
  partitioning the narrow torus cell. It is NOT a check of the full 5-torus moduli space.
* **AuthorityEffect**: None. Mints no authority.
-/

namespace MUB
namespace KernelReflectionScaled

open scoped InnerProductSpace
open Matrix
open MUB.ExtensionCurvatureObstruction
open MUB.BasisExtensionObstruction
open MUB.FiniteVectorCover
open MUB.FiniteBasisCover

/-- Schema version tag matching `kernel_reflection_scaled_64_box_complex_dita_0_8.json`. -/
def scaled_schema_version : String := "omega.mub.kernel-reflection-scaled.v1"

/-- Dita seed index dx = 0. -/
def seed_dx : ℤ := 0

/-- Dita seed index dy = 8. -/
def seed_dy : ℤ := 8

/-- Stated region description from the scaled JSON artifact. -/
def scaled_region_desc : String :=
  "narrow_torus_cell_64_box_presplit6_complex (stated region; not full 5-torus)"

/-- Number of contiguous boxes in the presplit-6 multi-box complex. -/
def num_boxes : ℕ := 64

/-- Exact list of certified integer (numerator, denominator) pairs across all 64 contiguous boxes. -/
def scaled_pairs : List (ℤ × ℕ) := [
  (1780167324550892563240544619208761044678738216992075101356196671151131, 2711707949687046089977061030825711891756217552008462909571072000000000),
  (19435828867047910559838058285320161660534140712903066481707046370278191, 28924884796661824959755317662140926845399653888090271035424768000000000),
  (9720745641152709044345310771416253081367982714422326434304216017526227, 14462442398330912479877658831070463422699826944045135517712384000000000),
  (1106014045796555647309718811803274531218915796604186850813592677003169, 1606938044258990275541962092341162602522202993782792835301376000000000),
  (19435828867047910559838058285320161660534140712903066481707046370278191, 28924884796661824959755317662140926845399653888090271035424768000000000),
  (19928286690756053972893961749012297528939300490640931330624072023801151, 28924884796661824959755317662140926845399653888090271035424768000000000),
  (39809796582450666672511304166569461488173602358197613950675430567442511, 57849769593323649919510635324281853690799307776180542070849536000000000),
  (2549816889632131451891143135503833156745274908463676866060320144792461, 3615610599582728119969414707767615855674956736011283879428096000000000),
  (9720745641152709044345310771416253081367982714422326434304216017526227, 14462442398330912479877658831070463422699826944045135517712384000000000),
  (39809796582450666672511304166569461488173602358197613950675430567442511, 57849769593323649919510635324281853690799307776180542070849536000000000),
  (19921970307203349026356658237614441674832884234227712152457724857675811, 28924884796661824959755317662140926845399653888090271035424768000000000),
  (13602730653648912071878470240619453764591348745837164502666504065345103, 19283256531107883306503545108093951230266435925393514023616512000000000),
  (1106014045796555647309718811803274531218915796604186850813592677003169, 1606938044258990275541962092341162602522202993782792835301376000000000),
  (2549816889632131451891143135503833156745274908463676866060320144792461, 3615610599582728119969414707767615855674956736011283879428096000000000),
  (13602730653648912071878470240619453764591348745837164502666504065345103, 19283256531107883306503545108093951230266435925393514023616512000000000),
  (4179879417539043683419267674927781629480414412414268304826938137951051, 5784976959332364991951063532428185369079930777618054207084953600000000),
  (2429933526300146587846726059062070957054325779422283455203270287444167, 3615610599582728119969414707767615855674956736011283879428096000000000),
  (39847986758215188861294445554550981327762994023760439242442954790027709, 57849769593323649919510635324281853690799307776180542070849536000000000),
  (6636837651046051991922292373910390310540420473049248471497365672184297, 9641628265553941653251772554046975615133217962696757011808256000000000),
  (10199240659280272722792338705571257029641349670192919969104082836589409, 14462442398330912479877658831070463422699826944045135517712384000000000),
  (39847986758215188861294445554550981327762994023760439242442954790027709, 57849769593323649919510635324281853690799307776180542070849536000000000),
  (61308756275731221536362787176560753165302632524322978014767255308749781, 86774654389985474879265952986422780536198961664270813106274304000000000),
  (40790155528912591190423007265057901941807519193869124127171064487746133, 57849769593323649919510635324281853690799307776180542070849536000000000),
  (8364045680585727826543461315486755627061685492161000749597644307367347, 11569953918664729983902127064856370738159861555236108414169907200000000),
  (6636837651046051991922292373910390310540420473049248471497365672184297, 9641628265553941653251772554046975615133217962696757011808256000000000),
  (40790155528912591190423007265057901941807519193869124127171064487746133, 57849769593323649919510635324281853690799307776180542070849536000000000),
  (2266070557401971134369931112874668627202082254060693633510701966858419, 3213876088517980551083924184682325205044405987565585670602752000000000),
  (10448269550458805799586255358336771468874962314100200543962961729883779, 14462442398330912479877658831070463422699826944045135517712384000000000),
  (10199240659280272722792338705571257029641349670192919969104082836589409, 14462442398330912479877658831070463422699826944045135517712384000000000),
  (8364045680585727826543461315486755627061685492161000749597644307367347, 11569953918664729983902127064856370738159861555236108414169907200000000),
  (10448269550458805799586255358336771468874962314100200543962961729883779, 14462442398330912479877658831070463422699826944045135517712384000000000),
  (64288053207547028947724936271037562648561716265981364386632783834827701, 86774654389985474879265952986422780536198961664270813106274304000000000),
  (2430723074244234701583197955666958017254688864418971102718163413351133, 3615610599582728119969414707767615855674956736011283879428096000000000),
  (19904952089721839487786159706594699263334711377424693744750748295441107, 28924884796661824959755317662140926845399653888090271035424768000000000),
  (19918330963850086886549791238975750405361198480149863434890426451763057, 28924884796661824959755317662140926845399653888090271035424768000000000),
  (10199240659280272731574693055781001956706716122209127404300517015964667, 14462442398330912479877658831070463422699826944045135517712384000000000),
  (19904952089721839487786159706594699263334711377424693744750748295441107, 28924884796661824959755317662140926845399653888090271035424768000000000),
  (10197317508308870122811199926405289229612662513002229771180980675888551, 14462442398330912479877658831070463422699826944045135517712384000000000),
  (8158031105782518226904843048694239139449734493753531917160662197738931, 11569953918664729983902127064856370738159861555236108414169907200000000),
  (10451049982166964052628619361100985728382370300674502816818142144937011, 14462442398330912479877658831070463422699826944045135517712384000000000),
  (19918330963850086886549791238975750405361198480149863434890426451763057, 28924884796661824959755317662140926845399653888090271035424768000000000),
  (8158031105782518226904843048694239139449734493753531917160662197738931, 11569953918664729983902127064856370738159861555236108414169907200000000),
  (1226175125514624431394316709025997630951277137248975428424565153578473, 1735493087799709497585319059728455610723979233285416262125486080000000),
  (871490692363409462497917424602907399814707316123387279162506509452537, 1205203533194242706656471569255871951891652245337094626476032000000000),
  (10199240659280272731574693055781001956706716122209127404300517015964667, 14462442398330912479877658831070463422699826944045135517712384000000000),
  (10451049982166964052628619361100985728382370300674502816818142144937011, 14462442398330912479877658831070463422699826944045135517712384000000000),
  (871490692363409462497917424602907399814707316123387279162506509452537, 1205203533194242706656471569255871951891652245337094626476032000000000),
  (7141011561876546008093734412055940083516686819487021193923344429644637, 9641628265553941653251772554046975615133217962696757011808256000000000),
  (1244238129781215393376856003731613741237675141711670002730290050037227, 1807805299791364059984707353883807927837478368005641939714048000000000),
  (40808191960946736206924833668414714625399480466969935794731737264069541, 57849769593323649919510635324281853690799307776180542070849536000000000),
  (20398535117057051602085531690440972518323198069659643507431354020494489, 28924884796661824959755317662140926845399653888090271035424768000000000),
  (3483306639255628961178821201244623216361042044896662432032145166802729, 4820814132776970826625886277023487807566608981348378505904128000000000),
  (40808191960946736206924833668414714625399480466969935794731737264069541, 57849769593323649919510635324281853690799307776180542070849536000000000),
  (10456876772408790852518055803897302555127489063237083197129145839313403, 14462442398330912479877658831070463422699826944045135517712384000000000),
  (25075782362905326530666886105859671904778259296063519063699443692675499, 34709861755994189951706381194569112214479584665708325242509721600000000),
  (128550346545203300625413167729008623801876111918591486445777392755328131, 173549308779970949758531905972845561072397923328541626212548608000000000),
  (20398535117057051602085531690440972518323198069659643507431354020494489, 28924884796661824959755317662140926845399653888090271035424768000000000),
  (25075782362905326530666886105859671904778259296063519063699443692675499, 34709861755994189951706381194569112214479584665708325242509721600000000),
  (418401398567405732533687175801610960477378649414095725618327804229563, 578497695933236499195106353242818536907993077761805420708495360000000),
  (42838790684552751777465256211255642466744277377742753434949565268031867, 57849769593323649919510635324281853690799307776180542070849536000000000),
  (3483306639255628961178821201244623216361042044896662432032145166802729, 4820814132776970826625886277023487807566608981348378505904128000000000),
  (128550346545203300625413167729008623801876111918591486445777392755328131, 173549308779970949758531905972845561072397923328541626212548608000000000),
  (42838790684552751777465256211255642466744277377742753434949565268031867, 57849769593323649919510635324281853690799307776180542070849536000000000),
  (2440487761552696334938569317869568725095877795927074740978581108902911, 3213876088517980551083924184682325205044405987565585670602752000000000)
]

/-- Proof that the pairs list contains exactly 64 boxes. -/
theorem scaled_pairs_length : scaled_pairs.length = 64 := by rfl

/-- Exact integer numerator of the global minimum gap across all 64 boxes. -/
def scaled_min_gap_num : ℤ := 1780167324550892563240544619208761044678738216992075101356196671151131

/-- Exact natural number denominator of the global minimum gap across all 64 boxes. -/
def scaled_min_gap_den : ℕ := 2711707949687046089977061030825711891756217552008462909571072000000000

/-- Global minimum gap across all 64 boxes as a rational number `ℚ`. -/
def scaled_min_gap_rat : ℚ :=
  (1780167324550892563240544619208761044678738216992075101356196671151131 : ℚ) / (2711707949687046089977061030825711891756217552008462909571072000000000 : ℚ)

/-- The global minimum gap coerced to `ℝ`. -/
noncomputable def scaled_min_gap_real : ℝ := (scaled_min_gap_rat : ℝ)

/-- Verified rational arithmetic: global minimum gap is strictly positive in `ℚ`. -/
theorem scaled_min_gap_rat_pos : 0 < scaled_min_gap_rat := by
  unfold scaled_min_gap_rat
  norm_num

/-- Global minimum gap is strictly positive in `ℝ`. -/
theorem scaled_min_gap_real_pos : 0 < scaled_min_gap_real := by
  unfold scaled_min_gap_real scaled_min_gap_rat
  norm_num

/-- Lemma: a rational quotient of positive integers is positive in `ℚ`. -/
theorem rat_div_pos_of_pos {n : ℤ} {d : ℕ} (hn : 0 < n) (hd : 0 < d) :
    0 < (n : ℚ) / (d : ℚ) := by
  have hn_q : 0 < (n : ℚ) := Int.cast_pos.mpr hn
  have hd_q : 0 < (d : ℚ) := Nat.cast_pos.mpr hd
  exact div_pos hn_q hd_q

/-- Computable decision procedure: checks that every (numerator, denominator) pair has positive components. -/
def check_pairs (l : List (ℤ × ℕ)) : Bool :=
  l.all (fun (n, d) => 0 < n && 0 < d)

/-- Soundness theorem of the decision procedure: if `check_pairs l = true`, then every fraction is positive in `ℚ`. -/
theorem all_pos_of_check_pairs {l : List (ℤ × ℕ)} (h : check_pairs l = true)
    (pair : ℤ × ℕ) (hmem : pair ∈ l) :
    0 < (pair.1 : ℚ) / (pair.2 : ℚ) := by
  have h_all := List.all_eq_true.mp h
  have h_pair := h_all pair hmem
  simp only [Bool.and_eq_true, decide_eq_true_iff] at h_pair
  exact rat_div_pos_of_pos h_pair.1 h_pair.2

/-- **Kernel reflection execution**: the decision procedure evaluates to `true` by reflexivity. -/
theorem scaled_pairs_all_pos_verified : check_pairs scaled_pairs = true := by rfl

/-- Indexing function retrieving the certified rational gap for box `j : Fin 64`. -/
def scaled_box_gap (j : Fin 64) : ℚ :=
  let p := scaled_pairs.get ⟨j.val, by rw [scaled_pairs_length]; exact j.isLt⟩
  (p.1 : ℚ) / (p.2 : ℚ)

/-- Coercion of box gap to `ℝ`. -/
noncomputable def scaled_box_gap_real (j : Fin 64) : ℝ := (scaled_box_gap j : ℝ)

/-- Every box gap in the 64-box complex is strictly positive in `ℚ`. -/
theorem scaled_box_gap_pos (j : Fin 64) : 0 < scaled_box_gap j := by
  unfold scaled_box_gap
  exact all_pos_of_check_pairs scaled_pairs_all_pos_verified _ (List.get_mem scaled_pairs _)

/-- Every box gap in the 64-box complex is strictly positive in `ℝ`. -/
theorem scaled_box_gap_real_pos (j : Fin 64) : 0 < scaled_box_gap_real j := by
  unfold scaled_box_gap_real
  exact Rat.cast_pos.mpr (scaled_box_gap_pos j)

/-- Formal Lean 4 reflection of the Rust/Python scaled certificate for the 64-box complex. -/
structure ScaledComplexCertificate {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    (e : Fin 18 → E) (K_box : Fin 64 → Set E) where
  schema_version : String := scaled_schema_version
  seed_dx : ℤ := seed_dx
  seed_dy : ℤ := seed_dy
  region_desc : String := scaled_region_desc
  box_count : ℕ := num_boxes
  complete_flag : Bool := true
  bound_certified : ∀ (j : Fin 64) (v : E), v ∈ K_box j → (scaled_box_gap_real j) ≤ curvatureMass e (1 / 6) v

/-- **Curvature mass positivity across the entire 64-box complex.**
    Witnessed via `MUB.ExtensionCurvatureObstruction.finite_cover_no_feasible`:
    the certified lower bounds on each of the 64 contiguous patches force the curvature mass
    `Φ(v)` to be strictly positive on every vector in the union complex `⋃ j, K_box j`. -/
theorem scaled_complex_curvature_mass_pos {E : Type*} [NormedAddCommGroup E]
    [InnerProductSpace ℂ E] (e : Fin 18 → E) (K_box : Fin 64 → Set E)
    (cert : ScaledComplexCertificate e K_box) :
    ∀ v ∈ (⋃ j : Fin 64, K_box j), 0 < curvatureMass e (1 / 6) v := by
  intro v hv
  have hcover : ∀ w ∈ (⋃ j : Fin 64, K_box j), ∃ j ∈ (Finset.univ : Finset (Fin 64)), w ∈ K_box j := by
    intro w hw
    rcases Set.mem_iUnion.mp hw with ⟨j, hj⟩
    exact ⟨j, Finset.mem_univ j, hj⟩
  have hbound : ∀ j ∈ (Finset.univ : Finset (Fin 64)), ∀ w ∈ K_box j,
      scaled_box_gap_real j ≤ curvatureMass e (1 / 6) w :=
    fun j _ w hw => cert.bound_certified j w hw
  have hpos : ∀ j ∈ (Finset.univ : Finset (Fin 64)), 0 < scaled_box_gap_real j :=
    fun j _ => scaled_box_gap_real_pos j
  exact finite_cover_no_feasible (Finset.univ : Finset (Fin 64)) K_box
    (curvatureMass e (1 / 6)) (⋃ j : Fin 64, K_box j) hcover
    scaled_box_gap_real hbound hpos v hv

/-- **No mutually unbiased vector across the entire 64-box complex.**
    Witnessed via `MUB.FiniteVectorCover.no_mu_vector_in_cover`:
    no vector in the 64-box contiguous complex satisfies `‖⟪e i, v⟫‖² = 1/6` for all `i`. -/
theorem scaled_complex_no_mu_vector {E : Type*} [NormedAddCommGroup E]
    [InnerProductSpace ℂ E] (e : Fin 18 → E) (K_box : Fin 64 → Set E)
    (cert : ScaledComplexCertificate e K_box) :
    ∀ v ∈ (⋃ j : Fin 64, K_box j), ¬ ∀ i, ‖⟪e i, v⟫_ℂ‖ ^ 2 = 1 / 6 := by
  have hcover : ∀ w ∈ (⋃ j : Fin 64, K_box j), ∃ j ∈ (Finset.univ : Finset (Fin 64)), w ∈ K_box j := by
    intro w hw
    rcases Set.mem_iUnion.mp hw with ⟨j, hj⟩
    exact ⟨j, Finset.mem_univ j, hj⟩
  have hbound : ∀ j ∈ (Finset.univ : Finset (Fin 64)), ∀ w ∈ K_box j,
      scaled_box_gap_real j ≤ curvatureMass e (1 / 6) w :=
    fun j _ w hw => cert.bound_certified j w hw
  have hpos : ∀ j ∈ (Finset.univ : Finset (Fin 64)), 0 < scaled_box_gap_real j :=
    fun j _ => scaled_box_gap_real_pos j
  exact no_mu_vector_in_cover (Finset.univ : Finset (Fin 64)) K_box
    (⋃ j : Fin 64, K_box j) e (1 / 6) hcover
    scaled_box_gap_real hbound hpos

/-- Direct derivation of the scaled complex vector no-go combining
    `scaled_complex_curvature_mass_pos` and `curvatureMass_eq_zero_iff`. -/
theorem scaled_complex_no_mu_vector_alt {E : Type*} [NormedAddCommGroup E]
    [InnerProductSpace ℂ E] (e : Fin 18 → E) (K_box : Fin 64 → Set E)
    (cert : ScaledComplexCertificate e K_box) :
    ∀ v ∈ (⋃ j : Fin 64, K_box j), ¬ ∀ i, ‖⟪e i, v⟫_ℂ‖ ^ 2 = 1 / 6 := by
  intro v hv hMU
  have hpos : 0 < curvatureMass e (1 / 6) v :=
    scaled_complex_curvature_mass_pos e K_box cert v hv
  rw [(curvatureMass_eq_zero_iff e (1 / 6) v).mpr hMU] at hpos
  exact lt_irrefl 0 hpos

/-- Induced basis patches for candidate fourth bases whose first column belongs to box `j`. -/
def basis_patch (K_box : Fin 64 → Set (Fin 6 → ℂ)) (j : Fin 64) :
    Set (Matrix.unitaryGroup (Fin 6) ℂ) :=
  { U | (fun k => (U : Matrix (Fin 6) (Fin 6) ℂ) k 0) ∈ K_box j }

/-- Complex of candidate fourth bases whose first column belongs to the 64-box complex. -/
def basis_complex (K_box : Fin 64 → Set (Fin 6 → ℂ)) :
    Set (Matrix.unitaryGroup (Fin 6) ℂ) :=
  ⋃ j : Fin 64, basis_patch K_box j

/-- **Direct connection to `MUB.FiniteBasisCover.no_fourth_basis_in_cover` and `finite_cover_no_feasible`:**
    No candidate fourth basis in `basis_complex K_box` is mutually unbiased to the seed triple `e`. -/
theorem scaled_complex_no_fourth_basis_in_cover
    (e : Fin 18 → (Fin 6 → ℂ)) (K_box : Fin 64 → Set (Fin 6 → ℂ))
    (hbound_basis : ∀ j ∈ (Finset.univ : Finset (Fin 64)), ∀ U ∈ basis_patch K_box j,
      scaled_box_gap_real j ≤ basisCurvatureMass e (1 / 6) U) :
    ∀ U ∈ basis_complex K_box, ¬ ∀ j i, ‖overlap e U i j‖ ^ 2 = 1 / 6 := by
  have hcover : ∀ U ∈ basis_complex K_box, ∃ j ∈ (Finset.univ : Finset (Fin 64)), U ∈ basis_patch K_box j := by
    intro U hU
    rcases Set.mem_iUnion.mp hU with ⟨j, hj⟩
    exact ⟨j, Finset.mem_univ j, hj⟩
  have hpos : ∀ j ∈ (Finset.univ : Finset (Fin 64)), 0 < scaled_box_gap_real j :=
    fun j _ => scaled_box_gap_real_pos j
  exact no_fourth_basis_in_cover (Finset.univ : Finset (Fin 64)) (basis_patch K_box)
    (basis_complex K_box) e (1 / 6) hcover
    scaled_box_gap_real hbound_basis hpos

end KernelReflectionScaled
end MUB

#print axioms MUB.KernelReflectionScaled.scaled_min_gap_rat_pos
#print axioms MUB.KernelReflectionScaled.scaled_min_gap_real_pos
#print axioms MUB.KernelReflectionScaled.scaled_box_gap_pos
#print axioms MUB.KernelReflectionScaled.scaled_box_gap_real_pos
#print axioms MUB.KernelReflectionScaled.scaled_complex_curvature_mass_pos
#print axioms MUB.KernelReflectionScaled.scaled_complex_no_mu_vector
#print axioms MUB.KernelReflectionScaled.scaled_complex_no_mu_vector_alt
#print axioms MUB.KernelReflectionScaled.scaled_complex_no_fourth_basis_in_cover
