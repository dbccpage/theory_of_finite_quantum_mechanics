"""Native graded-coordinate and map oracles. AuthorityEffect: None.

Integer arithmetic supplies expected vector entries and matrix-vector products;
raw-pair/degree/metadata failures are observed at their actual public gates.
"""
from pathlib import Path as _FilesystemPath
import sys as _contract_sys
_contract_sys.path.insert(0, str(_FilesystemPath(__file__).resolve().parents[4] / "scripts"))
from contract_scores import RecordPath as Path, copy_file as _copy_record_file

VECTOR = r'''
use crate::linear_algebra::scalars::q;
fn basis(s:&str)->BasisId{BasisId::new(s).unwrap()}
fn widened(n:i128)->Q{Q::from_integer(n.into())}
fn exercise<K:VectorKind>(){
 for a in -2i64..=2 {for b in -2i64..=2 {for c in -2i64..=2 {for d in -2i64..=2 {
  let x=GradedVector::<K>::new(Degree::new(-7),basis("family"),vec![q(a),q(b)]).unwrap();
  let y=GradedVector::<K>::new(Degree::new(-7),basis("family"),vec![q(c),q(d)]).unwrap();let before=(x.clone(),y.clone());
  let sum=x.add(&y).unwrap();let difference=x.sub(&y).unwrap();
  assert_eq!(sum.coefficients(),&[widened(a as i128+c as i128),widened(b as i128+d as i128)]);
  assert_eq!(difference.coefficients(),&[widened(a as i128-c as i128),widened(b as i128-d as i128)]);
  assert_eq!(sum.degree(),Degree::new(-7));assert_eq!(difference.basis_id(),&basis("family"));assert_eq!(sum.dimension(),2);
  for scalar in -2i64..=2 {let scaled=x.scalar_mul(&q(scalar)).unwrap();assert_eq!(scaled.coefficients(),&[widened((a as i128)*(scalar as i128)),widened((b as i128)*(scalar as i128))]);assert_eq!(scaled.degree(),x.degree());assert_eq!(scaled.basis_id(),x.basis_id());}
  assert_eq!((x,y),before);
 }}}}
 for dim in [0,1,7,64]{let z=GradedVector::<K>::zero(Degree::new(i32::MIN),basis("zero"),dim).unwrap();assert_eq!(z.dimension(),dim);assert!(z.is_zero());assert_eq!(z.degree(),Degree::new(i32::MIN));assert_eq!(z.coefficients(),vec![q(0);dim]);}
 assert_eq!(GradedVector::<K>::zero(Degree::new(0),basis("x"),usize::MAX).unwrap_err(),HomologicalError::ResourceLimit("zero vector allocation"));
 let large:num_bigint::BigInt=(num_bigint::BigInt::from(1)<<200usize)+1;
 let x=GradedVector::<K>::new(Degree::new(i32::MAX),basis("large"),vec![Q::new(large.clone(),2.into())]).unwrap();
 assert_eq!(x.scalar_mul(&q(2)).unwrap().coefficients(),&[Q::from_integer(large)]);
 let c=GradedVector::<K>::from_canonical(Degree::new(5),basis("literal"),vec![q(2),q(-3)]);assert_eq!(c.degree(),Degree::new(5));assert_eq!(c.basis_id(),&basis("literal"));assert_eq!(c.coefficients(),&[q(2),q(-3)]);
}
#[test] fn widened_coordinate_arithmetic_zero_and_owned_context(){exercise::<ChainKind>();exercise::<CochainKind>();}
fn bad<K:VectorKind>(){
 let x=GradedVector::<K>::new(Degree::new(2),basis("left"),vec![q(1),q(2)]).unwrap();
 let all_wrong=GradedVector::<K>::new(Degree::new(3),basis("right"),vec![q(1)]).unwrap();
 for result in [x.add(&all_wrong),x.sub(&all_wrong)]{assert_eq!(result.unwrap_err(),HomologicalError::DegreeMismatch{expected:2,got:3});}
 let wrong_basis=GradedVector::<K>::new(Degree::new(2),basis("right"),vec![q(1)]).unwrap();
 for result in [x.add(&wrong_basis),x.sub(&wrong_basis)]{assert_eq!(result.unwrap_err(),HomologicalError::BasisMismatch{description:"different graded basis families".into()});}
 let wrong_length=GradedVector::<K>::new(Degree::new(2),basis("left"),vec![q(1)]).unwrap();
 for result in [x.add(&wrong_length),x.sub(&wrong_length)]{assert_eq!(result.unwrap_err(),HomologicalError::DimensionMismatch{expected:2,got:1});}
 for (n,d) in [(1,0),(2,2),(0,2),(1,-1)]{let raw=Q::new_raw(n.into(),d.into());assert_eq!(GradedVector::<K>::new(Degree::new(0),basis("x"),vec![q(1),raw.clone()]).unwrap_err(),HomologicalError::InvalidRational{index:1});assert_eq!(x.scalar_mul(&raw).unwrap_err(),HomologicalError::InvalidRational{index:0});let empty=GradedVector::<K>::zero(Degree::new(0),basis("x"),0).unwrap();assert_eq!(empty.scalar_mul(&raw).unwrap_err(),HomologicalError::InvalidRational{index:0});}
 assert!(!x.is_zero());
 let mut wire=serde_json::to_value(&x).unwrap();wire["coefficients"]=serde_json::to_value(vec![Q::new_raw(2.into(),2.into())]).unwrap();assert!(serde_json::from_value::<GradedVector<K>>(wire).is_err());
 let wire=serde_json::to_value(&x).unwrap();assert_eq!(serde_json::from_value::<GradedVector<K>>(wire.clone()).unwrap(),x);let mut extra=wire.clone();extra["kind"]=serde_json::json!("forged");assert!(serde_json::from_value::<GradedVector<K>>(extra).is_err());let mut label=wire;label["basis_id"]=serde_json::json!(" ");assert!(serde_json::from_value::<GradedVector<K>>(label).is_err());
}
#[test] fn ordered_domain_compatibility_and_wire_gates(){bad::<ChainKind>();bad::<CochainKind>();}
#[test] fn kind_is_static_wire_is_untagged_and_hash_is_framed(){
 assert_eq!(ChainKind::TAG,b"chain");assert_eq!(CochainKind::TAG,b"cochain");
 let a=GradedVector::<ChainKind>::new(Degree::new(9),basis("family"),vec![q(1)]).unwrap();let b=GradedVector::<CochainKind>::new(Degree::new(9),basis("family"),vec![q(1)]).unwrap();
 assert_eq!(serde_json::to_value(&a).unwrap(),serde_json::to_value(&b).unwrap());assert_ne!(a.hash(),b.hash());
 assert_eq!(a.hash(),hash_graded_vector(b"chain",9,"family",&[q(1)]));assert_eq!(b.hash(),hash_graded_vector(b"cochain",9,"family",&[q(1)]));
}
'''

