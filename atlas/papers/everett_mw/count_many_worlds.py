"""Count the Threads posts in threads_many_worlds.md (len() of the exact text; limit 500)."""
import pathlib, re, sys
t = pathlib.Path("threads_many_worlds.md").read_text(encoding="utf-8")
bad = 0
for m in re.finditer(r"^## (Post \d+) — (.+?) \((\d+) characters\)\n\n(.+?)\n", t, re.M):
    name, title, stated, body = m.group(1), m.group(2), int(m.group(3)), m.group(4)
    n = len(body)
    ok = n <= 500 and n == stated
    bad += not ok
    print(f"{name} ({title}): {n} characters (limit 500; heading says {stated}){'' if ok else '  MISMATCH'}")
sys.exit(1 if bad else 0)
