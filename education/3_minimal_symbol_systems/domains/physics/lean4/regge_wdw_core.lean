/-! Finite integer gauge and nonnegative-energy identities.
AuthorityEffect: None. No CDT, WDW, sign-problem or supersymmetry theorem. -/
namespace PhysicsNormalForms

structure SimplicialU1GaugeField (num_edges : Nat) where
  theta : Fin num_edges → Int

/-- Local vertex gauge transformation alpha: V -> Int. -/
def LocalGaugeTransformation (num_vertices : Nat) :=
  Fin num_vertices → Int

/-- Plaquette oriented boundary sum:
    On oriented triangle f = (u, v, w) with directed edges e1=(u,v), e2=(v,w), e3=(w,u):
    flux theta_f = theta(e1) + theta(e2) + theta(e3). -/
def plaquette_flux (theta_uv theta_vw theta_wu : Int) : Int :=
  theta_uv + theta_vw + theta_wu

/-- Gauge transformation on an oriented edge (u, v):
    theta'_{uv} = theta_{uv} + alpha_u - alpha_v. -/
def gauge_transform_edge (theta_uv alpha_u alpha_v : Int) : Int :=
  theta_uv + alpha_u - alpha_v

/-- Theorem: Local U(1) gauge invariance of plaquette flux.
    Under arbitrary local gauge rotations alpha_u, alpha_v, alpha_w at vertices of triangle (u,v,w),
    the gauge transformations telescope and cancel identically:
    (theta_uv + alpha_u - alpha_v) + (theta_vw + alpha_v - alpha_w) + (theta_wu + alpha_w - alpha_u)
    = theta_uv + theta_vw + theta_wu. -/
theorem simplicial_u1_gauge_transformation_invariant
    (theta_uv theta_vw theta_wu alpha_u alpha_v alpha_w : Int) :
    gauge_transform_edge theta_uv alpha_u alpha_v +
    gauge_transform_edge theta_vw alpha_v alpha_w +
    gauge_transform_edge theta_wu alpha_w alpha_u =
    plaquette_flux theta_uv theta_vw theta_wu := by
  dsimp [gauge_transform_edge, plaquette_flux]
  omega

/-- Scalar field kinetic Dirichlet contribution on an edge (u, v):
    E_e(phi) = w_e * (diff)^2. -/
def scalar_edge_dirichlet_energy (w_e : Nat) (diff : Nat) : Nat :=
  w_e * (diff * diff)

/-- Theorem: Non-negativity of scalar Dirichlet energy on edge. -/
theorem simplicial_scalar_dirichlet_nonnegative (w_e : Nat) (diff : Nat) :
    scalar_edge_dirichlet_energy w_e diff ≥ 0 :=
  Nat.zero_le _


end PhysicsNormalForms
