#!/usr/bin/env python3
"""Stdlib-only independent verifier for PO-000 replay JSON."""

from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

KNOWN_KINDS = {
    "exact_finite",
    "exact_symbolic_instance",
    "finite_exhaustive",
    "numerical_replay",
    "counterexample",
    "premise_check",
    "static_scope_fence",
    "not_executable",
}
KNOWN_VERDICTS = {"pass", "fail", "refused", "open"}
REQUIRED_CLAIMS = {
    *(f"A{i}" for i in range(1, 8)),
    *(f"B{i}" for i in range(1, 5)),
    *(f"C{i}" for i in range(1, 5)),
    *(f"D{i}" for i in range(1, 9)),
    "D8a",
    *(f"E{i}" for i in range(1, 10)),
    *(f"F{i}" for i in range(1, 4)),
    *(f"G{i}" for i in range(1, 5)),
    *(f"H{i}" for i in range(1, 8)),
}

REQUIRED_GENERAL_UNRESOLVED = {
    "A1",
    "C1",
    "C2",
    "C4",
    "D1",
    "D2",
    "D3",
    "D4",
    "D5",
    "E1",
    "E2",
    "E3",
    "E4",
    "E5",
    "E8",
    "E9",
    "H3",
    "H4",
    "H6",
    "H7",
}
EXPECTED_EVIDENCE_KINDS = {
    **dict.fromkeys(("D6", "H5"), "counterexample"),
    **dict.fromkeys(
        (
            "A2",
            "A3",
            "B1",
            "B2",
            "D2",
            "D5",
            "D8",
            "E5",
            "E8",
            "E9",
            "G1",
            "H1",
            "H2",
            "H3",
            "H4",
            "H6",
            "H7",
        ),
        "exact_finite",
    ),
    **dict.fromkeys(("B3", "C1", "E1"), "exact_symbolic_instance"),
    **dict.fromkeys(("D1", "D3", "D4"), "finite_exhaustive"),
    **dict.fromkeys(("B4", "C2", "C4", "E3", "G2"), "not_executable"),
    **dict.fromkeys(("E2", "E4", "F1", "F2"), "numerical_replay"),
    **dict.fromkeys(("A1", "F3"), "premise_check"),
    **dict.fromkeys(
        ("A4", "A5", "A6", "A7", "C3", "D7", "E6", "E7", "G3", "G4"),
        "static_scope_fence",
    ),
}
EXPECTED_VERDICTS = {
    claim_id: "refused" if kind == "not_executable" else "pass"
    for claim_id, kind in EXPECTED_EVIDENCE_KINDS.items()
}
_here = Path(__file__).resolve().parent

def _resolve_po000_package_root(start: Path) -> Path:
    """Locate the PO-000 release/playpen package root for inventory hashing."""
    for p in [start, *start.parents]:
        published = (
            p
            / "published"
            / "004_projection_obstruction"
            / "projection_obstruction_paper"
        )
        if published.is_dir() and (published / "code").is_dir():
            return published
        if (p / "projection_obstruction_paper.md").exists() and (p / "code").is_dir():
            return p
        if (p / "crates").is_dir() and ((p / "_tests_unit").is_dir() or (p / "tests").is_dir()):
            return p
    # legacy layouts relative to this file
    if start.name == "po000" and start.parent.name == "src":
        return start.parent.parent
    if start.name in ("code", "po000_lib"):
        return start.parent
    if start.name == "coda":
        return (
            start.parents[2]
            / "published"
            / "004_projection_obstruction"
            / "projection_obstruction_paper"
        )
    return start

_pkg_root = _resolve_po000_package_root(_here)
RELEASE_ROOT = _pkg_root
_lib_dir_name = (
    "crates"
    if (_pkg_root / "crates").is_dir()
    else "src/po000"
    if (_pkg_root / "src" / "po000").is_dir()
    else "code"
    if (_pkg_root / "code").is_dir()
    else "coda"
    if (_pkg_root / "coda").is_dir()
    else "omega_engine"
    if (_pkg_root / "omega_engine").is_dir()
    else "po000_lib"
)
_tests_under_lib = (_pkg_root / _lib_dir_name / "tests").is_dir()