MAP = r'''
use crate::linear_algebra::scalars::q;
use crate::homology::ids::BasisId;
fn basis(s:&str)->BasisId{BasisId::new(s).unwrap()}
fn m(r:usize,c:usize,v:Vec<i64>)->BasicMatrix<Q>{BasicMatrix::from_row_major(r,c,v.into_iter().map(q).collect()).unwrap()}
fn widened(n:i128)->Q{Q::from_integer(n.into())}
#[test] fn independent_integer_products_and_context_transfer(){
 for a in [-1i64,0,1]{for b in [-1i64,0,1]{for c in [-1i64,0,1]{for d in [-1i64,0,1]{
  let matrix=m(2,2,vec![a,b,c,d]);let map=__MAP__::new(Degree::new(__FROM__),Degree::new(__TO__),matrix.clone()).unwrap();
  assert_eq!(map.from_degree(),Degree::new(__FROM__));assert_eq!(map.to_degree(),Degree::new(__TO__));assert_eq!(map.matrix(),&matrix);assert_eq!((map.source_dim(),map.target_dim()),(2,2));assert_eq!(map.hash(),hash_matrix(&matrix));assert_eq!(map.map_hash,hash_matrix(&matrix));assert_eq!(map.clone(),map);
  for x in -2i64..=2 {for y in -2i64..=2 {let input=__VECTOR__::new(Degree::new(__FROM__),basis("caller family"),vec![q(x),q(y)]).unwrap();let old=input.clone();let output=map.apply(&input).unwrap();assert_eq!(input,old);assert_eq!(output.degree(),Degree::new(__TO__));assert_eq!(output.basis_id(),&basis("caller family"));assert_eq!(output.coefficients(),&[widened((a as i128)*(x as i128)+(b as i128)*(y as i128)),widened((c as i128)*(x as i128)+(d as i128)*(y as i128))]);}}
 }}}}
 let map=__MAP__::new(Degree::new(__FROM__),Degree::new(__TO__),m(2,3,vec![1,2,3,4,5,6])).unwrap();assert_eq!((map.source_dim(),map.target_dim()),(3,2));
 let v=__VECTOR__::new(Degree::new(__FROM__),basis("different family is allowed"),vec![q(1),q(0),q(-1)]).unwrap();let output=map.apply(&v).unwrap();assert_eq!(output.coefficients(),&[q(-2),q(-2)]);assert_eq!(output.basis_id(),v.basis_id());
 let same_matrix=__MAP__::new(Degree::new(10),Degree::new(__TEN_TO__),map.matrix().clone()).unwrap();assert_eq!(map.hash(),same_matrix.hash()); // matrix fingerprint, not degree/family authentication
 for (r,c) in [(0,0),(0,2),(2,0)]{let map=__MAP__::new(Degree::new(__FROM__),Degree::new(__TO__),m(r,c,vec![0;r*c])).unwrap();let v=__VECTOR__::zero(Degree::new(__FROM__),basis("empty"),c).unwrap();let out=map.apply(&v).unwrap();assert_eq!(out.dimension(),r);assert!(out.is_zero());}
 let large:num_bigint::BigInt=(num_bigint::BigInt::from(1)<<200usize)+1;let v=__VECTOR__::new(Degree::new(__FROM__),basis("large"),vec![Q::new(large.clone(),2.into())]).unwrap();let map=__MAP__::new(Degree::new(__FROM__),Degree::new(__TO__),m(1,1,vec![2])).unwrap();assert_eq!(map.apply(&v).unwrap().coefficients(),&[Q::from_integer(large)]);
}
#[test] fn ordered_input_degree_length_and_overflow_failures(){
 for raw in [Q::new_raw(1.into(),0.into()),Q::new_raw(2.into(),2.into())]{let matrix=BasicMatrix::from_row_major(1,1,vec![raw]).unwrap();assert_eq!(__MAP__::new(Degree::new(__OVERFLOW__),Degree::new(0),matrix).unwrap_err(),HomologicalError::InvalidRational{index:0});}
 assert_eq!(__MAP__::new(Degree::new(__OVERFLOW__),Degree::new(0),m(0,0,vec![])).unwrap_err(),HomologicalError::DegreeOverflow);
 assert_eq!(__MAP__::new(Degree::new(10),Degree::new(20),m(0,0,vec![])).unwrap_err(),HomologicalError::DegreeMismatch{expected:__TEN_TO__,got:20});
 let map=__MAP__::new(Degree::new(__FROM__),Degree::new(__TO__),m(2,3,vec![0;6])).unwrap();
 let wrong=__VECTOR__::new(Degree::new(7),basis("x"),vec![q(1)]).unwrap();assert_eq!(map.apply(&wrong).unwrap_err(),HomologicalError::DegreeMismatch{expected:__FROM__,got:7});
 let short=__VECTOR__::new(Degree::new(__FROM__),basis("x"),vec![q(1)]).unwrap();assert_eq!(map.apply(&short).unwrap_err(),HomologicalError::DimensionMismatch{expected:3,got:1});
}
'''


def challenge(subject):
    name=Path(subject['path']).stem
    if name=='graded_vector':body=VECTOR
    else:
        down=name=='boundary'
        replacements={'__MAP__':'BoundaryMap' if down else 'CoboundaryMap',
                      '__VECTOR__':'Chain' if down else 'Cochain',
                      '__FROM__':'1' if down else '0','__TO__':'0' if down else '1',
                      '__TEN_TO__':'9' if down else '11',
                      '__OVERFLOW__':'i32::MIN' if down else 'i32::MAX'}
        body=MAP
        for key,value in replacements.items():body=body.replace(key,value)
    return '\n#[cfg(test)] mod independent_vector_maps { use super::*;\n'+body+'\n}\n'
