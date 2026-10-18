"""Write the msolve input for M(H): unit vectors v (v_0=1) unbiased to the columns of H.
Real coordinates v_j = a_j + i b_j (j=1..5). Entries of H may contain the complex unknowns
U=(au+i bu), W=(aw+i bw) (unit roots of a cubic) when a point of D needs them."""
import sympy as sp, sys
a=sp.symbols('a1:6',real=True); b=sp.symbols('b1:6',real=True)
au,bu,aw,bw=sp.symbols('au bu aw bw',real=True)
I=sp.I
def circ3(r): return [[r[(j-i)%3] for j in range(3)] for i in range(3)]
def szollosi(x,y,u,v):
    A=circ3([1,x,x*y]); B=circ3([1,u,u*v])
    H=[[0]*6 for _ in range(6)]
    for i in range(3):
        for j in range(3):
            H[i][j]=A[i][j]; H[i][j+3]=B[i][j]
            H[i+3][j]=sp.conjugate(B[j][i]); H[i+3][j+3]=-sp.conjugate(A[j][i])
    return H
def mu_eqs(H, ncols=5):
    v=[sp.Integer(1)]+[a[j]+I*b[j] for j in range(5)]
    eqs=[]
    for k in range(ncols):
        L=sum(sp.conjugate(H[j][k])*v[j] for j in range(6))
        e=sp.expand(L*sp.conjugate(L))-6
        e=sp.expand(e)
        assert sp.im(e)==0 or sp.simplify(sp.im(e))==0
        eqs.append(sp.expand(sp.re(e)))
    eqs+= [a[j]**2+b[j]**2-1 for j in range(5)]
    return eqs
def write(path, eqs, varlist):
    with open(path,'w') as f:
        f.write(",".join(str(v) for v in varlist)+"\n0\n")
        eqs=[sp.expand(sp.fraction(sp.together(e))[0]) for e in eqs]
        f.write(",\n".join(str(e).replace('**','^') for e in eqs)+"\n")
if __name__=="__main__":
    H=szollosi(sp.Integer(1),sp.Integer(-1),sp.Integer(1),I)
    write(sys.argv[1], mu_eqs(H), list(a)+list(b))
