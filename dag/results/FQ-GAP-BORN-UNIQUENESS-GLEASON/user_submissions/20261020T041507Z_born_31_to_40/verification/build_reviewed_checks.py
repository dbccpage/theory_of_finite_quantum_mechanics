"""Build a reviewed derivative; never mutate the submitted script."""
from pathlib import Path
import ast,json,hashlib
out=Path(__file__).resolve().parents[1]
src=out/'submission/br31_40_checks.py'
tree=ast.parse(src.read_text(encoding='utf-8-sig'))
helpers=ast.parse('''
from math import isqrt
from sympy import S as exact_S

def require(condition, message="expected an exact true Boolean"):
    if condition is not True and condition is not exact_S.true:
        raise ValueError(message)

def gaussian_rational(x):
    x=sympify(x)
    if not isinstance(x, Expr):
        return False
    return not x.has(Float) and simplify(re(x)).is_Rational is True and simplify(im(x)).is_Rational is True

def admit_matrix(value, square=False, hermitian=False):
    matrix=Matrix(value)
    require(all(gaussian_rational(x) for x in matrix), "entries must be exact Gaussian rationals")
    if square:
        require(matrix.rows==matrix.cols, "square matrix required")
    if hermitian:
        require(matrix==matrix.H, "Hermitian matrix required")
    return matrix
''').body
newcheck=ast.parse('''
def check(name, cond):
    global ok
    require(cond, "failed exact check: "+name)
    ok=True
    print("PASS "+name)
''').body[0]
newfour=ast.parse('''
def four_squares(n):
    require(sympify(n).is_Integer is True and n>=0, "nonnegative integer required")
    r=isqrt(int(n))
    for a,b,c,dd in product(range(r+1),repeat=4):
        if a*a+b*b+c*c+dd*dd==n:
            return [x for x in (a,b,c,dd) if x]
    raise RuntimeError("four-square search exhausted its exact bound")
''').body[0]
class Repair(ast.NodeTransformer):
    def visit_Assert(self,node):
        self.generic_visit(node)
        return ast.copy_location(ast.Expr(value=ast.Call(func=ast.Name(id='require',ctx=ast.Load()),args=[node.test,node.msg or ast.Constant(value='assertion obligation failed')],keywords=[])),node)
    def visit_BoolOp(self,node):
        self.generic_visit(node)
        if isinstance(node.op,ast.Or) and len(node.values)==2:
            a,b=node.values
            if isinstance(a,ast.Attribute) and isinstance(b,ast.Attribute) and a.attr=='is_rational' and b.attr=='is_Number' and ast.dump(a.value)==ast.dump(b.value):
                return ast.copy_location(ast.Call(func=ast.Name(id='gaussian_rational',ctx=ast.Load()),args=[a.value],keywords=[]),node)
        return node
    def visit_FunctionDef(self,node):
        if node.name=='check':return newcheck
        if node.name=='four_squares':return newfour
        node=self.generic_visit(node)
        if node.name=='psd_certify':
            node.body.insert(1,ast.parse('A=admit_matrix(A,square=True,hermitian=True)').body[0])
        if node.name=='match_unitary':
            node.body[1:1]=ast.parse('A=admit_matrix(A)\nB=admit_matrix(B)\nrequire(A.rows==B.rows,"matching row dimensions required")').body
        if node.name=='rational_roots_of_weight':
            node.body.insert(0,ast.parse('require(sympify(w).is_Rational is True and w>=0,"nonnegative rational weight required")').body[0])
        return node
    def visit_Call(self,node):
        node=self.generic_visit(node)
        if isinstance(node.func,ast.Name) and node.func.id=='check' and node.args and isinstance(node.args[0],ast.Constant) and isinstance(node.args[0].value,str) and node.args[0].value.startswith('BR-38 1/3 is not a single norm'):
            node.args[0]=ast.Constant(value='BR-38 integer control only: 3 is not a sum of two integer squares; rational non-norm uses the written descent proof')
        return node
    def visit_Assign(self,node):
        node=self.generic_visit(node)
        if any(isinstance(t,ast.Name) and t.id=='vecm' for t in node.targets):
            return ast.parse('vecm=lambda K: Matrix([K[a,j] for j in range(K.cols) for a in range(K.rows)])').body[0]
        return node
tree=Repair().visit(tree)
# Helper functions run only after SymPy has been imported, before the first submitted function.
first_function=next(i for i,n in enumerate(tree.body) if isinstance(n,ast.FunctionDef))
tree.body[first_function:first_function]=helpers
ast.fix_missing_locations(tree)
reviewed=out/'verification/br31_40_checks_reviewed.py'
reviewed.write_text(ast.unparse(tree)+'\n',encoding='utf-8')
report={'source':'submission/br31_40_checks.py','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'derived':'verification/br31_40_checks_reviewed.py','derived_sha256':hashlib.sha256(reviewed.read_bytes()).hexdigest(),'changes':['Replace assertion-only obligations with explicit exact Boolean guards','Make failed checks raise and exit nonzero','Admit all matrix entries as Gaussian rational; enforce PSD Hermiticity/square domain and matching row domains','Replace floating square-root search bound by integer isqrt','Replace is_Number carrier shortcuts by Gaussian-rational membership','Correct input-first vectorization to K[a,j] instead of K[j,a]'],'mathematical_ceiling':'Same 86 submitted fixtures; independent new obligations are in independent_checks.py.'}
(out/'verification/script_repairs.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('Reviewed derivative built.')
