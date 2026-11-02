"""Count the Threads-safe formulation and the classroom pocket version (limit 500)."""
import pathlib, sys
def quoted(fn, start):
    t = pathlib.Path(fn).read_text(encoding="utf-8")
    q = t[t.index("> " + start) + 2:]
    return q[:q.index("\n")]
bad = 0
for fn, start in [("where_to_contest_multiverse_realism.md", "Everett removes one rule"),
                  ("marbles_to_everett.md", "Marbles through two holes")]:
    n = len(quoted(fn, start))
    bad += n > 500
    print(f"{fn}: {n} chars (limit 500)")
sys.exit(1 if bad else 0)
