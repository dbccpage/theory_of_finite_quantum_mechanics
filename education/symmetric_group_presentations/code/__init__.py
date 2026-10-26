"""S(n) Tower Architecture Pedagogical and Verification Code Package.

Source models and headless test harness for the 30 S(n) curriculum notebooks.
AuthorityEffect: None.
"""

from __future__ import annotations

from .sn_applications import (
    DownstreamApplication,
    ReggeCurvature,
    ReggeMetric,
    SessionChannel,
    topological_relational_join,
)
from .sn_core import (
    S0Ground,
    S1Supply,
    S2Collapse,
    S3Separation,
    S4Orbit,
    S5Continuation,
    S6Descent,
)
from .sn_realizations import (
    AdjunctionCochain,
    AutopoieticAudit,
    DaggerArrow,
    DialectProjection,
    DiscreteHodge,
    FilteredIndObject,
    HashimotoGraph,
    Polygraph2,
    RGBChannel,
    Simplex1,
    Simplicial1Skeleton,
    authority_filter,
    bounded_exists,
    bounded_forall,
    debruijn_shift,
    irreflexive_cut,
)
from .sn_verification import (
    AlternationMonitor,
    DDAEventRecord,
    Kleene3Logic,
    VerificationRGBFirewall,
)

__all__ = [
    "S0Ground",
    "S1Supply",
    "S2Collapse",
    "S3Separation",
    "S4Orbit",
    "S5Continuation",
    "S6Descent",
    "Simplex1",
    "Simplicial1Skeleton",
    "irreflexive_cut",
    "bounded_forall",
    "bounded_exists",
    "Polygraph2",
    "AdjunctionCochain",
    "DaggerArrow",
    "debruijn_shift",
    "authority_filter",
    "RGBChannel",
    "FilteredIndObject",
    "DialectProjection",
    "DiscreteHodge",
    "HashimotoGraph",
    "AutopoieticAudit",
    "topological_relational_join",
    "SessionChannel",
    "DownstreamApplication",
    "ReggeMetric",
    "ReggeCurvature",
    "AlternationMonitor",
    "DDAEventRecord",
    "Kleene3Logic",
    "VerificationRGBFirewall",
]
