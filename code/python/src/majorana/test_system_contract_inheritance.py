import importlib.util
from pathlib import Path
import sys


def _load_validator(repo_root: Path):
    path = repo_root / "omega_engine_governance" / "contracts" / "contract_inheritance.py"
    spec = importlib.util.spec_from_file_location("contract_inheritance", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.validate_system_contracts


def test_system_contract_inheritance_and_coverage() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    validate_system_contracts = _load_validator(repo_root)
    report = validate_system_contracts(
        contracts_root=repo_root / "omega_engine_governance" / "contracts" / "contracts_system",
        crates_root=repo_root / "omega_engine" / "crates",
    )
    assert report.ok, "\n".join(report.findings)
    assert report.crate_contracts == 0
    assert report.object_contracts == 67
