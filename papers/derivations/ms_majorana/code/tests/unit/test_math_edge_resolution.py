from __future__ import annotations

"""Phase 1 math edge-resolution measurement: classification and resolution invariants."""


from pathlib import Path

from omega_engine_governance.contracts.math_edge_resolution import (
    RELATION_DEFINES,
    RELATION_PARAMETER,
    RELATION_PROVIDES,
    RELATION_UNCLASSIFIED,
    RELATION_UNDERLYING,
    build_math_id_index,
    build_report,
    camel_to_snake,
    classify_relation,
    extract_edges,
)


def test_camel_to_snake_keeps_acronym_and_digit_runs_together():
    assert camel_to_snake("LinearMap") == "linear_map"
    assert camel_to_snake("VectorSpace") == "vector_space"
    assert camel_to_snake("CanonicalBytes") == "canonical_bytes"
    assert camel_to_snake("L1Seminorm") == "l1_seminorm"
    assert camel_to_snake("CDGAlgebra") == "cdg_algebra"


def test_classify_relation_separates_verb_led_from_noun_led():
    assert classify_relation("provides normed space structure") == RELATION_PROVIDES
    assert (
        classify_relation("Provides underlying category structure") == RELATION_PROVIDES
    )
    assert classify_relation("defines_base_field_K") == RELATION_DEFINES
    assert classify_relation("Defines the diagram functor F") == RELATION_DEFINES
    assert (
        classify_relation("underlying_graded_module_structure") == RELATION_UNDERLYING
    )
    assert classify_relation("coefficient_field") == RELATION_PARAMETER
    assert classify_relation("matrix structure") == RELATION_PARAMETER


def test_classify_relation_strips_leading_articles_before_deciding():
    assert classify_relation("the underlying cochain complex") == RELATION_UNDERLYING
    assert classify_relation("The provides clause") == RELATION_PROVIDES


def test_classify_relation_only_empty_labels_are_unclassified():
    assert classify_relation(None) == RELATION_UNCLASSIFIED
    assert classify_relation("") == RELATION_UNCLASSIFIED
    assert classify_relation("   ") == RELATION_UNCLASSIFIED
    assert classify_relation("the") == RELATION_UNCLASSIFIED


def test_extract_edges_resolves_via_camel_to_snake_join():
    index = {("linear_map", "v0.1.0"): "urn:omega:math:linear_map:v0.1.0"}
    doc = {
        "relationships": [
            "urn:math:contract:LinearMap:v0.1.0 serves as defines_the_map",
            "urn:math:contract:MissingThing:v0.1.0 serves as coefficient_field",
        ]
    }
    edges = extract_edges("adjoint.contract.yaml", doc, index)
    assert len(edges) == 2

    resolved, dangling = edges[0], edges[1]
    assert resolved.resolved_target == "urn:omega:math:linear_map:v0.1.0"
    assert resolved.relation == RELATION_DEFINES
    assert resolved.note == "defines_the_map"

    assert dangling.resolved_target is None
    assert dangling.target_legacy_name == "MissingThing"
    assert dangling.relation == RELATION_PARAMETER


def test_extract_edges_ignores_non_legacy_relationship_entries():
    doc = {
        "relationships": [
            "urn:omega:math:already_typed:v1.0.0 serves as something",
            "free prose with no urn at all",
        ]
    }
    assert extract_edges("x.yaml", doc, {}) == []


def test_extract_edges_ignores_mapping_shaped_relationships():
    doc = {
        "relationships": {"extends": ["urn:omega:constitution:base_contract:v1.0.0"]}
    }
    assert extract_edges("x.yaml", doc, {}) == []


