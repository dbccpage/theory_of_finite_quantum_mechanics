import «holonomy_curvature»

/-!
# GR-4 — geodesic / parallel transport (functoriality + flat path-independence)

In GR, **parallel transport** is the connection's transport of a vector along a path, and a
**geodesic** is a curve that parallel-transports its own tangent (`∇_v v = 0`). The Omega shadow:
parallel transport along a path is the **Wilson line** — the ordered product of the edge transports —
and the two load-bearing structural facts are

* **path-functoriality** (`transport_append`): transport along a concatenated path is the product of
  the transports (the composition law of the parallel-transport functor); and
* **flat ⟹ path-independence** (`flat_transport_path_independent`): for a flat (pure-gauge)
  connection the transport between two endpoints is the *same for every path* — it depends only on
  the endpoints (homotopy class), because the pure-gauge holonomy telescopes (`holoG_telescope`,
  GR-1). The obstruction to path-independence is exactly non-trivial **curvature** (GR-1's
  `q8_curvature_wilson_nonflat`).

This is **GR-4** of the GR paper series (after GR-1 curvature = holonomy, GR-2 Bianchi = `d∘d=0`,
GR-3 metric = transport-invariant pairing).

Firewall: finite group-transport facts on a toy carrier — the parallel-transport functor and the
flat-path-independence shadow, NOT the continuum geodesic equation, the affine/Levi-Civita structure,
or any dynamics (Q-held). No authority minted (GTOC-5).
-/

namespace QM.GeodesicTransport

open QM.HolonomyCurvature

variable {G : Type*} [Group G]

/-- **Parallel transport along a path** = the ordered product of its edge transports (the Wilson
line). -/
def transport (edges : List G) : G := edges.prod

/-- The empty path carries the identity transport (no motion). -/
theorem transport_nil : transport ([] : List G) = 1 := rfl

/-- **Path-functoriality.** Transport along a concatenated path is the product of the transports —
the composition law of the parallel-transport functor (`transport (p ++ q) = transport p · transport
q`). -/
theorem transport_append (p q : List G) : transport (p ++ q) = transport p * transport q :=
  List.prod_append

/-- **Flat ⟹ path-independent transport.** For a flat (pure-gauge) connection, the holonomy of any
path from `x0` telescopes to `x0⁻¹ · (endpoint)` (`holoG_telescope`, GR-1); so two paths `l₁, l₂`
with the **same endpoint** carry the **same transport**. Flat parallel transport is a function of the
endpoints (homotopy class) — the geodesic/parallel-transport shadow of "no curvature ⇒ no
path-dependence". The obstruction is non-trivial curvature (GR-1). -/
theorem flat_transport_path_independent (x0 : G) (l₁ l₂ : List G)
    (hend : endptG x0 l₁ = endptG x0 l₂) : holoG x0 l₁ = holoG x0 l₂ := by
  rw [holoG_telescope, holoG_telescope, hend]

#print axioms transport_append
#print axioms flat_transport_path_independent

end QM.GeodesicTransport
