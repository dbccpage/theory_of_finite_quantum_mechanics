"""AuthorityEffect: None. Explicit finite-product and map-fiber oracles;frozen witness data;complete Boolean implication tables."""
FROZEN=r'''mod frozen {
//! Complete constructive finite predicate classifications, without phenomenology.
//!
//! Component data are not predicates: these theorems classify explicitly chosen
//! invariants of total finite maps. Every permitted signature has a concrete
//! witness with at most four states; necessity uses universal map arguments.

use std::collections::{BTreeMap, BTreeSet};

use crate::finite_moore::FiniteMoore;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ClassificationError {
    InvalidModel,
    ImpossibleSignature,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct RetentionSignature {
    pub nontrivial: bool,
    pub reversible: bool,
    pub observable: bool,
    pub tolerance: bool,
    pub minimal: bool,
    pub active: bool,
}

impl RetentionSignature {
    /// Complete necessary/sufficient criterion for these SIX predicates.
    /// Singleton maps force reversible/injective/minimal and no activity/tolerance.
    /// Injective recognized reports force minimality. Identity dynamics have no
    /// future distinguishing power, so minimal iff raw-injective and no tolerance.
    pub fn is_realizable(self) -> bool {
        if !self.nontrivial {
            return self.reversible
                && self.observable
                && !self.tolerance
                && self.minimal
                && !self.active;
        }
        if self.observable && !self.tolerance && !self.minimal {
            return false;
        }
        if !self.active {
            return self.reversible && self.minimal == (self.observable && !self.tolerance);
        }
        true
    }
}

/// Raw and recognized report identifiers, together with a total Moore system.
/// Recognition must factor through raw report equality, making a genuine finite
/// report equivalence; arbitrary nontransitive tolerances are outside this scope.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FiniteRetentionModel {
    raw_reports: Vec<usize>,
    moore: FiniteMoore,
}

impl FiniteRetentionModel {
    pub fn new(
        raw_reports: Vec<usize>,
        recognized: Vec<usize>,
        transitions: Vec<Vec<usize>>,
        inputs: usize,
    ) -> Result<Self, ClassificationError> {
        if raw_reports.len() != recognized.len() {
            return Err(ClassificationError::InvalidModel);
        }
        let mut factor = BTreeMap::new();
        for (&raw, &report) in raw_reports.iter().zip(&recognized) {
            if let Some(previous) = factor.insert(raw, report) {
                if previous != report {
                    return Err(ClassificationError::InvalidModel);
                }
            }
        }
        let moore = FiniteMoore::new(recognized, transitions, inputs)
            .map_err(|_| ClassificationError::InvalidModel)?;
        Ok(Self { raw_reports, moore })
    }

    pub fn raw_reports(&self) -> &[usize] {
        &self.raw_reports
    }
    pub fn moore(&self) -> &FiniteMoore {
        &self.moore
    }

    pub fn signature(&self) -> RetentionSignature {
        let n = self.moore.state_count();
        let observable = self.raw_reports.iter().collect::<BTreeSet<_>>().len() == n;
        let tolerance = (0..n).any(|x| {
            (0..n).any(|y| {
                self.raw_reports[x] != self.raw_reports[y]
                    && self.moore.reports()[x] == self.moore.reports()[y]
            })
        });
        let reversible = (0..self.moore.input_count()).all(|i| {
            self.moore
                .transitions()
                .iter()
                .map(|row| row[i])
                .collect::<BTreeSet<_>>()
                .len()
                == n
        });
        let active = self
            .moore
            .transitions()
            .iter()
            .enumerate()
            .any(|(x, row)| row.iter().any(|&y| x != y));
        RetentionSignature {
            nontrivial: n > 1,
            reversible,
            observable,
            tolerance,
            minimal: self.moore.behavioral_quotient().quotient.state_count() == n,
            active,
        }
    }
}

/// Construct every realizable signature; exhaustive checks are corroboration,
/// while the construction and universal implications prove completeness.
pub fn realize_retention(
    signature: RetentionSignature,
) -> Result<FiniteRetentionModel, ClassificationError> {
    if !signature.is_realizable() {
        return Err(ClassificationError::ImpossibleSignature);
    }
    let (raw, recognized) = if !signature.nontrivial {
        (vec![0], vec![0])
    } else if signature.minimal {
        match (signature.observable, signature.tolerance) {
            (true, false) => (vec![0, 1], vec![0, 1]),
            (false, false) => (vec![0, 0, 1], vec![0, 0, 1]),
            (true, true) => (vec![0, 1, 2], vec![0, 0, 1]),
            (false, true) => (vec![0, 0, 1, 2], vec![0, 0, 0, 1]),
        }
    } else {
        match (signature.observable, signature.tolerance) {
            (true, true) => (vec![0, 1], vec![0, 0]),
            (false, false) => (vec![0, 0], vec![0, 0]),
            (false, true) => (vec![0, 0, 1], vec![0, 0, 0]),
            (true, false) => return Err(ClassificationError::ImpossibleSignature),
        }
    };
    let n = raw.len();
    let transitions = (0..n)
        .map(|x| {
            vec![if !signature.active {
                x
            } else if signature.reversible {
                (x + 1) % n
            } else if signature.minimal {
                (x + 1).min(n - 1)
            } else {
                0
            }]
        })
        .collect();
    FiniteRetentionModel::new(raw, recognized, transitions, 1)
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct FunctionalSignature {
    /// An independent report s factors through the accessible presentation q.
    pub linked: bool,
    /// q is stable under the declared context action t.
    pub presentation_stable: bool,
    /// s is stable under t (the manuscript's REPORT-stability predicate).
    pub report_stable: bool,
    /// Report equals the declared behavioral target at every state.
    pub calibrated: bool,
    /// At least two states have the same accessible presentation.
    pub blind_spot: bool,
}

impl FunctionalSignature {
    /// Exactly two constraints: injective q forces factorization, and linked
    /// reports inherit presentation stability. All other combinations occur.
    pub fn is_realizable(self) -> bool {
        (self.blind_spot || self.linked)
            && !(self.linked && self.presentation_stable && !self.report_stable)
    }
}

/// Total finite maps q,s,t,b on a nonempty common carrier. Accessible self-state
/// is identified with that carrier. No report factorization is presumed.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FiniteFunctionalModel {
    presentation: Vec<usize>,
    report: Vec<usize>,
    context: Vec<usize>,
    target: Vec<usize>,
}

impl FiniteFunctionalModel {
    pub fn new(
        presentation: Vec<usize>,
        report: Vec<usize>,
        context: Vec<usize>,
        target: Vec<usize>,
    ) -> Result<Self, ClassificationError> {
        let n = presentation.len();
        if n == 0
            || report.len() != n
            || context.len() != n
            || target.len() != n
            || context.iter().any(|&x| x >= n)
        {
            return Err(ClassificationError::InvalidModel);
        }
        Ok(Self {
            presentation,
            report,
            context,
            target,
        })
    }
    pub fn presentation(&self) -> &[usize] {
        &self.presentation
    }
    pub fn report(&self) -> &[usize] {
        &self.report
    }
    pub fn context(&self) -> &[usize] {
        &self.context
    }
    pub fn target(&self) -> &[usize] {
        &self.target
    }

    /// Factorization exists iff every q-fiber has a constant s; this is a
    /// checked partial map on realized presentations, not a guessed decoder.
    pub fn report_factor(&self) -> Option<BTreeMap<usize, usize>> {
        let mut factor = BTreeMap::new();
        for (&q, &s) in self.presentation.iter().zip(&self.report) {
            if let Some(old) = factor.insert(q, s) {
                if old != s {
                    return None;
                }
            }
        }
        Some(factor)
    }
    pub fn signature(&self) -> FunctionalSignature {
        FunctionalSignature {
            linked: self.report_factor().is_some(),
            presentation_stable: self
                .context
                .iter()
                .enumerate()
                .all(|(x, &tx)| self.presentation[x] == self.presentation[tx]),
            report_stable: self
                .context
                .iter()
                .enumerate()
                .all(|(x, &tx)| self.report[x] == self.report[tx]),
            calibrated: self.report == self.target,
            blind_spot: self.presentation.iter().collect::<BTreeSet<_>>().len()
                < self.presentation.len(),
        }
    }
}

/// Construct all 20 realizable signatures with at most three states.
/// Calibration is independent: b=s for success, change b(0) for failure.
pub fn realize_functional(
    signature: FunctionalSignature,
) -> Result<FiniteFunctionalModel, ClassificationError> {
    if !signature.is_realizable() {
        return Err(ClassificationError::ImpossibleSignature);
    }
    let (q, s, t) = if !signature.blind_spot {
        let q = vec![0, 1];
        if signature.presentation_stable {
            (q, vec![0, 1], vec![0, 1])
        } else if signature.report_stable {
            (q, vec![0, 0], vec![1, 1])
        } else {
            (q, vec![0, 1], vec![1, 1])
        }
    } else if signature.linked {
        let q = vec![0, 0, 1];
        if signature.presentation_stable {
            (q, vec![0, 0, 1], vec![0, 1, 2])
        } else if signature.report_stable {
            (q, vec![0, 0, 0], vec![2, 1, 2])
        } else {
            (q, vec![0, 0, 1], vec![2, 1, 2])
        }
    } else {
        let q = vec![0, 0, 1];
        if signature.presentation_stable {
            if signature.report_stable {
                (q, vec![0, 1, 0], vec![0, 1, 2])
            } else {
                (q, vec![0, 1, 0], vec![1, 1, 2])
            }
        } else if signature.report_stable {
            (q, vec![0, 1, 0], vec![2, 1, 2])
        } else {
            (q, vec![0, 1, 2], vec![2, 1, 2])
        }
    };
    let mut target = s.clone();
    if !signature.calibrated {
        target[0] += 1;
    }
    FiniteFunctionalModel::new(q, s, t, target)
}

/// A positive or negative literal in the documented signature field order.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct PropertyLiteral {
    pub index: usize,
    pub value: bool,
}

/// Return an explicit countermodel, or None when every classified retention
/// model satisfying the premises satisfies the conclusion. Field order is
/// N,V,O,T,K,A. Contradictory premises entail vacuously; invalid indices refuse.
/// Completeness follows from the universal classification plus constructors,
/// not an assumed bound on possible carrier sizes.
pub fn retention_implication_countermodel(
    premises: &[PropertyLiteral],
    conclusion: PropertyLiteral,
) -> Result<Option<FiniteRetentionModel>, ClassificationError> {
    if conclusion.index >= 6 || premises.iter().any(|literal| literal.index >= 6) {
        return Err(ClassificationError::InvalidModel);
    }
    for bits in 0_usize..64 {
        let flags: [bool; 6] = std::array::from_fn(|i| bits & (1 << i) != 0);
        if flags[conclusion.index] == conclusion.value
            || premises
                .iter()
                .any(|literal| flags[literal.index] != literal.value)
        {
            continue;
        }
        let signature = RetentionSignature {
            nontrivial: flags[0],
            reversible: flags[1],
            observable: flags[2],
            tolerance: flags[3],
            minimal: flags[4],
            active: flags[5],
        };
        if signature.is_realizable() {
            return realize_retention(signature).map(Some);
        }
    }
    Ok(None)
}

/// Complete implication replay for F,P,S,C,B with an explicit finite witness
/// for every failed implication. Returns None iff the implication is valid in
/// the entire declared class (including the vacuous contradictory-premise case).
pub fn functional_implication_countermodel(
    premises: &[PropertyLiteral],
    conclusion: PropertyLiteral,
) -> Result<Option<FiniteFunctionalModel>, ClassificationError> {
    if conclusion.index >= 5 || premises.iter().any(|literal| literal.index >= 5) {
        return Err(ClassificationError::InvalidModel);
    }
    for bits in 0_usize..32 {
        let flags: [bool; 5] = std::array::from_fn(|i| bits & (1 << i) != 0);
        if flags[conclusion.index] == conclusion.value
            || premises
                .iter()
                .any(|literal| flags[literal.index] != literal.value)
        {
            continue;
        }
        let signature = FunctionalSignature {
            linked: flags[0],
            presentation_stable: flags[1],
            report_stable: flags[2],
            calibrated: flags[3],
            blind_spot: flags[4],
        };
        if signature.is_realizable() {
            return realize_functional(signature).map(Some);
        }
    }
    Ok(None)
}

}
'''
TESTS=r'''
fn flags6(s:RetentionSignature)->[bool;6]{[s.nontrivial,s.reversible,s.observable,s.tolerance,s.minimal,s.active]}
fn flags5(s:FunctionalSignature)->[bool;5]{[s.linked,s.presentation_stable,s.report_stable,s.calibrated,s.blind_spot]}
fn sig6(bits:usize)->RetentionSignature{RetentionSignature{nontrivial:bits&1!=0,reversible:bits&2!=0,observable:bits&4!=0,tolerance:bits&8!=0,minimal:bits&16!=0,active:bits&32!=0}}
fn sig5(bits:usize)->FunctionalSignature{FunctionalSignature{linked:bits&1!=0,presentation_stable:bits&2!=0,report_stable:bits&4!=0,calibrated:bits&8!=0,blind_spot:bits&16!=0}}
fn finite_future(raw:&[usize],transitions:&[Vec<usize>],x:usize,y:usize)->bool{let n=raw.len();let mut pending=vec![(x,y)];let mut visited=vec![false;n*n];while let Some((a,b))=pending.pop(){if visited[a*n+b]{continue}visited[a*n+b]=true;if raw[a]!=raw[b]{return false}for i in 0..transitions[a].len(){pending.push((transitions[a][i],transitions[b][i]));}}true}
fn retention_oracle(m:&FiniteRetentionModel)->[bool;6]{let raw=m.raw_reports();let r=m.moore().reports();let t=m.moore().transitions();let n=raw.len();let pairs:Vec<_>=(0..n).flat_map(|a|(0..a).map(move|b|(a,b))).collect();[n>1,(0..m.moore().input_count()).all(|i|pairs.iter().all(|&(a,b)|t[a][i]!=t[b][i])),pairs.iter().all(|&(a,b)|raw[a]!=raw[b]),pairs.iter().any(|&(a,b)|raw[a]!=raw[b]&&r[a]==r[b]),pairs.iter().all(|&(a,b)|!finite_future(r,t,a,b)),t.iter().enumerate().any(|(a,row)|row.iter().any(|&b|a!=b))]}
fn functional_oracle(m:&FiniteFunctionalModel)->[bool;5]{let q=m.presentation();let s=m.report();let t=m.context();let n=q.len();let pairs:Vec<_>=(0..n).flat_map(|a|(0..a).map(move|b|(a,b))).collect();[pairs.iter().all(|&(a,b)|q[a]!=q[b]||s[a]==s[b]),(0..n).all(|x|q[x]==q[t[x]]),(0..n).all(|x|s[x]==s[t[x]]),s==m.target(),pairs.iter().any(|&(a,b)|q[a]==q[b])]}
fn digits(mut bits:usize,n:usize)->Vec<usize>{(0..n).map(|_|{let d=bits%n;bits/=n;d}).collect()}
fn same<A:std::fmt::Debug,B:std::fmt::Debug>(a:A,b:B){assert_eq!(format!("{a:?}"),format!("{b:?}"));}
fn check_retention(raw:Vec<usize>,r:Vec<usize>,t:Vec<Vec<usize>>,inputs:usize){let lawful=(0..raw.len()).all(|x|(0..x).all(|y|raw[x]!=raw[y]||r[x]==r[y]));let model=FiniteRetentionModel::new(raw.clone(),r.clone(),t.clone(),inputs);let prior=frozen::FiniteRetentionModel::new(raw,r,t,inputs);same(&model,&prior);if !lawful{assert_eq!(model,Err(ClassificationError::InvalidModel));return}let m=model.unwrap();let expected=retention_oracle(&m);assert_eq!(flags6(m.signature()),expected);assert!(m.signature().is_realizable());assert_eq!(m.raw_reports().as_ptr(),m.raw_reports.as_ptr());assert!(std::ptr::eq(m.moore(),&m.moore));}
#[test]fn universal_predicates_finite_oracles_and_all_witnesses(){
 for bits in 0..64{let s=sig6(bits);let expected=if bits&1==0{bits==22}else{!(s.observable&&!s.tolerance&&!s.minimal) && (s.active||(s.reversible && (s.minimal==(s.observable&&!s.tolerance))))};assert_eq!(s.is_realizable(),expected);let m=realize_retention(s);same(&m,frozen::realize_retention(frozen::RetentionSignature{nontrivial:s.nontrivial,reversible:s.reversible,observable:s.observable,tolerance:s.tolerance,minimal:s.minimal,active:s.active}));match m{Ok(m)=>{assert!(expected);assert!(m.raw_reports().len()<=4);assert_eq!(retention_oracle(&m),flags6(s));assert_eq!(flags6(m.signature()),flags6(s));},Err(e)=>{assert!(!expected);assert_eq!(e,ClassificationError::ImpossibleSignature);}}}
 for n in 1usize..=3{let maps=n.pow(n as u32);for a in 0..maps{for b in 0..maps{let raw=digits(a,n);let recognized=digits(b,n);check_retention(raw.clone(),recognized.clone(),vec![vec![];n],0);for c in 0..maps{let first=digits(c,n);check_retention(raw.clone(),recognized.clone(),first.iter().map(|&x|vec![x]).collect(),1);check_retention(raw.clone(),recognized.clone(),first.iter().enumerate().map(|(x,&v)|vec![v,(x+1)%n]).collect(),2);}}}}
 for bits in 0..32{let s=sig5(bits);let allowed=(s.blind_spot||s.linked)&&(!s.linked||!s.presentation_stable||s.report_stable);assert_eq!(s.is_realizable(),allowed);let m=realize_functional(s);same(&m,frozen::realize_functional(frozen::FunctionalSignature{linked:s.linked,presentation_stable:s.presentation_stable,report_stable:s.report_stable,calibrated:s.calibrated,blind_spot:s.blind_spot}));match m{Ok(m)=>{assert!(allowed);assert!(m.presentation().len()<=3);assert_eq!(functional_oracle(&m),flags5(s));},Err(e)=>{assert!(!allowed);assert_eq!(e,ClassificationError::ImpossibleSignature);}}}
 for n in 1usize..=3{let maps=n.pow(n as u32);for a in 0..maps{for b in 0..maps{for c in 0..maps{let q=digits(a,n);let r=digits(b,n);let t=digits(c,n);for calibrated in [true,false]{let mut target=r.clone();if !calibrated{target[0]+=1}let m=FiniteFunctionalModel::new(q.clone(),r.clone(),t.clone(),target.clone()).unwrap();same(&m,frozen::FiniteFunctionalModel::new(q.clone(),r.clone(),t.clone(),target).unwrap());let oracle=functional_oracle(&m);assert_eq!(flags5(m.signature()),oracle);assert!(m.signature().is_realizable());let expected=if oracle[0]{Some((0..n).map(|i|(q[i],r[i])).collect::<BTreeMap<_,_>>())}else{None};assert_eq!(m.report_factor(),expected);assert_eq!(m.presentation().as_ptr(),m.presentation.as_ptr());assert_eq!(m.report().as_ptr(),m.report.as_ptr());assert_eq!(m.context().as_ptr(),m.context.as_ptr());assert_eq!(m.target().as_ptr(),m.target.as_ptr());}}}}}
}
fn premises(mut code:usize,n:usize)->Vec<PropertyLiteral>{let mut out=vec![];for i in 0..n{let digit=code%3;code/=3;if digit>0{out.push(PropertyLiteral{index:i,value:digit==2});}}out}
fn first_model<const N:usize>(models:&[(usize,[bool;N])],p:&[PropertyLiteral],c:PropertyLiteral)->Option<usize>{models.iter().find(|(_,f)|f[c.index]!=c.value && p.iter().all(|l|f[l.index]==l.value)).map(|(bits,_)|*bits)}
#[test]fn complete_implication_truth_tables_and_first_countermodels(){let retention:Vec<_>=(0..64).filter_map(|b|realize_retention(sig6(b)).ok().map(|m|(b,retention_oracle(&m)))).collect();let functional:Vec<_>=(0..32).filter_map(|b|realize_functional(sig5(b)).ok().map(|m|(b,functional_oracle(&m)))).collect();assert_eq!(functional.len(),20);
 for code in 0..729{let p=premises(code,6);for index in 0..6{for value in [false,true]{let c=PropertyLiteral{index,value};let expected=first_model(&retention,&p,c);let answer=retention_implication_countermodel(&p,c).unwrap();match(expected,answer){(None,None)=>{},(Some(bits),Some(m))=>{assert_eq!(retention_oracle(&m),flags6(sig6(bits)));},_=>panic!("retention truth table mismatch")}}}}
 for code in 0..243{let p=premises(code,5);for index in 0..5{for value in [false,true]{let c=PropertyLiteral{index,value};let expected=first_model(&functional,&p,c);let answer=functional_implication_countermodel(&p,c).unwrap();match(expected,answer){(None,None)=>{},(Some(bits),Some(m))=>{assert_eq!(functional_oracle(&m),flags5(sig5(bits)));},_=>panic!("functional truth table mismatch")}}}}
 for c in [PropertyLiteral{index:0,value:false},PropertyLiteral{index:0,value:true}]{let p=[PropertyLiteral{index:0,value:true},PropertyLiteral{index:0,value:false}];assert!(retention_implication_countermodel(&p,c).unwrap().is_none());assert!(functional_implication_countermodel(&p,c).unwrap().is_none());}
}
#[test]fn malformed_models_indices_zero_inputs_and_sparse_labels(){
 for(raw,r,t,inputs)in[(vec![],vec![],vec![],0),(vec![0],vec![],vec![vec![]],0),(vec![0,0],vec![0,1],vec![vec![0],vec![1]],1),(vec![0],vec![0],vec![],0),(vec![0],vec![0],vec![vec![]],1),(vec![0],vec![0],vec![vec![1]],1)]{assert_eq!(FiniteRetentionModel::new(raw,r,t,inputs),Err(ClassificationError::InvalidModel));}
 for(q,s,t,b)in[(vec![],vec![],vec![],vec![]),(vec![0],vec![],vec![0],vec![0]),(vec![0],vec![0],vec![],vec![0]),(vec![0],vec![0],vec![0],vec![]),(vec![0],vec![0],vec![1],vec![0])]{assert_eq!(FiniteFunctionalModel::new(q,s,t,b),Err(ClassificationError::InvalidModel));}
 for index in [6,usize::MAX]{assert_eq!(retention_implication_countermodel(&[],PropertyLiteral{index,value:true}),Err(ClassificationError::InvalidModel));assert_eq!(retention_implication_countermodel(&[PropertyLiteral{index,value:true}],PropertyLiteral{index:0,value:true}),Err(ClassificationError::InvalidModel));}for index in [5,usize::MAX]{assert_eq!(functional_implication_countermodel(&[],PropertyLiteral{index,value:true}),Err(ClassificationError::InvalidModel));assert_eq!(functional_implication_countermodel(&[PropertyLiteral{index,value:true}],PropertyLiteral{index:0,value:true}),Err(ClassificationError::InvalidModel));}
 check_retention(vec![usize::MAX,0],vec![usize::MAX,usize::MAX],vec![vec![1],vec![0]],1);let m=FiniteFunctionalModel::new(vec![usize::MAX,0],vec![99,42],vec![1,1],vec![99,42]).unwrap();assert_eq!(functional_oracle(&m),flags5(m.signature()));
}

'''

def challenge(subject):
    return '\n#[cfg(test)]mod independent_classification_tests{use super::*;\n'+FROZEN+TESTS+'\n}\n'
