"""Build the explicit one-fault policy; refuse ambiguous source edits."""
import hashlib
import json
from pathlib import Path as _FilesystemPath
import sys as _contract_sys
_contract_sys.path.insert(0, str(_FilesystemPath(__file__).resolve().parents[4] / "scripts"))
from contract_scores import RecordPath as Path, copy_file as _copy_record_file

ROOT = Path(__file__).resolve().parents[4]
BASE = "code/rust/src/homology/"

ROOT_FAULTS = [
    ('hasher.update(b"TheoryOfFiniteQM.ExactMatrix<Q>.v1");', 'hasher.update(b"WrongMatrix.v1");'),
    ('&(m.rows() as u64).to_le_bytes()', '&(m.cols() as u64).to_le_bytes()'),
    ('hashing::hash_stored_rational(&mut hasher, val);', 'hashing::hash_stored_rational(&mut hasher, &crate::linear_algebra::scalars::q(0));'),
    ('#[serde(rename = "CarrierWire")]', '#[serde(rename = "WrongCarrierWire")]'),
    ('serialize_newtype_struct("ExactMatrix", *matrix)', 'serialize_newtype_struct("WrongMatrix", *matrix)'),
    ('serializer.serialize_newtype_struct("ExactMatrix", *matrix)', '(*matrix).serialize(serializer)'),
    ('c0_dim: self.c0_dim(),', 'c0_dim: self.c1_dim(),'),
    ('c2_dim: self.c2_dim(),', 'c2_dim: self.c0_dim(),'),
    ('d0: self.d0(),', 'd0: self.d1(),'),
    ('weights: self.weights(),', 'weights: &[], '),
    ('d0_hash: hash_legacy_matrix(self.d0()),', 'd0_hash: hash_legacy_matrix(self.d1()),'),
    ('carrier::Carrier::new(c0_dim, c1_dim, c2_dim, d0.0, d1.0, weights, provenance)?', 'carrier::Carrier::new(c1_dim, c0_dim, c2_dim, d0.0, d1.0, weights, provenance)?'),
    ('self.inner.c0_dim()', 'self.inner.c1_dim()'),
    ('self.inner.rank_d0()', 'self.inner.rank_d1()'),
    ('self.c1_dim() - self.rank_d0()', 'self.c1_dim() + self.rank_d0()'),
    ('self.inner.dim_h1()', 'Ok(0)'),
    ('if expected != got {', 'if false {'),
    ('expected: expected.to_hex(),', 'expected: got.to_hex(),'),
    ('verify_hash(&value.d0_hash, &hash_exact_matrix(&value.d0))?;', ''),
    ('verify_hash(&value.d1_hash, &hash_exact_matrix(&value.d1))?;', ''),
    ('            value.weights,', '            vec![crate::linear_algebra::scalars::q(1); value.c1_dim],'),
    ('self.inner.d0()', 'self.inner.d1()'),
]

GRAPH_FAULTS = [
    ('c0_dim, c1_dim, c2_dim, d0, d1, weights, provenance,', 'c1_dim, c0_dim, c2_dim, d0, d1, weights, provenance,'),
    ('self.inner.c0_dim()', 'self.inner.c1_dim()'),
    ('self.inner.d0()', 'self.inner.d1()'),
    ('self.inner.rank_d0()', 'self.inner.rank_d1()'),
    ('self.c1_dim() - self.rank_d0()', 'self.c1_dim() + self.rank_d0()'),
    ('self.c1_dim() - self.rank_d1() - self.rank_d0()', 'self.c1_dim() + self.rank_d1() - self.rank_d0()'),
    ('d0.set(i, src, q(-1))?;', 'd0.set(i, src, q(1))?;'),
    ('d0.set(i, tgt, q(1))?;', 'd0.set(i, tgt, q(-1))?;'),
    ('(a, c, -1)', '(a, c, 1)'),
    ('if indices.insert((src, tgt), i).is_some() {', 'if indices.insert((src, tgt), i).is_some() && false {'),
    ('if src >= n {', 'if src > n {'),
    ('if tgt >= n {', 'if tgt > n {'),
    ('if src == tgt {', 'if false {'),
    ('if vertex >= n {', 'if vertex > n {'),
    ('if a == b || b == c || a == c {', 'if a == b && b == c && a == c {'),
    ('                    src,\n                    tgt,', '                    src: tgt,\n                    tgt: src,'),
    ('d1.set(i, *col, q(sign))?;', 'd1.set(i, *col, q(-sign))?;'),
    ('BasicMatrix::<Q>::zero(edges.len(), num_nodes)?', 'BasicMatrix::<Q>::zero(num_nodes, edges.len())?'),
]

def main():
    records = []
    for name, faults in [('mod.rs', ROOT_FAULTS), ('exact_carrier.rs', GRAPH_FAULTS)]:
        path = BASE + name
        data = (ROOT/path).read_bytes()
        source = data.decode('utf-8')
        for needle, replacement in faults:
            if source.count(needle) != 1:
                raise ValueError((name, source.count(needle), needle))
            assert needle != replacement
        record = {'family': '', 'path': path, 'sha256': hashlib.sha256(data).hexdigest(),
                  'independent_module': 'independent_carrier_facades', 'faults': faults}
        if name == 'mod.rs':
            record['native_context'] = 'homology'
        else:
            record['parent_aliases'] = ['carrier', 'cochain_complex', 'carrier_manifest', 'errors']
        records.append(record)
    target = Path(__file__).with_name('carrier_facade_boundaries.json')
    target.write_text(json.dumps({'AuthorityEffect': 'None', 'records': records}, indent=2)+'\n', encoding='utf-8', newline='\n')
    print({'records': len(records), 'faults': sum(len(r['faults']) for r in records)})

if __name__ == '__main__':
    main()
