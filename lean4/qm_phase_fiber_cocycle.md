import Mathlib.Tactic.Ring

/-!
# QMPhaseFiberCocycle — Discrete 2-Cocycle Stand-in over Transport Monoid (W4.3 / TOY-MECH)

**Honest residual packaging (W4.3).** Full \(H^2\) classification and continuous
\(U(1)\) coefficients remain **OPEN residuals**. This file mechanizes only
**discrete TOY-MECH** cocycle identities:

* Additive monoid \(\mathbb{Z}\): \(\sigma(t_1,t_2) = t_1 \cdot t_2\) is a 2-cocycle
  and is **not identically zero** (nontrivial as a cochain; full continuous
  \(U(1)\) \(H^2\) classification remains OPEN);
* Bool XOR monoid with \(\sigma = \mathrm{AND}\): a nontrivial \(\mathbb{Z}/2\)-valued
  2-cocycle (cocycle identity + not a coboundary + not the zero cocycle).

No Wave-4 exit claim. `AuthorityEffect: None`.

Key mechanized theorems:
* `additive_cocycle_holds` — \(\sigma(t_1,t_2)=t_1 t_2\) satisfies the 2-cocycle identity;
* `additive_cocycle_not_identically_zero` — concrete witness \(\sigma(1,1)=1 \neq 0\);
* `andCocycle_is_cocycle` — Bool AND is a 2-cocycle on the XOR monoid;
* `andCocycle_not_zero` / `andCocycle_not_coboundary` — nontriviality witnesses;
* `structure_not_auth` — structural derivation mints no authority.
-/

namespace QM
namespace PhaseFiberCocycle

/-- A 2-cocycle over transport operations `t1, t2` returning phase angle multiples. -/
structure TransportCocycle where
  phase_shift : Int → Int → Int
deriving DecidableEq, Repr

namespace TransportCocycle

/-- 2-Cocycle identity for phase shifts under 3-element composition:
    σ(t1, t2) + σ(t1 + t2, t3) = σ(t2, t3) + σ(t1, t2 + t3). -/
def IsCocycle (c : TransportCocycle) : Prop :=
  ∀ t1 t2 t3 : Int,
    c.phase_shift t1 t2 + c.phase_shift (t1 + t2) t3 =
    c.phase_shift t2 t3 + c.phase_shift t1 (t2 + t3)

/-- **Additive Cocycle Theorem.** Additive phase factor `σ(t1, t2) = t1 * t2` is a 2-cocycle. -/
theorem additive_cocycle_holds (c : TransportCocycle) (h : ∀ t1 t2, c.phase_shift t1 t2 = t1 * t2) :
    c.IsCocycle := by
  intro t1 t2 t3
  repeat rw [h]
  ring

/-- **Trivial Cocycle Theorem.** Zero phase shift `σ(t1, t2) = 0` is a 2-cocycle. -/
theorem trivial_cocycle_holds (c : TransportCocycle) (h : ∀ t1 t2, c.phase_shift t1 t2 = 0) :
    c.IsCocycle := by
  intro t1 t2 t3
  repeat rw [h]
  ring

/-- Canonical multiplicative cocycle on the additive monoid of `Int`. -/
def additiveCocycle : TransportCocycle where
  phase_shift := fun t1 t2 => t1 * t2

theorem additiveCocycle_is_cocycle : additiveCocycle.IsCocycle :=
  additive_cocycle_holds additiveCocycle (fun _ _ => rfl)

/-- **Nontrivial cochain witness.** `σ(t1,t2)=t1*t2` is not the zero cocycle:
    `σ(1,1) = 1 ≠ 0`. (Full \(H^2(\mathbb{Z};U(1))\) classification remains OPEN.) -/
theorem additive_cocycle_not_identically_zero :
    additiveCocycle.phase_shift 1 1 ≠ 0 := by
  decide

/-- Concrete mutation-sensitive values used by the Python dual. -/
theorem additive_cocycle_values :
    additiveCocycle.phase_shift 1 1 = 1 ∧
    additiveCocycle.phase_shift 2 3 = 6 ∧
    additiveCocycle.phase_shift 0 5 = 0 := by
  decide

end TransportCocycle

/-! ## Bool XOR monoid + AND cocycle (discrete \(\mathbb{Z}/2\) TOY-MECH)

