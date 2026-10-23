"""Add or remove module roots of the ImportedAtlas library in lean4/lakefile.lean.

AuthorityEffect: None.

    python -I -X utf8 lakefile_roots.py <repo> add roots.txt        # append the listed modules not yet present
    python -I -X utf8 lakefile_roots.py <repo> remove roots.txt     # drop the listed modules
"""
import re
import sys
from pathlib import Path


def main() -> int:
    repo, action, listing = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    mods = [m.strip() for m in listing.read_text(encoding="utf-8").splitlines() if m.strip()]
    path = repo / "lean4/lakefile.lean"
    text = path.read_text(encoding="utf-8")
    start = text.index("lean_lib ImportedAtlas where")
    open_i = text.index("#[", start)
    close_i = text.index("\n  ]", open_i)
    block = text[open_i + 2:close_i]
    entries = [e.strip().rstrip(",").strip() for e in block.split("\n") if e.strip()]
    if action == "add":
        for m in mods:
            tick = "`" + (m if re.fullmatch(r"[A-Za-z_][\w.]*", m) else "«" + m + "»")
            if tick not in entries:
                entries.append(tick)
    elif action == "remove":
        drop = {"`" + m for m in mods}
        entries = [e for e in entries if e not in drop]
    else:
        raise SystemExit("action must be add or remove")
    new_block = "\n" + ",\n".join("    " + e for e in entries)
    path.write_text(text[:open_i + 2] + new_block + text[close_i:], encoding="utf-8", newline="\n")
    print(action, len(mods), "modules;", len(entries), "roots now")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
