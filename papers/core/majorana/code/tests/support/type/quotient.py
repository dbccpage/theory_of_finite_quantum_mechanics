"""Canonical Quotient models for Python (omega_types)."""

from typing import List
from pydantic import BaseModel


class CongruenceCoreQuotient(BaseModel):
    equivalence_classes: List[List[int]]
    class_map: List[int]
    stabilization_index: int
    num_classes: int
