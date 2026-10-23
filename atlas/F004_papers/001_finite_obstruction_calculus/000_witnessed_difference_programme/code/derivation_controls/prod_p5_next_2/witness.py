"""Executable witness for PROD-P5-NEXT-2 (WdpCertificationService over validate_claim_map & 21.11 order)."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path


def _ensure_paths() -> Path:
    here = Path(__file__).resolve()
    repo_root = next((p for p in here.parents if (p / ".git").exists()), None)
    if repo_root is None:
        raise FileNotFoundError("repository root not found")
    for candidate in (
        repo_root,
        repo_root
        / "omega_engine_atlas"
        / "coda_atlas"
        / "F004_papers"
        / "001_finite_obstruction_calculus"
        / "000_witnessed_difference_programme"
        / "code",
    ):
        s = str(candidate)
        if s not in sys.path:
            sys.path.insert(0, s)
    return repo_root


_ensure_paths()

from omega_engine_applications.wdp_products.kernel.contracts import TypedRefusal  # noqa: E402
from omega_engine_applications.wdp_products.p5_claim_certification.adapter import (  # noqa: E402
    WdpCertificationService,
)
from omega_engine_applications.wdp_products.p5_claim_certification.contracts import (  # noqa: E402
    ClaimNode,
    EvidencePointers,
    Status,
)


def witness() -> dict[str, object]:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        (tmp_path / "code").mkdir(parents=True, exist_ok=True)
        (tmp_path / "code" / "mod_a.py").write_text("x = 1\n", encoding="utf-8")
        (tmp_path / "tests").mkdir(parents=True, exist_ok=True)
        (tmp_path / "tests" / "test_a.py").write_text("def test_a(): pass\n", encoding="utf-8")

        valid_ev = EvidencePointers(
            prose_statement="sec 4.1",
            claim_ledger_row="WDP-CH04-P01",
            implementation="code/mod_a.py",
            tests="tests/test_a.py",
            formal_theorem="lean4/WitnessedDifference/Exact.lean",
            axiom_or_import_report="none",
            source_revision_and_hash="sha256:abc",
            release_artifact="MANIFEST.sha256",
        )
        missing_file_ev = EvidencePointers(
            prose_statement="sec 4.2",
            claim_ledger_row="WDP-CH04-P02",
            implementation="code/missing_mod.py",
            tests="tests/test_a.py",
            formal_theorem="lean4/WitnessedDifference/Exact.lean",
            axiom_or_import_report="none",
            source_revision_and_hash="sha256:def",
            release_artifact="MANIFEST.sha256",
        )

        c3 = ClaimNode(claim_id="C3", status=Status.PROVED, evidence=valid_ev, depends_on=("C2",))
        c2 = ClaimNode(claim_id="C2", status=Status.PROVED, evidence=valid_ev, depends_on=("C1",))
        c1 = ClaimNode(claim_id="C1", status=Status.PROVED, evidence=missing_file_ev, depends_on=())
        c_ind = ClaimNode(claim_id="C_IND", status=Status.PROVED, evidence=valid_ev, depends_on=())

        service = WdpCertificationService(root=tmp_path)
        recomputed = service.certify((c3, c2, c1, c_ind), changed=("C1",))
        if not isinstance(recomputed, tuple):
            raise RuntimeError("expected tuple of recomputed ClaimNodes")
        by_id = {n.claim_id: n.status.value for n in recomputed}

        return {
            "goal_id": "PROD-P5-NEXT-2",
            "statuses": by_id,
            "authority_effect": recomputed[0].authority_effect,
        }


def refuse_dependency_cycle() -> None:
    ev = EvidencePointers(prose_statement="sec 1")
    a = ClaimNode(claim_id="A", status=Status.PROVED, evidence=ev, depends_on=("B",))
    b = ClaimNode(claim_id="B", status=Status.PROVED, evidence=ev, depends_on=("A",))
    res = WdpCertificationService().certify((a, b), changed=("A",))
    if isinstance(res, TypedRefusal):
        raise ValueError(f"{res.code}: {res.reason}")
