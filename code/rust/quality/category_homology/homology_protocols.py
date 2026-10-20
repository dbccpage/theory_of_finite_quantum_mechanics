"""Typed identifier and diagnostic wire protocols. AuthorityEffect: None.

Specifications are explicit boundary tables, widened integer oracles and
nominal source-chain checks; no mathematical algorithm grade is inherited.
"""
from pathlib import Path as _FilesystemPath
import sys as _contract_sys
_contract_sys.path.insert(0, str(_FilesystemPath(__file__).resolve().parents[4] / "scripts"))
from contract_scores import RecordPath as Path, copy_file as _copy_record_file

KINDS = ('ChainId','CochainId','CycleId','CocycleId','BoundaryId','CoboundaryId',
         'ChainComplexId','CochainComplexId','HomologyClassId','CohomologyClassId',
         'CarrierId','MatrixId','ManifestId','WitnessId')

ID_TESTS = r'''
#[test] fn every_nominal_numeric_wire() {
 macro_rules! kind {($t:ident,$name:literal)=>{{
  for n in [1,2,255,256,u32::MAX as u64,(u32::MAX as u64)+1,u64::MAX-1,u64::MAX] {
   let x=$t::new(n).unwrap();assert_eq!(x.clone().get(),n);assert_eq!(u64::from(x.clone()),n);assert_eq!($t::try_from(n).unwrap(),x);
   assert_eq!(x.to_string(),format!("{}({})",$name,n));assert_eq!(serde_json::to_string(&x).unwrap(),n.to_string());
   assert_eq!(serde_json::from_str::<$t>(&n.to_string()).unwrap(),x);
   use std::hash::{Hash,Hasher};let mut a=std::collections::hash_map::DefaultHasher::new();let mut b=std::collections::hash_map::DefaultHasher::new();x.hash(&mut a);x.clone().hash(&mut b);assert_eq!(a.finish(),b.finish());
  }
  assert_eq!($t::new(0),Err(IdError::ZeroId));assert_eq!($t::try_from(0),Err(IdError::ZeroId));
  for raw in ["0","-1","1.5","18446744073709551616","\"1\"","null","{}","true"] {assert!(serde_json::from_str::<$t>(raw).is_err(),"{} {}",$name,raw);}
 }}}
 __KINDS__
}
#[test] fn basis_admission_and_literal_storage() {
 for (text,ok) in [("",false),(" \t\n",false),("\u{2003}",false),(" basis ",true),("λ\0()",true)] {
  let result=BasisId::new(text);
  if ok {let x=result.unwrap();assert_eq!(x.as_str(),text);assert_eq!(x.to_string(),format!("BasisId({})",text));assert_eq!(String::from(x.clone()),text);assert_eq!(BasisId::try_from(text.to_string()).unwrap(),x);let wire=serde_json::to_string(text).unwrap();assert_eq!(serde_json::to_string(&x).unwrap(),wire);assert_eq!(serde_json::from_str::<BasisId>(&wire).unwrap(),x);}
  else {assert_eq!(result,Err(IdError::EmptyBasis));assert_eq!(BasisId::try_new(text),Err(IdError::EmptyBasis));assert!(serde_json::from_str::<BasisId>(&serde_json::to_string(text).unwrap()).is_err());}
 }
 for wire in ["0","null","[]","{}","true"] {assert!(serde_json::from_str::<BasisId>(wire).is_err());}
}
#[test] fn degree_widened_oracle() {
 for n in (i16::MIN as i32..=i16::MAX as i32).chain([i32::MIN,i32::MIN+1,i32::MAX-1,i32::MAX]) {
  let x=Degree::new(n);assert_eq!(x.value(),n);assert_eq!(x.to_string(),format!("deg({})",n));
  let pred=(n as i64)-1;let succ=(n as i64)+1;
  let expected_pred=if pred<i32::MIN as i64 {Err(IdError::DegreeOverflow)} else {Ok(Degree(pred as i32))};
  let expected_succ=if succ>i32::MAX as i64 {Err(IdError::DegreeOverflow)} else {Ok(Degree(succ as i32))};
  assert_eq!(x.checked_pred(),expected_pred);assert_eq!(x.checked_succ(),expected_succ);
  assert_eq!(boundary_lowers_degree_by_one(x),if n==i32::MIN{Err(IdError::DegreeOverflow)}else{Ok(())});
  assert_eq!(serde_json::to_string(&x).unwrap(),n.to_string());assert_eq!(serde_json::from_str::<Degree>(&n.to_string()).unwrap(),x);
  if n<i32::MAX {assert!(x<Degree(n+1));}
 }
 for raw in ["2147483648","-2147483649","1.5","null","\"0\"","{}"] {assert!(serde_json::from_str::<Degree>(raw).is_err());}
}
#[test] fn display_parser_and_kind_check() {
 for n in [0,1,2,u64::MAX] {assert_eq!(identifier_kinds_round_trip(n),if n==0{Err(IdError::ZeroId)}else{Ok(())});}
 for (text,expected) in [("ChainId(1)",Ok(1)),("ChainId(+1)",Ok(1)),("ChainId(0002)",Ok(2)),("ChainId(18446744073709551615)",Ok(u64::MAX)),("ChainId(0)",Err(IdError::ZeroId)),("ChainId(-1)",Err(IdError::ZeroId)),("ChainId(18446744073709551616)",Err(IdError::ZeroId)),("ChainId(x)",Err(IdError::ZeroId)),("ChainId()",Err(IdError::ZeroId)),("ChainId( 1)",Err(IdError::ZeroId)),("Other(1)",Err(IdError::EmptyBasis)),("ChainId1)",Err(IdError::EmptyBasis)),("ChainId(1",Err(IdError::EmptyBasis)),("ChainId((1))",Err(IdError::ZeroId)),("ChainId(1)x",Err(IdError::EmptyBasis))] {assert_eq!(parse_parenthesized(text,"ChainId"),expected,"{}",text);}
 assert_eq!(IdError::ZeroId.to_string(),"zero identifier");assert_eq!(IdError::EmptyBasis.to_string(),"empty basis identifier");assert_eq!(IdError::DegreeOverflow.to_string(),"degree overflow");
}
'''.replace('__KINDS__','\n'.join(f'kind!({kind},"{kind}");' for kind in KINDS))

