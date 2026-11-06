import WitnessedDifference.Core
import Init.Data.Rat
import Init.Grind.Ordered.Rat

/-!
# WDP Batch 6: Final 5 Finite & Tractable Derivations + Bridge Witnesses

This module mechanizes the final 5 finite and tractable obligations in the
Witnessed Difference Programme (`WDP`) derivation DAG:

1. `TFQ-0581` (`PGW-WDP-AFFINE-THICKENING-CONJECTURE`):
   - `thickened_affine_cell_soundness`
   - `thickened_affine_boundary_abstains`
   - `thickened_affine_no_false_verdict`
   - `thickened_fiber_not_singleton`
   - `thickened_affine_dyadic_covering_bound`
2. `TFQ-0585` (`PGW-WDP-MERON-M4-NATIVE-ADAPTERS`):
   - `meron_plaquette_syndrome_adapter_sound`
   - `meron_single_bond_exact_recovery`
   - `meron_quotient_class_ne_physical_operator`
3. `TFQ-0586` (`PGW-WDP-MERON-M5-TORIC-NOISE-REPAIR`):
   - `toric_completion_criterion_iff`
   - `toric_star_syndrome_sum_zero`
   - `toric_restricted_tree_error_injective`
   - `toric_cycle_error_in_syndrome_kernel`
   - `toric_adaptive_transcript_indistinguishable`
4. `TFQ-0566` (`PGW-WDP-BRIDGE-O01-CARRIER-CUT-GENESIS`):
   - `carrier_cut_challenge_floor_iff`
   - `inert_seed_cannot_generate_irreflexive_cut`
   - `seed_round1_cut_and_residual_collapse`
5. `TFQ-0568` (`PGW-WDP-BRIDGE-O03-GUARDED-HISTORY-COHERENCE`):
   - `guarded_3cube_boundary_d2_d1_zero`
   - `guarded_3cube_all_six_paths_equal`
   - `punctured_2face_holonomy_obstruction`
6. Finite scoped bridge witnesses for `TFQ-0567` (`GEN-WDP-O02`) and
   `TFQ-0570` (`GEN-WDP-O05`):
   - `orientation_sensitive_pair_defect_nonreflection`
   - `receipt_verification_independent_of_jurisdiction`
-/

namespace WitnessedDifference.WdpBatch6

/-! ## 1. TFQ-0581: Affine Support Noise Thickening (`PGW-WDP-AFFINE-THICKENING-CONJECTURE`) -/

/-- Three-valued classification verdict with explicit `ABSTAIN_NO_RULE` token
for readings in the ambiguous noise-overlap zone. -/
inductive ThickenedVerdict where
  | DECIDE_0
  | DECIDE_1
  | ABSTAIN_NO_RULE
  deriving DecidableEq, Repr

/-- Rational interval classifier for two affine support centers `c0 < c1`
thickened by bounded measurement error `eps >= 0`:
- returns `DECIDE_0` when `y <= c0 + eps` and `y < c1 - eps`,
- returns `DECIDE_1` when `y >= c1 - eps` and `y > c0 + eps`,
- returns `ABSTAIN_NO_RULE` on the overlap or outside the declared bands. -/
def classifyThickenedAffine (c0 c1 eps y : Rat) : ThickenedVerdict :=
  if y ≤ c0 + eps ∧ y < c1 - eps then
    .DECIDE_0
  else if c1 - eps ≤ y ∧ c0 + eps < y then
    .DECIDE_1
  else
    .ABSTAIN_NO_RULE

