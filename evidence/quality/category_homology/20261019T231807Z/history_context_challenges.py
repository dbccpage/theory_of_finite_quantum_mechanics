"""AuthorityEffect: None. Independent complete bounded product-state word enumeration,raw emission semantics,reachable action oracle and long witness;frozen previous implementation."""
FROZEN=r'''mod frozen {
//! Unbounded finite-word contexts and their exact finite-state descent test.
//! This owner never replaces an arbitrary action on D* by a sampled word table.
use crate::finite_moore::FiniteMoore;
use std::collections::{BTreeMap, VecDeque};

/// Two input histories whose equal source profiles have unequal output profiles.
pub type ProfileNoncongruenceWitness = (Vec<usize>, Vec<usize>);

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum HistoryError {
    InvalidAlphabet,
    InvalidWord,
    InvalidTransducer,
    InvalidInitialState,
    InvalidCertificate,
    UnavailableContext,
}

/// Executable original history action. Arbitrary implementations retain their
/// own semantics; callers check every output word. Only FiniteWordTransducer
/// below supplies a checked total finite-state realization and global descent test.
pub trait HistoryContext {
    fn apply(&self, word: &[usize]) -> Result<Vec<usize>, HistoryError>;
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FiniteWordTransducer {
    alphabet_size: usize,
    initial: usize,
    transitions: Vec<Vec<usize>>,
    outputs: Vec<Vec<Vec<usize>>>,
    initial_output: Vec<usize>,
    final_outputs: Vec<Vec<usize>>,
}

impl FiniteWordTransducer {
    pub fn new(
        alphabet_size: usize,
        initial: usize,
        transitions: Vec<Vec<usize>>,
        outputs: Vec<Vec<Vec<usize>>>,
        initial_output: Vec<usize>,
        final_outputs: Vec<Vec<usize>>,
    ) -> Result<Self, HistoryError> {
        let n = transitions.len();
        if n == 0
            || initial >= n
            || outputs.len() != n
            || final_outputs.len() != n
            || transitions
                .iter()
                .any(|row| row.len() != alphabet_size || row.iter().any(|&x| x >= n))
            || outputs.iter().any(|row| row.len() != alphabet_size)
            || outputs
                .iter()
                .flatten()
                .chain(final_outputs.iter())
                .chain(std::iter::once(&initial_output))
                .flatten()
                .any(|&d| d >= alphabet_size)
        {
            return Err(HistoryError::InvalidTransducer);
        }
        Ok(Self {
            alphabet_size,
            initial,
            transitions,
            outputs,
            initial_output,
            final_outputs,
        })
    }
    pub fn alphabet_size(&self) -> usize {
        self.alphabet_size
    }
    pub fn state_count(&self) -> usize {
        self.transitions.len()
    }
    pub fn substitution(images: Vec<Vec<usize>>) -> Result<Self, HistoryError> {
        let n = images.len();
        Self::new(n, 0, vec![vec![0; n]], vec![images], vec![], vec![vec![]])
    }
    pub fn prefix(alphabet_size: usize, prefix: Vec<usize>) -> Result<Self, HistoryError> {
        Self::new(
            alphabet_size,
            0,
            vec![vec![0; alphabet_size]],
            vec![(0..alphabet_size).map(|d| vec![d]).collect()],
            prefix,
            vec![vec![]],
        )
    }
    pub fn suffix(alphabet_size: usize, suffix: Vec<usize>) -> Result<Self, HistoryError> {
        Self::new(
            alphabet_size,
            0,
            vec![vec![0; alphabet_size]],
            vec![(0..alphabet_size).map(|d| vec![d]).collect()],
            vec![],
            vec![suffix],
        )
    }

    /// Finite product graph includes (original memory, transducer state,
    /// transformed-word memory). Its reachable vertices represent ALL words,
    /// not a cutoff. Final emissions are applied before comparing state images.
    pub fn descend(
        &self,
        memory: &FiniteMoore,
        start: usize,
    ) -> Result<HistoryDescent, HistoryError> {
        if memory.input_count() != self.alphabet_size {
            return Err(HistoryError::InvalidAlphabet);
        }
        if start >= memory.state_count() {
            return Err(HistoryError::InvalidInitialState);
        }
        let initial = (
            start,
            self.initial,
            run(memory, start, &self.initial_output)?,
        );
        let mut histories = BTreeMap::from([(initial, vec![])]);
        let mut pending = VecDeque::from([initial]);
        let mut images = vec![None; memory.state_count()];
        let mut representatives: Vec<Option<Vec<usize>>> = vec![None; memory.state_count()];
        while let Some((source, control, output)) = pending.pop_front() {
            let word = histories[&(source, control, output)].clone();
            let final_state = run(memory, output, &self.final_outputs[control])?;
            if let Some(previous) = images[source] {
                if previous != final_state {
                    return Ok(HistoryDescent::Obstructed(HistoryCollision {
                        first: representatives[source]
                            .clone()
                            .ok_or(HistoryError::InvalidCertificate)?,
                        second: word,
                        source_state: source,
                        first_image: previous,
                        second_image: final_state,
                    }));
                }
            } else {
                images[source] = Some(final_state);
                representatives[source] = Some(word.clone());
            }
            for d in 0..self.alphabet_size {
                let next = (
                    memory.transitions()[source][d],
                    self.transitions[control][d],
                    run(memory, output, &self.outputs[control][d])?,
                );
                if let std::collections::btree_map::Entry::Vacant(entry) = histories.entry(next) {
                    let mut extended = word.clone();
                    extended.push(d);
                    entry.insert(extended);
                    pending.push_back(next);
                }
            }
        }
        Ok(HistoryDescent::Descends(HistoryStateMap {
            images,
            reachable_product_states: histories.len(),
        }))
    }
    /// Exact O2 profile-kernel noncongruence witness over all input histories.
    pub fn profile_noncongruence(
        &self,
        memory: &FiniteMoore,
        start: usize,
    ) -> Result<Option<ProfileNoncongruenceWitness>, HistoryError> {
        if memory.input_count() != self.alphabet_size {
            return Err(HistoryError::InvalidAlphabet);
        }
        if start >= memory.state_count() {
            return Err(HistoryError::InvalidInitialState);
        }
        let first = (
            start,
            self.initial,
            run(memory, start, &self.initial_output)?,
        );
        let mut histories = BTreeMap::from([(first, vec![])]);
        let mut pending = VecDeque::from([first]);
        let mut profile_images: BTreeMap<usize, (usize, Vec<usize>)> = BTreeMap::new();
        while let Some((source, control, output)) = pending.pop_front() {
            let word = histories[&(source, control, output)].clone();
            let final_state = run(memory, output, &self.final_outputs[control])?;
            let source_profile = memory.reports()[source];
            let target_profile = memory.reports()[final_state];
            if let Some((previous, representative)) = profile_images.get(&source_profile) {
                if *previous != target_profile {
                    return Ok(Some((representative.clone(), word)));
                }
            } else {
                profile_images.insert(source_profile, (target_profile, word.clone()));
            }
            for d in 0..self.alphabet_size {
                let next = (
                    memory.transitions()[source][d],
                    self.transitions[control][d],
                    run(memory, output, &self.outputs[control][d])?,
                );
                if let std::collections::btree_map::Entry::Vacant(entry) = histories.entry(next) {
                    let mut next_word = word.clone();
                    next_word.push(d);
                    entry.insert(next_word);
                    pending.push_back(next);
                }
            }
        }
        Ok(None)
    }
    pub fn verify_descent(
        &self,
        memory: &FiniteMoore,
        start: usize,
        candidate: &HistoryDescent,
    ) -> Result<(), HistoryError> {
        if *candidate != self.descend(memory, start)? {
            return Err(HistoryError::InvalidCertificate);
        }
        Ok(())
    }
}
impl HistoryContext for FiniteWordTransducer {
    fn apply(&self, word: &[usize]) -> Result<Vec<usize>, HistoryError> {
        let mut output = self.initial_output.clone();
        let mut state = self.initial;
        for &d in word {
            if d >= self.alphabet_size {
                return Err(HistoryError::InvalidWord);
            }
            output.extend_from_slice(&self.outputs[state][d]);
            state = self.transitions[state][d];
        }
        output.extend_from_slice(&self.final_outputs[state]);
        Ok(output)
    }
}

pub fn run(memory: &FiniteMoore, start: usize, word: &[usize]) -> Result<usize, HistoryError> {
    if start >= memory.state_count() {
        return Err(HistoryError::InvalidInitialState);
    }
    let mut state = start;
    for &d in word {
        if d >= memory.input_count() {
            return Err(HistoryError::InvalidWord);
        }
        state = memory.transitions()[state][d];
    }
    Ok(state)
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct HistoryStateMap {
    pub images: Vec<Option<usize>>,
    pub reachable_product_states: usize,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct HistoryCollision {
    pub first: Vec<usize>,
    pub second: Vec<usize>,
    pub source_state: usize,
    pub first_image: usize,
    pub second_image: usize,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum HistoryDescent {
    Descends(HistoryStateMap),
    Obstructed(HistoryCollision),
}

/// Reachable-state context lifts to an action on every finite history iff all
/// context images of reachable states are reachable. The chosen representative
/// history is explicit; no chronology or report equality is used to invent it.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct StateContextLift {
    memory: FiniteMoore,
    start: usize,
    action: Vec<usize>,
    representatives: Vec<Option<Vec<usize>>>,
}
impl StateContextLift {
    pub fn new(
        memory: FiniteMoore,
        start: usize,
        action: Vec<usize>,
    ) -> Result<Self, HistoryError> {
        let n = memory.state_count();
        if start >= n {
            return Err(HistoryError::InvalidInitialState);
        }
        if action.len() != n || action.iter().any(|&x| x >= n) {
            return Err(HistoryError::InvalidTransducer);
        }
        let mut representatives = vec![None; n];
        representatives[start] = Some(vec![]);
        let mut pending = VecDeque::from([start]);
        while let Some(x) = pending.pop_front() {
            for d in 0..memory.input_count() {
                let y = memory.transitions()[x][d];
                if representatives[y].is_none() {
                    let mut word = representatives[x]
                        .clone()
                        .ok_or(HistoryError::InvalidCertificate)?;
                    word.push(d);
                    representatives[y] = Some(word);
                    pending.push_back(y);
                }
            }
        }
        if (0..n).any(|x| representatives[x].is_some() && representatives[action[x]].is_none()) {
            return Err(HistoryError::UnavailableContext);
        }
        Ok(Self {
            memory,
            start,
            action,
            representatives,
        })
    }
    pub fn reachable_representatives(&self) -> &[Option<Vec<usize>>] {
        &self.representatives
    }
    pub fn action(&self) -> &[usize] {
        &self.action
    }
}
impl HistoryContext for StateContextLift {
    fn apply(&self, word: &[usize]) -> Result<Vec<usize>, HistoryError> {
        let state = run(&self.memory, self.start, word)?;
        self.representatives[self.action[state]]
            .clone()
            .ok_or(HistoryError::UnavailableContext)
    }
}

}
'''
TESTS=r'''
fn same<A:std::fmt::Debug,B:std::fmt::Debug>(a:A,b:B){assert_eq!(format!("{a:?}"),format!("{b:?}"));}
fn words(k:usize,bound:usize)->Vec<Vec<usize>>{let mut all=vec![vec![]];let mut layer=vec![vec![]];for _ in 0..bound{let mut next=vec![];for prefix in &layer{for d in 0..k{let mut w=prefix.clone();w.push(d);next.push(w);}}all.extend(next.clone());layer=next;}all}
fn oracle_run(m:&FiniteMoore,start:usize,w:&[usize])->usize{w.iter().fold(start,|x,&d|m.transitions()[x][d])}
fn emitted(t:&FiniteWordTransducer,w:&[usize])->Vec<usize>{let mut state=t.initial;let mut out=t.initial_output.clone();for &d in w{out.extend(t.outputs[state][d].iter().copied());state=t.transitions[state][d];}out.extend(t.final_outputs[state].iter().copied());out}
fn record(t:&FiniteWordTransducer,m:&FiniteMoore,start:usize,w:&[usize])->((usize,usize,usize),usize){let mut source=start;let mut control=t.initial;let mut output=oracle_run(m,start,&t.initial_output);for &d in w{source=m.transitions()[source][d];output=oracle_run(m,output,&t.outputs[control][d]);control=t.transitions[control][d];}((source,control,output),oracle_run(m,output,&t.final_outputs[control]))}
fn expected(t:&FiniteWordTransducer,m:&FiniteMoore,start:usize)->(HistoryDescent,Option<ProfileNoncongruenceWitness>){let bound=m.state_count()*m.state_count()*t.state_count()-1;let mut records=vec![];let mut seen=vec![];for w in words(t.alphabet_size(),bound){let(triple,image)=record(t,m,start,&w);assert_eq!(oracle_run(m,start,&emitted(t,&w)),image);assert_eq!(t.apply(&w).unwrap(),emitted(t,&w));assert_eq!(run(m,start,&w).unwrap(),triple.0);if !seen.contains(&triple){seen.push(triple);records.push((triple,image,w));}}let mut images=vec![None;m.state_count()];let mut representatives:Vec<Option<Vec<usize>>>=vec![None;m.state_count()];let mut state_result=None;let mut profile_result=None;let mut profiles:Vec<(usize,usize,Vec<usize>)>=vec![];for((source,_,_),image,w)in &records{if state_result.is_none(){if let Some(previous)=images[*source]{if previous!=*image{state_result=Some(HistoryDescent::Obstructed(HistoryCollision{first:representatives[*source].clone().unwrap(),second:w.clone(),source_state:*source,first_image:previous,second_image:*image}));}}else{images[*source]=Some(*image);representatives[*source]=Some(w.clone());}}if profile_result.is_none(){let a=m.reports()[*source];let b=m.reports()[*image];if let Some((_,prior,first))=profiles.iter().find(|(p,_,_)|*p==a){if *prior!=b{profile_result=Some((first.clone(),w.clone()));}}else{profiles.push((a,b,w.clone()));}}}let descent=state_result.unwrap_or(HistoryDescent::Descends(HistoryStateMap{images,reachable_product_states:records.len()}));(descent,profile_result)}
fn old(t:&FiniteWordTransducer)->frozen::FiniteWordTransducer{frozen::FiniteWordTransducer::new(t.alphabet_size,t.initial,t.transitions.clone(),t.outputs.clone(),t.initial_output.clone(),t.final_outputs.clone()).unwrap()}
fn check(t:&FiniteWordTransducer,m:&FiniteMoore,start:usize){let(a,b)=expected(t,m,start);let actual=t.descend(m,start).unwrap();assert_eq!(actual,a);assert_eq!(t.profile_noncongruence(m,start).unwrap(),b);same(&actual,old(t).descend(m,start).unwrap());same(&b,old(t).profile_noncongruence(m,start).unwrap());assert_eq!(t.verify_descent(m,start,&actual),Ok(()));let mut bad=actual.clone();match &mut bad{HistoryDescent::Descends(map)=>map.reachable_product_states+=1,HistoryDescent::Obstructed(c)=>c.second.push(usize::MAX)}assert_eq!(t.verify_descent(m,start,&bad),Err(HistoryError::InvalidCertificate));for w in words(t.alphabet_size,2){same(t.apply(&w),frozen::HistoryContext::apply(&old(t),&w));}}
fn memory(k:usize,reports:usize,mut code:usize)->FiniteMoore{FiniteMoore::new((0..2).map(|i|(reports>>i)&1).collect(),(0..2).map(|_|(0..k).map(|_|{let n=code%2;code/=2;n}).collect()).collect(),k).unwrap()}
fn transducer(k:usize,n:usize,seed:usize)->FiniteWordTransducer{let fragments=if k==1{vec![vec![],vec![0],vec![0,0]]}else{vec![vec![],vec![0],vec![1],vec![0,1],vec![1,0]]};let f=|i:usize|fragments[i%fragments.len()].clone();FiniteWordTransducer::new(k,seed%n,(0..n).map(|s|(0..k).map(|d|(seed>>(s*k+d))%n).collect()).collect(),(0..n).map(|s|(0..k).map(|d|f(seed+s*k+d)).collect()).collect(),f(seed/2),(0..n).map(|s|f(seed+s+1)).collect()).unwrap()}
#[test]fn complete_product_states_from_independent_word_enumeration(){for k in 1..=2{for reports in 0..4{for transitions in 0..1usize<<(2*k){let m=memory(k,reports,transitions);for controls in 1..=2{for seed in 0..8{let t=transducer(k,controls,seed);for start in 0..2{check(&t,&m,start);}}}}}}
 let m=FiniteMoore::new(vec![usize::MAX,0],vec![vec![],vec![]],0).unwrap();for t in [FiniteWordTransducer::substitution(vec![]).unwrap(),FiniteWordTransducer::prefix(0,vec![]).unwrap(),FiniteWordTransducer::suffix(0,vec![]).unwrap()]{check(&t,&m,1);}
}
fn representatives(m:&FiniteMoore,start:usize)->Vec<Option<Vec<usize>>>{let mut reps=vec![None;m.state_count()];for w in words(m.input_count(),m.state_count()-1){let x=oracle_run(m,start,&w);if reps[x].is_none(){reps[x]=Some(w);}}reps}
#[test]fn lift_reachable_actions_helpers_and_admission_boundaries(){for k in 0..=2{for reports in 0..4{for transitions in 0..1usize<<(2*k){let m=memory(k,reports,transitions);for start in 0..2{let reps=representatives(&m,start);for code in 0..4{let action=vec![code&1,(code>>1)&1];let allowed=(0..2).all(|x|reps[x].is_none()||reps[action[x]].is_some());let result=StateContextLift::new(m.clone(),start,action.clone());assert_eq!(result.is_ok(),allowed);same(&result,frozen::StateContextLift::new(m.clone(),start,action.clone()));if let Ok(lift)=result{assert_eq!(lift.action(),action);assert_eq!(lift.reachable_representatives(),reps);for w in words(k,3){assert_eq!(lift.apply(&w).unwrap(),reps[action[oracle_run(&m,start,&w)]].clone().unwrap());}assert_eq!(lift.apply(&[k]),Err(HistoryError::InvalidWord));}}}}}}
 let m=memory(2,0,6);for images in [vec![vec![],vec![]],vec![vec![1,0],vec![0,1]]]{let t=FiniteWordTransducer::substitution(images.clone()).unwrap();for w in words(2,3){assert_eq!(t.apply(&w).unwrap(),w.iter().flat_map(|&d|images[d].clone()).collect::<Vec<_>>());}}for prefix in [vec![],vec![1,0]]{let t=FiniteWordTransducer::prefix(2,prefix.clone()).unwrap();let u=FiniteWordTransducer::suffix(2,prefix.clone()).unwrap();for w in words(2,3){assert_eq!(t.apply(&w).unwrap(),prefix.iter().chain(&w).copied().collect::<Vec<_>>());assert_eq!(u.apply(&w).unwrap(),w.iter().chain(&prefix).copied().collect::<Vec<_>>());}}
 for(k,initial,tr,out,head,tail)in[(1,0,vec![],vec![],vec![],vec![]),(1,1,vec![vec![0]],vec![vec![vec![]]],vec![],vec![vec![]]),(1,0,vec![vec![1]],vec![vec![vec![]]],vec![],vec![vec![]]),(1,0,vec![vec![]],vec![vec![vec![]]],vec![],vec![vec![]]),(1,0,vec![vec![0]],vec![],vec![],vec![vec![]]),(1,0,vec![vec![0]],vec![vec![]],vec![],vec![vec![]]),(1,0,vec![vec![0]],vec![vec![vec![1]]],vec![],vec![vec![]]),(1,0,vec![vec![0]],vec![vec![vec![]]],vec![1],vec![vec![]]),(1,0,vec![vec![0]],vec![vec![vec![]]],vec![],vec![vec![1]]),(1,0,vec![vec![0]],vec![vec![vec![]]],vec![],vec![])]{assert_eq!(FiniteWordTransducer::new(k,initial,tr,out,head,tail),Err(HistoryError::InvalidTransducer));}
 let t=FiniteWordTransducer::prefix(1,vec![]).unwrap();assert_eq!(t.apply(&[1]),Err(HistoryError::InvalidWord));assert_eq!(t.descend(&m,usize::MAX),Err(HistoryError::InvalidAlphabet));let t=FiniteWordTransducer::prefix(2,vec![]).unwrap();assert_eq!(t.descend(&m,2),Err(HistoryError::InvalidInitialState));assert_eq!(t.profile_noncongruence(&m,2),Err(HistoryError::InvalidInitialState));assert_eq!(run(&m,2,&[2]),Err(HistoryError::InvalidInitialState));assert_eq!(run(&m,0,&[2]),Err(HistoryError::InvalidWord));assert_eq!(StateContextLift::new(m.clone(),2,vec![0,1]),Err(HistoryError::InvalidInitialState));assert_eq!(StateContextLift::new(m.clone(),0,vec![]),Err(HistoryError::InvalidTransducer));assert_eq!(StateContextLift::new(m.clone(),0,vec![0,2]),Err(HistoryError::InvalidTransducer));
}
#[test]fn long_unsampled_history_collision_reconstructs_only_witnesses(){let mut frontier=ProductSearch::new((0,0,0));frontier.admit((1,0,0),0,1);frontier.admit((2,0,0),1,0);assert_eq!(frontier.word(2),vec![1,0]);let n=5000;let m=FiniteMoore::new((0..n).collect(),(0..n).map(|x|vec![(x+1)%n]).collect(),1).unwrap();let t=FiniteWordTransducer::new(1,0,vec![vec![1],vec![0]],vec![vec![vec![0]],vec![vec![]]],vec![],vec![vec![],vec![]]).unwrap();let first=vec![];let second=vec![0;n];assert_eq!(t.descend(&m,0).unwrap(),HistoryDescent::Obstructed(HistoryCollision{first:first.clone(),second:second.clone(),source_state:0,first_image:0,second_image:n/2}));assert_eq!(t.profile_noncongruence(&m,0).unwrap(),Some((first,second.clone())));assert_eq!(t.apply(&second).unwrap().len(),n/2);}

'''

def challenge(subject):
    return '\n#[cfg(test)]mod independent_history_context_tests{use super::*;\n'+FROZEN+TESTS+'\n}\n'
