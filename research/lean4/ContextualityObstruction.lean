

namespace ContextualityObstruction


abbrev Z2 := Fin 2

@[simp] theorem z2_sub_self (x : Z2) : x - x = 0 := by
  revert x
  decide

def Cochain0 (n m : Nat) := Fin m → Fin n → Z2

def Cochain1 (n m : Nat) := Fin m → Fin m → Fin n → Z2

def Cochain2 (n m : Nat) := Fin m → Fin m → Fin m → Fin n → Z2

def d0 {n m : Nat} (s : Cochain0 n m) : Cochain1 n m :=
  fun i j r => s j r - s i r

def d1 {n m : Nat} (w : Cochain1 n m) : Cochain2 n m :=
  fun i j k r => w j k r - w i k r + w i j r

theorem differential_squares_to_zero {n m : Nat} (s : Cochain0 n m) (i j k : Fin m) (r : Fin n) :
    d1 (d0 s) i j k r = 0 := by
  dsimp [d1, d0]
  generalize s k r = c
  generalize s j r = b
  generalize s i r = a
  revert a b c
  decide


structure MeasurementScenario (n m : Nat) where
  contexts : Fin m → List (Fin n)
  b_targets : Fin m → Z2

def ctxSum {n : Nat} (ctx : List (Fin n)) (g : Fin n → Z2) : Z2 :=
  ctx.foldl (fun acc r => acc + g r) 0


def IsGlobalSection {n m : Nat} (scen : MeasurementScenario n m) (g : Fin n → Z2) : Prop :=
  ∀ i : Fin m, ctxSum (scen.contexts i) g = scen.b_targets i

def sectionToCochain0 {n m : Nat} (g : Fin n → Z2) : Cochain0 n m :=
  fun _ r => g r

theorem d0_of_global_section {n m : Nat} (g : Fin n → Z2) (i j : Fin m) (r : Fin n) :
    d0 (sectionToCochain0 (m := m) g) i j r = 0 := by
  dsimp [d0, sectionToCochain0]
  exact z2_sub_self (g r)

structure InhabitedGlobalSection {n m : Nat} (scen : MeasurementScenario n m) where
  global_section : Fin n → Z2
  is_valid : IsGlobalSection scen global_section


def contexts_X2 : Fin 4 → List (Fin 4)
  | 0 => [0, 2]
  | 1 => [0, 3]
  | 2 => [1, 2]
  | 3 => [1, 3]

def targets_X2 : Fin 4 → Z2 :=
  fun _ => 1

def X2 : MeasurementScenario 4 4 := {
  contexts := contexts_X2
  b_targets := targets_X2
}

def g_X2 : Fin 4 → Z2
  | 0 => 1
  | 1 => 1
  | 2 => 0
  | 3 => 0

theorem x2_global_section_valid : IsGlobalSection X2 g_X2 := by
  intro i
  rcases i with ⟨val, h⟩
  match val with
  | 0 => decide +revert
  | 1 => decide +revert
  | 2 => decide +revert
  | 3 => decide +revert
  | n + 4 => omega

def x2_obstruction_vanishes : InhabitedGlobalSection X2 := {
  global_section := g_X2
  is_valid := x2_global_section_valid
}

theorem x2_d0_vanishes (i j : Fin 4) (r : Fin 4) :
    d0 (sectionToCochain0 (m := 4) g_X2) i j r = 0 :=
  d0_of_global_section g_X2 i j r


def contexts_X1 : Fin 9 → List (Fin 18)
  | 0 => [2, 9, 15, 17]
  | 1 => [4, 7, 13, 17]
  | 2 => [5, 6, 13, 15]
  | 3 => [0, 3, 9, 16]
  | 4 => [0, 6, 10, 14]
  | 5 => [1, 5, 11, 14]
  | 6 => [1, 7, 8, 12]
  | 7 => [2, 8, 11, 16]
  | 8 => [3, 4, 10, 12]

def targets_X1 : Fin 9 → Z2 :=
  fun _ => 1

def X1 : MeasurementScenario 18 9 := {
  contexts := contexts_X1
  b_targets := targets_X1
}

def contextSumNat (ctx : List (Fin 18)) (g : Fin 18 → Z2) : Nat :=
  match ctx with
  | [r0, r1, r2, r3] => (g r0).val + (g r1).val + (g r2).val + (g r3).val
  | _ => 0

theorem cabello_ray_incidence_identity (g : Fin 18 → Z2) :
    contextSumNat (contexts_X1 0) g +
    contextSumNat (contexts_X1 1) g +
    contextSumNat (contexts_X1 2) g +
    contextSumNat (contexts_X1 3) g +
    contextSumNat (contexts_X1 4) g +
    contextSumNat (contexts_X1 5) g +
    contextSumNat (contexts_X1 6) g +
    contextSumNat (contexts_X1 7) g +
    contextSumNat (contexts_X1 8) g =
    2 * ((g 0).val + (g 1).val + (g 2).val + (g 3).val + (g 4).val + (g 5).val +
         (g 6).val + (g 7).val + (g 8).val + (g 9).val + (g 10).val + (g 11).val +
         (g 12).val + (g 13).val + (g 14).val + (g 15).val + (g 16).val + (g 17).val) := by
  dsimp [contextSumNat, contexts_X1]
  omega

