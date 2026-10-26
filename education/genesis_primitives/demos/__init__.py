"""Genesis Demos Package.

Demonstrations of the Genesis ontological ascent:
<> -> <a> -> <ara> -> <arb> -> <arb><bra> -> boson/fermion parity ->
presentation -> instance -> regime -> comparison -> eval -> auth.

AuthorityEffect: None.
"""

from __future__ import annotations

from .demo_01_genesis_ascent import run_genesis_ascent_demo
from .demo_02_observer_presheaf_cech_bell import run_observer_presheaf_demo
from .demo_03_regge_cech_curvature import run_regge_cech_curvature_demo
from .demo_04_sheaf_hott_quantum_regge import run_sheaf_hott_quantum_regge_demo

__all__ = [
    "run_genesis_ascent_demo",
    "run_observer_presheaf_demo",
    "run_regge_cech_curvature_demo",
    "run_sheaf_hott_quantum_regge_demo",
]
