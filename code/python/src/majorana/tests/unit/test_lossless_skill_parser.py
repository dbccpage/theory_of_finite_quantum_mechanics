"""A skill document must survive a parse and a render unchanged.

`EPIC-OE-OEWAS-002` deliverable 1 asks for a parser "preserving line endings,
markdown formatting, and YAML AST nodes", and deliverable 4 for "non-regression
test vectors asserting zero AST mutation during roundtrip serialization".

The existing `parse_skill_frontmatter` is the *reading* parser and is
deliberately lossy -- it returns a mapping, discarding key order, comments,
quoting, blank lines, the body and the file's line endings. That is right for
asking what a skill declares and unusable for writing one back.

This parser is lossless **by construction**: it partitions the bytes and never
transforms them, so `render(parse(x)) == x` holds because no step could change a
byte. That distinction is the substance of the sprint. A parser that
reconstructs from a model is lossless only for the cases someone tested; a
parser that partitions is lossless for inputs nobody anticipated.

"By construction" is still a claim, so the corpus tests below run the whole
estate through it -- every skill package, and every frontmatter-bearing markdown
file across four hosts. Those are the non-regression vectors deliverable 4 asks
for, and they are real files rather than fixtures, so they cannot drift away from
what ships.

The corpus is counted, never quoted. Earlier revisions of this file wrote the
sizes into the assertions and the prose alike; the estate grew, and the numbers
became a claim about a corpus that had moved on. What is asserted now are the
properties that hold at any size: nothing is empty, every package appears on all
four hosts, and every document lands in exactly one of the two buckets.
"""

from __future__ import annotations

import pathlib

import pytest

from omega_engine_workflows_agents_skills.infrastructure.lossless_skill_parser import (
    LosslessParseError,
    parse_bytes,
    parse_path,
    round_trips,
)


def _find_repo_root() -> pathlib.Path:
    here = pathlib.Path(__file__).resolve()
    for candidate in [here, *here.parents]:
        if (candidate / ".git").exists():
            return candidate
    return here.parents[5]


REPO_ROOT = _find_repo_root()
HOSTS = (".agents", ".claude", ".codex", ".grok")


def skill_packages() -> list[pathlib.Path]:
    return sorted((REPO_ROOT / ".agents" / "skills").glob("*/SKILL.md"))


def all_host_markdown() -> list[pathlib.Path]:
    found: list[pathlib.Path] = []
    for host in HOSTS:
        found.extend(sorted((REPO_ROOT / host / "skills").rglob("*.md")))
    return found


# --------------------------------------------------------------------------
# The corpus vectors -- deliverable 4
# --------------------------------------------------------------------------


def test_the_estate_has_skills_to_test_against():
    """Anti-vacuity. A parser that round-trips nothing round-trips perfectly.

    Asserted as a relationship rather than a census. The literals here were 110
    and 692 and both were stale: the garden reached 112 and the corpus 700, so
    this test reported the estate's growth as the parser's defect and stayed red
    for twenty-five sprints. A count written into a test is a claim about a
    moving corpus that nothing keeps current.

    What the corpus must satisfy is that it is non-empty and that every package
    appears on all four hosts -- which is the four-host law, and is true at any
    size.
    """
    packages = skill_packages()
    documents = all_host_markdown()
    assert packages, "no skill packages found; the round-trip tests below are vacuous"
    assert len(documents) >= 4 * len(packages), (
        f"{len(documents)} host documents against {len(packages)} packages; "
        "each package should appear under all four host roots"
    )


def test_every_skill_package_round_trips_byte_for_byte():
    """Real files, not fixtures, so the vectors cannot drift from what ships."""
    failures = [
        path.relative_to(REPO_ROOT).as_posix()
        for path in skill_packages()
        if not round_trips(path)
    ]
    assert not failures, f"documents that did not survive a round trip: {failures}"


def test_every_frontmatter_bearing_document_across_four_hosts_round_trips():
    """Every host document either round-trips exactly or is refused by name.

    The partition is the property, not the tally. The previous form pinned
    `exact == 488` and `refused == 204`; both drifted with the corpus and neither
    could tell a document that was *dropped* from one that was *added*. Asserting
    that the two buckets sum to the corpus does exactly that, at any size: a
    document silently skipped is a document in neither bucket.
    """
    exact = 0
    refused = 0
    mismatched: list[str] = []
    for path in all_host_markdown():
        raw = path.read_bytes()
        try:
            document = parse_bytes(raw)
        except LosslessParseError as error:
            assert error.code == "NO_FRONTMATTER", f"{path}: {error}"
            refused += 1
            continue
        if document.render() == raw:
            exact += 1
        else:
            mismatched.append(path.relative_to(REPO_ROOT).as_posix())
    assert not mismatched, f"round-trip mismatches: {mismatched}"
    total = len(all_host_markdown())
    assert exact + refused == total, (
        f"{exact} round-tripped + {refused} refused != {total} documents; "
        "a document reached neither bucket and was silently skipped"
    )
    assert exact > 0, "no document round-tripped; the exact branch is unexercised"
    assert refused > 0, "no document was refused; the refusal branch is unexercised"


def test_a_reference_document_without_frontmatter_is_refused_not_defaulted():
    """Refused for the reason `fs_reader` gives: no defaulted signature."""
    with pytest.raises(LosslessParseError) as excinfo:
        parse_bytes(b"# Just a heading\n\nSome prose.\n")
    assert excinfo.value.code == "NO_FRONTMATTER"
    assert "defaulted" in str(excinfo.value)


