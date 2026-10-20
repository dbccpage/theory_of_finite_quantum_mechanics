"""Independent scalar, receipt and admitted-carrier boundary cases.

AuthorityEffect: None. Integer Euclid/dot products and known split ranks are
the oracles. Stored witness fields are deliberately not treated as theorems.
"""
from pathlib import Path as _FilesystemPath
import sys as _contract_sys
_contract_sys.path.insert(0, str(_FilesystemPath(__file__).resolve().parents[4] / "scripts"))
from contract_scores import RecordPath as Path, copy_file as _copy_record_file

SCALAR = r'''
fn raw(n:i64,d:i64)->Q{Q::new_raw(n.into(),d.into())}
fn euclid(mut a:i128,mut b:i128)->i128{a=a.abs();b=b.abs();while b!=0{let r=a%b;a=b;b=r;}a}
fn m(rows:usize,cols:usize,v:Vec<Q>)->BasicMatrix<Q>{BasicMatrix::from_row_major(rows,cols,v).unwrap()}
#[test] fn raw_integer_domain_first_index_and_preservation(){
 for n in -9..=9 {for d in -9..=9 {
  let v=vec![raw(1,1),raw(n,d),raw(0,1)];let before=v.iter().map(|x|(x.numer().clone(),x.denom().clone())).collect::<Vec<_>>();
  let result=admit_coefficients(&v);let valid=d>0&&euclid(n as i128,d as i128)==1;
  if valid{assert_eq!(result,Ok(()));}else{assert_eq!(result,Err(HomologicalError::InvalidRational{index:1}));}
  assert_eq!(v.iter().map(|x|(x.numer().clone(),x.denom().clone())).collect::<Vec<_>>(),before);
 }}
 assert_eq!(admit_coefficients(&[]),Ok(()));
 for index in 0..3 {let mut v=vec![raw(1,1);3];v[index]=raw(1,0);v[2]=raw(2,2);assert_eq!(admit_coefficients(&v),Err(HomologicalError::InvalidRational{index}));}
 let large=num_bigint::BigInt::from(1)<<200usize;
 assert_eq!(admit_coefficients(&[Q::new_raw(&large+1,2.into())]),Ok(()));
 assert_eq!(admit_coefficients(&[Q::new_raw(large,2.into())]),Err(HomologicalError::InvalidRational{index:0}));
}
#[test] fn shaped_admission_order_and_zero_area(){
 let bad=m(1,1,vec![raw(1,0)]);assert_eq!(admit_matrix(&bad),Err(HomologicalError::InvalidRational{index:0}));
 assert_eq!(admit_shaped_matrix(&bad,(2,3)),Err(HomologicalError::ShapeMismatch{expected:(2,3),got:(1,1)}));
 assert_eq!(admit_shaped_matrix(&bad,(1,1)),Err(HomologicalError::InvalidRational{index:0}));
 let good=m(1,1,vec![raw(1,1)]);assert_eq!(admit_shaped_matrix(&good,(1,1)),Ok(()));
 for (r,c) in [(0,0),(0,usize::MAX),(usize::MAX,0)]{assert_eq!(admit_shaped_matrix(&m(r,c,vec![]),(r,c)),Ok(()));}
}
#[test] fn canonical_products_match_widened_integer_oracle_and_preserve_error(){
 for a in [-1,0,1]{for b in [-1,0,1]{for c in [-1,0,1]{for d in [-1,0,1]{
  let first=m(1,2,vec![raw(a,1),raw(b,1)]);let second=m(2,1,vec![raw(c,1),raw(d,1)]);
  for violation in [HomologicalError::BoundaryLawViolation{degree:31},HomologicalError::DegreeOverflow,HomologicalError::NotCycle]{
   let want=if (a as i128)*(c as i128)+(b as i128)*(d as i128)==0 {Ok(())}else{Err(violation.clone())};
   assert_eq!(admit_zero_product(&first,&second,violation),want);
  }
 }}}}
 let first=m(1,2,vec![raw(0,1);2]);let second=m(3,1,vec![raw(0,1);3]);
 let error=admit_zero_product(&first,&second,HomologicalError::NotCycle).unwrap_err();assert!(matches!(error,HomologicalError::MatrixError(_)));
}
'''

