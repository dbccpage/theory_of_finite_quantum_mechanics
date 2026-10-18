"""Cochains over exact fields."""
from dataclasses import dataclass
from typing import List
from ..linear_algebra import Q

@dataclass
class Cochain:
    dim: int
    coefficients: List[Q]
