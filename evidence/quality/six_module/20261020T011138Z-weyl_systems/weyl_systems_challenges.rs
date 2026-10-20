#[cfg(test)]
mod boundary_review {
    use super::*;
    fn oracle(u: PhasePoint, v: PhasePoint, d: usize) -> usize {
        ((u.q as i128*v.p as i128-u.p as i128*v.q as i128).rem_euclid(d as i128)) as usize
    }
    #[test]
    fn exhaustive_small_ring_and_all_modulus_boundaries() {
        for d in 2..=11 {
            let system=DiscreteWeylSystem::new(d).unwrap();
            for a in 0..d*d {for b in 0..d*d {
                let u=PhasePoint::new(a/d,a%d);let v=PhasePoint::new(b/d,b%d);
                assert_eq!(system.symplectic_form(u,v).unwrap(),oracle(u,v,d));
                assert_eq!(system.commutes(u,v).unwrap(),oracle(u,v,d)==0);
                assert_eq!(system.add(u,v).unwrap(),PhasePoint::new((a/d+b/d)%d,(a%d+b%d)%d));
            }}
        }
        for d in 2..=256 {
            let system=DiscreteWeylSystem::new(d).unwrap();assert_eq!(system.dim(),d);
            for code in 0..128 {
                let u=PhasePoint::new((code*17+1)%d,(code*13+d-1)%d);
                let v=PhasePoint::new((code*11+d-1)%d,(code*7+3)%d);
                assert_eq!(system.symplectic_form(u,v).unwrap(),oracle(u,v,d));
                let sum=system.add(u,v).unwrap();assert_eq!((sum.q,sum.p),((u.q+v.q)%d,(u.p+v.p)%d));
                assert_eq!(system.symplectic_form(u,u).unwrap(),0);
            }
        }
    }
    #[test]
    fn every_prime_partition_against_inverse_classification() {
        for d in 2..=256 {
            let prime=!(2..=16).any(|factor| factor<d && d%factor==0);
            let system=DiscreteWeylSystem::new(d).unwrap();
            if !prime {
                assert_eq!(system.isotropic_rays(),Err(WeylSystemError::NotPrime(d)));
                assert_eq!(certify_ray_partition(d),Err(WeylSystemError::NotPrime(d)));continue;
            }
            let inverses:Vec<usize>=(0..d).map(|x|(1..d).find(|y|x*y%d==1).unwrap_or(0)).collect();
            let mut expected=vec![BTreeSet::new();d+1];
            for x in 0..d {for y in 0..d {
                if x==0 && y==0 {for set in &mut expected {set.insert(PhasePoint::new(0,0));}}
                else {let index=if x==0 {0} else {1+y*inverses[x]%d};expected[index].insert(PhasePoint::new(x,y));}
            }}
            let rays=system.isotropic_rays().unwrap();assert_eq!(rays.len(),d+1);let mut seen=BTreeSet::new();
            for (ray,set) in rays.iter().zip(expected) {
                assert_eq!(ray,&set.into_iter().collect::<Vec<_>>());assert_eq!(ray.len(),d);
                let anchor=ray[1];
                for &point in ray {
                    assert!(system.commutes(point,anchor).unwrap());
                    if point!=PhasePoint::new(0,0) {assert!(seen.insert(point));}
                }
            }
            assert_eq!(seen.len(),d*d-1);assert_eq!(certify_ray_partition(d),Ok((d+1,d*d-1)));
        }
    }
    #[test]
    fn raw_record_and_coordinate_failure_order() {
        assert_eq!(PhasePoint::new(usize::MAX,usize::MAX),PhasePoint{q:usize::MAX,p:usize::MAX});
        for d in [2,3,256] {
            let system=DiscreteWeylSystem::new(d).unwrap();let zero=PhasePoint::new(0,0);
            for point in [PhasePoint::new(d,0),PhasePoint::new(0,d),PhasePoint::new(usize::MAX,usize::MAX)] {
                let error=WeylSystemError::CoordinateOutOfBounds(point.q,point.p,d);
                assert_eq!(system.validate_point(point),Err(error.clone()));
                assert_eq!(system.symplectic_form(point,zero),Err(error.clone()));
                assert_eq!(system.symplectic_form(zero,point),Err(error.clone()));
                assert_eq!(system.add(point,zero),Err(error.clone()));assert_eq!(system.add(zero,point),Err(error));
            }
            assert_eq!(system.add(PhasePoint::new(d,1),PhasePoint::new(1,d)),Err(WeylSystemError::CoordinateOutOfBounds(d,1,d)));
        }
        for d in [0,1,257,usize::MAX] {
            assert_eq!(DiscreteWeylSystem::new(d),Err(WeylSystemError::InvalidDimension{dim:d,min:2,max:256}));
            assert!(certify_ray_partition(d).is_err());
        }
    }
    #[test]
    fn counting_is_union_without_origin_and_diagnostics() {
        let zero=PhasePoint::new(0,0);let a=PhasePoint::new(1,0);let b=PhasePoint::new(0,1);
        assert_eq!(count_nonzero(&[vec![zero,a,a],vec![a,b,zero]]),2);assert_eq!(count_nonzero(&[]),0);
        let mut seen=BTreeSet::new();collect_nonzero(&mut seen,&[zero,a,a]);assert_eq!(seen,BTreeSet::from([a]));
        let error=WeylSystemError::PartitionFailed{prime:5,rays:6,nonzero:23};
        assert_eq!(error.violated_invariant(),"nonzero phase points partition into isotropic rays");
        assert_eq!(error.measured_parameters(),vec![("prime","5".to_owned()),("rays","6".to_owned()),("nonzero","23".to_owned())]);
    }
}