# --------------------------------------------------------------------------
# Line endings are recorded, never normalised
# --------------------------------------------------------------------------


def test_a_crlf_document_round_trips_as_crlf():
    """The defect sprints 002 and 005 both found: a writer that silently converts.

    This repository is LF-only, so a parser that normalised CRLF would dirty any
    CRLF file it was asked to edit -- and would do it invisibly, because the
    content would be unchanged.
    """
    raw = b"---\r\nname: x\r\n---\r\n\r\nbody\r\n"
    document = parse_bytes(raw)
    assert document.render() == raw
    assert document.newline == b"\r\n"


def test_an_lf_document_reports_lf():
    document = parse_bytes(b"---\nname: x\n---\n\nbody\n")
    assert document.newline == b"\n"


def test_a_document_with_no_trailing_newline_round_trips():
    raw = b"---\nname: x\n---\nbody"
    assert parse_bytes(raw).render() == raw


def test_trailing_whitespace_in_the_body_survives():
    """Markdown is whitespace-sensitive; two trailing spaces are a line break."""
    raw = b"---\nname: x\n---\n\nline one  \nline two\n"
    assert parse_bytes(raw).render() == raw


# --------------------------------------------------------------------------
# Frontmatter detail the mapping view discards
# --------------------------------------------------------------------------


def test_comments_in_frontmatter_survive_the_round_trip():
    raw = b"---\n# why this skill exists\nname: x\n---\n\nbody\n"
    document = parse_bytes(raw)
    assert document.render() == raw
    assert b"# why this skill exists" in document.frontmatter


def test_key_order_is_reported_from_the_source():
    """`frontmatter_mapping()` cannot promise order; reading the lines can."""
    document = parse_bytes(b"---\nzebra: 1\nalpha: 2\nmiddle: 3\n---\n\nbody\n")
    assert document.frontmatter_keys == ("zebra", "alpha", "middle")


def test_nested_keys_are_not_reported_as_top_level():
    document = parse_bytes(
        b"---\nouter:\n  inner: 1\nsecond: 2\n---\n\nbody\n"
    )
    assert document.frontmatter_keys == ("outer", "second")


def test_a_duplicate_key_is_visible_in_source_order():
    """A mapping silently keeps the last; the source shows both."""
    document = parse_bytes(b"---\nname: a\nname: b\n---\n\nbody\n")
    assert document.frontmatter_keys == ("name", "name")


def test_the_mapping_view_is_available_and_separate():
    document = parse_bytes(b"---\nname: x\ncount: 3\n---\n\nbody\n")
    assert document.frontmatter_mapping() == {"name": "x", "count": 3}


def test_malformed_yaml_refuses_only_when_the_mapping_is_asked_for():
    """Partitioning does not need to understand the YAML.

    A document whose frontmatter is unparseable still round-trips exactly, which
    is what lets a tool move or copy a broken file without corrupting it further.
    """
    raw = b"---\nname: [unclosed\n---\n\nbody\n"
    document = parse_bytes(raw)
    assert document.render() == raw
    with pytest.raises(LosslessParseError, match="MALFORMED_YAML"):
        document.frontmatter_mapping()


# --------------------------------------------------------------------------
# Refusals
# --------------------------------------------------------------------------


def test_an_unterminated_frontmatter_block_is_refused():
    with pytest.raises(LosslessParseError) as excinfo:
        parse_bytes(b"---\nname: x\n\nbody with no closing fence\n")
    assert excinfo.value.code == "UNTERMINATED_FENCE"


def test_a_str_input_is_refused():
    """A lossless parse needs bytes; decoding first is where line endings die."""
    with pytest.raises(LosslessParseError, match="NOT_BYTES"):
        parse_bytes("---\nname: x\n---\n")


def test_a_missing_file_is_refused():
    with pytest.raises(LosslessParseError, match="MISSING"):
        parse_path(REPO_ROOT / "no" / "such" / "SKILL.md")


def test_a_fence_like_line_inside_the_body_does_not_confuse_the_parser():
    """The first `---` at column zero closes the block; later ones are body."""
    raw = b"---\nname: x\n---\n\nbody\n\n---\n\nmore body\n"
    document = parse_bytes(raw)
    assert document.render() == raw
    assert document.frontmatter == b"name: x\n"
    assert b"more body" in document.body


def test_an_empty_frontmatter_block_round_trips():
    raw = b"---\n---\n\nbody\n"
    document = parse_bytes(raw)
    assert document.render() == raw
    assert document.frontmatter == b""


# --------------------------------------------------------------------------
# The lossy parser is still the reading path, and still lossy
# --------------------------------------------------------------------------


def test_the_existing_reader_discards_what_this_parser_keeps():
    """States the difference, so neither is mistaken for the other.

    `parse_skill_frontmatter` returns a mapping. A caller that wrote a file back
    from one would lose the comment, the key order, and the body.
    """
    from omega_engine_workflows_agents_skills.infrastructure.fs_reader import (
        parse_skill_frontmatter,
    )

    text = "---\n# a comment\nzebra: 1\nalpha: 2\n---\n\nbody\n"
    mapping = parse_skill_frontmatter(text)
    assert mapping == {"zebra": 1, "alpha": 2}
    assert "a comment" not in str(mapping)

    document = parse_bytes(text.encode("utf-8"))
    assert b"# a comment" in document.frontmatter
    assert document.body == b"\nbody\n"
