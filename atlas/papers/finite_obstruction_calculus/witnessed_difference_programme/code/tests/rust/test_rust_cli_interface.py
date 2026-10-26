"""Direct CLI and subprocess protocol tests for compiled WDP Rust binaries.

# Executable finite evidence; AuthorityEffect: None.
"""

from __future__ import annotations

import json
import subprocess
from fractions import Fraction
from pathlib import Path
import pytest


def test_obstruction_cli_exact_triangle(obstruction_bin: Path):
    """Verify solve_wdp_obstruction CLI execution on exact 1-cochain."""
    req = {
        "vertices": ["v0", "v1", "v2"],
        "edges": [["v0", "v1"], ["v1", "v2"], ["v0", "v2"]],
        "cochain": {
            "v0,v1": "1",
            "v1,v2": "2",
            "v0,v2": "3",
        },
    }
    proc = subprocess.run(
        [str(obstruction_bin)],
        input=json.dumps(req),
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode == 0
    res = json.loads(proc.stdout)
    assert res["authority_effect"] == "None"
    assert res["phi1"] == "0"
    assert res["is_exact"] is True
    assert "potential" in res
    assert res["potential"]["v0"] == "0"
    assert res["potential"]["v1"] == "1"
    assert res["potential"]["v2"] == "3"


def test_obstruction_cli_obstructed_cycle(obstruction_bin: Path):
    """Verify solve_wdp_obstruction CLI execution on obstructed holonomy cycle."""
    req = {
        "vertices": ["a", "b", "c"],
        "edges": [["a", "b"], ["b", "c"], ["a", "c"]],
        "cochain": {
            "a,b": "1",
            "b,c": "1",
            "a,c": "0",
        },
    }
    proc = subprocess.run(
        [str(obstruction_bin)],
        input=json.dumps(req),
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode == 0
    res = json.loads(proc.stdout)
    assert res["authority_effect"] == "None"
    assert res["is_exact"] is False
    phi1 = Fraction(res["phi1"])
    assert phi1 > 0

    from types import SimpleNamespace
    from tests.functional_checks import verify_native
    vertices = tuple(req["vertices"])
    edges = tuple(tuple(e) for e in req["edges"])
    decode_edges = lambda values: {tuple(k.split(",")): Fraction(v) for k, v in values.items()}
    solution = SimpleNamespace(phi1=phi1,
        potential={k: Fraction(v) for k, v in res["potential"].items()},
        residual=decode_edges(res["residual"]), dual_witness=decode_edges(res["dual_witness"]))
    verify_native(vertices, edges, decode_edges(req["cochain"]), solution)


def test_obstruction_cli_malformed_json(obstruction_bin: Path):
    """Verify solve_wdp_obstruction rejects non-JSON input gracefully."""
    proc = subprocess.run(
        [str(obstruction_bin)],
        input="{not valid json",
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode != 0 or "error" in proc.stdout.lower() or "error" in proc.stderr.lower()


def test_obstruction_cli_missing_fields(obstruction_bin: Path):
    """Verify solve_wdp_obstruction rejects payload missing required schema fields."""
    proc = subprocess.run(
        [str(obstruction_bin)],
        input=json.dumps({"vertices": ["v0"]}),
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode != 0 or "error" in proc.stdout.lower() or "error" in proc.stderr.lower()


def test_genesis_cli_quotient_map(genesis_bin: Path):
    """Verify solve_genesis_observer CLI execution on valid quotient map."""
    req = {
        "memory_transitions": [[0, 1], [1, 0]],
        "memory_initial": 0,
        "transducer_transitions": [[0, 0]],
        "transducer_emit": [[[0], [1]]],
        "transducer_initial": 0,
        "prefix_words": [1],
        "final_words": [[]],
    }
    proc = subprocess.run(
        [str(genesis_bin)],
        input=json.dumps(req),
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode == 0
    res = json.loads(proc.stdout)
    assert res["authority_effect"] == "None"
    assert res["kind"] == "map"
    assert res["prefix"] == [1]


def test_genesis_cli_collision_witness(genesis_bin: Path):
    """Verify solve_genesis_observer CLI execution discovers collision witness."""
    req = {
        "memory_transitions": [[0, 1], [0, 1]],
        "memory_initial": 0,
        "transducer_transitions": [[0, 0]],
        "transducer_emit": [[[0], [1]]],
        "transducer_initial": 0,
        "prefix_words": [1],
        "final_words": [[]],
    }
    proc = subprocess.run(
        [str(genesis_bin)],
        input=json.dumps(req),
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode == 0
    res = json.loads(proc.stdout)
    assert res["authority_effect"] == "None"
    assert res["kind"] == "collision"
    assert "collision_first" in res
    assert "collision_second" in res


def test_genesis_cli_malformed_json(genesis_bin: Path):
    """Verify solve_genesis_observer rejects malformed input gracefully."""
    proc = subprocess.run(
        [str(genesis_bin)],
        input="invalid payload",
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode != 0 or "error" in proc.stdout.lower() or "error" in proc.stderr.lower()
