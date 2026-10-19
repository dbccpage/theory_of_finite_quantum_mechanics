"""Direct-index scalar sums, exact 2x2 positivity and explicit admission scope."""
from fractions import Fraction as Q
from pathlib import Path
import sys
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'dag/pfp/prepare_stage.py').is_file());sys.path.insert(0,str(ROOT/'dag/pfp'))
from exact_json import bound,require,vector,rational
TASK='FQ-DECLARED-QUANTUM-INTERFACE'
SLOTS={'scalar_field','inner_product','positive_states_and_effects','Born_trace','tensor','channels','unitary_step_and_time','observer_records'}
def mat(a,n):
    require(type(a) is list and len(a)==n,'G1_SCHEMA:matrix_shape');return [vector(r,n) for r in a]
def positive2(a):return a[0][1]==a[1][0] and a[0][0]>=0 and a[1][1]>=0 and a[0][0]*a[1][1]-a[0][1]*a[1][0]>=0
def check(request,candidate):
    _,cert,p=bound(request,candidate,TASK);data=cert['data']
    require(type(data) is dict and set(data)=={'cases'} and type(data['cases']) is list and len(data['cases'])==len(p['cases']),'G1_SCHEMA:cases')
    require(set(p['admissions'])==SLOTS and all(type(v) is str and v.startswith('ADMITTED: ') for v in p['admissions'].values()),'G5_SCOPE:admission_inputs')
    for c,a in zip(p['cases'],data['cases']):
        require(type(a) is dict and set(a)=={'id','admissions','matrices','scalars','derivation_status'} and a['id']==c['id'],'G1_SCHEMA:case')
        require(a['admissions']==p['admissions'] and a['derivation_status']=='ADMITTED_INTERFACE_EXERCISED_ONLY','G5_SCOPE:admission_promoted')
        rho,e,u=[mat(c[k],2) for k in ('rho','effect','unitary')];ks=[mat(k,2) for k in c['kraus']]
        eye=[[Q(int(i==j)) for j in range(2)] for i in range(2)]
        require(positive2(rho) and rho[0][0]+rho[1][1]==1 and positive2(e) and positive2([[eye[i][j]-e[i][j] for j in range(2)] for i in range(2)]),'G3_WITNESS:state_effect')
        completeness=[[sum(k[r][i]*k[r][j] for k in ks for r in range(2)) for j in range(2)] for i in range(2)]
        utu=[[sum(u[r][i]*u[r][j] for r in range(2)) for j in range(2)] for i in range(2)]
        require(completeness==utu==eye,'G3_WITNESS:channel_unitary_hypotheses')
        channel=[[sum(k[i][r]*rho[r][s]*k[j][s] for k in ks for r in range(2) for s in range(2)) for j in range(2)] for i in range(2)]
        evolved=[[sum(u[i][r]*rho[r][s]*u[j][s] for r in range(2) for s in range(2)) for j in range(2)] for i in range(2)]
        tensor=[[rho[i//2][j//2]*rho[i%2][j%2] for j in range(4)] for i in range(4)]
        matrices={'density':rho,'effect':e,'kraus_completeness':completeness,'channel_density':channel,'unitary_star_unitary':utu,'evolved_density':evolved,'tensor_density':tensor}
        require(type(a['matrices']) is dict and set(a['matrices'])==set(matrices),'G1_SCHEMA:matrix_fields')
        for k,v in matrices.items():require(mat(a['matrices'][k],len(v))==v,'G3_WITNESS:actual_matrix:'+k)
        scalars={'Born_weight':sum(rho[i][j]*e[j][i] for i in range(2) for j in range(2)),'unit_weight':sum(rho[i][i] for i in range(2)),'channel_trace':sum(channel[i][i] for i in range(2)),'evolved_trace':sum(evolved[i][i] for i in range(2)),'tensor_trace':sum(tensor[i][i] for i in range(4)),'channel_Born_weight':sum(channel[i][j]*e[j][i] for i in range(2) for j in range(2))}
        require(type(a['scalars']) is dict and set(a['scalars'])==set(scalars),'G1_SCHEMA:scalar_fields')
        for k,v in scalars.items():require(rational(a['scalars'][k])==v,'G3_WITNESS:actual_pairing:'+k)
    return {'admitted_slots':8,'cases':len(data['cases']),'scope':'Exact real-rational subcase of supplied complex interface; neither necessity nor derivation of the quantum assumptions.'}
if __name__=='__main__':
    import json
    print(json.dumps(check(*sys.argv[1:]),indent=2))
