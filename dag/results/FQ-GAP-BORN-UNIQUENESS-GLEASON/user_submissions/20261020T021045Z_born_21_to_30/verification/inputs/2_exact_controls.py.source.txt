"""Exact finite witnesses only; this does not certify any general theorem."""
from fractions import Fraction as F
import json

def need(v,m):
 if not v:raise ValueError(m)
def z(v):return tuple(map(F,v)) if isinstance(v,tuple) else (F(v),F(0))
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def neg(a):return (-a[0],-a[1])
def mul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def conj(a):return (a[0],-a[1])
def M(rows):return [[z(v) for v in row] for row in rows]
def adj(A):return [[conj(A[i][j]) for i in range(len(A))] for j in range(len(A[0]))]
def mm(A,B):
 need(len(A[0])==len(B),'matrix dimensions')
 return [[sumz(mul(A[i][k],B[k][j]) for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def sumz(xs):
 s=z(0)
 for x in xs:s=add(s,x)
 return s
def plus(A,B):return [[add(a,b) for a,b in zip(ar,br)] for ar,br in zip(A,B)]
def scale(c,A):return [[mul(z(c),a) for a in row] for row in A]
def tr(A):return sumz(A[i][i] for i in range(len(A)))
def real(a):
 need(a[1]==0,'expected real rational');return a[0]
def psd2(A):
 need(A==adj(A),'expected Hermitian')
 det=real(add(mul(A[0][0],A[1][1]),neg(mul(A[0][1],A[1][0]))))
 return real(A[0][0])>=0 and real(A[1][1])>=0 and det>=0,det

def main():
 I=M([[1,0],[0,1]]);A=M([[1,0],[0,0]]);B=scale(F(1,5),M([[4,-2],[-2,1]]))
 need(mm(A,A)==A and mm(B,B)==B,'projection replay')
 diff=plus(A,scale(-1,B));need(mm(diff,diff)==scale(F(1,5),I),'exact norm-squared witness')
 low=plus(scale(F(1,2),I),diff);high=plus(scale(F(1,2),I),scale(-1,diff))
 lo,ld=psd2(low);hi,hd=psd2(high);need(lo and hi and ld==hd==F(1,20),'sandwich PSD certificate')
 # A Hermitian, nonpositive affine representative fits all three axes.
 H=M([[1,(F(1,2),-F(1,2))],[(F(1,2),F(1,2)),0]])
 Px=scale(F(1,2),M([[1,1],[1,1]]));Py=scale(F(1,2),M([[1,(0,-1)],[(0,1),1]]))
 axes=[real(tr(mm(H,P))) for P in [A,Px,Py]];need(axes==[1,1,1],'three axes affine witness')
 fourth=M([[F(9,10),F(3,10)],[F(3,10),F(1,10)]])
 fv=real(tr(mm(H,fourth)));need(fv==F(6,5),'fourth-direction rejection')
 positive,hdet=psd2(H);need(not positive and hdet==F(-1,2),'nonpositive witness')
 # Range-normalized per-dilation trace valuations can still disagree.
 W=M([[1,0],[0,1],[0,0],[0,0]]);Q=M([[1,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
 sigma=M([[0,0,0,0],[0,1,0,0],[0,0,0,0],[0,0,0,0]])
 need(mm(adj(W),W)==I and mm(mm(adj(W),Q),W)==A,'isometry/compression')
 support=real(tr(mm(sigma,mm(W,adj(W)))));second=real(tr(mm(sigma,Q)))
 need(support==1 and second==0 and real(tr(mm(A,A)))==1,'range-normalized consistency counterexample')
 # Forgetting outcome slots before fixed-slot substitution is invalid.
 k=[F(3,5),F(4,5)];kp=k[::-1];l=k[:]
 out=[k[0]*l[0],k[0]*l[1],k[1]];outp=[kp[0]*l[0],kp[0]*l[1],kp[1]]
 need(sum(x*x for x in k)==sum(x*x for x in kp)==1,'outer normalization')
 need(sum(x*x for x in out)==sum(x*x for x in outp)==1,'composite normalization')
 need(sorted(k)==sorted(kp) and sorted(out)!=sorted(outp),'slot quotient counterexample')
 return {'scope':'Exact finite controls only; general proof and Lean acceptance are separate.','sandwich':{'projections':True,'difference_squared':'(1/5)I','lower_determinant':str(ld),'upper_determinant':str(hd)},'three_axis_affine_counterexample':{'axis_values':list(map(str,axes)),'determinant':str(hdet),'fourth_value':str(fv)},'range_normalized_consistency_counterexample':{'same_compression':True,'first_value':'1','second_value':str(second),'range_probability':str(support)},'fixed_slot_quotient_counterexample':{'outer_multisets_equal':True,'first_composite':list(map(str,out)),'second_composite':list(map(str,outp)),'composite_multisets_equal':False,'both_normalized':True}}
if __name__=='__main__':print(json.dumps(main(),indent=2))
