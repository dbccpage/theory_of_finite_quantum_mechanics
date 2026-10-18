"""Tower Boundary Invariants & Verifiers for GTOC, CODA-FOC, CODA-FDA, GTLA, CODA-MUR, and CODA-A.

Enforces:
1. GTOC Root: Local cut with PrimitiveDifference ⊔ Structure; source grounding required; no genesis-bias imports.
2. Prime 000 Order: Locus -> Carrier -> Observer -> Difference -> ZeroRel -> Witness/Refusal.
3. CODA-FOC Local Verifier: Exact repairs do not discharge open residuals; trichotomy classification (Exact, Open, Refused, BudgetUnknown, NoRule).
4. CODA-FDA Authority End Gate: Authority is an inhabited dependent type requiring a 5-field descent packet (K, E, V, tau, Lambda); terminal status controls authority, not answer text.
5. GTLA Summary Compression: Obligation conservation under summary compression (residual fingerprints, loci, refusal routes, debt statuses cannot be erased).
6. CODA-MUR Transport: Representation transport to target carrier retains loss ledger; target terminalization still mandatory for authority.
7. CODA-A Terminal Disjointness: Residual terminalization (ClosedResidual, OpenResidual, LiftRequired, RefusedClosure) is disjoint from AuthorityTerminal.
"""

from __future__ import annotations
import enum
from collections import Counter
from dataclasses import field
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Set

from .round9 import (
    SourceLocus,
)


class GtfocTerminalClass(str, enum.Enum):
    Exact = "Exact"
    Open = "Open"
    Refused = "Refused"
    BudgetUnknown = "BudgetUnknown"
    NoRule = "NoRule"


@dataclass
class ImportLedgerEntry:
    term_id: str
    term_name: str
    is_priced: bool
    status: str
    source_locus: Optional[SourceLocus] = None


@dataclass
class ImportLedger:
    entries: Dict[str, ImportLedgerEntry] = field(default_factory=dict)

    def add_term(
        self,
        name: str,
        is_priced: bool,
        status: str,
        locus: Optional[SourceLocus] = None,
    ) -> None:
        self.entries[name] = ImportLedgerEntry(
            term_id=f"imp_{name}",
            term_name=name,
            is_priced=is_priced,
            status=status,
            source_locus=locus,
        )

    def check_unpriced_imports(self) -> None:
        unpriced = [e.term_name for e in self.entries.values() if not e.is_priced]
        if unpriced:
            raise ValueError(
                f"NO_UNPRICED_IMPORT_REFUSAL: unpriced load-bearing terms detected {sorted(unpriced)}"
            )


@dataclass
class GtocCut:
    cut_id: str
    raw_prompt_hash: str
    primitive_differences: List[Dict[str, str]]
    retained_structure: Dict[str, Any]
    authority_effect: str = "None"

    def validate_grounding(self) -> None:
        for diff in self.primitive_differences:
            locus = diff.get("source_locus")
            if not locus or not isinstance(locus, dict) or not locus.get("span_text"):
                raise ValueError(
                    "REFUSED_UNGROUNDED_LOCUS: obstruction lacks retained textual locus"
                )


@dataclass
class GtfdaDescentPacket:
    carrier_k: str
    candidate_class_e: str
    verifier_evidence_v: str
    terminalizer_tau: str
    lift_discipline_lambda: str
    authority_effect: str = "None"


def validate_gtfda_authority(
    answer_text: str,
    descent_packet: Optional[GtfdaDescentPacket],
    claimed_authority: str,
) -> str:
    """Validate CODA-FDA authority gate. Returns R_nopacket if descent packet is missing or claimed authority is unauthorized."""
    if not descent_packet:
        if claimed_authority != "None":
            raise ValueError(
                "R_nopacket: authority claimed without finite descent packet"
            )
        return "R_nopacket"

    if claimed_authority == "Certified" and descent_packet.authority_effect == "None":
        raise ValueError(
            "R_nopacket: certified authority claims require certified descent packet"
        )

    return "DESCENT_PACKET_VALID"


def validate_prime000_declaration_order(declaration_sequence: List[str]) -> None:
    """Verify Prime 000 declaration order: locus -> carrier -> observer -> difference -> zero_rel -> witness."""
    expected_rank = {
        "source_locus": 1,
        "carrier": 2,
        "observer": 3,
        "primitive_difference": 4,
        "zero_rel": 5,
        "witness_or_refusal": 6,
    }
    last_rank = 0
    for item in declaration_sequence:
        rank = expected_rank.get(item, 99)
        if rank < last_rank:
            raise ValueError(
                f"REFUSE_DECLARATION_ORDER: '{item}' declared before precursor in Prime 000 order"
            )
        last_rank = rank


