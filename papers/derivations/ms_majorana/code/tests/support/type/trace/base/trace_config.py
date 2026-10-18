"""TraceConfig and TracePaths Value Objects.

Doctrine:
- Value/config objects supplying paths and runtime parameters.
- AuthorityEffect: None.
- emits: [].
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Final

CONTRACT_ID: Final[str] = "urn:omega:evidence:trace_config:v1.0.0"


@dataclass(frozen=True, slots=True)
class TracePaths:
    """Storage location paths configuration value object."""
    trace_dir: str = "traces"
    archive_dir: str = "traces/archive"
    authority_effect: str = "None"


@dataclass(frozen=True, slots=True)
class TraceConfig:
    """Trace subsystem configuration parameters value object."""
    config_id: str = "default_trace_config"
    paths: TracePaths = TracePaths()
    max_trace_size_bytes: int = 104857600
    authority_effect: str = "None"


__all__ = [
    "TracePaths",
    "TraceConfig",
    "CONTRACT_ID",
]
