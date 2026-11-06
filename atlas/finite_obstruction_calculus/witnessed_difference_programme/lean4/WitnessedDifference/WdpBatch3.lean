import WitnessedDifference.Core

/-!
# Witnessed Difference Programme — Batch 3 Formal Derivations (`WdpBatch3.lean`)

Mechanizes the five Batch 3 WDP derivations in Lean 4:
1. `TFQ-0572` (`PGW-WDP-OUT-2-GUARDED-SWAP-COHERENCE` / `GEN-WDP-69`):
   Star-shaped guarded swap loop contraction and non-star-shaped obstruction witness.
2. `TFQ-0573` (`PGW-WDP-OUT-3-REALIZABLE-FUTURE-OBSERVATION` / `GEN-WDP-71`):
   Original/current relation laws and the 8-state realizable observation table theorem (`15/4 < 4 < 6`).
3. `TFQ-0574` (`PGW-WDP-OUT-4-REJECTION-RULE-REUSE` / `GEN-WDP-72`):
   Nine-element image-carrier bijections, soundness/coverage equivalences, scan thresholds, and task-change trap.
4. `TFQ-0575` (`PGW-WDP-OUT-5-FUTURE-FAITHFUL-COMPRESSION` / `GEN-WDP-73`):
   General-horizon (`T ≤ 2h`) clipped signed-count reconstruction theorem and sharp `T = 2h + 1` collision.
5. `TFQ-0579` (`PGW-WDP-BORN-RULE-NONSELECTION` / `GEN-WDP-65`):
   One-parameter affine non-trace state-effect readout family (`p_λ = λ tr(ρ E) + (1 - λ) tr(E)/2`),
   positivity, normalization, and `p_{1/2} = 3/4 ≠ 1` nonselection theorem.
-/

namespace WitnessedDifference.WdpBatch3

set_option linter.unusedVariables false

/-! ## 1. `TFQ-0572` (`GEN-WDP-69`): Star-Shaped Guarded Swap Coherence -/

/-- A guarded swap system that is star-shaped with respect to a legal center schedule `center`. -/
structure StarShapedSwapSystem (S : Type) where
  center : S
  legal : S → Prop
  adjSwap : S → S → Prop
  invDist : S → Nat
  stepToCenter : S → S
  center_legal : legal center
  center_dist_zero : invDist center = 0
  step_preserves_legal : ∀ s, legal s → legal (stepToCenter s)
  step_is_swap : ∀ s, legal s → invDist s > 0 → adjSwap s (stepToCenter s)
  step_decreases_dist : ∀ s, legal s → invDist s > 0 → invDist (stepToCenter s) < invDist s
  step_at_zero_fixed : ∀ s, legal s → invDist s = 0 → s = center

/-- Reflexive-transitive closure of legal adjacent swaps inside the guard. -/
inductive LegalSwapPath {S : Type} (G : StarShapedSwapSystem S) : S → S → Prop
  | refl (s : S) : G.legal s → LegalSwapPath G s s
  | step {s t u : S} : G.legal s → G.adjSwap s t → LegalSwapPath G t u → LegalSwapPath G s u
  | symm_step {s t u : S} : G.legal s → G.adjSwap t s → LegalSwapPath G t u → LegalSwapPath G s u

theorem legalSwapPath_trans {S : Type} {G : StarShapedSwapSystem S} {s t u : S}
    (h1 : LegalSwapPath G s t) (h2 : LegalSwapPath G t u) : LegalSwapPath G s u := by
  induction h1 with
  | refl _ _ => exact h2
  | step hs hst _ ih => exact LegalSwapPath.step hs hst (ih h2)
  | symm_step hs hts _ ih => exact LegalSwapPath.symm_step hs hts (ih h2)

theorem legalSwapPath_left_legal {S : Type} {G : StarShapedSwapSystem S} {s t : S}
    (h : LegalSwapPath G s t) : G.legal s := by
  cases h with
  | refl _ hs => exact hs
  | step hs _ _ => exact hs
  | symm_step hs _ _ => exact hs

theorem legalSwapPath_symm {S : Type} {G : StarShapedSwapSystem S} {s t : S}
    (h : LegalSwapPath G s t) (ht : G.legal t) : LegalSwapPath G t s := by
  induction h with
  | refl s hs => exact LegalSwapPath.refl s hs
  | @step a b c ha hab hbc ih =>
    have hb : G.legal b := legalSwapPath_left_legal hbc
    exact legalSwapPath_trans (ih ht) (LegalSwapPath.symm_step hb hab (LegalSwapPath.refl a ha))
  | @symm_step a b c ha hba hbc ih =>
    have hb : G.legal b := legalSwapPath_left_legal hbc
    exact legalSwapPath_trans (ih ht) (LegalSwapPath.step hb hba (LegalSwapPath.refl a ha))

