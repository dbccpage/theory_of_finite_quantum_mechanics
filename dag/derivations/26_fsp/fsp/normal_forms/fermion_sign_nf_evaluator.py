"""Compatibility import for the single maintained evaluator in code/."""
import importlib.util
from pathlib import Path
import sys

_repo = next((p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").is_file()), Path(__file__).resolve().parents[3])
_src_fsp = _repo / "code" / "python" / "src" / "fsp"
_src = _repo / "code" / "python" / "src"

for p in (_src_fsp, _src):
    if p.exists() and str(p) not in sys.path:
        sys.path.insert(0, str(p))

_evaluator_path = _src_fsp / "fermion_sign_nf_evaluator.py"
_spec = importlib.util.spec_from_file_location("_fermion_sign_contract_evaluator", _evaluator_path)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
NormalFormEvaluator = _module.NormalFormEvaluator
main = _module.main

if __name__ == "__main__":
    sys.exit(main())
