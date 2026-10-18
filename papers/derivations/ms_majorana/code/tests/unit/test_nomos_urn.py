from __future__ import annotations
"""STORY-ORT-CONTRACTS-001 — Nomos URN schema parity sample tests.

Lev Landau mutations: leading-zero version, uppercase domain, prefix-only.
AuthorityEffect: None.
"""


import pytest

from omega_engine.crates.contract_core.nomos_urn import (
    CRITICAL_URN_NEGATIVE_SAMPLE,
    CRITICAL_URN_SAMPLE,
    ERR_BAD_DOMAIN,
    ERR_BAD_VERSION,
    NomosUrnError,
    audit_critical_urn_sample,
    format_nomos_urn,
    is_well_formed_nomos_urn,
    parse_nomos_urn,
)


def test_form_a_parse_roundtrip() -> None:
    u = parse_nomos_urn("urn:omega:math:cech_cochain:v1.0.0")
    assert u.domain == "math"
    assert u.name == "cech_cochain"
    assert u.version == "1.0.0"
    assert not u.file_locus
    assert u.crate_name is None
    assert format_nomos_urn(u) == "urn:omega:math:cech_cochain:v1.0.0"


def test_form_b_rust_binding() -> None:
    raw = (
        "urn:omega:rust:omega_discrete_deformation_algebra:"
        "discrete_deformation_algebra:v1.13.0"
    )
    u = parse_nomos_urn(raw)
    assert u.domain == "rust"
    assert u.crate_name == "omega_discrete_deformation_algebra"
    assert u.name == "discrete_deformation_algebra"
    assert u.version == "1.13.0"
    assert format_nomos_urn(u) == raw


def test_form_c_file_locus() -> None:
    u = parse_nomos_urn("urn:omega:engine:cycle_aware_engine:file:v1.0.0")
    assert u.file_locus
    assert u.domain == "engine"
    assert u.name == "cycle_aware_engine"


def test_hyphen_name_allowed() -> None:
    u = parse_nomos_urn("urn:omega:execution:omega-runtime:v1.0.0")
    assert u.name == "omega-runtime"


def test_negative_sample_all_reject() -> None:
    for urn in CRITICAL_URN_NEGATIVE_SAMPLE:
        assert not is_well_formed_nomos_urn(urn), f"expected reject for {urn!r}"


def test_critical_sample_all_pass() -> None:
    r = audit_critical_urn_sample()
    assert r["all_positive_pass"], r
    assert r["all_negative_reject"], r
    assert r["pass_count"] == len(CRITICAL_URN_SAMPLE)
    assert r["authority_effect"] == "None"
    assert r["story_id"] == "STORY-ORT-CONTRACTS-001"


def test_mutation_leading_zero_version_killed() -> None:
    with pytest.raises(NomosUrnError) as ei:
        parse_nomos_urn("urn:omega:math:x:v01.0.0")
    assert ei.value.kind == ERR_BAD_VERSION


def test_mutation_uppercase_domain_killed() -> None:
    with pytest.raises(NomosUrnError) as ei:
        parse_nomos_urn("urn:omega:Math:x:v1.0.0")
    assert ei.value.kind == ERR_BAD_DOMAIN


def test_mutation_prefix_only_insufficient() -> None:
    assert not is_well_formed_nomos_urn("urn:omega:math")
    assert not is_well_formed_nomos_urn("urn:omega:math:x:1.0.0")


def test_sample_size_stable() -> None:
    """Parity lock: Rust CRITICAL_URN_SAMPLE len must match (16)."""
    assert len(CRITICAL_URN_SAMPLE) == 16
    assert len(CRITICAL_URN_NEGATIVE_SAMPLE) == 13


