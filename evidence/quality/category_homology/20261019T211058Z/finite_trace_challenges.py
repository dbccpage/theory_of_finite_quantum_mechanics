"""Complete permutation-graph oracle plus original canonical BFS reference."""

REFERENCE = r'''
// Exact pre-refactor body, with `self` renamed to the free function argument.
fn reference(machine:&PartialDynamics,start:usize,word:&[usize],mode:ReplayMode,limits:TraceLimits)->Result<TraceComponent,ContinuationError>{
 if word.len()>limits.max_word_len||limits.max_words==0{return Err(ContinuationError::WorkLimit);}
 if machine.run(start,word)?.is_none(){return Err(ContinuationError::CertificateMismatch);}
 let pairs=machine.reports().len().checked_add(1).and_then(|n|n.checked_mul(n)).ok_or(ContinuationError::WorkLimit)?;
 let mut seen=BTreeSet::from([word.to_vec()]);let mut queue=VecDeque::from([word.to_vec()]);let mut tree=Vec::new();let mut checks=0usize;
 while let Some(w)=queue.pop_front(){for i in 0..w.len().saturating_sub(1){
  if checks>=limits.max_swap_checks{return Err(ContinuationError::WorkLimit);}checks+=1;
  let s=machine.run(start,&w[..i])?.ok_or(ContinuationError::CertificateMismatch)?;
  let swap=machine.certify_swap(s,w[i],w[i+1],pairs)?;
  let SwapOutcome::Independent{ab,ba}=swap.outcome else{continue;};
  if mode==ReplayMode::ExactState&&ab!=ba{continue;}
  let mut next=w.clone();next.swap(i,i+1);
  if !seen.contains(&next){if seen.len()>=limits.max_words{return Err(ContinuationError::WorkLimit);}
   seen.insert(next.clone());queue.push_back(next);tree.push(TraceLink{from:w.clone(),position:i,swap});}
 }}
 Ok(TraceComponent{start,word:word.to_vec(),mode,members:seen.into_iter().collect(),tree})
}
'''