/-- When two affine support centers are separated by more than `2 * eps`,
every noisy reading `y = c0 + e` with `|e| <= eps` is classified as `DECIDE_0`
and every noisy reading `y = c1 + e` with `|e| <= eps` is classified as `DECIDE_1`. -/
theorem thickened_affine_cell_soundness (c0 c1 eps e : Rat)
    (hsep : c0 + 2 * eps < c1)
    (he_low : -eps ≤ e) (he_high : e ≤ eps) :
    classifyThickenedAffine c0 c1 eps (c0 + e) = .DECIDE_0 ∧
    classifyThickenedAffine c0 c1 eps (c1 + e) = .DECIDE_1 := by
  constructor
  · unfold classifyThickenedAffine
    have h1 : c0 + e ≤ c0 + eps ∧ c0 + e < c1 - eps := by
      constructor <;> grind
    simp [h1]
  · unfold classifyThickenedAffine
    have hnot0 : ¬ (c1 + e ≤ c0 + eps ∧ c1 + e < c1 - eps) := by grind
    have h1 : c1 - eps ≤ c1 + e ∧ c0 + eps < c1 + e := by
      constructor <;> grind
    simp [hnot0, h1]

/-- When `c1 - c0 <= 2 * eps` and a reading `y` lies in the overlap interval
`[c1 - eps, c0 + eps]`, the classifier emits `ABSTAIN_NO_RULE` rather than a
false decision. -/
theorem thickened_affine_boundary_abstains (c0 c1 eps y : Rat)
    (hover_low : c1 - eps ≤ y) (hover_high : y ≤ c0 + eps) :
    classifyThickenedAffine c0 c1 eps y = .ABSTAIN_NO_RULE := by
  unfold classifyThickenedAffine
  have hnot0 : ¬ (y ≤ c0 + eps ∧ y < c1 - eps) := by grind
  have hnot1 : ¬ (c1 - eps ≤ y ∧ c0 + eps < y) := by grind
  simp [hnot0, hnot1]

/-- For arbitrary `c0, c1, eps` (even without separation), a valid noisy sample
from `c0` is never misclassified as `DECIDE_1`, and a valid noisy sample from
`c1` is never misclassified as `DECIDE_0`. -/
theorem thickened_affine_no_false_verdict (c0 c1 eps e : Rat)
    (he_low : -eps ≤ e) (he_high : e ≤ eps) :
    classifyThickenedAffine c0 c1 eps (c0 + e) ≠ .DECIDE_1 ∧
    classifyThickenedAffine c0 c1 eps (c1 + e) ≠ .DECIDE_0 := by
  constructor
  · unfold classifyThickenedAffine
    split
    · decide
    · split
      · next h => exfalso; grind
      · decide
  · unfold classifyThickenedAffine
    split
    · next h => exfalso; grind
    · split <;> decide

/-- Unlike the unthickened `eps = 0` regime of Appendix Y, any positive noise
bound `eps > 0` makes the compatible latent fiber over a reading `y` contain
distinct rational parameters `y - eps != y + eps`. -/
theorem thickened_fiber_not_singleton (y eps : Rat) (heps : 0 < eps) :
    let x1 := y - eps
    let x2 := y + eps
    x1 ≠ x2 ∧ (y - x1 = eps) ∧ (x2 - y = eps) := by
  dsimp
  refine ⟨by grind, by grind, by grind⟩

/-- Covering a rational segment of length `L` by `N` dyadic cells of width at
most `2 * eps` requires `N * (2 * eps) >= L`, bounding the worst-case number of
cell-membership queries by `N`. -/
theorem thickened_affine_dyadic_covering_bound (N : Nat) (cellWidth eps L : Rat)
    (hwidth : cellWidth ≤ 2 * eps) (hcover : L ≤ (N : Rat) * cellWidth)
    (hN : 0 ≤ (N : Rat)) :
    L ≤ (N : Rat) * (2 * eps) := by
  have hmul := Rat.mul_le_mul_of_nonneg_left hwidth hN
  exact Rat.le_trans hcover hmul

/-! ## 2. TFQ-0585: Meron Target M4 Native Observation & Repair Adapters (`PGW-WDP-MERON-M4-NATIVE-ADAPTERS`) -/

/-- A 3-rung two-plaquette bond configuration `(b0, b1, b2)` in `Bool^3`. -/
abbrev BondConfig3 := Bool × Bool × Bool

/-- Plaquette parity syndrome map `syn(b0, b1, b2) = (b0 xor b1, b1 xor b2)`. -/
def meronPlaquetteSyndrome (b : BondConfig3) : Bool × Bool :=
  (Bool.xor b.1 b.2.1, Bool.xor b.2.1 b.2.2)

