#[cfg(test)]
mod sum_review {
    use super::*;

    fn independent(values:&[(i64,i64)],total:(i64,i64))->bool {
        if total.1==0 || values.iter().any(|x|x.1==0) {return false;}
        let (mut n,mut d)=(0i128,1i128);
        for &(a,b) in values {n=n*b as i128+a as i128*d;d*=b as i128;}
        if d<0 {n=-n;d=-d;}
        let (mut tn,mut td)=(total.0 as i128,total.1 as i128);
        if td<0 {tn=-tn;td=-td;}
        tn>0 && n*td==tn*d
    }
    fn check(values:&[(i64,i64)],total:(i64,i64)) {
        let ratios:Vec<_>=values.iter().map(|&(n,d)|Ratio::new_raw(n,d)).collect();
        assert_eq!(verify_fusion_global_dimension(&ratios,Ratio::new_raw(total.0,total.1)),independent(values,total),"{values:?} -> {total:?}");
    }
    #[test]
    fn exhaustive_signed_raw_ratio_pairs() {
        let corpus:Vec<_>=(-2..=2).flat_map(|n|[-2,-1,1,2].map(|d|(n,d))).collect();
        for &a in &corpus {for &b in &corpus {for &t in &corpus {check(&[a,b],t);}}}
        for &t in &corpus {check(&[],t);check(&[t],t);}
    }
    #[test]
    fn triples_and_error_domains() {
        let corpus=[(1,2),(-1,2),(1,3),(-2,3),(2,1),(-2,1),(0,1),(1,-1)];
        for &a in &corpus {for &b in &corpus {for &c in &corpus {for &t in &corpus {check(&[a,b,c],t);}}}}
        for t in [(0,1),(-1,1),(1,0),(0,0)] {check(&[],t);check(&[(1,1)],t);}
        check(&[(1,0)],(1,1));check(&[(1,1),(1,0)],(1,1));
        check(&[(1,3),(2,3)],(1,1));
    }
    #[test]
    fn fixed_width_extremes_have_exact_big_integer_lifts() {
        let values=[Ratio::from_integer(i64::MAX),Ratio::from_integer(i64::MAX),Ratio::from_integer(-i64::MAX)];
        assert!(verify_fusion_global_dimension(&values,Ratio::from_integer(i64::MAX)));
        let one=Ratio::new_raw(i64::MIN,i64::MIN);
        assert!(verify_fusion_global_dimension(&[one],Ratio::from_integer(1)));
        let over=Ratio::new_raw(i64::MIN,-1);
        assert!(verify_fusion_global_dimension(&[over],over));
        assert!(verify_fusion_global_dimension(&[over,Ratio::from_integer(i64::MIN),Ratio::from_integer(1)],Ratio::from_integer(1)));
    }
}
