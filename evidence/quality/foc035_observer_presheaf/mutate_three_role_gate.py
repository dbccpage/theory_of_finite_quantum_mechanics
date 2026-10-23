"""Small AST mutation campaign for three_role_gate.py against test_three_role_gate.py.

Each mutant is written over the module, the test file is run, and the original is restored.
Outcomes follow SCORING.md section 3.4: killed, survived, invalid, inconclusive. A survivor is
reported with its location so that equivalence can be judged by hand; nothing is auto-excluded.
"""
import ast
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

W = Path(__file__).resolve().parents[3]
TARGET = W / 'code/python/src/wdp/three_role_gate.py'
TESTS = sys.argv[1:] or ['code/python/tests/test_three_role_gate.py']
ORIGINAL = TARGET.read_bytes()
TREE = ast.parse(ORIGINAL.decode('utf-8'))

SWAP_CMP = {ast.Eq: ast.NotEq, ast.NotEq: ast.Eq, ast.Is: ast.IsNot, ast.IsNot: ast.Is, ast.In: ast.NotIn, ast.NotIn: ast.In}


def sites(tree):
    """Yield (kind, node-index) for each mutation site in a stable walk order."""
    out = []
    for i, node in enumerate(ast.walk(tree)):
        if isinstance(node, ast.Compare):
            for j, op in enumerate(node.ops):
                if type(op) in SWAP_CMP:
                    out.append(('cmp', i, j))
        elif isinstance(node, ast.BoolOp):
            out.append(('boolop', i, 0))
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            out.append(('not', i, 0))
        elif isinstance(node, ast.Constant) and isinstance(node.value, bool):
            out.append(('bool', i, 0))
        elif isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value and not (
                isinstance(getattr(node, 'parent_is_doc', None), bool)):
            out.append(('str', i, 0))
        elif isinstance(node, ast.Raise):
            out.append(('raise', i, 0))
        elif isinstance(node, ast.If):
            out.append(('if_true', i, 0))
            out.append(('if_false', i, 0))
        elif isinstance(node, ast.Return) and node.value is not None:
            out.append(('return_none', i, 0))
    return out


def apply(kind, idx, sub):
    tree = copy.deepcopy(TREE)
    nodes = list(ast.walk(tree))
    node = nodes[idx]
    parents = {}
    for p in nodes:
        for field, value in ast.iter_fields(p):
            if isinstance(value, list):
                for k, c in enumerate(value):
                    if isinstance(c, ast.AST):
                        parents[id(c)] = (p, field, k)
            elif isinstance(value, ast.AST):
                parents[id(value)] = (p, field, None)

    def replace(old, new):
        p, field, k = parents[id(old)]
        if k is None:
            setattr(p, field, new)
        else:
            getattr(p, field)[k] = new

    if kind == 'cmp':
        node.ops[sub] = SWAP_CMP[type(node.ops[sub])]()
    elif kind == 'boolop':
        node.op = ast.Or() if isinstance(node.op, ast.And) else ast.And()
    elif kind == 'not':
        replace(node, node.operand)
    elif kind == 'bool':
        node.value = not node.value
    elif kind == 'str':
        node.value = node.value + 'X'
    elif kind == 'raise':
        replace(node, ast.Pass())
    elif kind == 'if_true':
        node.test = ast.Constant(True)
    elif kind == 'if_false':
        node.test = ast.Constant(False)
    elif kind == 'return_none':
        node.value = ast.Constant(None)
    ast.fix_missing_locations(tree)
    return ast.unparse(tree)


def run_tests():
    cmd = [sys.executable, '-I', '-X', 'utf8', '-m', 'pytest', *TESTS, '-x', '-q', '-p', 'no:cacheprovider']
    try:
        p = subprocess.run(cmd, cwd=W, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return 'inconclusive', 'timeout'
    return p.returncode, p.stdout[-300:]


def main():
    base = run_tests()
    assert base[0] == 0, base
    results = []
    all_sites = sites(TREE)
    # Skip string constants that are docstrings or f-string pieces: keep only strings in code positions.
    doc_ids = set()
    for node in ast.walk(TREE):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)) and node.body and isinstance(node.body[0], ast.Expr) \
                and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
            doc_ids.add(id(node.body[0].value))
    nodes = list(ast.walk(TREE))
    try:
        for n, (kind, idx, sub) in enumerate(all_sites):
            node = nodes[idx]
            if kind == 'str' and id(node) in doc_ids:
                continue
            line = getattr(node, 'lineno', None)
            try:
                text = apply(kind, idx, sub)
                compile(text, 'mutant', 'exec')
            except Exception as e:  # noqa: BLE001
                results.append({'kind': kind, 'line': line, 'outcome': 'invalid', 'detail': str(e)[:80]})
                continue
            if text == ast.unparse(TREE):
                results.append({'kind': kind, 'line': line, 'outcome': 'equivalent_by_construction', 'detail': 'unparse identical'})
                continue
            TARGET.write_bytes(text.encode('utf-8'))
            code, tail = run_tests()
            if code == 'inconclusive':
                outcome = 'inconclusive'
            elif code == 0:
                outcome = 'survived'
            elif code == 1:
                outcome = 'killed'
            else:
                outcome = 'invalid'
            results.append({'kind': kind, 'line': line, 'outcome': outcome, 'detail': ''})
            print(n, kind, line, outcome, flush=True)
    finally:
        TARGET.write_bytes(ORIGINAL)
    assert hashlib.sha256(TARGET.read_bytes()).hexdigest() == hashlib.sha256(ORIGINAL).hexdigest()
    counts = {}
    for r in results:
        counts[r['outcome']] = counts.get(r['outcome'], 0) + 1
    print(json.dumps(counts))
    (Path(__file__).with_name('mutation_results.json')).write_text(json.dumps({'counts': counts, 'results': results}, indent=1) + '\n', encoding='utf-8', newline='\n')


main()
