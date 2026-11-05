/-
Letter E: exact repair, over an abstract cochain complex with Int coefficients.
Cochains are functions `Nat → Int`; `d0` and `d1` are additive and `d1 ∘ d0 = 0`.
Replaces the sub-paper lemma that needed Mathlib (`abel`). AuthorityEffect: None.
-/
import Ddc.Law

namespace Ddc

structure Complex where
  d0 : (Nat → Int) → (Nat → Int)
  d1 : (Nat → Int) → (Nat → Int)
  d0_sub : ∀ f g, d0 (fun v => f v - g v) = fun e => d0 f e - d0 g e
  d1_sub : ∀ f g, d1 (fun e => f e - g e) = fun p => d1 f p - d1 g p
  chain : ∀ f, d1 (d0 f) = fun _ => 0

/-- `x` lies in the image of `d0`: E can repair it. -/
def IsExact (K : Complex) (x : Nat → Int) : Prop := ∃ φ, K.d0 φ = x

/-- A gauge move: subtract a coboundary. -/
def gaugeMove (K : Complex) (x φ : Nat → Int) : Nat → Int := fun e => x e - K.d0 φ e

/-- DDC-E-02: repairing with a potential of the defect leaves zero. -/
theorem E_gauge_repair_discharges (K : Complex) (x φ : Nat → Int) (h : K.d0 φ = x) :
    gaugeMove K x φ = fun _ => 0 := by
  funext e
  simp [gaugeMove, h]

/-- An exact defect is closed: Γ₂ vanishes on `im d0`. -/
theorem E_exact_is_closed (K : Complex) (x : Nat → Int) (h : IsExact K x) :
    K.d1 x = fun _ => 0 := by
  obtain ⟨φ, rfl⟩ := h
  exact K.chain φ

/-- Gauge moves leave the face defect unchanged (Γ₂ is gauge invariant). -/
theorem E_gauge_preserves_closure (K : Complex) (x φ : Nat → Int) :
    K.d1 (gaugeMove K x φ) = K.d1 x := by
  show K.d1 (fun e => x e - K.d0 φ e) = K.d1 x
  rw [K.d1_sub, K.chain]
  funext p
  simp

/-- Gauge moves leave exactness unchanged, so no gauge repair crosses a class. -/
theorem E_gauge_preserves_exactness (K : Complex) (x φ : Nat → Int) :
    IsExact K (gaugeMove K x φ) ↔ IsExact K x := by
  constructor
  · rintro ⟨ψ, hψ⟩
    refine ⟨fun v => ψ v + φ v, ?_⟩
    have hsub := K.d0_sub (fun v => ψ v + φ v) φ
    have hψ' : (fun v => (ψ v + φ v) - φ v) = ψ := by funext v; omega
    rw [hψ'] at hsub
    funext e
    have h1 := congrFun hsub e
    have h2 := congrFun hψ e
    simp only [gaugeMove] at h2
    omega
  · rintro ⟨ψ, hψ⟩
    refine ⟨fun v => ψ v - φ v, ?_⟩
    rw [K.d0_sub, hψ]
    rfl

/-- E-05: exact repair is idempotent — the repaired defect is zero, and zero is fixed. -/
theorem E_repair_idempotent (K : Complex) (x φ : Nat → Int) (h : K.d0 φ = x) :
    gaugeMove K (gaugeMove K x φ) (fun _ => 0) = gaugeMove K x φ := by
  rw [E_gauge_repair_discharges K x φ h]
  funext e
  have hz : K.d0 (fun _ => 0) = fun _ => 0 := by
    have := K.d0_sub (fun _ => 0) (fun _ => 0)
    simp only [Int.sub_self] at this
    funext e'
    have := congrFun this e'
    omega
  simp [gaugeMove, hz]

/-- The filled triangle: vertices 0 1 2, edges 0→1, 1→2, 2→0, one face. -/
def triangle : Complex where
  d0 φ e := if e = 0 then φ 1 - φ 0 else if e = 1 then φ 2 - φ 1 else if e = 2 then φ 0 - φ 2 else 0
  d1 x p := if p = 0 then x 0 + x 1 + x 2 else 0
  d0_sub f g := by
    funext e
    by_cases h0 : e = 0 <;> by_cases h1 : e = 1 <;> by_cases h2 : e = 2 <;> simp [h0, h1, h2] <;> omega
  d1_sub f g := by
    funext p
    by_cases h0 : p = 0 <;> simp [h0] <;> omega
  chain f := by
    funext p
    by_cases h0 : p = 0 <;> simp [h0] <;> omega

/-- The local-green / global-red triangle: every edge carries 1, yet Γ₂ ≠ 0, so E is refused. -/
theorem E_triangle_open_not_exact :
    ¬ IsExact triangle (fun e => if e ≤ 2 then 1 else 0) := by
  intro h
  have hc := congrFun (E_exact_is_closed triangle _ h) 0
  simp [triangle] at hc

end Ddc
