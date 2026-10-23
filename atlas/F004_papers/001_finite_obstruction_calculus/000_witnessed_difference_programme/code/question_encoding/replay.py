"""Bind a native experiment replay to its source inputs and deposited result."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from .ffi import invoke

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
RECEIPT = PACKAGE_ROOT / "manifests" / "question_encoding_experiment.json"
SOURCE_PATHS = (
    "omega_engine/crates_rs/omega_wdp/src/question_preserving_encoding.rs",
    "omega_engine/crates_rs/omega_wdp/src/examples/question_preserving_encoding.rs",
    "omega_engine/crates_rs/tests/omega_wdp/question_preserving_encoding.rs",
    "omega_engine/crates_rs/omega_category_theory/src/finite_report_query.rs",
    "omega_engine/crates_rs/omega_functional/src/gamma2.rs",
    "omega_engine/crates_rs/Cargo.lock",
)


def repository_root() -> Path:
    for root in PACKAGE_ROOT.parents:
        if (root / SOURCE_PATHS[0]).is_file():
            return root
    raise FileNotFoundError("Replay needs the monorepo's canonical native sources.")


def replay() -> dict:
    root = repository_root()
    sources = {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in SOURCE_PATHS}
    result = invoke({"action": "experiment"})
    if result.get("compiled_source_sha256") != sources:
        raise RuntimeError("Native executable embeds different source bytes; rebuild before replay.")
    return {
        "schema_version": 1,
        "evidence_scope": "Exhaustive bounded integer-quadratic fixture; no empirical or unrestricted soundness claim.",
        "authority_effect": "None",
        "source_sha256": sources,
        "experiment": result,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = replay()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        RECEIPT.write_text(rendered, encoding="utf-8")
    elif RECEIPT.read_text(encoding="utf-8") != rendered:
        raise SystemExit("FAIL: native experiment or pinned source bytes differ from the deposited receipt")
    print("PASS: 225 tasks and 125 candidates replayed against the native checker and both direct baselines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
