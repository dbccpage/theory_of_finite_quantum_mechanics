"""Native facade/wire and independent directed-incidence cases.

AuthorityEffect: None. Known axis ranks, widened integer incidence entries,
component partitions and independently framed legacy bytes are the oracles.
"""
from pathlib import Path

COMMON = r'''
use crate::linear_algebra::scalars::q;
use crate::linear_algebra::BasicMatrix;
use crate::homology::carrier_manifest::CarrierManifest;
fn m(r:usize,c:usize,v:Vec<i64>)->BasicMatrix<Q>{BasicMatrix::from_row_major(r,c,v.into_iter().map(q).collect()).unwrap()}
fn admitted(a:i64,b:i64)->Carrier{Carrier::new(1,2,1,__D0__,__D1__,vec![q(2),q(3)]).unwrap()}
#[test] fn independent_axis_ranks_views_and_admission(){
 for a in [-1i64,0,1]{for b in [-1i64,0,1]{let c=admitted(a,b);assert_eq!((c.c0_dim(),c.c1_dim(),c.c2_dim()),(1,2,1));assert_eq!((c.rank_d0(),c.rank_d1()),(usize::from(a!=0),usize::from(b!=0)));assert_eq!(c.dim_q1(),2-usize::from(a!=0));assert_eq!(__H1__,2-usize::from(a!=0)-usize::from(b!=0));assert_eq!(c.d0(),&m(2,1,vec![a,0]));assert_eq!(c.d1(),&m(1,2,vec![0,b]));assert_eq!(c.weights(),&[q(2),q(3)]);assert_eq!(c.as_ref().d0(),c.d0());assert_eq!(c.as_ref().d1(),c.d1());assert_eq!(c.clone(),c);assert!(CarrierManifest::from_carrier(&c).verifies(c.as_ref()));}}
 let raw=Q::new_raw(1.into(),0.into());assert_eq!(Carrier::new(1,2,1,__BAD0__,__BAD1__,vec![raw],).unwrap_err(),__ERR__::InvalidRational{index:0});
 assert_eq!(Carrier::new(1,2,1,__BAD0__,__BAD1__,vec![q(0)]).unwrap_err(),__ERR__::WeightDimensionMismatch{expected:2,got:1});
 assert_eq!(Carrier::new(1,2,1,__BAD0__,__BAD1__,vec![q(0),q(1)]).unwrap_err(),__ERR__::NonPositiveWeight{index:0});
 let c=Carrier::new(usize::MAX,0,0,__EMPTY0__,__EMPTY1__,vec![]).unwrap();assert_eq!(c.c0_dim(),usize::MAX);assert_eq!(c.dim_q1(),0);assert_eq!(__H1__,0);
}
'''

