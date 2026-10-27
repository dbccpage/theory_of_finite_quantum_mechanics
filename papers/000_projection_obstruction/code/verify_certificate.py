#!/usr/bin/env python3
"""Independent verifier: core records use stdlib; finite supplements declare capabilities."""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import tomllib
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
# 2026-09-03: this was a hand-maintained 47-id set whose ``H`` group stopped at
# H7, duplicating the same stale universe the producer carried -- so the
# "independent" verifier would have accepted a receipt that ignored
# ``E4-second``, ``E4-commutator``, ``H8`` and ``H9`` too.  It now reads the
# markdown ledger directly.  This keeps the verifier independent of the
# producer (it shares no code with ``evidence.py``) while both answer to the
# same declared authority.  It fails closed: no ledger, no verification.
_LEDGER_ROW = re.compile(r"^\|\s*`?([A-Z](?:\d+[A-Za-z0-9\-]*|-[A-Z][A-Z0-9\-]*))`?\s*\|", re.MULTILINE)


def _claims_from_ledger() -> set[str]:
    ledger = Path(__file__).resolve().parents[1] / "projection_obstruction_claim_ledger.md"
    if not ledger.is_file():
        raise FileNotFoundError(f"claim ledger required for verification: {ledger}")
    ids = {cid for cid in _LEDGER_ROW.findall(ledger.read_text(encoding="utf-8"))
           if not cid.startswith("P001-")}
    if not ids:
        raise ValueError(f"no claim rows parsed from {ledger}")
    return ids


# Independently retain the legacy scope plus the new written theorem groups.
REQUIRED_CLAIMS = _claims_from_ledger() | {
    "V68-CANCELLATION", "V68-LOCAL-ZERO", "V68-PHYSICAL",
    "V69-JORDAN", "V69-SELECTOR", "V6914-TRACE", "V6914-CENTER",
}

# Independently pinned: a finite example must not promote these general claims.
# Lemmas 3.6-3.14 are written proofs. The Python package does not witness them.
_CHART_PROSE_CLAIMS = (
    "C4d",
    "C4e",
    "C4f",
    "C4g",
    "C4h",
    "C4i",
    "C4j",
    "C4k",
    "C4l",
)
PROSE_SUPPLEMENT_CLAIMS = (
    'E-LIMITS', 'V65-METRIC', 'V65-PURE', 'V65-SUPPORT', 'V65-CUMULANT',
    'V65-DENSITY', 'V65-PHASE', 'V65-PREDICTION', 'V65-OBSERVABILITY',
    'V65-EXTENSION', 'V66-ONSET', 'V66-APPLICATIONS', 'V68-CANCELLATION',
    'V68-LOCAL-ZERO', 'V68-PHYSICAL', 'V69-JORDAN', 'V69-SELECTOR',
    'V6914-TRACE', 'V6914-CENTER',
)

REQUIRED_GENERAL_UNRESOLVED = {
    *PROSE_SUPPLEMENT_CLAIMS,
    # 2026-09-03: E4-second, E4-commutator, H8 and H9 joined the universe with
    # PROSE_OR_LEAN status, so they are unresolved for Python by construction.
    "E4-second",
    "E4-commutator",
    "H8",
    "H9",
    "P4-7",
    "E3-general",
    "E4-general",
    "A1",
    "C1",
    "C2",
    "C4a",
    "C4b",
    "C4c",
    *_CHART_PROSE_CLAIMS,
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
    **dict.fromkeys(PROSE_SUPPLEMENT_CLAIMS, "not_executable"),
    **dict.fromkeys(("D6", "H5", "C4"), "counterexample"),
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
    **dict.fromkeys(("B3", "C1", "C4a", "C4b", "C4c", "E1"), "exact_symbolic_instance"),
    **dict.fromkeys(_CHART_PROSE_CLAIMS, "not_executable"),
    **dict.fromkeys(("D1", "D3", "D4"), "finite_exhaustive"),
    # 2026-09-03: E4-second, E4-commutator, H8 and H9 joined the claim
    # universe but had no expected disposition here, so the verifier accepted
    # any evidence_kind/verdict for them -- a deliberately wrong
    # numerical_replay/pass passed clean.  They are Lean-resident refusals.
    **dict.fromkeys(
        ("B4", "C2", "E3", "G2",
         "E4-second", "E4-commutator", "H8", "H9",
         "P4-7", "E3-general", "E4-general"),
        "not_executable",
    ),
    **dict.fromkeys(("E2", "E4", "F1", "F2"), "numerical_replay"),
    **dict.fromkeys(("A1", "F3"), "premise_check"),
    **dict.fromkeys(
        # D8a added 2026-09-03: it is the repairable-mass scope fence, and
        # was previously unpinned here as well as mis-bound in the producer.
        ("A4", "A5", "A6", "A7", "C3", "D7", "D8a", "E6", "E7", "G3", "G4"),
        "static_scope_fence",
    ),
}
EXPECTED_VERDICTS = {
    claim_id: "refused" if kind == "not_executable" else "pass"
    for claim_id, kind in EXPECTED_EVIDENCE_KINDS.items()
}

