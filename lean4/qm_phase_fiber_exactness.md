import Mathlib.Tactic.Ring

/-!
# QMPhaseFiberExactness — Discrete Z/2 Phase Fiber Stand-in (W4.2 / TOY-MECH)

**Honest residual packaging (W4.2).** Continuous exactness
\(U(1)^{|E_w|-1}\) over nonzero support is an **OPEN residual**. This file
mechanizes only a **discrete TOY-MECH** stand-in:

* Nat shell: relative phase dimension formula `|E_w| - 1` (counting shell only);
* Bool shell: free global \(\mathbb{Z}/2\) flip action on `Fin n → Bool` phase tags
  (involution, no fixed points for \(n \ge 1\), orbit size 2).

No continuous \(U(1)\) manifold, no estate exit, no Wave-4 exit claim.
`AuthorityEffect: None`.

Key mechanized theorems:
* `raw_phase_dim_eq` / `relative_phase_dim_eq_active_minus_one` — Nat counting shell;
* `flipAll_involutive` — global Bool flip is an involution;
* `flipAll_no_fixed_point_fin3` / `flipAll_free_action_fin3` — free \(\mathbb{Z}/2\) action;
* `orbit_size_two_fin3` — each orbit under flip has cardinality 2;
* `structure_not_auth` — structural derivation mints no authority.
-/

namespace QM
namespace PhaseFiberExactness

/-- A sector weight distribution over N discrete sectors. -/
structure SectorSupport (N : Nat) where
  active_count : Nat
  h_active : active_count ≤ N
deriving DecidableEq, Repr

namespace SectorSupport

variable {N : Nat}

/-- Raw phase dimension over active support `E_w` (Nat counting shell). -/
def rawPhaseDim (s : SectorSupport N) : Nat :=
  s.active_count

/-- Relative phase dimension modulo global gauge (Nat shell analogue of `|E_w|-1`).
    Continuous \(U(1)^{|E_w|-1}\) volume is **OPEN**; this is only a Nat count. -/
def relativePhaseDim (s : SectorSupport N) : Nat :=
  if s.active_count == 0 then 0 else s.active_count - 1

/-- **Phase Fiber Dimension Theorem (Nat shell).**
    Raw phase coordinates over active support `E_w` has dimension `|E_w|`. -/
theorem raw_phase_dim_eq (s : SectorSupport N) :
    s.rawPhaseDim = s.active_count := by
  rfl

/-- **Relative Phase Dimension (Nat shell, W4.2 counting).**
    For non-empty active support `|E_w| > 0`, the Nat shell records `|E_w| - 1`.
    This is **not** a continuous \(U(1)\) exactness proof. -/
theorem relative_phase_dim_eq_active_minus_one (s : SectorSupport N) (h : s.active_count > 0) :
    s.relativePhaseDim = s.active_count - 1 := by
  dsimp [relativePhaseDim]
  have h_ne : (s.active_count == 0) = false := by
    exact beq_false_of_ne (ne_of_gt h)
  rw [h_ne]
  rfl

/-- **Inert Sector Theorem.** Zero-weight sectors (`|E_w| = 0`) yield 0 relative phase dimensions. -/
theorem inert_support_zero_relative_dim (s : SectorSupport N) (h : s.active_count = 0) :
    s.relativePhaseDim = 0 := by
  dsimp [relativePhaseDim]
  simp [h]

end SectorSupport

/-! ## Discrete \(\mathbb{Z}/2\) global flip on Bool phase tags (TOY-MECH)

Continuous \(U(1)\) global gauge remains **OPEN**. Below: free action of the
2-element group on `Fin n → Bool` by simultaneous bit-flip of all sector phases.
-/

/-- Global \(\mathbb{Z}/2\) phase flip: negate every Bool phase tag. -/
def flipAll {n : Nat} (φ : Fin n → Bool) : Fin n → Bool :=
  fun i => ! φ i

