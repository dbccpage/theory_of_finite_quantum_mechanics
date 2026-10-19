"""Finite extensional simulation truth tables and explicit admission precedence."""

ORACLE = r'''
fn machine(code: usize) -> PartialDynamics {
 let reports=vec![if code&1==0 {0} else {usize::MAX},if code&2==0 {0} else {usize::MAX}];
 let encode=|n|match n {0=>None,1=>Some(0),_=>Some(1)};
 PartialDynamics::new(reports,vec![vec![encode((code/4)%3)],vec![encode((code/12)%3)]],1).unwrap()
}
fn direct_run(m:&PartialDynamics,start:usize,word:&[usize])->Option<usize>{
 let mut s=Some(start);for &a in word {s=match s {None=>None,Some(t)=>m.transitions()[t][a]};}s
}
fn oracle(source:&PartialDynamics,target:&PartialDynamics,map:&[usize],words:&[Vec<usize>],mode:SimulationMode)->SimulationDecision {
 // Extensional allowed step pairs; a step witness is not inferred from a diagnostic branch.
 let mut allowed=vec![(None,None),(Some(0),Some(0)),(Some(1),Some(1))];
 if mode==SimulationMode::ResourceExtension {allowed.extend([(None,Some(0)),(None,Some(1))]);}
 let mut failures=Vec::new();let mut additions=Vec::new();
 for s in 0..2 {
  let t=map[s];
  if source.reports()[s]!=target.reports()[t] {failures.push((s*2,SimulationDecision::ReportMismatch{state:s,source_report:source.reports()[s],target_report:target.reports()[t]}));}
  let expected=source.transitions()[s][0].map(|v|map[v]);let actual=direct_run(target,t,&words[0]);
  if !allowed.contains(&(expected,actual)) {failures.push((s*2+1,SimulationDecision::StepMismatch{state:s,input:0,expected,actual}));}
  if [(None,Some(0)),(None,Some(1))].contains(&(expected,actual)) {additions.push((s,0));}
 }
 failures.sort_by_key(|x|x.0);failures.into_iter().next().map(|x|x.1).unwrap_or(SimulationDecision::Checked{added_availability:if mode==SimulationMode::ResourceExtension {additions} else {vec![]}})
}
#[test] fn all_two_state_one_event_simulations() {
 for sc in 0..36 {for tc in 0..36 {let source=machine(sc);let target=machine(tc);let saved=(source.clone(),target.clone());
  for map in [vec![0,0],vec![1,0],vec![0,1],vec![1,1]] {for word in [vec![],vec![0],vec![0,0]] {for mode in [SimulationMode::Exact,SimulationMode::ResourceExtension] {
   let words=vec![word.clone()];let unique=map[0]!=map[1];let cost=(word.len()+2)*2;
   if !unique && mode==SimulationMode::ResourceExtension {assert_eq!(check_simulation(&source,&target,&map,&words,mode,0),Err(SimulationError::InvalidMap));continue;}
   assert_eq!(check_simulation(&source,&target,&map,&words,mode,cost-1),Err(SimulationError::WorkLimit));
   let expected=oracle(&source,&target,&map,&words,mode);let c=check_simulation(&source,&target,&map,&words,mode,cost).unwrap();assert_eq!(c,expected);
   verify_simulation(&source,&target,&map,&words,mode,cost,&c).unwrap();
   let bad=match c.clone() {SimulationDecision::Checked{mut added_availability}=>{added_availability.push((usize::MAX,usize::MAX));SimulationDecision::Checked{added_availability}},SimulationDecision::ReportMismatch{state,source_report,target_report}=>SimulationDecision::ReportMismatch{state:state+2,source_report,target_report},SimulationDecision::StepMismatch{state,input,expected,actual}=>SimulationDecision::StepMismatch{state,input:input+1,expected,actual}};
   assert_eq!(verify_simulation(&source,&target,&map,&words,mode,cost,&bad),Err(SimulationError::CertificateMismatch));
   assert_eq!(verify_simulation(&source,&target,&map,&words,mode,cost-1,&c),Err(SimulationError::WorkLimit));
  }}}
  assert_eq!((source,target),saved);
 }}
}
#[test] fn admission_precedence_and_two_event_order() {
 let source=machine(0);let target=machine(0);
 for map in [vec![],vec![0],vec![0,1,0],vec![0,2],vec![usize::MAX,0]] {
  assert_eq!(check_simulation(&source,&target,&map,&[vec![usize::MAX]],SimulationMode::Exact,0),Err(SimulationError::InvalidMap));
  assert_eq!(verify_simulation(&source,&target,&map,&[vec![usize::MAX]],SimulationMode::Exact,0,&SimulationDecision::Checked{added_availability:vec![]}),Err(SimulationError::InvalidMap));
 }
 for words in [vec![],vec![vec![],vec![]],vec![vec![1]],vec![vec![usize::MAX]],vec![vec![0,1]]] {
  assert_eq!(check_simulation(&source,&target,&[0,1],&words,SimulationMode::Exact,0),Err(SimulationError::InvalidEncoding));
 }
 let noevents=PartialDynamics::new(vec![0],vec![vec![]],0).unwrap();
 assert_eq!(check_simulation(&noevents,&noevents,&[0],&[],SimulationMode::Exact,0),Err(SimulationError::WorkLimit));
 assert_eq!(check_simulation(&noevents,&noevents,&[0],&[],SimulationMode::Exact,1),Ok(SimulationDecision::Checked{added_availability:vec![]}));
 let source=PartialDynamics::new(vec![0,0],vec![vec![None,None],vec![None,None]],2).unwrap();
 let target=PartialDynamics::new(vec![0,0],vec![vec![Some(0),Some(1)],vec![Some(1),Some(0)]],2).unwrap();
 let words=vec![vec![1,0],vec![]];let cost=2*(1+3+1);
 let c=SimulationDecision::Checked{added_availability:vec![(0,0),(0,1),(1,0),(1,1)]};
 assert_eq!(check_simulation(&source,&target,&[1,0],&words,SimulationMode::ResourceExtension,cost),Ok(c.clone()));
 verify_simulation(&source,&target,&[1,0],&words,SimulationMode::ResourceExtension,cost,&c).unwrap();
 assert_eq!(check_simulation(&source,&target,&[1,0],&words,SimulationMode::Exact,cost),Ok(SimulationDecision::StepMismatch{state:0,input:0,expected:None,actual:Some(1)}));
 let source=PartialDynamics::new(vec![0,1],vec![vec![Some(0),Some(1)],vec![Some(1),Some(0)]],2).unwrap();
 let target=PartialDynamics::new(vec![1,0],vec![vec![Some(0),Some(1)],vec![Some(1),Some(0)]],2).unwrap();
 let c=SimulationDecision::StepMismatch{state:0,input:1,expected:Some(0),actual:Some(1)};
 assert_eq!(check_simulation(&source,&target,&[1,0],&[vec![0],vec![0]],SimulationMode::Exact,usize::MAX),Ok(c.clone()));
 verify_simulation(&source,&target,&[1,0],&[vec![0],vec![0]],SimulationMode::Exact,usize::MAX,&c).unwrap();
}
#[test] fn checked_budget_overflow_without_allocating_carrier() {
 assert_eq!(admit_budget(usize::MAX,&[vec![]],usize::MAX),Err(SimulationError::WorkLimit));
 assert_eq!(admit_budget(usize::MAX/2+1,&[vec![0]],usize::MAX),Err(SimulationError::WorkLimit));
 assert_eq!(admit_budget(0,&[vec![0]],0),Ok(())); // private scalar helper; public machines are nonempty.
}
'''


def challenge(subject):
    return '\n#[cfg(test)] mod independent_simulation_tests {use super::*;\n'+ORACLE+'\n}\n'