# 2026-09-03: the disposition loop below skips claims absent from this table,
# so a claim missing here is silently unverifiable rather than rejected.  That
# is how D8a and the four Lean-resident rows went unchecked.  Refuse to load
# at all if the table does not pin every claim in the universe.
_unpinned = REQUIRED_CLAIMS - set(EXPECTED_EVIDENCE_KINDS)
if _unpinned:
    raise SystemExit(
        "verify_certificate: no expected disposition for "
        f"{sorted(_unpinned)}; every claim in the ledger must be pinned here"
    )
# 2026-08-31: this deposit's only layout is code/ with tests under
# code/tests/.  The former src/po000 and tests/unit branches described a
# migration that was never applied here and are removed.  The inventory
# below names every shipping module (including the three that were
# previously missing: authorization_boundary, eval_auth_factor,
# projection_factor_experiment; plus the new stdlib engine exactsym) and
# every shipping test file, so replay.source_hashes and this set agree.
REQUIRED_SOURCE_PATHS = {
    "code/residual_error_budget.py",
    "code/tests/test_residual_error_budget.py",
    *(
        f"code/{name}.py"
        for name in (
            "artifact_bundle",
            "authorization_boundary",
            "calibration_quotient",
            "claim_coverage",
            "cochain_presentation",
            "covering_edge",
            "derivation_replays",
            "entanglement_production",
            "eval_auth_factor",
            "evidence",
            "exact",
            "exact_graph_state_separation",
            "exactsym",
            "falsification_sandbox",
            "family_bound",
            "feasible_tangent_cone",
            "ffi",
            "finite_certificates",
            "finite_inputs",
            "inline_code_companion",
            "jordan_lie_countermodels",
            "krylov_scaling_benchmark",
            "local_persistent_zero",
            "observable_duhamel",
            "observation_tradeoffs",
            "observer_carriers",
            "open_system_jets",
            "physical_obstruction",
            "polynomial_onset",
            "projection_factor_experiment",
            "quantum_lattice",
            "replay",
            "replica_hierarchy",
            "retraction_geometry",
            "short_time_defect_numerical_certificate",
            "short_time_jets",
            "so_k_3cell_benchmark",
            "transfer",
            "verify_certificate",
            "verify_finite_certificates",
            "worked_examples",
        )
    ),
    *(
        f"code/tests/{name}.py"
        for name in (
            "test_authorization_boundary",
            "test_calibration_quotient",
            "test_connected_cumulants",
            "test_entanglement_production",
            "test_eval_auth_factor",
            "test_exact_engine_edges",
            "test_exact_graph_state_separation",
            "test_fault_injection_guards",
            "test_feasible_tangent_cone",
            "test_figures_match_claims",
            "test_finite_certificates",
            "test_honeycomb_tdvp_duhamel_integration",
            "test_jordan_lie_countermodels",
            "test_krylov_regressions",
            "test_krylov_scaling_benchmark",
            "test_local_persistent_zero",
            "test_metric_phase_derivations",
            "test_notebook_portability",
            "test_observable_duhamel",
            "test_observable_duhamel_certification_boundary",
            "test_observation_tradeoffs",
            "test_open_system_jets",
            "test_paper_artifacts",
            "test_physical_obstruction",
            "test_po000_core",
            "test_po000_e2e",
            "test_po000_e2e_extension",
            "test_po000_integration",
            "test_po000_soviet_deep_coverage",
            "test_po000_soviet_extensions",
            "test_po000_unit",
            "test_polynomial_onset",
            "test_projection_factor_experiment",
            "test_publication_verification",
            "test_quantum_selector",
            "test_release_packaging",
            "test_republication_review_regressions",
            "test_sharp_onset",
            "test_short_time_defect_numerical_certificate",
            "test_short_time_jets",
            "test_so_k_3cell_benchmark",
            "test_tangent_certification_boundary",
            "test_theorem_falsification",
            "test_verifier_mutations",
        )
    ),
    "pyproject.toml",
}
# 2026-08-31: names track the current files (the paper and its ledgers lost
# their 000_ prefixes); this set must mirror replay.publication_hashes.
# 2026-08-31 (second pass): the set previously mixed files this deposit
# actually ships with release-build products that do not exist here, and the
# verifier silently filtered its own requirements to files that exist — so a
# required-but-missing file shrank the contract instead of failing it.  The
# split below is now explicit: REQUIRED paths must exist and be hashed;
# OPTIONAL paths are hashed only when present, and each carries a comment
# saying why absence is legitimate.  ``verify_po000_release.py`` is removed
# entirely (not even optional): the paper disclaims that script, and keeping
# it in the inventory meant a stray file dropped at that name would be
# silently hashed into the publication surface.
REQUIRED_PUBLICATION_PATHS = {
    "projection_obstruction.md",
    "projection_obstruction_claim_ledger.md",
    # 2026-09-03: the machine-readable ledger is now bound by the receipt.
    "projection_obstruction_claim_ledger.yaml",
    "projection_obstruction_change_log.md",
    # 2026-09-03: bound because the scope-fence receipt reads it.
    "README.md",
    "docs/claim_dependencies.json",
    "release_identity.json",
}

