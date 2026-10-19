//! Exact compatible binary pair-data separator construction. AuthorityEffect: None.
//! Pair order 00,01,10,11; cells --,-+,+-,++; mask bits A0,A1,B0,B1.
//! Native witnesses are not a general Lean proof of rational conditional gluing.
use num_integer::Integer;
use num_rational::BigRational as Q;
use num_traits::{One, Signed, Zero};

pub type PairData = [[Q; 4]; 4];
pub const FACET_MASKS: [u8;8] = [1,2,4,7,8,11,13,14];

#[derive(Debug,Clone,PartialEq,Eq,thiserror::Error)]
pub enum ExtensionError {
    #[error("noncanonical or negative probability, or nonunit mass")]
    InvalidLaw,
    #[error("incompatible one-party pair marginals")]
    IncompatibleMarginals,
    #[error("separator outside the setting interval or invalid setting")]
    InvalidSeparator,
    #[error("triple separator marginals differ")]
    SeparatorMismatch,
    #[error("joint witness does not project to observed pair data")]
    ProjectionMismatch,
    #[error("empty interval without a CHSH obstruction")]
    InconsistentReduction,
}

fn law(values:&[Q])->Result<(),ExtensionError> {
    for q in values {
        if !q.denom().is_positive() || !q.numer().gcd(q.denom()).is_one() || q.is_negative() {return Err(ExtensionError::InvalidLaw);}
    }
    if values.iter().cloned().sum::<Q>()!=Q::one(){return Err(ExtensionError::InvalidLaw);}
    Ok(())
}

pub fn validate_pairs(p:&PairData)->Result<(),ExtensionError> {
    for row in p {law(row)?;}
    for x in 0..2 {if &p[2*x][2]+&p[2*x][3]!=&p[2*x+1][2]+&p[2*x+1][3] {return Err(ExtensionError::IncompatibleMarginals);}}
    for y in 0..2 {if &p[y][1]+&p[y][3]!=&p[2+y][1]+&p[2+y][3] {return Err(ExtensionError::IncompatibleMarginals);}}
    Ok(())
}

pub fn project_joint(weights:&[Q;16])->Result<PairData,ExtensionError> {
    law(weights)?;
    let mut result:PairData=std::array::from_fn(|_|std::array::from_fn(|_|Q::zero()));
    for (m,p) in weights.iter().enumerate() {for x in 0..2 {for y in 0..2 {
        result[2*x+y][2*((m>>x)&1)+((m>>(2+y))&1)]+=p;
    }}}
    Ok(result)
}

pub fn verify_extension(p:&PairData,weights:&[Q;16])->Result<(),ExtensionError> {
    validate_pairs(p)?;
    if project_joint(weights)?!=*p {return Err(ExtensionError::ProjectionMismatch);}
    Ok(())
}

pub fn chsh_facets(p:&PairData)->Result<[Q;8],ExtensionError> {
    validate_pairs(p)?;
    let e:[Q;4]=std::array::from_fn(|j|&p[j][0]-&p[j][1]-&p[j][2]+&p[j][3]);
    Ok(std::array::from_fn(|i|(0..4).map(|j|if FACET_MASKS[i]&(1<<j)==0 {e[j].clone()} else {-&e[j]}).sum()))
}

fn caps(p:&PairData,y:usize,b:usize)->(Q,Q) {
    let u=&p[y][2+b];let v=&p[2+y][2+b];let w=&p[y][b]+u;
    ((u+v-w).max(Q::zero()),u.clone().min(v.clone()))
}

#[derive(Debug,Clone,PartialEq,Eq)]
pub struct SeparatorAnalysis {
    pub lower:[Q;2],pub upper:[Q;2],pub common_lower:Q,pub common_upper:Q,pub facets:[Q;8],
}

pub fn separator_intervals(p:&PairData)->Result<SeparatorAnalysis,ExtensionError> {
    validate_pairs(p)?;
    let lower:[Q;2]=std::array::from_fn(|y|caps(p,y,0).0+caps(p,y,1).0);
    let upper:[Q;2]=std::array::from_fn(|y|caps(p,y,0).1+caps(p,y,1).1);
    Ok(SeparatorAnalysis {common_lower:lower[0].clone().max(lower[1].clone()),common_upper:upper[0].clone().min(upper[1].clone()),
        lower,upper,facets:chsh_facets(p)?})
}

pub fn split_triple(p:&PairData,y:usize,r:&Q)->Result<[Q;8],ExtensionError> {
    validate_pairs(p)?;
    if y>1 || !r.denom().is_positive() || !r.numer().gcd(r.denom()).is_one() {return Err(ExtensionError::InvalidSeparator);}
    let c0=caps(p,y,0);let c1=caps(p,y,1);
    if r<&(&c0.0+&c1.0) || r>&(&c0.1+&c1.1) {return Err(ExtensionError::InvalidSeparator);}
    let t0=c0.0.max(r-&c1.1);let ts=[t0.clone(),r-t0];
    let mut triple:[Q;8]=std::array::from_fn(|_|Q::zero());
    for b in 0..2 {let u=&p[y][2+b];let v=&p[2+y][2+b];let w=&p[y][b]+u;let t=&ts[b];
        triple[4*b]=w-u-v+t;triple[4*b+1]=u-t;triple[4*b+2]=v-t;triple[4*b+3]=t.clone();}
    law(&triple)?;Ok(triple)
}

pub fn conditional_glue(left:&[Q;8],right:&[Q;8])->Result<[Q;16],ExtensionError> {
    law(left)?;law(right)?;
    let q:[Q;4]=std::array::from_fn(|s|&left[s]+&left[s+4]);
    if (0..4).any(|s|q[s]!=&right[s]+&right[s+4]) {return Err(ExtensionError::SeparatorMismatch);}
    Ok(std::array::from_fn(|m|if q[m&3].is_zero() {Q::zero()} else {&left[(m&3)+4*((m>>2)&1)]*&right[(m&3)+4*((m>>3)&1)]/&q[m&3]}))
}

#[derive(Debug,Clone,PartialEq,Eq)]
pub struct ExtensionDecision {
    pub analysis:SeparatorAnalysis,pub separator:Option<Q>,pub triples:Option<[[Q;8];2]>,
    pub weights:Option<[Q;16]>,pub violating_mask:Option<u8>,
}

pub fn construct_extension(p:&PairData)->Result<ExtensionDecision,ExtensionError> {
    let analysis=separator_intervals(p)?;
    if analysis.common_lower>analysis.common_upper {
        let two=Q::from_integer(2.into());
        let mask=FACET_MASKS.iter().zip(&analysis.facets).find(|(_,v)|**v>two).map(|(m,_)|*m).ok_or(ExtensionError::InconsistentReduction)?;
        return Ok(ExtensionDecision {analysis,separator:None,triples:None,weights:None,violating_mask:Some(mask)});
    }
    let r=analysis.common_lower.clone();let triples=[split_triple(p,0,&r)?,split_triple(p,1,&r)?];
    let weights=conditional_glue(&triples[0],&triples[1])?;verify_extension(p,&weights)?;
    Ok(ExtensionDecision {analysis,separator:Some(r),triples:Some(triples),weights:Some(weights),violating_mask:None})
}
