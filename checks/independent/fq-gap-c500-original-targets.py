"""Independent census of the ten C500 block entries in gap_register.yaml.

No repository imports. Reads the gap register as text.
"""

from pathlib import Path

failures = 0
checked = 0


def check(cond, msg):
    global failures, checked
    checked += 1
    if not cond:
        failures += 1
        print("FAIL", msg)


lines = Path("sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml").read_text(encoding="utf-8").splitlines()
starts = [i for i, line in enumerate(lines) if line.startswith("- gap_id: GAP-C500-B")]
blocks = []
for a, b in zip(starts, starts[1:] + [len(lines)]):
    chunk = []
    for line in lines[a:b]:
        if chunk and line.startswith("- gap_id:"):
            break
        chunk.append(line)
    gid = chunk[0].split(":", 1)[1].strip()
    fields = {}
    mode = None
    lists = {"unresolved_targets": [], "open_or_invalid_bet_clauses": [], "evidence": []}
    desc = []
    for line in chunk[1:]:
        if line.startswith("  ") and not line.startswith("   ") and line[2:3] != "-" and ":" in line:
            key, rest = line.split(":", 1)
            key = key.strip()
            rest = rest.strip()
            if key in lists and rest == "":
                mode = key
            elif key in lists and rest == "[]":
                mode = None
            elif key == "description":
                mode = "description"
                desc = [rest.strip("'")]
            else:
                mode = None
                fields[key] = rest.strip("'")
        elif mode in lists and line.startswith("  - "):
            lists[mode].append(line.split("-", 1)[1].strip())
        elif mode == "description" and (line.startswith("    ") or line.startswith("  description:")):
            desc.append(line.strip().strip("'"))
    blocks.append((gid, fields, lists, " ".join(desc)))

expected_ids = [f"GAP-C500-B{n:02d}" for n in range(1, 11)]
expected_clauses = [
    [],
    ["M2", "M5"],
    ["M1", "M3", "M5", "J2"],
    ["M3", "M5"],
    ["M2", "M5", "M6", "J2"],
    ["M5"],
    ["M6"],
    ["M6"],
    ["M6"],
    ["M2", "M5", "M7", "J1", "J2"],
]
expected_targets = [f"C500-T{n}" for n in range(301, 551)]

check([b[0] for b in blocks] == expected_ids, "ten block ids in order")
for index, (gid, fields, lists, desc) in enumerate(blocks):
    nn = f"{index + 1:02d}"
    check(fields.get("title") == f"C500 Block {nn} original target contract remains open", f"{gid} title")
    check(fields.get("status") == "RESOLVED_WITH_SCOPED_EVIDENCE", f"{gid} status")
    check(fields.get("resolution") == "RESOLVED", f"{gid} resolution")
    check(lists["unresolved_targets"] == expected_targets[25 * index : 25 * (index + 1)], f"{gid} targets")
    check(lists["open_or_invalid_bet_clauses"] == expected_clauses[index], f"{gid} clauses")

check(blocks[9][2]["open_or_invalid_bet_clauses"] == ["M2", "M5", "M7", "J1", "J2"], "block 10 clauses")
check(sum(len(row) for row in expected_clauses) == 21, "clause lengths sum to 21")
check(sum(len(b[2]["unresolved_targets"]) for b in blocks) == 250, "250 targets")
check("x^4-6*x^2+5" in blocks[8][3], "block 09 polynomial text")
check("{-sqrt(5),-1,1,sqrt(5)}" in blocks[8][3], "block 09 spectrum text")


def poly(n):
    return n ** 4 - 6 * n ** 2 + 5


check(poly(1) == 0, "poly(1) = 0")
check(poly(-1) == 0, "poly(-1) = 0")
check(5 * 5 - 6 * 5 + 5 == 0, "substitution at square 5")

# (x^2 - 5)(x^2 - 1) = x^4 - 6x^2 + 5 by integer coefficients.
left = (1, 0, -5)
right = (1, 0, -1)
coeff = [0, 0, 0, 0, 0]
for i, a in enumerate(left):
    for j, b in enumerate(right):
        coeff[i + j] += a * b
check(coeff == [1, 0, -6, 0, 5], "coefficient identity")

print(f"checked {checked} claims, failures {failures}")
raise SystemExit(failures)
