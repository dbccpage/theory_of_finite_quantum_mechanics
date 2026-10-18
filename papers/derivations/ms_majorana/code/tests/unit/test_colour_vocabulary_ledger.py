"""M0 owner ledger for the operad colour vocabulary.

`EPIC-OE-OEWAS-RUST-001` stage M0 asks for duplicate models to be identified
before any port. The colour vocabulary is declared in **five** places. A comment
in the Rust crate says four, states that the sites once drifted -- dropping
`Contract` and `Diagram` and silently changing the arity of sixteen skills --
and instructs the reader to keep them in step.

Nothing enforced that. These tests do: they compare the declarations, and they
compare the number of declarations against the number the comment claims, so a
sixth site fails until it is either removed or acknowledged.

This file also pins the epic's provenance claim, which is **exactly correct in
all seven of its assertions** -- a deliberate counter-example to
`ESC-002-001`.
"""

from __future__ import annotations

import hashlib
import json
import pathlib

import pytest

from omega_engine_workflows_agents_skills.infrastructure.colour_vocabulary_ledger import (
    CANONICAL_ORDER,
    LedgerError,
    OwnerLedger,
    SiteRole,
    VocabularySite,
    build_ledger,
    disagreements,
    find_consumers,
    find_declaration_sites,
    read_claimed_site_count,
    read_rust_colours,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
RUST_MODEL = REPO_ROOT / "omega_engine/crates_rs/omega_oewas/src/model.rs"
MEMO = (
    REPO_ROOT
    / "omega_engine_product_planning_office/plans/epics/source_memos"
    / "2026-08-26_antimorphism_immunity_concept_memo.txt"
)
EPIC = (
    REPO_ROOT
    / "omega_engine_product_planning_office/plans/epics"
    / "epic_oe_oewas_rust_001_staged_convergence_plan.md"
)


@pytest.fixture(scope="module")
def ledger() -> OwnerLedger:
    return build_ledger(REPO_ROOT)


def site(symbol: str, colours: frozenset[str]) -> VocabularySite:
    return VocabularySite(
        path=f"synthetic/{symbol}.py",
        symbol=symbol,
        role=SiteRole.DECLARATION,
        colours=colours,
    )


ALL_TEN = frozenset(CANONICAL_ORDER)




def test_the_vocabulary_is_declared_five_times(ledger):
    assert len(ledger.declarations) == 5


def test_the_source_comment_claims_four(ledger):
    assert ledger.claimed_site_count == 4


def test_the_comment_undercounts_the_sites_by_one(ledger):
    """The finding in one number.

    If the comment is corrected to five, or the fifth site is removed, this
    fails and the module docstring should be revised rather than left stale.
    """
    assert ledger.undercount() == 1


def test_the_site_the_comment_omits_is_the_operad_domain_module(ledger):
    """And it is the one whose name most claims to own the vocabulary."""
    paths = {declaration.path for declaration in ledger.declarations}
    assert ".agents/operad/domain/colours.py" in paths


def test_all_declarations_currently_agree(ledger):
    """The obligation is met today, by hand. That is what makes it fragile."""
    assert ledger.drift() == ()


def test_every_declaration_carries_exactly_ten_colours(ledger):
    for declaration in ledger.declarations:
        assert declaration.colours == ALL_TEN, declaration.path


def test_the_rust_constant_is_the_canonical_order():
    """Order is only expressible on the Rust side; the Python sites are sets.

    The acceptance matrix names reordering as a decisive mutation, so the order
    is pinned where it exists rather than being lost because most sites cannot
    hold it.
    """
    source = RUST_MODEL.read_text(encoding="utf-8")
    listed = source.split("ADMITTED_COLOURS")[1].split("];")[0]
    order = [part.split('"')[1] for part in listed.split(",") if '"' in part]
    assert tuple(order) == CANONICAL_ORDER


def test_a_consumer_is_not_counted_as_a_declaration(ledger):
    """A site that uses the vocabulary holds no copy and cannot drift."""
    assert len(ledger.consumers) == 1
    assert ledger.consumers[0].role is SiteRole.CONSUMER
    assert all(d.role is SiteRole.DECLARATION for d in ledger.declarations)


def test_the_consumer_names_all_ten_without_declaring_them(ledger):
    consumer = ledger.consumers[0]
    assert consumer.colours == ALL_TEN
    document = json.loads(
        (REPO_ROOT / consumer.path).read_text(encoding="utf-8")
    )
    assert "colours" not in document


def test_no_adr_selects_a_canonical_owner():
    """Epic section 4 requires one; section 9 lists it as an open obligation.

    Pinned rather than resolved: choosing an owner is a governance decision this
    pipeline has no standing to make. If an ADR ever names one, this fails and
    the ledger's "none selected" line becomes wrong.

    The query is deliberately narrow. A first version searched for the substring
    `colour` or `color` in any ADR and matched
    `06_oeags_adr_001_...md`, which uses "not optional color" as an English
    metaphor and says nothing about the operad vocabulary. A search broad enough
    to hit that word is not a search for an ownership decision -- so the query
    names the symbols and the phrase an actual decision would have to use.
    """
    markers = (
        b"ADMITTED_COLOURS",
        b"OPERAD_COLOURS",
        b"ADMITTED_FINITE_COLOURS",
        b"colour vocabulary",
        b"color vocabulary",
    )
    adrs = [
        path
        for path in REPO_ROOT.rglob("*adr*.md")
        if "target" not in path.parts and "library" not in path.parts
    ]
    assert adrs, "the search found no ADRs at all; the query is wrong"
    naming = [
        path.name
        for path in adrs
        if any(marker in path.read_bytes() for marker in markers)
    ]
    assert naming == [], f"an ADR now names a colour-vocabulary owner: {naming}"


def test_the_narrow_adr_query_would_find_a_real_decision(tmp_path):
    """The previous test asserts an absence, so its query must be shown to work.

    An absence test with a broken query passes for the wrong reason forever.
    This constructs the decision the estate does not have and confirms the same
    marker set finds it.
    """
    adr = tmp_path / "adr_001_colour_owner.md"
    adr.write_text(
        "# ADR 001\n\nThe canonical colour vocabulary owner is "
        "`ADMITTED_COLOURS` in `omega_oewas`.\n",
        encoding="utf-8",
    )
    markers = (
        b"ADMITTED_COLOURS",
        b"OPERAD_COLOURS",
        b"ADMITTED_FINITE_COLOURS",
        b"colour vocabulary",
        b"color vocabulary",
    )
    found = [
        path.name
        for path in tmp_path.rglob("*adr*.md")
        if any(marker in path.read_bytes() for marker in markers)
    ]
    assert found == ["adr_001_colour_owner.md"]


def test_the_report_states_that_no_owner_is_selected(ledger):
    assert "none selected" in ledger.render()




def test_the_memo_matches_its_declared_digest():
    raw = MEMO.read_bytes()
    assert (
        hashlib.sha256(raw).hexdigest()
        == "cb36f18de3b1e1086c96da4e6691aef57e6baeb70bb2c0ae0e00ee39a6200653"
    )


def test_the_memo_matches_its_declared_byte_count():
    assert len(MEMO.read_bytes()) == 50344


def test_the_memo_matches_its_declared_line_count_and_ending():
    """655 CRLF-terminated lines, and no bare LF hiding among them."""
    raw = MEMO.read_bytes()
    assert raw.count(b"\r\n") == 655
    assert raw.count(b"\n") - raw.count(b"\r\n") == 0


def test_the_memo_is_utf8_without_bom_and_ends_with_a_newline():
    raw = MEMO.read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf")
    assert raw.endswith(b"\n")
    raw.decode("utf-8")


def test_the_epic_states_every_number_this_file_checks():
    """The claims are pinned to the epic, not to a copy of them here."""
    text = EPIC.read_text(encoding="utf-8")
    assert "cb36f18de3b1e1086c96da4e6691aef57e6baeb70bb2c0ae0e00ee39a6200653" in text
    assert "50,344 exact bytes" in text
    assert "655 CRLF-terminated" in text


def test_the_five_named_rust_crates_all_exist():
    """Epic section 2 lists them as already present. They are."""
    crates = REPO_ROOT / "omega_engine" / "crates_rs"
    for name in (
        "omega_oewas",
        "omega_operad_theory",
        "omega_prompt_civilization",
        "omega_symbol_game_runtime",
        "omega_symbol_game",
    ):
        assert (crates / name / "Cargo.toml").is_file(), name




def test_a_dropped_colour_is_named():
    """The historical failure: `Contract` and `Diagram` went missing."""
    reduced = ALL_TEN - {"Contract", "Diagram"}
    problems = disagreements((site("a", ALL_TEN), site("b", reduced)))
    assert any("missing Contract, Diagram" in problem for problem in problems)


def test_an_added_colour_is_named():
    problems = disagreements((site("a", ALL_TEN), site("b", ALL_TEN | {"Vibes"})))
    assert any("adds Vibes" in problem for problem in problems)


def test_every_disagreeing_site_is_reported_not_just_the_first():
    problems = disagreements(
        (
            site("a", ALL_TEN),
            site("b", ALL_TEN - {"Audit"}),
            site("c", ALL_TEN - {"Post"}),
        )
    )
    assert any("b" in p and "Audit" in p for p in problems)
    assert any("c" in p and "Post" in p for p in problems)


def test_agreeing_sites_report_nothing():
    assert disagreements((site("a", ALL_TEN), site("b", ALL_TEN))) == ()


def test_comparing_fewer_than_two_declarations_is_refused():
    """One site cannot disagree with anything; reporting `()` would read clean."""
    with pytest.raises(LedgerError) as excinfo:
        disagreements((site("only", ALL_TEN),))
    assert excinfo.value.code == "TOO_FEW_SITES"


def test_an_empty_declaration_is_refused():
    """An empty vocabulary is a subset of everything and would read as agreeing."""
    with pytest.raises(LedgerError) as excinfo:
        VocabularySite(
            path="p", symbol="s", role=SiteRole.DECLARATION, colours=frozenset()
        )
    assert excinfo.value.code == "EMPTY_DECLARATION"


def test_a_consumer_may_be_empty():
    """A consumer holds no copy, so an empty one is meaningful rather than broken."""
    VocabularySite(
        path="p", symbol="s", role=SiteRole.CONSUMER, colours=frozenset()
    )




def test_an_annotated_assignment_is_found(tmp_path):
    """The bug that hid the fifth site.

    `ADMITTED_FINITE_COLOURS: FrozenSet[str] = frozenset({...})` is an
    `ast.AnnAssign`, not an `ast.Assign`. A walker that only looked at `Assign`
    returned four sites and looked correct.
    """
    from omega_engine_workflows_agents_skills.infrastructure import (
        colour_vocabulary_ledger as module,
    )

    source = 'X: FrozenSet[str] = frozenset({"Audit", "Code"})\n'
    assert module._python_string_collection(source, "X") == frozenset(
        {"Audit", "Code"}
    )


def test_a_plain_assignment_is_found():
    from omega_engine_workflows_agents_skills.infrastructure import (
        colour_vocabulary_ledger as module,
    )

    source = 'X = ("Audit", "Code")\n'
    assert module._python_string_collection(source, "X") == frozenset(
        {"Audit", "Code"}
    )


def test_an_absent_symbol_returns_none():
    from omega_engine_workflows_agents_skills.infrastructure import (
        colour_vocabulary_ledger as module,
    )

    assert module._python_string_collection("Y = 1\n", "X") is None


def test_a_rust_array_whose_declared_length_lies_is_refused(tmp_path):
    """`[&str; 10]` listing nine is a drift the compiler would catch, and a
    reader would not."""
    model = tmp_path / "omega_engine/crates_rs/omega_oewas/src/model.rs"
    model.parent.mkdir(parents=True)
    model.write_text(
        'pub const ADMITTED_COLOURS: [&str; 10] = ["Audit", "Code"];\n',
        encoding="utf-8",
    )
    with pytest.raises(LedgerError) as excinfo:
        read_rust_colours(tmp_path)
    assert excinfo.value.code == "RUST_LENGTH_MISMATCH"


def test_a_rust_model_without_the_constant_is_refused(tmp_path):
    model = tmp_path / "omega_engine/crates_rs/omega_oewas/src/model.rs"
    model.parent.mkdir(parents=True)
    model.write_text("// nothing here\n", encoding="utf-8")
    with pytest.raises(LedgerError) as excinfo:
        read_rust_colours(tmp_path)
    assert excinfo.value.code == "RUST_UNREADABLE"


def test_the_claimed_count_is_read_from_the_comment(tmp_path):
    model = tmp_path / "omega_engine/crates_rs/omega_oewas/src/model.rs"
    model.parent.mkdir(parents=True)
    model.write_text("/// Keep all seven in step.\n", encoding="utf-8")
    assert read_claimed_site_count(tmp_path) == 7


def test_a_missing_claim_is_refused(tmp_path):
    """Deleting the obligation must fail loudly, not silently pass."""
    model = tmp_path / "omega_engine/crates_rs/omega_oewas/src/model.rs"
    model.parent.mkdir(parents=True)
    model.write_text("/// no obligation stated\n", encoding="utf-8")
    with pytest.raises(LedgerError) as excinfo:
        read_claimed_site_count(tmp_path)
    assert excinfo.value.code == "CLAIM_ABSENT"


def test_an_unreadable_number_word_is_refused(tmp_path):
    model = tmp_path / "omega_engine/crates_rs/omega_oewas/src/model.rs"
    model.parent.mkdir(parents=True)
    model.write_text("/// Keep all several in step.\n", encoding="utf-8")
    with pytest.raises(LedgerError) as excinfo:
        read_claimed_site_count(tmp_path)
    assert excinfo.value.code == "CLAIM_UNREADABLE"


def test_a_vanished_declaration_site_is_refused(tmp_path):
    """A ledger that silently drops a site it cannot find reports false agreement."""
    (tmp_path / "omega_engine/crates_rs/omega_oewas/src").mkdir(parents=True)
    (tmp_path / "omega_engine/crates_rs/omega_oewas/src/model.rs").write_text(
        'pub const ADMITTED_COLOURS: [&str; 1] = ["Audit"];\n', encoding="utf-8"
    )
    with pytest.raises(LedgerError) as excinfo:
        find_declaration_sites(tmp_path)
    assert excinfo.value.code == "SITE_ABSENT"


def test_the_consumer_becoming_a_declaration_is_refused(tmp_path):
    slices = tmp_path / ".agents/operad/agent_capability_slices.json"
    slices.parent.mkdir(parents=True)
    slices.write_text(json.dumps({"colours": ["Audit"]}), encoding="utf-8")
    with pytest.raises(LedgerError) as excinfo:
        find_consumers(tmp_path)
    assert excinfo.value.code == "ROLE_CHANGED"


def test_the_live_sites_are_all_readable(ledger):
    """Every extractor reached its target; none silently returned nothing."""
    assert len(find_declaration_sites(REPO_ROOT)) == len(ledger.declarations)
    for declaration in ledger.declarations:
        assert (REPO_ROOT / declaration.path).exists()
