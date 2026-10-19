"""AuthorityEffect: None. Complete small equivalence enumeration/least congruent upper bound,exact checked-arrow and comma factor laws;frozen original reference."""
FROZEN=r'''mod frozen {
//! Finite contextual systems, checked morphisms and relation-coarsening reflection.
//! AuthorityEffect: None. No authority or report-reflecting completion is claimed.
//!
//! Objects have a total action for each fixed context label and a profile
//! equivalence. Morphisms commute with actions and preserve that equivalence.
//! The full subcategory Cong consists of action-stable equivalences. Closing
//! an equivalence upward under actions gives a reflector with identity carrier
//! unit, initial in (S down-arrow Cong). It can merge previously distinct
//! profiles. A profile-reflecting unit into Cong cannot repair noncongruence.
use crate::finite_moore::{FiniteMoore, MooreError};

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ContextError {
    Carrier(MooreError),
    InvalidMap,
    ContextCountMismatch,
    ProfileNotPreserved,
    ActionNotPreserved,
    WrongDomain,
    TargetNotCongruent,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ContextSystem {
    model: FiniteMoore,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct ContextWitness {
    pub left: usize,
    pub right: usize,
    pub context: usize,
}

impl ContextSystem {
    pub fn new(
        profiles: Vec<usize>,
        transitions: Vec<Vec<usize>>,
        context_count: usize,
    ) -> Result<Self, ContextError> {
        Ok(Self {
            model: FiniteMoore::new(profiles, transitions, context_count)
                .map_err(ContextError::Carrier)?,
        })
    }
    pub fn state_count(&self) -> usize {
        self.model.state_count()
    }
    pub fn context_count(&self) -> usize {
        self.model.input_count()
    }
    pub fn profiles(&self) -> &[usize] {
        self.model.reports()
    }
    pub fn transitions(&self) -> &[Vec<usize>] {
        self.model.transitions()
    }
    pub fn related(&self, x: usize, y: usize) -> bool {
        x < self.state_count() && y < self.state_count() && self.profiles()[x] == self.profiles()[y]
    }
    pub fn check_witness(&self, witness: &ContextWitness) -> bool {
        let (x, y, c) = (witness.left, witness.right, witness.context);
        c < self.context_count()
            && self.related(x, y)
            && !self.related(self.transitions()[x][c], self.transitions()[y][c])
    }
    pub fn obstruction(&self) -> Option<ContextWitness> {
        for x in 0..self.state_count() {
            for y in 0..x {
                for c in 0..self.context_count() {
                    let witness = ContextWitness {
                        left: x,
                        right: y,
                        context: c,
                    };
                    if self.check_witness(&witness) {
                        return Some(witness);
                    }
                }
            }
        }
        None
    }
    pub fn is_congruent(&self) -> bool {
        self.obstruction().is_none()
    }
}

/// Typed checked arrow. No caller can replace its domain, codomain or map.
#[derive(Debug, Clone)]
pub struct ContextHom<'a> {
    source: &'a ContextSystem,
    target: &'a ContextSystem,
    map: Vec<usize>,
}
impl<'a> ContextHom<'a> {
    pub fn new(
        source: &'a ContextSystem,
        target: &'a ContextSystem,
        map: Vec<usize>,
    ) -> Result<Self, ContextError> {
        if source.context_count() != target.context_count() {
            return Err(ContextError::ContextCountMismatch);
        }
        if map.len() != source.state_count() || map.iter().any(|&v| v >= target.state_count()) {
            return Err(ContextError::InvalidMap);
        }
        for x in 0..source.state_count() {
            for y in 0..source.state_count() {
                if source.related(x, y) && !target.related(map[x], map[y]) {
                    return Err(ContextError::ProfileNotPreserved);
                }
            }
            for c in 0..source.context_count() {
                if map[source.transitions()[x][c]] != target.transitions()[map[x]][c] {
                    return Err(ContextError::ActionNotPreserved);
                }
            }
        }
        Ok(Self {
            source,
            target,
            map,
        })
    }
    pub fn source(&self) -> &ContextSystem {
        self.source
    }
    pub fn target(&self) -> &ContextSystem {
        self.target
    }
    pub fn map(&self) -> &[usize] {
        &self.map
    }
    pub fn identity(system: &'a ContextSystem) -> Result<Self, ContextError> {
        Self::new(system, system, (0..system.state_count()).collect())
    }
    pub fn then(&self, next: &Self) -> Result<Self, ContextError> {
        if self.target != next.source {
            return Err(ContextError::WrongDomain);
        }
        Self::new(
            self.source,
            next.target,
            self.map.iter().map(|&v| next.map[v]).collect(),
        )
    }
    pub fn reflects_profiles(&self) -> bool {
        (0..self.source.state_count()).all(|x| {
            (0..self.source.state_count()).all(|y| {
                !self.target.related(self.map[x], self.map[y]) || self.source.related(x, y)
            })
        })
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CongruenceReflection {
    source: ContextSystem,
    completed: ContextSystem,
    chain: Vec<Vec<usize>>,
}

fn canonicalize(labels: &[usize]) -> Vec<usize> {
    let mut representatives = Vec::new();
    labels
        .iter()
        .map(|label| {
            if let Some(i) = representatives.iter().position(|old| old == label) {
                i
            } else {
                representatives.push(*label);
                representatives.len() - 1
            }
        })
        .collect()
}
fn merge(labels: &mut [usize], x: usize, y: usize) {
    let from = labels[y];
    let to = labels[x];
    for label in labels {
        if *label == from {
            *label = to;
        }
    }
}

impl CongruenceReflection {
    /// Least stable equivalence above the given profile equivalence. Every
    /// strict round merges at least two blocks, hence at most n-1 strict rounds.
    pub fn new(source: &ContextSystem) -> Result<Self, ContextError> {
        let mut labels = canonicalize(source.profiles());
        let mut chain = vec![labels.clone()];
        loop {
            let old = labels.clone();
            for x in 0..source.state_count() {
                for y in 0..x {
                    if old[x] == old[y] {
                        for c in 0..source.context_count() {
                            merge(
                                &mut labels,
                                source.transitions()[x][c],
                                source.transitions()[y][c],
                            );
                        }
                    }
                }
            }
            labels = canonicalize(&labels);
            if labels == old {
                break;
            }
            chain.push(labels.clone());
        }
        let completed = ContextSystem::new(
            labels,
            source.transitions().to_vec(),
            source.context_count(),
        )?;
        Ok(Self {
            source: source.clone(),
            completed,
            chain,
        })
    }
    pub fn source(&self) -> &ContextSystem {
        &self.source
    }
    pub fn completed(&self) -> &ContextSystem {
        &self.completed
    }
    pub fn chain(&self) -> &[Vec<usize>] {
        &self.chain
    }
    pub fn unit(&self) -> Result<ContextHom<'_>, ContextError> {
        ContextHom::new(
            &self.source,
            &self.completed,
            (0..self.source.state_count()).collect(),
        )
    }
    /// Given an object (T,f:S->T) of the comma category S↓Cong, construct its
    /// unique arrow from (R(S),eta). Relation-preservation is independently
    /// checked on the saturated relation; no trust in a claimed factor flag.
    pub fn factor<'a>(&'a self, arrow: &ContextHom<'a>) -> Result<ContextHom<'a>, ContextError> {
        if arrow.source != &self.source {
            return Err(ContextError::WrongDomain);
        }
        if !arrow.target.is_congruent() {
            return Err(ContextError::TargetNotCongruent);
        }
        ContextHom::new(&self.completed, arrow.target, arrow.map.clone())
    }
    /// Check the actual comma triangle for a candidate factor. Since eta is
    /// identity on carriers, two accepted factors have exactly the same map.
    pub fn is_factor(&self, arrow: &ContextHom<'_>, candidate: &ContextHom<'_>) -> bool {
        arrow.source == &self.source
            && arrow.target.is_congruent()
            && candidate.source == &self.completed
            && candidate.target == arrow.target
            && candidate.map == arrow.map
    }
}

/// The reflector's action on arrows, with endpoints checked against both units.
pub fn reflect_arrow<'a>(
    source: &'a CongruenceReflection,
    target: &'a CongruenceReflection,
    arrow: &ContextHom<'_>,
) -> Result<ContextHom<'a>, ContextError> {
    if arrow.source != source.source() || arrow.target != target.source() {
        return Err(ContextError::WrongDomain);
    }
    ContextHom::new(source.completed(), target.completed(), arrow.map.clone())
}

}
'''
TESTS=r'''
fn same<A:std::fmt::Debug,B:std::fmt::Debug>(a:A,b:B){assert_eq!(format!("{a:?}"),format!("{b:?}"));}
fn canon(labels:&[usize])->Vec<usize>{let mut unique=vec![];labels.iter().map(|v|if let Some(i)=unique.iter().position(|x|x==v){i}else{unique.push(*v);unique.len()-1}).collect()}
fn partitions(n:usize)->Vec<Vec<usize>>{let mut all=vec![];for mut code in 0..n.pow(n as u32){let labels:Vec<_>=(0..n).map(|_|{let v=code%n;code/=n;v}).collect();let p=canon(&labels);if !all.contains(&p){all.push(p);}}all}
fn congruent(labels:&[usize],actions:&[Vec<usize>])->bool{(0..labels.len()).all(|x|(0..labels.len()).all(|y|labels[x]!=labels[y]||(0..actions[x].len()).all(|i|labels[actions[x][i]]==labels[actions[y][i]])))}
fn inclusion(a:&[usize],b:&[usize])->bool{(0..a.len()).all(|x|(0..a.len()).all(|y|a[x]!=a[y]||b[x]==b[y]))}
fn expected(s:&ContextSystem,all:&[Vec<usize>])->Vec<usize>{let valid:Vec<_>=all.iter().filter(|p|inclusion(s.profiles(),p)&&congruent(p,s.transitions())).collect();assert!(!valid.is_empty());let mut ids=vec![];let mut next=0;for x in 0..s.state_count(){if let Some(y)=(0..x).find(|&y|valid.iter().all(|p|p[x]==p[y])){ids.push(ids[y]);}else{ids.push(next);next+=1;}}ids}
fn old(s:&ContextSystem)->frozen::ContextSystem{frozen::ContextSystem::new(s.profiles().to_vec(),s.transitions().to_vec(),s.context_count()).unwrap()}
fn check(s:&ContextSystem,all:&[Vec<usize>]){let r=CongruenceReflection::new(s).unwrap();let prior=frozen::CongruenceReflection::new(&old(s)).unwrap();same(&r,&prior);assert_eq!(r.completed().profiles(),expected(s,all));assert_eq!(r.source(),s);assert_eq!(r.completed().transitions(),s.transitions());assert!(congruent(r.completed().profiles(),r.completed().transitions()));assert_eq!(r.chain().first().unwrap(),&canon(s.profiles()));assert_eq!(r.chain().last().unwrap(),r.completed().profiles());assert!(r.chain().len()<=s.state_count());for w in r.chain().windows(2){assert!(inclusion(&w[0],&w[1]));assert_ne!(w[0],w[1]);}let expected_obstruction=(0..s.state_count()).flat_map(|x|(0..x).flat_map(move|y|(0..s.context_count()).map(move|context|ContextWitness{left:x,right:y,context}))).find(|w|s.profiles()[w.left]==s.profiles()[w.right]&&s.profiles()[s.transitions()[w.left][w.context]]!=s.profiles()[s.transitions()[w.right][w.context]]);assert_eq!(s.obstruction(),expected_obstruction);assert_eq!(s.is_congruent(),congruent(s.profiles(),s.transitions()));if let Some(w)=s.obstruction(){assert!(s.check_witness(&w));}let unit=r.unit().unwrap();assert_eq!(unit.map(),(0..s.state_count()).collect::<Vec<_>>());assert_eq!(unit.reflects_profiles(),s.is_congruent());let factor=r.factor(&unit).unwrap();assert!(r.is_factor(&unit,&factor));assert_eq!(factor.map(),unit.map());let twice=CongruenceReflection::new(r.completed()).unwrap();assert_eq!(twice.completed().profiles(),r.completed().profiles());assert_eq!(twice.chain().len(),1);let id=ContextHom::identity(s).unwrap();assert_eq!(reflect_arrow(&r,&r,&id).unwrap().map(),id.map());assert_eq!(r.chain().as_ptr(),r.chain.as_ptr());assert!(std::ptr::eq(r.source(),&r.source));assert!(std::ptr::eq(r.completed(),&r.completed));}
fn system(n:usize,k:usize,labels:Vec<usize>,mut code:usize)->ContextSystem{ContextSystem::new(labels,(0..n).map(|_|(0..k).map(|_|{let x=code%n;code/=n;x}).collect()).collect(),k).unwrap()}
#[test]fn least_congruent_coarsening_by_complete_partition_enumeration(){for(n,k)in[(3usize,1usize),(3,2),(4,1)]{let all=partitions(n);for labels in &all{for code in 0..n.pow((n*k)as u32){let s=system(n,k,labels.clone(),code);check(&s,&all);}}}let all=partitions(3);let sparse=system(3,1,vec![usize::MAX,usize::MAX,2],15);check(&sparse,&all);for labels in &all{check(&system(3,0,labels.clone(),0),&all);}}
fn admission(s:&ContextSystem,t:&ContextSystem,map:&[usize])->Result<(),ContextError>{if s.context_count()!=t.context_count(){return Err(ContextError::ContextCountMismatch)}if map.len()!=s.state_count()||map.iter().any(|&x|x>=t.state_count()){return Err(ContextError::InvalidMap)}for x in 0..s.state_count(){for y in 0..s.state_count(){if s.profiles()[x]==s.profiles()[y]&&t.profiles()[map[x]]!=t.profiles()[map[y]]{return Err(ContextError::ProfileNotPreserved)}}for c in 0..s.context_count(){if map[s.transitions()[x][c]]!=t.transitions()[map[x]][c]{return Err(ContextError::ActionNotPreserved)}}}Ok(())}
#[test]fn checked_morphisms_reflector_arrows_and_unique_comma_factors(){let systems:Vec<_>=(0..4).flat_map(|r|(0..4).map(move|code|system(2,1,vec![r&1,(r>>1)&1],code))).collect();let reflections:Vec<_>=systems.iter().map(|s|CongruenceReflection::new(s).unwrap()).collect();for(a,s)in systems.iter().enumerate(){let identity=ContextHom::identity(s).unwrap();assert!(std::ptr::eq(identity.source(),s));assert!(std::ptr::eq(identity.target(),s));assert_eq!(identity.map().as_ptr(),identity.map.as_ptr());for(b,t)in systems.iter().enumerate(){let os=old(s);let ot=old(t);for code in 0..4{let map=vec![code&1,(code>>1)&1];let arrow=ContextHom::new(s,t,map.clone());assert_eq!(arrow.as_ref().map(|_|()).map_err(Clone::clone),admission(s,t,&map));same(&arrow,frozen::ContextHom::new(&os,&ot,map.clone()));let f=match arrow{Ok(f)=>f,Err(_)=>continue};let reflected=reflect_arrow(&reflections[a],&reflections[b],&f).unwrap();assert_eq!(reflected.map(),map);assert_eq!(f.reflects_profiles(),(0..2).all(|x|(0..2).all(|y|t.profiles()[map[x]]!=t.profiles()[map[y]]||s.profiles()[x]==s.profiles()[y])));assert_eq!(identity.then(&f).unwrap().map(),f.map());assert_eq!(f.then(&ContextHom::identity(t).unwrap()).unwrap().map(),f.map());let left=f.then(&reflections[b].unit().unwrap()).unwrap();let right=reflections[a].unit().unwrap().then(&reflected).unwrap();assert_eq!(left.map(),right.map());if t.is_congruent(){let factor=reflections[a].factor(&f).unwrap();assert_eq!(factor.map(),map);assert!(reflections[a].is_factor(&f,&factor));for other in 0..4{if let Ok(candidate)=ContextHom::new(reflections[a].completed(),t,vec![other&1,(other>>1)&1]){assert_eq!(reflections[a].is_factor(&f,&candidate),candidate.map()==map);}}}else{assert!(matches!(reflections[a].factor(&f),Err(ContextError::TargetNotCongruent)));}
 for(c,u)in systems.iter().enumerate(){for next in 0..4{if let Ok(g)=ContextHom::new(t,u,vec![next&1,(next>>1)&1]){let composite=f.then(&g).unwrap();assert_eq!(composite.map(),map.iter().map(|&x|g.map()[x]).collect::<Vec<_>>());let lhs=reflect_arrow(&reflections[a],&reflections[c],&composite).unwrap();let rg=reflect_arrow(&reflections[b],&reflections[c],&g).unwrap();assert_eq!(lhs.map(),reflected.then(&rg).unwrap().map());}}}
 }}}}
#[test]fn typed_boundaries_value_contexts_and_reflection_ceiling(){assert!(matches!(ContextSystem::new(vec![],vec![],0),Err(ContextError::Carrier(_))));let s=system(2,1,vec![0,0],2);let t=system(2,1,vec![0,1],2);let zero=system(2,0,vec![0,0],0);assert!(matches!(ContextHom::new(&s,&zero,vec![]),Err(ContextError::ContextCountMismatch)));assert!(matches!(ContextHom::new(&s,&s,vec![]),Err(ContextError::InvalidMap)));assert!(matches!(ContextHom::new(&s,&s,vec![0,2]),Err(ContextError::InvalidMap)));assert!(matches!(ContextHom::new(&s,&s,vec![usize::MAX,0]),Err(ContextError::InvalidMap)));assert!(!s.related(2,0));assert!(!s.related(0,usize::MAX));for w in [ContextWitness{left:2,right:0,context:0},ContextWitness{left:0,right:0,context:1},ContextWitness{left:0,right:0,context:usize::MAX}]{assert!(!s.check_witness(&w));}let rs=CongruenceReflection::new(&s).unwrap();let rt=CongruenceReflection::new(&t).unwrap();let is=ContextHom::identity(&s).unwrap();let it=ContextHom::identity(&t).unwrap();assert!(matches!(is.then(&it),Err(ContextError::WrongDomain)));assert!(matches!(rs.factor(&it),Err(ContextError::WrongDomain)));assert!(matches!(reflect_arrow(&rs,&rt,&is),Err(ContextError::WrongDomain)));assert!(!rs.is_factor(&it,&it));let clone=s.clone();assert!(!std::ptr::eq(&s,&clone));assert!(is.then(&ContextHom::identity(&clone).unwrap()).is_ok());let renamed=system(2,1,vec![3,3],2);assert!(matches!(is.then(&ContextHom::identity(&renamed).unwrap()),Err(ContextError::WrongDomain)));let n1=system(1,1,vec![usize::MAX],0);assert!(ContextHom::new(&s,&n1,vec![0,0]).is_ok());let wrong_target=ContextHom::new(rs.completed(),&renamed,vec![0,1]).unwrap();assert!(!rs.is_factor(&is,&wrong_target));let wrong_arrow=ContextHom::identity(&renamed).unwrap();assert!(!rs.is_factor(&wrong_arrow,&wrong_target));let counter=system(3,1,vec![0,0,1],15);assert!(!counter.is_congruent());let r=CongruenceReflection::new(&counter).unwrap();assert!(r.completed().is_congruent());assert!(!r.unit().unwrap().reflects_profiles());let unit=r.unit().unwrap();assert!(!r.is_factor(&unit,&unit));}

'''

def challenge(subject):
    return '\n#[cfg(test)]mod independent_context_reflection_tests{use super::*;\n'+FROZEN+TESTS+'\n}\n'
