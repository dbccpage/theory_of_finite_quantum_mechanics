"""Native index-repair, finite-complex and simplicial boundary specifications.

AuthorityEffect: None. Tests use actual peers; no method adapters or replacement
providers. Mathematical oracles use integer dot products, subset bit masks,
graph connectivity and cycle parity rather than production matrix/rank code.
"""
import json
from pathlib import Path
from homology_protocols import ERROR_ROWS, ERROR_TESTS

INDEX_TESTS = r'''
fn assert_index(error: &HomologicalError, index: usize) {
 match error {
  HomologicalError::InvalidDegree(value) => {assert!(index <= i32::MAX as usize);assert_eq!(*value as i128,index as i128);},
  HomologicalError::InvalidDegreeIndex(value) => {assert!(index > i32::MAX as usize);assert_eq!(*value,index);},
  other=>panic!("wrong index error: {:?}",other),
 }
 assert_eq!(error.to_string(),format!("invalid degree: {}",index));
}
'''

ERROR_EXTRA = r'''
#[test] fn exact_index_refusal_protocol() {
 for index in [0,1,2,3,i32::MAX as usize,(i32::MAX as usize)+1,u32::MAX as usize,usize::MAX].into_iter().chain(usize::try_from(4294967296u64)) {
  assert_index(&HomologicalError::invalid_degree_index(index),index);
  let raw=HomologicalError::InvalidDegreeIndex(index);assert_eq!(raw.to_string(),format!("invalid degree: {}",index));
  assert_eq!(raw.clone(),raw);assert!(std::error::Error::source(&raw).is_none());
 }
}
'''

COMPLEX_TESTS = r'''
fn matrix(rows:usize,cols:usize,values:Vec<i64>)->BasicMatrix<Q>{BasicMatrix::from_row_major(rows,cols,values.into_iter().map(crate::linear_algebra::scalars::q).collect()).unwrap()}
#[test] fn independent_dot_product_and_owned_context() {
 for a in [-1,0,1] {for b in [-1,0,1] {for c in [-1,0,1] {for d in [-1,0,1] {
  let left=matrix(1,2,vec![a,b]);let right=matrix(2,1,vec![c,d]);let expected=(a as i128)*(c as i128)+(b as i128)*(d as i128)==0;
  let result=__BUILD__;
  if expected {let x=result.unwrap();assert_eq!(x.dim(0).unwrap(),__DIM0__);assert_eq!(x.dim(1).unwrap(),__DIM1__);assert_eq!(x.dim(2).unwrap(),__DIM2__);__OBSERVERS__
   for index in [3,i32::MAX as usize,(i32::MAX as usize)+1,u32::MAX as usize,usize::MAX].into_iter().chain(usize::try_from(4294967296u64)) {assert_index(&x.dim(index).unwrap_err(),index);}
  } else {assert_eq!(result.unwrap_err(),__LAW_ERROR__);}
 }}}}
}
#[test] fn shape_and_rational_failure_order() {
 let good_left=matrix(1,2,vec![0,0]);let good_right=matrix(2,1,vec![0,0]);
 let bad_left=matrix(2,2,vec![0,0,0,0]);let bad_right=matrix(3,1,vec![0,0,0]);
 assert_eq!(__BAD_FIRST__.unwrap_err(),HomologicalError::ShapeMismatch{expected:__FIRST_SHAPE__,got:__BAD_FIRST_SHAPE__});
 assert_eq!(__BAD_SECOND__.unwrap_err(),HomologicalError::ShapeMismatch{expected:__SECOND_SHAPE__,got:__BAD_SECOND_SHAPE__});
 let invalid=BasicMatrix::from_row_major(__FIRST_ROWS__,__FIRST_COLS__,vec![Q::new_raw(1.into(),0.into()),Q::from_integer(0.into())]).unwrap();
 assert_eq!(__BAD_RATIONAL__.unwrap_err(),HomologicalError::InvalidRational{index:0});
}
#[test] fn zero_area_dimensions_and_full_index() {
 for (a,b,c) in [(0,0,0),(3,0,0),(0,0,5),(2,3,4)] {
  let x=__ZERO_BUILD__.unwrap();for (index,want) in [a,b,c].into_iter().enumerate(){assert_eq!(x.dim(index).unwrap(),want);}
  assert_index(&x.dim(usize::MAX).unwrap_err(),usize::MAX);
 }
}
'''