ORACLE = r'''
fn direct(m:&PartialDynamics,start:usize,word:&[usize])->Option<usize>{let mut s=Some(start);for &a in word{s=s.and_then(|v|m.transitions()[v][a]);}s}
fn same_futures(m:&PartialDynamics,left:usize,right:usize)->bool{
 let mut seen=BTreeSet::new();let mut pending=vec![(Some(left),Some(right))];
 while let Some((l,r))=pending.pop(){if !seen.insert((l,r)){continue;}if l.map(|s|m.reports()[s])!=r.map(|s|m.reports()[s]){return false;}
  for a in 0..m.transitions()[0].len(){pending.push((l.and_then(|s|m.transitions()[s][a]),r.and_then(|s|m.transitions()[s][a])));}
 }true
}
fn permutations(input:&[usize])->BTreeSet<Vec<usize>>{
 fn visit(remaining:&[usize],prefix:&mut Vec<usize>,out:&mut BTreeSet<Vec<usize>>){if remaining.is_empty(){out.insert(prefix.clone());return;}
  for i in 0..remaining.len(){let mut rest=remaining.to_vec();let a=rest.remove(i);prefix.push(a);visit(&rest,prefix,out);prefix.pop();}}
 let mut out=BTreeSet::new();visit(input,&mut Vec::new(),&mut out);out
}
// Enumerate the ENTIRE candidate universe first, build every edge from direct
// transition/readout semantics, then use set saturation instead of BFS discovery.
fn graph_members(m:&PartialDynamics,start:usize,word:&[usize],mode:ReplayMode)->Vec<Vec<usize>>{
 let universe=permutations(word);let mut edges=Vec::new();
 for w in &universe{if direct(m,start,w).is_none(){continue;}for i in 0..w.len().saturating_sub(1){
  let Some(s)=direct(m,start,&w[..i])else{continue;};
  let (Some(ab),Some(ba))=(direct(m,s,&[w[i],w[i+1]]),direct(m,s,&[w[i+1],w[i]]))else{continue;};
  let allowed=match mode{ReplayMode::ExactState=>ab==ba,ReplayMode::ProtectedFutures=>same_futures(m,ab,ba)};
  if allowed{let mut other=w.clone();other.swap(i,i+1);assert!(universe.contains(&other));assert!(direct(m,start,&other).is_some());edges.push((w.clone(),other));}
 }}
 let mut reached=BTreeSet::from([word.to_vec()]);loop{let before=reached.clone();for (a,b) in &edges{if before.contains(a){reached.insert(b.clone());}}if reached==before{break;}}
 reached.into_iter().collect()
}
fn two_state(code:usize)->PartialDynamics{
 let t=code/4;let label=|n|match n{0=>None,1=>Some(0),_=>Some(1)};
 PartialDynamics::new(vec![if code&1==0{0}else{usize::MAX},if code&2==0{0}else{usize::MAX}],vec![vec![label(t%3),label((t/3)%3)],vec![label((t/9)%3),label((t/27)%3)]],2).unwrap()
}
fn check(m:&PartialDynamics,start:usize,word:&[usize],mode:ReplayMode){
 let limits=TraceLimits{max_words:24,max_word_len:4,max_swap_checks:100};let saved=m.clone();
 let actual=m.trace_component(start,word,mode,limits);assert_eq!(actual,reference(m,start,word,mode,limits));
 if direct(m,start,word).is_none(){assert_eq!(actual,Err(ContinuationError::CertificateMismatch));return;}
 let c=actual.unwrap();assert_eq!((c.start,&c.word,c.mode),(start,&word.to_vec(),mode));assert_eq!(c.members,graph_members(m,start,word,mode));assert_eq!(c.tree.len()+1,c.members.len());m.verify_trace(start,word,mode,limits,&c).unwrap();
 let count=c.members.len();let checks=count*word.len().saturating_sub(1);
 let exact=TraceLimits{max_words:count,max_word_len:word.len(),max_swap_checks:checks};assert_eq!(m.trace_component(start,word,mode,exact),Ok(c.clone()));
 let fewer_words=TraceLimits{max_words:count-1,..exact};assert_eq!(m.trace_component(start,word,mode,fewer_words),Err(ContinuationError::WorkLimit));
 if checks>0{let fewer=TraceLimits{max_swap_checks:checks-1,..exact};assert_eq!(m.trace_component(start,word,mode,fewer),Err(ContinuationError::WorkLimit));assert_eq!(m.verify_trace(start,word,mode,fewer,&c),Err(ContinuationError::WorkLimit));}
 if !word.is_empty(){let short=TraceLimits{max_word_len:word.len()-1,..exact};assert_eq!(m.trace_component(start,word,mode,short),Err(ContinuationError::WorkLimit));}
 let mut bad=c.clone();bad.members.push(vec![usize::MAX]);assert_eq!(m.verify_trace(start,word,mode,limits,&bad),Err(ContinuationError::CertificateMismatch));
 let mut bad=c.clone();bad.members.remove(0);assert_eq!(m.verify_trace(start,word,mode,limits,&bad),Err(ContinuationError::CertificateMismatch));
 let mut bad=c.clone();bad.word.push(usize::MAX);assert_eq!(m.verify_trace(start,word,mode,limits,&bad),Err(ContinuationError::CertificateMismatch));
 let mut bad=c.clone();bad.start=usize::MAX;assert_eq!(m.verify_trace(start,word,mode,limits,&bad),Err(ContinuationError::CertificateMismatch));
 let mut bad=c.clone();bad.mode=match mode{ReplayMode::ExactState=>ReplayMode::ProtectedFutures,_=>ReplayMode::ExactState};assert_eq!(m.verify_trace(start,word,mode,limits,&bad),Err(ContinuationError::CertificateMismatch));
 let mut bad=c.clone();bad.tree.push(TraceLink{from:vec![],position:usize::MAX,swap:SwapCertificate{start:usize::MAX,a:usize::MAX,b:usize::MAX,outcome:SwapOutcome::Independent{ab:usize::MAX,ba:usize::MAX}}});assert_eq!(m.verify_trace(start,word,mode,limits,&bad),Err(ContinuationError::CertificateMismatch));
 assert_eq!(m,&saved);
}
#[test] fn all_two_state_short_trace_graphs(){for code in 0..324{let m=two_state(code);for len in 0..=3{for bits in 0..(1usize<<len){let word:Vec<_>=(0..len).map(|i|(bits>>i)&1).collect();for start in 0..2{for mode in [ReplayMode::ExactState,ReplayMode::ProtectedFutures]{check(&m,start,&word,mode);}}}}}}
#[test] fn scratch_restore_fifo_modes_and_refusals(){
 let commuting=PartialDynamics::new(vec![0],vec![vec![Some(0),Some(0)]],2).unwrap();
 for bits in 0..16{let word:Vec<_>=(0..4).map(|i|(bits>>i)&1).collect();for mode in [ReplayMode::ExactState,ReplayMode::ProtectedFutures]{check(&commuting,0,&word,mode);}}
 let m=PartialDynamics::new(vec![0,0,1,7,7],vec![vec![Some(1),Some(2)],vec![Some(1),Some(3)],vec![Some(4),Some(2)],vec![Some(3),Some(3)],vec![Some(4),Some(4)]],2).unwrap();
 for mode in [ReplayMode::ExactState,ReplayMode::ProtectedFutures]{check(&m,0,&[0,1],mode);check(&m,0,&[1,0,0],mode);}
 let limits=TraceLimits{max_words:24,max_word_len:4,max_swap_checks:100};
 assert_eq!(m.trace_component(0,&[0,1],ReplayMode::ExactState,limits).unwrap().members,vec![vec![0,1]]);
 assert_eq!(m.trace_component(0,&[0,1],ReplayMode::ProtectedFutures,limits).unwrap().members,vec![vec![0,1],vec![1,0]]);
 assert_eq!(m.trace_component(99,&[99],ReplayMode::ExactState,TraceLimits{max_words:0,..limits}),Err(ContinuationError::WorkLimit));
 assert_eq!(m.trace_component(99,&[99],ReplayMode::ExactState,limits),Err(ContinuationError::OutsideCarrier));
 assert_eq!(m.trace_component(0,&[99],ReplayMode::ExactState,limits),Err(ContinuationError::OutsideAlphabet));
 let unavailable=PartialDynamics::new(vec![0],vec![vec![None]],1).unwrap();assert_eq!(unavailable.trace_component(0,&[0,99],ReplayMode::ExactState,limits),Err(ContinuationError::OutsideAlphabet));
 assert_eq!(unavailable.trace_component(0,&[0],ReplayMode::ExactState,limits),Err(ContinuationError::CertificateMismatch));
 // Root pair(1,0) discovers all nine completed pairs before dequeuing the
 // distinguishing one; using n^2=4 instead of(n+1)^2=9 is insufficient.
 let wide=PartialDynamics::new(vec![0,0],vec![vec![Some(0),Some(1),Some(1),Some(0),Some(1),None,None,None],vec![Some(0),Some(1),Some(0),None,None,Some(0),Some(1),None]],8).unwrap();
 assert_eq!(wide.certify_swap(0,0,1,4),Err(ContinuationError::WorkLimit));
 assert!(matches!(wide.certify_swap(0,0,1,9).unwrap().outcome,SwapOutcome::Distinguished{..}));
 check(&wide,0,&[0,1],ReplayMode::ProtectedFutures);
 let mut frontier=TraceFrontier::new(&[]);frontier.checks=usize::MAX-1;frontier.charge(usize::MAX).unwrap();assert_eq!(frontier.checks,usize::MAX);assert_eq!(frontier.charge(usize::MAX),Err(ContinuationError::WorkLimit));
}
'''


def challenge(subject):
    return '\n#[cfg(test)] mod independent_trace_tests {use super::*;\n'+REFERENCE+ORACLE+'\n}\n'
