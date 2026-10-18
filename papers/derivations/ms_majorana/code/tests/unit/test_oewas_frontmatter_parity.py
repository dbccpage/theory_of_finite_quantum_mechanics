"""Frontmatter parsing parity between the Python and Rust estate readers.

Two divergences existed, in opposite directions, and both meant one `SKILL.md`
could compile to two different operations depending on which reader saw it:

- A document with no frontmatter was `{}` in Python -- every declared field
  falling to a default -- and an error in Rust.
- A document whose closing fence ended the file with no trailing newline
  parsed fully in Rust and read as having no frontmatter in Python.

Resolved toward the stricter reading in the first case and the more forgiving
one in the second, on the same principle: a skill that declares no signature
must not be handed a fabricated one, and a document's meaning must not turn on
an invisible trailing byte.

Neither case appears in the 142 shipped skills, so this fixes latent drift
rather than live breakage.

The Rust side is `omega_engine/crates_rs/omega_oewas/src/estate.rs`
(`split_frontmatter`) and its tests.

AuthorityEffect: None.
"""

from __future__ import annotations

import pytest

from omega_engine_workflows_agents_skills.infrastructure.fs_reader import (
    MissingFrontmatterError,
    parse_skill_frontmatter,
)

BODY = "name: demo\noperad_arity: 2\n"


def test_ordinary_frontmatter_parses() -> None:
    assert parse_skill_frontmatter(f"---\n{BODY}---\n\n# Heading\n")["operad_arity"] == 2


def test_a_closing_fence_at_end_of_file_still_parses() -> None:
    """The whole divergence: no trailing newline after the final `---`."""
    assert parse_skill_frontmatter(f"---\n{BODY}---")["name"] == "demo"


def test_a_closing_fence_with_trailing_spaces_at_end_of_file_parses() -> None:
    assert parse_skill_frontmatter(f"---\n{BODY}---  ")["name"] == "demo"


def test_a_closing_fence_with_a_carriage_return_parses() -> None:
    assert parse_skill_frontmatter(f"---\r\n{BODY}---\r\n")["name"] == "demo"


def test_a_document_with_no_frontmatter_is_refused() -> None:
    with pytest.raises(MissingFrontmatterError):
        parse_skill_frontmatter("# Just a heading\n\nSome prose.\n")


def test_an_unterminated_frontmatter_block_is_refused() -> None:
    """An opening fence with no closing fence is not a frontmatter block."""
    with pytest.raises(MissingFrontmatterError):
        parse_skill_frontmatter(f"---\n{BODY}\n# no closing fence\n")


def test_an_empty_document_is_refused() -> None:
    with pytest.raises(MissingFrontmatterError):
        parse_skill_frontmatter("")


def test_a_dashed_rule_in_the_body_does_not_close_the_block() -> None:
    """`---` mid-line or inside a scalar must not be read as the fence."""
    parsed = parse_skill_frontmatter(f"---\ndescription: 'a --- b'\n{BODY}---\n")
    assert parsed["description"] == "a --- b"
    assert parsed["operad_arity"] == 2


def test_every_shipped_skill_still_parses() -> None:
    """The change must not make any of the live estate unreadable.

    This is the check that matters: the strict branch is only safe because
    nothing shipped relies on the defaulting it removes.
    """
    from pathlib import Path

    root = Path(__file__).resolve().parents[2] / ".agents" / "skills"
    if not root.is_dir():
        pytest.skip(f"skill estate not present at {root}")

    skills = sorted(root.rglob("SKILL.md"))
    assert len(skills) >= 100, f"expected the full estate, found {len(skills)}"

    for skill in skills:
        parsed = parse_skill_frontmatter(skill.read_text(encoding="utf-8"))
        assert isinstance(parsed, dict), skill
