import re
from pathlib import Path
import sys

FORBIDDEN = [
    'proves', 'guarantees', 'mathematically verifies', 'fundamentally',
    'true intelligence', 'impossible', 'universal', 'flawless',
    'perfectly', 'clearly', 'obviously', 'simply', 'merely', 'weaponized'
]

pattern = re.compile(r'\b(' + '|'.join(re.escape(w) for w in FORBIDDEN) + r')\b', re.IGNORECASE)

files_to_check = [
    Path('dag/theory_of_finite_qm.jsonl'),
    Path('dag/theory_of_finite_qm.md'),
    Path('dag/derivations/README.md'),
] + list(Path('dag/derivations').glob('*/*.md'))

violations = []
for p in sorted(files_to_check):
    txt = p.read_text(encoding='utf-8')
    for i, line in enumerate(txt.splitlines(), 1):
        matches = pattern.findall(line)
        if matches:
            violations.append((p.as_posix(), i, matches, line.strip()))

print(f"Total files checked for Claim Hygiene: {len(files_to_check)}")
print(f"Total violations found: {len(violations)}")
if violations:
    for v in violations:
        print(f"VIOLATION: {v[0]}:{v[1]} - matches: {v[2]} in: {v[3]}")
    sys.exit(1)
else:
    print("CLAIM HYGIENE AUDIT: ZERO FORBIDDEN TOKENS FOUND. 100% CLEAN.")
