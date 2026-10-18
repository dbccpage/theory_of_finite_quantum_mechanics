"""Exact system for M(S) at x=(-8-15i)/17, y=(56-33i)/65, u=(3+4i)/5 (all Gaussian rational).
v and w=1/(uv) are the other two unit roots of t^3 - d t^2 + conj(d) t - 1, d=-phi(x,y);
they satisfy w^2+(u-d)w+(u^2-du+conj d)=0. Unknown w=aw+i*bw; uv = conj(w)."""
import sympy as sp, sys
from gen import a,b,I,mu_eqs,write,aw,bw
x=sp.Rational(-8,17)-sp.Rational(15,17)*I; y=sp.Rational(56,65)-sp.Rational(33,65)*I; u=sp.Rational(3,5)+sp.Rational(4,5)*I
d=sp.expand(-(x+y+sp.conjugate(x*y)))
assert sp.expand(u**3-d*u**2+sp.conjugate(d)*u-1)==0
w=aw+I*bw
q=sp.expand(w**2+(u-d)*w+(u**2-d*u+sp.conjugate(d)))
param=[aw**2+bw**2-1, sp.expand(sp.re(q)), sp.expand(sp.im(q))]
uv=aw-I*bw
A=[[ [1,x,x*y][(j-i)%3] for j in range(3)] for i in range(3)]
B=[[ [1,u,uv][(j-i)%3] for j in range(3)] for i in range(3)]
H=[[0]*6 for _ in range(6)]
for i in range(3):
    for j in range(3):
        H[i][j]=A[i][j]; H[i][j+3]=B[i][j]
        H[i+3][j]=sp.conjugate(B[j][i]); H[i+3][j+3]=-sp.conjugate(A[j][i])
write(sys.argv[1], mu_eqs(H)+param, list(a)+list(b)+[aw,bw])
print("d =",d)
