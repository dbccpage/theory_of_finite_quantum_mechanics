"""Exact channel control fixtures; no general theorem or physical axiom is certified."""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,json
H=Path(__file__).resolve().parents[2]/'20261020T014538Z_born_11_to_20/verification/exact_controls.py'
s=importlib.util.spec_from_file_location('gaussian_controls',H);h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
need,z,add,neg,mul,conj,M,adj,mm,sumz,plus,scale,tr,real=[getattr(h,n) for n in ['need','z','add','neg','mul','conj','M','adj','mm','sumz','plus','scale','tr','real']]
def E(e,d,i,j):return M([[int(a==i and b==j) for b in range(d)] for a in range(e)])
def I(n):return M([[int(a==b) for b in range(n)] for a in range(n)])
def sm(mats):
 need(bool(mats),'nonempty finite fixture family');out=scale(0,mats[0])
 for a in mats:out=plus(out,a)
 return out
def phi(ks,x):return sm([mm(mm(k,x),adj(k)) for k in ks])
def norm(ks):return sm([mm(adj(k),k) for k in ks])
def kernel(ks):
 e=len(ks[0]);d=len(ks[0][0]);columns=[phi(ks,E(d,d,j,j)) for j in range(d)]
 return [[real(columns[j][a][a]) for j in range(d)] for a in range(e)]
def plainmm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def diag(a):return [[v if i==j else z(0) for j,v in enumerate(row)] for i,row in enumerate(a)]
def choi(ks):
 e=len(ks[0]);d=len(ks[0][0]);vs=[[[k[a][j]] for j in range(d) for a in range(e)] for k in ks]
 return sm([mm(v,adj(v)) for v in vs])
def tr_output(c,d,e):return [[sumz(c[j*e+a][k*e+a] for a in range(e)) for k in range(d)] for j in range(d)]
def tr_env(x,e,r):return [[sumz(x[a*r+t][b*r+t] for t in range(r)) for b in range(e)] for a in range(e)]
def invert(c):
 q=c[0]*c[0]+c[1]*c[1];need(q!=0,'nonzero Gaussian denominator');return (c[0]/q,-c[1]/q)
def update(v):
 n=len(v);eye=I(n);e1=[[z(int(j==0))] for j in range(n)]
 if v==e1:return eye
 w=plus(e1,scale(-1,v));c=add(z(1),neg(conj(v[0][0])))
 return plus(eye,scale(mul(z(-1),invert(c)),mm(w,adj(w))))
def strings(x):
 if isinstance(x,list):return [strings(a) for a in x]
 return str(x)
def main():
 U=scale(F(1,5),M([[3,-4],[4,3]]));UH=adj(U);need(mm(UH,U)==I(2),'unitary fixture')
 cp_trace=real(tr(phi([I(2),I(2)],E(2,2,0,0))));zero_trace=real(tr(phi([scale(0,I(2))],E(2,2,0,0))))
 need(cp_trace==2 and zero_trace==0,'CP is not normalized')
 swap=M([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]]);psi=M([[0],[1],[-1],[0]])
 witness=real(mm(mm(adj(psi),swap),psi)[0][0]);need(witness==-2,'transpose witness')
 normalized=witness/2;need(normalized==-1,'normalized transpose witness')
 su=kernel([U]);sd=kernel([UH]);product=plainmm(sd,su);actual=kernel([mm(UH,U)])
 expected=[[F(337,625),F(288,625)],[F(288,625),F(337,625)]]
 need(product==expected and actual==[[1,0],[0,1]] and actual!=product,'kernel multiplication failure')
 prep=[scale(F(1,5),M([[3,0],[4,0]])),scale(F(1,5),M([[0,3],[0,4]]))]
 need(norm(prep)==I(2),'preparation normalization');comp=[mm(k,U) for k in prep]
 for a in range(2):
  for b in range(2):need(phi(comp,E(2,2,a,b))==phi(prep,E(2,2,a,b)),'preparation composite basis')
 success=kernel(comp)==plainmm(kernel(prep),su);need(success,'kernel multiplicativity without covariance')
 for ks in [prep,[U]]:
  image=phi(ks,E(2,2,0,0));need(diag(image)!=image,'both fixtures fail dephasing covariance')
 rect=[]
 for out,inp,coeff in [(0,0,F(1,2)),(1,0,F(1,2)),(2,0,F(1,2)),(2,0,F(1,2)),(1,1,F(3,5)),(2,1,F(4,5))]:rect.append(scale(coeff,E(3,2,out,inp)))
 sr=[[F(1,4),0],[F(1,4),F(9,25)],[F(1,2),F(16,25)]]
 need(norm(rect)==I(2) and kernel(rect)==sr,'rectangular classical lift')
 need(tr_output(choi(rect),2,3)==I(2),'rectangular Choi TP')
 complexk=M([[1,(0,1)],[0,0]]);m=norm([complexk]);mt=[[m[j][i] for j in range(2)] for i in range(2)]
 need(tr_output(choi([complexk]),2,2)==mt and mt!=m,'Choi partial trace transpose')
 deph=[E(2,2,0,0),E(2,2,1,1)];need(phi(deph,E(2,2,0,1))!=E(2,2,0,1),'classical identity lift dephases')
 ks=[scale(F(3,5),U),scale(F(4,5),U)];r=len(ks);v=[[ks[a][out][j] for j in range(2)] for out in range(2) for a in range(r)]
 need(mm(adj(v),v)==I(2),'Stinespring fixture isometry')
 for a in range(2):
  for b in range(2):
   x=E(2,2,a,b);need(tr_env(mm(mm(v,x),adj(v)),2,r)==phi(ks,x),'Stinespring fixture partial trace')
 tested=[]
 for v in [M([[1],[0]]),M([[(F(1,2),F(1,2))],[(F(1,2),F(1,2))]]),M([[(0,1)],[0]])]:
  need(real(mm(adj(v),v)[0][0])==1,'unit vector fixture');u=update(v)
  need(mm(adj(u),u)==I(2) and mm(u,E(2,1,0,0))==v,'rational unitary rank-one update');tested.append(True)
 return {'scope':'Exact finite matrix controls only; general theorems and physical assumptions are separate.','CP_not_TP':{'two_identity_kraus_output_trace':str(cp_trace),'zero_map_output_trace':str(zero_trace)},'transpose_witness':{'unnormalized':str(witness),'normalized_state':str(normalized)},'kernel_composition_failure':{'actual':strings(actual),'product':strings(product)},'kernel_composition_success_without_either_map_dephasing_covariant':success,'rectangular_lift':{'kraus_shape':'3x2','kraus_count':len(rect),'kernel':strings(sr),'normalization':True},'choi_partial_trace_is_transposed_kraus_sum':True,'classical_identity_lift_is_dephasing':True,'stinespring_two_kraus_fixture_basis_checks':4,'rational_unitary_update_fixtures_passed':len(tested),'same_identity_channel_presentations':{'first_kraus_count':1,'second_kraus_count':2,'index_bijection_possible':False}}
if __name__=='__main__':print(json.dumps(main(),indent=2))
