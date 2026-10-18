"""Cryptographic witnesses and receipts for homology complexes."""
from dataclasses import dataclass
from typing import Dict, Any
from .carrier import Carrier

@dataclass
class HomologyWitness:
    carrier_hash: str
    dim_q1: int
    dim_h1: int
    is_valid: bool

    @classmethod
    def from_carrier(cls, carrier: Carrier) -> "HomologyWitness":
        return cls(
            carrier_hash=carrier.sha256(),
            dim_q1=carrier.dim_q1(),
            dim_h1=carrier.dim_h1(),
            is_valid=(carrier.dim_h1() >= 0)
        )