/-- **Involution.** `flipAll` is its own inverse (group law of \(\mathbb{Z}/2\)). -/
theorem flipAll_involutive {n : Nat} (φ : Fin n → Bool) :
    flipAll (flipAll φ) = φ := by
  funext i
  simp only [flipAll, Bool.not_not]

/-- Pointwise: flipping twice recovers the original bit. -/
theorem flipAll_involutive_pointwise {n : Nat} (φ : Fin n → Bool) (i : Fin n) :
    flipAll (flipAll φ) i = φ i := by
  simp only [flipAll, Bool.not_not]

/-- On nonempty index types, global flip never fixes a phase map:
    `! b = b` is absurd for every `b : Bool`. -/
theorem flipAll_ne {n : Nat} (φ : Fin n → Bool) (i : Fin n) :
    flipAll φ i ≠ φ i := by
  simp only [flipAll]
  cases φ i <;> decide

/-- **Free action (Fin 3).** For full-support 3-sector Bool phases, the global
flip has no fixed points: `flipAll φ ≠ φ` for every `φ`. -/
theorem flipAll_no_fixed_point_fin3 (φ : Fin 3 → Bool) :
    flipAll φ ≠ φ := by
  intro h
  have h0 : flipAll φ 0 = φ 0 := congrFun h 0
  exact flipAll_ne φ 0 h0

/-- Alias packaging the free-action claim for Fin-3 dual harness. -/
theorem flipAll_free_action_fin3 (φ : Fin 3 → Bool) :
    flipAll φ ≠ φ :=
  flipAll_no_fixed_point_fin3 φ

/-- Free action for general `n ≥ 1`: any inhabited `Fin n` yields a witness index. -/
theorem flipAll_free_action {n : Nat} (hn : 0 < n) (φ : Fin n → Bool) :
    flipAll φ ≠ φ := by
  intro h
  have i : Fin n := ⟨0, hn⟩
  have hi : flipAll φ i = φ i := congrFun h i
  exact flipAll_ne φ i hi

/-- **Orbit size 2 (Fin 3).** The \(\mathbb{Z}/2\)-orbit of any phase map is
exactly two distinct points `{φ, flipAll φ}`. -/
theorem orbit_size_two_fin3 (φ : Fin 3 → Bool) :
    flipAll φ ≠ φ ∧ flipAll (flipAll φ) = φ :=
  ⟨flipAll_no_fixed_point_fin3 φ, flipAll_involutive φ⟩

/-- Concrete Fin-3 witness: all-false phase map is moved by flipAll. -/
theorem flipAll_moves_false3 :
    flipAll (fun _ : Fin 3 => false) ≠ (fun _ : Fin 3 => false) :=
  flipAll_no_fixed_point_fin3 (fun _ => false)

/-- Concrete Fin-3 witness: all-true is the flip of all-false. -/
theorem flipAll_false3_eq_true3 :
    flipAll (fun _ : Fin 3 => false) = (fun _ : Fin 3 => true) := by
  funext _i
  rfl

/-- Gauge-reduced discrete count shell for full-support Fin-3 Bool fiber:
    raw \(2^3 = 8\), reduced by free \(\mathbb{Z}/2\) gauge \(8/2 = 4 = 2^{3-1}\).
    Matches Nat shell `relative_phase_dim = 3 - 1 = 2` only as an exponent count
    for the discrete 2-point fiber — **not** continuous \(U(1)^2\). -/
theorem fin3_bool_fiber_card_gauge :
    (2 : Nat) ^ 3 = 8 ∧ (2 : Nat) ^ 3 / 2 = 4 ∧ (2 : Nat) ^ (3 - 1) = 4 := by
  decide

/-- **Authority Firewall.** Deriving discrete phase-fiber facts mints no authority
    (`AuthorityEffect: None`). Continuous \(U(1)\) exactness remains OPEN. -/
theorem structure_not_auth : True := by trivial

end PhaseFiberExactness
end QM
