import omega_engine_governance.contracts as omega_contracts
import json
from omega_engine_governance.contracts.contract_corpus import (
    CONTRACT_CORPUS_ROOT,
    corpus_hash,
    corpus_paths,
    load_manifest,
    validate_contract_corpus,
)
from omega_engine_governance.contracts.certificate_promotion import evaluate_certificate_promotion


def test_historical_mirror_manifest_retains_its_declared_source_records():
    manifest = load_manifest()
    assert manifest
    raw_manifest = json.loads((CONTRACT_CORPUS_ROOT / "MIRROR_MANIFEST.json").read_text())
    assert len(manifest) == raw_manifest["file_count"]
    sources = {entry["source"] for entry in manifest}
    assert len(sources) == len(manifest)
    assert all(len(entry["source_sha256"]) == 64 for entry in manifest)
    assert "src/lib.rs" in sources
    assert (
        "src/contract_canonical_definitions/contracts/rust/lib.contract.yaml" in sources
    )
    assert "tests/v1_corpus_gate.rs" in sources


def test_contracts_corpus_is_available_and_hashable():
    paths = corpus_paths()
    assert CONTRACT_CORPUS_ROOT.exists()
    names = (
        "contract_governance", "contracts_base", "contracts_oe",
        "contracts_oeos",
    )
    expected = set()
    for name in names:
        vault = CONTRACT_CORPUS_ROOT / name
        assert vault.is_dir() and list(vault.rglob("*.yaml"))
        expected.update(path for path in vault.rglob("*") if path.is_file() and path.suffix.lower() in {".yaml", ".yml", ".md"})
    expected.add(CONTRACT_CORPUS_ROOT / "contracts_oeos/oeos_contract_registry.v1.json")
    assert set(paths) == expected and len(paths) == len(expected)
    digest = corpus_hash()
    assert len(digest) == 64
    assert int(digest, 16) >= 0


def test_contracts_corpus_file_contract_gate_runs_evidence_only():
    report = validate_contract_corpus()
    summary = report.summary_dict()
    paths = corpus_paths()
    assert summary["total_documents"] == len(paths)
    assert summary["checked_yaml"] == sum(path.suffix in {".yaml", ".yml"} for path in paths)
    assert sum(summary["disposition_counts"].values()) == len(paths)
    assert {item.relpath for item in report.dispositions} == {
        path.relative_to(CONTRACT_CORPUS_ROOT).as_posix() for path in paths
    }
    assert summary["operationally_validated"] == 0
    assert summary["status"] == "INVALID" and not report.ok
    unsupported = {item.relpath for item in report.dispositions if item.disposition == "UNSUPPORTED_DOCUMENT_SCHEMA" and item.relpath.endswith(".contract.yaml")}
    assert unsupported == {
        "contracts_oe/operators/projector.contract.yaml",
        "contracts_oe/operators/retractor.contract.yaml",
    }


def test_certificate_promotion_never_grants_authority_locally():
    for effect in (None, "none", "evidence_only", "state_transition"):
        decision = evaluate_certificate_promotion(effect)
        assert decision.authority_granted is False


def test_root_package_imports_core_surface():
    assert hasattr(omega_contracts, "ContractTrait")
    assert hasattr(omega_contracts, "validate_python_contract_mirror")
    assert hasattr(omega_contracts, "NoAuthorityGuard")


