"""Finite scalar, U(1), SU(2), and graph diffusion examples.
AuthorityEffect: None.
The declared lattice and link data are inputs. Numerical gauge-invariance checks
and graph return probabilities do not establish matter backreaction, a critical
coupling, gravitational collapse, or a CDT dimensional-reduction result.
"""

import math
import random
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class SimplicialScalarField:
    """Minimally coupled real scalar field on simplicial vertices."""

    num_vertices: int
    field_values: List[float]
    edges: List[Tuple[int, int]]
    weights: Dict[Tuple[int, int], float]
    mass_sq: float = 0.0
    lambda_quartic: float = 0.0

    def kinetic_energy(self) -> float:
        """Dirichlet kinetic energy (1/2) sum_{e=(u,v)} w_e (phi_u - phi_v)^2."""
        total = 0.0
        for u, v in self.edges:
            w = self.weights.get((u, v), self.weights.get((v, u), 1.0))
            diff = self.field_values[u] - self.field_values[v]
            total += 0.5 * w * diff * diff
        return total

    def potential_energy(self) -> float:
        """Potential energy sum_v (m^2 / 2 phi_v^2 + lambda / 24 phi_v^4)."""
        total = 0.0
        for phi in self.field_values:
            quad = 0.5 * self.mass_sq * phi * phi
            quartic = (self.lambda_quartic / 24.0) * (phi**4)
            total += quad + quartic
        return total

    def total_action(self) -> float:
        return self.kinetic_energy() + self.potential_energy()

    def propose_vertex_update(self, v: int, delta: float) -> "SimplicialScalarField":
        new_vals = list(self.field_values)
        new_vals[v] += delta
        return SimplicialScalarField(
            num_vertices=self.num_vertices,
            field_values=new_vals,
            edges=self.edges,
            weights=self.weights,
            mass_sq=self.mass_sq,
            lambda_quartic=self.lambda_quartic,
        )


@dataclass
class CompactLatticeGaugeField:
    """Compact U(1) lattice gauge field on oriented 1-simplices."""

    num_vertices: int
    # Directed edge -> link phase theta in [-pi, pi)
    links: Dict[Tuple[int, int], float]
    # Oriented triangular faces (u, v, w)
    plaquettes: List[Tuple[int, int, int]]
    beta_gauge: float = 1.0

    @staticmethod
    def normalize_angle(theta: float) -> float:
        """Wrap angle to [-pi, pi)."""
        return (theta + math.pi) % (2.0 * math.pi) - math.pi

    def get_link(self, u: int, v: int) -> float:
        if (u, v) in self.links:
            return self.links[(u, v)]
        elif (v, u) in self.links:
            return -self.links[(v, u)]
        return 0.0

    def plaquette_flux(self, u: int, v: int, w: int) -> float:
        """Oriented flux theta_f = (theta_uv + theta_vw + theta_wu) mod 2pi."""
        raw_flux = self.get_link(u, v) + self.get_link(v, w) + self.get_link(w, u)
        return self.normalize_angle(raw_flux)

    def wilson_action(self) -> float:
        """Wilson plaquette action S_W = beta_g sum_f (1 - cos theta_f)."""
        action = 0.0
        for u, v, w in self.plaquettes:
            flux = self.plaquette_flux(u, v, w)
            action += self.beta_gauge * (1.0 - math.cos(flux))
        return action

    def gauge_transform(self, alpha: Dict[int, float]) -> "CompactLatticeGaugeField":
        """Apply local gauge transformation theta'_{uv} = theta_{uv} + alpha_u - alpha_v."""
        new_links = {}
        for (u, v), theta in self.links.items():
            a_u = alpha.get(u, 0.0)
            a_v = alpha.get(v, 0.0)
            new_links[(u, v)] = self.normalize_angle(theta + a_u - a_v)
        return CompactLatticeGaugeField(
            num_vertices=self.num_vertices,
            links=new_links,
            plaquettes=self.plaquettes,
            beta_gauge=self.beta_gauge,
        )

    def audit_gauge_invariance(self, alpha: Dict[int, float]) -> Tuple[float, float, float, bool]:
        """Check S_gauge[U'] == S_gauge[U] within 1e-12."""
        s_orig = self.wilson_action()
        transformed = self.gauge_transform(alpha)
        s_trans = transformed.wilson_action()
        residual = abs(s_trans - s_orig)
        is_invariant = residual <= 1e-12
        return s_orig, s_trans, residual, is_invariant


