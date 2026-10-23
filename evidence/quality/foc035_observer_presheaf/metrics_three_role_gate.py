import ast, json, sys
from pathlib import Path
import lizard
from radon.complexity import cc_visit

W = Path(__file__).resolve().parents[3]
out = {}
CONTROL = (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.IfExp, ast.comprehension, ast.ExceptHandler, ast.Match)


def depth_and_cog(fn):
    best = 0
    cog = 0

    def visit(node, depth):
        nonlocal best, cog
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
                continue
            if isinstance(child, CONTROL):
                cog += 1 + depth
                best = max(best, depth + 1)
                visit(child, depth + 1)
            else:
                if isinstance(child, ast.BoolOp):
                    cog += 1
                visit(child, depth)

    visit(fn, 0)
    return best, cog


for rel in ('code/python/src/wdp/three_role_gate.py', 'code/python/tests/test_three_role_gate.py'):
    src = (W / rel).read_text(encoding='utf-8')
    tree = ast.parse(src)
    radon_max = max((b.complexity for b in cc_visit(src)), default=0)
    liz = lizard.analyze_file.analyze_source_code(rel, src)
    liz_max = max((f.cyclomatic_complexity for f in liz.function_list), default=0)
    nest = cog = 0
    worst = None
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            d, c = depth_and_cog(node)
            nest = max(nest, d)
            if c > cog:
                cog, worst = c, node.name
    out[rel] = {'radon_max_ccn': radon_max, 'lizard_max_ccn': liz_max, 'ast_max_control_nesting': nest,
                'ast_max_cognitive_approximation': cog, 'ast_cognitive_worst_function': worst,
                'functions': len(liz.function_list), 'nloc': liz.nloc}
print(json.dumps(out, indent=1))
print('radon', __import__('radon').__version__, 'lizard', lizard.version)
