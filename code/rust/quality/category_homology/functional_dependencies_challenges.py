"""AuthorityEffect: None. Closed-superset FD oracle, full-tuple join oracle and frozen charging reference."""
FROZEN = r'''mod frozen {
//! Finite heading/FD decisions, separate from instance checks and authorization.
//! Exact equality and set relations only; no NULL, bag, MVD or join-dependency theory.

use serde::{Deserialize, Serialize};
use std::collections::BTreeSet;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct FunctionalDependency {
    pub determinant: u16,
    pub dependent: u16,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct FdSchema {
    pub arity: usize,
    pub dependencies: Vec<FunctionalDependency>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum FdRefusal {
    UnsupportedHeading,
    AttributeOutsideHeading,
    InvalidDecomposition,
    BudgetUnknown,
    InstanceShape,
    DuplicateTuple,
    InstanceDependencyViolation {
        dependency: usize,
        first: usize,
        second: usize,
    },
}
impl std::fmt::Display for FdRefusal {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{self:?}")
    }
}
impl std::error::Error for FdRefusal {}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ClosureWitness {
    pub input: u16,
    pub result: u16,
    pub applications: Vec<usize>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct BinaryDecompositionReport {
    pub intersection_closure: ClosureWitness,
    pub determined_component: Option<usize>,
    pub original_bcnf_violations: Vec<FunctionalDependency>,
    pub component_bcnf_violations: [Vec<FunctionalDependency>; 2],
    pub projected_dependencies: [Vec<FunctionalDependency>; 2],
    pub lost_dependencies: Vec<FunctionalDependency>,
    pub work_used: u64,
}

struct Work {
    used: u64,
    limit: u64,
}
impl Work {
    fn spend(&mut self) -> Result<(), FdRefusal> {
        if self.used == self.limit {
            return Err(FdRefusal::BudgetUnknown);
        }
        self.used += 1;
        Ok(())
    }
}

impl FdSchema {
    pub fn heading(&self) -> Result<u16, FdRefusal> {
        if self.arity == 0 || self.arity > 8 || self.dependencies.len() > 128 {
            return Err(FdRefusal::UnsupportedHeading);
        }
        let heading = (1u16 << self.arity) - 1;
        if self
            .dependencies
            .iter()
            .any(|fd| (fd.determinant | fd.dependent) & !heading != 0)
        {
            return Err(FdRefusal::AttributeOutsideHeading);
        }
        Ok(heading)
    }

    fn close(&self, input: u16, work: &mut Work) -> Result<ClosureWitness, FdRefusal> {
        let heading = self.heading()?;
        if input & !heading != 0 {
            return Err(FdRefusal::AttributeOutsideHeading);
        }
        let mut result = input;
        let mut applications = Vec::new();
        loop {
            let before = result;
            for (i, fd) in self.dependencies.iter().enumerate() {
                work.spend()?;
                if fd.determinant & !result == 0 && fd.dependent & !result != 0 {
                    result |= fd.dependent;
                    applications.push(i);
                }
            }
            if result == before {
                break;
            }
        }
        Ok(ClosureWitness {
            input,
            result,
            applications,
        })
    }

    pub fn closure(&self, input: u16, budget: u64) -> Result<ClosureWitness, FdRefusal> {
        self.close(
            input,
            &mut Work {
                used: 0,
                limit: budget,
            },
        )
    }

    /// Replay applications, then check that the final set is closed under all FDs.
    /// Minimality follows because each added attribute has an admitted derivation.
    pub fn verify_closure(&self, witness: &ClosureWitness) -> bool {
        let Ok(heading) = self.heading() else {
            return false;
        };
        if (witness.input | witness.result) & !heading != 0 {
            return false;
        }
        let mut result = witness.input;
        for &index in &witness.applications {
            let Some(fd) = self.dependencies.get(index) else {
                return false;
            };
            if fd.determinant & !result != 0 || fd.dependent & !result == 0 {
                return false;
            }
            result |= fd.dependent;
        }
        result == witness.result
            && self
                .dependencies
                .iter()
                .all(|fd| fd.determinant & !result != 0 || fd.dependent & !result == 0)
    }

    fn projection(
        &self,
        component: u16,
        work: &mut Work,
    ) -> Result<(Vec<FunctionalDependency>, Vec<FunctionalDependency>), FdRefusal> {
        let mut projected = Vec::new();
        let mut violations = Vec::new();
        let mut subset = component;
        loop {
            work.spend()?;
            let closure = self.close(subset, work)?.result & component;
            let dependent = closure & !subset;
            if dependent != 0 {
                let fd = FunctionalDependency {
                    determinant: subset,
                    dependent,
                };
                if closure != component {
                    violations.push(fd.clone());
                }
                projected.push(fd);
            }
            if subset == 0 {
                break;
            }
            subset = (subset - 1) & component;
        }
        Ok((projected, violations))
    }

    /// Complete FD-only decisions on the supported finite heading, or BudgetUnknown.
    /// No successful current instance is used to infer schema membership.
    pub fn binary_decomposition(
        &self,
        components: [u16; 2],
        budget: u64,
    ) -> Result<BinaryDecompositionReport, FdRefusal> {
        let heading = self.heading()?;
        if components.iter().any(|&c| c == 0 || c & !heading != 0)
            || components[0] | components[1] != heading
        {
            return Err(FdRefusal::InvalidDecomposition);
        }
        let mut work = Work {
            used: 0,
            limit: budget,
        };
        let intersection_closure = self.close(components[0] & components[1], &mut work)?;
        let determined_component = components
            .iter()
            .position(|&c| c & !intersection_closure.result == 0);
        let (_, original_bcnf_violations) = self.projection(heading, &mut work)?;
        let (p0, v0) = self.projection(components[0], &mut work)?;
        let (p1, v1) = self.projection(components[1], &mut work)?;
        // The projected cover can exceed the input cover's size. This is internal,
        // bounded by 2*(2^8); close it directly without the public input-cover cap.
        let projected = p0.iter().chain(&p1).collect::<Vec<_>>();
        let mut lost_dependencies = Vec::new();
        for fd in &self.dependencies {
            let mut closure = fd.determinant;
            loop {
                let before = closure;
                for local in &projected {
                    work.spend()?;
                    if local.determinant & !closure == 0 {
                        closure |= local.dependent;
                    }
                }
                if closure == before {
                    break;
                }
            }
            if fd.dependent & !closure != 0 {
                lost_dependencies.push(fd.clone());
            }
        }
        Ok(BinaryDecompositionReport {
            intersection_closure,
            determined_component,
            original_bcnf_violations,
            component_bcnf_violations: [v0, v1],
            projected_dependencies: [p0, p1],
            lost_dependencies,
            work_used: work.used,
        })
    }

    pub fn check_instance<T: Ord>(&self, rows: &[Vec<T>]) -> Result<(), FdRefusal> {
        self.heading()?;
        if rows.len() > 128 || rows.iter().any(|r| r.len() != self.arity) {
            return Err(FdRefusal::InstanceShape);
        }
        if rows.iter().collect::<BTreeSet<_>>().len() != rows.len() {
            return Err(FdRefusal::DuplicateTuple);
        }
        for (dependency, fd) in self.dependencies.iter().enumerate() {
            for first in 0..rows.len() {
                for second in 0..first {
                    let agree = |mask: u16| {
                        (0..self.arity)
                            .all(|i| mask & (1 << i) == 0 || rows[first][i] == rows[second][i])
                    };
                    if agree(fd.determinant) && !agree(fd.dependent) {
                        return Err(FdRefusal::InstanceDependencyViolation {
                            dependency,
                            first,
                            second,
                        });
                    }
                }
            }
        }
        Ok(())
    }
}

pub fn project<T: Ord + Clone>(
    rows: &[Vec<T>],
    arity: usize,
    component: u16,
) -> Result<BTreeSet<Vec<T>>, FdRefusal> {
    if arity == 0
        || arity > 8
        || component == 0
        || component >> arity != 0
        || rows.len() > 128
        || rows.iter().any(|r| r.len() != arity)
    {
        return Err(FdRefusal::InstanceShape);
    }
    Ok(rows
        .iter()
        .map(|row| {
            (0..arity)
                .filter(|&i| component & (1 << i) != 0)
                .map(|i| row[i].clone())
                .collect()
        })
        .collect())
}

/// Exact natural join in original heading order. Quadratic bounded instance work.
pub fn natural_join<T: Ord + Clone>(
    left: &BTreeSet<Vec<T>>,
    right: &BTreeSet<Vec<T>>,
    arity: usize,
    components: [u16; 2],
) -> Result<BTreeSet<Vec<T>>, FdRefusal> {
    if arity == 0
        || arity > 8
        || components.iter().any(|&c| c == 0 || c >> arity != 0)
        || components[0] | components[1] != (1 << arity) - 1
        || left.len() > 128
        || right.len() > 128
    {
        return Err(FdRefusal::InvalidDecomposition);
    }
    let indices = components.map(|c| {
        (0..arity)
            .filter(|&i| c & (1 << i) != 0)
            .collect::<Vec<_>>()
    });
    if left.iter().any(|r| r.len() != indices[0].len())
        || right.iter().any(|r| r.len() != indices[1].len())
    {
        return Err(FdRefusal::InstanceShape);
    }
    let mut joined = BTreeSet::new();
    for a in left {
        for b in right {
            if indices[0].iter().enumerate().all(|(j, i)| {
                indices[1]
                    .iter()
                    .position(|k| k == i)
                    .is_none_or(|k| a[j] == b[k])
            }) {
                joined.insert(
                    (0..arity)
                        .map(|i| {
                            if let Some(j) = indices[0].iter().position(|&k| k == i) {
                                a[j].clone()
                            } else {
                                b[indices[1].iter().position(|&k| k == i).unwrap()].clone()
                            }
                        })
                        .collect(),
                );
            }
        }
    }
    Ok(joined)
}

}
'''
TESTS = r'''
fn closed(s:&FdSchema,x:u16)->bool{s.dependencies.iter().all(|f|f.determinant & !x != 0 || f.dependent & !x == 0)}
fn oracle(s:&FdSchema,x:u16)->u16{let h=(1u16<<s.arity)-1;(0..=h).filter(|&y|x & !y==0 && closed(s,y)).fold(h,|a,b|a&b)}
fn schemas()->Vec<FdSchema>{let mut out=vec![FdSchema{arity:3,dependencies:vec![]}];for a in 0..8{for b in 0..8{out.push(FdSchema{arity:3,dependencies:vec![FunctionalDependency{determinant:a,dependent:b}]});for c in [0,3]{out.push(FdSchema{arity:3,dependencies:vec![FunctionalDependency{determinant:b,dependent:c},FunctionalDependency{determinant:a,dependent:b}]});}}}out}
fn old(s:&FdSchema)->frozen::FdSchema{serde_json::from_value(serde_json::to_value(s).unwrap()).unwrap()}
fn expected_projection(s:&FdSchema,c:u16)->(Vec<FunctionalDependency>,Vec<FunctionalDependency>){let mut masks:Vec<_>=(0..8).filter(|x|x & !c==0).collect();masks.reverse();let mut p=vec![];let mut v=vec![];for x in masks{let z=oracle(s,x)&c;let y=z&!x;if y!=0{let f=FunctionalDependency{determinant:x,dependent:y};p.push(f.clone());if z!=c{v.push(f);}}}(p,v)}
fn same<A:std::fmt::Debug,B:std::fmt::Debug>(a:A,b:B){assert_eq!(format!("{a:?}"),format!("{b:?}"));}
#[test]fn closed_supersets_replay_budget_and_complete_projection(){
 for s in schemas(){let prior=old(&s);for x in 0..8{let w=s.closure(x,u64::MAX).unwrap();assert_eq!(w.result,oracle(&s,x));assert!(s.verify_closure(&w));same(&w,prior.closure(x,u64::MAX).unwrap());for budget in 0..=32{same(s.closure(x,budget),prior.closure(x,budget));}let mut bad=w.clone();bad.result^=8;assert!(!s.verify_closure(&bad));bad=w.clone();bad.applications.push(usize::MAX);assert!(!s.verify_closure(&bad));bad=w.clone();bad.applications.clear();assert_eq!(s.verify_closure(&bad),x==w.result);}
 for a in 1..8{for b in 1..8{if a|b!=7{continue}let components=[a,b];let r=s.binary_decomposition(components,u64::MAX).unwrap();same(&r,prior.binary_decomposition(components,u64::MAX).unwrap());assert_eq!(r.intersection_closure.result,oracle(&s,a&b));assert_eq!(r.determined_component,components.iter().position(|&c|c & !oracle(&s,a&b)==0));let(_,v)=expected_projection(&s,7);assert_eq!(r.original_bcnf_violations,v);for(i,c)in components.into_iter().enumerate(){let(p,v)=expected_projection(&s,c);assert_eq!(r.projected_dependencies[i],p);assert_eq!(r.component_bcnf_violations[i],v);}let joined=FdSchema{arity:3,dependencies:r.projected_dependencies.iter().flatten().cloned().collect()};let lost:Vec<_>=s.dependencies.iter().filter(|fd|fd.dependent & !oracle(&joined,fd.determinant)!=0).cloned().collect();assert_eq!(r.lost_dependencies,lost);for budget in [0,r.work_used-1,r.work_used,r.work_used+1]{same(s.binary_decomposition(components,budget),prior.binary_decomposition(components,budget));}}}
 }
 let s=FdSchema{arity:3,dependencies:vec![FunctionalDependency{determinant:1,dependent:2},FunctionalDependency{determinant:1,dependent:4}]};assert!(s.verify_closure(&ClosureWitness{input:1,result:7,applications:vec![1,0]}));for w in [ClosureWitness{input:1,result:7,applications:vec![0,0,1]},ClosureWitness{input:0,result:7,applications:vec![0,1]},ClosureWitness{input:1,result:3,applications:vec![0]},ClosureWitness{input:9,result:7,applications:vec![0,1]}]{assert!(!s.verify_closure(&w));}
 let big=FdSchema{arity:8,dependencies:vec![FunctionalDependency{determinant:0,dependent:255}]};let r=big.binary_decomposition([255,255],u64::MAX).unwrap();assert_eq!(r.projected_dependencies.iter().map(Vec::len).sum::<usize>(),510);assert!(r.lost_dependencies.is_empty());same(&r,old(&big).binary_decomposition([255,255],u64::MAX).unwrap());
}
fn universe(arity:usize)->Vec<Vec<u8>>{(0..1<<arity).map(|x|(0..arity).map(|i|((x>>i)&1)as u8).collect()).collect()}
fn relation(universe:&[Vec<u8>],bits:usize)->Vec<Vec<u8>>{universe.iter().enumerate().filter(|(i,_)|bits & (1<<i)!=0).map(|(_,r)|r.clone()).collect()}
fn tuple_project(row:&[u8],c:u16)->Vec<u8>{row.iter().enumerate().filter(|(i,_)|c & (1<<i)!=0).map(|(_,v)|*v).collect()}
fn expected_join(left:&BTreeSet<Vec<u8>>,right:&BTreeSet<Vec<u8>>,arity:usize,c:[u16;2])->BTreeSet<Vec<u8>>{universe(arity).into_iter().filter(|r|left.contains(&tuple_project(r,c[0])) && right.contains(&tuple_project(r,c[1]))).collect()}
fn instance_error(s:&FdSchema,rows:&[Vec<u8>])->Result<(),FdRefusal>{for(d,f)in s.dependencies.iter().enumerate(){for i in 0..rows.len(){for j in 0..i{let coords=|mask:u16|->Vec<usize>{(0..s.arity).filter(|k|mask & (1<<k)!=0).collect()};if coords(f.determinant).iter().all(|&k|rows[i][k]==rows[j][k]) && coords(f.dependent).iter().any(|&k|rows[i][k]!=rows[j][k]){return Err(FdRefusal::InstanceDependencyViolation{dependency:d,first:i,second:j})}}}}Ok(())}
#[test]fn row_sets_projection_join_and_first_violation(){let u=universe(3);for bits in 0..256{let rows=relation(&u,bits);for a in 1..8{let p:BTreeSet<_>=rows.iter().map(|r|tuple_project(r,a)).collect();assert_eq!(project(&rows,3,a).unwrap(),p);for b in 1..8{if a|b!=7{continue}let q=project(&rows,3,b).unwrap();assert_eq!(natural_join(&p,&q,3,[a,b]).unwrap(),expected_join(&p,&q,3,[a,b]));same(natural_join(&p,&q,3,[a,b]),frozen::natural_join(&p,&q,3,[a,b]));}}for a in 0..8{for b in 0..8{let s=FdSchema{arity:3,dependencies:vec![FunctionalDependency{determinant:a,dependent:b},FunctionalDependency{determinant:0,dependent:7}]};assert_eq!(s.check_instance(&rows),instance_error(&s,&rows));same(s.check_instance(&rows),old(&s).check_instance(&rows));}}}
 let u=universe(2);for left_bits in 0..16{for right_bits in 0..16{let l=relation(&u,left_bits);let r=relation(&u,right_bits);for a in 1..4{for b in 1..4{if a|b!=3{continue}let p=project(&l,2,a).unwrap();let q=project(&r,2,b).unwrap();assert_eq!(natural_join(&p,&q,2,[a,b]).unwrap(),expected_join(&p,&q,2,[a,b]));}}}}
}
#[test]fn typed_refusals_raw_serde_and_generic_copy_boundary(){
 for n in [0,9,usize::MAX]{let s=FdSchema{arity:n,dependencies:vec![]};assert_eq!(s.heading(),Err(FdRefusal::UnsupportedHeading));assert_eq!(s.closure(0,0),Err(FdRefusal::UnsupportedHeading));assert!(!s.verify_closure(&ClosureWitness{input:0,result:0,applications:vec![]}));assert_eq!(s.check_instance::<u8>(&[]),Err(FdRefusal::UnsupportedHeading));}
 let s=FdSchema{arity:8,dependencies:vec![FunctionalDependency{determinant:0,dependent:0};129]};assert_eq!(s.heading(),Err(FdRefusal::UnsupportedHeading));for f in [FunctionalDependency{determinant:8,dependent:0},FunctionalDependency{determinant:0,dependent:8}]{assert_eq!(FdSchema{arity:3,dependencies:vec![f]}.heading(),Err(FdRefusal::AttributeOutsideHeading));}
 let s=FdSchema{arity:3,dependencies:vec![]};assert_eq!(s.closure(8,0),Err(FdRefusal::AttributeOutsideHeading));for c in [[0,7],[1,2],[8,7]]{assert_eq!(s.binary_decomposition(c,0),Err(FdRefusal::InvalidDecomposition));assert_eq!(natural_join::<u8>(&BTreeSet::new(),&BTreeSet::new(),3,c),Err(FdRefusal::InvalidDecomposition));}for n in [0,9,usize::MAX]{assert_eq!(natural_join::<u8>(&BTreeSet::new(),&BTreeSet::new(),n,[1,1]),Err(FdRefusal::InvalidDecomposition));assert_eq!(project::<u8>(&[],n,1),Err(FdRefusal::InstanceShape));}
 assert_eq!(s.check_instance(&vec![vec![0u8;3];129]),Err(FdRefusal::InstanceShape));assert_eq!(s.check_instance(&[vec![0u8;2]]),Err(FdRefusal::InstanceShape));assert_eq!(s.check_instance(&[vec![0u8;3],vec![0u8;3]]),Err(FdRefusal::DuplicateTuple));for c in [0,8]{assert_eq!(project::<u8>(&[],3,c),Err(FdRefusal::InstanceShape));}assert_eq!(project(&vec![vec![0u8;3];129],3,1),Err(FdRefusal::InstanceShape));assert_eq!(project(&[vec![0u8;2]],3,1),Err(FdRefusal::InstanceShape));
 let empty=BTreeSet::<Vec<u16>>::new();let huge=(0..129).map(|x|vec![x]).collect();let shape=[vec![0,0]].into_iter().collect();assert_eq!(natural_join(&huge,&empty,2,[1,2]),Err(FdRefusal::InvalidDecomposition));assert_eq!(natural_join(&empty,&huge,2,[1,2]),Err(FdRefusal::InvalidDecomposition));assert_eq!(natural_join(&shape,&empty,2,[1,2]),Err(FdRefusal::InstanceShape));assert_eq!(natural_join(&empty,&shape,2,[1,2]),Err(FdRefusal::InstanceShape));
 let raw:ClosureWitness=serde_json::from_str(r#"{"input":0,"result":7,"applications":[]}"#).unwrap();assert!(!FdSchema{arity:3,dependencies:vec![]}.verify_closure(&raw));assert!(serde_json::from_str::<FdSchema>(r#"{"arity":1,"dependencies":[],"unknown":true}"#).is_err());
 #[derive(Debug)]struct Counted(u8,std::rc::Rc<std::cell::Cell<usize>>);impl Clone for Counted{fn clone(&self)->Self{self.1.set(self.1.get()+1);Self(self.0,self.1.clone())}}impl PartialEq for Counted{fn eq(&self,o:&Self)->bool{self.0==o.0}}impl Eq for Counted{}impl PartialOrd for Counted{fn partial_cmp(&self,o:&Self)->Option<std::cmp::Ordering>{Some(self.cmp(o))}}impl Ord for Counted{fn cmp(&self,o:&Self)->std::cmp::Ordering{self.0.cmp(&o.0)}}
 let count=std::rc::Rc::new(std::cell::Cell::new(0));let rows=vec![vec![Counted(3,count.clone()),Counted(4,count.clone())]];let p=project(&rows,2,1).unwrap();assert_eq!(count.get(),1);let q=project(&rows,2,2).unwrap();assert_eq!(count.get(),2);let r=natural_join(&p,&q,2,[1,2]).unwrap();assert_eq!(count.get(),4);assert_eq!(r.iter().next().unwrap().iter().map(|v|v.0).collect::<Vec<_>>(),vec![3,4]);
}

'''

def challenge(subject):
    return '\n#[cfg(test)]mod independent_fd_tests{use super::*;\n'+FROZEN+TESTS+'\n}\n'
