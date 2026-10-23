"""Tests for native Rust WDP solver and Python bridge.

# Executable finite evidence; AuthorityEffect: None.
"""

from fractions import Fraction
import pytest

from native_wdp import (
    solve_native_obstruction,
    solve_native_genesis_descent,
)


def test_exact_rational_float_firewall():
    """Verify that floats and bools are rejected by the exact rational firewall."""
    vertices = ["v0", "v1"]
    edges = [("v0", "v1")]

    # Float rejection
    with pytest.raises(TypeError, match="Exact rational required"):
        solve_native_obstruction(vertices, edges, {("v0", "v1"): 1.5})

    # Bool rejection
    with pytest.raises(TypeError, match="Exact rational required"):
        solve_native_obstruction(vertices, edges, {("v0", "v1"): True})  # type: ignore[arg-type]


def test_native_obstruction_solver_exact():
    """Verify that an exact 1-cochain has phi1 = 0 and is_exact = True."""
    vertices = ["v0", "v1", "v2"]
    edges = [("v0", "v1"), ("v1", "v2"), ("v0", "v2")]
    cochain = {
        ("v0", "v1"): Fraction(1),
        ("v1", "v2"): Fraction(2),
        ("v0", "v2"): Fraction(3),
    }

    res = solve_native_obstruction(vertices, edges, cochain)
    assert res.value["phi1"] == Fraction(0)
    assert res.value["is_exact"] is True
    assert res.value["authority_effect"] == "None"
    assert res.value["potential"]["v0"] == Fraction(0)
    assert res.value["potential"]["v1"] == Fraction(1)
    assert res.value["potential"]["v2"] == Fraction(3)


def test_native_obstruction_solver_obstructed():
    """Verify that a non-zero holonomy cochain yields positive phi1 defect."""
    vertices = ["v0", "v1", "v2"]
    edges = [("v0", "v1"), ("v1", "v2"), ("v0", "v2")]
    cochain = {
        ("v0", "v1"): Fraction(1),
        ("v1", "v2"): Fraction(1),
        ("v0", "v2"): Fraction(0),
    }

    res = solve_native_obstruction(vertices, edges, cochain)
    assert res.value["phi1"] > Fraction(0)
    assert res.value["is_exact"] is False
    assert res.value["authority_effect"] == "None"


def test_native_genesis_descent_map():
    """Verify that native Genesis descent correctly identifies quotient map."""
    memory_transitions = [[0, 1], [1, 0]]
    memory_initial = 0
    transducer_transitions = [[0, 0]]
    transducer_emit = [[[0], [1]]]
    transducer_initial = 0
    prefix_words = [1]
    final_words = [[]]

    res = solve_native_genesis_descent(
        memory_transitions,
        memory_initial,
        transducer_transitions,
        transducer_emit,
        transducer_initial,
        prefix_words,
        final_words,
    )
    assert res.value["kind"] == "map"
    assert res.value["prefix"] == [1]
    assert res.value["authority_effect"] == "None"


def test_native_genesis_descent_collision():
    """Verify that native Genesis descent extracts collision witnesses when not a map."""
    memory_transitions = [[0, 1], [0, 1]]
    memory_initial = 0
    transducer_transitions = [[0, 0]]
    transducer_emit = [[[0], [1]]]
    transducer_initial = 0
    prefix_words = [1]
    final_words = [[]]

    res = solve_native_genesis_descent(
        memory_transitions,
        memory_initial,
        transducer_transitions,
        transducer_emit,
        transducer_initial,
        prefix_words,
        final_words,
    )
    assert res.value["kind"] == "collision"
    assert res.value["collision_first"] is not None
    assert res.value["collision_second"] is not None
    assert res.value["authority_effect"] == "None"


def test_missing_native_refuses_without_functional_fallback(monkeypatch):
    import native_wdp
    monkeypatch.setattr(native_wdp, "find_binary", lambda *args: None)
    result = solve_native_obstruction(["a", "b"], [("a", "b")], {("a", "b"): Fraction(1)})
    assert result.is_err
    assert result.unwrap_err().code == "WDP_NATIVE_UNAVAILABLE"