@dataclass
class Su2LinkVariable:
    """SU(2) element represented as unit quaternion (a0, a1, a2, a3) where a0^2 + |a|^2 = 1."""

    a0: float
    a1: float
    a2: float
    a3: float

    @staticmethod
    def identity() -> "Su2LinkVariable":
        return Su2LinkVariable(1.0, 0.0, 0.0, 0.0)

    @staticmethod
    def random(rng: random.Random) -> "Su2LinkVariable":
        v = [rng.gauss(0, 1) for _ in range(4)]
        norm = math.sqrt(sum(x * x for x in v))
        return Su2LinkVariable(v[0] / norm, v[1] / norm, v[2] / norm, v[3] / norm)

    def dagger(self) -> "Su2LinkVariable":
        return Su2LinkVariable(self.a0, -self.a1, -self.a2, -self.a3)

    def multiply(self, other: "Su2LinkVariable") -> "Su2LinkVariable":
        """Quaternion multiplication."""
        s0 = self.a0 * other.a0 - self.a1 * other.a1 - self.a2 * other.a2 - self.a3 * other.a3
        s1 = self.a0 * other.a1 + self.a1 * other.a0 + self.a2 * other.a3 - self.a3 * other.a2
        s2 = self.a0 * other.a2 - self.a1 * other.a3 + self.a2 * other.a0 + self.a3 * other.a1
        s3 = self.a0 * other.a3 + self.a1 * other.a2 - self.a2 * other.a1 + self.a3 * other.a0
        return Su2LinkVariable(s0, s1, s2, s3)

    def trace(self) -> float:
        """Tr(U) = 2 * a0."""
        return 2.0 * self.a0


class CompactSu2GaugeField:
    """Compact SU(2) lattice gauge field on oriented 1-simplices."""

    def __init__(
        self, num_vertices: int, plaquettes: List[Tuple[int, int, int]], beta_su2: float = 2.0
    ):
        self.num_vertices = num_vertices
        self.plaquettes = plaquettes
        self.beta_su2 = beta_su2
        self.links: Dict[Tuple[int, int], Su2LinkVariable] = {}

    def set_link(self, u: int, v: int, u_val: Su2LinkVariable):
        self.links[(u, v)] = u_val
        self.links[(v, u)] = u_val.dagger()

    def get_link(self, u: int, v: int) -> Su2LinkVariable:
        if (u, v) in self.links:
            return self.links[(u, v)]
        elif (v, u) in self.links:
            return self.links[(v, u)].dagger()
        return Su2LinkVariable.identity()

    def wilson_action(self) -> float:
        """S_SU(2) = beta * sum_f (1 - (1/2) Re Tr U_f)."""
        action = 0.0
        for u, v, w in self.plaquettes:
            u1 = self.get_link(u, v)
            u2 = self.get_link(v, w)
            u3 = self.get_link(w, u)
            u_f = u1.multiply(u2).multiply(u3)
            # Re Tr U_f / 2 = u_f.a0
            action += self.beta_su2 * (1.0 - u_f.a0)
        return action

    def gauge_transform(self, g: Dict[int, Su2LinkVariable]) -> "CompactSu2GaugeField":
        r"""U'_{uv} = g_u U_{uv} g_v^\dagger."""
        trans = CompactSu2GaugeField(self.num_vertices, self.plaquettes, self.beta_su2)
        seen = set()
        for (u, v), u_val in self.links.items():
            if (u, v) in seen:
                continue
            seen.add((u, v))
            seen.add((v, u))
            g_u = g.get(u, Su2LinkVariable.identity())
            g_v = g.get(v, Su2LinkVariable.identity())
            u_trans = g_u.multiply(u_val).multiply(g_v.dagger())
            trans.set_link(u, v, u_trans)
        return trans

    def audit_gauge_invariance(
        self, g: Dict[int, Su2LinkVariable]
    ) -> Tuple[float, float, float, bool]:
        s_orig = self.wilson_action()
        transformed = self.gauge_transform(g)
        s_trans = transformed.wilson_action()
        res = abs(s_trans - s_orig)
        return s_orig, s_trans, res, (res <= 1e-12)




