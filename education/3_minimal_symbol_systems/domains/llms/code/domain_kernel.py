"""
Domain LLMs Generic Kernel Re-export Shim
AuthorityEffect: None
"""

import sys
from pathlib import Path

# Self-registering parent directory resolution for isolated import loaders
_code_dir = str(Path(__file__).resolve().parent)
if _code_dir not in sys.path:
    sys.path.insert(0, _code_dir)

try:
    from .domain_llms_kernel import (
        CausalAttentionDAGReceipt,
        DomainEngine,
        DomainState,
        PrimitiveDifferenceSetting,
        SimplicialBoundaryReceipt,
        TokenSequenceReceipt,
    )
except (ImportError, ValueError):
    from domain_llms_kernel import (
        CausalAttentionDAGReceipt,
        DomainEngine,
        DomainState,
        PrimitiveDifferenceSetting,
        SimplicialBoundaryReceipt,
        TokenSequenceReceipt,
    )

__all__ = [
    "CausalAttentionDAGReceipt",
    "DomainEngine",
    "DomainState",
    "PrimitiveDifferenceSetting",
    "SimplicialBoundaryReceipt",
    "TokenSequenceReceipt",
]