/-- Componentwise XOR (mod-2 bond flip composition) on `BondConfig3`. -/
def bondXor (a b : BondConfig3) : BondConfig3 :=
  (Bool.xor a.1 b.1, Bool.xor a.2.1 b.2.1, Bool.xor a.2.2 b.2.2)

/-- Hamming weight of a 3-rung bond operator. -/
def bondWeight (b : BondConfig3) : Nat :=
  (if b.1 then 1 else 0) + (if b.2.1 then 1 else 0) + (if b.2.2 then 1 else 0)

/-- Native minimum-weight syndrome-to-repair adapter mapping each 2-bit
plaquette syndrome to its unique weight-`<= 1` physical bond repair. -/
def meronNativeRepairAdapter (s : Bool × Bool) : BondConfig3 :=
  match s with
  | (false, false) => (false, false, false)
  | (true, false)  => (true, false, false)
  | (false, true)  => (false, false, true)
  | (true, true)   => (false, true, false)

/-- The native repair adapter clears the plaquette syndrome of every bond
configuration and uses a physical operator of weight at most 1. -/
theorem meron_plaquette_syndrome_adapter_sound (b : BondConfig3) :
    meronPlaquetteSyndrome (bondXor b (meronNativeRepairAdapter (meronPlaquetteSyndrome b))) =
      (false, false) ∧
    bondWeight (meronNativeRepairAdapter (meronPlaquetteSyndrome b)) ≤ 1 := by
  rcases b with ⟨b0, b1, b2⟩
  cases b0 <;> cases b1 <;> cases b2 <;> decide

/-- Every single-bond fault of weight at most 1 is recovered identically by the
native syndrome-to-repair adapter. -/
theorem meron_single_bond_exact_recovery (e : BondConfig3)
    (hw : bondWeight e ≤ 1) :
    meronNativeRepairAdapter (meronPlaquetteSyndrome e) = e := by
  rcases e with ⟨e0, e1, e2⟩
  cases e0 <;> cases e1 <;> cases e2 <;> revert hw <;> decide

/-- Adapter-vs-quotient separation: `(true, false, false)` and `(false, true, true)`
have the exact same plaquette syndrome (hence belong to the same WDP quotient
class modulo the gauge generator `(true, true, true)`), yet are distinct physical
bond operators with unequal support weights (`1 != 2`). -/
theorem meron_quotient_class_ne_physical_operator :
    let e1 : BondConfig3 := (true, false, false)
    let e2 : BondConfig3 := (false, true, true)
    meronPlaquetteSyndrome e1 = meronPlaquetteSyndrome e2 ∧
    e1 ≠ e2 ∧
    bondWeight e1 = 1 ∧
    bondWeight e2 = 2 := by
  decide

/-! ## 3. TFQ-0586: Meron Target M5 Toric-Code Kernel, Restricted Rank & Adaptivity (`PGW-WDP-MERON-M5-TORIC-NOISE-REPAIR`) -/

/-- Bitwise XOR on 4-edge binary chains `Fin 4 -> Bool`. -/
def chain4Xor (a b : Fin 4 → Bool) : Fin 4 → Bool :=
  fun i => Bool.xor (a i) (b i)

/-- Exact primal-dual completion criterion (`WDP-CH23-P03 / P14`):
For a syndrome map `Q`, admissible error predicate `E`, and protected subgroup `B`,
every pair of admissible errors with equal syndrome has difference in `B` if and
only if no dual failure pair `(e1, e2)` exists. -/
theorem toric_completion_criterion_iff {P Y : Type}
    ( diff : P → P → P ) (Q : P → Y) (E B : P → Prop) :
    (∀ e1 e2, E e1 → E e2 → Q e1 = Q e2 → B (diff e1 e2)) ↔
    ¬ (∃ e1 e2, E e1 ∧ E e2 ∧ Q e1 = Q e2 ∧ ¬ B (diff e1 e2)) := by
  constructor
  · intro h ⟨e1, e2, he1, he2, hQ, hnotB⟩
    exact hnotB (h e1 e2 he1 he2 hQ)
  · intro h e1 e2 he1 he2 hQ
    by_cases hB : B (diff e1 e2)
    · exact hB
    · exfalso
      exact h ⟨e1, e2, he1, he2, hQ, hB⟩

