from __future__ import annotations

import hashlib
import json
import re
import runpy
import subprocess
import sys
from pathlib import Path

import pytest
from witnessed_difference.claims import load_claim_map, validate_claim_map

ROOT = Path(__file__).resolve().parents[4]
CANONICAL_LEDGER_BEGIN = "<!-- CANONICAL-CLAIM-TABLE:BEGIN -->"
CANONICAL_LEDGER_END = "<!-- CANONICAL-CLAIM-TABLE:END -->"


def _canonical_ledger_section(text: str) -> str:
    assert text.count(CANONICAL_LEDGER_BEGIN) == 1
    assert text.count(CANONICAL_LEDGER_END) == 1
    start = text.index(CANONICAL_LEDGER_BEGIN) + len(CANONICAL_LEDGER_BEGIN)
    stop = text.index(CANONICAL_LEDGER_END, start)
    return text[start:stop]


def _canonical_ledger_rows(ledger_text: str) -> list[dict[str, str]]:
    section = _canonical_ledger_section(ledger_text)
    rows: list[dict[str, str]] = []
    for line in section.splitlines():
        if line.startswith("| WDP-CH"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                claim_id = parts[1]
                status = parts[2]
                if re.fullmatch(r"WDP-CH\d{2}-[DPCON]\d{2}", claim_id):
                    rows.append({"claim_id": claim_id, "status": status})
    return rows


def test_claim_code_map_is_a_bijection_from_unique_ids_to_real_code_and_tests() -> None:
    records = load_claim_map(ROOT / "manifests" / "claim_code_map.json")
    ledger_text = (ROOT / "witnessed_difference_programme_claim_ledger.md").read_text(encoding="utf-8")
    registry = _canonical_ledger_rows(ledger_text)
    registry_by_id = {item["claim_id"]: item for item in registry}
    registry_ids = [item["claim_id"] for item in registry]
    manuscript = (ROOT / "witnessed_difference_programme.md").read_text(encoding="utf-8")
    prose_ids = re.findall(
        r"WDP-CH\d{2}-[DPCON]\d{2}",
        manuscript,
    )
    assert len(registry) == 154
    assert len(set(registry_ids)) == 154
    canonical_ids = set(registry_ids)
    canonical_prose_ids = [claim_id for claim_id in prose_ids if claim_id in canonical_ids]
    assert len(canonical_prose_ids) == len(set(canonical_prose_ids)) == 154
    assert set(canonical_prose_ids) == canonical_ids
    # Later imported chapters are outside the sealed 154-row claim registry.
    # Their presence must not promote them into its status/evidence coverage.
    postcanonical_ids = set(prose_ids) - canonical_ids
    assert all(int(claim_id[6:8]) >= 22 for claim_id in postcanonical_ids)
    lean_ids = re.findall(
        r"WDP-CH\d{2}-[DPCON]\d{2}",
        (ROOT / "lean4" / "claim_map.md").read_text(encoding="utf-8"),
    )
    assert len(lean_ids) == len(set(lean_ids)) == 154
    assert set(lean_ids) == canonical_ids
    ledger_ids = re.findall(
        r"WDP-CH\d{2}-[DPCON]\d{2}",
        _canonical_ledger_section(ledger_text),
    )
    assert len(ledger_ids) == len(set(ledger_ids)) == 154
    assert set(ledger_ids) == canonical_ids
    assert len(records) >= 12
    assert validate_claim_map(records, ROOT) == ()
    assert len({record.claim_id for record in records}) == len(records)
    assert {record.claim_id for record in records}.issubset(canonical_ids)
    for record in records:
        assert record.status.value == registry_by_id[record.claim_id]["status"]
        if record.status.value in {"OPEN_CLAIM", "OPEN_INTERFACE", "NONCLAIM"}:
            assert any(
                marker in record.evidence_type
                for marker in ("scope", "refusal", "firewall", "nonclaim")
            )


def test_figure_manifest_hashes_assets_and_labels_conceptual_art_non_evidentiary() -> None:
    payload = json.loads((ROOT / "manifests" / "figure_manifest.json").read_text(encoding="utf-8"))
    assert payload["authority_effect"] == "None"
    conceptual = [item for item in payload["figures"] if item["role"] == "conceptual_art"]
    assert len(conceptual) == 1
    assert conceptual[0]["deterministic"] is False
    assert "non-evidentiary" in conceptual[0]["caption"]
    for item in payload["figures"]:
        path = ROOT / item["path"]
        if item.get("present", True):
            assert path.is_file()
            assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"]
        assert item["alt_text"] and item["caption"]


def test_reproduction_status_does_not_promote_bindings_to_execution() -> None:
    validate = runpy.run_path(str(ROOT / "scripts" / "verify_claim_map.py"))[
        "validate_reproduction_inventory"
    ]
    # A written proof can have neither a formalization nor a replay.
    canonical = {"WDP-CH04-P01": {"status": "FINITE_PROPOSITION", "evidence": "P"}}
    ledger = """<!-- REPRODUCTION-TABLE:BEGIN -->
| CH04-P01 | NONE_BOUND | INCOMPLETE | PAIRED_REPLAY_PENDING |
<!-- REPRODUCTION-TABLE:END -->"""
    assert validate(ledger, canonical) == []
    forged = ledger.replace("PAIRED_REPLAY_PENDING", "RECORDED_PAIRED_PASS_2026-10-09")
    assert any("lacks exact Lean and Python" in error for error in validate(forged, canonical))
    # Even complete bindings may correctly remain pending.
    canonical["WDP-CH04-P01"]["evidence"] = "P; C; L:exact(example)"
    pending = ledger.replace("NONE_BOUND", "EXACT_DECLARATION").replace("INCOMPLETE", "COMPLETE")
    assert validate(pending, canonical) == []
    assert validate(pending.replace("PAIRED_REPLAY_PENDING", "PASS"), canonical)


def test_notebook_manifest_and_sources_are_deterministic_output_free_lessons() -> None:
    payload = json.loads((ROOT / "manifests" / "notebook_manifest.json").read_text(encoding="utf-8"))
    assert payload["authority_effect"] == "None"
    ledger_text = (ROOT / "witnessed_difference_programme_claim_ledger.md").read_text(encoding="utf-8")
    canonical_rows = _canonical_ledger_rows(ledger_text)
    canonical_ids = {row["claim_id"] for row in canonical_rows}
    canonical_statuses = {row["claim_id"]: row["status"] for row in canonical_rows}
    assert len(canonical_rows) == len(canonical_ids) == payload["canonical_claim_count"] == 154
    canonical_serialization = ("\n".join(sorted(canonical_ids)) + "\n").encode("utf-8")
    assert hashlib.sha256(canonical_serialization).hexdigest() == payload["canonical_claim_set_sha256"]
    assert len(payload["notebooks"]) == 10
    assert payload["curriculum_order"] == [
        "000_primitive_difference",
        "010_cochains_and_vector_obstruction",
        "020_retention_and_reaccess",
        "030_observer_representations",
        "040_observation_to_measurement",
        "050_duration_and_finite_probability",
        "060_bounded_history_sums",
        "070_declared_u1_holonomy",
        "080_claim_status_and_receipts",
        "090_mutation_recovery_and_scope",
    ]
    expected_claim_ids = {
        "000_primitive_difference": ["WDP-CH01-D01", "WDP-CH01-P01", "WDP-CH03-P01"],
        "010_cochains_and_vector_obstruction": ["WDP-CH04-P02", "WDP-CH04-C01", "WDP-CH04-P07", "WDP-CH07-P02"],
        "020_retention_and_reaccess": ["WDP-CH02-P01", "WDP-CH02-N01", "WDP-CH03-O02"],
        "030_observer_representations": ["WDP-CH10-D01", "WDP-CH10-D03", "WDP-CH10-O01"],
        "040_observation_to_measurement": ["WDP-CH12-D01", "WDP-CH12-P01", "WDP-CH13-D01", "WDP-CH13-N01"],
        "050_duration_and_finite_probability": ["WDP-CH07-D01", "WDP-CH07-P01", "WDP-CH08-P01", "WDP-CH09-N01"],
        "060_bounded_history_sums": ["WDP-CH17-P01", "WDP-CH17-P02", "WDP-CH17-N01"],
        "070_declared_u1_holonomy": ["WDP-CH05-D01", "WDP-CH05-P01", "WDP-CH05-N01"],
        "080_claim_status_and_receipts": ["WDP-CH20-D01", "WDP-CH20-O01", "WDP-CH20-N01"],
        "090_mutation_recovery_and_scope": ["WDP-CH00-N03", "WDP-CH20-N01", "WDP-CH22-C01"],
    }
    index_path = ROOT / payload["index_path"]
    assert index_path.is_file()
    assert hashlib.sha256(index_path.read_bytes()).hexdigest() == payload["index_sha256"]
    index_text = index_path.read_text(encoding="utf-8")
    levels = [item["level"] for item in payload["notebooks"]]
    assert levels[0] == "Novice" and levels[-1] == "Deep expert"
    assert sum(item["interactive_html_widget"] for item in payload["notebooks"]) == 1
    for sequence, item in enumerate(payload["notebooks"]):
        path = ROOT / item["path"]
        assert path.name.startswith(f"{sequence * 10:03d}_")
        assert not path.name.startswith("reviewer_")
        assert "_qm_" not in path.name
        assert f"]({path.name})" in index_text
        assert item["sequence"] == sequence
        assert item["claim_ids"] == expected_claim_ids[path.stem]
        assert len(item["learning_objectives"]) == 3
        assert item["claim_ids"]
        assert item["cell_count"] >= 10
        assert item["code_cell_count"] >= 4
        for asset in item["generated_assets"]:
            assert (ROOT / asset).is_file()
        data = path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == item["sha256"]
        notebook = json.loads(data)
        assert notebook["metadata"]["wdp"]["curriculum_index"] == sequence
        assert notebook["metadata"]["wdp"]["claim_ids"] == item["claim_ids"]
        assert notebook["metadata"]["wdp"]["receipt_claim_ids"] == item["receipt_claim_ids"]
        assert len(notebook["cells"]) == item["cell_count"]
        assert sum(cell["cell_type"] == "code" for cell in notebook["cells"]) == item["code_cell_count"]
        ids = [cell["id"] for cell in notebook["cells"]]
        assert len(ids) == len(set(ids))
        source_text = "\n".join("".join(cell["source"]) for cell in notebook["cells"])
        embedded_claim_ids = set(re.findall(r"WDP-CH\d{2}-[DPCON]\d{2}", source_text))
        assert embedded_claim_ids <= canonical_ids
        assert set(item["claim_ids"]) <= embedded_claim_ids
        assert set(item["receipt_claim_ids"]) <= embedded_claim_ids
        assert ("make_receipt(" in source_text) == bool(item["receipt_claim_ids"])
        executable_claims = re.findall(
            r"Claim\(['\"](WDP-CH\d{2}-[DPCON]\d{2})['\"],\s*ClaimStatus\.([A-Z_]+)\)",
            source_text,
        )
        if "Claim(" in source_text:
            assert executable_claims
        for claim_id, status in executable_claims:
            assert status == canonical_statuses[claim_id]
        if path.stem == "000_primitive_difference":
            assert "fixed_points" in source_text
        if path.stem == "010_cochains_and_vector_obstruction":
            assert "finite_quotient_l1" in source_text
            assert "path_independence" in source_text
            assert "obstruction_signature" in source_text
        if path.stem == "040_observation_to_measurement":
            assert "external_standard" in source_text
            assert "additive_upper_bound" in source_text
        if path.stem == "080_claim_status_and_receipts":
            assert item["receipt_claim_ids"] == ["WDP-CH05-D01"]
        assert "## Learning objectives" in source_text
        assert "## Derivation" in source_text
        assert "## Exercise" in source_text
        assert any("Scope check" in "".join(cell["source"]) for cell in notebook["cells"])
        assert any(cell.get("metadata", {}).get("tags") == ["solution"] for cell in notebook["cells"])
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                assert cell["execution_count"] is None
                assert cell["outputs"] == []

    execution = json.loads((ROOT / "manifests" / "notebook_execution.json").read_text(encoding="utf-8"))
    names = {Path(item["path"]).name for item in payload["notebooks"]}
    assert execution["authority_effect"] == "None"
    assert execution["cwd_modes"] == ["paper_root", "notebook_directory"]
    assert execution["execution_passes_per_notebook"] == 2
    assert execution["notebook_count"] == len(names)
    assert execution["status"] == "PASS"
    assert execution["curriculum_order"] == [Path(item["path"]).name for item in payload["notebooks"]]
    assert execution["index_sha256"] == payload["index_sha256"]
    assert execution["widget_replay_mode"] == payload["widget_replay_mode"]
    assert execution["static_fallback_notebooks"] == [
        Path(item["path"]).name
        for item in payload["notebooks"]
        if item["interactive_html_widget"]
    ]
    assert set(execution["normalized_output_sha256"]) == names
    assert set(execution["source_sha256"]) == names


def test_mutation_manifest_and_receipt_bind_real_source_injections() -> None:
    matrix = json.loads((ROOT / "manifests" / "mutation_matrix.json").read_text(encoding="utf-8"))
    receipt = json.loads((ROOT / "manifests" / "mutation_receipt.json").read_text(encoding="utf-8"))
    assert matrix["critical_score_required"] == 100
    assert len(matrix["mutations"]) >= 6
    mutation_ids = [item["id"] for item in matrix["mutations"]]
    assert len(mutation_ids) == len(set(mutation_ids))
    for item in matrix["mutations"]:
        assert item["path"].startswith("code/witnessed_difference/")
        assert item["before"] and item["before"] != item["after"]
        assert item["expected_failed_nodeids"]
        assert set(item["expected_failed_nodeids"]) <= set(item["tests"])
    assert receipt["authority_effect"] == "None"
    assert receipt["expected"] == receipt["killed"] == len(matrix["mutations"])
    assert receipt["score"] == 100.0
    assert receipt["survived"] == []
    assert receipt["baseline"]["exit_code"] == 0
    assert [item["id"] for item in receipt["mutations"]] == mutation_ids
    for item in receipt["mutations"]:
        assert item["killed"] is True
        assert item["mutant_exit_code"] == 1
        assert item["imported_from_mutant_copy"] is True
        assert item["scratch_cleaned"] is True
        assert len(item["before_sha256"]) == len(item["after_sha256"]) == 64
        assert item["before_sha256"] != item["after_sha256"]
    recovery = receipt["recovery"]
    assert recovery["exit_code"] == 0
    assert recovery["scratch_directories_cleaned"] is True
    assert recovery["source_unchanged"] is True
    assert recovery["source_tree_sha256_before"] == recovery["source_tree_sha256_after"]


def test_source_provenance_aggregate_matches_its_declared_serialization() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "verify_source_provenance.py")],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    receipt = json.loads(result.stdout)
    assert receipt == {
        "absorbed_snapshots": [
            {
                "file_count": 48,
                "id": "006_primitive_axiomatics@v2.10.0",
                "sha256": "1c8f9ac63b8ac2b943dd774fce145aeba52b9435d3ca3f3ee40cca1aaf8138b2",
                "source_bytes_checked": False,
                "total_bytes": 3377736,
            },
            {
                "file_count": 5,
                "id": "012_primitive_difference_residual_quotients_and_simplex_growth@PO-012",
                "sha256": "cb86d62b8010dcb33e3b887a8657a16b88a500fd7ab18bb5e70963741fd2c413",
                "source_bytes_checked": False,
                "total_bytes": 22140,
            },
            {
                "file_count": 5,
                "id": "015_primitive_projection_obstruction_descent_and_retraction_calculus@v2.0.0",
                "sha256": "cf6f975f6c4b26055f089243ab80409990c55f4d53fde2643bb1e38efef7ecf8",
                "source_bytes_checked": False,
                "total_bytes": 45479,
            },
            {
                "file_count": 15,
                "id": "003_operational_probabilistic_state_spaces@draft",
                "sha256": "67b407be3c1961a2da440f4f0c7dab1f0c996faedd41260ff30adc318cfed26e",
                "source_bytes_checked": False,
                "total_bytes": 326912,
            },
            {
                "file_count": 37,
                "id": "035_cost_of_closing_observer_blind_spots@scoped-draft",
                "sha256": "2923afc5d17018e282d08766033c42bae89422534d49c7e02222de86ff22e7dd",
                "source_bytes_checked": False,
                "total_bytes": 187536,
            },
            {
                "file_count": 2,
                "id": "020_finite_hilbert_lift_adequacy@v1.0.0",
                "sha256": "8f3ed66d1c6685b81a31b6b93a3d7dee5926877b4a3f3d88240c68270d552e6f",
                "source_bytes_checked": False,
                "total_bytes": 9802,
            },
            {
                "file_count": 100,
                "id": "007_what_the_basis_forces_minima_difference_cost@paper-2",
                "sha256": "7faad3eb1d45a60566a20a6055bc1e6cf14dfecbadeac0747aeef98f5602d04c",
                "source_bytes_checked": False,
                "total_bytes": 1253288,
            },
            {
                "file_count": 16,
                "id": "004_nonlocality_contextuality_finite_commutator_obstructions@v0.2",
                "sha256": "03e611f3e33bf0b5d7fa73afa2a47c196716131ce7fd2040d7d2dfe3fe13974b",
                "source_bytes_checked": False,
                "total_bytes": 196047,
            },
            {
                "file_count": 17,
                "id": "005_discrete_phase_spaces_stabilizer_grounded_semantics@v0.3",
                "sha256": "6877101c934f1a36d7bd1b54c66c8e98cb2faf794e7ca4dcaa83f72965ee48a4",
                "source_bytes_checked": False,
                "total_bytes": 427253,
            },
            {
                "file_count": 204,
                "id": "006_no_free_conclusions_minimal_calculus@v0.3-draft",
                "sha256": "04385426e316e971c808af59ff76deeadcb7cdd06b61da6896ff07405528e789",
                "source_bytes_checked": False,
                "total_bytes": 7168270,
            },
            {
                "file_count": 26,
                "id": "008_l1_coboundary_certificates_and_lift_refusal@v1.0.1",
                "sha256": "464dd49b5dc298deb18798c62e78dbe0d824127123eb04aaa1826d4bdfc628f5",
                "source_bytes_checked": False,
                "total_bytes": 371041,
            },
            {
                "file_count": 31,
                "id": "009_representation_lifts_and_coherence_defects@v1.0.1",
                "sha256": "790eb23084082e88027d5d3344922b1c7d0e84efe16b45e2a29f4f22dbca765d",
                "source_bytes_checked": False,
                "total_bytes": 335775,
            },
            {
                "file_count": 4,
                "id": "010_reasoning_and_intelligence_as_containers@v0.2",
                "sha256": "3df14ca851c1399439893d51c9fcafa51c302081ef42937b3573d010608de7dd",
                "source_bytes_checked": False,
                "total_bytes": 64682,
            },
            {
                "file_count": 17,
                "id": "011_finite_and_infinite_as_observer_relative_regimes_of_obstruction@v1.1",
                "sha256": "d61ed11045778b488785dcb5facb867c2b16edceeac9d1453056708dae1f7adc",
                "source_bytes_checked": False,
                "total_bytes": 63350,
            },
            {
                "file_count": 2,
                "id": "022_finite_presentation_calculus_for_computation@v0.1.0",
                "sha256": "12730ea590adea6fa5753126a75f1c69b238d4d33fb751dba006d4a4645e9cfb",
                "source_bytes_checked": False,
                "total_bytes": 15262,
            },
        ],
        "archived_files_checked": 0,
        "archived_uncommitted_bytes_complete": True,
        "authority_effect": "None",
        "file_count": 44,
        "sha256": "ef19a585f6bb5c95794e3edfc7348e3ae1535bf613b9a0aa8f9f6e54a7f9d383",
        "source_bytes_checked": False,
        "status": "PASS",
        "total_bytes": 1967435,
    }


