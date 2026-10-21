import json
from pathlib import Path
import re

with open('dag/theory_of_finite_qm.jsonl', encoding='utf-8') as f:
    jsonl_nodes = {row['id']: row for row in (json.loads(line) for line in f)}

monographs = list(Path('dag/derivations').glob('*/*.md'))
print(f"Total monographs found: {len(monographs)}")

id_to_file = {}
for p in monographs:
    # Match ID from filename or content
    txt = p.read_text(encoding='utf-8')
    m = re.search(r'# \[(TFQ-\d{4})\]', txt)
    if m:
        id_to_file[m.group(1)] = (p, txt)
    else:
        print(f"Could not find ID in {p}")

print(f"Matched monograph IDs: {len(id_to_file)}")

mismatches = []
for nid, row in jsonl_nodes.items():
    if nid not in id_to_file:
        mismatches.append((nid, "File missing"))
        continue
    p, txt = id_to_file[nid]
    
    # Check UUID
    if row['uuid'] not in txt:
        mismatches.append((nid, "UUID mismatch in file"))
        
    # Check Status
    if f"`{row['record_status']}`" not in txt:
        mismatches.append((nid, f"Status `{row['record_status']}` not in file"))
        
    # Check Obligation
    # Normalize whitespace for check
    clean_obl = " ".join(row['obligation'].split())
    clean_txt = " ".join(txt.split())
    if clean_obl not in clean_txt:
        mismatches.append((nid, "Obligation mismatch in file"))

print(f"Total mismatches: {len(mismatches)}")
if mismatches:
    print("Sample mismatches:", mismatches[:10])
