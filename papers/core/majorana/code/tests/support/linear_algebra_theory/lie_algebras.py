import math
import numpy as np
from typing import List, Dict


class MultiChannelSymmetry:
    """
    S6: Generates representations of coupled transport matrices and verifies
    Lie algebra closures.
    """

    sigma_1 = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma_3 = np.array([[1, 0], [0, -1]], dtype=complex)

    @classmethod
    def get_su2_generators(cls) -> List[np.ndarray]:
        return [0.5j * cls.sigma_1, 0.5j * cls.sigma_2, 0.5j * cls.sigma_3]

    @staticmethod
    def commutator(A: np.ndarray, B: np.ndarray) -> np.ndarray:
        return A @ B - B @ A

    @classmethod
    def verify_su2_closure(cls) -> Dict:
        G = cls.get_su2_generators()
        comm_01 = cls.commutator(G[0], G[1])
        comm_12 = cls.commutator(G[1], G[2])
        comm_20 = cls.commutator(G[2], G[0])

        c01_match = np.allclose(comm_01, -G[2])
        c12_match = np.allclose(comm_12, -G[0])
        c20_match = np.allclose(comm_20, -G[1])

        return {
            "G1_G2_closure": c01_match,
            "G2_G3_closure": c12_match,
            "G3_G1_closure": c20_match,
            "all_closed": c01_match and c12_match and c20_match,
        }

    @staticmethod
    def get_su3_generators() -> List[np.ndarray]:
        l1 = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex)
        l2 = np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex)
        l3 = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex)
        l4 = np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex)
        l5 = np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex)
        l6 = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
        l7 = np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex)
        l8 = np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex) / math.sqrt(3)
        return [0.5j * lamb for lamb in [l1, l2, l3, l4, l5, l6, l7, l8]]

    @classmethod
    def verify_su3_closure(cls) -> bool:
        G = cls.get_su3_generators()
        for a in range(8):
            for b in range(8):
                cab = cls.commutator(G[a], G[b])
                reconstructed = np.zeros((3, 3), dtype=complex)
                for c in range(8):
                    coeff = -2.0 * np.trace(cab @ G[c])
                    reconstructed += coeff * G[c]
                if not np.allclose(cab, reconstructed, atol=1e-10):
                    return False
        return True

    @staticmethod
    def build_coupled_transport(n_nodes: int, G_a: np.ndarray) -> np.ndarray:
        I_N = np.eye(n_nodes)
        return np.kron(I_N, G_a)

