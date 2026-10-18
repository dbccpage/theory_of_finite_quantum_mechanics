"""Canonical Witness models for Python (omega_types)."""

from typing import List, Union
from pydantic import BaseModel


class IdentityWitness(BaseModel):
    witness_id: str
    payload_hash: str
    source_layer: str
    target_layer: str
    is_valid: bool


class CriticalContextWitness(BaseModel):
    left_state: str
    right_state: str
    action_context: str
    observation_left: str
    observation_right: str
    is_valid_lift_trigger: bool


class ExactTrichotomyWitness(BaseModel):
    repair_vector: List[float]


class SurvivorTrichotomyWitness(BaseModel):
    duality_certificate: str
    gamma2_mass: float


class OpenTrichotomyWitness(BaseModel):
    phi1_mass: float
    gamma2_mass: float
    unresolved_reason: str


TrichotomyWitness = Union[
    ExactTrichotomyWitness, SurvivorTrichotomyWitness, OpenTrichotomyWitness
]