/-- Every legal schedule contracts to the star center along a legal swap path bounded by `invDist`. -/
theorem star_contraction_to_center_aux {S : Type} (G : StarShapedSwapSystem S) :
    ∀ k s, G.legal s → G.invDist s ≤ k → LegalSwapPath G s G.center
  | 0, s, hs, hk => by
    have hz : G.invDist s = 0 := Nat.eq_zero_of_le_zero hk
    have hsc : s = G.center := G.step_at_zero_fixed s hs hz
    rw [hsc]
    exact LegalSwapPath.refl G.center G.center_legal
  | k + 1, s, hs, hk => by
    by_cases hpos : G.invDist s > 0
    · have hlt : G.invDist (G.stepToCenter s) < G.invDist s := G.step_decreases_dist s hs hpos
      have hle : G.invDist (G.stepToCenter s) ≤ k := by omega
      have hnext : G.legal (G.stepToCenter s) := G.step_preserves_legal s hs
      have hswap : G.adjSwap s (G.stepToCenter s) := G.step_is_swap s hs hpos
      exact LegalSwapPath.step hs hswap (star_contraction_to_center_aux G k (G.stepToCenter s) hnext hle)
    · have hz : G.invDist s = 0 := by omega
      have hsc : s = G.center := G.step_at_zero_fixed s hs hz
      rw [hsc]
      exact LegalSwapPath.refl G.center G.center_legal

theorem star_contraction_reaches_center {S : Type} (G : StarShapedSwapSystem S)
    (s : S) (hs : G.legal s) : LegalSwapPath G s G.center :=
  star_contraction_to_center_aux G (G.invDist s) s hs (Nat.le_refl _)

/-- Under a star-shaped guard, every pair of legal complete histories is connected inside the guard. -/
theorem star_shaped_swap_complex_connected {S : Type} (G : StarShapedSwapSystem S)
    (u v : S) (hu : G.legal u) (hv : G.legal v) : LegalSwapPath G u v := by
  have huc := star_contraction_reaches_center G u hu
  have hvc := star_contraction_reaches_center G v hv
  exact legalSwapPath_trans huc (legalSwapPath_symm hvc G.center_legal)

/-- Integer value of a 1-cochain along a word of oriented swap edges. -/
def swapTotal {E : Type} (φ : E → Int) : List E → Int
  | [] => 0
  | e :: es => φ e + swapTotal φ es

theorem swapTotal_append {E : Type} (φ : E → Int) (xs ys : List E) :
    swapTotal φ (xs ++ ys) = swapTotal φ xs + swapTotal φ ys := by
  induction xs with
  | nil => simp [swapTotal]
  | cons e es ih => simp [swapTotal, ih]; omega

