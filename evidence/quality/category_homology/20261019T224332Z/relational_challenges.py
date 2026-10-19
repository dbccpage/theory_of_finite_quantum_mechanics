"""AuthorityEffect: None. Greatest-pair fixed point,DFS reachability and exact bounded-map oracles;frozen original production source."""
FROZEN=r'''mod frozen {
//! Finite labelled relational systems: strong report-respecting bisimulation.
//!
//! Labels index declared successor sets, which may be empty or branching.
//! This is exact set-level coalgebra, not trace equivalence, a clock, HoTT
//! equivalence, or Kan fibrancy. Reports are caller-interned equality classes.

use std::collections::{BTreeMap, BTreeSet};

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RelationalError {
    EmptyCarrier,
    TransitionShape,
    TransitionOutsideCarrier,
    DuplicateSuccessor,
    InvalidPartition,
    InvalidBoundedMap,
    RelationOutsideCarrier,
    StateOutsideCarrier,
}

impl std::fmt::Display for RelationalError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{self:?}")
    }
}
impl std::error::Error for RelationalError {}

/// Least reflexive, transitive relation containing the supplied finite edges.
/// Empty carriers are allowed. Cycles identify preorder-equivalent states;
/// they do not establish antisymmetry on the original carrier.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FinitePreorder {
    relation: Vec<Vec<bool>>,
}

fn close_transitively(relation: &mut [Vec<bool>]) {
    let n = relation.len();
    for via in 0..n {
        for x in 0..n {
            for y in 0..n {
                relation[x][y] |= relation[x][via] && relation[via][y];
            }
        }
    }
}

impl FinitePreorder {
    pub fn from_edges(size: usize, edges: &[(usize, usize)]) -> Result<Self, RelationalError> {
        if edges.iter().any(|&(x, y)| x >= size || y >= size) {
            return Err(RelationalError::RelationOutsideCarrier);
        }
        let mut relation = vec![vec![false; size]; size];
        for (i, row) in relation.iter_mut().enumerate() {
            row[i] = true;
        }
        for &(x, y) in edges {
            relation[x][y] = true;
        }
        close_transitively(&mut relation);
        Ok(Self { relation })
    }

    pub fn relation(&self) -> &[Vec<bool>] {
        &self.relation
    }

    pub fn leq(&self, x: usize, y: usize) -> Result<bool, RelationalError> {
        self.relation
            .get(x)
            .and_then(|row| row.get(y))
            .copied()
            .ok_or(RelationalError::StateOutsideCarrier)
    }

    pub fn is_partial_order(&self) -> bool {
        (0..self.relation.len())
            .all(|x| (0..x).all(|y| !(self.relation[x][y] && self.relation[y][x])))
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FiniteRelational {
    reports: Vec<usize>,
    successors: Vec<Vec<Vec<usize>>>,
    label_count: usize,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RelationalQuotient {
    pub partitions: Vec<Vec<usize>>,
    pub state_to_block: Vec<usize>,
    pub quotient: FiniteRelational,
}

/// Nonempty reachability classifies raw succession. Cycles forbid a strict
/// order on the original carrier. SCC condensation supplies a strict order
/// on a *different* carrier; internal transitions do not become strict edges.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SuccessionClassification {
    pub nonempty_reachability: Vec<Vec<bool>>,
    pub acyclic: bool,
    pub state_to_component: Vec<usize>,
    pub component_strict_order: Vec<Vec<bool>>,
}

fn normalize<T: Ord>(values: Vec<T>) -> Vec<usize> {
    let mut classes = BTreeMap::new();
    values
        .into_iter()
        .map(|value| {
            let fresh = classes.len();
            *classes.entry(value).or_insert(fresh)
        })
        .collect()
}

impl FiniteRelational {
    pub fn new(
        reports: Vec<usize>,
        mut successors: Vec<Vec<Vec<usize>>>,
        label_count: usize,
    ) -> Result<Self, RelationalError> {
        let n = reports.len();
        if n == 0 {
            return Err(RelationalError::EmptyCarrier);
        }
        if successors.len() != n || successors.iter().any(|row| row.len() != label_count) {
            return Err(RelationalError::TransitionShape);
        }
        for next in successors.iter_mut().flatten() {
            if next.iter().any(|&state| state >= n) {
                return Err(RelationalError::TransitionOutsideCarrier);
            }
            next.sort_unstable();
            if next.windows(2).any(|pair| pair[0] == pair[1]) {
                return Err(RelationalError::DuplicateSuccessor);
            }
        }
        Ok(Self {
            reports,
            successors,
            label_count,
        })
    }

    pub fn reports(&self) -> &[usize] {
        &self.reports
    }
    pub fn successors(&self) -> &[Vec<Vec<usize>>] {
        &self.successors
    }
    pub fn label_count(&self) -> usize {
        self.label_count
    }
    pub fn state_count(&self) -> usize {
        self.reports.len()
    }

    fn block_successors(&self, state: usize, label: usize, partition: &[usize]) -> BTreeSet<usize> {
        self.successors[state][label]
            .iter()
            .map(|&next| partition[next])
            .collect()
    }

    fn refine(&self, partition: &[usize]) -> Vec<usize> {
        normalize(
            (0..self.state_count())
                .map(|state| {
                    (
                        partition[state],
                        (0..self.label_count)
                            .map(|label| self.block_successors(state, label, partition))
                            .collect::<Vec<_>>(),
                    )
                })
                .collect(),
        )
    }

    /// Equality partitions are bisimulations exactly when related states have
    /// equal reports and identical sets of successor blocks for every label.
    pub fn is_report_bisimulation_partition(&self, partition: &[usize]) -> bool {
        if partition.len() != self.state_count() {
            return false;
        }
        for x in 0..self.state_count() {
            for y in 0..self.state_count() {
                if partition[x] == partition[y] {
                    if self.reports[x] != self.reports[y] {
                        return false;
                    }
                    for label in 0..self.label_count {
                        if self.block_successors(x, label, partition)
                            != self.block_successors(y, label, partition)
                        {
                            return false;
                        }
                    }
                }
            }
        }
        true
    }

    /// Every strict round splits at least one block. At most n-1 strict
    /// rounds occur; the repeated stable partition is not stored twice.
    pub fn bisimulation_quotient(&self) -> RelationalQuotient {
        let mut partition = normalize(self.reports.clone());
        let mut partitions = vec![partition.clone()];
        loop {
            let next = self.refine(&partition);
            if next == partition {
                break;
            }
            partition = next;
            partitions.push(partition.clone());
        }
        let blocks = 1 + partition.iter().copied().max().unwrap();
        let mut representatives = vec![0; blocks];
        for state in (0..self.state_count()).rev() {
            representatives[partition[state]] = state;
        }
        let reports = representatives
            .iter()
            .map(|&state| self.reports[state])
            .collect();
        let successors = representatives
            .iter()
            .map(|&state| {
                (0..self.label_count)
                    .map(|label| {
                        self.block_successors(state, label, &partition)
                            .into_iter()
                            .collect()
                    })
                    .collect()
            })
            .collect();
        let quotient = FiniteRelational::new(reports, successors, self.label_count)
            .expect("refinement constructs a nonempty well-typed quotient");
        RelationalQuotient {
            partitions,
            state_to_block: partition,
            quotient,
        }
    }

    /// Receipts are replayed from the actual system, including maximality:
    /// a merely stable but unnecessarily fine partition is rejected.
    pub fn verify_quotient(&self, receipt: &RelationalQuotient) -> bool {
        &self.bisimulation_quotient() == receipt
    }

    /// Unpointed behavioral classification. Report IDs and label positions
    /// must have the same interpretation in both inputs. Equality of the
    /// represented bisimulation classes is equivalent to isomorphism of
    /// their minimal quotients, without choosing an initial state.
    pub fn same_behavior_set(&self, other: &Self) -> bool {
        if self.label_count != other.label_count {
            return false;
        }
        let offset = self.state_count();
        let mut reports = self.reports.clone();
        reports.extend_from_slice(&other.reports);
        let mut successors = self.successors.clone();
        successors.extend(other.successors.iter().map(|row| {
            row.iter()
                .map(|next| next.iter().map(|state| state + offset).collect())
                .collect()
        }));
        let combined = Self::new(reports, successors, self.label_count)
            .expect("disjoint union of validated finite relational systems");
        let classes = combined.bisimulation_quotient().state_to_block;
        classes[..offset].iter().copied().collect::<BTreeSet<_>>()
            == classes[offset..].iter().copied().collect::<BTreeSet<_>>()
    }

    /// A surjective bounded morphism has equal reports and exactly the
    /// target successor set as the image of each source successor set.
    /// Forward edge preservation alone does not suffice.
    pub fn factor_through_bounded_quotient(
        &self,
        target: &Self,
        map: &[usize],
    ) -> Result<Vec<usize>, RelationalError> {
        if map.len() != self.state_count()
            || target.label_count != self.label_count
            || map.iter().any(|&state| state >= target.state_count())
            || map.iter().copied().collect::<BTreeSet<_>>().len() != target.state_count()
        {
            return Err(RelationalError::InvalidBoundedMap);
        }
        for state in 0..self.state_count() {
            if self.reports[state] != target.reports[map[state]] {
                return Err(RelationalError::InvalidBoundedMap);
            }
            for label in 0..self.label_count {
                let image: BTreeSet<_> = self.successors[state][label]
                    .iter()
                    .map(|&next| map[next])
                    .collect();
                let expected: BTreeSet<_> = target.successors[map[state]][label]
                    .iter()
                    .copied()
                    .collect();
                if image != expected {
                    return Err(RelationalError::InvalidBoundedMap);
                }
            }
        }
        let stable = self.bisimulation_quotient().state_to_block;
        let mut factor = vec![None; target.state_count()];
        for state in 0..self.state_count() {
            match factor[map[state]] {
                Some(block) if block != stable[state] => {
                    return Err(RelationalError::InvalidBoundedMap)
                }
                _ => factor[map[state]] = Some(stable[state]),
            }
        }
        Ok(factor
            .into_iter()
            .map(|block| block.expect("surjective map"))
            .collect())
    }

    /// Classify the union of *declared* labelled transitions without selecting
    /// or orienting new transitions from reports. Index enumeration affects
    /// only identifiers, not reachability, SCCs, or the component strict order.
    pub fn succession_classification(&self) -> SuccessionClassification {
        let n = self.state_count();
        let mut reach = vec![vec![false; n]; n];
        for (state, row) in self.successors.iter().enumerate() {
            for &next in row.iter().flatten() {
                reach[state][next] = true;
            }
        }
        close_transitively(&mut reach);
        let acyclic = (0..n).all(|state| !reach[state][state]);
        let mut component = vec![usize::MAX; n];
        let mut representatives = Vec::new();
        for x in 0..n {
            if component[x] != usize::MAX {
                continue;
            }
            let block = representatives.len();
            representatives.push(x);
            for y in x..n {
                if x == y || (reach[x][y] && reach[y][x]) {
                    component[y] = block;
                }
            }
        }
        let order = representatives
            .iter()
            .enumerate()
            .map(|(i, &x)| {
                representatives
                    .iter()
                    .enumerate()
                    .map(|(j, &y)| i != j && reach[x][y])
                    .collect()
            })
            .collect();
        SuccessionClassification {
            nonempty_reachability: reach,
            acyclic,
            state_to_component: component,
            component_strict_order: order,
        }
    }
}


}
'''
TESTS=r'''
fn greatest(left:&FiniteRelational,right:&FiniteRelational)->Vec<Vec<bool>>{let n=left.state_count();let m=right.state_count();let mut r:Vec<Vec<_>>=(0..n).map(|x|(0..m).map(|y|left.reports()[x]==right.reports()[y]).collect()).collect();assert_eq!(left.label_count(),right.label_count());loop{let before=r.clone();for x in 0..n{for y in 0..m{if !before[x][y]{continue}for label in 0..left.label_count(){let a=&left.successors()[x][label];let b=&right.successors()[y][label];if a.iter().any(|&u|!b.iter().any(|&v|before[u][v])) || b.iter().any(|&v|!a.iter().any(|&u|before[u][v])){r[x][y]=false;}}}}if r==before{return r}}}
fn canonical(r:&[Vec<bool>])->Vec<usize>{let mut ids=vec![];let mut fresh=0;for x in 0..r.len(){if let Some(y)=(0..x).find(|&y|r[x][y]){ids.push(ids[y]);}else{ids.push(fresh);fresh+=1;}}ids}
fn old(m:&FiniteRelational)->frozen::FiniteRelational{frozen::FiniteRelational::new(m.reports().to_vec(),m.successors().to_vec(),m.label_count()).unwrap()}
fn same<A:std::fmt::Debug,B:std::fmt::Debug>(a:A,b:B){assert_eq!(format!("{a:?}"),format!("{b:?}"));}
fn reach(m:&FiniteRelational)->Vec<Vec<bool>>{let n=m.state_count();(0..n).map(|start|{let mut seen=vec![false;n];let mut pending:Vec<usize>=m.successors()[start].iter().flatten().copied().collect();while let Some(next)=pending.pop(){if seen[next]{continue}seen[next]=true;pending.extend(m.successors()[next].iter().flatten().copied());}seen}).collect()}
fn partition_valid(m:&FiniteRelational,p:&[usize])->bool{if p.len()!=m.state_count(){return false}for x in 0..p.len(){for y in 0..x{if p[x]!=p[y]{continue}if m.reports()[x]!=m.reports()[y]{return false}for i in 0..m.label_count(){let a=&m.successors()[x][i];let b=&m.successors()[y][i];if a.iter().any(|&u|!b.iter().any(|&v|p[u]==p[v]))||b.iter().any(|&v|!a.iter().any(|&u|p[u]==p[v])){return false}}}}true}
fn digits(mut code:usize,n:usize)->Vec<usize>{(0..n).map(|_|{let x=code%n;code/=n;x}).collect()}
fn check(m:&FiniteRelational){let r=greatest(m,m);let q=m.bisimulation_quotient();assert_eq!(q.state_to_block,canonical(&r));same(&q,old(m).bisimulation_quotient());assert!(m.verify_quotient(&q));assert!(q.partitions.len()<=m.state_count());for code in 0..m.state_count().pow(m.state_count()as u32){let p=digits(code,m.state_count());assert_eq!(m.is_report_bisimulation_partition(&p),partition_valid(m,&p));let sparse:Vec<_>=p.iter().map(|&i|if i==0{usize::MAX}else{i-1}).collect();assert_eq!(m.is_report_bisimulation_partition(&sparse),partition_valid(m,&sparse));}let nonempty=reach(m);let c=m.succession_classification();assert_eq!(c.nonempty_reachability,nonempty);assert_eq!(c.acyclic,(0..m.state_count()).all(|i|!nonempty[i][i]));same(&c,old(m).succession_classification());let mutual:Vec<Vec<_>>=(0..m.state_count()).map(|i|(0..m.state_count()).map(|j|i==j||(nonempty[i][j]&&nonempty[j][i])).collect()).collect();assert_eq!(c.state_to_component,canonical(&mutual));for i in 0..c.component_strict_order.len(){let x=c.state_to_component.iter().position(|&k|k==i).unwrap();for j in 0..c.component_strict_order.len(){let y=c.state_to_component.iter().position(|&k|k==j).unwrap();assert_eq!(c.component_strict_order[i][j],i!=j&&nonempty[x][y]);}}
 assert_eq!(m.reports().as_ptr(),m.reports.as_ptr());assert_eq!(m.successors().as_ptr(),m.successors.as_ptr());
}
fn machine(n:usize,labels:usize,report_bits:usize,edge_bits:usize)->FiniteRelational{FiniteRelational::new((0..n).map(|i|(report_bits>>i)&1).collect(),(0..n).map(|x|(0..labels).map(|i|(0..n).filter(|&y|edge_bits & (1<<(labels*n*x+n*i+y))!=0).rev().collect()).collect()).collect(),labels).unwrap()}
#[test]fn greatest_bisimulation_not_trace_and_reachability_oracles(){for reports in 0..8{for edges in 0..512{check(&machine(3,1,reports,edges));}}for reports in 0..4{for edges in 0..256{check(&machine(2,2,reports,edges));}}for reports in 0..8{check(&machine(3,0,reports,0));}for seed in 0usize..32{check(&machine(4,2,seed&15,seed.wrapping_mul(2654435761usize)));}
 // Same possible report traces, different strong branching: a chooses one of
 // two one-step continuations; b chooses one state with both continuations.
 let m=FiniteRelational::new(vec![0,0,1,1,1,2,3],vec![vec![vec![2,3]],vec![vec![4]],vec![vec![5]],vec![vec![6]],vec![vec![5,6]],vec![vec![]],vec![vec![]]],1).unwrap();assert!(!greatest(&m,&m)[0][1]);assert_ne!(m.bisimulation_quotient().state_to_block[0],m.bisimulation_quotient().state_to_block[1]);
}
fn bounded(source:&FiniteRelational,target:&FiniteRelational,map:&[usize])->bool{if map.len()!=source.state_count() || source.label_count()!=target.label_count() || map.iter().any(|&v|v>=target.state_count()) || (0..target.state_count()).any(|v|!map.contains(&v)){return false}for x in 0..source.state_count(){if source.reports()[x]!=target.reports()[map[x]]{return false}for i in 0..source.label_count(){for v in 0..target.state_count(){if source.successors()[x][i].iter().any(|&u|map[u]==v)!=target.successors()[map[x]][i].contains(&v){return false}}}}true}
#[test]fn cross_system_classes_exact_bounded_images_and_factor(){let models:Vec<_>=(0..4).flat_map(|r|(0..16).map(move|e|machine(2,1,r,e))).collect();for source in &models{for target in &models{let cross=greatest(source,target);let equal=cross.iter().all(|row|row.iter().any(|&v|v))&&(0..target.state_count()).all(|y|(0..source.state_count()).any(|x|cross[x][y]));assert_eq!(source.same_behavior_set(target),equal);same(source.same_behavior_set(target),old(source).same_behavior_set(&old(target)));for bits in 0..4{let map=digits(bits,2);let result=source.factor_through_bounded_quotient(target,&map);same(&result,old(source).factor_through_bounded_quotient(&old(target),&map));assert_eq!(result.is_ok(),bounded(source,target,&map));if let Ok(f)=result{let classes=canonical(&greatest(source,source));for x in 0..source.state_count(){assert_eq!(f[map[x]],classes[x]);}}}}
 for reports in 0..2{for edges in 0..2{let target=machine(1,1,reports,edges);let map=[0,0];let result=source.factor_through_bounded_quotient(&target,&map);assert_eq!(result.is_ok(),bounded(source,&target,&map));if let Ok(f)=result{let classes=canonical(&greatest(source,source));assert_eq!(classes,vec![f[0],f[0]]);}}}}
}
#[test]fn preorder_zero_cycles_exact_refusals_and_forged_receipts(){for bits in 0..512{let edges:Vec<_>=(0..3).flat_map(|x|(0..3).filter(move|&y|bits & (1<<(3*x+y))!=0).map(move|y|(x,y))).collect();let p=FinitePreorder::from_edges(3,&edges).unwrap();let m=machine(3,1,0,bits);let r=reach(&m);for x in 0..3{for y in 0..3{assert_eq!(p.leq(x,y),Ok(x==y||r[x][y]));}}assert_eq!(p.is_partial_order(),(0..3).all(|x|(0..x).all(|y|!(r[x][y]&&r[y][x]))));same(&p,frozen::FinitePreorder::from_edges(3,&edges).unwrap());assert_eq!(p.relation().as_ptr(),p.relation.as_ptr());}
 let empty=FinitePreorder::from_edges(0,&[]).unwrap();assert!(empty.is_partial_order());assert!(empty.relation().is_empty());assert_eq!(empty.leq(0,0),Err(RelationalError::StateOutsideCarrier));assert_eq!(FinitePreorder::from_edges(0,&[(0,0)]),Err(RelationalError::RelationOutsideCarrier));assert_eq!(FinitePreorder::from_edges(2,&[(usize::MAX,0)]),Err(RelationalError::RelationOutsideCarrier));
 assert_eq!(FiniteRelational::new(vec![],vec![],0),Err(RelationalError::EmptyCarrier));assert_eq!(FiniteRelational::new(vec![0],vec![],0),Err(RelationalError::TransitionShape));assert_eq!(FiniteRelational::new(vec![0],vec![vec![vec![]]],0),Err(RelationalError::TransitionShape));assert_eq!(FiniteRelational::new(vec![0],vec![vec![vec![1]]],1),Err(RelationalError::TransitionOutsideCarrier));assert_eq!(FiniteRelational::new(vec![0],vec![vec![vec![0,0]]],1),Err(RelationalError::DuplicateSuccessor));
 let m=machine(3,1,0,0);let q=m.bisimulation_quotient();assert_eq!(q.state_to_block,vec![0,0,0]);assert!(!m.is_report_bisimulation_partition(&[0]));let mut forged=q.clone();forged.partitions.clear();assert!(!m.verify_quotient(&forged));forged=q.clone();forged.partitions.push(q.state_to_block.clone());assert!(!m.verify_quotient(&forged));forged=q.clone();forged.state_to_block=vec![0,1,2];assert!(!m.verify_quotient(&forged));let fine=RelationalQuotient{partitions:vec![vec![0,1,2]],state_to_block:vec![0,1,2],quotient:m.clone()};assert!(m.is_report_bisimulation_partition(&fine.state_to_block));assert!(!m.verify_quotient(&fine));
 let other=machine(3,0,0,0);assert!(!m.same_behavior_set(&other));assert_eq!(m.factor_through_bounded_quotient(&other,&[0,1,2]),Err(RelationalError::InvalidBoundedMap));for map in [vec![],vec![0,1,usize::MAX],vec![0,0,0]]{assert_eq!(m.factor_through_bounded_quotient(&m,&map),Err(RelationalError::InvalidBoundedMap));}
 let p=FinitePreorder::from_edges(2,&[(0,1),(0,1)]).unwrap();assert!(p.leq(0,1).unwrap());assert_eq!(p.leq(2,0),Err(RelationalError::StateOutsideCarrier));assert_eq!(p.leq(0,usize::MAX),Err(RelationalError::StateOutsideCarrier));assert_eq!(format!("{}",RelationalError::InvalidPartition),"InvalidPartition");
}

'''

def challenge(subject):
    return '\n#[cfg(test)]mod independent_relational_tests{use super::*;\n'+FROZEN+TESTS+'\n}\n'
