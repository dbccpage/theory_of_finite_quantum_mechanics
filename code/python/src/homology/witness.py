"""Cryptographic witnesses and receipts for homology complexes.

Origin: code/python/src/homology/witness.py
Claim: a witness is valid only when d1 d0 is the zero matrix and dim H1 matches rank-nullity.
AuthorityEffect: None. Validity is a recomputation, not a stored flag.
"""
from dataclasses import dataclass

from ..linear_algebra import ExactMatrix
from .carrier import Carrier


@dataclass
class HomologyWitness:
    carrier_hash: str
    dim_q1: int
    dim_h1: int
    is_valid: bool

    @classmethod
    def from_carrier(cls, carrier: Carrier) -> "HomologyWitness":
        product = carrier.d1 * carrier.d0
        zero = ExactMatrix.zeros(product.rows, product.cols)
        rank0 = carrier.d0.rank()
        rank1 = carrier.d1.rank()
        recomputed = (carrier.dim1 - rank1) - rank0
        digest = carrier.sha256()
        nilpotent = product == zero
        return cls(
            carrier_hash=digest,
            dim_q1=carrier.dim1 - rank0,
            dim_h1=recomputed,
            is_valid=nilpotent and recomputed == carrier.dim_h1() and digest == carrier.sha256(),
        )
