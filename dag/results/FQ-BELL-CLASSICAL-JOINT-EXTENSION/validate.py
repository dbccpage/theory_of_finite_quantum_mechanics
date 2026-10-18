"""Run and record the targeted checks for this one prompt; never dispatch others."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LOGS = HERE / "logs"
LOGS.mkdir(exist_ok=True)


def run(name, command, cwd=ROOT, env=None):
    proc = subprocess.run(command,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding="utf-8",errors="replace")
    (LOGS / (name+".log")).write_text(proc.stdout,encoding="utf-8")
    return {"name":name,"command":command,"cwd":str(cwd.relative_to(ROOT)),"exit_code":proc.returncode,"log":"logs/"+name+".log"}


def python_checks():
    return [
        run("python_tests",[sys.executable,"code/python/tests/test_bell_joint_extension.py","-v"]),
        run("replay",[sys.executable,str(HERE / "replay.py")]),
    ]


def rust_checks():
    return [run("rust_tests",["cargo","test","--manifest-path","code/rust/Cargo.toml","-p","tfqm_finite_probability","--lib","bell_joint_extension","--offline"])]


def lean_checks():
    cwd = ROOT / "lean4"
    build = cwd / ".lake/build/lib/lean"
    build.mkdir(parents=True,exist_ok=True)
    env = dict(os.environ,LEAN_PATH=str(build))
    checks = [run("lean_version",["lean","--version"],cwd,env)]
    checks.append(run("lean_existing",["lean","-o",str(build / "DerivationDagQMClosure.olean"),"DerivationDagQMClosure.lean"],cwd,env))
    if checks[-1]["exit_code"] == 0:
        checks.append(run("lean_bell",["lean","-o",str(build / "BellClassicalJointExtension.olean"),"BellClassicalJointExtension.lean"],cwd,env))
    return checks


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=3) as pool:
        checks = [check for group in pool.map(lambda f:f(),[python_checks,rust_checks,lean_checks]) for check in group]
    source_paths = [
        "code/python/src/qm/bell_joint_extension.py","code/python/tests/test_bell_joint_extension.py",
        "code/rust/src/finite_probability/bell_joint_extension.rs","code/rust/src/finite_probability/lib.rs",
        "lean4/BellClassicalJointExtension.lean","lean4/DerivationDagQMClosure.lean","lean4/lakefile.lean","lean4/lean-toolchain",
        "dag/results/FQ-BELL-CLASSICAL-JOINT-EXTENSION/prompt.yaml",
    ]
    hashes = {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in source_paths}
    receipt = {
        "node_id":"FQ-BELL-CLASSICAL-JOINT-EXTENSION","authority_effect":"None",
        "execution_kind":"Codex-assisted derivation with native exact checks; no external model API",
        "base_commit":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
        "checked_at_utc":datetime.now(timezone.utc).isoformat(),
        "source_sha256":hashes,"checks":checks,
        "all_targeted_checks_passed":len(checks)==6 and all(c["exit_code"] == 0 for c in checks),
        "scope":"This single prompt and the listed checks only; no full-suite or other-prompt execution.",
    }
    (HERE/"checks.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    for c in checks:
        print(c["name"],"PASS" if c["exit_code"] == 0 else "FAIL",c["log"],flush=True)
    sys.exit(0 if receipt["all_targeted_checks_passed"] else 1)
