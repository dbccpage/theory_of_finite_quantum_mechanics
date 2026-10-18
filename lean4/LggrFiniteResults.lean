

namespace LggrFiniteResults


abbrev Meas (A : Type) := List (A × Nat)

def push {A B : Type} (f : A → B) (p : Meas A) : Meas B :=
  p.map (fun e => (f e.1, e.2))

def mass {A : Type} (p : Meas A) : Nat :=
  p.foldr (fun e acc => e.2 + acc) 0

def weightAt {B : Type} [DecidableEq B] (p : Meas B) (b : B) : Nat :=
  mass (p.filter (fun e => decide (e.1 = b)))

theorem push_id {A : Type} (p : Meas A) : push (fun a => a) p = p := by
  induction p with
  | nil => rfl
  | cons e t ih => simp [push] at ih ⊢

theorem push_comp {A B C : Type} (f : A → B) (g : B → C) (p : Meas A) :
    push (fun a => g (f a)) p = push g (push f p) := by
  induction p with
  | nil => rfl
  | cons e t ih => simp [push] at ih ⊢

theorem mass_push {A B : Type} (f : A → B) (p : Meas A) : mass (push f p) = mass p := by
  induction p with
  | nil => rfl
  | cons e t ih => simp [push, mass] at ih ⊢; exact ih

theorem weightAt_push {A B : Type} [DecidableEq B] (f : A → B) (p : Meas A) (b : B) :
    weightAt (push f p) b = mass (p.filter (fun e => decide (f e.1 = b))) := by
  induction p with
  | nil => rfl
  | cons e t ih =>
    unfold weightAt at ih ⊢
    by_cases h : f e.1 = b <;> simp [push, mass, h] at ih ⊢ <;> omega


theorem matching_on_overlap {G AC AC' AW : Type}
    (rC : G → AC) (rC' : G → AC') (ρ : AC → AW) (ρ' : AC' → AW)
    (h : ∀ g, ρ (rC g) = ρ' (rC' g)) (q : Meas G) :
    push ρ (push rC q) = push ρ' (push rC' q) := by
  rw [← push_comp, ← push_comp]
  congr 1
  funext g
  exact h g

theorem matching_weights_on_overlap {G AC AC' AW : Type} [DecidableEq AW]
    (rC : G → AC) (rC' : G → AC') (ρ : AC → AW) (ρ' : AC' → AW)
    (h : ∀ g, ρ (rC g) = ρ' (rC' g)) (q : Meas G) (w : AW) :
    weightAt (push ρ (push rC q)) w = weightAt (push ρ' (push rC' q)) w := by
  rw [matching_on_overlap rC rC' ρ ρ' h q]


def IsSection (n : Nat) (b : Nat → Bool) (g : Nat → Bool) : Prop :=
  ∀ i, i < n → xor (g i) (g ((i + 1) % n)) = b i

def holonomy (b : Nat → Bool) : Nat → Bool
  | 0 => false
  | k + 1 => xor (holonomy b k) (b k)

private theorem xor3 (a c d : Bool) : xor (xor a c) (xor c d) = xor a d := by
  cases a <;> cases c <;> cases d <;> rfl

