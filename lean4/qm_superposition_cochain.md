import Mathlib

/-!
# The superposition cochain backbone — one complex under the holonomy ladder

The rungs interference / entanglement / curvature are all features of ONE finite cochain
complex `C⁰ →d₀ C¹` on a cycle (vertices and edges indexed by `ZMod n`; edge `x` runs
`x → x+1`):

* **superposition** = a 1-cochain `a : ZMod n → A` (the phase datum the L1/diagonal marginal
  forgets);
* **gauge** = `im d₀` (global/relative phase reparametrisation — physically removable);
* **interference** = the holonomy `hol a = Σ_x a x`, the `H¹` pairing with the fundamental
  1-cycle; it annihilates gauge (`hol ∘ d₀ = 0`), so it descends to `C¹ / im d₀ = H¹`;
* **entanglement** = the rank of `H¹` (many independent cycles, cf. `holonomy_resource_injective`),
  **curvature** = the non-abelian version of the same `hol`/`d₀` telescoping (cf.
  `HolonomyCurvature.lean`).

This file is the abelian backbone (Slice 1): the complex, the holonomy pairing, `hol ∘ d₀ = 0`
(gauge is holonomy-invisible — the cycle's `d∘d = 0` shadow, cf. `coboundary_loop_zero_holonomy`),
and surjectivity of `hol` (interference is fully realised). The converse `ker hol = im d₀`
(⇒ `H¹ ≅ A`, the full single-loop classification) is the next slice.

No authority minted (GTOC-5); finite, carrier-declared (`ZMod n` cycle).
-/

namespace QM.SuperpositionCochain

variable {n : ℕ} [NeZero n] {A : Type*}

/-- The coboundary `d₀ : C⁰ → C¹`, `(d₀ φ) x = φ(x+1) − φ x` — a **gauge** (phase
reparametrisation of a superposition). -/
def d0 [Sub A] (φ : ZMod n → A) : ZMod n → A := fun x => φ (x + 1) - φ x

/-- The **holonomy** `hol a = Σ_x a x`: the `H¹` pairing of a superposition with the
fundamental 1-cycle — i.e. the **interference** content. -/
def hol [AddCommMonoid A] (a : ZMod n → A) : A := ∑ x, a x

/-- A 1-cochain is **gauge** (pure phase reparametrisation) iff it is a coboundary `a ∈ im d₀`. -/
def IsGauge [Sub A] (a : ZMod n → A) : Prop := ∃ φ : ZMod n → A, d0 φ = a

/-- **`hol ∘ d₀ = 0`** — gauge is holonomy-invisible. The `H¹` pairing annihilates coboundaries,
so holonomy descends to `C¹ / im d₀`. (The `n`-cycle has no 2-cells, so this is the complex's
`d∘d = 0` shadow; the abelian sibling of `coboundary_loop_zero_holonomy`.) -/
theorem hol_d0_zero [AddCommGroup A] (φ : ZMod n → A) : hol (d0 φ) = 0 := by
  have key : ∑ x, φ (x + 1) = ∑ x, φ x := by
    have h := Equiv.sum_comp (Equiv.addRight (1 : ZMod n)) φ
    simpa using h
  simp only [hol, d0]
  rw [Finset.sum_sub_distrib, key, sub_self]

/-- Gauge superpositions carry zero interference. -/
theorem gauge_holonomy_zero [AddCommGroup A] {a : ZMod n → A} (h : IsGauge a) :
    hol a = 0 := by
  obtain ⟨φ, rfl⟩ := h; exact hol_d0_zero φ

/-- **`hol` is surjective** — every interference value is realised by some superposition (put it
all on edge `0`). So interference is not constrained away by the complex. -/
theorem hol_surjective [AddCommGroup A] (c : A) : ∃ a : ZMod n → A, hol a = c := by
  refine ⟨fun x => if x = 0 then c else 0, ?_⟩
  simp [hol, Finset.sum_ite_eq']

/-! ## Slice 2 — the converse: `ker hol = im d₀`, so `H¹ ≅ A` (single-loop classification) -/

open Finset in
/-- The interference `hol a` equals the sum of edge weights along the path `0,1,…,n−1` (the
canonical `ℕ → ZMod n` bijection on `range n`). -/
private theorem hol_eq_sum_range [AddCommMonoid A] (a : ZMod n → A) :
    hol a = ∑ k ∈ Finset.range n, a (k : ZMod n) := by
  have hinj : ∀ x ∈ Finset.range n, ∀ y ∈ Finset.range n,
      ((x : ZMod n) = (y : ZMod n)) → x = y := by
    intro x hx y hy hxy
    rw [Finset.mem_range] at hx hy
    have hv := congrArg ZMod.val hxy
    rwa [ZMod.val_natCast, ZMod.val_natCast, Nat.mod_eq_of_lt hx, Nat.mod_eq_of_lt hy] at hv
  have himg : (Finset.range n).image (fun k : ℕ => (k : ZMod n)) = Finset.univ := by
    rw [Finset.eq_univ_iff_forall]
    intro x
    rw [Finset.mem_image]
    exact ⟨x.val, Finset.mem_range.mpr (ZMod.val_lt x), ZMod.natCast_zmod_val x⟩
  rw [hol, ← himg, Finset.sum_image hinj]

open Finset in
/-- **Converse — single-loop classification.** A superposition with zero interference is gauge:
`hol a = 0 → a ∈ im d₀`. With `hol_d0_zero` this gives `ker hol = im d₀`, hence the holonomy is a
*complete* invariant of `H¹ = C¹ / im d₀` — for the single loop `H¹ ≅ A` (`dim H¹ = E − V + 1 = 1`).
Interference is exactly the L1-invisible content of a superposition, modulo gauge. -/
theorem holonomy_zero_imp_gauge [AddCommGroup A] (a : ZMod n → A) (h : hol a = 0) :
    IsGauge a := by
  refine ⟨fun x => ∑ k ∈ Finset.range x.val, a (k : ZMod n), ?_⟩
  funext x
  simp only [d0]
  have hxlt : x.val < n := ZMod.val_lt x
  rcases eq_or_ne (x.val + 1) n with hwrap | hnowrap
  · -- wrap: `x` is the last vertex, `x + 1 = 0`
    have hx0 : x + 1 = 0 := by
      have hz : ((x.val + 1 : ℕ) : ZMod n) = 0 := by rw [hwrap]; exact ZMod.natCast_self n
      rwa [Nat.cast_add, Nat.cast_one, ZMod.natCast_zmod_val] at hz
    rw [hx0, ZMod.val_zero, Finset.range_zero, Finset.sum_empty, zero_sub]
    have e1 : (∑ k ∈ Finset.range x.val, a (k : ZMod n)) + a x
            = ∑ k ∈ Finset.range (x.val + 1), a (k : ZMod n) := by
      rw [Finset.sum_range_succ, ZMod.natCast_zmod_val]
    have hsplit : hol a = (∑ k ∈ Finset.range x.val, a (k : ZMod n)) + a x := by
      rw [e1, hol_eq_sum_range, hwrap]
    rw [h] at hsplit
    rw [eq_neg_of_add_eq_zero_left hsplit.symm, neg_neg]
  · -- non-wrap: `(x+1).val = x.val + 1`
    have hlt : x.val + 1 < n := by omega
    haveI : Fact (1 < n) := ⟨by omega⟩
    have hx1 : (x + 1).val = x.val + 1 := by
      rw [ZMod.val_add, ZMod.val_one, Nat.mod_eq_of_lt hlt]
    rw [hx1, Finset.sum_range_succ, ZMod.natCast_zmod_val]
    abel

/-- **`ker hol = im d₀`** (single loop): interference vanishes **iff** the superposition is gauge.
The forward direction is `gauge_holonomy_zero`; the converse is `holonomy_zero_imp_gauge`. So
`hol` is the complete `H¹` invariant. -/
theorem holonomy_zero_iff_gauge [AddCommGroup A] (a : ZMod n → A) :
    hol a = 0 ↔ IsGauge a :=
  ⟨holonomy_zero_imp_gauge a, gauge_holonomy_zero⟩

#print axioms hol_d0_zero
#print axioms gauge_holonomy_zero
#print axioms hol_surjective
#print axioms holonomy_zero_imp_gauge
#print axioms holonomy_zero_iff_gauge

end QM.SuperpositionCochain
