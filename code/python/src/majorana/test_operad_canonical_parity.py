"""Cross-language canonical-identifier parity for the higher-operad kernel.

The Rust port in `omega_engine/crates_rs/omega_operad_theory/src/kernel/` must
produce byte-identical `canonical_id` values to the Python kernel, because those
identifiers are what the estate stores. A drift would silently reissue every
identifier in the repository.

The contract is enforced through a checked-in fixture that both languages read:

- this module recomputes every entry with the Python kernel and asserts equality;
- `omega_engine/crates_rs/tests/omega_operad_theory/canonical_parity.rs`
  recomputes the same entries with the Rust kernel and asserts equality.

Both compare against the same stored strings, so agreement with the fixture is
agreement with each other. Neither side can be "fixed" by regenerating alone --
regeneration changes the file the other side is also checked against.

To regenerate after a deliberate encoding change, run with
`OMEGA_REGEN_PARITY=1`, then run the Rust test and expect it to fail until the
Rust encoder is updated to match.

AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import json
import os
import pathlib

import pytest

from omega_engine.crates.kernel.higher_operad.canonical import canonical_id
from omega_engine.crates.kernel.higher_operad.model import (
    AuthorityEffect,
    ColourSpec,
    InvocationGrade,
    OperandRef,
    OperationSpec,
    PortSpec,
)

_REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
_SIGNATURE = _REPO_ROOT / ".agents" / "operad" / "operad_signature.json"
_FIXTURE = (
    _REPO_ROOT
    / "omega_engine"
    / "crates_rs"
    / "omega_operad_theory"
    / "tests"
    / "fixtures"
    / "canonical_parity.json"
)

_ENVELOPE_CASES = [
    ("null", "omega.test", None),
    ("empty-object", "omega.test", {}),
    ("nested-sorting", "omega.test", {"b": 1, "a": {"d": 2, "c": 3}}),
    ("array-of-mixed", "omega.test", [1, True, None, "x", {"k": "v"}]),
    ("bool-not-int", "omega.test", {"t": True, "f": False, "one": 1, "zero": 0}),
    ("negative-int", "omega.test", {"n": -42}),
    ("deep-nest", "omega.test", {"a": {"b": {"c": {"d": [1, {"e": "f"}]}}}}),
]


def _digest_for(name: str) -> str:
    """A deterministic stand-in digest, so the fixture needs no real artifacts."""
    return "sha256:" + hashlib.sha256(name.encode("utf-8")).hexdigest()


def _operation_spec(skill_id: str, source_colours, target_colour) -> OperationSpec:
    return OperationSpec(
        operation_id=skill_id,
        version="v1",
        input_ports=tuple(
            PortSpec(port_id=f"in_{index}", colour_id=colour, schema_ref="any")
            for index, colour in enumerate(source_colours)
        ),
        output_port=PortSpec(port_id="out", colour_id=target_colour, schema_ref="any"),
        executor_ref=skill_id,
        executor_digest=_digest_for(skill_id),
        invocation_grade=InvocationGrade.DISCIPLINE,
        authority_effect=AuthorityEffect.NONE,
        authority_ceiling=AuthorityEffect.NONE,
    )


def _colour_spec(colour_id: str) -> ColourSpec:
    return ColourSpec(
        colour_id=colour_id,
        family="estate",
        schema_ref="any",
        schema_digest=_digest_for(f"schema:{colour_id}"),
        validator_ref="estate.validator",
        validator_digest=_digest_for(f"validator:{colour_id}"),
        schema_version="v1",
    )


def _operand_ref() -> OperandRef:
    return OperandRef(
        artifact_digest=_digest_for("artifact"),
        colour_id="Receipt",
        schema_ref="any",
        admission_receipt_ref=_digest_for("admission"),
        provenance_root=_digest_for("provenance"),
    )


_OBSERVER_CASES = [
    (
        "finite-f2-gauge",
        {
            "regime": "finite-f2-gauge.v1",
            "comparison_relation": "exact-equality",
            "allowed_lifts_and_gauges": ["coefficient-extension", "vertex-rephasing"],
            "defect_definition": "l1-residual-mass",
            "terminal_rule": "strict-descent",
        },
    ),
    (
        "same-card-other-defect",
        {
            "regime": "finite-f2-gauge.v1",
            "comparison_relation": "exact-equality",
            "allowed_lifts_and_gauges": ["coefficient-extension", "vertex-rephasing"],
            "defect_definition": "gamma2-curvature-mass",
            "terminal_rule": "strict-descent",
        },
    ),
    (
        "no-permitted-lifts",
        {
            "regime": "finite-f2-gauge.v1",
            "comparison_relation": "exact-equality",
            "allowed_lifts_and_gauges": [],
            "defect_definition": "l1-residual-mass",
            "terminal_rule": "strict-descent",
        },
    ),
]


def _observer_id(declaration: dict) -> str:
    """Mirror `ObserverDeclaration::observer_id`.

    `allowed_lifts_and_gauges` is sorted here for the same reason the Rust
    constructor sorts it: the same permissions listed in a different order are
    the same rule card and must digest identically.
    """
    payload = dict(declaration)
    payload["allowed_lifts_and_gauges"] = sorted(payload["allowed_lifts_and_gauges"])
    return canonical_id("omega.observer.v1", payload)


def _build_fixture() -> dict:
    signature = json.loads(_SIGNATURE.read_text(encoding="utf-8"))

    operations = []
    skipped: list[dict] = []
    for entry in signature["identities"] + signature["operations"]:
        skill_id = entry["skill_id"]
        try:
            spec = _operation_spec(skill_id, entry["source_colours"], entry["target_colour"])
        except ValueError as exc:
            skipped.append({"operation_id": skill_id, "reason": str(exc)})
            continue
        operations.append(
            {
                "operation_id": skill_id,
                "source_colours": list(entry["source_colours"]),
                "target_colour": entry["target_colour"],
                "executor_digest": _digest_for(skill_id),
                "key": spec.key,
                "canonical_id": spec.canonical_id,
            }
        )

    colours = []
    for colour_id in sorted(signature["colours"]):
        spec = _colour_spec(colour_id)
        colours.append(
            {
                "colour_id": colour_id,
                "schema_digest": spec.schema_digest,
                "validator_digest": spec.validator_digest,
                "canonical_id": spec.canonical_id,
            }
        )

    operand = _operand_ref()

    return {
        "_comment": (
            "Cross-language canonical-identifier parity fixture. Generated by "
            "omega_engine/_tests_unit/test_operad_canonical_parity.py and read by both that "
            "module and omega_operad_theory/tests/canonical_parity.rs. Do not hand-edit."
        ),
        "authority_effect": "None",
        "generator": "omega_engine/_tests_unit/test_operad_canonical_parity.py",
        "envelopes": [
            {
                "name": name,
                "domain": domain,
                "payload": payload,
                "canonical_id": canonical_id(domain, payload),
            }
            for name, domain, payload in _ENVELOPE_CASES
        ],
        "colours": colours,
        "operand_ref": {
            "artifact_digest": operand.artifact_digest,
            "colour_id": operand.colour_id,
            "schema_ref": operand.schema_ref,
            "admission_receipt_ref": operand.admission_receipt_ref,
            "provenance_root": operand.provenance_root,
            "canonical_id": operand.canonical_id,
        },
        "observers": [
            {"name": name, "declaration": declaration, "observer_id": _observer_id(declaration)}
            for name, declaration in _OBSERVER_CASES
        ],
        "operations": operations,
        "skipped": skipped,
    }


def _write_fixture(fixture: dict) -> None:
    _FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    _FIXTURE.write_text(json.dumps(fixture, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if os.environ.get("OMEGA_REGEN_PARITY") == "1":
    _write_fixture(_build_fixture())


@pytest.fixture(scope="module")
def fixture() -> dict:
    if not _FIXTURE.is_file():
        pytest.fail(
            f"parity fixture missing at {_FIXTURE}; regenerate with OMEGA_REGEN_PARITY=1"
        )
    return json.loads(_FIXTURE.read_text(encoding="utf-8"))


def test_fixture_accounts_for_every_catalog_entry(fixture: dict) -> None:
    """Guard against a fixture that silently shrinks.

    A parity suite that quietly stopped covering most operations would still be
    green, which is the failure mode this asserts against. Entries neither
    language can compile are counted as skips rather than dropped, so adding one
    to the registry does not make this permanently unrepairable.
    """
    signature = json.loads(_SIGNATURE.read_text(encoding="utf-8"))
    expected = len(signature["identities"]) + len(signature["operations"])
    covered = len(fixture["operations"]) + len(fixture.get("skipped", []))
    assert covered == expected, (
        f"{expected - covered} catalog entries are neither covered nor recorded as skipped"
    )
    assert len(fixture["colours"]) == len(signature["colours"]) == 10


def test_skips_are_rare_and_explained(fixture: dict) -> None:
    """A skip is an escape hatch, not a place to hide coverage loss."""
    skipped = fixture.get("skipped", [])
    assert len(skipped) <= 5, f"too many uncompilable catalog entries: {skipped}"
    for entry in skipped:
        assert entry["reason"], entry["operation_id"]


def test_every_operation_canonical_id_reproduces(fixture: dict) -> None:
    for case in fixture["operations"]:
        spec = _operation_spec(
            case["operation_id"], case["source_colours"], case["target_colour"]
        )
        assert spec.canonical_id == case["canonical_id"], case["operation_id"]
        assert spec.key == case["key"], case["operation_id"]


def test_every_colour_canonical_id_reproduces(fixture: dict) -> None:
    for case in fixture["colours"]:
        assert _colour_spec(case["colour_id"]).canonical_id == case["canonical_id"]


def test_operand_ref_canonical_id_reproduces(fixture: dict) -> None:
    assert _operand_ref().canonical_id == fixture["operand_ref"]["canonical_id"]


def test_every_envelope_canonical_id_reproduces(fixture: dict) -> None:
    for case in fixture["envelopes"]:
        assert canonical_id(case["domain"], case["payload"]) == case["canonical_id"], case["name"]


def test_canonical_ids_are_distinct_across_operations(fixture: dict) -> None:
    """A collision would mean the encoder is dropping a distinguishing field."""
    ids = [case["canonical_id"] for case in fixture["operations"]]
    assert len(set(ids)) == len(ids)


def test_domain_separation_changes_the_identifier() -> None:
    payload = {"colour_id": "State"}
    assert canonical_id("omega.oewas.colour.v1", payload) != canonical_id(
        "omega.oewas.operation-spec.v1", payload
    )


def test_every_stored_identifier_is_a_lowercase_sha256(fixture: dict) -> None:
    groups = [fixture["operations"], fixture["colours"], fixture["envelopes"]]
    for group in groups:
        for case in group:
            value = case["canonical_id"]
            assert value.startswith("sha256:")
            assert len(value) == len("sha256:") + 64
            assert value[7:] == value[7:].lower()


def test_every_observer_id_reproduces(fixture: dict) -> None:
    for case in fixture["observers"]:
        assert _observer_id(case["declaration"]) == case["observer_id"], case["name"]


def test_observer_ids_separate_different_rule_cards(fixture: dict) -> None:
    """The block-tower property: same data under a different rule card is a
    different observer, and the atlas must be able to tell."""
    ids = {case["name"]: case["observer_id"] for case in fixture["observers"]}
    assert ids["finite-f2-gauge"] != ids["same-card-other-defect"]
    assert ids["finite-f2-gauge"] != ids["no-permitted-lifts"]


def test_observer_id_ignores_lift_ordering() -> None:
    """Identical rule cards must collide regardless of how they were written."""
    base = dict(_OBSERVER_CASES[0][1])
    shuffled = dict(base)
    shuffled["allowed_lifts_and_gauges"] = list(reversed(base["allowed_lifts_and_gauges"]))
    assert _observer_id(base) == _observer_id(shuffled)