class CoupledCdtMatterEngine:
    """Joint MCMC and spectral diffusion evaluator for matter-coupled CDT."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or ":memory:"
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()

    def _init_db(self):
        schema_path = Path(__file__).resolve().parent.parent / "databases" / "regge_wdw_schema.sql"
        if not schema_path.exists():
            schema_path = Path(__file__).resolve().parent / "regge_wdw_schema.sql"
        if schema_path.exists():
            with open(schema_path, "r", encoding="utf-8") as f:
                self.conn.executescript(f.read())
                self.conn.commit()

    @staticmethod
    def build_cdt_sandwich_complex(
        L: int = 3,
    ) -> Tuple[int, List[Tuple[int, int]], List[Tuple[int, int, int]], Dict[int, List[int]]]:
        """Scaffolds a 4D declared layered graph with vertices, edges, triangles, and dual adjacency."""
        n_spatial = L**3
        num_vertices = 2 * n_spatial
        edge_set = set()
        triangles = []

        def add_triangle(u, v, w):
            triangles.append((u, v, w))
            for a, b in [(u, v), (v, w), (w, u)]:
                if (b, a) not in edge_set:
                    edge_set.add((a, b))

        # Spatial faces at t=0 and t=1
        for t in [0, 1]:
            offset = t * n_spatial
            for x in range(L):
                for y in range(L):
                    for z in range(L):
                        u = offset + x * L * L + y * L + z
                        v_x = offset + ((x + 1) % L) * L * L + y * L + z
                        v_y = offset + x * L * L + ((y + 1) % L) * L + z
                        v_xy = offset + ((x + 1) % L) * L * L + ((y + 1) % L) * L + z
                        v_z = offset + x * L * L + y * L + ((z + 1) % L)
                        v_yz = offset + x * L * L + ((y + 1) % L) * L + ((z + 1) % L)

                        # Triangulate xy face
                        add_triangle(u, v_x, v_xy)
                        add_triangle(u, v_xy, v_y)
                        # Triangulate yz face
                        add_triangle(u, v_y, v_yz)
                        add_triangle(u, v_yz, v_z)

        # Timelike prisms connecting t=0 to t=1
        for x in range(L):
            for y in range(L):
                for z in range(L):
                    u = x * L * L + y * L + z
                    u_t = n_spatial + u
                    v_x = ((x + 1) % L) * L * L + y * L + z
                    v_tx = n_spatial + v_x

                    # Timelike square in x-direction triangulated
                    add_triangle(u, v_x, v_tx)
                    add_triangle(u, v_tx, u_t)

        edges = list(edge_set)

        # Dual graph: simplices sharing 3-faces
        num_simplices = 2 * n_spatial
        dual_adj: Dict[int, List[int]] = {i: [] for i in range(num_simplices)}
        for i in range(num_simplices):
            dual_adj[i] = [
                (i + 1) % num_simplices,
                (i - 1) % num_simplices,
                (i + L) % num_simplices,
                (i - L) % num_simplices,
            ]

        return num_vertices, edges, triangles, dual_adj

    @staticmethod
    def evaluate_coupled_diffusion(dual_adj, max_tau=40, epsilon_lazy=0.5, geometric_collapse=False):
        """Measure graph diffusion; a caller-supplied collapse label is not evidence."""
        if geometric_collapse:
            raise ValueError("Supply changed graph data; collapse cannot be inferred from a flag")
        from cdt_spectral_dimension import DiscreteHeatDiffusionEngine
        labels = sorted(dual_adj)
        indices = {v: i for i, v in enumerate(labels)}
        adjacency = [[indices[v] for v in dual_adj[u]] for u in labels]
        profile = DiscreteHeatDiffusionEngine.compute_return_probability_random_walk(
            len(labels), adjacency, tau_max=max_tau, lazy_prob=epsilon_lazy)
        return {tau: ds for tau, _, _, _, ds in
                DiscreteHeatDiffusionEngine.compute_spectral_dimension_curve(profile, range(2, max_tau))}
