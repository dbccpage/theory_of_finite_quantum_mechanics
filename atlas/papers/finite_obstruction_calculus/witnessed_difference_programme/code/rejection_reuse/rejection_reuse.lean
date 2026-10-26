import Std

/- Selected laws for the finite reuse example. The integer decoder is used only
   on the exact image, where both numerators are even. Off-image rational values
   are checked separately in Python. No correspondence to engine code is assumed. -/
namespace WDPReuse

abbrev Point := Int × Int
def c0 (p : Point) : Prop := -1 ≤ p.1 ∧ p.1 ≤ 1 ∧ -1 ≤ p.2 ∧ p.2 ≤ 1
def f01 (p : Point) : Point := (p.1 + p.2, p.1 - p.2)
def g10Int (p : Point) : Point := ((p.1 + p.2) / 2, (p.1 - p.2) / 2)
def f12 (p : Point) : Point := (p.1, p.2 + p.1)
def g21 (p : Point) : Point := (p.1, p.2 - p.1)
def encode2 (p : Point) : Point := f12 (f01 p)
def decode2 (p : Point) : Point := g10Int (g21 p)
def c1 (q : Point) : Prop := ∃ p, c0 p ∧ f01 p = q
def c2 (q : Point) : Prop := ∃ p, c0 p ∧ encode2 p = q
def good0 (d : Int) (p : Point) : Prop := p.1 + p.2 = d
def good1 (d : Int) (p : Point) : Prop := p.1 = d

theorem g10_f01 (p : Point) : g10Int (f01 p) = p := by
  apply Prod.ext <;> simp only [g10Int, f01] <;> omega

theorem g21_f12 (p : Point) : g21 (f12 p) = p := by
  apply Prod.ext <;> simp only [g21, f12] <;> omega

theorem f12_g21 (p : Point) : f12 (g21 p) = p := by
  apply Prod.ext <;> simp only [g21, f12] <;> omega

theorem decode_encode2 (p : Point) : decode2 (encode2 p) = p := by
  simp only [decode2, encode2, g21_f12, g10_f01]

theorem f01_g10_image (q : Point) (hq : c1 q) : f01 (g10Int q) = q := by
  obtain ⟨p, _, rfl⟩ := hq
  rw [g10_f01]

theorem encode_decode_image (q : Point) (hq : c2 q) : encode2 (decode2 q) = q := by
  obtain ⟨p, _, rfl⟩ := hq
  rw [decode_encode2]

theorem decoder_carrier1 (q : Point) (hq : c1 q) : c0 (g10Int q) := by
  obtain ⟨p, hp, rfl⟩ := hq
  rw [g10_f01]
  exact hp

theorem decoder_carrier2 (q : Point) (hq : c2 q) : c0 (decode2 q) := by
  obtain ⟨p, hp, rfl⟩ := hq
  rw [decode_encode2]
  exact hp

theorem validity1 (d : Int) (q : Point) (hq : c1 q) :
    good1 d q ↔ good0 d (g10Int q) := by
  obtain ⟨p, _, rfl⟩ := hq
  rw [g10_f01]
  rfl

theorem validity2 (d : Int) (q : Point) (hq : c2 q) :
    good1 d q ↔ good0 d (decode2 q) := by
  obtain ⟨p, _, rfl⟩ := hq
  rw [decode_encode2]
  rfl

