"""Record the prior evidence this run builds on, with exact digests; nothing is modified."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parents[1]
ROOT=next(p for p in B.parents if (p/'lean4/lakefile.lean').is_file())
E='dag/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/runs/20261020T205000Z_effect_valuation_lean/'
G='dag/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/runs/20261020T224000Z_gaussian_hermitian_carrier/'
PRIOR=[E+'README.md',E+'BornEffectValuation.lean',E+'BornMatrixCarrier.lean',E+'verification/effect_valuation_01/compiled.olean.bin',E+'verification/matrix_carrier_01/compiled.olean.bin',E+'next_steps.md',E+'tools/replay.py',
 G+'README.md',G+'BornGaussRat.lean',G+'BornHermitianCarrier.lean',G+'BornHermitianPsdDecomposition.lean',G+'verification/gauss_rat_01/compiled.olean.bin',G+'verification/hermitian_carrier_01/compiled.olean.bin',G+'verification/hermitian_psd_01/compiled.olean.bin',G+'next_steps.md',G+'tools/replay.py',G+'tools/seal.py',
 'lean4/H005InnerProductAdmission.lean','lean4/H006PermutationUnitary.lean','lean4/BornRedundancy.lean',
 'dag/operads/l1_imp_hilbert_inner_product.yaml','dag/operads/l1_imp_orthogonal_additivity.yaml',
 'dag/results/L1-IMP-HILBERT-INNER-PRODUCT/reviews/20261019_l1_import_audit/README.md','dag/results/L1-IMP-ORTHOGONAL-ADDITIVITY/reviews/20261020_born_boundary_audit/README.md',
 'code/python/src/qm/born_effect_valuation.py','code/python/src/qm/born_hermitian_valuation.py','code/rust/src/qm/born_effect_valuation.rs','code/rust/src/qm/born_hermitian_valuation.rs','lean4/lean-toolchain','lean4/lake-manifest.json']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
if __name__=='__main__':
    entries=[{'path':p,'bytes':(ROOT/p).stat().st_size,'sha256':sha(ROOT/p)} for p in PRIOR]
    (B/'provenance.json').write_text(json.dumps({'authority_effect':'None','prior_evidence':entries,'builds_on':'The rational module imports BornMatrixCarrier (whose qf is the readout selected here) and the Hermitian module imports BornHermitianCarrier and BornHermitianPsdDecomposition; their sealed oleans (and those of their imports BornEffectValuation and BornGaussRat) were restored into build/ from the receipts named above. H005InnerProductAdmission supplies the non-uniqueness countermodel diag(1,2), H006PermutationUnitary the permutation-isometry convention, BornRedundancy the D1 additivity defect that SectorAdditive transcribes.','replay_tool':'tools/replay.py and tools/seal.py are byte-identical to those of the Gaussian-rational Born run.','unchanged':'Prior sealed bundles, canonical operad collections and user submissions are not modified by this run.'},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'prior_entries':len(entries)}))