GRAPH = r'''
fn component_count(n:usize,edges:&[(usize,usize)])->usize{let mut labels=(0..n).collect::<Vec<_>>();for &(a,b) in edges{let from=labels[b];let to=labels[a];for label in &mut labels{if *label==from{*label=to;}}}labels.into_iter().collect::<std::collections::BTreeSet<_>>().len()}
#[test] fn all_three_vertex_directed_graphs_and_each_triangle_orientation(){
 let possible=[(0,1),(0,2),(1,0),(1,2),(2,0),(2,1)];let ordered=[(0,1,2),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0)];
 for bits in 0..64usize{let edges=possible.iter().enumerate().filter(|(i,_)|bits&(1<<i)!=0).map(|(_,edge)|*edge).collect::<Vec<_>>();let components=component_count(3,&edges);
  let mut families=vec![vec![]];for &(a,b,c) in &ordered{if edges.contains(&(a,b))&&edges.contains(&(b,c))&&edges.contains(&(a,c)){families.push(vec![(a,b,c)]);families.push(vec![(a,b,c);2]);}}
  for triangles in families{let c=graph_carrier(3,&edges,&triangles,vec![q(1);edges.len()]).unwrap();let upper_rank=usize::from(!triangles.is_empty());
   assert_eq!((c.c0_dim(),c.c1_dim(),c.c2_dim()),(3,edges.len(),triangles.len()));assert_eq!(c.rank_d0(),3-components);assert_eq!(c.rank_d1(),upper_rank);assert_eq!(c.dim_h1(),edges.len()+components-3-upper_rank);
   for (row,&(src,tgt)) in edges.iter().enumerate(){for vertex in 0..3{let expected=i64::from(vertex==tgt)-i64::from(vertex==src);assert_eq!(c.d0().get(row,vertex).unwrap(),q(expected));}}
   for (row,&(a,b,t)) in triangles.iter().enumerate(){for (col,&edge) in edges.iter().enumerate(){let expected=i64::from(edge==(a,b))+i64::from(edge==(b,t))-i64::from(edge==(a,t));assert_eq!(c.d1().get(row,col).unwrap(),q(expected));}}
  }
 }
}
#[test] fn exact_incidence_refusal_priority_and_payloads(){
 assert_eq!(graph_carrier(0,&[(0,0)],&[],vec![Q::new_raw(1.into(),0.into())]).unwrap_err(),CarrierError::EdgeSourceOutOfRange{edge:0,src:0});
 assert_eq!(graph_carrier(3,&[(usize::MAX,0)],&[],vec![q(1)]).unwrap_err(),CarrierError::EdgeSourceOutOfRange{edge:0,src:usize::MAX});
 assert_eq!(graph_carrier(3,&[(0,usize::MAX)],&[],vec![q(1)]).unwrap_err(),CarrierError::EdgeTargetOutOfRange{edge:0,tgt:usize::MAX});
 assert_eq!(graph_carrier(3,&[(0,3)],&[],vec![q(1)]).unwrap_err(),CarrierError::EdgeTargetOutOfRange{edge:0,tgt:3});
 assert_eq!(graph_carrier(3,&[(1,1)],&[],vec![q(1)]).unwrap_err(),CarrierError::SelfLoopNotAllowed{node:1});
 assert_eq!(graph_carrier(3,&[(0,1),(0,1)],&[],vec![q(1);2]).unwrap_err(),CarrierError::BasisMismatch{description:"parallel directed edges".into()});
 assert_eq!(graph_carrier(3,&[],&[(0,1,usize::MAX)],vec![]).unwrap_err(),CarrierError::TriangleVertexOutOfRange{triangle:0,vertex:usize::MAX});
 assert_eq!(graph_carrier(3,&[],&[(0,1,3)],vec![]).unwrap_err(),CarrierError::TriangleVertexOutOfRange{triangle:0,vertex:3});
 assert_eq!(graph_carrier(3,&[],&[(0,0,1)],vec![]).unwrap_err(),CarrierError::BasisMismatch{description:"triangle vertices must be distinct".into()});
 for (edges,src,tgt) in [(vec![],0,1),(vec![(0,1)],1,2),(vec![(0,1),(1,2)],0,2)]{assert_eq!(graph_carrier(3,&edges,&[(0,1,2)],vec![q(1);edges.len()]).unwrap_err(),CarrierError::TriangleMissingEdge{triangle:0,src,tgt});}
 assert_eq!(graph_carrier(2,&[(0,1)],&[],vec![]).unwrap_err(),CarrierError::WeightDimensionMismatch{expected:1,got:0});
 let c=graph_carrier(usize::MAX,&[],&[],vec![]).unwrap();assert_eq!(c.c0_dim(),usize::MAX);assert_eq!(c.dim_h1(),0);
 assert!(matches!(graph_carrier(usize::MAX,&[(0,1)],&[],vec![q(1)]),Err(CarrierError::MatrixError(_))));
}
'''