# Independent public diagnostic contract: constructor expression, exact message.
ERROR_ROWS = [
('InvalidRational{index:7}','noncanonical or undefined rational at coefficient 7'),
('CertificateMismatch{identity:"L*R"}','certificate identity failed: L*R'),
('ShapeMismatch{expected:(2,3),got:(5,7)}','matrix shape mismatch: expected (2, 3), got (5, 7)'),
('DegreeMismatch{expected:-2,got:7}','degree mismatch: expected -2, got 7'),
('DegreeOverflow','degree shift overflows its representation'),
('ResourceLimit("budget")','resource limit exceeded: budget'),
('DimensionMismatch{expected:3,got:7}','dimension mismatch: expected 3, got 7'),
('BoundaryLawViolation{degree:-2}','boundary law violated: d_(k) * d_(k+1) != 0 at degree -2'),
('CoboundaryLawViolation{degree:7}','coboundary law violated: d^(k+1) * d^(k) != 0 at degree 7'),
('InvalidDegree(-2)','invalid degree: -2'),
('NonExactDivision','non-exact division encountered'),
('BasisMismatch{description:"literal λ".into()}','basis mismatch: literal λ'),
('NotCycle','element is not a cycle: boundary is non-zero'),
('NotCocycle','element is not a cocycle: coboundary is non-zero'),
('NotBoundary','element is not a boundary'),
('NotCoboundary','element is not a coboundary'),
('HomologyDimensionUnderflow{ker_dim:2,im_dim:7}','homology dimension underflow: ker_dim=2, im_dim=7'),
('EmptyBasis','empty basis'),
('InvalidManifest{reason:"literal λ".into()}','invalid manifest: literal λ'),
('HashMismatch{expected:"abc".into(),got:"def".into()}','hash mismatch: expected abc, got def'),
('MissingWitness','missing witness'),
('BettiRankInconsistency{dimension:2,rank_sum:7,degree:3}','Betti rank inconsistency at degree 3: rank sum 7 exceeds dimension 2'),
('NonIntegralBoundaryMap{map:"d1",row:2,col:7}',"boundary map d1 is not integral in the carrier's coordinate lattice: non-integer entry at row 2, column 7"),
('UnsupportedOperation("literal λ".into())','unsupported operation: literal λ'),
('NonPositiveWeight{index:7}','non-positive weight at index 7'),
('WeightDimensionMismatch{expected:2,got:7}','weight dimension mismatch: expected 2, got 7'),
('EmptyVerificationSource','empty verification source'),
('EdgeSourceOutOfRange{edge:2,src:7}','edge source out of range: edge 2, source 7'),
('EdgeTargetOutOfRange{edge:2,tgt:7}','edge target out of range: edge 2, target 7'),
('SelfLoopNotAllowed{node:7}','self-loop not allowed: node 7'),
('TriangleVertexOutOfRange{triangle:2,vertex:7}','triangle vertex out of range: triangle 2, vertex 7'),
('TriangleMissingEdge{triangle:2,src:3,tgt:7}','triangle missing required edge: triangle 2, edge (3, 7)'),
('SerializationError("literal λ".into())','serialization error: literal λ'),
]