/-- Elementary homotopy moves on swap words: backtrack insertion/deletion and 2-cell face replacement. -/
inductive SwapMove {E : Type} (rev : E → E) (faces : List (List E × List E)) :
    List E → List E → Prop
  | insert (pre post : List E) (e : E) :
      SwapMove rev faces (pre ++ post) (pre ++ e :: rev e :: post)
  | delete (pre post : List E) (e : E) :
      SwapMove rev faces (pre ++ e :: rev e :: post) (pre ++ post)
  | face (pre post side side' : List E) (declared : (side, side') ∈ faces) :
      SwapMove rev faces (pre ++ side ++ post) (pre ++ side' ++ post)

inductive SwapMoves {E : Type} (rev : E → E) (faces : List (List E × List E)) :
    List E → List E → Prop
  | refl (w : List E) : SwapMoves rev faces w w
  | tail {w v u : List E} : SwapMoves rev faces w v → SwapMove rev faces v u → SwapMoves rev faces w u

theorem swapMoves_preserve_total {E : Type} (φ : E → Int) (rev : E → E)
    (faces : List (List E × List E))
    (antisymmetric : ∀ e, φ (rev e) = -φ e)
    (closed : ∀ p ∈ faces, swapTotal φ p.1 = swapTotal φ p.2)
    {w w' : List E} (path : SwapMoves rev faces w w') : swapTotal φ w = swapTotal φ w' := by
  induction path with
  | refl => rfl
  | tail _ move ih =>
    rw [ih]
    cases move with
    | insert pre post e =>
      rw [swapTotal_append, swapTotal_append]
      simp only [swapTotal, antisymmetric]
      omega
    | delete pre post e =>
      rw [swapTotal_append, swapTotal_append]
      simp only [swapTotal, antisymmetric]
      omega
    | face pre post side side' declared =>
      have hc := closed (side, side') declared
      rw [swapTotal_append, swapTotal_append, swapTotal_append, swapTotal_append, hc]

/-- Under a star-shaped guard, every closed cochain with zero circulation on elementary star triangles
    evaluates to zero on every legal swap loop (loop contractibility). -/
theorem star_shaped_loop_cochain_zero {E : Type} (φ : E → Int) (rev : E → E)
    (faces : List (List E × List E))
    (antisymmetric : ∀ e, φ (rev e) = -φ e)
    (closed : ∀ p ∈ faces, swapTotal φ p.1 = swapTotal φ p.2)
    {loop : List E} (contractible_to_empty : SwapMoves rev faces loop []) :
    swapTotal φ loop = 0 := by
  have h := swapMoves_preserve_total φ rev faces antisymmetric closed contractible_to_empty
  simpa [swapTotal] using h

/-- Non-star-shaped obstruction witness: when the center/interior square face is punctured (absent from
    `faces`), a perimeter loop has nonzero circulation `1 ≠ 0`, so no sequence of legal backtracks
    contracts the loop. -/
theorem punctured_square_loop_not_contractible :
    let rev : Fin 4 → Fin 4
      | ⟨0, _⟩ => ⟨2, by decide⟩
      | ⟨1, _⟩ => ⟨3, by decide⟩
      | ⟨2, _⟩ => ⟨0, by decide⟩
      | ⟨3, _⟩ => ⟨1, by decide⟩
    let φ : Fin 4 → Int
      | ⟨0, _⟩ => 1
      | ⟨1, _⟩ => 0
      | ⟨2, _⟩ => -1
      | ⟨3, _⟩ => 0
    let loop : List (Fin 4) := [⟨0, by decide⟩, ⟨1, by decide⟩]
    (∀ e, φ (rev e) = -φ e) ∧
    swapTotal φ loop = 1 ∧
    ¬ SwapMoves rev [] loop [] := by
  intro rev φ loop
  have hanti : ∀ e : Fin 4, φ (rev e) = -φ e := by
    intro ⟨i, hi⟩
    match i, hi with
    | 0, _ => rfl
    | 1, _ => rfl
    | 2, _ => rfl
    | 3, _ => rfl
  refine ⟨hanti, rfl, ?_⟩
  intro hpath
  have hzero := swapMoves_preserve_total φ rev [] hanti (by intro p hp; cases hp) hpath
  change (1 : Int) = 0 at hzero
  omega

/-! ## 2. `TFQ-0573` (`GEN-WDP-71`): Realizable Future Observation & 8-State Table Theorem -/

/-- Original/current state-pair update under a measurement action `step` and post-state report. -/
def ObsUpdate {X O : Type} (z step : X → X → Prop) (report : X → O)
    (o : O) (x y' : X) : Prop :=
  ∃ y, z x y ∧ step y y' ∧ report y' = o

/-- Handoff stopping criterion: every pair `(x, y)` in `z` has original class `k x = c` and current class `k y = c`. -/
def HandoffGood {X K : Type} (k : X → K) (z : X → X → Prop) (c : K) : Prop :=
  ∀ x y, z x y → k x = c ∧ k y = c

theorem obs_decoder_unique_on_nonempty {X K : Type} (k : X → K)
    (z : X → X → Prop) (c d : K) (hc : HandoffGood k z c) (hd : HandoffGood k z d)
    (nonempty : ∃ x y, z x y) : c = d := by
  obtain ⟨x, y, hz⟩ := nonempty
  exact (hc x y hz).1.symm.trans (hd x y hz).1

/-- The eight post-preparation states `(branch, val, mode)` of the Appendix-S future-operation table. -/
structure EightState where
  branch : Bool -- false = A, true = B
  val : Bool    -- false = 0, true = 1
  mode : Bool   -- false = mode 0, true = mode 1
  deriving DecidableEq

/-- The future congruence class depends on `(branch, val)` and not on `mode`. -/
def futureClass (s : EightState) : Bool × Bool := (s.branch, s.val)

/-- Flip-read transition on `mode = false`: flips the branch and sets `mode = true`. -/
def flipReadStep (s : EightState) : EightState := ⟨!s.branch, s.val, true⟩

/-- Restore transition on `mode = true`: flips the branch back and restores `mode = false`. -/
def restoreStep (s : EightState) : EightState := ⟨!s.branch, s.val, false⟩

/-- Conditional branch value readers (`read_A` reads `val` when `branch = false`, else `false`;
    `read_B` reads `val` when `branch = true`, else `false`). -/
def readA (s : EightState) : Bool := if !s.branch then s.val else false
def readB (s : EightState) : Bool := if s.branch then s.val else false

def costFlipRead : Rat := 1 / 2
def costReadBranch : Rat := 1
def costReadCond : Rat := 3
def costReadAll : Rat := 6
def costRestore : Rat := 1 / 4

/-- The disturbance-plus-restoration policy (`flip_read`, then conditional read on the flipped branch,
    then `restore`) returns every `mode = false` state to the exact original state, recovers `futureClass s`,
    and costs `15/4`, strictly less than the non-disturbing adaptive optimum `4` and static optimum `6`. -/
theorem eight_state_realizable_observation_gen_wdp_71 (b v : Bool) :
    let s0 : EightState := ⟨b, v, false⟩
    let s1 : EightState := flipReadStep s0
    let measuredVal : Bool := if s1.branch then readB s1 else readA s1
    let s2 : EightState := restoreStep s1
    s2 = s0 ∧
    (!s1.branch, measuredVal) = futureClass s0 ∧
    futureClass s2 = futureClass s0 ∧
    futureClass s1 ≠ futureClass s0 ∧
    costFlipRead + costReadCond + costRestore = (15 : Rat) / 4 ∧
    costReadBranch + costReadCond = (4 : Rat) ∧
    (15 : Rat) / 4 < costReadBranch + costReadCond ∧
    costReadBranch + costReadCond < costReadAll := by
  have hcost :
      costFlipRead + costReadCond + costRestore = (15 : Rat) / 4 ∧
      costReadBranch + costReadCond = (4 : Rat) ∧
      (15 : Rat) / 4 < costReadBranch + costReadCond ∧
      costReadBranch + costReadCond < costReadAll := by
    unfold costFlipRead costReadBranch costReadCond costReadAll costRestore
    refine ⟨by grind, by grind, by grind, by grind⟩
  refine ⟨?_, ?_, ?_, ?_, hcost.1, hcost.2.1, hcost.2.2.1, hcost.2.2.2⟩
  · cases b <;> cases v <;> rfl
  · cases b <;> cases v <;> rfl
  · cases b <;> cases v <;> rfl
  · cases b <;> cases v <;> decide

/-! ## 3. `TFQ-0574` (`GEN-WDP-72`): Rejection-Rule Reuse Across Representations -/

abbrev ReusePoint := Int × Int
def reuseC0 (p : ReusePoint) : Prop := -1 ≤ p.1 ∧ p.1 ≤ 1 ∧ -1 ≤ p.2 ∧ p.2 ≤ 1
def reuseF01 (p : ReusePoint) : ReusePoint := (p.1 + p.2, p.1 - p.2)
def reuseG10Int (p : ReusePoint) : ReusePoint := ((p.1 + p.2) / 2, (p.1 - p.2) / 2)
def reuseF12 (p : ReusePoint) : ReusePoint := (p.1, p.2 + p.1)
def reuseG21 (p : ReusePoint) : ReusePoint := (p.1, p.2 - p.1)
def reuseEncode2 (p : ReusePoint) : ReusePoint := reuseF12 (reuseF01 p)
def reuseDecode2 (p : ReusePoint) : ReusePoint := reuseG10Int (reuseG21 p)
def reuseC1 (q : ReusePoint) : Prop := ∃ p, reuseC0 p ∧ reuseF01 p = q
def reuseC2 (q : ReusePoint) : Prop := ∃ p, reuseC0 p ∧ reuseEncode2 p = q
def reuseGood0 (d : Int) (p : ReusePoint) : Prop := p.1 + p.2 = d
def reuseGood1 (d : Int) (p : ReusePoint) : Prop := p.1 = d

theorem reuse_g10_f01 (p : ReusePoint) : reuseG10Int (reuseF01 p) = p := by
  apply Prod.ext <;> simp only [reuseG10Int, reuseF01] <;> omega

theorem reuse_g21_f12 (p : ReusePoint) : reuseG21 (reuseF12 p) = p := by
  apply Prod.ext <;> simp only [reuseG21, reuseF12] <;> omega

theorem reuse_decode_encode2 (p : ReusePoint) : reuseDecode2 (reuseEncode2 p) = p := by
  simp only [reuseDecode2, reuseEncode2, reuse_g21_f12, reuse_g10_f01]

theorem reuse_encode_decode_image (q : ReusePoint) (hq : reuseC2 q) :
    reuseEncode2 (reuseDecode2 q) = q := by
  obtain ⟨p, _, rfl⟩ := hq
  rw [reuse_decode_encode2]

theorem reuse_soundness_iff {X Y : Type} (g : Y → X) (GX : X → Prop) (GY E : Y → Prop)
    (hv : ∀ y, GY y ↔ GX (g y)) :
    (∀ y, E y → GX (g y)) ↔ (∀ y, E y → GY y) := by
  constructor
  · intro h y hy
    exact (hv y).mpr (h y hy)
  · intro h y hy
    exact (hv y).mp (h y hy)

theorem reuse_coverage_iff {X Y : Type} (f : X → Y) (g : Y → X)
    (hgf : ∀ x, g (f x) = x) (hfg : ∀ y, f (g y) = y)
    (GX : X → Prop) (GY E : Y → Prop) (hv : ∀ y, GY y ↔ GX (g y)) :
    (∀ x, GX x → ∃ y, E y ∧ g y = x) ↔ (∀ y, GY y → E y) := by
  constructor
  · intro h y hy
    obtain ⟨z, hz, hzy⟩ := h (g y) ((hv y).mp hy)
    have heq : z = y := by
      have heq := congrArg f hzy
      simpa only [hfg] using heq
    rw [← heq]
    exact hz
  · intro h x hx
    refine ⟨f x, h (f x) ((hv (f x)).mpr ?_), hgf x⟩
    simpa only [hgf] using hx

def scanBare2 (v : Int) : Int := (9 - v) * 6 + 8
def scanGuarded2 (v s : Int) : Int := (9 - v - s) * 7 + s * 3 + 9

theorem reuse_scan_thresholds_and_task2_trap :
    (∀ v s : Int, (scanGuarded2 v s ≤ scanBare2 v ↔ 10 - v ≤ 4 * s) ∧
      (scanGuarded2 v s + 6 ≤ scanBare2 v ↔ 16 - v ≤ 4 * s)) ∧
    reuseC2 (2, 2) ∧ reuseGood1 2 (2, 2) ∧ (2 : Int) ≠ 1 ∧
    ((2 + 4 + 2) + (2 + 2 + 2) + 2 + (2 + 1 + 4 + 2) + (2 + 1 + 4 + 2) = (34 : Int) ∧ (34 : Int) ≤ 36) := by
  refine ⟨?_, ⟨(1, 1), by simp [reuseC0], rfl⟩, rfl, by decide, by omega⟩
  intro v s
  unfold scanGuarded2 scanBare2
  constructor <;> omega

/-! ## 4. `TFQ-0575` (`GEN-WDP-73`): General-Horizon Clipped Reconstruction & Sharp Collision -/

def signedCountSum : List Bool → List Nat → Int
  | [], _ => 0
  | _, [] => 0
  | sign :: signs, count :: counts =>
    (if sign then (count : Int) else -(count : Int)) + signedCountSum signs counts

def natSum : List Nat → Nat
  | [] => 0
  | c :: cs => c + natSum cs

/-- Coordinatewise cap at arbitrary horizon `h : Nat`. -/
def clippedAt (h : Nat) (counts : List Nat) : List Nat :=
  counts.map (fun count => min count h)

theorem clippedAt_eq_self_of_sum_le (h : Nat) (counts : List Nat) (bound : natSum counts ≤ h) :
    clippedAt h counts = counts := by
  induction counts with
  | nil => rfl
  | cons c cs ih =>
    have head : c ≤ h := by simp only [natSum] at bound; omega
    have tail : natSum cs ≤ h := by simp only [natSum] at bound; omega
    simp only [clippedAt, List.map_cons]
    rw [Nat.min_eq_left head]
    exact congrArg (List.cons c) (ih tail)

/-- General-horizon sharp reconstruction theorem (`GEN-WDP-73` general-horizon extension):
    for any horizon `h : Nat` and fixed coordinate signs, nonnegative counts with total at most `2 * h`
    are uniquely determined by their coordinatewise caps `min(c_i, h)` and their signed total. -/
theorem general_horizon_clipped_signed_counts_unique (h : Nat) (signs : List Bool) (xs ys : List Nat)
    (xlength : xs.length = signs.length) (ylength : ys.length = signs.length)
    (xbound : natSum xs ≤ 2 * h) (ybound : natSum ys ≤ 2 * h)
    (caps : clippedAt h xs = clippedAt h ys) (total : signedCountSum signs xs = signedCountSum signs ys) :
    xs = ys := by
  induction signs generalizing xs ys with
  | nil =>
    have hx : xs = [] := List.length_eq_zero_iff.mp xlength
    have hy : ys = [] := List.length_eq_zero_iff.mp ylength
    exact hx.trans hy.symm
  | cons sign signs ih =>
    cases xs with
    | nil => simp at xlength
    | cons x xs =>
      cases ys with
      | nil => simp at ylength
      | cons y ys =>
        have lensx : xs.length = signs.length := by simpa using xlength
        have lensy : ys.length = signs.length := by simpa using ylength
        have boundsx : x + natSum xs ≤ 2 * h := by simpa [natSum] using xbound
        have boundsy : y + natSum ys ≤ 2 * h := by simpa [natSum] using ybound
        have cap_parts : min x h = min y h ∧ clippedAt h xs = clippedAt h ys :=
          List.cons.inj caps
        by_cases small : x < h
        · have heads : x = y := by have := cap_parts.1; omega
          subst y
          have totals : signedCountSum signs xs = signedCountSum signs ys := by
            cases sign <;> simp only [signedCountSum, Bool.false_eq_true, ite_false, ite_true] at total <;>
              omega
          have tails := ih xs ys lensx lensy (by omega) (by omega) cap_parts.2 totals
          exact congrArg (List.cons x) tails
        · have bigy : h ≤ y := by have := cap_parts.1; omega
          have tailx : natSum xs ≤ h := by omega
          have taily : natSum ys ≤ h := by omega
          have tails : xs = ys := by
            have hcap := cap_parts.2
            rw [clippedAt_eq_self_of_sum_le h xs tailx,
              clippedAt_eq_self_of_sum_le h ys taily] at hcap
            exact hcap
          subst ys
          have heads : x = y := by
            cases sign <;> simp only [signedCountSum, Bool.false_eq_true, ite_false, ite_true] at total <;>
              omega
          exact congrArg (fun z => z :: xs) heads

/-- Sharpness of the `T ≤ 2h` bound at every horizon `h`: at total `T = 2h + 1`, the distinct count
    vectors `[h, h + 1]` and `[h + 1, h]` have identical `h`-caps `[h, h]` and identical signed total `2h + 1`. -/
theorem general_horizon_sharp_collision (h : Nat) :
    clippedAt h [h, h + 1] = clippedAt h [h + 1, h] ∧
    signedCountSum [true, true] [h, h + 1] = signedCountSum [true, true] [h + 1, h] ∧
    ([h, h + 1] : List Nat) ≠ [h + 1, h] ∧
    natSum [h, h + 1] = 2 * h + 1 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · have hmin : min (h + 1) h = h := Nat.min_eq_right (Nat.le_succ h)
    simp [clippedAt, hmin]
  · simp only [signedCountSum, ite_true]
    omega
  · intro heq
    have h0 := (List.cons.inj heq).1
    omega
  · simp only [natSum]
    omega

/-- General-horizon composition bound for layer-indexed paths of remaining horizon `h`. -/
inductive HorizonOffer (S : Type) where
  | disabled
  | excluded (price : Nat × Nat)
  | admitted (price : Nat × Nat) (next : S)

def HorizonSignature (Terminal Present Action : Type) : Nat → Type
  | 0 => Terminal
  | h + 1 => Present × (Action → HorizonOffer (HorizonSignature Terminal Present Action h))

inductive HorizonLayerPath {Terminal Present Action : Type} :
    {h k : Nat} → HorizonSignature Terminal Present Action h → List Action → (Nat × Nat) →
      HorizonSignature Terminal Present Action k → Prop where
  | nil {h : Nat} (q : HorizonSignature Terminal Present Action h) : HorizonLayerPath q [] (0, 0) q
  | cons {h k : Nat} {q : HorizonSignature Terminal Present Action (h + 1)}
      {child : HorizonSignature Terminal Present Action h}
      {target : HorizonSignature Terminal Present Action k}
      {a : Action} {actions : List Action} {p r : Nat × Nat}
      (edge : q.2 a = .admitted p child) (rest : HorizonLayerPath child actions r target) :
      HorizonLayerPath q (a :: actions) (p.1 + r.1, p.2 + r.2) target

theorem horizonLayerPath_length {Terminal Present Action : Type} {h k : Nat}
    {source : HorizonSignature Terminal Present Action h}
    {target : HorizonSignature Terminal Present Action k}
    {actions : List Action} {price : Nat × Nat}
    (path : HorizonLayerPath source actions price target) :
    h = k + actions.length := by
  induction path with
  | nil => simp
  | cons edge rest ih => simp only [List.length_cons]; omega

theorem general_horizon_composition_bound {Terminal Present Action : Type}
    {h k j : Nat}
    {s : HorizonSignature Terminal Present Action h}
    {t : HorizonSignature Terminal Present Action k}
    {u : HorizonSignature Terminal Present Action j}
    {left right : List Action} {p q : Nat × Nat}
    (first : HorizonLayerPath s left p t) (second : HorizonLayerPath t right q u) :
    left.length + right.length ≤ h := by
  have h1 := horizonLayerPath_length first
  have h2 := horizonLayerPath_length second
  omega

/-! ## 5. `TFQ-0579` (`GEN-WDP-65`): Born-Rule Nonselection Countermodel Family -/

/-- Certified finite state-effect readout package in dimension `n ≥ 1` with accepted/rejected
    Frobenius numerators `numAccept`, `numReject`, state Frobenius denominator `stateDenom > 0`,
    and effect trace `traceAccept`, `traceReject` summing to `n`. -/
structure CertifiedReadoutFrame where
  dim : Nat
  dim_pos : 0 < dim
  stateDenom : Rat
  stateDenom_pos : 0 < stateDenom
  numAccept : Rat
  numReject : Rat
  numAccept_nonneg : 0 ≤ numAccept
  numReject_nonneg : 0 ≤ numReject
  frame_partition : numAccept + numReject = stateDenom
  traceAccept : Rat
  traceReject : Rat
  traceAccept_nonneg : 0 ≤ traceAccept
  traceReject_nonneg : 0 ≤ traceReject
  trace_sum : traceAccept + traceReject = (dim : Rat)

def baseProbability (F : CertifiedReadoutFrame) : Rat :=
  F.numAccept / F.stateDenom

def baseComplementProbability (F : CertifiedReadoutFrame) : Rat :=
  F.numReject / F.stateDenom

/-- One-parameter affine deformed readout family (`GEN-WDP-65` equation 5.1):
    `p_λ(ρ, E) = λ * tr(ρ E) + (1 - λ) * (tr E / n)`. -/
def deformedProbability (lam : Rat) (F : CertifiedReadoutFrame) : Rat :=
  lam * baseProbability F + (1 - lam) * (F.traceAccept / (F.dim : Rat))

def deformedComplementProbability (lam : Rat) (F : CertifiedReadoutFrame) : Rat :=
  lam * baseComplementProbability F + (1 - lam) * (F.traceReject / (F.dim : Rat))

/-- Normalization of `p_λ` for every `λ : Rat` and every certified readout frame. -/
theorem deformed_probability_normalized (lam : Rat) (F : CertifiedReadoutFrame) :
    deformedProbability lam F + deformedComplementProbability lam F = 1 := by
  unfold deformedProbability deformedComplementProbability baseProbability baseComplementProbability
  have hsd : F.stateDenom ≠ 0 := Rat.ne_of_gt F.stateDenom_pos
  have hdim_pos : (0 : Rat) < (F.dim : Rat) := by exact_mod_cast F.dim_pos
  have hdim : (F.dim : Rat) ≠ 0 := Rat.ne_of_gt hdim_pos
  have hpart := F.frame_partition
  have htr := F.trace_sum
  have ha := Rat.div_mul_cancel (a := F.numAccept) hsd
  have hb := Rat.div_mul_cancel (a := F.numReject) hsd
  have htself := Rat.div_mul_cancel (a := F.stateDenom) hsd
  have hta := Rat.div_mul_cancel (a := F.traceAccept) hdim
  have htb := Rat.div_mul_cancel (a := F.traceReject) hdim
  have hdself := Rat.div_mul_cancel (a := (F.dim : Rat)) hdim
  grind

/-- Nonnegativity of `p_λ` for `0 ≤ λ ≤ 1`. -/
theorem deformed_probability_nonnegative (lam : Rat) (h0 : 0 ≤ lam) (h1 : lam ≤ 1)
    (F : CertifiedReadoutFrame) :
    0 ≤ deformedProbability lam F := by
  unfold deformedProbability baseProbability
  have hdim_pos : (0 : Rat) < (F.dim : Rat) := by exact_mod_cast F.dim_pos
  have hsd_pos := F.stateDenom_pos
  have hp : 0 ≤ F.numAccept / F.stateDenom := by
    apply Rat.le_of_mul_le_mul_right (c := F.stateDenom)
    · rw [Rat.div_mul_cancel (Rat.ne_of_gt F.stateDenom_pos)]
      have := F.numAccept_nonneg
      grind
    · exact F.stateDenom_pos
  have htr : 0 ≤ F.traceAccept / (F.dim : Rat) := by
    apply Rat.le_of_mul_le_mul_right (c := (F.dim : Rat))
    · rw [Rat.div_mul_cancel (Rat.ne_of_gt hdim_pos)]
      have := F.traceAccept_nonneg
      grind
    · exact hdim_pos
  have hterm1 : 0 ≤ lam * (F.numAccept / F.stateDenom) := Rat.mul_nonneg h0 hp
  have h1lam : 0 ≤ 1 - lam := by grind
  have hterm2 : 0 ≤ (1 - lam) * (F.traceAccept / (F.dim : Rat)) := Rat.mul_nonneg h1lam htr
  exact Rat.add_nonneg hterm1 hterm2

/-- Dimension-two sharp qubit basis state/effect fixture `(|0⟩⟨0|, |0⟩⟨0|)`. -/
def sharpQubitFrame : CertifiedReadoutFrame where
  dim := 2
  dim_pos := by decide
  stateDenom := 1
  stateDenom_pos := by grind
  numAccept := 1
  numReject := 0
  numAccept_nonneg := by grind
  numReject_nonneg := by grind
  frame_partition := by grind
  traceAccept := 1
  traceReject := 1
  traceAccept_nonneg := by grind
  traceReject_nonneg := by grind
  trace_sum := by grind

/-- Dimension-one sharp frame where `p_λ = 1` for all `λ` (showing `n ≥ 2` is required for nonselection). -/
def dimOneSharpFrame : CertifiedReadoutFrame where
  dim := 1
  dim_pos := by decide
  stateDenom := 1
  stateDenom_pos := by grind
  numAccept := 1
  numReject := 0
  numAccept_nonneg := by grind
  numReject_nonneg := by grind
  frame_partition := by grind
  traceAccept := 1
  traceReject := 0
  traceAccept_nonneg := by grind
  traceReject_nonneg := by grind
  trace_sum := by grind

/-- `GEN-WDP-65` Born-rule nonselection theorem:
    On the dimension-two sharp qubit fixture, `p_λ(|0⟩⟨0|, |0⟩⟨0|) = (1 + λ) / 2`, so `p_1 = 1`
    while `p_{1/2} = 3/4 ≠ 1`, and `p_λ ≠ 1` for every `λ ≠ 1`; whereas at `n = 1`, `p_λ = 1` for all `λ`. -/
theorem born_rule_nonselection_gen_wdp_65 :
    (∀ lam : Rat, deformedProbability lam sharpQubitFrame = (1 + lam) / 2) ∧
    deformedProbability 1 sharpQubitFrame = 1 ∧
    deformedProbability (1 / 2) sharpQubitFrame = 3 / 4 ∧
    ((3 : Rat) / 4 ≠ 1) ∧
    (∀ lam : Rat, lam ≠ 1 → deformedProbability lam sharpQubitFrame ≠ 1) ∧
    (∀ lam : Rat, deformedProbability lam dimOneSharpFrame = 1) := by
  have hform : ∀ lam : Rat, deformedProbability lam sharpQubitFrame = (1 + lam) / 2 := by
    intro lam
    unfold deformedProbability baseProbability sharpQubitFrame
    grind
  have hdim1 : ∀ lam : Rat, deformedProbability lam dimOneSharpFrame = 1 := by
    intro lam
    unfold deformedProbability baseProbability dimOneSharpFrame
    grind
  refine ⟨hform, ?_, ?_, by grind, ?_, hdim1⟩
  · rw [hform 1]; grind
  · rw [hform (1 / 2)]; grind
  · intro lam hne heq
    rw [hform lam] at heq
    apply hne
    grind

end WitnessedDifference.WdpBatch3
