// Independent fixed-input wire specification; trusts BLAKE3 and BigInt byte storage,
// but calls neither the production scalar encoder nor production hash composition.
#[cfg(test)]
mod wire_specification {
    use super::*;
    use crate::linear_algebra::scalars::q;

    fn number(bytes: &mut Vec<u8>, n: u64) { bytes.extend(n.to_le_bytes()); }
    fn integer(bytes: &mut Vec<u8>, n: BigInt) {
        let stored = n.to_signed_bytes_le();
        number(bytes, stored.len() as u64);
        bytes.extend(stored);
    }
    fn pair(bytes: &mut Vec<u8>, n: BigInt, d: BigInt) {
        integer(bytes, n); integer(bytes, d);
    }
    fn finish(bytes: Vec<u8>) -> [u8; 32] { *blake3::hash(&bytes).as_bytes() }
    fn vector_wire(tag: &[u8]) -> [u8; 32] {
        let mut bytes = tag.to_vec(); number(&mut bytes, 4);
        pair(&mut bytes, 0.into(), 1.into());
        pair(&mut bytes, 1.into(), 2.into());
        pair(&mut bytes, (-1).into(), 2.into());
        pair(&mut bytes, BigInt::from(1) << 200, 11.into());
        finish(bytes)
    }
    fn sample() -> Vec<Q> {
        vec![q(0), Q::new_raw(2.into(),4.into()), Q::new_raw(1.into(),(-2).into()),
            Q::new_raw(BigInt::from(1) << 200, 11.into())]
    }

    #[test]
    fn rational_and_integer_wires() {
        let values = sample();
        assert_eq!(*hash_vector(&values).as_bytes(), vector_wire(b"OMEGA.Vector<BigRational>.v2"));
        assert_eq!(*hash_weights(&values).as_bytes(), vector_wire(b"MSSN.CarrierWeights<BigRational>.v2"));
        let mut bytes = b"MSSN.BasicMatrix<BigRational>.v2".to_vec();
        number(&mut bytes, 2); number(&mut bytes, 2);
        for (n,d) in [(0,1),(1,2),(-1,2)] { pair(&mut bytes,n.into(),d.into()); }
        pair(&mut bytes,BigInt::from(1) << 200,11.into());
        let matrix = BasicMatrix::from_row_major(2,2,values).unwrap();
        assert_eq!(*hash_matrix(&matrix).as_bytes(),finish(bytes));
        let integers = vec![(-129).into(),128.into(),BigInt::from(1) << 200];
        let mut bytes = b"MSSN.BasicMatrix<BigInt>.lattice.v1".to_vec();
        number(&mut bytes,1); number(&mut bytes,3);
        for n in integers.clone() { integer(&mut bytes,n); }
        let matrix = BasicMatrix::from_row_major(1,3,integers).unwrap();
        assert_eq!(*hash_integer_matrix(&matrix).as_bytes(),finish(bytes));
        for (rows,cols) in [(0,usize::MAX),(usize::MAX,0)] {
            let mut bytes = b"MSSN.BasicMatrix<BigRational>.v2".to_vec();
            number(&mut bytes,rows as u64); number(&mut bytes,cols as u64);
            let matrix = BasicMatrix::from_row_major(rows,cols,vec![]).unwrap();
            assert_eq!(*hash_matrix(&matrix).as_bytes(),finish(bytes));
        }
    }