WITNESS = r'''
fn h(tag:u8)->Hash256{Hash256([tag;32])}
fn wire_hash(tag:u8)->serde_json::Value{serde_json::json!(vec![tag;32])}
#[test] fn every_constructor_preserves_distinct_fields_and_wire(){
 let c=ChainComplexWitness::new(h(1),h(2),h(3),5,7,usize::MAX);
 assert_eq!((&c.complex_hash,&c.boundary_1_hash,&c.boundary_2_hash),( &h(1),&h(2),&h(3)));
 assert_eq!((c.c0_dim,c.c1_dim,c.c2_dim),(5,7,usize::MAX));assert_eq!(c.clone(),c);
 let wire=serde_json::to_value(&c).unwrap();assert_eq!(wire["complex_hash"],wire_hash(1));assert_eq!(wire["boundary_1_hash"],wire_hash(2));assert_eq!(wire["boundary_2_hash"],wire_hash(3));
 assert_eq!(wire["c0_dim"],5);assert_eq!(wire["c1_dim"],7);assert_eq!(wire["c2_dim"],serde_json::json!(usize::MAX));assert!(wire["_private"].is_null());
 let co=CochainComplexWitness::new(h(4),h(5),h(6),(7,11),(13,17),h(8));
 assert_eq!((&co.complex_hash,&co.d0_hash,&co.d1_hash,&co.provenance_hash),(&h(4),&h(5),&h(6),&h(8)));
 assert_eq!(co.d0_shape(),(7,11));assert_eq!(co.d1_shape(),(13,17));assert_eq!(co.clone(),co);
 let wire=serde_json::to_value(&co).unwrap();for (key,tag) in [("complex_hash",4),("d0_hash",5),("d1_hash",6),("provenance_hash",8)]{assert_eq!(wire[key],wire_hash(tag));}
 assert_eq!(wire["d0_shape"],serde_json::json!([7,11]));assert_eq!(wire["d1_shape"],serde_json::json!([13,17]));
 let b=BoundaryZeroWitness::new(h(9),usize::MAX,h(10),Some(h(11)));
 let co=CoboundaryZeroWitness::new(h(12),19,h(13),Some(h(14)));
 assert_eq!((&b.complex_hash,b.degree,&b.element_hash,&b.boundary_map_hash),(&h(9),usize::MAX,&h(10),&Some(h(11))));
 assert_eq!((&co.complex_hash,co.degree,&co.element_hash,&co.coboundary_map_hash),(&h(12),19,&h(13),&Some(h(14))));
 let wire=serde_json::to_value(CycleWitness{boundary_zero:b.clone()}).unwrap();assert_eq!(wire["boundary_zero"]["element_hash"],wire_hash(10));assert_eq!(wire["boundary_zero"]["boundary_map_hash"],wire_hash(11));
 let wire=serde_json::to_value(CocycleWitness{coboundary_zero:co.clone()}).unwrap();assert_eq!(wire["coboundary_zero"]["element_hash"],wire_hash(13));assert_eq!(wire["coboundary_zero"]["coboundary_map_hash"],wire_hash(14));
 assert!(BoundaryZeroWitness::new(h(1),0,h(2),None).boundary_map_hash.is_none());assert!(CoboundaryZeroWitness::new(h(1),0,h(2),None).coboundary_map_hash.is_none());
}
#[test] fn result_records_store_annotations_without_proving_them(){
 // Deliberately inconsistent metadata is stored: these are not checkers.
 let h=HomologyWitness{complex_hash:h(1),degree:usize::MAX,ker_dim:0,im_dim:usize::MAX,homology_dim:7};
 let co=CohomologyWitness{complex_hash:Hash256([2;32]),degree:3,ker_dim:1,im_dim:9,cohomology_dim:11};
 assert_eq!((h.ker_dim,h.im_dim,h.homology_dim),(0,usize::MAX,7));assert_eq!((co.ker_dim,co.im_dim,co.cohomology_dim),(1,9,11));
 let w=serde_json::to_value(&h).unwrap();assert_eq!(w["homology_dim"],7);assert_eq!(w["degree"],serde_json::json!(usize::MAX));
 let w=serde_json::to_value(&co).unwrap();assert_eq!(w["cohomology_dim"],11);assert_eq!(w["complex_hash"],wire_hash(2));assert_eq!(h.clone(),h);assert_eq!(co.clone(),co);
}
'''