OPTIONAL_PUBLICATION_PATHS = {
    # Rendered-paper build products; the deposit ships the Markdown source
    # and does not require a local TeX toolchain.
    "projection_obstruction.pdf",
    "projection_obstruction.tex",
    # Release-packaging artifacts produced only by the (historical) archive
    # release flow; no v6.3 deposit builds them.
    "PO000_ENVIRONMENT_RECEIPT.json",
    "PO000_REPRODUCTION_REQUIREMENTS.txt",
    "PO000_LEAN_AXIOM_REPORT.txt",
    "PO000_LICENSE.md",
    "PO000_RELEASE_NOTES.md",
    "PO000_RELEASE_README.md",
    "PO000_ZENODO_METADATA.json",
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
    "finite_certificates",
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


def _unique_identity_fields(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate release identity field")
        result[key] = value
    return result


def _verify_identity_header(package_root: Path, identity: dict[str, Any]) -> None:
    source = (package_root / "projection_obstruction.md").read_text(encoding="utf-8")
    end = source.find("</div>")
    if end == -1:
        raise ValueError("canonical manuscript header is missing")
    for field, expected in (("Version", identity["manuscript_version"]),
                            ("Date", identity["release_date"])):
        observed = re.findall(r"^\*\*" + field + r":\*\*[ \t]*(\S+)[ \t]*$",
                              source[:end], flags=re.MULTILINE)
        if len(observed) != 1 or observed[0] != expected:
            raise ValueError(f"manuscript header differs from release identity: {field}")


def verify_release_identity(data: dict[str, Any], package_root: Path) -> list[str]:
    """Independently check the identity contract; import no producer validators."""
    try:
        identity = json.loads(
            (package_root / "release_identity.json").read_text(encoding="utf-8"),
            object_pairs_hook=_unique_identity_fields,
        )
        if not isinstance(identity, dict) or identity.get("schema") != "po000.release_identity.v1":
            raise ValueError("invalid release identity schema")
        for key in ("manuscript_version", "code_version", "release_version"):
            if not isinstance(identity.get(key), str) or re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", identity[key]) is None:
                raise ValueError(f"invalid release identity: {key}")
        if identity["release_version"] != identity["manuscript_version"]:
            raise ValueError("manuscript and release versions differ")
        date = identity.get("release_date")
        if not isinstance(date, str) or datetime.date.fromisoformat(date).isoformat() != date:
            raise ValueError("invalid release identity date")
        if identity.get("authority_effect") != "None":
            raise ValueError("invalid release identity authority_effect")
        if not isinstance(identity.get("status"), str) or not identity["status"].strip():
            raise ValueError("invalid release identity status")
        project = tomllib.loads((package_root / "pyproject.toml").read_text(encoding="utf-8"))
        metadata = project.get("project")
        if not isinstance(metadata, dict) or metadata.get("version") != identity["code_version"]:
            raise ValueError("release identity code version differs from pyproject.toml")
        _verify_identity_header(package_root, identity)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return [f"missing or malformed release_identity.json: {exc}"]
    return [
        f"{receipt_key} must match release_identity.json: {identity[identity_key]}"
        for receipt_key, identity_key in (
            ("paper_version", "manuscript_version"), ("python_package_version", "code_version")
        )
        if data.get(receipt_key) != identity[identity_key]
    ]


def verify_hash_inventory(
    value: Any,
    *,
    required_paths: set[str],
    root: Path,
    field_name: str,
    optional_paths: set[str] = frozenset(),  # type: ignore[assignment]
) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict) or not value:
        return [f"{field_name} must be a nonempty object"]
    if not all(isinstance(key, str) and isinstance(digest, str) for key, digest in value.items()):
        return [f"{field_name} keys and values must be strings"]

    actual_paths = set(value)
    missing_paths = required_paths - actual_paths
    extra_paths = actual_paths - required_paths - set(optional_paths)
    if missing_paths:
        errors.append(f"{field_name} inventory missing: {sorted(missing_paths)}")
    if extra_paths:
        errors.append(f"{field_name} inventory has unexpected paths: {sorted(extra_paths)}")

    resolved_root = root.resolve()
    for relative in sorted((required_paths | set(optional_paths)) & actual_paths):
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
    if data.get("schema_version") != "po000.mechanization_run.v4":
        errors.append("unexpected schema_version")

    extra_top_level = set(data) - TOP_LEVEL_FIELDS
    missing_top_level = TOP_LEVEL_FIELDS - set(data)
    if extra_top_level:
        errors.append(f"unknown top-level fields: {sorted(extra_top_level)}")
    if missing_top_level:
        errors.append(f"missing top-level fields: {sorted(missing_top_level)}")
    errors.extend(verify_release_identity(data, package_root))
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
        witness = result.get("witness")
        if not isinstance(witness, dict):
            errors.append(f"{prefix}.witness must be an object")
        elif verdict == "pass":
            if not witness:
                errors.append(
                    f"{prefix}.witness must be a nonempty object for passing executable check"
                )
            else:
                # Mathematical witness sanity & non-negativity checks
                for norm_key in ("raw_I", "bound", "norm", "coboundary_norm", "distance"):
                    if norm_key in witness:
                        val_str = str(witness[norm_key]).strip()
                        try:
                            if float(val_str) < 0.0:
                                errors.append(
                                    f"{prefix}.witness.{norm_key} must be non-negative, got {val_str}"
                                )
                        except ValueError:
                            pass

                # Claim-specific witness reconstruction & predicate checks
                res_claim_ids = result.get("claim_ids")
                if isinstance(res_claim_ids, list):
                    if "B1" in res_claim_ids or "B2" in res_claim_ids:
                        for req_fld in ("defect", "raw_I", "bound"):
                            if req_fld not in witness:
                                errors.append(
                                    f"{prefix}.witness missing required covering-edge field {req_fld!r}"
                                )
                        if "raw_I" in witness and "bound" in witness:
                            try:
                                raw_val = float(witness["raw_I"])
                                bound_val = float(witness["bound"])
                                if raw_val < 0.0 or bound_val < 0.0:
                                    errors.append(
                                        f"{prefix}.witness: raw_I and bound must be non-negative"
                                    )
                                elif raw_val > bound_val:
                                    errors.append(
                                        f"{prefix}.witness: raw_I ({witness['raw_I']}) exceeds bound ({witness['bound']})"
                                    )
                            except ValueError:
                                pass
                        if "defect" in witness:
                            defect_repr = str(witness["defect"]).strip()
                            if "2" not in defect_repr:
                                errors.append(
                                    f"{prefix}.witness.defect ({defect_repr}) does not match declared covering-edge defect"
                                )
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
    pub_root = root if (root / "projection_obstruction.md").exists() else root.parent
    # 2026-08-31: requirements are no longer filtered to files that exist.
    # A required-but-missing file now FAILS verification (reported twice, by
    # design: once as an inventory omission if the certificate also lacks it,
    # and once as a missing hashed file if the certificate still lists it).
    errors.extend(
        verify_hash_inventory(
            data.get("source_hashes"),
            required_paths=set(REQUIRED_SOURCE_PATHS),
            root=root,
            field_name="source_hashes",
        )
    )
    errors.extend(
        verify_hash_inventory(
            data.get("publication_hashes"),
            required_paths=set(REQUIRED_PUBLICATION_PATHS),
            root=pub_root,
            field_name="publication_hashes",
            optional_paths=set(OPTIONAL_PUBLICATION_PATHS),
        )
    )
    if not errors:
        from verify_finite_certificates import verify_finite_records
        errors.extend(verify_finite_records(data["finite_certificates"]))
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
    pkg_dir = Path(__file__).resolve().parent
    pkg_root = pkg_dir.parent if pkg_dir.name == "code" else pkg_dir
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
