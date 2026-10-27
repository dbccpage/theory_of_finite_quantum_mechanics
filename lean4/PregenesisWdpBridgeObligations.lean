/-!
# Finite case for PG-WDP-GENESIS-BRIDGE-OBLIGATIONS

AuthorityEffect: None.

The five register rows GEN-WDP-O01..O05 stay open. This module does not discharge them.
It records one finite reading of the O02 candidate "symmetrised adjacency":

* `pairDefect` is false at `(u, v)` exactly when both directed adjacencies are false.
* On two vertices, `pairDefect` is not a directed-step certificate: the opposite
  orientations of one edge differ as directed steps and agree as pair-defects.
* The identity on adjacency is a directed-step certificate on every finite window,
  so the failure of `pairDefect` does not refute every candidate and does not refute O02.
* No positive integers `p, q` satisfy `p * p = 2 * q * q`. That arithmetic fact is not O04.
-/

namespace PregenesisWdpBridgeObligations

/-- A finite directed window: a Bool adjacency on `Fin m`. -/
structure Window (m : Nat) where
  adj : Fin m → Fin m → Bool

/-- Symmetrised adjacency, the candidate O02 map under test. -/
def pairDefect {m : Nat} (w : Window m) (u v : Fin m) : Bool :=
  w.adj u v || w.adj v u

/-- A directed step is the presence of one oriented adjacency. -/
def DirectedStep {m : Nat} (w : Window m) (u v : Fin m) : Prop :=
  w.adj u v = true

/-- A Bool matrix extracted from a window certifies directed steps when it matches them exactly. -/
def IsDirectedStepCertificate {m : Nat}
    (φ : Window m → Fin m → Fin m → Bool) : Prop :=
  ∀ w u v, DirectedStep w u v ↔ φ w u v = true

theorem pairDefect_false_iff {m : Nat} (w : Window m) (u v : Fin m) :
    pairDefect w u v = false ↔ w.adj u v = false ∧ w.adj v u = false := by
  unfold pairDefect
  cases w.adj u v <;> cases w.adj v u <;>
    simp

/-- Identity on adjacency. This is a certificate, and it is not a source-admission map. -/
def idAdj {m : Nat} (w : Window m) (u v : Fin m) : Bool :=
  w.adj u v

theorem idAdj_is_certificate {m : Nat} :
    IsDirectedStepCertificate (m := m) idAdj := by
  intro w u v
  constructor
  · intro h
    simpa [DirectedStep, idAdj] using h
  · intro h
    simpa [DirectedStep, idAdj] using h

theorem some_certificate_exists {m : Nat} :
    ∃ φ : Window m → Fin m → Fin m → Bool, IsDirectedStepCertificate φ :=
  ⟨idAdj, idAdj_is_certificate⟩

/-- One directed edge `0 → 1` on two vertices. -/
def edge01 : Window 2 :=
  ⟨fun u v => u.val == 0 && v.val == 1⟩

/-- The opposite edge `1 → 0`. -/
def edge10 : Window 2 :=
  ⟨fun u v => u.val == 1 && v.val == 0⟩

theorem witness_orientation_swap :
    pairDefect edge01 0 1 = true ∧
    pairDefect edge10 0 1 = true ∧
    DirectedStep edge01 0 1 ∧
    ¬ DirectedStep edge10 0 1 ∧
    DirectedStep edge10 1 0 ∧
    ¬ DirectedStep edge01 1 0 := by
  unfold pairDefect DirectedStep edge01 edge10
  decide

