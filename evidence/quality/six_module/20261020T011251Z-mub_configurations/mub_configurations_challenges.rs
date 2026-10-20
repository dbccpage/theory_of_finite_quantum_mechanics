
#[cfg(test)]
mod boundary_review {
 use super::*;
 fn independent_valid(d:usize,bundles:&[Vec<PhasePoint>])->bool {
  if !(2..=256).contains(&d) || bundles.len()>d+1 {return false;} let mut points=vec![];
  for bundle in bundles {
   if bundle.len()!=d-1 {return false;}
   for point in bundle {if point.q>=d || point.p>=d || (point.q==0 && point.p==0) || points.contains(point) {return false;} points.push(*point);}
   for u in bundle {for v in bundle {let determinant=u.q as i128*v.p as i128-u.p as i128*v.q as i128;if determinant.rem_euclid(d as i128)!=0 {return false;}}}
  } true
 }
 #[test]
 fn singleton_coordinates_and_overflow_refuse() {
  for point in [PhasePoint::new(2,0),PhasePoint::new(0,2),PhasePoint::new(usize::MAX,1)] {
   assert_eq!(MubOperatorConfiguration::new(2,vec![vec![point]]),Err(MubConfigError::Weyl(WeylSystemError::CoordinateOutOfBounds(point.q,point.p,2))));
  }
  assert!(matches!(MubOperatorConfiguration::new(usize::MAX,vec![]),Err(MubConfigError::Weyl(WeylSystemError::InvalidDimension {..}))));
  assert_eq!(mub_theoretical_upper_bound(usize::MAX),Err(MubConfigError::UpperBoundOverflow {dim:usize::MAX}));
  assert_eq!(mub_theoretical_upper_bound(usize::MAX-1),Ok(usize::MAX));
  for d in [0,1,2,6,256,257] {assert_eq!(mub_theoretical_upper_bound(d),Ok(d+1));}
  assert_eq!(MubConfigError::UpperBoundOverflow {dim:usize::MAX}.violated_invariant(),"dimension plus one is representable");
 }
 #[test]
 fn exhaustive_small_bundle_candidate_oracle() {
  for d in [2usize,3] {
   let points:Vec<_>=(0..d*d).map(|x|PhasePoint::new(x/d,x%d)).collect();let mut candidates=vec![vec![]];
   for &a in &points {if d==2 {candidates.push(vec![a]);} else {for &b in &points {candidates.push(vec![a,b]);}}}
   for a in &candidates {for b in &candidates {for bundles in [vec![a.clone()],vec![a.clone(),b.clone()]] {
    let original=bundles.clone();let good=independent_valid(d,&original);let result=MubOperatorConfiguration::new(d,bundles);
    assert_eq!(result.is_ok(),good,"d={d} bundles={original:?}");
    if let Ok(config)=result {assert_eq!(config.dim(),d);assert_eq!(config.num_bases(),original.len());assert_eq!(config.bundles(),&original);assert_eq!(config.is_complete(),original.len()==d+1);}
   }}}
  }
 }
 #[test]
 fn prime_bundles_composition_and_largest_ring() {
  for p in [2,3,5,7,11,13,17,31,61,127,251] {
   let config=MubOperatorConfiguration::canonical_prime(p).unwrap();assert_eq!((config.dim(),config.num_bases(),config.is_complete()),(p,p+1,true));let mut seen=BTreeSet::new();
   for bundle in config.bundles() {assert_eq!(bundle.len(),p-1);assert!(bundle.iter().all(|x|x.q<p && x.p<p && *x!=PhasePoint::new(0,0)));let anchor=bundle[0];
    for &point in bundle {assert!(seen.insert(point));assert_eq!((point.q as i128*anchor.p as i128-point.p as i128*anchor.q as i128).rem_euclid(p as i128),0);}
   }
   assert_eq!(seen.len(),p*p-1);let copied=config.clone();drop(config);assert_eq!(copied.num_bases(),p+1);
  }
  let vertical:Vec<_>=(1..256).map(|p|PhasePoint::new(0,p)).collect();assert!(MubOperatorConfiguration::new(256,vec![vertical]).is_ok());assert!(MubOperatorConfiguration::new(256,vec![]).is_ok());
  for d in [4,6,256] {assert!(matches!(MubOperatorConfiguration::canonical_prime(d),Err(MubConfigError::Weyl(WeylSystemError::NotPrime(_)))));}
 }
 #[test]
 fn failure_order_and_owned_boundary() {
  assert!(matches!(MubOperatorConfiguration::new(1,vec![vec![];5]),Err(MubConfigError::InvalidDimension {..})));
  assert!(matches!(MubOperatorConfiguration::new(257,vec![vec![];259]),Err(MubConfigError::Weyl(WeylSystemError::InvalidDimension {..}))));
  assert!(matches!(MubOperatorConfiguration::new(2,vec![vec![];4]),Err(MubConfigError::TooManyBundles {found:4,bound:3,dim:2})));
  assert!(matches!(MubOperatorConfiguration::new(3,vec![vec![PhasePoint::new(99,0)]]),Err(MubConfigError::InvalidBundleSize {index:0,found:1,expected:2})));
  assert!(matches!(MubOperatorConfiguration::new(3,vec![vec![PhasePoint::new(0,0),PhasePoint::new(99,0)]]),Err(MubConfigError::ContainsIdentity)));
  let point=PhasePoint::new(0,1);assert_eq!(MubOperatorConfiguration::new(3,vec![vec![point,point]]),Err(MubConfigError::NonDisjointBundles {q:0,p:1}));
  assert_eq!(MubOperatorConfiguration::new(3,vec![vec![point,PhasePoint::new(1,0)]]),Err(MubConfigError::NonCommutingBundle {index:0,q0:0,p0:1,q1:1,p1:0}));
  assert!(!MubOperatorConfiguration::new(3,vec![]).unwrap().is_complete());let config=MubOperatorConfiguration::canonical_prime(3).unwrap();let mut forged=config.bundles().to_vec();forged[0][0]=PhasePoint::new(99,0);assert!(MubOperatorConfiguration::new(3,forged).is_err());assert!(config.is_complete());
 }
}