PROVENANCE = r'''
#[test] fn provenance_is_checked_label_only() {
 for (label,valid) in [("",false),(" \n\t",false),("\u{2003}",false),(" unverified claim ",true),("λ\0",true)] {
  let result=TheoremProvenance::new(label.into());let wire=serde_json::to_string(label).unwrap();
  if valid {let p=result.unwrap();assert_eq!(p.verification_source(),label);assert_eq!(p.provenance_hash(),hash_provenance(label));assert_eq!(String::from(p.clone()),label);assert_eq!(TheoremProvenance::try_from(label.to_string()).unwrap(),p);assert_eq!(serde_json::from_str::<TheoremProvenance>(&wire).unwrap(),p);assert_eq!(serde_json::to_string(&p).unwrap(),wire);}
  else {assert_eq!(result.unwrap_err(),HomologicalError::EmptyVerificationSource);assert!(serde_json::from_str::<TheoremProvenance>(&wire).is_err());}
 }
}
'''

SIMPLICIAL = r'''
#[test] fn full_index_and_wire_admission() {
 let s=Simplex::new(vec![1,3,8]).unwrap();for index in [3,i32::MAX as usize,(i32::MAX as usize)+1,u32::MAX as usize,usize::MAX].into_iter().chain(usize::try_from(4294967296u64)) {assert_index(&s.face(index).unwrap_err(),index);}
 assert_eq!(Simplex::new(vec![1]).unwrap().face(0).unwrap_err(),HomologicalError::InvalidDegree(0));
 assert!(Simplex::new(vec![]).is_err());assert!(Simplex::new(vec![1,1]).is_err());assert!(Simplex::new(vec![2,1]).is_err());
 for wire in [r#"{"vertices":[]}"#,r#"{"vertices":[1,1]}"#,r#"{"vertices":[2,1]}"#,r#"{"vertices":[1],"extra":0}"#] {assert!(serde_json::from_str::<Simplex>(wire).is_err());}
 for sign in [-2,-1,0,1,2] {let wire=format!(r#"{{"simplex":{{"vertices":[1,3]}},"orientation":{}}}"#,sign);assert_eq!(serde_json::from_str::<OrientedSimplex>(&wire).is_ok(),sign==-1||sign==1);}
}
fn permute(values:&mut [usize],start:usize,check:&mut impl FnMut(&[usize])) {
 if start==values.len(){check(values);return;}
 for i in start..values.len(){values.swap(start,i);permute(values,start+1,check);values.swap(start,i);}
}
#[test] fn independent_cycle_orientation_and_faces() {
 for n in 1..=6 {
  let mut values=(0..n).collect::<Vec<_>>();permute(&mut values,0,&mut |p| {
   let mut visited=vec![false;n];let mut cycles=0;for start in 0..n {if !visited[start] {cycles+=1;let mut i=start;while !visited[i] {visited[i]=true;i=p[i];}}}
   let want=if (n-cycles)%2==0{1}else{-1};let labels=p.iter().map(|v|10*v+7).collect::<Vec<_>>();let x=OrientedSimplex::from_ordered(labels).unwrap();assert_eq!(x.orientation(),want);assert_eq!(x.dimension(),n-1);assert_eq!(x.num_vertices(),n);assert_eq!(x.vertices(),(0..n).map(|v|10*v+7).collect::<Vec<_>>());
   let plain=OrientedSimplex::from_unordered(p.iter().map(|v|10*v+7).collect()).unwrap();assert_eq!(plain.orientation(),1);assert_eq!(plain.simplex(),x.simplex());
   if n>1 {for i in 0..n {let (face,sign)=plain.simplex().face(i).unwrap();let expected=(0..n).filter(|j|*j!=i).map(|v|10*v+7).collect::<Vec<_>>();assert_eq!(face.vertices(),expected);assert_eq!(sign,if i%2==0{1}else{-1});}}
   for (i,(face,sign)) in x.faces().iter().enumerate(){let expected=(0..n).filter(|j|*j!=i).map(|v|10*v+7).collect::<Vec<_>>();assert_eq!(face.vertices(),expected);assert_eq!(face.orientation(),1);assert_eq!(*sign,if i%2==0{want}else{-want});}
  });
 }
 assert!(OrientedSimplex::from_ordered(vec![]).is_err());assert!(OrientedSimplex::from_ordered(vec![1,1]).is_err());
}
fn vertices(mask:usize)->Vec<usize>{(0..3).filter(|i|mask&(1<<i)!=0).collect()}
fn faces_at(closed:&[usize],dimension:usize)->Vec<usize>{let mut out=closed.iter().copied().filter(|s|s.count_ones() as usize==dimension+1).collect::<Vec<_>>();out.sort_by_key(|s|vertices(*s));out}
#[test] fn all_three_vertex_families_and_integer_boundaries() {
 for family in 0..128usize {
  let input=(1..8).filter(|s|family&(1<<(s-1))!=0).collect::<Vec<_>>();let closed=(1..8).filter(|s|input.iter().any(|t|s&t==*s)).collect::<Vec<_>>();
  let x=SimplicialComplex::from_simplices(input.iter().map(|s|Simplex::new(vertices(*s)).unwrap()).collect()).unwrap();
  assert_eq!(x.total_simplices(),closed.len());assert_eq!(x.num_vertices(),closed.iter().map(|s|vertices(*s).last().unwrap()+1).max().unwrap_or(0));
  let max=closed.iter().map(|s|s.count_ones() as usize-1).max().unwrap_or(0);assert_eq!(x.max_dimension(),max);
  let mut euler=0i64;for d in 0..=4 {let expected=faces_at(&closed,d);assert_eq!(x.count(d),expected.len());let actual=x.simplices(d).iter().map(|s|s.vertices().to_vec()).collect::<Vec<_>>();assert_eq!(actual,expected.iter().map(|s|vertices(*s)).collect::<Vec<_>>());if d%2==0{euler+=expected.len() as i64;}else{euler-=expected.len() as i64;}}
  assert_eq!(x.euler_characteristic(),euler);
  for k in 0..=4 {let rows=if k==0{vec![]}else{faces_at(&closed,k-1)};let cols=faces_at(&closed,k);let matrix=x.boundary_matrix(k).unwrap();assert_eq!(matrix.shape(),(rows.len(),cols.len()));
   for (r,face) in rows.iter().enumerate(){for (c,simplex) in cols.iter().enumerate(){let vs=vertices(*simplex);let mut want=0i64;for (i,v) in vs.iter().enumerate(){if simplex^(1<<v)==*face{want=if i%2==0{1}else{-1};}}assert_eq!(matrix.get(r,c).unwrap(),q(want));}}
   if k>0 {let co=x.coboundary_matrix(k-1).unwrap();assert_eq!(co.shape(),(cols.len(),rows.len()));for r in 0..rows.len(){for c in 0..cols.len(){assert_eq!(co.get(c,r).unwrap(),matrix.get(r,c).unwrap());}}}
  }
  let nodes=faces_at(&closed,0);let edges=faces_at(&closed,1);let triangles=faces_at(&closed,2);let mut reach=[[false;3];3];for a in 0..3{reach[a][a]=true;}for edge in &edges{let v=vertices(*edge);reach[v[0]][v[1]]=true;reach[v[1]][v[0]]=true;}for k in 0..3{for a in 0..3{for b in 0..3{reach[a][b]|=reach[a][k]&&reach[k][b];}}}
  let components=nodes.iter().map(|s|vertices(*s)[0]).filter(|a|!(0..*a).any(|b|nodes.contains(&(1<<b))&&reach[*a][b])).count();let h1=edges.len() as i64-nodes.len() as i64+components as i64-triangles.len() as i64;
  let mut expected=vec![components];if max>=1{expected.push(h1 as usize);}if max>=2{expected.push(0);}assert_eq!(x.rational_betti_numbers().unwrap(),expected);
  assert!(x.verify_boundary_law().unwrap());assert!(x.verify_coboundary_law().unwrap());let wire=serde_json::to_string(&x).unwrap();assert_eq!(serde_json::from_str::<SimplicialComplex>(&wire).unwrap(),x);
 }
}
#[test] fn bounded_closure_and_gapped_ambient_set() {
 assert_eq!(SimplicialComplex::standard_n_simplex(MAX_SIMPLEX_VERTICES).unwrap_err(),HomologicalError::ResourceLimit("simplex dimension"));
 let vertex=Simplex::new(vec![3]).unwrap();assert_eq!(SimplicialComplex::from_simplices(vec![vertex.clone();MAX_SIMPLICES]).unwrap().num_vertices(),4);assert!(matches!(SimplicialComplex::from_simplices(vec![vertex;MAX_SIMPLICES+1]),Err(HomologicalError::ResourceLimit("simplicial face closure"))));
 assert!(matches!(SimplicialComplex::from_simplices(vec![Simplex::new(vec![usize::MAX]).unwrap()]),Err(HomologicalError::ResourceLimit("vertex label overflow"))));
}
'''