def test_find_binary_prefers_target_paper_rust(tmp_path, monkeypatch):
    """A fresh repo build wins over a stale package binary. A set env path still wins."""
    import native_wdp
    monkeypatch.delenv("CARGO_TARGET_DIR", raising=False)

    repo = tmp_path / "repo"
    rust_dir = repo / "pkg" / "code" / "rust"
    stale_dir = rust_dir / "target" / "debug"
    stale_dir.mkdir(parents=True)
    (stale_dir / "solve_wdp_obstruction.exe").write_bytes(b"stale")
    (repo / ".git").write_text("gitdir: unused\n", encoding="utf-8")
    fresh_dir = repo / "target_paper_rust" / "debug"
    fresh_dir.mkdir(parents=True)
    fresh = fresh_dir / "solve_wdp_obstruction"
    fresh.write_bytes(b"fresh")
    monkeypatch.setattr(native_wdp, "RUST_DIR", rust_dir)
    assert native_wdp.find_binary("solve_wdp_obstruction") == fresh
    release_dir = repo / "target_paper_rust" / "release"
    release_dir.mkdir()
    release = release_dir / "solve_wdp_obstruction"
    release.write_bytes(b"release")
    workspace = repo / "target" / "debug"
    workspace.mkdir(parents=True)
    (workspace / "solve_wdp_obstruction.exe").write_bytes(b"workspace")
    assert native_wdp.find_binary("solve_wdp_obstruction") == release
    monkeypatch.setenv("WDP_OBSTRUCTION_BIN", str(tmp_path / "missing.exe"))
    with pytest.raises(native_wdp.NativeWdpUnavailable):
        native_wdp.find_binary("solve_wdp_obstruction", "WDP_OBSTRUCTION_BIN")
    env_bin = tmp_path / "from-env.exe"
    env_bin.write_bytes(b"env")
    monkeypatch.setenv("WDP_OBSTRUCTION_BIN", str(env_bin))
    assert native_wdp.find_binary("solve_wdp_obstruction", "WDP_OBSTRUCTION_BIN") == env_bin


def test_require_native_false_maps_boundary_failures_to_err(monkeypatch):
    """A missing or bad native run is Err unless the caller demanded the binary."""
    import subprocess

    import native_wdp

    monkeypatch.setattr(native_wdp, "find_binary", lambda *_args, **_kwargs: native_wdp.Path("missing-bin"))

    def timeout(*_args, **_kwargs):
        raise subprocess.TimeoutExpired(cmd="missing-bin", timeout=1)

    monkeypatch.setattr(native_wdp.subprocess, "run", timeout)
    timed = native_wdp.solve_native_obstruction(["v0"], [], {}, require_native=False)
    assert timed.is_err
    assert timed.unwrap_err().code == "WDP_NATIVE_TIMEOUT"
    with pytest.raises(native_wdp.NativeWdpTimeout):
        native_wdp.solve_native_obstruction(["v0"], [], {}, require_native=True)

    def unavailable(*_args, **_kwargs):
        raise OSError("nope")

    monkeypatch.setattr(native_wdp.subprocess, "run", unavailable)
    missing = native_wdp.solve_native_obstruction(["v0"], [], {}, require_native=False)
    assert missing.unwrap_err().code == native_wdp.NativeWdpUnavailable.code == "WDP_NATIVE_UNAVAILABLE"
    with pytest.raises(native_wdp.NativeWdpUnavailable):
        native_wdp.solve_native_obstruction(["v0"], [], {}, require_native=True)

    class NotJson:
        returncode = 0
        stdout = "not-json"
        stderr = ""

    monkeypatch.setattr(native_wdp.subprocess, "run", lambda *_args, **_kwargs: NotJson())
    protocol = native_wdp.solve_native_obstruction(["v0"], [], {}, require_native=False)
    assert protocol.unwrap_err().code == native_wdp.NativeWdpProtocolError.code == "WDP_NATIVE_PROTOCOL"
    with pytest.raises(native_wdp.NativeWdpProtocolError):
        native_wdp.solve_native_obstruction(["v0"], [], {}, require_native=True)

    class Unexpected:
        returncode = 2
        stdout = '{"status": "ERROR"}'
        stderr = ""

    monkeypatch.setattr(native_wdp.subprocess, "run", lambda *_args, **_kwargs: Unexpected())
    unexpected = native_wdp.solve_native_obstruction(["v0"], [], {}, require_native=False)
    assert unexpected.unwrap_err().code == "WDP_NATIVE_UNEXPECTED"
    genesis = native_wdp.solve_native_genesis_descent(
        [[0]],
        0,
        [[0]],
        [[[0]]],
        0,
        [0],
        [[]],
        require_native=False,
    )
    assert genesis.unwrap_err().code == "WDP_NATIVE_UNEXPECTED"
    with pytest.raises(native_wdp.NativeWdpProtocolError):
        native_wdp.solve_native_genesis_descent(
            [[0]],
            0,
            [[0]],
            [[[0]]],
            0,
            [0],
            [[]],
            require_native=True,
        )