private theorem holonomy_prefix (n : Nat) (b : Nat → Bool) (g : Nat → Bool)
    (hg : IsSection n b g) : ∀ k, k < n → holonomy b k = xor (g 0) (g k) := by
  intro k
  induction k with
  | zero => intro _; simp [holonomy]
  | succ k ih =>
    intro hk
    have hk' : k < n := by omega
    have hmod : (k + 1) % n = k + 1 := Nat.mod_eq_of_lt hk
    have hb := hg k hk'
    rw [hmod] at hb
    simp only [holonomy]
    rw [ih hk', ← hb]
    exact xor3 (g 0) (g k) (g (k + 1))

theorem section_exists_iff_holonomy_zero (n : Nat) (hn : 0 < n) (b : Nat → Bool) :
    (∃ g, IsSection n b g) ↔ holonomy b n = false := by
  constructor
  · rintro ⟨g, hg⟩
    obtain ⟨m, rfl⟩ : ∃ m, n = m + 1 := ⟨n - 1, by omega⟩
    have hlast := hg m (by omega)
    have hpre := holonomy_prefix (m + 1) b g hg m (by omega)
    have hz : (m + 1) % (m + 1) = 0 := Nat.mod_self _
    rw [hz] at hlast
    simp only [holonomy]
    rw [hpre, ← hlast]
    cases g 0 <;> cases g m <;> rfl
  · intro h
    refine ⟨fun k => holonomy b k, ?_⟩
    intro i hi
    by_cases hlt : i + 1 < n
    · rw [Nat.mod_eq_of_lt hlt]
      simp only [holonomy]
      cases holonomy b i <;> cases b i <;> rfl
    · have hi' : i + 1 = n := by omega
      have hz : (i + 1) % n = 0 := by rw [hi']; exact Nat.mod_self n
      rw [hz]
      have h2 : holonomy b (i + 1) = false := by rw [hi']; exact h
      simp only [holonomy] at h2 ⊢
      cases hh : holonomy b i <;> cases hb : b i <;> simp [hh, hb] at h2 ⊢


def restrictCtx (n : Nat) (i : Nat) (g : Nat → Bool) : Bool × Bool :=
  (g i, g ((i + 1) % n))

theorem entry_weight_zero_of_weightAt_zero {B : Type} [DecidableEq B] (p : Meas B) (b : B)
    (h : weightAt p b = 0) : ∀ e ∈ p, e.1 = b → e.2 = 0 := by
  induction p with
  | nil => intro e he; cases he
  | cons x t ih =>
    unfold weightAt at h
    intro e he hb
    by_cases hx : x.1 = b
    · simp [mass, hx] at h
      rcases List.mem_cons.mp he with rfl | het
      · exact h.1
      · exact ih (by unfold weightAt; exact h.2) e het hb
    · simp [mass, hx] at h
      rcases List.mem_cons.mp he with rfl | het
      · exact absurd hb hx
      · exact ih (by unfold weightAt; exact h) e het hb

theorem exists_positive_entry {A : Type} (q : Meas A) (h : 0 < mass q) : ∃ e ∈ q, 0 < e.2 := by
  induction q with
  | nil => simp [mass] at h
  | cons x t ih =>
    by_cases hx : 0 < x.2
    · exact ⟨x, List.mem_cons_self .., hx⟩
    · have h' : 0 < x.2 + mass t := h
      have : mass t > 0 := by omega
      obtain ⟨e, he, hp⟩ := ih this
      exact ⟨e, List.mem_cons_of_mem _ he, hp⟩

theorem no_joint_measure_when_holonomy_one (n : Nat) (hn : 0 < n) (b : Nat → Bool)
    (hh : holonomy b n = true) (q : Meas (Nat → Bool)) (hpos : 0 < mass q)
    (hsupp : ∀ i, i < n → ∀ w : Bool × Bool, xor w.1 w.2 ≠ b i →
      weightAt (push (restrictCtx n i) q) w = 0) : False := by
  obtain ⟨e, he, hp⟩ := exists_positive_entry q hpos
  have hsec : IsSection n b e.1 := by
    intro i hi
    by_cases hc : xor (e.1 i) (e.1 ((i + 1) % n)) = b i
    · exact hc
    · exfalso
      have hz := hsupp i hi (restrictCtx n i e.1) (by simpa [restrictCtx] using hc)
      have hmem : (restrictCtx n i e.1, e.2) ∈ push (restrictCtx n i) q :=
        List.mem_map.mpr ⟨e, he, rfl⟩
      have h0 := entry_weight_zero_of_weightAt_zero _ _ hz _ hmem rfl
      omega
  have : holonomy b n = false := (section_exists_iff_holonomy_zero n hn b).mp ⟨e.1, hsec⟩
  rw [hh] at this
  exact Bool.noConfusion this


theorem odd_triangle_holonomy : holonomy (fun _ => true) 3 = true := by decide

theorem odd_triangle_has_no_section : ¬ ∃ g, IsSection 3 (fun _ => true) g := by
  intro h
  have := (section_exists_iff_holonomy_zero 3 (by decide) (fun _ => true)).mp h
  rw [odd_triangle_holonomy] at this
  exact Bool.noConfusion this

theorem even_triangle_has_section : ∃ g, IsSection 3 (fun i => decide (i < 2)) g :=
  (section_exists_iff_holonomy_zero 3 (by decide) _).mpr (by decide)


abbrev TriVertex := Bool × Bool × Bool

def satCount3 (g : TriVertex) : Nat :=
  (if xor g.1 g.2.1 then 1 else 0) +
  (if xor g.2.1 g.2.2 then 1 else 0) +
  (if xor g.2.2 g.1 then 1 else 0)

theorem satCount3_le_two (g : TriVertex) : satCount3 g ≤ 2 := by
  rcases g with ⟨g0, g1, g2⟩
  cases g0 <;> cases g1 <;> cases g2 <;> decide

def totalSatWeight3 (q : Meas TriVertex) : Nat :=
  q.foldr (fun e acc => e.2 * satCount3 e.1 + acc) 0

theorem totalSatWeight3_le_two_mul_mass (q : Meas TriVertex) :
    totalSatWeight3 q ≤ 2 * mass q := by
  induction q with
  | nil => simp [totalSatWeight3, mass]
  | cons e t ih =>
    change e.2 * satCount3 e.1 + totalSatWeight3 t ≤ 2 * (e.2 + mass t)
    have hsat := satCount3_le_two e.1
    have hmul : e.2 * satCount3 e.1 ≤ e.2 * 2 := Nat.mul_le_mul_left e.2 hsat
    omega

theorem odd_triangle_lp_dual_defect_pos (q : Meas TriVertex) (hpos : 0 < mass q) :
    totalSatWeight3 q + mass q ≤ 3 * mass q ∧ totalSatWeight3 q < 3 * mass q := by
  have hbound := totalSatWeight3_le_two_mul_mass q
  omega

def lggrCycleGateAdmits (n : Nat) (b : Nat → Bool) (M : Nat) : Bool :=
  decide (M = 0) || !holonomy b n

theorem lggrCycleGateAdmits_iff_section_or_zero_mass (n : Nat) (hn : 0 < n)
    (b : Nat → Bool) (M : Nat) :
    lggrCycleGateAdmits n b M = true ↔ (M = 0 ∨ ∃ g, IsSection n b g) := by
  unfold lggrCycleGateAdmits
  rw [Bool.or_eq_true, decide_eq_true_eq, Bool.not_eq_true',
    ← section_exists_iff_holonomy_zero n hn b]

end LggrFiniteResults

#print axioms LggrFiniteResults.push_id
#print axioms LggrFiniteResults.push_comp
#print axioms LggrFiniteResults.mass_push
#print axioms LggrFiniteResults.weightAt_push
#print axioms LggrFiniteResults.matching_on_overlap
#print axioms LggrFiniteResults.matching_weights_on_overlap
#print axioms LggrFiniteResults.section_exists_iff_holonomy_zero
#print axioms LggrFiniteResults.no_joint_measure_when_holonomy_one
#print axioms LggrFiniteResults.odd_triangle_has_no_section
#print axioms LggrFiniteResults.even_triangle_has_section
#print axioms LggrFiniteResults.satCount3_le_two
#print axioms LggrFiniteResults.totalSatWeight3_le_two_mul_mass
#print axioms LggrFiniteResults.odd_triangle_lp_dual_defect_pos
#print axioms LggrFiniteResults.lggrCycleGateAdmits_iff_section_or_zero_mass


private def l5aProvenance : String :=
  "Origin: lean4/LggrFiniteResults.lean Claim: push_id AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
