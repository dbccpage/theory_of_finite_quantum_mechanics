import json
from pathlib import Path

import pytest
from witnessed_difference.claims import ClaimRecord, load_claim_map, validate_claim_map
from witnessed_difference.figures import figure_assets, flow_svg, tiny_png
from witnessed_difference.notebook_support import (
    STATIC_WIDGET_ENV,
    display_json,
    slider_html,
    static_slider,
)
from witnessed_difference.relative_status import ClaimStatus


def test_claim_map_load_and_validate(tmp_path: Path) -> None:
    module = tmp_path / "code" / "module.py"
    test = tmp_path / "code" / "test_module.py"
    module.parent.mkdir()
    module.write_text("VALUE = 1\n", encoding="utf-8")
    test.write_text("def test_value(): pass\n", encoding="utf-8")
    manifest = tmp_path / "claims.json"
    manifest.write_text(
        json.dumps(
            {
                "claims": [
                    {
                        "claim_id": "C-1",
                        "status": "FINITE_WITNESS",
                        "module": "code/module.py",
                        "tests": ["code/test_module.py"],
                        "evidence_type": "finite exhaustive witness",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    records = load_claim_map(manifest)
    assert records[0].status is ClaimStatus.FINITE_WITNESS
    assert validate_claim_map(records, tmp_path) == ()


def test_claim_map_reports_duplicates_missing_paths_and_empty_fields(tmp_path: Path) -> None:
    records = (
        ClaimRecord("C", ClaimStatus.OPEN, "missing.py", (), ""),
        ClaimRecord("C", ClaimStatus.OPEN, "also-missing.py", ("missing-test.py",), "assertion"),
        ClaimRecord("", ClaimStatus.OPEN, "missing.py", ("missing-test.py",), "assertion"),
    )
    errors = validate_claim_map(records, tmp_path)
    assert "claim ids must be unique" in errors
    assert "claim id and evidence type must be nonempty" in errors
    assert "claim has no tests: C" in errors
    assert any(error.startswith("missing module:") for error in errors)
    assert any(error.startswith("missing test:") for error in errors)


def test_flow_svg_is_accessible_escaped_and_deterministic() -> None:
    first = flow_svg("A < B", ("one", "two & three"))
    second = flow_svg("A < B", ("one", "two & three"))
    assert first == second
    assert 'role="img"' in first
    assert "A &lt; B" in first
    assert "two &amp; three" in first
    assert "<title" in first and "<desc" in first
    with pytest.raises(ValueError, match="at least one"):
        flow_svg("empty", ())


def test_png_and_asset_bundle_are_deterministic() -> None:
    png = tiny_png(8, 8)
    assert png.startswith(b"\x89PNG\r\n\x1a\n")
    assert png == tiny_png(8, 8)
    assert tiny_png(1, 1).startswith(b"\x89PNG\r\n\x1a\n")
    assert set(figure_assets()) == {
        "witness_ladder.svg",
        "observer_types.svg",
        "duration_classes.svg",
        "u1_holonomy.png",
    }
    assert all(figure_assets()[name] for name in figure_assets())
    with pytest.raises(ValueError, match="positive"):
        tiny_png(0, 8)
    with pytest.raises(ValueError, match="positive"):
        tiny_png(8, -1)


def test_static_widget_fallback_and_display_json(monkeypatch: pytest.MonkeyPatch) -> None:
    slider = static_slider("carrier size", 1, 4, 3)
    assert slider == {
        "control": "static_slider_fallback",
        "label": "carrier size",
        "maximum": 4,
        "minimum": 1,
        "value": 3,
    }
    assert json.loads(display_json({"b": 2, "a": 1})) == {
        "__wdp_type__": "mapping",
        "items": [["a", 1], ["b", 2]],
    }
    interactive = slider_html("carrier <size>", 1, 4, 3, static=False)
    assert 'type="range"' in interactive
    assert 'data-widget-mode="interactive"' in interactive
    assert "carrier &lt;size&gt;" in interactive
    assert "addEventListener('input'" in interactive
    assert slider_html("carrier <size>", 1, 4, 3, static=False) == interactive
    explicit_static = slider_html("carrier size", 1, 4, 3, static=True)
    assert 'data-widget-mode="static"' in explicit_static
    assert "static_slider_fallback" in explicit_static
    assert "<script>" not in explicit_static
    monkeypatch.setenv(STATIC_WIDGET_ENV, "1")
    assert slider_html("carrier size", 1, 4, 3) == explicit_static
    monkeypatch.delenv(STATIC_WIDGET_ENV)
    assert 'data-widget-mode="interactive"' in slider_html("carrier size", 1, 4, 3)
    for args in (("", 0, 1, 0), ("x", 2, 1, 1), ("x", 0, 1, 2)):
        with pytest.raises(ValueError, match="static slider"):
            static_slider(*args)
# Executable finite evidence; AuthorityEffect: None.
