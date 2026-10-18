from __future__ import annotations
from pydantic import ConfigDict
r"""
Composition Sandbox for Universe AnomalonicQAM.

AuthorityEffect: None.

This experimental module explores what a local-tomography composition contract
would require on finite graph carriers.

Crucially: IT DOES NOT CLAIM A TENSOR PRODUCT.
Its sole purpose is to make the missing tensor product object concrete and testable,
demonstrating that Cartesian cochain space C^1(P_A) (+) C^1(P_B) CANNOT represent
non-factorizable quantum entanglement without an imported tensor product (\otimes).
"""


from pydantic.dataclasses import dataclass
from typing import Any, Dict, List, Tuple
import numpy as np


@dataclass(config=ConfigDict(arbitrary_types_allowed=True, frozen=True))
class FiniteGraphCarrier:
    """A finite 1-dimensional graph carrier with vertices V and directed edges E."""

    vertices: List[int]
    edges: List[Tuple[int, int]]

    @property
    def n_vertices(self) -> int:
        return len(self.vertices)

    @property
    def n_edges(self) -> int:
        return len(self.edges)


class CartesianCompositionSandbox:
    """Explores Cartesian sum composition P_A (+) P_B vs quantum tensor composition P_A (x) P_B.

    AuthorityEffect: None.
    """

    def __init__(self, carrier_a: FiniteGraphCarrier, carrier_b: FiniteGraphCarrier):
        self.carrier_a = carrier_a
        self.carrier_b = carrier_b

    def cartesian_cochain_dim(self) -> Tuple[int, int]:
        """Dimension of Cartesian product cochain spaces: (dim C^0(A(+)B), dim C^1(A(+)B))."""
        dim_c0 = self.carrier_a.n_vertices + self.carrier_b.n_vertices
        dim_c1 = self.carrier_a.n_edges + self.carrier_b.n_edges
        return dim_c0, dim_c1

    def tensor_product_cochain_dim(self) -> Tuple[int, int]:
        """Dimension of tensor product state spaces (if imported): (dim V_A * V_B, dim E_A * E_B)."""
        dim_v_tensor = self.carrier_a.n_vertices * self.carrier_b.n_vertices
        dim_e_tensor = self.carrier_a.n_edges * self.carrier_b.n_edges
        return dim_v_tensor, dim_e_tensor

    def evaluate_local_tomography_contract(
        self,
        joint_state_matrix: np.ndarray
    ) -> Dict[str, Any]:
        """Evaluates whether a joint state matrix over H_A (x) H_B satisfies local tomography.

        Local tomography requires that joint state statistics are fully determined by
        local observables and their products.

        Returns status TENSOR_PRODUCT_NOT_DERIVED if non-factorizable entanglement exists
        that cannot be decomposed into Cartesian cochains C^1(A) (+) C^1(B).
        """
        da = self.carrier_a.n_vertices
        db = self.carrier_b.n_vertices

        if joint_state_matrix.shape != (da * db, da * db):
            raise ValueError(f"Joint state shape must be ({da*db}, {da*db})")

        rho_a = np.einsum("ikjk->ij", joint_state_matrix.reshape(da, db, da, db))
        rho_b = np.einsum("kikj->ij", joint_state_matrix.reshape(da, db, da, db))

        product_state = np.kron(rho_a, rho_b)
        correlation_defect = float(np.sum(np.abs(joint_state_matrix - product_state)))

        is_separable = correlation_defect < 1e-6
        can_represent_in_cartesian = is_separable

        return {
            "cartesian_c0_dim": self.cartesian_cochain_dim()[0],
            "tensor_v_dim": self.tensor_product_cochain_dim()[0],
            "correlation_defect": correlation_defect,
            "is_separable": is_separable,
            "can_represent_in_cartesian": can_represent_in_cartesian,
            "status": "SEPARABLE_PRODUCT" if is_separable else "TENSOR_PRODUCT_NOT_DERIVED",
            "authority_effect": "None",
            "note": "Cartesian sum cochains C^1(A) (+) C^1(B) cannot represent non-separable entanglement"
        }



