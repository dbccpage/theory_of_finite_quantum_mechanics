"""Cross-runtime semantic-key fixtures shared with the Lean package."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from omega_engine.kernel.higher_operad import (
    ColourSpec,
    OperationSpec,
    PortSpec,
    Primitive,
    Substitute,
    normalize_term,
)


def _colour_key(colours: dict, name: str) -> str:
    colour = colours[name]
    version = int(colour.schema_version.removeprefix("v"))
    return f"{colour.colour_id}@{version}#{colour.schema_digest}"


def _lean_term_key(tree: dict, colours: dict) -> str:
    if "input" in tree:
        return "wire(" + _colour_key(colours, tree["input"]["colour_id"]) + ")"
    operation = tree["operation"]
    inputs = ",".join(
        _colour_key(colours, port["colour_id"])
        for port in operation["input_ports"]
    )
    output = _colour_key(colours, operation["output_port"]["colour_id"])
    profile = f"([{inputs}])->{output}"
    children = ",".join(_lean_term_key(item, colours) for item in tree["children"])
    return (
        f"op({operation['operation_id']}|{profile}|"
        f"{operation['executor_digest']};[{children}])"
    )


class CrossRuntimeGoldenTests(unittest.TestCase):
    def test_python_normal_form_matches_lean_semantic_fixture(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        path = (
            repo_root
            / "lean4"
            / "genx"
            / "oewas_higher_operad"
            / "golden"
            / "finite_operad_fixture_v1.json"
        )
        if not path.exists():
            self.skipTest(f"Lean4 golden fixture not found at {path}")
        raw = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(raw["schema"], "omega.oewas.cross-runtime-operad-fixture.v1")
        colours = {
            item["name"]: ColourSpec(
                colour_id=item["name"],
                family="golden",
                schema_ref=item["schema_ref"],
                schema_digest=item["schema_digest"],
                validator_ref="fixture-envelope-checker",
                validator_digest="sha256:" + "f" * 64,
                schema_version=f"v{item['version']}",
            )
            for item in raw["colours"]
        }
        generators = {}
        for item in raw["generators"]:
            inputs = tuple(
                PortSpec(f"input-{index}", name, colours[name].schema_ref)
                for index, name in enumerate(item["inputs"])
            )
            output_name = item["output"]
            generators[item["name"]] = OperationSpec(
                operation_id=item["name"],
                version="v1",
                input_ports=inputs,
                output_port=PortSpec("output", output_name, colours[output_name].schema_ref),
                executor_ref=f"fixture.{item['name']}",
                executor_digest=item["implementation_digest"],
            )

        inspect = normalize_term(Primitive(generators["inspect"])).unwrap()
        reviewed = normalize_term(
            Substitute(Primitive(generators["review"]), 0, Primitive(generators["inspect"]))
        ).unwrap()
        self.assertEqual(
            _lean_term_key(inspect.to_canonical()["tree"], colours),
            raw["expected_lean_inspect_key"],
        )
        self.assertEqual(
            _lean_term_key(reviewed.to_canonical()["tree"], colours),
            raw["expected_lean_reviewed_key"],
        )


if __name__ == "__main__":
    unittest.main()
