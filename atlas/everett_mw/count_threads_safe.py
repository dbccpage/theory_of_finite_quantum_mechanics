"""Validate the complete Threads-safe and classroom pocket sections (limit 500)."""
from pathlib import Path
import re
import sys


SECTIONS = [("where_to_contest_multiverse_realism.md", "# 5. A Threads-safe formulation"),
            ("marbles_to_everett.md", "### Pocket version (fits one post)")]
HEADING = re.compile(r"^(#{1,6})\s")
COUNT = re.compile(r"\((\d+) characters, counted[^\n)]*\.\)")


def quoted(text, heading):
    """Count the full section, removing quote markers and its separate count annotation.

    Unprefixed continuation lines and blank paragraphs are part of the post too.
    The count annotation must be the last nonblank line, separated from the body.
    """
    lines = text.split("\n")
    starts = [i for i, line in enumerate(lines) if line == heading]
    if len(starts) != 1:
        raise ValueError(f"Expected exactly one section: {heading}")
    level = len(heading.split(" ", 1)[0])
    section = []
    for line in lines[starts[0] + 1:]:
        next_heading = HEADING.match(line)
        if next_heading:
            if len(next_heading[1]) <= level:
                break
            raise ValueError(f"Unexpected subheading inside post: {line}")
        section.append(line)
    while section and not section[0].strip():
        section.pop(0)
    if not section or not re.match(r"^>(?:\s|$)", section[0]):
        raise ValueError(f"Missing quoted post in {heading}")
    # Remove a single Markdown quote marker, retaining the rest of each line.
    content = [re.sub(r"^> ?", "", line) for line in section]
    while content and not content[-1].strip():
        content.pop()
    annotation = COUNT.fullmatch(content[-1]) if content else None
    if not annotation or len(content) < 3 or content[-2].strip():
        raise ValueError(f"Missing or malformed trailing character count in {heading}")
    body = "\n".join(content[:-1]).strip("\n")
    if not body.strip():
        raise ValueError(f"Empty post in {heading}")
    return body, int(annotation[1])


def main():
    bad = False
    for filename, heading in SECTIONS:
        try:
            body, stated = quoted(Path(filename).read_text(encoding="utf-8"), heading)
        except (OSError, ValueError) as error:
            print(f"{filename}: {error}", file=sys.stderr)
            bad = True
            continue
        n = len(body)
        ok = n <= 500 and n == stated
        bad |= not ok
        print(f"{filename}: {n} chars (limit 500; annotation says {stated})"
              f"{'' if ok else '  MISMATCH'}")
    return int(bad)


if __name__ == "__main__":
    sys.exit(main())
