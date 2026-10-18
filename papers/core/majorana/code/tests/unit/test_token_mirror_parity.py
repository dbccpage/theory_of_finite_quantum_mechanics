from __future__ import annotations
"""M3b/OD-5 — omega_replay's axis-token mirror binds byte-for-byte to DDA.

THEORETICAL MINIMUM
  INVARIANT  omega_replay/__init__.py deliberately keeps its own copy of the
             three non-authority axis token sets (DiagnosticClass /
             RoutingTerminal / ExtensionStatus) instead of importing
             omega_discrete_deformation_algebra, so it stays a leaf package
             with no intra-repo dependency (see the module docstring
             there). The mirror's own comment claims "the replay and DDA
             test suites bind both sides" of that mirror — this file is
             that binding.
  BREAK      A token is added, renamed, or retired in
             omega_discrete_deformation_algebra.types and the mirror in
             omega_replay/__init__.py is not updated in the same commit.
             Because ``_checked_layer_path`` ACCEPTS any token present in
             its local mirror, a token retired from types.py would stay
             silently accepted by receipts forever (fail-open in the
             dangerous direction) — no prior test caught this (repo-wide
             grep before this commit found no test binding both sides).
  WITNESS    Set equality between each private mirror frozenset in
             omega_replay and ``{m.value for m in <TypesEnum>}`` from the
             canonical owner.
  MUTATION   Add, rename, or delete one member of DiagnosticClass (or
             RoutingTerminal, or ExtensionStatus) in
             omega_discrete_deformation_algebra/types.py without touching
             the corresponding frozenset in omega_replay/__init__.py -> the
             matching test in this file goes red.

AuthorityEffect: None throughout.
"""


import omega_engine.crates.replay as omega_replay
from omega_engine.crates.type.runtime_axes import (
    DiagnosticClass,
    ExtensionStatus,
    RoutingTerminal,
)


def test_diagnostic_class_mirror_is_byte_identical_to_the_canonical_enum() -> None:
    assert omega_replay._DIAGNOSTIC_CLASS_TOKENS == {
        member.value for member in DiagnosticClass
    }


def test_routing_terminal_mirror_is_byte_identical_to_the_canonical_enum() -> None:
    assert omega_replay._ROUTING_TERMINAL_TOKENS == {
        member.value for member in RoutingTerminal
    }


def test_extension_status_mirror_is_byte_identical_to_the_canonical_enum() -> None:
    assert omega_replay._EXTENSION_STATUS_TOKENS == {
        member.value for member in ExtensionStatus
    }


def test_mirrored_axes_cover_exactly_the_three_non_authority_axes() -> None:
    # AuthorityStatus is deliberately NOT mirrored: _checked_layer_path
    # requires the literal 'None' on every step rather than accepting the
    # full AuthorityStatus token set (the receipt mints no authority).
    assert set(omega_replay._AXIS_TOKEN_SETS.keys()) == {
        "diagnostic_class",
        "routing_terminal",
        "extension_status",
    }