-- The actual finite image types instantiate the general emission criteria below.
abbrev Original := {p : Point // c0 p}
abbrev Level2 := {q : Point // c2 q}
def forward2 (p : Original) : Level2 := ⟨encode2 p.val, p.val, p.property, rfl⟩
def backward2 (q : Level2) : Original := ⟨decode2 q.val, decoder_carrier2 q.val q.property⟩

theorem backward_forward (p : Original) : backward2 (forward2 p) = p := by
  apply Subtype.ext
  exact decode_encode2 p.val

theorem forward_backward (q : Level2) : forward2 (backward2 q) = q := by
  apply Subtype.ext
  exact encode_decode_image q.val q.property

theorem soundness_iff {X Y : Type} (g : Y → X) (GX : X → Prop) (GY E : Y → Prop)
    (hv : ∀ y, GY y ↔ GX (g y)) :
    (∀ y, E y → GX (g y)) ↔ (∀ y, E y → GY y) := by
  constructor
  · intro h y hy
    exact (hv y).mpr (h y hy)
  · intro h y hy
    exact (hv y).mp (h y hy)

theorem coverage_iff {X Y : Type} (f : X → Y) (g : Y → X)
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

def gx (d : Int) (p : Original) : Prop := good0 d p.val
def gy (d : Int) (q : Level2) : Prop := good1 d q.val

theorem finite_soundness (d : Int) (E : Level2 → Prop) :
    (∀ q, E q → gx d (backward2 q)) ↔ (∀ q, E q → gy d q) := by
  exact soundness_iff backward2 (gx d) (gy d) E (fun q => validity2 d q.val q.property)

theorem finite_coverage (d : Int) (E : Level2 → Prop) :
    (∀ p, gx d p → ∃ q, E q ∧ backward2 q = p) ↔ (∀ q, gy d q → E q) := by
  exact coverage_iff forward2 backward2 backward_forward forward_backward
    (gx d) (gy d) E (fun q => validity2 d q.val q.property)

theorem safe_union {X : Type} (G R S : X → Prop)
    (hr : ∀ x, G x → ¬ R x) (hs : ∀ x, G x → ¬ S x) :
    ∀ x, G x → ¬ (R x ∨ S x) := by
  intro x hx h
  cases h with
  | inl h => exact hr x hx h
  | inr h => exact hs x hx h

theorem guard_coverage_iff {X : Type} (G R : X → Prop) :
    (∀ x, G x → G x ∧ ¬ R x) ↔ (∀ x, G x → ¬ R x) := by
  constructor
  · intro h x hx
    exact (h x hx).2
  · intro h x hx
    exact ⟨hx, h x hx⟩

-- Pullback directions: new candidates go to the source of the installed rule.
theorem rule_pullback0 (d : Int) (p : Point) :
    ((f01 p).1 ≠ d) ↔ p.1 + p.2 ≠ d := Iff.rfl

theorem rule_pullback2 (d : Int) (p : Point) :
    ((g21 p).1 ≠ d) ↔ p.1 ≠ d := Iff.rfl

-- Costs are doubled so that the half-unit guard has integral charge.
-- These are scan-family algebra, not a theorem of global optimality.
def bare2 (v : Int) : Int := (9 - v) * 6 + 8
def guarded2 (v s : Int) : Int := (9 - v - s) * 7 + s * 3 + 9

theorem bare_formula (v : Int) : bare2 v = 62 - 6 * v := by
  unfold bare2
  omega

theorem guarded_formula (v s : Int) : guarded2 v s = 72 - 7 * v - 4 * s := by
  unfold guarded2
  omega

theorem operating_threshold (v s : Int) : guarded2 v s ≤ bare2 v ↔ 10 - v ≤ 4 * s := by
  rw [guarded_formula, bare_formula]
  omega

theorem setup_threshold (v s : Int) : guarded2 v s + 6 ≤ bare2 v ↔ 16 - v ≤ 4 * s := by
  rw [guarded_formula, bare_formula]
  omega

theorem maximal_guard_formula (v : Int) : guarded2 v (9 - v) = 36 - 3 * v := by
  rw [guarded_formula]
  omega

theorem successful_trace_within_budget :
    (2 + 4 + 2) + (2 + 2 + 2) + 2 + (2 + 1 + 4 + 2) + (2 + 1 + 4 + 2) = (34 : Int)
    ∧ (34 : Int) ≤ 36 := by omega

theorem nonreset_step (spent charge budget : Int)
    (hc : 0 ≤ charge) (hfit : spent + charge ≤ budget) :
    spent ≤ spent + charge ∧ spent + charge ≤ budget := by omega

theorem fuel_reset_excess : (18 : Int) - 5 = 13 ∧ (5 + 18 : Int) = 23 ∧ (23 : Int) > 18 := by omega

theorem fixed_rule_blocks_task2 : c2 (2, 2) ∧ good1 2 (2, 2) ∧ (2 : Int) ≠ 1 := by
  refine ⟨⟨(1, 1), ?_, rfl⟩, rfl, ?_⟩
  · simp only [c0]
    decide
  · decide

theorem installation_unnecessary_witness : c0 (1, 1) ∧ good0 2 (1, 1)
    ∧ (1 + 2 + 1 : Int) = 4 ∧ (4 : Int) ≤ 18 := by
  simp only [c0, good0]
  decide

#print axioms g10_f01
#print axioms validity2
#print axioms finite_soundness
#print axioms finite_coverage
#print axioms safe_union
#print axioms guard_coverage_iff
#print axioms operating_threshold
#print axioms setup_threshold
#print axioms successful_trace_within_budget
#print axioms nonreset_step
#print axioms fixed_rule_blocks_task2
#print axioms installation_unnecessary_witness
end WDPReuse
