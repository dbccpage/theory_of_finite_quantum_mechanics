import re
import json

def extract_mub_derivs():
    with open('papers/core/mub6/theory_of_finite_mub6.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Matches pattern: ### MUB6-DERIV-XXX: Title
    blocks = re.split(r'###\s+(MUB6-DERIV-\d+):', content)
    derivs = []
    for i in range(1, len(blocks), 2):
        did = blocks[i]
        block = blocks[i+1]
        lines = block.strip().split('\n')
        title = lines[0].strip()
        
        uuid_m = re.search(r'\*\*UUID:\*\*\s+`([^`]+)`', block)
        uuid = uuid_m.group(1) if uuid_m else "N/A"
        
        py_m = re.search(r'-\s+\*\*Python:\*\*\s+`?([^`\n]+)`?', block)
        py = py_m.group(1).strip() if py_m else "N/A"
        
        rust_m = re.search(r'-\s+\*\*Rust:\*\*\s+`?([^`\n]+)`?', block)
        rust = rust_m.group(1).strip() if rust_m else "N/A"
        
        lean_m = re.search(r'-\s+\*\*Lean 4:\*\*\s+`?([^`\n]+)`?', block)
        lean = lean_m.group(1).strip() if lean_m else "N/A"
        
        derivs.append({
            'id': did,
            'title': title,
            'uuid': uuid,
            'python': py,
            'rust': rust,
            'lean4': lean
        })
    print(f"Extracted {len(derivs)} MUB derivations")
    return derivs

def extract_fsp_derivs():
    with open('papers/core/fsp/theory_of_finite_fsp.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    blocks = re.split(r'####\s+(FSP-DERIV-\d+):', content)
    derivs = []
    for i in range(1, len(blocks), 2):
        did = blocks[i]
        block = blocks[i+1]
        lines = block.strip().split('\n')
        title = lines[0].strip()
        
        uuid_m = re.search(r'\*\*UUID:\*\*\s+`([^`]+)`', block)
        uuid = uuid_m.group(1) if uuid_m else "N/A"
        
        status_m = re.search(r'\*\*Status:\*\*\s+`?([^`\n]+)`?', block)
        status = status_m.group(1).strip() if status_m else "VERIFIED"
        
        py_m = re.search(r'\*\s+\*\*Python:\*\*\s+\[`?([^`\]]+)`?\]', block)
        py = py_m.group(1) if py_m else "N/A"
        
        rust_m = re.search(r'\*\s+\*\*Rust:\*\*\s+\[`?([^`\]]+)`?\]', block)
        rust = rust_m.group(1) if rust_m else "N/A"
        
        lean_m = re.search(r'\*\s+\*\*Lean 4:\*\*\s+\[`?([^`\]]+)`?\]', block)
        lean = lean_m.group(1) if lean_m else "N/A"
        
        derivs.append({
            'id': did,
            'title': title,
            'uuid': uuid,
            'status': status,
            'python': py,
            'rust': rust,
            'lean4': lean
        })
    print(f"Extracted {len(derivs)} FSP derivations")
    return derivs

if __name__ == '__main__':
    mub_d = extract_mub_derivs()
    fsp_d = extract_fsp_derivs()
    with open('.agents/teamwork/worker_m4_matrix/derivations_extracted.json', 'w', encoding='utf-8') as out:
        json.dump({'mub_derivs': mub_d, 'fsp_derivs': fsp_d}, out, indent=2)
    print("Saved derivations_extracted.json")
