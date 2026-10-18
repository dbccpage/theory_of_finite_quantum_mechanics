"""Unified Carrier Subsystem Factory and Adapters.

Conforms to urn:omega:state:carrier:v1.0.0.
Collapses fragmented carrier topology definitions across coda/ and codaq/
onto standardized CarrierArtifact and CheckedCarrierArtifact records.
"""

from __future__ import annotations
import hashlib
import json
from typing import Any, Dict, List, Optional, Tuple, Sequence
from sympy import Matrix

try:
    from omega_engine.crates.carrier.carrier import CarrierArtifact, CheckedCarrierArtifact
except ImportError:
    from .carrier import CarrierArtifact, CheckedCarrierArtifact


class CarrierFactory:
    """Factory to build and check CarrierArtifact records from graph/simplicial specifications."""

    @staticmethod
    def create_carrier(
        carrier_id: str,
        carrier_kind: str,
        nodes: Sequence[Any],
        edges: Sequence[Tuple[Any, Any]],
        faces: Optional[Sequence[Tuple[Any, Any, Any]]] = None,
        context_family: str = "StandardSimplicial",
    ) -> CheckedCarrierArtifact:
        nodes_list = sorted(list(nodes))
        edges_list = list(edges)
        faces_list = list(faces) if faces else []

        node_map = {n: i for i, n in enumerate(nodes_list)}
        edge_map = {e: i for i, e in enumerate(edges_list)}

        d0_mat = Matrix.zeros(len(edges_list), len(nodes_list))
        for e_idx, (u, v) in enumerate(edges_list):
            d0_mat[e_idx, node_map[v]] = 1
            d0_mat[e_idx, node_map[u]] = -1

        if not faces_list:
            d1_mat = Matrix.zeros(1, len(edges_list))
        else:
            d1_mat = Matrix.zeros(len(faces_list), len(edges_list))
            for f_idx, (u, v, w) in enumerate(faces_list):
                for (e_u, e_v), sign in [((u, v), 1), ((v, w), 1), ((u, w), -1)]:
                    if (e_u, e_v) in edge_map:
                        d1_mat[f_idx, edge_map[(e_u, e_v)]] += sign
                    elif (e_v, e_u) in edge_map:
                        d1_mat[f_idx, edge_map[(e_v, e_u)]] -= sign

        composition = d1_mat * d0_mat
        is_valid_chain_law = bool(composition == Matrix.zeros(d1_mat.rows, d0_mat.cols))

        schema_payload = {"carrier_id": carrier_id, "kind": carrier_kind, "nodes": len(nodes_list), "edges": len(edges_list)}
        carrier_hash = hashlib.sha256(json.dumps(schema_payload, sort_keys=True).encode("utf-8")).hexdigest()

        artifact = CarrierArtifact(
            carrier_id=carrier_id,
            carrier_kind=carrier_kind,
            c0_ref=f"C0[{len(nodes_list)}]",
            c1_ref=f"C1[{len(edges_list)}]",
            c2_ref=f"C2[{len(faces_list)}]",
            d0_ref=f"d0[{d0_mat.rows}x{d0_mat.cols}]",
            d1_ref=f"d1[{d1_mat.rows}x{d1_mat.cols}]",
            admissible_repair_set="GaugeShift_d0",
            context_family=context_family,
            coefficient_semantics="IntegralZ",
            schema_hash="omega.contract.v1",
            carrier_hash=carrier_hash,
            chain_law_witness="d1*d0==0" if is_valid_chain_law else "d1*d0!=0",
            authority_effect="EvidenceOnly",
        )

        return CheckedCarrierArtifact(
            artifact=artifact,
            is_valid_chain_law=is_valid_chain_law,
            authority_effect="FactOnly" if is_valid_chain_law else "EvidenceOnly",
        )


__all__ = [
    "CarrierFactory",
]


