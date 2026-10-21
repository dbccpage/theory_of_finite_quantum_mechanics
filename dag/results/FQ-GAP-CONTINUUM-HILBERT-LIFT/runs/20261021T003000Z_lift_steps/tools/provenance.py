"""Record the prior evidence this run builds on, with exact digests; nothing is modified."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parents[1]
ROOT=next(p for p in B.parents if (p/'lean4/lakefile.lean').is_file())
PRIOR=['dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261020T230000Z_completion/README.md','dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261020T230000Z_completion/review.md','dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261020T230000Z_completion/claim_status.json','dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261020T230000Z_completion/next_steps.md','dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261020T230000Z_completion/accepted_modules.json','dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261020T230000Z_completion/manifest.json','dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261020T230000Z_completion/tools/replay.py','lean4/HilbertLiftFiniteTower.lean','lean4/HilbertLiftRationalUniformity.lean','lean4/HilbertLiftCompletion.lean','lean4/HilbertLiftComplexCarrier.lean','lean4/lean-toolchain','lean4/lake-manifest.json']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
if __name__=='__main__':
    entries=[{'path':p,'bytes':(ROOT/p).stat().st_size,'sha256':sha(ROOT/p)} for p in PRIOR]
    (B/'provenance.json').write_text(json.dumps({'authority_effect':'None','prior_evidence':entries,'relation_to_prior':'This run carries out items 2 to 6 of the prior run\'s next_steps.md (item 1 was already discharged by HilbertLiftComplexCarrier). The four prior modules are copied byte for byte into this run and re-replayed so that the bundle is self-contained; their statements are unchanged.','replay_tool':'tools/replay.py is byte-identical to the one of runs/20261020T230000Z_completion.','unchanged':'The sealed prior run, canonical operad collections and monographs are not modified by this run.'},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'prior_entries':len(entries)}))
