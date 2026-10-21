"""Record this run on the DAG nodes L1-IMP-HILBERT-INNER-PRODUCT and L1-IMP-ORTHOGONAL-ADDITIVITY and add the two conditional routes; bytes are written with LF line endings."""
from pathlib import Path
import json
B=Path(__file__).resolve().parents[1]
ROOT=next(p for p in B.parents if (p/'lean4/lakefile.lean').is_file())
DAG=ROOT/'dag/derivation_dag.json'
RUN='dag/results/L1-IMP-HILBERT-INNER-PRODUCT/runs/20261021T013500Z_sector_form'
R='lean4/SectorFormUniqueness.lean::InnerProductFable.SectorForm.'
H='lean4/SectorFormHermitian.lean::InnerProductFable.HermitianSectorForm.'
def add(lst,items):
    for x in items:
        if x not in lst:lst.append(x)
def main():
    raw=DAG.read_bytes();assert b'\r\n' not in raw,'DAG is expected to use LF line endings'
    d=json.loads(raw.decode('utf-8'));nodes={n['id']:n for n in d['nodes']};routes={r['id']:r for r in d['routes']}
    ip=nodes['L1-IMP-HILBERT-INNER-PRODUCT'];oa=nodes['L1-IMP-ORTHOGONAL-ADDITIVITY']
    assert ip['status']=='IMPORTED_ASSUMPTION' and oa['status']=='IMPORTED_ASSUMPTION','already updated'
    ip['status']='CONDITIONAL'
    ip['source_status']=('Sector-form selection kernel-checked in '+RUN+': a symmetric (Hermitian) Gram form whose readout is additive on disjoint sector supports and invariant under a set of sector permutations generating a transitive group equals G i0 i0 * 1 (SectorFormUniqueness.eq_smul_one, eq_smul_one_generated; SectorFormHermitian.eq_smul_one over Q(i)); the scale is positive for a positive-definite readout (scale_pos), two such forms are proportional (unique_up_to_scale), and the unit-normalised form is the standard form qf 1 / hf 1 of the Born carriers (eq_one_of_normalized). Countermodels diag(1,2) (the H005 form; sector additive, not swap invariant) and 1+(all ones) (swap invariant, not sector additive) show each law is used. Exact replays: code/python/src/qm/inner_product_uniqueness.py, code/rust/src/qm/inner_product_uniqueness.rs. Earlier: '+ip['source_status'])
    ip['statement']=ip['statement']+' The form is selected up to a unit scale by two laws on the quadratic readout: sector additivity on disjoint supports and invariance under a transitive group of sector permutations ('+RUN+').'
    ip['bottleneck']='Sector additivity of the quadratic readout (transcribed from edgewise l1 additivity) and transitive sector symmetry are supplied as laws of the readout, not derived from primitives; the sector carrier, the scalar field and the quadratic shape of the readout remain imports. The H005 non-uniqueness is exactly the failure of the symmetry law (diag12_not_invariant_swap); without transitivity the diagonal is constant only on orbits.'
    add(ip['lean'],[R+n for n in ['eq_smul_one','eq_smul_one_generated','qf_eq_scale_dot','scale_pos','unique_up_to_scale','eq_one_of_normalized','diag12_not_invariant_swap','unif12_not_sectorAdditive']]+[H+n for n in ['eq_smul_one','eq_smul_one_generated','hf_eq_scale_vnorm','imagLeak12_not_sectorAdditive']])
    add(ip['rust'],['code/rust/src/qm/inner_product_uniqueness.rs::derive_scale','code/rust/src/qm/inner_product_uniqueness.rs::hermitian_derive_scale'])
    ip['imported_structure']=['sector additivity of the quadratic readout on disjoint supports: assumption (transcribed from l1 additivity)','transitive sector symmetry of the readout: assumption','sector carrier, scalar field and quadratic readout shape: assumption','free linearization coefficient pack: assumption']
    ip['tags']=[t for t in ip.get('tags',[]) if t!='gap']+['conditional-on-readout-laws']
    oa['status']='CONDITIONAL'
    oa['source_status']=('Orthogonality of the sector basis derived from sector additivity of the readout alone in '+RUN+' (SectorFormUniqueness.offdiag_pair_sum_eq_zero, offdiag_eq_zero, eq_diagonal_of_sectorAdditive, qf_eq_sum_diag_sq_of_sectorAdditive; SectorFormHermitian.offdiag_eq_zero with the two directions 1 and i, and imagLeak12 showing the second direction is needed). Earlier: '+oa['source_status'])
    oa['statement']=oa['statement']+' Sector additivity of the quadratic readout on disjoint supports forces every off-diagonal Gram entry to vanish, so the sector basis is orthogonal for every sector-additive form and the readout is the diagonal sum ('+RUN+').'
    oa['bottleneck']='Sector additivity of the quadratic readout is supplied as a law (transcribed from l1 additivity); frame additivity on arbitrary orthogonal frames of the selected form, as Gleason-type uniqueness needs, is not derived here (H013 headers say Candidate only).'
    add(oa['lean'],[R+n for n in ['offdiag_pair_sum_eq_zero','offdiag_eq_zero','eq_diagonal_of_sectorAdditive','qf_eq_sum_diag_sq_of_sectorAdditive','l1_disjoint_additive']]+[H+n for n in ['offdiag_eq_zero','imagLeak12_imag_direction_not_additive']])
    add(oa.setdefault('rust',[]),['code/rust/src/qm/inner_product_uniqueness.rs::sector_additivity_certificate','code/rust/src/qm/inner_product_uniqueness.rs::hermitian_sector_additivity_certificate'])
    oa['imported_structure']=['sector additivity of the quadratic readout on disjoint supports: assumption (transcribed from l1 additivity)','projection measures / frames beyond the sector basis: assumption']
    oa['tags']=[t for t in oa.get('tags',[]) if t!='gap']+['conditional-on-readout-laws']
    src=[RUN+'/README.md','lean4/SectorFormUniqueness.lean','lean4/SectorFormHermitian.lean']
    new=[{'id':'L1-R-INNER-PRODUCT-SECTOR-FORM','inputs':['L1-GS000-EDGEWISE-L1','L1-QM020-THM2A-L1-ADDITIVITY-DEFECT'],'output':'L1-IMP-HILBERT-INNER-PRODUCT','status':'CONDITIONAL_ON_IMPORT','source':src,'note':'Holds once two laws of the quadratic readout are supplied: sector additivity on disjoint supports (the transcription of edgewise l1 additivity) and invariance under sector permutations generating a transitive group; yields G = c * 1 with c > 0, the standard form of the Born carriers (rational and Gaussian-rational cases).'},
         {'id':'L1-R-ORTHOGONAL-ADDITIVITY-SECTOR-FORM','inputs':['L1-GS000-EDGEWISE-L1','L1-QM020-THM2A-L1-ADDITIVITY-DEFECT'],'output':'L1-IMP-ORTHOGONAL-ADDITIVITY','status':'CONDITIONAL_ON_IMPORT','source':src,'note':'Holds once sector additivity of the quadratic readout is supplied; orthogonality of the sector basis follows without any symmetry assumption.'}]
    first_app=next((i for i,r in enumerate(d['routes']) if r['id'].startswith('APP-R-')),len(d['routes']))
    for k,r in enumerate(new):
        assert r['id'] not in routes;d['routes'].insert(first_app+k,r)  # application-branch routes stay last (dag/sync_application_branches.py)
    DAG.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode('utf-8'))
    print(json.dumps({'nodes':len(d['nodes']),'routes':len(d['routes']),'updated':['L1-IMP-HILBERT-INNER-PRODUCT','L1-IMP-ORTHOGONAL-ADDITIVITY'],'added_routes':[r['id'] for r in new]}))
if __name__=='__main__':main()
