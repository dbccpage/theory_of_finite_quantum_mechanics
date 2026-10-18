"""Evidence level and ceiling tracking (spine §1.6/1.7).

Provides the 5-rung lattice for EvidenceCeiling.
"""

from typing import Any, Dict


class EvidenceLevel:
    """Ordered evidence level."""

    def __init__(self, level: int, description: str = "") -> None:
        self.level = level
        self.description = description

    def __lt__(self, other: "EvidenceLevel") -> bool:
        return self.level < other.level

    def __le__(self, other: "EvidenceLevel") -> bool:
        return self.level <= other.level

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EvidenceLevel):
            return NotImplemented
        return self.level == other.level

    def __repr__(self) -> str:
        return f"EvidenceLevel({self.level}: {self.description})"


class EvidenceCeiling(str):
    """Evidence routing levels (spine §1.6/1.7).

    5-rung lattice total order:
    ShapeOnly (GrammarOnly) < LocalReplay (SchemaChecked) < BoundaryChecked < ExternalOracleRequired (ExternalOracle) < EmpiricalOracleRequired.
    """

    GRAMMAR_ONLY: "EvidenceCeiling"
    SHAPE_ONLY: "EvidenceCeiling"
    SCHEMA_CHECKED: "EvidenceCeiling"
    LOCAL_REPLAY: "EvidenceCeiling"
    BOUNDARY_CHECKED: "EvidenceCeiling"
    EXTERNAL_ORACLE: "EvidenceCeiling"
    EXTERNAL_ORACLE_REQUIRED: "EvidenceCeiling"
    EMPIRICAL_ORACLE_REQUIRED: "EvidenceCeiling"

    def __new__(cls, val_or_level: Any):
        if isinstance(val_or_level, EvidenceLevel):
            val = val_or_level.description or str(val_or_level.level)
        elif isinstance(val_or_level, EvidenceCeiling):
            val = val_or_level.value
        else:
            val = str(val_or_level)
        obj = str.__new__(cls, val)
        return obj

    def __init__(self, val_or_level: Any) -> None:
        if isinstance(val_or_level, EvidenceLevel):
            self.max_level = val_or_level
            # An explicitly typed numeric level is a deliberate API use,
            # not an unrecognized token: the gates below honor it.
            self._explicit_level = True
        elif isinstance(val_or_level, EvidenceCeiling):
            self.max_level = val_or_level.max_level
            self._explicit_level = getattr(val_or_level, "_explicit_level", False)
        else:
            token = str(val_or_level)
            rank = EVIDENCE_RANK.get(token, 0)
            self.max_level = EvidenceLevel(rank, token)
            # Construction from an unregistered token is permitted (the
            # object can be displayed/serialized) but the three gate
            # functions below refuse it fail-closed (Inspector OD-6/M13).
            self._explicit_level = token in EVIDENCE_RANK

    @property
    def value(self) -> str:
        return str(self)

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: Any) -> Any:
        from pydantic_core import core_schema

        return core_schema.no_info_after_validator_function(
            cls, core_schema.str_schema()
        )


# Total order on the evidence route (spine §1.6 Lemma: this is a total order).
EVIDENCE_RANK: Dict[str, int] = {
    "GrammarOnly": 0,
    "ShapeOnly": 0,
    "SchemaChecked": 1,
    "LocalReplay": 2,
    "BoundaryChecked": 3,
    "ExternalOracle": 4,
    "ExternalOracleRequired": 4,
    "EmpiricalOracleRequired": 5,
}

# Attach members as class attributes to mimic Enum
EvidenceCeiling.GRAMMAR_ONLY = EvidenceCeiling("GrammarOnly")
EvidenceCeiling.SHAPE_ONLY = EvidenceCeiling("ShapeOnly")
EvidenceCeiling.SCHEMA_CHECKED = EvidenceCeiling("SchemaChecked")
EvidenceCeiling.LOCAL_REPLAY = EvidenceCeiling("LocalReplay")
EvidenceCeiling.BOUNDARY_CHECKED = EvidenceCeiling("BoundaryChecked")
EvidenceCeiling.EXTERNAL_ORACLE = EvidenceCeiling("ExternalOracle")
EvidenceCeiling.EXTERNAL_ORACLE_REQUIRED = EvidenceCeiling("ExternalOracleRequired")
EvidenceCeiling.EMPIRICAL_ORACLE_REQUIRED = EvidenceCeiling("EmpiricalOracleRequired")


def evidence_rank(e: Any) -> int:
    """Total-order rank of an evidence route/ceiling — FAIL-CLOSED.

    Law (spine §1.6 total order; Inspector OD-6/M13): only members of the
    registered 5-rung lattice (:data:`EVIDENCE_RANK`) and explicitly typed
    ``EvidenceLevel`` values have a rank. An unknown token used to rank as
    0 silently (fail-open — an unregistered route would pass every gate at
    the bottom rung); it now refuses.

    Typed refusal: ``ValueError`` with token
    ``UNKNOWN_EVIDENCE_TOKEN_REFUSED``.
    """
    if isinstance(e, EvidenceLevel):
        return e.level
    if isinstance(e, EvidenceCeiling):
        # _explicit_level is True for registered tokens (whose max_level
        # equals the table rank by construction) and for deliberately
        # typed EvidenceLevel constructions — both are grounded.
        if getattr(e, "_explicit_level", False):
            return e.max_level.level
    else:
        token = str(e)
        if token in EVIDENCE_RANK:
            return EVIDENCE_RANK[token]
    raise ValueError(
        f"UNKNOWN_EVIDENCE_TOKEN_REFUSED: '{e}' is not a registered "
        f"evidence token (legal: {sorted(EVIDENCE_RANK)}); refusing to "
        f"assign a default rank"
    )


def allowed_evidence(e: Any, ceiling: Any) -> bool:
    """Allowed(e, c) (spine §1.7): route e is within ceiling c.

    Law: total over registered tokens/explicit levels only. Unknown tokens
    refuse via :func:`evidence_rank` (``UNKNOWN_EVIDENCE_TOKEN_REFUSED``)
    instead of silently ranking 0 and passing under every ceiling.
    """
    return evidence_rank(e) <= evidence_rank(ceiling)


def assert_no_ceiling_raise(
    current: EvidenceCeiling, proposed: EvidenceCeiling
) -> None:
    """Enforces that the ceiling cannot be raised — FAIL-CLOSED.

    Law: raises ``ValueError`` when ``proposed`` ranks above ``current``.
    Both arguments must be registered tokens or explicitly typed levels;
    an unknown token refuses via :func:`evidence_rank`
    (``UNKNOWN_EVIDENCE_TOKEN_REFUSED``) rather than comparing at a silent
    default rank.
    """
    if evidence_rank(current) < evidence_rank(proposed):
        raise ValueError(
            f"Evidence ceiling violation: cannot raise ceiling from {current.max_level} to {proposed.max_level}"
        )


class EvidenceScope:
    """Tracks current evidence level against a ceiling."""

    def __init__(self, ceiling: EvidenceCeiling) -> None:
        self.ceiling = ceiling
        self.current_level = EvidenceLevel(0, "No evidence")

    def record_evidence(self, level: EvidenceLevel) -> None:
        """Records a new evidence level, ensuring it does not exceed the ceiling."""
        if self.ceiling.max_level < level:
            raise ValueError(
                f"Evidence level {level} exceeds current ceiling of {self.ceiling.max_level}"
            )
        if self.current_level < level:
            self.current_level = level