theorem odd_sum_nine_contradiction
    (c0 c1 c2 c3 c4 c5 c6 c7 c8 K : Nat)
    (h0 : c0 % 2 = 1)
    (h1 : c1 % 2 = 1)
    (h2 : c2 % 2 = 1)
    (h3 : c3 % 2 = 1)
    (h4 : c4 % 2 = 1)
    (h5 : c5 % 2 = 1)
    (h6 : c6 % 2 = 1)
    (h7 : c7 % 2 = 1)
    (h8 : c8 % 2 = 1)
    (htot : c0 + c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 = 2 * K) :
    False := by
  omega

theorem ctxSum_four_eq_mod2 (r0 r1 r2 r3 : Fin 18) (g : Fin 18 → Z2) :
    (ctxSum [r0, r1, r2, r3] g).val = ((g r0).val + (g r1).val + (g r2).val + (g r3).val) % 2 := by
  dsimp [ctxSum]
  generalize (g r0) = a
  generalize (g r1) = b
  generalize (g r2) = c
  generalize (g r3) = d
  revert a b c d
  decide

theorem x1_has_no_global_section : ¬ (∃ g, IsGlobalSection X1 g) := by
  intro ⟨g, hg⟩
  have h_targets (i : Fin 9) : (ctxSum (contexts_X1 i) g).val = 1 := by
    have hi := hg i
    dsimp [X1, targets_X1] at hi
    rw [hi]
    rfl

  have hc (i : Fin 9) : (contextSumNat (contexts_X1 i) g) % 2 = 1 := by
    rcases i with ⟨val, hval⟩
    match val with
    | 0 =>
      have h0 := h_targets 0
      dsimp [contexts_X1] at h0
      rw [ctxSum_four_eq_mod2 2 9 15 17 g] at h0
      dsimp [contextSumNat, contexts_X1]
      exact h0
    | 1 =>
      have h1 := h_targets 1
      dsimp [contexts_X1] at h1
      rw [ctxSum_four_eq_mod2 4 7 13 17 g] at h1
      dsimp [contextSumNat, contexts_X1]
      exact h1
    | 2 =>
      have h2 := h_targets 2
      dsimp [contexts_X1] at h2
      rw [ctxSum_four_eq_mod2 5 6 13 15 g] at h2
      dsimp [contextSumNat, contexts_X1]
      exact h2
    | 3 =>
      have h3 := h_targets 3
      dsimp [contexts_X1] at h3
      rw [ctxSum_four_eq_mod2 0 3 9 16 g] at h3
      dsimp [contextSumNat, contexts_X1]
      exact h3
    | 4 =>
      have h4 := h_targets 4
      dsimp [contexts_X1] at h4
      rw [ctxSum_four_eq_mod2 0 6 10 14 g] at h4
      dsimp [contextSumNat, contexts_X1]
      exact h4
    | 5 =>
      have h5 := h_targets 5
      dsimp [contexts_X1] at h5
      rw [ctxSum_four_eq_mod2 1 5 11 14 g] at h5
      dsimp [contextSumNat, contexts_X1]
      exact h5
    | 6 =>
      have h6 := h_targets 6
      dsimp [contexts_X1] at h6
      rw [ctxSum_four_eq_mod2 1 7 8 12 g] at h6
      dsimp [contextSumNat, contexts_X1]
      exact h6
    | 7 =>
      have h7 := h_targets 7
      dsimp [contexts_X1] at h7
      rw [ctxSum_four_eq_mod2 2 8 11 16 g] at h7
      dsimp [contextSumNat, contexts_X1]
      exact h7
    | 8 =>
      have h8 := h_targets 8
      dsimp [contexts_X1] at h8
      rw [ctxSum_four_eq_mod2 3 4 10 12 g] at h8
      dsimp [contextSumNat, contexts_X1]
      exact h8
    | n + 9 => omega

  have h_geom := cabello_ray_incidence_identity g
  exact odd_sum_nine_contradiction
    (contextSumNat (contexts_X1 0) g)
    (contextSumNat (contexts_X1 1) g)
    (contextSumNat (contexts_X1 2) g)
    (contextSumNat (contexts_X1 3) g)
    (contextSumNat (contexts_X1 4) g)
    (contextSumNat (contexts_X1 5) g)
    (contextSumNat (contexts_X1 6) g)
    (contextSumNat (contexts_X1 7) g)
    (contextSumNat (contexts_X1 8) g)
    ((g 0).val + (g 1).val + (g 2).val + (g 3).val + (g 4).val + (g 5).val +
     (g 6).val + (g 7).val + (g 8).val + (g 9).val + (g 10).val + (g 11).val +
     (g 12).val + (g 13).val + (g 14).val + (g 15).val + (g 16).val + (g 17).val)
    (hc 0) (hc 1) (hc 2) (hc 3) (hc 4) (hc 5) (hc 6) (hc 7) (hc 8)
    h_geom

#print axioms differential_squares_to_zero
#print axioms d0_of_global_section
#print axioms x2_global_section_valid
#print axioms x2_obstruction_vanishes
#print axioms x1_has_no_global_section

end ContextualityObstruction

private def l5aProvenance : String :=
  "Origin: lean4/ContextualityObstruction.lean Claim: differential_squares_to_zero AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
