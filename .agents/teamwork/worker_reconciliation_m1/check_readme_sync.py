import json
from pathlib import Path

with open('dag/theory_of_finite_qm.jsonl', encoding='utf-8') as f:
    jsonl_nodes = [json.loads(line) for line in f]

readme_text = open('dag/derivations/README.md', encoding='utf-8').read()

mismatches = []
for node in jsonl_nodes:
    nid = node['id']
    status = node['record_status']
    
    if f"[`{nid}`]" not in readme_text:
        mismatches.append((nid, "ID missing in README"))
    if f"`{status}`" not in readme_text:
        mismatches.append((nid, f"Status {status} not in README"))

print(f"Total mismatches between JSONL and README.md: {len(mismatches)}")
if mismatches:
    print("Sample mismatches:", mismatches[:10])
