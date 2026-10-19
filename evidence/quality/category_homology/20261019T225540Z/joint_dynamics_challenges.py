"""AuthorityEffect: None. Independent Option-product greatest fixed point,BFS separators,linear relation lookup and frozen admission reference."""
FROZEN=r'''mod frozen {
//! Joint operations on an explicit relation of component states.
//! Local transitions must preserve the relation; missing pairs are NOT silently
//! interpreted as unavailable operations. Interaction tables are supplied premises.
use crate::finite_continuation::{ContinuationError, DistinguishingWord, PartialDynamics};
use crate::finite_moore::MooreQuotient;
use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum JointOperation {
    Left(usize),
    Right(usize),
    /// One target row (or genuine unavailability) per admitted pair.
    Interaction(Vec<Option<usize>>),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum JointDynamicsError {
    InvalidRelation,
    InvalidOperation,
    NotClosed {
        row: usize,
        operation: usize,
        target: (usize, usize),
    },
    WorkLimit,
    Dynamics(ContinuationError),
    CertificateMismatch,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct JointDynamicsAnalysis {
    /// Includes the separately labelled internal unavailable sink.
    pub refinement: MooreQuotient,
    /// None iff paired local classes preserve all joint futures/availability.
    pub collision: Option<DistinguishingWord>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct JointDynamics {
    pairs: Vec<(usize, usize)>,
    local_reports: Vec<(usize, usize)>,
    dynamics: PartialDynamics,
    pair_budget: usize,
}

fn refinement_cost(m: &PartialDynamics) -> Option<usize> {
    let n = m.reports().len().checked_add(1)?;
    n.checked_mul(n)?
        .checked_mul(m.transitions()[0].len().checked_add(1)?)
}

impl JointDynamics {
    pub fn new(
        left: &PartialDynamics,
        right: &PartialDynamics,
        pairs: Vec<(usize, usize)>,
        operations: &[JointOperation],
        max_cells: usize,
    ) -> Result<Self, JointDynamicsError> {
        let size = pairs
            .len()
            .checked_add(1)
            .ok_or(JointDynamicsError::WorkLimit)?;
        let pair_budget = size
            .checked_mul(size)
            .ok_or(JointDynamicsError::WorkLimit)?;
        let cost = pair_budget
            .checked_mul(
                operations
                    .len()
                    .checked_add(1)
                    .ok_or(JointDynamicsError::WorkLimit)?,
            )
            .and_then(|n| refinement_cost(left).and_then(|l| n.checked_add(l)))
            .and_then(|n| refinement_cost(right).and_then(|r| n.checked_add(r)));
        if cost.is_none_or(|n| n > max_cells) {
            return Err(JointDynamicsError::WorkLimit);
        }
        let ids: BTreeMap<_, _> = pairs
            .iter()
            .copied()
            .enumerate()
            .map(|(i, p)| (p, i))
            .collect();
        if pairs.is_empty()
            || ids.len() != pairs.len()
            || pairs
                .iter()
                .any(|&(l, r)| l >= left.reports().len() || r >= right.reports().len())
        {
            return Err(JointDynamicsError::InvalidRelation);
        }
        for op in operations {
            let valid = match op {
                JointOperation::Left(a) => *a < left.transitions()[0].len(),
                JointOperation::Right(a) => *a < right.transitions()[0].len(),
                JointOperation::Interaction(t) => {
                    t.len() == pairs.len() && t.iter().flatten().all(|&s| s < pairs.len())
                }
            };
            if !valid {
                return Err(JointDynamicsError::InvalidOperation);
            }
        }
        let mut transitions = Vec::new();
        for (row, &(l, r)) in pairs.iter().enumerate() {
            let mut next = Vec::new();
            for (operation, op) in operations.iter().enumerate() {
                let target = match op {
                    JointOperation::Left(a) => left.transitions()[l][*a].map(|t| (t, r)),
                    JointOperation::Right(a) => right.transitions()[r][*a].map(|t| (l, t)),
                    JointOperation::Interaction(t) => {
                        next.push(t[row]);
                        continue;
                    }
                };
                next.push(match target {
                    None => None,
                    Some(target) => {
                        Some(*ids.get(&target).ok_or(JointDynamicsError::NotClosed {
                            row,
                            operation,
                            target,
                        })?)
                    }
                });
            }
            transitions.push(next);
        }
        let lc = left.quotient().state_to_block;
        let rc = right.quotient().state_to_block;
        let local_reports: Vec<_> = pairs.iter().map(|&(l, r)| (lc[l], rc[r])).collect();
        let mut labels = BTreeMap::new();
        let reports = local_reports
            .iter()
            .map(|&p| {
                let id = labels.len();
                *labels.entry(p).or_insert(id)
            })
            .collect();
        let dynamics = PartialDynamics::new(reports, transitions, operations.len())
            .map_err(JointDynamicsError::Dynamics)?;
        Ok(Self {
            pairs,
            local_reports,
            dynamics,
            pair_budget,
        })
    }
    pub fn pairs(&self) -> &[(usize, usize)] {
        &self.pairs
    }
    pub fn local_reports(&self) -> &[(usize, usize)] {
        &self.local_reports
    }
    pub fn dynamics(&self) -> &PartialDynamics {
        &self.dynamics
    }

    pub fn analyze(&self) -> Result<JointDynamicsAnalysis, JointDynamicsError> {
        let refinement = self.dynamics.quotient();
        let mut collision = None;
        'outer: for r in 0..self.pairs.len() {
            for l in 0..r {
                if self.local_reports[l] == self.local_reports[r]
                    && refinement.state_to_block[l] != refinement.state_to_block[r]
                {
                    collision = self
                        .dynamics
                        .distinguish(l, r, self.pair_budget)
                        .map_err(JointDynamicsError::Dynamics)?;
                    break 'outer;
                }
            }
        }
        Ok(JointDynamicsAnalysis {
            refinement,
            collision,
        })
    }
    /// Recompute against the expected relation AND complete operation table.
    pub fn verify(&self, c: &JointDynamicsAnalysis) -> Result<(), JointDynamicsError> {
        if self.analyze()? == *c {
            Ok(())
        } else {
            Err(JointDynamicsError::CertificateMismatch)
        }
    }
}

}
'''
TESTS=r'''
fn same<A:std::fmt::Debug,B:std::fmt::Debug>(a:A,b:B){assert_eq!(format!("{a:?}"),format!("{b:?}"));}
fn classes(m:&PartialDynamics)->Vec<usize>{let n=m.reports().len();let k=m.transitions()[0].len();let answer=|x:usize|if x==n{None}else{Some(m.reports()[x])};let step=|x:usize,i:usize|if x==n{n}else{m.transitions()[x][i].unwrap_or(n)};let mut r:Vec<Vec<_>>=(0..=n).map(|x|(0..=n).map(|y|answer(x)==answer(y)).collect()).collect();loop{let before=r.clone();for x in 0..=n{for y in 0..=n{r[x][y]=before[x][y]&&(0..k).all(|i|before[step(x,i)][step(y,i)]);}}if r==before{break}}let mut ids=vec![];let mut fresh=0;for x in 0..=n{if let Some(y)=(0..x).find(|&y|r[x][y]){ids.push(ids[y]);}else{ids.push(fresh);fresh+=1;}}ids}
fn separator(m:&PartialDynamics,l:usize,r:usize)->Option<DistinguishingWord>{let answer=|x:Option<usize>|x.map(|x|m.reports()[x]);let step=|x:Option<usize>,i:usize|x.and_then(|x|m.transitions()[x][i]);let mut pending=std::collections::VecDeque::from([(Some(l),Some(r),vec![])]);let mut visited=std::collections::BTreeSet::new();while let Some((x,y,w))=pending.pop_front(){if !visited.insert((x,y)){continue}if answer(x)!=answer(y){return Some(DistinguishingWord{left:l,right:r,word:w,left_answer:answer(x),right_answer:answer(y)})}for i in 0..m.transitions()[0].len(){let mut next=w.clone();next.push(i);pending.push_back((step(x,i),step(y,i),next));}}None}
fn prior_ops(ops:&[JointOperation])->Vec<frozen::JointOperation>{ops.iter().map(|op|match op{JointOperation::Left(i)=>frozen::JointOperation::Left(*i),JointOperation::Right(i)=>frozen::JointOperation::Right(*i),JointOperation::Interaction(t)=>frozen::JointOperation::Interaction(t.clone())}).collect()}
fn cost(l:&PartialDynamics,r:&PartialDynamics,p:usize,ops:usize)->usize{let one=|m:&PartialDynamics|(m.reports().len()+1).pow(2)*(m.transitions()[0].len()+1);(p+1).pow(2)*(ops+1)+one(l)+one(r)}
fn expected(l:&PartialDynamics,r:&PartialDynamics,p:&[(usize,usize)],ops:&[JointOperation])->Result<(Vec<(usize,usize)>,Vec<usize>,Vec<Vec<Option<usize>>>),JointDynamicsError>{if p.is_empty()||p.iter().enumerate().any(|(i,v)|p[..i].contains(v))||p.iter().any(|&(a,b)|a>=l.reports().len()||b>=r.reports().len()){return Err(JointDynamicsError::InvalidRelation)}for op in ops{let good=match op{JointOperation::Left(i)=>*i<l.transitions()[0].len(),JointOperation::Right(i)=>*i<r.transitions()[0].len(),JointOperation::Interaction(t)=>t.len()==p.len()&&t.iter().all(|v|v.is_none_or(|v|v<p.len()))};if !good{return Err(JointDynamicsError::InvalidOperation)}}let mut table=vec![];for(row,&(a,b))in p.iter().enumerate(){let mut out=vec![];for(operation,op)in ops.iter().enumerate(){let target=match op{JointOperation::Left(i)=>l.transitions()[a][*i].map(|x|(x,b)),JointOperation::Right(i)=>r.transitions()[b][*i].map(|y|(a,y)),JointOperation::Interaction(t)=>{out.push(t[row]);continue}};let cell=match target{None=>None,Some(target)=>Some(p.iter().position(|v|*v==target).ok_or(JointDynamicsError::NotClosed{row,operation,target})?)};out.push(cell);}table.push(out);}let lc=classes(l);let rc=classes(r);let profiles:Vec<_>=p.iter().map(|&(a,b)|(lc[a],rc[b])).collect();let mut unique=vec![];let reports=profiles.iter().map(|v|if let Some(i)=unique.iter().position(|u|u==v){i}else{unique.push(*v);unique.len()-1}).collect();Ok((profiles,reports,table))}
fn check(l:&PartialDynamics,r:&PartialDynamics,p:Vec<(usize,usize)>,ops:Vec<JointOperation>){let max=cost(l,r,p.len(),ops.len());let oracle=expected(l,r,&p,&ops);let result=JointDynamics::new(l,r,p.clone(),&ops,max);let prior=frozen::JointDynamics::new(l,r,p.clone(),&prior_ops(&ops),max);same(&result,&prior);assert_eq!(result.is_ok(),oracle.is_ok());for budget in [0,max-1]{assert_eq!(JointDynamics::new(l,r,p.clone(),&ops,budget),Err(JointDynamicsError::WorkLimit));}let m=match(result,oracle){(Ok(m),Ok((profiles,reports,table)))=>{assert_eq!(m.pairs(),p);assert_eq!(m.local_reports(),profiles);assert_eq!(m.dynamics().reports(),reports);assert_eq!(m.dynamics().transitions(),table);m},(Err(a),Err(b))=>{assert_eq!(a,b);return},_=>unreachable!()};assert_eq!(m.pairs().as_ptr(),m.pairs.as_ptr());assert_eq!(m.local_reports().as_ptr(),m.local_reports.as_ptr());assert!(std::ptr::eq(m.dynamics(),&m.dynamics));let a=m.analyze().unwrap();same(&a,prior.unwrap().analyze().unwrap());let joint=classes(m.dynamics());assert_eq!(a.refinement.state_to_block,joint);let mut collision=None;for right in 0..p.len(){for left in 0..right{if m.local_reports()[left]==m.local_reports()[right]&&joint[left]!=joint[right]{collision=Some((left,right));break}}if collision.is_some(){break}}assert_eq!(a.collision,collision.and_then(|(x,y)|separator(m.dynamics(),x,y)));assert_eq!(m.verify(&a),Ok(()));let mut bad=a.clone();bad.refinement.partitions.clear();assert_eq!(m.verify(&bad),Err(JointDynamicsError::CertificateMismatch));if a.collision.is_some(){bad=a.clone();bad.collision=None;assert_eq!(m.verify(&bad),Err(JointDynamicsError::CertificateMismatch));}}
fn model(reports:usize,mut code:usize)->PartialDynamics{PartialDynamics::new((0..2).map(|i|(reports>>i)&1).collect(),(0..2).map(|_|{let i=code%3;code/=3;vec![if i==2{None}else{Some(i)}]}).collect(),1).unwrap()}
#[test]fn exhaustive_component_pairs_relations_and_exact_refusals(){for lr in 0..4{for lt in 0..9{let l=model(lr,lt);for rr in 0..4{for rt in 0..9{let r=model(rr,rt);for bits in 1..16{let p:Vec<_>=[(0,0),(0,1),(1,0),(1,1)].into_iter().enumerate().filter(|(i,_)|bits&(1<<i)!=0).map(|(_,v)|v).collect();check(&l,&r,p,vec![JointOperation::Left(0),JointOperation::Right(0)]);}}}}}}
#[test]fn interaction_tables_all_words_and_declaration_identity_ceiling(){let l=model(0,0);let r=model(0,0);for n in 1..=4usize{let p=[(0,0),(0,1),(1,0),(1,1)][..n].to_vec();for mut code in 0..(n+1).pow(n as u32){let mut table=vec![];for _ in 0..n{let x=code%(n+1);code/=n+1;table.push(if x==n{None}else{Some(x)});}check(&l,&r,p.clone(),vec![JointOperation::Interaction(table)]);}}
 let z=PartialDynamics::new(vec![0,0],vec![vec![],vec![]],0).unwrap();let one=PartialDynamics::new(vec![0],vec![vec![]],0).unwrap();check(&z,&one,vec![(0,0),(1,0)],vec![]);let a=JointDynamics::new(&z,&one,vec![(0,0)],&[],usize::MAX).unwrap();let b=JointDynamics::new(&z,&one,vec![(1,0)],&[],usize::MAX).unwrap();assert_ne!(a.pairs(),b.pairs());assert_eq!(a.verify(&b.analyze().unwrap()),Ok(()));
}
#[test]fn preflight_order_overflow_guards_and_invalid_tables(){let l=model(0,0);let r=model(0,0);for p in [vec![],vec![(0,0),(0,0)],vec![(2,0)],vec![(0,2)],vec![(usize::MAX,0)]]{check(&l,&r,p,vec![]);}for op in [JointOperation::Left(1),JointOperation::Right(1),JointOperation::Left(usize::MAX),JointOperation::Interaction(vec![]),JointOperation::Interaction(vec![None,None]),JointOperation::Interaction(vec![Some(1)]),JointOperation::Interaction(vec![Some(usize::MAX)])]{check(&l,&r,vec![(0,0)],vec![op]);}
 let move_left=model(0,4);let ops=[JointOperation::Left(0),JointOperation::Right(1)];assert_eq!(JointDynamics::new(&move_left,&r,vec![(0,0)],&ops,usize::MAX),Err(JointDynamicsError::InvalidOperation));assert_eq!(JointDynamics::new(&move_left,&r,vec![(0,0)],&ops,0),Err(JointDynamicsError::WorkLimit));
 for(p,o)in[(usize::MAX,0),(usize::MAX/2,0),(0,usize::MAX),(2,usize::MAX/2)]{assert_eq!(admit_work(&l,&r,p,o,usize::MAX),Err(JointDynamicsError::WorkLimit));}assert_eq!(admit_work(&l,&r,1,2,cost(&l,&r,1,2)),Ok(4));
}

'''

def challenge(subject):
    return '\n#[cfg(test)]mod independent_joint_dynamics_tests{use super::*;\n'+FROZEN+TESTS+'\n}\n'