ROOT = r'''
#[test] fn unequal_outer_dimensions_preserve_each_wire_field(){
 let c=Carrier::new(2,0,3,ExactMatrix(m(0,2,vec![])),ExactMatrix(m(3,0,vec![])),vec![]).unwrap();
 let owned=CarrierWire{c0_dim:2,c1_dim:0,c2_dim:3,d0:ExactMatrix(m(0,2,vec![])),d1:ExactMatrix(m(3,0,vec![])),weights:vec![],d0_hash:legacy_bytes(0,2,&[]),d1_hash:legacy_bytes(3,0,&[])};
 assert_eq!(serde_json::to_string(&c).unwrap(),serde_json::to_string(&owned).unwrap());
 assert_eq!(serde_json::from_str::<Carrier>(&serde_json::to_string(&c).unwrap()).unwrap(),c);
}
fn gcd(mut a:i128,mut b:i128)->i128{a=a.abs();b=b.abs();while b!=0{let r=a%b;a=b;b=r;}a}
fn legacy_bytes(rows:usize,cols:usize,pairs:&[(i64,i64)])->Hash256{
 let mut bytes=b"TheoryOfFiniteQM.ExactMatrix<Q>.v1".to_vec();bytes.extend((rows as u64).to_le_bytes());bytes.extend((cols as u64).to_le_bytes());
 for &(n,d) in pairs{let (n,d)=if d==0{(n as i128,0)}else{let g=gcd(n as i128,d as i128);let sign=if d<0{-1}else{1};((n as i128)/g*sign,(d as i128)/g*sign)};for value in [n,d]{let digits=num_bigint::BigInt::from(value).to_signed_bytes_le();bytes.extend((digits.len() as u64).to_le_bytes());bytes.extend(digits);}}
 Hash256(*blake3::hash(&bytes).as_bytes())
}
#[test] fn raw_legacy_fingerprints_and_borrowed_wire_match_owned_protocol(){
 for n in -4..=4{for d in -4..=4{let pairs=[(n,d),(1,2)];let values=pairs.iter().map(|(n,d)|Q::new_raw((*n).into(),(*d).into())).collect();let matrix=ExactMatrix(BasicMatrix::from_row_major(1,2,values).unwrap());assert_eq!(hash_exact_matrix(&matrix),legacy_bytes(1,2,&pairs));}}
 for a in [-1i64,0,1]{for b in [-1i64,0,1]{let c=admitted(a,b);let owned=CarrierWire{c0_dim:1,c1_dim:2,c2_dim:1,d0:ExactMatrix(m(2,1,vec![a,0])),d1:ExactMatrix(m(1,2,vec![0,b])),weights:vec![q(2),q(3)],d0_hash:legacy_bytes(2,1,&[(a,1),(0,1)]),d1_hash:legacy_bytes(1,2,&[(0,1),(b,1)])};
  assert_eq!(serde_json::to_string(&c).unwrap(),serde_json::to_string(&owned).unwrap());assert_eq!(c.serialize(Probe).unwrap(),owned.serialize(Probe).unwrap());
  assert_eq!(c.serialize(Probe).unwrap(),vec!["struct:CarrierWire","c0_dim:u64","c1_dim:u64","c2_dim:u64","d0:newtype:ExactMatrix","d1:newtype:ExactMatrix","weights:seq","d0_hash:newtype:Hash256","d1_hash:newtype:Hash256"]);
  let wire=serde_json::to_value(&c).unwrap();assert_eq!(serde_json::from_value::<Carrier>(wire.clone()).unwrap(),c);let mut positive=wire.clone();positive["weights"]=serde_json::to_value(vec![q(5),q(7)]).unwrap();assert_eq!(serde_json::from_value::<Carrier>(positive).unwrap().weights(),&[q(5),q(7)]);
  for field in ["d0_hash","d1_hash"]{let mut wrong=wire.clone();let mut h=if field=="d0_hash"{owned.d0_hash.clone()}else{owned.d1_hash.clone()};h.0[0]^=1;wrong[field]=serde_json::to_value(h).unwrap();assert!(serde_json::from_value::<Carrier>(wrong).is_err());}
  let mut bad=wire.clone();bad["weights"]=serde_json::to_value(vec![q(0),q(3)]).unwrap();assert!(serde_json::from_value::<Carrier>(bad).is_err());let mut wrong=wire.clone();wrong["c1_dim"]=serde_json::json!(3);assert!(serde_json::from_value::<Carrier>(wrong).is_err());let mut extra=wire;extra["rank_d0"]=serde_json::json!(999);assert!(serde_json::from_value::<Carrier>(extra).is_err());
  for budget in [0,1,32]{assert!(serde_json::to_writer(FailWriter(budget),&c).is_err());}
 }}
 let expected=Hash256([0;32]);let got=Hash256([1;32]);assert_eq!(verify_hash(&expected,&got),Err(HomologicalError::HashMismatch{expected:"00".repeat(32),got:"01".repeat(32)}));assert_eq!(verify_hash(&expected,&expected),Ok(()));
 let bad=CarrierWire{c0_dim:1,c1_dim:1,c2_dim:0,d0:ExactMatrix(m(1,1,vec![1])),d1:ExactMatrix(m(0,1,vec![])),weights:vec![q(0)],d0_hash:Hash256([0;32]),d1_hash:Hash256([0;32])};assert!(matches!(Carrier::try_from(bad),Err(HomologicalError::HashMismatch{..})));
}
struct FailWriter(usize);impl std::io::Write for FailWriter{fn write(&mut self,bytes:&[u8])->std::io::Result<usize>{if self.0==0{return Err(std::io::Error::other("fixture writer full"));}let n=self.0.min(bytes.len());self.0-=n;Ok(n)}fn flush(&mut self)->std::io::Result<()>{Ok(())}}
// Observe the Serde envelope independently of JSON's ignored type names.
struct Probe;struct ProbeStruct(Vec<String>);struct ProbeSeq;
type ProbeError=serde_json::Error;fn unsupported()->ProbeError{<ProbeError as serde::ser::Error>::custom("unsupported fixture token")}
impl serde::ser::SerializeStruct for ProbeStruct{type Ok=Vec<String>;type Error=ProbeError;fn serialize_field<T:serde::Serialize+?Sized>(&mut self,key:&'static str,value:&T)->Result<(),Self::Error>{let token=value.serialize(Probe)?.join("|");self.0.push(format!("{}:{}",key,token));Ok(())}fn end(self)->Result<Self::Ok,Self::Error>{Ok(self.0)}}
impl serde::ser::SerializeSeq for ProbeSeq{type Ok=Vec<String>;type Error=ProbeError;fn serialize_element<T:serde::Serialize+?Sized>(&mut self,_:&T)->Result<(),Self::Error>{Ok(())}fn end(self)->Result<Self::Ok,Self::Error>{Ok(vec!["seq".into()])}}
macro_rules! unsupported_primitive {($($name:ident($ty:ty)),* $(,)?)=>{$(fn $name(self,_:$ty)->Result<Self::Ok,Self::Error>{Err(unsupported())})*};}
impl serde::Serializer for Probe{
 type Ok=Vec<String>;type Error=ProbeError;type SerializeSeq=ProbeSeq;type SerializeTuple=serde::ser::Impossible<Self::Ok,Self::Error>;type SerializeTupleStruct=serde::ser::Impossible<Self::Ok,Self::Error>;type SerializeTupleVariant=serde::ser::Impossible<Self::Ok,Self::Error>;type SerializeMap=serde::ser::Impossible<Self::Ok,Self::Error>;type SerializeStruct=ProbeStruct;type SerializeStructVariant=serde::ser::Impossible<Self::Ok,Self::Error>;
 unsupported_primitive!(serialize_bool(bool),serialize_i8(i8),serialize_i16(i16),serialize_i32(i32),serialize_i64(i64),serialize_i128(i128),serialize_u8(u8),serialize_u16(u16),serialize_u32(u32),serialize_u128(u128),serialize_f32(f32),serialize_f64(f64),serialize_char(char),serialize_str(&str),serialize_bytes(&[u8]));
 fn serialize_u64(self,_:u64)->Result<Self::Ok,Self::Error>{Ok(vec!["u64".into()])}
 fn serialize_newtype_struct<T:serde::Serialize+?Sized>(self,name:&'static str,_:&T)->Result<Self::Ok,Self::Error>{Ok(vec![format!("newtype:{}",name)])}
 fn serialize_struct(self,name:&'static str,_:usize)->Result<Self::SerializeStruct,Self::Error>{Ok(ProbeStruct(vec![format!("struct:{}",name)]))}
 fn serialize_seq(self,_:Option<usize>)->Result<Self::SerializeSeq,Self::Error>{Ok(ProbeSeq)}
 fn serialize_none(self)->Result<Self::Ok,Self::Error>{Err(unsupported())}fn serialize_unit(self)->Result<Self::Ok,Self::Error>{Err(unsupported())}fn serialize_unit_struct(self,_:&'static str)->Result<Self::Ok,Self::Error>{Err(unsupported())}
 fn serialize_some<T:serde::Serialize+?Sized>(self,_:&T)->Result<Self::Ok,Self::Error>{Err(unsupported())}fn serialize_unit_variant(self,_:&'static str,_:u32,_:&'static str)->Result<Self::Ok,Self::Error>{Err(unsupported())}
 fn serialize_newtype_variant<T:serde::Serialize+?Sized>(self,_:&'static str,_:u32,_:&'static str,_:&T)->Result<Self::Ok,Self::Error>{Err(unsupported())}fn serialize_tuple(self,_:usize)->Result<Self::SerializeTuple,Self::Error>{Err(unsupported())}
 fn serialize_tuple_struct(self,_:&'static str,_:usize)->Result<Self::SerializeTupleStruct,Self::Error>{Err(unsupported())}fn serialize_tuple_variant(self,_:&'static str,_:u32,_:&'static str,_:usize)->Result<Self::SerializeTupleVariant,Self::Error>{Err(unsupported())}
 fn serialize_map(self,_:Option<usize>)->Result<Self::SerializeMap,Self::Error>{Err(unsupported())}fn serialize_struct_variant(self,_:&'static str,_:u32,_:&'static str,_:usize)->Result<Self::SerializeStructVariant,Self::Error>{Err(unsupported())}
}
'''


def challenge(subject):
    root=Path(subject['path']).name=='mod.rs'
    body=COMMON
    pairs={'__D0__':'ExactMatrix(m(2,1,vec![a,0]))' if root else 'm(2,1,vec![a,0])',
           '__D1__':'ExactMatrix(m(1,2,vec![0,b]))' if root else 'm(1,2,vec![0,b])',
           '__BAD0__':'ExactMatrix(m(0,0,vec![]))' if root else 'm(0,0,vec![])',
           '__BAD1__':'ExactMatrix(m(0,0,vec![]))' if root else 'm(0,0,vec![])',
           '__EMPTY0__':'ExactMatrix(m(0,usize::MAX,vec![]))' if root else 'm(0,usize::MAX,vec![])',
           '__EMPTY1__':'ExactMatrix(m(0,0,vec![]))' if root else 'm(0,0,vec![])',
           '__ERR__':'HomologicalError' if root else 'CarrierError',
           '__H1__':'c.dim_h1().unwrap()' if root else 'c.dim_h1()'}
    for needle,value in pairs.items():body=body.replace(needle,value)
    return '\n#[cfg(test)] mod independent_carrier_facades { use super::*;\n'+body+(ROOT if root else GRAPH)+'\n}\n'