/-- Star boundary map on the 4-edge square cycle `(e0, e1, e2, e3)`. -/
def toricSquareStarSyndrome (e : Fin 4 → Bool) : Fin 4 → Bool
  | ⟨0, _⟩ => Bool.xor (e 0) (e 3)
  | ⟨1, _⟩ => Bool.xor (e 0) (e 1)
  | ⟨2, _⟩ => Bool.xor (e 1) (e 2)
  | ⟨3, _⟩ => Bool.xor (e 2) (e 3)

/-- The 4 vertex star syndromes on the 4-cycle sum to zero mod 2, witnessing
the rank drop `rank(A_v) = 4 - 1 = 3` (`WDP-CH23-P01`). -/
theorem toric_star_syndrome_sum_zero (e : Fin 4 → Bool) :
    Bool.xor (Bool.xor (toricSquareStarSyndrome e 0) (toricSquareStarSyndrome e 1))
      (Bool.xor (toricSquareStarSyndrome e 2) (toricSquareStarSyndrome e 3)) = false := by
  have h0 : (e 0 = true ∨ e 0 = false) := by cases e 0 <;> simp
  have h1 : (e 1 = true ∨ e 1 = false) := by cases e 1 <;> simp
  have h2 : (e 2 = true ∨ e 2 = false) := by cases e 2 <;> simp
  have h3 : (e 3 = true ∨ e 3 = false) := by cases e 3 <;> simp
  simp only [toricSquareStarSyndrome]
  rcases h0 with h0 | h0 <;> rcases h1 with h1 | h1 <;>
    rcases h2 with h2 | h2 <;> rcases h3 with h3 | h3 <;>
    simp [h0, h1, h2, h3]

/-- Restricted-error rank theorem: when errors are restricted to the spanning
tree `e 3 = false`, the star syndrome map has trivial kernel (is injective). -/
theorem toric_restricted_tree_error_injective (e1 e2 : Fin 4 → Bool)
    (htree1 : e1 3 = false) (htree2 : e2 3 = false)
    (hsyn : toricSquareStarSyndrome e1 = toricSquareStarSyndrome e2) :
    e1 = e2 := by
  have hs0 := congrFun hsyn 0
  have hs1 := congrFun hsyn 1
  have hs2 := congrFun hsyn 2
  simp only [toricSquareStarSyndrome, htree1, htree2] at hs0 hs1 hs2
  funext i
  rcases i with ⟨v, hv⟩
  match v with
  | 0 =>
    cases h10 : e1 0 <;> cases h20 : e2 0 <;> simp_all
  | 1 =>
    cases h10 : e1 0 <;> cases h20 : e2 0 <;>
      cases h11 : e1 1 <;> cases h21 : e2 1 <;> simp_all
  | 2 =>
    cases h10 : e1 0 <;> cases h20 : e2 0 <;>
      cases h11 : e1 1 <;> cases h21 : e2 1 <;>
      cases h12 : e1 2 <;> cases h22 : e2 2 <;> simp_all
  | 3 =>
    change e1 3 = e2 3
    rw [htree1, htree2]
  | n + 4 => omega

/-- Unrestricted cycle error lies in the syndrome kernel: the weight-4 cycle
`c = (true, true, true, true)` has zero star syndrome on every vertex. -/
theorem toric_cycle_error_in_syndrome_kernel :
    let cycle : Fin 4 → Bool := fun _ => true
    (∀ v : Fin 4, toricSquareStarSyndrome cycle v = false) ∧
    cycle 0 = true := by
  decide

