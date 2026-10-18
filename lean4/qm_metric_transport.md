import Mathlib

/-!
# GR-3 — the metric as a transport-invariant measurement pairing

In GR the metric `g_μν` is the pairing that assigns lengths/angles, and the Levi-Civita connection's
defining property is **metric compatibility** `∇g = 0`: parallel transport preserves the metric — its
holonomies are **isometries** of `g`. The Omega shadow types the metric as a *measurement pairing*
(which pairing is imported, cf. `QM_008`) and metric compatibility as: each edge transport is an
isometry of the pairing, hence (isometries composing) the **Wilson loop preserves the metric**.

This file mechanizes that: `IsometryOf B T` (transport `T` preserves pairing `B`); isometries contain
the identity and are closed under composition (`isometry_comp`), so the holonomy of a list of
metric-compatible transports is itself an isometry (`holonomy_isometry`) — *metric compatibility is
closed under loop composition*. A concrete discrete orthogonal transport: a **permutation** preserves
the standard pairing (`perm_isometry`).

This is **GR-3** of the GR paper series (after GR-1 curvature = holonomy, GR-2 Bianchi = `d∘d=0`).
Firewall: a finite pairing-preservation fact on a toy carrier — the metric-compatibility shadow, NOT
the continuum metric, the Levi-Civita uniqueness, or any dynamics (Q-held). *Which* pairing is the
physical metric is imported (`QM_008`). No authority minted (GTOC-5).
-/

namespace QM.MetricTransport

variable {V : Type*} {𝕜 : Type*} [CommRing 𝕜]

/-- A **transport `T` is metric-compatible** (an isometry of the measurement pairing `B`) iff it
preserves `B`: `B (T v) (T w) = B v w`. The finite shadow of `∇g = 0`. -/
def IsometryOf (B : V → V → 𝕜) (T : V → V) : Prop := ∀ v w, B (T v) (T w) = B v w

/-- The identity transport is metric-compatible. -/
theorem isometry_id (B : V → V → 𝕜) : IsometryOf B id := fun _ _ => rfl

/-- Metric-compatible transports are **closed under composition** (isometries form a monoid; with
inverses, the structure group `O(B)`). -/
theorem isometry_comp {B : V → V → 𝕜} {T S : V → V}
    (hT : IsometryOf B T) (hS : IsometryOf B S) : IsometryOf B (T ∘ S) := by
  intro v w
  simp only [Function.comp_apply]
  rw [hT, hS]

/-- **Metric-compatible holonomy preserves the metric.** The ordered composition (Wilson loop) of a
list of metric-compatible transports is itself metric-compatible: transport-invariance of the metric
is closed under loop composition. Ties GR-1: an `SU(2)`/isometry holonomy preserves the (Hermitian)
pairing. -/
theorem holonomy_isometry (B : V → V → 𝕜) (ts : List (V → V))
    (h : ∀ T ∈ ts, IsometryOf B T) : IsometryOf B (ts.foldr (· ∘ ·) id) := by
  induction ts with
  | nil => exact isometry_id B
  | cons T rest ih =>
    have hrest := ih (fun S hS => h S (List.mem_cons.mpr (Or.inr hS)))
    show IsometryOf B (T ∘ rest.foldr (· ∘ ·) id)
    exact isometry_comp (h T (List.mem_cons.mpr (Or.inl rfl))) hrest

/-! ## A concrete discrete orthogonal transport -/

/-- The standard measurement pairing on `Fin n → 𝕜`: `⟨v, w⟩ = Σ_i v_i w_i`. -/
def stdPairing {n : ℕ} (v w : Fin n → 𝕜) : 𝕜 := ∑ i, v i * w i

/-- **A permutation is metric-compatible** for the standard pairing: relabelling the carrier
(`v ↦ v ∘ σ`) preserves `⟨v, w⟩` by reindexing the sum — a concrete discrete orthogonal transport,
the finite shadow of an isometry of `g`. -/
theorem perm_isometry {n : ℕ} (σ : Equiv.Perm (Fin n)) :
    IsometryOf (stdPairing (𝕜 := 𝕜)) (fun v => v ∘ σ) := by
  intro v w
  simp only [stdPairing, Function.comp_apply]
  exact Equiv.sum_comp σ (fun j => v j * w j)

#print axioms isometry_comp
#print axioms holonomy_isometry
#print axioms perm_isometry

end QM.MetricTransport