def test_build_math_id_index_only_indexes_math_domain_ids():
    docs = [
        (Path("a.yaml"), {"contract_id": "urn:omega:math:adjoint:v0.1.0"}),
        (Path("b.yaml"), {"contract_id": '"urn:omega:math:quoted:v1.0.0"'}),
        (Path("c.yaml"), {"contract_id": "urn:omega:solver_objects:phi1:v1.0.0"}),
        (
            Path("d.yaml"),
            {"contract_id": "urn:omega:rust:omega_functional:phi1:v1.1.0"},
        ),
        (Path("e.yaml"), {}),
    ]
    index = build_math_id_index(docs)
    assert index == {
        ("adjoint", "v0.1.0"): "urn:omega:math:adjoint:v0.1.0",
        ("quoted", "v1.0.0"): "urn:omega:math:quoted:v1.0.0",
    }


def test_resolution_preserves_requested_version_and_accepts_wildcard():
    index = {
        ("linear_map", "v0.1.0"): "urn:omega:math:linear_map:v0.1.0",
        ("linear_map", "v1.0.0"): "urn:omega:math:linear_map:v1.0.0",
    }
    exact = extract_edges(
        "x.yaml",
        {"relationships": ["urn:math:contract:LinearMap:v2.0.0"]},
        index,
    )
    wildcard = extract_edges(
        "x.yaml",
        {"relationships": ["urn:math:contract:LinearMap:v*"]},
        index,
    )
    assert len(exact) == 1 and exact[0].resolved_target is None
    assert len(wildcard) == 1
    assert wildcard[0].target_legacy_version == "v*"
    assert wildcard[0].resolved_target == "urn:omega:math:linear_map:v0.1.0"


def test_build_report_exact_counts_on_fixture(tmp_path: Path):
    root = tmp_path / "contracts_math"
    root.mkdir()
    (root / "linear_map.contract.yaml").write_text(
        "contract_id: urn:omega:math:linear_map:v0.1.0\n", encoding="utf-8"
    )
    (root / "adjoint.contract.yaml").write_text(
        "contract_id: urn:omega:math:adjoint:v0.1.0\n"
        "relationships:\n"
        "- urn:math:contract:LinearMap:v0.1.0 serves as defines_the_map\n"
        "- urn:math:contract:Basis:v0.1.0 serves as coefficient_field\n",
        encoding="utf-8",
    )

    report, edges = build_report(math_root=root)
    assert report.math_contract_count == 2
    assert report.indexed_math_ids == 2
    assert report.files_with_edges == 1
    assert report.total_edges == 2
    assert report.resolved_edges == 1
    assert report.unresolved_edges == 1
    assert report.unresolved_targets == {"Basis": 1}
    assert report.resolution_rate == 0.5
    assert report.authority_effect == "None"
    assert len(edges) == 2


def test_build_report_is_read_only(tmp_path: Path):
    root = tmp_path / "contracts_math"
    root.mkdir()
    src = root / "adjoint.contract.yaml"
    body = (
        "contract_id: urn:omega:math:adjoint:v0.1.0\n"
        "relationships:\n"
        "- urn:math:contract:Basis:v0.1.0 serves as coefficient_field\n"
    )
    src.write_text(body, encoding="utf-8")
    before = src.read_bytes()
    build_report(math_root=root)
    assert src.read_bytes() == before


def test_build_report_on_missing_root_reports_nothing(tmp_path: Path):
    report, edges = build_report(math_root=tmp_path / "absent")
    assert report.total_edges == 0
    assert report.math_contract_count == 0
    assert edges == []
    assert report.resolution_rate == 0.0


def test_markdown_reports_unresolved_targets_and_authority(tmp_path: Path):
    root = tmp_path / "contracts_math"
    root.mkdir()
    (root / "adjoint.contract.yaml").write_text(
        "contract_id: urn:omega:math:adjoint:v0.1.0\n"
        "relationships:\n"
        "- urn:math:contract:Basis:v0.1.0 serves as coefficient_field\n",
        encoding="utf-8",
    )
    report, _ = build_report(math_root=root)
    text = report.to_markdown()
    assert "AuthorityEffect" in text
    assert "`None`" in text
    assert "Basis" in text
    assert "urn:omega:math:basis" in text
