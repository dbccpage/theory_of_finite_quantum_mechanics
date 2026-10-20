"""Record the prior evidence this run builds on, with exact digests; nothing is modified."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parents[1]
ROOT=next(p for p in B.parents if (p/'lean4/lakefile.lean').is_file())
E='dag/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/runs/20261020T205000Z_effect_valuation_lean/'
PRIOR=[E+'README.md',E+'BornEffectValuation.lean',E+'BornLinearExtension.lean',E+'BornMatrixCarrier.lean',E+'BornPsdDecomposition.lean',E+'BornTraceRepresentation.lean',E+'verification/effect_valuation_01/compiled.olean.bin',E+'verification/linear_extension_01/compiled.olean.bin',E+'next_steps.md',E+'tools/replay.py','code/python/src/qm/born_effect_valuation.py','code/rust/src/qm/born_effect_valuation.rs','lean4/lean-toolchain','lean4/lake-manifest.json']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
if __name__=='__main__':
    entries=[{'path':p,'bytes':(ROOT/p).stat().st_size,'sha256':sha(ROOT/p)} for p in PRIOR]
    (B/'provenance.json').write_text(json.dumps({'authority_effect':'None','prior_evidence':entries,'builds_on':'The abstract modules BornEffectValuation and BornLinearExtension of the effect-valuation run are imported unchanged (their sealed oleans were restored into build/ from the receipts named above); the real-symmetric carrier modules are the templates mirrored here over Q(i).','replay_tool':'tools/replay.py is byte-identical to the one of the effect-valuation run.','unchanged':'Prior sealed bundles, canonical operad collections and user submissions are not modified by this run.'},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'prior_entries':len(entries)}))
