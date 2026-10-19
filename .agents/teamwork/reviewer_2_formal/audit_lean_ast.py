import os
import re

lean_dir = 'lean4'
files = [f for f in os.listdir(lean_dir) if f.endswith('.lean')]

sorry_hits = []
admit_hits = []
axiom_hits = []

def strip_comments_and_strings(code):
    res = []
    i = 0
    n = len(code)
    in_string = False
    comment_depth = 0
    in_line_comment = False
    while i < n:
        if in_string:
            if code[i] == '\\':
                i += 2
                continue
            elif code[i] == '"':
                in_string = False
            i += 1
            continue
        if in_line_comment:
            if code[i] == '\n':
                in_line_comment = False
                res.append('\n')
            i += 1
            continue
        if comment_depth > 0:
            if i + 1 < n and code[i:i+2] == '/-':
                comment_depth += 1
                i += 2
                continue
            elif i + 1 < n and code[i:i+2] == '-/':
                comment_depth -= 1
                i += 2
                continue
            elif code[i] == '\n':
                res.append('\n')
            i += 1
            continue
        # normal code
        if code[i] == '"':
            in_string = True
            i += 1
            continue
        if i + 1 < n and code[i:i+2] == '--':
            in_line_comment = True
            i += 2
            continue
        if i + 1 < n and code[i:i+2] == '/-':
            comment_depth += 1
            i += 2
            continue
        res.append(code[i])
        i += 1
    return ''.join(res)

for f in sorted(files):
    path = os.path.join(lean_dir, f)
    raw = open(path, encoding='utf-8', errors='ignore').read()
    clean = strip_comments_and_strings(raw)
    
    # Check sorry
    for m in re.finditer(r'\b(sorry)\b', clean):
        line_no = raw[:m.start()].count('\n') + 1
        raw_lines = raw.splitlines()
        line_text = raw_lines[line_no - 1] if line_no <= len(raw_lines) else ''
        sorry_hits.append((f, line_no, line_text.strip()))
        
    # Check admit as tactic
    # Match admit not preceded by . or | or constructor syntax
    for m in re.finditer(r'(?:^|[^\w\.\|])(admit)(?:[^\w]|$)', clean):
        line_no = raw[:m.start()].count('\n') + 1
        raw_lines = raw.splitlines()
        line_text = raw_lines[line_no - 1] if line_no <= len(raw_lines) else ''
        admit_hits.append((f, line_no, line_text.strip()))
        
    # Check axiom
    for m in re.finditer(r'^\s*axiom\s+([A-Za-z0-9_]+)', clean, re.MULTILINE):
        line_no = raw[:m.start()].count('\n') + 1
        raw_lines = raw.splitlines()
        line_text = raw_lines[line_no - 1] if line_no <= len(raw_lines) else ''
        axiom_hits.append((f, line_no, m.group(1), line_text.strip()))

print(f"Audited {len(files)} files.")
print(f"Active sorry occurrences: {len(sorry_hits)}")
for h in sorry_hits:
    print("  SORRY:", h)
print(f"Admit occurrences: {len(admit_hits)}")
for h in admit_hits:
    print("  ADMIT:", h)
print(f"Axiom declarations: {len(axiom_hits)}")
for h in axiom_hits:
    print("  AXIOM:", h)