theorem pairDefect_not_directed_step_certificate :
    ¬ IsDirectedStepCertificate (m := 2) pairDefect := by
  intro h
  have hw := witness_orientation_swap
  have hstep : DirectedStep edge01 0 1 := hw.2.2.1
  have hnostep : ¬ DirectedStep edge10 0 1 := hw.2.2.2.1
  have htrue : pairDefect edge01 0 1 = true := hw.1
  have htrue' : pairDefect edge10 0 1 = true := hw.2.1
  exact hnostep ((h edge10 0 1).mpr htrue')

/-- No positive integers satisfy `p * p = 2 * q * q`. -/
theorem no_sq_eq_two_sq : ∀ q : Nat, 0 < q → ∀ p : Nat, p * p ≠ 2 * (q * q) := by
  intro q
  induction q using Nat.strongRecOn with
  | ind q ih =>
    intro hq p hp
    have hpmod : p % 2 = 0 := by
      cases Nat.mod_two_eq_zero_or_one p with
      | inl h => exact h
      | inr h =>
        exfalso
        have hodd : (p * p) % 2 = 1 := by
          rw [Nat.mul_mod, h]
        have heven : (2 * (q * q)) % 2 = 0 :=
          Nat.mod_eq_zero_of_dvd (Nat.dvd_mul_right 2 (q * q))
        have hmod : (p * p) % 2 = (2 * (q * q)) % 2 := by rw [hp]
        rw [hodd, heven] at hmod
        cases hmod
    obtain ⟨r, hr⟩ := Nat.dvd_of_mod_eq_zero hpmod
    have hsq : (2 * r) * (2 * r) = 2 * (2 * (r * r)) := by
      calc
        (2 * r) * (2 * r) = 2 * (r * (2 * r)) := Nat.mul_assoc 2 r (2 * r)
        _ = 2 * ((r * 2) * r) := by rw [← Nat.mul_assoc r 2 r]
        _ = 2 * ((2 * r) * r) := by rw [Nat.mul_comm r 2]
        _ = 2 * (2 * (r * r)) := by rw [Nat.mul_assoc 2 r r]
    have hqeq : q * q = 2 * (r * r) := by
      have hmul : 2 * (2 * (r * r)) = 2 * (q * q) := by
        simpa [hsq, hr] using hp
      exact (Nat.mul_left_cancel Nat.two_pos hmul).symm
    have hrpos : 0 < r := by
      cases r with
      | zero =>
        rw [hr] at hp
        have h0 : 2 * (q * q) = 0 := by simpa using hp.symm
        have hqsq : q * q = 0 := by
          cases Nat.mul_eq_zero.mp h0 with
          | inl htwo => exact absurd htwo (by decide)
          | inr hqq => exact hqq
        have hq0 : q = 0 := by
          cases Nat.mul_eq_zero.mp hqsq with
          | inl h => exact h
          | inr h => exact h
        exact absurd hq0 (Nat.ne_of_gt hq)
      | succ n =>
        exact Nat.zero_lt_succ n
    have hrr : 0 < r * r := (Nat.mul_pos_iff_of_pos_left hrpos).mpr hrpos
    have hlt : r * r < 2 * (r * r) := by
      have : r * r < r * r + r * r := Nat.lt_add_of_pos_right hrr
      simpa [Nat.two_mul] using this
    have hrlt : r < q := (Nat.mul_self_lt_mul_self_iff).mp (by simpa [hqeq] using hlt)
    exact ih r hrlt hrpos q hqeq

theorem one_sq_ne_two : (1 : Nat) * 1 ≠ 2 * (1 * 1) := by
  decide

theorem one_sq_values : (1 : Nat) * 1 = 1 ∧ 2 * (1 * 1) = 2 := by
  decide

theorem no_sq_at_one : ∀ p : Nat, p * p ≠ 2 * (1 * 1) :=
  no_sq_eq_two_sq 1 (by decide)

end PregenesisWdpBridgeObligations

#print axioms PregenesisWdpBridgeObligations.pairDefect_false_iff
#print axioms PregenesisWdpBridgeObligations.idAdj_is_certificate
#print axioms PregenesisWdpBridgeObligations.some_certificate_exists
#print axioms PregenesisWdpBridgeObligations.witness_orientation_swap
#print axioms PregenesisWdpBridgeObligations.pairDefect_not_directed_step_certificate
#print axioms PregenesisWdpBridgeObligations.no_sq_eq_two_sq
#print axioms PregenesisWdpBridgeObligations.one_sq_ne_two
#print axioms PregenesisWdpBridgeObligations.one_sq_values
#print axioms PregenesisWdpBridgeObligations.no_sq_at_one