ERROR_TESTS = r'''
#[test] fn complete_diagnostic_table_and_sources() {
 use std::error::Error;
 let entries:Vec<(HomologicalError,&str)>=vec![__ERRORS__];
 for (error,message) in entries {assert_eq!(error.to_string(),message);assert_eq!(error.clone(),error);assert!(error.source().is_none(),"{}",message);}
 let inner=MatrixError::InvalidOperation("sentinel λ".into());let outer:HomologicalError=inner.clone().into();
 assert_eq!(outer,HomologicalError::MatrixError(inner.clone()));assert_eq!(outer.to_string(),format!("matrix error: {}",inner));assert_eq!(outer.source().unwrap().downcast_ref::<MatrixError>(),Some(&inner));
 let reduction=crate::linear_algebra::image_kernel::ExactLinearAlgebraError::DimensionMismatch{expected:3,got:7};
 let outer=HomologicalError::RankReductionFailed{source:reduction.clone()};assert_eq!(outer.to_string(),"rank factorization row reduction failed");assert_eq!(outer.source().unwrap().downcast_ref::<crate::linear_algebra::image_kernel::ExactLinearAlgebraError>(),Some(&reduction));assert_eq!(outer.clone(),outer);
 let inverse=crate::linear_algebra::ExactFieldError::Singular{rank:2,size:3};
 let outer=HomologicalError::RankInverseFailed{source:inverse.clone()};assert_eq!(outer.to_string(),"rank factorization inverse failed");assert_eq!(outer.source().unwrap().downcast_ref::<crate::linear_algebra::ExactFieldError>(),Some(&inverse));assert_eq!(outer.clone(),outer);
 for source in [SmithError::Overflow,SmithError::VerificationFailed,SmithError::DivisibilityViolation{left:2.into(),right:3.into()}] {
  let outer=HomologicalError::SmithNormalFormFailed{map:"d1",source:source.clone()};assert_eq!(outer.to_string(),"Smith normal form of boundary map d1 failed");assert_eq!(outer.source().unwrap().downcast_ref::<SmithError>(),Some(&source));assert_eq!(outer.clone(),outer);
 }
}
#[test] fn extreme_payload_and_formatter_refusal() {
 use std::fmt::Write;
 let degree=HomologicalError::DegreeMismatch{expected:i32::MIN,got:i32::MAX};assert_eq!(degree.to_string(),"degree mismatch: expected -2147483648, got 2147483647");
 let dimensions=HomologicalError::DimensionMismatch{expected:usize::MAX,got:0};assert_eq!(dimensions.to_string(),format!("dimension mismatch: expected {}, got 0",usize::MAX));
 struct Refuse;impl std::fmt::Write for Refuse{fn write_str(&mut self,_:&str)->std::fmt::Result{Err(std::fmt::Error)}}
 assert!(write!(&mut Refuse,"{}",degree).is_err());
}
'''


def challenge(subject):
    import json
    body = ID_TESTS if Path(subject['path']).stem == 'ids' else ERROR_TESTS.replace(
        '__ERRORS__',','.join('(HomologicalError::'+value+','+json.dumps(message,ensure_ascii=False)+')'
                            for value,message in ERROR_ROWS))
    return '\n#[cfg(test)] mod independent_protocol_tests {use super::*;\n'+body+'\n}\n'


def variants(subject, source):
    for index,(needle,replacement) in enumerate(subject['faults']):
        if source.count(needle) != 1:
            raise ValueError('Ambiguous fault: '+subject['path']+' '+needle)
        yield str(index),source.replace(needle,replacement,1),needle,replacement
