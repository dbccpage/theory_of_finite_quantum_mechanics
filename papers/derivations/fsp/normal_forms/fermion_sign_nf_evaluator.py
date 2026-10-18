"""Compatibility import for the single maintained evaluator in code/."""
import importlib.util
from pathlib import Path
import sys

_code_dir = Path(__file__).resolve().parent.parent / "code"
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))
_spec = importlib.util.spec_from_file_location("_fermion_sign_contract_evaluator", _code_dir / "fermion_sign_nf_evaluator.py")
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
NormalFormEvaluator = _module.NormalFormEvaluator
main = _module.main

if __name__ == "__main__":
    sys.exit(main())
