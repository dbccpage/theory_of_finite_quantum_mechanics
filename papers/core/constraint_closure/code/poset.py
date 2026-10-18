import numpy as np
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Extension:
    """Represents a proposed structural augmentation (e.g., edge subdivision, face addition)."""
    type: str  # 'subdivide', 'face', etc.
    source_edge: Tuple[int, int]
    new_vertices: List[int]
    new_edges: List[Tuple[int, int]]
    new_faces: List[Tuple[int, int, int]]
    cost: float

class Poset:
    """
    Poset geometry data structure with exact L1 coboundary operator.
    """
    def __init__(self, num_vertices: int, edges: List[Tuple[int, int]], faces: List[Tuple[int, int, int]] = None):
        self.num_vertices = num_vertices
        self.edges = edges
        self.faces = faces if faces is not None else []
        self._build_incidence()

    def _build_incidence(self):
        """Constructs the discrete exterior derivative d0 (vertices -> edges)."""
        self.d0 = np.zeros((len(self.edges), self.num_vertices))
        for i, (u, v) in enumerate(self.edges):
            self.d0[i, v] = 1.0
            self.d0[i, u] = -1.0
            
    def coboundary(self, section: np.ndarray) -> np.ndarray:
        """
        Computes the coboundary of the 0-cochain (section).
        delta(s) = d0 * s
        """
        return self.d0 @ section

    def get_admissible_extensions(self, defect: np.ndarray, tolerance: float = 1e-6) -> List[Extension]:
        """
        Generate mathematically allowable topological repairs.
        If an edge has non-zero defect tension, it inherently produces subdivision capacity.
        """
        extensions = []
        for i, edge in enumerate(self.edges):
            tension = abs(defect[i])
            if tension > tolerance:
                # Propose subdivision: u -> w -> v
                v_new = self.num_vertices + len(extensions)
                # Cost is the L1 structural metric (number of new geometric insertions minus old)
                ext = Extension(
                    type="subdivide",
                    source_edge=edge,
                    new_vertices=[v_new],
                    new_edges=[(edge[0], v_new), (v_new, edge[1])],
                    new_faces=[],
                    cost=1.0  # minimal structural cost unit
                )
                extensions.append(ext)
        return extensions
        
    def add_extensions(self, selected_extensions: List[Extension]) -> 'Poset':
        """
        Instantiate a newly augmented topological poset.
        """
        new_v = self.num_vertices
        new_edges = list(self.edges)
        new_faces = list(self.faces)
        
        edges_to_remove = set()
        
        for ext in selected_extensions:
            if ext.type == "subdivide":
                edges_to_remove.add(ext.source_edge)
                # Safely allocate exact new integer index
                mapped_new_v = new_v
                new_v += len(ext.new_vertices)
                # Map tuple logic to fresh vertices
                mapped_edges = [(e[0], mapped_new_v) if e[1] == ext.new_vertices[0] else (mapped_new_v, e[1]) for e in ext.new_edges]
                new_edges.extend(mapped_edges)
                new_faces.extend(ext.new_faces)
                
        final_edges = [e for e in new_edges if e not in edges_to_remove]
        return Poset(num_vertices=new_v, edges=final_edges, faces=new_faces)

    def extract_betti_number(self) -> int:
        """Compute the first Betti number (cyclomatic complexity) β₁."""
        V = self.num_vertices
        E = len(self.edges)
        F = len(self.faces)
        # Euler characteristic chi = V - E + F
        # Assuming path connectedness (b0 = 1).
        chi = V - E + F
        beta_1 = 1 - chi
        return max(0, beta_1)
