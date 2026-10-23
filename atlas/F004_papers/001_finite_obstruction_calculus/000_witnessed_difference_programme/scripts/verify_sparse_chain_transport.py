"""Replay the native sparse-transport CLI and hostile certificates.

This script orchestrates Rust execution. It implements no chain arithmetic,
contraction, functional or certificate checker.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import platform
import subprocess
import tempfile
from pathlib import Path


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def invoke(binary: Path, arguments: list[str], expected: int) -> dict:
    command = [str(binary), *arguments]
    result = subprocess.run(command, capture_output=True, text=True, timeout=60, check=False)
    if result.returncode != expected:
        raise RuntimeError(f"{command}: exit {result.returncode}, expected {expected}: {result.stderr}")
    report = json.loads(result.stdout if expected == 0 else result.stderr)
    required = "PASS" if expected == 0 else "REFUSED"
    if report.get("status") != required or report.get("authority_effect") != "None":
        raise RuntimeError(f"wrong native outcome for {command}: {report}")
    return {"command": command, "exit_code": result.returncode, "report": report}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    binary = args.binary.resolve(strict=True)
    binary_before = digest(binary)
    paper = Path(__file__).resolve().parents[1]
    root = next(path for path in paper.parents if (path / "omega_engine/crates_rs/Cargo.toml").is_file())
    paths = [
        "omega_engine/crates_rs/omega_homology/src/permutohedral.rs",
        "omega_engine/crates_rs/omega_homology/src/finite_poset.rs",
        "omega_engine/crates_rs/omega_wdp/src/guarded_chain_transport.rs",
        "omega_engine/crates_rs/omega_wdp/src/guarded_chain_transport/sparse.rs",
        "omega_engine/crates_rs/omega_wdp/src/examples/sparse_guarded_transport.rs",
        str(Path(__file__).resolve().relative_to(root)),
    ]
    before = {name: digest(root / name) for name in paths}
    positive: list[dict] = []
    hostile: list[dict] = []
    retained = None
    with tempfile.TemporaryDirectory(prefix="wdp-sparse-replay-") as temporary:
        directory = Path(temporary)
        for n in (4, 8, 16, 32, 64, 128):
            for degree in range(3):
                path = directory / f"n{n}_q{degree}.json"
                proposed = invoke(binary, ["demo", str(n), str(degree), "--certificate-out", str(path)], 0)
                checked = invoke(binary, ["verify", str(n), str(degree), "--certificate", str(path)], 0)
                if proposed["report"]["ambient_enumeration"] is not False:
                    raise RuntimeError("wrong proposal mode")
                if checked["report"]["transport_constructor_called"] is not False:
                    raise RuntimeError("independent checker called the constructor")
                positive.append({"pairs": n, "degree": degree, "proposal": proposed,
                                 "independent_check": checked, "certificate_sha256": digest(path)})
                if n == 32 and degree == 2:
                    retained = json.loads(path.read_text(encoding="utf-8"))
        if retained is None:
            raise RuntimeError("missing required retained case")
        mutations = []
        bad = copy.deepcopy(retained)
        bad["filling"][0]["coefficient"] *= -1
        mutations.append(("reversed_filling_sign", bad))
        bad = copy.deepcopy(retained)
        bad["filling"] = []
        mutations.append(("missing_filling", bad))
        bad = copy.deepcopy(retained)
        bad["filling"].append(copy.deepcopy(bad["filling"][0]))
        mutations.append(("duplicate_term", bad))
        bad = copy.deepcopy(retained)
        bad["filling"][0]["coefficient"] = True
        mutations.append(("boolean_coefficient", bad))
        bad = copy.deepcopy(retained)
        bad["filling"][0]["cell"][0][0] = 999
        mutations.append(("invalid_label", bad))
        bad = copy.deepcopy(retained)
        bad["cycle"][0]["coefficient"] *= -1
        mutations.append(("changed_problem", bad))
        bad = copy.deepcopy(retained)
        bad["capacity"] = 2
        mutations.append(("changed_capacity", bad))
        bad = copy.deepcopy(retained)
        bad["degree"] = 2.0
        mutations.append(("floating_degree", bad))
        bad = copy.deepcopy(retained)
        bad["verified"] = True
        mutations.append(("supplied_verification_flag", bad))
        for name, candidate in mutations:
            path = directory / f"hostile_{name}.json"
            path.write_text(json.dumps(candidate), encoding="utf-8")
            hostile.append({"mutation": name, **invoke(binary, ["verify", "32", "2", "--certificate", str(path)], 2)})
    after = {name: digest(root / name) for name in paths}
    if before != after:
        raise RuntimeError("source bytes changed during native replay")
    if binary_before != digest(binary):
        raise RuntimeError("native executable bytes changed during replay")
    output = {
        "schema_version": 1, "status": "PASS", "authority_effect": "None",
        "scope": "Native V2 sparse filling fixtures and independent checker; no full-complex enumeration or universal benchmark claim.",
        "python_version": platform.python_version(), "binary": str(binary),
        "binary_sha256": binary_before, "binary_stable_across_replay": True,
        "source_sha256": after,
        "positive_cases": positive, "hostile_cases": hostile,
        "retained_certificate_n32_q2": retained,
        "positive_count": len(positive), "hostile_count": len(hostile),
        "baseline_scope": "Known one-cell fillers; a direct checker is a favorable baseline and no search speedup is inferred.",
    }
    # Exclusive creation refuses existing files and aliases (including links
    # to the checked binary or source); the receipt cannot overwrite its inputs.
    with args.output.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "positive": len(positive), "hostile": len(hostile), "output": str(args.output)}))


if __name__ == "__main__":
    main()
