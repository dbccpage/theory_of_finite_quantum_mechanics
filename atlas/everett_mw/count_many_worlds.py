"""Validate whole numbered post sections in threads_many_worlds.md (limit 500)."""
from pathlib import Path
import re
import sys


HEADING = re.compile(r"^[ \t]*#{1,6}(?:\s|$)")
POST = re.compile(r"## Post (\d+) — (.+?) \((\d+) characters\)")


def posts(text):
    """Read every post up to the next heading, excluding the final sources section."""
    result, body, seen = [], [], set()
    current = None
    sources = False

    def finish():
        if current is not None:
            content = "\n".join(body).strip("\n")
            if not content.strip():
                raise ValueError(f"Post {current[0]} has no text")
            result.append((*current, content))

    for line in text.split("\n"):
        if not HEADING.match(line):
            if current is not None:
                body.append(line)
            continue
        match = POST.fullmatch(line)
        if match:
            if sources:
                raise ValueError("A post appears after the sources section")
            finish()
            number, title, stated = int(match[1]), match[2], int(match[3])
            if number in seen:
                raise ValueError(f"Duplicate Post {number}")
            seen.add(number)
            current, body = (number, title, stated), []
        elif line == "## Sources behind each claim" and not sources:
            finish()
            current, sources = None, True
        elif line.startswith("# ") and not seen and not sources and not re.search(r"\bPost\b", line):
            continue  # Document title before the numbered sections.
        else:
            raise ValueError(f"Malformed or unexpected heading: {line}")
    finish()
    if not result:
        raise ValueError("No numbered posts found")
    return result


def main():
    try:
        parsed = posts(Path("threads_many_worlds.md").read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        print(f"count_many_worlds: {error}", file=sys.stderr)
        return 1
    bad = False
    for number, title, stated, body in parsed:
        n = len(body)
        ok = n <= 500 and n == stated
        bad |= not ok
        print(f"Post {number} ({title}): {n} characters (limit 500; heading says {stated})"
              f"{'' if ok else '  MISMATCH'}")
    return int(bad)


if __name__ == "__main__":
    sys.exit(main())