CARRIER_HELPERS = r'''
use crate::linear_algebra::scalars::q;
fn m(r:usize,c:usize,v:Vec<i64>)->crate::linear_algebra::BasicMatrix<crate::linear_algebra::scalars::Q>{crate::linear_algebra::BasicMatrix::from_row_major(r,c,v.into_iter().map(q).collect()).unwrap()}
fn provenance()->crate::homology::cochain_complex::TheoremProvenance{crate::homology::cochain_complex::TheoremProvenance::new("unchecked source label".into()).unwrap()}
fn admitted(a:i64,b:i64)->__CARRIER__{__CARRIER__::new(1,2,1,m(2,1,vec![a,0]),m(1,2,vec![0,b]),vec![q(2),q(3)],provenance()).unwrap()}
'''
CARRIER = r'''
#[test] fn independent_known_ranks_quotient_dimensions_and_owned_views(){
 for a in [-1,0,1]{for b in [-1,0,1]{let c=admitted(a,b);let ra=usize::from(a!=0);let rb=usize::from(b!=0);
  assert_eq!((c.c0_dim(),c.c1_dim(),c.c2_dim()),(1,2,1));assert_eq!((c.rank_d0(),c.rank_d1()),(ra,rb));assert_eq!(c.dim_q1().unwrap(),2-ra);assert_eq!(c.dim_h1().unwrap(),2-ra-rb);
  assert_eq!(c.d0(),&m(2,1,vec![a,0]));assert_eq!(c.d1(),&m(1,2,vec![0,b]));assert_eq!(c.weights(),&[q(2),q(3)]);assert_eq!(c.complex().d0().matrix(),c.d0());assert_eq!(c.complex().d1().matrix(),c.d1());assert_eq!(c.as_ref(),&c);assert_eq!(c.clone(),c);
  let (x,y)=c.rank_certificates();x.verify_against(c.d0()).unwrap();y.verify_against(c.d1()).unwrap();assert_eq!((x.rank(),y.rank()),(ra,rb));assert!(c.manifest().verifies(&c));
 }}
 let c=Carrier::new(usize::MAX,0,0,m(0,usize::MAX,vec![]),m(0,0,vec![]),vec![],provenance()).unwrap();assert_eq!(c.c0_dim(),usize::MAX);assert_eq!(c.dim_q1().unwrap(),0);assert_eq!(c.dim_h1().unwrap(),0);
}
#[test] fn ordered_scalar_weight_shape_and_law_failures(){
 let raw=crate::linear_algebra::scalars::Q::new_raw(1.into(),0.into());
 assert_eq!(Carrier::new(1,2,1,m(0,0,vec![]),m(0,0,vec![]),vec![raw],provenance()).unwrap_err(),HomologicalError::InvalidRational{index:0});
 assert_eq!(Carrier::new(1,2,1,m(0,0,vec![]),m(0,0,vec![]),vec![q(0)],provenance()).unwrap_err(),HomologicalError::WeightDimensionMismatch{expected:2,got:1});
 for (weights,index) in [(vec![q(0),q(1)],0),(vec![q(1),q(-1)],1)]{assert_eq!(Carrier::new(1,2,1,m(0,0,vec![]),m(0,0,vec![]),weights,provenance()).unwrap_err(),HomologicalError::NonPositiveWeight{index});}
 assert_eq!(Carrier::new(1,2,1,m(0,0,vec![]),m(0,0,vec![]),vec![q(1),q(1)],provenance()).unwrap_err(),HomologicalError::ShapeMismatch{expected:(2,1),got:(0,0)});
 assert_eq!(Carrier::new(1,2,1,m(2,1,vec![1,1]),m(1,2,vec![1,1]),vec![q(1),q(1)],provenance()).unwrap_err(),HomologicalError::CoboundaryLawViolation{degree:0});
}
'''
MANIFEST = r'''
#[test] fn full_manifest_binding_getters_generic_input_and_tampering(){
 assert_eq!(CARRIER_MANIFEST_VERSION,1);assert_eq!(COEFFICIENT_DOMAIN,"Q");assert_eq!(COEFFICIENT_REPRESENTATION,"BigRational");
 for a in [-1,0,1]{for b in [-1,0,1]{let c=admitted(a,b);let r=CarrierManifest::from_carrier(&c);
  assert_eq!(r.version,1);assert_eq!(r.dimensions(),(1,2,1));assert_eq!(r.ranks(),(usize::from(a!=0),usize::from(b!=0)));
  assert_eq!(r.d0_hash(),&hash_matrix(&m(2,1,vec![a,0])));assert_eq!(r.d1_hash(),&hash_matrix(&m(1,2,vec![0,b])));assert_eq!(r.weights_hash,hash_weights(&[q(2),q(3)]));
  assert_eq!(r.carrier_hash(),&hash_carrier_manifest(1,2,1,r.d0_hash(),r.d1_hash(),&r.weights_hash));assert!(r.verifies(&c));assert_eq!(r.clone(),r);
  for field in 0..10 {let mut wrong=r.clone();match field {0=>wrong.version^=1,1=>wrong.carrier_hash.0[0]^=1,2=>wrong.d0_hash.0[0]^=1,3=>wrong.d1_hash.0[0]^=1,4=>wrong.weights_hash.0[0]^=1,5=>wrong.dimensions.0^=1,6=>wrong.dimensions.1^=1,7=>wrong.dimensions.2^=1,8=>wrong.ranks.0^=1,_=>wrong.ranks.1^=1};assert!(!wrong.verifies(&c),"tamper {}",field);}
  let wire=serde_json::to_value(&r).unwrap();assert_eq!(wire["version"],1);assert_eq!(wire["dimensions"],serde_json::json!([1,2,1]));assert_eq!(wire["ranks"],serde_json::json!([usize::from(a!=0),usize::from(b!=0)]));
 }}
 struct Wrapper(crate::homology::carrier::Carrier);impl AsRef<crate::homology::carrier::Carrier> for Wrapper{fn as_ref(&self)->&crate::homology::carrier::Carrier{&self.0}}
 let w=Wrapper(admitted(1,0));assert_eq!(CarrierManifest::from_carrier(&w),CarrierManifest::from_carrier(&w.0));
 assert!(!CarrierManifest::from_carrier(&admitted(1,0)).verifies(&admitted(0,1)));
}
'''


def challenge(subject):
    name = Path(subject['path']).stem
    bodies = {'exact_scalar':SCALAR, 'witness':WITNESS,
              'carrier':CARRIER_HELPERS.replace('__CARRIER__','Carrier')+CARRIER,
              'carrier_manifest':CARRIER_HELPERS.replace('__CARRIER__','crate::homology::carrier::Carrier')+MANIFEST}
    return '\n#[cfg(test)] mod independent_storage_admission { use super::*;\n'+bodies[name]+'\n}\n'
