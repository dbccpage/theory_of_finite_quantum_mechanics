"""Compile the new core-only proof spine and verify source-bound axiom receipts.

This does not rebuild or change the historical Mathlib 202-declaration census.
The printed declarations are the selected audit surface of each complete source.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import stat
import subprocess
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES = (
    "RefinementFactorization",
    "BehavioralQuotient",
    "SemiringCoarseGraining",
    "ContextReflection",
    "RelationalRetention",
    "RetentionChoices",
    "FunctionalClassification",
    "SelfReferenceBridges",
    "ObserverDescent",
    "ReconstructionClassification",
    "RationalPhaseBoundary",
    "InstrumentRepeatability",
    "EmpiricalRepair",
    "LegacyObserverAdapters",
    "FiniteRouting",
    "ObserverAdapterCompleteness",
    "OriginalGenesisObserver",
    "PolicyObserverAdapter",
    "ProposalAdmissionBridge",
    "FoundationalBridges",
    "PrimitiveAdmissionFloor",
    "CochainTransport",
    "Source25PairTransport",
    "AdmissionCount",
    "PrimitiveContextFloor",
    "RootGaugeNormalization",
    "MarkedGaugeTransport",
    "ComplexTensorBalancing",
    "DyadicPresentation",
    "FaithfulRepresentation",
    "FiniteConstraintRepresentation",
    "CertifiedProgress",
    "BeliefGameQuotient",
    "ExactProgressQuotient",
    "LocalObservationCompletion",
    "TrotterObservableFiltering",
    "CARResponseWitness",
    "GenerativeHistoryCompression",
    "AdditiveTensorCompletion",
    "DaggerObserverPairing",
    "FiniteHermitianization",
    "CertifiedPreservers",
    "RationalUnitaryReachability",
    "ProjectiveFrameRigidity",
    "FiniteStateEffectReadout",
    "FiniteProcessComposition",
    "DistinctImageCompletion",
    "ToricSyndromeCorrespondence",
    "GuardedHistoryCoherence",
    "NativeFutureCompression",
)
ALLOWED_AXIOMS = frozenset({"Classical.choice", "Quot.sound", "propext"})


def regular(path: Path) -> bytes:
    for parent in path.parents:
        metadata = parent.lstat()
        if not stat.S_ISDIR(metadata.st_mode) or getattr(metadata, "st_file_attributes", 0) & 0x400:
            raise ValueError(f"non-regular proof directory: {parent}")
    metadata = path.lstat()
    if not stat.S_ISREG(metadata.st_mode) or getattr(metadata, "st_file_attributes", 0) & 0x400:
        raise ValueError(f"non-regular proof/control file: {path}")
    return path.read_bytes()


def receipt_for(name: str) -> Path:
    filename = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower() + "_axioms.txt"
    return ROOT / "lean4" / filename


def contains_admission(output: str) -> bool:
    return "sorryAx" in output or bool(re.search(r"declaration uses [`'‘]sorry[`'’]", output))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", default=shutil.which("lean"))
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if not args.lean:
        parser.error("provide the Lean 4.33.1 binary using --lean")
    sources = [ROOT / "lean4" / "WitnessedDifference" / f"{name}.lean" for name in MODULES]
    sources.extend(
        [
            ROOT / "lean4" / "WitnessedDifference" / "FiniteDerivations.lean",
            Path(__file__).absolute(),
        ]
    )
    source_snapshot = {path: hashlib.sha256(regular(path)).hexdigest() for path in sources}
    for name in MODULES:
        receipt = receipt_for(name)
        if not args.write or receipt.exists() or receipt.is_symlink():
            regular(receipt)
    version = subprocess.run(
        [args.lean, "--version"], check=True, text=True, capture_output=True
    ).stdout
    if "version 4.33.1" not in version:
        raise SystemExit("the standalone proof spine requires Lean 4.33.1")
    declarations = 0
    with tempfile.TemporaryDirectory(prefix="wdp-core-proofs-") as temporary:
        directory = Path(temporary)
        (directory / "WitnessedDifference").mkdir()
        environment = os.environ.copy()
        environment["LEAN_PATH"] = str(directory)
        for name in MODULES:
            source = ROOT / "lean4" / "WitnessedDifference" / f"{name}.lean"
            digest = source_snapshot[source]
            for attempt in range(5):
                result = subprocess.run(
                    [
                        args.lean,
                        "-o",
                        str(directory / "WitnessedDifference" / f"{name}.olean"),
                        f"WitnessedDifference/{name}.lean",
                    ],
                    cwd=ROOT / "lean4",
                    env=environment,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                output = result.stdout + result.stderr
                if "failed to read file" in output and attempt < 4:
                    time.sleep(0.5)
                    continue
                break
            if result.returncode or contains_admission(output):
                raise SystemExit(f"{name}: proof compilation failed\n{output}")
            audit_lines = re.findall(
                r"'[^']+' (?:depends on axioms:|does not depend on any axioms)", output
            )
            if not audit_lines:
                raise SystemExit(f"{name}: no printed declaration audit")
            axioms = set()
            for group in re.findall(r"depends on axioms:\s*\[([^]]*)\]", output):
                axioms.update(x.strip() for x in group.split(",") if x.strip())
            if not axioms <= ALLOWED_AXIOMS:
                raise SystemExit(f"{name}: unexpected axioms {sorted(axioms - ALLOWED_AXIOMS)}")
            receipt = receipt_for(name)
            body = (
                f"Lean 4.33.1 standalone {name} selected declaration audit\n"
                f"Source SHA-256: {digest}\n"
                f"Declarations audited: {len(audit_lines)}\n"
                "Compilation exit code: 0\n"
                f"Axiom union: {', '.join(sorted(axioms)) or 'none'}\n\n{output}"
            )
            if args.write:
                receipt.write_text(body, encoding="utf-8", newline="\n")
            elif regular(receipt).decode("utf-8").replace("\r\n", "\n") != body:
                raise SystemExit(f"{receipt.relative_to(ROOT)} is absent or stale; run --write")
            declarations += len(audit_lines)
            print(f"{name}: {len(audit_lines)} selected declarations checked")
        aggregate = subprocess.run(
            [args.lean, "WitnessedDifference/FiniteDerivations.lean"],
            cwd=ROOT / "lean4",
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )
        if aggregate.returncode or contains_admission(aggregate.stdout + aggregate.stderr):
            raise SystemExit(f"finite import spine failed\n{aggregate.stdout}{aggregate.stderr}")
    if {path: hashlib.sha256(regular(path)).hexdigest() for path in sources} != source_snapshot:
        raise SystemExit("proof sources or verifier changed during compiler subprocesses")
    print(
        f"{len(MODULES)} core-only modules; {declarations} selected declarations; no admitted-proof diagnostics in the compiled modules"
    )


if __name__ == "__main__":
    main()
