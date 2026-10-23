"""Build or independently replay exact finite guarded-schedule certificates.

The checker reconstructs every declared cell, verifies d*d=0, replays supplied
integer matrix operations without rank search, and compares all cells with a
direct all-word/all-refinement baseline. Native replay is separately configured
by an explicit binary, build receipt, and source root. AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "code"))
sys.path.insert(0, str(PACKAGE))

from guarded_schedule_topology.experiment import (  # noqa: E402
    build_certificate,
    check_certificate,
    encoded,
    read_certificate_data,
    source_hashes,
)
from guarded_schedule_topology.model import TopologyRefusal  # noqa: E402


def regular_path(path: Path, *, may_be_missing: bool = False) -> Path:
    path = path.absolute()
    for part in reversed((path, *path.parents)):
        if not part.exists() and not part.is_symlink():
            if may_be_missing:
                continue
            raise TopologyRefusal(f"missing input: {part}")
        info = part.lstat()
        if stat.S_ISLNK(info.st_mode):
            raise TopologyRefusal(f"linked artifact path: {part}")
        if (part == path and not stat.S_ISREG(info.st_mode)
                or part != path and not stat.S_ISDIR(info.st_mode)):
            raise TopologyRefusal(f"nonregular artifact path: {part}")
    return path


def check_output(path: Path, protected: list[Path]) -> None:
    path = regular_path(path, may_be_missing=True)
    for other in protected:
        if path.resolve() == other.resolve() or (path.exists() and other.exists() and path.samefile(other)):
            raise TopologyRefusal(f"output aliases a protected input: {other}")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "check"))
    parser.add_argument("--certificate", type=Path, required=True)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--native-bin", type=Path)
    parser.add_argument("--native-build-receipt", type=Path)
    parser.add_argument("--source-root", type=Path)
    args = parser.parse_args(argv)
    try:
        native_args = (args.native_bin, args.native_build_receipt, args.source_root)
        if any(value is not None for value in native_args) and any(value is None for value in native_args):
            raise TopologyRefusal("native replay needs binary, build receipt, and source root together")
        before = source_hashes(PACKAGE)
        protected = [regular_path(PACKAGE / name) for name in before]
        owner = None
        if args.native_bin is not None:
            from scripts.check_causal_execution import NativeOwner
            owner = NativeOwner(*native_args)
            protected.extend([regular_path(args.native_bin), regular_path(args.native_build_receipt)])
            protected.extend(regular_path(args.source_root / name) for name in owner.build["sources"])
            protected.extend([PACKAGE / "code/causal_certificates/native/main.rs",
                              PACKAGE / "code/causal_certificates/native/build_native.py"])
        if args.mode == "build":
            check_output(args.certificate, protected)
        else:
            protected.append(regular_path(args.certificate))
        if args.receipt:
            check_output(args.receipt, [*protected, args.certificate])
        if args.mode == "build":
            certificate = build_certificate(PACKAGE)
            certificate_bytes = encoded(certificate) + b"\n"
        else:
            certificate, certificate_bytes = read_certificate_data(args.certificate)
        checked = check_certificate(PACKAGE, certificate)
        native = {"fresh_native_replay": False, "scope": "native replay was not requested"}
        if owner is not None:
            from guarded_schedule_topology.native import replay_native
            native = replay_native(owner)
        if source_hashes(PACKAGE) != before:
            raise TopologyRefusal("checker sources changed during verification")
        if args.mode == "build":
            check_output(args.certificate, protected)
            args.certificate.parent.mkdir(parents=True, exist_ok=True)
            args.certificate.write_bytes(certificate_bytes)
        elif read_certificate_data(args.certificate)[1] != certificate_bytes:
            raise TopologyRefusal("certificate input changed during verification")
        receipt = {"schema": "wdp-guarded-schedule-topology-validation-v1", "status": "PASS",
                   "authority_effect": "None", "utc": datetime.now(timezone.utc).isoformat(),
                   "python": platform.python_version(), "mode": args.mode, "sources": before,
                   "certificate_sha256": hashlib.sha256(certificate_bytes).hexdigest(),
                   "checks": checked, "native": native}
        if args.receipt:
            check_output(args.receipt, [*protected, args.certificate])
            args.receipt.parent.mkdir(parents=True, exist_ok=True)
            args.receipt.write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        if source_hashes(PACKAGE) != before:
            raise TopologyRefusal("checker sources changed during artifact writing")
        if read_certificate_data(args.certificate)[1] != certificate_bytes:
            raise TopologyRefusal("certificate changed during artifact writing")
        if owner is not None:
            owner.verify_custody()
        print(json.dumps({"status": "PASS", "cases": len(checked["cases"]),
                          "fresh_native_replay": native["fresh_native_replay"],
                          "certificate_sha256": receipt["certificate_sha256"]}, sort_keys=True))
        return 0
    except (ValueError, TypeError, KeyError, IndexError, OSError, RecursionError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
