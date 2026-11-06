"""Finite honeycomb link-sign, plaquette-product and skew-matrix examples.
AuthorityEffect: None.
The historical Kitaev name is a model label. No measured Berry phase, Pfaffian
parity, spin-liquid phase, Majorana zero mode, or braiding certification is provided.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import numpy as np

# Ensure directory is on sys.path
code_dir = Path(__file__).resolve().parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))


@dataclass(frozen=True)
class HoneycombSite:
    site_id: int
    x: int
    y: int
    sublattice: str  # 'A' or 'B'


@dataclass
class HoneycombLink:
    link_id: str
    site_u: int
    site_v: int
    bond_dir: str  # 'X', 'Y', 'Z'
    gauge_u: int  # +1 or -1


@dataclass
class HoneycombPlaquette:
    plaquette_id: str
    center_x: float
    center_y: float
    boundary_links: List[Tuple[str, int]]  # list of (link_id, orientation)
    flux_wp: int = 1  # +1 or -1
    vortex_charge: int = 0  # 0 if flux_wp == 1, 1 if flux_wp == -1


class MockHoneycombGinIndex:
    """
    Generalized Inverted Index (GIN) for 2D Honeycomb Kitaev Lattice.
    Maps link gauge IDs to incident hexagonal plaquettes for O(1) vortex flux auditing.
    """

    def __init__(self, links: Dict[str, HoneycombLink], plaquettes: Dict[str, HoneycombPlaquette]):
        self.links = links
        self.plaquettes = plaquettes
        self.link_to_plaquettes: Dict[str, List[str]] = {}
        self.site_to_links: Dict[int, List[str]] = {}
        self.vortex_postings: Set[str] = set()

        self._build_inverted_index()

    def _build_inverted_index(self) -> None:
        for p_id, p in self.plaquettes.items():
            for link_id, _ in p.boundary_links:
                if link_id not in self.link_to_plaquettes:
                    self.link_to_plaquettes[link_id] = []
                self.link_to_plaquettes[link_id].append(p_id)

        for l_id, link in self.links.items():
            for s in [link.site_u, link.site_v]:
                if s not in self.site_to_links:
                    self.site_to_links[s] = []
                self.site_to_links[s].append(l_id)

        self.recompute_all_fluxes()

    def recompute_all_fluxes(self) -> None:
        self.vortex_postings.clear()
        for p_id, p in self.plaquettes.items():
            prod = 1
            for link_id, orient in p.boundary_links:
                prod *= self.links[link_id].gauge_u ** orient
            p.flux_wp = prod
            p.vortex_charge = 1 if prod == -1 else 0
            if prod == -1:
                self.vortex_postings.add(p_id)

    def flip_link(self, link_id: str) -> None:
        """Flips a link gauge variable u_e -> -u_e and updates incident plaquettes in O(1)."""
        link = self.links[link_id]
        link.gauge_u = -link.gauge_u
        for p_id in self.link_to_plaquettes.get(link_id, []):
            p = self.plaquettes[p_id]
            p.flux_wp = -p.flux_wp
            p.vortex_charge = 1 if p.flux_wp == -1 else 0
            if p.flux_wp == -1:
                self.vortex_postings.add(p_id)
            else:
                self.vortex_postings.discard(p_id)

    def get_vortices(self) -> List[str]:
        return sorted(list(self.vortex_postings))

    def create_vortex_pair(self, path_links: List[str]) -> Tuple[str, str]:
        """Flips gauge links along an open path, creating a pair of vortices at the endpoints."""
        for link_id in path_links:
            self.flip_link(link_id)
        vortices = self.get_vortices()
        if len(vortices) == 2:
            return vortices[0], vortices[1]
        elif len(vortices) > 2:
            return vortices[0], vortices[-1]
        return ("", "")


class KitaevHoneycombModel:
    """
    Constructs a declared finite periodic honeycomb link model.
    """

    def __init__(
        self,
        lattice_id: str = "kitaev_2d_torus",
        lx: int = 3,
        ly: int = 3,
        boundary_condition: str = "TORUS",
        jx: float = 1.0,
        jy: float = 1.0,
        jz: float = 1.0,
        kappa: float = 0.1,  # Declared next-neighbor hopping coefficient; no gap theorem
    ):
        self.lattice_id = lattice_id
        self.lx = lx
        self.ly = ly
        self.boundary_condition = boundary_condition
        self.jx = jx
        self.jy = jy
        self.jz = jz
        self.kappa = kappa

        self.sites: Dict[int, HoneycombSite] = {}
        self.links: Dict[str, HoneycombLink] = {}
        self.plaquettes: Dict[str, HoneycombPlaquette] = {}

        self._build_lattice()
        self.gin_index = MockHoneycombGinIndex(self.links, self.plaquettes)

    def _build_lattice(self) -> None:
        # 2 sites per unit cell: A (sublattice 0) and B (sublattice 1)
        self.lx * self.ly
        for y in range(self.ly):
            for x in range(self.lx):
                cell_idx = y * self.lx + x
                site_a = cell_idx * 2
                site_b = cell_idx * 2 + 1
                self.sites[site_a] = HoneycombSite(site_id=site_a, x=x, y=y, sublattice="A")
                self.sites[site_b] = HoneycombSite(site_id=site_b, x=x, y=y, sublattice="B")

        # Links in unit cell:
        # Z-link: A(x, y) -> B(x, y)
        # X-link: A(x, y) -> B(x-1 mod lx, y)
        # Y-link: A(x, y) -> B(x, y-1 mod ly)
        for y in range(self.ly):
            for x in range(self.lx):
                cell_idx = y * self.lx + x
                u_a = cell_idx * 2
                v_b_z = cell_idx * 2 + 1

                # Z-link
                lz_id = f"link_z_{x}_{y}"
                self.links[lz_id] = HoneycombLink(lz_id, u_a, v_b_z, "Z", 1)

                # X-link: connecting to cell (x-1, y)
                x_prev = (x - 1) % self.lx
                v_b_x = (y * self.lx + x_prev) * 2 + 1
                lx_id = f"link_x_{x}_{y}"
                self.links[lx_id] = HoneycombLink(lx_id, u_a, v_b_x, "X", 1)

                # Y-link: connecting to cell (x, y-1)
                y_prev = (y - 1) % self.ly
                v_b_y = (y_prev * self.lx + x) * 2 + 1
                ly_id = f"link_y_{x}_{y}"
                self.links[ly_id] = HoneycombLink(ly_id, u_a, v_b_y, "Y", 1)

        # Build hexagonal plaquettes: each unit cell (x, y) corresponds to a hexagon
        for y in range(self.ly):
            for x in range(self.lx):
                p_id = f"plaq_{x}_{y}"
                x_prev = (x - 1) % self.lx
                y_prev = (y - 1) % self.ly
                x_next = (x + 1) % self.lx
                y_next = (y + 1) % self.ly

                # 6 boundary links around hexagon (x, y):
                # link_z_{x}_{y}, link_x_{(x+1)%lx}_{y}, link_y_{(x+1)%lx}_{(y+1)%ly},
                # link_z_{(x+1)%lx}_{(y+1)%ly}, link_x_{(x+1)%lx}_{(y+1)%ly}, link_y_{x}_{(y+1)%ly}
                b_links = [
                    (f"link_z_{x}_{y}", 1),
                    (f"link_x_{x_next}_{y}", -1),
                    (f"link_y_{x_next}_{y_next}", 1),
                    (f"link_z_{x_next}_{y_next}", -1),
                    (f"link_x_{x_next}_{y_next}", 1),
                    (f"link_y_{x}_{y_next}", -1),
                ]
                self.plaquettes[p_id] = HoneycombPlaquette(
                    plaquette_id=p_id,
                    center_x=x + 0.5,
                    center_y=y + 0.5,
                    boundary_links=b_links,
                    flux_wp=1,
                    vortex_charge=0,
                )

    def compute_majorana_hamiltonian(self) -> np.ndarray:
        """
        Builds the skew-symmetric quadratic Majorana matter matrix A (size N x N)
        such that H_m = (i/4) sum_{j,k} A_{jk} c_j c_k.
        """
        n = len(self.sites)
        A = np.zeros((n, n), dtype=float)

        # Nearest neighbor hopping with link gauge u_e
        for link in self.links.values():
            j, k = link.site_u, link.site_v
            coupling = (
                self.jz if link.bond_dir == "Z" else (self.jx if link.bond_dir == "X" else self.jy)
            )
            val = coupling * link.gauge_u
            A[j, k] += val
            A[k, j] -= val

        # Second neighbor chiral hopping (time-reversal breaking kappa)
        if abs(self.kappa) > 1e-6:
            for p in self.plaquettes.values():
                # Introduce next-nearest neighbor hopping around the hexagon
                for i in range(len(p.boundary_links)):
                    l1_id, _ = p.boundary_links[i]
                    l2_id, _ = p.boundary_links[(i + 1) % len(p.boundary_links)]
                    l1 = self.links[l1_id]
                    l2 = self.links[l2_id]
                    # Common site between l1 and l2
                    shared = set([l1.site_u, l1.site_v]) & set([l2.site_u, l2.site_v])
                    if shared:
                        mid = list(shared)[0]
                        ends = (set([l1.site_u, l1.site_v]) | set([l2.site_u, l2.site_v])) - {mid}
                        if len(ends) == 2:
                            s1, s2 = list(ends)
                            val = self.kappa * l1.gauge_u * l2.gauge_u
                            A[s1, s2] += val
                            A[s2, s1] -= val

        return A



    def evaluate_state_routing(
        self,
        gauge_projector_valid: bool = True,
        force_parity_flip: bool = False,
    ) -> str:
        """Evaluates overall BQNF terminal routing for current lattice state."""
        if not gauge_projector_valid:
            return "CLOSURE_FAILURE"

        vortex_count = len(self.gin_index.get_vortices())
        if self.boundary_condition == "TORUS" and (vortex_count % 2 != 0):
            return "SPLIT_BRAIN_REFUSAL"

        if force_parity_flip:
            return "SPLIT_BRAIN_REFUSAL"

        return "REPAIR"