def _resolve_required_source_paths(pkg_root: Path, lib_dir_name: str) -> set[str]:
    source_module_names = (
        "artifact_bundle",
        "claim_coverage",
        "cochain_presentation",
        "covering_edge",
        "evidence",
        "exact",
        "family_bound",
        "falsification_sandbox",
        "inline_code_companion",
        "observer_carriers",
        "quantum_lattice",
        "replay",
        "replica_hierarchy",
        "retraction_geometry",
        "transfer",
        "worked_examples",
        "lattice_simulation",
        "generate_figures",
        "short_time_defect_numerical_certificate",
        "so_k_3cell_benchmark",
    )
    test_module_names = (
        "test_po000_core",
        "test_po000_unit",
        "test_po000_soviet_deep_coverage",
        "test_po000_integration",
        "test_po000_e2e",
        "test_short_time_defect_numerical_certificate",
        "test_so_k_3cell_benchmark",
    )

    res: set[str] = set()
    lib_dir = pkg_root / lib_dir_name
    for name in source_module_names:
        flat = lib_dir / f"{name}.py"
        if flat.is_file():
            res.add(flat.relative_to(pkg_root).as_posix())
        else:
            matches = [p for p in lib_dir.rglob(f"{name}.py") if p.is_file()]
            if matches:
                res.add(matches[0].relative_to(pkg_root).as_posix())

    for test_name in test_module_names:
        for parent_dir in (
            lib_dir / "tests",
            pkg_root / "tests" / "unit",
            pkg_root / "tests" / "integration",
            pkg_root / "tests" / "e2e",
            pkg_root / "_tests_unit",
            pkg_root / "_tests_integration",
            pkg_root / "_tests_e2e",
        ):
            candidate = parent_dir / f"{test_name}.py"
            if candidate.is_file():
                res.add(candidate.relative_to(pkg_root).as_posix())
                break

    for doc_name in ("000_mutation_audit.md", "000_nonclaims.md", "000_python_mechanization_notes.md"):
        for doc_dir in (pkg_root / "docs", pkg_root / "_docs"):
            candidate = doc_dir / doc_name
            if candidate.is_file():
                res.add(candidate.relative_to(pkg_root).as_posix())
                break

    if (pkg_root / "pyproject.toml").is_file():
        res.add("pyproject.toml")

    vc = lib_dir / "projection_obstruction" / "verify_certificate.py"
    if vc.is_file():
        res.add(vc.relative_to(pkg_root).as_posix())
    elif (lib_dir / "certificate" / "verify_certificate.py").is_file():
        res.add((lib_dir / "certificate" / "verify_certificate.py").relative_to(pkg_root).as_posix())
    elif (lib_dir / "verify_certificate.py").is_file():
        res.add(f"{lib_dir_name}/verify_certificate.py")
    elif (pkg_root / "verify_certificate.py").is_file():
        res.add("verify_certificate.py")

    return res

REQUIRED_SOURCE_PATHS = _resolve_required_source_paths(_pkg_root, _lib_dir_name)
REQUIRED_PUBLICATION_PATHS = {
    "projection_obstruction_paper.md",
    "000_projection_obstruction_claim_ledger.md",
    "000_projection_obstruction_change_log.md",
    "projection_obstruction_paper.pdf",
    "projection_obstruction_paper.tex",
    "PO000_ENVIRONMENT_RECEIPT.json",
    "PO000_REPRODUCTION_REQUIREMENTS.txt",
    "PO000_LEAN_axiom_report.txt",
    "PO000_LICENSE.md",
    "PO000_RELEASE_NOTES.md",
    "PO000_RELEASE_README.md",
    "PO000_ZENODO_METADATA.json",
    "verify_po000_release.py",
}

