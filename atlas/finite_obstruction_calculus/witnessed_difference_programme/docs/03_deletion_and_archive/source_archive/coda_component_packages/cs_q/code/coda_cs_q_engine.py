"""
coda_cs_q_engine.py: Thin Backwards-Compatible Façade for CODA-CS-Q.

Re-exports core classes from `coda_cs_q_bridge_core.py`.
Does not duplicate class definitions or execute side-effects.

AuthorityEffect: None.
"""

from __future__ import annotations

from typing import Any

from coda_cs_q_bridge_core import (
    BRIDGE_ADMISSIBLE_8_STEPS,
    BRIDGE_PACKET_14_SCHEMA_FIELDS,
    BridgePacketCore,
    BridgeResidualTaxonomy,
    CofinalShadowTower,
    GeneratorSemigroupAdapter,
    HigherQueryFamily,
    ImagePoint,
    NamedTerminalizers,
    ProfileFactorizationSolver,
    ProfileFiberQuotient,
    QueryProbe,
    ShadowNode,
    _validate_exact_int,
    _validate_exact_rational,
    compute_transition_quotient_obstruction,
    reproduce_section_0_worked_example,
    terminals_agree,
)

# Backwards compatibility alias for historical packet name
BridgePacket14Tuple = BridgePacketCore


def run_coda_cs_q_bridge_demo() -> dict[str, Any]:
    """Runs the canonical section 0 worked example demonstration."""
    return reproduce_section_0_worked_example()


def run_engine_selfcheck() -> bool:
    """Quick diagnostic verifying that core worked example executes cleanly."""
    res = reproduce_section_0_worked_example()
    return bool(res["is_admissible"] and res["is_cochain_exact"])


run_gttc_q_bridge_demo = run_coda_cs_q_bridge_demo


__all__ = [
    "BRIDGE_ADMISSIBLE_8_STEPS",
    "BRIDGE_PACKET_14_SCHEMA_FIELDS",
    "BridgePacket14Tuple",
    "BridgePacketCore",
    "BridgeResidualTaxonomy",
    "CofinalShadowTower",
    "GeneratorSemigroupAdapter",
    "HigherQueryFamily",
    "ImagePoint",
    "NamedTerminalizers",
    "ProfileFactorizationSolver",
    "ProfileFiberQuotient",
    "QueryProbe",
    "ShadowNode",
    "_validate_exact_int",
    "_validate_exact_rational",
    "compute_transition_quotient_obstruction",
    "reproduce_section_0_worked_example",
    "run_coda_cs_q_bridge_demo",
    "run_engine_selfcheck",
    "run_gttc_q_bridge_demo",
    "terminals_agree",
]