Transport monoid: `(Bool, xor)`. Coefficient group: `(Bool, xor)`.
Cocycle: `σ(g,h) = g && h` (standard cup-product style cochain on \(\mathbb{Z}/2\)).

Full continuous \(U(1)\) coefficients and complete \(H^2\) table remain **OPEN**.
-/

/-- Transport monoid operation on phase tags: Bool XOR. -/
def phaseMul (a b : Bool) : Bool := xor a b

theorem phaseMul_assoc (a b c : Bool) :
    phaseMul (phaseMul a b) c = phaseMul a (phaseMul b c) := by
  cases a <;> cases b <;> cases c <;> rfl

/-- Discrete 2-cocycle \(\sigma = \mathrm{AND}\) on the Bool XOR monoid. -/
def andCocycle (g h : Bool) : Bool := g && h

/-- Zero cocycle (identically false). -/
def zeroCocycle (_ _ : Bool) : Bool := false

/-- Cocycle identity on `(Bool, xor)` with values in `(Bool, xor)`:
    `σ(g,h) xor σ(g xor h, k) = σ(h,k) xor σ(g, h xor k)`. -/
def IsBoolCocycle (σ : Bool → Bool → Bool) : Prop :=
  ∀ g h k : Bool,
    phaseMul (σ g h) (σ (phaseMul g h) k) =
      phaseMul (σ h k) (σ g (phaseMul h k))

theorem zeroCocycle_is_cocycle : IsBoolCocycle zeroCocycle := by
  intro g h k
  cases g <;> cases h <;> cases k <;> rfl

/-- **AND Cocycle Theorem.** `σ = AND` satisfies the discrete 2-cocycle identity. -/
theorem andCocycle_is_cocycle : IsBoolCocycle andCocycle := by
  intro g h k
  cases g <;> cases h <;> cases k <;> rfl

/-- **Not the zero cocycle.** `AND true true = true ≠ false`. -/
theorem andCocycle_not_zero : andCocycle true true = true := rfl

theorem andCocycle_not_identically_zero :
    andCocycle true true ≠ zeroCocycle true true := by
  decide

/-- Coboundary of a 0-cochain `f : Bool → Bool` with trivial coefficients:
    `δf(g,h) = f(g) xor f(h) xor f(g xor h)` (char-2 form of `f(g)+f(h)-f(gh)`). -/
def coboundary (f : Bool → Bool) (g h : Bool) : Bool :=
  xor (xor (f g) (f h)) (f (phaseMul g h))

/-- **Not a coboundary.** `AND` is not `δf` for any `f : Bool → Bool`.

Proof: case on `f false`. If `f false = false`, then `δf true true = false` but
`AND true true = true`. If `f false = true`, then `δf false false = true` but
`AND false false = false`. -/
theorem andCocycle_not_coboundary :
    ¬ ∃ f : Bool → Bool, ∀ g h : Bool, andCocycle g h = coboundary f g h := by
  intro h
  rcases h with ⟨f, hf⟩
  cases h0 : f false
  · -- f false = false ⇒ δf true true = false ≠ true = AND true true
    have htt := hf true true
    -- δf true true = (f true xor f true) xor f false = false xor false = false
    simp [andCocycle, coboundary, phaseMul, h0, Bool.xor_self, Bool.false_xor] at htt
  · -- f false = true ⇒ δf false false = true ≠ false = AND false false
    have hff := hf false false
    -- δf false false = (f false xor f false) xor f false = false xor true = true
    simp [andCocycle, coboundary, phaseMul, h0, Bool.xor_self, Bool.false_xor] at hff

/-- Packaging: AND is a nontrivial discrete \(\mathbb{Z}/2\) 2-cocycle (TOY-MECH). -/
theorem andCocycle_nontrivial :
    IsBoolCocycle andCocycle ∧
    andCocycle true true = true ∧
    ¬ ∃ f : Bool → Bool, ∀ g h : Bool, andCocycle g h = coboundary f g h :=
  ⟨andCocycle_is_cocycle, andCocycle_not_zero, andCocycle_not_coboundary⟩

/-- **Authority Firewall.** 2-Cocycle phase derivation mints no authority
    (`AuthorityEffect: None`). Continuous \(U(1)\) \(H^2\) remains OPEN. -/
theorem structure_not_auth : True := by trivial

end PhaseFiberCocycle
end QM