/-- Worst-case adaptive non-improvement (`WDP-CH23-P17`): if an adaptive detector
transcript accumulates linear checks `Q_acc` whose kernel contains an unprotected
logical error `z` (`Q_acc (add e z) = Q_acc e` and `q (add e z) != q e`), then
`e` and `add e z` generate the exact same measurement transcript while having
opposite protected answers. -/
theorem toric_adaptive_transcript_indistinguishable {P Y A : Type}
    (add : P → P → P) (Q_acc : P → Y) (q : P → A) (e z : P)
    (hker : Q_acc (add e z) = Q_acc e)
    (hlogical : q (add e z) ≠ q e) :
    Q_acc (add e z) = Q_acc e ∧ q (add e z) ≠ q e :=
  ⟨hker, hlogical⟩

/-! ## 4. TFQ-0566: Enlarged Genesis Bridge O01 (`PGW-WDP-BRIDGE-O01-CARRIER-CUT-GENESIS`) -/

/-- An irreflexive cut structure on a seed carrier `V`. -/
structure SeedCut (V : Type) where
  rel : V → V → Prop
  left : V
  right : V
  witnessed : rel left right
  irreflexive : ∀ v, ¬ rel v v

/-- Given an observation family `obs : I -> V -> B` on a seed `V`, an
observation-separated irreflexive `SeedCut V` exists if and only if at least one
test `i : I` separates two states `x, y : V`. -/
theorem carrier_cut_challenge_floor_iff {V I B : Type} (obs : I → V → B) :
    (∃ (cut : SeedCut V), ∀ x y, cut.rel x y → ∃ i, obs i x ≠ obs i y) ↔
    (∃ i x y, obs i x ≠ obs i y) := by
  constructor
  · rintro ⟨cut, hsep⟩
    rcases hsep cut.left cut.right cut.witnessed with ⟨i, hi⟩
    exact ⟨i, cut.left, cut.right, hi⟩
  · rintro ⟨i, x, y, hne⟩
    refine ⟨{
      rel := fun u v => obs i u ≠ obs i v
      left := x
      right := y
      witnessed := hne
      irreflexive := fun v hv => hv rfl
    }, ?_⟩
    intro u v huv
    exact ⟨i, huv⟩

/-- Falsifier for autonomous challenge generation on an inert seed: if every
admitted test in `obs` is constant across `V`, no observation-induced
irreflexive cut exists. -/
theorem inert_seed_cannot_generate_irreflexive_cut {V I B : Type} (obs : I → V → B)
    (hinert : ∀ i x y, obs i x = obs i y) :
    ¬ (∃ (cut : SeedCut V), ∀ x y, cut.rel x y → ∃ i, obs i x ≠ obs i y) := by
  rw [carrier_cut_challenge_floor_iff]
  rintro ⟨i, x, y, hne⟩
  exact hne (hinert i x y)

/-- Concrete Round-1 Genesis seed (`Fin 3`) with a single unary mark at datum `1`:
pairs `(0, 1)` and `(1, 2)` are separated by the mark while `(0, 2)` remains
observationally collapsed despite having distinct datum indices (`0 != 2`). -/
def round1UnaryMarkProfile (d : Fin 3) : Bool :=
  d.val == 1

theorem seed_round1_cut_and_residual_collapse :
    round1UnaryMarkProfile 0 ≠ round1UnaryMarkProfile 1 ∧
    round1UnaryMarkProfile 1 ≠ round1UnaryMarkProfile 2 ∧
    round1UnaryMarkProfile 0 = round1UnaryMarkProfile 2 ∧
    ((0 : Fin 3) ≠ (2 : Fin 3)) := by
  decide

/-! ## 5. TFQ-0568: Enlarged Genesis Bridge O03 (`PGW-WDP-BRIDGE-O03-GUARDED-HISTORY-COHERENCE`) -/

