"""Option-pair word-language oracle and adversarial state-relative swap receipts."""

ORACLE = r'''
use std::collections::{BTreeSet,VecDeque};
fn run_direct(m:&PartialDynamics,start:usize,word:&[usize])->Option<usize>{let mut s=Some(start);for &a in word {s=s.and_then(|x|m.transitions()[x][a]);}s}
fn distinguish_direct(m:&PartialDynamics,left:usize,right:usize)->Option<Vec<usize>>{
 let mut seen=BTreeSet::new();let mut queue=VecDeque::from([(Some(left),Some(right),vec![])]);
 while let Some((l,r,w))=queue.pop_front(){if !seen.insert((l,r)){continue;}
  if l.map(|s|m.reports()[s])!=r.map(|s|m.reports()[s]){return Some(w);}
  for a in 0..m.transitions()[0].len(){let mut next=w.clone();next.push(a);queue.push_back((l.and_then(|s|m.transitions()[s][a]),r.and_then(|s|m.transitions()[s][a]),next));}
 }None
}
fn machine(code:usize)->PartialDynamics{
 let outputs=vec![if code&1==0{0}else{usize::MAX},if code&2==0{0}else{usize::MAX}];let t=code/4;let label=|n|match n{0=>None,1=>Some(0),_=>Some(1)};
 PartialDynamics::new(outputs,vec![vec![label(t%3),label((t/3)%3)],vec![label((t/9)%3),label((t/27)%3)]],2).unwrap()
}
fn check(m:&PartialDynamics,start:usize,a:usize,b:usize){
 let saved=m.clone();let sa=run_direct(m,start,&[a]);let sb=run_direct(m,start,&[b]);let ab=run_direct(m,start,&[a,b]);let ba=run_direct(m,start,&[b,a]);
 let c=m.certify_swap(start,a,b,usize::MAX).unwrap();assert_eq!((c.start,c.a,c.b),(start,a,b));
 match (ab,ba){
  (Some(x),Some(y))=>match distinguish_direct(m,x,y){
   None=>{assert_eq!(c.outcome,SwapOutcome::Independent{ab:x,ba:y});assert_eq!(m.certify_swap(start,a,b,0),Ok(c.clone()));},
   Some(word)=>{let SwapOutcome::Distinguished{ab:cx,ba:cy,future}=&c.outcome else{panic!("expected distinction")};assert_eq!((*cx,*cy),(x,y));assert_eq!((future.left,future.right),(x,y));assert_eq!(future.word,word);assert_eq!(future.left_answer,run_direct(m,x,&word).map(|s|m.reports()[s]));assert_eq!(future.right_answer,run_direct(m,y,&word).map(|s|m.reports()[s]));assert_eq!(m.certify_swap(start,a,b,0),Err(ContinuationError::WorkLimit));}
  },
  _=>{assert_eq!(c.outcome,SwapOutcome::Unavailable{a:sa,b:sb,ab,ba});assert_eq!(m.certify_swap(start,a,b,0),Ok(c.clone()));}
 }
 m.verify_swap(&c).unwrap();let mut bad=c.clone();bad.start=m.reports().len();assert_eq!(m.verify_swap(&bad),Err(ContinuationError::OutsideCarrier));
 let mut bad=c.clone();bad.a=m.transitions()[0].len();assert_eq!(m.verify_swap(&bad),Err(ContinuationError::OutsideAlphabet));let mut bad=c.clone();bad.b=usize::MAX;assert_eq!(m.verify_swap(&bad),Err(ContinuationError::OutsideAlphabet));
 let mut bad=c.clone();bad.outcome=SwapOutcome::Independent{ab:usize::MAX,ba:usize::MAX};assert_eq!(m.verify_swap(&bad),Err(ContinuationError::CertificateMismatch));
 for field in 0..4{let mut values=[sa,sb,ab,ba];values[field]=Some(usize::MAX);let bad=SwapCertificate{start,a,b,outcome:SwapOutcome::Unavailable{a:values[0],b:values[1],ab:values[2],ba:values[3]}};assert_eq!(m.verify_swap(&bad),Err(ContinuationError::CertificateMismatch));}
 if ab.is_some()&&ba.is_some(){let bad=SwapCertificate{start,a,b,outcome:SwapOutcome::Unavailable{a:sa,b:sb,ab,ba}};assert_eq!(m.verify_swap(&bad),Err(ContinuationError::CertificateMismatch));}
 assert_eq!(m,&saved);
}
#[test] fn all_two_state_two_event_swaps(){for code in 0..324{let m=machine(code);for start in 0..2{for a in 0..2{for b in 0..2{check(&m,start,a,b);}}}}}
#[test] fn future_equivalence_and_nonshortest_distinction(){
 let transitions=vec![vec![Some(1),Some(2)],vec![Some(1),Some(3)],vec![Some(4),Some(2)],vec![Some(3),Some(3)],vec![Some(4),Some(4)]];
 let same=PartialDynamics::new(vec![0,0,1,7,7],transitions.clone(),2).unwrap();check(&same,0,0,1);
 assert_eq!(same.certify_swap(0,0,1,0).unwrap().outcome,SwapOutcome::Independent{ab:3,ba:4});
 let different=PartialDynamics::new(vec![0,0,1,0,1],transitions,2).unwrap();check(&different,0,0,1);
 let c=SwapCertificate{start:0,a:0,b:1,outcome:SwapOutcome::Distinguished{ab:3,ba:4,future:DistinguishingWord{left:3,right:4,word:vec![0,0],left_answer:Some(0),right_answer:Some(1)}}};different.verify_swap(&c).unwrap();
 let unrelated=SwapCertificate{start:0,a:0,b:1,outcome:SwapOutcome::Distinguished{ab:0,ba:2,future:DistinguishingWord{left:0,right:2,word:vec![],left_answer:Some(0),right_answer:Some(1)}}};
 // The future is valid and bound to its submitted endpoints, but those are not
 // this swap's actual endpoints. This isolates the outer endpoint guard.
 assert!(different.verify_distinction(match &unrelated.outcome{SwapOutcome::Distinguished{future,..}=>future,_=>unreachable!()}).is_ok());
 assert_eq!(different.verify_swap(&unrelated),Err(ContinuationError::CertificateMismatch));
 for field in 0..7{let mut bad=c.clone();let SwapOutcome::Distinguished{ab,ba,future}=&mut bad.outcome else{unreachable!()};match field{0=>*ab=4,1=>*ba=3,2=>future.left=0,3=>future.right=2,4=>future.word=vec![usize::MAX],5=>future.left_answer=None,_=>future.right_answer=Some(0)};assert_eq!(different.verify_swap(&bad),Err(ContinuationError::CertificateMismatch));}
 let mut bad=c.clone();bad.outcome=SwapOutcome::Independent{ab:3,ba:4};assert_eq!(different.verify_swap(&bad),Err(ContinuationError::CertificateMismatch));
 assert_eq!(same.verify_swap(&c),Err(ContinuationError::CertificateMismatch));
 for (s,a,b,error) in [(99,99,99,ContinuationError::OutsideCarrier),(0,99,99,ContinuationError::OutsideAlphabet),(0,0,99,ContinuationError::OutsideAlphabet)]{assert_eq!(different.certify_swap(s,a,b,0),Err(error));}
}
'''


def challenge(subject):
    return '\n#[cfg(test)] mod independent_swap_tests {use super::*;\n'+ORACLE+'\n}\n'
