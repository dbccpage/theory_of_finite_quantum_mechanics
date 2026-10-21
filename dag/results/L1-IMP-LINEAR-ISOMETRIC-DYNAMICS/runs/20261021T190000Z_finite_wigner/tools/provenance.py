"""Record the prior evidence this run builds on and the restored import oleans, with exact digests; nothing is modified."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parents[1]
ROOT=next(p for p in B.parents if (p/'lean4/lakefile.lean').is_file())
S='dag/results/L1-IMP-HILBERT-INNER-PRODUCT/runs/20261021T013500Z_sector_form/'
E='dag/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/runs/20261020T205000Z_effect_valuation_lean/'
G='dag/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/runs/20261020T224000Z_gaussian_hermitian_carrier/'
PRIOR=[S+'README.md',S+'review.md',S+'next_steps.md',S+'SectorFormHermitian.lean',S+'verification/h01/compiled.olean.bin',S+'tools/replay.py',S+'tools/seal.py',S+'tools/companions.py',
 E+'README.md',E+'BornEffectValuation.lean',G+'README.md',G+'BornGaussRat.lean',G+'BornHermitianCarrier.lean',G+'BornHermitianPsdDecomposition.lean',
 'lean4/BornEffectValuation.lean','lean4/BornGaussRat.lean','lean4/BornHermitianCarrier.lean','lean4/BornHermitianPsdDecomposition.lean','lean4/SectorFormHermitian.lean',
 'lean4/H006PermutationUnitary.lean','lean4/H003ReversibilityGate.lean','lean4/DiscreteTimeStoneSpec.lean','lean4/U1QuadraticTowerAndCayleyStone.lean','lean4/lean-toolchain','lean4/lake-manifest.json',
 'dag/operads/l1_imp_linear_isometric_dynamics.yaml','dag/results/L1-IMP-LINEAR-ISOMETRIC-DYNAMICS/reviews/20261020_born_boundary_audit/README.md','dag/results/L1-IMP-LINEAR-ISOMETRIC-DYNAMICS/runs/20261020T000351Z_staged/README.md','dag/derivations/08_l1_to_l2/tfq_0303_linear_isometric_dynamics_are_an_import.md',
 'code/python/src/qm/inner_product_uniqueness.py','code/python/src/qm/born_hermitian_valuation.py','code/rust/src/qm/inner_product_uniqueness.rs','code/rust/src/qm/born_hermitian_valuation.rs']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
if __name__=='__main__':
    entries=[{'path':p,'bytes':(ROOT/p).stat().st_size,'sha256':sha(ROOT/p)} for p in PRIOR]
    restored=json.loads((B/'tools/restored_oleans.json').read_text(encoding='utf-8'))
    for r in restored['restored']:
        here=B/'build'/(r['module']+'.olean')
        r['restored_copy_sha256']=sha(here) if here.is_file() else None
        r['source_sha256_now']=sha(ROOT/r['source'])
    (B/'provenance.json').write_text(json.dumps({'authority_effect':'None','prior_evidence':entries,'restored_import_oleans':restored,'builds_on':'FiniteWignerKernel imports BornHermitianCarrier (the Gaussian-rational carrier, its readout hf and the rank-one effects P x whose Born readout is the transition probability) and BornHermitianPsdDecomposition (hf_single, hf_add_vec, mulVec_single\'); FiniteWignerSimilarity imports SectorFormHermitian for the coordinate action permute of the H006 permutation envelope; GaussRatAutomorphisms imports BornGaussRat. The sector-form run fixed the inner product up to a unit scale, which is why the transition probability (scale-free) is the right invariant to impose on the dynamics; this run is item 2 of its next_steps.md.','replay_tool':'tools/replay.py is byte-identical to the Born and sector-form runs\' tool; tools/seal.py differs only in the pinned compiler version 4.35.0.','unchanged':'Prior sealed bundles, canonical operad collections and user submissions are not modified by this run.'},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'prior_entries':len(entries),'restored_oleans':len(restored['restored'])}))