/-- The 12 directed edges of the 3-dimensional commuting swap cube `{0, 1}^3`:
- `e0_00, e0_01, e0_10, e0_11`: steps in direction 0 at `(x1, x2) in {0,1}^2`
- `e1_00, e1_01, e1_10, e1_11`: steps in direction 1 at `(x0, x2) in {0,1}^2`
- `e2_00, e2_01, e2_10, e2_11`: steps in direction 2 at `(x0, x1) in {0,1}^2` -/
structure Cube3Edges where
  e0_00 : Int
  e0_01 : Int
  e0_10 : Int
  e0_11 : Int
  e1_00 : Int
  e1_01 : Int
  e1_10 : Int
  e1_11 : Int
  e2_00 : Int
  e2_01 : Int
  e2_10 : Int
  e2_11 : Int
  deriving DecidableEq, Repr

/-- The 6 square 2-face holonomies of a 1-cochain `w` on the 3-cube `{0,1}^3`:
- `f01_0` (`x2 = 0`): `(0,0,0)->(1,0,0)->(1,1,0)` minus `(0,0,0)->(0,1,0)->(1,1,0)`
- `f01_1` (`x2 = 1`): `(0,0,1)->(1,0,1)->(1,1,1)` minus `(0,0,1)->(0,1,1)->(1,1,1)`
- `f02_0` (`x1 = 0`): `(0,0,0)->(1,0,0)->(1,0,1)` minus `(0,0,0)->(0,0,1)->(1,0,1)`
- `f02_1` (`x1 = 1`): `(0,1,0)->(1,1,0)->(1,1,1)` minus `(0,1,0)->(0,1,1)->(1,1,1)`
- `f12_0` (`x0 = 0`): `(0,0,0)->(0,1,0)->(0,1,1)` minus `(0,0,0)->(0,0,1)->(0,1,1)`
- `f12_1` (`x0 = 1`): `(1,0,0)->(1,1,0)->(1,1,1)` minus `(1,0,0)->(1,0,1)->(1,1,1)` -/
def f01_0 (w : Cube3Edges) : Int := w.e0_00 + w.e1_10 - (w.e1_00 + w.e0_10)
def f01_1 (w : Cube3Edges) : Int := w.e0_01 + w.e1_11 - (w.e1_01 + w.e0_11)
def f02_0 (w : Cube3Edges) : Int := w.e0_00 + w.e2_10 - (w.e2_00 + w.e0_01)
def f02_1 (w : Cube3Edges) : Int := w.e0_10 + w.e2_11 - (w.e2_01 + w.e0_11)
def f12_0 (w : Cube3Edges) : Int := w.e1_00 + w.e2_01 - (w.e2_00 + w.e1_01)
def f12_1 (w : Cube3Edges) : Int := w.e1_10 + w.e2_11 - (w.e2_10 + w.e1_11)

/-- 3-cell boundary identity `d2 (d1 w) = 0` on the 3-cube: the alternating sum
of the 6 square face holonomies vanishes identically for every 1-cochain `w`. -/
theorem guarded_3cube_boundary_d2_d1_zero (w : Cube3Edges) :
    (f01_1 w - f01_0 w) - (f02_1 w - f02_0 w) + (f12_1 w - f12_0 w) = 0 := by
  dsimp [f01_0, f01_1, f02_0, f02_1, f12_0, f12_1]
  omega

/-- Path holonomies of all 6 permutation schedules in `S_3` from `(0,0,0)` to `(1,1,1)`. -/
def path012 (w : Cube3Edges) : Int := w.e0_00 + w.e1_10 + w.e2_11
def path021 (w : Cube3Edges) : Int := w.e0_00 + w.e2_10 + w.e1_11
def path102 (w : Cube3Edges) : Int := w.e1_00 + w.e0_10 + w.e2_11
def path120 (w : Cube3Edges) : Int := w.e1_00 + w.e2_01 + w.e0_11
def path201 (w : Cube3Edges) : Int := w.e2_00 + w.e0_01 + w.e1_11
def path210 (w : Cube3Edges) : Int := w.e2_00 + w.e1_01 + w.e0_11

