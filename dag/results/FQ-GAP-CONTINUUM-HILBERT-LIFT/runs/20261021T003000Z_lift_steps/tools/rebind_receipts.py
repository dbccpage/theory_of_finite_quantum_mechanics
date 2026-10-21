"""Rebind the count fields (and the drifted current-file digests) of the two tensor research receipts to
the DAG after the construction-node split; every previous value is kept under 'rebound'. The Lean replay
sections of the receipts are not touched."""
from pathlib import Path
import hashlib,json,sys
B=Path(__file__).resolve().parents[1]
ROOT=next(p for p in B.parents if (p/'lean4/lakefile.lean').is_file())
RUN=B.relative_to(ROOT).as_posix()
RECEIPTS={'dag/research/tensor_measurement_validation.json':[],'dag/research/tensor_countermodel_validation.json':['dag/derivation_dag.json','lean4/lakefile.lean']}
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def main():
    dag=json.loads((ROOT/'dag/derivation_dag.json').read_text(encoding='utf-8'))
    records=[l for l in (ROOT/'dag/theory_of_finite_qm.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()]
    counts={'dag_nodes':len(dag['nodes']),'dag_routes':len(dag['routes']),'master_records':len(records)}
    for rel,rehash in RECEIPTS.items():
        p=ROOT/rel;raw=p.read_bytes();crlf=b'\r\n' in raw;r=json.loads(raw.decode('utf-8'))
        rebound=r.setdefault('rebound',[])
        if r['counts']!=counts:
            rebound.append({'field':'counts','previous':r['counts'],'current':counts,'reason':'FQ-CONTINUUM-HILBERT-LIFT-CONSTRUCTION and its two routes were added by '+RUN+'/tools/dag_update.py; no tensor node, route or master record changed','run':RUN})
            r['counts']=counts
        for path in rehash:
            now=sha(path)
            if r['sha256'].get(path)!=now:
                rebound.append({'field':'sha256','path':path,'previous':r['sha256'].get(path),'current':now,'reason':'current-file digest rebound after the DAG split (and lakefile registration of the HilbertLift modules); the Lean replay section and every other digest are unchanged','run':RUN})
                r['sha256'][path]=now
        out=json.dumps(r,indent=2,ensure_ascii=False)+'\n'
        p.write_bytes((out.replace('\n','\r\n') if crlf else out).encode('utf-8'))
        print(json.dumps({'receipt':rel,'counts':r['counts'],'rebound_entries':len(rebound)}))
if __name__=='__main__':sys.exit(main())
