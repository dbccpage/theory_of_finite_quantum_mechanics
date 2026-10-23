"""Configuration, estate metadata, and path constants for E2E Verification Suite.

AuthorityEffect: None.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path


ESTATE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = Path(__file__).resolve().parents[4]

PO000_DIR = ESTATE_ROOT / "000_projection_obstruction"
PO001_DIR = ESTATE_ROOT / "001_from_covering_edge_descent_complexes_to_functorial_presheaves_and_coherence_defects"
PO006_DIR = ESTATE_ROOT / "006_vector_and_quantum_observer_geometries"
PO007_DIR = ESTATE_ROOT / "007_m_compatible_gauge_classification"
PO008_DIR = ESTATE_ROOT / "008_so_k_invariant_gauge_classification"
PO009_DIR = ESTATE_ROOT / "009_coordinate_wise_additivity"
PO033_DIR = ESTATE_ROOT / "033_certified_adaptive_quantum_dynamics"
PO034_DIR = ESTATE_ROOT / "034_higher_cell_cochain_projection_and_retraction_dynamics"
PO035_DIR = ESTATE_ROOT / "035_zero_container_relational_spacetime_and_witness_holonomy"


@dataclass(frozen=True)
class PackageSpec:
    pkg_id: str
    name: str
    path: Path
    manuscript_name: str
    pytest_command: list[str]
    deposit_verifier_command: list[str]
    manifest_names: list[str] = field(default_factory=lambda: ["SHA256SUMS", "MANIFEST.sha256"])


ALL_PACKAGES: dict[str, PackageSpec] = {
    "000": PackageSpec(
        pkg_id="000",
        name="000_projection_obstruction",
        path=PO000_DIR,
        manuscript_name="projection_obstruction.md",
        pytest_command=[sys.executable, "-m", "pytest", "code/tests", "-m", "not native_integration", "-q", "--disable-warnings", "--tb=short"],
        deposit_verifier_command=[sys.executable, "verify_deposit.py"],
        manifest_names=["SHA256SUMS", "MANIFEST.sha256"],
    ),
    "001": PackageSpec(
        pkg_id="001",
        name="001_from_covering_edge_descent_complexes_to_functorial_presheaves_and_coherence_defects",
        path=PO001_DIR,
        manuscript_name="covering_edge_descent.md",
        pytest_command=[sys.executable, "-m", "pytest", "code/tests", "-q", "-p", "no:cacheprovider"],
        deposit_verifier_command=[sys.executable, "scripts/verify_package.py"],
        manifest_names=["SHA256SUMS", "MANIFEST.sha256"],
    ),
    "006": PackageSpec(
        pkg_id="006",
        name="006_vector_and_quantum_observer_geometries",
        path=PO006_DIR,
        manuscript_name="vector_and_quantum_observer_geometries.md",
        pytest_command=[sys.executable, "-m", "pytest", "code/tests", "-q"],
        deposit_verifier_command=[sys.executable, "verify_deposit.py"],
        manifest_names=["SHA256SUMS", "MANIFEST.sha256"],
    ),
    "007": PackageSpec(
        pkg_id="007",
        name="007_m_compatible_gauge_classification",
        path=PO007_DIR,
        manuscript_name="m_compatible_gauge_classification.md",
        pytest_command=[sys.executable, "-m", "pytest", "code/tests", "-q"],
        deposit_verifier_command=[sys.executable, "verify_deposit.py"],
        manifest_names=["SHA256SUMS", "MANIFEST.sha256"],
    ),
    "008": PackageSpec(
        pkg_id="008",
        name="008_so_k_invariant_gauge_classification",
        path=PO008_DIR,
        manuscript_name="so_k_invariant_gauge_classification.md",
        pytest_command=[sys.executable, "-m", "pytest", "code/tests", "-q", "--cov=code", "--cov-branch", "--cov-fail-under=95"],
        deposit_verifier_command=[sys.executable, "verify_deposit.py", "--tree-only", "--skip-lake"],
        manifest_names=["SHA256SUMS", "MANIFEST.sha256"],
    ),
    "009": PackageSpec(
        pkg_id="009",
        name="009_coordinate_wise_additivity",
        path=PO009_DIR,
        manuscript_name="coordinate_wise_additivity.md",
        pytest_command=[sys.executable, "-m", "pytest", "code/tests", "-q"],
        deposit_verifier_command=[sys.executable, "verify_deposit.py", "--tree-only"],
        manifest_names=["SHA256SUMS", "MANIFEST.sha256"],
    ),
    "033": PackageSpec(
        pkg_id="033",
        name="033_certified_adaptive_quantum_dynamics",
        path=PO033_DIR,
        manuscript_name="033_certified_adaptive_quantum_dynamics.md",
        pytest_command=[sys.executable, "-m", "pytest", "code/tests", "-q"],
        deposit_verifier_command=[sys.executable, "verify_deposit.py", "--skip-lean"],
        manifest_names=["SHA256SUMS", "MANIFEST.sha256"],
    ),
    "034": PackageSpec(
        pkg_id="034",
        name="034_higher_cell_cochain_projection_and_retraction_dynamics",
        path=PO034_DIR,
        manuscript_name="034_higher_cell_cochain_projection_and_retraction_dynamics.md",
        pytest_command=[sys.executable, "-m", "pytest", "code/tests", "-q", "--import-mode=importlib"],
        deposit_verifier_command=[sys.executable, "verify_deposit.py", "--review"],
        manifest_names=["SHA256SUMS", "MANIFEST.sha256"],
    ),
    "035": PackageSpec(
        pkg_id="035",
        name="035_zero_container_relational_spacetime_and_witness_holonomy",
        path=PO035_DIR,
        manuscript_name="zero_container_relational_spacetime_and_witness_holonomy.md",
        pytest_command=[sys.executable, "-m", "pytest", "code/tests", "-q"],
        deposit_verifier_command=[sys.executable, "verify_deposit.py"],
        manifest_names=["SHA256SUMS"],
    ),
}

SIBLING_PACKAGES: dict[str, PackageSpec] = {
    k: v for k, v in ALL_PACKAGES.items() if k != "000"
}

# Forbidden unearned consensus & hype words under strict Claim Hygiene
CLAIM_HYGIENE_FORBIDDEN_WORDS: list[str] = [
    "proves",
    "guarantees",
    "mathematically verifies",
    "fundamentally",
    "true intelligence",
    "impossible",
    "universal",
    "flawless",
    "perfectly",
    "clearly",
    "obviously",
    "simply",
    "merely",
    "weaponized",
]

# Required Authoritative Sibling Reference Table entries in PO-000
EXPECTED_SIBLING_TABLE_ROWS = [
    {"pkg": "001", "anchor": "PO-001", "topic": "Covering-edge descent complexes, saturated-chain presheaves, degree-2 curvature cochains"},
    {"pkg": "006", "anchor": "PO-006", "topic": "Vector and quantum observer geometries, operator-norm bounds, phase metrics"},
    {"pkg": "007", "anchor": "PO-007", "topic": "M-compatible gauge classification for Banach presheaf coboundaries"},
    {"pkg": "008", "anchor": "PO-008", "topic": "SO(k)-invariant gauge classification on Euclidean stalks"},
    {"pkg": "009", "anchor": "PO-009", "topic": "Coordinate-wise additivity and l1 norm on finite graph cochains"},
    {"pkg": "033", "anchor": "PO-033", "topic": "Conditional analytic bounds, uncertified adaptive cluster prototype"},
    {"pkg": "034", "anchor": "PO-034", "topic": "Higher-cell cochain projection and retraction dynamics"},
    {"pkg": "035", "anchor": "PO-035", "topic": "Zero-container relational spacetime and witness holonomy"},
]
