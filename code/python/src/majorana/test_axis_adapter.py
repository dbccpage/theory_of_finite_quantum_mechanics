from __future__ import annotations
"""M3 — Four-axis conflation refusal + ADAPT-01 adapter totality (OD-5).

THEORETICAL MINIMUM
  INVARIANT  resolve_alias is axis-typed, total over the closed table, and
             fail-closed: every RoutingTerminal token refuses where
             DiagnosticClass is required (and vice versa); unknown tokens
             refuse on every axis; GtlaReceipt's layer-path validation
             refuses wrong-axis and unknown tokens naming the axis.
  BREAK      Pre-repair OD-5: no adapter existed (three spellings coexisted
             unmapped) and _checked_layer_path accepted ANY non-empty string.
  WITNESS    AliasAdapterRefusal.token per arm; ValueError naming the axis
             and its legal set from GtlaReceipt.
  MUTATION   In axis_adapter.resolve_alias, replace the final refusal with a
             default-member return -> the unknown-token rows go red.

AuthorityEffect: None throughout.
"""


import pytest

from omega_engine.crates.discrete_deformation_algebra.axis_adapter import (
    AliasAdapterRefusal,
    SUPPORTED_AXES,
    alias_table,
    known_axes_for,
    resolve_alias,
)
from omega_engine.crates.type.runtime_axes import (
    CohomologicalStatus,
    DdaLetter,
    DiagnosticClass,
    ExtensionStatus,
    RoutingTerminal,
)
from omega_engine.crates.replay import GtlaReceipt

ROUTING_TOKENS = [member.value for member in RoutingTerminal]
DIAGNOSTIC_TOKENS = [member.value for member in DiagnosticClass]


def _valid_step() -> dict:
    return {
        "step_id": "s1",
        "letter": "E",
        "diagnostic_class": "ExactClass",
        "routing_terminal": "CheckPassed",
        "extension_status": "NoExtensionNeeded",
        "authority_status": "None",
    }


def _receipt_kwargs(step: dict) -> dict:
    return {
        "claim_id": "AXIS_TEST",
        "claim_sha256": "a" * 64,
        "scope": "axis-adapter-test",
        "layer_path": (step,),
        "dda_tape": "E",
        "residuals": (),
        "debt": (),
        "unresolved_obligations": (),
    }


class TestCrossAxisConflationRefused:
    @pytest.mark.parametrize("routing_token", ROUTING_TOKENS)
    def test_every_routing_token_refused_where_diagnostic_required(
        self, routing_token: str
    ) -> None:
        with pytest.raises(
            AliasAdapterRefusal, match="AXIS_MISMATCH_REFUSED"
        ) as excinfo:
            resolve_alias(routing_token, DiagnosticClass)
        assert excinfo.value.token == "AXIS_MISMATCH_REFUSED"

    @pytest.mark.parametrize("diagnostic_token", DIAGNOSTIC_TOKENS)
    def test_every_diagnostic_token_refused_where_routing_required(
        self, diagnostic_token: str
    ) -> None:
        with pytest.raises(
            AliasAdapterRefusal, match="AXIS_MISMATCH_REFUSED"
        ) as excinfo:
            resolve_alias(diagnostic_token, RoutingTerminal)
        assert excinfo.value.token == "AXIS_MISMATCH_REFUSED"

    def test_named_docstring_case_requires_lift_on_diagnostic_axis(self) -> None:
        with pytest.raises(AliasAdapterRefusal, match="AXIS_MISMATCH_REFUSED"):
            resolve_alias("RequiresLift", DiagnosticClass)


class TestAdapterTotalityOverDeclaredTable:
    def test_every_exported_spelling_resolves_on_its_axis(self) -> None:
        axis_by_name = {axis.__name__: axis for axis in SUPPORTED_AXES}
        table = alias_table()
        assert set(table) == set(axis_by_name)
        checked_rows = 0
        for axis_name, rows in table.items():
            axis = axis_by_name[axis_name]
            for spelling, expected_value in rows.items():
                member = resolve_alias(spelling, axis)
                assert member.value == expected_value
                assert isinstance(member, axis)
                checked_rows += 1
        assert checked_rows == (8 + 3) + (5 + 5) + (3 + 6) + (4 + 0)

    @pytest.mark.parametrize(
        ("spelling", "axis", "expected"),
        [
            ("LiftRequired", RoutingTerminal, RoutingTerminal.RequiresLift),
            ("Refused", RoutingTerminal, RoutingTerminal.Refusal),
            ("RefusedClosure", RoutingTerminal, RoutingTerminal.Refusal),
            ("Survivor", DiagnosticClass, DiagnosticClass.ClosedResidual),
            ("Survivor", CohomologicalStatus, CohomologicalStatus.ClosedSurvivor),
            (
                "StabilizedSurvivor",
                CohomologicalStatus,
                CohomologicalStatus.ClosedSurvivor,
            ),
            ("Exact", DiagnosticClass, DiagnosticClass.ExactClass),
            ("Exact", CohomologicalStatus, CohomologicalStatus.ExactRepair),
            ("Open", DiagnosticClass, DiagnosticClass.ActiveClosureFailure),
            ("OpenResidual", DiagnosticClass, DiagnosticClass.ActiveClosureFailure),
            (
                "OpenObstruction",
                CohomologicalStatus,
                CohomologicalStatus.ActiveClosureFailure,
            ),
        ],
    )
    def test_declared_paper_aliases_resolve(self, spelling, axis, expected) -> None:
        assert resolve_alias(spelling, axis) is expected

    def test_known_axes_for_reports_every_axis_a_token_lives_on(self) -> None:
        assert known_axes_for("Survivor") == ("DiagnosticClass", "CohomologicalStatus")
        assert known_axes_for("RequiresLift") == ("RoutingTerminal",)
        assert known_axes_for("TotallyUnknown") == ()