    #[test]
    fn undefined_pairs_are_stored_without_rational_arithmetic() {
        for n in [BigInt::from(0),1.into(),(-1).into(),BigInt::from(1) << 200] {
            let value = Q::new_raw(n.clone(),0.into());
            for (tag,actual) in [
                (b"OMEGA.Vector<BigRational>.v2".as_slice(),hash_vector(&[value.clone()])),
                (b"MSSN.CarrierWeights<BigRational>.v2".as_slice(),hash_weights(&[value.clone()])),
            ] {
                let mut bytes = tag.to_vec(); number(&mut bytes,1);
                pair(&mut bytes,n.clone(),0.into());
                assert_eq!(*actual.as_bytes(),finish(bytes));
            }
            let mut bytes = b"MSSN.BasicMatrix<BigRational>.v2".to_vec();
            number(&mut bytes,1); number(&mut bytes,1); pair(&mut bytes,n,0.into());
            let matrix = BasicMatrix::from_row_major(1,1,vec![value]).unwrap();
            assert_eq!(*hash_matrix(&matrix).as_bytes(),finish(bytes));
        }
    }

    #[test]
    fn graded_identifiers_use_byte_lengths_and_signed_degrees() {
        for kind in [b"chain".as_slice(),b"cochn",b"\0\xff"] {
            for degree in [i32::MIN,-1,0,i32::MAX] {
                for basis in ["a\0b","\u{03b1}",""] {
                    let mut bytes = b"TFQM.GradedVector.v1".to_vec();
                    number(&mut bytes,kind.len() as u64); bytes.extend(kind);
                    bytes.extend(degree.to_le_bytes());
                    number(&mut bytes,basis.len() as u64); bytes.extend(basis.as_bytes());
                    bytes.extend(vector_wire(b"OMEGA.Vector<BigRational>.v2"));
                    assert_eq!(*hash_graded_vector(kind,degree,basis,&sample()).as_bytes(),finish(bytes));
                }
            }
        }
    }

    #[test]
    fn manifest_fields_have_the_declared_order_and_domains() {
        let a = Hash256([17;32]); let b = Hash256([29;32]); let c = Hash256([53;32]);
        let dimensions = [2usize,5,11];
        for (tag,actual) in [
            (b"OMEGA.ChainComplexManifest.v1".as_slice(),hash_chain_complex_manifest(2,5,11,&a,&b)),
            (b"OMEGA.CochainComplexManifest.v1".as_slice(),hash_cochain_complex_manifest(2,5,11,&a,&b)),
        ] {
            let mut bytes = tag.to_vec();
            for n in dimensions { number(&mut bytes,n as u64); }
            bytes.extend(a.0); bytes.extend(b.0);
            assert_eq!(actual.0,finish(bytes));
        }
        let mut bytes = b"TFQM.CarrierManifest.v1".to_vec();
        bytes.extend(1u32.to_le_bytes()); bytes.extend(a.0); bytes.extend(b.0); bytes.extend(c.0);
        for n in dimensions { number(&mut bytes,n as u64); }
        bytes.extend(b"Q"); bytes.extend(b"BigRational");
        assert_eq!(hash_carrier_manifest(2,5,11,&a,&b,&c).0,finish(bytes));
        let mut bytes = b"MSSN.CochainComplexWitness.v1".to_vec();
        for n in [2,5,11,17] { number(&mut bytes,n); } bytes.extend(a.0);
        assert_eq!(hash_cochain_witness((2,5),(11,17),&a).0,finish(bytes));
        let mut bytes = b"MSSN.TheoremProvenance.v1".to_vec(); bytes.extend("source\0\u{03b1}".as_bytes());
        assert_eq!(hash_provenance("source\0\u{03b1}").0,finish(bytes));
    }

    #[test]
    fn digest_views_and_wire_roundtrip_preserve_every_byte() {
        let h = Hash256(std::array::from_fn(|i| (i as u8)*7));
        let hex = "00070e151c232a31383f464d545b626970777e858c939aa1a8afb6bdc4cbd2d9";
        assert_eq!(h.to_hex(),hex);
        assert_eq!(h.to_string(),"00070e15..c4cbd2d9");
        assert_eq!(h.as_bytes(),&h.0);
        let restored: Hash256 = serde_json::from_str(&serde_json::to_string(&h).unwrap()).unwrap();
        assert_eq!(restored,h);
    }
}
