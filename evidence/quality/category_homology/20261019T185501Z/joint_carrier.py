"""Direct finite relation/profile/fiber oracles; no product availability premise."""

ORACLE = r'''
use std::collections::{BTreeMap, VecDeque};
// Explore the product transition graph until every reachable pair is visited.
// This compares all words, independently of iterative partition refinement.
fn language_equal(m: &PartialDynamics, a: usize, b: usize) -> bool {
 let mut seen=BTreeSet::new();let mut todo=VecDeque::from([(Some(a),Some(b))]);
 while let Some((x,y))=todo.pop_front() {
  if !seen.insert((x,y)) {continue;}
  if x.map(|s|m.reports()[s]) != y.map(|s|m.reports()[s]) {return false;}
  for k in 0..m.transitions()[0].len() {todo.push_back((x.and_then(|s|m.transitions()[s][k]),y.and_then(|s|m.transitions()[s][k])));}
 }
 true
}
fn classes(m: &PartialDynamics) -> Vec<usize> {
 let mut representatives=Vec::new();let mut ids=Vec::new();
 for s in 0..m.reports().len() {
  let id=representatives.iter().position(|&r|language_equal(m,s,r)).unwrap_or_else(||{representatives.push(s);representatives.len()-1});
  ids.push(id);
 }
 assert_eq!(&m.quotient().state_to_block[..m.reports().len()],ids);
 ids
}
fn machine(which: usize) -> PartialDynamics {
 match which {
  0=>PartialDynamics::new(vec![0,0],vec![vec![],vec![]],0).unwrap(),
  1=>PartialDynamics::new(vec![usize::MAX,0],vec![vec![],vec![]],0).unwrap(),
  2=>PartialDynamics::new(vec![0,0],vec![vec![None],vec![Some(1)]],1).unwrap(),
  _=>PartialDynamics::new(vec![0,1,0],vec![vec![Some(1)],vec![Some(1)],vec![Some(2)]],1).unwrap(),
 }
}
fn exact_cost(m: &PartialDynamics) -> usize {(m.reports().len()+1).pow(2)*(m.transitions()[0].len()+1)}
fn check(p: &JointCarrierProblem, pairs: &[(usize,usize)], answers: &[usize], lc: &[usize],rc: &[usize]) {
 assert_eq!(p.pairs(),pairs);let before=p.clone();
 let reports:Vec<_>=pairs.iter().map(|&(l,r)|(lc[l],rc[r])).collect();
 let c=p.analyze().unwrap();assert_eq!(c.reports,reports);p.verify_analysis(&c).unwrap();
 let mut profiles:Vec<_>=reports.iter().zip(answers).map(|(&(l,r),&a)|vec![l,r,a]).collect();profiles.sort();profiles.dedup();
 assert_eq!(c.refinement.profiles,profiles);
 let ids:Vec<_>=reports.iter().zip(answers).map(|(&(l,r),&a)|profiles.iter().position(|v|v==&vec![l,r,a]).unwrap()).collect();
 assert_eq!(c.refinement.class_of,ids);
 let first_collision=(0..pairs.len()).find_map(|i|((i+1)..pairs.len()).find(|&j|reports[i]==reports[j]&&answers[i]!=answers[j]).map(|j|(i,j)));
 match &c.decision {
  ReportQueryDecision::Factorable(f)=>{
   assert!(first_collision.is_none());
   let image:BTreeSet<_>=reports.iter().copied().collect();assert_eq!(f.realized_image,image);
   assert_eq!(f.decoder.keys().copied().collect::<BTreeSet<_>>(),image);
   assert_eq!(f.representative.keys().copied().collect::<BTreeSet<_>>(),image);
   for (i,r) in reports.iter().enumerate(){assert_eq!(f.decoder[r],answers[i]);let j=f.representative[r];assert!(j<pairs.len());assert_eq!(reports[j],*r);assert_eq!(j,reports.iter().position(|s|s==r).unwrap());}
  },
  ReportQueryDecision::Collision(w)=>{
   assert!(first_collision.is_some());let (i,j)=(w.first,w.second);assert_ne!(i,j);assert!(i<pairs.len()&&j<pairs.len());
   assert_eq!(reports[i],reports[j]);assert_eq!(w.report,reports[i]);assert_ne!(answers[i],answers[j]);assert_eq!((w.first_query,w.second_query),(answers[i],answers[j]));
  }
 }
 let mut bad=c.clone();bad.reports.push((usize::MAX,0));assert_eq!(p.verify_analysis(&bad),Err(JointError::CertificateMismatch));
 let mut bad=c.clone();bad.refinement.profiles.push(vec![]);assert_eq!(p.verify_analysis(&bad),Err(JointError::CertificateMismatch));
 let mut bad=c.clone();bad.refinement.class_of.push(usize::MAX);assert_eq!(p.verify_analysis(&bad),Err(JointError::CertificateMismatch));
 let mut bad=c.clone();match &mut bad.decision {ReportQueryDecision::Factorable(f)=>{f.decoder.insert((usize::MAX,usize::MAX),0);},ReportQueryDecision::Collision(w)=>{w.first=w.second;}};assert_eq!(p.verify_analysis(&bad),Err(JointError::CertificateMismatch));
 for l in 0..=lc.len() {for r in 0..=rc.len() {
  let result=p.fiber((l,r));
  if !lc.contains(&l)||!rc.contains(&r) {assert_eq!(result,Err(JointError::UnknownLocalClass));continue;}
  let f=result.unwrap();let rows:Vec<_>=reports.iter().enumerate().filter(|(_,v)|**v==(l,r)).map(|(i,_)|i).collect();
  assert_eq!(f.locals,(l,r));assert_eq!(f.rows,rows);assert_eq!(f.answers,rows.iter().map(|&i|answers[i]).collect());p.verify_fiber((l,r),&f).unwrap();
  let mut bad=f.clone();bad.rows.push(usize::MAX);assert_eq!(p.verify_fiber((l,r),&bad),Err(JointError::CertificateMismatch));
  let mut bad=f.clone();bad.answers.insert(usize::MAX);assert_eq!(p.verify_fiber((l,r),&bad),Err(JointError::CertificateMismatch));
  let mut bad=f.clone();bad.locals=(usize::MAX,r);assert_eq!(p.verify_fiber((l,r),&bad),Err(JointError::CertificateMismatch));
 }}
 assert_eq!(p,&before);
}
#[test] fn independent_relations_and_answers() {
 for a in 0..4 {for b in 0..4 {
  let left=machine(a);let right=machine(b);let lc=classes(&left);let rc=classes(&right);let saved=(left.clone(),right.clone());
  // All absent/zero/one assignments on four candidate pairs; not a full-product premise.
  for mask in 0..81usize {let mut code=mask;let mut pairs=Vec::new();let mut answers=Vec::new();
   for pair in [(0,0),(1,0),(0,1),(1,1)] {let t=code%3;code/=3;if t!=0 {pairs.push(pair);answers.push(if t==1 {0} else {usize::MAX});}}
   let cost=exact_cost(&left)+exact_cost(&right)+3*pairs.len();
   assert_eq!(JointCarrierProblem::new(&left,&right,pairs.clone(),answers.clone(),cost-1),Err(JointError::WorkLimit));
   let p=JointCarrierProblem::new(&left,&right,pairs.clone(),answers.clone(),cost).unwrap();check(&p,&pairs,&answers,&lc,&rc);
   pairs.reverse();answers.reverse();let p=JointCarrierProblem::new(&left,&right,pairs.clone(),answers.clone(),usize::MAX).unwrap();check(&p,&pairs,&answers,&lc,&rc);
  }
  assert_eq!((left,right),saved);
 }}
}
#[test] fn typed_refusals_and_context() {
 let l=machine(3);let r=machine(2);
 for (pairs,answers) in [(vec![(0,0)],vec![]),(vec![(0,0),(0,0)],vec![0,1]),(vec![(3,0)],vec![0]),(vec![(0,2)],vec![0]),(vec![(usize::MAX,0)],vec![0]),(vec![(0,usize::MAX)],vec![0])] {
  assert_eq!(JointCarrierProblem::new(&l,&r,pairs.clone(),answers.clone(),0),Err(JointError::WorkLimit));
  assert_eq!(JointCarrierProblem::new(&l,&r,pairs,answers,usize::MAX),Err(JointError::InvalidRelation));
 }
 let p=JointCarrierProblem::new(&l,&r,vec![(0,0),(1,1),(2,1)],vec![1,2,3],usize::MAX).unwrap();
 check(&p,p.pairs(),&[1,2,3],&classes(&l),&classes(&r));
 let other=JointCarrierProblem::new(&l,&r,vec![(0,0),(1,1)],vec![0,0],usize::MAX).unwrap();
 assert_eq!(p.verify_analysis(&other.analyze().unwrap()),Err(JointError::CertificateMismatch));
 let f=JointFiber{locals:(99,0),rows:vec![],answers:BTreeSet::new()};assert_eq!(p.verify_fiber((99,0),&f),Err(JointError::UnknownLocalClass));
 // Replay binds the requested projections; equal observable receipts need not identify raw relation rows.
 let same=JointCarrierProblem::new(&machine(0),&machine(0),vec![(1,1)],vec![7],usize::MAX).unwrap();
 let equal=JointCarrierProblem::new(&machine(0),&machine(0),vec![(0,0)],vec![7],usize::MAX).unwrap();
 assert_ne!(same.pairs(),equal.pairs());same.verify_analysis(&equal.analyze().unwrap()).unwrap();
}
'''


def challenge(subject):
    return '\n#[cfg(test)] mod independent_joint_tests { use super::*;\n' + ORACLE + '\n}\n'