def validate_gtfoc_exact_repair_isolation(
    repaired_packet_family: str, open_packet_families: List[str], claimed_terminal: str
) -> None:
    """Fixing a typo (exact repair) must not discharge open model/unit/parameter residuals."""
    if open_packet_families and claimed_terminal == "LOCAL_GREEN":
        raise ValueError(
            f"LOCAL_GREEN_REFUSED_GLOBAL_RESIDUAL_PRESENT: exact repair of '{repaired_packet_family}' "
            f"cannot discharge open residuals {sorted(open_packet_families)}"
        )


def classify_gtfoc_trichotomy(
    packet_family: str, is_repaired: bool, is_missing_fields: bool
) -> GtfocTerminalClass:
    """Classify diagnostic packet into CODA-FOC trichotomy terminal class."""
    if is_repaired and not is_missing_fields:
        return GtfocTerminalClass.Exact
    if is_missing_fields:
        return GtfocTerminalClass.Open
    return GtfocTerminalClass.Refused


def validate_gtla_summary_compression(
    original_fingerprints: Set[str],
    original_refusal_routes: Set[str],
    compressed_fingerprints: Set[str],
    compressed_refusal_routes: Set[str],
) -> None:
    """GTLA Obligation Conservation: summary compression cannot erase residual fingerprints or refusal routes.

    NOTE (Inspector M11): this check is SET-based — a compression that
    keeps one copy of a fingerprint while dropping duplicates
    (multiplicity laundering) is invisible to it. Use
    :func:`validate_gtla_summary_compression_multiset` when obligation
    MULTIPLICITY is load-bearing. Kept unchanged for existing callers.
    """
    missing_fps = original_fingerprints - compressed_fingerprints
    missing_routes = original_refusal_routes - compressed_refusal_routes
    if missing_fps or missing_routes:
        raise ValueError(
            f"OBLIGATION_COMPRESSION_LAUNDERING_REFUSED: compression dropped obligations "
            f"fingerprints_missing={sorted(list(missing_fps))}, routes_missing={sorted(list(missing_routes))}"
        )


def validate_gtla_summary_compression_multiset(
    original_fingerprints: Iterable[str],
    original_refusal_routes: Iterable[str],
    compressed_fingerprints: Iterable[str],
    compressed_refusal_routes: Iterable[str],
) -> None:
    """GTLA Obligation Conservation, MULTISET form (Inspector M11).

    Law: summary compression must conserve each residual fingerprint and
    refusal route WITH multiplicity (``collections.Counter`` semantics).
    Dropping a duplicate occurrence — keeping one copy of an obligation
    that the original carried twice — is multiplicity laundering and
    refuses exactly like erasing it.

    Typed refusal: ``ValueError`` with token
    ``OBLIGATION_COMPRESSION_LAUNDERING_REFUSED_MULTIPLICITY`` listing
    every dropped item as ``item x missing_count``.

    Extra copies in the compressed summary are NOT refused here — the law
    conserves obligations downward; duplication adds no discharge.
    AuthorityEffect: None.
    """
    fp_missing = Counter(original_fingerprints) - Counter(compressed_fingerprints)
    route_missing = Counter(original_refusal_routes) - Counter(
        compressed_refusal_routes
    )
    if fp_missing or route_missing:
        fp_report = [f"{item} x{count}" for item, count in sorted(fp_missing.items())]
        route_report = [
            f"{item} x{count}" for item, count in sorted(route_missing.items())
        ]
        raise ValueError(
            f"OBLIGATION_COMPRESSION_LAUNDERING_REFUSED_MULTIPLICITY: compression "
            f"dropped obligation multiplicity "
            f"fingerprints_missing={fp_report}, routes_missing={route_report}"
        )


def validate_gtmur_target_authority(
    has_transport_receipt: bool,
    has_loss_ledger: bool,
    target_terminalized: bool,
    claimed_target_authority: str,
) -> str:
    """CODA-MUR representation transport: transport receipt + loss ledger does not create target authority without target terminalization."""
    if claimed_target_authority != "None" and not target_terminalized:
        raise ValueError(
            "TARGET_TERMINALIZATION_REQUIRED: transport receipt and loss ledger do not imply target authority without target terminalization"
        )
    return (
        "TARGET_TERMINALIZATION_REQUIRED"
        if not target_terminalized
        else "TRANSPORT_AUTHORITY_VALID"
    )


def validate_gtta_terminal_disjointness(
    terminal_status: str, claimed_authority_effect: str
) -> None:
    """CODA-A Disjointness: residual terminals (ClosedResidual, OpenResidual, TERMINAL_WITH_DEBT) are disjoint from AuthorityTerminal."""
    residual_terminals = {
        "ClosedResidual",
        "OpenResidual",
        "TERMINAL_WITH_DEBT",
        "RefusedClosure",
        "LiftRequired",
    }
    if (
        terminal_status in residual_terminals
        and claimed_authority_effect == "Certified"
    ):
        raise ValueError(
            f"RESIDUAL_AUTHORITY_LAUNDERING_REFUSED: residual terminal status '{terminal_status}' is disjoint from AuthorityTerminal"
        )



