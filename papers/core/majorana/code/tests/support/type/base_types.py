from pydantic import ConfigDict
"""Data-only base containers."""

from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class PresheafCoboundaryData:
    """Serialization DTO carrying presheaf coboundary inputs.

    Data-only transport object: it MUST NOT carry methods, validation, or
    authority. It only holds the node/edge/gauge payload for (de)serialization
    and hand-off between layers.
    """

    nodes: List[str]
    edges: List[Tuple[str, str]]
    gauge: Dict[Tuple[str, str], float] = field(default_factory=dict)



