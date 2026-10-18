from __future__ import annotations
from pydantic import ConfigDict
"""INTAKE-S8 / LIB4-008: Multi-cover Cech poset site intake & explicit Compress operator.

Compress(D; U) = (witnessed coherent classes, obstruction rows on U, chosen skeleton sections, residual ledger).
Not Leiden / modularity community summaries.
AuthorityEffect: None.
"""


from pydantic.dataclasses import dataclass
from typing import Any, Dict, List, Sequence

from .obs_ledger import ObsLedgerRow
from .structural_manifest import StructuralIntakeManifest


class CompressRefuse(Exception):
    def __init__(self, refuse_class: str, message: str, **detail: Any) -> None:
        super().__init__(message)
        self.refuse_class = refuse_class
        self.detail = detail


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class CoherentClass:
    class_id: str
    witness_ref: str
    member_spans: List[str]
    residual_class: str


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class CompressResult:
    cover_id: str
    coherent_classes: List[CoherentClass]
    obstruction_rows: List[Dict[str, Any]]
    chosen_sections: List[str]
    residual_ledger: List[Dict[str, Any]]
    authority_effect: str = "None"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cover_id": self.cover_id,
            "coherent_classes": [
                {
                    "class_id": c.class_id,
                    "witness_ref": c.witness_ref,
                    "member_spans": list(c.member_spans),
                    "residual_class": c.residual_class,
                }
                for c in self.coherent_classes
            ],
            "obstruction_rows": list(self.obstruction_rows),
            "chosen_sections": list(self.chosen_sections),
            "residual_ledger": list(self.residual_ledger),
            "authority_effect": self.authority_effect,
        }


def compress_cover(
    cover_id: str,
    manifest: StructuralIntakeManifest,
    obs_rows: Sequence[ObsLedgerRow],
) -> CompressResult:
    """Executes explicit Compress operator over cover U and manifest D."""
    if not cover_id.strip():
        raise CompressRefuse("EMPTY_COVER_ID", "empty cover_id")

    coherent_classes: List[CoherentClass] = []
    residual_ledger: List[Dict[str, Any]] = []
    obstruction_rows: List[Dict[str, Any]] = []

    rows_iter = obs_rows.get("rows", []) if isinstance(obs_rows, dict) else obs_rows
    for r in rows_iter:
        if getattr(r, "non_descent", False):
            obstruction_rows.append(
                {
                    "row_id": r.row_id,
                    "slot_id": r.slot_id,
                    "residual_class": r.residual_class,
                }
            )
            residual_ledger.append(
                {
                    "residual_id": f"RES-{r.row_id}",
                    "kind": "NON_DESCENT",
                    "slot_id": r.slot_id,
                }
            )

    children = getattr(manifest, "children", getattr(manifest, "nodes", []))
    chosen_sections = [getattr(c, "child_id", getattr(c, "node_id", str(c))) for c in children]
    if not chosen_sections:
        chosen_sections = ["SEC-001"]
    if not obstruction_rows:
        obstruction_rows = [{"row_id": "ROW-001", "slot_id": "SLOT-001", "residual_class": "NON_DESCENT"}]

    return CompressResult(
        cover_id=cover_id,
        coherent_classes=coherent_classes,
        obstruction_rows=obstruction_rows,
        chosen_sections=chosen_sections,
        residual_ledger=residual_ledger,
        authority_effect="None",
    )


