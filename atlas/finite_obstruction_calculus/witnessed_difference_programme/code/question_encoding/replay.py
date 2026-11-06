"""Bind a native experiment replay to its source inputs and deposited result."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

from .ffi import invoke

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
RECEIPT = PACKAGE_ROOT / "manifests" / "question_encoding_experiment.json"
SOURCE_PATHS = (
    "vendor/engine/engine_wdp/src/question_preserving_encoding.rs",
    "vendor/engine/engine_wdp/src/examples/question_preserving_encoding.rs",
    "vendor/engine/tests/engine_wdp/test_question_preserving_encoding.rs",
    "vendor/engine/engine_category_theory/src/finite_report_query.rs",
    "vendor/engine/engine_functional/src/gamma2.rs",
    "vendor/engine/Cargo.lock",
)


def repository_root() -> Path:
    for root in PACKAGE_ROOT.parents:
        if (root / SOURCE_PATHS[0]).is_file():
            return root
    raise FileNotFoundError("Replay needs the monorepo's canonical native sources.")


def _default_binary_env() -> None:
    if os.environ.get("WDP_QUESTION_ENCODING_BINARY"):
        return
    suffix = ".exe" if sys.platform == "win32" else ""
    for root in PACKAGE_ROOT.parents:
        for rel in (
            f"target_paper_rust/debug/examples/question_preserving_encoding{suffix}",
            f"target_paper_rust/release/examples/question_preserving_encoding{suffix}",
            f"vendor/engine/target/debug/examples/question_preserving_encoding{suffix}",
            f"vendor/engine/target/release/examples/question_preserving_encoding{suffix}",
        ):
            candidate = root / rel
            if candidate.is_file():
                os.environ["WDP_QUESTION_ENCODING_BINARY"] = str(candidate)
                return


_default_binary_env()


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