def complex_tests(cochain):
    if cochain:
        build=lambda a,b: f'CochainComplex::new(1,2,1,{b},{a},TheoremProvenance::new("unverified label".into()).unwrap())'
        replacements={'__BUILD__':build('left.clone()','right.clone()'),'__DIM0__':'1','__DIM1__':'2','__DIM2__':'1',
          '__LAW_ERROR__':'HomologicalError::CoboundaryLawViolation{degree:0}',
          '__OBSERVERS__':'assert_eq!(x.d0().matrix(),&right);assert_eq!(x.d1().matrix(),&left);assert_eq!(x.witness().d0_shape(),(2,1));assert_eq!(x.witness().d1_shape(),(1,2));assert_eq!(x.witness().provenance_hash,hash_provenance("unverified label"));assert_eq!(x.complex_hash(),&hash_cochain_complex_manifest(1,2,1,&x.d0().hash(),&x.d1().hash()));',
          '__BAD_FIRST__':build('good_left.clone()','bad_right.clone()'),'__BAD_SECOND__':build('bad_left.clone()','good_right.clone()'),
          '__FIRST_SHAPE__':'(2,1)','__SECOND_SHAPE__':'(1,2)','__BAD_FIRST_SHAPE__':'(3,1)','__BAD_SECOND_SHAPE__':'(2,2)',
          '__FIRST_ROWS__':'2','__FIRST_COLS__':'1','__BAD_RATIONAL__':build('good_left','invalid'),
          '__ZERO_BUILD__':'CochainComplex::new(a,b,c,matrix(b,a,vec![0;a*b]),matrix(c,b,vec![0;b*c]),TheoremProvenance::new("label".into()).unwrap())'}
    else:
        build=lambda a,b:f'ChainComplex::new(1,2,1,{a},{b})'
        replacements={'__BUILD__':build('left.clone()','right.clone()'),'__DIM0__':'1','__DIM1__':'2','__DIM2__':'1',
          '__LAW_ERROR__':'HomologicalError::BoundaryLawViolation{degree:1}',
          '__OBSERVERS__':'assert_eq!(x.boundary_1().matrix(),&left);assert_eq!(x.boundary_2().matrix(),&right);assert_eq!(x.complex_hash(),&hash_chain_complex_manifest(1,2,1,&x.boundary_1().hash(),&x.boundary_2().hash()));assert_eq!(omega_homology::chain_map::FiniteChainComplexView::boundaries(&x),&[left.clone(),right.clone()]);assert_eq!(omega_homology::chain_map::FiniteChainComplexView::complex_hash_bytes(&x),x.complex_hash().0);',
          '__BAD_FIRST__':build('bad_left.clone()','good_right.clone()'),'__BAD_SECOND__':build('good_left.clone()','bad_right.clone()'),
          '__FIRST_SHAPE__':'(1,2)','__SECOND_SHAPE__':'(2,1)','__BAD_FIRST_SHAPE__':'(2,2)','__BAD_SECOND_SHAPE__':'(3,1)',
          '__FIRST_ROWS__':'1','__FIRST_COLS__':'2','__BAD_RATIONAL__':build('invalid','good_right'),
          '__ZERO_BUILD__':'ChainComplex::new(a,b,c,matrix(a,b,vec![0;a*b]),matrix(b,c,vec![0;b*c]))'}
    body=COMPLEX_TESTS
    for old,new in replacements.items():body=body.replace(old,new)
    if '__' in body:raise ValueError('Unexpanded complex oracle marker')
    return body+(PROVENANCE if cochain else '')


def challenge(subject):
    name=Path(subject['path']).stem
    if name=='errors':
        rows=[*ERROR_ROWS,('InvalidDegreeIndex(7)','invalid degree: 7')]
        body=ERROR_TESTS.replace('__ERRORS__',','.join('(HomologicalError::'+value+','+json.dumps(message,ensure_ascii=False)+')' for value,message in rows))+ERROR_EXTRA
    elif name=='simplicial':body=SIMPLICIAL
    else:body=complex_tests(name=='cochain_complex')
    return '\n#[cfg(test)] mod independent_degree_repair_tests { use super::*;\n'+INDEX_TESTS+body+'\n}\n'


def variants(subject,source):
    for index,(needle,replacement) in enumerate(subject['faults']):
        if source.count(needle)!=1:raise ValueError('Ambiguous fault '+subject['path']+' '+needle)
        yield str(index),source.replace(needle,replacement,1),needle,replacement
