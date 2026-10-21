import json
from pathlib import Path

with open('dag/theory_of_finite_qm.jsonl', encoding='utf-8') as f:
    jsonl_nodes = [json.loads(line) for line in f]

print(f"JSONL nodes count: {len(jsonl_nodes)}")

md_text = open('dag/theory_of_finite_qm.md', encoding='utf-8').read()

mismatches = []
for node in jsonl_nodes:
    nid = node['id']
    uuid = node['uuid']
    name = node['name']
    status = node['record_status']
    parent = node['parent_id'] or 'root'
    obligation = node['obligation']
    
    # Check if node header is in MD
    if f"### {nid} " not in md_text:
        mismatches.append((nid, "Header missing in MD"))
        continue
    
    # Check UUID
    if f"- UUID: `{uuid}`" not in md_text:
        mismatches.append((nid, "UUID mismatch in MD"))
        
    # Check Status
    if f"- Status: `{status}`" not in md_text:
        mismatches.append((nid, "Status mismatch in MD"))
        
    # Check Parent
    if f"- Parent: `{parent}`" not in md_text:
        mismatches.append((nid, "Parent mismatch in MD"))
        
    # Check Obligation
    if f"Obligation: {obligation}" not in md_text:
        mismatches.append((nid, "Obligation mismatch in MD"))

print(f"Total mismatches between JSONL and theory_of_finite_qm.md: {len(mismatches)}")
if mismatches:
    print("Sample mismatches:", mismatches[:10])