TOP_LEVEL_FIELDS = {
    "schema_version",
    "paper_id",
    "paper_version",
    "python_package_version",
    "results",
    "unresolved_claim_ids",
    "source_hashes",
    "publication_hashes",
    "execution_completed",
    "executable_checks_passed",
    "open_obligations_present",
    "refusals_present",
    "claim_disposition_complete",
    "promotion_eligible",
    "authority_effect",
}
RESULT_FIELDS = {
    "claim_ids",
    "title",
    "evidence_kind",
    "verdict",
    "statement_scope",
    "algorithm",
    "witness",
    "limitations",
    "authority_effect",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_hash_inventory(
    value: Any,
    *,
    required_paths: set[str],
    root: Path,
    field_name: str,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict) or (not value and required_paths):
        return [f"{field_name} must be a nonempty object"]
    if not all(isinstance(key, str) and isinstance(digest, str) for key, digest in value.items()):
        return [f"{field_name} keys and values must be strings"]

    actual_paths = set(value)
    missing_paths = required_paths - actual_paths
    extra_paths = actual_paths - required_paths
    if missing_paths:
        errors.append(f"{field_name} inventory missing: {sorted(missing_paths)}")
    if extra_paths:
        errors.append(f"{field_name} inventory has unexpected paths: {sorted(extra_paths)}")

    resolved_root = root.resolve()
    for relative in sorted(required_paths & actual_paths):
        expected = value[relative]
        if len(expected) != 64 or any(
            character not in "0123456789abcdef" for character in expected
        ):
            errors.append(f"invalid SHA-256 digest for {field_name}.{relative}")
            continue
        candidate = (resolved_root / relative).resolve()
        try:
            candidate.relative_to(resolved_root)
        except ValueError:
            errors.append(f"{field_name} path escapes its root: {relative}")
            continue
        if not candidate.is_file():
            errors.append(f"hashed file is missing: {field_name}.{relative}")
        elif sha256(candidate) != expected:
            errors.append(f"hash mismatch: {field_name}.{relative}")
    return errors


def verify_document(data: Any, package_root: Path) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["top-level JSON value must be an object"]
    if data.get("schema_version") != "po000.mechanization_run.v3":
        errors.append("unexpected schema_version")

    extra_top_level = set(data) - TOP_LEVEL_FIELDS
    missing_top_level = TOP_LEVEL_FIELDS - set(data)
    if extra_top_level:
        errors.append(f"unknown top-level fields: {sorted(extra_top_level)}")
    if missing_top_level:
        errors.append(f"missing top-level fields: {sorted(missing_top_level)}")
    if data.get("paper_version") != "6.0":
        errors.append("paper_version must be 6.0")
    if data.get("python_package_version") != "6.1.1":
        errors.append("python_package_version must be 6.1.1")
    if data.get("paper_id") != "PO-000":
        errors.append("unexpected paper_id")
    if data.get("authority_effect") != "None":
        errors.append("authority_effect must be the literal string None")

    results = data.get("results")
    unresolved = data.get("unresolved_claim_ids")
    if not isinstance(results, list):
        errors.append("results must be a list")
        results = []
    if not isinstance(unresolved, list) or not all(isinstance(item, str) for item in unresolved):
        errors.append("unresolved_claim_ids must be a list of strings")
        unresolved = []

    unresolved_set = set(unresolved)
    if len(unresolved_set) != len(unresolved):
        errors.append("unresolved_claim_ids contains duplicates")
    unknown_unresolved = unresolved_set - REQUIRED_CLAIMS
    if unknown_unresolved:
        errors.append(f"unresolved_claim_ids contains unknown claims: {sorted(unknown_unresolved)}")

    owners: dict[str, int] = {}
    observed: set[str] = set()
    dispositions: dict[str, tuple[Any, Any]] = {}
    for index, result in enumerate(results):
        prefix = f"results[{index}]"
        if not isinstance(result, dict):
            errors.append(f"{prefix} must be an object")
            continue
        extra_result = set(result) - RESULT_FIELDS
        missing_result = RESULT_FIELDS - set(result)
        if extra_result:
            errors.append(f"{prefix} has unknown fields: {sorted(extra_result)}")
        if missing_result:
            errors.append(f"{prefix} is missing fields: {sorted(missing_result)}")
        if result.get("authority_effect") != "None":
            errors.append(f"{prefix}.authority_effect must be None")
        if result.get("evidence_kind") not in KNOWN_KINDS:
            errors.append(f"{prefix}.evidence_kind is unknown")
        verdict = result.get("verdict")
        if verdict not in KNOWN_VERDICTS:
            errors.append(f"{prefix}.verdict is unknown")
        if verdict == "fail":
            errors.append(f"{prefix} records a failed executable check")
        for field in ("title", "statement_scope", "algorithm"):
            if not isinstance(result.get(field), str) or not result.get(field):
                errors.append(f"{prefix}.{field} must be a nonempty string")
        if not isinstance(result.get("witness"), dict):
            errors.append(f"{prefix}.witness must be an object")
        limitations = result.get("limitations")
        if not isinstance(limitations, list) or not all(
            isinstance(item, str) for item in limitations
        ):
            errors.append(f"{prefix}.limitations must be a list of strings")
        claim_ids = result.get("claim_ids")
        if (
            not isinstance(claim_ids, list)
            or not claim_ids
            or not all(isinstance(item, str) for item in claim_ids)
        ):
            errors.append(f"{prefix}.claim_ids must be a nonempty list of strings")
        else:
            if len(set(claim_ids)) != len(claim_ids):
                errors.append(f"{prefix}.claim_ids contains duplicates")
            unknown = set(claim_ids) - REQUIRED_CLAIMS
            if unknown:
                errors.append(f"{prefix}.claim_ids contains unknown claims: {sorted(unknown)}")
            for claim_id in claim_ids:
                previous = owners.get(claim_id)
                if previous is not None:
                    errors.append(
                        f"claim {claim_id!r} appears in both results[{previous}] and {prefix}"
                    )
                else:
                    owners[claim_id] = index
                    dispositions[claim_id] = (result.get("evidence_kind"), result.get("verdict"))
            observed.update(claim_ids)

    missing = REQUIRED_CLAIMS - observed
    if missing:
        errors.append(f"claim coverage missing: {sorted(missing)}")
    if unresolved_set != REQUIRED_GENERAL_UNRESOLVED:
        errors.append(
            "unresolved general-theorem set mismatch; "
            f"missing={sorted(REQUIRED_GENERAL_UNRESOLVED - unresolved_set)}, "
            f"extra={sorted(unresolved_set - REQUIRED_GENERAL_UNRESOLVED)}"
        )
    for claim_id, expected_kind in EXPECTED_EVIDENCE_KINDS.items():
        if claim_id not in dispositions:
            continue
        actual_kind, actual_verdict = dispositions[claim_id]
        if actual_kind != expected_kind:
            errors.append(
                f"claim {claim_id} evidence_kind must be {expected_kind}, got {actual_kind}"
            )
        expected_verdict = EXPECTED_VERDICTS[claim_id]
        if actual_verdict != expected_verdict:
            errors.append(
                f"claim {claim_id} verdict must be {expected_verdict}, got {actual_verdict}"
            )

    expected_executable_pass = all(
        result.get("verdict") != "fail"
        for result in results
        if isinstance(result, dict)
    )

    expected_refusals = any(
        result.get("verdict") == "refused"
        for result in results
        if isinstance(result, dict)
    )

    expected_open = bool(unresolved) or any(
        result.get("verdict") == "open"
        for result in results
        if isinstance(result, dict)
    )

    expected_complete = (observed == REQUIRED_CLAIMS)

    if data.get("execution_completed") is not True:
        errors.append("execution_completed must be true")

    if data.get("executable_checks_passed") is not expected_executable_pass:
        errors.append("executable_checks_passed is inconsistent with result verdicts")

    if data.get("refusals_present") is not expected_refusals:
        errors.append("refusals_present is inconsistent with result verdicts")

    if data.get("open_obligations_present") is not expected_open:
        errors.append("open_obligations_present is inconsistent with unresolved/open claims")

    if data.get("claim_disposition_complete") is not expected_complete:
        errors.append("claim_disposition_complete is inconsistent with claim coverage")

    if data.get("promotion_eligible") is not False:
        errors.append("promotion_eligible must be false")

    root = package_root.resolve()
    pub_root = root if (root / "projection_obstruction_paper.md").exists() else root.parent
    req_pub = {p for p in REQUIRED_PUBLICATION_PATHS if (pub_root / p).exists()}
    req_src = {p for p in REQUIRED_SOURCE_PATHS if (root / p).exists()}
    errors.extend(
        verify_hash_inventory(
            data.get("source_hashes"),
            required_paths=req_src,
            root=root,
            field_name="source_hashes",
        )
    )
    errors.extend(
        verify_hash_inventory(
            data.get("publication_hashes"),
            required_paths=req_pub,
            root=pub_root,
            field_name="publication_hashes",
        )
    )
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args(argv)
    certificate = args.certificate.resolve()
    try:
        data = json.loads(certificate.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"verdict": "fail", "errors": [str(exc)], "authority_effect": "None"}))
        return 1
    pkg_root = _resolve_po000_package_root(Path(__file__).resolve().parent)
    errors = verify_document(data, pkg_root)
    print(
        json.dumps(
            {
                "verdict": "pass" if not errors else "fail",
                "errors": errors,
                "authority_effect": "None",
            },
            sort_keys=True,
        )
    )
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