class TestFailClosedRefusals:
    @pytest.mark.parametrize("axis", list(SUPPORTED_AXES))
    def test_unknown_token_refused_on_every_axis(self, axis) -> None:
        with pytest.raises(
            AliasAdapterRefusal, match="UNKNOWN_TERMINAL_TOKEN_REFUSED"
        ) as excinfo:
            resolve_alias("LocalGreen", axis)
        assert excinfo.value.token == "UNKNOWN_TERMINAL_TOKEN_REFUSED"

    @pytest.mark.parametrize("non_string", [3, None, ["Refusal"], RoutingTerminal])
    def test_non_string_token_refused(self, non_string) -> None:
        with pytest.raises(
            AliasAdapterRefusal, match="NON_STRING_TOKEN_REFUSED"
        ) as excinfo:
            resolve_alias(non_string, RoutingTerminal)
        assert excinfo.value.token == "NON_STRING_TOKEN_REFUSED"

    @pytest.mark.parametrize("bad_axis", [str, int, DdaLetter, None])
    def test_unsupported_axis_refused(self, bad_axis) -> None:
        with pytest.raises(
            AliasAdapterRefusal, match="UNSUPPORTED_AXIS_REFUSED"
        ) as excinfo:
            resolve_alias("Refusal", bad_axis)
        assert excinfo.value.token == "UNSUPPORTED_AXIS_REFUSED"


class TestGtlaReceiptLayerPathAxisValidation:
    """The omega_replay half of M3: wrong-axis/unknown tokens refuse, naming
    the axis and its legal set (pre-repair: ANY non-empty string passed)."""

    def test_valid_step_constructs(self) -> None:
        receipt = GtlaReceipt(**_receipt_kwargs(_valid_step()))
        assert receipt.layer_path[0]["diagnostic_class"] == "ExactClass"

    @pytest.mark.parametrize(
        ("axis_key", "wrong_axis_token", "axis_enum_name"),
        [
            ("diagnostic_class", "RequiresLift", "DiagnosticClass"),
            ("diagnostic_class", "CheckPassed", "DiagnosticClass"),
            ("routing_terminal", "ExactClass", "RoutingTerminal"),
            ("routing_terminal", "NoExtensionNeeded", "RoutingTerminal"),
            ("extension_status", "Repair", "ExtensionStatus"),
            ("extension_status", "ClosedResidual", "ExtensionStatus"),
        ],
    )
    def test_wrong_axis_token_refused_naming_the_axis(
        self, axis_key: str, wrong_axis_token: str, axis_enum_name: str
    ) -> None:
        step = _valid_step()
        step[axis_key] = wrong_axis_token
        with pytest.raises(ValueError, match="unregistered token") as excinfo:
            GtlaReceipt(**_receipt_kwargs(step))
        message = str(excinfo.value)
        assert wrong_axis_token in message
        assert axis_enum_name in message
        assert "legal tokens" in message

    @pytest.mark.parametrize(
        "axis_key", ["diagnostic_class", "routing_terminal", "extension_status"]
    )
    def test_unknown_garbage_token_refused_on_each_axis(self, axis_key: str) -> None:
        step = _valid_step()
        step[axis_key] = "TotallyMadeUpTerminal"
        with pytest.raises(ValueError, match="unregistered token"):
            GtlaReceipt(**_receipt_kwargs(step))

    def test_receipt_token_sets_mirror_the_live_enums_exactly(self) -> None:
        from omega_engine.crates.replay import (
            _DIAGNOSTIC_CLASS_TOKENS,
            _EXTENSION_STATUS_TOKENS,
            _ROUTING_TERMINAL_TOKENS,
        )

        assert _DIAGNOSTIC_CLASS_TOKENS == {m.value for m in DiagnosticClass}
        assert _ROUTING_TERMINAL_TOKENS == {m.value for m in RoutingTerminal}
        assert _EXTENSION_STATUS_TOKENS == {m.value for m in ExtensionStatus}


