#[cfg(test)]
mod ring_review {
    use super::*;
    use omega_number_theory::rational::rq;

    fn oracle(n:&[u64],r:usize,commutative:bool)->Option<RingDefect> {
        let at=|a,b,c|n[(a*r+b)*r+c];
        for a in 0..r {for c in 0..r {let e=u64::from(a==c);if at(0,a,c)!=e || at(a,0,c)!=e {return Some(RingDefect::Unit{label:a});}}}
        if commutative {for a in 0..r {for b in a+1..r {if (0..r).any(|c|at(a,b,c)!=at(b,a,c)) {return Some(RingDefect::Commutativity{left:a,right:b});}}}}
        for a in 0..r {for b in 0..r {for c in 0..r {for d in 0..r {
            let left:u128=(0..r).map(|e|at(a,b,e) as u128*at(e,c,d) as u128).sum();
            let right:u128=(0..r).map(|e|at(b,c,e) as u128*at(a,e,d) as u128).sum();
            if left!=right {return Some(RingDefect::Associativity{labels:(a,b,c),outcome:d,left,right});}
        }}}}
        let mut dual=vec![];
        for a in 0..r {let hits:Vec<_>=(0..r).filter(|&b|at(a,b,0)!=0).collect();if hits.len()!=1 || at(a,hits[0],0)!=1 {return Some(RingDefect::Duality{label:a});}dual.push(hits[0]);}
        for a in 0..r {if dual[dual[a]]!=a {return Some(RingDefect::Duality{label:a});}}
        for a in 0..r {for b in 0..r {for c in 0..r {if at(a,b,c)!=at(dual[a],c,b) || at(a,b,c)!=at(c,dual[b],a) {return Some(RingDefect::Reciprocity{labels:(a,b,c)});}}}}
        None
    }
    #[test]
    fn exhaustive_small_tables_and_isolated_ising_defects() {
        for mut code in 0..3usize.pow(8) {
            let n:Vec<u64>=(0..8).map(|_|{let x=(code%3) as u64;code/=3;x}).collect();
            let table=FusionTable::new(2,n.clone()).unwrap();
            assert_eq!(table.first_defect(),oracle(&n,2,true));
            let expected=oracle(&n,2,false);
            assert_eq!(table.first_defect_allowing_noncommutative(),expected);
            assert_eq!(table.validate().is_ok(),expected.is_none());
        }
        let original=FusionTable::ising();
        for index in 0..27 {for value in 0..=2 {let mut n=original.n.clone();n[index]=value;let table=FusionTable::new(3,n.clone()).unwrap();assert_eq!(table.first_defect(),oracle(&n,3,true));assert_eq!(table.validate().is_ok(),oracle(&n,3,false).is_none());}}
        assert!(FusionTable::new(MAX_RANK,vec![0;MAX_RANK.pow(3)]).is_ok());
        assert!(matches!(FusionTable::new(0,vec![]),Err(FusionError::RankOutOfRange{..})));
        assert!(matches!(FusionTable::new(MAX_RANK+1,vec![]),Err(FusionError::RankOutOfRange{..})));
        assert!(matches!(FusionTable::new(3,vec![0;26]),Err(FusionError::TableShape{..})));
        assert!(matches!(FusionTable::with_names(2,vec![],vec![0;8]),Err(FusionError::ListLength{..})));
        assert!(FusionTable::ising().first_reciprocity_defect(&[0,2,1]).is_some());
        let huge=FusionTable::new(2,vec![u64::MAX;8]).unwrap();
        assert_eq!(huge.associativity_defect_at(0,0,0,0),Some(RingDefect::Overflow{labels:(0,0,0)}));
    }
    fn s3()->(FusionRing,Vec<[usize;3]>) {
        let permutations=vec![[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]];
        let mut n=vec![0u64;216];
        for (a,p) in permutations.iter().enumerate() {for (b,q) in permutations.iter().enumerate() {let product=[p[q[0]],p[q[1]],p[q[2]]];let c=permutations.iter().position(|x|*x==product).unwrap();n[(a*6+b)*6+c]=1;}}
        (FusionTable::new(6,n).unwrap().validate().unwrap(),permutations)
    }
    #[test]
    fn actual_noncommutative_group_ring_and_owned_immutable_state() {
        let (ring,permutations)=s3();assert!(!ring.is_commutative());assert!(ring.is_pointed());assert!(ring.is_multiplicity_free());assert!(matches!(ring.table().first_defect(),Some(RingDefect::Commutativity{..})));
        assert_eq!(ring.unit(),0);assert_eq!(ring.rank(),6);assert_eq!(ring.names().len(),6);
        for a in 0..6 {assert_eq!(ring.fuse(a,ring.dual(a).unwrap()).unwrap(),vec![0]);for b in 0..6 {
            let p=permutations[a];let q=permutations[b];let product=[p[q[0]],p[q[1]],p[q[2]]];let c=permutations.iter().position(|x|*x==product).unwrap();assert_eq!(ring.fuse(a,b).unwrap(),vec![c]);
            let counts=ring.fusion_path_counts(&[a,b]).unwrap();assert_eq!(counts[c],BigUint::one());assert_eq!(counts.iter().cloned().sum::<BigUint>(),BigUint::one());
        }}
        let original=ring.clone();let mut candidate=ring.table().clone();candidate.n[0]=0;assert!(candidate.validate().is_err());assert_eq!(original,ring);
    }
    fn explicit_paths(table:&FusionTable,word:&[usize])->Vec<BigUint> {
        let mut endpoints=vec![0usize];
        for &w in word {let mut next=vec![];for a in endpoints {for c in 0..table.rank {for _ in 0..table.n[(a*table.rank+w)*table.rank+c] {next.push(c);}}}endpoints=next;}
        (0..table.rank).map(|c|BigUint::from(endpoints.iter().filter(|a|**a==c).count())).collect()
    }
    #[test]
    fn path_enumeration_group_coordinates_and_admission() {
        for ring in [FusionRing::ising().unwrap(),FusionRing::fibonacci().unwrap(),FusionRing::rep_s3().unwrap()] {
            for length in 0..=5 {for mut code in 0..ring.rank().pow(length) {let word:Vec<_>=(0..length).map(|_|{let x=code%ring.rank();code/=ring.rank();x}).collect();assert_eq!(ring.fusion_path_counts(&word).unwrap(),explicit_paths(ring.table(),&word));}}
        }
        for moduli in [vec![],vec![2],vec![3],vec![2,3],vec![2,2,2],vec![2,2,2,2,2],vec![32]] {
            let group=AbelianGroup::new(&moduli).unwrap();assert_eq!(group.moduli(),&moduli);
            for a in 0..group.order() {let digits=group.digits(a).unwrap();assert_eq!(group.label(&digits),Ok(a));let minus=group.negate(a).unwrap();assert_eq!(group.add(a,minus),Ok(0));for b in 0..group.order() {let bd=group.digits(b).unwrap();let expected:Vec<_>=digits.iter().zip(bd).zip(&moduli).map(|((&x,y),&m)|(x+y)%m).collect();assert_eq!(group.add(a,b).unwrap(),group.label(&expected).unwrap());}}
            assert!(group.add(group.order(),0).is_err());assert!(group.negate(group.order()).is_err());
        }
        let raw=FusionTable::new(1,vec![u64::MAX]).unwrap();assert_eq!(raw.path_growth(0),64);assert!(matches!(raw.admit_path_work(std::iter::repeat(0).take(MAX_FUSION_WORD)),Err(FusionError::Budget{what:"fusion path scalar-bit work",..})));
        assert!(matches!(raw.charge_counts(0,MAX_FUSION_WORD),Err(FusionError::Budget{what:"fusion path scalar-bit work",..})));
        assert_eq!(raw.charge_counts(0,2).unwrap(),vec![BigUint::from(u64::MAX).pow(2)]);
        assert!(raw.charge_counts_u64(0,2).is_err());
        let accepted=(1..=MAX_FUSION_WORD).take_while(|&n|{let n=n as u128;65*n+64*n*(n-1)/2<=MAX_FUSION_PATH_WORK}).last().unwrap();
        assert!(raw.admit_path_work(std::iter::repeat(0).take(accepted)).is_ok());
        assert!(raw.admit_path_work(std::iter::repeat(0).take(accepted+1)).is_err());
        assert_eq!(FusionTable::new(1,vec![1]).unwrap().charge_counts(0,MAX_FUSION_WORD).unwrap(),vec![BigUint::one()]);
        assert_eq!(raw.charge_counts(0,0).unwrap(),vec![BigUint::one()]);
        assert!(matches!(raw.charge_counts(1,usize::MAX),Err(FusionError::Label{..})));
        let ring=FusionRing::ising().unwrap();
        assert!(ring.multiplicity(ring.rank(),0,0).is_err());assert!(ring.fuse(ring.rank(),0).is_err());assert!(ring.dual(ring.rank()).is_err());assert!(ring.fusion_matrix(ring.rank()).is_err());
        assert!(matches!(ring.fusion_path_counts(&vec![99;MAX_FUSION_WORD+1]),Err(FusionError::Budget{what:"fusion word length",..})));
        assert!(matches!(ring.fusion_path_counts(&[0,99]),Err(FusionError::Label{label:99,..})));
        assert!(ring.fusion_paths(&[0],99).is_err());
        assert_eq!(FusionTable::new(1,vec![0]).unwrap().path_growth(0),0);
        assert!(FusionTable::new(1,vec![1]).unwrap().admit_path_work(std::iter::repeat(0).take(MAX_FUSION_WORD)).is_ok());
    }
    fn determinant_polynomial(matrix:&[Vec<BigInt>])->Vec<BigInt> {
        fn permutations(prefix:Vec<usize>,remaining:Vec<usize>,out:&mut Vec<Vec<usize>>) {if remaining.is_empty(){out.push(prefix);return;}for i in 0..remaining.len(){let mut next=prefix.clone();next.push(remaining[i]);let mut rest=remaining.clone();rest.remove(i);permutations(next,rest,out);}}
        let r=matrix.len();let mut ps=vec![];permutations(vec![],(0..r).collect(),&mut ps);let mut total=vec![BigInt::zero();r+1];
        for p in ps {let inversions=(0..r).map(|i|(i+1..r).filter(|&j|p[i]>p[j]).count()).sum::<usize>();let mut product=vec![BigInt::from(if inversions%2==0 {1}else{-1})];for i in 0..r {let mut next=vec![BigInt::zero();product.len()+1];for (degree,c) in product.iter().enumerate(){next[degree]-=c*&matrix[i][p[i]];if i==p[i]{next[degree+1]+=c;}}product=next;}for (i,c) in product.into_iter().enumerate(){total[i]+=c;}}
        total
    }
    #[test]
    fn characteristic_polynomials_and_exact_spectral_controls() {
        let (s3,_)=s3();
        for ring in [FusionRing::ising().unwrap(),FusionRing::fibonacci().unwrap(),FusionRing::rep_s3().unwrap(),s3] {
            for a in 0..ring.rank() {let expected:Vec<Vec<BigInt>>=(0..ring.rank()).map(|b|(0..ring.rank()).map(|c|BigInt::from(ring.table().n[(a*ring.rank()+b)*ring.rank()+c])).collect()).collect();assert_eq!(ring.fusion_matrix(a).unwrap(),expected);assert_eq!(ring.characteristic_polynomial(a).unwrap(),determinant_polynomial(&expected));}
        }
        assert_eq!(FusionRing::toric_code().unwrap().global_dimension_squared().unwrap(),RealAlgebraic::Rational(rq(4,1)));
        assert_eq!(FusionRing::ising().unwrap().global_dimension_squared().unwrap(),RealAlgebraic::Rational(rq(4,1)));
        assert_eq!(FusionRing::rep_s3().unwrap().global_dimension_squared().unwrap(),RealAlgebraic::Rational(rq(6,1)));
        assert_eq!(FusionRing::semion().unwrap().frobenius_perron_dimension(1).unwrap(),RealAlgebraic::Rational(rq(1,1)));
        assert!(FusionRing::integral_coefficients(vec![rq(1,2)]).is_err());assert_eq!(FusionRing::integral_coefficients(vec![rq(-2,1),rq(0,1)]).unwrap(),vec![BigInt::from(-2),BigInt::zero()]);
    }
    #[test]
    fn verlinde_character_oracle_errors_and_su2_rules() {
        let ring=FusionRing::toric_code().unwrap();let mut values:Vec<Vec<_>>=(0..4usize).map(|a|(0..4usize).map(|x|rq(if (a&x).count_ones()%2==0 {1}else{-1},1)).collect()).collect();let s=matrix::from_rows(values.clone()).unwrap();assert!(ring.verlinde_defects(&s,&rq(4,1)).unwrap().is_empty());
        values[1][1]=rq(2,1);let broken=matrix::from_rows(values.clone()).unwrap();let mut expected=vec![];
        for a in 0..4 {for b in 0..4 {for c in 0..4 {let sum:i128=(0..4).map(|x|values[a][x].to_integer().to_i128().unwrap()*values[b][x].to_integer().to_i128().unwrap()*values[c][x].to_integer().to_i128().unwrap()).sum();if sum!=4*i128::from(u8::from(c==a^b)){expected.push([a,b,c]);}}}}
        assert_eq!(ring.verlinde_defects(&broken,&rq(4,1)).unwrap(),expected);
        {
            use omega_number_theory::cyclotomic::Cyc12;
            let group=FusionRing::z_n(3).unwrap();
            let fourier=matrix::from_rows((0..3).map(|a|(0..3).map(|x|crate::scalar::root_of_unity::<Cyc12>(3,(a*x) as i64).unwrap()).collect()).collect()).unwrap();
            let dimension=omega_number_theory::scalar::from_i64::<Cyc12>(3);
            assert!(group.verlinde_defects(&fourier,&dimension).unwrap().is_empty());
        }
        let wrong=matrix::zeros(3,3).unwrap();assert!(matches!(ring.verlinde_defects(&wrong,&rq(0,1)),Err(FusionError::Shape{..})));
        assert!(ring.verlinde_defects(&s,&rq(0,1)).is_err());let mut zero=values;zero[0][0]=rq(0,1);assert!(ring.verlinde_defects(&matrix::from_rows(zero).unwrap(),&rq(4,1)).is_err());
        let huge=FusionTable::from_array([[[1,0],[0,1]],[[0,1],[1,u64::MAX]]]).unwrap().validate().unwrap();let ones=matrix::from_rows(vec![vec![rq(1,1);2];2]).unwrap();assert!(matches!(huge.verlinde_defects(&ones,&rq(1,1)),Err(FusionError::Overflow{context:"embedding a fusion coefficient"})));
        for k in 1..=7 {let ring=FusionRing::su2_level(k).unwrap();for i in 0..=k {for j in 0..=k {for l in 0..=k {let allowed=i+j>=l && i+l>=j && j+l>=i && i+j+l<=2*k && (i+j+l)%2==0;assert_eq!(ring.multiplicity(i,j,l).unwrap(),u64::from(allowed));}}}}
    }
}