/-- When all 5 generating square 2-faces of the guarded 3-cube are coherent
(`f = 0`), the 6th square face is automatically coherent and all 6 permutation
schedules from `(0,0,0)` to `(1,1,1)` have equal holonomy. -/
theorem guarded_3cube_all_six_paths_equal (w : Cube3Edges)
    (h01_0 : f01_0 w = 0) (h01_1 : f01_1 w = 0)
    (h02_0 : f02_0 w = 0) (h02_1 : f02_1 w = 0)
    (h12_0 : f12_0 w = 0) :
    f12_1 w = 0 ∧
    path021 w = path012 w ∧
    path102 w = path012 w ∧
    path120 w = path012 w ∧
    path201 w = path012 w ∧
    path210 w = path012 w := by
  dsimp [f01_0, f01_1, f02_0, f02_1, f12_0, f12_1,
         path012, path021, path102, path120, path201, path210] at *
  refine ⟨by omega, by omega, by omega, by omega, by omega, by omega⟩

/-- Puncturing a 2-face on the boundary of the 3-cube obstructs path coherence:
this explicit 1-cochain has `path012 != path102` when the `(0,1)` square face
at `x2 = 0` is missing from the guard. -/
def puncturedCubeCochain : Cube3Edges where
  e0_00 := 1
  e0_01 := 0
  e0_10 := 0
  e0_11 := 0
  e1_00 := 0
  e1_01 := 0
  e1_10 := 0
  e1_11 := 0
  e2_00 := 0
  e2_01 := 0
  e2_10 := 0
  e2_11 := 0

theorem punctured_2face_holonomy_obstruction :
    f01_0 puncturedCubeCochain = 1 ∧
    path012 puncturedCubeCochain ≠ path102 puncturedCubeCochain := by
  decide

/-! ## 6. Finite Scoped Witnesses for TFQ-0567 (`GEN-WDP-O02`) and TFQ-0570 (`GEN-WDP-O05`) -/

/-- `TFQ-0567` (`GEN-WDP-O02`) finite orientation-sensitivity witness:
a symmetric pair-defect map `pairDefect u v = pairDefect v u` cannot reflect
asymmetric directed transition costs (`cost 0 1 = 1 != cost 1 0 = 2`). -/
def asymmetricStepCost (u v : Fin 2) : Nat :=
  if u == 0 && v == 1 then 1
  else if u == 1 && v == 0 then 2
  else 0

theorem orientation_sensitive_pair_defect_nonreflection
    (pairDefect : Fin 2 → Fin 2 → Nat)
    (hsym : ∀ u v, pairDefect u v = pairDefect v u) :
    asymmetricStepCost 0 1 ≠ asymmetricStepCost 1 0 ∧
    ¬ (∀ u v, pairDefect u v = asymmetricStepCost u v) := by
  constructor
  · decide
  · intro hall
    have h01 := hall 0 1
    have h10 := hall 1 0
    have hs := hsym 0 1
    rw [h01, h10] at hs
    revert hs
    decide

/-- `TFQ-0570` (`GEN-WDP-O05`) authorization firewall non-implication witness:
internal receipt verification (`verify r = true`) does not determine external
institutional jurisdiction or appeal standing (`standing1 != standing2`). -/
structure GovernanceInterpretation where
  verifyReceipt : Nat → Bool
  externalJurisdiction : Nat → Bool
  appealStanding : Nat → Bool

def modelWithStanding : GovernanceInterpretation where
  verifyReceipt := fun _ => true
  externalJurisdiction := fun _ => true
  appealStanding := fun _ => true

def modelWithoutStanding : GovernanceInterpretation where
  verifyReceipt := fun _ => true
  externalJurisdiction := fun _ => false
  appealStanding := fun _ => false

theorem receipt_verification_independent_of_jurisdiction (r : Nat) :
    modelWithStanding.verifyReceipt r = true ∧
    modelWithoutStanding.verifyReceipt r = true ∧
    modelWithStanding.externalJurisdiction r ≠ modelWithoutStanding.externalJurisdiction r ∧
    modelWithStanding.appealStanding r ≠ modelWithoutStanding.appealStanding r := by
  simp [modelWithStanding, modelWithoutStanding]

end WitnessedDifference.WdpBatch6