def test_release_manifest_binds_the_complete_intentional_package() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "verify_release.py"), "--check"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads((ROOT / "manifests" / "release_manifest.json").read_text(encoding="utf-8"))
    assert payload["authority_effect"] == "None"
    listed = {item["path"] for item in payload["files"]}
    required = {
        "README.md",
        "docs/references.md",
        "source_provenance.json",
        "witnessed_difference_programme.md",
        "witnessed_difference_programme_change_log.md",
        "witnessed_difference_programme_claim_ledger.md",
        "pyproject.toml",
        "uv.lock",
        "code/witnessed_difference/observation.py",
        "code/tests/python/e2e_tests/test_historical_claim_crosswalk.py",
        "manifests/historical_claim_occurrences.json",
        "scripts/generate_historical_claim_crosswalk.py",
        "scripts/verify_source_provenance.py",
        "lean4/claim_map.md",
        "lean4/lake-manifest.json",
        "lean4/lakefile.lean",
        "lean4/lean-toolchain",
        "lean4/VERIFICATION.md",
        "lean4/WitnessedDifference/AxiomReport.lean",
    }
    assert required <= listed
    assert not any(".egg-info/" in path for path in listed)
    assert not any("/__pycache__/" in f"/{path}" for path in listed)
    assert "manifests/.coverage" not in listed
    assert "manifests/coverage.json" not in listed
    assert "manifests/release_manifest.json" not in listed
    assert "manifests/release_verification.json" not in listed
    for item in payload["files"]:
        path = ROOT / item["path"]
        assert path.is_file()
        assert path.stat().st_size == item["size"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"]

    receipt = json.loads(
        (ROOT / "manifests" / "release_verification.json").read_text(encoding="utf-8")
    )
    manifest_bytes = (ROOT / "manifests" / "release_manifest.json").read_bytes()
    assert receipt["authority_effect"] == "None"
    assert receipt["status"] == "PASS"
    assert receipt["assertions"]["canonical_surfaces_present"] is True
    assert receipt["assertions"]["canonical_surfaces_singleton"] is True
    assert receipt["assertions"]["forbidden_legacy_surfaces_absent"] is True
    assert receipt["manifest_sha256"] == hashlib.sha256(manifest_bytes).hexdigest()
    assert receipt["file_count"] == payload["inventory"]["file_count"] == len(listed)
    assert receipt["tree_sha256"] == payload["inventory"]["tree_sha256"]


def test_deposit_coverage_gate_refuses_uncovered_sources_outside_legacy_list() -> None:
    verifier = runpy.run_path(str(ROOT / "verify_deposit.py"))
    files = {
        f"code/witnessed_difference/{name}": {
            "summary": {
                "num_statements": 10,
                "covered_lines": 10,
                "num_branches": 10,
                "covered_branches": 10,
            }
        }
        for name in verifier["PRODUCTION_MODULES"]
    }
    extra = "code/witnessed_difference/added_module.py"
    files[extra] = {
        "summary": {
            "num_statements": 1000,
            "covered_lines": 1000,
            "num_branches": 1000,
            "covered_branches": 1000,
        }
    }
    counts, problems = verifier["coverage_counts"]({"files": files})
    assert problems == []
    assert extra in counts
    for missing, category in (("covered_lines", "line"), ("covered_branches", "branch")):
        files[extra]["summary"][missing] = 0
        _, problems = verifier["coverage_counts"]({"files": files})
        assert any(f"aggregate {category} coverage" in problem for problem in problems)
        files[extra]["summary"][missing] = 1000


def test_source_provenance_refuses_colliding_paths_duplicate_ids_and_malformed_entries(tmp_path, monkeypatch) -> None:
    import importlib.util

    spec = importlib.util.spec_from_file_location("wdp_provenance_under_test", ROOT / "scripts" / "verify_source_provenance.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
        for first, second in (("code/a.py", "./code/a.py"), ("code/a.py", "Code/A.py"), ("asset", "asset/child")):
            claims = module._PathClaims()
            claims.claim(first)
            with pytest.raises(ValueError, match="case-colliding"):
                claims.claim(second)
        payload = json.loads((ROOT / "source_provenance.json").read_text(encoding="utf-8"))
        block = payload["absorbed_snapshots"][-1]
        forged = dict(block, files=[dict(block["files"][0], bytes=True)])
        with pytest.raises(ValueError, match="invalid byte count"):
            module._verify_absorbed(forged, module._PathClaims(), None)
        with pytest.raises(ValueError, match="needs path, bytes, and sha256"):
            module._verify_absorbed(dict(block, files=[{"path": "x"}]), module._PathClaims(), None)
        duplicated = dict(payload, absorbed_snapshots=payload["absorbed_snapshots"] + [block])
        manifest = tmp_path / "source_provenance.json"
        manifest.write_text(json.dumps(duplicated), encoding="utf-8")
        monkeypatch.setattr(module, "MANIFEST", manifest)
        with pytest.raises(ValueError, match="duplicate absorbed snapshot id"):
            module.verify()
    finally:
        sys.modules.pop(spec.name, None)


# Executable finite evidence; AuthorityEffect: None.
