"""Exact finite Born/operad correction fixtures; no general proof certification."""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,json
P=Path(__file__).resolve().parents[2]/'20261020T015433Z_channel_class_21_to_25/verification/channel_controls.py'
s=importlib.util.spec_from_file_location('channel_fixture_helper',P);c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
need,M,I,E,adj,mm,scale,plus,tr,real,phi,norm,choi,z=[getattr(c,n) for n in ['need','M','I','E','adj','mm','scale','plus','tr','real','phi','norm','choi','z']]
def shape(a):return (len(a),len(a[0]))
def strict_sum(mats):
 need(bool(mats),'nonempty sum fixture');s=scale(0,mats[0]);dimensions=shape(s)
 for a in mats:
  need(shape(a)==dimensions,'heterogeneous output colors cannot be matrix-summed');s=plus(s,a)
 return s
def direct_sum(mats):
 n=sum(len(a) for a in mats);out=M([[0]*n for _ in range(n)]);offset=0
 for a in mats:
  need(len(a)==len(a[0]),'square state blocks')
  for j,row in enumerate(a):
   for k,v in enumerate(row):out[offset+j][offset+k]=v
  offset+=len(a)
 return out
def transpose(a):return [[a[j][i] for j in range(len(a))] for i in range(len(a[0]))]
def psd2(a):return c.h.psd2(a)[0]
def main():
 eye=I(2);S=M([[0,1],[1,0]]);T=M([[0,(0,1)],[(0,-1),0]])
 G=scale(F(1,2),plus(eye,S));H=scale(F(1,2),plus(eye,T));D=E(2,2,0,0)
 for a in [D,G,H]:need(psd2(a) and psd2(plus(eye,scale(-1,a))),'probe effect fixture')
 # Scalar-output convention is a transpose, not an identity.
 row=M([[(F(1,2),-F(1,2)),(F(1,2),F(1,2))]])
 effect=norm([row]);C=choi([row]);need(effect==H and C==transpose(effect) and C!=effect,'POVM Choi transpose witness')
 value=phi([row],E(2,2,0,1))[0][0];need(value==C[0][1] and value==z((0,-F(1,2))),'basis readout orientation')
 # The d=2 informationally complete measurement reconstructs a complex rational state.
 probes=[D,G,H];mi=[scale(F(1,3),a) for a in probes];m0=plus(eye,scale(-1,strict_sum(mi)));povm=[m0,*mi]
 need(strict_sum(povm)==eye and all(psd2(a) for a in povm),'IC POVM normalization/positivity')
 need(psd2(plus(m0,scale(-F(1,12),eye))),'strict remainder bound fixture')
 q=[real(tr(mm(H,a))) for a in povm];need(sum(q)==1,'IC probabilities')
 x=3*q[1];re=3*q[2]-F(1,2);im=3*q[3]-F(1,2);reconstructed=M([[x,(re,im)],[(re,-im),1-x]])
 need(reconstructed==H,'IC reconstruction fixture')
 smaller=scale(F(1,4),plus(eye,S));need(psd2(smaller) and psd2(plus(eye,scale(-1,smaller))),'smaller affine shift witness')
 need(not psd2(plus(eye,scale(-2,eye))),'sum of effects need not be an effect')
 # Pairwise principal tests are not full PSD admission.
 bad=scale(F(1,3),M([[1,-1,-1],[-1,1,-1],[-1,-1,1]]));need(real(tr(bad))==1,'bad data trace')
 for j in range(3):
  for k in range(j+1,3):
   pair=[[bad[j][j],bad[j][k]],[bad[k][j],bad[k][k]]];positive,det=c.h.psd2(pair);need(positive and det==0,'pairwise minor control')
 v=M([[1],[1],[1]]);negative=real(mm(mm(adj(v),bad),v)[0][0]);need(negative==-1,'negative quadratic witness')
 # Distinct continuation maps can coincide on the reached branch ranges.
 k1=D;k2=E(2,2,1,1);Z=M([[-1,0],[0,1]])
 need(norm([k1,k2])==eye and norm([Z])==eye,'merge fixtures normalized')
 need(phi([Z],E(2,2,0,1))!=phi([eye],E(2,2,0,1)),'continuations genuinely differ as CP maps')
 after=[mm(eye,k1),mm(Z,k2)];before=[mm(eye,k1),mm(eye,k2)];need(after==before,'different-continuation common merge-first witness')
 # Heterogeneous branch states have scalar marginals but no untagged matrix sum.
 l1=M([[F(3,5)]]);l2=M([[F(4,5)],[0]]);need(norm([l1,l2])==I(1),'heterogeneous continuation normalization')
 states=[phi([l1],I(1)),phi([l2],I(1))];rejected=False
 try:strict_sum(states)
 except ValueError:rejected=True
 need(rejected,'heterogeneous state sum must be rejected');probs=[real(tr(a)) for a in states];need(sum(probs)==1,'scalar marginal')
 tagged=direct_sum(states);need(shape(tagged)==(3,3) and real(tr(tagged))==1,'tagged direct sum')
 return {'scope':'Exact finite fixtures only; general written results and Lean certification are separate.','choi_scalar_output':{'effect_upper_entry':['0','1/2'],'choi_upper_entry':[str(value[0]),str(value[1])],'transpose_required':C==transpose(effect)},'IC_d2':{'probabilities':list(map(str,q)),'reconstructed_state_matches':reconstructed==H,'remainder_lower_bound':'I/12'},'pairwise_checks_insufficient':{'trace':'1','pairwise_minors':'0','negative_quadratic_value':str(negative)},'different_continuations_can_merge_first':after==before,'heterogeneous_states':{'shapes':[list(shape(a)) for a in states],'untagged_matrix_sum_rejected':rejected,'probabilities':list(map(str,probs)),'tagged_shape':list(shape(tagged))},'smaller_affine_probe_shift_is_valid':True,'partial_effect_sum_domain_guard':True}
if __name__=='__main__':print(json.dumps(main(),indent=2))
