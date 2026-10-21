
import json, pathlib, sys, types
root, source, temp, *tests = sys.argv[1:]
sys.path.insert(0, str(pathlib.Path(root) / "code/python"))
import src.finite_probability as parent
name = "src.finite_probability.simplex"
module = types.ModuleType(name)
module.__file__ = source
module.__package__ = "src.finite_probability"
sys.modules[name] = module
parent.simplex = module
try:
    exec(compile(pathlib.Path(source).read_bytes(), source, "exec"), module.__dict__)
except Exception as error:
    print(json.dumps({"phase": "load", "error": type(error).__name__, "detail": str(error)}))
    sys.exit(3)
import pytest
result = pytest.main([*tests, "-q", "--basetemp", temp, "-p", "no:cacheprovider"])
print(json.dumps({"phase": "pytest", "exit_code": int(result)}))
sys.exit(result)
